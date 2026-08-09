"""Tests for batch set lookup."""

from app.batch_sets import find_batch_set_by_code
from app.models import BatchSet


class Cursor:
    def __init__(self, row):
        self.row = row

    def execute(self, query, args):
        self.args = args

    def fetchone(self):
        return self.row


def test_find_batch_set_by_code() -> None:
    """A matching row becomes the insights BatchSet model."""
    assert find_batch_set_by_code(Cursor((1, "set-a", 1)), "set-a") == BatchSet(
        1, "set-a", True
    )


def test_find_batch_set_by_code_missing() -> None:
    """A missing set returns None."""
    assert find_batch_set_by_code(Cursor(None), "missing") is None
