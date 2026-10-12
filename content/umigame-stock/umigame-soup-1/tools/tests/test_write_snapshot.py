"""Offline tests for the manual umigame snapshot writer."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

import write_snapshot


EXPECTED_JSON = (
    '{"schema_version": 4, "set_code": "umigame-soup-1", '
    '"media_id": "media-123", "content_key": "U042", '
    '"posted_at": "2026-10-12T01:02:03Z", "problem_text": "なぜ？", '
    '"truth": "扉が開いた。", "fact_sheet": ["焦げ跡はない", "鍵は閉まっていた"], '
    '"core_points": ["実は鍵が内側にある"], '
    '"judge_criteria": {"points": [{"hit": "内側に鍵", '
    '"touch": "鍵の位置を説明"}], "errors": ["誰かが侵入した"]}, '
    '"core_words": {"words": ["内側", "鍵"], "except": ["鍵の遊び方"]}, '
    '"reveal_text": "真相を公開。", "rule_text": "はい/いいえで質問", '
    '"master_rules": "質問への回答は「はい」「いいえ」"}'
)


def candidate_row() -> dict[str, Any]:
    """Return a Data API row with JSON columns encoded as strings."""
    return {
        "media_id": "media-123",
        "generation_run_id": 45,
        "item_id": 7,
        "content_key": "U042",
        "posted_at": "2026-10-12 01:02:03",
        "problem_text": "なぜ？",
        "truth": "扉が開いた。",
        "fact_sheet": '["焦げ跡はない", "鍵は閉まっていた"]',
        "core_points": '["実は鍵が内側にある"]',
        "judge_criteria": (
            '{"points": [{"hit": "内側に鍵", "touch": "鍵の位置を説明"}], '
            '"errors": ["誰かが侵入した"]}'
        ),
        "core_words": '{"words": ["内側", "鍵"], "except": ["鍵の遊び方"]}',
        "reveal_text": "真相を公開。",
        "rule_text": "はい/いいえで質問",
        "master_rules": "質問への回答は「はい」「いいえ」",
    }


class MockAwsCli:
    """Route AWS CLI subprocess calls to canned offline responses."""

    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self.commands: list[list[str]] = []
        self.events: list[str] = []
        self.uploaded_bodies: list[bytes] = []

    def __call__(
        self, command: list[str], **_kwargs: Any
    ) -> subprocess.CompletedProcess:
        self.commands.append(command)
        if command[1:3] == ["rds-data", "execute-statement"]:
            sql = command[command.index("--sql") + 1]
            if sql.startswith("UPDATE umigame_items"):
                self.events.append("update")
                stdout = json.dumps({"numberOfRecordsUpdated": 1})
            else:
                self.events.append("select")
                stdout = json.dumps(
                    {"formattedRecords": json.dumps(self.rows, ensure_ascii=False)},
                    ensure_ascii=False,
                )
            return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

        if command[1:3] == ["s3api", "put-object"]:
            self.events.append("put")
            body_path = command[command.index("--body") + 1]
            self.uploaded_bodies.append(Path(body_path).read_bytes())
            return subprocess.CompletedProcess(command, 0, stdout="{}", stderr="")

        if command[1:3] == ["sts", "get-caller-identity"]:
            return subprocess.CompletedProcess(
                command, 0, stdout="123456789012\n", stderr=""
            )

        raise AssertionError(f"Unexpected AWS CLI command: {command}")


def run_with_mocked_aws(
    monkeypatch: pytest.MonkeyPatch,
    rows: list[dict[str, Any]],
    args: list[str],
) -> tuple[int, MockAwsCli]:
    """Run the CLI with AWS and Aurora calls redirected to an in-memory mock."""
    aws_cli = MockAwsCli(rows)
    monkeypatch.setattr(
        write_snapshot, "resolve_endpoints", lambda: ("cluster", "secret")
    )
    monkeypatch.setattr(write_snapshot.subprocess, "run", aws_cli)
    return write_snapshot.main(args), aws_cli


def test_apply_serializes_the_service_snapshot_and_puts_before_update(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The Data API row becomes the exact service JSON, then S3 precedes UPDATE."""
    exit_code, aws_cli = run_with_mocked_aws(
        monkeypatch,
        [candidate_row()],
        ["--apply", "--bucket", "snapshot-test-bucket"],
    )

    assert exit_code == 0
    assert aws_cli.uploaded_bodies == [EXPECTED_JSON.encode("utf-8")]
    assert aws_cli.events == ["select", "put", "update"]

    put_command = next(
        command
        for command in aws_cli.commands
        if command[1:3] == ["s3api", "put-object"]
    )
    assert put_command[put_command.index("--content-type") + 1] == (
        "application/json; charset=utf-8"
    )
    update_command = next(
        command
        for command in aws_cli.commands
        if command[1:3] == ["rds-data", "execute-statement"]
        and command[command.index("--sql") + 1].startswith("UPDATE umigame_items")
    )
    update_sql = update_command[update_command.index("--sql") + 1]
    assert "WHERE id = :item_id AND snapshot_s3_key IS NULL" in update_sql


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("core_points", None),
        ("judge_criteria", None),
        ("core_words", None),
        ("reveal_text", "  "),
        ("master_rules", ""),
    ],
)
def test_invalid_required_fields_are_skipped_and_return_one(
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: Any,
) -> None:
    """Rows without required problem data or a non-empty prompt are rejected."""
    row = candidate_row()
    row[field] = value

    exit_code, aws_cli = run_with_mocked_aws(
        monkeypatch,
        [row],
        ["--apply", "--bucket", "snapshot-test-bucket"],
    )

    assert exit_code == 1
    assert "put" not in aws_cli.events
    assert "update" not in aws_cli.events


def test_default_mode_lists_without_put_or_update(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The default invocation only prints the selected post details."""
    exit_code, aws_cli = run_with_mocked_aws(monkeypatch, [candidate_row()], [])

    assert exit_code == 0
    assert capsys.readouterr().out.strip().splitlines() == [
        "media_id\tgeneration_run_id\tcontent_key\tposted_at",
        "media-123\t45\tU042\t2026-10-12 01:02:03",
    ]
    assert aws_cli.events == ["select"]
    assert not aws_cli.uploaded_bodies


def test_media_id_filter_uses_a_named_data_api_parameter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The optional platform media filter is passed as a SQL parameter."""
    exit_code, aws_cli = run_with_mocked_aws(
        monkeypatch,
        [candidate_row()],
        ["--media-id", "media-123"],
    )

    assert exit_code == 0
    select_command = next(
        command
        for command in aws_cli.commands
        if command[1:3] == ["rds-data", "execute-statement"]
    )
    select_sql = select_command[select_command.index("--sql") + 1]
    assert "p.platform_post_id = :media_id" in select_sql
    parameters = json.loads(select_command[select_command.index("--parameters") + 1])
    assert parameters[-1] == {
        "name": "media_id",
        "value": {"stringValue": "media-123"},
    }


@pytest.mark.parametrize("value", [
    "broken", b"\xff", "[]", "{}",
    {"words": ["核心"]}, {"except": []},
    {"words": [], "except": []}, {"words": "核心", "except": []},
    {"words": ["核心"], "except": None}, {"words": ["核心"], "except": "例外"},
    {"words": ["核心", "核心"], "except": []},
    {"words": ["核心"], "except": ["例外", "例外"]},
    {"words": ["核心"], "except": [], "extra": []},
    *({"words": [word], "except": []} for word in ("", " ", "核\n心", "核\r心", 1, None, [])),
    *({"words": ["核心"], "except": [word]} for word in ("", " ", "例\n外", "例\r外", 1, None, [])),
])
def test_build_snapshot_rejects_invalid_core_words(value: object) -> None:
    row = candidate_row()
    row["core_words"] = value
    with pytest.raises(RuntimeError, match="core_words"):
        write_snapshot.build_snapshot(row, "umigame-soup-1")


@pytest.mark.parametrize("encode", [
    lambda value: value,
    lambda value: json.dumps(value, ensure_ascii=False),
    lambda value: json.dumps(value, ensure_ascii=False).encode("utf-8"),
    lambda value: bytearray(json.dumps(value, ensure_ascii=False).encode("utf-8")),
])
@pytest.mark.parametrize("excepts", [[], ["遊び方"]])
def test_build_snapshot_accepts_valid_core_words(encode, excepts) -> None:
    row = candidate_row()
    value = {"words": ["遊び", "鬼"], "except": excepts}
    row["core_words"] = encode(value)
    snapshot = write_snapshot.build_snapshot(row, "umigame-soup-1")
    assert snapshot["schema_version"] == 4
    assert snapshot["core_words"] == value


def test_rewrite_lists_recorded_keys_without_upload_or_db_update(monkeypatch, capsys) -> None:
    row = {**candidate_row(), "snapshot_s3_key": "old/custom/key.json"}
    exit_code, aws_cli = run_with_mocked_aws(monkeypatch, [row], ["--rewrite"])
    assert exit_code == 0
    assert capsys.readouterr().out.strip().splitlines() == [
        "media_id\tcontent_key\tsnapshot_s3_key",
        "media-123\tU042\told/custom/key.json",
    ]
    assert aws_cli.events == ["select"]
    select_command = aws_cli.commands[0]
    select_sql = select_command[select_command.index("--sql") + 1]
    assert "ui.snapshot_s3_key AS snapshot_s3_key" in select_sql
    assert "ui.snapshot_s3_key IS NOT NULL" in select_sql
    assert "ui.snapshot_s3_key IS NULL" not in select_sql


def test_rewrite_default_lists_targets_before_core_words_are_backfilled(monkeypatch, capsys) -> None:
    row = {**candidate_row(), "snapshot_s3_key": "old/custom/key.json", "core_words": None}
    exit_code, aws_cli = run_with_mocked_aws(monkeypatch, [row], ["--rewrite"])
    assert exit_code == 0
    assert "media-123\tU042\told/custom/key.json" in capsys.readouterr().out
    assert aws_cli.events == ["select"]


def test_rewrite_apply_uses_the_recorded_key_and_never_updates_db(monkeypatch) -> None:
    row = {**candidate_row(), "snapshot_s3_key": "old/custom/key.json"}
    exit_code, aws_cli = run_with_mocked_aws(
        monkeypatch, [row],
        ["--rewrite", "--apply", "--bucket", "snapshot-test-bucket", "--media-id", "media-123"],
    )
    assert exit_code == 0
    assert aws_cli.events == ["select", "put"]
    assert aws_cli.uploaded_bodies == [EXPECTED_JSON.encode("utf-8")]
    put_command = aws_cli.commands[-1]
    assert put_command[put_command.index("--key") + 1] == "old/custom/key.json"
    select_command = aws_cli.commands[0]
    select_sql = select_command[select_command.index("--sql") + 1]
    assert "ui.snapshot_s3_key IS NOT NULL" in select_sql
    assert "p.platform_post_id = :media_id" in select_sql
    parameters = json.loads(select_command[select_command.index("--parameters") + 1])
    assert parameters[-1] == {"name": "media_id", "value": {"stringValue": "media-123"}}


@pytest.mark.parametrize("key", [None, "", " ", 123])
def test_rewrite_rejects_missing_recorded_key_without_upload(monkeypatch, key) -> None:
    row = {**candidate_row(), "snapshot_s3_key": key}
    exit_code, aws_cli = run_with_mocked_aws(
        monkeypatch, [row], ["--rewrite", "--apply", "--bucket", "snapshot-test-bucket"],
    )
    assert exit_code == 1
    assert aws_cli.events == ["select"]


def test_rewrite_rejects_missing_core_words_without_upload_or_db_update(monkeypatch) -> None:
    row = {**candidate_row(), "snapshot_s3_key": "old/key.json", "core_words": None}
    exit_code, aws_cli = run_with_mocked_aws(
        monkeypatch, [row], ["--rewrite", "--apply", "--bucket", "snapshot-test-bucket"],
    )
    assert exit_code == 1
    assert aws_cli.events == ["select"]


def test_rewrite_put_failure_does_not_update_db(monkeypatch, capsys) -> None:
    row = {**candidate_row(), "snapshot_s3_key": "old/key.json"}
    aws_cli = MockAwsCli([row])

    def fail_put(command, **kwargs):
        if command[1:3] == ["s3api", "put-object"]:
            return subprocess.CompletedProcess(command, 1, stdout="", stderr="S3 failed")
        return aws_cli(command, **kwargs)

    monkeypatch.setattr(write_snapshot, "resolve_endpoints", lambda: ("cluster", "secret"))
    monkeypatch.setattr(write_snapshot.subprocess, "run", fail_put)
    assert write_snapshot.main(["--rewrite", "--apply", "--bucket", "snapshot-test-bucket"]) == 1
    assert "S3 failed" in capsys.readouterr().err
    assert aws_cli.events == ["select"]
