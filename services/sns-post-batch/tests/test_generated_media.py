"""Tests for generated media repository functions."""

from unittest.mock import Mock

from app.generated_media import fetch_first_generated_media
from app.models import GeneratedMediaRef


def test_fetch_first_generated_media_returns_smallest_id_row() -> None:
    """The first generated media row is mapped to its storage reference."""
    cursor = Mock()
    cursor.fetchone.return_value = (7, "images", "images/set/a.jpg", "jpg")

    assert fetch_first_generated_media(cursor, 12) == GeneratedMediaRef(
        7, "images", "images/set/a.jpg", "jpg"
    )
    cursor.execute.assert_called_once_with(
        "SELECT id, s3_bucket, s3_key, file_format FROM generated_media "
        "WHERE generation_run_id = %s ORDER BY id LIMIT 1",
        (12,),
    )


def test_fetch_first_generated_media_returns_none_when_empty() -> None:
    """A generation run without media returns None."""
    cursor = Mock()
    cursor.fetchone.return_value = None

    assert fetch_first_generated_media(cursor, 12) is None
