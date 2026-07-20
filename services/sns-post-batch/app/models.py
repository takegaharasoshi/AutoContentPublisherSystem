"""Data models used by the SNS posting batch."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BatchSet:
    """A batch set selected for SNS posting."""

    id: int
    set_code: str
    is_active: bool


@dataclass(frozen=True)
class SnsAccount:
    """An active SNS account configured for a batch set."""

    id: int
    platform: str
    account_code: str
    account_name: str


@dataclass(frozen=True)
class CaptionTemplate:
    """An active caption template."""

    id: int
    template_text: str


@dataclass(frozen=True)
class GeneratedImageRef:
    """Storage reference for a generated image."""

    id: int
    s3_bucket: str
    s3_key: str


@dataclass(frozen=True)
class Post:
    """Current posting state for one generation run and SNS account."""

    id: int
    status: str
    platform_container_id: str | None
    platform_post_id: str | None
