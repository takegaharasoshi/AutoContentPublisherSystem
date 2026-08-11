"""Tests for the engine-independent TTS measurements and VOICEVOX adapter."""

from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
import sys
import wave

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import tts  # noqa: E402


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "voicevox_queries.json"


@pytest.fixture(scope="module")
def queries() -> dict[str, dict[str, object]]:
    """Load audio queries captured from VOICEVOX speaker 12."""
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_query_seconds_matches_all_voicevox_wavs(
    queries: dict[str, dict[str, object]],
) -> None:
    """The query duration model stays inside the tolerance for every WAV."""
    for key, fixture in queries.items():
        error = abs(tts.query_seconds(fixture["query"]) - fixture["wavSeconds"])
        assert error <= tts.LENGTH_TOLERANCE_SECONDS, key


@pytest.mark.parametrize("key", ["teaser_question", "outro_question"])
def test_query_seconds_models_interrogative_upspeak(
    queries: dict[str, dict[str, object]], key: str
) -> None:
    """疑問形は語尾上げのモーラが 1 つ増えるぶんを query の外から補う。"""
    query = queries[key]["query"]
    plain = query["prePhonemeLength"] + query["postPhonemeLength"]
    for phrase in query["accent_phrases"]:
        for mora in phrase["moras"]:
            plain += (mora["consonant_length"] or 0) + mora["vowel_length"]
        pause = phrase.get("pause_mora")
        if pause is not None:
            plain += (pause["consonant_length"] or 0) + pause["vowel_length"]
    plain /= query["speedScale"]
    # 補正なしでは実測に 0.1 秒以上足りず、補正すると許容差に収まる。
    assert queries[key]["wavSeconds"] - plain > 0.1
    assert (
        abs(tts.query_seconds(query) - queries[key]["wavSeconds"])
        <= tts.LENGTH_TOLERANCE_SECONDS
    )


@pytest.mark.parametrize(
    ("call_key", "name_key"),
    [("call_saitama", "name_saitama"), ("call_hokkaido", "name_hokkaido")],
)
def test_name_offset_finds_prefecture_at_right_edge(
    queries: dict[str, dict[str, object]], call_key: str, name_key: str
) -> None:
    """Captured call cues expose a plausible prefecture-name offset."""
    name_moras = [
        text for text, _ in tts.mora_entries(queries[name_key]["query"])
    ]
    offset = tts.name_offset_seconds(queries[call_key]["query"], name_moras)
    assert offset is not None
    assert 0.8 <= offset <= 1.4


def test_name_offset_returns_none_when_name_is_absent(
    queries: dict[str, dict[str, object]],
) -> None:
    """A closing cue does not falsely match an unrelated prefecture."""
    name_moras = [
        text for text, _ in tts.mora_entries(queries["name_saitama"]["query"])
    ]
    assert (
        tts.name_offset_seconds(queries["closing_gyoza"]["query"], name_moras)
        is None
    )


def test_seconds_to_frames_uses_rounding() -> None:
    """Seconds are rounded rather than always truncated or rounded up."""
    assert tts.seconds_to_frames(1.01, 30) == 30
    assert tts.seconds_to_frames(1.02, 30) == 31


class StubResponse:
    """Minimal context-manager response returned by urlopen stubs."""

    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> "StubResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


def short_wav() -> bytes:
    """Build a valid 0.1-second mono WAV in memory."""
    output = BytesIO()
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(b"\0\0" * 2400)
    return output.getvalue()


def test_engine_id_covers_speaker_and_intonation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """抑揚を変えたら別の識別子になる（= 合成キャッシュが無効になる）。"""

    def urlopen(request: object, timeout: float) -> StubResponse:
        return StubResponse(b'"0.24.1"')

    monkeypatch.setattr(tts.urllib.request, "urlopen", urlopen)
    assert tts.VoicevoxEngine(intonation_scale=1.9).engine_id == (
        "voicevox/0.24.1/speaker12/int1.9"
    )
    assert tts.VoicevoxEngine(intonation_scale=1.2).engine_id != (
        tts.VoicevoxEngine(intonation_scale=1.9).engine_id
    )


def test_voicevox_engine_rejects_query_and_wav_duration_mismatch(
    queries: dict[str, dict[str, object]], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The adapter detects an engine duration-model change beyond the tolerance."""
    query_body = json.dumps(queries["call_saitama"]["query"]).encode("utf-8")
    wav_body = short_wav()

    def urlopen(request: object, timeout: float) -> StubResponse:
        url = request.full_url
        return StubResponse(query_body if "/audio_query" in url else wav_body)

    monkeypatch.setattr(tts.urllib.request, "urlopen", urlopen)
    engine = tts.VoicevoxEngine()
    with pytest.raises(tts.TtsError, match="秒を超えています"):
        engine.synthesize(
            tts.CueRequest("intro", "まずは5位、埼玉県！"),
            tmp_path / "intro.wav",
            speed_scale=1.1,
        )
