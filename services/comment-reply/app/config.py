"""Validated runtime settings for the two Lambda handlers and local trial."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


JUDGE_MODES = frozenset({"luna", "jev", "haiku"})
REPLY_VARIANTS = frozenset({"1b", "1d-luna", "2b", "2c-luna", "1b-haiku", "1d-haiku"})
HAIKU_EFFORTS = frozenset({"low", "medium", "high", "xhigh", "max"})
LUNA_EFFORTS = HAIKU_EFFORTS


@dataclass(frozen=True)
class Config:
    """Runtime configuration, with AWS resource names optional for local use."""

    judge_mode: str = "haiku"
    reply_variant: str = "1b-haiku"
    luna_model: str = "gpt-6-luna"
    secret_arn: str = ""
    queue_url: str = ""
    assets_bucket: str = ""
    problems_prefix: str = "assets/umigame-soup-1/problems/"
    comment_log_bucket: str = ""
    set_code: str = "umigame-soup-1"
    graph_api_base: str = "https://graph.instagram.com/v23.0"
    haiku_effort: str = "high"
    luna_effort: str = "xhigh"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Config:
        """Read and validate supported environment variables."""
        source = os.environ if env is None else env
        mode = source.get("JUDGE_MODE", "haiku")
        variant = source.get("REPLY_VARIANT", "1b-haiku")
        haiku_effort = source.get("HAIKU_EFFORT", "high")
        luna_effort = source.get("LUNA_EFFORT", "xhigh")
        if mode not in JUDGE_MODES:
            raise ValueError(f"invalid JUDGE_MODE: {mode}")
        if variant not in REPLY_VARIANTS:
            raise ValueError(f"invalid REPLY_VARIANT: {variant}")
        if haiku_effort not in HAIKU_EFFORTS:
            raise ValueError(f"invalid HAIKU_EFFORT: {haiku_effort}")
        if luna_effort not in LUNA_EFFORTS:
            raise ValueError(f"invalid LUNA_EFFORT: {luna_effort}")
        prefix = source.get("PROBLEMS_PREFIX", "assets/umigame-soup-1/problems/")
        if not prefix or not prefix.endswith("/") or prefix.startswith("/"):
            raise ValueError("PROBLEMS_PREFIX must be a relative S3 prefix ending in /")
        bucket = source.get("ASSETS_BUCKET", "")
        return cls(
            judge_mode=mode,
            reply_variant=variant,
            luna_model=source.get("LUNA_MODEL", "gpt-6-luna"),
            secret_arn=source.get("SECRET_ARN", ""),
            queue_url=source.get("QUEUE_URL", ""),
            assets_bucket=bucket,
            problems_prefix=prefix,
            comment_log_bucket=source.get("COMMENT_LOG_BUCKET", bucket),
            set_code=source.get("SET_CODE", "umigame-soup-1"),
            graph_api_base=source.get("GRAPH_API_BASE", "https://graph.instagram.com/v23.0"),
            haiku_effort=haiku_effort,
            luna_effort=luna_effort,
        )

    def require(self, *names: str) -> None:
        """Reject missing settings needed by a particular handler."""
        missing = [name for name in names if not getattr(self, name)]
        if missing:
            raise ValueError(f"missing configuration: {', '.join(missing)}")
