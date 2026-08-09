"""Tests for collectible post selection."""

import datetime

from app.posts import fetch_collectible_posts


class Cursor:
    """Query-recording cursor."""

    def __init__(self) -> None:
        self.query = ""
        self.args = ()

    def execute(self, query, args):
        self.query = query
        self.args = args

    def fetchall(self):
        return [(1, "reel", "media", datetime.datetime(2026, 8, 9))]


def test_fetch_collectible_posts_uses_distinct_cutoffs() -> None:
    """Persistent media and stories receive fourteen-day and 24-hour cutoffs."""
    cursor = Cursor()
    now = datetime.datetime(2026, 8, 10, 9)
    posts = fetch_collectible_posts(
        cursor,
        set_id=2,
        sns_account_id=3,
        now=now,
        media_lookback_days=14,
    )
    assert cursor.args == (
        2,
        3,
        now - datetime.timedelta(days=14),
        now - datetime.timedelta(hours=24),
    )
    assert posts[0].platform_post_id == "media"
