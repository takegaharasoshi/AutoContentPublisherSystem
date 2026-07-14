"""Tests for application orchestration."""

import logging
from unittest.mock import Mock

import app.main as main_module
import pytest

from app.config import AppConfig, ConfigError


class FakeCursor:
    """Cursor fake that supports the context-manager protocol."""

    def __init__(self, lastrowid: int = 42, row_count: int = 3) -> None:
        self.lastrowid = lastrowid
        self.row_count = row_count
        self.executed: list[tuple[str, tuple[str, ...] | None]] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> bool:
        return False

    def execute(self, query: str, params: tuple[str, ...] | None = None) -> None:
        self.executed.append((query, params))

    def fetchone(self) -> tuple[int]:
        return (self.row_count,)


class FakeConnection:
    """Connection fake that returns supplied cursors."""

    def __init__(self, cursors: list[FakeCursor]) -> None:
        self.cursors = cursors
        self.commit_called = False

    def cursor(self) -> FakeCursor:
        return self.cursors.pop(0)

    def commit(self) -> None:
        self.commit_called = True


class FakeOpenConnection:
    """Database connection context-manager fake."""

    def __init__(self, connection: FakeConnection) -> None:
        self.connection = connection

    def __enter__(self) -> FakeConnection:
        return self.connection

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> bool:
        return False


def _config(db_secret_json: str | None = None) -> AppConfig:
    return AppConfig(
        env_name="prod",
        db_secret_arn="arn:example",
        db_secret_json=db_secret_json,
    )


def _connection() -> tuple[FakeConnection, FakeCursor, FakeCursor]:
    insert_cursor = FakeCursor(lastrowid=42)
    select_cursor = FakeCursor(row_count=3)
    return FakeConnection([insert_cursor, select_cursor]), insert_cursor, select_cursor


def test_main_succeeds_after_insert_and_select(monkeypatch, caplog) -> None:
    connection, insert_cursor, select_cursor = _connection()
    monkeypatch.setattr(main_module, "setup_logging", lambda: None)
    monkeypatch.setattr(main_module, "load_config", lambda: _config())
    monkeypatch.setattr(main_module, "get_db_secret", lambda arn: object())
    monkeypatch.setattr(
        main_module, "open_connection", lambda secret: FakeOpenConnection(connection)
    )

    with caplog.at_level(logging.INFO):
        assert main_module.main() == 0

    assert "DB 接続成功" in caplog.text
    assert connection.commit_called
    assert insert_cursor.executed == [
        ("INSERT INTO connection_test (service_name) VALUES (%s)", ("image-batch",))
    ]
    assert select_cursor.executed == [("SELECT COUNT(*) FROM connection_test", None)]


def test_main_returns_one_for_config_error(monkeypatch) -> None:
    get_secret = Mock()
    monkeypatch.setattr(main_module, "setup_logging", lambda: None)
    monkeypatch.setattr(
        main_module, "load_config", lambda: (_ for _ in ()).throw(ConfigError())
    )
    monkeypatch.setattr(main_module, "get_db_secret", get_secret)

    assert main_module.main() == 1
    get_secret.assert_not_called()


def test_main_hides_secret_value_when_secret_resolution_fails(
    monkeypatch, caplog
) -> None:
    secret_value = "very-secret-password"
    monkeypatch.setattr(main_module, "setup_logging", lambda: None)
    monkeypatch.setattr(main_module, "load_config", lambda: _config())
    monkeypatch.setattr(
        main_module,
        "get_db_secret",
        lambda arn: (_ for _ in ()).throw(RuntimeError(secret_value)),
    )

    assert main_module.main() == 1
    assert secret_value not in caplog.text


@pytest.mark.parametrize("fail_on_select", [False, True])
def test_main_returns_one_when_insert_or_select_fails(
    monkeypatch, fail_on_select: bool
) -> None:
    connection, insert_cursor, select_cursor = _connection()
    failing_cursor = select_cursor if fail_on_select else insert_cursor

    def fail_execute(query: str, params: tuple[str, ...] | None = None) -> None:
        raise RuntimeError("query failed")

    monkeypatch.setattr(failing_cursor, "execute", fail_execute)
    monkeypatch.setattr(main_module, "setup_logging", lambda: None)
    monkeypatch.setattr(main_module, "load_config", lambda: _config())
    monkeypatch.setattr(main_module, "get_db_secret", lambda arn: object())
    monkeypatch.setattr(
        main_module,
        "open_connection",
        lambda secret: FakeOpenConnection(connection),
    )

    assert main_module.main() == 1


def test_main_uses_json_secret_without_calling_secrets_manager(monkeypatch) -> None:
    connection, _, _ = _connection()
    parsed_secret = object()
    get_secret = Mock()
    parse_secret = Mock(return_value=parsed_secret)
    monkeypatch.setattr(main_module, "setup_logging", lambda: None)
    monkeypatch.setattr(
        main_module, "load_config", lambda: _config("{\"host\": \"db\"}")
    )
    monkeypatch.setattr(main_module, "parse_db_secret", parse_secret)
    monkeypatch.setattr(main_module, "get_db_secret", get_secret)
    monkeypatch.setattr(
        main_module, "open_connection", lambda secret: FakeOpenConnection(connection)
    )

    assert main_module.main() == 0
    parse_secret.assert_called_once_with("{\"host\": \"db\"}")
    get_secret.assert_not_called()
