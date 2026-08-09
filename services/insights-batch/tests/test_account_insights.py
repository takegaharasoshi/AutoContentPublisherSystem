"""Tests for account insights date and persistence helpers."""

import datetime
import json

from app.account_insights import insert_account_insights, resolve_target_dates


def test_resolve_target_dates_initial_backfill_is_ninety_days() -> None:
    """An empty table triggers a full retention-window backfill."""
    dates = resolve_target_dates(None, datetime.date(2026, 8, 10))
    assert len(dates) == 90
    assert dates[0] == datetime.date(2026, 5, 12)
    assert dates[-1] == datetime.date(2026, 8, 9)


def test_resolve_target_dates_continues_after_latest() -> None:
    """Missing dates begin at MAX(metric_date) plus one."""
    assert resolve_target_dates(
        datetime.date(2026, 8, 7), datetime.date(2026, 8, 10)
    ) == [datetime.date(2026, 8, 8), datetime.date(2026, 8, 9)]


def test_resolve_target_dates_returns_empty_when_current() -> None:
    """No API call is needed when the latest closed day exists."""
    assert resolve_target_dates(
        datetime.date(2026, 8, 9), datetime.date(2026, 8, 10)
    ) == []


def test_resolve_target_dates_clips_old_latest_to_retention() -> None:
    """A stale MAX date cannot extend the Graph API retention window."""
    dates = resolve_target_dates(
        datetime.date(2020, 1, 1), datetime.date(2026, 8, 10)
    )
    assert len(dates) == 90
    assert dates[0] == datetime.date(2026, 5, 12)


class Cursor:
    """Cursor recording an INSERT IGNORE call."""

    def __init__(self, affected: int) -> None:
        self.affected = affected
        self.args = None

    def execute(self, query, args):
        self.args = args
        return self.affected


def test_insert_account_insights_serializes_unicode_json() -> None:
    """Metrics are passed as UTF-8-preserving JSON and affected rows become bool."""
    cursor = Cursor(1)
    assert insert_account_insights(
        cursor,
        set_id=1,
        sns_account_id=2,
        metric_date=datetime.date(2026, 8, 9),
        metrics={"label": "日本語"},
        followers_count=3,
        collected_at=datetime.datetime(2026, 8, 10),
        api_version="v25.0",
    )
    assert json.loads(cursor.args[3]) == {"label": "日本語"}
