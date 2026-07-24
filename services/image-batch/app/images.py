"""Repository and key helpers for generated images."""

from __future__ import annotations

import datetime
from typing import Any


def build_s3_key(
    set_code: str,
    scheduled_at: datetime.datetime,
    generation_run_id: int,
    prompt_config_id: int,
    output_index: int,
) -> str:
    """Build the deterministic S3 key for one generated image.

    Args:
        set_code: External batch set code.
        scheduled_at: Scheduled UTC timestamp.
        generation_run_id: Generation run ID.
        prompt_config_id: Prompt configuration ID.
        output_index: Generator output position.

    Returns:
        S3 key ending in the JPEG filename for this output.
    """
    return (
        f"images/{set_code}/{scheduled_at:%Y%m%d}/{generation_run_id}/"
        f"{prompt_config_id}_{output_index}.jpg"
    )


def has_generated_image(
    cursor: Any,
    generation_run_id: int,
    prompt_config_id: int,
) -> bool:
    """Return whether a prompt configuration has any generated image.

    Args:
        cursor: Database cursor.
        generation_run_id: Generation run ID.
        prompt_config_id: Prompt configuration ID.

    Returns:
        ``True`` if at least one image row exists.
    """
    cursor.execute(
        "SELECT 1 FROM generated_media WHERE generation_run_id = %s "
        "AND prompt_config_id = %s LIMIT 1",
        (generation_run_id, prompt_config_id),
    )
    return cursor.fetchone() is not None


def insert_generated_image(
    cursor: Any,
    *,
    set_id: int,
    generation_run_id: int,
    prompt_config_id: int,
    output_index: int,
    prompt_text_snapshot: str,
    negative_prompt_snapshot: str | None,
    parameters_snapshot: str | None,
    s3_key: str,
    s3_bucket: str,
    file_size_bytes: int,
    generated_at: datetime.datetime,
) -> int:
    """Insert generated-image metadata and return the new row ID.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.
        generation_run_id: Generation run ID.
        prompt_config_id: Prompt configuration ID.
        output_index: Generator output position.
        prompt_text_snapshot: Prompt used to generate the image.
        negative_prompt_snapshot: Negative prompt used, if any.
        parameters_snapshot: Raw JSON parameter snapshot, if any.
        s3_key: Stored object key.
        s3_bucket: Stored object bucket.
        file_size_bytes: Stored object size.
        generated_at: UTC generation timestamp.

    Returns:
        Newly inserted generated-image ID.
    """
    cursor.execute(
        "INSERT INTO generated_media "
        "(set_id, generation_run_id, prompt_config_id, output_index, "
        "prompt_text_snapshot, negative_prompt_snapshot, parameters_snapshot, "
        "s3_key, s3_bucket, file_format, file_size_bytes, generated_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'jpg', %s, %s)",
        (
            set_id,
            generation_run_id,
            prompt_config_id,
            output_index,
            prompt_text_snapshot,
            negative_prompt_snapshot,
            parameters_snapshot,
            s3_key,
            s3_bucket,
            file_size_bytes,
            generated_at,
        ),
    )
    return cursor.lastrowid
