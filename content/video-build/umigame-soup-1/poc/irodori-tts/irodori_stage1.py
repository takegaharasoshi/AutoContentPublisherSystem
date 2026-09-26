"""Irodori で問題文 + ルール文を 1 回で合成する（声・演技の比較用）。Irodori の venv で実行。"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

IRODORI = Path.home() / "tools" / "Irodori-TTS"
SET = Path("/home/takegaharawork/projects/AutoContentPublisherSystem/content/video-build/umigame-soup-1")
NARR = SET / "work" / "narration"
OUT = SET / "work" / "irodori-poc"
POC2 = IRODORI / "outputs" / "poc2"
G4_CLEAN = sorted((SET / "assets" / "voice" / "kamerock-g4").glob("*.wav"))
V2 = sorted((POC2 / "voice2_clips" / "1").glob("clip*.wav"))
PROBLEMS = ["016-umigame-soup", "008-who-made-the-mistake"]
STYLE = "子供に語り掛ける優しいパパの口調で、とっておきの謎を得意げに語り、続けて同じ口調のまま親しげに呼びかける。間は短く、早口ぎみの速いテンポで。"


def emoji_text(problem: str, rule: str) -> str:
    """冒頭に 🫶（優しく）、最後の問いかけの前に 😎（得意げ）、ルール文の前に 😊（楽しげ）。"""
    sentences = re.findall(r"[^。？]+[。？]", problem)
    if sentences and sentences[-1].endswith("？"):
        body = "".join(sentences[:-1])
        problem = f"🫶{body}😎{sentences[-1]}"
    else:
        problem = f"🫶{problem}"
    return f"{problem} 😊{rule}"


VARIANTS = {
    "g4c": {"refs": G4_CLEAN, "caption": None, "emoji": False, "extra": [],
            "label": "G4（① 息を下げた参照・演技指示なし）"},
    "v2": {"refs": V2, "caption": None, "emoji": False, "extra": [],
           "label": "voice2（演技指示なし）"},
    "v2a": {"refs": V2, "caption": STYLE, "emoji": False, "extra": [],
            "label": "voice2 + 演技の説明文（G4 と同じ文）"},
    "v2b": {"refs": V2, "caption": STYLE, "emoji": False,
            "extra": ["--cfg-scale-caption", "5.0", "--cfg-scale-speaker", "3.5"],
            "label": "voice2 + 演技の説明文を強めに（説明文 5.0 / 声 3.5）"},
    "v2c": {"refs": V2, "caption": STYLE, "emoji": True, "extra": [],
            "label": "voice2 + 演技の説明文 + 絵文字（🫶 優しく・😎 得意げ・😊 楽しげ）"},
}


def main() -> None:
    only = set(sys.argv[1:])
    meta = {}
    for key in PROBLEMS:
        texts = json.loads((NARR / key / "narration.json").read_text(encoding="utf-8"))["texts"]
        for vid, v in VARIANTS.items():
            if only and vid not in only:
                continue
            out_dir = OUT / key / vid
            out_dir.mkdir(parents=True, exist_ok=True)
            text = emoji_text(texts["problem"], texts["rule"]) if v["emoji"] else f"{texts['problem']} {texts['rule']}"
            cmd = [
                "uv", "run", "--no-sync", "python", "infer.py",
                "--hf-checkpoint", "Aratako/Irodori-TTS-v4.1-Small",
                "--model-device", "cuda", "--codec-device", "cuda",
                "--model-precision", "bf16", "--codec-precision", "bf16",
                "--seed", "1", "--seconds", "20.0", "--text", text,
                "--ref-wavs", *map(str, v["refs"]),
                "--output-wav", str(out_dir / "irodori_raw.wav"), *v["extra"],
            ]
            if v["caption"]:
                cmd += ["--caption", v["caption"]]
            with open(OUT / "infer.log", "a", encoding="utf-8") as log:
                subprocess.run(cmd, cwd=IRODORI, check=True, stdout=log, stderr=subprocess.STDOUT)
            meta[f"{key}/{vid}"] = {"text": text, "caption": v["caption"], "extra": v["extra"],
                                    "label": v["label"], "refs": [p.name for p in v["refs"]]}
            print(key, vid, "done", flush=True)
    (OUT / "stage1.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
