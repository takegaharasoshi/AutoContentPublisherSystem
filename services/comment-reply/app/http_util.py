"""Small urllib transport shared by LLM and Graph API clients."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib import error, request


def post_with_retry(
    req: request.Request, *, retries: int = 3, initial_backoff_s: float = 2.0,
    timeout: float = 90.0, retry_statuses: set[int] | None = None,
) -> bytes:
    """POST and retry only rate limits and server errors with exponential delay."""
    for attempt in range(retries + 1):
        try:
            with request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except error.HTTPError as exc:
            eligible = exc.code in retry_statuses if retry_statuses is not None else (
                exc.code == 429 or 500 <= exc.code <= 599
            )
            if eligible and attempt < retries:
                time.sleep(initial_backoff_s * 2**attempt)
                continue
            raise
    raise RuntimeError("unreachable")


def post_json_with_retry(req: request.Request, **kwargs: Any) -> dict[str, Any]:
    """POST and parse a JSON object."""
    body = json.loads(post_with_retry(req, **kwargs).decode("utf-8"))
    if not isinstance(body, dict):
        raise ValueError("HTTP response must be a JSON object")
    return body
