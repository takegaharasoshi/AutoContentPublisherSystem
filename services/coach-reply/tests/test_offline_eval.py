"""Only pure evaluation aggregation is tested; no evaluation API calls."""

from __future__ import annotations

import pytest

from tools.offline_eval import aggregate_results, print_summary


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
    summary = aggregate_results(rows)
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
    assert "誤返信: 2" in output and "1/3 (33.3%)" in output and "判定の失敗件数: 1" in output


def test_no_correct_labels_uses_undefined_recall_instead_of_dividing_by_zero():
    summary = aggregate_results([row("wrong", "wrong")])
    assert summary["correct_recall"] is None and summary["false_reply_count"] == 0
    assert aggregate_results([])["judge_failures"] == 0


def test_unknown_label_is_an_input_error():
    with pytest.raises(ValueError):
        aggregate_results([row("unexpected")])
