"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os
from collections.abc import Mapping


class ConfigError(Exception):
    """Raised when required application configuration is unavailable."""


@dataclass(frozen=True)
class AppConfig:
    """Configuration required to run the readiness check."""

    db_secret_arn: str
    env_name: str


def load_config(environ: Mapping[str, str] | None = None) -> AppConfig:
    """Load and validate required environment variables.

    Args:
        environ: Environment mapping to load from. Uses ``os.environ`` by default.

    Returns:
        Validated application configuration.

    Raises:
        ConfigError: If a required environment variable is missing or empty.
    """
    source = os.environ if environ is None else environ
    values: dict[str, str] = {}

    for name in ("DB_SECRET_ARN", "ENV_NAME"):
        value = source.get(name)
        if value is None or value == "":
            raise ConfigError(f"Required environment variable is missing: {name}")
        values[name] = value

    return AppConfig(
        db_secret_arn=values["DB_SECRET_ARN"],
        env_name=values["ENV_NAME"],
    )
