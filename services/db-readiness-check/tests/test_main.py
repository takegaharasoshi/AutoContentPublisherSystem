"""Tests for application orchestration."""

import os
from unittest.mock import Mock, patch

from app.config import AppConfig
from app.secrets import DbSecret
from app.main import main


def _config() -> AppConfig:
    return AppConfig(db_secret_arn="arn:example", env_name="prod")


def _secret() -> DbSecret:
    return DbSecret(
        username="user",
        password="very-secret-password",
        host="db.internal.example",
        port=3306,
        dbname="appdb",
    )


def test_main_returns_zero_when_database_is_ready() -> None:
    with patch("app.main.setup_logging"), \
            patch("app.main.load_config", return_value=_config()), \
            patch("app.main.get_db_secret", return_value=_secret()), \
            patch("app.main.wait_for_db", return_value=True) as wait:
        assert main() == 0

    wait.assert_called_once()


def test_main_returns_one_when_database_is_not_ready() -> None:
    with patch("app.main.setup_logging"), \
            patch("app.main.load_config", return_value=_config()), \
            patch("app.main.get_db_secret", return_value=_secret()), \
            patch("app.main.wait_for_db", return_value=False):
        assert main() == 1


def test_main_stops_before_secret_retrieval_when_config_is_invalid() -> None:
    get_secret = Mock()
    with patch.dict(os.environ, {}, clear=True), patch(
        "app.main.setup_logging"
    ), patch("app.main.get_db_secret", get_secret):
        assert main() == 1

    get_secret.assert_not_called()


def test_main_returns_one_when_secret_retrieval_fails() -> None:
    with patch("app.main.setup_logging"), \
            patch("app.main.load_config", return_value=_config()), \
            patch("app.main.get_db_secret", side_effect=RuntimeError("failed")):
        assert main() == 1


def test_main_never_logs_password(caplog) -> None:
    with patch("app.main.load_config", return_value=_config()), \
            patch("app.main.get_db_secret", return_value=_secret()), \
            patch("app.main.wait_for_db", return_value=True):
        assert main() == 0

    assert "very-secret-password" not in caplog.text
