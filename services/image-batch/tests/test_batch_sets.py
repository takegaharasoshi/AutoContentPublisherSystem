"""Tests for batch set repository functions."""

from unittest.mock import Mock

from app.batch_sets import find_batch_set_by_code
from app.models import BatchSet


def test_find_batch_set_returns_none_when_not_found() -> None:
    """An absent set code produces no model."""
    cursor = Mock()
    cursor.fetchone.return_value = None

    assert find_batch_set_by_code(cursor, "missing") is None
    cursor.execute.assert_called_once_with(
        "SELECT id, set_code, generator_name, is_active "
        "FROM batch_sets WHERE set_code = %s",
        ("missing",),
    )


def test_find_batch_set_normalizes_active_flag() -> None:
    """The database integer active flag is returned as bool."""
    cursor = Mock()
    cursor.fetchone.return_value = (3, "set-a", "fake", 0)

    assert find_batch_set_by_code(cursor, "set-a") == BatchSet(3, "set-a", "fake", False)
