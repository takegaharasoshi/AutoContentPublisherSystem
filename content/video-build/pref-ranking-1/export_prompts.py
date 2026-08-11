"""対象ランキングストックの imagegen 用背景プロンプトを書き出す。"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import DURATIONS, WORK, fetch_stock_rows, local_connection, select_targets


# 背景の品質をネタ間で揃え、版面のパレットになじませるため固定する。
# 配色は 17-4a で Fix した「生成り × 淡墨茶 × 金（差し色に朱）」= remotion/src/theme.ts が正。
# 17-2 時点の「藍」は 17-4a で淡墨茶へ差し替えたため、ここに藍を書かない。
STYLE_LINE = (
    "画風: 和モダンのフラットイラスト調。生成り地・淡い墨茶・金の落ち着いた配色で、"
    "写実・写真・3Dは禁止。版面の文字を邪魔しない低コントラストの装飾密度にする。"
)
# Remotion の縦長全面背景をクロップ損失なく作るため出力比率と寸法を固定する。
SIZE_LINE = "画像サイズ: 9:16 の縦長（1080x1920 ピクセル）で出力する。"
# 生成画像内の疑似文字はレビューで修復できないため、独立した強い禁止指定にする。
NO_TEXT_LINE = "文字・数字・記号は一切描かない。"


def build_prompt(bg_motif: str) -> str:
    """背景モチーフへセット固定の生成条件を付加する。"""
    return "\n".join((bg_motif.strip(), STYLE_LINE, SIZE_LINE, NO_TEXT_LINE)) + "\n"


def _parse_durations(value: str) -> tuple[str, ...]:
    values = tuple(item.strip() for item in value.split(",") if item.strip())
    unknown = set(values) - set(DURATIONS)
    if not values or unknown:
        raise argparse.ArgumentTypeError(
            f"尺は {','.join(DURATIONS)} からカンマ区切りで指定してください"
        )
    return values


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild", action="store_true", help="ビルド済み尺の行を対象にする")
    parser.add_argument(
        "--durations", type=_parse_durations, default=DURATIONS,
        help="対象尺（既定: 20s,30s）",
    )
    parser.add_argument(
        "--content-key", action="append", dest="content_keys",
        help="対象 content_key（複数指定可）",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """DB の対象行から 1 行 1 ファイルのプロンプトを生成する。"""
    args = _parser().parse_args(argv)
    connection = local_connection()
    try:
        rows = fetch_stock_rows(connection)
    finally:
        connection.close()
    targets = select_targets(
        rows, args.durations, rebuild=args.rebuild, content_keys=args.content_keys
    )
    output = WORK / "prompts"
    output.mkdir(parents=True, exist_ok=True)
    for row in targets:
        fields = row.get("content_fields")
        motif = fields.get("bg_motif") if isinstance(fields, dict) else None
        if not isinstance(motif, str) or not motif.strip():
            raise RuntimeError(f"{row['content_key']}: content_fields.bg_motif がありません")
        path = output / f"{row['content_key']}.txt"
        path.write_text(build_prompt(motif), encoding="utf-8")
    print(f"{len(targets)} 件のプロンプトを書き出しました: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
