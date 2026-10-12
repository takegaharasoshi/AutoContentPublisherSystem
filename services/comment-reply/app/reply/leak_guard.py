"""Shared core-word checks for reply output and offline probe evaluation."""

from __future__ import annotations

from app.judge.contract import CoreWords


def find_leaks(reply: str, comment_text: str, core_words: CoreWords) -> list[str]:
    """Return unquoted core words in snapshot order, after exclusions."""
    checked = reply
    for phrase in core_words.excepts:
        if phrase:
            checked = checked.replace(phrase, "")
    return list(dict.fromkeys(word for word in core_words.words
                              if word and word in checked and word not in comment_text))


def is_correct_reveal(kind: str | None, reply: str) -> bool:
    """Allow a declared correct answer to disclose the solution."""
    return kind == "guess_correct" or reply.startswith("正解")
