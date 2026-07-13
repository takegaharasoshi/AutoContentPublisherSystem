"""Tests for environment configuration loading."""

import pytest

from app.config import AppConfig, ConfigError, load_config


def test_load_config_creates_config_from_environment() -> None:
    config = load_config({"DB_SECRET_ARN": "arn:example", "ENV_NAME": "prod"})

    assert config == AppConfig(db_secret_arn="arn:example", env_name="prod")


@pytest.mark.parametrize(
    "environ",
    [
        {"ENV_NAME": "prod"},
        {"DB_SECRET_ARN": "arn:example"},
        {"DB_SECRET_ARN": "", "ENV_NAME": "prod"},
        {"DB_SECRET_ARN": "arn:example", "ENV_NAME": ""},
    ],
)
def test_load_config_rejects_missing_or_empty_required_value(
    environ: dict[str, str],
) -> None:
    with pytest.raises(ConfigError):
        load_config(environ)
