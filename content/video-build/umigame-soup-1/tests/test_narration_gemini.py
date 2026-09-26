"""Gemini TTS アダプタと build 側の分岐を外部 API なしで検査する。"""

from __future__ import annotations

import array
import base64
import io
import json
from pathlib import Path
import shutil
import urllib.error
import wave

import pytest

import build
import review_sheet
from scripts import narration_gemini


RATE = 1000


def _wav_bytes(*segments: tuple[float, int]) -> bytes:
    samples = array.array("h")
    for seconds, amplitude in segments:
        samples.extend([amplitude] * round(seconds * RATE))
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(samples.tobytes())
    return output.getvalue()


def _config() -> dict:
    return {
        "model": "gemini-3.8-flash-tts",
        "voice_id": "voice_1m8w495yafud",
        "style": "得意げに語る",
        "gap_seconds": 1.2,
        "budget_seconds": 21.0,
        "target_seconds": 19.0,
        "max_tempo": 1.19,
    }


def _fake_ffmpeg(source: Path, target: Path, filters: str) -> None:
    """ffmpeg の入出力だけ模し、atempo 時は WAV を短くする。"""
    if "atempo=" not in filters:
        shutil.copyfile(source, target)
        return
    tempo = float(filters.rsplit("atempo=", 1)[1])
    with wave.open(str(source), "rb") as wav:
        params = wav.getparams()
        samples = wav.readframes(wav.getnframes())
    kept_frames = round(params.nframes / tempo)
    with wave.open(str(target), "wb") as wav:
        wav.setparams(params)
        wav.writeframes(samples[:kept_frames * params.sampwidth])


def _mock_audio(monkeypatch, audio: bytes) -> list[dict]:
    calls: list[dict] = []

    def post(path: str, body: dict) -> dict:
        assert path == "interactions"
        calls.append(body)
        return {
            "output": [{"mime_type": "audio/wav", "data": base64.b64encode(audio).decode()}]
        }

    monkeypatch.setattr(narration_gemini, "_post", post)
    return calls


def test_interactions_request_body_and_pcm_wav(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    requests = []

    def urlopen(request, timeout):
        requests.append((request, timeout))
        response = {"output": [{
            "mime_type": "audio/pcm",
            "data": base64.b64encode(array.array("h", [100, 200]).tobytes()).decode(),
        }]}
        return io.BytesIO(json.dumps(response).encode())

    monkeypatch.setattr(narration_gemini.urllib.request, "urlopen", urlopen)
    path = tmp_path / "combined.wav"
    assert narration_gemini.synthesize(
        "問題\n\nルール", "得意げに語る", "gemini-3.8-flash-tts", "voice-id", path
    ) == pytest.approx(2 / 24000)
    request, timeout = requests[0]
    assert len(requests) == 1
    assert request.full_url == f"{narration_gemini.API_BASE}/interactions"
    assert request.get_method() == "POST"
    assert request.get_header("X-goog-api-key") == "test-key"
    assert timeout == 180
    body = json.loads(request.data)
    assert body == {
        "model": "gemini-3.8-flash-tts",
        "input": [{"type": "user_input", "content": [{
            "type": "text", "text": "問題\n\nルール",
            "annotations": [{"type": "speech_metadata", "style": "得意げに語る"}],
        }]}],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": "voice-id"}]},
    }
    with wave.open(str(path), "rb") as wav:
        assert (wav.getframerate(), wav.getnchannels(), wav.getnframes()) == (24000, 1, 2)


def test_api_key_prefers_environment_then_config_file(
    tmp_path: Path, monkeypatch
) -> None:
    key_path = tmp_path / ".config" / "gemini" / "api_key"
    key_path.parent.mkdir(parents=True)
    key_path.write_text("file-key\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", " env-key ")
    assert narration_gemini._api_key() == "env-key"
    monkeypatch.delenv("GEMINI_API_KEY")
    assert narration_gemini._api_key() == "file-key"


def test_cache_force_and_changed_inputs(tmp_path: Path, monkeypatch) -> None:
    audio = _wav_bytes((1.0, 1200), (0.4, 0), (1.0, 1200))
    calls = _mock_audio(monkeypatch, audio)
    config = _config()
    out_dir = tmp_path / "narration"

    first = narration_gemini.synthesize_cues(
        "問題", "ルール", out_dir, config=config, ffmpeg_runner=_fake_ffmpeg
    )
    cached = narration_gemini.synthesize_cues(
        "問題", "ルール", out_dir, config=config, ffmpeg_runner=_fake_ffmpeg
    )
    assert cached == first
    assert len(calls) == 1
    assert first["attempt"] == 1
    assert first["engine_id"] == "gemini/gemini-3.8-flash-tts/voice_1m8w495yafud"
    assert first["synthesized_at"].endswith("Z")
    assert first["cues"]["problem"]["frames"] == round(
        first["cues"]["problem"]["seconds"] * 30
    )

    forced = narration_gemini.synthesize_cues(
        "問題", "ルール", out_dir, config=config, force=True,
        ffmpeg_runner=_fake_ffmpeg,
    )
    assert forced["attempt"] == 2
    changed_text = narration_gemini.synthesize_cues(
        "別の問題", "ルール", out_dir, config=config, ffmpeg_runner=_fake_ffmpeg
    )
    assert changed_text["attempt"] == 3
    changed_style = narration_gemini.synthesize_cues(
        "別の問題", "ルール", out_dir,
        config={**config, "style": "静かに語る"}, ffmpeg_runner=_fake_ffmpeg,
    )
    assert changed_style["attempt"] == 4
    assert len(calls) == 4
    assert calls[-1]["input"][0]["content"][0]["text"] == "別の問題\n\nルール"


def test_split_chooses_gap_nearest_character_ratio(tmp_path: Path) -> None:
    combined = tmp_path / "combined.wav"
    combined.write_bytes(_wav_bytes(
        (2.0, 1200), (0.4, 0), (2.0, 1200), (0.4, 0), (2.0, 1200)
    ))
    cut = narration_gemini._split(
        combined, 0.7, tmp_path / "problem.wav", tmp_path / "rule.wav"
    )
    assert cut == pytest.approx(4.6)
    with wave.open(str(tmp_path / "problem.wav"), "rb") as wav:
        assert wav.getnframes() == 4600


def test_split_without_silence_fails(tmp_path: Path) -> None:
    combined = tmp_path / "combined.wav"
    combined.write_bytes(_wav_bytes((2.0, 1200)))
    with pytest.raises(RuntimeError, match="無音が見つかりません"):
        narration_gemini._split(
            combined, 0.5, tmp_path / "problem.wav", tmp_path / "rule.wav"
        )


@pytest.mark.parametrize(
    ("rule_seconds", "expected_natural", "expected_tempo"),
    [(9.0, 20.6, 1.0), (10.0, 21.6, 1.146)],
)
def test_tempo_only_when_over_budget(
    tmp_path: Path, monkeypatch, rule_seconds: float,
    expected_natural: float, expected_tempo: float,
) -> None:
    audio = _wav_bytes((10.0, 1200), (0.4, 0), (rule_seconds, 1200))
    _mock_audio(monkeypatch, audio)
    filters: list[str] = []

    def runner(source: Path, target: Path, value: str) -> None:
        filters.append(value)
        _fake_ffmpeg(source, target, value)

    report = narration_gemini.synthesize_cues(
        "問題", "ルール", tmp_path, config=_config(), ffmpeg_runner=runner
    )
    assert report["natural_seconds"] == pytest.approx(expected_natural)
    assert report["tempo"] == expected_tempo
    assert len(filters) == (4 if expected_tempo > 1 else 2)
    assert all("silenceremove=" in value for value in filters)
    assert sum("atempo=" in value for value in filters) == (2 if expected_tempo > 1 else 0)


def test_over_tempo_writes_report_and_cached_failure(
    tmp_path: Path, monkeypatch
) -> None:
    calls = _mock_audio(
        monkeypatch, _wav_bytes((10.0, 1200), (0.4, 0), (11.0, 1200))
    )
    with pytest.raises(narration_gemini.TempoLimitError, match="--retake-tts") as exc:
        narration_gemini.synthesize_cues(
            "問題", "ルール", tmp_path, config=_config(),
            ffmpeg_runner=_fake_ffmpeg,
        )
    report = json.loads((tmp_path / "narration.json").read_text(encoding="utf-8"))
    assert report["tempo"] == exc.value.tempo
    assert report["tempo"] > 1.19
    assert report["attempt"] == 1
    with pytest.raises(narration_gemini.TempoLimitError):
        narration_gemini.synthesize_cues(
            "問題", "ルール", tmp_path, config=_config(),
            ffmpeg_runner=_fake_ffmpeg,
        )
    assert len(calls) == 1


@pytest.mark.parametrize(
    ("status", "body", "error_type"),
    [
        (429, "too many requests", narration_gemini.GeminiQuotaError),
        (403, "quota exceeded", narration_gemini.GeminiQuotaError),
        (400, "RESOURCE_EXHAUSTED billing", narration_gemini.GeminiQuotaError),
        (403, "permission denied", narration_gemini.GeminiApiError),
        (400, "invalid generation_config for generateContent", narration_gemini.GeminiApiError),
        (429, "rate limit exceeded", narration_gemini.GeminiQuotaError),
        (500, "server failed", narration_gemini.GeminiApiError),
    ],
)
def test_http_error_classification_and_redaction(
    monkeypatch, status: int, body: str, error_type: type[Exception]
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-secret")

    def urlopen(request, timeout):
        raise urllib.error.HTTPError(
            request.full_url, status, "error", {},
            io.BytesIO(f"{body} test-secret".encode()),
        )

    monkeypatch.setattr(narration_gemini.urllib.request, "urlopen", urlopen)
    with pytest.raises(error_type) as exc:
        narration_gemini._post("interactions", {})
    assert type(exc.value) is error_type
    assert f"HTTP {status}" in str(exc.value)
    assert body in str(exc.value)
    assert "test-secret" not in str(exc.value)


def _build_inputs(tmp_path: Path, monkeypatch, keys: tuple[str, ...]) -> None:
    monkeypatch.setattr(build, "WORK", tmp_path)
    backgrounds = tmp_path / "backgrounds"
    backgrounds.mkdir()
    for key in keys:
        (backgrounds / f"{key}.jpg").write_bytes(b"background")
    monkeypatch.setattr(build, "load_items", lambda batch: [
        {"content_key": key, "narration": {"problem": key, "rule": "ルール"}}
        for key in keys
    ])
    monkeypatch.setattr(build, "load_manifest", lambda: {})
    monkeypatch.setattr(build, "load_bgm_tracks", lambda: [{
        "output": "track.m4a", "s3_key": "track", "provisional": False,
    }])
    monkeypatch.setattr(build, "stage_assets", lambda *args: None)
    monkeypatch.setattr(build, "build_props", lambda *args: {})
    monkeypatch.setattr(build, "write_json", lambda *args: None)
    monkeypatch.setattr(review_sheet, "write_review", lambda *args, **kwargs: None)


def _report(engine: str = "gemini") -> dict:
    return {
        "engine_id": f"{engine}/test",
        "tempo": 1.0,
        "cues": {
            "problem": {"seconds": 5.0, "frames": 150},
            "rule": {"seconds": 5.0, "frames": 150},
        },
    }


def test_build_tts_polly_uses_existing_adapter(tmp_path: Path, monkeypatch) -> None:
    _build_inputs(tmp_path, monkeypatch, ("001-test",))
    calls = []

    def polly(problem, rule, out_dir):
        calls.append((problem, rule, out_dir))
        return _report("polly")

    monkeypatch.setattr(build.narration_polly, "synthesize_cues", polly)
    monkeypatch.setattr(
        build.narration_gemini, "synthesize_cues",
        lambda *args, **kwargs: pytest.fail("Gemini must not be called"),
    )
    assert build.main(["--tts", "polly", "--content-key", "001-test", "--skip-render"]) == 0
    assert calls == [("001-test", "ルール", tmp_path / "narration" / "001-test")]


def test_polly_retake_uses_fresh_directory(tmp_path: Path, monkeypatch) -> None:
    out_dir = tmp_path / "001-test"
    out_dir.mkdir()
    (out_dir / "narration.json").write_text("old", encoding="utf-8")
    calls = []

    def polly(problem, rule, target):
        calls.append(target)
        assert target != out_dir
        for name in ("problem.wav", "rule.wav", "narration.json"):
            (target / name).write_text("new", encoding="utf-8")
        return _report("polly")

    monkeypatch.setattr(build.narration_polly, "synthesize_cues", polly)
    report = build._synthesize_polly("問題", "ルール", out_dir, force=True)
    assert report["engine_id"] == "polly/test"
    assert len(calls) == 1
    assert (out_dir / "narration.json").read_text(encoding="utf-8") == "new"


def test_build_quota_stops_before_next_item(tmp_path: Path, monkeypatch) -> None:
    _build_inputs(tmp_path, monkeypatch, ("001-first", "002-next"))
    calls = []

    def gemini(problem, rule, out_dir, *, config, force):
        calls.append(problem)
        raise narration_gemini.GeminiQuotaError("interactions", 429, "quota")

    monkeypatch.setattr(build.narration_gemini, "synthesize_cues", gemini)
    assert build.main(["--tts", "gemini", "--skip-render"]) == 1
    assert calls == ["001-first"]


def test_build_tempo_failure_continues_to_next_item(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    _build_inputs(tmp_path, monkeypatch, ("001-first", "002-next"))
    calls = []

    def gemini(problem, rule, out_dir, *, config, force):
        calls.append((problem, force))
        if problem == "001-first":
            raise narration_gemini.TempoLimitError(1.234, 1.19)
        return _report()

    monkeypatch.setattr(build.narration_gemini, "synthesize_cues", gemini)
    assert build.main(["--tts", "gemini", "--skip-render", "--retake-tts"]) == 1
    assert calls == [("001-first", True), ("002-next", True)]
    assert "倍率 1.234 > 1.19・--retake-tts で取り直し" in capsys.readouterr().err
