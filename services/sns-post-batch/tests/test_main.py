"""Tests for SNS posting batch orchestration."""

from contextlib import contextmanager
from datetime import datetime
import logging
from unittest.mock import Mock, call

import pytest

import app.main as main_module

from app.config import AppConfig, ConfigError
from app.models import BatchSet, CaptionTemplate, GeneratedMediaRef, SnsAccount
from app.processing import ProcessingResult
from app.target_selection import TargetOutcome, TargetSelection


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
        scheduled_at=datetime(2026, 10, 12, 22, 30),
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


def _patch_target_dependencies(monkeypatch, *, media=True) -> None:
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
        "fetch_first_generated_media",
        lambda cursor, run_id: GeneratedMediaRef(4, "bucket", "images/a.jpg", "jpg")
        if media
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
    selector = Mock()
    monkeypatch.setattr(main_module, "select_current_generation_run", selector)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    selector.assert_not_called()
    assert finalizer.call_args.kwargs["status"] == "succeeded"
    assert finalizer.call_args.kwargs["records_processed"] == 0
    assert connection.commit.call_count == 2


def test_main_succeeds_when_current_run_is_already_terminal(
    monkeypatch, caplog
) -> None:
    """A terminal current run succeeds with zero records and no posting work."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    selector = Mock(
        return_value=TargetSelection(TargetOutcome.ALREADY_TERMINAL, 8)
    )
    monkeypatch.setattr(main_module, "select_current_generation_run", selector)
    processor = Mock()
    monkeypatch.setattr(main_module, "process_target_generation_run", processor)
    caplog.set_level(logging.INFO)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    selector.assert_called_once_with(
        connection.cursor_value, 1, datetime(2026, 10, 12, 22, 30)
    )
    processor.assert_not_called()
    assert "ALREADY_TERMINAL" in caplog.text
    assert "records_processed=0" in caplog.text
    assert finalizer.call_args.kwargs == {
        "log_id": 10,
        "status": "succeeded",
        "records_processed": 0,
        "error_message": None,
        "finished_at": finalizer.call_args.kwargs["finished_at"],
    }


@pytest.mark.parametrize(
    "outcome", [TargetOutcome.RUN_NOT_FOUND, TargetOutcome.NO_MEDIA]
)
def test_main_fails_when_current_run_or_media_is_missing(
    monkeypatch, caplog, outcome: TargetOutcome
) -> None:
    """A missing current run or media fails without attempting any posting work."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module, "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    selector = Mock(
        return_value=TargetSelection(
            outcome, None if outcome == TargetOutcome.RUN_NOT_FOUND else 8
        )
    )
    monkeypatch.setattr(main_module, "select_current_generation_run", selector)
    dependencies = [
        "fetch_first_generated_media",
        "fetch_active_caption_template",
        "build_caption",
        "fetch_active_sns_accounts",
        "process_target_generation_run",
    ]
    unused = [Mock() for _ in dependencies]
    for name, dependency in zip(dependencies, unused):
        monkeypatch.setattr(main_module, name, dependency)
    opener = Mock()

    assert main_module.main(s3_client=Mock(), urlopen=opener) == 1
    selector.assert_called_once_with(
        connection.cursor_value, 1, datetime(2026, 10, 12, 22, 30)
    )
    for dependency in unused:
        dependency.assert_not_called()
    opener.assert_not_called()
    assert finalizer.call_args.kwargs["status"] == "failed"
    assert finalizer.call_args.kwargs["records_processed"] == 0
    error_message = finalizer.call_args.kwargs["error_message"]
    for value in (outcome.name, "set-a", "2026-10-12T22:30:00Z"):
        assert value in error_message
        assert value in caplog.text
    assert any(record.levelno == logging.ERROR for record in caplog.records)


@pytest.mark.parametrize(
    "scheduled_at",
    [
        None,
        "",
        "2026-10-13 21:00:00",
        "2026-10-13T21:00:00+09:00",
        "2026-10-13T12:00:00.000Z",
        "2026-10-13",
        "2026-1-13T12:00:00Z",
        "2026-02-30T12:00:00Z",
    ],
)
def test_main_rejects_invalid_scheduled_at_before_db_connection(
    monkeypatch, scheduled_at: str | None
) -> None:
    """The real config loader rejects invalid times before DB or API calls."""
    for name, value in {
        "ENV_NAME": "local",
        "DB_SECRET_JSON": '{"host":"db"}',
        "SET_CODE": "set-a",
        "EXECUTION_ARN": "arn:execution",
        "S3_BUCKET_NAME": "bucket",
    }.items():
        monkeypatch.setenv(name, value)
    if scheduled_at is None:
        monkeypatch.delenv("SCHEDULED_AT", raising=False)
    else:
        monkeypatch.setenv("SCHEDULED_AT", scheduled_at)
    forbidden_connection = Mock(
        side_effect=AssertionError("DB must not be opened")
    )
    monkeypatch.setattr(main_module, "open_connection", forbidden_connection)
    opener = Mock()

    assert main_module.main(s3_client=Mock(), urlopen=opener) == 1
    forbidden_connection.assert_not_called()
    opener.assert_not_called()


def test_main_fails_when_target_has_no_generated_media(monkeypatch) -> None:
    """Missing target media is a data inconsistency recorded as failed."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    finalizer = _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(
        main_module,
        "select_current_generation_run",
        lambda *args: TargetSelection(TargetOutcome.SELECTED, 8),
    )
    _patch_target_dependencies(monkeypatch, media=False)

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
    monkeypatch.setattr(
        main_module,
        "select_current_generation_run",
        lambda *args: TargetSelection(TargetOutcome.SELECTED, 8),
    )
    _patch_target_dependencies(monkeypatch)
    processor = Mock(return_value=ProcessingResult(1, True))
    monkeypatch.setattr(main_module, "process_target_generation_run", processor)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    assert finalizer.call_args.kwargs["status"] == "succeeded"
    assert finalizer.call_args.kwargs["records_processed"] == 1
    processor.assert_called_once()
    assert processor.call_args.kwargs["stories_enabled"] is False
    assert processor.call_args.kwargs["problem_snapshot_enabled"] is False


def test_main_passes_enabled_problem_snapshot_flag(monkeypatch) -> None:
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True, False, True),
    )
    monkeypatch.setattr(
        main_module,
        "select_current_generation_run",
        lambda *args: TargetSelection(TargetOutcome.SELECTED, 8),
    )
    _patch_target_dependencies(monkeypatch)
    processor = Mock(return_value=ProcessingResult(1, True))
    monkeypatch.setattr(main_module, "process_target_generation_run", processor)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    assert processor.call_args.kwargs["problem_snapshot_enabled"] is True


def test_main_builds_caption_once_before_processing_accounts(monkeypatch) -> None:
    """Caption expansion happens once for the selected generation run."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(
        main_module,
        "select_current_generation_run",
        lambda *args: TargetSelection(TargetOutcome.SELECTED, 8),
    )
    _patch_target_dependencies(monkeypatch)
    builder = Mock(return_value="展開後キャプション")
    processor = Mock(return_value=ProcessingResult(1, True))
    monkeypatch.setattr(main_module, "build_caption", builder)
    monkeypatch.setattr(main_module, "process_target_generation_run", processor)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    builder.assert_called_once_with(connection.cursor_value, 8, "caption", set_id=1)
    assert processor.call_args.kwargs["caption_text"] == "展開後キャプション"


def test_main_fetches_media_before_caption_assembly(monkeypatch, caplog) -> None:
    """The selected run's media is checked before templates or dynamic captions."""
    connection = FakeConnection()
    _patch_base(monkeypatch, connection)
    _patch_started_log(monkeypatch)
    monkeypatch.setattr(
        main_module, "find_batch_set_by_code",
        lambda cursor, code: BatchSet(1, "set-a", True),
    )
    monkeypatch.setattr(
        main_module, "select_current_generation_run",
        lambda *args: TargetSelection(TargetOutcome.SELECTED, 8),
    )
    _patch_target_dependencies(monkeypatch)
    calls = Mock()
    calls.attach_mock(
        Mock(return_value=GeneratedMediaRef(4, "bucket", "images/a.jpg", "jpg")),
        "media",
    )
    calls.attach_mock(
        Mock(return_value=CaptionTemplate(3, "caption")), "template"
    )
    calls.attach_mock(Mock(return_value="expanded"), "caption")
    calls.attach_mock(Mock(return_value=ProcessingResult(1, True)), "process")
    monkeypatch.setattr(main_module, "fetch_first_generated_media", calls.media)
    monkeypatch.setattr(main_module, "fetch_active_caption_template", calls.template)
    monkeypatch.setattr(main_module, "build_caption", calls.caption)
    monkeypatch.setattr(main_module, "process_target_generation_run", calls.process)
    caplog.set_level(logging.INFO)

    assert main_module.main(s3_client=Mock(), urlopen=Mock()) == 0
    assert [entry[0] for entry in calls.mock_calls] == [
        "media", "template", "caption", "process"
    ]
    assert calls.mock_calls[:3] == [
        call.media(connection.cursor_value, 8),
        call.template(connection.cursor_value, 1),
        call.caption(connection.cursor_value, 8, "caption", set_id=1),
    ]
    assert "set_code=set-a scheduled_at=2026-10-12T22:30:00Z" in caplog.text


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
    monkeypatch.setattr(
        main_module,
        "select_current_generation_run",
        lambda *args: TargetSelection(TargetOutcome.SELECTED, 8),
    )
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
    monkeypatch.setattr(
        main_module,
        "select_current_generation_run",
        lambda *args: TargetSelection(TargetOutcome.SELECTED, 8),
    )
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
