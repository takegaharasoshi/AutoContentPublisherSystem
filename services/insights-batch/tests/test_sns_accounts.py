"""Tests for active Instagram account lookup."""

from app.sns_accounts import fetch_active_sns_accounts


class Cursor:
    def execute(self, query, args):
        self.query = query
        self.args = args

    def fetchall(self):
        return [(2, "instagram", "main", "Main")]


def test_fetch_active_sns_accounts_filters_instagram() -> None:
    """The repository enforces platform and active-state filters."""
    cursor = Cursor()
    accounts = fetch_active_sns_accounts(cursor, 1)
    assert "platform = 'instagram'" in cursor.query
    assert "is_active = 1" in cursor.query
    assert accounts[0].id == 2
