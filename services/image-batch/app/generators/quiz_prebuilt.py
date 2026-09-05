"""Prebuilt-video quiz generator used at runtime."""

from __future__ import annotations

import logging
from typing import Any

from acps_shared.s3 import get_object

from ..clock import now_utc
from .contracts import GeneratorContext, GeneratorResult, MediaOutput
from .gpt_quiz_multicut import (
    _insert_quiz_item,
    _parse_parameters,
    resolve_slot,
    validate_content_fields,
)


logger = logging.getLogger(__name__)

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_DURATION_SECONDS = 16

# 版面に焼き込まれるのは hook / hint / question のみで、答え・解説・コーチの一言は
# キャプション専用（動画には出ない）。prebuilt 方式の動画はビルド時に版面適合を
# 検証済みのため、実行時にキャプション専用フィールドの長さを縛らない。
# 縛ると「答えが手順の問題は全手順を書く」（2026-08-31 ユーザー決定）と衝突し、
# 実際に 2026-09-04 夜の生成が answer_text 37 字で停止した。
CAPTION_ONLY_FIELDS = frozenset({"answer", "explanation", "coach_comment"})


def _fetch_prebuilt_stock_item(
    cursor: Any,
    set_id: int,
    quiz_type: str,
    difficulty: str,
) -> dict[str, Any]:
    """Fetch and validate the least-recently-used built stock item."""
    cursor.execute(
        "SELECT id, question_text, answer_text, content_fields, video_s3_key, "
        "video_audio_asset_id, last_used_at "
        "FROM quiz_stock_items WHERE set_id = %s AND quiz_type = %s "
        "AND difficulty = %s AND is_active = 1 AND video_s3_key IS NOT NULL "
        "ORDER BY last_used_at ASC, id ASC LIMIT 1",
        (set_id, quiz_type, difficulty),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(
            "No built active quiz stock item for "
            f"set_id={set_id} quiz_type={quiz_type} difficulty={difficulty}"
        )

    stock_id = int(row[0])
    question_text = row[1]
    answer_text = row[2]
    for name, value in (
        ("question_text", question_text),
        ("answer_text", answer_text),
    ):
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"quiz_stock_items.{name} is required")
    # question_text は版面に出るため上限を残す（answer_text はキャプション専用）
    if len(question_text) > 90:
        raise RuntimeError("quiz_stock_items.question_text exceeds 90 characters")

    fields = validate_content_fields(row[3], quiz_type, CAPTION_ONLY_FIELDS)
    video_s3_key = row[4]
    if not isinstance(video_s3_key, str) or not video_s3_key.strip():
        raise RuntimeError("quiz_stock_items.video_s3_key is required")
    if row[5] is None:
        raise RuntimeError(
            f"quiz_stock_items.video_audio_asset_id is required: stock_id={stock_id}"
        )

    if row[6] is not None:
        logger.warning(
            "Built quiz stock item is being reused: stock_id=%s quiz_type=%s "
            "difficulty=%s",
            stock_id,
            quiz_type,
            difficulty,
        )

    cursor.execute(
        "SELECT COUNT(*) FROM quiz_stock_items WHERE set_id = %s "
        "AND quiz_type = %s AND difficulty = %s AND is_active = 1 "
        "AND video_s3_key IS NULL",
        (set_id, quiz_type, difficulty),
    )
    unbuilt_count_row = cursor.fetchone()
    if unbuilt_count_row is not None and int(unbuilt_count_row[0]) > 0:
        logger.warning(
            "Active quiz stock items remain unbuilt: count=%s quiz_type=%s "
            "difficulty=%s",
            unbuilt_count_row[0],
            quiz_type,
            difficulty,
        )

    return {
        "id": stock_id,
        "question_text": question_text,
        "answer_text": answer_text,
        "content_fields": fields,
        "video_s3_key": video_s3_key,
        "video_audio_asset_id": int(row[5]),
    }


def generate(context: GeneratorContext) -> GeneratorResult:
    """Return one prebuilt quiz MP4 and stage its stock consumption."""
    slots = _parse_parameters(context.prompt_config.parameters)
    slot = resolve_slot(context.scheduled_at, slots)
    quiz_type = slot["quiz_type"]
    difficulty = slot["difficulty"]
    stock_item = _fetch_prebuilt_stock_item(
        context.cursor,
        context.prompt_config.set_id,
        quiz_type,
        difficulty,
    )

    video = get_object(
        context.s3_bucket,
        stock_item["video_s3_key"],
        client=context.s3_client,
    )
    _insert_quiz_item(
        context,
        stock_item["id"],
        quiz_type,
        difficulty,
        stock_item["question_text"],
        stock_item["answer_text"],
        stock_item["content_fields"],
    )
    context.cursor.execute(
        "UPDATE quiz_stock_items SET last_used_at = %s, "
        "use_count = use_count + 1 WHERE id = %s",
        (now_utc(), stock_item["id"]),
    )
    return GeneratorResult(
        media=[
            MediaOutput(
                content=video,
                file_format="mp4",
                width=OUTPUT_WIDTH,
                height=OUTPUT_HEIGHT,
                duration_seconds=OUTPUT_DURATION_SECONDS,
                audio_asset_id=stock_item["video_audio_asset_id"],
            )
        ]
    )
