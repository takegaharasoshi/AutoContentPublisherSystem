"""Repository functions for batch execution logs."""

from __future__ import annotations

import datetime
from typing import Any

import pymysql


def start_or_resume_execution_log(
    cursor: Any,
    *,
    set_id: int,
    execution_arn: str,
    batch_type: str,
    started_at: datetime.datetime,
) -> int:
    """Insert or resume a batch execution log and return its ID.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.
        execution_arn: Step Functions execution ARN.
        batch_type: Batch type stored in the execution log.
        started_at: UTC start timestamp for a new log.

    Returns:
        The execution log ID.

    Raises:
        pymysql.err.IntegrityError: If an unexpected integrity error occurs.
    """
    try:
        cursor.execute(
            "INSERT INTO batch_execution_logs "
            "(set_id, batch_type, execution_arn, status, attempt_count, started_at) "
            "VALUES (%s, %s, %s, 'running', 1, %s)",
            (set_id, batch_type, execution_arn, started_at),
        )
        return cursor.lastrowid
    except pymysql.err.IntegrityError as exc:
        if not exc.args or exc.args[0] != pymysql.constants.ER.DUP_ENTRY:
            raise

    cursor.execute(
        "SELECT id FROM batch_execution_logs "
        "WHERE execution_arn = %s AND batch_type = %s",
        (execution_arn, batch_type),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError("Execution log was not found after duplicate insert")
    log_id = row[0]
    cursor.execute(
        "UPDATE batch_execution_logs "
        "SET attempt_count = attempt_count + 1, status = 'running' WHERE id = %s",
        (log_id,),
    )
    return log_id


def finalize_execution_log(
    cursor: Any,
    *,
    log_id: int,
    status: str,
    finished_at: datetime.datetime,
    records_processed: int | None,
    error_message: str | None,
) -> None:
    """Persist the final state of an execution log.

    Args:
        cursor: Database cursor.
        log_id: Execution log ID.
        status: Final execution status.
        finished_at: UTC completion timestamp.
        records_processed: Number of posting attempts processed.
        error_message: Failure reason, if any.
    """
    cursor.execute(
        "UPDATE batch_execution_logs SET status = %s, finished_at = %s, "
        "error_message = %s, records_processed = %s WHERE id = %s",
        (status, finished_at, error_message, records_processed, log_id),
    )
