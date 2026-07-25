"""Prompt processing and generated-media persistence."""

from __future__ import annotations

import datetime
import logging
from dataclasses import dataclass
from typing import Any

from acps_shared.s3 import put_object

from .clock import now_utc
from .generators import GeneratorContext, GeneratorFn, IntermediateOutput
from .media import build_s3_key, has_generated_media, insert_generated_media
from .models import PromptConfig


logger = logging.getLogger(__name__)

FILE_FORMATS: dict[str, tuple[str, str]] = {
    "jpg": ("images", "image/jpeg"),
    "mp4": ("videos", "video/mp4"),
}


@dataclass(frozen=True)
class ProcessingResult:
    """Result of processing active prompt configurations."""

    new_media_inserted: int
    all_prompt_configs_complete: bool


def process_prompt_configs(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    set_code: str,
    scheduled_at: datetime.datetime,
    generation_run_id: int,
    prompt_configs: list[PromptConfig],
    generator: GeneratorFn,
    s3_bucket: str,
    s3_client: Any,
) -> ProcessingResult:
    """Generate, store, and register media for active prompt configurations.

    Each media object is independently attempted so a storage or metadata
    failure does not stop other outputs. Completion is determined from a final DB
    recheck, including prompt configurations skipped as already complete.

    Args:
        cursor: Database cursor.
        connection: Database connection used to commit successful media rows.
        set_id: Batch set ID.
        set_code: Batch set code used in the S3 key.
        scheduled_at: Scheduled UTC timestamp.
        generation_run_id: Current generation run ID.
        prompt_configs: Active prompt configurations to process.
        generator: Final-media generation implementation.
        s3_bucket: Destination S3 bucket.
        s3_client: S3 client used for uploads.

    Returns:
        Count of newly inserted media and final completion status.
    """
    new_media_inserted = 0
    for prompt_config in prompt_configs:
        if has_generated_media(cursor, generation_run_id, prompt_config.id):
            logger.info(
                "既に完了済みのためスキップ: prompt_config_id=%s",
                prompt_config.id,
            )
            continue

        try:
            generated = generator(
                GeneratorContext(
                    prompt_config=prompt_config,
                    cursor=cursor,
                    s3_client=s3_client,
                    s3_bucket=s3_bucket,
                )
            )
        except Exception as exc:
            connection.rollback()
            logger.error(
                "生成方式の呼び出しに失敗: prompt_config_id=%s type=%s",
                prompt_config.id,
                type(exc).__name__,
            )
            continue

        if not generated.media:
            connection.rollback()
            logger.error(
                "生成方式が0件のメディアを返却: prompt_config_id=%s",
                prompt_config.id,
            )
            continue

        for output_index, media in enumerate(generated.media):
            try:
                prefix, content_type = FILE_FORMATS[media.file_format]
            except KeyError:
                connection.rollback()
                logger.error(
                    "未知のファイル形式: prompt_config_id=%s "
                    "output_index=%s file_format=%s",
                    prompt_config.id,
                    output_index,
                    media.file_format,
                )
                continue

            for intermediate in _intermediates_for(
                generated.intermediates, output_index
            ):
                _store_intermediate(
                    intermediate,
                    prefix=prefix,
                    set_code=set_code,
                    scheduled_at=scheduled_at,
                    generation_run_id=generation_run_id,
                    prompt_config_id=prompt_config.id,
                    s3_bucket=s3_bucket,
                    s3_client=s3_client,
                )

            key = build_s3_key(
                set_code,
                scheduled_at,
                generation_run_id,
                prompt_config.id,
                output_index,
                prefix=prefix,
                extension=media.file_format,
            )
            try:
                put_object(
                    s3_bucket,
                    key,
                    media.content,
                    content_type=content_type,
                    client=s3_client,
                )
                insert_generated_media(
                    cursor,
                    set_id=set_id,
                    generation_run_id=generation_run_id,
                    prompt_config_id=prompt_config.id,
                    output_index=output_index,
                    prompt_text_snapshot=prompt_config.prompt_text,
                    negative_prompt_snapshot=prompt_config.negative_prompt,
                    parameters_snapshot=prompt_config.parameters,
                    s3_key=key,
                    s3_bucket=s3_bucket,
                    file_format=media.file_format,
                    file_size_bytes=len(media.content),
                    width=media.width,
                    height=media.height,
                    duration_seconds=media.duration_seconds,
                    audio_asset_id=media.audio_asset_id,
                    generated_at=now_utc(),
                )
                connection.commit()
                new_media_inserted += 1
            except Exception:
                connection.rollback()
                logger.exception(
                    "メディアの保存に失敗（S3孤児は許容）: "
                    "prompt_config_id=%s output_index=%s",
                    prompt_config.id,
                    output_index,
                )
                continue

    all_complete = all(
        has_generated_media(cursor, generation_run_id, prompt_config.id)
        for prompt_config in prompt_configs
    )
    return ProcessingResult(new_media_inserted, all_complete)


def _intermediates_for(
    intermediates: list[IntermediateOutput],
    output_index: int,
) -> list[IntermediateOutput]:
    """Return intermediate artifacts belonging to one final media output."""
    return [
        intermediate
        for intermediate in intermediates
        if intermediate.output_index == output_index
    ]


def _store_intermediate(
    intermediate: IntermediateOutput,
    *,
    prefix: str,
    set_code: str,
    scheduled_at: datetime.datetime,
    generation_run_id: int,
    prompt_config_id: int,
    s3_bucket: str,
    s3_client: Any,
) -> None:
    """Best-effort upload of a debug-only intermediate artifact."""
    try:
        _, content_type = FILE_FORMATS[intermediate.file_format]
        key = build_s3_key(
            set_code,
            scheduled_at,
            generation_run_id,
            prompt_config_id,
            intermediate.output_index,
            prefix=prefix,
            extension=intermediate.file_format,
            suffix=intermediate.suffix,
        )
        put_object(
            s3_bucket,
            key,
            intermediate.content,
            content_type=content_type,
            client=s3_client,
        )
    except Exception:
        logger.warning(
            "中間生成物の保存に失敗（処理続行）: "
            "prompt_config_id=%s output_index=%s suffix=%s",
            prompt_config_id,
            intermediate.output_index,
            intermediate.suffix,
            exc_info=True,
        )
