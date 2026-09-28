from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import run_reply_trial as reply_trial
import templates
from judge_contract import Problem


PROBLEM = Problem(
    no="N1",
    problem_text="架空の問題文です。",
    truth="秘密の真相マーカーです。",
    fact_sheet=["確定事実マーカーです。"],
    truth_points=["要点マーカー一。", "要点マーカー二。"],
    reveal_text="架空の開示文です。",
    core_points=["コア要点マーカーです。"],
)


def _custom_templates(*, q_yesno: tuple[str, ...] = ("一言です。",)) -> SimpleNamespace:
    return SimpleNamespace(
        TEMPLATES={
            "q_yesno": q_yesno,
            "q_multi": ("質問を分けてください。",),
            "guess_close": ("もう少しです。",),
            "guess_wrong": ("別の推理です。",),
            "spam": None,
            "personal_info": None,
        },
        YESNO_OPENERS={"yes": "はい。", "no": "いいえ。", "unknown": "判定保留。"},
        CORRECT_PREFIX="正答です。",
    )


def test_template_reply_uses_sha1_choice_and_keeps_empty_phrase() -> None:
    module = _custom_templates(q_yesno=("一言A。", "一言B。", "一言C。"))
    row = {"id": "fake-case-7", "kind": "q_yesno", "answer": "yes"}
    digest = hashlib.sha1(row["id"].encode("utf-8")).digest()
    index = int.from_bytes(digest[:8], "big") % 3
    assert reply_trial.render_template_reply(row, PROBLEM, module) == "はい。" + module.TEMPLATES["q_yesno"][index]

    empty_module = _custom_templates(q_yesno=("",))
    assert reply_trial.render_template_reply(row, PROBLEM, empty_module) == "はい。"
    assert reply_trial.render_template_reply(
        {"id": "fake", "kind": "guess_correct"}, PROBLEM, module
    ) == "正答です。架空の開示文です。"
    assert reply_trial.render_template_reply(
        {"id": "fake", "kind": "spam"}, PROBLEM, module
    ) is None


def test_as_is_reuses_source_reply_exactly() -> None:
    source = {"id": "fake-case", "kind": "q_yesno", "answer": "no", "reply": "元の返信です。"}
    variant = {"name": "is", "type": "as_is"}
    reply, debug = reply_trial._reply_for_row(source, variant, PROBLEM, templates, None)
    assert reply == "元の返信です。"
    assert debug["error"] is None


def test_llm_fixed_request_contains_only_problem_text_when_truth_is_disabled(monkeypatch, tmp_path: Path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "reply.txt").write_text(
        "問題={problem_text}\n真相={truth}\n事実={fact_sheet}\n要点={core_points}\n"
        "種別={kind} 回答={answer} 未知={not_a_placeholder}",
        encoding="utf-8",
    )
    monkeypatch.setattr(reply_trial, "HERE", tmp_path)
    captured: dict[str, object] = {}

    def fake_post(req):
        captured["payload"] = json.loads(req.data.decode("utf-8"))
        return {
            "choices": [{"message": {"content": json.dumps({"reply": "架空の返信です。"})}}],
            "usage": {"prompt_tokens": 17, "completion_tokens": 9},
        }

    monkeypatch.setattr(reply_trial.pattern1_luna, "_post_with_retry", fake_post)
    source = {
        "id": "fake-llm-case", "kind": "q_yesno", "answer": "yes",
        "comment_text": "架空のコメントです。",
    }
    problem = Problem(
        no="N1",
        problem_text="架空の{truth}問題文です。",
        truth=PROBLEM.truth,
        fact_sheet=PROBLEM.fact_sheet,
        truth_points=PROBLEM.truth_points,
        reveal_text=PROBLEM.reveal_text,
        core_points=PROBLEM.core_points,
    )
    variant = {"prompt": "reply.txt", "with_truth": False, "model": "gpt-6-luna", "effort": "low", "max_tokens": 123}
    reply, debug = reply_trial._call_llm_reply(source, variant, problem, "unit-test-key")

    payload = captured["payload"]
    system = payload["messages"][0]["content"]
    user = payload["messages"][1]["content"]
    assert reply == "架空の返信です。"
    assert "架空の{truth}問題文です。" in system
    assert "秘密の真相マーカー" not in system
    assert "確定事実マーカー" not in system
    assert "要点マーカー" not in system
    assert "真相=" in system and "事実=" in system and "要点=" in system
    assert "{not_a_placeholder}" in system
    assert user == "架空のコメントです。"
    assert payload["response_format"]["json_schema"]["strict"] is True
    assert payload["response_format"]["json_schema"]["schema"]["required"] == ["reply"]
    assert payload["max_completion_tokens"] == 123
    assert debug["input_tokens"] == 17
    assert debug["output_tokens"] == 9


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        ("guess_correct", templates.CORRECT_PREFIX + PROBLEM.reveal_text),
        ("spam", None),
        ("troll", templates.pick("troll", "fake-rule-case")),
        ("abuse", templates.pick("abuse", "fake-rule-case")),
    ],
)
def test_llm_fixed_code_rules_bypass_llm(monkeypatch, kind: str, expected: str | None) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("code rule should bypass LLM")

    monkeypatch.setattr(reply_trial, "_call_llm_reply", forbidden)
    source = {"id": "fake-rule-case", "kind": kind, "answer": None, "reply": "ignored"}
    variant = {"name": "llm", "type": "llm_fixed"}
    reply, debug = reply_trial._reply_for_row(source, variant, PROBLEM, templates, "unused")
    assert reply == expected
    assert debug["error"] is None


def test_reply_metrics_m2_to_m6_and_length_metrics() -> None:
    rows = [
        {
            "id": "fake-q1", "no": "N1", "kind": "q_yesno", "answer": "yes",
            "expected_kind": "q_yesno", "comment_text": "架空コメント。",
            "reply": "はい。秘密の青空は核心に近い🔍",
        },
        {
            "id": "fake-q2", "no": "N1", "kind": "q_yesno", "answer": "yes",
            "expected_kind": "q_yesno", "comment_text": "架空コメント。",
            "reply": "はい。秘密の青空は核心に近い🔍",
        },
        {
            "id": "fake-q3", "no": "N1", "kind": "q_yesno", "answer": "no",
            "expected_kind": "q_yesno", "comment_text": "架空コメント。",
            "reply": "いいえ。これは二十字を超える長さを確認するための架空の一言です。",
        },
        {
            "id": "fake-wrong", "no": "N1", "kind": "guess_wrong", "answer": None,
            "expected_kind": "guess_wrong", "comment_text": "架空の推理です。",
            "reply": "着眼点はよいですが別の答えです。",
        },
        {
            "id": "fake-close", "no": "N1", "kind": "guess_close", "answer": None,
            "expected_kind": "guess_close", "comment_text": "架空の推理です。",
            "reply": "惜しい！もう少しです。",
        },
        {
            "id": "fake-close-near", "no": "N1", "kind": "guess_close", "answer": None,
            "expected_kind": "guess_close", "comment_text": "架空の推理です。",
            "reply": "鋭い推理ですが惜しいです。",
        },
        {
            "id": "fake-complaint", "no": "N1", "kind": "complaint", "answer": None,
            "expected_kind": "complaint", "comment_text": "架空の指摘です。",
            "reply": "確認します✨",
        },
        {
            "id": "fake-correct", "no": "N1", "kind": "guess_correct", "answer": None,
            "expected_kind": "guess_correct", "comment_text": "架空の正解です。",
            "reply": "正解です！架空の開示文✨",
        },
    ]
    variant = {"name": "metrics", "label": "架空案", "type": "template"}
    metrics = reply_trial.aggregate_variant(
        rows,
        variant,
        core={"N1": ["秘密"]},
        allow_words=["秘密"],
        opener_values=["はい。", "いいえ."],
    )

    assert metrics["M1_length"]["over_80_count"] == 0
    assert metrics["M1_length"]["q_yesno_one_liner_over_20_ids"] == ["fake-q3"]
    assert metrics["M2_answer_word"]["starts_count"] == 3
    assert metrics["M2_answer_word"]["contains_count"] == 3
    assert metrics["M3_variation"]["by_kind"]["q_yesno"]["distinct_replies"] == 2
    assert metrics["M3_variation"]["by_kind"]["q_yesno"]["over_50_percent"] is True
    assert metrics["M3_variation"]["q_yesno_one_liner"]["distinct_replies"] == 2
    assert metrics["M3_variation"]["q_yesno_one_liner_empty_count"] == 0
    assert metrics["M4_leak_candidates"]["core_by_no"]["N1"]["count"] == 2
    assert metrics["M4_leak_candidates"]["comment_missing_content_words_count"] == 4
    missing_items = metrics["M4_leak_candidates"]["comment_missing_content_words"]
    assert all("fake-correct" != item["id"] for item in missing_items)
    assert all("秘密" not in item["words"] for item in missing_items)
    assert metrics["M5_emoji"]["reply_count"] == 4
    assert metrics["M5_emoji"]["complaint_abuse_guess_correct_count"] == 2
    assert set(metrics["M5_emoji"]["types"]) == {"🔍", "✨"}
    assert metrics["M6_proximity"]["count"] == 4
    close_item = next(item for item in metrics["M6_proximity"]["items"] if item["kind"] == "guess_close")
    assert close_item["words"] == ["鋭い"]


def test_source_filters_error_rows_and_cache_read_write(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text(json.dumps({
        "version": 1,
        "results": {
            "fake-good::p1": {"id": "fake-good", "no": "N1", "comment_text": "架空", "expected_kind": "chat", "kind": "chat", "reply": "返信", "debug": {}},
            "fake-kind-error::p1": {"id": "fake-kind-error", "no": "N1", "comment_text": "架空", "expected_kind": "chat", "kind": "error", "reply": None, "debug": {}},
            "fake-reply-error::p2": {"id": "fake-reply-error", "no": "N1", "comment_text": "架空", "expected_kind": "chat", "kind": "chat", "reply": None, "debug": {"reply_error": "fake error"}},
        },
    }), encoding="utf-8")
    loaded, excluded = reply_trial.load_source_rows(source)
    assert list(loaded["p1"]) == ["fake-good"]
    assert excluded["p1"]["kind_error"] == 1
    assert excluded["p2"]["reply_error"] == 1

    cache_path = tmp_path / "work" / "reply_results.json"
    cached = {"fake-good::1a": {"id": "fake-good", "reply": "架空返信"}}
    reply_trial._save_cache(cached, cache_path)
    assert reply_trial._load_cache(cache_path) == cached


def test_llm_cost_metrics_use_only_requests() -> None:
    rows = [
        {
            "id": "fake-request", "no": "N1", "kind": "q_yesno", "answer": "yes",
            "comment_text": "架空の質問です。", "reply": "はい。",
            "debug": {"input_tokens": 10, "output_tokens": 20, "latency_s": 0.25, "error": None},
        },
        {
            "id": "fake-rule", "no": "N1", "kind": "guess_correct", "answer": None,
            "comment_text": "架空の正解です。", "reply": "正解です！架空の開示文です。",
            "debug": {"input_tokens": 900, "output_tokens": 800, "latency_s": 8.0, "error": None},
        },
    ]
    variant = {"name": "llm", "type": "llm_fixed", "model": "gpt-6-luna"}
    metrics = reply_trial.aggregate_variant(rows, variant, core={}, allow_words=[])["M7_llm"]
    assert metrics["request_count"] == 1
    assert metrics["input_tokens"] == 10
    assert metrics["output_tokens"] == 20
    assert metrics["latency_s"] == {"median": 0.25, "p95": 0.25, "max": 0.25}
    assert metrics["cost_usd"] == pytest.approx(0.000011)


def test_variant_definition_starts_with_baseline_variants() -> None:
    variants = reply_trial.load_variants(reply_trial.DEFAULT_VARIANTS)
    assert [variant["name"] for variant in variants][:3] == ["1a", "2a", "1c"]
    assert [variant["type"] for variant in variants][:3] == ["as_is", "as_is", "template"]


@pytest.mark.parametrize(("with_truth", "calls_llm"), [(True, True), (False, False)])
def test_llm_correct_lets_llm_write_reveal_only_with_truth(monkeypatch, with_truth: bool, calls_llm: bool) -> None:
    monkeypatch.setattr(reply_trial, "_call_llm_reply", lambda *args, **kwargs: ("LLM の開示", {"error": None}))
    source = {"id": "fake-correct-llm", "kind": "guess_correct", "answer": None, "reply": "ignored"}
    variant = {"name": "llm", "type": "llm_fixed", "llm_correct": True, "with_truth": with_truth}
    reply, _ = reply_trial._reply_for_row(source, variant, PROBLEM, templates, "unused")
    expected = "LLM の開示" if calls_llm else templates.CORRECT_PREFIX + PROBLEM.reveal_text
    assert reply == expected
