"""Tests for SNS posting batch environment configuration."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.config import AppConfig, ConfigError, load_config


def _environ(**overrides: str) -> dict[str, str]:
    """Build valid configuration environment values."""
    values = {
        "ENV_NAME": "prod",
        "DB_SECRET_ARN": "arn:db",
        "SET_CODE": "sample-set",
        "SCHEDULED_AT": "2026-10-12T22:30:00Z",
        "EXECUTION_ARN": "arn:execution",
        "S3_BUCKET_NAME": "bucket-name",
    }
    values.update(overrides)
    return values


@pytest.mark.parametrize("value", [None, ""])
def test_load_config_rejects_missing_or_empty_env_name(value: str | None) -> None:
    """ENV_NAME is mandatory."""
    environ = _environ()
    if value is None:
        del environ["ENV_NAME"]
    else:
        environ["ENV_NAME"] = value

    with pytest.raises(ConfigError, match="ENV_NAME"):
        load_config(environ)


@pytest.mark.parametrize("variable", ["SET_CODE", "EXECUTION_ARN", "S3_BUCKET_NAME"])
@pytest.mark.parametrize("value", [None, ""])
def test_load_config_rejects_missing_or_empty_required_value(
    variable: str,
    value: str | None,
) -> None:
    """SNS batch runtime settings are mandatory."""
    environ = _environ()
    if value is None:
        del environ[variable]
    else:
        environ[variable] = value

    with pytest.raises(ConfigError, match=variable):
        load_config(environ)


def test_load_config_rejects_missing_secret_source() -> None:
    """At least one database secret source is required."""
    environ = _environ()
    del environ["DB_SECRET_ARN"]

    with pytest.raises(ConfigError, match="DB_SECRET_JSON or DB_SECRET_ARN"):
        load_config(environ)


def test_load_config_accepts_json_secret() -> None:
    """JSON DB settings and SNS settings are retained."""
    environ = _environ(DB_SECRET_JSON='{"host": "db"}')
    del environ["DB_SECRET_ARN"]

    assert load_config(environ) == AppConfig(
        env_name="prod",
        db_secret_arn=None,
        db_secret_json='{"host": "db"}',
        set_code="sample-set",
        scheduled_at=datetime(2026, 10, 12, 22, 30, 0),
        execution_arn="arn:execution",
        s3_bucket_name="bucket-name",
    )


def test_load_config_does_not_require_image_batch_only_variables() -> None:
    """API_SECRET_ARN is not an SNS batch setting."""
    config = load_config(_environ())

    assert config.set_code == "sample-set"
    assert config.s3_bucket_name == "bucket-name"


def test_load_config_parses_scheduled_at_as_naive_utc() -> None:
    """The scheduler timestamp matches the UTC DATETIME stored in MySQL."""
    config = load_config(_environ())

    assert config.scheduled_at == datetime(2026, 10, 12, 22, 30, 0)
    assert config.scheduled_at.tzinfo is None


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "2026-10-13 21:00:00",
        "2026-10-13T21:00:00+09:00",
        "2026-10-13T12:00:00.000Z",
        "2026-10-13",
        "2026-1-13T12:00:00Z",
        "2026-10-3T12:00:00Z",
        "2026-10-13T2:00:00Z",
        "2026-10-13T12:0:00Z",
        "2026-10-13T12:00:0Z",
        "2026-02-30T12:00:00Z",
        "2026-10-13T24:00:00Z",
        "2026-10-13T12:60:00Z",
        "2026-10-13T12:00:60Z",
        "2026-10-13T12:00:00Z\n",
        " 2026-10-13T12:00:00Z",
        "2026-10-13T12:00:00Z ",
    ],
)
def test_load_config_rejects_invalid_scheduled_at(value: str | None) -> None:
    """Only an exact UTC timestamp representing a real datetime is accepted."""
    environ = _environ()
    if value is None:
        del environ["SCHEDULED_AT"]
    else:
        environ["SCHEDULED_AT"] = value

    with pytest.raises(ConfigError, match="SCHEDULED_AT"):
        load_config(environ)
