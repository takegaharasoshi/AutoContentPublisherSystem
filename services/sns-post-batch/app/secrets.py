"""SNS credential naming and parsing helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json


def build_sns_secret_name(
    env_name: str,
    set_code: str,
    platform: str,
    account_code: str,
) -> str:
    """Build the Secrets Manager name for one SNS account."""
    return f"acps/{env_name}/{set_code}/sns/{platform}/{account_code}"


@dataclass(frozen=True)
class SnsCredentials:
    """Credentials required by the supported Instagram API flow."""

    access_token: str
    ig_user_id: str


def parse_sns_secret(secret_string: str) -> SnsCredentials:
    """Parse an SNS credential SecretString.

    Args:
        secret_string: JSON SecretString from Secrets Manager.

    Returns:
        Parsed access token and Instagram user ID.

    Raises:
        ValueError: If the JSON or required keys are invalid.
    """
    try:
        value = json.loads(secret_string)
    except (TypeError, json.JSONDecodeError):
        raise ValueError("SNS secret JSON is invalid") from None

    if not isinstance(value, dict):
        raise ValueError("SNS secret JSON must be an object")

    required_keys = ("access_token", "ig_user_id")
    missing_keys = [key for key in required_keys if key not in value]
    if missing_keys:
        raise ValueError(
            "SNS secret is missing required keys: " + ", ".join(missing_keys)
        )

    for key in required_keys:
        if not isinstance(value[key], str):
            raise ValueError(f"SNS secret key must be a string: {key}")

    return SnsCredentials(
        access_token=value["access_token"],
        ig_user_id=value["ig_user_id"],
    )
