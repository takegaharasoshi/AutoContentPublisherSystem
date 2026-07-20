"""Repository functions for SNS posting target selection."""

from __future__ import annotations

from typing import Any


def resolve_target_generation_run(cursor: Any, set_id: int) -> int | None:
    """Return the oldest generation run with an actionable active account.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.

    Returns:
        The selected generation run ID, or ``None`` when no target exists.
    """
    cursor.execute(
        "SELECT gr.id FROM generation_runs gr "
        "WHERE gr.set_id = %s "
        "AND EXISTS ("
        "SELECT 1 FROM sns_accounts sa "
        "WHERE sa.set_id = gr.set_id AND sa.is_active = 1 "
        "AND NOT EXISTS ("
        "SELECT 1 FROM posts p "
        "WHERE p.generation_run_id = gr.id AND p.sns_account_id = sa.id "
        "AND p.status IN ('success','failed','published_unconfirmed')"
        ")"
        ") "
        "ORDER BY gr.scheduled_at ASC, gr.id ASC "
        "LIMIT 1",
        (set_id,),
    )
    row = cursor.fetchone()
    return None if row is None else row[0]
