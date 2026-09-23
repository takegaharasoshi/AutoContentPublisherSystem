"""背景 intake の中央クロップ出力テスト。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

import intake


def test_intake_outputs_1080x1920_jpeg(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(intake, "WORK", tmp_path)
    raw = tmp_path / "backgrounds" / "raw"
    raw.mkdir(parents=True)
    Image.new("RGB", (40, 30), (12, 34, 56)).save(raw / "001-test.png")

    intake.intake_backgrounds([{"content_key": "001-test"}])

    with Image.open(tmp_path / "backgrounds" / "001-test.jpg") as image:
        assert image.size == (1080, 1920)
        assert image.format == "JPEG"
