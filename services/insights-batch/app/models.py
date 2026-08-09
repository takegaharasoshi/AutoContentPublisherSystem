"""Data models used by the insights collection batch."""

from __future__ import annotations

from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class BatchSet:
    """A batch set selected for insights collection."""

    id: int
    set_code: str
    is_active: bool


@dataclass(frozen=True)
class SnsAccount:
    """An active Instagram account configured for a batch set."""

    id: int
    platform: str
    account_code: str
    account_name: str


@dataclass(frozen=True)
class Post:
    """A successfully published media item eligible for collection."""

    id: int
    media_type: str
    platform_post_id: str
    posted_at: datetime.datetime
