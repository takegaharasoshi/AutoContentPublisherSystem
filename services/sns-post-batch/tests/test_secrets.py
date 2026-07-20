"""Tests for SNS credential helpers."""

import json

import pytest

from app.secrets import (
    SnsCredentials,
    build_sns_secret_name,
    parse_sns_secret,
)


def test_build_sns_secret_name_follows_security_convention() -> None:
    """The name includes environment, set, platform, and account code."""
    assert build_sns_secret_name("prod", "set-a", "instagram", "main") == (
        "acps/prod/set-a/sns/instagram/main"
    )


def test_parse_sns_secret_reads_required_credentials_and_ignores_expiry() -> None:
    """Only access_token and ig_user_id are needed by the API client."""
    assert parse_sns_secret(
        json.dumps(
            {
                "access_token": "token",
                "ig_user_id": "123",
                "token_expires_at": "2099-01-01T00:00:00Z",
            }
        )
    ) == SnsCredentials("token", "123")


@pytest.mark.parametrize(
    "secret",
    ["not-json", "[]", '{"access_token":"token"}', '{"ig_user_id":"123"}'],
)
def test_parse_sns_secret_rejects_invalid_or_missing_values(secret: str) -> None:
    """Malformed JSON and missing required keys are errors."""
    with pytest.raises(ValueError):
        parse_sns_secret(secret)
