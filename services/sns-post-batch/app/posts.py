"""Repository functions for post state and snapshots."""

from __future__ import annotations

import json
from typing import Any

import pymysql

from .clock import now_utc
from .models import Post


def get_post(
    cursor: Any,
    generation_run_id: int,
    sns_account_id: int,
) -> Post | None:
    """Fetch one post state for a generation run and SNS account."""
    cursor.execute(
        "SELECT id, status, platform_container_id, platform_post_id FROM posts "
        "WHERE generation_run_id = %s AND sns_account_id = %s",
        (generation_run_id, sns_account_id),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return Post(
        id=row[0],
        status=row[1],
        platform_container_id=row[2],
        platform_post_id=row[3],
    )


def create_pending_post(
    cursor: Any,
    *,
    set_id: int,
    generation_run_id: int,
    sns_account_id: int,
) -> int:
    """Create a pending post or return the existing post ID.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.
        generation_run_id: Generation run ID.
        sns_account_id: SNS account ID.

    Returns:
        The new or existing post ID.
    """
    try:
        cursor.execute(
            "INSERT INTO posts "
            "(set_id, generation_run_id, sns_account_id, status) "
            "VALUES (%s, %s, %s, 'pending')",
            (set_id, generation_run_id, sns_account_id),
        )
        return cursor.lastrowid
    except pymysql.err.IntegrityError as exc:
        if not exc.args or exc.args[0] != pymysql.constants.ER.DUP_ENTRY:
            raise

    cursor.execute(
        "SELECT id FROM posts "
        "WHERE generation_run_id = %s AND sns_account_id = %s",
        (generation_run_id, sns_account_id),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError("Post was not found after duplicate insert")
    return row[0]


def update_post_caption(
    cursor: Any,
    post_id: int,
    *,
    caption_template_id: int | None,
    caption_text: str,
) -> None:
    """Persist the caption template reference and text snapshot."""
    cursor.execute(
        "UPDATE posts SET caption_template_id = %s, "
        "caption_text_snapshot = %s WHERE id = %s",
        (caption_template_id, caption_text, post_id),
    )


def update_post_container_created(
    cursor: Any,
    post_id: int,
    *,
    platform_container_id: str,
) -> None:
    """Mark a post as having a platform container."""
    cursor.execute(
        "UPDATE posts SET status = 'container_created', "
        "platform_container_id = %s WHERE id = %s",
        (platform_container_id, post_id),
    )


def _encode_api_response(api_response: dict[str, Any] | None) -> str | None:
    """Encode an API response for a MySQL JSON column."""
    if api_response is None:
        return None
    return json.dumps(api_response)


def update_post_success(
    cursor: Any,
    post_id: int,
    *,
    platform_post_id: str,
    api_response: dict[str, Any] | None,
) -> None:
    """Mark a post successful and persist its platform response."""
    cursor.execute(
        "UPDATE posts SET status = 'success', platform_post_id = %s, "
        "api_response = %s, posted_at = %s WHERE id = %s",
        (platform_post_id, _encode_api_response(api_response), now_utc(), post_id),
    )


def update_post_failed(
    cursor: Any,
    post_id: int,
    *,
    error_message: str,
    api_response: dict[str, Any] | None,
) -> None:
    """Mark a post as clearly failed and persist diagnostic data."""
    cursor.execute(
        "UPDATE posts SET status = 'failed', error_message = %s, "
        "api_response = %s WHERE id = %s",
        (error_message, _encode_api_response(api_response), post_id),
    )


def update_post_unconfirmed(
    cursor: Any,
    post_id: int,
    *,
    error_message: str,
    api_response: dict[str, Any] | None,
) -> None:
    """Mark a post whose publish result cannot be confirmed."""
    cursor.execute(
        "UPDATE posts SET status = 'published_unconfirmed', error_message = %s, "
        "api_response = %s WHERE id = %s",
        (error_message, _encode_api_response(api_response), post_id),
    )
