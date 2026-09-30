"""Secrets Manager lookup, cached only within a warm Lambda process."""

from __future__ import annotations

import base64
import json
from typing import Any


_cache: dict[str, dict[str, str]] = {}


def get_secrets(secret_arn: str, *, client: Any = None) -> dict[str, str]:
    """Load a JSON secret from AWS and cache it by ARN."""
    if not secret_arn:
        raise ValueError("SECRET_ARN is required")
    if client is None and secret_arn in _cache:
        return _cache[secret_arn]
    if client is None:
        import boto3

        client = boto3.client("secretsmanager")
    result = client.get_secret_value(SecretId=secret_arn)
    if "SecretString" in result:
        encoded = result["SecretString"]
    else:
        encoded = base64.b64decode(result["SecretBinary"]).decode("utf-8")
    data = json.loads(encoded)
    if not isinstance(data, dict):
        raise ValueError("SecretString must contain a JSON object")
    secrets = {key: str(value) for key, value in data.items() if isinstance(value, str)}
    if client is not None:
        _cache[secret_arn] = secrets
    return secrets


def require_keys(secrets: dict[str, str], *keys: str) -> None:
    """Reject absent or blank secret fields without displaying secret values."""
    missing = [key for key in keys if not secrets.get(key)]
    if missing:
        raise ValueError(f"missing secret fields: {', '.join(missing)}")
