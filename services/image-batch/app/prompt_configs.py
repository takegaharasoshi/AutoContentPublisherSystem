"""Repository functions for prompt configurations."""

from typing import Any

from .models import PromptConfig


def fetch_active_prompt_configs(cursor: Any, set_id: int) -> list[PromptConfig]:
    """Fetch all active prompt configurations for a batch set.

    Args:
        cursor: Database cursor.
        set_id: Batch set ID.

    Returns:
        Active prompt configurations ordered by ID.
    """
    cursor.execute(
        "SELECT id, set_id, prompt_text, negative_prompt, parameters "
        "FROM prompt_configs WHERE set_id = %s AND is_active = 1 ORDER BY id",
        (set_id,),
    )
    return [
        PromptConfig(
            id=row[0],
            set_id=row[1],
            prompt_text=row[2],
            negative_prompt=row[3],
            parameters=row[4],
        )
        for row in cursor.fetchall()
    ]
