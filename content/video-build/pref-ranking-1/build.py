"""pref-ranking-1 の対象抽出、TTS 合成、動画レンダリングを実行する。"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable

import boto3

from common import (
    BASE,
    DURATIONS,
    LABELS,
    REMOTION_DIR,
    ROOT,
    SET_CODE,
    WORK,
    PREFECTURE_BY_CODE,
    dump_json,
    fetch_stock_rows,
    load_json,
    local_connection,
    select_targets,
    utc_now,
)


SCRIPTS_DIR = REMOTION_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_timeline  # noqa: E402


REQUIRED_CONTENT_FIELDS = ("source_display", "value_suffix", "bg_motif")
LOUDNESS_PATTERN = re.compile(
    r"after:\s+I=(?P<i>-?\d+(?:\.\d+)?)\s+LUFS.*?"
    r"TP=(?P<tp>-?\d+(?:\.\d+)?)\s+dBFS"
)


class PropsValidationError(ValueError):
    """ストック行を Remotion props へ安全に変換できないことを表す。"""

    def __init__(self, errors: Iterable[str]) -> None:
        self.errors = list(errors)
        super().__init__(" / ".join(self.errors))


def resolve_bgm_source(row: dict[str, Any], *, rebuild: bool) -> int | None:
    """BGM を既存 ID から引き継ぐか LRU 選曲するか決める純関数。

    Args:
        row: ``video_audio_asset_id`` を含むランキングストック行。
        rebuild: 再ビルドとして処理するか。

    Returns:
        引き継ぐ audio_assets ID。``None`` は新規 LRU 選曲を表す。

    Raises:
        ValueError: 再ビルド行に既存 BGM の記録がない場合。
    """
    existing_id = row.get("video_audio_asset_id")
    if existing_id is not None:
        return int(existing_id)
    if rebuild:
        raise ValueError("再ビルド元の video_audio_asset_id が NULL です")
    return None


def _duration_timeline(duration: str) -> build_timeline.Timeline:
    """単一ソースの定数から指定尺のタイムラインを返す。"""
    spec = build_timeline.DURATION_SPECS.get(duration)
    if spec is None:
        raise ValueError(f"未対応の尺です: {duration}")
    return build_timeline.build_timeline(duration, spec)


def validate_props_input(row: dict[str, Any], duration: str) -> list[str]:
    """props 組み立て前のストック行を検査する純関数。

    Args:
        row: ランキングストック行。
        duration: 検査する尺。

    Returns:
        利用者が修正できる検査エラーの一覧。
    """
    errors: list[str] = []
    fields = row.get("content_fields")
    if not isinstance(fields, dict):
        errors.append("content_fields がオブジェクトではありません")
        fields = {}
    for key in REQUIRED_CONTENT_FIELDS:
        value = fields.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"content_fields.{key} がありません")

    ranking_data = row.get("ranking_data")
    entries = ranking_data.get("entries") if isinstance(ranking_data, dict) else None
    if not isinstance(entries, list):
        errors.append("ranking_data.entries が配列ではありません")
        entries = []
    ranks: list[int] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{index}] がオブジェクトではありません")
            continue
        rank = entry.get("rank")
        pref_code = entry.get("pref_code")
        value = entry.get("value")
        if not isinstance(rank, int):
            errors.append(f"entries[{index}].rank が整数ではありません")
        else:
            ranks.append(rank)
        if not isinstance(pref_code, int) or pref_code not in range(1, 48):
            errors.append(f"entries[{index}].pref_code は 1〜47 にしてください")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"entries[{index}].value が数値ではありません")
    if sorted(ranks) != [1, 2, 3, 4, 5]:
        errors.append("entries の rank は 1〜5 を重複なく 1 件ずつ指定してください")

    narration = row.get("narration")
    cue_texts = narration.get(duration) if isinstance(narration, dict) else None
    if not isinstance(cue_texts, dict):
        errors.append(f"narration.{duration} がオブジェクトではありません")
        cue_texts = {}
    expected = {anchor.id for anchor in _duration_timeline(duration).cue_anchors}
    actual = set(cue_texts)
    if actual != expected:
        missing = ", ".join(sorted(expected - actual)) or "なし"
        unknown = ", ".join(sorted(actual - expected)) or "なし"
        errors.append(
            f"narration.{duration} の cue が不一致です"
            f"（不足: {missing} / 余分: {unknown}）"
        )
    for cue_id, text in cue_texts.items():
        if not isinstance(text, str) or not text.strip():
            errors.append(f"narration.{duration}.{cue_id} が空です")
    return errors


def build_props(
    row: dict[str, Any],
    duration: str,
    *,
    background_src: str,
    bgm_src: str | None,
) -> dict[str, Any]:
    """ストック行から Remotion の ``PrefRankingProps`` を組み立てる。

    Raises:
        PropsValidationError: 必須フィールド、順位、cue が不正な場合。
    """
    errors = validate_props_input(row, duration)
    if errors:
        raise PropsValidationError(errors)
    fields = row["content_fields"]
    entries = []
    for entry in sorted(row["ranking_data"]["entries"], key=lambda item: item["rank"]):
        pref_code = entry["pref_code"]
        entries.append(
            {
                "rank": entry["rank"],
                "prefCode": pref_code,
                "prefName": PREFECTURE_BY_CODE[pref_code].name,
                "value": entry["value"],
            }
        )
    timeline = _duration_timeline(duration)
    texts = row["narration"][duration]
    cues = {
        anchor.id: {
            "id": anchor.id,
            "text": texts[anchor.id],
            "audioSrc": None,
            "startFrame": anchor.anchor,
        }
        for anchor in timeline.cue_anchors
    }
    subtitle = fields.get("subtitle")
    value_prefix = fields.get("value_prefix")
    return {
        "duration": duration,
        "title": row["title"],
        "subtitle": subtitle if isinstance(subtitle, str) else None,
        "sourceDisplay": fields["source_display"],
        "valuePrefix": value_prefix if isinstance(value_prefix, str) else None,
        "valueSuffix": fields["value_suffix"],
        "backgroundSrc": background_src,
        "bgmSrc": bgm_src,
        "entries": entries,
        "cues": cues,
        "labels": dict(LABELS),
    }


def _parse_durations(value: str) -> tuple[str, ...]:
    """CLI のカンマ区切り尺を検査して返す。"""
    values = tuple(
        dict.fromkeys(item.strip() for item in value.split(",") if item.strip())
    )
    unknown = set(values) - set(DURATIONS)
    if not values or unknown:
        raise argparse.ArgumentTypeError(
            f"尺は {','.join(DURATIONS)} からカンマ区切りで指定してください"
        )
    return values


def _select_bgm(connection: Any, *, existing_id: int | None = None) -> tuple[int, str]:
    """既存 ID の指定時は引き継ぎ、それ以外は LRU で BGM を解決する。"""
    with connection.cursor() as cursor:
        if existing_id is None:
            cursor.execute(
                "SELECT a.id, a.s3_key FROM audio_assets a "
                "JOIN batch_sets b ON b.id = a.set_id "
                "WHERE b.set_code = %s AND a.asset_type = 'bgm' "
                "AND a.is_active = 1 AND a.time_slot IS NULL "
                "ORDER BY a.last_used_at ASC, a.id ASC LIMIT 1",
                (SET_CODE,),
            )
        else:
            cursor.execute(
                "SELECT a.id, a.s3_key FROM audio_assets a "
                "JOIN batch_sets b ON b.id = a.set_id "
                "WHERE b.set_code = %s AND a.id = %s AND a.asset_type = 'bgm'",
                (SET_CODE, existing_id),
            )
        row = cursor.fetchone()
    if row is None:
        if existing_id is None:
            raise RuntimeError("time_slot が NULL の有効な BGM がありません")
        raise RuntimeError(
            f"引き継ぎ用 BGM が見つかりません: audio_asset_id={existing_id}"
        )
    return int(row[0]), str(row[1])


def _record_bgm_use(connection: Any, bgm_id: int) -> None:
    """対象動画の完成後にだけ BGM の LRU 消費を記録する。"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE audio_assets SET last_used_at = %s WHERE id = %s",
                (utc_now(), bgm_id),
            )
            if cursor.rowcount != 1:
                raise RuntimeError(f"BGM の使用日時を更新できません: {bgm_id}")
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def _download_bgm(s3_key: str) -> Path:
    """未取得の BGM を Remotion public 配下へダウンロードする。"""
    destination = REMOTION_DIR / "public" / "bgm" / Path(s3_key).name
    if destination.is_file():
        return destination
    bucket = os.environ.get("S3_BUCKET_NAME")
    if not bucket:
        raise RuntimeError("BGM 取得には環境変数 S3_BUCKET_NAME が必要です")
    destination.parent.mkdir(parents=True, exist_ok=True)
    boto3.client("s3").download_file(bucket, s3_key, str(destination))
    return destination


def _container_path(path: Path) -> str:
    """リポジトリ内のホストパスを /repo マウント上のパスへ変換する。"""
    return (Path("/repo") / path.resolve().relative_to(ROOT.resolve())).as_posix()


def _run_command(command: list[str], label: str) -> subprocess.CompletedProcess[str]:
    """外部コマンドを実行し、失敗時に診断可能な例外を送出する。"""
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


def _render(props_path: Path, output_path: Path, duration: str) -> None:
    """remotion-render イメージで指定尺の動画をレンダリングする。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = os.environ.get("REMOTION_IMAGE", "remotion-render")
    command = [
        "docker", "run", "--rm", "-v", f"{ROOT}:/repo",
        "-w", _container_path(REMOTION_DIR), "-e", "HOME=/tmp",
        "--user", f"{os.getuid()}:{os.getgid()}", image,
        "npx", "remotion", "render", "src/index.ts",
        f"PrefRanking{duration}", _container_path(output_path),
        f"--props={_container_path(props_path)}", "--concurrency=3",
        "--timeout=120000",
    ]
    _run_command(command, f"Remotion {duration} レンダリング")


def _normalize(source: Path, destination: Path) -> tuple[float | None, float | None]:
    """image-batch イメージでラウドネスを正規化し実測値を返す。"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    image = os.environ.get("FFMPEG_IMAGE", "image-batch:ffmpeg-check")
    command = [
        "docker", "run", "--rm", "-u", f"{os.getuid()}:{os.getgid()}",
        "-v", f"{ROOT}:/repo", "-w", _container_path(REMOTION_DIR),
        "--entrypoint", "python", image, "scripts/normalize_loudness.py",
        _container_path(source), _container_path(destination),
    ]
    completed = _run_command(command, "ラウドネス正規化")
    match = LOUDNESS_PATTERN.search(completed.stdout)
    if match is None:
        return None, None
    return float(match.group("i")), float(match.group("tp"))


def _build_narration(props_path: Path, engine_url: str, name: str) -> int:
    """既存のナレーションビルダーをライブラリとして呼び出す。"""
    from build_narration import build_narration
    from tts import VoicevoxEngine

    return build_narration(
        props_path, engine=VoicevoxEngine(base_url=engine_url), name=name
    )


def _manifest_duration(
    video: Path, props: Path, loudness_i: float | None, loudness_tp: float | None
) -> dict[str, Any]:
    """環境非依存のリポジトリ相対パスで尺別台帳を作る。"""
    return {
        "video": video.relative_to(BASE).as_posix(),
        "props": props.relative_to(BASE).as_posix(),
        "loudness_i": loudness_i,
        "loudness_tp": loudness_tp,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rebuild", action="store_true",
        help="ビルド済み尺を既存 BGM のまま再ビルドする",
    )
    parser.add_argument(
        "--durations", type=_parse_durations, default=DURATIONS,
        help="対象尺（既定: 20s,30s）",
    )
    parser.add_argument(
        "--content-key", action="append", dest="content_keys",
        help="対象 content_key（複数指定可）",
    )
    parser.add_argument("--list", action="store_true", help="対象一覧を表示して終了する")
    parser.add_argument(
        "--engine", default="http://127.0.0.1:50021",
        help="VOICEVOX Engine URL",
    )
    parser.add_argument("--no-bgm", action="store_true", help="検証用: BGM なしでビルドする")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="props とナレーションまで作りレンダリングを省略する",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """対象を最後まで処理し、失敗をまとめて報告する。"""
    args = _parser().parse_args(argv)
    failures: list[str] = []
    manifest = load_json(WORK / "build_manifest.json", {})
    if not isinstance(manifest, dict):
        print("エラー: work/build_manifest.json は JSON オブジェクトにしてください", file=sys.stderr)
        return 1
    connection = local_connection()
    try:
        targets = select_targets(
            fetch_stock_rows(connection), args.durations,
            rebuild=args.rebuild, content_keys=args.content_keys,
        )
        if args.list:
            for row in targets:
                print(
                    f"{row['content_key']}\t"
                    f"{','.join(row['target_durations'])}\t{row['title']}"
                )
            print(f"対象: {len(targets)} 件")
            return 0

        for row in targets:
            content_key = row["content_key"]
            background_path = REMOTION_DIR / "public" / "bg" / f"{content_key}.jpg"
            if not background_path.is_file():
                failures.append(f"{content_key}: 背景 JPEG がありません: {background_path}")
                continue
            try:
                uses_lru_bgm = False
                if args.no_bgm:
                    bgm_id, bgm_s3_key, bgm_src = None, None, None
                else:
                    existing_id = resolve_bgm_source(row, rebuild=args.rebuild)
                    uses_lru_bgm = existing_id is None
                    bgm_id, bgm_s3_key = _select_bgm(
                        connection, existing_id=existing_id
                    )
                    bgm_path = _download_bgm(bgm_s3_key)
                    bgm_src = f"bgm/{bgm_path.name}"
                    source_label = "新規選曲" if uses_lru_bgm else "引き継ぎ"
                    print(
                        f"{content_key}: BGM {source_label} "
                        f"audio_asset_id={bgm_id}"
                    )
            except Exception as exc:
                failures.append(f"{content_key}: BGM の準備に失敗しました: {exc}")
                continue

            duration_records: dict[str, dict[str, Any]] = {}
            successful = []
            for duration in row["target_durations"]:
                props_path = WORK / "props" / f"{content_key}-{duration}.json"
                try:
                    props = build_props(
                        row, duration, background_src=f"bg/{content_key}.jpg",
                        bgm_src=bgm_src,
                    )
                    dump_json(props_path, props)
                    narration_status = _build_narration(
                        props_path, args.engine, f"{content_key}-{duration}"
                    )
                    if narration_status != 0:
                        raise RuntimeError("ナレーションの予算検査に失敗しました")
                    if args.dry_run:
                        successful.append(duration)
                        print(f"{content_key} {duration}: props・ナレーション生成 OK（dry-run）")
                        continue
                    raw_path = WORK / "out" / f"{content_key}_{duration}.raw.mp4"
                    video_path = WORK / "videos" / f"{content_key}_{duration}.mp4"
                    _render(props_path, raw_path, duration)
                    loudness_i, loudness_tp = _normalize(raw_path, video_path)
                    duration_records[duration] = _manifest_duration(
                        video_path, props_path, loudness_i, loudness_tp
                    )
                    successful.append(duration)
                    print(f"{content_key} {duration}: ビルド完了")
                except Exception as exc:
                    failures.append(f"{content_key} {duration}: {exc}")

            all_succeeded = set(successful) == set(row["target_durations"])
            if (
                not args.dry_run
                and all_succeeded
                and uses_lru_bgm
                and bgm_id is not None
            ):
                try:
                    _record_bgm_use(connection, bgm_id)
                except Exception as exc:
                    failures.append(f"{content_key}: BGM 使用日時の記録に失敗しました: {exc}")
                    all_succeeded = False
            if duration_records:
                previous = manifest.get(content_key, {})
                previous_durations = (
                    previous.get("durations", {})
                    if isinstance(previous, dict)
                    else {}
                )
                if not isinstance(previous_durations, dict):
                    previous_durations = {}
                manifest[content_key] = {
                    "content_key": content_key,
                    "stock_item_id": row["id"],
                    "title": row["title"],
                    "audio_asset_id": bgm_id,
                    "bgm_s3_key": bgm_s3_key,
                    "rebuild": args.rebuild,
                    "durations": {**previous_durations, **duration_records},
                }
                dump_json(WORK / "build_manifest.json", manifest)
            if all_succeeded and not args.dry_run:
                print(f"{content_key}: 対象尺をすべて完了しました")
    finally:
        connection.close()

    if failures:
        print("\n失敗一覧:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"完了: {len(targets)} 件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
