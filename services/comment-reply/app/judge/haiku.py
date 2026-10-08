"""Haiku single-pass judge using Luna's prompt, schema and postprocessing."""

from __future__ import annotations

from app.anthropic_util import AnthropicError, AnthropicRefusalError, MODEL, request_json
from app.judge import luna
from app.judge.contract import Judgement, Problem


def judge(comment_id: str, text: str, problem: Problem, *, api_key: str) -> Judgement:
    """Ask Haiku once, preserving error telemetry for Luna fallback and probes."""
    data, debug = request_json(
        luna.build_prompt(problem), text, luna._schema(), api_key=api_key,
        effort="max", max_tokens=16000,
    )
    try:
        return luna.parse_judgement(data, text, method="haiku", debug=debug)
    except (KeyError, TypeError, ValueError) as exc:
        debug["error_reason"] = "invalid_judgement"
        raise AnthropicError(str(exc), debug=debug) from exc
