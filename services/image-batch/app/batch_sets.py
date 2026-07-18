"""Repository functions for batch sets."""

from typing import Any

from .models import BatchSet


def find_batch_set_by_code(cursor: Any, set_code: str) -> BatchSet | None:
    """Find a batch set by its external set code.

    Args:
        cursor: Database cursor.
        set_code: Batch set code to find.

    Returns:
        The batch set, or ``None`` when it is not found.
    """
    cursor.execute(
        "SELECT id, set_code, generator_name, is_active "
        "FROM batch_sets WHERE set_code = %s",
        (set_code,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return BatchSet(
        id=row[0],
        set_code=row[1],
        generator_name=row[2],
        is_active=bool(row[3]),
    )
