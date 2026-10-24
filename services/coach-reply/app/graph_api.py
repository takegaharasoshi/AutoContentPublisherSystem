"""Independent Instagram transport copied from comment-reply and extended."""

from __future__ import annotations

import json
from typing import Any
from urllib import parse, request

from app.http_util import post_json_with_retry, post_with_retry


DEFAULT_BASE = "https://graph.instagram.com/v25.0"


def _get_json(url: str, access_token: str, *, timeout: float = 20.0) -> dict:
    """GET JSON without exposing token-bearing URLs in exceptions or logs."""
    req = request.Request(
        url, method="GET", headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        return post_json_with_retry(req, retries=2, timeout=timeout)
    except Exception:
        raise RuntimeError("Graph API GET failed") from None


def _url(base_url: str, path: str, **query: str) -> str:
    return f"{base_url.rstrip('/')}/{path}?{parse.urlencode(query)}"


def _next_url(page: dict, base_url: str) -> str | None:
    next_url = page.get("paging", {}).get("next")
    if next_url is None:
        return None
    if not isinstance(next_url, str) or not next_url:
        raise ValueError("invalid Graph API next page")
    parsed = parse.urlsplit(next_url)
    base = parse.urlsplit(base_url)
    if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc):
        raise ValueError("Graph API next page has an unexpected origin")
    return next_url


def _pages(url: str, access_token: str, base_url: str) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    while url:
        if url in seen:
            raise ValueError("Graph API pagination loop")
        seen.add(url)
        page = _get_json(url, access_token)
        data = page.get("data")
        if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
            raise ValueError("Graph API page has no data list")
        rows.extend(data)
        url = _next_url(page, base_url)
    return rows


def me(access_token: str, *, base_url: str = DEFAULT_BASE) -> dict:
    """Read the operator username for this invocation only."""
    data = _get_json(_url(base_url, "me", fields="user_id,username"), access_token)
    if not isinstance(data.get("username"), str) or not data["username"].strip():
        raise ValueError("Graph API me has no username")
    return data


def list_media(access_token: str, *, base_url: str = DEFAULT_BASE) -> list[dict]:
    """Read every media page, retaining counts that increased or decreased."""
    rows = _pages(_url(base_url, "me/media", fields="id,timestamp,comments_count", limit="100"),
                  access_token, base_url)
    for row in rows:
        if (not isinstance(row.get("id"), str) or not row["id"]
                or type(row.get("comments_count")) is not int or row["comments_count"] < 0):
            raise ValueError("invalid Graph API media id or comments_count")
    return rows


def list_comments(
    media_id: str, access_token: str, *, base_url: str = DEFAULT_BASE,
) -> list[dict]:
    """Read all comments and embedded reply IDs, including their next pages."""
    rows = _pages(_url(base_url, f"{parse.quote(media_id, safe='')}/comments",
                       fields="id,text,username,timestamp,replies{id}", limit="50"),
                  access_token, base_url)
    for row in rows:
        if not isinstance(row.get("id"), str) or not row["id"]:
            raise ValueError("Graph API comment has no id")
        replies = row.get("replies", {"data": []})
        if not isinstance(replies, dict) or not isinstance(replies.get("data"), list):
            raise ValueError("Graph API comment replies must contain a data list")
        next_url = _next_url(replies, base_url)
        data = list(replies["data"])
        if next_url:
            data.extend(_pages(next_url, access_token, base_url))
        if any(not isinstance(reply, dict) or not isinstance(reply.get("id"), str)
               or not reply["id"] for reply in data):
            raise ValueError("Graph API reply has no id")
        row["replies"] = {"data": data}
    return rows


def post_reply(
    comment_id: str, message: str, access_token: str, *, base_url: str = DEFAULT_BASE,
) -> str:
    """Send a comment reply and return its ID; truncate only at this boundary."""
    if not comment_id or not access_token or not message:
        raise ValueError("comment_id, access_token and message are required")
    url = f"{base_url.rstrip('/')}/{parse.quote(comment_id, safe='')}/replies"
    payload = parse.urlencode({"message": message[:200], "access_token": access_token}).encode("utf-8")
    req = request.Request(
        url, data=payload, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        data = json.loads(post_with_retry(req, timeout=20).decode("utf-8"))
    except Exception:
        raise RuntimeError("Graph API reply failed") from None
    reply_id = data.get("id") if isinstance(data, dict) else None
    if not isinstance(reply_id, str) or not reply_id:
        raise ValueError("Graph API response has no reply id")
    return reply_id


def refresh_token(
    access_token: str, *, base_url: str = "https://graph.instagram.com",
) -> dict[str, Any]:
    """Call the unversioned refresh endpoint; the handler stores the result."""
    if not isinstance(access_token, str) or not access_token.strip():
        raise ValueError("ig_access_token must be a nonblank string")
    return _get_json(_url(base_url, "refresh_access_token", grant_type="ig_refresh_token",
                          access_token=access_token), access_token, timeout=30)
