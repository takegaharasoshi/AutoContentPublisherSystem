"""Repository functions for SNS posting target selection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import enum
from typing import Any


class TargetOutcome(enum.Enum):
    """Outcome of selecting the generation run for this scheduled execution."""

    SELECTED = "SELECTED"
    RUN_NOT_FOUND = "RUN_NOT_FOUND"
    NO_MEDIA = "NO_MEDIA"
    ALREADY_TERMINAL = "ALREADY_TERMINAL"


@dataclass(frozen=True)
class TargetSelection:
    """Selection result; only RUN_NOT_FOUND has no generation run ID."""

    outcome: TargetOutcome
    generation_run_id: int | None


def select_current_generation_run(
    cursor: Any, set_id: int, scheduled_at: datetime
) -> TargetSelection:
    """Select only the generation run for the exact set and UTC scheduled time.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.
        scheduled_at: Scheduled time as naive UTC, matching the DB DATETIME.

    Returns:
        Whether the current run exists, has media, and needs posting work.
    """
    cursor.execute(
        "SELECT gr.id FROM generation_runs gr "
        "WHERE gr.set_id = %s AND gr.scheduled_at = %s",
        (set_id, scheduled_at),
    )
    row = cursor.fetchone()
    if row is None:
        return TargetSelection(TargetOutcome.RUN_NOT_FOUND, None)
    generation_run_id = row[0]

    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM generated_media gm "
        "WHERE gm.generation_run_id = %s)",
        (generation_run_id,),
    )
    if not cursor.fetchone()[0]:
        return TargetSelection(TargetOutcome.NO_MEDIA, generation_run_id)

    # Story rows are only created after their preceding reel row reaches success.
    cursor.execute(
        "SELECT EXISTS ("
        "SELECT 1 FROM sns_accounts sa "
        "WHERE sa.set_id = %s AND sa.is_active = 1 "
        "AND NOT EXISTS ("
        "SELECT 1 FROM posts p "
        "WHERE p.generation_run_id = %s AND p.sns_account_id = sa.id "
        "AND p.status IN ('success','failed','published_unconfirmed')"
        ")"
        ")",
        (set_id, generation_run_id),
    )
    if not cursor.fetchone()[0]:
        return TargetSelection(
            TargetOutcome.ALREADY_TERMINAL, generation_run_id
        )
    return TargetSelection(TargetOutcome.SELECTED, generation_run_id)
