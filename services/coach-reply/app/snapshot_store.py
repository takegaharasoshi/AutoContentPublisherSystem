"""Look up only quiz snapshots in the configured S3 prefix."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from app.state_store import read_json


def snapshot_from_answer(answer: dict) -> dict:
    """Build the schema-v1 backfill/evaluation snapshot from a Data API row."""
    fields = answer.get("content_fields") or {}
    if isinstance(fields, str):
        fields = json.loads(fields)
    if not isinstance(fields, dict):
        raise ValueError("content_fields must be a JSON object")
    posted_at = answer.get("posted_at")
    if posted_at:
        posted = datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
        if posted.tzinfo is None:
            posted = posted.replace(tzinfo=timezone.utc)
        posted_at = posted.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": 1, "kind": "quiz", "set_code": "logic-training-1",
        "media_id": str(answer["media_id"]), "posted_at": posted_at,
        "quiz_type": answer.get("quiz_type"), "difficulty": answer.get("difficulty"),
        "question_text": answer["question_text"], "answer_text": answer["answer_text"],
        "explanation": fields.get("explanation"), "hint": fields.get("hint"),
        "source": "backfill",
    }


def get_snapshot(
    bucket: str, prefix: str, media_id: str, *, client: Any = None,
) -> dict | None:
    """Return None for an absent key or a snapshot of another kind."""
    data = read_json(bucket, f"{prefix}{media_id}.json", client=client)
    if data is None or data.get("kind") != "quiz":
        return None
    if data.get("media_id") != media_id:
        raise ValueError("snapshot media_id does not match requested media_id")
    for field in ("question_text", "answer_text"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"quiz snapshot has no {field}")
    return data
