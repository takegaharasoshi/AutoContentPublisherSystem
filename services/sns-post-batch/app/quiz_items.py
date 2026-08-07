"""Repository functions for generated quiz items."""

from __future__ import annotations

import json
from typing import Any

from .models import QuizItem


def fetch_quiz_item(cursor: Any, generation_run_id: int) -> QuizItem | None:
    """Fetch and JSON-decode the quiz item for one generation run."""
    cursor.execute(
        "SELECT question_text, answer_text, content_fields FROM quiz_items "
        "WHERE generation_run_id = %s LIMIT 1",
        (generation_run_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None

    raw_fields = row[2]
    if isinstance(raw_fields, (bytes, bytearray)):
        raw_fields = raw_fields.decode("utf-8")
    if isinstance(raw_fields, str):
        try:
            raw_fields = json.loads(raw_fields)
        except json.JSONDecodeError as exc:
            raise RuntimeError("quiz_items.content_fields is invalid JSON") from exc
    if not isinstance(raw_fields, dict):
        raise RuntimeError("quiz_items.content_fields must be a JSON object")
    return QuizItem(row[0], row[1], raw_fields)
