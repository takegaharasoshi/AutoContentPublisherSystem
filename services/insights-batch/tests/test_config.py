"""Tests for insights batch configuration."""

import pytest

from app.config import ConfigError, load_config


BASE_ENV = {
    "ENV_NAME": "prod",
    "DB_SECRET_JSON": "{}",
    "SET_CODE": "set-a",
    "EXECUTION_ARN": "arn:execution",
    "SCHEDULED_AT": "2026-08-10T09:00:00Z",
}


def test_load_config_uses_default_lookback() -> None:
    """Media lookback defaults to fourteen days."""
    config = load_config(BASE_ENV)
    assert config.media_lookback_days == 14
    assert config.comment_log_bucket is None
    assert config.comment_log_lookback_days == 3
    assert config.comment_log_retention_days == 365


def test_load_config_accepts_positive_lookback() -> None:
    """A positive integer override is accepted."""
    assert load_config({**BASE_ENV, "MEDIA_LOOKBACK_DAYS": "90"}).media_lookback_days == 90


def test_load_config_accepts_comment_log_settings() -> None:
    """Comment log bucket and positive day overrides are loaded."""
    config = load_config(
        {
            **BASE_ENV,
            "COMMENT_LOG_BUCKET": "assets",
            "COMMENT_LOG_LOOKBACK_DAYS": "7",
            "COMMENT_LOG_RETENTION_DAYS": "180",
        }
    )
    assert config.comment_log_bucket == "assets"
    assert config.comment_log_lookback_days == 7
    assert config.comment_log_retention_days == 180


@pytest.mark.parametrize(
    ("variable", "value"),
    [
        ("COMMENT_LOG_LOOKBACK_DAYS", "0"),
        ("COMMENT_LOG_LOOKBACK_DAYS", "-1"),
        ("COMMENT_LOG_LOOKBACK_DAYS", "x"),
        ("COMMENT_LOG_LOOKBACK_DAYS", "1.5"),
        ("COMMENT_LOG_RETENTION_DAYS", "0"),
        ("COMMENT_LOG_RETENTION_DAYS", "-1"),
        ("COMMENT_LOG_RETENTION_DAYS", "x"),
        ("COMMENT_LOG_RETENTION_DAYS", "1.5"),
    ],
)
def test_load_config_rejects_invalid_comment_log_days(variable: str, value: str) -> None:
    """Comment log date settings must be positive integers."""
    with pytest.raises(ConfigError):
        load_config({**BASE_ENV, variable: value})


@pytest.mark.parametrize("value", ["0", "-1", "x", "1.5"])
def test_load_config_rejects_invalid_lookback(value: str) -> None:
    """Lookback must be a positive integer."""
    with pytest.raises(ConfigError):
        load_config({**BASE_ENV, "MEDIA_LOOKBACK_DAYS": value})


@pytest.mark.parametrize(
    "missing", ["ENV_NAME", "DB_SECRET_JSON", "SET_CODE", "EXECUTION_ARN", "SCHEDULED_AT"]
)
def test_load_config_rejects_missing_required_values(missing: str) -> None:
    """Every required configuration input is validated."""
    env = dict(BASE_ENV)
    env.pop(missing)
    with pytest.raises(ConfigError):
        load_config(env)
