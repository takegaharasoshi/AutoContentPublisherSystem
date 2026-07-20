"""Tests for generated image repository functions."""

from unittest.mock import Mock

from app.generated_images import fetch_first_generated_image
from app.models import GeneratedImageRef


def test_fetch_first_generated_image_returns_smallest_id_row() -> None:
    """The first generated image row is mapped to its storage reference."""
    cursor = Mock()
    cursor.fetchone.return_value = (7, "images", "images/set/a.jpg")

    assert fetch_first_generated_image(cursor, 12) == GeneratedImageRef(
        7, "images", "images/set/a.jpg"
    )
    cursor.execute.assert_called_once_with(
        "SELECT id, s3_bucket, s3_key FROM generated_images "
        "WHERE generation_run_id = %s ORDER BY id LIMIT 1",
        (12,),
    )


def test_fetch_first_generated_image_returns_none_when_empty() -> None:
    """A generation run without images returns None."""
    cursor = Mock()
    cursor.fetchone.return_value = None

    assert fetch_first_generated_image(cursor, 12) is None
