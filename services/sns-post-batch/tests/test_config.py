"""Tests for environment configuration loading."""

import pytest

from app.config import AppConfig, ConfigError, load_config


@pytest.mark.parametrize("environ", [{}, {"ENV_NAME": ""}])
def test_load_config_rejects_missing_or_empty_env_name(
    environ: dict[str, str],
) -> None:
    with pytest.raises(ConfigError, match="ENV_NAME"):
        load_config(environ)


@pytest.mark.parametrize(
    "environ",
    [{"ENV_NAME": "prod"}, {"ENV_NAME": "prod", "DB_SECRET_JSON": ""}],
)
def test_load_config_rejects_missing_secret_source(environ: dict[str, str]) -> None:
    with pytest.raises(ConfigError, match="DB_SECRET_JSON or DB_SECRET_ARN"):
        load_config(environ)


def test_load_config_accepts_secret_arn() -> None:
    config = load_config({"ENV_NAME": "prod", "DB_SECRET_ARN": "arn:example"})

    assert config == AppConfig("prod", "arn:example", None)


def test_load_config_accepts_secret_json() -> None:
    config = load_config({"ENV_NAME": "local", "DB_SECRET_JSON": "{\"host\": \"db\"}"})

    assert config == AppConfig("local", None, "{\"host\": \"db\"}")


def test_load_config_keeps_both_secret_sources() -> None:
    config = load_config(
        {
            "ENV_NAME": "prod",
            "DB_SECRET_ARN": "arn:example",
            "DB_SECRET_JSON": "{\"host\": \"db\"}",
        }
    )

    assert config == AppConfig("prod", "arn:example", "{\"host\": \"db\"}")
