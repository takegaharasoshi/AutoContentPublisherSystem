"""Batch quiz-comment judgments using Anthropic Messages structured output."""

from __future__ import annotations

import json
import logging
from collections import Counter
from pathlib import Path

from app import anthropic_util, secrets
from app.config import Config


LOGGER = logging.getLogger(__name__)
MAX_BATCH_SIZE = 20
VERDICTS = frozenset({"correct", "alt", "wrong", "unsure"})
CONFIDENCES = frozenset({"high", "low"})
PROMPT = Path(__file__).with_name("prompts").joinpath("judge.md").read_text(encoding="utf-8")
SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["results"],
    "properties": {"results": {
        "type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "verdict", "confidence", "reason"],
            "properties": {
                "id": {"type": "string"},
                "verdict": {"type": "string", "enum": sorted(VERDICTS)},
                "confidence": {"type": "string", "enum": sorted(CONFIDENCES)},
                "reason": {"type": "string"},
            },
        },
    }},
}


def _validated_results(raw: dict, ids: set[str]) -> dict[str, dict]:
    """Omit malformed, missing, duplicated and foreign IDs, keeping valid peers."""
    if not isinstance(raw, dict) or set(raw) != {"results"} or not isinstance(raw["results"], list):
        return {}
    rows = raw["results"]
    counts = Counter(row["id"] for row in rows
                     if isinstance(row, dict) and isinstance(row.get("id"), str))
    results = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"id", "verdict", "confidence", "reason"}:
            continue
        cid = row["id"]
        if (not isinstance(cid, str) or cid not in ids or counts[cid] != 1
                or not isinstance(row["verdict"], str) or row["verdict"] not in VERDICTS
                or not isinstance(row["confidence"], str) or row["confidence"] not in CONFIDENCES
                or not isinstance(row["reason"], str) or not row["reason"].strip()):
            continue
        results[cid] = {key: row[key] for key in ("verdict", "confidence", "reason")}
    return results


def judge_comments(
    snapshot: dict, comments: list[dict], *, config: Config | None = None,
    api_key: str | None = None, timeout: float = anthropic_util.TIMEOUT_S,
) -> dict[str, dict]:
    """Judge at most twenty comments per request, omitting failed judgments.

    Args:
        snapshot: Quiz question, canonical answer, explanation and optional hint.
        comments: Comment IDs and text. Any other fields are discarded.
        config: Optional runtime settings for tests and the scheduled handler.
        api_key: Explicit key (Lambda Secret or offline environment variable).
        timeout: Optional per-request socket timeout from the runner.

    Returns:
        Only validated id -> verdict/confidence/reason records. Missing IDs are
        failures for the runner to retry on its next scheduled invocation.
    """
    if not comments:
        return {}
    config = config or Config.from_env()
    if api_key is None:
        credentials = secrets.get_secrets(config.secret_arn)
        secrets.require_keys(credentials, "anthropic_api_key")
        api_key = credentials["anthropic_api_key"]
    problem = {key: snapshot.get(key) for key in
               ("question_text", "answer_text", "explanation", "hint")}
    results = {}
    for offset in range(0, len(comments), MAX_BATCH_SIZE):
        batch = [{"id": c["id"], "text": c["text"]}
                 for c in comments[offset:offset + MAX_BATCH_SIZE]]
        try:
            raw, _debug = anthropic_util.request_json(
                PROMPT, json.dumps({"snapshot": problem, "comments": batch}, ensure_ascii=False),
                SCHEMA, api_key=api_key, model=config.judge_model,
                effort=config.judge_effort, max_tokens=16000, timeout=timeout,
            )
            results.update(_validated_results(raw, {c["id"] for c in batch}))
        except Exception as exc:
            # API errors can include sensitive request information: log only type.
            LOGGER.warning("judge batch failed: comments=%d error=%s", len(batch), type(exc).__name__)
    return results
