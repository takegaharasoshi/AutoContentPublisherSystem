"""Tests for caption template repository functions."""

from unittest.mock import Mock

from app.caption_templates import fetch_active_caption_template
from app.models import CaptionTemplate


def test_fetch_active_caption_template_returns_first_row() -> None:
    """The first active template is returned."""
    cursor = Mock()
    cursor.fetchone.return_value = (8, "caption")

    assert fetch_active_caption_template(cursor, 4) == CaptionTemplate(8, "caption")
    cursor.execute.assert_called_once_with(
        "SELECT id, template_text FROM caption_templates "
        "WHERE set_id = %s AND is_active = 1 ORDER BY id LIMIT 1",
        (4,),
    )


def test_fetch_active_caption_template_returns_none_when_empty() -> None:
    """No active template is allowed."""
    cursor = Mock()
    cursor.fetchone.return_value = None

    assert fetch_active_caption_template(cursor, 4) is None
