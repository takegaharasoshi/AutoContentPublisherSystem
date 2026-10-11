"""Caption placeholder expansion."""

from __future__ import annotations

import re
from typing import Any

from .quiz_items import fetch_quiz_item
from .ranking_items import fetch_ranking_item
from .models import PreviousUmigameTruth
from .umigame_items import fetch_previous_umigame_truth, fetch_umigame_item


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
UMIGAME_PLACEHOLDERS = {
    "caption",
    "problem_text",
    "hook",
    "rule_text",
    "prev_truth_block",
}
# Expands to an empty string on the set's first post.
OPTIONAL_PLACEHOLDERS = {"prev_truth_block"}
# Instagram caption limit, enforced when the previous truth is inserted.
MAX_CAPTION_LENGTH = 2200
KNOWN_PLACEHOLDERS = (
    QUIZ_PLACEHOLDERS | RANKING_PLACEHOLDERS | UMIGAME_PLACEHOLDERS
)
TOKEN_PATTERN = re.compile(r"\{\{([a-z_]+)\}\}")


def build_prev_truth_block(previous: PreviousUmigameTruth | None) -> str:
    """Build the previous-truth block appended after the hashtags.

    Args:
        previous: Previous problem, or ``None`` on the set's first post.

    Returns:
        Three blank lines, the spoiler header, four dot lines and the truth,
        or an empty string when there is no previous post.
    """
    if previous is None:
        return ""
    return (
        "\n\n\n\n"
        f"――― 前回の問題「{previous.title}」の真相（ネタバレ注意）―――\n"
        "・\n・\n・\n・\n"
        "【真相】\n"
        f"{previous.truth}"
    )


def build_caption(
    cursor: Any,
    generation_run_id: int,
    template_text: str,
    *,
    set_id: int | None = None,
) -> str:
    """Expand supported placeholders from the run's generated item.

    Args:
        cursor: Database cursor.
        generation_run_id: Generation run being posted.
        template_text: Caption template text.
        set_id: Batch set ID. Required when the template uses
            ``{{prev_truth_block}}``.

    Returns:
        The expanded caption.

    Raises:
        RuntimeError: On unknown or incompatible placeholders, missing
            sources, or a caption over the limit after inserting the
            previous truth.
    """
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
        if ranking_item is not None:
            placeholders = RANKING_PLACEHOLDERS
            values = {
                "hook": ranking_item.content_fields.get("hook"),
                "title": ranking_item.title,
                "result_list": ranking_item.content_fields.get("result_list"),
                "trivia": ranking_item.content_fields.get("trivia"),
                "source_display": ranking_item.content_fields.get("source_display"),
            }
        else:
            umigame_item = fetch_umigame_item(cursor, generation_run_id)
            if umigame_item is None:
                raise RuntimeError(
                    "quiz_items or ranking_items or umigame_items row is "
                    "required for caption placeholder expansion: "
                    f"generation_run_id={generation_run_id}"
                )
            placeholders = UMIGAME_PLACEHOLDERS
            values = {
                "caption": umigame_item.caption,
                "problem_text": umigame_item.problem_text,
                "hook": umigame_item.hook,
                "rule_text": umigame_item.rule_text,
            }
            if "prev_truth_block" in tokens:
                if set_id is None:
                    raise RuntimeError(
                        "set_id is required for {{prev_truth_block}} expansion"
                    )
                values["prev_truth_block"] = build_prev_truth_block(
                    fetch_previous_umigame_truth(
                        cursor, set_id, generation_run_id
                    )
                )

    mismatched = tokens - placeholders
    if mismatched:
        raise RuntimeError(
            "Caption placeholder is incompatible with the generation item: "
            + ", ".join(sorted(mismatched))
        )
    for token in tokens - OPTIONAL_PLACEHOLDERS:
        value = values[token]
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"Caption expansion source is missing: {token}")

    caption = template_text
    for token in placeholders:
        value = values.get(token)
        if isinstance(value, str):
            caption = caption.replace("{{" + token + "}}", value)
    if "prev_truth_block" in tokens and len(caption) > MAX_CAPTION_LENGTH:
        raise RuntimeError(
            "Caption exceeds the limit after inserting the previous truth: "
            f"{len(caption)} > {MAX_CAPTION_LENGTH}"
        )
    return caption
