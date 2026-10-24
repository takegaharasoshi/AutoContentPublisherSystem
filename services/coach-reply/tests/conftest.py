"""Shared fixtures and mandatory network isolation, copied from comment-reply."""

from __future__ import annotations

import subprocess
from urllib import request

import boto3
import pytest


@pytest.fixture(autouse=True)
def block_live_http(monkeypatch) -> None:
    """Require an explicit HTTP/AWS stub before every external operation."""
    def blocked(*args, **kwargs):
        raise AssertionError("live API requests are forbidden in offline tests")

    monkeypatch.setattr(request, "urlopen", blocked)
    monkeypatch.setattr(boto3, "client", blocked)
    monkeypatch.setattr(boto3.session.Session, "client", blocked)
    monkeypatch.setattr(subprocess, "run", blocked)


@pytest.fixture
def snapshot() -> dict:
    """Return a minimal quiz snapshot with explanation and hint."""
    return {
        "schema_version": 1, "kind": "quiz", "set_code": "logic-training-1",
        "media_id": "m1", "question_text": "食べられないパンは？", "answer_text": "フライパン",
        "explanation": "調理器具だから。", "hint": "料理に使う", "source": "post",
    }
