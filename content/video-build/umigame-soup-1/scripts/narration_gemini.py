"""Gemini 3.8 Flash TTS で問題文・ルールを一度に合成して WAV 化する。"""

from __future__ import annotations

import argparse
import array
import base64
import datetime as dt
import json
import os
from pathlib import Path
import re
from typing import Any, Callable
import urllib.error
import urllib.request
import wave


API_BASE = "https://generativelanguage.googleapis.com/v1beta"
FPS = 30
FfmpegRunner = Callable[[Path, Path, str], None]


class GeminiApiError(RuntimeError):
    """Gemini API が HTTP エラーを返したことを表す。"""

    def __init__(self, path: str, status: int, detail: str) -> None:
        self.status = status
        self.detail = detail
        super().__init__(f"{path}: HTTP {status}: {detail}")


class GeminiQuotaError(GeminiApiError):
    """課金・クォータ・レート制限で合成を続けられないことを表す。"""


class TempoLimitError(ValueError):
    """合成結果に必要な話速が許容倍率を超えたことを表す。"""

    def __init__(self, tempo: float, max_tempo: float) -> None:
        self.tempo = tempo
        self.max_tempo = max_tempo
        super().__init__(
            f"倍率 {tempo:.3f} > {max_tempo:.2f}・--retake-tts で取り直し"
        )


def _api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key and key.strip():
        return key.strip()
    path = Path.home() / ".config" / "gemini" / "api_key"
    if path.is_file():
        key = path.read_text(encoding="utf-8").strip()
        if key:
            return key
    raise RuntimeError("GEMINI_API_KEY も ~/.config/gemini/api_key もありません")


def _post(path: str, body: dict[str, Any]) -> dict[str, Any]:
    key = _api_key()
    request = urllib.request.Request(
        f"{API_BASE}/{path}",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", "replace")
        detail = body_text[:2000].replace(key, "[REDACTED]")
        error_type = (
            GeminiQuotaError
            if exc.code == 429 or (
                exc.code in (400, 403)
                and re.search(r"quota|billing|RESOURCE_EXHAUSTED|\brate[ _-]?limit", body_text, re.I)
            )
            else GeminiApiError
        )
        raise error_type(path, exc.code, detail) from exc


def _find_audio(node: Any) -> bytes | None:
    """レスポンス JSON から base64 の音声データを探す。"""
    if isinstance(node, dict):
        mime = str(node.get("mime_type") or node.get("mimeType") or "")
        data = node.get("data")
        if isinstance(data, str) and (mime.startswith("audio") or len(data) > 1000):
            return base64.b64decode(data)
        for value in node.values():
            found = _find_audio(value)
            if found:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_audio(value)
            if found:
                return found
    return None


def _to_wav(audio: bytes, out_wav: Path) -> float:
    """WAV は保存し、ヘッダなし PCM は 24 kHz mono WAV に包む。"""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    if audio[:4] == b"RIFF":
        out_wav.write_bytes(audio)
    else:
        with wave.open(str(out_wav), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(24000)
            wav.writeframes(audio)
    with wave.open(str(out_wav), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def synthesize(
    text: str, style: str, model: str, voice: str, out_wav: Path
) -> float:
    """1 回の interactions 呼び出しで全ナレーションを合成する。"""
    body = {
        "model": model,
        "input": [{
            "type": "user_input",
            "content": [{
                "type": "text",
                "text": text,
                "annotations": [{"type": "speech_metadata", "style": style}],
            }],
        }],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }
    response = _post("interactions", body)
    audio = _find_audio(response)
    if not audio:
        raise RuntimeError(f"interactions: 音声データがありません: {json.dumps(response)[:800]}")
    return _to_wav(audio, out_wav)


def _default_ffmpeg_runner(source: Path, target: Path, filters: str) -> None:
    """既存の Docker ffmpeg を使用する（build との循環 import を避ける）。"""
    import build

    build._docker(
        build.FFMPEG_IMAGE,
        build.HERE,
        ["-v", "error", "-y", "-i", build._container_path(source),
         "-af", filters, "-ar", "24000", "-ac", "1",
         build._container_path(target)],
        entrypoint="ffmpeg",
    )


def _fit(wav: Path, tempo: float, ffmpeg_runner: FfmpegRunner) -> float:
    """前後の無音を 0.05 秒残して削り、必要なら話速を上げる。"""
    filters = [
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05",
        "areverse",
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05",
        "areverse",
    ]
    if tempo > 1.0:
        filters.append(f"atempo={tempo}")
    tmp = wav.with_suffix(".tmp.wav")
    ffmpeg_runner(wav, tmp, ",".join(filters))
    tmp.replace(wav)
    with wave.open(str(wav), "rb") as handle:
        return handle.getnframes() / handle.getframerate()


def _split(combined: Path, ratio: float, first: Path, second: Path) -> float:
    """文字数比に最も近い 0.3 秒以上の無音で WAV を分ける。"""
    with wave.open(str(combined), "rb") as handle:
        params = handle.getparams()
        samples = array.array("h", handle.readframes(handle.getnframes()))
    rate = params.framerate
    window = rate // 100
    quiet = [
        max((abs(v) for v in samples[i:i + window]), default=0) < 600
        for i in range(0, len(samples), window)
    ]
    gaps: list[tuple[int, int]] = []
    start = None
    for index, flag in enumerate(quiet + [False]):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            if index - start >= 30 and start > 0 and index < len(quiet):
                gaps.append((start, index))
            start = None
    if not gaps:
        raise RuntimeError(f"{combined}: 切り分け用の無音が見つかりません")
    total = len(quiet)
    best = min(gaps, key=lambda gap: abs((gap[0] + gap[1]) / 2 / total - ratio))
    cut = (best[0] + best[1]) // 2 * window
    for path, chunk in ((first, samples[:cut]), (second, samples[cut:])):
        with wave.open(str(path), "wb") as out:
            out.setparams(params)
            out.writeframes(chunk.tobytes())
    return round(cut / rate, 3)


def _previous_report(path: Path) -> dict[str, Any] | None:
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return report if isinstance(report, dict) else None


def synthesize_cues(
    problem_text: str,
    rule_text: str,
    out_dir: Path,
    *,
    config: dict[str, Any],
    force: bool = False,
    ffmpeg_runner: FfmpegRunner | None = None,
) -> dict[str, Any]:
    """問題文とルールを一度に合成し、切り分けた実測値を保存する。"""
    out_dir = Path(out_dir)
    texts = {"problem": problem_text, "rule": rule_text}
    model = str(config["model"])
    voice_id = str(config["voice_id"])
    style = str(config["style"])
    gap = float(config["gap_seconds"])
    budget = float(config["budget_seconds"])
    target = float(config["target_seconds"])
    max_tempo = float(config["max_tempo"])
    report_path = out_dir / "narration.json"
    previous = _previous_report(report_path)
    if not force and previous is not None and all(
        (out_dir / f"{cue}.wav").is_file() for cue in texts
    ) and all(previous.get(key) == value for key, value in (
        ("texts", texts), ("model", model), ("voice_id", voice_id), ("style", style),
    )):
        if float(previous.get("tempo", 1.0)) > max_tempo:
            raise TempoLimitError(float(previous["tempo"]), max_tempo)
        return previous

    runner = ffmpeg_runner or _default_ffmpeg_runner
    out_dir.mkdir(parents=True, exist_ok=True)
    combined = out_dir / "combined.wav"
    synthesize(f"{problem_text}\n\n{rule_text}", style, model, voice_id, combined)
    ratio = len(problem_text) / (len(problem_text) + len(rule_text))
    split_at = _split(combined, ratio, out_dir / "problem.wav", out_dir / "rule.wav")
    raw = {
        cue: _fit(out_dir / f"{cue}.wav", 1.0, runner)
        for cue in texts
    }
    natural = raw["problem"] + gap + raw["rule"]
    tempo = round((natural - gap) / (target - gap), 3) if natural > budget else 1.0
    seconds = {
        cue: _fit(out_dir / f"{cue}.wav", tempo, runner)
        if tempo > 1.0 else raw[cue]
        for cue in texts
    }
    cues = {
        cue: {"seconds": round(duration, 3), "frames": round(duration * FPS)}
        for cue, duration in seconds.items()
    }
    prior_attempt = previous.get("attempt", 0) if previous is not None else 0
    report = {
        "texts": texts,
        "engine_id": f"gemini/{model}/{voice_id}",
        "model": model,
        "voice_id": voice_id,
        "style": style,
        "split_at_seconds": split_at,
        "natural_seconds": round(natural, 3),
        "tempo": tempo,
        "gap_seconds": gap,
        "cues": cues,
        "total_seconds": round(seconds["problem"] + gap + seconds["rule"], 3),
        "synthesized_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "attempt": int(prior_attempt) + 1,
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if tempo > max_tempo:
        raise TempoLimitError(tempo, max_tempo)
    return report


def main(argv: list[str] | None = None) -> int:
    """問題 JSON の narration_cue を読み、design.json の設定で合成する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem_json", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    source = json.loads(args.problem_json.read_text(encoding="utf-8"))
    cues = source.get("narration_cue", source.get("narration"))
    if not isinstance(cues, dict):
        raise SystemExit("narration_cue または narration がありません")
    design_path = Path(__file__).resolve().parent.parent / "assets" / "design.json"
    config = json.loads(design_path.read_text(encoding="utf-8"))["narration"]
    try:
        report = synthesize_cues(
            str(cues["problem"]), str(cues["rule"]), args.out_dir,
            config=config, force=args.force,
        )
    except (GeminiApiError, TempoLimitError, RuntimeError) as exc:
        parser.exit(1, f"エラー: {exc}\n")
    print(
        f"{report['engine_id']}: {report['total_seconds']:.3f}s "
        f"(×{report['tempo']:.3f})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
