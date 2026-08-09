"""Tests for shared SNS credential helpers."""

import pytest

from acps_shared.sns_secrets import (
    SnsCredentials,
    build_sns_secret_name,
    parse_sns_secret,
)


def test_build_sns_secret_name() -> None:
    """The SNS secret naming convention is stable."""
    assert build_sns_secret_name("prod", "set-a", "instagram", "main") == (
        "acps/prod/set-a/sns/instagram/main"
    )


def test_parse_sns_secret() -> None:
    """Required credentials are parsed from JSON."""
    assert parse_sns_secret('{"access_token":"token","ig_user_id":"123"}') == (
        SnsCredentials("token", "123")
    )


@pytest.mark.parametrize(
    "value",
    ["not-json", "[]", "{}", '{"access_token":1,"ig_user_id":"123"}'],
)
def test_parse_sns_secret_rejects_invalid_values(value: str) -> None:
    """Malformed and incomplete secrets are rejected."""
    with pytest.raises(ValueError):
        parse_sns_secret(value)
