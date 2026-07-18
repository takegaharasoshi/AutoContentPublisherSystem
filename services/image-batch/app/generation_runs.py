"""Repository functions for idempotent generation runs."""

import datetime
from typing import Any

import pymysql


def parse_scheduled_at(raw: str) -> datetime.datetime:
    """Parse a UTC ISO 8601 timestamp into a naive UTC datetime.

    Args:
        raw: Timestamp in ``YYYY-MM-DDTHH:MM:SSZ`` format.

    Returns:
        A naive UTC datetime.

    Raises:
        ValueError: If the timestamp has an invalid format.
    """
    return datetime.datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ")


def resolve_generation_run(
    cursor: Any,
    *,
    set_id: int,
    scheduled_at: datetime.datetime,
) -> int:
    """Insert or find a generation run and return its ID.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.
        scheduled_at: Scheduled UTC timestamp.

    Returns:
        The generation run ID.
    """
    try:
        cursor.execute(
            "INSERT INTO generation_runs (set_id, scheduled_at) VALUES (%s, %s)",
            (set_id, scheduled_at),
        )
        return cursor.lastrowid
    except pymysql.err.IntegrityError as exc:
        if not exc.args or exc.args[0] != pymysql.constants.ER.DUP_ENTRY:
            raise

    cursor.execute(
        "SELECT id FROM generation_runs WHERE set_id = %s AND scheduled_at = %s",
        (set_id, scheduled_at),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError("Generation run was not found after duplicate insert")
    return row[0]
