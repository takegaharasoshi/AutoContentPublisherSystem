"""Tests for image batch orchestration."""

from contextlib import contextmanager
from unittest.mock import Mock

import app.main as main_module
import pytest

from app.config import AppConfig, ConfigError
from app.generators import GeneratorNotFoundError
from app.models import BatchSet, PromptConfig
from app.processing import ProcessingResult


class FakeCursor:
    """Cursor fake that supports context manager usage."""

    def __enter__(self) -> "FakeCursor":
        """Return this cursor."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Do not suppress exceptions."""
        return False


class FakeConnection:
    """Connection fake with a stable cursor."""

    def __init__(self) -> None:
        """Initialize commit tracking."""
        self.cursor_value = FakeCursor()
        self.commit = Mock()

    def cursor(self) -> FakeCursor:
        """Return the test cursor."""
        return self.cursor_value


@contextmanager
def _open_connection(connection: FakeConnection):
    """Yield a fake connection in the same shape as open_connection."""
    yield connection


def _config() -> AppConfig:
    """Return a valid image batch configuration."""
    return AppConfig(
        env_name="prod",
        db_secret_arn="arn:db",
        db_secret_json=None,
        set_code="set-a",
        execution_arn="arn:execution",
        scheduled_at="2026-07-19T00:00:00Z",
        api_secret_arn="arn:api",
        s3_bucket_name="bucket",
    )


def _patch_base(monkeypatch, connection: FakeConnection) -> None:
    """Patch common startup dependencies for a main test."""
    monkeypatch.setattr(main_module, "setup_logging", lambda: None)
    monkeypatch.setattr(main_module, "load_config", _config)
    monkeypatch.setattr(main_module, "get_db_secret", lambda arn: object())
    monkeypatch.setattr(
        main_module,
        "open_connection",
        lambda secret: _open_connection(connection),
    )


def _patch_started_log(monkeypatch) -> Mock:
    """Patch successful log startup and return the finalizer mock."""
    monkeypatch.setattr(main_module, "start_or_resume_execution_log", Mock(return_value=10))
    finalizer = Mock()
    monkeypatch.setattr(main_module, "finalize_execution_log", finalizer)
    return finalizer


def test_main_returns_one_when_config_loading_fails(monkeypatch) -> None:
    """Configuration failure prevents all DB work."""
    get_secret = Mock()
    monkeypatch.setattr(main_module, "setup_logging", lambda: None)
    monkeypatch.setattr(
        main_module,
        "load_config",
        lambda: (_ for _ in ()).throw(ConfigError("ENV_NAME")),
    )
    monkeypatch.setattr(main_module, "get_db_secret", get_secret)

    assert main_module.main() == 1
    get_secret.assert_not_called()


def test_main_returns_one_when_set_code_is_not_found(monkeypatch) -> None:
    """No execution log is written before the set ID is known."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    start_log = Mock()
    monkeypatch.setattr(main_module, "find_batch_set_by_code", lambda cursor, code: None)
    monkeypatch.setattr(main_module, "start_or_resume_execution_log", start_log)

    assert main_module.main(s3_client=Mock()) == 1
    start_log.assert_not_called()


def test_main_skips_inactive_set_and_succeeds(monkeypatch) -> None:
    """An inactive set finalizes successfully without generation work."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", "fake", False),
    )

    assert main_module.main(s3_client=Mock()) == 0
    assert finalizer.call_args.kwargs["status"] == "succeeded"
    assert finalizer.call_args.kwargs["records_processed"] == 0
    assert connection.commit.call_count == 2


def test_main_finalizes_failed_for_unknown_generator(monkeypatch) -> None:
    """An unknown generator is a terminal configuration failure."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", "unknown", True),
    )
    monkeypatch.setattr(
        main_module,
        "resolve_generator",
        lambda name: (_ for _ in ()).throw(GeneratorNotFoundError(name)),
    )

    assert main_module.main(s3_client=Mock()) == 1
    assert finalizer.call_args.kwargs["status"] == "failed"
    assert finalizer.call_args.kwargs["records_processed"] == 0


def test_main_finalizes_failed_when_no_active_prompts(monkeypatch) -> None:
    """A selected active set requires at least one active prompt config."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", "fake", True),
    )
    monkeypatch.setattr(main_module, "resolve_generator", lambda name: Mock())
    monkeypatch.setattr(main_module, "resolve_generation_run", lambda *args, **kwargs: 8)
    monkeypatch.setattr(main_module, "fetch_active_prompt_configs", lambda cursor, set_id: [])

    assert main_module.main(s3_client=Mock()) == 1
    assert finalizer.call_args.kwargs["status"] == "failed"


def test_main_finalizes_success_when_all_prompts_complete(monkeypatch) -> None:
    """A complete processing result returns success and its new-image count."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", "fake", True),
    )
    monkeypatch.setattr(main_module, "resolve_generator", lambda name: Mock())
    monkeypatch.setattr(main_module, "resolve_generation_run", lambda *args, **kwargs: 8)
    monkeypatch.setattr(
        main_module,
        "fetch_active_prompt_configs",
        lambda cursor, set_id: [PromptConfig(2, 1, "prompt", None, None)],
    )
    monkeypatch.setattr(
        main_module,
        "process_prompt_configs",
        lambda *args, **kwargs: ProcessingResult(3, True),
    )

    assert main_module.main(s3_client=Mock()) == 0
    assert finalizer.call_args.kwargs["status"] == "succeeded"
    assert finalizer.call_args.kwargs["records_processed"] == 3


def test_main_finalizes_failed_for_incomplete_prompts(monkeypatch) -> None:
    """An incomplete processing result returns failure after finalization."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", "fake", True),
    )
    monkeypatch.setattr(main_module, "resolve_generator", lambda name: Mock())
    monkeypatch.setattr(main_module, "resolve_generation_run", lambda *args, **kwargs: 8)
    monkeypatch.setattr(
        main_module,
        "fetch_active_prompt_configs",
        lambda cursor, set_id: [PromptConfig(2, 1, "prompt", None, None)],
    )
    monkeypatch.setattr(
        main_module,
        "process_prompt_configs",
        lambda *args, **kwargs: ProcessingResult(1, False),
    )

    assert main_module.main(s3_client=Mock()) == 1
    assert finalizer.call_args.kwargs["status"] == "failed"
    assert finalizer.call_args.kwargs["error_message"] == (
        "one or more prompt_configs did not complete"
    )


def test_main_does_not_finalize_when_execution_log_start_fails(monkeypatch) -> None:
    """A log creation failure is returned directly because no log is available."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = Mock()
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", "fake", True),
    )
    monkeypatch.setattr(
        main_module,
        "start_or_resume_execution_log",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("failed")),
    )
    monkeypatch.setattr(main_module, "finalize_execution_log", finalizer)

    assert main_module.main(s3_client=Mock()) == 1
    finalizer.assert_not_called()


def test_main_returns_one_when_success_finalization_fails(monkeypatch) -> None:
    """A final log write failure makes an otherwise successful execution fail."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", "fake", True),
    )
    monkeypatch.setattr(main_module, "resolve_generator", lambda name: Mock())
    monkeypatch.setattr(main_module, "resolve_generation_run", lambda *args, **kwargs: 8)
    monkeypatch.setattr(
        main_module,
        "fetch_active_prompt_configs",
        lambda cursor, set_id: [PromptConfig(2, 1, "prompt", None, None)],
    )
    monkeypatch.setattr(
        main_module,
        "process_prompt_configs",
        lambda *args, **kwargs: ProcessingResult(1, True),
    )
    monkeypatch.setattr(
        main_module,
        "finalize_execution_log",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("finalize")),
    )

    assert main_module.main(s3_client=Mock()) == 1
