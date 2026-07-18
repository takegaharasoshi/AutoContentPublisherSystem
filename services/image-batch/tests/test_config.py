"""Tests for image batch environment configuration."""

from __future__ import annotations

import pytest

from app.config import AppConfig, ConfigError, load_config


def _environ(**overrides: str) -> dict[str, str]:
    """Build valid configuration environment values."""
    values = {
        "ENV_NAME": "prod",
        "DB_SECRET_ARN": "arn:db",
        "SET_CODE": "sample-set",
        "EXECUTION_ARN": "arn:execution",
        "SCHEDULED_AT": "2026-07-19T00:00:00Z",
        "API_SECRET_ARN": "arn:api",
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


@pytest.mark.parametrize(
    "variable",
    ["SET_CODE", "EXECUTION_ARN", "SCHEDULED_AT", "API_SECRET_ARN", "S3_BUCKET_NAME"],
)
@pytest.mark.parametrize("value", [None, ""])
def test_load_config_rejects_missing_or_empty_required_value(
    variable: str,
    value: str | None,
) -> None:
    """Every image batch runtime setting is mandatory."""
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


def test_load_config_accepts_json_secret_and_keeps_raw_scheduled_at() -> None:
    """JSON DB settings and the raw scheduled time are retained as supplied."""
    environ = _environ(DB_SECRET_JSON='{"host": "db"}')
    del environ["DB_SECRET_ARN"]

    config = load_config(environ)

    assert config == AppConfig(
        env_name="prod",
        db_secret_arn=None,
        db_secret_json='{"host": "db"}',
        set_code="sample-set",
        execution_arn="arn:execution",
        scheduled_at="2026-07-19T00:00:00Z",
        api_secret_arn="arn:api",
        s3_bucket_name="bucket-name",
    )
