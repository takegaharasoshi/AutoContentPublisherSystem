"""Tests for SNS posting target selection."""

from datetime import datetime

import pytest

from app.target_selection import (
    TargetOutcome,
    TargetSelection,
    select_current_generation_run,
)


class FakeCursor:
    """Record SQL and provide one row per selection stage."""

    def __init__(self, rows: list[tuple[int] | None]) -> None:
        self.rows = iter(rows)
        self.queries: list[tuple[str, tuple[object, ...]]] = []

    def execute(self, query: str, parameters: tuple[object, ...]) -> None:
        self.queries.append((query, parameters))

    def fetchone(self) -> tuple[int] | None:
        return next(self.rows)


@pytest.mark.parametrize(
    ("rows", "outcome", "run_id"),
    [
        ([None], TargetOutcome.RUN_NOT_FOUND, None),
        ([(17,), (0,)], TargetOutcome.NO_MEDIA, 17),
        ([(17,), (1,), (0,)], TargetOutcome.ALREADY_TERMINAL, 17),
        ([(17,), (1,), (1,)], TargetOutcome.SELECTED, 17),
    ],
    ids=["RUN_NOT_FOUND", "NO_MEDIA", "ALREADY_TERMINAL", "SELECTED"],
)
def test_select_current_generation_run_checks_stages_in_order(
    rows: list[tuple[int] | None], outcome: TargetOutcome, run_id: int | None
) -> None:
    """Each outcome stops at its stage and never searches another run."""
    cursor = FakeCursor(rows)
    scheduled_at = datetime(2026, 10, 12, 22, 30)

    selection = select_current_generation_run(cursor, 3, scheduled_at)
    assert selection == TargetSelection(outcome, run_id)
    assert len(cursor.queries) == len(rows)
    assert cursor.queries[0] == (
        "SELECT gr.id FROM generation_runs gr "
        "WHERE gr.set_id = %s AND gr.scheduled_at = %s",
        (3, scheduled_at),
    )
    for query, _ in cursor.queries:
        assert "ORDER BY" not in query.upper()
        assert "LIMIT" not in query.upper()

    if len(rows) >= 2:
        assert cursor.queries[1] == (
            "SELECT EXISTS (SELECT 1 FROM generated_media gm "
            "WHERE gm.generation_run_id = %s)",
            (17,),
        )
    if len(rows) == 3:
        query, parameters = cursor.queries[2]
        assert "SELECT EXISTS (SELECT 1 FROM sns_accounts sa" in query
        assert "sa.set_id = %s AND sa.is_active = 1" in query
        assert "AND NOT EXISTS (SELECT 1 FROM posts p" in query
        assert "p.generation_run_id = %s AND p.sns_account_id = sa.id" in query
        assert "p.status IN ('success','failed','published_unconfirmed')" in query
        assert parameters == (3, 17)
