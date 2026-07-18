"""Prompt processing and generated-image persistence."""

from __future__ import annotations

import datetime
import logging
from dataclasses import dataclass
from typing import Any

from acps_shared.s3 import put_object

from .clock import now_utc
from .generators import GeneratorFn
from .images import build_s3_key, has_generated_image, insert_generated_image
from .models import PromptConfig


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProcessingResult:
    """Result of processing active prompt configurations."""

    new_images_inserted: int
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
    """Generate, store, and register images for active prompt configurations.

    Each image is independently attempted so a storage or metadata failure does
    not stop other image outputs. Completion is determined from a final DB
    recheck, including prompt configurations skipped as already complete.

    Args:
        cursor: Database cursor.
        connection: Database connection used to commit successful image rows.
        set_id: Batch set ID.
        set_code: Batch set code used in the S3 key.
        scheduled_at: Scheduled UTC timestamp.
        generation_run_id: Current generation run ID.
        prompt_configs: Active prompt configurations to process.
        generator: Image generation implementation.
        s3_bucket: Destination S3 bucket.
        s3_client: S3 client used for uploads.

    Returns:
        Count of newly inserted images and final completion status.
    """
    new_images_inserted = 0
    for prompt_config in prompt_configs:
        if has_generated_image(cursor, generation_run_id, prompt_config.id):
            logger.info(
                "既に完了済みのためスキップ: prompt_config_id=%s",
                prompt_config.id,
            )
            continue

        try:
            generated = generator(prompt_config)
        except Exception as exc:
            logger.error(
                "生成方式の呼び出しに失敗: prompt_config_id=%s type=%s",
                prompt_config.id,
                type(exc).__name__,
            )
            continue

        if not generated:
            logger.error(
                "生成方式が0件の画像を返却: prompt_config_id=%s",
                prompt_config.id,
            )
            continue

        for output_index, image_bytes in enumerate(generated):
            key = build_s3_key(
                set_code,
                scheduled_at,
                generation_run_id,
                prompt_config.id,
                output_index,
            )
            try:
                put_object(
                    s3_bucket,
                    key,
                    image_bytes,
                    content_type="image/jpeg",
                    client=s3_client,
                )
                insert_generated_image(
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
                    file_size_bytes=len(image_bytes),
                    generated_at=now_utc(),
                )
                connection.commit()
                new_images_inserted += 1
            except Exception:
                logger.exception(
                    "画像の保存に失敗（S3孤児は許容）: "
                    "prompt_config_id=%s output_index=%s",
                    prompt_config.id,
                    output_index,
                )
                continue

    all_complete = all(
        has_generated_image(cursor, generation_run_id, prompt_config.id)
        for prompt_config in prompt_configs
    )
    return ProcessingResult(new_images_inserted, all_complete)
