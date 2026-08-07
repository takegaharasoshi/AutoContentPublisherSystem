"""Caption placeholder expansion."""

from __future__ import annotations

import re
from typing import Any

from .quiz_items import fetch_quiz_item


PLACEHOLDERS = {
    "hook",
    "question",
    "answer",
    "explanation",
    "coach_comment",
}
TOKEN_PATTERN = re.compile(r"\{\{([a-z_]+)\}\}")


def build_caption(
    cursor: Any,
    generation_run_id: int,
    template_text: str,
) -> str:
    """Expand supported placeholders, fetching quiz data only when needed."""
    tokens = set(TOKEN_PATTERN.findall(template_text))
    unknown = tokens - PLACEHOLDERS
    if unknown:
        raise RuntimeError(
            "Unknown caption placeholder: " + ", ".join(sorted(unknown))
        )
    if not tokens:
        return template_text

    quiz_item = fetch_quiz_item(cursor, generation_run_id)
    if quiz_item is None:
        raise RuntimeError(
            "quiz_items row is required for caption placeholder expansion: "
            f"generation_run_id={generation_run_id}"
        )

    values = {
        "question": quiz_item.question_text,
        "answer": quiz_item.answer_text,
        "hook": quiz_item.content_fields.get("hook"),
        "explanation": quiz_item.content_fields.get("explanation"),
        "coach_comment": quiz_item.content_fields.get("coach_comment"),
    }
    for token in tokens:
        value = values[token]
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"Caption expansion source is missing: {token}")

    caption = template_text
    for token in PLACEHOLDERS:
        value = values[token]
        if isinstance(value, str):
            caption = caption.replace("{{" + token + "}}", value)
    return caption
