"""Repository and key helpers for generated media."""

from __future__ import annotations

import datetime
from typing import Any


def build_s3_key(
    set_code: str,
    scheduled_at: datetime.datetime,
    generation_run_id: int,
    prompt_config_id: int,
    output_index: int,
    *,
    prefix: str,
    extension: str,
    suffix: str = "",
) -> str:
    """Build a deterministic S3 key for final or intermediate media.

    Args:
        set_code: External batch set code.
        scheduled_at: Scheduled UTC timestamp.
        generation_run_id: Generation run ID.
        prompt_config_id: Prompt configuration ID.
        output_index: Generator output position.
        prefix: Top-level media prefix, such as ``images`` or ``videos``.
        extension: Filename extension without a leading dot.
        suffix: Optional filename suffix before the extension.

    Returns:
        Deterministic S3 object key.
    """
    return (
        f"{prefix}/{set_code}/{scheduled_at:%Y%m%d}/{generation_run_id}/"
        f"{prompt_config_id}_{output_index}{suffix}.{extension}"
    )


def has_generated_media(
    cursor: Any,
    generation_run_id: int,
    prompt_config_id: int,
) -> bool:
    """Return whether a prompt configuration has any generated media.

    Args:
        cursor: Database cursor.
        generation_run_id: Generation run ID.
        prompt_config_id: Prompt configuration ID.

    Returns:
        ``True`` if at least one media row exists.
    """
    cursor.execute(
        "SELECT 1 FROM generated_media WHERE generation_run_id = %s "
        "AND prompt_config_id = %s LIMIT 1",
        (generation_run_id, prompt_config_id),
    )
    return cursor.fetchone() is not None


def insert_generated_media(
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
    file_format: str,
    file_size_bytes: int,
    width: int | None,
    height: int | None,
    duration_seconds: int | None,
    audio_asset_id: int | None,
    generated_at: datetime.datetime,
) -> int:
    """Insert generated-media metadata and return the new row ID.

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
        file_format: Final media file format.
        file_size_bytes: Stored object size.
        width: Media width in pixels, if known.
        height: Media height in pixels, if known.
        duration_seconds: Video duration, or ``None`` for images.
        audio_asset_id: Composited audio asset ID, if any.
        generated_at: UTC generation timestamp.

    Returns:
        Newly inserted generated-media ID.
    """
    cursor.execute(
        "INSERT INTO generated_media "
        "(set_id, generation_run_id, prompt_config_id, output_index, "
        "prompt_text_snapshot, negative_prompt_snapshot, parameters_snapshot, "
        "s3_key, s3_bucket, file_format, file_size_bytes, width, height, "
        "duration_seconds, audio_asset_id, generated_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
        "%s, %s, %s)",
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
            file_format,
            file_size_bytes,
            width,
            height,
            duration_seconds,
            audio_asset_id,
            generated_at,
        ),
    )
    return cursor.lastrowid
