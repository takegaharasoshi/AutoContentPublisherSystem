"""Tests for post media type derivation."""

import pytest

from app.media_types import (
    MEDIA_TYPE_FEED_IMAGE,
    MEDIA_TYPE_REEL,
    derive_media_type,
)


@pytest.mark.parametrize(
    ("file_format", "expected"),
    [
        ("mp4", MEDIA_TYPE_REEL),
        ("MP4", MEDIA_TYPE_REEL),
        ("jpg", MEDIA_TYPE_FEED_IMAGE),
        ("png", MEDIA_TYPE_FEED_IMAGE),
    ],
)
def test_derive_media_type(file_format: str, expected: str) -> None:
    """Only MP4 media is posted as an Instagram reel."""
    assert derive_media_type(file_format) == expected
