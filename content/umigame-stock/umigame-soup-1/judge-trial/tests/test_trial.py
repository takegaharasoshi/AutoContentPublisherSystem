from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import pattern1_luna
import pattern2_jev
import templates
from judge_contract import KINDS, JudgeResult, Problem
from run_trial import aggregate_results


PROBLEM = Problem(
    no="U01",
    problem_text="男はなぜ喜んだ？",
    truth="真相です。",
    fact_sheet=["確定事実です。"],
    truth_points=["男は医師から良い知らせを聞いた。", "影は病気の跡を指す。"],
    reveal_text="男は検査結果が良くなり、医師に感謝した。",
)


def test_templates_have_rotations_and_are_deterministic() -> None:
    for kind in KINDS:
        options = templates.TEMPLATES[kind]
        if options is not None:
            assert len(options) >= 3
            assert all(len(option) <= 80 for option in options)
            assert all(not any(ord(char) > 0x1F000 for char in option) for option in options)
        assert templates.pick(kind, "same-id") == templates.pick(kind, "same-id")
    assert templates.TEMPLATES["spam"] is None
    assert templates.TEMPLATES["personal_info"] is None
    assert len(templates.TEMPLATES["q_yesno"]) >= 6
    assert all(len(line) <= 20 for line in templates.TEMPLATES["q_yesno"])


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("詳細はこちら https://example.com", "spam"),
        ("✨👏🎉", "emoji_only"),
    ],
)
def test_pattern2_local_rules_do_not_call_jev(monkeypatch, text: str, expected: str) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("規則段では Jev を呼ばない")

    monkeypatch.setattr(pattern2_jev, "_jev_request", forbidden)
    result = pattern2_jev.judge("C-1", text, PROBLEM, api_key="test")
    assert result.kind == expected
    assert result.reply is None if expected == "spam" else result.reply is not None


def _mock_answers(*stages):
    iterator = iter(stages)

    def request(*args, **kwargs):
        return {"answers": next(iterator), "input_tokens": 12}

    return request


def test_pattern2_b_threshold_close_and_correct(monkeypatch) -> None:
    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "question_or_guess"}},
            {"qg": {"choice": "guess", "probabilities": {"guess": 0.98, "question": 0.02}}},
            {"point_0": {"noul": 0.7}, "point_1": {"noul": 0.49}},
        ),
    )
    close = pattern2_jev.judge("C-2", "解決の推理", PROBLEM, api_key="test", t_point=0.5)
    assert close.kind == "guess_close"
    assert close.debug["probabilities"]["B"] == {"point_0": 0.7, "point_1": 0.49}

    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "question_or_guess"}},
            {"qg": {"choice": "guess"}},
            {"point_0": {"noul": 0.9}, "point_1": {"noul": 0.6}},
        ),
    )
    correct = pattern2_jev.judge("C-3", "全て言い当てた推理", PROBLEM, api_key="test")
    assert correct.kind == "guess_correct"
    assert correct.reply.startswith("正解です！")
    assert correct.debug["input_tokens"] == 36  # 段 A1 + 段 A1b + 段 B（要点をまとめて 1 回）


def test_pattern2_c_and_d_thresholds(monkeypatch) -> None:
    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "question_or_guess"}},
            {"qg": {"choice": "question"}},
            {"kind": {"choice": "q_yesno"}},
            {"point_0": {"noul": 0.2}, "point_1": {"noul": 0.1}},
            {"quality": {"noul": 0.19}},
        ),
    )
    open_question = pattern2_jev.judge("C-4", "なぜ？", PROBLEM, api_key="test", t_quality=0.2)
    assert open_question.kind == "q_open"

    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "question_or_guess"}},
            {"qg": {"choice": "question"}},
            {"kind": {"choice": "q_yesno"}},
            {"point_0": {"noul": 0.2}, "point_1": {"noul": 0.1}},
            {"quality": {"noul": 0.8}},
            {"answer": {"choice": "yes", "probabilities": {"yes": 0.54, "no": 0.4, "irrelevant": 0.06}}},
        ),
    )
    unknown = pattern2_jev.judge("C-5", "男は喜びましたか？", PROBLEM, api_key="test", t_answer=0.55)
    assert unknown.kind == "q_yesno"
    assert unknown.answer == "unknown"
    assert unknown.reply.startswith("それは問題の答えに関わりません。")

    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "question_or_guess"}},
            {"qg": {"choice": "question"}},
            {"kind": {"choice": "q_yesno"}},
            {"point_0": {"noul": 0.2}, "point_1": {"noul": 0.1}},
            {"quality": {"noul": 0.8}},
            {"answer": {"choice": "yes", "probabilities": {"yes": 0.7, "no": 0.2, "irrelevant": 0.1}}},
        ),
    )
    yes = pattern2_jev.judge("C-6", "男は喜びましたか？", PROBLEM, api_key="test")
    assert yes.answer == "yes"
    assert yes.reply.startswith("はい。")


class _FakeResponse:
    def __init__(self, body: dict):
        self.body = json.dumps(body).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


def _openai_response(kind: str, *, finish_reason: str = "stop"):
    content = json.dumps({"kind": kind, "answer": None, "reply": "LLM の返信"}, ensure_ascii=False)
    return {
        "choices": [{"finish_reason": finish_reason, "message": {"content": content}}],
        "usage": {"prompt_tokens": 20, "completion_tokens": 30, "completion_tokens_details": {"reasoning_tokens": 11}},
    }


def test_pattern1_forces_no_reply_and_abuse_template(monkeypatch) -> None:
    monkeypatch.setattr(pattern1_luna.request, "urlopen", lambda *args, **kwargs: _FakeResponse(_openai_response("spam")))
    spam = pattern1_luna.judge("C-7", "宣伝", PROBLEM, api_key="test")
    assert spam.kind == "spam" and spam.reply is None

    monkeypatch.setattr(pattern1_luna.request, "urlopen", lambda *args, **kwargs: _FakeResponse(_openai_response("abuse")))
    abuse = pattern1_luna.judge("C-8", "攻撃", PROBLEM, api_key="test")
    assert abuse.kind == "abuse"
    assert abuse.reply == templates.pick("abuse", "C-8")


def test_pattern1_length_becomes_error(monkeypatch) -> None:
    monkeypatch.setattr(
        pattern1_luna.request,
        "urlopen",
        lambda *args, **kwargs: _FakeResponse(_openai_response("impression", finish_reason="length")),
    )
    result = pattern1_luna.judge("C-9", "面白い", PROBLEM, api_key="test")
    assert result.kind == "error"
    assert result.reply is None
    assert result.debug["finish_reason"] == "length"


def test_aggregate_p3_p4_p2_p5_metrics() -> None:
    rows = [
        {"id": "1", "no": "U01", "method": "p1", "expected_kind": "q_yesno", "expected_answer": "yes", "kind": "q_yesno", "answer": "no", "reply": "いいえ。", "comment_text": "a", "debug": {}},
        {"id": "2", "no": "U01", "method": "p1", "expected_kind": "q_yesno", "expected_answer": "no", "kind": "q_yesno", "answer": "irrelevant", "reply": "関係ありません。", "comment_text": "b", "debug": {}},
        {"id": "3", "no": "U01", "method": "p1", "expected_kind": "q_yesno", "expected_answer": "irrelevant", "kind": "q_yesno", "answer": "unknown", "reply": "それは問題の答えに関わりません。", "comment_text": "c", "debug": {}},
        {"id": "4", "no": "U01", "method": "p1", "expected_kind": "impression", "expected_answer": None, "kind": "impression", "answer": None, "reply": "正解です！（誤宣言）", "comment_text": "d", "debug": {}},
        {"id": "5", "no": "U01", "method": "p1", "expected_kind": "guess_correct", "expected_answer": None, "kind": "guess_correct", "answer": None, "reply": "正解です！開示。", "comment_text": "e", "debug": {}},
        {"id": "6", "no": "U01", "method": "p1", "expected_kind": "guess_correct", "expected_answer": None, "kind": "guess_correct", "answer": None, "reply": "少し惜しい。", "comment_text": "f", "debug": {}},
    ]
    metrics = aggregate_results(rows, core={})
    assert metrics["q_yesno"]["accuracy"] == {"correct": 0, "total": 3, "rate": 0.0}
    assert metrics["q_yesno"]["p3_yes_no_confusions"]["correct"] == 1
    assert metrics["q_yesno"]["p4_no_irrelevant_unknown_drift"]["correct"] == 2
    assert metrics["p2_wrong_correct_declarations"] == 1
    assert metrics["p5_correct_declaration_rate"]["correct"] == 1
    assert metrics["p5_correct_declaration_rate"]["total"] == 2


def test_pattern2_major_then_detailed_kind(monkeypatch) -> None:
    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "reaction", "probabilities": {"reaction": 0.9}}},
            {"kind": {"choice": "complaint", "probabilities": {"complaint": 0.7}}},
        ),
    )
    result = pattern2_jev.judge("C-7", "つまらない問題", PROBLEM, api_key="test")
    assert result.kind == "complaint"
    assert result.debug["major"] == "reaction"
    assert result.reply

    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers({"major": {"choice": "other"}}),
    )
    foreign = pattern2_jev.judge("C-8", "太难了", PROBLEM, api_key="test")
    assert foreign.kind == "foreign"
    assert foreign.debug["calls"] == 1


def test_pattern2_latin_only_goes_to_jev(monkeypatch) -> None:
    """1 語だけの英字の羅列は段 0 で外国語と決めず、段 A1 に任せる（試行 5）。"""
    monkeypatch.setattr(pattern2_jev, "_jev_request", _mock_answers({"major": {"choice": "other"}}))
    result = pattern2_jev.judge("C-9", "QWERTYZZZ", PROBLEM, api_key="test")
    assert result.kind == "foreign"
    assert result.debug["calls"] == 1


def test_pattern2_multiword_english_is_foreign_without_jev(monkeypatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("規則段では Jev を呼ばない")

    monkeypatch.setattr(pattern2_jev, "_jev_request", forbidden)
    assert pattern2_jev.judge("C-10", "Please explain this puzzle", PROBLEM, api_key="test").kind == "foreign"


def test_pattern2_recheck_turns_open_into_yesno(monkeypatch) -> None:
    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "question_or_guess"}},
            {"qg": {"choice": "question"}},
            {"kind": {"choice": "q_open"}},
            {"recheck": {"noul": 0.8}},
            {"point_0": {"noul": 0.1}, "point_1": {"noul": 0.1}},
            {"quality": {"noul": 0.9}},
            {"answer": {"choice": "no", "probabilities": {"yes": 0.1, "no": 0.85, "irrelevant": 0.05}}},
        ),
    )
    result = pattern2_jev.judge("C-11", "その子は彼に会ったことがある？", PROBLEM, api_key="test")
    assert result.kind == "q_yesno" and result.answer == "no"
    assert result.debug["probabilities"]["A3"] == 0.8


def test_pattern2_demonstrative_yesno_goes_to_recheck(monkeypatch) -> None:
    """A2 が ① を選んでも、指示語を含む質問は段 A3 で確かめ直し、主語が決まらなければ ③（試行 6）。"""
    monkeypatch.setattr(
        pattern2_jev,
        "_jev_request",
        _mock_answers(
            {"major": {"choice": "question_or_guess"}},
            {"qg": {"choice": "question"}},
            {"kind": {"choice": "q_yesno"}},
            {"recheck": {"noul": 0.2}},
        ),
    )
    result = pattern2_jev.judge("C-12", "それはまだ持ってるの？", PROBLEM, api_key="test")
    assert result.kind == "q_open"
