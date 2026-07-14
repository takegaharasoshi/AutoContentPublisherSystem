"""Tests for database connection helpers."""

from unittest.mock import MagicMock, patch

import pytest

from acps_shared import DbSecret, connect, open_connection


@pytest.fixture
def secret() -> DbSecret:
    return DbSecret(
        username="user",
        password="password",
        host="db.example",
        port=3306,
        dbname="appdb",
    )


@pytest.mark.parametrize("connect_timeout", [10, 30])
def test_connect_uses_expected_connect_arguments(
    secret: DbSecret, connect_timeout: int
) -> None:
    connection = MagicMock()

    with patch("acps_shared.db.pymysql.connect", return_value=connection) as mocked_connect:
        result = connect(secret, connect_timeout=connect_timeout)

    assert result is connection
    mocked_connect.assert_called_once_with(
        host="db.example",
        port=3306,
        user="user",
        password="password",
        database="appdb",
        connect_timeout=connect_timeout,
        charset="utf8mb4",
    )
    connection.close.assert_not_called()


def test_connect_defaults_connect_timeout_to_10(secret: DbSecret) -> None:
    connection = MagicMock()

    with patch("acps_shared.db.pymysql.connect", return_value=connection) as mocked_connect:
        connect(secret)

    assert mocked_connect.call_args.kwargs["connect_timeout"] == 10


def test_open_connection_yields_connection_and_closes_it(secret: DbSecret) -> None:
    connection = MagicMock()

    with patch("acps_shared.db.pymysql.connect", return_value=connection):
        with open_connection(secret) as result:
            assert result is connection

    connection.close.assert_called_once_with()


def test_open_connection_closes_and_propagates_exception(secret: DbSecret) -> None:
    connection = MagicMock()

    with patch("acps_shared.db.pymysql.connect", return_value=connection):
        with pytest.raises(RuntimeError, match="query failed"):
            with open_connection(secret):
                raise RuntimeError("query failed")

    connection.close.assert_called_once_with()
