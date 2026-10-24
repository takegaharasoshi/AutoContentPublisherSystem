"""Validated settings for the scheduled coach reply service."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


JUDGE_EFFORTS = frozenset({"low", "medium", "high", "xhigh", "max"})


@dataclass(frozen=True)
class Config:
    """Runtime settings; resource names may be omitted for offline evaluation."""

    secret_arn: str = ""
    assets_bucket: str = ""
    problems_prefix: str = "assets/logic-training-1/problems/"
    state_prefix: str = "coach-reply/logic-training-1/state/"
    param_prefix: str = "/acps/prod/coach-reply/"
    graph_api_base: str = "https://graph.instagram.com/v25.0"
    judge_model: str = "claude-haiku-5-5"
    judge_effort: str = "high"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Config:
        """Read environment settings and reject malformed prefixes or effort."""
        source = os.environ if env is None else env
        config = cls(**{
            name: source.get(name.upper(), field.default)
            for name, field in cls.__dataclass_fields__.items()
        })
        for name in ("problems_prefix", "state_prefix"):
            prefix = getattr(config, name)
            if not prefix or prefix.startswith("/") or not prefix.endswith("/"):
                raise ValueError(f"{name.upper()} must be a relative S3 prefix ending in /")
        if not config.param_prefix.startswith("/") or not config.param_prefix.endswith("/"):
            raise ValueError("PARAM_PREFIX must start and end with /")
        if config.judge_effort not in JUDGE_EFFORTS:
            raise ValueError("invalid JUDGE_EFFORT")
        if not config.judge_model.strip() or not config.graph_api_base.strip():
            raise ValueError("JUDGE_MODEL and GRAPH_API_BASE must not be blank")
        return config

    def require(self, *names: str) -> None:
        """Reject missing resource settings needed by a Lambda handler."""
        missing = [name for name in names if not getattr(self, name).strip()]
        if missing:
            raise ValueError(f"missing configuration: {', '.join(missing)}")
