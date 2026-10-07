"""OpenAI Decisions transport for the shared Jev staged classifier."""

from __future__ import annotations

import json
import math
import time
from functools import partial
from typing import Any
from urllib import error, request

from app.http_util import post_json_with_retry
from app.judge import jev
from app.judge.contract import Judgement, Problem


DECISIONS_URL = "https://api.openai.com/v1/decisions"
MODEL = "gpt-6-luna"
MAX_RETRIES = 3
# Keep independent settings: the two models' probabilities may need different tuning.
T_POINT = 0.5
T_CLOSE = 0.25
T_GUESS = 0.95
T_RECHECK = 0.6
T_QUALITY = 0.2
T_ANSWER = 0.55
T_BARE_TERM = 0.5
T_CONTRADICT = 0.5


class DecisionsError(RuntimeError):
    """A failed decision, retaining telemetry for fallback logs and probes."""

    def __init__(self, message: str, *, debug: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.debug = debug if debug is not None else {}


def _questions(questions: dict[str, dict]) -> list[dict[str, Any]]:
    """Translate Jev questions mechanically, preserving their order and wording."""
    converted = []
    for name, question in questions.items():
        kind = question["type"]
        if kind not in {"noul", "choice"}:
            raise DecisionsError(f"unsupported question type: {kind}")
        instructions = question["instructions"]
        if kind == "noul" and question.get("criteria"):
            # predicate には criteria の欄がないため、Jev に渡している true / false の基準を
            # 指示文の末尾に付ける（21-6d10b の小試走で、基準なしでは段 B2 が正解の推理にも
            # 矛盾ありを 0.92〜1.0 で返した）。
            criteria = question["criteria"]
            instructions += (f"\nTrue: {criteria['true']}\nFalse: {criteria['false']}")
        item = {"type": "predicate" if kind == "noul" else "choice",
                "name": name, "instructions": instructions}
        if kind == "choice":
            item["choices"] = [{"value": key, "description": description}
                               for key, description in question["criteria"].items()]
        converted.append(item)
    return converted


def _probability(value: Any) -> float:
    """Reject missing, nonnumeric and out-of-range probabilities."""
    if (
        not isinstance(value, (int, float)) or isinstance(value, bool)
        or not math.isfinite(value) or not 0 <= value <= 1
    ):
        raise ValueError(f"invalid probability: {value!r}")
    return float(value)


def _convert_response(result: Any, questions: dict[str, dict]) -> dict:
    """Validate ordered answers and expose the shape consumed by Jev parsers."""
    debug: dict[str, Any] = {
        "input_tokens": 0, "output_tokens": 0, "confidence": {},
        "refusals": {"count": 0, "names": []},
    }
    try:
        if not isinstance(result, dict) or not isinstance(result.get("model"), str):
            raise ValueError("response requires a model string")
        usage = result["usage"]
        if not isinstance(usage, dict):
            raise ValueError("response requires a usage object")
        for key in ("input_tokens", "output_tokens"):
            value = usage[key]
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"invalid usage.{key}")
            debug[key] = value
        answers = result["answers"]
        if not isinstance(answers, list) or len(answers) != len(questions):
            raise ValueError("answers must contain one answer per question")
        for (name, question), answer in zip(questions.items(), answers):
            if not isinstance(answer, dict) or answer.get("name") != name:
                raise ValueError(f"missing or out-of-order answer: {name}")
            expected_type = "predicate" if question["type"] == "noul" else "choice"
            if answer.get("type") == "refusal":
                debug["refusals"]["names"].append(name)
                debug["refusals"]["count"] += 1
            elif answer.get("type") != expected_type:
                raise ValueError(f"invalid answer type for {name}")
        converted = {}
        for (name, question), answer in zip(questions.items(), answers):
            if answer["type"] == "refusal":
                continue
            if answer["type"] == "predicate":
                converted[name] = {"noul": {"true": _probability(answer["probability"])}}
                continue
            criteria = question["criteria"]
            choice = answer["choice"]
            if not isinstance(choice, str) or choice not in criteria:
                raise ValueError(f"invalid choice for {name}: {choice!r}")
            confidence = _probability(answer["confidence"])
            debug["confidence"][name] = confidence
            entries = answer["probabilities"]
            if not isinstance(entries, list) or len(entries) != len(criteria):
                raise ValueError(f"missing choice probabilities for {name}")
            probabilities = {}
            for entry in entries:
                if not isinstance(entry, dict):
                    raise ValueError(f"invalid probability entry for {name}")
                value = entry["value"]
                if not isinstance(value, str) or value not in criteria or value in probabilities:
                    raise ValueError(f"invalid or duplicate choice value for {name}")
                probabilities[value] = _probability(entry["probability"])
            if not math.isclose(sum(probabilities.values()), 1.0, abs_tol=0.01):
                raise ValueError(f"choice probabilities do not sum to approximately 1 for {name}")
            converted[name] = {"choice": choice, "confidence": confidence,
                               "probabilities": probabilities}
    except (KeyError, TypeError, ValueError) as exc:
        raise DecisionsError(f"Decisions API 応答の形が不正です: {exc}", debug=debug) from exc
    if debug["refusals"]["count"]:
        names = ", ".join(debug["refusals"]["names"])
        raise DecisionsError(f"必要な問いが refusal を返しました: {names}", debug=debug)
    return {**result, "answers": converted,
            "confidence": debug["confidence"], "refusals": debug["refusals"]}


def _decisions_request(
    api_key: str, state: dict, questions: dict[str, dict], *, model: str = MODEL,
) -> dict:
    """POST to Decisions, retrying 429 and all 5xx errors three times."""
    payload = {"model": model, "input": json.dumps(state, ensure_ascii=False),
               "questions": _questions(questions)}
    req = request.Request(
        DECISIONS_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        result = post_json_with_retry(req, retries=MAX_RETRIES, initial_backoff_s=1)
    except error.HTTPError as exc:
        raise DecisionsError(f"HTTP {exc.code}") from exc
    except (error.URLError, ValueError, UnicodeError) as exc:
        raise DecisionsError(f"Decisions API 応答を読めません: {exc}") from exc
    return _convert_response(result, questions)


def _record_call(
    api_key: str, state: dict, questions: dict[str, dict], debug: dict, stage: str,
    *, model: str = MODEL,
) -> dict:
    """Record usage, confidence and refusals even when a stage fails."""
    started = time.monotonic()
    telemetry: dict = {}
    try:
        result = _decisions_request(api_key, state, questions, model=model)
        telemetry = {**result, **result["usage"]}
        return result["answers"]
    except DecisionsError as exc:
        telemetry = exc.debug
        raise
    finally:
        debug["calls"] += 1
        debug["latency_s"] = round(debug["latency_s"] + time.monotonic() - started, 6)
        debug["input_tokens"] += telemetry.get("input_tokens", 0)
        debug["output_tokens"] += telemetry.get("output_tokens", 0)
        debug["confidence"][stage] = telemetry.get("confidence", {})
        refusals = telemetry.get("refusals", {"count": 0, "names": []})
        debug["refusals"]["count"] += refusals["count"]
        debug["refusals"]["names"].extend(refusals["names"])


def judge(
    comment_id: str, text: str, problem: Problem, *, api_key: str, model: str = MODEL,
    t_point: float = T_POINT, t_close: float = T_CLOSE,
    t_recheck: float = T_RECHECK, t_guess: float = T_GUESS,
    t_quality: float = T_QUALITY, t_answer: float = T_ANSWER,
    t_bare_term: float = T_BARE_TERM, t_contradict: float = T_CONTRADICT,
) -> Judgement:
    """Run the unchanged Jev stages with Decisions and independent thresholds."""
    return jev._judge_staged(
        comment_id, text, problem, api_key=api_key,
        transport=partial(_record_call, model=model), method="decisions", model=model,
        make_error=lambda exc, debug: DecisionsError(
            f"Decisions judgement failed: {exc}", debug=debug,
        ),
        t_point=t_point, t_close=t_close, t_recheck=t_recheck, t_guess=t_guess,
        t_quality=t_quality, t_answer=t_answer, t_bare_term=t_bare_term,
        t_contradict=t_contradict,
        debug_fields={"confidence": {}, "refusals": {"count": 0, "names": []}},
    )
