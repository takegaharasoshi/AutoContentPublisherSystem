"""Tests for execution log repository functions."""

import datetime
from unittest.mock import Mock

import pymysql
import pytest

from app.execution_log import finalize_execution_log, start_or_resume_execution_log


def test_start_execution_log_inserts_and_returns_id() -> None:
    """A new execution log returns the insert ID."""
    cursor = Mock(lastrowid=15)
    started_at = datetime.datetime(2026, 7, 19)

    assert start_or_resume_execution_log(
        cursor,
        set_id=4,
        execution_arn="arn:execution",
        batch_type="image_generation",
        started_at=started_at,
    ) == 15
    cursor.execute.assert_called_once_with(
        "INSERT INTO batch_execution_logs "
        "(set_id, batch_type, execution_arn, status, attempt_count, started_at) "
        "VALUES (%s, %s, %s, 'running', 1, %s)",
        (4, "image_generation", "arn:execution", started_at),
    )


def test_start_execution_log_resumes_duplicate_without_rollback() -> None:
    """A duplicate execution ARN updates the existing log attempt count."""
    cursor = Mock()
    cursor.execute.side_effect = [
        pymysql.err.IntegrityError(1062, "duplicate"),
        None,
        None,
    ]
    cursor.fetchone.return_value = (9,)

    assert start_or_resume_execution_log(
        cursor,
        set_id=4,
        execution_arn="arn:execution",
        batch_type="image_generation",
        started_at=datetime.datetime(2026, 7, 19),
    ) == 9
    assert cursor.execute.call_args_list[-1].args == (
        "UPDATE batch_execution_logs "
        "SET attempt_count = attempt_count + 1, status = 'running' WHERE id = %s",
        (9,),
    )


def test_start_execution_log_reraises_non_duplicate_integrity_error() -> None:
    """Integrity errors other than duplicates are not swallowed."""
    cursor = Mock()
    cursor.execute.side_effect = pymysql.err.IntegrityError(1452, "foreign key")

    with pytest.raises(pymysql.err.IntegrityError):
        start_or_resume_execution_log(
            cursor,
            set_id=4,
            execution_arn="arn:execution",
            batch_type="image_generation",
            started_at=datetime.datetime(2026, 7, 19),
        )


def test_finalize_execution_log_updates_final_fields() -> None:
    """Finalization persists all terminal-state fields."""
    cursor = Mock()
    finished_at = datetime.datetime(2026, 7, 19, 1)

    finalize_execution_log(
        cursor,
        log_id=9,
        status="failed",
        finished_at=finished_at,
        records_processed=2,
        error_message="failed",
    )

    cursor.execute.assert_called_once_with(
        "UPDATE batch_execution_logs SET status = %s, finished_at = %s, "
        "error_message = %s, records_processed = %s WHERE id = %s",
        ("failed", finished_at, "failed", 2, 9),
    )
