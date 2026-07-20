"""Tests for SNS posting data models."""

from dataclasses import FrozenInstanceError

import pytest

from app.models import (
    BatchSet,
    CaptionTemplate,
    GeneratedImageRef,
    Post,
    SnsAccount,
)


@pytest.mark.parametrize(
    "model",
    [
        BatchSet(1, "set", True),
        SnsAccount(2, "instagram", "main", "Main"),
        CaptionTemplate(3, "caption"),
        GeneratedImageRef(4, "bucket", "key"),
        Post(5, "pending", None, None),
    ],
)
def test_models_are_frozen(model) -> None:
    """All repository models reject field mutation."""
    with pytest.raises(FrozenInstanceError):
        model.id = 99
