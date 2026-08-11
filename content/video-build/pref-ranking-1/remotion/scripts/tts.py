"""TTS エンジンを差し替え可能にする音声合成アダプタ。"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Protocol, Sequence
import urllib.error
import urllib.parse
import urllib.request
import wave


class TtsError(RuntimeError):
    """音声合成または計測に失敗したことを表す。"""


# query の音素長から予測した秒数と WAV 実測長の許容差。第 1 バッチ 10 件 × 2 尺 ×
# 話速 1.1 / 1.2 の全 cue で実測したところ、中央値 0.01 秒・最大 0.06 秒（語尾上げのある
# 疑問形 cue）だったため、実測の最大値に少し余裕を持たせた値にしている。
LENGTH_TOLERANCE_SECONDS = 0.08

DEFAULT_INTONATION_SCALE = 1.9
"""抑揚。17-4d でユーザーが 6 案（抑揚 1.5〜1.9 × 音高 0 / +0.03）の実音声を比較して選定した値。

既定の 1.2 は棒読みに聞こえるとの判断（セット別設計書 pref-ranking-1.html セクション 7）。
話者・話速とあわせて ``engine_id`` に載せ、変えたら合成キャッシュが無効になるようにしている。
"""


@dataclass(frozen=True)
class CueRequest:
    """TTS エンジンへ渡す cue 単位の合成要求。"""

    id: str
    text: str
    name_text: str | None = None


@dataclass(frozen=True)
class CueAudio:
    """合成済み音声と、タイムライン解決に使う実測値。"""

    id: str
    path: Path
    seconds: float
    frames: int
    name_offset_frames: int | None
    speed_scale: float
    engine_id: str


class TtsEngine(Protocol):
    """TTS 実装が満たす最小インターフェース。"""

    @property
    def engine_id(self) -> str:
        """証跡とキャッシュ判定に使うエンジン識別子を返す。"""
        ...

    def synthesize(
        self, request: CueRequest, out_path: Path, *, speed_scale: float
    ) -> CueAudio:
        """cue を音声ファイルへ合成し、実測値を返す。"""
        ...


def mora_entries(query: dict[str, Any]) -> list[tuple[str, float]]:
    """VOICEVOX の query を発話順のモーラ文字列と長さへ展開する。"""
    entries: list[tuple[str, float]] = []
    for phrase in query.get("accent_phrases", []):
        moras = phrase.get("moras", [])
        for mora in moras:
            entries.append(
                (
                    mora["text"],
                    (mora.get("consonant_length") or 0)
                    + (mora.get("vowel_length") or 0),
                )
            )
        # 疑問形の語尾上げ（enable_interrogative_upspeak の既定 = 有効）は、合成時に
        # 末尾モーラの母音をもう 1 つ足す。query には現れないため、ここで補う。
        # 文字列は空にしておく（県名のモーラ列と誤って一致させないため）。
        if moras and phrase.get("is_interrogative"):
            last = moras[-1]
            if str(last.get("vowel", "")).lower() in ("a", "i", "u", "e", "o"):
                entries.append(("", last.get("vowel_length") or 0))
        pause = phrase.get("pause_mora")
        if pause is not None:
            entries.append(
                (
                    pause["text"],
                    (pause.get("consonant_length") or 0)
                    + (pause.get("vowel_length") or 0),
                )
            )
    return entries


def query_seconds(query: dict[str, Any]) -> float:
    """VOICEVOX query の音素長から合成音声の予測秒数を返す。"""
    mora_seconds = sum(length for _, length in mora_entries(query))
    return (
        (query.get("prePhonemeLength") or 0)
        + (query.get("postPhonemeLength") or 0)
        + mora_seconds
    ) / query["speedScale"]


def name_offset_seconds(
    query: dict[str, Any], name_moras: Sequence[str]
) -> float | None:
    """cue 内で右端にある県名モーラの発話開始秒を返す。"""
    if not name_moras:
        return None
    entries = mora_entries(query)
    texts = [text for text, _ in entries]
    width = len(name_moras)
    for index in range(len(texts) - width, -1, -1):
        if texts[index : index + width] == list(name_moras):
            leading = sum(length for _, length in entries[:index])
            return ((query.get("prePhonemeLength") or 0) + leading) / query[
                "speedScale"
            ]
    return None


def seconds_to_frames(seconds: float, fps: int) -> int:
    """秒数を指定 fps のフレーム数へ四捨五入する。"""
    return round(seconds * fps)


class VoicevoxEngine:
    """VOICEVOX Engine の HTTP API を利用する TTS 実装。"""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:50021",
        speaker: int = 12,
        intonation_scale: float = DEFAULT_INTONATION_SCALE,
        fps: int = 30,
        timeout: float = 60.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.speaker = speaker
        self.intonation_scale = intonation_scale
        self.fps = fps
        self.timeout = timeout
        self._engine_id: str | None = None

    @property
    def engine_id(self) -> str:
        """VOICEVOX のバージョンを初回だけ取得して合成条件の識別子を返す。"""
        if self._engine_id is None:
            version = self._request_json("GET", "/version")
            if not isinstance(version, str):
                raise TtsError("VOICEVOX Engine のバージョン応答が不正です。")
            self._engine_id = (
                f"voicevox/{version}/speaker{self.speaker}"
                f"/int{self.intonation_scale:g}"
            )
        return self._engine_id

    def synthesize(
        self, request: CueRequest, out_path: Path, *, speed_scale: float
    ) -> CueAudio:
        """VOICEVOX で cue を合成し、WAV と発話位置を計測する。"""
        query = self._audio_query(request.text)
        query["speedScale"] = speed_scale
        query["intonationScale"] = self.intonation_scale
        wav_data = self._request_bytes(
            "POST",
            "/synthesis",
            query={"speaker": str(self.speaker)},
            body=json.dumps(query, ensure_ascii=False).encode("utf-8"),
            content_type="application/json",
        )

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(wav_data)
        try:
            with wave.open(str(out_path), "rb") as wav_file:
                seconds = wav_file.getnframes() / wav_file.getframerate()
        except (wave.Error, EOFError, OSError) as exc:
            raise TtsError(
                f"cue「{request.id}」の WAV 実測長を取得できません: {exc}"
            ) from exc

        expected_seconds = query_seconds(query)
        if abs(expected_seconds - seconds) > LENGTH_TOLERANCE_SECONDS:
            raise TtsError(
                f"cue「{request.id}」の query 予測長 {expected_seconds:.3f} 秒と "
                f"WAV 実測長 {seconds:.3f} 秒の差が "
                f"{LENGTH_TOLERANCE_SECONDS} 秒を超えています。"
            )

        offset_frames: int | None = None
        if request.name_text is not None:
            name_query = self._audio_query(request.name_text)
            name_moras = [text for text, _ in mora_entries(name_query)]
            offset_seconds = name_offset_seconds(query, name_moras)
            if offset_seconds is None:
                cue_moras = [text for text, _ in mora_entries(query)]
                raise TtsError(
                    f"cue「{request.id}」に県名「{request.name_text}」のモーラ列が"
                    f"見つかりません。cue のモーラ列: {cue_moras}"
                )
            offset_frames = seconds_to_frames(offset_seconds, self.fps)

        return CueAudio(
            id=request.id,
            path=out_path,
            seconds=seconds,
            frames=seconds_to_frames(seconds, self.fps),
            name_offset_frames=offset_frames,
            speed_scale=speed_scale,
            engine_id=self.engine_id,
        )

    def _audio_query(self, text: str) -> dict[str, Any]:
        result = self._request_json(
            "POST",
            "/audio_query",
            query={"text": text, "speaker": str(self.speaker)},
        )
        if not isinstance(result, dict):
            raise TtsError("VOICEVOX Engine の audio_query 応答が不正です。")
        return result

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
    ) -> Any:
        data = self._request_bytes(method, path, query=query)
        try:
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TtsError(
                f"VOICEVOX Engine の応答 JSON を読み取れません: {exc}"
            ) from exc

    def _request_bytes(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        body: bytes | None = None,
        content_type: str | None = None,
    ) -> bytes:
        suffix = f"?{urllib.parse.urlencode(query)}" if query else ""
        request = urllib.request.Request(
            f"{self.base_url}{path}{suffix}", data=body, method=method
        )
        if content_type is not None:
            request.add_header("Content-Type", content_type)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as exc:
            raise TtsError(
                f"VOICEVOX Engine への接続に失敗しました: {exc}。"
                "VOICEVOX Engine を起動してください。"
            ) from exc
