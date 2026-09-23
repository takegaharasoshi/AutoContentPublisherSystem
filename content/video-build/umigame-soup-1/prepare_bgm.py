"""24 秒 BGM を前処理し、正式トラックの audio_assets SQL を生成する。

``UmigameReel.tsx`` はナレーション中のダッキングだけを行うため、セット設計の
フェードイン 0.5 秒・フェードアウト 1.0 秒は本スクリプトで素材へ焼き込む。
正式トラックは 2 パス loudnorm（-14 LUFS）後に AAC へ変換する。
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any

from common import HERE, ROOT, SET_CODE, WORK


BGM_DIR = WORK / "bgm"
SOURCE_DIR = BGM_DIR / "source"
OUT_DIR = BGM_DIR / "out"
TRACKS_PATH = BGM_DIR / "tracks.json"
SQL_PATH = (
    ROOT / "content" / "umigame-stock" / SET_CODE / "set-registration"
    / "03_audio_assets.sql"
)
DURATION_SECONDS = 24
FADE_IN_SECONDS = 0.5
FADE_OUT_SECONDS = 1.0
TARGET_I = -14.0
TARGET_TP = -1.5
TARGET_LRA = 11.0
ACQUIRED_AT_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_KEYS = (
    "file", "start", "title", "source_url", "license_type", "license_note",
    "acquired_at",
)

PROVISIONAL_TEMPLATE = [
    {
        "file": "poc/classic-umigame/normalized/bgm_24s.m4a",
        "start": 0,
        "title": "Study Lofi Music（暫定・20 秒地点に継ぎ目あり）",
        "source_url": "audio/logic-training-1/night/track01.m4a",
        "license_type": "Pixabay Content License",
        "license_note": "logic-training-1 night track01 の 20 秒版を 24 秒へループした PoC 資材",
        "acquired_at": "2026-09-04",
        "provisional": True,
    }
]


class ManifestError(ValueError):
    """tracks.json の検査エラー。"""


class FfmpegError(RuntimeError):
    """ffmpeg の実行・出力解析エラー。"""


def validate_tracks(value: object) -> list[dict[str, Any]]:
    """tracks.json を検査し、trackNN の出力名と S3 キーを補う。"""
    if not isinstance(value, list) or not value:
        raise ManifestError("tracks.json は 1〜5 件の配列にしてください")
    if len(value) > 5:
        raise ManifestError("BGM は 5 曲までです")
    tracks: list[dict[str, Any]] = []
    allowed = set(REQUIRED_KEYS) | {"provisional"}
    for index, raw in enumerate(value, start=1):
        if not isinstance(raw, dict):
            raise ManifestError(f"[{index}] トラックはオブジェクトにしてください")
        missing = [key for key in REQUIRED_KEYS if key not in raw]
        if missing:
            raise ManifestError(f"[{index}] 必須キーがありません: {', '.join(missing)}")
        unknown = set(raw) - allowed
        if unknown:
            raise ManifestError(f"[{index}] 未知のキー: {', '.join(sorted(unknown))}")
        for key in ("file", "title", "source_url", "license_type", "acquired_at"):
            if not isinstance(raw[key], str) or not raw[key].strip():
                raise ManifestError(f"[{index}] {key} は空でない文字列にしてください")
        if raw["license_note"] is not None and not isinstance(raw["license_note"], str):
            raise ManifestError(f"[{index}] license_note は文字列または null にしてください")
        start = raw["start"]
        if isinstance(start, bool) or not isinstance(start, (int, float)) or start < 0:
            raise ManifestError(f"[{index}] start は 0 以上の秒数にしてください")
        if not ACQUIRED_AT_PATTERN.match(raw["acquired_at"]):
            raise ManifestError(f"[{index}] acquired_at は YYYY-MM-DD 形式にしてください")
        if re.search(r"\bNC\b|NonCommercial|非商用", raw["license_type"], re.I):
            raise ManifestError(f"[{index}] 非商用ライセンスは使用できません")
        if "provisional" in raw and not isinstance(raw["provisional"], bool):
            raise ManifestError(f"[{index}] provisional は真偽値にしてください")
        output = f"track{index:02d}.m4a"
        tracks.append(
            {
                **raw,
                "provisional": bool(raw.get("provisional", False)),
                "output": output,
                "s3_key": f"audio/{SET_CODE}/{output}",
            }
        )
    return tracks


def _sql_literal(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def _sql_value(value: object) -> str:
    return "NULL" if value is None else _sql_literal(str(value))


def generate_audio_assets_sql(tracks: list[dict[str, Any]]) -> str:
    """暫定トラックを除く正式トラックだけの登録 SQL を返す。"""
    lines = [
        f"-- {SET_CODE}: 正式 BGM の audio_assets 登録 SQL",
        "-- prepare_bgm.py が生成。provisional=true のトラックは含めない。",
        "",
    ]
    for track in tracks:
        if track["provisional"]:
            continue
        lines.extend(
            [
                "INSERT INTO audio_assets (set_id, s3_key, asset_type, time_slot,",
                "  title, source_url, license_type, license_note, acquired_at, duration_seconds, is_active)",
                f"SELECT b.id, {_sql_literal(track['s3_key'])}, 'bgm', NULL,",
                f"  {_sql_literal(track['title'])}, {_sql_literal(track['source_url'])},",
                f"  {_sql_literal(track['license_type'])}, {_sql_value(track['license_note'])},",
                f"  {_sql_literal(track['acquired_at'] + ' 00:00:00')}, {DURATION_SECONDS}, 1",
                "FROM batch_sets b",
                f"WHERE b.set_code = {_sql_literal(SET_CODE)};",
                "",
            ]
        )
    return "\n".join(lines)


def _container_path(path: Path) -> str:
    return (Path("/repo") / path.resolve().relative_to(ROOT.resolve())).as_posix()


def _ffmpeg_command(args: list[str], docker: bool) -> list[str]:
    if not docker:
        return [os.environ.get("FFMPEG_BIN", "ffmpeg"), *args]
    return [
        "docker", "run", "--rm", "-u", f"{os.getuid()}:{os.getgid()}",
        "-v", f"{ROOT}:/repo", "-w", _container_path(HERE),
        "--entrypoint", "ffmpeg",
        os.environ.get("FFMPEG_IMAGE", "image-batch:ffmpeg-check"), *args,
    ]


def _run_ffmpeg(args: list[str], *, docker: bool, label: str) -> str:
    try:
        completed = subprocess.run(
            _ffmpeg_command(args, docker), capture_output=True, text=True, check=False
        )
    except FileNotFoundError as exc:
        raise FfmpegError(f"{label} を起動できません: {exc}") from exc
    if completed.returncode != 0:
        detail = "\n".join(completed.stderr.strip().splitlines()[-10:])
        raise FfmpegError(f"{label} が失敗しました:\n{detail}")
    return completed.stderr


def parse_loudnorm_json(stderr: str) -> dict[str, str]:
    start, end = stderr.rfind("{"), stderr.rfind("}")
    if start < 0 or end < start:
        raise FfmpegError("loudnorm の計測 JSON が見つかりません")
    try:
        return json.loads(stderr[start:end + 1])
    except json.JSONDecodeError as exc:
        raise FfmpegError(f"loudnorm の計測 JSON が不正です: {exc}") from exc


def loudnorm_filter(measured: dict[str, str]) -> str:
    return (
        f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
        f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
        f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
        f":offset={measured['target_offset']}:linear=true:print_format=summary"
    )


def _fade_filter() -> str:
    return (
        f"afade=t=in:st=0:d={FADE_IN_SECONDS},"
        f"afade=t=out:st={DURATION_SECONDS - FADE_OUT_SECONDS}:d={FADE_OUT_SECONDS}"
    )


def _source_path(track: dict[str, Any]) -> Path:
    value = Path(track["file"])
    if value.is_absolute():
        return value
    source_candidate = SOURCE_DIR / value
    return source_candidate if source_candidate.is_file() else HERE / value


def process_track(track: dict[str, Any], *, docker: bool = True) -> None:
    """正式トラックを 24 秒化・フェード・2 パス正規化して書き出す。"""
    source = _source_path(track)
    if not source.is_file():
        raise FfmpegError(f"原曲がありません: {source}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / track["output"]
    source_arg = _container_path(source) if docker else str(source)
    destination_arg = _container_path(destination) if docker else str(destination)
    trim = ["-ss", str(track["start"]), "-i", source_arg, "-t", str(DURATION_SECONDS)]
    fade = _fade_filter()
    measured = parse_loudnorm_json(
        _run_ffmpeg(
            ["-hide_banner", "-nostats", *trim, "-af",
             f"{fade},loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
             "-f", "null", "-"],
            docker=docker, label=f"{track['output']} の loudnorm 計測",
        )
    )
    _run_ffmpeg(
        ["-hide_banner", "-nostats", "-y", *trim, "-af",
         f"{fade},{loudnorm_filter(measured)}", "-c:a", "aac", "-b:a", "128k",
         "-ar", "48000", "-ac", "2", destination_arg],
        docker=docker, label=f"{track['output']} の書き出し",
    )


def copy_provisional(track: dict[str, Any]) -> None:
    """加工済み暫定ファイルを trackNN へそのままコピーする。"""
    source = _source_path(track)
    if not source.is_file():
        raise ManifestError(f"暫定 BGM がありません: {source}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, OUT_DIR / track["output"])


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init-provisional", action="store_true")
    parser.add_argument("--no-docker", action="store_true")
    parser.add_argument("--sql-only", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.init_provisional:
        TRACKS_PATH.parent.mkdir(parents=True, exist_ok=True)
        if TRACKS_PATH.exists():
            print(f"エラー: すでに存在します: {TRACKS_PATH}", file=sys.stderr)
            return 1
        TRACKS_PATH.write_text(
            json.dumps(PROVISIONAL_TEMPLATE, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"暫定トラックを登録しました: {TRACKS_PATH}")
        return 0
    try:
        tracks = validate_tracks(json.loads(TRACKS_PATH.read_text(encoding="utf-8")))
        if not args.sql_only:
            for track in tracks:
                if track["provisional"]:
                    copy_provisional(track)
                    print(f"{track['output']}: 暫定ファイルを無加工でコピー")
                else:
                    process_track(track, docker=not args.no_docker)
                    print(f"{track['output']}: 24 秒・fade 0.5/1.0 秒・-14 LUFS")
        SQL_PATH.parent.mkdir(parents=True, exist_ok=True)
        SQL_PATH.write_text(generate_audio_assets_sql(tracks), encoding="utf-8")
    except (OSError, ValueError, FfmpegError, json.JSONDecodeError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    print(f"登録 SQL: {SQL_PATH}")
    for track in tracks:
        label = "暫定（publish 不可）" if track["provisional"] else "正式"
        print(f"{label}: {OUT_DIR / track['output']} -> s3://$S3_BUCKET_NAME/{track['s3_key']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
