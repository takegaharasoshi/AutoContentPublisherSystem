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
    assert load_config(BASE_ENV).media_lookback_days == 14


def test_load_config_accepts_positive_lookback() -> None:
    """A positive integer override is accepted."""
    assert load_config({**BASE_ENV, "MEDIA_LOOKBACK_DAYS": "90"}).media_lookback_days == 90


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
