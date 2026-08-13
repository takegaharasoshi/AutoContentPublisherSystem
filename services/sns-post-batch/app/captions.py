"""Caption placeholder expansion."""

from __future__ import annotations

import re
from typing import Any

from .quiz_items import fetch_quiz_item
from .ranking_items import fetch_ranking_item


QUIZ_PLACEHOLDERS = {
    "hook",
    "question",
    "answer",
    "explanation",
    "coach_comment",
}
RANKING_PLACEHOLDERS = {
    "hook",
    "title",
    "result_list",
    "trivia",
    "source_display",
}
KNOWN_PLACEHOLDERS = QUIZ_PLACEHOLDERS | RANKING_PLACEHOLDERS
TOKEN_PATTERN = re.compile(r"\{\{([a-z_]+)\}\}")


def build_caption(
    cursor: Any,
    generation_run_id: int,
    template_text: str,
) -> str:
    """Expand supported placeholders from the run's quiz or ranking item."""
    tokens = set(TOKEN_PATTERN.findall(template_text))
    unknown = tokens - KNOWN_PLACEHOLDERS
    if unknown:
        raise RuntimeError(
            "Unknown caption placeholder: " + ", ".join(sorted(unknown))
        )
    if not tokens:
        return template_text

    quiz_item = fetch_quiz_item(cursor, generation_run_id)
    if quiz_item is not None:
        placeholders = QUIZ_PLACEHOLDERS
        values = {
            "question": quiz_item.question_text,
            "answer": quiz_item.answer_text,
            "hook": quiz_item.content_fields.get("hook"),
            "explanation": quiz_item.content_fields.get("explanation"),
            "coach_comment": quiz_item.content_fields.get("coach_comment"),
        }
    else:
        ranking_item = fetch_ranking_item(cursor, generation_run_id)
        if ranking_item is None:
            raise RuntimeError(
                "quiz_items or ranking_items row is required for caption "
                "placeholder expansion: "
                f"generation_run_id={generation_run_id}"
            )
        placeholders = RANKING_PLACEHOLDERS
        values = {
            "hook": ranking_item.content_fields.get("hook"),
            "title": ranking_item.title,
            "result_list": ranking_item.content_fields.get("result_list"),
            "trivia": ranking_item.content_fields.get("trivia"),
            "source_display": ranking_item.content_fields.get("source_display"),
        }

    mismatched = tokens - placeholders
    if mismatched:
        raise RuntimeError(
            "Caption placeholder is incompatible with the generation item: "
            + ", ".join(sorted(mismatched))
        )
    for token in tokens:
        value = values[token]
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"Caption expansion source is missing: {token}")

    caption = template_text
    for token in placeholders:
        value = values[token]
        if isinstance(value, str):
            caption = caption.replace("{{" + token + "}}", value)
    return caption
