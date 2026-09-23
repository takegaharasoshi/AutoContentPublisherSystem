"""プロンプト出力のテスト。"""

from __future__ import annotations

from pathlib import Path

import export_prompts


def test_export_prompt_is_unmodified_with_one_trailing_newline(
    tmp_path: Path, monkeypatch,
) -> None:
    monkeypatch.setattr(export_prompts, "WORK", tmp_path)
    prompt = "line 1\nline 2\n\n"

    keys = export_prompts.export_prompts(
        [{"content_key": "001-test", "illustration_prompt": prompt}]
    )

    assert keys == ["001-test"]
    assert (tmp_path / "prompts" / "001-test.txt").read_text(encoding="utf-8") == (
        "line 1\nline 2\n"
    )
