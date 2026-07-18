"""Tests for Secrets Manager parsing."""

import json
from unittest.mock import Mock

import pytest

from acps_shared import (
    DbSecret,
    SecretFormatError,
    get_db_secret,
    get_secret_string,
    parse_db_secret,
)


def _secret_json(**overrides: object) -> str:
    values: dict[str, object] = {
        "username": "test-user",
        "password": "very-secret-password",
        "host": "db.internal.example",
        "port": 3306,
        "dbname": "appdb",
    }
    values.update(overrides)
    return json.dumps(values)


def test_parse_db_secret_parses_valid_json() -> None:
    secret = parse_db_secret(_secret_json())

    assert secret == DbSecret(
        username="test-user",
        password="very-secret-password",
        host="db.internal.example",
        port=3306,
        dbname="appdb",
    )


def test_parse_db_secret_converts_string_port_to_int() -> None:
    secret = parse_db_secret(_secret_json(port="3306"))

    assert secret.port == 3306
    assert isinstance(secret.port, int)


def test_parse_db_secret_reports_missing_key_without_secret_values() -> None:
    secret_value = _secret_json()
    secret_data = json.loads(secret_value)
    del secret_data["password"]

    with pytest.raises(SecretFormatError) as exc_info:
        parse_db_secret(json.dumps(secret_data))

    message = str(exc_info.value)
    assert "password" in message
    assert "test-user" not in message
    assert "db.internal.example" not in message
    assert "very-secret-password" not in message


def test_parse_db_secret_rejects_invalid_json() -> None:
    with pytest.raises(SecretFormatError):
        parse_db_secret("not valid json")


def test_get_db_secret_uses_injected_client_and_arn() -> None:
    client = Mock()
    client.get_secret_value.return_value = {"SecretString": _secret_json()}

    secret = get_db_secret("arn:aws:secretsmanager:example", client=client)

    client.get_secret_value.assert_called_once_with(
        SecretId="arn:aws:secretsmanager:example"
    )
    assert secret.port == 3306


def test_get_secret_string_uses_injected_client_without_parsing() -> None:
    client = Mock()
    client.get_secret_value.return_value = {"SecretString": "not-json"}

    value = get_secret_string("arn:aws:secretsmanager:example", client=client)

    assert value == "not-json"
    client.get_secret_value.assert_called_once_with(
        SecretId="arn:aws:secretsmanager:example"
    )


def test_db_secret_repr_masks_all_values() -> None:
    secret = parse_db_secret(_secret_json())

    representation = repr(secret)

    assert "very-secret-password" not in representation
    assert "db.internal.example" not in representation
    assert "test-user" not in representation
    assert "appdb" not in representation
