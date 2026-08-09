"""Tests for insights batch data models."""

import datetime

from app.models import BatchSet, Post, SnsAccount


def test_models_are_value_objects() -> None:
    """Repository rows have immutable, comparable representations."""
    assert BatchSet(1, "set-a", True) == BatchSet(1, "set-a", True)
    assert SnsAccount(2, "instagram", "main", "Main").platform == "instagram"
    assert Post(3, "reel", "media", datetime.datetime(2026, 8, 10)).id == 3
