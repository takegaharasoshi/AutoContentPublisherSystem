"""Secrets Manager integration for database connection credentials."""

from dataclasses import dataclass
import json
from typing import Any

import boto3


class SecretFormatError(Exception):
    """Raised when a database secret does not have the expected schema."""


@dataclass(frozen=True, repr=False)
class DbSecret:
    """Database connection parameters kept out of diagnostic representations."""

    username: str
    password: str
    host: str
    port: int
    dbname: str

    def __repr__(self) -> str:
        """Return a representation that never exposes secret values."""
        return (
            "DbSecret(username='***', password='***', host='***', "
            "port=***, dbname='***')"
        )


def parse_db_secret(secret_string: str) -> DbSecret:
    """Parse a Secrets Manager JSON value into database connection parameters.

    Args:
        secret_string: JSON SecretString returned by Secrets Manager.

    Returns:
        Validated database connection parameters.

    Raises:
        SecretFormatError: If the JSON is malformed or does not have the schema.
    """
    try:
        value = json.loads(secret_string)
    except (TypeError, json.JSONDecodeError):
        raise SecretFormatError("Secret JSON is invalid") from None

    if not isinstance(value, dict):
        raise SecretFormatError("Secret JSON must be an object")

    required_keys = ("username", "password", "host", "port", "dbname")
    missing_keys = [key for key in required_keys if key not in value]
    if missing_keys:
        raise SecretFormatError(
            "Secret is missing required keys: " + ", ".join(missing_keys)
        )

    port_value = value["port"]
    if isinstance(port_value, bool) or not isinstance(port_value, (str, int)):
        raise SecretFormatError("Secret port must be an integer")
    try:
        port = int(port_value)
    except ValueError:
        raise SecretFormatError("Secret port must be an integer") from None

    for key in ("username", "password", "host", "dbname"):
        if not isinstance(value[key], str):
            raise SecretFormatError(f"Secret key must be a string: {key}")

    return DbSecret(
        username=value["username"],
        password=value["password"],
        host=value["host"],
        port=port,
        dbname=value["dbname"],
    )


def get_db_secret(secret_arn: str, client: Any | None = None) -> DbSecret:
    """Retrieve and parse the database secret once from Secrets Manager.

    Args:
        secret_arn: ARN of the database secret.
        client: Optional Secrets Manager client, for dependency injection.

    Returns:
        Parsed database connection parameters.
    """
    secrets_client = client if client is not None else boto3.client("secretsmanager")
    response = secrets_client.get_secret_value(SecretId=secret_arn)
    return parse_db_secret(response["SecretString"])
