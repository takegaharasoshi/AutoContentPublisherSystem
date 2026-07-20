"""Tests for SNS posting batch orchestration."""

from contextlib import contextmanager
from unittest.mock import Mock

import app.main as main_module

from app.config import AppConfig, ConfigError
from app.models import BatchSet, CaptionTemplate, GeneratedImageRef, SnsAccount
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


def _config(db_secret_json: str | None = None) -> AppConfig:
    """Return a valid SNS posting configuration."""
    return AppConfig(
        env_name="prod",
        db_secret_arn="arn:db",
        db_secret_json=db_secret_json,
        set_code="set-a",
        execution_arn="arn:execution",
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
    monkeypatch.setattr(
        main_module,
        "start_or_resume_execution_log",
        Mock(return_value=10),
    )
    finalizer = Mock()
    monkeypatch.setattr(main_module, "finalize_execution_log", finalizer)
    return finalizer


def _patch_target_dependencies(monkeypatch, *, image=True) -> None:
    """Patch repositories needed after a target is selected."""
    monkeypatch.setattr(
        main_module,
        "fetch_active_sns_accounts",
        lambda cursor, set_id: [SnsAccount(2, "instagram", "main", "Main")],
    )
    monkeypatch.setattr(
        main_module,
        "fetch_active_caption_template",
        lambda cursor, set_id: CaptionTemplate(3, "caption"),
    )
    monkeypatch.setattr(
        main_module,
        "fetch_first_generated_image",
        lambda cursor, run_id: GeneratedImageRef(4, "bucket", "images/a.jpg")
        if image
        else None,
    )


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

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 1
    start_log.assert_not_called()


def test_main_skips_inactive_set_and_succeeds(monkeypatch) -> None:
    """An inactive set finalizes successfully without posting work."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", False),
    )

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    assert finalizer.call_args.kwargs["status"] == "succeeded"
    assert finalizer.call_args.kwargs["records_processed"] == 0
    assert connection.commit.call_count == 2


def test_main_succeeds_when_no_posting_target_exists(monkeypatch) -> None:
    """No target is a normal successful execution with zero records."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(main_module, "resolve_target_generation_run", lambda *args: None)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    assert finalizer.call_args.kwargs == {
        "log_id": 10,
        "status": "succeeded",
        "records_processed": 0,
        "error_message": None,
        "finished_at": finalizer.call_args.kwargs["finished_at"],
    }


def test_main_fails_when_target_has_no_generated_image(monkeypatch) -> None:
    """Missing target image is a data inconsistency recorded as failed."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(main_module, "resolve_target_generation_run", lambda *args: 8)
    _patch_target_dependencies(monkeypatch, image=False)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 1
    assert finalizer.call_args.kwargs["status"] == "failed"
    assert finalizer.call_args.kwargs["records_processed"] == 0


def test_main_finalizes_success_with_processed_account_count(monkeypatch) -> None:
    """A completely successful posting result finalizes with its count."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(main_module, "resolve_target_generation_run", lambda *args: 8)
    _patch_target_dependencies(monkeypatch)
    processor = Mock(return_value=ProcessingResult(1, True))
    monkeypatch.setattr(main_module, "process_target_generation_run", processor)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    assert finalizer.call_args.kwargs["status"] == "succeeded"
    assert finalizer.call_args.kwargs["records_processed"] == 1
    processor.assert_called_once()


def test_main_finalizes_failed_when_an_account_does_not_succeed(monkeypatch) -> None:
    """A non-success account produces the fixed failure message."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(main_module, "resolve_target_generation_run", lambda *args: 8)
    _patch_target_dependencies(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "process_target_generation_run",
        lambda *args, **kwargs: ProcessingResult(1, False),
    )

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 1
    assert finalizer.call_args.kwargs["status"] == "failed"
    assert finalizer.call_args.kwargs["error_message"] == (
        "one or more sns_accounts did not reach success"
    )


def test_main_fails_processing_exception_and_finalizes_log(monkeypatch) -> None:
    """Unexpected processing errors are reflected in the execution log."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(main_module, "resolve_target_generation_run", lambda *args: 8)
    _patch_target_dependencies(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "process_target_generation_run",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("processing")),
    )

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 1
    assert finalizer.call_args.kwargs["status"] == "failed"
    assert finalizer.call_args.kwargs["records_processed"] == 0


def test_main_does_not_finalize_when_execution_log_start_fails(monkeypatch) -> None:
    """A log creation failure is returned directly because no log is available."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = Mock()
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(
        main_module,
        "start_or_resume_execution_log",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("failed")),
    )
    monkeypatch.setattr(main_module, "finalize_execution_log", finalizer)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 1
    finalizer.assert_not_called()


def test_main_uses_json_db_secret_without_secrets_manager(monkeypatch) -> None:
    """DB_SECRET_JSON is parsed directly."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    parsed_secret = object()
    parse_secret = Mock(return_value=parsed_secret)
    get_secret = Mock()
    monkeypatch.setattr(
        main_module,
        "load_config",
        lambda: _config('{"host":"db"}'),
    )
    monkeypatch.setattr(main_module, "parse_db_secret", parse_secret)
    monkeypatch.setattr(main_module, "get_db_secret", get_secret)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", False),
    )
    _patch_started_log(monkeypatch)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    parse_secret.assert_called_once_with('{"host":"db"}')
    get_secret.assert_not_called()
