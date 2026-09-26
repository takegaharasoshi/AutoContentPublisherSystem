"""Tests for SNS posting data models."""

from dataclasses import FrozenInstanceError

import pytest

from app.models import (
    BatchSet,
    CaptionTemplate,
    GeneratedMediaRef,
    Post,
    RankingItem,
    SnsAccount,
    UmigameItem,
)


@pytest.mark.parametrize(
    "model",
    [
        BatchSet(1, "set", True, False),
        SnsAccount(2, "instagram", "main", "Main"),
        CaptionTemplate(3, "caption"),
        GeneratedMediaRef(4, "bucket", "key", "jpg"),
        RankingItem("ランキング題", {"hook": "つかみ"}),
        UmigameItem(
            1, "001-problem", "問題", "真相", ["事実"], "ルール", "フック", "本文"
        ),
        Post(5, "pending", None, None),
    ],
)
def test_models_are_frozen(model) -> None:
    """All repository models reject field mutation."""
    with pytest.raises(FrozenInstanceError):
        model.id = 99
