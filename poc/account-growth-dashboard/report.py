"""週 1 回の届くレポート（LINE 用の数行の文面）を集計結果から組み立てる。

既定では文面を標準出力に出すだけ。``--send`` を付けたときだけ LINE の Messaging API で
プッシュ送信する（``LINE_CHANNEL_ACCESS_TOKEN`` と ``LINE_USER_ID`` が必要。環境変数に
無ければ ``~/.bashrc`` の ``export`` 行から読む — 無人の実行では ``~/.bashrc`` が読み込まれないため）。
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import urllib.request
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[1] / "content" / "insights-analysis" / "results"
PAGE_URL = "https://claude.ai/artifact/NMPNxbEYTwtC8AVQDSFwBk"
# 表示名と節目の人数（仮置き）。template.html の SETS と同じ値にそろえる
SETS: list[tuple[str, str, list[int]]] = [
    ("logic-training-1", "脳みそコーチ", [100, 200, 300, 350, 400, 500, 750, 1000]),
    ("pref-ranking-1", "都道府県ランキング", [10, 25, 50, 100, 200, 300, 500, 1000]),
    ("umigame-soup-1", "ウミガメのスープ", [10, 25, 50, 100, 200, 300, 500, 1000]),
]


def load(name: str) -> list[dict]:
    """集計結果を読む。

    Args:
        name: 集計ランナーのクエリ名。

    Returns:
        行の辞書のリスト。
    """
    return json.loads((RESULTS / f"{name}.json").read_text(encoding="utf-8"))


def md(day: date) -> str:
    """日付を「月/日」にする。"""
    return f"{day.month}/{day.day}"


def signed(value: int) -> str:
    """増減を符号つきで書く。"""
    return f"+{value:,}" if value > 0 else ("±0" if value == 0 else f"−{abs(value):,}")


def build_report() -> str:
    """最新の「7 日そろった週」についての文面を組み立てる。

    Returns:
        LINE に送る文面。
    """
    account = load("growth_account_weekly")
    posts = load("growth_post_weekly")
    full_weeks = sorted({r["week_from"] for r in account if int(r["days"]) == 7})
    week = full_weeks[-1]
    start = date.fromisoformat(week)
    lines: list[str] = []
    events: list[str] = []
    total = 0
    total_gain = 0
    for code, name, milestones in SETS:
        rows = sorted(
            (r for r in account if r["set_code"] == code and r["followers_end"] is not None),
            key=lambda r: r["week_from"],
        )
        by_week = {r["week_from"]: int(r["followers_end"]) for r in rows}
        if week not in by_week:
            continue
        now = by_week[week]
        prev = by_week.get((start - timedelta(days=7)).isoformat())
        gain = now - prev if prev is not None else 0
        total += now
        total_gain += gain
        line = f"{name} {now:,} 人（{signed(gain)}）"
        nxt = next((m for m in milestones if m > now), None)
        if nxt is not None:
            line += f" 次の {nxt:,} まであと {nxt - now:,}"
        lines.append(line)
        reached = [m for m in milestones if prev is not None and prev < m <= now]
        if reached:
            events.append(f"{name}が {reached[-1]:,} 人に到達")
        # 開始からの歩み（フォロワーが初めて 1 人以上になった週から数える）
        first = next((r for r in rows if int(r["followers_end"]) > 0), None)
        if first is not None and first["week_from"] != week:
            n_weeks = (start - date.fromisoformat(first["week_from"])).days // 7
            lines.append(f"　{n_weeks} 週で {int(first['followers_end']):,} → {now:,}")
        views = sorted(
            (r for r in posts if r["set_code"] == code and r["week_from"] <= week),
            key=lambda r: r["week_from"],
        )
        if views and views[-1]["week_from"] == week:
            latest = float(views[-1]["median_views_72h"])
            if len(views) > 1 and latest > max(float(r["median_views_72h"]) for r in views[:-1]):
                events.append(f"{name}の再生（中央値）がこれまでの最高 {latest:,.0f}")
    end = start + timedelta(days=6)
    head = [f"成長ノート {md(start)}〜{md(end)} の週", f"合計 {total:,} 人（先週 {signed(total_gain)}）", ""]
    tail = ["", *[f"★ {e}" for e in events], PAGE_URL]
    return "\n".join([*head, *lines, *tail]).replace("\n\n\n", "\n\n")


def setting(name: str) -> str | None:
    """送信の設定値を、環境変数 → ``~/.bashrc`` の ``export`` 行の順に探す。

    Args:
        name: 変数名。

    Returns:
        値。どちらにも無ければ None。
    """
    value = os.environ.get(name)
    if value:
        return value
    bashrc = Path.home() / ".bashrc"
    if not bashrc.exists():
        return None
    found = None
    for line in bashrc.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(f"export {name}="):
            parts = shlex.split(line[len("export "):])
            if parts:
                found = parts[0].split("=", 1)[1]
    return found


def send(text: str) -> None:
    """LINE の Messaging API でプッシュ送信する。

    Args:
        text: 送る文面。

    Raises:
        SystemExit: 設定値が足りないとき。
    """
    token = setting("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = setting("LINE_USER_ID")
    if not token or not user_id:
        raise SystemExit("LINE_CHANNEL_ACCESS_TOKEN と LINE_USER_ID を環境変数か ~/.bashrc に入れてください。")
    body = json.dumps({"to": user_id, "messages": [{"type": "text", "text": text}]}).encode("utf-8")
    request = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        print(f"LINE 送信: HTTP {response.status}")


def main() -> None:
    """文面を出し、指定があれば送信する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--send", action="store_true", help="LINE に送信する（既定は文面を出すだけ）")
    args = parser.parse_args()
    text = build_report()
    print(text)
    if args.send:
        send(text)


if __name__ == "__main__":
    main()
