"""UTC clock helpers."""

import datetime


def now_utc() -> datetime.datetime:
    """Return the current naive UTC datetime."""
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
