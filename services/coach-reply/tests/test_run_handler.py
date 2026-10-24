"""Complete invocation tests with boto3, Graph and Anthropic all stubbed."""

from __future__ import annotations

import io
import json
from copy import deepcopy
from urllib import parse, request

import boto3
import pytest
from botocore.exceptions import ClientError

from app import run_handler


BUCKET = "test-assets"
PROBLEMS = "assets/logic-training-1/problems/"
STATE = "coach-reply/logic-training-1/state/"
COUNTS = f"{STATE}media-counts.json"


def comment(cid: str, second: int = 1, **overrides) -> dict:
    return {
        "id": cid, "text": "フライパン", "username": f"reader_{cid}",
        "timestamp": f"2026-10-24T01:00:{second:02}Z", **overrides,
    }


def verdict(value: str = "correct", confidence: str = "high") -> dict:
    return {"verdict": value, "confidence": confidence, "reason": "答えの核心が一致"}


class Context:
    remaining = 300_000

    def get_remaining_time_in_millis(self) -> int:
        return self.remaining


class FakeAWS:
    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}
        self.puts: list[tuple[str, dict]] = []
        self.gets: list[str] = []
        self.enabled = "on"
        self.start = "2026-10-24T01:00:00Z"
        self.secret_reads = 0

    def client(self, service):
        assert service in {"ssm", "secretsmanager", "s3"}
        return self

    def get_parameter(self, *, Name):
        value = self.enabled if Name.endswith("reply-enabled") else self.start
        return {"Parameter": {"Value": value}}

    def get_secret_value(self, **kwargs):
        self.secret_reads += 1
        return {"SecretString": json.dumps({"ig_access_token": "private-token", "anthropic_api_key": "private-key"})}

    def get_object(self, *, Bucket, Key):
        assert Bucket == BUCKET
        self.gets.append(Key)
        if Key not in self.objects:
            raise ClientError({"Error": {"Code": "NoSuchKey"}}, "GetObject")
        return {"Body": io.BytesIO(self.objects[Key])}

    def put_object(self, *, Bucket, Key, Body, ContentType):
        assert Bucket == BUCKET and ContentType == "application/json"
        self.objects[Key] = Body
        self.puts.append((Key, json.loads(Body)))
        return {}

    def save(self, key, data):
        self.objects[key] = json.dumps(data).encode()

    def load(self, key):
        return json.loads(self.objects[key])


class FakeAPIs:
    def __init__(self) -> None:
        self.media = [{"id": "m1", "comments_count": 1}]
        self.comments = {"m1": [comment("c1")]}
        self.results = {"c1": verdict()}
        self.reply_calls = []
        self.judge_calls = []
        self.comment_reads = []
        self.requests = []
        self.fail_reply_ids = set()
        self.after_reply = lambda: None
        self.after_judge = lambda: None

    def open(self, req, **kwargs):
        self.requests.append(req)
        path = parse.urlsplit(req.full_url).path
        if req.full_url.endswith("/v1/messages"):
            payload = json.loads(req.data)
            data = json.loads(payload["messages"][0]["content"])
            self.judge_calls.append(data["comments"])
            results = [{"id": c["id"], **self.results[c["id"]]}
                       for c in data["comments"] if self.results.get(c["id"]) is not None]
            self.after_judge()
            body = {"stop_reason": "end_turn", "content": [
                {"type": "text", "text": json.dumps({"results": results})},
            ]}
        elif path.endswith("/me/media"):
            body = {"data": self.media}
        elif path.endswith("/me"):
            body = {"user_id": "own-id", "username": "coach"}
        elif path.endswith("/comments"):
            media_id = path.split("/")[-2]
            self.comment_reads.append(media_id)
            body = {"data": self.comments[media_id]}
        elif path.endswith("/replies"):
            cid = path.split("/")[-2]
            if cid in self.fail_reply_ids:
                raise OSError("sensitive Graph failure with private-token")
            self.reply_calls.append((cid, parse.parse_qs(req.data.decode())["message"][0]))
            self.after_reply()
            body = {"id": f"reply-{cid}"}
        else:
            raise AssertionError(f"unexpected stub path: {path}")
        return io.BytesIO(json.dumps(body, ensure_ascii=False).encode())


@pytest.fixture
def system(monkeypatch, snapshot):
    aws, apis, context = FakeAWS(), FakeAPIs(), Context()
    monkeypatch.setenv("SECRET_ARN", "test-arn")
    monkeypatch.setenv("ASSETS_BUCKET", BUCKET)
    monkeypatch.setenv("PROBLEMS_PREFIX", PROBLEMS)
    monkeypatch.setenv("STATE_PREFIX", STATE)
    monkeypatch.setenv("PARAM_PREFIX", "/acps/test/coach-reply/")
    monkeypatch.setattr(boto3, "client", aws.client)
    monkeypatch.setattr(request, "urlopen", apis.open)
    monkeypatch.setattr(run_handler.reply_text.random, "choice", lambda choices: choices[0])
    aws.save(f"{PROBLEMS}m1.json", snapshot)
    return aws, apis, context


def test_on_replies_chronologically_and_checkpoints_each_reply(system, caplog):
    aws, apis, context = system
    apis.media[0]["comments_count"] = 3
    apis.comments["m1"] = [comment("c2", 2), comment("wrong", 0), comment("c1", 1)]
    apis.results = {"c1": verdict(), "c2": verdict(), "wrong": verdict("wrong")}
    summary = run_handler.lambda_handler({}, context)
    assert [cid for cid, _ in apis.reply_calls] == ["c1", "c2"]
    assert apis.reply_calls[0][1].startswith("@reader_c1 正解")
    assert "一番乗り" in apis.reply_calls[0][1] and "一番乗り" not in apis.reply_calls[1][1]
    state = aws.load(f"{STATE}judged/m1.json")
    assert state["first_correct_replied"] is True
    assert state["comments"]["c1"]["reply_id"] == "reply-c1"
    assert state["comments"]["c2"]["first"] is False
    assert any(data["comments"].get("c1", {}).get("replied") and "c2" not in data["comments"]
               for key, data in aws.puts if key.endswith("judged/m1.json"))
    assert aws.load(COUNTS)["media"]["m1"]["comments_count"] == 3
    assert summary["judged"] == 3 and summary["replied"] == 2 and summary["judge_failures"] == 0
    assert len([r for r in caplog.records if r.message.startswith("coach_reply_summary ")]) == 1
    assert "private-token" not in caplog.text and "private-key" not in caplog.text
    stored = json.dumps(state, ensure_ascii=False)
    assert "フライパン" not in stored and "reader_c1" not in stored


def test_off_records_would_reply_and_switching_on_does_not_replay(system):
    aws, apis, context = system
    aws.enabled = "off"
    summary = run_handler.lambda_handler({}, context)
    record = aws.load(f"{STATE}judged/m1.json")["comments"]["c1"]
    assert record["verdict"] == "correct" and record["switch"] == "off"
    assert record["replied"] is False and record["reply_id"] is None
    assert not aws.load(f"{STATE}judged/m1.json")["first_correct_replied"]
    assert summary["replied"] == 0 and apis.reply_calls == []
    aws.enabled = "on"
    apis.media[0]["comments_count"] = 2
    apis.comments["m1"].append(comment("new-alt", 2))
    apis.results["new-alt"] = verdict("alt")
    run_handler.lambda_handler({}, context)
    assert apis.reply_calls == []
    assert [[c["id"] for c in call] for call in apis.judge_calls] == [["c1"], ["new-alt"]]
    assert aws.secret_reads == 2


@pytest.mark.parametrize("value,confidence", [
    ("correct", "low"), ("alt", "high"), ("wrong", "high"), ("unsure", "high"),
])
def test_only_correct_high_is_replied_to(system, value, confidence):
    aws, apis, context = system
    apis.results["c1"] = verdict(value, confidence)
    run_handler.lambda_handler({}, context)
    assert not apis.reply_calls
    assert aws.load(f"{STATE}judged/m1.json")["comments"]["c1"]["verdict"] == value


def test_unchanged_skips_snapshot_and_decreased_counts_are_processed(system):
    aws, apis, context = system
    aws.save(COUNTS, {"media": {"m1": {"comments_count": 1}}})
    summary = run_handler.lambda_handler({}, context)
    assert summary["selected"] == 0 and apis.comment_reads == []
    assert f"{PROBLEMS}m1.json" not in aws.gets
    aws.save(COUNTS, {"media": {"m1": {"comments_count": 9}}})
    summary = run_handler.lambda_handler({}, context)
    assert summary["selected"] == 1 and apis.comment_reads == ["m1"]


@pytest.mark.parametrize("other_kind", [False, True])
def test_missing_or_non_quiz_snapshot_updates_count_without_reading_comments(system, other_kind):
    aws, apis, context = system
    if other_kind:
        aws.save(f"{PROBLEMS}m1.json", {"kind": "umigame"})
    else:
        del aws.objects[f"{PROBLEMS}m1.json"]
    summary = run_handler.lambda_handler({}, context)
    assert summary["no_snapshot"] == 1 and apis.comment_reads == []
    assert aws.load(COUNTS)["media"]["m1"]["comments_count"] == 1


def test_manual_reply_start_exclusions_and_bodyless_rows_are_not_judged(system):
    aws, apis, context = system
    apis.media[0]["comments_count"] = 7
    apis.comments["m1"] = [
        comment("manual", 1, replies={"data": [{"id": "own-reply"}]}),
        comment("own-reply", 2, username="coach"),
        comment("old", timestamp="2026-10-24T00:59:59Z"),
        comment("reader-parent", 3, replies={"data": [{"id": "other-reply"}]}),
        comment("other-reply", 4), comment("empty", 0, text=None), comment("c1", 5),
    ]
    apis.results["reader-parent"] = verdict("wrong")
    run_handler.lambda_handler({}, context)
    records = aws.load(f"{STATE}judged/m1.json")["comments"]
    assert records["manual"]["verdict"] == "operator_replied"
    assert records["old"]["verdict"] == "before_start"
    assert {"own-reply", "other-reply", "empty"}.isdisjoint(records)
    assert {c["id"] for c in apis.judge_calls[0]} == {"reader-parent", "c1"}
    assert not records["c1"]["first"]


def test_failed_judgment_retries_three_times_then_advances_count(system):
    aws, apis, context = system
    apis.media[0]["comments_count"] = 2
    apis.comments["m1"] = [comment("missing", 0), comment("c1", 1)]
    apis.results["missing"] = None
    for count in (1, 2, 3):
        summary = run_handler.lambda_handler({}, context)
        state = aws.load(f"{STATE}judged/m1.json")
        assert state["comments"]["missing"]["fail_count"] == count
        assert summary["judge_failures"] == 1
        if count < 3:
            assert "verdict" not in state["comments"]["missing"]
            assert "m1" not in aws.load(COUNTS)["media"]
        else:
            assert state["comments"]["missing"]["verdict"] == "judge_failed"
            assert aws.load(COUNTS)["media"]["m1"]["comments_count"] == 2
    assert len(apis.reply_calls) == 1
    assert "一番乗り" not in apis.reply_calls[0][1]
    run_handler.lambda_handler({}, context)
    assert len(apis.judge_calls) == 3


def test_success_after_failure_resets_counter_and_can_reply(system):
    aws, apis, context = system
    apis.results["c1"] = None
    run_handler.lambda_handler({}, context)
    apis.results["c1"] = verdict()
    run_handler.lambda_handler({}, context)
    record = aws.load(f"{STATE}judged/m1.json")["comments"]["c1"]
    assert record["fail_count"] == 0 and record["replied"] is True
    assert len(apis.reply_calls) == 1


@pytest.mark.parametrize("setting,value", [("enabled", "bad"), ("start", "bad")])
def test_invalid_switch_errors_before_secrets_or_any_api_call(system, setting, value, caplog):
    aws, apis, context = system
    setattr(aws, setting, value)
    with pytest.raises(ValueError):
        run_handler.lambda_handler({}, context)
    assert aws.secret_reads == 0 and apis.requests == [] and aws.puts == []
    assert '"failures":1' in caplog.text


def test_under_thirty_seconds_leaves_all_posts_for_next_invocation(system):
    aws, apis, context = system
    context.remaining = 29_999
    summary = run_handler.lambda_handler({}, context)
    assert summary["deferred"] == 1 and summary["replied"] == 0
    assert aws.load(COUNTS)["media"] == {} and apis.comment_reads == []


def test_time_after_first_post_saves_it_and_defers_other_posts(system, snapshot):
    aws, apis, context = system
    apis.media.append({"id": "m2", "comments_count": 1})
    aws.save(f"{PROBLEMS}m2.json", dict(snapshot, media_id="m2"))
    apis.after_reply = lambda: setattr(context, "remaining", 29_999)
    summary = run_handler.lambda_handler({}, context)
    assert summary["deferred"] == 1
    assert set(aws.load(COUNTS)["media"]) == {"m1"}
    assert f"{PROBLEMS}m2.json" not in aws.gets


def test_time_after_judgment_does_not_mark_unreplied_results_as_done(system):
    aws, apis, context = system
    apis.after_judge = lambda: setattr(context, "remaining", 29_999)
    summary = run_handler.lambda_handler({}, context)
    assert summary["deferred"] == 1 and not apis.reply_calls
    assert "c1" not in aws.load(f"{STATE}judged/m1.json")["comments"]
    assert not aws.load(COUNTS)["media"]
    context.remaining = 300_000
    apis.after_judge = lambda: None
    run_handler.lambda_handler({}, context)
    assert len(apis.reply_calls) == 1


def test_time_between_batches_leaves_unattempted_comments_pending(system):
    aws, apis, context = system
    apis.media[0]["comments_count"] = 21
    apis.comments["m1"] = [comment(f"c{i}", i) for i in range(21)]
    apis.results = {f"c{i}": verdict("wrong") for i in range(21)}
    apis.after_judge = lambda: setattr(context, "remaining", 29_999)
    summary = run_handler.lambda_handler({}, context)
    assert len(apis.judge_calls) == 1 and len(apis.judge_calls[0]) == 20
    assert summary["judge_failures"] == 0 and not aws.load(COUNTS)["media"]
    records = aws.load(f"{STATE}judged/m1.json")["comments"]
    assert "c20" not in records and len(records) == 20
    context.remaining = 300_000
    apis.after_judge = lambda: None
    run_handler.lambda_handler({}, context)
    assert [len(call) for call in apis.judge_calls] == [20, 1]
    assert aws.load(COUNTS)["media"]["m1"]["comments_count"] == 21


def test_first_place_can_use_wrong_results_from_preceding_batch(system):
    aws, apis, context = system
    apis.media[0]["comments_count"] = 21
    apis.comments["m1"] = [comment(f"c{i}", i) for i in reversed(range(21))]
    apis.results = {f"c{i}": verdict("wrong") for i in range(20)}
    apis.results["c20"] = verdict()
    run_handler.lambda_handler({}, context)
    assert [len(call) for call in apis.judge_calls] == [20, 1]
    assert len(apis.reply_calls) == 1 and apis.reply_calls[0][0] == "c20"
    assert "一番乗り" in apis.reply_calls[0][1]


def test_replies_completed_in_previous_batch_survive_later_time_limit(system):
    aws, apis, context = system
    apis.media[0]["comments_count"] = 21
    apis.comments["m1"] = [comment(f"c{i}", i) for i in range(21)]
    apis.results = {f"c{i}": verdict() for i in range(21)}

    def expire_second_batch():
        if len(apis.judge_calls) == 2:
            context.remaining = 29_999

    apis.after_judge = expire_second_batch
    run_handler.lambda_handler({}, context)
    assert len(apis.reply_calls) == 20
    records = aws.load(f"{STATE}judged/m1.json")["comments"]
    assert len(records) == 20 and "c20" not in records
    assert not aws.load(COUNTS)["media"]
    context.remaining = 300_000
    apis.after_judge = lambda: None
    run_handler.lambda_handler({}, context)
    assert [len(call) for call in apis.judge_calls] == [20, 1, 1]
    assert len(apis.reply_calls) == 21


def test_graph_failure_preserves_previous_reply_and_retries_only_unfinished(system, caplog):
    aws, apis, context = system
    apis.media[0]["comments_count"] = 2
    apis.comments["m1"].append(comment("c2", 2))
    apis.results["c2"] = verdict()
    apis.fail_reply_ids.add("c2")
    with pytest.raises(RuntimeError):
        run_handler.lambda_handler({}, context)
    assert aws.load(f"{STATE}judged/m1.json")["comments"]["c1"]["replied"]
    assert "m1" not in aws.load(COUNTS)["media"]
    assert "private-token" not in caplog.text
    apis.fail_reply_ids.clear()
    run_handler.lambda_handler({}, context)
    assert [cid for cid, _ in apis.reply_calls] == ["c1", "c2"]
    assert [c["id"] for c in apis.judge_calls[-1]] == ["c2"]
