"""Irodori アダプタの実行・取り直し・build 分岐を GPU なしで検査する。"""

from __future__ import annotations

import array
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import wave

import pytest

import build
import review_sheet
from scripts import narration_irodori


RATE = 1000


def _audio(problem_seconds: float, rule_seconds: float, *, width: int = 2) -> bytes:
    samples = array.array("h")
    for seconds, amplitude in (
        (problem_seconds, 1200), (0.4, 0), (rule_seconds, 1200)
    ):
        samples.extend([amplitude] * round(seconds * RATE))
    if width == 2:
        frames = samples.tobytes()
    else:
        frames = b"".join(int(sample).to_bytes(3, "little", signed=True) for sample in samples)
    import io

    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(width)
        wav.setframerate(RATE)
        wav.writeframes(frames)
    return output.getvalue()


def _config() -> dict:
    return {
        "model": "Aratako/Irodori-TTS-v4.1-Small",
        "ref_dir": "assets/voice/kamerock-g4",
        "precision": "bf16",
        "seed": 1,
        "seconds": 20.0,
        "seconds_step": 0.5,
        "max_takes": 3,
        "gap_seconds": 1.2,
        "budget_seconds": 21.0,
    }


def _refs(tmp_path: Path, monkeypatch) -> Path:
    monkeypatch.setattr(narration_irodori, "SET_DIR", tmp_path)
    ref_dir = tmp_path / "assets" / "voice" / "kamerock-g4"
    ref_dir.mkdir(parents=True)
    (ref_dir / "b.wav").write_bytes(b"reference b")
    (ref_dir / "a.wav").write_bytes(b"reference a")
    return ref_dir


def _fake_ffmpeg(source: Path, target: Path, filters: str) -> None:
    assert "atempo=" not in filters
    if filters == "anull":
        shutil.copyfile(source, target)
        return
    with wave.open(str(source), "rb") as wav:
        params = wav.getparams()
        samples = array.array("h", wav.readframes(wav.getnframes()))
    start = next((index for index, sample in enumerate(samples) if sample), len(samples))
    end = next(
        (index + 1 for index in range(len(samples) - 1, -1, -1) if samples[index]),
        start,
    )
    with wave.open(str(target), "wb") as wav:
        wav.setparams(params)
        wav.writeframes(samples[start:end].tobytes())


class FakeInfer:
    def __init__(self, durations: list[tuple[float, float]], *, returncode: int = 0) -> None:
        self.durations = durations
        self.returncode = returncode
        self.calls: list[tuple[list[str], dict]] = []

    def __call__(self, command: list[str], **kwargs):
        self.calls.append((command, kwargs))
        kwargs["stdout"].write(f"take {len(self.calls)} result\n")
        kwargs["stdout"].flush()
        if self.returncode == 0:
            problem, rule = self.durations[min(len(self.calls) - 1, len(self.durations) - 1)]
            Path(command[command.index("--output-wav") + 1]).write_bytes(
                _audio(problem, rule)
            )
        return subprocess.CompletedProcess(command, self.returncode)


def test_command_report_and_first_take(tmp_path: Path, monkeypatch) -> None:
    ref_dir = _refs(tmp_path, monkeypatch)
    irodori_dir = tmp_path / "irodori"
    monkeypatch.setenv("IRODORI_DIR", str(irodori_dir))
    infer = FakeInfer([(8.0, 8.0)])
    out_dir = tmp_path / "out"

    report = narration_irodori.synthesize_cues(
        "問題", "ルール", out_dir, config=_config(),
        runner=infer, ffmpeg_runner=_fake_ffmpeg,
    )

    assert len(infer.calls) == 1
    command, kwargs = infer.calls[0]
    assert command[:7] == [
        "uv", "run", "--no-sync", "python", "infer.py", "--hf-checkpoint",
        "Aratako/Irodori-TTS-v4.1-Small",
    ]
    assert command[7:15] == [
        "--model-device", "cuda", "--codec-device", "cuda",
        "--model-precision", "bf16", "--codec-precision", "bf16",
    ]
    assert command[15:21] == ["--seed", "1", "--seconds", "20.0", "--text", "問題 ルール"]
    assert command[command.index("--ref-wavs") + 1:command.index("--output-wav")] == [
        str(ref_dir / "a.wav"), str(ref_dir / "b.wav")
    ]
    assert command[-1] == str(out_dir / "combined.wav")
    assert "--caption" not in command
    assert kwargs["cwd"] == irodori_dir
    assert kwargs["timeout"] == 900
    assert kwargs["stderr"] == subprocess.STDOUT
    assert kwargs["check"] is False
    assert report["engine_id"] == "irodori/Aratako/Irodori-TTS-v4.1-Small/kamerock-g4"
    assert report["ref_wavs"] == [
        {"name": name, "sha256": hashlib.sha256((ref_dir / name).read_bytes()).hexdigest()}
        for name in ("a.wav", "b.wav")
    ]
    assert report["seed"] == 1
    assert report["seconds"] == 20.0
    assert report["attempt"] == 1
    assert report["precision"] == "bf16"
    assert report["total_seconds"] == pytest.approx(17.2)
    assert report["takes"] == [{"seed": 1, "seconds": 20.0, "total_seconds": 17.2}]
    assert report["cues"]["problem"]["frames"] == round(
        report["cues"]["problem"]["seconds"] * 30
    )
    assert "tempo" not in report
    assert report["synthesized_at"].endswith("Z")
    assert "take 1 result" in (out_dir / "irodori.log").read_text(encoding="utf-8")


def test_retries_shorten_seconds_and_advance_seed(tmp_path: Path, monkeypatch) -> None:
    _refs(tmp_path, monkeypatch)
    infer = FakeInfer([(11.0, 11.0), (10.0, 10.0), (9.0, 9.0)])

    report = narration_irodori.synthesize_cues(
        "問題", "ルール", tmp_path / "out", config=_config(),
        runner=infer, ffmpeg_runner=_fake_ffmpeg,
    )

    assert [call[0][call[0].index("--seconds") + 1] for call in infer.calls] == [
        "20.0", "19.5", "19.0"
    ]
    assert [call[0][call[0].index("--seed") + 1] for call in infer.calls] == [
        "1", "2", "3"
    ]
    assert report["attempt"] == 3
    assert report["seconds"] == 19.0
    assert [take["total_seconds"] for take in report["takes"]] == [23.2, 21.2, 19.2]


def test_all_takes_over_budget_writes_last_report(tmp_path: Path, monkeypatch) -> None:
    _refs(tmp_path, monkeypatch)
    infer = FakeInfer([(11.0, 11.0)] * 3)
    out_dir = tmp_path / "out"

    with pytest.raises(narration_irodori.IrodoriBudgetError) as exc:
        narration_irodori.synthesize_cues(
            "問題", "ルール", out_dir, config=_config(),
            runner=infer, ffmpeg_runner=_fake_ffmpeg,
        )

    report = json.loads((out_dir / "narration.json").read_text(encoding="utf-8"))
    assert report["attempt"] == 3
    assert report["seed"] == 3
    assert report["seconds"] == 19.0
    assert len(report["takes"]) == 3
    assert report["total_seconds"] == pytest.approx(23.2)
    assert exc.value.attempted_seconds == [20.0, 19.5, 19.0]
    assert "20.0, 19.5, 19.0" in str(exc.value)
    assert "23.200" in str(exc.value)
    assert (out_dir / "irodori.log").read_text(encoding="utf-8").count("result") == 3


def test_cache_force_and_reference_hash(tmp_path: Path, monkeypatch) -> None:
    ref_dir = _refs(tmp_path, monkeypatch)
    infer = FakeInfer([(8.0, 8.0)])
    out_dir = tmp_path / "out"

    first = narration_irodori.synthesize_cues(
        "問題", "ルール", out_dir, config=_config(),
        runner=infer, ffmpeg_runner=_fake_ffmpeg,
    )
    cached = narration_irodori.synthesize_cues(
        "問題", "ルール", out_dir, config=_config(),
        runner=infer, ffmpeg_runner=_fake_ffmpeg,
    )
    assert cached == first
    assert len(infer.calls) == 1

    forced = narration_irodori.synthesize_cues(
        "問題", "ルール", out_dir, config=_config(), force=True,
        runner=infer, ffmpeg_runner=_fake_ffmpeg,
    )
    assert forced["seed"] == 2
    assert forced["attempt"] == 2
    assert forced["seconds"] == 20.0
    assert len(infer.calls) == 2

    (ref_dir / "a.wav").write_bytes(b"changed reference")
    changed = narration_irodori.synthesize_cues(
        "問題", "ルール", out_dir, config=_config(),
        runner=infer, ffmpeg_runner=_fake_ffmpeg,
    )
    assert changed["attempt"] == 3
    assert changed["seed"] == 3
    assert len(infer.calls) == 3


def test_force_after_budget_failure_resets_seconds(tmp_path: Path, monkeypatch) -> None:
    _refs(tmp_path, monkeypatch)
    out_dir = tmp_path / "out"
    infer = FakeInfer([(11.0, 11.0)] * 3 + [(8.0, 8.0)])
    with pytest.raises(narration_irodori.IrodoriBudgetError):
        narration_irodori.synthesize_cues(
            "問題", "ルール", out_dir, config=_config(),
            runner=infer, ffmpeg_runner=_fake_ffmpeg,
        )

    report = narration_irodori.synthesize_cues(
        "問題", "ルール", out_dir, config=_config(), force=True,
        runner=infer, ffmpeg_runner=_fake_ffmpeg,
    )

    assert report["attempt"] == 4
    assert report["seed"] == 4
    assert report["seconds"] == 20.0
    assert report["takes"] == [{"seed": 4, "seconds": 20.0, "total_seconds": 17.2}]


def test_non_pcm_output_uses_ffmpeg_before_split(tmp_path: Path, monkeypatch) -> None:
    _refs(tmp_path, monkeypatch)
    filters: list[str] = []

    def infer(command: list[str], **kwargs):
        Path(command[-1]).write_bytes(_audio(8.0, 8.0, width=3))
        return subprocess.CompletedProcess(command, 0)

    def ffmpeg(source: Path, target: Path, value: str) -> None:
        filters.append(value)
        if value == "anull":
            target.write_bytes(_audio(8.0, 8.0))
        else:
            _fake_ffmpeg(source, target, value)

    report = narration_irodori.synthesize_cues(
        "問題", "ルール", tmp_path / "out", config=_config(),
        runner=infer, ffmpeg_runner=ffmpeg,
    )
    assert report["total_seconds"] == pytest.approx(17.2)
    assert filters[0] == "anull"
    assert len(filters) == 3
    assert all("atempo=" not in value for value in filters)


def test_infer_failure_raises_irodori_error_with_log(tmp_path: Path, monkeypatch) -> None:
    _refs(tmp_path, monkeypatch)
    infer = FakeInfer([], returncode=7)
    with pytest.raises(narration_irodori.IrodoriError) as exc:
        narration_irodori.synthesize_cues(
            "問題", "ルール", tmp_path / "out", config=_config(),
            runner=infer, ffmpeg_runner=_fake_ffmpeg,
        )
    assert "（7）" in str(exc.value)
    assert "take 1 result" in str(exc.value)
    assert not (tmp_path / "out" / "narration.json").exists()


def _build_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(build, "WORK", tmp_path)
    background = tmp_path / "backgrounds"
    background.mkdir()
    for key in ("001-first", "002-next"):
        (background / f"{key}.jpg").write_bytes(b"background")
    monkeypatch.setattr(build, "load_items", lambda batch: [
        {
            "content_key": key, "title": key,
            "narration": {"problem": key, "rule": "ルール"},
        }
        for key in ("001-first", "002-next")
    ])
    monkeypatch.setattr(build, "load_manifest", lambda: {})
    monkeypatch.setattr(build, "load_bgm_tracks", lambda: [{
        "output": "track.m4a", "s3_key": "track", "provisional": False,
    }])
    monkeypatch.setattr(build, "stage_assets", lambda *args: None)
    monkeypatch.setattr(build, "build_props", lambda *args: {})
    monkeypatch.setattr(build, "write_json", lambda *args: None)
    monkeypatch.setattr(review_sheet, "write_review", lambda *args, **kwargs: None)


def _report(engine: str) -> dict:
    return {
        "engine_id": f"{engine}/model/voice", "seed": 4, "seconds": 19.5,
        "cues": {
            "problem": {"seconds": 5.0, "frames": 150},
            "rule": {"seconds": 5.0, "frames": 150},
        },
    }


def test_build_default_irodori_and_gemini_config(tmp_path: Path, monkeypatch) -> None:
    _build_inputs(tmp_path, monkeypatch)
    irodori_calls = []
    gemini_calls = []

    def irodori(problem, rule, out_dir, *, config, force):
        irodori_calls.append((problem, config, force))
        return _report("irodori")

    def gemini(problem, rule, out_dir, *, config, force):
        gemini_calls.append((problem, config, force))
        return _report("gemini")

    monkeypatch.setattr(build.narration_irodori, "synthesize_cues", irodori)
    monkeypatch.setattr(build.narration_gemini, "synthesize_cues", gemini)
    assert build._parser().parse_args([]).tts == "irodori"
    assert build.main(["--skip-render"]) == 0
    assert len(irodori_calls) == 2
    assert not gemini_calls
    assert all(call[1]["engine"] == "irodori" for call in irodori_calls)

    assert build.main(["--tts", "gemini", "--skip-render"]) == 0
    assert len(gemini_calls) == 2
    assert all(call[1]["max_tempo"] == 1.19 for call in gemini_calls)
    assert all(call[1]["engine"] == "gemini" for call in gemini_calls)


def test_build_manifest_keeps_irodori_seed_and_seconds(
    tmp_path: Path, monkeypatch
) -> None:
    _build_inputs(tmp_path, monkeypatch)
    saved = []
    monkeypatch.setattr(
        build.narration_irodori, "synthesize_cues", lambda *args, **kwargs: _report("irodori")
    )
    monkeypatch.setattr(build, "render", lambda *args: None)
    monkeypatch.setattr(build, "normalize_loudness", lambda *args: None)
    monkeypatch.setattr(build, "extract_stills", lambda *args: {})
    monkeypatch.setattr(build, "probe_video", lambda *args: {})
    monkeypatch.setattr(build, "inspect_seam", lambda *args: 0.1)
    monkeypatch.setattr(build, "save_manifest", lambda manifest: saved.append(manifest.copy()))

    assert build.main(["--content-key", "001-first"]) == 0
    narration = saved[0]["001-first"]["narration"]
    assert narration["engine_id"] == "irodori/model/voice"
    assert narration["seed"] == 4
    assert narration["seconds"] == 19.5
    assert "tempo" not in narration


def test_build_irodori_budget_continues_but_infer_error_stops(
    tmp_path: Path, monkeypatch
) -> None:
    _build_inputs(tmp_path, monkeypatch)
    calls = []

    def budget(problem, rule, out_dir, *, config, force):
        calls.append(problem)
        if problem == "001-first":
            raise narration_irodori.IrodoriBudgetError(22.0, 21.0, [20.0, 19.5, 19.0])
        return _report("irodori")

    monkeypatch.setattr(build.narration_irodori, "synthesize_cues", budget)
    assert build.main(["--skip-render"]) == 1
    assert calls == ["001-first", "002-next"]

    calls.clear()

    def failed(problem, rule, out_dir, *, config, force):
        calls.append(problem)
        raise narration_irodori.IrodoriError("GPU failed")

    monkeypatch.setattr(build.narration_irodori, "synthesize_cues", failed)
    assert build.main(["--skip-render"]) == 1
    assert calls == ["001-first"]
