"""Media type helpers for SNS post creation."""

from __future__ import annotations


MEDIA_TYPE_FEED_IMAGE = "feed_image"
MEDIA_TYPE_REEL = "reel"


def derive_media_type(file_format: str) -> str:
    """Derive the post media type from a generated media file format.

    Args:
        file_format: Stored generated media file format.

    Returns:
        ``reel`` for MP4 media, otherwise ``feed_image``.
    """
    if file_format.strip().lower() == "mp4":
        return MEDIA_TYPE_REEL
    return MEDIA_TYPE_FEED_IMAGE
