"""UTC clock helpers."""

from __future__ import annotations

import datetime


def now_utc() -> datetime.datetime:
    """Return the current naive UTC datetime."""
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)


def parse_scheduled_at(raw: str) -> datetime.datetime:
    """Parse a UTC ISO 8601 timestamp into a naive UTC datetime."""
    return datetime.datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ")
