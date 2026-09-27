"""gpt-6-luna に一括判定させるパターン 1。"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from urllib import error, request

from judge_contract import JudgeResult, KINDS, Problem
import templates


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_SECRET_ID = "umigame-poc/credentials"
RULES_PATH = Path(__file__).resolve().parent / "prompts" / "pattern1_rules.txt"


def load_api_key(secret_id: str = DEFAULT_SECRET_ID) -> str:
    """環境変数を優先し、なければ Secrets Manager から API キーを読む。"""
    key = os.environ.get("OPENAI_API_KEY", "")
    if key:
        return key
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("OPENAI_API_KEY がなく、boto3 も利用できません") from exc
    secret = json.loads(boto3.client("secretsmanager").get_secret_value(SecretId=secret_id)["SecretString"])
    key = secret.get("openai_api_key", "")
    if not key:
        raise RuntimeError(f"{secret_id} の openai_api_key が空です")
    return key


def _error_result(message: str, debug: dict) -> JudgeResult:
    return JudgeResult(kind="error", answer=None, reply=None, method="p1", debug={**debug, "error": message})


def judge(
    comment_id: str,
    text: str,
    problem: Problem,
    *,
    api_key: str,
    model: str = "gpt-6-luna",
    effort: str = "xhigh",
    max_tokens: int = 400,
) -> JudgeResult:
    """一回の chat completions で種別・回答・返信を生成する。"""
    started = time.monotonic()
    debug: dict = {
        "latency_s": 0.0,
        "finish_reason": None,
        "completion_tokens": 0,
        "reasoning_tokens": 0,
        "prompt_tokens": 0,
    }
    try:
        system = RULES_PATH.read_text(encoding="utf-8").format(
            problem_text=problem.problem_text,
            truth=problem.truth,
            fact_sheet="\n".join(f"- {line}" for line in problem.fact_sheet),
        )
        schema = {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": list(KINDS)},
                "answer": {
                    "anyOf": [
                        {"type": "string", "enum": ["yes", "no", "irrelevant", "unknown"]},
                        {"type": "null"},
                    ]
                },
                "reply": {"type": "string"},
            },
            "required": ["kind", "answer", "reply"],
            "additionalProperties": False,
        }
        payload = {
            "model": model,
            "reasoning_effort": effort,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": text},
            ],
            "max_completion_tokens": max_tokens,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "comment_judgement", "strict": True, "schema": schema},
            },
        }
        req = request.Request(
            OPENAI_CHAT_COMPLETIONS_URL,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=90) as response:
            body = json.loads(response.read().decode("utf-8"))
        choice = body["choices"][0]
        debug["finish_reason"] = choice.get("finish_reason")
        usage = body.get("usage", {})
        debug["completion_tokens"] = usage.get("completion_tokens", 0) or 0
        debug["reasoning_tokens"] = usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0) or 0
        debug["prompt_tokens"] = usage.get("prompt_tokens", 0) or 0
        debug["latency_s"] = round(time.monotonic() - started, 6)
        if debug["finish_reason"] == "length":
            return _error_result("finish_reason=length", debug)
        raw_content = choice.get("message", {}).get("content")
        if not isinstance(raw_content, str):
            return _error_result("JSON content is missing", debug)
        data = json.loads(raw_content)
        kind = data["kind"]
        answer = data["answer"]
        reply = data["reply"]
        if kind not in KINDS or not isinstance(reply, str):
            return _error_result("JSON has invalid kind or reply", debug)
        if kind == "q_yesno":
            if answer not in {"yes", "no", "irrelevant", "unknown"}:
                return _error_result("q_yesno answer is invalid", debug)
        else:
            answer = None
        if kind in templates.NO_REPLY_KINDS:
            reply = None
        elif kind in {"troll", "abuse"}:
            reply = templates.pick(kind, comment_id)
        return JudgeResult(kind=kind, answer=answer, reply=reply, method="p1", debug=debug)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        debug["latency_s"] = round(time.monotonic() - started, 6)
        return _error_result(f"invalid response: {exc}", debug)
    except error.HTTPError as exc:
        debug["latency_s"] = round(time.monotonic() - started, 6)
        detail = exc.read().decode("utf-8", "replace")[:300]
        return _error_result(f"HTTP {exc.code}: {detail}", debug)
    except Exception as exc:  # noqa: BLE001 - 試走中の API エラーを結果に残す
        debug["latency_s"] = round(time.monotonic() - started, 6)
        return _error_result(str(exc), debug)
