"""Pure comment exclusions based on the complete top-level Graph listing."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.switch import parse_utc_timestamp


@dataclass
class Selection:
    """Separate candidates, recorded exclusions and chronology for first place."""

    candidates: list[dict] = field(default_factory=list)
    already_judged: list[dict] = field(default_factory=list)
    operator_replied: list[dict] = field(default_factory=list)
    before_start: list[dict] = field(default_factory=list)
    top_level: list[dict] = field(default_factory=list)
    has_operator_reply: bool = False


def reply_ids(comment: dict) -> set[str]:
    """Return IDs of the embedded replies (their usernames are unavailable)."""
    return {reply["id"] for reply in comment.get("replies", {}).get("data", [])}


def select_comments(
    comments: list[dict], own_username: str, judged: dict[str, dict],
    not_before: datetime,
) -> Selection:
    """Apply chapter 2 exclusions in order without changing input documents.

    A failure counter without a verdict is pending, rather than judged. Bodyless
    comments remain in top_level so they cannot establish an earlier wrong answer.
    """
    own_ids = {c["id"] for c in comments if c.get("username") == own_username}
    replies = set().union(*(reply_ids(c) for c in comments)) if comments else set()
    result = Selection(has_operator_reply=bool(own_ids & replies))
    seen: set[str] = set()
    for comment in comments:
        cid = comment["id"]
        if cid in seen or cid in replies or cid in own_ids:
            continue
        seen.add(cid)
        result.top_level.append(comment)
        text = comment.get("text")
        if not isinstance(text, str) or not text.strip():
            continue
        if judged.get(cid, {}).get("verdict"):
            result.already_judged.append(comment)
        elif reply_ids(comment) & own_ids:
            result.operator_replied.append(comment)
        elif parse_utc_timestamp(comment["timestamp"]) < not_before:
            result.before_start.append(comment)
        else:
            result.candidates.append(comment)
    return result
