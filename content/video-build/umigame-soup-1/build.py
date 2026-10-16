"""umigame-soup-1 のストックから事前動画（27 秒・一本道）を一括ビルドする。"""

from __future__ import annotations

import argparse
import datetime as dt
from fractions import Fraction
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Iterable

from common import (
    ASSETS_DIR,
    DURATION_SECONDS,
    FPS,
    HERE,
    NARRATION_BUDGET_SECONDS,
    NARRATION_GAP,
    NARRATION_START,
    OPENING_END,
    OPENING_FADE_FRAMES,
    REMOTION_DIR,
    ROOT,
    TOTAL_FRAMES,
    WORK,
    load_items,
    load_manifest,
    save_manifest,
    select_items,
    write_json,
)
from prepare_bgm import TRACKS_PATH, OUT_DIR as BGM_OUT_DIR, validate_tracks
from scripts import narration_gemini, narration_irodori, narration_polly


PUBLIC_DIR = REMOTION_DIR / "public"
PREF_DIR = HERE.parent / "pref-ranking-1"
FONT_SOURCE = PREF_DIR / "remotion" / "public" / "fonts"
NORMALIZE_SCRIPT = PREF_DIR / "remotion" / "scripts" / "normalize_loudness.py"
FONT_FILES = (
    "ZenKakuGothicNew-Black.ttf",
    "ZenKakuGothicNew-Bold.ttf",
    "ZenKakuGothicNew-Medium.ttf",
)
COMPOSITION_ID = "UmigameReel"
REMOTION_IMAGE = os.environ.get("REMOTION_IMAGE", "remotion-render")
FFMPEG_IMAGE = os.environ.get("FFMPEG_IMAGE", "image-batch:ffmpeg-check")

# 各カットの確認点（R-1-1 で導入シーンを足し、継ぎ目の確認点を末尾の確認点に替えた）。
STILL_FRAMES = {
    "opening": 0,
    "switch": OPENING_END + OPENING_FADE_FRAMES // 2,
    "intro": 120,
    "q1": 195,
    "a1": 255,
    "q2": 315,
    "a2": 375,
    "q3": 435,
    "a3": 495,
    "master_outro": 580,
    "jr_outro": 720,
    "end": TOTAL_FRAMES - 1,
}


class NarrationBudgetError(ValueError):
    """ナレーションが 21 秒予算を超過したことを表す。"""


def _container_path(path: Path) -> str:
    return (Path("/repo") / path.resolve().relative_to(ROOT.resolve())).as_posix()


def _run(command: list[str], label: str) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise RuntimeError(f"{label} を起動できません: {exc}") from exc
    if completed.returncode != 0:
        detail = "\n".join(
            (completed.stdout + completed.stderr).strip().splitlines()[-12:]
        )
        raise RuntimeError(f"{label} が失敗しました（{completed.returncode}）:\n{detail}")
    return completed


def _docker(
    image: str, workdir: Path, args: list[str], *, entrypoint: str | None = None
) -> subprocess.CompletedProcess[str]:
    command = [
        "docker", "run", "--rm", "-v", f"{ROOT}:/repo",
        "-w", _container_path(workdir), "-e", "HOME=/tmp",
        "--user", f"{os.getuid()}:{os.getgid()}",
    ]
    if entrypoint:
        command += ["--entrypoint", entrypoint]
    command += [image, *args]
    print("+", " ".join(command), flush=True)
    return _run(command, f"Docker {entrypoint or image}")


def validate_narration_budget(report: dict[str, Any]) -> dict[str, float]:
    """実測 cue 長と 1.2 秒の間が 21 秒以内かを検査する。"""
    try:
        problem = float(report["cues"]["problem"]["seconds"])
        rule = float(report["cues"]["rule"]["seconds"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("narration.json の cue 実測値が不正です") from exc
    total = problem + NARRATION_GAP / FPS + rule
    if total > NARRATION_BUDGET_SECONDS:
        raise NarrationBudgetError(
            f"ナレーション予算超過: problem {problem:.3f}s + 1.2s + "
            f"rule {rule:.3f}s = {total:.3f}s > {NARRATION_BUDGET_SECONDS:.1f}s"
        )
    return {"problem_sec": problem, "rule_sec": rule, "total_sec": total}


def _load_cached_narration(
    item: dict[str, Any], out_dir: Path, *, max_tempo: float = 1.19
) -> dict[str, Any]:
    report_path = out_dir / "narration.json"
    required = [report_path, out_dir / "problem.wav", out_dir / "rule.wav"]
    if not all(path.is_file() for path in required):
        raise RuntimeError(
            f"ナレーション未合成です: {out_dir} "
            "（--no-tts を外して TTS 合成するか、先にナレーションを合成）"
        )
    report = json.loads(report_path.read_text(encoding="utf-8"))
    expected = {
        "problem": item["narration"]["problem"],
        "rule": item["narration"]["rule"],
    }
    if report.get("texts") != expected:
        raise RuntimeError(f"ナレーションの文章がストックと一致しません: {out_dir}")
    if str(report.get("engine_id", "")).startswith("gemini/"):
        tempo = float(report.get("tempo", 1.0))
        if tempo > max_tempo:
            raise narration_gemini.TempoLimitError(tempo, max_tempo)
    return report


def _synthesize_polly(
    problem_text: str, rule_text: str, out_dir: Path, *, force: bool
) -> dict[str, Any]:
    """Polly アダプタを変更せず、取り直し時は一時領域で再合成する。"""
    if not force:
        return narration_polly.synthesize_cues(problem_text, rule_text, out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="polly-retake-", dir=out_dir.parent) as temp:
        temporary_dir = Path(temp)
        report = narration_polly.synthesize_cues(problem_text, rule_text, temporary_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in ("problem.wav", "rule.wav", "narration.json"):
            (temporary_dir / name).replace(out_dir / name)
    return report


def load_bgm_tracks() -> list[dict[str, Any]]:
    """tracks.json と実ファイルが揃った BGM 一覧を返す。"""
    if not TRACKS_PATH.is_file():
        raise RuntimeError(
            f"BGM 台帳がありません: {TRACKS_PATH}（prepare_bgm.py を先に実行）"
        )
    tracks = validate_tracks(json.loads(TRACKS_PATH.read_text(encoding="utf-8")))
    missing = [track["output"] for track in tracks if not (BGM_OUT_DIR / track["output"]).is_file()]
    if missing:
        raise RuntimeError("前処理済み BGM がありません: " + ", ".join(missing))
    return tracks


def select_bgm_track(
    manifest: dict[str, Any],
    content_key: str,
    tracks: list[dict[str, Any]],
    *,
    rebuild_bgm: bool = False,
) -> dict[str, Any]:
    """既存割当を維持するか、使用回数最少・番号順で BGM を割り当てる。"""
    by_name = {str(track["output"]): track for track in tracks}
    current = manifest.get(content_key)
    if not rebuild_bgm and isinstance(current, dict):
        bgm = current.get("bgm")
        name = bgm.get("track") if isinstance(bgm, dict) else None
        if name in by_name:
            return by_name[name]
    counts = {name: 0 for name in by_name}
    for key, record in manifest.items():
        if rebuild_bgm and key == content_key:
            continue
        if not isinstance(record, dict) or not isinstance(record.get("bgm"), dict):
            continue
        name = record["bgm"].get("track")
        if name in counts:
            counts[name] += 1
    if not counts:
        raise RuntimeError("割り当て可能な BGM がありません")
    selected = min(counts, key=lambda name: (counts[name], name))
    return by_name[selected]


def opening_copies(design: dict[str, Any]) -> tuple[str, dict[str, str]]:
    """design.json の導入シーンの固定コピー（採用中の案 ID・案の一覧）を返す。"""
    section = design.get("opening_copy")
    if not isinstance(section, dict):
        raise ValueError("design.json に opening_copy がありません")
    candidates = section.get("candidates")
    selected = section.get("selected")
    if not isinstance(candidates, dict) or not candidates:
        raise ValueError("opening_copy.candidates は 1 件以上の object にしてください")
    if selected not in candidates:
        raise ValueError(f"opening_copy.selected が候補にありません: {selected}")
    for copy_id, text in candidates.items():
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"opening_copy.candidates.{copy_id} が空です")
    return str(selected), {str(key): str(value) for key, value in candidates.items()}


def timeline_summary(narration_report: dict[str, Any]) -> dict[str, int]:
    """導入 → 本編の切替とナレーション開始・終了のフレームを返す（レビュー・記録用）。"""
    problem = int(narration_report["cues"]["problem"]["frames"])
    rule = int(narration_report["cues"]["rule"]["frames"])
    rule_start = NARRATION_START + problem + NARRATION_GAP
    return {
        "total_frames": TOTAL_FRAMES,
        "opening_end": OPENING_END,
        "main_fully_visible": OPENING_END + OPENING_FADE_FRAMES,
        "narration_problem_start": NARRATION_START,
        "narration_rule_start": rule_start,
        "narration_end": rule_start + rule,
    }


def stage_assets(content_key: str, track: dict[str, Any], narration_dir: Path) -> None:
    """レンダリングに必要な固定・問別アセットを public へ配置する。"""
    for directory in (
        PUBLIC_DIR / "fonts", PUBLIC_DIR / "bg", PUBLIC_DIR / "char",
        PUBLIC_DIR / "audio" / "bgm", PUBLIC_DIR / "narration" / content_key,
    ):
        directory.mkdir(parents=True, exist_ok=True)
    for name in FONT_FILES:
        shutil.copy2(FONT_SOURCE / name, PUBLIC_DIR / "fonts" / name)
    shutil.copy2(WORK / "backgrounds" / f"{content_key}.jpg", PUBLIC_DIR / "bg" / f"{content_key}.jpg")
    for name in ("master_base", "master_happy", "jr_base"):
        shutil.copy2(ASSETS_DIR / "characters" / f"{name}.png", PUBLIC_DIR / "char" / f"{name}.png")
    shutil.copy2(BGM_OUT_DIR / track["output"], PUBLIC_DIR / "audio" / "bgm" / track["output"])
    shutil.copy2(ASSETS_DIR / "se" / "bubble_pop.wav", PUBLIC_DIR / "audio" / "se_pop.wav")
    for cue in ("problem", "rule"):
        shutil.copy2(narration_dir / f"{cue}.wav", PUBLIC_DIR / "narration" / content_key / f"{cue}.wav")


def build_props(
    item: dict[str, Any],
    design: dict[str, Any],
    narration_report: dict[str, Any],
    bgm_track: dict[str, Any],
    *,
    copy_id: str | None = None,
) -> dict[str, Any]:
    """ストックと実測音声から Zod スキーマどおりの props を組み立てる。

    Args:
        item: ストック 1 件。
        design: ``assets/design.json``。
        narration_report: ナレーションの実測（cue ごとの frames）。
        bgm_track: 割り当てた BGM。
        copy_id: 導入シーンの固定コピーの案 ID。省略時は ``opening_copy.selected``。
    """
    play = item.get("play_example")
    if not isinstance(play, list) or len(play) != 6:
        raise ValueError("play_example は質問→返答 3 往復（6 件）にしてください")
    for index, line in enumerate(play):
        if not isinstance(line, dict) or line.get("role") not in {"questioner", "master"}:
            raise ValueError(f"play_example[{index}] の role が不正です")
    validate_narration_budget(narration_report)
    selected, candidates = opening_copies(design)
    copy_key = selected if copy_id is None else copy_id
    if copy_key not in candidates:
        raise ValueError(f"導入シーンの固定コピーの案がありません: {copy_key}")
    key = str(item["content_key"])
    lines = item["character_lines"]
    return {
        "contentKey": key,
        "openingCopy": candidates[copy_key],
        "hook": item["hook"],
        "problemText": item["problem_text"],
        "ruleText": item["rule_text"],
        "background": f"bg/{key}.jpg",
        "master": {
            "name": design["master"]["name"],
            "base": "char/master_base.png",
            "happy": "char/master_happy.png",
        },
        "jr": {"name": design["jr"]["name"], "base": "char/jr_base.png"},
        "masterLines": lines["master"],
        "jrLines": lines["jr"],
        "playExample": [
            {"role": line["role"], "text": line["text"]} for line in play
        ],
        "narration": {
            cue: {
                "file": f"narration/{key}/{cue}.wav",
                "frames": int(narration_report["cues"][cue]["frames"]),
            }
            for cue in ("problem", "rule")
        },
        "bgm": f"audio/bgm/{bgm_track['output']}",
        "bubbleSe": "audio/se_pop.wav",
    }


def render(props_path: Path, raw_path: Path) -> None:
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    _docker(
        REMOTION_IMAGE,
        REMOTION_DIR,
        [
            "npx", "remotion", "render", "src/index.ts", COMPOSITION_ID,
            _container_path(raw_path), f"--props={_container_path(props_path)}",
            "--concurrency=3", "--timeout=120000",
        ],
    )


def normalize_loudness(raw_path: Path, final_path: Path) -> None:
    final_path.parent.mkdir(parents=True, exist_ok=True)
    _docker(
        FFMPEG_IMAGE,
        HERE,
        [_container_path(NORMALIZE_SCRIPT), _container_path(raw_path), _container_path(final_path)],
        entrypoint="python",
    )


def extract_stills(final_path: Path, content_key: str, out_dir: Path | None = None) -> dict[str, str]:
    output = (out_dir or WORK) / "stills"
    output.mkdir(parents=True, exist_ok=True)
    result: dict[str, str] = {}
    for label, frame in STILL_FRAMES.items():
        path = output / f"{content_key}_{label}.jpg"
        _docker(
            FFMPEG_IMAGE, HERE,
            ["-v", "error", "-y", "-i", _container_path(final_path),
             "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1", "-q:v", "3",
             _container_path(path)],
            entrypoint="ffmpeg",
        )
        result[label] = path.relative_to(WORK).as_posix()
    return result


def probe_video(final_path: Path, content_key: str, out_dir: Path | None = None) -> dict[str, Any]:
    """ffprobe JSON を要約し、配信物の寸法・fps・尺・AAC を検査する。"""
    completed = _docker(
        FFMPEG_IMAGE, HERE,
        ["-v", "error", "-show_streams", "-show_format", "-of", "json",
         _container_path(final_path)],
        entrypoint="ffprobe",
    )
    raw = json.loads(completed.stdout)
    streams = raw.get("streams", [])
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    audio = next((stream for stream in streams if stream.get("codec_type") == "audio"), {})
    try:
        fps = float(Fraction(video.get("r_frame_rate", "0/1")))
    except (ValueError, ZeroDivisionError):
        fps = 0.0
    duration = float(raw.get("format", {}).get("duration", 0.0))
    summary = {
        "width": video.get("width"),
        "height": video.get("height"),
        "fps": fps,
        "duration": duration,
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name"),
        "sample_rate": audio.get("sample_rate"),
        "channels": audio.get("channels"),
    }
    errors = validate_probe(summary)
    summary["valid"] = not errors
    summary["errors"] = errors
    path = (out_dir or WORK) / "probe" / f"{content_key}.json"
    write_json(path, summary)
    if errors:
        raise RuntimeError("ffprobe 検査エラー: " + " / ".join(errors))
    return summary


def validate_probe(probe: dict[str, Any]) -> list[str]:
    """manifest に保存する probe 要約を純関数で検査する。"""
    errors: list[str] = []
    if probe.get("width") != 1080 or probe.get("height") != 1920:
        errors.append(f"寸法が 1080x1920 ではありません: {probe.get('width')}x{probe.get('height')}")
    try:
        fps = float(probe.get("fps", 0))
    except (TypeError, ValueError):
        fps = 0
    if abs(fps - FPS) > 0.01:
        errors.append(f"fps が 30 ではありません: {fps}")
    try:
        duration = float(probe.get("duration", 0))
    except (TypeError, ValueError):
        duration = 0
    if abs(duration - TOTAL_FRAMES / FPS) > 0.2:
        errors.append(f"尺が {DURATION_SECONDS}.0±0.2 秒ではありません: {duration}")
    if duration >= 30:
        errors.append(f"尺が 30 秒以上です: {duration}")
    if probe.get("audio_codec") != "aac":
        errors.append(f"AAC 音声がありません: {probe.get('audio_codec')}")
    return errors


def render_copy_variants(
    props: dict[str, Any], candidates: dict[str, str], out_dir: Path
) -> None:
    """導入シーンのコマを固定コピーの全案で静止画にする（work/.../copy-variants/<key>_<案>_opening.jpg）。"""
    output = out_dir / "copy-variants"
    job_items: list[dict[str, str]] = []
    for copy_id, text in candidates.items():
        variant = {**props, "openingCopy": text}
        path = output / "props" / f"{props['contentKey']}_{copy_id}.json"
        write_json(path, variant)
        job_items.append(
            {"props": _container_path(path), "out": _container_path(output / f"{props['contentKey']}_{copy_id}")}
        )
    job = output / f"job_{props['contentKey']}.json"
    write_json(job, {"frames": {"opening": STILL_FRAMES["opening"]}, "items": job_items})
    _docker(REMOTION_IMAGE, REMOTION_DIR, ["node", "scripts/render_stills.mjs", _container_path(job)])


def _record(
    item: dict[str, Any], props_path: Path, video_path: Path,
    track: dict[str, Any], narration: dict[str, float | str], probe: dict[str, Any],
    stills: dict[str, str], timeline: dict[str, int],
    opening_copy: dict[str, str],
) -> dict[str, Any]:
    return {
        "content_key": item["content_key"],
        "title": item["title"],
        "video": video_path.relative_to(WORK).as_posix(),
        "background_png": (
            WORK / "backgrounds" / "raw" / f"{item['content_key']}.png"
        ).relative_to(WORK).as_posix(),
        "props": props_path.relative_to(WORK).as_posix(),
        "stills": stills,
        "bgm": {
            "track": track["output"],
            "s3_key": track["s3_key"],
            "provisional": track["provisional"],
        },
        "narration": {
            key: round(value, 3) if isinstance(value, (int, float)) else value
            for key, value in narration.items()
        },
        "probe": probe,
        "timeline": timeline,
        "opening_copy": opening_copy,
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", default="batch-01")
    parser.add_argument("--content-key", action="append", dest="content_keys")
    parser.add_argument("--skip-render", action="store_true", help="props 生成までで止める")
    parser.add_argument(
        "--out-dir", type=Path, default=None,
        help="props・動画・静止画・probe・manifest の書き出し先（既定: work/。試作は work/ の下の別ディレクトリへ）",
    )
    parser.add_argument(
        "--opening-copy", default=None,
        help="導入シーンの固定コピーの案 ID（既定: design.json の opening_copy.selected）",
    )
    parser.add_argument(
        "--copy-variants", action="store_true",
        help="導入シーンを固定コピーの全案で静止画にし、review.html で見比べられるようにする",
    )
    parser.add_argument("--rebuild-bgm", action="store_true", help="既存割当を破棄して再選曲する")
    parser.add_argument(
        "--tts", choices=("irodori", "gemini", "polly"), default="irodori",
        help="ナレーションの TTS（既定: irodori）",
    )
    parser.add_argument(
        "--retake-tts", action="store_true", help="対象のナレーションを取り直す",
    )
    parser.add_argument(
        "--no-tts", action="store_true",
        help="TTS を呼ばず、work/narration の既存 WAV だけを使う",
    )
    return parser


def _preflight_inputs(
    items: Iterable[dict[str, Any]], *, no_tts: bool, max_tempo: float = 1.19
) -> list[str]:
    """BGM 前に問別の必須入力をまとめて検査する。"""
    errors: list[str] = []
    for item in items:
        key = str(item["content_key"])
        background = WORK / "backgrounds" / f"{key}.jpg"
        if not background.is_file():
            errors.append(
                f"{key}: 背景 JPEG がありません: {background}（intake.py を先に実行）"
            )
        if no_tts:
            try:
                _load_cached_narration(
                    item, WORK / "narration" / key, max_tempo=max_tempo
                )
            except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"{key}: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.no_tts and args.retake_tts:
        print("エラー: --no-tts と --retake-tts は同時に指定できません", file=sys.stderr)
        return 1
    failures: list[str] = []
    out_dir = WORK if args.out_dir is None else args.out_dir.resolve()
    manifest_path = out_dir / "manifest.json"
    try:
        targets = select_items(load_items(args.batch), args.content_keys)
        manifest = load_manifest(manifest_path)
        design = json.loads((ASSETS_DIR / "design.json").read_text(encoding="utf-8"))
        selected_copy, copy_candidates = opening_copies(design)
        copy_id = args.opening_copy or selected_copy
        if copy_id not in copy_candidates:
            raise ValueError(f"導入シーンの固定コピーの案がありません: {copy_id}")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    max_tempo = float(design["narration_gemini"]["max_tempo"])
    failures = _preflight_inputs(
        targets, no_tts=args.no_tts, max_tempo=max_tempo
    )
    if failures:
        print("入力不足:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    try:
        tracks = load_bgm_tracks()
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    for item in targets:
        key = str(item["content_key"])
        try:
            background = WORK / "backgrounds" / f"{key}.jpg"
            if not background.is_file():
                raise RuntimeError(
                    f"背景 JPEG がありません: {background}（intake.py を先に実行）"
                )
            narration_dir = WORK / "narration" / key
            if args.no_tts:
                report = _load_cached_narration(
                    item, narration_dir, max_tempo=max_tempo
                )
            elif args.tts == "irodori":
                report = narration_irodori.synthesize_cues(
                    item["narration"]["problem"], item["narration"]["rule"],
                    narration_dir, config=design["narration"], force=args.retake_tts,
                )
            elif args.tts == "gemini":
                report = narration_gemini.synthesize_cues(
                    item["narration"]["problem"], item["narration"]["rule"],
                    narration_dir, config=design["narration_gemini"], force=args.retake_tts,
                )
            else:
                report = _synthesize_polly(
                    item["narration"]["problem"], item["narration"]["rule"],
                    narration_dir, force=args.retake_tts,
                )
            narration_summary = validate_narration_budget(report)
            if report.get("engine_id") is not None:
                narration_summary["engine_id"] = str(report["engine_id"])
            if report.get("tempo") is not None:
                narration_summary["tempo"] = float(report["tempo"])
            if str(report.get("engine_id", "")).startswith("irodori/"):
                narration_summary["seed"] = int(report["seed"])
                narration_summary["seconds"] = float(report["seconds"])
            track = select_bgm_track(
                manifest, key, tracks, rebuild_bgm=args.rebuild_bgm
            )
            stage_assets(key, track, narration_dir)
            props = build_props(item, design, report, track, copy_id=copy_id)
            props_path = out_dir / "props" / f"{key}.json"
            write_json(props_path, props)
            if args.skip_render:
                print(f"{key}: props 生成完了（skip-render）")
                continue
            raw_path = out_dir / "out" / f"{key}.raw.mp4"
            video_path = out_dir / "videos" / f"{key}.mp4"
            render(props_path, raw_path)
            normalize_loudness(raw_path, video_path)
            stills = extract_stills(video_path, key, out_dir)
            probe = probe_video(video_path, key, out_dir)
            timeline = timeline_summary(report)
            if args.copy_variants:
                render_copy_variants(props, copy_candidates, out_dir)
            manifest[key] = _record(
                item, props_path, video_path, track, narration_summary,
                probe, stills, timeline,
                {"id": copy_id, "text": copy_candidates[copy_id]},
            )
            save_manifest(manifest, manifest_path)
            print(
                f"{key}: ビルド完了（尺 {float(probe.get('duration', 0)):.3f}s / 導入 0–{timeline['opening_end']}f"
                f" → 本編 {timeline['main_fully_visible']}f で切替完了 / ナレーション problem "
                f"{timeline['narration_problem_start']}f・rule {timeline['narration_rule_start']}f"
                f"・終了 {timeline['narration_end']}f / 総 {timeline['total_frames']}f）"
            )
        except (narration_gemini.GeminiQuotaError, narration_irodori.IrodoriError) as exc:
            failures.append(f"{key}: {exc}")
            print(f"エラー: {key}: {exc}", file=sys.stderr)
            print("\n失敗一覧:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
            return 1
        except (narration_gemini.TempoLimitError, narration_irodori.IrodoriBudgetError) as exc:
            failures.append(f"{key}: {exc}")
            print(f"エラー: {key}: {exc}", file=sys.stderr)
        except Exception as exc:
            failures.append(f"{key}: {exc}")
            print(f"エラー: {key}: {exc}", file=sys.stderr)

    try:
        from review_sheet import write_review

        write_review(
            load_manifest(manifest_path), batch=args.batch, content_keys=args.content_keys,
            copy_candidates=copy_candidates if args.copy_variants else None,
            variant_dir=out_dir / "copy-variants" if args.copy_variants else None,
        )
    except Exception as exc:
        failures.append(f"review_sheet: {exc}")

    if failures:
        print("\n失敗一覧:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"完了: {len(targets)} 件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
