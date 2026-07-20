"""UTC clock helpers."""

from __future__ import annotations

import datetime


def now_utc() -> datetime.datetime:
    """Return the current naive UTC datetime."""
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
