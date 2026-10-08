"""Standard-library Anthropic structured output transport and diagnostics."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib import error, request

from app.http_util import post_json_with_retry


MESSAGES_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-5-5"
USAGE_FIELDS = (
    "input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
)
STRING_CONSTRAINTS = frozenset({"minLength", "maxLength", "pattern", "format"})
# Thinking at effort max can run past 16000 tokens (21-6d13: 7 truncations), so max_tokens is 32000;
# at ~200 tokens/s that is up to ~160 s, and 90 s (the shared default) is too short.
TIMEOUT_S = 420.0


class AnthropicError(RuntimeError):
    """Failed structured output, retaining usage and the reason for the failure."""

    def __init__(self, message: str, *, debug: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.debug = debug if debug is not None else {}


class AnthropicRefusalError(AnthropicError):
    """A safety refusal with its server-provided category."""

    def __init__(
        self, message: str, *, debug: dict[str, Any] | None = None,
        category: str | None = None,
    ) -> None:
        super().__init__(message, debug=debug)
        self.category = category if category is not None else self.debug.get("refusal_category")


def adapt_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Copy a schema, dropping string constraints and closing every object."""
    def adapt(value: Any) -> Any:
        if isinstance(value, list):
            return [adapt(item) for item in value]
        if not isinstance(value, dict):
            return value
        converted = {}
        for key, item in value.items():
            if key in STRING_CONSTRAINTS:
                continue
            if key in {"properties", "$defs", "definitions", "patternProperties"}:
                converted[key] = {name: adapt(child) for name, child in item.items()}
            else:
                converted[key] = adapt(item)
        if converted.get("type") == "object" or "properties" in converted:
            converted["additionalProperties"] = False
        return converted

    return adapt(schema)


def request_json(
    system: str, text: str, schema: dict[str, Any], *, api_key: str,
    effort: str, max_tokens: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Request one non-streaming JSON object, ignoring thinking blocks.

    Args:
        system: The shared Luna system prompt.
        text: The single user message.
        schema: The shared structured output contract, copied for Anthropic.
        api_key: The local ANTHROPIC_API_KEY value.
        effort: Explicit effort for this judge or writer variant.
        max_tokens: Output budget, including thinking tokens.

    Returns:
        The decoded object and telemetry, including cache usage.

    Raises:
        AnthropicRefusalError: The model refused the request.
        AnthropicError: Transport, truncation, or invalid output failure.
    """
    started = time.monotonic()
    debug: dict[str, Any] = {"model": MODEL, "stop_reason": None, "refusal_category": None}
    try:
        if not api_key:
            raise ValueError("anthropic_api_key is empty")
        payload = {
            "model": MODEL,
            "system": [{"type": "text", "text": system,
                        "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": text}],
            "output_config": {"effort": effort,
                              "format": {"type": "json_schema", "schema": adapt_schema(schema)}},
            "max_tokens": max_tokens,
            "stream": False,
        }
        req = request.Request(
            MESSAGES_URL, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"}, method="POST",
        )
        try:
            body = post_json_with_retry(req, retries=3, initial_backoff_s=5, timeout=TIMEOUT_S)
        except error.HTTPError as exc:
            # Keep the API's error type and message (e.g. low credit balance) for diagnosis.
            try:
                detail = json.loads(exc.read().decode("utf-8")).get("error") or {}
            except Exception:
                detail = {}
            debug["error_reason"] = "request_failed"
            debug["http_status"] = exc.code
            debug["api_error_type"] = detail.get("type")
            raise AnthropicError(
                f"HTTP Error {exc.code}: {detail.get('type')}: {detail.get('message')}", debug=debug,
            ) from exc
        usage = body.get("usage") or {}
        debug["usage"] = {key: usage.get(key, 0) or 0 for key in USAGE_FIELDS}
        debug.update(debug["usage"])
        debug["prompt_tokens"] = sum(debug[key] for key in (
            "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
        ))
        debug["completion_tokens"] = debug["output_tokens"]
        debug["stop_reason"] = body.get("stop_reason")
        if debug["stop_reason"] == "refusal":
            debug["refusal_category"] = (body.get("stop_details") or {}).get("category")
            debug["error_reason"] = "refusal"
            raise AnthropicRefusalError("Anthropic response refused", debug=debug)
        if debug["stop_reason"] == "max_tokens":
            debug["error_reason"] = "max_tokens"
            raise AnthropicError("Anthropic response exceeded max_tokens", debug=debug)
        content = body.get("content")
        if not isinstance(content, list):
            content = []
        blocks = [block for block in content
                  if isinstance(block, dict) and block.get("type") == "text"]
        if not blocks:
            debug["error_reason"] = "missing_text"
            raise AnthropicError("Anthropic response has no text block", debug=debug)
        parts = [block.get("text") for block in blocks]
        if any(not isinstance(part, str) for part in parts):
            debug["error_reason"] = "invalid_text"
            raise AnthropicError("Anthropic response text is not a string", debug=debug)
        output = "".join(parts)
        if not output.strip():
            debug["error_reason"] = "empty_text"
            raise AnthropicError("Anthropic response text is empty", debug=debug)
        debug["error_reason"] = "invalid_json"
        data = json.loads(output)
        if not isinstance(data, dict):
            raise ValueError("Anthropic response is not an object")
        debug.pop("error_reason")
        return data, debug
    except AnthropicError:
        raise
    except Exception as exc:
        debug.setdefault("error_reason", "request_failed")
        raise AnthropicError(str(exc), debug=debug) from exc
    finally:
        debug["latency_s"] = round(time.monotonic() - started, 6)
