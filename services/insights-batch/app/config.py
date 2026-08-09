"""Application configuration loaded from environment variables."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import os


class ConfigError(Exception):
    """Raised when required application configuration is unavailable."""


@dataclass(frozen=True)
class AppConfig:
    """Configuration required to run the insights collection batch."""

    env_name: str
    db_secret_arn: str | None
    db_secret_json: str | None
    set_code: str
    execution_arn: str
    scheduled_at: str
    media_lookback_days: int


def load_config(environ: Mapping[str, str] | None = None) -> AppConfig:
    """Load and validate required environment variables."""
    source = os.environ if environ is None else environ
    env_name = source.get("ENV_NAME")
    if env_name is None or env_name == "":
        raise ConfigError("Required environment variable is missing: ENV_NAME")

    db_secret_json = source.get("DB_SECRET_JSON")
    db_secret_arn = source.get("DB_SECRET_ARN")
    if (db_secret_json is None or db_secret_json == "") and (
        db_secret_arn is None or db_secret_arn == ""
    ):
        raise ConfigError(
            "Required environment variable is missing: DB_SECRET_JSON or DB_SECRET_ARN"
        )

    required_values = {
        "SET_CODE": source.get("SET_CODE"),
        "EXECUTION_ARN": source.get("EXECUTION_ARN"),
        "SCHEDULED_AT": source.get("SCHEDULED_AT"),
    }
    for variable_name, value in required_values.items():
        if value is None or value == "":
            raise ConfigError(
                f"Required environment variable is missing: {variable_name}"
            )

    raw_lookback = source.get("MEDIA_LOOKBACK_DAYS", "14")
    try:
        media_lookback_days = int(raw_lookback)
    except (TypeError, ValueError):
        raise ConfigError(
            "MEDIA_LOOKBACK_DAYS must be an integer of at least 1"
        ) from None
    if media_lookback_days < 1:
        raise ConfigError("MEDIA_LOOKBACK_DAYS must be an integer of at least 1")

    return AppConfig(
        env_name=env_name,
        db_secret_arn=db_secret_arn,
        db_secret_json=db_secret_json,
        set_code=required_values["SET_CODE"],
        execution_arn=required_values["EXECUTION_ARN"],
        scheduled_at=required_values["SCHEDULED_AT"],
        media_lookback_days=media_lookback_days,
    )
