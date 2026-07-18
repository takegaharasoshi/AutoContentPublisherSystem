"""Tests for generation run helpers."""

import datetime
from unittest.mock import Mock

import pymysql
import pytest

from app.generation_runs import parse_scheduled_at, resolve_generation_run


def test_parse_scheduled_at_returns_naive_utc_datetime() -> None:
    """The configured UTC format is parsed without tzinfo."""
    assert parse_scheduled_at("2026-07-19T00:00:00Z") == datetime.datetime(2026, 7, 19)


@pytest.mark.parametrize("raw", ["", "2026-07-19", "2026-07-19T00:00:00+00:00"])
def test_parse_scheduled_at_rejects_invalid_format(raw: str) -> None:
    """Only the exact UTC input format is valid."""
    with pytest.raises(ValueError):
        parse_scheduled_at(raw)


def test_resolve_generation_run_returns_new_id() -> None:
    """A new generation run returns its insert ID."""
    cursor = Mock(lastrowid=7)
    scheduled_at = datetime.datetime(2026, 7, 19)

    assert resolve_generation_run(cursor, set_id=3, scheduled_at=scheduled_at) == 7


def test_resolve_generation_run_fetches_duplicate_id() -> None:
    """An idempotency duplicate returns the existing run ID."""
    cursor = Mock()
    cursor.execute.side_effect = [pymysql.err.IntegrityError(1062, "duplicate"), None]
    cursor.fetchone.return_value = (8,)
    scheduled_at = datetime.datetime(2026, 7, 19)

    assert resolve_generation_run(cursor, set_id=3, scheduled_at=scheduled_at) == 8
    cursor.execute.assert_called_with(
        "SELECT id FROM generation_runs WHERE set_id = %s AND scheduled_at = %s",
        (3, scheduled_at),
    )
