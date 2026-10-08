"""Reply variants using the final judge decision as immutable input."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib import request

from app import anthropic_util
from app.http_util import post_json_with_retry
from app.judge.combiner import Combined
from app.judge.contract import Problem
from app.reply import leak_guard, templates


LOGGER = logging.getLogger(__name__)
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
SLOTS = ("判定語だけ", "判定語 + 復唱", "判定語 + 一言", "判定語 + 一言")
HAIKU_VARIANTS = frozenset({"1b-haiku", "1d-haiku"})
TRUTH_VARIANTS = frozenset({"1b", "1b-haiku"})


@dataclass(frozen=True)
class Reply:
    """Generated response and compact writer diagnostics."""

    text: str | None
    source: str
    over_80: bool
    error: str | None = None
    debug: dict[str, Any] = field(default_factory=dict)
    guard: dict[str, Any] | None = None


def pick_slot(comment_id: str) -> str:
    """Select the trial's four-way reply slot by comment ID."""
    digest = hashlib.sha1(f"slot:{comment_id}".encode("utf-8")).digest()
    return SLOTS[int.from_bytes(digest[:8], "big") % len(SLOTS)]


def _render_prompt(
    template: str, result: Combined, problem: Problem, with_truth: bool,
    *, style: str, slot: str,
) -> str:
    values = {
        "problem_text": problem.problem_text,
        "truth": problem.truth if with_truth else "",
        "fact_sheet": "\n".join(f"- {fact}" for fact in problem.fact_sheet) if with_truth else "",
        "core_points": "\n".join(f"- {point}" for point in problem.core_points) if with_truth else "",
        "reveal_text": problem.reveal_text if with_truth else "",
        "kind": result.kind,
        "answer": result.answer or "",
        "bare_term": result.bare_term or "",
        "style": style,
        "slot": slot,
    }
    pattern = r"\{(problem_text|truth|fact_sheet|core_points|reveal_text|kind|answer|bare_term|style|slot)\}"
    return re.sub(pattern, lambda match: values[match.group(1)], template)


def _clean_text_reply(reply: str) -> str:
    """Strip incidental think blocks, wrappers and reply labels."""
    if "</think>" in reply:
        reply = reply.split("</think>", 1)[1]
    reply = reply.strip()
    quote_pairs = (("「", "」"), ("『", "』"), ('"', '"'), ("“", "”"))
    for opening, closing in quote_pairs:
        if reply.startswith(opening) and reply.endswith(closing) and len(reply) >= 2:
            reply = reply[len(opening):-len(closing)].strip()
            break
    reply = re.sub(r"^(?:返信|reply)\s*[:：]\s*", "", reply, flags=re.IGNORECASE).strip()
    for opening, closing in quote_pairs:
        if reply.startswith(opening) and reply.endswith(closing) and len(reply) >= 2:
            reply = reply[len(opening):-len(closing)].strip()
            break
    return reply


def _template_reply(result: Combined, comment_id: str, problem: Problem) -> str | None:
    if result.kind == "q_yesno":
        return templates.yesno_reply(result.answer or "irrelevant", comment_id)
    if result.kind == "guess_correct":
        return templates.correct_reply(problem.reveal_text)
    if result.kind == "q_open" and result.bare_term:
        return templates.bare_term_reply(result.bare_term, comment_id)
    return templates.pick(result.kind, comment_id)


def build_prompt(
    result: Combined, comment_id: str, problem: Problem, *, variant: str,
) -> tuple[str, str]:
    """Share the exact prompt and slot between the Luna and Haiku variants."""
    with_truth = variant in TRUTH_VARIANTS
    prompt_name = "reply_1b_with_truth.txt" if with_truth else "reply_writer.txt"
    template = (PROMPTS_DIR / prompt_name).read_text(encoding="utf-8")
    style = (PROMPTS_DIR / "reply_style.txt").read_text(encoding="utf-8")
    slot = pick_slot(comment_id) if result.kind == "q_yesno" else "（この種別では使わない）"
    system = _render_prompt(template, result, problem, with_truth, style=style, slot=slot)
    return system, slot


def reply_schema() -> dict[str, Any]:
    """Return the shared single-field structured reply contract."""
    return {
        "type": "object", "properties": {"reply": {"type": "string"}},
        "required": ["reply"], "additionalProperties": False,
    }


def _llm_reply(
    result: Combined, comment_id: str, text: str, problem: Problem,
    *, variant: str, api_key: str, model: str,
) -> tuple[str, dict[str, Any]]:
    system, slot = build_prompt(result, comment_id, problem, variant=variant)
    with_truth = variant in TRUTH_VARIANTS
    if variant in HAIKU_VARIANTS:
        data, debug = anthropic_util.request_json(
            system, text, reply_schema(), api_key=api_key,
            effort="max" if with_truth else "low", max_tokens=16000 if with_truth else 4000,
        )
        debug["slot"] = slot
        reply = data.get("reply")
        if not isinstance(reply, str):
            debug["error_reason"] = "invalid_reply"
            raise anthropic_util.AnthropicError("writer JSON reply is not a string", debug=debug)
        return _clean_text_reply(reply), debug
    if not api_key:
        raise ValueError("openai_api_key is empty")
    payload = {
        "model": model,
        "reasoning_effort": "xhigh" if with_truth else "low",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": text}],
        "max_completion_tokens": 2400 if with_truth else 800,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "reply_only", "strict": True,
                "schema": reply_schema(),
            },
        },
    }
    req = request.Request(
        OPENAI_CHAT_COMPLETIONS_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.monotonic()
    body = post_json_with_retry(req, retries=5, initial_backoff_s=2)
    choice = body["choices"][0]
    usage = body.get("usage", {}) or {}
    details = usage.get("completion_tokens_details", {}) or {}
    debug = {
        "model": model, "slot": slot, "prompt_tokens": usage.get("prompt_tokens", 0) or 0,
        "completion_tokens": usage.get("completion_tokens", 0) or 0,
        "reasoning_tokens": details.get("reasoning_tokens", 0) or 0,
        "cached_tokens": (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0) or 0,
        "finish_reason": choice.get("finish_reason"),
        "latency_s": round(time.monotonic() - started, 6),
    }
    try:
        if choice.get("finish_reason") == "length":
            debug["error_reason"] = "max_tokens"
            raise ValueError("writer exceeded max_completion_tokens")
        content = choice["message"]["content"]
        if not content:
            debug["error_reason"] = "missing_text" if content is None else "empty_text"
        data = json.loads(content)
        reply = data.get("reply") if isinstance(data, dict) else None
        if not isinstance(reply, str):
            raise ValueError("writer JSON reply is not a string")
        return _clean_text_reply(reply), debug
    except Exception as exc:
        exc.debug = debug
        raise


def write_reply(
    result: Combined, comment_id: str, text: str, problem: Problem, *,
    variant: str, openai_api_key: str = "", model: str = "gpt-6-luna",
    anthropic_api_key: str = "",
) -> Reply:
    """Write one reply, preserving the final kind and answer."""
    kind = result.kind
    if kind in templates.NO_REPLY_KINDS:
        return Reply(None, "no_reply", False)
    if result.decision == "consensus_split":
        value, source = templates.split_reply(comment_id), "consensus_split"
        error, debug = None, {}
    elif kind in {"troll", "abuse"}:
        value, source = templates.pick(kind, comment_id), "template"
        error, debug = None, {}
    elif variant == "2b" or (kind == "guess_correct" and variant not in TRUTH_VARIANTS):
        value, source = _template_reply(result, comment_id, problem), "template"
        error, debug = None, {}
    else:
        debug = {}
        try:
            value, debug = _llm_reply(
                result, comment_id, text, problem, variant=variant,
                api_key=anthropic_api_key if variant in HAIKU_VARIANTS else openai_api_key,
                model=model,
            )
            if not value:
                debug["error_reason"] = "empty_reply"
                raise ValueError("writer reply is empty")
            if kind == "q_yesno" and not value.startswith(templates.YESNO_OPENERS[result.answer or "irrelevant"]):
                raise ValueError("writer reply does not begin with the required answer word")
            if kind == "q_open" and result.bare_term:
                asks_about_term = (
                    result.bare_term in value
                    and any(phrase in value for phrase in ("何が", "何のこと", "どうした"))
                    and any(phrase in value for phrase in ("教えて", "聞かせて", "？", "?"))
                )
                if not asks_about_term:
                    raise ValueError("writer did not ask what bare_term means")
            source, error = "llm", None
        except Exception as exc:
            error = str(exc)
            debug = getattr(exc, "debug", debug)
            LOGGER.warning("REPLY_WRITER_FALLBACK comment_id=%s error=%s", comment_id, error)
            value, source = _template_reply(result, comment_id, problem), "fallback_template"
    guard = None
    reveal_kind = None if result.decision == "consensus_split" else kind
    if value is not None and not leak_guard.is_correct_reveal(reveal_kind, value):
        entry = leak_guard.entry_for_content_key(problem.content_key)
        if entry is None:
            LOGGER.warning("REPLY_LEAK_GUARD_NO_DICT content_key=%s", problem.content_key)
        else:
            words = leak_guard.find_leaks(value, text, entry)
            if words:
                guard = {"words": words, "original_text": value, "original_source": source}
                value = (templates.YESNO_OPENERS[result.answer or "irrelevant"]
                         if kind == "q_yesno" else templates.LEAK_GUARD_TEXT)
                source = "leak_guard"
                LOGGER.warning("REPLY_LEAK_GUARD comment_id=%s words=%s", comment_id, words)
    over_80 = bool(value and len(value) > 80)
    if over_80:
        LOGGER.warning("REPLY_OVER_80 comment_id=%s length=%s", comment_id, len(value))
    return Reply(value, source, over_80, error, debug, guard)
