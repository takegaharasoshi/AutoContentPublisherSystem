"""Haiku single-pass judge with its own prompt and Luna's postprocessing."""

from __future__ import annotations

import re
from pathlib import Path

from app.anthropic_util import AnthropicError, AnthropicRefusalError, MODEL, request_json
from app.judge import luna
from app.judge.contract import Judgement, Problem


RULES_PATH = Path(__file__).resolve().parent.parent / "prompts" / "haiku_judge.txt"


def build_prompt(problem: Problem) -> str:
    """Fill only the named placeholders, preserving other literal braces."""
    values = {
        "problem_text": problem.problem_text,
        "truth": problem.truth,
        "fact_sheet": "\n".join(f"- {fact}" for fact in problem.fact_sheet),
        "core_points": "\n".join(f"- {point}" for point in problem.core_points),
        "judge_criteria": luna.format_judge_criteria(problem),
    }
    pattern = r"\{(problem_text|truth|fact_sheet|core_points|judge_criteria)\}"
    return re.sub(pattern, lambda match: values[match.group(1)],
                  RULES_PATH.read_text(encoding="utf-8"))


def judge(
    comment_id: str, text: str, problem: Problem, *, api_key: str, effort: str = "max",
) -> Judgement:
    """Ask Haiku once, preserving error telemetry for Luna fallback and probes."""
    data, debug = request_json(
        build_prompt(problem), "<comment>\n" + text + "\n</comment>", luna._schema(),
        api_key=api_key, effort=effort, max_tokens=32000,
    )
    try:
        return luna.parse_judgement(data, text, method="haiku", debug=debug)
    except (KeyError, TypeError, ValueError) as exc:
        debug["error_reason"] = "invalid_judgement"
        raise AnthropicError(str(exc), debug=debug) from exc
