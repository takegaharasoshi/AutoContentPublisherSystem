"""Trial-8b single-pass gpt-6-luna classifier and draft reply."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from urllib import request

from app.http_util import post_json_with_retry
from app.judge.contract import ANSWERS, KINDS, Judgement, Problem, bare_term_text


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
RULES_PATH = Path(__file__).resolve().parent.parent / "prompts" / "pattern1_rules.txt"


def format_judge_criteria(problem: Problem) -> str:
    """Format each core point with its hit and touch boundary for Luna."""
    lines = []
    for index, (point, (hit, touch)) in enumerate(
        zip(problem.core_points, problem.judge_criteria.points), start=1
    ):
        lines.extend((
            f"- 要点 {index}: {point}",
            f"  当てた: {hit}",
            f"  触れた: {touch}",
        ))
    errors = "／".join(problem.judge_criteria.errors) or "なし"
    lines.append(f"- 正解にしない誤りの例: {errors}")
    return "\n".join(lines)


def _schema() -> dict[str, Any]:
    """Return the strict OpenAI structured output contract."""
    return {
        "type": "object",
        "properties": {
            "kind": {"type": "string", "enum": list(KINDS)},
            "answer": {"anyOf": [
                {"type": "string", "enum": ["yes", "no", "irrelevant"]},
                {"type": "null"},
            ]},
            "reply": {"type": "string"},
            "reason": {"type": "string"},
            "bare_term": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        },
        "required": ["kind", "answer", "reply", "reason", "bare_term"],
        "additionalProperties": False,
    }


def build_prompt(problem: Problem) -> str:
    """Render the unchanged single-pass system prompt for either provider."""
    return RULES_PATH.read_text(encoding="utf-8").format(
        problem_text=problem.problem_text,
        truth=problem.truth,
        fact_sheet="\n".join(f"- {fact}" for fact in problem.fact_sheet),
        core_points="\n".join(f"- {point}" for point in problem.core_points),
        judge_criteria=format_judge_criteria(problem),
    )


def parse_judgement(
    data: Any, text: str, *, method: str, debug: dict[str, Any],
) -> Judgement:
    """Validate and normalize both single-pass judges with the Luna rules."""
    label = "Luna" if method == "luna" else "Haiku"
    if not isinstance(data, dict):
        raise ValueError(f"{label} response is not an object")
    kind = data["kind"]
    answer = data["answer"]
    draft = data["reply"]
    reason = data["reason"]
    bare_term = data["bare_term"]
    if kind not in KINDS or not isinstance(draft, str) or not isinstance(reason, str):
        raise ValueError(f"{label} response has invalid kind, reply or reason")
    if bare_term is not None and not isinstance(bare_term, str):
        raise ValueError(f"{label} response has invalid bare_term")
    if bare_term:
        bare_term = bare_term_text(text)
        kind = "q_open"
        answer = None
    if kind == "q_yesno" and answer not in ANSWERS:
        raise ValueError(f"{label} q_yesno answer is invalid")
    if kind != "q_yesno" and answer is not None:
        raise ValueError(f"{label} non-q_yesno answer must be null")
    return Judgement(
        method, kind, answer=answer, reason=reason, bare_term=bare_term or None,
        reply_draft=draft, debug=debug,
    )


def judge(
    comment_id: str, text: str, problem: Problem, *, api_key: str,
    model: str = "gpt-6-luna",
) -> Judgement:
    """Ask Luna once for kind, answer, rationale, term and a draft."""
    if not api_key:
        raise ValueError("openai_api_key is empty")
    started = time.monotonic()
    system = build_prompt(problem)
    payload = {
        "model": model,
        "reasoning_effort": "xhigh",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        "max_completion_tokens": 2400,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "comment_judgement", "strict": True, "schema": _schema()},
        },
    }
    req = request.Request(
        OPENAI_CHAT_COMPLETIONS_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    body = post_json_with_retry(req, retries=3, initial_backoff_s=5)
    choice = body["choices"][0]
    usage = body.get("usage", {}) or {}
    debug = {
        "model": model, "finish_reason": choice.get("finish_reason"),
        "prompt_tokens": usage.get("prompt_tokens", 0) or 0,
        "completion_tokens": usage.get("completion_tokens", 0) or 0,
        "reasoning_tokens": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0,
        "cached_tokens": (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0) or 0,
        "latency_s": round(time.monotonic() - started, 6),
    }
    try:
        if choice.get("finish_reason") == "length":
            debug["error_reason"] = "max_tokens"
            raise ValueError("Luna response exceeded max_completion_tokens")
        content = choice["message"]["content"]
        if not content:
            debug["error_reason"] = "missing_text" if content is None else "empty_text"
        return parse_judgement(json.loads(content), text, method="luna", debug=debug)
    except Exception as exc:
        # Preserve exception types and behavior while letting probes retain failed-call usage.
        exc.debug = debug
        raise
