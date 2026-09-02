"""1 問分の Remotion props JSON を、ローカル DB と work/ の資材から組む。

ホスト側（WSL）で実行する。Pillow を使わずに済むよう、イラストの実寸は
PNG の IHDR チャンクから直接読む（枠へ内接させた矩形の計算に使う）。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import struct
import sys

BASE = Path(__file__).resolve().parents[2]  # content/video-build/logic-training-1
sys.path.insert(0, str(BASE))

from common import WORK, local_connection  # noqa: E402

REMOTION = BASE / "remotion"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _png_size(path: Path) -> tuple[int, int]:
    """Read one PNG's pixel size from its IHDR chunk."""
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != PNG_SIGNATURE:
        raise RuntimeError(f"PNG ではありません: {path}")
    width, height = struct.unpack(">II", header[16:24])
    return int(width), int(height)


def _slot_of(connection, quiz_type: str, difficulty: str) -> dict[str, str]:
    """Resolve the palette slot for one type/difficulty pair from prompt_configs."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT p.parameters FROM prompt_configs p "
            "JOIN batch_sets b ON b.id = p.set_id "
            "WHERE b.set_code = 'logic-training-1' AND p.is_active = 1"
        )
        rows = cursor.fetchall()
    matches = []
    for (parameters,) in rows:
        payload = json.loads(parameters) if isinstance(parameters, str) else parameters
        for slot in payload.get("slots", []):
            if slot["quiz_type"] == quiz_type and slot["difficulty"] == difficulty:
                matches.append(slot)
    unique = {
        (slot["slot_code"], slot["slot_label"], slot["slot_hook"]) for slot in matches
    }
    if len(unique) != 1:
        raise RuntimeError(
            f"slot が一意に決まりません: quiz_type={quiz_type} difficulty={difficulty}"
        )
    slot_code, slot_label, slot_hook = next(iter(unique))
    return {"slot_code": slot_code, "slot_label": slot_label, "slot_hook": slot_hook}


def main() -> None:
    """Emit props JSON and stage the illustration under remotion/public/."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--item", type=int, required=True, help="quiz_stock_items.id")
    args = parser.parse_args()

    connection = local_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT q.content_key, q.quiz_type, q.difficulty, q.question_text, "
                "q.content_fields FROM quiz_stock_items q "
                "JOIN batch_sets b ON b.id = q.set_id "
                "WHERE b.set_code = 'logic-training-1' AND q.id = %s",
                (args.item,),
            )
            row = cursor.fetchone()
        if row is None:
            raise RuntimeError(f"quiz_stock_items に見つかりません: id={args.item}")
        content_key, quiz_type, difficulty, question_text, content_fields = row
        fields = (
            json.loads(content_fields)
            if isinstance(content_fields, str)
            else content_fields
        )
        slot = _slot_of(connection, str(quiz_type), str(difficulty))
    finally:
        connection.close()

    source = WORK / "illustrations" / f"{args.item}.png"
    if not source.is_file():
        raise RuntimeError(f"イラストがありません: {source}")
    staged = REMOTION / "public" / "illustrations" / f"{args.item}.png"
    staged.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, staged)
    width, height = _png_size(staged)

    props = {
        "slotCode": slot["slot_code"],
        "slotLabel": slot["slot_label"],
        "slotHook": slot["slot_hook"],
        "question": str(question_text),
        "hint": str(fields["hint"]),
        "illustrationSrc": f"illustrations/{args.item}.png",
        "illustrationWidth": width,
        "illustrationHeight": height,
    }
    destination = REMOTION / "work" / "props" / f"{args.item}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{destination} ({content_key} / {slot['slot_code']} / {width}x{height})")


if __name__ == "__main__":
    main()
