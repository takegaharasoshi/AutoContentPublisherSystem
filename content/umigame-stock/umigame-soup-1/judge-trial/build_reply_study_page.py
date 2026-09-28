"""21-6b2 返信文の品質の検討ページを組み立てる。

入力は run_reply_trial.py の出力（work/reply_metrics.json・work/reply_compare.json。gitignore でこの PC にだけある）。
本文（基準・案・所見）はこのスクリプト内に直書きし、試行を足すたびに書き換えて再実行する。

    services/image-batch/.venv/bin/python content/umigame-stock/umigame-soup-1/judge-trial/build_reply_study_page.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = REPO / "docs" / "app" / "sets" / "umigame-soup-1-reply-study.html"
METRICS = HERE / "work" / "reply_metrics.json"
COMPARE = HERE / "work" / "reply_compare.json"

UPDATED = "2026-09-28（21-6b2 ゴール 1: 基準の叩き台・案・見比べの枠。試走の本実行はゴール 2）"

# 種別の表示順と名前（5.1.1 の ①〜㉒）
KINDS: list[tuple[str, str]] = [
    ("q_yesno", "① はい / いいえ質問"), ("q_multi", "② 複数の質問"), ("q_open", "③ 答えられない・曖昧な質問"),
    ("guess_correct", "④ 正解推理"), ("guess_close", "⑤ 惜しい推理"), ("guess_wrong", "⑥ 外れた推理"),
    ("ask_hint", "⑦ ヒント要求"), ("ask_spoiler", "⑧ ネタバレ要求"), ("ask_howto", "⑨ 遊び方・アカウント"),
    ("impression", "⑩ 感想"), ("greeting", "⑪ 挨拶"), ("cheer", "⑫ 応援"), ("chat", "⑬ 雑談"),
    ("request", "⑭ リクエスト"), ("complaint", "⑮ 指摘・クレーム"), ("mention", "⑯ メンション"),
    ("emoji_only", "⑰ 絵文字だけ"), ("troll", "⑱ 荒らし"), ("abuse", "⑲ 誹謗中傷"), ("spam", "⑳ 宣伝・スパム"),
    ("personal_info", "㉑ 個人情報"), ("foreign", "㉒ 外国語"),
]
KIND_NAME = dict(KINDS)

# 基準（① 叩き台）。state: 決定 / 叩き台（ユーザー判断待ち）
CRITERIA_FIXED: list[tuple[str, str, str]] = [
    ("P1〜P7", "判定の正しさ（5.1.1）。特に P1 真相の漏洩 0 件・P7 80 字以内", "どの案でも満たす（変えない）"),
    ("一言の長さ", "判定語・定型の後ろに添える一言", "20 字以内（5.1.1 レベル 2）"),
    ("⑲ への一言", "誹謗中傷には一言を付けない", "0 件（5.1.1）"),
    ("⑱〜㉑ の扱い", "⑱⑲ はコードの定型文・⑳㉑ は返信しない", "LLM の文面を使わない（5.1.2 契約）"),
]
CRITERIA_HUMAN: list[tuple[str, str, str, str]] = [
    ("H1 口調の一貫性", "全部の返信が同じカメロックの声か。リールの台詞（「質問してみて！」「何度でも答えるよ」）とずれないか", "見比べで目視", "叩き台"),
    ("H2 キャラらしさ", "探偵らしさ・カメらしさが出ているか。やりすぎて寒くないか", "「キャラが立っている」が過半数（レベル 2）", "叩き台"),
    ("H3 噛み合い", "コメントの中身に合っているか。汎用の一言が浮いていないか", "浮いている・ずれているが 1 割以下（レベル 2）", "叩き台"),
    ("H4 くどさ", "同じ投稿で 10 件続けて読んでも鬱陶しくないか。判定がひと目で分かるか", "見比べで目視", "叩き台"),
    ("H5 公平さ", "一言がヒントにならないか（「鋭い！」が「はい」にだけ付くと手がかりになる）", "近さを示す一言 0 件（M6）", "叩き台"),
]
CRITERIA_MACHINE: list[tuple[str, str, str, str]] = [
    ("M1 字数", "全体・種別ごとの平均と最大、一言の字数", "全体 80 字以内・一言 20 字以内", "決定（P7・レベル 2）"),
    ("M2 冒頭の判定語", "① の返信が判定に合う判定語で始まるか", "100%", "叩き台"),
    ("M3 言い回しの散らばり", "種別ごとの異なる言い回しの数・最頻の割合・一言なしの割合", "最頻 50% 以下（レベル 1）", "決定（レベル 1）"),
    ("M4 漏れ候補", "CORE 語（leak_count.py）と、コメントにない内容語（許可語を除く）", "CORE 語 0 件・内容語は全件を人が確認", "叩き台"),
    ("M5 絵文字", "絵文字の件数・種類。⑮⑲・正解の開示に付いていないか", "決めた規則どおり", "叩き台"),
    ("M6 近さを示す語", "「鋭い」「いい線」「核心」など。① と ⑥ の返信", "0 件（合意制の定型文は除く）", "叩き台"),
    ("M7 費用・応答時間", "軽量 LLM を呼ぶ案だけ。応答時間の中央値・p95・最大、1 件あたりの金額", "参考値（方式選定は 21-6e）", "叩き台"),
]
OPEN_DECISIONS: list[str] = [
    "口調: (a) リールに合わせたくだけた口調（「はい！」「〜だよ」）/ (b) 今の丁寧な探偵口調 / (c) 判定語は丁寧・一言だけくだけた口調。一人称も決める",
    "絵文字: (a) 使わない / (b) 決めた一覧（🐢🔍🥣 など）から 1 個まで・⑮⑲ と開示には付けない / (c) 種別ごとに決める",
    "質問の復唱（「はい、食べたことがあります」）: (a) しない / (b) ① だけ質問の言葉の範囲で許す（推理への返事では禁止）",
    "一言を付ける割合: (a) 毎回 / (b) 半分くらい / (c) 判定語だけの返事も散らばりの 1 通りとして数える",
    "H5 と M6（近さを示す語の禁止）を基準に入れるか",
]

# ② 作り方の案（name, 判定元, 文章の作り方, 真相を渡すか, 費用・応答時間, 状態）
VARIANT_PLANS: list[tuple[str, str, str, str, str, str]] = [
    ("1a", "パターン 1（luna）", "今のプロンプト（pattern1_rules.txt 手順 3）のまま", "渡す（判定と同じ呼び出し）", "追加なし", "試走済み（試行 8b の返信）"),
    ("1b", "パターン 1（luna）", "手順 3 を作り直す（口調・絵文字・復唱の規則とキャラ設定。例文は評価データにない汎用文）", "渡す", "追加なし（本番は判定と 1 回の呼び出し）", "判断待ち"),
    ("1c", "パターン 1（luna）", "luna は判定だけ。返信文はコードの定型文（templates.py）", "—（文を作らない）", "追加なし", "試走済み（判定を固定して組み立て）"),
    ("2a", "パターン 2（Jev）", "今の定型文（templates.py）", "—（文を作らない）", "追加なし", "試走済み（試行 8b の返信）"),
    ("2b", "パターン 2（Jev）", "定型文を ① の基準で書き直し、種別ごとに 6〜10 通りに増やす", "—（文を作らない）", "追加なし", "判断待ち"),
    ("2c", "パターン 2（Jev）", "Jev の判定のあとに軽量な LLM で文章を書く。④ は reveal_text の固定文・⑱〜㉑ はコード", "渡さない（コメント本文・種別・判定だけ）", "gpt-6-luna effort low: 1 件約 $0.0001・応答 1〜3 秒の見込み（ゴール 2 で実測）", "判断待ち"),
]


def esc(text: object) -> str:
    return html.escape("" if text is None else str(text))


def table(head: list[str], rows: list[list[str]], cls: str = "") -> str:
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def metrics_section(metrics: dict | None) -> str:
    if not metrics:
        return "<p>集計はまだない（<code>run_reply_trial.py</code> を実行すると入る）。</p>"
    rows = []
    for name, v in metrics["variants"].items():
        m1, m2, m3 = v["M1_length"], v["M2_answer_word"], v["M3_variation"]
        m4, m5, m6 = v["M4_leak_candidates"], v["M5_emoji"], v["M6_proximity"]
        yes = m3["q_yesno_one_liner"]
        over = [
            f"{KIND_NAME.get(k, k).split(' ')[0]} {x['most_frequent_rate']:.0%}"
            for k, x in m3["by_kind"].items()
            if x.get("over_50_percent") and x.get("count", 0) >= 3 and k not in ("spam", "personal_info")
        ]
        rows.append([
            f"<strong>{esc(name)}</strong> {esc(v.get('label'))}",
            f"{m1['average_chars']:.1f} / {m1['max_chars']}（80 字超 {m1['over_80_count']}）",
            f"{m2['starts_rate']:.0%}（{m2['starts_count']}/{m2['q_yesno_count']}）",
            f"{yes['distinct_replies']} 種・最頻 {yes['most_frequent_rate']:.0%}・一言なし {m3['q_yesno_one_liner_empty_rate']:.0%}",
            esc("、".join(over) or "なし"),
            f"CORE {m4['core_count']}・内容語 {m4['comment_missing_content_words_count']}",
            f"{m5['reply_count']}",
            f"{m6['count']}",
        ])
    head = ["案", "M1 字数 平均 / 最大", "M2 判定語", "M3 ① の一言", "M3 最頻 50% 超の種別（3 件以上）", "M4 漏れ候補", "M5 絵文字", "M6 近さ"]
    note = (
        '<p class="trend-note">M3 の種別ごとの件数は ⑦〜㉒ が 5 件前後と少なく、定型文 3 通りでは偏りで 60% になりやすい'
        "（sha1 の選び方の偶然）。⑳㉑ は返信しないので除いた。</p>"
    )
    return table(head, rows, "metrics") + note


def compare_section(compare: dict | None, variant_names: list[str]) -> str:
    if not compare:
        return "<p>見比べのデータはまだない。</p>"
    by_kind: dict[str, list[tuple[str, dict]]] = {}
    for case_id, case in compare["cases"].items():
        by_kind.setdefault(case.get("expected_kind") or "other", []).append((case_id, case))
    parts = []
    for code, name in KINDS:
        rows = sorted(by_kind.get(code, []))
        if not rows:
            continue
        cards = []
        for case_id, case in rows:
            replies = case.get("variants", {})
            items = "".join(
                f"<dt>{esc(vn)}</dt><dd>{'（返信しない）' if replies.get(vn) is None else esc(replies.get(vn))}</dd>"
                for vn in variant_names
            )
            diff = [f"{m}: {KIND_NAME.get(k, k)}" for m, k in (case.get("kind") or {}).items() if k and k != code]
            diff_html = f'<span class="cmp-diff">判定の種別が違う → {esc(" / ".join(diff))}</span>' if diff else ""
            answers = sorted({a for a in (case.get("answer") or {}).values() if a})
            answer = f"（{esc(' / '.join(answers))}）" if answers else ""
            cards.append(
                f'<div class="cmp-card"><p class="cmp-q"><span class="cmp-id">{esc(case_id)}</span>'
                f'{esc(case["comment_text"])}{answer}{diff_html}</p><dl class="cmp-dl">{items}</dl></div>'
            )
        parts.append(f'<details class="cmp-kind"><summary>{esc(name)}（{len(rows)} 件）</summary>{"".join(cards)}</details>')
    return "\n".join(parts)


def build() -> str:
    metrics = load_json(METRICS)
    compare = load_json(COMPARE)
    variant_names = list(metrics["variants"].keys()) if metrics else []

    fixed = table(["項目", "中身", "合格ライン"], [[f'<span class="kid">{esc(a)}</span>', esc(b), esc(c)] for a, b, c in CRITERIA_FIXED])
    human = table(["観点", "何を見るか", "合格の目安", "状態"], [[f'<span class="kid">{esc(a)}</span>', esc(b), esc(c), esc(d)] for a, b, c, d in CRITERIA_HUMAN])
    machine = table(["観点", "何を数えるか", "合格の目安", "状態"], [[f'<span class="kid">{esc(a)}</span>', esc(b), esc(c), esc(d)] for a, b, c, d in CRITERIA_MACHINE])
    plans = table(["案", "判定", "返信文の作り方", "真相を渡すか", "費用・応答時間", "状態"], [[f"<strong>{esc(r[0])}</strong>", *(esc(c) for c in r[1:])] for r in VARIANT_PLANS])
    decisions = "".join(f"<li>{esc(d)}</li>" for d in OPEN_DECISIONS)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>コメント返信文の品質の検討 | AutoContentPublisherSystem</title>
<link rel="stylesheet" href="../../assets/style.css?v=20260921">
<style>
.kid {{ font-weight: 700; }}
table.metrics td {{ white-space: nowrap; }}
details.cmp-kind {{ margin: .5rem 0; border: 1px solid var(--border); border-radius: 8px; padding: 0 .6rem; }}
details.cmp-kind > summary {{ cursor: pointer; font-weight: 700; font-size: .95rem; padding: .5rem 0; min-height: 36px; }}
.cmp-card {{ border-top: 1px solid var(--border); padding: .5rem 0; }}
.cmp-q {{ margin: 0 0 .3rem; font-weight: 600; }}
.cmp-id {{ font-size: .75rem; color: var(--text-muted); margin-right: .5rem; font-weight: 400; }}
.cmp-diff {{ display: block; font-size: .78rem; color: var(--text-muted); font-weight: 400; }}
.cmp-dl {{ display: grid; grid-template-columns: 2.5rem 1fr; gap: .15rem .5rem; margin: 0; font-size: .9rem; }}
.cmp-dl dt {{ font-weight: 700; color: var(--text-muted); }}
.cmp-dl dd {{ margin: 0; overflow-wrap: anywhere; }}
</style>
</head>
<body>
<div class="container">

<nav class="breadcrumb"><a href="../../index.html">設計書体系ガイド</a> / <a href="../index.html">アプリ設計</a> / <a href="umigame-soup-1.html">探偵カメロックのウミガメのスープ</a> / コメント返信文の品質の検討</nav>
<h1>コメント返信文の品質の検討</h1>
<div class="page-meta">
  <span class="badge badge-draft">検討中（21-6b2）</span>
  <span>set_code: umigame-soup-1</span>
  <span>最終更新: {esc(UPDATED)}</span>
</div>

<div class="note">
  <span class="callout-title">このページの位置づけ</span>
  判定（種別・はい / いいえ・正解判定）が同じでも、返信文は「はい」「はい、食べたことがあります。」「うん。食べたことがあるよ🐢」のように変えられる。
  返信文そのものの品質の<strong>試行錯誤の記録</strong>をここに積み、決まったことだけを<a href="umigame-soup-1.html#quality-levels">セット別設計書 5.1.1</a>（レベル 2）・<a href="umigame-soup-1.html#judge-design">5.1.2</a> へ移す。
  判定品質の検討は<a href="umigame-soup-1-judge-study.html">コメント返信処理方式の検討</a>（21-6b で完了）。方式の選定はしない（21-6e）。
</div>

<h2 id="criteria">1. 前提: 返信文の品質の基準</h2>
<h3>1.1 どの案でも守ること（決定済み）</h3>
{fixed}
<h3>1.2 人が見る観点</h3>
{human}
<h3>1.3 機械で数える観点</h3>
{machine}
<h3 id="open">1.4 判断待ちの論点</h3>
<ul>{decisions}</ul>

<h2 id="variants">2. 返信文の作り方の案</h2>
<p>判定は試行 8b の結果（パターン 1 / パターン 2 それぞれ 220 件）に固定し、返信文だけを案ごとに作り直して比べる（判定を使い回すので費用と揺れを抑えられる）。試走スクリプトは <code>judge-trial/run_reply_trial.py</code>、案の定義は <code>judge-trial/reply_variants.json</code>。</p>
{plans}
<div class="note">
  <span class="callout-title">2c（Jev + 軽量 LLM）の漏洩の防ぎ方</span>
  書き手の LLM には<strong>コメント本文・種別・判定だけ</strong>を渡し、真相・確定事実・コアの要点を渡さない（真相を知らないので構造的に漏らせない）。④ の開示は問題ごとの <code>reveal_text</code>（固定文）、⑱〜㉑ はコードの定型文・返信しない。残る危険は、復唱のときに質問にない語を足すことで、M4 の「コメントにない内容語」で数える。
  モデル候補: 第 1 候補 = <code>gpt-6-luna</code> effort <code>low</code>（キー・仕組みが今のまま）。第 2 候補 = Claude Haiku 4.5（OpenAI が止まったときの逃げ道になるが、キーの追加が要る・価格は未確認）。Jev は選択式と確率だけで文章を作れない。
</div>

<h2 id="metrics">3. 機械の集計（案ごと）</h2>
<p>M1〜M6 の要約。詳細は <code>work/reply_report.md</code>（ローカルにだけある）。</p>
{metrics_section(metrics)}

<h2 id="compare">4. 種別ごとの見比べ</h2>
<p>同じコメントに対する案ごとの返信を並べる。種別は評価データの正解ラベルで分けた（判定が違った案は「判定が違う」と書く）。括弧内は ① の判定。</p>
{compare_section(compare, variant_names)}

<h2 id="next">5. 次の打ち手</h2>
<ul>
  <li>1.4 の判断を反映して、1b（luna の手順 3 の作り直し）・2b（定型文の作り直し）・2c（Jev + 軽量 LLM）を案の定義に足し、試走する（21-6b2 ゴール 2）</li>
  <li>M4 の許可語（<code>prompts/reply_allow_words.txt</code>）に、口調が決まったあとのキャラの汎用語（「探偵」「捜査」「推理」など）を足し、本当に見るべき語だけが残るようにする</li>
</ul>

</div>
</body>
</html>
"""


def main() -> None:
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
