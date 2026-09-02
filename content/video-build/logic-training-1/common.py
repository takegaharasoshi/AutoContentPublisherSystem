"""Shared local-only helpers for the logic-training-1 video build tools."""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any

import pymysql


BASE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
WORK = BASE / "work"
REMOTION_DIR = BASE / "remotion"
SET_CODE = "logic-training-1"


def local_connection() -> pymysql.connections.Connection:
    """Open the local Docker MySQL connection used by build operations."""
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
    """Return a naive UTC datetime suitable for MySQL DATETIME."""
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def load_json(path: Path, default: Any) -> Any:
    """Load JSON from a work artifact, returning the supplied default if absent."""
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    """Write a UTF-8 JSON build artifact, creating its parent directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_unbuilt_items(
    connection: pymysql.connections.Connection,
    *,
    rebuild: bool = False,
) -> list[dict[str, Any]]:
    """Return active stock rows to build.

    既定は未ビルド行（``video_s3_key IS NULL``）。``rebuild`` ではレンダラー変更の
    反映を目的にビルド済み行を対象とし、選曲済みの ``video_audio_asset_id`` を
    そのまま使い回せるよう併せて返す（再ビルドで BGM を変えない）。
    """
    condition = "IS NOT NULL" if rebuild else "IS NULL"
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q.id, q.content_key, q.quiz_type, q.difficulty, q.question_text, "
            "q.answer_text, q.content_fields, q.video_audio_asset_id "
            "FROM quiz_stock_items q "
            "JOIN batch_sets b ON b.id = q.set_id "
            "WHERE b.set_code = %s AND q.is_active = 1 "
            f"AND q.video_s3_key {condition} ORDER BY q.id ASC",
            (SET_CODE,),
        )
        rows = cursor.fetchall()
    return [
        {
            "id": int(row[0]),
            "content_key": str(row[1]),
            "quiz_type": str(row[2]),
            "difficulty": str(row[3]),
            "question_text": str(row[4]),
            "answer_text": str(row[5]),
            "content_fields": json.loads(row[6]) if isinstance(row[6], str) else row[6],
            "video_audio_asset_id": None if row[7] is None else int(row[7]),
        }
        for row in rows
    ]


def _parse_slots(raw: str | None) -> list[dict[str, Any]]:
    """prompt_configs.parameters からスロット定義を検査して返す。"""
    try:
        parameters = json.loads(raw or "{}")
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("parameters は JSON オブジェクトにしてください") from exc
    if not isinstance(parameters, dict):
        raise RuntimeError("parameters は JSON オブジェクトにしてください")

    slots = parameters.get("slots")
    if not isinstance(slots, list) or not slots:
        raise RuntimeError("parameters.slots は空でない配列にしてください")
    required = {
        "from_jst_hour",
        "quiz_type",
        "difficulty",
        "slot_code",
        "slot_label",
        "slot_hook",
    }
    validated: list[dict[str, Any]] = []
    for index, slot in enumerate(slots):
        if not isinstance(slot, dict):
            raise RuntimeError(f"parameters.slots[{index}] はオブジェクトにしてください")
        missing = required - set(slot)
        if missing:
            raise RuntimeError(
                f"parameters.slots[{index}] の必須項目がありません: "
                + ", ".join(sorted(missing))
            )
        hour = slot["from_jst_hour"]
        if isinstance(hour, bool) or not isinstance(hour, int) or not 0 <= hour <= 23:
            raise RuntimeError(
                f"parameters.slots[{index}].from_jst_hour は 0〜23 の整数にしてください"
            )
        normalized: dict[str, Any] = {"from_jst_hour": hour}
        for field in required - {"from_jst_hour"}:
            value = slot[field]
            if not isinstance(value, str) or not value.strip():
                raise RuntimeError(
                    f"parameters.slots[{index}].{field} は空でない文字列にしてください"
                )
            normalized[field] = value.strip()
        validated.append(normalized)
    return validated


def resolve_slots(
    connection: pymysql.connections.Connection,
) -> dict[tuple[str, str], dict[str, str]]:
    """Derive one deterministic palette slot for every type/difficulty pair."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT p.parameters FROM prompt_configs p "
            "JOIN batch_sets b ON b.id = p.set_id "
            "WHERE b.set_code = %s AND p.is_active = 1",
            (SET_CODE,),
        )
        parameter_rows = cursor.fetchall()
    candidates: dict[tuple[str, str], set[tuple[str, str]]] = {}
    for (parameters,) in parameter_rows:
        for slot in _parse_slots(parameters):
            key = (slot["quiz_type"], slot["difficulty"])
            candidates.setdefault(key, set()).add(
                (slot["slot_code"], slot["slot_label"], slot["slot_hook"])
            )
    resolved: dict[tuple[str, str], dict[str, str]] = {}
    for key, values in candidates.items():
        if len(values) != 1:
            raise RuntimeError(
                "prompt_configs の slots が一意に決まりません: "
                f"quiz_type/difficulty={key}"
            )
        slot_code, slot_label, slot_hook = next(iter(values))
        resolved[key] = {
            "slot_code": slot_code,
            "slot_label": slot_label,
            "slot_hook": slot_hook,
        }
    return resolved
