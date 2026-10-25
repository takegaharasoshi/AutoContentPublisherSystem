"""Human-authored reply candidates, with an injectable random chooser."""

from __future__ import annotations

import random
from typing import Callable, Sequence


CORRECT = (
    "正解！！\nお見事👏👏",
    "正解💪💪\nお見事👏",
    "正解！\nお見事👏👏",
    "正解！！！\nお見事💪💪💪",
    "正解だ💪\nお見事🔥🔥",
    "正解！！\nお見事💪💪",
    "お見事！\n正解だ👏👏",
    "正解！！\nお見事🔥",
    "正解！\nお見事👏\nナイス脳みそトレーニング！",
    "正解💪💪\nお見事！\n脳みそトレーニングお疲れ様🔥🔥",
    "正解！\nお見事👏👏\n脳みそトレーニングお疲れ様！",
    "正解！\nお見事👏\nいい脳みそトレーニングになったな💪💪💪",
    "正解だ👏\nお見事🔥🔥\nこの調子で脳みそトレーニングを続けよう💪",
    "正解！！\nお見事💪💪\nこの調子で脳みそトレーニングを続けよう🔥🔥🔥",
    "お見事！\n正解だ👏👏\nナイス脳みそトレーニング！🔥",
    "正解！！\nお見事🔥\nこの調子で脳みそトレーニングを続けよう💪💪",
)
FIRST_CORRECT = (
    "正解！！\nお見事👏\n一番乗りだな💪💪",
    "正解💪\n一番乗りだ！\nお見事👏👏",
    "一番乗りで正解だ！！\nお見事🔥",
    "正解！！\nお見事👏\n一番乗りだな💪💪\nナイス脳みそトレーニング！🔥",
    "正解💪\n一番乗りだ！\nお見事👏👏\n脳みそトレーニングお疲れ様！💪",
    "一番乗りで正解だ！！\nお見事🔥\nこの調子で脳みそトレーニングを続けよう💪💪",
)


def make_reply(
    username: str, *, first: bool = False,
    chooser: Callable[[Sequence[str]], str] | None = None,
) -> str:
    """Choose a fixed reply and prepend the recipient's Instagram username."""
    if not isinstance(username, str) or not username.strip():
        raise ValueError("reply recipient username is required")
    return f"@{username} {(chooser or random.choice)(FIRST_CORRECT if first else CORRECT)}"
