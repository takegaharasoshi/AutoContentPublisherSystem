"""Tests for narration synthesis, caching, and guarded props updates."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Callable


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_narration  # noqa: E402
import build_timeline  # noqa: E402
from tts import CueAudio, CueRequest  # noqa: E402


class FakeEngine:
    """Create deterministic measurements without contacting a TTS process."""

    engine_id = "fake/1/speaker12"

    def __init__(
        self, frame_for: Callable[[str, float], int] | None = None
    ) -> None:
        self.frame_for = frame_for or (lambda cue_id, speed: 20)
        self.calls: list[tuple[str, float]] = []

    def synthesize(
        self, request: CueRequest, out_path: Path, *, speed_scale: float
    ) -> CueAudio:
        self.calls.append((request.id, speed_scale))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"fake wav")
        frames = self.frame_for(request.id, speed_scale)
        return CueAudio(
            id=request.id,
            path=out_path,
            seconds=frames / 30,
            frames=frames,
            name_offset_frames=10 if request.name_text is not None else None,
            speed_scale=speed_scale,
            engine_id=self.engine_id,
        )


def props_document() -> dict[str, object]:
    """Return the minimum complete 20-second props document."""
    timeline = build_timeline.build_timelines()["20s"]
    return {
        "duration": "20s",
        "entries": [
            {"rank": rank, "prefName": f"県{rank}"} for rank in range(1, 6)
        ],
        "cues": {
            anchor.id: {
                "id": anchor.id,
                "text": f"原稿 {anchor.id}",
                "audioSrc": None,
                "startFrame": 0,
                "frames": None,
            }
            for anchor in timeline.cue_anchors
        },
    }


def write_props(path: Path) -> bytes:
    """Write test props and return its original bytes."""
    body = (json.dumps(props_document(), ensure_ascii=False, indent=2) + "\n").encode()
    path.write_bytes(body)
    return body


def test_build_resolves_props_and_reuses_manifest_cache(
    tmp_path: Path, monkeypatch: object
) -> None:
    """A second identical build reuses all generated WAV measurements."""
    monkeypatch.setattr(build_narration, "PROJECT_DIR", tmp_path)
    props_path = tmp_path / "001-20s.json"
    write_props(props_path)
    engine = FakeEngine()

    assert build_narration.build_narration(props_path, engine=engine) == 0
    first_call_count = len(engine.calls)
    resolved = json.loads(props_path.read_text(encoding="utf-8"))
    assert resolved["cues"]["r5"]["audioSrc"] == "narration/001-20s/r5.wav"
    assert resolved["cues"]["r5"]["startFrame"] == 155
    assert resolved["cues"]["r5"]["frames"] == 20

    assert build_narration.build_narration(props_path, engine=engine) == 0
    assert len(engine.calls) == first_call_count
    manifest = json.loads(
        (tmp_path / "public/narration/001-20s/manifest.json").read_text()
    )
    assert manifest["r5"]["engineId"] == engine.engine_id
    assert manifest["r5"]["nameOffsetFrames"] == 10


def test_violation_returns_nonzero_without_updating_props(
    tmp_path: Path, monkeypatch: object
) -> None:
    """An invalid placement leaves the input props byte-for-byte unchanged."""
    monkeypatch.setattr(build_narration, "PROJECT_DIR", tmp_path)
    props_path = tmp_path / "invalid.json"
    original = write_props(props_path)
    engine = FakeEngine(lambda cue_id, speed: 100 if cue_id == "outro" else 20)

    assert build_narration.build_narration(props_path, engine=engine) == 1
    assert props_path.read_bytes() == original


def test_auto_speed_raises_only_involved_cue_until_it_fits(
    tmp_path: Path, monkeypatch: object
) -> None:
    """Auto speed retries a violating cue at 1.15 and then 1.2 only."""
    monkeypatch.setattr(build_narration, "PROJECT_DIR", tmp_path)
    props_path = tmp_path / "auto.json"
    write_props(props_path)
    engine = FakeEngine(
        lambda cue_id, speed: (
            80 if cue_id == "outro" and speed >= 1.2 else 100
        )
        if cue_id == "outro"
        else 20
    )

    assert (
        build_narration.build_narration(
            props_path, engine=engine, auto_speed=True
        )
        == 0
    )
    assert [speed for cue_id, speed in engine.calls if cue_id == "outro"] == [
        1.1,
        1.15,
        1.2,
    ]
    assert all(
        speed == 1.1 for cue_id, speed in engine.calls if cue_id != "outro"
    )
    resolved = json.loads(props_path.read_text(encoding="utf-8"))
    assert resolved["cues"]["outro"]["frames"] == 80
