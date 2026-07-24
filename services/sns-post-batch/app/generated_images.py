"""Repository functions for generated images used in posts."""

from __future__ import annotations

from typing import Any

from .models import GeneratedImageRef


def fetch_first_generated_image(
    cursor: Any,
    generation_run_id: int,
) -> GeneratedImageRef | None:
    """Fetch the first generated image for a generation run.

    Args:
        cursor: Database cursor.
        generation_run_id: Generation run ID.

    Returns:
        The image with the smallest ID, or ``None`` when no image exists.
    """
    cursor.execute(
        "SELECT id, s3_bucket, s3_key FROM generated_media "
        "WHERE generation_run_id = %s ORDER BY id LIMIT 1",
        (generation_run_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return GeneratedImageRef(id=row[0], s3_bucket=row[1], s3_key=row[2])
