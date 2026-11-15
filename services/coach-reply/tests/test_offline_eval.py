"""Only pure evaluation aggregation is tested; no evaluation API calls."""

from __future__ import annotations

import pytest

import json

from app import reply_rule
from tools.offline_eval import (
    aggregate_results, main, print_summary, total_usage, would_reply, write_review,
)


def row(label, verdict="correct", confidence="high", **overrides):
    return {
        "media_id": "m", "comment_id": label, "comment_text": "コメント本文", "answer_text": "答え",
        "label": label, "prediction": {"verdict": verdict, "confidence": confidence, "reason": "理由"},
        **overrides,
    }


def test_table_false_replies_recall_and_failures(capsys):
    rows = [
        row("correct"), row("correct", confidence="low"), row("correct", prediction=None),
        row("alt"), row("wrong"), row("wrong", "wrong"), row("other"),
        row("other", "unsure"), row("unanswered"),
    ]
    summary = aggregate_results(rows, "high")
    assert summary["table"]["correct"] == {"reply": 1, "no_reply": 2}
    assert summary["table"]["wrong"] == {"reply": 1, "no_reply": 1}
    assert summary["table"]["alt"]["reply"] == 1
    assert summary["table"]["unanswered"]["reply"] == 1
    assert summary["false_reply_count"] == 2
    assert {r["comment_id"] for r in summary["false_replies"]} == {"wrong", "other"}
    assert all(r["comment_text"] == "コメント本文" and r["answer_text"] == "答え" and r["reason"] == "理由"
               for r in summary["false_replies"])
    assert summary["correct_recall"] == pytest.approx(1 / 3)
    assert summary["judge_failures"] == 1
    print_summary(summary)
    output = capsys.readouterr().out
    assert "誤返信(wrong・other への返す): 2" in output and "1/3 (33.3%)" in output and "判定の失敗件数: 1" in output


def test_no_correct_labels_uses_undefined_recall_instead_of_dividing_by_zero():
    summary = aggregate_results([row("wrong", "wrong")])
    assert summary["correct_recall"] is None and summary["false_reply_count"] == 0
    assert aggregate_results([])["judge_failures"] == 0


def test_unknown_label_is_an_input_error():
    with pytest.raises(ValueError):
        aggregate_results([row("unexpected")])


@pytest.mark.parametrize("verdict", ["correct", "alt", "wrong", "unsure"])
@pytest.mark.parametrize("confidence", ["high", "low"])
def test_default_would_reply_is_the_online_gate(verdict, confidence):
    prediction = {"verdict": verdict, "confidence": confidence, "reason": "r"}
    assert would_reply(prediction) is reply_rule.should_reply(prediction)
    assert would_reply(prediction) is (verdict == "correct")
    assert would_reply(prediction) is would_reply(prediction, "any")
    assert not would_reply(None)


def test_reply_rules_high_and_any_for_comparison():
    assert would_reply({"verdict": "correct", "confidence": "high"}, "high")
    assert not would_reply({"verdict": "correct", "confidence": "low"}, "high")
    assert would_reply({"verdict": "correct", "confidence": "low"}, "any")
    assert not would_reply({"verdict": "alt", "confidence": "high"}, "any")
    assert not would_reply(None, "any")
    with pytest.raises(ValueError):
        would_reply({"verdict": "correct", "confidence": "high"}, "loose")


def test_any_rule_counts_low_confidence_and_review_list_includes_unanswered():
    rows = [row("correct", confidence="low"), row("unanswered", confidence="low"), row("wrong")]
    high, any_ = aggregate_results(rows, "high"), aggregate_results(rows)
    assert high["correct_replied"] == 0 and any_["correct_replied"] == 1
    assert [r["label"] for r in high["review_replies"]] == ["wrong"]
    assert [r["label"] for r in any_["review_replies"]] == ["unanswered", "wrong"]
    assert any_["false_reply_count"] == 1


def test_total_usage_sums_tokens_and_prices_haiku():
    totals = total_usage([{"input_tokens": 1_000_000, "output_tokens": 0},
                          {"output_tokens": 1_000_000, "cache_read_input_tokens": 1_000_000}])
    assert totals["requests"] == 2 and totals["output_tokens"] == 1_000_000
    assert totals["cost_usd"] == pytest.approx(0.10 + 0.50 + 0.01)


def test_review_file_and_summary_from_saved_results(tmp_path, capsys):
    rows = [row("other", confidence="low", question_text="問題"), row("correct"), row("alt")]
    out = tmp_path / "review.md"
    assert write_review(out, rows, "xhigh") == 1
    text = out.read_text(encoding="utf-8")
    assert "effort xhigh" in text and "ラベル other（1 件）" in text and "自信低も返すときだけ" in text
    assert "コメント: コメント本文" in text and "用意した答え: 答え" in text
    saved = tmp_path / "result.jsonl"
    saved.write_text("\n".join(json.dumps(dict(r, effort="high"), ensure_ascii=False) for r in rows),
                     encoding="utf-8")
    main(["--summary-from", str(saved), "--review-out", str(tmp_path / "again.md")])
    output = capsys.readouterr().out
    assert "返信の条件: high" in output and "返信の条件: any" in output
    assert (tmp_path / "again.md").exists()
