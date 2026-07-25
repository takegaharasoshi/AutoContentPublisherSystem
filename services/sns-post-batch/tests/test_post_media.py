"""Tests for post-media repository functions."""

from unittest.mock import Mock

import pymysql
import pytest

from app.post_media import ensure_post_media


def test_ensure_post_media_inserts_display_order_zero() -> None:
    """The first media association has display order zero."""
    cursor = Mock()

    ensure_post_media(cursor, post_id=4, generated_media_id=8)

    cursor.execute.assert_called_once_with(
        "INSERT INTO post_media (post_id, generated_media_id, display_order) "
        "VALUES (%s, %s, 0)",
        (4, 8),
    )


def test_ensure_post_media_ignores_duplicate() -> None:
    """A duplicate association is safe during a resumed attempt."""
    cursor = Mock()
    cursor.execute.side_effect = pymysql.err.IntegrityError(1062, "duplicate")

    ensure_post_media(cursor, post_id=4, generated_media_id=8)


def test_ensure_post_media_reraises_other_integrity_errors() -> None:
    """Non-duplicate database errors remain visible to processing."""
    cursor = Mock()
    cursor.execute.side_effect = pymysql.err.IntegrityError(1452, "foreign key")

    with pytest.raises(pymysql.err.IntegrityError):
        ensure_post_media(cursor, post_id=4, generated_media_id=8)
