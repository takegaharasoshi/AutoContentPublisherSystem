"""Instagram Graph API comment reply transport."""

from __future__ import annotations

import json
from urllib import parse, request

from app.http_util import post_with_retry


def reply_to_comment(
    comment_id: str, text: str, access_token: str, *,
    base_url: str = "https://graph.instagram.com/v23.0",
) -> str:
    """Send a comment reply and return its ID; truncate only at this boundary."""
    if not comment_id or not access_token or not text:
        raise ValueError("comment_id, access_token and text are required")
    url = f"{base_url.rstrip('/')}/{parse.quote(comment_id, safe='')}/replies"
    payload = parse.urlencode({"message": text[:200], "access_token": access_token}).encode("utf-8")
    req = request.Request(
        url, data=payload, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    data = json.loads(post_with_retry(req, timeout=20).decode("utf-8"))
    reply_id = data.get("id") if isinstance(data, dict) else None
    if not isinstance(reply_id, str) or not reply_id:
        raise ValueError("Graph API response has no reply id")
    return reply_id
