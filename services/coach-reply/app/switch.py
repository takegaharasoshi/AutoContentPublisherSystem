"""Read both reply controls on every invocation, failing closed."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


UTC_TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]00:?00)"
)


def parse_utc_timestamp(value: str) -> datetime:
    """Parse a full ISO 8601 datetime with an explicit UTC offset."""
    if not isinstance(value, str) or not UTC_TIMESTAMP.fullmatch(value):
        raise ValueError("timestamp must be an ISO 8601 UTC datetime")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() != timedelta(0):
        raise ValueError("timestamp must use UTC")
    return parsed


@dataclass(frozen=True)
class ReplySwitch:
    """One invocation's immutable reply controls."""

    enabled: bool
    not_before: datetime

    @property
    def value(self) -> str:
        """Return the value persisted alongside each judgment."""
        return "on" if self.enabled else "off"


def read_switch(prefix: str, *, client: Any = None) -> ReplySwitch:
    """Read only GetParameter, as allowed by the service execution role."""
    if client is None:
        import boto3

        client = boto3.client("ssm")
    enabled = client.get_parameter(Name=f"{prefix}reply-enabled")["Parameter"]["Value"]
    start = client.get_parameter(Name=f"{prefix}reply-not-before")["Parameter"]["Value"]
    if enabled not in {"on", "off"}:
        raise ValueError("reply-enabled must be on or off")
    return ReplySwitch(enabled == "on", parse_utc_timestamp(start))
