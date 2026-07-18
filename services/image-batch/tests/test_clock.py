"""Tests for UTC clock helpers."""

import datetime

from app.clock import now_utc


def test_now_utc_returns_naive_current_utc_time() -> None:
    """The clock result has no timezone and falls within the call interval."""
    before = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    value = now_utc()
    after = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)

    assert value.tzinfo is None
    assert before <= value <= after
