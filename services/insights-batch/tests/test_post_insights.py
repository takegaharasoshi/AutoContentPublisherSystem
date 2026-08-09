"""Tests for post insights persistence."""

import datetime
import json

from app.post_insights import fetch_collected_post_ids, insert_post_insights


class Cursor:
    """Configurable repository cursor double."""

    def __init__(self) -> None:
        self.rows = [(2,), (3,)]
        self.args = None

    def execute(self, query, args):
        self.args = args
        return 1

    def fetchall(self):
        return self.rows


def test_fetch_collected_post_ids_returns_set() -> None:
    """Precollection lookup supports constant-time membership checks."""
    assert fetch_collected_post_ids(
        Cursor(), set_id=1, scheduled_at=datetime.datetime(2026, 8, 10)
    ) == {2, 3}


def test_insert_post_insights_serializes_metrics() -> None:
    """The raw metric map is stored as JSON through INSERT IGNORE."""
    cursor = Cursor()
    assert insert_post_insights(
        cursor,
        set_id=1,
        post_id=2,
        scheduled_at=datetime.datetime(2026, 8, 10),
        collected_at=datetime.datetime(2026, 8, 10, 1),
        metrics={"views": 4},
        api_version="v25.0",
    )
    assert json.loads(cursor.args[4]) == {"views": 4}
