"""Offline checks for the shared core-word dictionary and reply output guard."""

from __future__ import annotations

import logging
from dataclasses import FrozenInstanceError, replace

import pytest

from app import comment_log
from app.config import Config
from app.judge.combiner import Combined
from app.judge.contract import Judgement
from app.reply import leak_guard, templates, writer


def _combined(kind: str, answer: str | None = None,
              decision: str = "luna") -> Combined:
    judgement = Judgement("luna", kind, answer=answer)
    return Combined(judgement, None, kind, answer, None, decision, None)


def _problem(problem, no: str = "U01"):
    return replace(problem, content_key=leak_guard.load_leak_words()[no].content_key)


def test_dictionary_entries_and_lookup() -> None:
    entries = leak_guard.load_leak_words()
    assert entries
    assert all(entry.no == no and entry.content_key and entry.words
               for no, entry in entries.items())
    assert len({entry.content_key for entry in entries.values()}) == len(entries)
    assert all(leak_guard.entry_for_content_key(entry.content_key) == entry
               for entry in entries.values())
    assert leak_guard.entry_for_content_key("missing") is None
    with pytest.raises(FrozenInstanceError):
        entries["U01"].content_key = "changed"


def test_find_leaks_excludes_comment_words_and_exception() -> None:
    entry = leak_guard.load_leak_words()["U16"]
    assert leak_guard.find_leaks("遊び方を説明するよ", "", entry) == []
    assert leak_guard.find_leaks("鬼ごっこで遊んだ", "鬼ごっこ？", entry) == ["遊ん"]
    assert leak_guard.find_leaks("鬼と鬼", "", entry) == ["鬼"]
    assert leak_guard.is_correct_reveal("guess_correct", "説明")
    assert leak_guard.is_correct_reveal("impression", "正解を話す")


def test_writer_yesno_guard_keeps_answer_and_diagnostics(monkeypatch, caplog, problem) -> None:
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs:
                        ("はい！レントゲン写真だよ", {"model": "fake"}))
    with caplog.at_level(logging.WARNING):
        reply = writer.write_reply(_combined("q_yesno", "yes"), "comment-1", "質問", _problem(problem),
                                   variant="1b", openai_api_key="fake")
    assert reply.text == templates.YESNO_OPENERS["yes"]
    assert reply.source == "leak_guard" and reply.over_80 is False
    assert reply.guard == {"words": ["レントゲン", "写真"],
                           "original_text": "はい！レントゲン写真だよ", "original_source": "llm"}
    assert reply.debug == {"model": "fake"}
    assert "REPLY_LEAK_GUARD comment_id=comment-1" in caplog.text


def test_writer_reveal_comment_and_exception_do_not_guard(monkeypatch, problem) -> None:
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs: ("レントゲンだよ", {}))
    correct = writer.write_reply(_combined("guess_correct"), "1", "質問", _problem(problem),
                                 variant="1b", openai_api_key="fake")
    assert correct.source == "llm" and correct.guard is None
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs:
                        ("正解はレントゲンだよ", {}))
    declared = writer.write_reply(_combined("impression"), "1", "質問", _problem(problem),
                                  variant="1b", openai_api_key="fake")
    assert declared.source == "llm" and declared.guard is None
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs:
                        ("レントゲンだよ", {}))
    quoted = writer.write_reply(_combined("impression"), "1", "レントゲン？", _problem(problem),
                                variant="1b", openai_api_key="fake")
    assert quoted.source == "llm" and quoted.guard is None
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs:
                        ("遊び方を説明するよ", {}))
    excepted = writer.write_reply(_combined("impression"), "1", "質問", _problem(problem, "U16"),
                                  variant="1b", openai_api_key="fake")
    assert excepted.source == "llm" and excepted.guard is None


def test_writer_non_yesno_template_split_and_missing_dict(monkeypatch, caplog, problem) -> None:
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs: ("病院だよ", {}))
    reply = writer.write_reply(_combined("impression"), "1", "質問", _problem(problem),
                               variant="1b", openai_api_key="fake")
    assert reply.text == templates.LEAK_GUARD_TEXT
    assert reply.source == "leak_guard" and reply.guard["original_source"] == "llm"

    monkeypatch.setattr(templates, "split_reply", lambda comment_id: "病院だよ")
    split = writer.write_reply(_combined("guess_correct", decision="consensus_split"), "1",
                               "質問", _problem(problem), variant="1b")
    assert split.text == templates.LEAK_GUARD_TEXT
    assert split.guard["original_source"] == "consensus_split"

    monkeypatch.setattr(templates, "pick", lambda kind, comment_id: "病院だよ")
    template = writer.write_reply(_combined("impression"), "1", "質問", _problem(problem),
                                  variant="2b")
    assert template.text == templates.LEAK_GUARD_TEXT
    assert template.guard["original_source"] == "template"

    with caplog.at_level(logging.WARNING):
        missing = writer.write_reply(_combined("impression"), "1", "質問", problem,
                                     variant="1b", openai_api_key="fake")
    assert missing.text == "病院だよ" and missing.source == "llm" and missing.guard is None
    assert "REPLY_LEAK_GUARD_NO_DICT content_key=001-test" in caplog.text


def test_all_fixed_reply_phrases_are_safe_for_every_problem() -> None:
    phrases = [text for options in templates.TEMPLATES.values() if options is not None
               for text in options]
    phrases.extend(templates.CONSENSUS_SPLIT)
    phrases.extend(templates.YESNO_OPENERS.values())
    phrases.extend(text.format(term="") for text in templates.BARE_TERM_QUESTIONS)
    phrases.append(templates.LEAK_GUARD_TEXT)
    phrases.extend(opener + text for opener in templates.YESNO_OPENERS.values()
                   for text in templates.TEMPLATES["q_yesno"])
    for entry in leak_guard.load_leak_words().values():
        for phrase in phrases:
            assert leak_guard.find_leaks(phrase, "", entry) == [], (entry.no, phrase)


def test_comment_record_preserves_guard(monkeypatch, problem) -> None:
    problem = _problem(problem)
    monkeypatch.setattr(writer, "_llm_reply", lambda *args, **kwargs:
                        ("はい！病院だよ", {}))
    combined = _combined("q_yesno", "yes")
    record = comment_log.new_record({"id": "1", "text": "質問"}, None,
                                    "2026-10-08T00:00:00Z", Config(), problem)
    assert record["reply"]["guard"] is None
    reply = writer.write_reply(combined, "1", "質問", problem,
                               variant="1b", openai_api_key="fake")
    comment_log.apply_decision(record, combined, reply)
    assert record["reply"]["guard"] == reply.guard
    assert record["reply"]["guard"]["words"] == ["病院"]
    assert writer.Reply(**{"text": "旧キャッシュ", "source": "template", "over_80": False}).guard is None
