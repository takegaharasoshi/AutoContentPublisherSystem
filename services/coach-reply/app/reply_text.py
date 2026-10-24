"""Human-authored reply candidates, with an injectable random chooser."""

from __future__ import annotations

import random
from typing import Callable, Sequence


CORRECT = (
    "正解！！お見事👏", "正解💪💪 お見事👏", "正解！お見事👏👏",
    "正解！！！お見事💪💪💪", "正解だ💪 お見事👏", "正解！！ よくわかったな💪",
    "お見事！正解だ👏👏", "正解！！お見事🔥",
)
FIRST_CORRECT = (
    "正解！！お見事👏 一番乗りだな💪💪", "正解💪 一番乗りだ！お見事👏👏",
    "一番乗りで正解だ！！お見事🔥",
)


def make_reply(
    username: str, *, first: bool = False,
    chooser: Callable[[Sequence[str]], str] | None = None,
) -> str:
    """Choose a fixed reply and prepend the recipient's Instagram username."""
    if not isinstance(username, str) or not username.strip():
        raise ValueError("reply recipient username is required")
    return f"@{username} {(chooser or random.choice)(FIRST_CORRECT if first else CORRECT)}"
