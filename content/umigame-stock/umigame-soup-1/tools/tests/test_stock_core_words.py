"""Offline checks for the authored core words, generated migration and probes."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from types import ModuleType

import pytest

from app.judge.contract import CoreWords
from app.reply import leak_guard, templates
from tools import local_trial, probe_metrics


BATCH_DIR = Path(__file__).resolve().parents[2] / "batch-01"


def _load_module(name: str) -> ModuleType:
    """Load one batch authoring module without invoking its CLI."""
    spec = importlib.util.spec_from_file_location(f"test_core_words_{name}", BATCH_DIR / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def stock() -> ModuleType:
    return _load_module("stock_items")


@pytest.fixture
def validation() -> ModuleType:
    return _load_module("validate")


@pytest.mark.parametrize("value", [
    None, [], {}, {"words": ["核心"]}, {"except": []},
    {"words": [], "except": []}, {"words": "核心", "except": []},
    {"words": ["核心"], "except": None}, {"words": ["核心"], "except": "例外"},
    {"words": ["核心", "核心"], "except": []},
    {"words": ["核心"], "except": ["例外", "例外"]},
    {"words": ["核心"], "except": [], "extra": []},
    *({"words": [word], "except": []} for word in ("", " ", "核\n心", "核\r心", 1, None, [])),
    *({"words": ["核心"], "except": [word]} for word in ("", " ", "例\n外", "例\r外", 1, None, [])),
])
def test_authoring_rejects_invalid_core_words(validation, value) -> None:
    validation.check_core_words("001-test", value)
    assert validation.errors
    assert all("001-test: core_words" in message for message in validation.errors)


@pytest.mark.parametrize("excepts", [[], ["遊び方"]])
def test_authoring_accepts_valid_core_words(validation, excepts) -> None:
    validation.check_core_words("001-test", {"words": ["遊び", "鬼"], "except": excepts})
    assert validation.errors == []


def test_all_authored_problems_reach_v4_snapshots(stock, validation) -> None:
    assert len(stock.ITEMS) == 14
    assert len({item["content_key"] for item in stock.ITEMS}) == 14
    words_by_no = probe_metrics.load_core_words()
    for item in stock.ITEMS:
        validation.check_item(item)
        value = item["core_words"]
        problem = local_trial._load_stock_problem(item["no"])
        assert problem.schema_version == 4
        assert problem.content_key == item["content_key"]
        assert problem.core_words == CoreWords(tuple(value["words"]), tuple(value["except"]))
        assert words_by_no[item["no"]] == value["words"]
    assert validation.errors == []


def test_generated_migration_preserves_words_and_backfills_only_nulls(stock) -> None:
    sql = (BATCH_DIR / "update_core_words.sql").read_text(encoding="utf-8")
    updates = re.findall(
        r"UPDATE umigame_stock_items SET core_words = '([^']+)'\nWHERE content_key = '([^']+)'",
        sql,
    )
    assert len(updates) == 14
    assert {key: json.loads(value) for value, key in updates} == {
        item["content_key"]: item["core_words"] for item in stock.ITEMS
    }
    assert "s.set_id = ui.set_id AND s.content_key = ui.content_key" in sql
    assert "SET ui.core_words = s.core_words\nWHERE ui.core_words IS NULL" in sql
    assert "FROM umigame_stock_items i" in sql
    assert "FROM umigame_items i" in sql
    assert sql.count("SUM(i.core_words IS NOT NULL) AS core_words_set") == 2


@pytest.mark.parametrize("existing_rows", [0, 14])
def test_generate_dry_run_checks_core_words_then_rolls_back(monkeypatch, existing_rows) -> None:
    generate = _load_module("generate")
    commands = []

    def run_mysql(sql):
        commands.append(sql)
        return (0, str(existing_rows), "") if len(commands) == 1 else (0, "14", "")

    monkeypatch.setattr(generate, "_run_mysql", run_mysql)
    assert generate.dry_run(
        "INSERT marker", "UPDATE marker", "CRITERIA marker", generate.build_core_words_update_sql(),
    ) == 0
    assert len(commands) == 2
    transaction = commands[1]
    assert transaction.startswith("START TRANSACTION;\n")
    assert transaction.endswith("\nROLLBACK;")
    assert ("UPDATE marker" in transaction) == bool(existing_rows)
    assert ("INSERT marker" in transaction) == (not existing_rows)
    assert "SET ui.core_words = s.core_words" in transaction
    assert "SUM(core_words IS NOT NULL) AS core_words_set" in transaction


def test_probe_uses_stock_exclusions() -> None:
    case = {"no": "U16", "text": "質問", "expected_kind": "impression"}
    row = {"record": {"final": {"kind": "impression"}, "reply": {"text": "遊び方を説明するよ"}}}
    assert probe_metrics.row_flags(row, case)["leak_words"] == []
    row["record"]["reply"]["text"] = "鬼ごっこで遊んだ"
    case["text"] = "鬼ごっこ？"
    assert probe_metrics.row_flags(row, case)["leak_words"] == ["遊ん"]


def test_all_fixed_reply_phrases_are_safe_for_every_stock_problem(stock) -> None:
    phrases = [text for options in templates.TEMPLATES.values() if options is not None
               for text in options]
    phrases.extend(templates.YESNO_OPENERS.values())
    phrases.extend(text.format(term="") for text in templates.BARE_TERM_QUESTIONS)
    phrases.append(templates.LEAK_GUARD_TEXT)
    phrases.extend(opener + text for opener in templates.YESNO_OPENERS.values()
                   for text in templates.TEMPLATES["q_yesno"])
    for item in stock.ITEMS:
        value = item["core_words"]
        core_words = CoreWords(tuple(value["words"]), tuple(value["except"]))
        for phrase in phrases:
            assert leak_guard.find_leaks(phrase, "", core_words) == [], (item["no"], phrase)


def test_review_sheet_displays_words_and_exclusions_with_html_escaping(stock) -> None:
    review = _load_module("review_sheet")
    item = {**stock.ITEMS[0], "core_words": {"words": ["<核心>"], "except": ["<例外>"]}}
    rendered = "\n".join(review.judge_html(item))
    assert "core_words.words" in rendered and "core_words.except" in rendered
    assert "&lt;核心&gt;" in rendered and "&lt;例外&gt;" in rendered
    assert "<核心>" not in rendered and "<例外>" not in rendered
