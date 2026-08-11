"""pref-ranking-1 の事前動画ビルドツールで共有するヘルパー。"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
import sys
from typing import Any, Iterable

import pymysql


SET_CODE = "pref-ranking-1"
DURATIONS = ("20s", "30s")
ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
WORK = BASE / "work"
REMOTION_DIR = BASE / "remotion"
LABELS = {
    "setLabel": "都道府県ランキング TOP5",
    "rankSuffix": "位",
    "searching": "第{rank}位は…？",
}

PREFECTURE_COMMON = ROOT / "content" / "ranking-stock" / SET_CODE / "common"
if str(PREFECTURE_COMMON) not in sys.path:
    sys.path.insert(0, str(PREFECTURE_COMMON))

from prefectures import PREFECTURE_BY_CODE  # noqa: E402


def local_connection() -> pymysql.connections.Connection:
    """ローカル Docker MySQL への接続を開く。"""
    return pymysql.connect(
        host=os.environ.get("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("LOCAL_DB_PORT", "3306")),
        user=os.environ.get("LOCAL_DB_USER", "app"),
        password=os.environ.get("LOCAL_DB_PASSWORD", "password"),
        database=os.environ.get("LOCAL_DB_NAME", "acps"),
        charset="utf8mb4",
        autocommit=False,
    )


def utc_now() -> datetime.datetime:
    """MySQL の DATETIME に保存できる naive UTC を返す。"""
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def load_json(path: Path, default: Any) -> Any:
    """JSON 生成物を読み、存在しない場合は既定値を返す。"""
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    """親ディレクトリを作成し、UTF-8 の JSON 生成物を書き出す。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _json_value(value: Any) -> Any:
    """MySQL の JSON 文字列を Python 値へ復元する。"""
    return json.loads(value) if isinstance(value, str) else value


def fetch_stock_rows(
    connection: pymysql.connections.Connection,
) -> list[dict[str, Any]]:
    """セットに属する有効なランキングストックを content_key 順で返す。"""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT r.id, r.content_key, r.title, r.content_fields, "
            "r.ranking_data, r.narration, r.video_s3_key_20s, "
            "r.video_s3_key_30s, r.video_audio_asset_id "
            "FROM ranking_stock_items r "
            "JOIN batch_sets b ON b.id = r.set_id "
            "WHERE b.set_code = %s AND r.is_active = 1 "
            "ORDER BY r.content_key ASC",
            (SET_CODE,),
        )
        rows = cursor.fetchall()
    return [
        {
            "id": int(row[0]),
            "content_key": str(row[1]),
            "title": str(row[2]),
            "content_fields": _json_value(row[3]),
            "ranking_data": _json_value(row[4]),
            "narration": _json_value(row[5]),
            "video_s3_key_20s": row[6],
            "video_s3_key_30s": row[7],
            "video_audio_asset_id": (
                None if row[8] is None else int(row[8])
            ),
        }
        for row in rows
    ]


def select_targets(
    rows: Iterable[dict[str, Any]],
    durations: Iterable[str],
    *,
    rebuild: bool,
    content_keys: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """各ストック行についてビルド対象尺を決める純関数。

    Args:
        rows: ``fetch_stock_rows`` が返す行。
        durations: 今回処理する尺。
        rebuild: 真ならビルド済み尺、偽なら未ビルド尺を対象にする。
        content_keys: 指定時に対象とする content_key。

    Returns:
        ``target_durations`` を追加した対象行。

    Raises:
        ValueError: 未対応の尺が含まれる場合。
    """
    selected_durations = tuple(dict.fromkeys(durations))
    unknown = set(selected_durations) - set(DURATIONS)
    if unknown:
        raise ValueError(f"未対応の尺です: {', '.join(sorted(unknown))}")
    key_filter = set(content_keys) if content_keys is not None else None
    targets: list[dict[str, Any]] = []
    for row in rows:
        if key_filter is not None and row.get("content_key") not in key_filter:
            continue
        target_durations = []
        for duration in selected_durations:
            built = row.get(f"video_s3_key_{duration}") is not None
            if built == rebuild:
                target_durations.append(duration)
        if target_durations:
            targets.append({**row, "target_durations": target_durations})
    return targets
