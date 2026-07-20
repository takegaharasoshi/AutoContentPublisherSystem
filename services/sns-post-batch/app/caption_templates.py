"""Repository functions for caption templates."""

from __future__ import annotations

from typing import Any

from .models import CaptionTemplate


def fetch_active_caption_template(
    cursor: Any,
    set_id: int,
) -> CaptionTemplate | None:
    """Fetch the first active caption template ordered by ID.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.

    Returns:
        The first active template, or ``None`` when no template is configured.
    """
    cursor.execute(
        "SELECT id, template_text FROM caption_templates "
        "WHERE set_id = %s AND is_active = 1 ORDER BY id LIMIT 1",
        (set_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return CaptionTemplate(id=row[0], template_text=row[1])
