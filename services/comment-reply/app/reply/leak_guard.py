"""Shared core-word checks for reply output and offline probe evaluation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


LEAK_WORDS_PATH = Path(__file__).with_name("leak_words.json")


@dataclass(frozen=True)
class LeakEntry:
    """Core words and exclusions for one problem."""

    no: str
    content_key: str
    words: tuple[str, ...]
    excepts: tuple[str, ...] = ()


@lru_cache(maxsize=4)
def load_leak_words(path: Path = LEAK_WORDS_PATH) -> dict[str, LeakEntry]:
    """Load the problem-number index from the bundled leak-word dictionary."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = {
        no: LeakEntry(no, item["content_key"], tuple(item["words"]),
                      tuple(item.get("except", ())))
        for no, item in data["problems"].items()
    }
    keys = [entry.content_key for entry in entries.values()]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate content_key in leak-word dictionary")
    return entries


def entry_for_content_key(content_key: str) -> LeakEntry | None:
    """Find the entry belonging to a stored content key."""
    return next((entry for entry in load_leak_words().values()
                 if entry.content_key == content_key), None)


def find_leaks(reply: str, comment_text: str, entry: LeakEntry) -> list[str]:
    """Return unquoted core words in dictionary order, after exclusions."""
    checked = reply
    for phrase in entry.excepts:
        if phrase:
            checked = checked.replace(phrase, "")
    return list(dict.fromkeys(word for word in entry.words
                              if word and word in checked and word not in comment_text))


def is_correct_reveal(kind: str | None, reply: str) -> bool:
    """Allow a declared correct answer to disclose the solution."""
    return kind == "guess_correct" or reply.startswith("正解")
