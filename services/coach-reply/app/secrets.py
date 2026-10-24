"""Secrets Manager lookup, refreshed on each scheduled invocation."""

from __future__ import annotations

import base64
import json
from typing import Any


def get_secrets(secret_arn: str, *, client: Any = None) -> dict[str, str]:
    """Load the current JSON secret so weekly token refreshes take effect."""
    if not secret_arn:
        raise ValueError("SECRET_ARN is required")
    if client is None:
        import boto3

        client = boto3.client("secretsmanager")
    result = client.get_secret_value(SecretId=secret_arn)
    if "SecretString" in result:
        encoded = result["SecretString"]
    else:
        raw = result["SecretBinary"]
        encoded = raw.decode("utf-8") if isinstance(raw, bytes) else base64.b64decode(raw).decode("utf-8")
    data = json.loads(encoded)
    if not isinstance(data, dict):
        raise ValueError("SecretString must contain a JSON object")
    secrets = {key: str(value) for key, value in data.items() if isinstance(value, str)}
    return secrets


def require_keys(secrets: dict[str, str], *keys: str) -> None:
    """Reject absent or blank secret fields without displaying secret values."""
    missing = [key for key in keys if not secrets.get(key, "").strip()]
    if missing:
        raise ValueError(f"missing secret fields: {', '.join(missing)}")
