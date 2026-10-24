"""Graph API pagination, fields, encoded replies and credential-safe errors."""

from __future__ import annotations

import io
import json
from urllib import error, parse, request

import pytest

from app import graph_api, http_util


class Response(io.BytesIO):
    def __init__(self, data) -> None:
        super().__init__(json.dumps(data, ensure_ascii=False).encode("utf-8"))


def test_me_and_media_follow_all_pages_with_exact_fields(monkeypatch) -> None:
    seen = []
    pages = iter([
        {"user_id": "own-id", "username": "coach"},
        {"data": [{"id": "m1", "comments_count": 4}],
         "paging": {"next": f"{graph_api.DEFAULT_BASE}/me/media?after=cursor"}},
        {"data": [{"id": "m2", "comments_count": 0}]},
    ])

    def respond(req, **kwargs):
        seen.append(req)
        assert req.get_header("Authorization") == "Bearer secret-token"
        return Response(next(pages))

    monkeypatch.setattr(request, "urlopen", respond)
    assert graph_api.me("secret-token")["username"] == "coach"
    assert [m["id"] for m in graph_api.list_media("secret-token")] == ["m1", "m2"]
    assert parse.parse_qs(parse.urlsplit(seen[0].full_url).query) == {"fields": ["user_id,username"]}
    assert parse.parse_qs(parse.urlsplit(seen[1].full_url).query) == {
        "fields": ["id,timestamp,comments_count"], "limit": ["100"],
    }
    assert len(seen) == 3


def test_comment_pages_and_nested_reply_pages_are_complete(monkeypatch) -> None:
    seen = []
    pages = iter([
        {"data": [{"id": "c1", "replies": {"data": [{"id": "r1"}],
                    "paging": {"next": f"{graph_api.DEFAULT_BASE}/c1/replies?after=r1"}}}],
         "paging": {"next": f"{graph_api.DEFAULT_BASE}/m/comments?after=c1"}},
        {"data": [{"id": "c2"}]},
        {"data": [{"id": "r2"}]},
    ])

    def respond(req, **kwargs):
        seen.append(req)
        return Response(next(pages))

    monkeypatch.setattr(request, "urlopen", respond)
    comments = graph_api.list_comments("m", "token")
    assert comments[0]["replies"]["data"] == [{"id": "r1"}, {"id": "r2"}]
    assert comments[1]["replies"]["data"] == []
    query = parse.parse_qs(parse.urlsplit(seen[0].full_url).query)
    assert query == {"fields": ["id,text,username,from{id,username},timestamp,replies{id}"], "limit": ["50"]}
    assert len(seen) == 3


def test_commenter_username_falls_back_to_from(monkeypatch) -> None:
    pages = iter([{"data": [
        {"id": "c1", "text": "a", "from": {"id": "u1", "username": "viewer"}},
        {"id": "c2", "text": "b", "username": "owner", "from": {"id": "u2", "username": "owner"}},
        {"id": "c3", "text": "c"},
    ]}])
    monkeypatch.setattr(request, "urlopen", lambda req, **kwargs: Response(next(pages)))
    comments = graph_api.list_comments("m", "token")
    assert [c.get("username") for c in comments] == ["viewer", "owner", None]


@pytest.mark.parametrize("payload", [
    {"data": [] , "paging": {"next": "https://attacker.invalid/steal"}},
    {"data": {}}, {"data": [{"id": "m", "comments_count": True}]},
])
def test_bad_media_or_foreign_pagination_does_not_silently_skip(monkeypatch, payload) -> None:
    monkeypatch.setattr(request, "urlopen", lambda *a, **k: Response(payload))
    with pytest.raises(ValueError):
        graph_api.list_media("token")


def test_pagination_cycle_fails_instead_of_looping(monkeypatch) -> None:
    url = graph_api._url(graph_api.DEFAULT_BASE, "me/media", fields="id,timestamp,comments_count", limit="100")
    monkeypatch.setattr(request, "urlopen", lambda *a, **k: Response({"data": [], "paging": {"next": url}}))
    with pytest.raises(ValueError, match="loop"):
        graph_api.list_media("token")


def test_post_reply_encodes_recipient_and_message(monkeypatch) -> None:
    seen = []

    def respond(req, **kwargs):
        seen.append(req)
        return Response({"id": "reply-id"})

    monkeypatch.setattr(request, "urlopen", respond)
    assert graph_api.post_reply("comment/id", "@reader 正解👏", "token") == "reply-id"
    req = seen[0]
    assert req.get_method() == "POST" and "/comment%2Fid/replies" in req.full_url
    assert parse.parse_qs(req.data.decode()) == {"message": ["@reader 正解👏"], "access_token": ["token"]}


def test_post_reply_missing_id_is_failure(monkeypatch) -> None:
    monkeypatch.setattr(request, "urlopen", lambda *a, **k: Response({}))
    with pytest.raises(ValueError):
        graph_api.post_reply("c", "message", "token")


def test_refresh_uses_unversioned_endpoint_and_sanitizes_failure(monkeypatch, caplog) -> None:
    seen = []

    def respond(req, **kwargs):
        seen.append(req)
        return Response({"access_token": "new", "expires_in": 3600})

    monkeypatch.setattr(request, "urlopen", respond)
    assert graph_api.refresh_token("secret+/token")["access_token"] == "new"
    assert parse.urlsplit(seen[0].full_url).path == "/refresh_access_token"
    assert parse.parse_qs(parse.urlsplit(seen[0].full_url).query) == {
        "grant_type": ["ig_refresh_token"], "access_token": ["secret+/token"],
    }

    def fail(req, **kwargs):
        raise error.HTTPError(req.full_url, 400, "secret+/token", None, io.BytesIO(b"{}"))

    monkeypatch.setattr(request, "urlopen", fail)
    with pytest.raises(RuntimeError) as raised:
        graph_api.refresh_token("secret+/token")
    assert "secret" not in str(raised.value) and "https://" not in str(raised.value)
    assert "secret+/token" not in caplog.text
