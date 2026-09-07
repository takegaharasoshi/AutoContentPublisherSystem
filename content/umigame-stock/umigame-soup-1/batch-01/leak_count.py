"""プローブ結果の補足漏れを数える（21-4a-2 で新設）。

出題者の返答に、質問側には無い「核心語」（問題ごとに手書きの辞書。core 宣言の反転部分の語）が
出た応答を数える。probe_test.py の機械判定（冒頭語）では拾えない「補足で正体を言う」漏れの指標。

使い方: python3 leak_count.py [work/probe_results.json]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
CORE = {
    "U01": ["レントゲン", "病気", "医者", "主治医", "病院", "治療", "写真"],
    "U02": ["始発", "座"], "U03": ["合図", "無事", "耳"], "U04": ["バス", "合図", "知らせ"],
    "U05": ["誕生日", "料理", "うれし"], "U06": ["麺", "うどん"], "U07": ["体重", "ジム", "トレーナー", "減量"],
    "U08": ["玉ねぎ"], "U11": ["救急", "バックミラー", "譲"], "U09": ["ヒーローショー", "悪役", "演技", "スーツアクター", "ショー"], "U10": ["道の駅"],
}
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "work" / "probe_results.json"
d = json.load(open(path, encoding="utf-8"))
allr = d if "U01" in d else d["results"]
tot_q = tot_leak = tot_sup = 0
for no, words in CORE.items():
    recs = [r for r in allr[no] if r["kind"] != "extra"]
    # 正解宣言の返答は真相を開示してよいので数えない
    leak = sum(
        1 for r in recs
        if not r["reply"].startswith("正解") and any(w in r["reply"] and w not in r["q"] for w in words)
    )
    sup = sum(1 for r in recs if len(r["reply"].strip()) > 8)
    mis = sum(1 for r in allr[no] if r["judge"] == "mismatch")
    tot_q += len(recs); tot_leak += leak; tot_sup += sup
    print(f"{no}: 想定質問 {len(recs)} / 補足あり {sup} / 核心語漏れ {leak} / 冒頭語不一致 {mis}")
print(f"合計: 想定質問 {tot_q} / 補足あり {tot_sup} / 核心語漏れ {tot_leak}")
