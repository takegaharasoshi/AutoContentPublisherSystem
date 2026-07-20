"""Tests for SNS account repository functions."""

from unittest.mock import Mock

from app.models import SnsAccount
from app.sns_accounts import fetch_active_sns_accounts


def test_fetch_active_sns_accounts_maps_rows_in_id_order() -> None:
    """Active account rows are mapped to frozen models."""
    cursor = Mock()
    cursor.fetchall.return_value = [
        (2, "instagram", "second", "Second"),
        (5, "threads", "first", "First"),
    ]

    assert fetch_active_sns_accounts(cursor, 4) == [
        SnsAccount(2, "instagram", "second", "Second"),
        SnsAccount(5, "threads", "first", "First"),
    ]
    cursor.execute.assert_called_once_with(
        "SELECT id, platform, account_code, account_name "
        "FROM sns_accounts WHERE set_id = %s AND is_active = 1 ORDER BY id",
        (4,),
    )
