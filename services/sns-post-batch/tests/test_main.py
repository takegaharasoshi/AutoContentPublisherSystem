"""Tests for the Phase 4 dry-run batch."""

import logging

from app.main import main


def test_main_returns_zero() -> None:
    assert main() == 0


def test_main_logs_hello_world(caplog) -> None:
    with caplog.at_level(logging.INFO):
        main()

    assert "Hello World" in caplog.text
