"""21-6b 検討ページ（docs/app/sets/umigame-soup-1-judge-study.html）を試走キャッシュから組み立てる。

図と数値は work/trial_results*.json（gitignore・ローカルにだけある）から計算し、本文は下のテンプレートに直書きしている。
試行を足すときは: 前回のキャッシュを work/trial_results_runN.json として残す → run_trial.py を回す →
TRIALS と試走の実費の計算に足す → 3.3 の記録と 4〜7 章の本文を書き換える → このスクリプトを実行する。

使い方: services/image-batch/.venv/bin/python build_study_page.py（リポジトリのどこから実行してもよい）
"""
import html
import json
from pathlib import Path

TRIAL = Path(__file__).resolve().parent
ROOT = TRIAL.parents[3]
OUT = ROOT / "docs/app/sets/umigame-soup-1-judge-study.html"

KINDS = [
    ("q_yesno", "① はい / いいえ質問"), ("q_multi", "② 複数の質問"), ("q_open", "③ 答えられない質問"),
    ("guess_correct", "④ 正解推理"), ("guess_close", "⑤ 惜しい推理"), ("guess_wrong", "⑥ 外れた推理"),
    ("ask_hint", "⑦ ヒント要求"), ("ask_spoiler", "⑧ ネタバレ要求"), ("ask_howto", "⑨ 遊び方の質問"),
    ("impression", "⑩ 感想"), ("greeting", "⑪ 挨拶"), ("cheer", "⑫ 応援"), ("chat", "⑬ 雑談"),
    ("request", "⑭ リクエスト"), ("complaint", "⑮ 指摘・クレーム"), ("mention", "⑯ メンション"),
    ("emoji_only", "⑰ 絵文字だけ"), ("troll", "⑱ 荒らし"), ("abuse", "⑲ 誹謗中傷"),
    ("spam", "⑳ 宣伝・スパム"), ("personal_info", "㉑ 個人情報"), ("foreign", "㉒ 外国語"),
]
KIND_LABEL = dict(KINDS)
GROUPS = {"q": ["q_yesno", "q_multi", "q_open"], "g": ["guess_correct", "guess_close", "guess_wrong"]}


def load(p):
    r = json.load(open(p, encoding="utf-8"))["results"]
    return r if isinstance(r, list) else list(r.values())


import sys as _sys
_sys.path.insert(0, str(TRIAL))
from run_trial import apply_labels as _apply_labels, load_cases as _load_cases  # noqa: E402

_CASES = {c["id"]: c for c in _load_cases()}


def _relabel(rs):
    # 最新のラベル（ユーザー確認の反映・別解）で数え直す。今は無いケース（名前を変えた旧 id）はそのまま
    return [_apply_labels(x, _CASES[x["id"]]) if x["id"] in _CASES else x for x in rs]


R = _relabel(load(TRIAL / "work/trial_results.json"))
R1 = _relabel(load(TRIAL / "work/trial_results_run1.json"))
R2 = _relabel(load(TRIAL / "work/trial_results_run2.json"))
R3 = _relabel(load(TRIAL / "work/trial_results_run3.json"))
R4 = _relabel(load(TRIAL / "work/trial_results_run4.json"))
R5 = _relabel(load(TRIAL / "work/trial_results_run5.json"))
R6A = _relabel(load(TRIAL / "work/trial_results_run6a.json"))
R6 = _relabel(load(TRIAL / "work/trial_results_run6.json"))
R7X = _relabel(load(TRIAL / "work/trial_results_run7_429.json"))
R7A = _relabel(load(TRIAL / "work/trial_results_run7a.json"))
R7 = _relabel(load(TRIAL / "work/trial_results_run7.json"))
R8A = _relabel(load(TRIAL / "work/trial_results_run8a.json"))


def rows(res, m):
    return [x for x in res if x["method"] == m]


def acc(rs, pred=lambda x: True):
    s = [x for x in rs if pred(x)]
    ok = sum(x["kind"] == x["expected_kind"] for x in s)
    return ok, len(s)


def yesno(rs):
    s = [x for x in rs if x["expected_kind"] == "q_yesno"]
    def ok(x):
        if x["answer"] == x["expected_answer"]:
            return True
        return (x["expected_answer"] == "irrelevant" and x["answer"] == "no"
                and any(w in x["comment_text"] for w in ("関係", "重要", "大事")))
    return sum(x["kind"] == "q_yesno" and ok(x) for x in s), len(s)


def pct(a, b):
    return 100.0 * a / b if b else 0.0


stats = {}
for m in ("p1", "p2"):
    rs = rows(R, m)
    stats[m] = {
        "全体": acc(rs),
        "質問系 ①〜③": acc(rs, lambda x: x["expected_kind"] in GROUPS["q"]),
        "推理系 ④〜⑥": acc(rs, lambda x: x["expected_kind"] in GROUPS["g"]),
        "その他 ⑦〜㉒": acc(rs, lambda x: x["expected_kind"] not in GROUPS["q"] + GROUPS["g"]),
        "① の判定（はい / いいえ）": yesno(rs),
        "kinds": {k: acc(rs, lambda x, k=k: x["expected_kind"] == k) for k, _ in KINDS},
    }
run1_p2 = acc(rows(R1, "p2"))


def _yn(m, blind):
    rs = [x for x in rows(R, m) if ("-b" in x["id"]) == blind]
    return yesno(rs)


def yn_old(m):
    ok, n = _yn(m, False)
    return f"{ok}/{n}（{pct(ok, n):.0f}%）"


def yn_new(m):
    ok, n = _yn(m, True)
    return f"{ok}/{n}（{pct(ok, n):.0f}%）"


def _cost(res, m):
    rs = rows(res, m)
    if m == "p1":
        return sum((x["debug"].get("prompt_tokens", 0) or 0) * 0.10
                   + (x["debug"].get("completion_tokens", 0) or 0) * 0.50 for x in rs) / 1e6
    return sum((x["debug"].get("input_tokens", 0) or 0) for x in rs) * 0.042 / 1e6


_tc = []
_total = 0.0
for n, res in ((1, R1), (2, R2), (3, R3), (4, R4), (5, R5), (6, R6), (7, R7), (8, R)):
    c1 = 0.0 if n == 2 else _cost(res, "p1")  # 試行 2 のパターン 1 は試行 1 の結果を流用（実費なし）
    c2 = _cost(res, "p2") + (_cost(R6A, "p2") if n == 6 else 0.0)  # 試行 6 は 6a と 6b の 2 回分
    if n == 7:  # 試行 7 は 7（レート制限で一部失敗）・7a（パターン 1 だけ再実行）・7b の 3 回分
        c1 += _cost(R7X, "p1") + _cost(R7A, "p1")
        c2 += _cost(R7X, "p2")
    if n == 8:  # 試行 8 は 8a と 8b の 2 回分
        c1 += _cost(R8A, "p1")
        c2 += _cost(R8A, "p2")
    _total += c1 + c2
    _tc.append(f"試行 {n} = パターン 1 ${c1:.3f} / パターン 2 ${c2:.3f}")
trial_costs = "、".join(_tc) + "（試行 2 のパターン 1 は試行 1 の結果を流用したので 0。上限の測り直しなどの小さな実行は含まない）"
trial_cost_total = f"${_total:.2f}（約 {_total * 150:.0f} 円）"


def e(s):
    return html.escape(str(s))


# ---------- 棒グラフ（横棒・2 系列・直接ラベル） ----------
def bar_chart(items, target, target_label, aria):
    """items: [(label, (ok1,n1), (ok2,n2))]"""
    W, L, R_ = 400, 8, 104
    plot_w = W - L - R_
    row_h = 52
    top = 52
    H = top + row_h * len(items) + 22
    x0 = L
    def X(v):
        return x0 + plot_w * v / 100.0
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(aria)}" class="study-chart">']
    # 凡例
    out.append(f'<rect x="{L}" y="6" width="12" height="12" rx="3" class="s1"/>'
               f'<text x="{L+18}" y="16" class="lg">パターン 1（luna）</text>'
               f'<rect x="{L+150}" y="6" width="12" height="12" rx="3" class="s2"/>'
               f'<text x="{L+168}" y="16" class="lg">パターン 2（Jev）</text>')
    # グリッド
    for v in (0, 50, 100):
        out.append(f'<line x1="{X(v):.1f}" y1="{top-4}" x2="{X(v):.1f}" y2="{H-18}" class="grid"/>'
                   f'<text x="{X(v):.1f}" y="{H-6}" class="ax" text-anchor="middle">{v}%</text>')
    for i, (label, a, b) in enumerate(items):
        y = top + i * row_h
        out.append(f'<text x="{L}" y="{y+10}" class="rl">{e(label)}</text>')
        for j, (ok, n) in enumerate((a, b)):
            v = pct(ok, n)
            by = y + 16 + j * 14
            w = max(plot_w * v / 100.0, 2)
            cls = "s1" if j == 0 else "s2"
            name = "パターン 1" if j == 0 else "パターン 2"
            out.append(f'<g><title>{e(label)} / {name}: {ok}/{n}（{v:.1f}%）</title>'
                       f'<rect x="{x0}" y="{by}" width="{w:.1f}" height="12" rx="4" class="{cls}"/>'
                       f'<text x="{x0 + w + 4:.1f}" y="{by+10}" class="vl">{v:.0f}%（{ok}/{n}）</text></g>')
    tx = X(target)
    out.append(f'<line x1="{tx:.1f}" y1="{top-4}" x2="{tx:.1f}" y2="{H-18}" class="target"/>'
               f'<text x="{tx:.1f}" y="{top-10}" class="tl" text-anchor="middle">{e(target_label)}</text>')
    out.append("</svg>")
    return "\n".join(out)


chart_trials = bar_chart(
    [(f"試行 {n}", acc(rows(res, "p1")), acc(rows(res, "p2"))) for n, res in ((1, R1), (2, R2), (3, R3), (4, R4), (5, R5), (6, R6), (7, R7), (8, R))],
    90, "レベル 1 の基準 90%", "試行ごとの種別一致率の推移")
chart_groups = bar_chart(
    [(k, stats["p1"][k], stats["p2"][k]) for k in
     ("全体", "質問系 ①〜③", "推理系 ④〜⑥", "その他 ⑦〜㉒")]
    + [("① の判定（従来の質問）", _yn("p1", False), _yn("p2", False)),
       ("① の判定（新しい質問）", _yn("p1", True), _yn("p2", True))],
    90, "レベル 1 の基準 90%", "区分別の種別一致率の比較")
chart_kinds = bar_chart(
    [(lab, stats["p1"]["kinds"][k], stats["p2"]["kinds"][k]) for k, lab in KINDS],
    80, "種別ごとの基準 80%", "種別ごとの一致率の比較")



# ---------- 全試行の推移（1 項目 1 行の小さな折れ線。試行 4 章） ----------
TRIALS = [(1, R1), (2, R2), (3, R3), (4, R4), (5, R5), (6, R6), (7, R7), (8, R)]  # 試行 6 のパターン 2 は 6b、試行 7 は 7b、試行 8 は 8b


def _series(pred, yn=False):
    out = {}
    for m in ("p1", "p2"):
        vals = []
        for _, res in TRIALS:
            rs = [x for x in rows(res, m) if pred(x)]
            vals.append(yesno(rs) if yn else acc(rs))
        out[m] = vals
    return out


def trend_chart(items, target, aria):
    """items: [(label, {"p1": [(ok, n)...], "p2": [...]})]。1 行 = 1 項目、横軸 = 試行 1〜7。"""
    W, LW, PX0, PX1, VX = 400, 118, 148, 314, 330
    RH = 92
    top = 26
    H = top + RH * len(items) + 18
    nt = len(TRIALS)

    def X(i):
        return PX0 + (PX1 - PX0) * i / (nt - 1)

    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(aria)}" class="study-chart trend">']
    o.append(f'<rect x="{PX0}" y="6" width="10" height="10" rx="2" class="s1"/><text x="{PX0 + 14}" y="15" class="lg">パターン 1</text>'
             f'<rect x="{PX0 + 90}" y="6" width="10" height="10" rx="2" class="s2"/><text x="{PX0 + 104}" y="15" class="lg">パターン 2</text>'
             f'<text x="{VX}" y="15" class="tl">試行 {TRIALS[-1][0]}</text>')
    for r, (label, ser) in enumerate(items):
        y0 = top + r * RH
        ybot, ytop = y0 + 76, y0 + 16

        def Y(v):
            return ybot - (ybot - ytop) * v / 100.0

        o.append(f'<line x1="0" y1="{y0 + RH - 2}" x2="{W}" y2="{y0 + RH - 2}" class="grid"/>')
        o.append(f'<text x="0" y="{y0 + RH / 2 + 3}" class="rl">{e(label)}</text>')
        for gv in (0, 50, 100):
            o.append(f'<text x="{PX0 - 16}" y="{Y(gv) + 3:.1f}" class="gv" text-anchor="end">{gv}</text>')
        o.append(f'<line x1="{PX0}" y1="{Y(target):.1f}" x2="{PX1}" y2="{Y(target):.1f}" class="target"/>')
        o.append(f'<line x1="{PX0}" y1="{Y(0):.1f}" x2="{PX1}" y2="{Y(0):.1f}" class="axis0"/>')
        # 点ごとの数値: 同じ試行で値の高いほうを点の上、低いほうを点の下に置いて重ならないようにする
        for i in range(nt):
            (a1, n1), (a2, n2) = ser["p1"][i], ser["p2"][i]
            if not (n1 and n2):
                continue
            v1, v2 = pct(a1, n1), pct(a2, n2)
            p1_above = v1 >= v2
            for v, cls, above in ((v1, "t1", p1_above), (v2, "t2", not p1_above)):
                ty = Y(v) - 5 if above else Y(v) + 11
                o.append(f'<text x="{X(i):.1f}" y="{ty:.1f}" class="pv {cls}" text-anchor="middle">{v:.0f}</text>')
        for m, cls in (("p1", "s1"), ("p2", "s2")):
            pts = [(i, ok, n) for i, (ok, n) in enumerate(ser[m]) if n]
            if len(pts) > 1:
                d = " ".join(f"{X(i):.1f},{Y(pct(ok, n)):.1f}" for i, ok, n in pts)
                o.append(f'<polyline points="{d}" class="ln {cls}l"/>')
            for i, ok, n in pts:
                name = "パターン 1" if m == "p1" else "パターン 2"
                o.append(f'<g><title>{e(label)} / 試行 {TRIALS[i][0]} / {name}: {ok}/{n}（{pct(ok, n):.1f}%）</title>'
                         f'<circle cx="{X(i):.1f}" cy="{Y(pct(ok, n)):.1f}" r="2.6" class="{cls}"/>'
                         f'<circle cx="{X(i):.1f}" cy="{Y(pct(ok, n)):.1f}" r="7" class="hit"/></g>')
        last1, last2 = ser["p1"][-1], ser["p2"][-1]
        o.append(f'<text x="{VX}" y="{y0 + 40}" class="vl"><tspan class="t1">■</tspan> {pct(*last1):.1f}%</text>')
        o.append(f'<text x="{VX}" y="{y0 + 56}" class="vl"><tspan class="t2">■</tspan> {pct(*last2):.1f}%</text>')
    yb = top + RH * len(items) + 12
    for i, (n, _) in enumerate(TRIALS):
        o.append(f'<text x="{X(i):.1f}" y="{yb}" class="ax" text-anchor="middle">{n}</text>')
    o.append(f'<text x="{PX0 - 4}" y="{yb}" class="ax" text-anchor="end">試行</text>')
    o.append("</svg>")
    return "\n".join(o)



def trend_table(items):
    """推移グラフの数値版。行 = 項目、列 = 試行。各マスにパターン 1 / 2 の割合と件数。"""
    head = "".join(f"<th>試行 {n}</th>" for n, _ in TRIALS)
    body = []
    for label, ser in items:
        cells = []
        for i in range(len(TRIALS)):
            lines = []
            for m, cls in (("p1", "t1"), ("p2", "t2")):
                ok, n = ser[m][i]
                val = f"{pct(ok, n):.1f}%（{ok}/{n}）" if n else "—"
                lines.append(f'<span class="{cls}">■</span> {val}')
            cells.append("<td>" + "<br>".join(lines) + "</td>")
        body.append(f'<tr><th scope="row">{e(label)}</th>{"".join(cells)}</tr>')
    return ('<div class="table-wrap trend-table-wrap"><table class="trend-table"><thead><tr><th>項目</th>'
            + head + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>")


_GROUP_ITEMS = [
    ("全体", _series(lambda x: True)),
    ("質問系 ①〜③", _series(lambda x: x["expected_kind"] in GROUPS["q"])),
    ("推理系 ④〜⑥", _series(lambda x: x["expected_kind"] in GROUPS["g"])),
    ("その他 ⑦〜㉒", _series(lambda x: x["expected_kind"] not in GROUPS["q"] + GROUPS["g"])),
    ("① 判定（従来）", _series(lambda x: "-b" not in x["id"], yn=True)),
    ("① 判定（新しい質問）", _series(lambda x: "-b" in x["id"], yn=True)),
]
trend_groups = trend_chart(_GROUP_ITEMS, 90, "区分別の種別一致率の試行ごとの推移")
table_groups = trend_table(_GROUP_ITEMS)

_KIND_BLOCKS = [
    ("質問系 ①〜③", ["q_yesno", "q_multi", "q_open"], True),
    ("推理系 ④〜⑥", ["guess_correct", "guess_close", "guess_wrong"], True),
    ("依頼系 ⑦〜⑨", ["ask_hint", "ask_spoiler", "ask_howto"], False),
    ("反応系 ⑩〜⑰", ["impression", "greeting", "cheer", "chat", "request", "complaint", "mention", "emoji_only"], False),
    ("不適切系 ⑱〜㉑", ["troll", "abuse", "spam", "personal_info"], False),
    ("その他 ㉒", ["foreign"], False),
]
_kb = []
for title, codes, opened in _KIND_BLOCKS:
    items = [(KIND_LABEL[c], _series(lambda x, c=c: x["expected_kind"] == c)) for c in codes]
    chart = trend_chart(items, 80, f"{title} の種別ごとの一致率の推移")
    op = " open" if opened else ""
    _kb.append(f'<details class="trend-block"{op}><summary>{e(title)}</summary>\n<figure class="diagram">\n{chart}\n</figure>\n'
               f'<p class="trend-note">数値（<span class="t1">■</span> パターン 1 / <span class="t2">■</span> パターン 2。割合（一致件数 / 件数））</p>\n{trend_table(items)}\n</details>')
trend_kinds = "\n".join(_kb)

# ---------- フローチャート ----------
def box(x, y, w, h, lines, cls="bx", size=12):
    t = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="{cls}"/>']
    n = len(lines)
    for i, ln in enumerate(lines):
        ty = y + h / 2 + (i - (n - 1) / 2) * (size + 3) + size * 0.35
        weight = ' font-weight="700"' if i == 0 and cls != "ex" else ""
        t.append(f'<text x="{x + w/2}" y="{ty:.1f}" text-anchor="middle" font-size="{size}"{weight} class="ft">{e(ln)}</text>')
    return "".join(t)


def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="ar" marker-end="url(#{MID[0]})"/>'
    if label:
        s += f'<text x="{lx}" y="{ly}" font-size="10.5" class="al">{e(label)}</text>'
    return s


DEFS_T = ('<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arh"/></marker></defs>')
MID = ["arw"]

def defs(mid):
    MID[0] = mid
    return DEFS_T.replace("{mid}", mid)


def flow_p1():
    W, H = 420, 470
    M, MW = 10, 230   # 本流
    S, SW = 268, 146  # 分岐先
    cx = M + MW / 2
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="パターン 1 の処理フロー" class="study-flow">', defs("arw-p1")]
    o.append(box(M, 10, MW, 40, ["コメント 1 件", "本文 + comment_id"]))
    o.append(arrow(cx, 50, cx, 72))
    o.append(box(M, 72, MW, 58, ["system プロンプトを組み立て", "改訂案の判定ルール", "+ 問題文・真相・確定事実"]))
    o.append(arrow(cx, 130, cx, 152))
    o.append(box(M, 152, MW, 72, ["gpt-6-luna を 1 回呼ぶ", "effort xhigh・上限 2,400", "出力は JSON", "{種別, 判定, 返信文}"], cls="bx2"))
    o.append(arrow(cx, 224, cx, 246))
    o.append(box(M, 246, MW, 58, ["コードの後処理", "種別で出口を分ける", "（LLM の判断を上書き）"]))
    o.append(box(S, 236, SW, 36, ["⑳ 宣伝・㉑ 個人情報", "→ 返信しない"], cls="ex", size=11))
    o.append(box(S, 280, SW, 36, ["⑱ 荒らし・⑲ 誹謗中傷", "→ コードの定型文"], cls="ex", size=11))
    o.append(arrow(M + MW, 262, S, 254))
    o.append(arrow(M + MW, 290, S, 298))
    o.append(arrow(cx, 304, cx, 330, "その他 18 種", cx + 6, 322))
    o.append(box(M, 330, MW, 96, ["LLM の返信文をそのまま使う", "① 判定語 + 20 字以内の一言", "④ 正解です！+ 真相 2〜3 文", "⑤ 惜しい！ / ⑥ 残念、違います", "⑦〜⑰・㉒ 種別に合う短い返事"], cls="bx3", size=11.5))
    o.append(f'<text x="{M}" y="{H-14}" font-size="10.5" class="al">失敗・打ち切り（finish_reason=length）は返信なし。本番は固定文言にフォールバック</text>')
    o.append("</svg>")
    return "\n".join(o)


def flow_p2():
    W, H = 420, 1000
    M, MW = 10, 230
    S, SW = 262, 152
    cx = M + MW / 2
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="パターン 2 の処理フロー" class="study-flow">', defs("arw-p2")]
    y = 10
    o.append(box(M, y, MW, 40, ["コメント 1 件", "本文 + comment_id"]))
    o.append(arrow(cx, 50, cx, 70))
    o.append(box(M, 70, MW, 52, ["段 0 文字種の規則", "Jev を呼ばない"], cls="bx2"))
    o.append(box(S, 62, SW, 68, ["URL あり → ⑳ 返信しない", "絵文字だけ → ⑰ 相づち", "英単語 2 語以上（かな・", "漢字なし）→ ㉒"], cls="ex", size=11))
    o.append(arrow(M + MW, 96, S, 96, "当たり", M + MW + 4, 90))
    o.append(arrow(cx, 122, cx, 146, "当たらない", cx + 6, 138))
    o.append(box(M, 146, MW, 70, ["段 A1 大分類", "Jev choice 5 択（問題文なし）", "質問・推理 / 依頼 / 反応 /", "不適切 / その他"], cls="bx2"))
    o.append(box(S, 162, SW, 36, ["その他 → ㉒", "日本語でお願い"], cls="ex", size=11))
    o.append(arrow(M + MW, 180, S, 180))
    o.append(arrow(cx, 216, cx, 242, "質問・推理", cx + 6, 234))
    o.append(box(M, 242, MW, 58, ["段 A1b 振り分け直し", "Jev choice 2 択（問題文つき）", "推理 = 確率 0.95 以上 かつ", "コアのどれかが 0.25 以上"], cls="bx2", size=11))
    o.append(box(S, 226, SW, 50, ["コアに触れない推理は質問", "に戻す（A2 で ③ なら ⑥）"], cls="ex", size=11))
    o.append(arrow(cx, 300, cx, 326, "質問（推理は段 B へ）", cx + 6, 318))
    o.append(box(M, 326, MW, 70, ["段 A2 細分類", "大分類ごとの Jev choice", "質問 → ①②③ / 依頼 → ⑦⑧⑨", "反応 → ⑩〜⑯ / 不適切 → ⑱〜㉑"], cls="bx2", size=11.5))
    o.append(box(S, 328, SW, 66, ["②⑦〜⑯・⑱⑲ →", "種別ごとの定型文", "⑳㉑ → 返信しない", "（3 通り以上を順繰り）"], cls="ex", size=11))
    o.append(arrow(M + MW, 361, S, 361))
    o.append(arrow(cx, 396, cx, 422, "③、または指示語を含む ①", cx + 6, 414))
    o.append(box(M, 422, MW, 70, ["段 A3 確かめ直し", "Jev noul（問題文つき）", "主語が一つに決まる", "はい / いいえの質問か"], cls="bx2"))
    o.append(box(S, 436, SW, 40, ["0.6 未満", "→ ③ 聞き直しの誘導文"], cls="ex", size=11))
    o.append(arrow(M + MW, 456, S, 456))
    o.append(arrow(cx, 492, cx, 518, "① または推理", cx + 6, 510))
    o.append(box(M, 518, MW, 70, ["段 B 正解判定", "Jev noul × コアの要点（1〜2 個）", "「言い換えも含めて", "同じ内容を述べているか」"], cls="bx2", size=11.5))
    o.append(box(S, 510, SW, 40, ["コアの要点がすべて 0.5 以上", "→ ④ 正解です！+ 開示文"], cls="ok", size=11))
    o.append(box(S, 556, SW, 40, ["推理でどれかが 0.25 以上", "→ ⑤ 惜しい！ / なし → ⑥"], cls="ex", size=11))
    o.append(arrow(M + MW, 538, S, 530))
    o.append(arrow(M + MW, 573, S, 576))
    o.append(arrow(cx, 588, cx, 616, "① で正解に届かない", cx + 6, 606))
    o.append(box(M, 616, MW, 58, ["段 C 質問の品質", "Jev noul「はい / いいえで", "一意に答えられるか」"], cls="bx2"))
    o.append(box(S, 624, SW, 40, ["確率 0.2 未満", "→ ③ 聞き直しの誘導文"], cls="ex", size=11))
    o.append(arrow(M + MW, 645, S, 645))
    o.append(arrow(cx, 674, cx, 700, "0.2 以上", cx + 6, 692))
    o.append(box(M, 700, MW, 70, ["段 D 判定", "Jev choice 3 択", "state = 問題文 + 真相", "+ 確定事実 + 質問"], cls="bx2"))
    o.append(box(S, 708, SW, 54, ["最大確率 0.55 未満", "→「それは問題の答えに", "関わりません。」"], cls="ex", size=11))
    o.append(arrow(M + MW, 735, S, 735))
    o.append(arrow(cx, 770, cx, 796, "0.55 以上", cx + 6, 788))
    o.append(box(M, 796, MW, 58, ["返信（すべて定型文）", "はい。/ いいえ。/ 関係ありません。", "+ 20 字以内の定型の一言"], cls="bx3", size=11.5))
    o.append(f'<text x="{M}" y="884" font-size="10.5" class="al">閾値は試走の値（0.95 / 0.6 / 0.5 / 0.25 / 0.2 / 0.55。21-6d で決める）。</text>')
    o.append(f'<text x="{M}" y="902" font-size="10.5" class="al">1 コメントあたり Jev を 1〜7 回呼ぶ（種別によって段の数が違う）。</text>')
    o.append(f'<text x="{M}" y="920" font-size="10.5" class="al">返信文を AI に書かせないので、補足やお礼から真相が漏れない。</text>')
    o.append("</svg>")
    return "\n".join(o)


# ---------- 例（誤り） ----------
def examples(m, ids):
    idx = {x["id"]: x for x in rows(R, m)}
    out = []
    for i in ids:
        x = idx[i]
        got = KIND_LABEL.get(x["kind"], x["kind"])
        extra = ""
        P = x["debug"].get("probabilities") or {}
        if m == "p2" and (P.get("A1") or P.get("A")):
            parts = []
            for st in ("A1", "A1b", "A2", "A3", "A"):
                if isinstance(P.get(st), (int, float)):
                    parts.append(f"段 {st}: {P[st]:.2f}")
                elif P.get(st):
                    top = sorted(P[st].items(), key=lambda kv: -kv[1])[:2]
                    parts.append(f"段 {st}: " + " / ".join(f"{k} {v:.2f}" for k, v in top))
            extra = "（" + "、".join(parts)
            if P.get("B"):
                extra += "、段 B: " + " / ".join(
                    f"hit={v['hit']:.2f},close={v['close']:.2f}"
                    if isinstance(v, dict) else f"{v:.2f}"
                    for v in P["B"].values()
                )
            extra += "）"
        reply = x["reply"] if x["reply"] else "（返信なし）"
        AN = {"yes": "はい", "no": "いいえ", "irrelevant": "関係ありません", "unknown": "答えに関わりません"}
        exp = KIND_LABEL[x["expected_kind"]] + (f"（{AN[x['expected_answer']]}）" if x.get("expected_answer") else "")
        got += f"（{AN[x['answer']]}）" if x.get("answer") else ""
        ln = f"・{len(x['reply'])} 字" if x["reply"] and len(x["reply"]) > 80 else ""
        out.append(f'<li>「{e(x["comment_text"])}」 — 正解 {e(exp)} → 判定 {e(got)}。返信「{e(reply)}」{e(ln)}{e(extra)}</li>')
    return "<ul>\n" + "\n".join(out) + "\n</ul>"


p1_ex = examples("p1", ["U01-e19", "U01-e18", "U13-e15", "c-ask_howto-05"])
p2_ex = examples("p2", ["U13-e19", "U20-e19", "U20-e21", "U13-b25"])

S = {m: stats[m] for m in stats}


def f(m, k):
    ok, n = S[m][k]
    return f"{pct(ok, n):.1f}%（{ok}/{n}）"


P_ROWS = [
    ("P1", "真相の漏洩", "正解宣言以外の返信に、真相の核心語が出ない", "0 件"),
    ("P2", "誤った正解宣言", "正解でない推理に「正解です！」と言わない", "0 件"),
    ("P3", "はい / いいえの取り違え", "「はい」が正しいのに「いいえ」（またはその逆）と答える", "全質問の 3% 以下、かつ 1 問あたり 2 件以下"),
    ("P4", "いいえ / 関係ありません の揺れ", "「いいえ」「関係ありません」「答えに関わりません」の間で取り違える", "10% 以下"),
    ("P5", "正解宣言率", "正解推理を「正解です！」と宣言できた割合", "80% 以上"),
    ("P6", "不適切なコメントへの扱い", "⑱〜㉑ に判定語や真相を返す / ⑱⑲ を定型文で返す / ⑳㉑ に返信する / 普通のコメントを不適切と誤判定", "0 件 / 80% 以上 / 0 件 / 5% 以下"),
    ("P7", "返信の長さ", "返信の字数", "すべて 80 字以内"),
    ("L1", "レベル 1 の機械基準", "種別の一致率 / 同じ種別で最も多い言い回しの割合 / 答えられない質問（②③）に誘導文を返した割合", "全体 90% 以上・質問以外の各種別 80% 以上 / 50% 以下 / 80% 以上"),
]
P_TABLE = ('<div class="table-wrap"><table><thead><tr><th>項目</th><th>合格ライン</th><th>何を見るか</th></tr></thead><tbody>'
           + "".join(f'<tr><td class="kid">{a} {e(b)}</td><td>{e(d)}</td><td>{e(c)}</td></tr>' for a, b, c, d in P_ROWS)
           + '</tbody></table></div>')
KIND_ROWS = [
    ("質問系", [("① はい / いいえ質問", "判定（はい / いいえ / 関係ありません）を返す"),
               ("② 複数の質問", "「1 つずつ聞いてね」と誘導"),
               ("③ 答えられない・曖昧な質問", "はい / いいえで答えられる形に聞き直す誘導文")]),
    ("推理系", [("④ 正解推理", "「正解です！」+ 真相の開示"),
               ("⑤ 惜しい推理", "「惜しい！」（どこが足りないかは言わない）"),
               ("⑥ 外れた推理", "「残念、違います」")]),
    ("依頼系", [("⑦ ヒント要求", "「質問で絞ってみて」（ヒントは出さない）"),
               ("⑧ 答え・ネタバレ要求", "「誰かが当てるまで秘密」"),
               ("⑨ 遊び方・アカウントへの質問", "遊び方の案内（bot かどうかの質問も含む）")]),
    ("反応系", [("⑩ 感想", "お礼"), ("⑪ 挨拶", "お礼"), ("⑫ 応援", "お礼"), ("⑬ 雑談", "軽い相づち"),
               ("⑭ リクエスト", "お礼"), ("⑮ 指摘・クレーム", "お礼と「確認します」だけ（反論・言い訳はしない）"),
               ("⑯ メンション", "短い歓迎"), ("⑰ 絵文字だけ", "短い相づち")]),
    ("不適切系", [("⑱ 荒らし", "定型文"), ("⑲ 誹謗中傷", "定型文（一言は付けない）"),
                 ("⑳ 宣伝・スパム", "返信しない"), ("㉑ 個人情報", "返信しない")]),
    ("その他", [("㉒ 外国語", "日本語の定型で「日本語で質問してね」")]),
]
KIND_TABLE = ('<div class="table-wrap"><table><thead><tr><th>種別</th><th>返し方</th></tr></thead><tbody>'
              + "".join(f'<tr class="grp"><th colspan="2">{e(g)}</th></tr>'
                        + "".join(f'<tr><td class="kid">{e(k)}</td><td>{e(r)}</td></tr>' for k, r in items)
                        for g, items in KIND_ROWS)
              + '</tbody></table></div>')


page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>コメント返信処理方式の検討 | AutoContentPublisherSystem</title>
<link rel="stylesheet" href="../../assets/style.css?v=20260921">
<style>
/* 本ページだけの図の色。系列色はパレット検証済み（ライト / ダーク） */
:root {{ --s1: #0a69da; --s2: #c2610c; --target: #b98900; --ok-box: #e6f4ea; --ok-box-border: #3f9a5a; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --s1: #4d8fe0; --s2: #d67a2c; --target: #c69026; --ok-box: #15291c; --ok-box-border: #4fae6d; }}
}}
.study-chart, .study-flow {{ width: 100%; max-width: 560px; height: auto; }}
.study-chart .s1 {{ fill: var(--s1); }} .study-chart .s2 {{ fill: var(--s2); }}
.study-chart text {{ fill: var(--text); }}
.study-chart .lg, .study-chart .rl {{ font-size: 12px; }}
.study-chart .vl {{ font-size: 10.5px; fill: var(--text-muted); }}
.study-chart .ax {{ font-size: 10px; fill: var(--text-muted); }}
.study-chart .grid {{ stroke: var(--border); stroke-width: 1; }}
.study-chart .target {{ stroke: var(--target); stroke-width: 1.5; stroke-dasharray: 4 3; }}
.study-chart .tl {{ font-size: 10.5px; fill: var(--text-muted); }}
.study-flow .bx {{ fill: var(--diag-box-alt); stroke: var(--diag-box-alt-border); }}
.study-flow .bx2 {{ fill: var(--diag-box); stroke: var(--diag-box-border); }}
.study-flow .bx3 {{ fill: var(--diag-emph); stroke: var(--diag-emph-border); }}
.study-flow .ex {{ fill: var(--bg); stroke: var(--diag-box-alt-border); stroke-dasharray: 4 3; }}
.study-flow .ok {{ fill: var(--ok-box); stroke: var(--ok-box-border); }}
.study-flow .ft {{ fill: var(--diag-text); }}
.study-flow .al {{ fill: var(--text-muted); }}
.study-flow .ar {{ stroke: var(--diag-line); stroke-width: 1.4; }}
.study-flow .arh {{ fill: var(--diag-line); }}
.ref-bar {{ position: sticky; top: 0; z-index: 20; display: flex; align-items: center; gap: .5rem; flex-wrap: wrap;
  margin: .5rem -.25rem 1rem; padding: .45rem .25rem; background: var(--bg); border-bottom: 1px solid var(--border); }}
.ref-bar-label {{ font-size: .8rem; color: var(--text-muted); }}
.ref-top {{ margin-left: auto; font-size: .8rem; }}
details.ref > summary {{ list-style: none; cursor: pointer; font-size: .85rem; font-weight: 700; padding: .3rem .8rem;
  min-height: 36px; display: inline-flex; align-items: center; border: 1px solid var(--border-strong); border-radius: 999px;
  background: var(--bg-subtle); color: var(--text); }}
details.ref > summary::-webkit-details-marker {{ display: none; }}
details.ref[open] > summary {{ background: var(--link); border-color: var(--link); color: var(--bg); }}
.ref-panel {{ position: absolute; left: 0; right: 0; top: 100%; max-height: 70vh; overflow: auto; padding: .25rem .75rem .75rem;
  background: var(--bg); border: 1px solid var(--border-strong); border-top: none; border-radius: 0 0 10px 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,.18); }}
.ref-panel .table-wrap {{ margin: .5rem 0 0; }}
tr.grp > th {{ background: var(--note-bg); font-size: .85rem; }}
td.pid {{ white-space: nowrap; font-weight: 700; }} td.kid {{ font-weight: 700; }}
.study-chart.trend .rl {{ font-size: 10.5px; }}
.study-chart.trend .lg, .study-chart.trend .tl {{ font-size: 10px; }}
.study-chart.trend .vl {{ font-size: 10px; fill: var(--text); }}
.study-chart.trend .ax {{ font-size: 9.5px; }}
.study-chart .ln {{ fill: none; stroke-width: 1.6; }}
.study-chart .s1l {{ stroke: var(--s1); }} .study-chart .s2l {{ stroke: var(--s2); }}
.study-chart .t1 {{ fill: var(--s1); }} .study-chart .t2 {{ fill: var(--s2); }}
.study-chart .axis0 {{ stroke: var(--border); stroke-width: 1; }}
.study-chart .hit {{ fill: transparent; }}
.study-chart.trend .target {{ stroke-width: 1; }}
details.trend-block {{ margin: .5rem 0; border: 1px solid var(--border); border-radius: 8px; padding: 0 .6rem; }}
details.trend-block > summary {{ cursor: pointer; font-weight: 700; font-size: .9rem; padding: .5rem 0; min-height: 36px; }}
details.trend-block figure.diagram {{ margin: .25rem 0 .6rem; padding: .5rem; }}
.trend-note {{ font-size: .85rem; color: var(--text-muted); }}
.trend-table {{ font-size: .78rem; width: auto; }}
.trend-table th, .trend-table td {{ white-space: nowrap; padding: .3rem .5rem; }}
.trend-table thead th {{ text-align: center; }}
.trend-table tbody th {{ position: sticky; left: 0; background: var(--bg-subtle); z-index: 1; font-weight: 600; }}
.trend-table thead th:first-child {{ position: sticky; left: 0; z-index: 2; }}
.t1 {{ color: var(--s1); }} .t2 {{ color: var(--s2); }}
.study-chart.trend .pv {{ font-size: 9px; font-weight: 600; }}
.study-chart.trend .gv {{ font-size: 8px; fill: var(--text-muted); }}
.pass {{ font-weight: 700; }} .fail {{ font-weight: 700; color: var(--warn-border); }}
</style>
</head>
<body>
<div class="container">

<nav class="breadcrumb"><a href="../../index.html">設計書体系ガイド</a> / <a href="../index.html">アプリ設計</a> / <a href="umigame-soup-1.html">探偵カメロックのウミガメのスープ</a> / コメント返信処理方式の検討</nav>
<h1>コメント返信処理方式の検討</h1>
<div class="page-meta">
  <span class="badge badge-fixed">判定品質の検討は完了（21-6b・2026-09-28）</span>
  <span>set_code: umigame-soup-1</span>
  <span>最終更新: 2026-09-28（試行 8 まで。21-6b 完了・方針を 8 章に整理）</span>
</div>

<div class="ref-bar" id="ref-bar">
  <span class="ref-bar-label">前提</span>
  <details class="ref" name="ref"><summary>P1〜P7</summary><div class="ref-panel">{P_TABLE}</div></details>
  <details class="ref" name="ref"><summary>22 種</summary><div class="ref-panel">{KIND_TABLE}</div></details>
  <a class="ref-top" href="#premise">本文の前提へ</a>
</div>

<div class="note">
  <span class="callout-title">このページの位置づけ</span>
  コメント返信の判定方式（パターン 1 = <code>gpt-6-luna</code> の一括方式 / パターン 2 = Jev の段階判定 + 定型文）の<strong>試行錯誤の記録</strong>。何を試して、どうなったかをここに積み、決まったことだけを<a href="umigame-soup-1.html#judge-design">セット別設計書 5.1.2</a>（判定モジュールの契約・方式の設計）へ移す。方式の選定は 21-6e。試走の資材とスクリプトは <code>content/umigame-stock/umigame-soup-1/judge-trial/</code>。
</div>

<h2 id="premise">1. 前提: 判定の正しさ（P1〜P7）</h2>
<p>21-6a で承認した品質レベル（<a href="umigame-soup-1.html#quality-levels">セット別設計書 5.1.1</a>）のうち、どのレベルでも満たす前提条件。1 つでも割れたらリリース不可。最低ラインは「レベル 1（22 種を見分けて種別に合った返事をする）+ P1〜P7」、目標はレベル 2（探偵カメロックの一言を添える）。画面上部の「P1〜P7」ボタンでいつでも開ける。</p>
{P_TABLE}

<h2 id="kinds">2. 前提: コメントの種別（22 種）</h2>
<p>レベル 1 以上で見分ける種別。画面上部の「22 種」ボタンでいつでも開ける。</p>
{KIND_TABLE}

<h2 id="test">3. テスト内容とやったこと</h2>
<h3>3.1 テストデータ（220 件）</h3>
<ul>
  <li><strong>問題ごとのケース（従来）</strong>: 5 問（U01・U13・U18・U20・U26）× 21 件 = 105 件。内訳は 1 問あたり ① 10 件・② 2 件・③ 3 件・④ 2 件（うち 1 件は「〜ってこと？」の質問の形）・⑤ 2 件・⑥ 2 件。① には正解の判定（はい / いいえ / 関係ありません）も付けた。書き手が確定事実シートの言い回しに寄せてしまい、実際のコメントより易しめ</li>
  <li><strong>新しい質問（試行 4 で追加）</strong>: 真相を見せずに書かせた ① 32 件。50 件書かせたうち 18 件（36%）は、真相から答えが一つに決まらない質問だったので採点から外した。実際のプレイヤーもこの割合で「答えが決まらない質問」をしてくると見ておく</li>
  <li><strong>共通のケース</strong>: ⑦〜㉒ の 16 種 × 5 件 + 3 件 = 83 件。試行 3 で「作品へのけなしは ⑮」と決めたため、元の ⑲ のうち 3 件を ⑮ に付け替え、⑲ には人への攻撃・性的な文を 3 件足した（⑮ 8 件・⑲ 5 件）</li>
  <li><strong>ラベルの確認（試行 4 のあと・ユーザー）</strong>: 2 方式のどちらかがラベルと食い違った新しい質問 11 件をユーザーが確認。7 件はラベルどおり、4 件は「どちらでもよい」（「男はその子の主治医なの？」「男は有名人なの？」「演奏は録音だったの？」は いいえ / 関係ありません のどちらも正解、「曲の選び方を間違えたってこと？」は質問としての いいえ でも外れた推理でも正解）。「その子は彼に会ったことがある？」は、「その子」= 男の子なので「彼」は消去法で男と決まり、曖昧な主語ではない → ③ から ①（いいえ）へ付け替えた。<strong>過去の試行も、この確認後のラベルで数え直してある</strong></li>
  <li><strong>ラベルの確認（試行 5 のあと・ユーザー）</strong>: パターン 1 の答えのうち 3 件を「許容範囲」として別解に登録した（「義母も外国出身なの？」→ 関係ありません、「義母は日本語以外の言葉を話してたの？」→ 答えに関わりません、「影が薄くなったのは見た目の変化？」→ はい）。「男はその場所に入院してたの？」（U01。確定事実は「入院はしていない」、パターン 1 は「その場所」が問題文に無いため聞き直しにした）はユーザー判断待ちで、ラベルは いいえ のまま（その後ユーザーが「聞き直しでよい」と判断し、別解に登録）</li>
  <li><strong>推理のラベルの付け直し（試行 7 の前・ユーザー確認）</strong>: ④⑤⑥ をコア基準（5.1.1）で付け直した。「影が薄くなったのは、男の病気が良くなってきた知らせなんだね」は ⑤ → ④（コアの 2 点を言い当てている）、「隣の女性も男がその曲を知っている理由を分かっていて…」は ⑤ → ⑥（周辺だけ）。U13 の 2 件（「学校で書かれた古い手紙が何十年も保管されていて…」「手紙は未来の誰かに宛てたもので…」）は、「未来の自分宛てで長く保管された手紙」をコアの半分として扱い ⑤ のまま（外れと返すのは厳しすぎるというユーザー判断）</li>
  <li><strong>作り方</strong>: プロンプトの調整に使った想定質問（<code>expected_questions</code>）は使わない。新しい質問は、Codex を読み取り専用（ファイルを開かない指示つき）で動かし、問題文だけを渡して書かせた。正解ラベルは Claude が付け、ユーザーが確認した。プロンプトや Jev の説明に書く例文は、評価データと重ならない文にする。置き場は <code>judge-trial/data/</code></li>
</ul>
<h3>3.2 測ったこと</h3>
<ul>
  <li>種別の一致率（全体・区分別・種別ごと）、① の判定の一致率（従来の質問と新しい質問を分けて出す）</li>
  <li>P1〜P7（上の基準をそのまま機械で数える。P1 は既存の <code>leak_count.py</code> の核心語辞書で漏れ候補を拾う）</li>
  <li>応答時間・トークン・金額（パターン 1 の打ち切り件数、パターン 2 の入力トークン）</li>
  <li><strong>採点の約束</strong>: 「〜って関係ある？」「〜は重要？」への「いいえ」は、正解ラベルが「関係ありません」でも一致とする（21-4a の <code>probe_test.py</code> と同じ扱い）。ユーザーが「どちらでもよい」とした別解も一致とする</li>
  <li><strong>金額の単価</strong>（試算。請求画面で確認が必要）: <code>gpt-6-luna</code> は入力 $0.10・出力 $0.50 / 100 万トークン（公開情報 2026-09-27 時点。推論トークンは出力として課金される前提）、Jev は入力 $0.042 / 100 万トークン・出力無料。円は 1 ドル 150 円の仮レート、月の件数は 6,000 件（アイデア記録の見込み）</li>
</ul>
<h3>3.3 試行の記録</h3>
<p>一致率は、すべて確認後のラベルで数え直した値。</p>
<ul>
  <li><strong>試行 1</strong>: 2 方式を 185 件で実行。パターン 1 = {pct(*acc(rows(R1, "p1"))):.1f}%、パターン 2 = {pct(*acc(rows(R1, "p2"))):.1f}%。パターン 2 は段 A の指示文に「質問の形の推理も推理に入れる」と書いていたため、はい / いいえ質問の大半が推理に流れた</li>
  <li><strong>試行 2</strong>: パターン 2 の段 A の指示文を設計どおりに直して再実行。パターン 2 = {pct(*acc(rows(R2, "p2"))):.1f}%（パターン 1 は試行 1 のまま）。このあと、出力上限 400 → 800・effort <code>xhigh</code> をユーザーが承認</li>
  <li><strong>試行 3</strong>（ユーザー指示）: パターン 1 はプロンプトに開示文 70 字以内・作品へのけなしは ⑮・主語が曖昧な質問は ③ を追加。パターン 2 は段 A を「A1 大分類 6 択（問題文なし）→ A2 細分類」の 2 段に変えた。パターン 1 = {pct(*acc(rows(R3, "p1"))):.1f}%、パターン 2 = {pct(*acc(rows(R3, "p2"))):.1f}%</li>
  <li><strong>試行 4</strong>（次の打ち手の候補をそのまま実施）: パターン 1 は曖昧な主語の例文・漢字だけの中国語の扱いを追加（絵のルールは誤変換だったので削除）。パターン 2 は要点を「1 要点 = 1 事柄」の 4〜5 個に割り、惜しいの閾値 0.35 を新設、段 0 の英字の規則を外した。新しい質問 32 件を足して 220 件。パターン 1 = {pct(*acc(rows(R4, "p1"))):.1f}%、パターン 2 = {pct(*acc(rows(R4, "p2"))):.1f}%。このあと、出力上限 800 → 1,200 をユーザーが承認</li>
  <li><strong>試行 5</strong>（ユーザー判断 + 判断不要の打ち手）: パターン 1 は「確定事実に直接書いていなくても、真相から明らかに違うことは いいえ」を手順 2 に追加。パターン 2 は正解判定を「要点の 75% 以上」に緩め（ユーザー承認）、A2 が ③ を選んだときだけ問題文つきで確かめ直す段 A3 を新設（ユーザー指示）、段 0 の英字の規則を「英単語 2 語以上なら ㉒」で戻し、段 B の呼び出しを 1 回にまとめた。パターン 1 = {pct(*acc(rows(R5, "p1"))):.1f}%、パターン 2 = {pct(*acc(rows(R5, "p2"))):.1f}%</li>
  <li><strong>試行 6</strong>（ユーザー指示）: パターン 1 は出力上限を 2,400 に上げただけ（プロンプトは変えていない）。パターン 2 は大分類の「質問」と「推理」を 1 つにまとめ、問題文を渡して振り分け直す段 A1b を新設。指示語を含む ① も段 A3 で確かめ直し、要点の判定を「言い換えも含めて」に変えた。6a（最大確率で振り分け）= {pct(*acc(rows(R6A, "p2"))):.1f}% に悪化したため、推理の確率 0.95 以上だけ推理にする 6b に直して再実行。パターン 1 = {pct(*acc(rows(R6, "p1"))):.1f}%、パターン 2（6b）= {pct(*acc(rows(R6, "p2"))):.1f}%</li>
  <li><strong>試行 7</strong>（ユーザー合意のコア基準）: 推理の ④⑤⑥ を「コア（その問題の仕掛け）に触れたか」で判定するよう、要点をコア 1〜2 個と周辺に分け、両方式の判定を変えた。7（最初の実行）はパターン 1 が OpenAI のレート制限で 14 件失敗したため、再試行を入れて 7a でパターン 1 だけ再実行。7a はパターン 1 が外れた推理を大量に ⑤ にし（推理系 73.3%）、パターン 2 は ⑤ を取りこぼした。7b でパターン 1 に「コアに触れる」の意味を足し、パターン 2 の惜しいの閾値を 0.25 に下げた。パターン 1 = {pct(*acc(rows(R7, "p1"))):.1f}%、パターン 2 = {pct(*acc(rows(R7, "p2"))):.1f}%</li>
  <li><strong>試行 8</strong>（ユーザー指示）: パターン 1 は「コアの一部を確かめる質問は推理にせず はい / いいえ で答える」を手順 1 に追加。パターン 2 は段 A1b の推理の条件に「コアの要点のどれかが 0.25 以上」を足し、段 A3 の閾値を 0.6 に上げた。8a はどちらも推理系が悪化（パターン 1 は「〜かな」で終わる惜しい推理を質問にした、パターン 2 は定義上コアに触れない外れた推理まで質問に戻した）。8b でパターン 1 の対象を「事実を 1 つだけ確かめる短い質問」に絞り、パターン 2 は質問に戻したものが「答えられない質問」なら推理（外れ）に戻すようにした。パターン 1 = {f("p1", "全体")}、パターン 2 = {f("p2", "全体")}</li>
</ul>
<figure class="diagram">
{chart_trials}
<figcaption>試行ごとの種別一致率の推移（件数は 185 / 185 / 188 / 220 件以降。試行 6 のパターン 2 は 6b、試行 7 は 7b、試行 8 は 8b。すべて最新のラベルで数え直した値）</figcaption>
</figure>

<h2 id="compare">4. パターン 1 とパターン 2 の比較（全試行）</h2>
<p class="trend-note">1 行 = 1 項目。横軸は試行 1〜8、縦は 0〜100%（点線はレベル 1 の基準）、右端の数字は試行 8 の値。点に触れると件数が出る。試行 6 のパターン 2 は 6b、試行 7 は 7b、試行 8 は 8b。すべて最新のラベルで数え直した値（試行 1〜3 は新しい質問が無いので、その行は試行 4 から）。</p>
<h3>区分別の推移</h3>
<figure class="diagram">
{trend_groups}
<figcaption>区分別の種別一致率と ① の判定一致（点線 = 全体の基準 90%）</figcaption>
</figure>
<p class="trend-note">数値（<span class="t1">■</span> パターン 1 / <span class="t2">■</span> パターン 2。割合（一致件数 / 件数）。スマホでは表を横にスクロール）</p>
{table_groups}
<h3>種別ごとの推移</h3>
<p class="trend-note">系統ごとに折りたたんである（質問系・推理系は開いた状態）。点線 = 質問以外の種別の基準 80%。</p>
{trend_kinds}
<details class="trend-block"><summary>試行 8 時点の棒グラフ（件数つき）</summary>
<figure class="diagram">
{chart_groups}
<figcaption>区分別の種別一致率と ① の判定一致（試行 8）</figcaption>
</figure>
<figure class="diagram">
{chart_kinds}
<figcaption>種別ごとの一致率（試行 8。各 5〜83 件）</figcaption>
</figure>
</details>

<h3>P1〜P7 の結果（試行 8b）</h3>
<ul>
  <li><strong>P1 漏れ候補</strong>: 両方式とも 0 件 <span class="pass">合格</span></li>
  <li><strong>P2 誤った正解宣言</strong>: 両方式とも 0 件 <span class="pass">合格</span></li>
  <li><strong>P3 はい / いいえの取り違え</strong>: 両方式とも 0 件 <span class="pass">合格</span></li>
  <li><strong>P4 いいえ / 関係ありません の揺れ</strong>: 両方式とも 0 件 <span class="pass">合格</span></li>
  <li><strong>P5 正解宣言率</strong>: 両方式とも 10/11（90.9%）<span class="pass">合格</span></li>
  <li><strong>P6 ⑱⑲ を定型文で返した割合</strong>: パターン 1 = 10/10（100%）<span class="pass">合格</span> / パターン 2 = 9/10（90%）<span class="pass">合格</span>。⑱〜㉑ に判定語を返した・⑳㉑ に返信した・普通のコメントを不適切と誤判定は両方式とも 0 件</li>
  <li><strong>P7 80 字超</strong>: 両方式とも 0 件 <span class="pass">合格</span></li>
  <li><strong>① の判定一致</strong>: パターン 1 = 従来 {yn_old("p1")} / 新しい質問 {yn_new("p1")}、パターン 2 = 従来 {yn_old("p2")} / 新しい質問 {yn_new("p2")}</li>
  <li><strong>レベル 1 の種別一致率</strong>（全体 90% 以上・質問以外の各種別 80% 以上）: <strong>両方式とも合格</strong>。パターン 1 = 全体 98.2%（最も低い種別は ⑤ 7/8・⑨ 4/5）<span class="pass">合格</span> / パターン 2 = 全体 96.4%（最も低い種別は ⑭ ⑱ ㉒ 4/5・⑥ 9/11）<span class="pass">合格</span>。ただし ⑤ は 8 件・⑦〜㉒ は各 5 件しかなく、1 件で合否が割れる</li>
</ul>
<h3>応答時間・トークン・金額（試行 8b）</h3>
<div class="card-grid">
  <div class="card"><div class="card-title">応答時間（中央値）</div><p>パターン 1: 2.0 秒（p95 3.9 秒・最大 11.7 秒）<br>パターン 2: 0.76 秒（最大 2.3 秒）</p></div>
  <div class="card"><div class="card-title">トークン</div><p>パターン 1: 入力 合計 60 万・出力 平均 144（うち推論 102）・最大 1,148（上限 2,400）<br>パターン 2: 入力 合計 57 万（出力は無料）</p></div>
  <div class="card"><div class="card-title">金額（1 件あたり）</div><p>パターン 1: $0.00035（約 0.05 円）<br>パターン 2: $0.00011（約 0.016 円）</p></div>
  <div class="card"><div class="card-title">金額（月 6,000 件の見込み）</div><p>パターン 1: $2.07（約 310 円）<br>パターン 2: $0.65（約 98 円）<br>どちらも月数百円で、方式選定の決め手にはならない水準</p></div>
</div>
<p><strong>試走で使った金額（試算）</strong>: {trial_costs}。8 回の合計 {trial_cost_total}。</p>
<div class="note">
  <span class="callout-title">運用上の注意: OpenAI のレート制限（試行 7）</span>
  パターン 1 を 6 並列で呼んだら 429（1 分あたりのトークン数の上限）で失敗した。試走スクリプトに 429・5xx の再試行（指数バックオフ・3 回まで）を入れ、3 並列に下げた。本番の Reply Lambda の再試行（SQS）でも 429 を再試行の対象にしておく（21-6c・21-6f）。
</div>

<h2 id="p1">5. パターン 1（gpt-6-luna の一括方式）</h2>
<h3>5.1 処理方式</h3>
<figure class="diagram">
{flow_p1()}
<figcaption>パターン 1: LLM に 1 回で種別・判定・返信文を出させ、不適切系だけコードが上書きする</figcaption>
</figure>
<ul>
  <li><strong>呼び出し</strong>: コメント 1 件につき chat completions を 1 回。<code>response_format</code> を JSON スキーマ（strict）にし、<code>{{種別, 判定, 返信文}}</code> を返させる。429・5xx は待ってから 3 回まで再試行する</li>
  <li><strong>プロンプト</strong>: 5.1 のマスタープロンプトを改訂した <code>judge-trial/prompts/pattern1_rules.txt</code>。手順 1 で 22 種を定義して種別を選ばせ、手順 2 で判定、手順 3 で種別ごとの返し方を書く。⑱〜㉑ は返信文を空にしてコードに任せる</li>
  <li><strong>推理の判定（コア基準）</strong>: 問題ごとの「コアの要点」（1〜2 個）を渡し、④ = コアをすべて言い当てて明らかな誤りがない、⑤ = コアのどれかに触れている、⑥ = コアに触れていない。「問題文の言葉を使っているだけ、問題文どおりの読み方をしているだけではコアに触れていない」（試行 7）。「問題文の言葉や事実を 1 つだけ確かめる短い質問は、コアの一部に触れていても はい / いいえ で答える。自分の言葉で説明して『〜かな』『〜じゃない？』を付けたものは推理」（試行 8b）</li>
  <li><strong>そのほかのルール</strong>: 開示文 70 字以内・作品へのけなしは ⑮・主語が曖昧な質問は ③・漢字だけの中国語・真相から明らかに違うことは いいえ（試行 3〜5）</li>
  <li><strong>パラメータ</strong>: effort <code>xhigh</code>・出力上限 2,400・温度は送らない</li>
</ul>
<h3>5.2 結果（試行 8）</h3>
<ul>
  <li><strong>8a（「コアの一部を確かめる質問は はい / いいえ」を足した直後）: 推理系が 73.3% に悪化</strong>。「病院に通ってたのかな？」「〜渡ったんじゃない？」のように、推理の最後に「〜かな」「〜じゃない？」を付けた惜しい推理 5 件を質問として はい と答えた</li>
  <li><strong>8b（対象を「事実を 1 つだけ確かめる短い質問」に絞った版）: {f("p1", "全体")}</strong>。推理系 28/30（⑤ 7/8・⑥ 11/11）、③ 14/14、① の判定 {yn_old("p1")}・新しい質問 {yn_new("p1")}。<strong>P1〜P7 とレベル 1 の機械基準をすべて満たした</strong></li>
  <li>残った誤り: 「影が薄くなったのは、男の病気が良くなってきた知らせなんだね」を ⑤（④ が正解。パターン 2 も同じ）、「影は男の存在感のことじゃなくて、体の写真に写ったもの。病院に通ってたのかな？」を質問（⑤ が正解）、「その子は彼に会ったことがある？」を聞き直し（① が正解）、「これ中の人？自動で返してる？」を ②</li>
  <li>出力の最大は 1,148 トークン（上限 2,400）・応答時間の最大は 11.7 秒</li>
</ul>
<p>誤りの例:</p>
{p1_ex}
<h3>5.3 見えた課題と次の打ち手</h3>
<ul>
  <li>レベル 1 の機械基準・P1〜P7 はすべて満たした。これ以上は 5 問への合わせ込みになりやすいので、21-6d の全 14 問で件数を増やして見る</li>
  <li>応答時間の最大 11.7 秒 → 本番の Reply Lambda のタイムアウトは余裕を持って取る（21-6f）</li>
</ul>

<h2 id="p2">6. パターン 2（Jev の段階判定 + 定型文）</h2>
<h3>6.1 処理方式</h3>
<figure class="diagram">
{flow_p2()}
<figcaption>パターン 2: Jev の選択式（choice）と真偽の確率（noul）を段ごとに使い、返信文はすべてコードの定型文</figcaption>
</figure>
<ul>
  <li><strong>Jev の呼び方</strong>: <code>POST https://api.typesafe.ai/v1/systemone</code>（<code>model: jev-latest</code>）。<code>choice</code> は選択肢ごとの確率、<code>noul</code> は命題が真である確率を返す。指示文は英語、コメントと問題は日本語のまま渡す</li>
  <li><strong>段 0〜A2</strong>: 段 0 の文字種規則 → A1 大分類 5 択（問題文なし）→ A1b 質問か推理かの振り分け直し（問題文つき）→ A2 細分類</li>
  <li><strong>段 A1b の推理の条件（試行 8）</strong>: 推理の確率が 0.95 以上、かつコアの要点のどれかが 0.25 以上（段 B を先に取って使い回す）のときだけ推理。コアに全く触れないものはいったん質問に戻し、A2 が「はい / いいえで答えられる質問（①）」と判定すれば質問、「答えられない質問（③）」と判定すれば推理（⑥ 外れ）に戻す（8b）</li>
  <li><strong>段 A3 確かめ直し</strong>: ③、または指示語を含む ① を、問題文つきで確かめ直す。閾値を 0.5 → 0.6 に上げた（試行 8）</li>
  <li><strong>段 B 正解判定（コア基準）</strong>: コアの要点 1〜2 個がすべて 0.5 以上なら ④、推理でどれかが 0.25 以上なら ⑤、なければ ⑥</li>
  <li><strong>段 C・段 D・返信</strong>: 変えていない</li>
</ul>
<h3>6.2 結果（試行 8）</h3>
<ul>
  <li><strong>8a（コアへの接触を条件にした直後）: 推理系が 56.7% に悪化</strong>。⑥ 外れた推理は定義上コアに触れないので、11 件中 9 件まで質問に戻され、③ 答えられない質問になった（条件の設計の誤り）</li>
  <li><strong>8b（質問に戻して ③ になったら推理に戻す版）: {f("p2", "全体")}</strong>。これまでで最高。質問系 107/107・① の判定 {yn_old("p2")}・新しい質問 {yn_new("p2")}・③ 14/14（曖昧な主語も含めて全件）・推理系 26/30。<strong>P1〜P7 とレベル 1 の機械基準をすべて満たした</strong></li>
  <li>質問に戻す処理は 15 件で動き、短い はい / いいえ質問 4 件（「誰かのいたずらだった？」「濡れたものを乾かしたの？」「男はその子の主治医なの？」「曲の選び方を間違えたってこと？」）を質問に戻せた。外れた推理 10 件は A2 で ③ → 推理に戻った。逆に誤ったのは 2 件（「手紙は未来の誰かに宛てたもので…のかな」を ③、「隣の女性も…笑ったんだね」を ①）</li>
  <li>残った誤り: ④ → ⑤ 1 件・⑥ → ⑤ 1 件（「男は音楽のプロで、別の編曲だったから…」）、「手紙が届く前から知ってた？」に「答えに関わりません」、⑦〜㉒ の境目 4 件（「短めの問題リクエストです」「答えを聞いても腑に落ちないかも」「あああ???ぴょ」「答案是什么？」）</li>
</ul>
<p>誤りの例（括弧内は Jev が返した確率）:</p>
{p2_ex}
<h3>6.3 見えた課題と次の打ち手</h3>
<ul>
  <li>レベル 1 の機械基準・P1〜P7 はすべて満たした。閾値（推理 0.95・惜しい 0.25・確かめ直し 0.6 など）は 5 問で選んだ値なので、21-6d の全 14 問で確かめる</li>
  <li>⑦〜㉒ の境目の 4 件は試行 3 からほぼ同じ顔ぶれ。21-6d で件数を増やして、同じ型が多ければ手当てする</li>
</ul>

<h2 id="next">7. 次の試行の候補</h2>
<p>試行 8b で、両方式とも P1〜P7 とレベル 1 の機械基準を満たした。この試走は 5 問・220 件で、⑤ は 8 件・⑦〜㉒ は各 5 件しかなく 1 件で合否が割れる。閾値もこの 5 問で選んだ値なので、ここからの改善は 5 問への合わせ込みになりやすい。</p>
<ul>
  <li><strong>区切り（ユーザー判断 2026-09-28）</strong>: 判定品質の試行錯誤はここで完了。返信文の品質は 21-6b2、実装は 21-6c、全 14 問の判定は 21-6d（8 章）</li>
  <li>21-6d で比べたいもの: パターン 1 のプロンプトの版（試行 5 版 と 試行 8b 版）、パターン 2 の閾値</li>
</ul>


<h2 id="summary">8. 判定品質の検討のまとめと方針（21-6b 完了・2026-09-28）</h2>
<div class="decision">
  <span class="callout-title">暫定方針: パターン 1（luna）が主役。Jev は返信の判定には使わず「見張り役」と「真相を開示する前の二重確認」に使う（ユーザー。確定は 21-6e）</span>
  判定品質の試行錯誤はここで区切る。返信文そのものの品質（同じ判定でも「はい」「はい、食べたことがあります。」「うん。食べたことがあるよ🐢」のどれで返すか）は、21-6b2 で別の検討ページを立てて試行錯誤する。設計書側の記載は<a href="umigame-soup-1.html#judge-policy">セット別設計書 5.1.2 の暫定方針</a>。
</div>
<h3>8.1 組み合わせ方の試算（試行 8b の結果を組み替えて計算。API は呼び直していない）</h3>
<p>数字は「種別と、はい / いいえ の判定の両方が合っていた割合」（220 件）。</p>
<ul>
  <li><strong>パターン 1 単独</strong>: 98.2%（216/220）</li>
  <li><strong>パターン 2 単独</strong>: 94.5%（208/220）</li>
  <li><strong>案 1: 質問は Jev、推理とそれ以外は luna</strong>: 95.9%。質問の判定でも luna のほうが正確だったので、分担すると下がる</li>
  <li><strong>案 2: luna が主役で、判定が Jev と食い違ったら「答えに関わりません」に倒す</strong>: 94.1%。食い違い 9 件はすべて luna が正しかった</li>
  <li><strong>案 3: luna が主役で、正解宣言（真相の開示）だけは Jev も正解と判定したときに限る</strong>: 98.2% のまま（正解宣言率 10/11・誤った正解宣言 0 件）。成績を落とさずに、取り返しのつかない操作に安全装置を足せる → 採用</li>
</ul>
<h3>8.2 方針の中身</h3>
<ul>
  <li><strong>見張り役</strong>: 全コメントを Jev にも判定させ、返信には使わず、luna との食い違い率だけをログに残す。試走の平常値は種別 10/220・判定 9 件。平常値の 2 倍を超えたら通知する（生成 AI の品質低下にも、Jev 側の異常にも気づける）。費用は月 100 円前後</li>
  <li><strong>真相を開示する前の二重確認</strong>: 正解宣言は 2 方式がそろって「正解」のときだけ</li>
  <li><strong>意見が割れたとき</strong>（試行 7b で 2 件・試行 8b で 0 件。7b の 2 件はどちらも luna が正しかった）:
    <ul>
      <li>luna だけが正解 → 開示せず、専用の定型文（例「核心にかなり迫っています！何が起きたのかを通して説明してみてください」、言い回しは複数）で説明の追加を促す。食い違いをログに残してユーザーに通知し、手動で正解を伝えられるようにする（手段は 21-6c）</li>
      <li>Jev だけが正解 → 主役の luna の判定どおりに返し、ログにだけ残す</li>
      <li>理由: 状態を持たないので見逃しは次のコメントで取り返せるが、誤った開示は取り消せない</li>
    </ul>
  </li>
  <li><strong>そのほかの守り</strong>: 生成 AI のモデルを日付付きの ID で固定できれば固定し、モデル・プロンプトを変えるときは全件の機械プローブ（21-6d）に合格してから切り替える。パターン 2 への切り替えスイッチは残す（Jev にも SLA がない）</li>
</ul>
<h3>8.3 次のステップへ</h3>
<ul>
  <li><strong>21-6b2 返信文の品質の検討と試走</strong>: 別の検討ページで行う。今の返信文の作り方は、パターン 1 = プロンプト（<code>prompts/pattern1_rules.txt</code> 手順 3）、パターン 2 = 定型文（<code>templates.py</code>）。Jev の場合は判定のあとに軽量な LLM で文章を書く案も比べる</li>
  <li><strong>21-6c 実装</strong>: 両パターン + 見張り役 + 合意制（オン / オフ）+ 割れたときの定型文と通知。OpenAI の 429 の再試行</li>
  <li><strong>21-6d 全 14 問の機械プローブ</strong>: パターン 1 単独と「パターン 1 + 合意制」の比較、割れる頻度、パターン 1 のプロンプトの 2 版（試行 5 版・試行 8b 版）、パターン 2 の閾値（5 問で選んだ値）の見直し。⑦〜㉒ の境目の誤り（試行 3 からほぼ同じ顔ぶれ）も件数を増やして見る</li>
  <li>試走の資材: <code>content/umigame-stock/umigame-soup-1/judge-trial/</code>（<code>run_trial.py</code>・評価データ <code>data/</code>・このページの生成スクリプト <code>build_study_page.py</code>。結果のキャッシュ <code>work/</code> は gitignore でローカルにだけ残る）</li>
</ul>

</div>
<script>
// 前提パネル: 外側のクリック / Esc で閉じ、同時に開くのは 1 つだけ（name 属性が効かないブラウザー向け）
(function () {{
  var refs = Array.prototype.slice.call(document.querySelectorAll('details.ref'));
  refs.forEach(function (d) {{
    d.addEventListener('toggle', function () {{
      if (d.open) refs.forEach(function (o) {{ if (o !== d) o.open = false; }});
    }});
  }});
  document.addEventListener('click', function (ev) {{
    if (!ev.target.closest('#ref-bar')) refs.forEach(function (d) {{ d.open = false; }});
  }});
  document.addEventListener('keydown', function (ev) {{
    if (ev.key === 'Escape') refs.forEach(function (d) {{ d.open = false; }});
  }});
}})();
</script>
</body>
</html>
'''
OUT.write_text(page, encoding="utf-8")
print("wrote", OUT)
