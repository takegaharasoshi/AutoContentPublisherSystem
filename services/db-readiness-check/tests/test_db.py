"""Tests for database connection checks."""

from unittest.mock import MagicMock, patch

import pytest

from app.db import check_connection
from app.secrets import DbSecret


@pytest.fixture
def secret() -> DbSecret:
    return DbSecret(
        username="user",
        password="password",
        host="db.example",
        port=3306,
        dbname="appdb",
    )


def test_check_connection_uses_expected_connect_arguments(secret: DbSecret) -> None:
    connection = MagicMock()
    cursor = connection.cursor.return_value

    with patch("app.db.pymysql.connect", return_value=connection) as connect:
        check_connection(secret)

    connect.assert_called_once_with(
        host="db.example",
        port=3306,
        user="user",
        password="password",
        database="appdb",
        connect_timeout=10,
    )
    cursor.execute.assert_called_once_with("SELECT 1")
    cursor.fetchone.assert_called_once_with()
    connection.close.assert_called_once_with()


def test_check_connection_closes_connection_when_cursor_raises(
    secret: DbSecret,
) -> None:
    connection = MagicMock()
    connection.cursor.side_effect = RuntimeError("cursor failed")

    with patch("app.db.pymysql.connect", return_value=connection):
        with pytest.raises(RuntimeError, match="cursor failed"):
            check_connection(secret)

    connection.close.assert_called_once_with()
