"""umigame-soup-1 のストックから 24 秒事前動画を一括ビルドする。"""

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
from typing import Any, Iterable

from common import (
    ASSETS_DIR,
    FPS,
    HERE,
    NARRATION_BUDGET_SECONDS,
    NARRATION_GAP,
    NARRATION_START,
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
from scripts.narration_polly import synthesize_cues


PUBLIC_DIR = REMOTION_DIR / "public"
PREF_DIR = HERE.parent / "pref-ranking-1"
FONT_SOURCE = PREF_DIR / "remotion" / "public" / "fonts"
NORMALIZE_SCRIPT = PREF_DIR / "remotion" / "scripts" / "normalize_loudness.py"
FONT_FILES = (
    "ZenKakuGothicNew-Black.ttf",
    "ZenKakuGothicNew-Bold.ttf",
    "ZenKakuGothicNew-Medium.ttf",
)
COMPOSITION_ID = "UmigameReel24s"
REMOTION_IMAGE = os.environ.get("REMOTION_IMAGE", "remotion-render")
FFMPEG_IMAGE = os.environ.get("FFMPEG_IMAGE", "image-batch:ffmpeg-check")

# 21-2 PoC の各カット確認点を維持する。
STILL_FRAMES = {
    "intro": 45,
    "q1": 120,
    "a1": 180,
    "q2": 240,
    "a2": 300,
    "q3": 360,
    "a3": 420,
    "master_outro": 500,
    "jr_outro": 620,
    "seam_tail": 714,
}

# 圧縮後の隣接ループ端には微小な量子化差が残るため、画素 0〜255 の平均差 3.0 を
# 仮の許容値とする。初回全数レビューの実測分布を得た後に再校正する前提。
SEAM_MAX_MEAN_DIFF = 3.0


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


def _load_cached_narration(item: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    report_path = out_dir / "narration.json"
    required = [report_path, out_dir / "problem.wav", out_dir / "rule.wav"]
    if not all(path.is_file() for path in required):
        raise RuntimeError(
            f"ナレーション未合成です: {out_dir} "
            "（--no-tts を外して Polly 合成するか、先に narration_polly.py を実行）"
        )
    report = json.loads(report_path.read_text(encoding="utf-8"))
    expected = {
        "problem": item["narration"]["problem"],
        "rule": item["narration"]["rule"],
    }
    if report.get("texts") != expected:
        raise RuntimeError(f"ナレーションの文章がストックと一致しません: {out_dir}")
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
) -> dict[str, Any]:
    """ストックと実測音声から Zod スキーマどおりの props を組み立てる。"""
    play = item.get("play_example")
    if not isinstance(play, list) or len(play) != 6:
        raise ValueError("play_example は質問→返答 3 往復（6 件）にしてください")
    for index, line in enumerate(play):
        if not isinstance(line, dict) or line.get("role") not in {"questioner", "master"}:
            raise ValueError(f"play_example[{index}] の role が不正です")
    validate_narration_budget(narration_report)
    key = str(item["content_key"])
    lines = item["character_lines"]
    return {
        "contentKey": key,
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


def extract_stills(final_path: Path, content_key: str) -> dict[str, str]:
    output = WORK / "stills"
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


def probe_video(final_path: Path, content_key: str) -> dict[str, Any]:
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
    path = WORK / "probe" / f"{content_key}.json"
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
        errors.append(f"尺が 24.0±0.2 秒ではありません: {duration}")
    if probe.get("audio_codec") != "aac":
        errors.append(f"AAC 音声がありません: {probe.get('audio_codec')}")
    return errors


def seam_mean_diff(first: Path, last: Path) -> float:
    """2 枚の RGB 画像についてチャンネル横断の平均絶対差を返す。"""
    from PIL import Image, ImageChops, ImageStat

    with Image.open(first) as first_image, Image.open(last) as last_image:
        left = first_image.convert("RGB")
        right = last_image.convert("RGB")
        if left.size != right.size:
            raise ValueError(f"継ぎ目画像の寸法が違います: {left.size} / {right.size}")
        means = ImageStat.Stat(ImageChops.difference(left, right)).mean
    return sum(means) / len(means)


def inspect_seam(final_path: Path, content_key: str) -> float:
    output = WORK / "seam"
    output.mkdir(parents=True, exist_ok=True)
    paths = []
    for label, frame in (("first", 0), ("last", TOTAL_FRAMES - 1)):
        path = output / f"{content_key}_{label}.png"
        _docker(
            FFMPEG_IMAGE, HERE,
            ["-v", "error", "-y", "-i", _container_path(final_path),
             "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1", _container_path(path)],
            entrypoint="ffmpeg",
        )
        paths.append(path)
    difference = seam_mean_diff(paths[0], paths[1])
    if difference > SEAM_MAX_MEAN_DIFF:
        raise RuntimeError(
            f"継ぎ目差分 {difference:.3f} が閾値 {SEAM_MAX_MEAN_DIFF:.1f} を超えました"
        )
    return difference


def _record(
    item: dict[str, Any], props_path: Path, video_path: Path,
    track: dict[str, Any], narration: dict[str, float], probe: dict[str, Any],
    stills: dict[str, str], seam_difference: float,
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
        "narration": {key: round(value, 3) for key, value in narration.items()},
        "probe": probe,
        "seam_mean_diff": round(seam_difference, 4),
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", default="batch-01")
    parser.add_argument("--content-key", action="append", dest="content_keys")
    parser.add_argument("--skip-render", action="store_true", help="props 生成までで止める")
    parser.add_argument("--rebuild-bgm", action="store_true", help="既存割当を破棄して再選曲する")
    parser.add_argument(
        "--no-tts", action="store_true",
        help="Polly を呼ばず、work/narration の既存 WAV だけを使う",
    )
    return parser


def _preflight_inputs(items: Iterable[dict[str, Any]], *, no_tts: bool) -> list[str]:
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
                _load_cached_narration(item, WORK / "narration" / key)
            except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"{key}: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    failures: list[str] = []
    try:
        targets = select_items(load_items(args.batch), args.content_keys)
        manifest = load_manifest()
        design = json.loads((ASSETS_DIR / "design.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    failures = _preflight_inputs(targets, no_tts=args.no_tts)
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
                report = _load_cached_narration(item, narration_dir)
            else:
                report = synthesize_cues(
                    item["narration"]["problem"], item["narration"]["rule"], narration_dir
                )
            narration_summary = validate_narration_budget(report)
            track = select_bgm_track(
                manifest, key, tracks, rebuild_bgm=args.rebuild_bgm
            )
            stage_assets(key, track, narration_dir)
            props = build_props(item, design, report, track)
            props_path = WORK / "props" / f"{key}.json"
            write_json(props_path, props)
            if args.skip_render:
                print(f"{key}: props 生成完了（skip-render）")
                continue
            raw_path = WORK / "out" / f"{key}.raw.mp4"
            video_path = WORK / "videos" / f"{key}.mp4"
            render(props_path, raw_path)
            normalize_loudness(raw_path, video_path)
            stills = extract_stills(video_path, key)
            probe = probe_video(video_path, key)
            seam_difference = inspect_seam(video_path, key)
            manifest[key] = _record(
                item, props_path, video_path, track, narration_summary,
                probe, stills, seam_difference,
            )
            save_manifest(manifest)
            print(f"{key}: ビルド完了（seam={seam_difference:.3f}）")
        except Exception as exc:
            failures.append(f"{key}: {exc}")
            print(f"エラー: {key}: {exc}", file=sys.stderr)

    try:
        from review_sheet import write_review

        write_review(load_manifest(), batch=args.batch, content_keys=args.content_keys)
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
