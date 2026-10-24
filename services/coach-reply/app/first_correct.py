"""Conservative, pure first-correct selection."""

from __future__ import annotations

from app.switch import parse_utc_timestamp


def is_first_correct(
    comment: dict, top_level: list[dict], judged: dict[str, dict], *,
    first_correct_replied: bool, has_operator_reply: bool,
) -> bool:
    """Allow first place only when every strictly earlier answer is wrong."""
    record = judged.get(comment["id"], {})
    if (first_correct_replied or has_operator_reply
            or record.get("verdict") != "correct" or record.get("confidence") != "high"):
        return False
    if any(item.get("verdict") == "operator_replied" for item in judged.values()):
        return False
    timestamp = parse_utc_timestamp(comment["timestamp"])
    for earlier in top_level:
        if earlier["id"] == comment["id"]:
            continue
        # An unavailable timestamp cannot prove that no earlier answer exists.
        if not earlier.get("timestamp"):
            return False
        if parse_utc_timestamp(earlier["timestamp"]) < timestamp:
            if judged.get(earlier["id"], {}).get("verdict") != "wrong":
                return False
    return True
