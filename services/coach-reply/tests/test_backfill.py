"""Offline backfill tests: SELECT discovery, dry runs and no overwrites."""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

from tools import backfill_snapshots as tool


def error(code):
    return ClientError({"Error": {"Code": code}}, "HeadObject")


def answer(media_id="m"):
    return {"media_id": media_id, "posted_at": "2026-10-24 00:00:00", "quiz_type": "L1",
            "difficulty": "light", "question_text": "問題", "answer_text": "答え",
            "content_fields": '{"explanation":"解説","hint":"ヒント"}'}


def test_dry_run_is_default_and_deduplicates_media() -> None:
    client = Mock()
    client.head_object.side_effect = [None, error("404")]
    result = tool.backfill([answer("existing"), answer("missing"), answer("missing")],
                           "bucket", "p/", client=client)
    assert result == {"posts": 2, "existing": 1, "missing": 1, "written": 0}
    assert client.head_object.call_count == 2
    client.put_object.assert_not_called()


def test_apply_only_writes_missing_snapshots_conditionally() -> None:
    client = Mock()
    client.head_object.side_effect = [None, error("NoSuchKey")]
    result = tool.backfill([answer("existing"), answer("missing")], "bucket", "p/",
                           apply=True, client=client)
    assert result == {"posts": 2, "existing": 1, "missing": 1, "written": 1}
    call = client.put_object.call_args.kwargs
    snapshot = json.loads(call["Body"])
    assert call["IfNoneMatch"] == "*" and call["Key"] == "p/missing.json"
    assert snapshot["source"] == "backfill" and snapshot["hint"] == "ヒント"
    assert snapshot["explanation"] == "解説" and snapshot["posted_at"].endswith("Z")


def test_concurrent_post_snapshot_is_never_overwritten() -> None:
    client = Mock()
    client.head_object.side_effect = error("404")
    client.put_object.side_effect = error("PreconditionFailed")
    assert tool.backfill([answer()], "b", "p/", apply=True, client=client) == {
        "posts": 1, "existing": 1, "missing": 0, "written": 0,
    }


def test_access_denied_is_fatal_and_not_treated_as_missing() -> None:
    client = Mock()
    client.head_object.side_effect = error("AccessDenied")
    with pytest.raises(ClientError):
        tool.backfill([answer()], "b", "p/", apply=True, client=client)
    client.put_object.assert_not_called()


def test_cli_dry_run_is_default_and_apply_is_explicit(monkeypatch, capsys) -> None:
    monkeypatch.setattr(tool, "aurora_execute", lambda: [answer()])
    seen = []

    def backfill(*args, **kwargs):
        seen.append(kwargs["apply"])
        return {"posts": 1, "existing": 0, "missing": 1, "written": int(kwargs["apply"])}

    monkeypatch.setattr(tool, "backfill", backfill)
    tool.main(["--bucket", "b"])
    tool.main(["--bucket", "b", "--apply"])
    assert seen == [False, True]
    assert '"mode": "dry-run"' in capsys.readouterr().out


def test_select_uses_same_env_arn_overrides_as_collect(monkeypatch) -> None:
    monkeypatch.setenv("AURORA_CLUSTER_ARN", "cluster-override")
    monkeypatch.setenv("AURORA_SECRET_ARN", "secret-override")
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout=json.dumps({"formattedRecords": json.dumps([answer()])}), stderr="")

    monkeypatch.setattr(tool.subprocess, "run", run)
    assert tool.aurora_execute() == [answer()]
    assert len(calls) == 1
    command = calls[0]
    assert command[:3] == ["aws", "rds-data", "execute-statement"]
    assert command[command.index("--resource-arn") + 1] == "cluster-override"
    assert command[command.index("--secret-arn") + 1] == "secret-override"
    assert command[command.index("--sql") + 1] == tool.ANSWERS_SQL
    assert "p.status = 'success'" in tool.ANSWERS_SQL and "q.generation_run_id = p.generation_run_id" in tool.ANSWERS_SQL


def test_missing_arns_use_collect_discovery_and_database_resume_retry(monkeypatch) -> None:
    monkeypatch.delenv("AURORA_CLUSTER_ARN", raising=False)
    monkeypatch.delenv("AURORA_SECRET_ARN", raising=False)
    calls, sleeps = [], []

    def run(command, **kwargs):
        calls.append(command)
        if command[1] == "rds":
            return SimpleNamespace(stdout="discovered-cluster\n")
        if command[1] == "secretsmanager":
            return SimpleNamespace(stdout="discovered-secret\n")
        if len(calls) == 3:
            return SimpleNamespace(returncode=1, stdout="", stderr="DatabaseResumingException")
        return SimpleNamespace(returncode=0, stdout='{"formattedRecords":"[]"}', stderr="")

    monkeypatch.setattr(tool.subprocess, "run", run)
    monkeypatch.setattr(tool.time, "sleep", sleeps.append)
    assert tool.aurora_execute() == []
    assert "DBClusters[0].DBClusterArn" in calls[0]
    assert "SecretList[?contains(Name,'db/credentials')].ARN" in calls[1]
    assert calls[2] == calls[3] and sleeps == [20]
