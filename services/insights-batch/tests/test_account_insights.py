"""Tests for account insights date and persistence helpers."""

import datetime
import json

from app.account_insights import (
    fetch_follows_backfill_dates,
    insert_account_insights,
    resolve_target_dates,
    update_follows_and_unfollows,
)


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


class RowsCursor:
    """Cursor double returning stored metric rows and recording SQL calls."""

    def __init__(self, rows=None, affected: int = 1) -> None:
        self.rows = rows or []
        self.affected = affected
        self.query = None
        self.args = None

    def execute(self, query, args):
        self.query = query
        self.args = args
        return self.affected

    def fetchall(self):
        return self.rows


def test_fetch_follows_backfill_dates_accepts_json_strings_and_dicts() -> None:
    """Rows with absent or empty breakdowns are selected in date order."""
    dates = [datetime.date(2026, 9, day) for day in range(1, 5)]
    cursor = RowsCursor(
        [
            (dates[0], json.dumps({"follows_and_unfollows": {"breakdowns": []}})),
            (
                dates[1],
                {
                    "follows_and_unfollows": {
                        "breakdowns": [{"results": [{"value": 1}]}]
                    }
                },
            ),
            (
                dates[2],
                {
                    "follows_and_unfollows": {
                        "breakdowns": [{"dimension_keys": ["follow_type"]}]
                    }
                },
            ),
            (dates[3], json.dumps({"reach": 10})),
        ]
    )

    result = fetch_follows_backfill_dates(cursor, 7, dates[0], dates[3])

    assert result == [dates[0], dates[2], dates[3]]
    assert cursor.query == (
        "SELECT metric_date, metrics FROM account_insights_daily "
        "WHERE sns_account_id = %s AND metric_date BETWEEN %s AND %s "
        "ORDER BY metric_date ASC"
    )
    assert cursor.args == (7, dates[0], dates[3])


def test_update_follows_and_unfollows_uses_json_set_and_unicode_json() -> None:
    """The update changes only the metric JSON path and reports affected rows."""
    value = {"breakdowns": [{"results": [{"dimension_values": ["日本語"]}]}]}
    cursor = RowsCursor(affected=1)

    assert update_follows_and_unfollows(
        cursor,
        sns_account_id=7,
        metric_date=datetime.date(2026, 9, 1),
        value=value,
    )
    assert cursor.query == (
        "UPDATE account_insights_daily SET metrics = "
        "JSON_SET(metrics, '$.follows_and_unfollows', CAST(%s AS JSON)) "
        "WHERE sns_account_id = %s AND metric_date = %s"
    )
    assert json.loads(cursor.args[0]) == value
    assert "\\u" not in cursor.args[0]
    assert cursor.args[1:] == (7, datetime.date(2026, 9, 1))
    assert not update_follows_and_unfollows(
        RowsCursor(affected=0),
        sns_account_id=7,
        metric_date=datetime.date(2026, 9, 1),
        value=value,
    )
