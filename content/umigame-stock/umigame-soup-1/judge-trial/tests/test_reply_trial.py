from __future__ import annotations

import hashlib
import io
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
        "開示={reveal_text}\nスタイル={style}\n"
        "種別={kind} 回答={answer} 未知={not_a_placeholder}",
        encoding="utf-8",
    )
    (prompt_dir / "style.txt").write_text("架空の共有スタイルです。", encoding="utf-8")
    monkeypatch.setattr(reply_trial, "HERE", tmp_path)
    captured: dict[str, object] = {}

    def fake_post(req):
        captured["payload"] = json.loads(req.data.decode("utf-8"))
        return {
            "choices": [{"message": {"content": json.dumps({"reply": "架空の返信です。"})}}],
            "usage": {"prompt_tokens": 17, "completion_tokens": 9},
        }

    monkeypatch.setattr(reply_trial, "_post_json_with_retry", fake_post)
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
    variant = {
        "prompt": "reply.txt", "style": "style.txt", "with_truth": False,
        "model": "gpt-6-luna", "effort": "low", "max_tokens": 123,
    }
    reply, debug = reply_trial._call_llm_reply(source, variant, problem, "unit-test-key")

    payload = captured["payload"]
    system = payload["messages"][0]["content"]
    user = payload["messages"][1]["content"]
    assert reply == "架空の返信です。"
    assert "架空の{truth}問題文です。" in system
    assert "秘密の真相マーカー" not in system
    assert "確定事実マーカー" not in system
    assert "要点マーカー" not in system
    assert "開示=" in system and "架空の開示文です。" not in system
    assert "架空の共有スタイルです。" in system
    assert "真相=" in system and "事実=" in system and "要点=" in system
    assert "{not_a_placeholder}" in system
    assert user == "架空のコメントです。"
    assert payload["response_format"]["json_schema"]["strict"] is True
    assert payload["response_format"]["json_schema"]["schema"]["required"] == ["reply"]
    assert payload["max_completion_tokens"] == 123
    assert debug["input_tokens"] == 17
    assert debug["output_tokens"] == 9


def test_openrouter_request_merges_extra_body_and_cleans_text(monkeypatch, tmp_path: Path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "router.txt").write_text("system {problem_text}", encoding="utf-8")
    monkeypatch.setattr(reply_trial, "HERE", tmp_path)
    captured: dict[str, object] = {}

    def fake_post(req):
        captured["request"] = req
        return {
            "choices": [{"message": {"content": "\nreply: 「Router の返信」\n"}}],
            "usage": {"prompt_tokens": 21, "completion_tokens": 8},
        }

    monkeypatch.setattr(reply_trial, "_post_json_with_retry", fake_post)
    variant = {
        "provider": "openrouter", "output": "text", "prompt": "router.txt",
        "model": "qwen/qwen3.5-9b", "max_tokens": 321,
        "extra_body": {"reasoning": {"enabled": False}},
    }
    row = {"id": "fake-router", "kind": "chat", "answer": None, "comment_text": "架空の入力"}
    reply, debug = reply_trial._call_llm_reply(row, variant, PROBLEM, "router-test-key")

    req = captured["request"]
    body = json.loads(req.data.decode("utf-8"))
    assert req.full_url == reply_trial.OPENROUTER_CHAT_COMPLETIONS_URL
    assert req.get_header("Authorization") == "Bearer router-test-key"
    assert body["model"] == "qwen/qwen3.5-9b"
    assert body["max_tokens"] == 321
    assert body["reasoning"] == {"enabled": False}
    assert body["messages"][0]["content"].endswith("返信文だけをプレーンテキストで出力してください。")
    assert body["messages"][1] == {"role": "user", "content": "架空の入力"}
    assert reply == "Router の返信"
    assert debug["input_tokens"] == 21
    assert debug["thought_tokens"] == 0


def test_gemini_request_filters_thought_parts_and_records_usage(monkeypatch, tmp_path: Path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "gemini.txt").write_text("問題={problem_text} 開示={reveal_text} style={style}", encoding="utf-8")
    (prompt_dir / "style.txt").write_text("共通スタイル", encoding="utf-8")
    monkeypatch.setattr(reply_trial, "HERE", tmp_path)
    captured: dict[str, object] = {}

    def fake_post(req):
        captured["request"] = req
        return {
            "candidates": [{"content": {"parts": [
                {"text": "考え中の内部テキスト", "thought": True},
                {"text": "Gemini "},
                {"text": "の返信"},
            ]}}],
            "usageMetadata": {
                "promptTokenCount": 11,
                "candidatesTokenCount": 7,
                "thoughtsTokenCount": 3,
            },
        }

    monkeypatch.setattr(reply_trial, "_post_json_with_retry", fake_post)
    variant = {
        "provider": "gemini", "output": "text", "prompt": "gemini.txt", "style": "style.txt",
        "model": "gemma-4-26b-a4b-it", "max_tokens": 456,
        "extra_body": {"safetySettings": [{"category": "TEST", "threshold": "BLOCK_NONE"}]},
    }
    row = {"id": "fake-gemini", "kind": "chat", "answer": None, "comment_text": "架空の質問"}
    reply, debug = reply_trial._call_llm_reply(row, variant, PROBLEM, "gemini-test-key")

    req = captured["request"]
    body = json.loads(req.data.decode("utf-8"))
    assert "/models/gemma-4-26b-a4b-it:generateContent" in req.full_url
    assert req.get_header("X-goog-api-key") == "gemini-test-key"
    assert body["systemInstruction"]["parts"][0]["text"] == (
        "問題=架空の問題文です。 開示=架空の開示文です。 style=共通スタイル"
        "\n\n返信文だけをプレーンテキストで出力してください。"
    )
    assert body["contents"] == [{"role": "user", "parts": [{"text": "架空の質問"}]}]
    assert body["generationConfig"]["maxOutputTokens"] == 456
    assert body["safetySettings"][0]["threshold"] == "BLOCK_NONE"
    assert reply == "Gemini の返信"
    assert debug["input_tokens"] == 11
    assert debug["output_tokens"] == 7
    assert debug["thought_tokens"] == 3


def test_clean_text_reply_discards_think_prefix_and_labels() -> None:
    assert reply_trial._clean_text_reply("分析は表示しない</think> 返信: \"完成した返信\" ") == "完成した返信"


def test_retry_uses_exponential_backoff_for_429_and_5xx(monkeypatch) -> None:
    sleeps: list[float] = []
    attempts = 0

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b'{"ok": true}'

    def fake_urlopen(*args, **kwargs):
        nonlocal attempts
        attempts += 1
        if attempts <= 2:
            status = 429 if attempts == 1 else 503
            raise reply_trial.error.HTTPError("https://example.invalid", status, "retry", None, io.BytesIO())
        return FakeResponse()

    monkeypatch.setattr(reply_trial.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(reply_trial.time, "sleep", sleeps.append)
    req = reply_trial.request.Request("https://example.invalid", data=b"{}", method="POST")
    assert reply_trial._post_json_with_retry(req) == {"ok": True}
    assert attempts == 3
    assert sleeps == [2.0, 4.0]


def test_retry_exhaustion_becomes_error_and_variant_limit_caps_workers(monkeypatch, tmp_path: Path) -> None:
    attempts = 0
    sleeps: list[float] = []
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "retry.txt").write_text("返信を書いてください。", encoding="utf-8")
    monkeypatch.setattr(reply_trial, "HERE", tmp_path)

    def always_busy(*args, **kwargs):
        nonlocal attempts
        attempts += 1
        raise reply_trial.error.HTTPError("https://example.invalid", 503, "busy", None, io.BytesIO())

    monkeypatch.setattr(reply_trial.request, "urlopen", always_busy)
    monkeypatch.setattr(reply_trial.time, "sleep", sleeps.append)
    row = {"id": "fake-retry", "kind": "chat", "comment_text": "架空のコメント"}
    variant = {"provider": "openrouter", "output": "text", "prompt": "retry.txt"}
    reply, debug = reply_trial._call_llm_reply(row, variant, PROBLEM, "retry-test-key")
    assert reply is None
    assert "503" in debug["error"]
    assert attempts == 6
    assert sleeps == [2.0, 4.0, 8.0, 16.0, 32.0]
    assert reply_trial._variant_worker_count(3, {"max_workers": 1}) == 1
    assert reply_trial._variant_worker_count(3, {}) == 3


def test_provider_key_loading_and_missing_key_error(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "router-env-key")
    assert reply_trial._load_provider_api_key("openrouter") == "router-env-key"
    monkeypatch.delenv("OPENROUTER_API_KEY")
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        reply_trial._load_provider_api_key("openrouter")

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    key_path = tmp_path / ".config" / "gemini" / "api_key"
    key_path.parent.mkdir(parents=True)
    key_path.write_text("gemini-file-key\n", encoding="utf-8")
    assert reply_trial._load_provider_api_key("gemini") == "gemini-file-key"

    llm_variant = {"type": "llm_fixed", "provider": "openrouter"}
    row = {"id": "fake-missing-key", "kind": "chat", "comment_text": "架空", "reply": "old"}
    reply, debug = reply_trial._reply_for_row(row, llm_variant, PROBLEM, templates, None, "missing key")
    assert reply is None
    assert debug["error"] == "missing key"


def test_missing_provider_key_records_rows_and_runs_other_variants(monkeypatch, tmp_path: Path) -> None:
    source_path = tmp_path / "source.json"
    source_path.write_text(json.dumps({
        "version": 1,
        "results": {
            "fake-source::p1": {
                "id": "fake-source", "no": "N1", "comment_text": "架空のコメント",
                "problem_text": "架空の問題", "expected_kind": "chat", "kind": "chat",
                "answer": None, "reply": "元の返信", "debug": {},
            },
        },
    }), encoding="utf-8")
    variants_path = tmp_path / "variants.json"
    variants_path.write_text(json.dumps([
        {
            "name": "router", "source_method": "p1", "type": "llm_fixed",
            "provider": "openrouter", "prompt": "reply.txt", "with_truth": False,
            "max_workers": 1,
        },
        {"name": "copy", "source_method": "p1", "type": "as_is"},
    ]), encoding="utf-8")
    work_dir = tmp_path / "work"
    monkeypatch.setattr(reply_trial, "WORK_DIR", work_dir)
    monkeypatch.setattr(reply_trial, "RESULTS_PATH", work_dir / "reply_results.json")
    monkeypatch.setattr(reply_trial, "REPORT_PATH", work_dir / "reply_report.md")
    monkeypatch.setattr(reply_trial, "METRICS_PATH", work_dir / "reply_metrics.json")
    monkeypatch.setattr(reply_trial, "COMPARE_PATH", work_dir / "reply_compare.json")
    monkeypatch.setattr(reply_trial, "load_problem", lambda no: PROBLEM)
    monkeypatch.setattr(reply_trial.run_trial, "load_core_words", lambda: {})

    def missing_key(provider: str) -> str:
        raise RuntimeError("router key absent")

    monkeypatch.setattr(reply_trial, "_load_provider_api_key", missing_key)
    assert reply_trial.main([
        "--source", str(source_path), "--variants-file", str(variants_path), "--workers", "3",
    ]) == 0

    cached = reply_trial._load_cache(work_dir / "reply_results.json")
    assert cached["fake-source::router"]["reply"] is None
    assert cached["fake-source::router"]["debug"]["error"] == "router key absent"
    assert cached["fake-source::copy"]["reply"] == "元の返信"
    metrics = json.loads((work_dir / "reply_metrics.json").read_text(encoding="utf-8"))["variants"]
    assert metrics["router"]["error_count"] == 1
    assert metrics["copy"]["error_count"] == 0


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


def test_custom_templates_module_controls_template_and_llm_code_rules() -> None:
    module = _custom_templates()
    picked: list[tuple[str, str]] = []

    def custom_pick(kind: str, comment_id: str) -> str:
        picked.append((kind, comment_id))
        return f"差し替え定型 {kind} {comment_id}"

    module.pick = custom_pick
    template_row = {"id": "fake-custom-template", "kind": "q_multi", "answer": None}
    template_reply, _ = reply_trial._reply_for_row(
        template_row, {"type": "template"}, PROBLEM, module, None
    )
    assert template_reply == "質問を分けてください。"

    troll_row = {"id": "fake-custom-troll", "kind": "troll", "answer": None}
    troll_reply, _ = reply_trial._reply_for_row(
        troll_row, {"type": "llm_fixed"}, PROBLEM, module, None
    )
    correct_row = {"id": "fake-custom-correct", "kind": "guess_correct", "answer": None}
    correct_reply, _ = reply_trial._reply_for_row(
        correct_row, {"type": "llm_fixed"}, PROBLEM, module, None
    )
    assert troll_reply == "差し替え定型 troll fake-custom-troll"
    assert correct_reply == "正答です。架空の開示文です。"
    assert picked == [("troll", "fake-custom-troll")]


def test_reply_metrics_m2_to_m6_and_length_metrics() -> None:
    rows = [
        {
            "id": "fake-q1", "no": "N1", "kind": "q_yesno", "answer": "yes",
            "expected_kind": "q_yesno", "comment_text": "架空コメント。",
            "reply": "はい。秘密の青空は核心に近い🤔",
        },
        {
            "id": "fake-q2", "no": "N1", "kind": "q_yesno", "answer": "yes",
            "expected_kind": "q_yesno", "comment_text": "架空コメント。",
            "reply": "はい。秘密の青空は核心に近い🤔",
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
            "reply": "確認します✨✨",
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
    assert set(metrics["M5_emoji"]["types"]) == {"🤔", "✨"}
    assert metrics["M5_emoji"]["unlisted_reply_count"] == 2
    assert metrics["M5_emoji"]["unlisted_ids"] == ["fake-complaint", "fake-correct"]
    assert metrics["M5_emoji"]["multiple_emoji_reply_count"] == 1
    assert metrics["M5_emoji"]["multiple_emoji_ids"] == ["fake-complaint"]
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


@pytest.mark.parametrize(
    ("model", "expected_cost"),
    [
        ("qwen/qwen3.5-9b", 0.00000445),
        ("qwen/qwen3.5-flash-02-23", 0.00000663),
        ("gemma-4-26b-a4b-it", 0.0),
    ],
)
def test_llm_cost_metrics_use_only_requests_and_count_thought_as_output(model: str, expected_cost: float) -> None:
    rows = [
        {
            "id": "fake-request", "no": "N1", "kind": "q_yesno", "answer": "yes",
            "comment_text": "架空の質問です。", "reply": "はい。",
            "debug": {"input_tokens": 10, "output_tokens": 20, "thought_tokens": 3, "latency_s": 0.25, "error": None},
        },
        {
            "id": "fake-rule", "no": "N1", "kind": "guess_correct", "answer": None,
            "comment_text": "架空の正解です。", "reply": "正解です！架空の開示文です。",
            "debug": {"input_tokens": 900, "output_tokens": 800, "latency_s": 8.0, "error": None},
        },
    ]
    variant = {"name": "llm", "type": "llm_fixed", "model": model}
    metrics = reply_trial.aggregate_variant(rows, variant, core={}, allow_words=[])["M7_llm"]
    assert metrics["request_count"] == 1
    assert metrics["input_tokens"] == 10
    assert metrics["output_tokens"] == 20
    assert metrics["thought_tokens"] == 3
    assert metrics["latency_s"] == {"median": 0.25, "p95": 0.25, "max": 0.25}
    assert metrics["cost_usd"] == pytest.approx(expected_cost)


def test_variant_provider_and_output_defaults(tmp_path: Path) -> None:
    path = tmp_path / "variants.json"
    path.write_text(json.dumps([
        {"name": "oa", "source_method": "p1", "type": "llm_fixed", "prompt": "prompt.txt"},
        {"name": "or", "source_method": "p1", "type": "llm_fixed", "provider": "openrouter", "prompt": "prompt.txt"},
        {"name": "gm", "source_method": "p2", "type": "llm_fixed", "provider": "gemini", "prompt": "prompt.txt"},
    ]), encoding="utf-8")
    variants = {variant["name"]: variant for variant in reply_trial.load_variants(path)}
    assert variants["oa"]["provider"] == "openai"
    assert variants["oa"]["output"] == "json"
    assert variants["or"]["output"] == "text"
    assert variants["gm"]["output"] == "text"


@pytest.mark.parametrize(("with_truth", "calls_llm"), [(True, True), (False, False)])
def test_llm_correct_lets_llm_write_reveal_only_with_truth(monkeypatch, with_truth: bool, calls_llm: bool) -> None:
    monkeypatch.setattr(reply_trial, "_call_llm_reply", lambda *args, **kwargs: ("LLM の開示", {"error": None}))
    source = {"id": "fake-correct-llm", "kind": "guess_correct", "answer": None, "reply": "ignored"}
    variant = {"name": "llm", "type": "llm_fixed", "llm_correct": True, "with_truth": with_truth}
    reply, _ = reply_trial._reply_for_row(source, variant, PROBLEM, templates, "unused")
    expected = "LLM の開示" if calls_llm else templates.CORRECT_PREFIX + PROBLEM.reveal_text
    assert reply == expected


def test_pick_slot_is_deterministic_and_rendered() -> None:
    variant = {"slots": ["A", "B", "C"]}
    first = reply_trial.pick_slot(variant, "fake-slot-1")
    assert first == reply_trial.pick_slot(variant, "fake-slot-1")
    assert first in {"A", "B", "C"}
    assert reply_trial.pick_slot({}, "fake-slot-1") == ""
    rendered = reply_trial._render_prompt("形={slot}", {"kind": "q_yesno"}, PROBLEM, False, slot="B")
    assert rendered == "形=B"


def test_m2b_conflict_and_newline() -> None:
    rows = [
        {"id": "c1", "no": "N1", "kind": "q_yesno", "answer": "no", "reply": "いいえ。それは関係ないんだ。", "comment_text": "架空？"},
        {"id": "c2", "no": "N1", "kind": "q_yesno", "answer": "yes", "reply": "はい！\nその調子。", "comment_text": "架空？"},
        {"id": "c3", "no": "N1", "kind": "q_yesno", "answer": "yes", "reply": "はい！", "comment_text": "架空？"},
    ]
    metrics = reply_trial.aggregate_variant(rows, {"name": "t", "label": "t", "type": "as_is"}, core={}, allow_words=[])
    assert metrics["M2_answer_word"]["conflict_count"] == 1
    assert metrics["M2_answer_word"]["conflict_items"][0]["id"] == "c1"
    assert metrics["M2_answer_word"]["newline_count"] == 1
