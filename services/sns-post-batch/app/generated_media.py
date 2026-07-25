"""Repository functions for generated media used in posts."""

from __future__ import annotations

from typing import Any

from .models import GeneratedMediaRef


def fetch_first_generated_media(
    cursor: Any,
    generation_run_id: int,
) -> GeneratedMediaRef | None:
    """Fetch the first generated media item for a generation run.

    Args:
        cursor: Database cursor.
        generation_run_id: Generation run ID.

    Returns:
        The media item with the smallest ID, or ``None`` when none exists.
    """
    cursor.execute(
        "SELECT id, s3_bucket, s3_key, file_format FROM generated_media "
        "WHERE generation_run_id = %s ORDER BY id LIMIT 1",
        (generation_run_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return GeneratedMediaRef(
        id=row[0],
        s3_bucket=row[1],
        s3_key=row[2],
        file_format=row[3],
    )
