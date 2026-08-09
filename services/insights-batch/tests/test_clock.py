"""Tests for UTC clock parsing."""

import datetime

import pytest

from app.clock import parse_scheduled_at


def test_parse_scheduled_at() -> None:
    """The scheduler timestamp becomes a naive UTC datetime."""
    assert parse_scheduled_at("2026-08-10T09:00:00Z") == datetime.datetime(
        2026, 8, 10, 9
    )


def test_parse_scheduled_at_rejects_invalid_format() -> None:
    """Only the workflow contract format is accepted."""
    with pytest.raises(ValueError):
        parse_scheduled_at("2026-08-10")
