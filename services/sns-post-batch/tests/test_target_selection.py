"""Tests for SNS posting target selection."""

from unittest.mock import Mock

from app.target_selection import resolve_target_generation_run


def test_resolve_target_generation_run_returns_oldest_actionable_run() -> None:
    """The repository returns the selected generation run ID."""
    cursor = Mock()
    cursor.fetchone.return_value = (17,)

    assert resolve_target_generation_run(cursor, 3) == 17
    query = cursor.execute.call_args.args[0]
    assert "FROM generation_runs gr" in query
    assert "sa.is_active = 1" in query
    assert "p.status IN ('success','failed','published_unconfirmed')" in query
    assert "ORDER BY gr.scheduled_at ASC, gr.id ASC" in query
    assert query.endswith("LIMIT 1")
    assert cursor.execute.call_args.args[1] == (3,)


def test_resolve_target_generation_run_returns_none_without_target() -> None:
    """No actionable generation run is represented by None."""
    cursor = Mock()
    cursor.fetchone.return_value = None

    assert resolve_target_generation_run(cursor, 3) is None
