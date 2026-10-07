"""Validated runtime settings for the two Lambda handlers and local trial."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


JUDGE_MODES = frozenset({"luna", "jev", "hybrid", "decisions"})
REPLY_VARIANTS = frozenset({"1b", "1d-luna", "2b", "2c-luna"})


def _flag(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "on", "yes"}:
        return True
    if normalized in {"0", "false", "off", "no"}:
        return False
    raise ValueError(f"{name} must be on/off: {value!r}")


@dataclass(frozen=True)
class Config:
    """Runtime configuration, with AWS resource names optional for local use."""

    judge_mode: str = "hybrid"
    shadow: bool = True
    consensus: bool = True
    reply_variant: str = "1d-luna"
    luna_model: str = "gpt-6-luna"
    secret_arn: str = ""
    queue_url: str = ""
    assets_bucket: str = ""
    problems_prefix: str = "assets/umigame-soup-1/problems/"
    comment_log_bucket: str = ""
    set_code: str = "umigame-soup-1"
    graph_api_base: str = "https://graph.instagram.com/v23.0"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Config:
        """Read and validate supported environment variables."""
        source = os.environ if env is None else env
        mode = source.get("JUDGE_MODE", "hybrid")
        variant = source.get("REPLY_VARIANT", "1d-luna")
        if mode not in JUDGE_MODES:
            raise ValueError(f"invalid JUDGE_MODE: {mode}")
        if variant not in REPLY_VARIANTS:
            raise ValueError(f"invalid REPLY_VARIANT: {variant}")
        prefix = source.get("PROBLEMS_PREFIX", "assets/umigame-soup-1/problems/")
        if not prefix or not prefix.endswith("/") or prefix.startswith("/"):
            raise ValueError("PROBLEMS_PREFIX must be a relative S3 prefix ending in /")
        bucket = source.get("ASSETS_BUCKET", "")
        return cls(
            judge_mode=mode,
            shadow=_flag(source.get("JUDGE_SHADOW", "on"), "JUDGE_SHADOW"),
            consensus=_flag(source.get("JUDGE_CONSENSUS", "on"), "JUDGE_CONSENSUS"),
            reply_variant=variant,
            luna_model=source.get("LUNA_MODEL", "gpt-6-luna"),
            secret_arn=source.get("SECRET_ARN", ""),
            queue_url=source.get("QUEUE_URL", ""),
            assets_bucket=bucket,
            problems_prefix=prefix,
            comment_log_bucket=source.get("COMMENT_LOG_BUCKET", bucket),
            set_code=source.get("SET_CODE", "umigame-soup-1"),
            graph_api_base=source.get("GRAPH_API_BASE", "https://graph.instagram.com/v23.0"),
        )

    def require(self, *names: str) -> None:
        """Reject missing settings needed by a particular handler."""
        missing = [name for name in names if not getattr(self, name)]
        if missing:
            raise ValueError(f"missing configuration: {', '.join(missing)}")
