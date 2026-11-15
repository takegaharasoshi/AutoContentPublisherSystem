"""The single reply gate shared by the scheduled handler and offline evaluation."""

from __future__ import annotations


# Phase 33-2 (2026-11-15): reply to every "correct" judgment, low confidence included.
# First place (first_correct.is_first_correct) still requires high confidence.
REPLY_CONFIDENCES = frozenset({"high", "low"})


def should_reply(result: dict | None) -> bool:
    """Return True when a validated judgment earns the fixed "correct" reply."""
    return bool(result and result.get("verdict") == "correct"
                and result.get("confidence") in REPLY_CONFIDENCES)
