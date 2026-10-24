"""Write the comment reply problem snapshot after a reel is published."""

from __future__ import annotations

import datetime
import json
from typing import Any

from acps_shared.s3 import put_object

from .clock import now_utc
from .quiz_items import fetch_quiz_snapshot_item
from .umigame_items import fetch_umigame_item


CONTENT_TYPE = "application/json; charset=utf-8"


def _posted_at_utc(posted_at: datetime.datetime) -> str:
    """Format the exact posts.posted_at value as an ISO 8601 UTC timestamp."""
    if posted_at.tzinfo is None:
        posted_at = posted_at.replace(tzinfo=datetime.UTC)
    return posted_at.astimezone(datetime.UTC).isoformat().replace("+00:00", "Z")


def write_problem_snapshot(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    set_code: str,
    generation_run_id: int,
    media_id: str,
    posted_at: datetime.datetime,
    s3_bucket: str,
    s3_client: Any,
) -> bool:
    """Upload one snapshot for this run's umigame or quiz item.

    The caller commits the successful post before invoking this function and
    rolls back this function's transaction if it raises. Quiz snapshots do not
    write to the database.
    """
    item = fetch_umigame_item(cursor, generation_run_id)
    if item is None:
        quiz_item = fetch_quiz_snapshot_item(cursor, generation_run_id)
        if quiz_item is None:
            return False
        if (
            not isinstance(quiz_item.question_text, str)
            or not quiz_item.question_text.strip()
        ):
            raise RuntimeError("quiz_items.question_text is NULL or empty")
        if (
            not isinstance(quiz_item.answer_text, str)
            or not quiz_item.answer_text.strip()
        ):
            raise RuntimeError("quiz_items.answer_text is NULL or empty")

        key = f"assets/{set_code}/problems/{media_id}.json"
        snapshot = {
            "schema_version": 1,
            "kind": "quiz",
            "set_code": set_code,
            "media_id": media_id,
            "posted_at": _posted_at_utc(posted_at),
            "quiz_type": quiz_item.quiz_type,
            "difficulty": quiz_item.difficulty,
            "question_text": quiz_item.question_text,
            "answer_text": quiz_item.answer_text,
            "explanation": quiz_item.content_fields.get("explanation"),
            "hint": quiz_item.content_fields.get("hint"),
            "source": "post",
        }
        put_object(
            s3_bucket,
            key,
            json.dumps(snapshot, ensure_ascii=False).encode("utf-8"),
            content_type=CONTENT_TYPE,
            client=s3_client,
        )
        return True

    if (
        not isinstance(item.core_points, list)
        or not item.core_points
        or not isinstance(item.judge_criteria, dict)
        or not isinstance(item.core_words, dict)
        or not isinstance(item.reveal_text, str)
        or not item.reveal_text.strip()
    ):
        raise RuntimeError(
            "umigame_items.core_points / judge_criteria / core_words / reveal_text is NULL or empty; "
            "apply V013, V014 and V017 and update the umigame_stock_items rows before publishing snapshots"
        )

    cursor.execute(
        "SELECT prompt_text FROM prompt_configs "
        "WHERE set_id = %s AND is_active = 1 ORDER BY id LIMIT 1",
        (set_id,),
    )
    prompt_row = cursor.fetchone()
    if (
        prompt_row is None
        or not isinstance(prompt_row[0], str)
        or not prompt_row[0].strip()
    ):
        raise RuntimeError(
            f"Active prompt_configs.prompt_text is missing: set_id={set_id}"
        )

    key = f"assets/{set_code}/problems/{media_id}.json"
    snapshot = {
        "schema_version": 4,
        "set_code": set_code,
        "media_id": media_id,
        "content_key": item.content_key,
        "posted_at": _posted_at_utc(posted_at),
        "problem_text": item.problem_text,
        "truth": item.truth,
        "fact_sheet": item.fact_sheet,
        "core_points": item.core_points,
        "judge_criteria": item.judge_criteria,
        "core_words": item.core_words,
        "reveal_text": item.reveal_text,
        "rule_text": item.rule_text,
        "master_rules": prompt_row[0],
    }
    put_object(
        s3_bucket,
        key,
        json.dumps(snapshot, ensure_ascii=False).encode("utf-8"),
        content_type=CONTENT_TYPE,
        client=s3_client,
    )
    cursor.execute(
        "UPDATE umigame_items SET snapshot_s3_key = %s, "
        "snapshot_written_at = %s WHERE id = %s",
        (key, now_utc(), item.id),
    )
    connection.commit()
    return True
