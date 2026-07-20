"""Tests for SNS posting batch environment configuration."""

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
        execution_arn="arn:execution",
        s3_bucket_name="bucket-name",
    )


def test_load_config_does_not_require_image_batch_only_variables() -> None:
    """SCHEDULED_AT and API_SECRET_ARN are not SNS batch settings."""
    config = load_config(_environ())

    assert config.set_code == "sample-set"
    assert config.s3_bucket_name == "bucket-name"
