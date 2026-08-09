"""Tests for insights collection batch orchestration."""

from __future__ import annotations

from unittest.mock import Mock

from app.config import AppConfig
from app.models import BatchSet
from app.processing import InsightsCollectionResult
from app import main as main_module


class Cursor:
    """Context-managed cursor double."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None


class Connection:
    """Context-managed database connection double."""

    def __init__(self) -> None:
        self.cursor_value = Cursor()
        self.commits = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def cursor(self):
        return self.cursor_value

    def commit(self):
        self.commits += 1


def _config() -> AppConfig:
    return AppConfig(
        env_name="prod",
        db_secret_arn=None,
        db_secret_json="{}",
        set_code="set-a",
        execution_arn="arn:execution",
        scheduled_at="2026-08-10T09:00:00Z",
        media_lookback_days=14,
    )


def _patch_base(monkeypatch, batch_set: BatchSet | None):
    connection = Connection()
    monkeypatch.setattr(main_module, "load_config", _config)
    monkeypatch.setattr(main_module, "parse_db_secret", lambda value: object())
    monkeypatch.setattr(main_module, "open_connection", lambda secret: connection)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: batch_set,
    )
    monkeypatch.setattr(main_module, "start_or_resume_execution_log", lambda *args, **kwargs: 9)
    finalizer = Mock()
    monkeypatch.setattr(main_module, "finalize_execution_log", finalizer)
    monkeypatch.setattr(main_module, "fetch_active_sns_accounts", lambda *args: [])
    return connection, finalizer


def test_main_success_returns_zero(monkeypatch) -> None:
    """A failure-free result finalizes the log as succeeded."""
    _, finalizer = _patch_base(monkeypatch, BatchSet(1, "set-a", True))
    monkeypatch.setattr(
        main_module,
        "process_accounts",
        lambda *args, **kwargs: InsightsCollectionResult(3, 0, 1),
    )
    assert main_module.main(urlopen=Mock()) == 0
    assert finalizer.call_args.kwargs["status"] == "succeeded"
    assert finalizer.call_args.kwargs["records_processed"] == 3


def test_main_failure_result_returns_one(monkeypatch) -> None:
    """Partial failures produce a failed execution log and exit one."""
    _, finalizer = _patch_base(monkeypatch, BatchSet(1, "set-a", True))
    monkeypatch.setattr(
        main_module,
        "process_accounts",
        lambda *args, **kwargs: InsightsCollectionResult(2, 1, 1),
    )
    assert main_module.main(urlopen=Mock()) == 1
    assert finalizer.call_args.kwargs["status"] == "failed"
    assert finalizer.call_args.kwargs["records_processed"] == 2


def test_main_inactive_set_succeeds_without_processing(monkeypatch) -> None:
    """An inactive set is a normal no-op after execution-log creation."""
    _, finalizer = _patch_base(monkeypatch, BatchSet(1, "set-a", False))
    process = Mock()
    monkeypatch.setattr(main_module, "process_accounts", process)
    assert main_module.main() == 0
    process.assert_not_called()
    assert finalizer.call_args.kwargs["records_processed"] == 0


def test_main_missing_set_returns_one_without_log(monkeypatch) -> None:
    """An unknown SET_CODE cannot create a set-scoped execution log."""
    _, finalizer = _patch_base(monkeypatch, None)
    assert main_module.main() == 1
    finalizer.assert_not_called()
