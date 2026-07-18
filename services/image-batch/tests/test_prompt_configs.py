"""Tests for prompt configuration repository functions."""

from unittest.mock import Mock

from app.models import PromptConfig
from app.prompt_configs import fetch_active_prompt_configs


def test_fetch_active_prompt_configs_maps_rows_in_order() -> None:
    """Raw database JSON is kept unchanged in models."""
    cursor = Mock()
    cursor.fetchall.return_value = [
        (2, 1, "first", None, '{"size":"1024"}'),
        (4, 1, "second", "avoid", None),
    ]

    assert fetch_active_prompt_configs(cursor, 1) == [
        PromptConfig(2, 1, "first", None, '{"size":"1024"}'),
        PromptConfig(4, 1, "second", "avoid", None),
    ]
