"""Tests for readiness retry behavior."""

from unittest.mock import Mock

import pytest
import pymysql

from app.retry import wait_for_db


def test_wait_for_db_returns_true_on_initial_success() -> None:
    check = Mock()
    delays: list[float] = []

    assert wait_for_db(check, sleep=delays.append) is True
    assert check.call_count == 1
    assert delays == []


def test_wait_for_db_retries_until_third_attempt_succeeds() -> None:
    check = Mock(
        side_effect=[
            pymysql.err.OperationalError(2003, "connection failed"),
            pymysql.err.OperationalError(2003, "connection failed"),
            None,
        ]
    )
    delays: list[float] = []

    assert wait_for_db(check, sleep=delays.append) is True
    assert check.call_count == 3
    assert delays == [2.0, 4.0]


def test_wait_for_db_returns_false_after_nine_retryable_failures() -> None:
    check = Mock(
        side_effect=[pymysql.err.OperationalError(2003, "connection failed")] * 9
    )
    delays: list[float] = []

    assert wait_for_db(check, sleep=delays.append) is False
    assert check.call_count == 9
    assert delays == [2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0]


def test_wait_for_db_retries_interface_error() -> None:
    check = Mock(
        side_effect=[pymysql.err.InterfaceError(0, "connection failed"), None]
    )
    delays: list[float] = []

    assert wait_for_db(check, sleep=delays.append) is True
    assert check.call_count == 2
    assert delays == [2.0]


def test_wait_for_db_propagates_non_retryable_exception() -> None:
    check = Mock(side_effect=ValueError("unexpected"))
    delays: list[float] = []

    with pytest.raises(ValueError, match="unexpected"):
        wait_for_db(check, sleep=delays.append)

    assert check.call_count == 1
    assert delays == []
