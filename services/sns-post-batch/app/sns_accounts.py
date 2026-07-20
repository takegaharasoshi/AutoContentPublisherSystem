"""Repository functions for SNS accounts."""

from __future__ import annotations

from typing import Any

from .models import SnsAccount


def fetch_active_sns_accounts(cursor: Any, set_id: int) -> list[SnsAccount]:
    """Fetch active SNS accounts ordered by ID.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.

    Returns:
        Active accounts belonging to the set.
    """
    cursor.execute(
        "SELECT id, platform, account_code, account_name "
        "FROM sns_accounts WHERE set_id = %s AND is_active = 1 ORDER BY id",
        (set_id,),
    )
    return [
        SnsAccount(
            id=row[0],
            platform=row[1],
            account_code=row[2],
            account_name=row[3],
        )
        for row in cursor.fetchall()
    ]
