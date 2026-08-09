"""Tests for insights execution log persistence."""

import datetime

import pymysql

from app.execution_log import finalize_execution_log, start_or_resume_execution_log


class Cursor:
    """Execution-log cursor with configurable insert behavior."""

    def __init__(self, *, duplicate: bool = False) -> None:
        self.duplicate = duplicate
        self.lastrowid = 4
        self.calls = []

    def execute(self, query, args):
        self.calls.append((query, args))
        if self.duplicate and query.startswith("INSERT"):
            raise pymysql.err.IntegrityError(
                pymysql.constants.ER.DUP_ENTRY, "duplicate"
            )

    def fetchone(self):
        return (8,)


def test_start_execution_log_uses_insights_batch_type() -> None:
    """A new log returns the inserted row ID."""
    cursor = Cursor()
    assert start_or_resume_execution_log(
        cursor,
        set_id=1,
        execution_arn="arn",
        batch_type="insights_collection",
        started_at=datetime.datetime(2026, 8, 10),
    ) == 4
    assert cursor.calls[0][1][1] == "insights_collection"


def test_start_execution_log_resumes_duplicate() -> None:
    """A Step Functions retry fetches and increments the existing log."""
    cursor = Cursor(duplicate=True)
    assert start_or_resume_execution_log(
        cursor,
        set_id=1,
        execution_arn="arn",
        batch_type="insights_collection",
        started_at=datetime.datetime(2026, 8, 10),
    ) == 8
    assert len(cursor.calls) == 3


def test_finalize_execution_log_records_insert_count() -> None:
    """The final update stores the collected-row count."""
    cursor = Cursor()
    finalize_execution_log(
        cursor,
        log_id=4,
        status="succeeded",
        finished_at=datetime.datetime(2026, 8, 10),
        records_processed=12,
        error_message=None,
    )
    assert cursor.calls[0][1][3] == 12
