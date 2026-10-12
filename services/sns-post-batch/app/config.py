"""Application configuration loaded from environment variables."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import datetime
import os
import re


class ConfigError(Exception):
    """Raised when required application configuration is unavailable."""


@dataclass(frozen=True)
class AppConfig:
    """Configuration required to run the SNS posting batch."""

    env_name: str
    db_secret_arn: str | None
    db_secret_json: str | None
    set_code: str
    scheduled_at: datetime.datetime
    execution_arn: str
    s3_bucket_name: str


def load_config(environ: Mapping[str, str] | None = None) -> AppConfig:
    """Load and validate required environment variables.

    Args:
        environ: Environment mapping to load from. Uses ``os.environ`` by default.

    Returns:
        Validated application configuration.

    Raises:
        ConfigError: If a required variable is missing, empty, or invalid.
    """
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
        "S3_BUCKET_NAME": source.get("S3_BUCKET_NAME"),
    }
    for variable_name, value in required_values.items():
        if value is None or value == "":
            raise ConfigError(f"Required environment variable is missing: {variable_name}")

    raw_scheduled_at = source.get("SCHEDULED_AT")
    if raw_scheduled_at is None or raw_scheduled_at == "":
        raise ConfigError(
            "Required environment variable is missing: SCHEDULED_AT"
        )
    if re.fullmatch(
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", raw_scheduled_at
    ) is None:
        raise ConfigError(
            "Invalid SCHEDULED_AT: expected UTC YYYY-MM-DDTHH:MM:SSZ"
        )
    try:
        scheduled_at = datetime.datetime.strptime(
            raw_scheduled_at, "%Y-%m-%dT%H:%M:%SZ"
        )
    except ValueError as exc:
        raise ConfigError(
            "Invalid SCHEDULED_AT: datetime does not exist"
        ) from exc

    return AppConfig(
        env_name=env_name,
        db_secret_arn=db_secret_arn,
        db_secret_json=db_secret_json,
        set_code=required_values["SET_CODE"],
        scheduled_at=scheduled_at,
        execution_arn=required_values["EXECUTION_ARN"],
        s3_bucket_name=required_values["S3_BUCKET_NAME"],
    )
