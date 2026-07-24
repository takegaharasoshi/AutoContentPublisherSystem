"""Repository functions for post-image associations."""

from __future__ import annotations

from typing import Any

import pymysql


def ensure_post_image(
    cursor: Any,
    *,
    post_id: int,
    generated_image_id: int,
) -> None:
    """Insert the first image association, ignoring a duplicate association."""
    try:
        cursor.execute(
            "INSERT INTO post_media (post_id, generated_media_id, display_order) "
            "VALUES (%s, %s, 0)",
            (post_id, generated_image_id),
        )
    except pymysql.err.IntegrityError as exc:
        if not exc.args or exc.args[0] != pymysql.constants.ER.DUP_ENTRY:
            raise
