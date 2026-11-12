"""アカウント成長ノート（HTML ページ）を集計結果から組み立てる。

集計ランナーの結果 JSON（growth_account_weekly / growth_post_weekly）を
template.html の ``/*DATA*/`` に埋め込み、out/growth.html を書き出す。
読み取りと書き出しだけを行い、公開はしない（公開は Claude Code の Artifact で行う）。
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[1] / "content" / "insights-analysis" / "results"
EXCLUDED_SETS = {"fantasy-animals-1"}  # 停止済みのセットは載せない


def load(name: str) -> list[dict]:
    """集計結果を読み、載せないセットを除いて返す。

    Args:
        name: 集計ランナーのクエリ名。

    Returns:
        行の辞書のリスト。
    """
    rows = json.loads((RESULTS / f"{name}.json").read_text(encoding="utf-8"))
    return [r for r in rows if r["set_code"] not in EXCLUDED_SETS]


def main() -> None:
    """ページを組み立てて out/growth.html に書き出す。"""
    data = {
        "account": load("growth_account_weekly"),
        "posts": load("growth_post_weekly"),
    }
    if not data["account"] or not data["posts"]:
        raise SystemExit("集計結果が空です。先に run_queries.py を実行してください。")
    template = (HERE / "template.html").read_text(encoding="utf-8")
    if template.count("/*DATA*/") != 1:
        raise SystemExit("template.html の /*DATA*/ が 1 か所ではありません。")
    page = template.replace(
        "/*DATA*/", json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    )
    out = HERE / "out" / "growth.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    latest = max(r["last_date"] for r in data["account"])
    print(f"{out}（{latest} 収集分まで・{len(data['account'])} + {len(data['posts'])} 行）")


if __name__ == "__main__":
    main()
