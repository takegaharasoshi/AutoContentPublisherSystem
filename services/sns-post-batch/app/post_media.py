"""Repository functions for post-media associations."""

from __future__ import annotations

from typing import Any

import pymysql


def ensure_post_media(
    cursor: Any,
    *,
    post_id: int,
    generated_media_id: int,
) -> None:
    """Insert the first media association, ignoring a duplicate association."""
    try:
        cursor.execute(
            "INSERT INTO post_media (post_id, generated_media_id, display_order) "
            "VALUES (%s, %s, 0)",
            (post_id, generated_media_id),
        )
    except pymysql.err.IntegrityError as exc:
        if not exc.args or exc.args[0] != pymysql.constants.ER.DUP_ENTRY:
            raise
