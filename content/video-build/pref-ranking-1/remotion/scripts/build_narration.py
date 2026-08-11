"""ナレーションを合成し、配置検査済みの Remotion props を生成する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Mapping, TextIO

import build_timeline
from tts import CueAudio, CueRequest, TtsEngine, TtsError, VoicevoxEngine


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SPEED_SCALE = 1.2


class NarrationBuildError(RuntimeError):
    """props またはキャッシュが不正で処理を続行できないことを表す。"""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise NarrationBuildError(f"入力 props がありません: {path}") from exc
    except json.JSONDecodeError as exc:
        raise NarrationBuildError(f"入力 props の JSON が不正です: {exc}") from exc
    if not isinstance(value, dict):
        raise NarrationBuildError("入力 props は JSON オブジェクトにしてください。")
    return value


def _read_manifest(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise NarrationBuildError(f"manifest.json が不正です: {exc}") from exc
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, dict)
        for key, item in value.items()
    ):
        raise NarrationBuildError("manifest.json の形式が不正です。")
    return value


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _entry_names(props: dict[str, Any]) -> dict[int, str]:
    entries = props.get("entries")
    if not isinstance(entries, list):
        raise NarrationBuildError("props の entries は配列にしてください。")
    names: dict[int, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        rank = entry.get("rank")
        name = entry.get("prefName")
        if isinstance(rank, int) and isinstance(name, str):
            names[rank] = name
    return names


def _cue_requests(
    props: dict[str, Any], timeline: build_timeline.Timeline
) -> dict[str, CueRequest]:
    cues = props.get("cues")
    if not isinstance(cues, dict):
        raise NarrationBuildError("props の cues は cue ID をキーにしたオブジェクトにしてください。")
    names = _entry_names(props)
    name_cues = {
        anchor.id: int(anchor.id[1:])
        for anchor in timeline.cue_anchors
        if anchor.align == "name"
    }
    for cue_id, rank in name_cues.items():
        if rank not in names:
            raise NarrationBuildError(
                f"後ろ合わせ cue「{cue_id}」に対応する {rank} 位の entry がありません。"
            )

    requests: dict[str, CueRequest] = {}
    for cue_id, cue in cues.items():
        if not isinstance(cue_id, str) or not isinstance(cue, dict):
            raise NarrationBuildError("props の cues の形式が不正です。")
        text = cue.get("text")
        if not isinstance(text, str):
            raise NarrationBuildError(f"cue「{cue_id}」の text がありません。")
        requests[cue_id] = CueRequest(
            id=cue_id,
            text=text,
            name_text=names[name_cues[cue_id]] if cue_id in name_cues else None,
        )
    return requests


def _manifest_entry(audio: CueAudio, text: str) -> dict[str, Any]:
    return {
        "text": text,
        "speedScale": audio.speed_scale,
        "engineId": audio.engine_id,
        "seconds": audio.seconds,
        "frames": audio.frames,
        "nameOffsetFrames": audio.name_offset_frames,
    }


def _audio_from_manifest(
    cue_id: str,
    out_path: Path,
    entry: Mapping[str, Any],
    *,
    require_identity: tuple[str, float, str] | None = None,
) -> CueAudio | None:
    if require_identity is not None:
        text, speed_scale, engine_id = require_identity
        if (
            entry.get("text") != text
            or entry.get("speedScale") != speed_scale
            or entry.get("engineId") != engine_id
            or not out_path.exists()
        ):
            return None
    seconds = entry.get("seconds")
    frames = entry.get("frames")
    speed_scale = entry.get("speedScale")
    engine_id = entry.get("engineId")
    name_offset = entry.get("nameOffsetFrames")
    if (
        not isinstance(seconds, (int, float))
        or not isinstance(frames, int)
        or not isinstance(speed_scale, (int, float))
        or not isinstance(engine_id, str)
        or (name_offset is not None and not isinstance(name_offset, int))
    ):
        return None
    return CueAudio(
        id=cue_id,
        path=out_path,
        seconds=float(seconds),
        frames=frames,
        name_offset_frames=name_offset,
        speed_scale=float(speed_scale),
        engine_id=engine_id,
    )


def _synthesize_requests(
    requests: Mapping[str, CueRequest],
    audio_dir: Path,
    manifest: dict[str, dict[str, Any]],
    engine: TtsEngine,
    speed_scale: float,
    *,
    force_ids: set[str],
) -> dict[str, CueAudio]:
    engine_id = engine.engine_id
    audios: dict[str, CueAudio] = {}
    for cue_id, request in requests.items():
        out_path = audio_dir / f"{cue_id}.wav"
        entry = manifest.get(cue_id, {})
        cached = None
        if cue_id not in force_ids:
            cached = _audio_from_manifest(
                cue_id,
                out_path,
                entry,
                require_identity=(request.text, speed_scale, engine_id),
            )
        audio = cached or engine.synthesize(
            request, out_path, speed_scale=speed_scale
        )
        audios[cue_id] = audio
        manifest[cue_id] = _manifest_entry(audio, request.text)
    return audios


def _dry_run_audios(
    requests: Mapping[str, CueRequest],
    audio_dir: Path,
    manifest: Mapping[str, Mapping[str, Any]],
) -> dict[str, CueAudio]:
    audios: dict[str, CueAudio] = {}
    for cue_id in requests:
        entry = manifest.get(cue_id)
        audio = (
            _audio_from_manifest(cue_id, audio_dir / f"{cue_id}.wav", entry)
            if entry is not None
            else None
        )
        if audio is None:
            raise NarrationBuildError(
                f"cue「{cue_id}」の manifest 実測値がありません。先に音声を合成してください。"
            )
        audios[cue_id] = audio
    return audios


def _resolve(
    timeline: build_timeline.Timeline, audios: Mapping[str, CueAudio]
) -> build_timeline.ResolvedCues:
    measures = {
        cue_id: build_timeline.CueMeasure(
            frames=audio.frames,
            name_offset_frames=audio.name_offset_frames,
        )
        for cue_id, audio in audios.items()
    }
    return build_timeline.resolve_cue_frames(timeline, measures)


def _print_report(
    timeline: build_timeline.Timeline,
    result: build_timeline.ResolvedCues,
    stream: TextIO,
) -> None:
    print("cue ID | 開始 | 長さ | 終端 | 次 cue 間隔 | 県名遅れ | 判定", file=stream)
    ordered = sorted(timeline.cue_anchors, key=lambda item: item.anchor)
    violation_ids = {item.id for item in result.violations}
    for index, anchor in enumerate(ordered):
        cue = result.cues[anchor.id]
        end = cue.start_frame + cue.frames
        next_start = (
            result.cues[ordered[index + 1].id].start_frame
            if index + 1 < len(ordered)
            else timeline.total
        )
        lag = str(cue.name_lag_frames) if cue.align == "name" else "-"
        status = "違反" if anchor.id in violation_ids else "OK"
        print(
            f"{anchor.id} | {cue.start_frame} | {cue.frames} | {end} | "
            f"{next_start - end} | {lag} | {status}",
            file=stream,
        )
    if result.violations:
        print("\n違反一覧:", file=stream)
        for violation in result.violations:
            print(
                f"- {violation.id} [{violation.kind}] {violation.message}",
                file=stream,
            )


def build_narration(
    props_path: Path,
    *,
    engine: TtsEngine,
    out_path: Path | None = None,
    name: str | None = None,
    speed_scale: float = DEFAULT_SPEED_SCALE,
    force: bool = False,
    dry_run: bool = False,
    stdout: TextIO = sys.stdout,
) -> int:
    """合成・配置検査を行い、成功時だけ解決済み props を書き出す。"""
    if speed_scale <= 0 or speed_scale > 1.2:
        raise NarrationBuildError("話速は 0 より大きく 1.2 以下にしてください。")

    props_path = Path(props_path)
    props = _read_json(props_path)
    duration = props.get("duration")
    if duration not in build_timeline.DURATION_SPECS:
        raise NarrationBuildError(f"未対応の duration です: {duration}")
    timeline = build_timeline.build_timeline(
        duration, build_timeline.DURATION_SPECS[duration]
    )
    requests = _cue_requests(props, timeline)
    output_name = name or props_path.stem
    audio_dir = PROJECT_DIR / "public" / "narration" / output_name
    manifest_path = audio_dir / "manifest.json"
    manifest = _read_manifest(manifest_path)

    if dry_run:
        audios = _dry_run_audios(requests, audio_dir, manifest)
    else:
        audios = _synthesize_requests(
            requests,
            audio_dir,
            manifest,
            engine,
            speed_scale,
            force_ids=set(requests) if force else set(),
        )
        _write_json(manifest_path, manifest)

    result = _resolve(timeline, audios)
    _print_report(timeline, result, stdout)
    if not result.ok:
        return 1

    cue_props = props["cues"]
    for cue_id, cue in result.cues.items():
        if cue_id not in cue_props:
            continue
        cue_props[cue_id]["audioSrc"] = (
            Path("narration") / output_name / f"{cue_id}.wav"
        ).as_posix()
        cue_props[cue_id]["startFrame"] = cue.start_frame
        cue_props[cue_id]["frames"] = cue.frames
    _write_json(Path(out_path) if out_path is not None else props_path, props)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("props", type=Path, help="Remotion に渡す props JSON")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED_SCALE, help="既定話速")
    parser.add_argument("--engine", default="http://127.0.0.1:50021", help="VOICEVOX Engine URL")
    parser.add_argument("--speaker", type=int, default=12, help="VOICEVOX 話者 ID")
    parser.add_argument("--out", type=Path, help="解決済み props の出力先")
    parser.add_argument("--name", help="public/narration/ 配下の出力名")
    parser.add_argument("--force", action="store_true", help="キャッシュを使わず全 cue を再合成")
    parser.add_argument("--dry-run", action="store_true", help="manifest の実測値だけで再検査")
    return parser


def main(
    argv: list[str] | None = None, *, engine: TtsEngine | None = None
) -> int:
    """CLI 引数を解釈し、利用者向けエラーを表示して終了コードを返す。"""
    args = _parser().parse_args(argv)
    selected_engine = engine or VoicevoxEngine(
        base_url=args.engine, speaker=args.speaker
    )
    try:
        return build_narration(
            args.props,
            engine=selected_engine,
            out_path=args.out,
            name=args.name,
            speed_scale=args.speed,
            force=args.force,
            dry_run=args.dry_run,
        )
    except (NarrationBuildError, TtsError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
