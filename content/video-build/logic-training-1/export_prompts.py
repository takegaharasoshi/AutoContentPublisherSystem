"""Export imagegen prompts for active, unbuilt logic-training-1 stock items."""

from __future__ import annotations

from common import WORK, fetch_unbuilt_items, local_connection, resolve_slots
from app.generators.gpt_quiz_multicut import _build_illustration_prompt


STYLE_LINE = (
    "画風: フラットデザインのベクターイラスト調（単純な形状・均一な塗り・柔らかい輪郭）。"
    "写実調・写真調・3D 調は禁止。全ての生成で同一の画風に統一する。"
)
# 組版のブロックは 3:2。これ以外の比率で出力されると intake の中央クロップで
# 左右が捨てられ、被写体が見切れる（16-5 のユーザー指摘）。imagegen は指定しないと
# 16:9 前後で出力が揺れるため、サイズを明示する
SIZE_LINE = (
    "画像サイズ: 3:2 の横長（1536x1024 ピクセル）で出力する。"
    "他の縦横比では出力しない。"
)


def main() -> None:
    """Write one code-owned image prompt text file for each build target."""
    connection = local_connection()
    try:
        slots = resolve_slots(connection)
        items = fetch_unbuilt_items(connection)
    finally:
        connection.close()
    output = WORK / "prompts"
    output.mkdir(parents=True, exist_ok=True)
    for item in items:
        key = (item["quiz_type"], item["difficulty"])
        if key not in slots:
            raise RuntimeError(f"No prompt_configs slot for stock item {item['id']}: {key}")
        scene = item["content_fields"].get("illustration_scene")
        if not isinstance(scene, str) or not scene.strip():
            raise RuntimeError(f"Stock item {item['id']} has no illustration_scene")
        prompt = _build_illustration_prompt(scene, slots[key]["slot_code"])
        (output / f"{item['id']}.txt").write_text(
            f"{prompt}\n{STYLE_LINE}\n{SIZE_LINE}\n", encoding="utf-8"
        )
    print(f"exported {len(items)} prompts to {output}")


if __name__ == "__main__":
    main()
