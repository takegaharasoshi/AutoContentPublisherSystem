"""Repository functions for Instagram SNS accounts."""

from __future__ import annotations

from typing import Any

from .models import SnsAccount


def fetch_active_sns_accounts(cursor: Any, set_id: int) -> list[SnsAccount]:
    """Fetch active Instagram accounts ordered by ID."""
    cursor.execute(
        "SELECT id, platform, account_code, account_name FROM sns_accounts "
        "WHERE set_id = %s AND platform = 'instagram' AND is_active = 1 ORDER BY id",
        (set_id,),
    )
    return [SnsAccount(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
