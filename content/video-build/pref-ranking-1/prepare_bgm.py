"""pref-ranking-1 の BGM を前処理し、audio_assets 登録 SQL まで書き出す。

調達・前処理・登録の運用ルールは docs/app/operation.html セクション 3
「音源の調達・前処理・登録」、セット固有の構成は
docs/app/sets/pref-ranking-1.html セクション 6 が正。

本セット固有の前処理仕様（他セットとの差分）:

* **尺は動画と同じ 30 秒ちょうど**に切り出す。コンポジションは曲が尺より短ければ
  ループするが（remotion/src/PrefRankingVideo.tsx の ``<Audio loop>``）、
  30 秒に満たない曲を使うと動画内でループの継ぎ目が鳴る。
* **フェードは焼き込まない**。頭 0.5 秒 / 尻 1.5 秒のフェードはコンポジション側が
  掛ける（remotion/src/audio.ts の ``bgmVolumeAt``）。素材にも焼くと二重に掛かる。
* ラウドネスは共通ルールどおり 2 パス loudnorm（linear）で I=-14 LUFS に揃える。
  ミキシングゲイン ``BGM_GAIN`` は -13.8 LUFS の音源で校正した値のため、
  この基準から外れた素材を混ぜると曲ごとに BGM の音量が変わる。

ffmpeg は WSL ホストに無いため、既定では image-batch イメージの中で実行する
（build.py のラウドネス正規化と同じ方式）。

使い方:

    # 1. 原曲を work/bgm/source/ に置き、work/bgm/tracks.json に証跡を書く
    python prepare_bgm.py --init          # tracks.json の雛形を書き出す
    # 2. 前処理（work/bgm/out/trackNN.m4a）+ 登録 SQL の生成
    python prepare_bgm.py
    # 3. 試聴のうえ S3 へ配置し、SQL を両環境へ適用する（--print-upload で手順表示）
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from common import BASE, ROOT, SET_CODE, WORK


BGM_DIR = WORK / "bgm"
SOURCE_DIR = BGM_DIR / "source"
OUT_DIR = BGM_DIR / "out"
MANIFEST_PATH = BGM_DIR / "tracks.json"
SQL_PATH = (
    ROOT / "content" / "ranking-stock" / SET_CODE / "set-registration"
    / "03_audio_assets.sql"
)

DURATION_SECONDS = 30
"""切り出す尺（秒）。30 秒版の動画と同尺にしてループの継ぎ目を作らない。"""

TARGET_I = -14.0
TARGET_TP = -1.5
TARGET_LRA = 11.0
AUDIO_BITRATE = "128k"
SAMPLE_RATE = "48000"

REQUIRED_KEYS = ("file", "start", "title", "source_url", "license_type", "acquired_at")
OPTIONAL_KEYS = ("license_note", "output")
ACQUIRED_AT_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

MANIFEST_TEMPLATE = [
    {
        "file": "example-source.mp3",
        "start": 0,
        "title": "曲名（管理用表示名）",
        "source_url": "https://pixabay.com/music/.../",
        "license_type": "Pixabay License",
        "license_note": None,
        "acquired_at": "2026-08-26",
    }
]


class ManifestError(ValueError):
    """tracks.json の内容が前処理の前提を満たさないことを表す。"""


class FfmpegError(RuntimeError):
    """ffmpeg の実行に失敗したことを表す。"""


def validate_manifest(entries: object) -> list[dict[str, object]]:
    """tracks.json を検査し、正規化した音源定義を返す。

    Args:
        entries: tracks.json をパースした値。

    Returns:
        ``output`` を補完した音源定義のリスト。

    Raises:
        ManifestError: 件数・必須キー・値の形式・ライセンス種別が不正な場合。
    """
    if not isinstance(entries, list) or not entries:
        raise ManifestError("tracks.json は 1 件以上の配列である必要があります")
    if not 3 <= len(entries) <= 5:
        raise ManifestError(
            f"BGM は 3〜5 曲で登録します（現在 {len(entries)} 件）。"
            "docs/app/operation.html セクション 3"
        )

    validated: list[dict[str, object]] = []
    seen_outputs: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ManifestError(f"[{index}] 各要素はオブジェクトである必要があります")
        missing = [key for key in REQUIRED_KEYS if key not in entry]
        if missing:
            raise ManifestError(f"[{index}] 必須キーがありません: {', '.join(missing)}")
        unknown = set(entry) - set(REQUIRED_KEYS) - set(OPTIONAL_KEYS)
        if unknown:
            raise ManifestError(f"[{index}] 未知のキー: {', '.join(sorted(unknown))}")

        for key in ("file", "title", "source_url", "license_type", "acquired_at"):
            value = entry[key]
            if not isinstance(value, str) or not value.strip():
                raise ManifestError(f"[{index}] {key} は空でない文字列が必要です")
        start = entry["start"]
        if isinstance(start, bool) or not isinstance(start, (int, float)) or start < 0:
            raise ManifestError(f"[{index}] start は 0 以上の秒数が必要です")
        if not ACQUIRED_AT_PATTERN.match(str(entry["acquired_at"])):
            raise ManifestError(f"[{index}] acquired_at は YYYY-MM-DD 形式が必要です")

        license_type = str(entry["license_type"])
        if re.search(r"\bNC\b|NonCommercial|非商用", license_type, re.IGNORECASE):
            raise ManifestError(
                f"[{index}] 非商用ライセンス（{license_type}）は使用できません"
            )
        if re.search(r"CC[- ]?BY(?![- ]?SA)", license_type, re.IGNORECASE):
            print(
                f"WARNING: [{index}] {license_type} はクレジット表記の運用が必要です"
                "（原則は CC0 / Pixabay License を選ぶ）",
                file=sys.stderr,
            )

        output = entry.get("output") or f"track{index:02d}.m4a"
        if not isinstance(output, str) or not output.endswith(".m4a"):
            raise ManifestError(f"[{index}] output は .m4a のファイル名が必要です")
        if output in seen_outputs:
            raise ManifestError(f"[{index}] output が重複しています: {output}")
        seen_outputs.add(output)

        normalized = {key: entry[key] for key in REQUIRED_KEYS}
        normalized["license_note"] = entry.get("license_note")
        normalized["output"] = output
        validated.append(normalized)
    return validated


def s3_key(output: str) -> str:
    """前処理済み音源の S3 キーを返す。"""
    return f"audio/{SET_CODE}/{output}"


def _sql_literal(value: str) -> str:
    """生成 SQL 用の MySQL 文字列リテラルを返す。"""
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def _sql_value(value: object) -> str:
    """NULL 許容カラム用のリテラルを返す。"""
    if value is None:
        return "NULL"
    return _sql_literal(str(value))


def generate_audio_assets_sql(tracks: list[dict[str, object]]) -> str:
    """audio_assets への INSERT 文を生成する。

    Args:
        tracks: ``validate_manifest`` が返した音源定義。

    Returns:
        両環境へ適用できる SQL スクリプト。set_id は set_code から解決する。
    """
    lines = [
        f"-- {SET_CODE} セット登録 (3/3): audio_assets（BGM）",
        "-- prepare_bgm.py が work/bgm/tracks.json から生成する（手書きしない）。",
        "-- 前処理済み音源を S3 の audio/" + SET_CODE + "/ へ配置してから適用する。",
        "-- time_slot は NULL（スロット共通の汎用曲）。証跡 3 点は本テーブルに記録する",
        "-- （docs/app/operation.html セクション 3。別ドキュメントで管理しない）。",
        "",
    ]
    for index, track in enumerate(tracks, start=1):
        key = s3_key(str(track["output"]))
        lines.extend(
            [
                f"-- ({index}) {track['title']}",
                "INSERT INTO audio_assets (set_id, s3_key, asset_type, time_slot, "
                "title, source_url, license_type, license_note, acquired_at, "
                "duration_seconds, is_active)",
                f"SELECT b.id, {_sql_literal(key)}, 'bgm', NULL,",
                f"       {_sql_literal(str(track['title']))},",
                f"       {_sql_literal(str(track['source_url']))},",
                f"       {_sql_literal(str(track['license_type']))},",
                f"       {_sql_value(track['license_note'])},",
                f"       {_sql_literal(str(track['acquired_at']) + ' 00:00:00')},",
                f"       {DURATION_SECONDS}, 1",
                "FROM batch_sets b",
                f"WHERE b.set_code = {_sql_literal(SET_CODE)};",
                "",
            ]
        )
    return "\n".join(lines)


def _container_path(path: Path) -> str:
    """リポジトリ内のホストパスを /repo マウント上のパスへ変換する。"""
    return (Path("/repo") / path.resolve().relative_to(ROOT.resolve())).as_posix()


def ffmpeg_command(args: list[str], *, docker: bool) -> list[str]:
    """ffmpeg の実行コマンドを組み立てる。

    Args:
        args: ffmpeg に渡す引数（パスはコンテナ側に変換済みであること）。
        docker: image-batch イメージ経由で実行するか。

    Returns:
        subprocess へ渡すコマンド。
    """
    if not docker:
        return [os.environ.get("FFMPEG_BIN", "ffmpeg"), *args]
    image = os.environ.get("FFMPEG_IMAGE", "image-batch:ffmpeg-check")
    return [
        "docker", "run", "--rm", "-u", f"{os.getuid()}:{os.getgid()}",
        "-v", f"{ROOT}:/repo", "-w", _container_path(BASE),
        "--entrypoint", "ffmpeg", image,
        *args,
    ]


def _run_ffmpeg(args: list[str], *, docker: bool, label: str) -> str:
    """ffmpeg を実行し、標準エラー出力（ログ）を返す。"""
    command = ffmpeg_command(args, docker=docker)
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise FfmpegError(f"{label}: 実行できません（{exc}）") from exc
    if completed.returncode != 0:
        tail = "\n".join(completed.stderr.strip().splitlines()[-8:])
        raise FfmpegError(f"{label} が失敗しました（{completed.returncode}）:\n{tail}")
    return completed.stderr


def parse_loudnorm_json(stderr: str) -> dict[str, str]:
    """loudnorm の 1 パス目（計測）の JSON を読み取る。

    Args:
        stderr: ffmpeg の標準エラー出力。

    Returns:
        ``input_i`` 等の計測値。

    Raises:
        FfmpegError: JSON が見つからない、または壊れている場合。
    """
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start < 0 or end < start:
        raise FfmpegError("loudnorm の計測 JSON が見つかりません")
    try:
        return json.loads(stderr[start : end + 1])
    except json.JSONDecodeError as exc:
        raise FfmpegError(f"loudnorm の計測 JSON が不正です: {exc}") from exc


def parse_ebur128_summary(stderr: str) -> dict[str, float]:
    """ebur128 の集計行から I / LRA / True Peak を読み取る。"""
    summary = stderr[stderr.rfind("Integrated loudness"):]
    values: dict[str, float] = {}
    for key, pattern in (
        ("integrated", r"I:\s*(-?\d+(?:\.\d+)?) LUFS"),
        ("lra", r"LRA:\s*(-?\d+(?:\.\d+)?) LU"),
        ("true_peak", r"Peak:\s*(-?\d+(?:\.\d+)?) dBFS"),
    ):
        match = re.search(pattern, summary)
        if match is None:
            raise FfmpegError(f"ffmpeg の出力から {key} を読み取れません")
        values[key] = float(match.group(1))
    return values


def loudnorm_filter(measured: dict[str, str]) -> str:
    """2 パス目（線形適用）の loudnorm フィルタ式を返す。"""
    return (
        f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
        f":measured_I={measured['input_i']}"
        f":measured_TP={measured['input_tp']}"
        f":measured_LRA={measured['input_lra']}"
        f":measured_thresh={measured['input_thresh']}"
        f":offset={measured['target_offset']}:linear=true:print_format=summary"
    )


def process_track(
    track: dict[str, object], *, docker: bool, duration: int
) -> dict[str, float]:
    """1 曲を切り出し → 2 パス loudnorm → AAC 化し、実測ラウドネスを返す。"""
    source = SOURCE_DIR / str(track["file"])
    if not source.is_file():
        raise FfmpegError(f"原曲がありません: {source}")
    destination = OUT_DIR / str(track["output"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    start = str(track["start"])
    source_arg = _container_path(source) if docker else str(source)
    destination_arg = _container_path(destination) if docker else str(destination)

    trim = ["-ss", start, "-i", source_arg, "-t", str(duration)]
    measured = parse_loudnorm_json(
        _run_ffmpeg(
            [
                "-hide_banner", "-nostats", *trim,
                "-af", f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
                       ":print_format=json",
                "-f", "null", "-",
            ],
            docker=docker,
            label=f"{track['output']} の計測",
        )
    )
    _run_ffmpeg(
        [
            "-hide_banner", "-nostats", "-y", *trim,
            "-af", loudnorm_filter(measured),
            "-c:a", "aac", "-b:a", AUDIO_BITRATE, "-ar", SAMPLE_RATE, "-ac", "2",
            destination_arg,
        ],
        docker=docker,
        label=f"{track['output']} の書き出し",
    )
    stderr = _run_ffmpeg(
        ["-hide_banner", "-nostats", "-i", destination_arg,
         "-af", "ebur128=peak=true", "-f", "null", "-"],
        docker=docker,
        label=f"{track['output']} の実測",
    )
    values = parse_ebur128_summary(stderr)
    values["duration"] = _probe_duration(stderr)
    return values


def _probe_duration(stderr: str) -> float:
    """ffmpeg のログから入力尺（秒）を読み取る。"""
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", stderr)
    if match is None:
        return 0.0
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def main(argv: list[str] | None = None) -> int:
    """CLI エントリポイント。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--init", action="store_true", help="tracks.json の雛形を書き出して終了する"
    )
    parser.add_argument(
        "--duration", type=int, default=DURATION_SECONDS,
        help="切り出す尺（秒）。既定は 30 秒版の動画と同尺",
    )
    parser.add_argument(
        "--no-docker", action="store_true",
        help="ホストの ffmpeg を直接使う（既定は image-batch イメージ経由）",
    )
    parser.add_argument(
        "--sql-only", action="store_true", help="音声処理を行わず SQL だけ再生成する"
    )
    args = parser.parse_args(argv)

    if args.init:
        SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        if MANIFEST_PATH.exists():
            print(f"すでに存在します: {MANIFEST_PATH}")
            return 0
        MANIFEST_PATH.write_text(
            json.dumps(MANIFEST_TEMPLATE, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"雛形を書き出しました: {MANIFEST_PATH}")
        print(f"原曲は {SOURCE_DIR} に置いてください")
        return 0

    if not MANIFEST_PATH.is_file():
        print(f"エラー: {MANIFEST_PATH} がありません（--init で雛形を作成）", file=sys.stderr)
        return 1
    try:
        tracks = validate_manifest(json.loads(MANIFEST_PATH.read_text(encoding="utf-8")))
    except (ManifestError, json.JSONDecodeError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    failures: list[str] = []
    if not args.sql_only:
        for track in tracks:
            try:
                values = process_track(
                    track, docker=not args.no_docker, duration=args.duration
                )
            except FfmpegError as exc:
                failures.append(str(exc))
                print(f"エラー: {exc}", file=sys.stderr)
                continue
            gap = abs(values["duration"] - args.duration)
            warning = "  ※尺が想定と違います" if gap > 0.2 else ""
            print(
                f"{track['output']}: I={values['integrated']} LUFS / "
                f"LRA={values['lra']} LU / TP={values['true_peak']} dBFS / "
                f"{values['duration']:.2f}s{warning}"
            )
    if failures:
        return 1

    SQL_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQL_PATH.write_text(generate_audio_assets_sql(tracks), encoding="utf-8")
    print(f"登録 SQL: {SQL_PATH}")
    print("次の手順:")
    print(f"  1. {OUT_DIR} の m4a を試聴する（頭切れ・ノイズ・曲の入り）")
    print("  2. S3 へ配置する:")
    for track in tracks:
        print(
            f"       aws s3 cp {OUT_DIR / str(track['output'])} "
            f"s3://$S3_BUCKET_NAME/{s3_key(str(track['output']))}"
        )
    print("  3. SQL をローカル MySQL と Aurora の両環境へ適用する")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
