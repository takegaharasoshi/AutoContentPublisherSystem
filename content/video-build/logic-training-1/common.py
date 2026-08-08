"""Shared local-only helpers for the logic-training-1 video build tools."""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
import sys
from typing import Any

import pymysql


ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent / "work"
SET_CODE = "logic-training-1"

for source_root in (ROOT / "services" / "image-batch", ROOT / "shared"):
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))


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


def fetch_unbuilt_items(connection: pymysql.connections.Connection) -> list[dict[str, Any]]:
    """Return active stock rows whose prebuilt video has not been registered."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q.id, q.quiz_type, q.difficulty, q.question_text, "
            "q.answer_text, q.content_fields FROM quiz_stock_items q "
            "JOIN batch_sets b ON b.id = q.set_id "
            "WHERE b.set_code = %s AND q.is_active = 1 "
            "AND q.video_s3_key IS NULL ORDER BY q.id ASC",
            (SET_CODE,),
        )
        rows = cursor.fetchall()
    return [
        {
            "id": int(row[0]),
            "quiz_type": str(row[1]),
            "difficulty": str(row[2]),
            "question_text": str(row[3]),
            "answer_text": str(row[4]),
            "content_fields": json.loads(row[5]) if isinstance(row[5], str) else row[5],
        }
        for row in rows
    ]


def resolve_slots(connection: pymysql.connections.Connection) -> dict[tuple[str, str], dict[str, str]]:
    """Derive one deterministic palette slot for every type/difficulty pair."""
    from app.generators.gpt_quiz_multicut import _parse_parameters

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
        for slot in _parse_parameters(parameters):
            key = (slot["quiz_type"], slot["difficulty"])
            candidates.setdefault(key, set()).add(
                (slot["slot_code"], slot["slot_label"])
            )
    resolved: dict[tuple[str, str], dict[str, str]] = {}
    for key, values in candidates.items():
        if len(values) != 1:
            raise RuntimeError(
                "prompt_configs slots do not uniquely resolve "
                f"quiz_type/difficulty={key}"
            )
        slot_code, slot_label = next(iter(values))
        resolved[key] = {"slot_code": slot_code, "slot_label": slot_label}
    return resolved
