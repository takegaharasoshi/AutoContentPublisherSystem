"""Irodori-TTS で問題文とルールを一度に合成し、WAV を切り分ける。"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any, Callable
import wave

from scripts import narration_gemini


SET_DIR = Path(__file__).resolve().parent.parent
FPS = 30
TIMEOUT_SECONDS = 900
InferRunner = Callable[..., subprocess.CompletedProcess]


class IrodoriError(RuntimeError):
    """Irodori の起動または合成に失敗したことを表す。"""


class IrodoriBudgetError(ValueError):
    """すべてのテイクがナレーション予算を超過したことを表す。"""

    def __init__(
        self, total: float, budget: float, attempted_seconds: list[float]
    ) -> None:
        self.total = total
        self.budget = budget
        self.attempted_seconds = attempted_seconds
        tried = ", ".join(str(value) for value in attempted_seconds)
        super().__init__(
            f"ナレーション予算超過: {total:.3f}s > {budget:.1f}s"
            f"（試行 seconds: {tried}）"
        )


def _ref_wavs(ref_dir: Path) -> tuple[list[Path], list[dict[str, str]]]:
    """名前順の参照 WAV と、キャッシュ照合用のハッシュを返す。"""
    paths = sorted(ref_dir.glob("*.wav"))
    if not paths:
        raise IrodoriError(f"参照 WAV がありません: {ref_dir}")
    refs = []
    for path in paths:
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        refs.append({"name": path.name, "sha256": digest.hexdigest()})
    return paths, refs


def _log_tail(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return "（ログを読めません）"
    return "\n".join(lines[-8:]) or "（ログは空です）"


def _infer(
    text: str,
    model: str,
    refs: list[Path],
    seed: int,
    seconds: float,
    combined: Path,
    runner: InferRunner,
) -> None:
    """Irodori 本体の環境で infer.py を実行し、出力をログへ追記する。"""
    irodori_dir = Path(
        os.environ.get("IRODORI_DIR", "~/tools/Irodori-TTS")
    ).expanduser().resolve()
    command = [
        "uv", "run", "--no-sync", "python", "infer.py",
        "--hf-checkpoint", model,
        "--model-device", "cuda", "--codec-device", "cuda",
        "--model-precision", "bf16", "--codec-precision", "bf16",
        "--seed", str(seed), "--seconds", str(seconds), "--text", text,
        "--ref-wavs", *(str(path.resolve()) for path in refs),
        "--output-wav", str(combined.resolve()),
    ]
    log_path = combined.parent / "irodori.log"
    try:
        with log_path.open("a", encoding="utf-8") as log:
            result = runner(
                command, cwd=irodori_dir, stdout=log,
                stderr=subprocess.STDOUT, timeout=TIMEOUT_SECONDS, check=False,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise IrodoriError(f"Irodori を実行できません: {exc}\n{_log_tail(log_path)}") from exc
    if result.returncode != 0:
        raise IrodoriError(
            f"Irodori が失敗しました（{result.returncode}）:\n{_log_tail(log_path)}"
        )
    if not combined.is_file():
        raise IrodoriError(f"Irodori の出力 WAV がありません: {combined}\n{_log_tail(log_path)}")


def _ensure_pcm16_mono(
    combined: Path, ffmpeg_runner: narration_gemini.FfmpegRunner
) -> None:
    """_split が扱える mono 16bit PCM へ必要な場合だけ変換する。"""
    try:
        with wave.open(str(combined), "rb") as wav:
            if wav.getnchannels() == 1 and wav.getsampwidth() == 2:
                return
    except (OSError, EOFError, wave.Error):
        pass
    converted = combined.with_name("combined.pcm16.wav")
    ffmpeg_runner(combined, converted, "anull")
    try:
        with wave.open(str(converted), "rb") as wav:
            if wav.getnchannels() != 1 or wav.getsampwidth() != 2:
                raise IrodoriError(f"16bit PCM mono に変換できませんでした: {converted}")
    except (OSError, EOFError, wave.Error) as exc:
        raise IrodoriError(f"変換後の WAV を読めません: {converted}") from exc
    converted.replace(combined)


def _prior_attempt(previous: dict[str, Any] | None) -> int:
    if previous is None or not str(previous.get("engine_id", "")).startswith(
        "irodori/"
    ):
        return 0
    try:
        return max(0, int(previous.get("attempt", 0)))
    except (TypeError, ValueError):
        return 0


def synthesize_cues(
    problem_text: str,
    rule_text: str,
    out_dir: Path,
    *,
    config: dict[str, Any],
    force: bool = False,
    runner: InferRunner | None = None,
    ffmpeg_runner: narration_gemini.FfmpegRunner | None = None,
) -> dict[str, Any]:
    """予算内の音声を最大 max_takes 回合成し、通算テイクを記録する。"""
    out_dir = Path(out_dir).resolve()
    texts = {"problem": problem_text, "rule": rule_text}
    model = str(config["model"])
    ref_dir = SET_DIR / str(config.get("ref_dir", "assets/voice/kamerock-g4"))
    refs, ref_fingerprints = _ref_wavs(ref_dir)
    precision = str(config.get("precision", "bf16"))
    if precision != "bf16":
        raise ValueError(f"Irodori の precision は bf16 にしてください: {precision}")
    base_seed = int(config.get("seed", 1))
    base_seconds = float(config.get("seconds", 20.0))
    seconds_step = float(config.get("seconds_step", 0.5))
    max_takes = int(config.get("max_takes", 3))
    gap = float(config.get("gap_seconds", 1.2))
    budget = float(config.get("budget_seconds", 21.0))
    if (
        max_takes < 1 or seconds_step < 0
        or base_seconds - (max_takes - 1) * seconds_step <= 0
    ):
        raise ValueError("Irodori の max_takes / seconds 設定が不正です")
    engine_id = f"irodori/{model}/{ref_dir.name}"
    report_path = out_dir / "narration.json"
    previous = narration_gemini._previous_report(report_path)
    if not force and previous is not None and all(
        (out_dir / f"{cue}.wav").is_file() for cue in texts
    ) and all(previous.get(key) == value for key, value in (
        ("texts", texts), ("engine_id", engine_id), ("model", model),
        ("ref_wavs", ref_fingerprints), ("precision", precision),
        ("base_seconds", base_seconds), ("gap_seconds", gap),
    )):
        try:
            cue_total = round(
                float(previous["cues"]["problem"]["seconds"])
                + gap + float(previous["cues"]["rule"]["seconds"]),
                3,
            )
            if cue_total <= budget and float(previous["total_seconds"]) == cue_total:
                return previous
        except (KeyError, TypeError, ValueError):
            pass

    out_dir.mkdir(parents=True, exist_ok=True)
    infer_runner = runner or subprocess.run
    audio_runner = ffmpeg_runner or narration_gemini._default_ffmpeg_runner
    prior_attempt = _prior_attempt(previous)
    takes: list[dict[str, float | int]] = []
    ratio = len(problem_text) / (len(problem_text) + len(rule_text))
    combined = out_dir / "combined.wav"
    for take in range(max_takes):
        seed = base_seed + prior_attempt + take
        seconds = round(base_seconds - take * seconds_step, 3)
        combined.unlink(missing_ok=True)
        _infer(
            f"{problem_text} {rule_text}", model, refs, seed, seconds,
            combined, infer_runner,
        )
        _ensure_pcm16_mono(combined, audio_runner)
        split_at = narration_gemini._split(
            combined, ratio, out_dir / "problem.wav", out_dir / "rule.wav"
        )
        durations = {
            cue: round(
                narration_gemini._fit(out_dir / f"{cue}.wav", 1.0, audio_runner),
                3,
            )
            for cue in texts
        }
        cues = {
            cue: {"seconds": duration, "frames": round(duration * FPS)}
            for cue, duration in durations.items()
        }
        total = round(durations["problem"] + gap + durations["rule"], 3)
        takes.append({"seed": seed, "seconds": seconds, "total_seconds": total})
        report = {
            "texts": texts,
            "engine_id": engine_id,
            "model": model,
            "ref_wavs": ref_fingerprints,
            "seed": seed,
            "seconds": seconds,
            "base_seconds": base_seconds,
            "precision": precision,
            "split_at_seconds": split_at,
            "gap_seconds": gap,
            "cues": cues,
            "total_seconds": total,
            "takes": takes.copy(),
            "synthesized_at": dt.datetime.now(dt.timezone.utc).isoformat().replace(
                "+00:00", "Z"
            ),
            "attempt": prior_attempt + take + 1,
        }
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        if total <= budget:
            return report
    raise IrodoriBudgetError(total, budget, [entry["seconds"] for entry in takes])


def main(argv: list[str] | None = None) -> int:
    """問題 JSON と design.json の narration 節を使って合成する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem_json", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    source = json.loads(args.problem_json.read_text(encoding="utf-8"))
    cues = source.get("narration_cue", source.get("narration"))
    if not isinstance(cues, dict):
        raise SystemExit("narration_cue または narration がありません")
    design_path = SET_DIR / "assets" / "design.json"
    config = json.loads(design_path.read_text(encoding="utf-8"))["narration"]
    try:
        report = synthesize_cues(
            str(cues["problem"]), str(cues["rule"]), args.out_dir,
            config=config, force=args.force,
        )
    except (IrodoriError, IrodoriBudgetError, RuntimeError) as exc:
        parser.exit(1, f"エラー: {exc}\n")
    print(
        f"{report['engine_id']}: {report['total_seconds']:.3f}s "
        f"(seed {report['seed']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
