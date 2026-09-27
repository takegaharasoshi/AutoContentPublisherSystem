"""判定試走で両方式が共有するデータ契約。"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SET_DIR = HERE.parent
BATCH_DIR = SET_DIR / "batch-01"

KINDS = (
    "q_yesno",
    "q_multi",
    "q_open",
    "guess_correct",
    "guess_close",
    "guess_wrong",
    "ask_hint",
    "ask_spoiler",
    "ask_howto",
    "impression",
    "greeting",
    "cheer",
    "chat",
    "request",
    "complaint",
    "mention",
    "emoji_only",
    "troll",
    "abuse",
    "spam",
    "personal_info",
    "foreign",
)


@dataclass(frozen=True)
class Problem:
    """一問分の問題文と正解情報。"""

    no: str
    problem_text: str
    truth: str
    fact_sheet: list[str]
    truth_points: list[str]
    reveal_text: str


@dataclass(frozen=True)
class JudgeResult:
    """コメント判定と返信。"""

    kind: str
    answer: str | None
    reply: str | None
    method: str
    debug: dict[str, Any] = field(default_factory=dict)


def load_problem(no: str) -> Problem:
    """batch-01 の問題素材と試走用真相ポイントを読み込む。"""
    no = str(no)
    if not BATCH_DIR.is_dir():
        raise FileNotFoundError(f"batch-01 素材ディレクトリがありません: {BATCH_DIR}")
    batch_path = str(BATCH_DIR)
    if batch_path not in sys.path:
        sys.path.insert(0, batch_path)
    try:
        from stock_items import ITEMS  # type: ignore[import-not-found]
    except Exception as exc:  # noqa: BLE001 - 入力不足を分かりやすく報告する
        raise RuntimeError(f"batch-01/stock_items.py を読み込めません: {exc}") from exc

    item = next((row for row in ITEMS if str(row.get("no")) == no), None)
    if item is None:
        raise KeyError(f"問題 {no} は batch-01/stock_items.py にありません")

    points_path = HERE / "data" / "truth_points.json"
    if not points_path.is_file():
        raise FileNotFoundError(
            f"試走フィクスチャがありません: {points_path} "
            "（{no: {truth_points: [...], reveal_text: ...}} 形式で作成してください）"
        )
    try:
        points_data = json.loads(points_path.read_text(encoding="utf-8"))
        fixture = points_data[no]
        truth_points = fixture["truth_points"]
        reveal_text = fixture["reveal_text"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError(f"{points_path} の {no} の設定が不正です: {exc}") from exc

    if not isinstance(truth_points, list) or not all(isinstance(point, str) for point in truth_points):
        raise ValueError(f"{points_path} の {no}.truth_points は文字列配列で指定してください")
    if not 2 <= len(truth_points) <= 4:
        raise ValueError(f"{points_path} の {no}.truth_points は 2〜4 項目で指定してください")
    if not isinstance(reveal_text, str):
        raise ValueError(f"{points_path} の {no}.reveal_text は文字列で指定してください")
    if len(reveal_text) > 70:
        raise ValueError(f"{points_path} の {no}.reveal_text は 70 字以内で指定してください")
    return Problem(
        no=no,
        problem_text=str(item["problem_text"]),
        truth=str(item["truth"]),
        fact_sheet=list(item["fact_sheet"]),
        truth_points=truth_points,
        reveal_text=reveal_text,
    )
