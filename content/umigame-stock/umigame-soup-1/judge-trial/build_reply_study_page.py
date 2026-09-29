"""21-6b2 返信文の品質の検討ページを組み立てる。

入力は run_reply_trial.py の出力（work/reply_metrics.json・work/reply_compare.json。gitignore でこの PC にだけある）。
本文（基準・案・所見）はこのスクリプト内に直書きし、試行を足すたびに書き換えて再実行する。

    services/image-batch/.venv/bin/python content/umigame-stock/umigame-soup-1/judge-trial/build_reply_study_page.py
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = REPO / "docs" / "app" / "sets" / "umigame-soup-1-reply-study.html"
METRICS = HERE / "work" / "reply_metrics.json"
COMPARE = HERE / "work" / "reply_compare.json"
VARIANTS = HERE / "reply_variants.json"

UPDATED = "2026-09-29（21-6b2 ゴール 2: 候補を 4 案に絞り、絵文字の一覧と ⑧ の返し方を変えて 4 案を試走 2 回目。基準と見比べの確認待ち）"

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
    ("⑧ ネタバレ要求", "「質問には答えられるけど、真相は教えられないよ」の趣旨。「誰かが当てるまで秘密」のように、いつか明かす約束はしない", "決定（2026-09-29 ユーザー。当てた人が出ても明かす義務が生じないように）"),
    ("P1〜P7", "判定の正しさ（5.1.1）。特に P1 真相の漏洩 0 件・P7 80 字以内", "どの案でも満たす（変えない）"),
    ("一言の長さ", "判定語・定型の後ろに添える一言", "20 字以内（5.1.1 レベル 2）"),
    ("⑲ への一言", "誹謗中傷には一言を付けない", "0 件（5.1.1）"),
    ("⑱〜㉑ の扱い", "⑱⑲ はコードの定型文・⑳㉑ は返信しない", "LLM の文面を使わない（5.1.2 契約）"),
]
CRITERIA_HUMAN: list[tuple[str, str, str, str]] = [
    ("H1 口調の一貫性", "全部の返信が同じカメロックの声か。リールの台詞（「質問してみて！」「何度でも答えるよ」）とずれないか", "見比べで目視", "決定: リールに合わせたくだけた口調。パパが息子に話しかけるイメージ。一人称は「私」（ユーザー）"),
    ("H2 キャラらしさ", "探偵らしさ・カメらしさが出ているか。やりすぎて寒くないか", "「キャラが立っている」が過半数（レベル 2）", "叩き台"),
    ("H3 噛み合い", "コメントの中身に合っているか。汎用の一言が浮いていないか", "浮いている・ずれているが 1 割以下（レベル 2）", "叩き台"),
    ("H4 くどさ", "同じ投稿で 10 件続けて読んでも鬱陶しくないか。判定がひと目で分かるか", "見比べで目視", "叩き台"),
    ("H5 公平さ", "一言がヒントにならないか（「鋭い！」が「はい」にだけ付くと手がかりになる）", "近さを示す一言 0 件（M6）", "決定（ユーザー）"),
]
CRITERIA_MACHINE: list[tuple[str, str, str, str]] = [
    ("M1 字数", "全体・種別ごとの平均と最大、一言の字数", "全体 80 字以内・一言 20 字以内", "決定（P7・レベル 2）"),
    ("M2 冒頭の判定語", "① の返信が判定に合う判定語で始まるか", "100%", "叩き台"),
    ("M3 言い回しの散らばり", "種別ごとの異なる言い回しの数・最頻の割合・一言なしの割合", "最頻 50% 以下（レベル 1）。一言は候補に「一言なし」を 1 つ混ぜて選び、判定語だけの返事（「はい！」）も言い回しの 1 通りとして数える", "決定（レベル 1・一言の割合はユーザー）"),
    ("M4 漏れ候補", "CORE 語（leak_count.py）と、コメントにない内容語（許可語を除く）", "CORE 語 0 件・内容語は全件を人が確認", "決定: ① の復唱は質問の言葉の範囲で許す（推理への返事では禁止）。質問にない語の混入は 0 件（ユーザー）"),
    ("M5 絵文字", "絵文字の件数・種類。⑮⑲・正解の開示に付いていないか", "一覧（☺️ 😌 😉 🧐 🙂‍↕️ 🙂‍↔️ 🥳 🙌 👏 🤔 🫢 🤭 🤐）から 1 個まで。⑮⑲・正解の開示には付けない", "決定（ユーザー。2026-09-29 に一覧を差し替え。当初は 🐢 🔍 🥣 📝）"),
    ("M6 近さを示す語", "「鋭い」「いい線」「核心」など。① と ⑥ の返信", "0 件（合意制の定型文は除く）", "決定（ユーザー）"),
    ("M7 費用・応答時間", "軽量 LLM を呼ぶ案だけ。応答時間の中央値・p95・最大、1 件あたりの金額", "参考値（方式選定は 21-6e）", "叩き台"),
]
OPEN_DECISIONS: list[str] = [
    "基準（1.1〜1.3）と見比べ（4 章）の確認（ユーザー。21-6b2 の人間ゲート）",
]

# ② 作り方の案（name, 判定元, 文章の作り方, 真相を渡すか, 費用・応答時間, 状態）
VARIANT_PLANS: list[tuple[str, str, str, str, str, str]] = [
    ("1a", "パターン 1（luna）", "今のプロンプト（pattern1_rules.txt 手順 3）のまま", "渡す（判定と同じ呼び出し）", "追加なし", "試走 1 回目済み"),
    ("1b", "パターン 1（luna）", "手順 3 を作り直す（口調・絵文字・復唱の規則とキャラ設定。例文は評価データにない汎用文）", "渡す", "追加なし（本番は判定と 1 回の呼び出し）", "試走 1 回目済み"),
    ("1c", "パターン 1（luna）", "luna は判定だけ。返信文はコードの定型文（templates.py）", "—（文を作らない）", "追加なし", "試走 1 回目済み"),
    ("1d", "パターン 1（luna）", "luna の判定のあとに軽量な LLM で文章を書く（2c と同じ書き手。2026-09-28 ユーザー指示で追加）。④ は reveal_text の固定文・⑱〜㉑ はコード", "渡さない（コメント本文・種別・判定だけ）", "2c と同じ", "試走 1 回目済み（書き手 4 モデル = 1d-luna・1d-q9b・1d-qflash・1d-gemma）"),
    ("2a", "パターン 2（Jev）", "今の定型文（templates.py）", "—（文を作らない）", "追加なし", "試走 1 回目済み"),
    ("2b", "パターン 2（Jev）", "定型文を ① の基準で書き直し、種別ごとに 6〜10 通りに増やす", "—（文を作らない）", "追加なし", "試走 1 回目済み"),
    ("2c", "パターン 2（Jev）", "Jev の判定のあとに軽量な LLM で文章を書く。④ は reveal_text の固定文・⑱〜㉑ はコード", "渡さない（コメント本文・種別・判定だけ）", "実測は 3 章 M7（gpt-6-luna effort low・OpenRouter の Qwen3.5-9B / Qwen3.5-Flash・Gemini API の Gemma 4 26B-A4B〔無料枠〕）", "試走 1 回目済み（2c-luna・2c-q9b・2c-qflash・2c-gemma）"),
]


FINDINGS: list[str] = [
    "<strong>書き手が luna の案（1b・1d-luna・2c-luna）と定型文の案（1c・2a・2b）は、機械の基準をほぼ満たした</strong>。判定の食い違い（M2b）0〜1 件・CORE 語 0 件・近さを示す語 0 件・絵文字は一覧の中だけ。"
    "① の形の割り振り（判定語だけ / 復唱 / 一言を 1:1:2）も守り、判定語だけの返事が 29% 前後（割り振りの 25% とほぼ同じ）。2c-luna の食い違い 1 件は「いいえ。曲名は謎の答えに関係ないよ。」",
    "<strong>小型モデル（Qwen3.5-9B・Qwen3.5-Flash・Gemma 4 26B-A4B）は、判定を書き換える</strong>。① の返信が決まった判定語で始まる割合 86〜98%、判定の食い違い 3〜21 件"
    "（例: 判定が「いいえ」なのに「いいえ。家族かどうかは関係ないんだよ」、Gemma が種別のコード「q_open」をそのまま書く、Qwen3.5-9B がプロンプトの「種別 q_yesno / 答え no」を返信に漏らす）。"
    "真相を渡していないのに、Qwen3.5-9B は存在しない事実を作って外れた推理に説明を付けた（「隣の見守る男が、娘の失敗を…」）。真相の漏洩ではないが、誤った手がかりを与える",
    "<strong>小型モデルは形の指定を守らない</strong>: 判定語だけの返事 0〜1%（指定は 25%）、絵文字が 159〜191 件/220 件（「付けないほうが多くてよい」を無視）。Qwen3.5-9B は一覧外の絵文字 12〜13 件・2 個以上 9 件・改行 46〜58 件、⑮ クレームや ④ 開示にも絵文字を付けた",
    "<strong>応答時間</strong>: Qwen3.5-Flash が最速（中央値 0.7 秒）、luna（effort low）1.3〜1.5 秒、Qwen3.5-9B 1.8〜2.0 秒（p95 3〜8 秒）、Gemma 4（Gemini API 無料枠）は中央値 1.5 秒だが p95 33 秒・最大 66 秒（レート制限の再試行）。1b（luna xhigh・真相あり）は中央値 2.4 秒・p95 4.0 秒で、本番のパターン 1 は判定と返信を 1 回で出すので追加の呼び出しはない",
    "<strong>費用（今回の 220 件あたり）</strong>: 1b $0.053・1d/2c-luna $0.030・Qwen3.5-9B $0.022・Qwen3.5-Flash $0.014・Gemma 4 $0（無料枠）。どれも 1 件 0.02 円以下で、費用は選ぶ決め手にならない",
    "<strong>2b（定型文の作り直し）</strong>は API を呼ばず、食い違い・漏れ・近さの語がすべて 0。代わりに ① の一言は 9 通り（+ 一言なし）で、噛み合い（H3）はコメントに合わせられない",
]


FINDINGS_RUN2: list[str] = [
    "<strong>4 案とも機械の基準をほぼ満たしたまま</strong>: 80 字超 0 件・① の判定語で始まる割合 100%（2b・2c-luna は Jev の判定の 1 件が冒頭で外れる = 83/84。1 回目と同じ）・判定の食い違いは 2c-luna の 1 件だけ・CORE 語 0 件・近さの語 0 件・④⑮⑲ への絵文字 0 件",
    "<strong>⑧ ネタバレ要求</strong>は 4 案とも「質問には答えられるけど、真相は教えられないよ」の形になり、「誰かが当てるまで」は 0 件。luna の案は同じ文で始まることが多く（例: 1b・2c-luna は 5〜6 件中ほぼ全部が同じ出だし）、2b は 6 通りを散らしている",
    "<strong>絵文字</strong>: 付いた返信は 1b 50 件・1d-luna 45 件・2c-luna 48 件・2b 58 件（220 件中。1 回目の luna の案は 12〜19 件で、一覧が増えて付けやすくなった）。"
    "<strong>luna は 🙂‍↕️（うなずき）・🙂‍↔️（首振り）を出せず、ただの 🙂 を書いた</strong>（1b 21 件・1d-luna 21 件・2c-luna 20 件。プロンプトの一覧には合成絵文字が正しく入っているが、出力に合成絵文字は 0 件）。定型文の 2b はそのまま出せる",
    "<strong>応答時間と費用</strong>（220 件）: 1b 中央値 2.2 秒・p95 3.6 秒・$0.054、1d-luna 1.4 秒・2.8 秒・$0.032、2c-luna 1.4 秒・2.5 秒・$0.033、2b は API を呼ばない",
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
        m7 = v.get("M7_llm")
        if m7 and m7.get("request_count"):
            lat = m7["latency_s"]
            per = (m7["cost_usd"] or 0) / m7["request_count"] * 1000
            m7_text = f"{lat['median']:.1f} / {lat['p95']:.1f} / {lat['max']:.1f} 秒・1,000 件 ${per:.3f}"
        else:
            m7_text = "—（API を呼ばない）"
        rows.append([
            f"<strong>{esc(name)}</strong> {esc(v.get('label'))}",
            f"{m1['average_chars']:.1f} / {m1['max_chars']}（80 字超 {m1['over_80_count']}）",
            f"{m2['starts_rate']:.0%}（{m2['starts_count']}/{m2['q_yesno_count']}）",
            f"{m2.get('conflict_count', 0)}",
            f"{yes['distinct_replies']} 種・最頻 {yes['most_frequent_rate']:.0%}・一言なし {m3['q_yesno_one_liner_empty_rate']:.0%}",
            esc("、".join(over) or "なし"),
            f"CORE {m4['core_count']}・内容語 {m4['comment_missing_content_words_count']}",
            f"{m5['reply_count']}（一覧外 {m5.get('unlisted_reply_count', 0)}・2 個以上 {m5.get('multiple_emoji_reply_count', 0)}）",
            f"{m6['count']}",
            m7_text,
            f"{v.get('error_count', 0)}",
        ])
    head = ["案", "M1 字数 平均 / 最大", "M2 判定語", "M2b 判定の食い違い", "M3 ① の一言", "M3 最頻 50% 超の種別（3 件以上）",
            "M4 漏れ候補", "M5 絵文字", "M6 近さ", "M7 応答 中央値 / p95 / 最大・費用", "エラー"]
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


EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def per_variant_section(compare: dict | None, metrics: dict | None) -> str:
    """案ごとに、その案の判定した種別で返信をまとめた表（件数・字数・散らばり・絵文字・機械検査・例）。"""
    if not compare or not metrics:
        return "<p>データはまだない。</p>"
    variants = {v["name"]: v for v in json.loads(VARIANTS.read_text(encoding="utf-8"))}
    parts = []
    for name, m in metrics["variants"].items():
        method = variants.get(name, {}).get("source_method", "p1")
        flagged: dict[str, list[str]] = {}
        for it in m["M2_answer_word"].get("conflict_items", []):
            flagged.setdefault(it["id"], []).append("食い違い")
        for group in m["M4_leak_candidates"]["core_by_no"].values():
            for it in group["items"]:
                flagged.setdefault(it["id"], []).append("CORE 語")
        for it in m["M6_proximity"]["items"]:
            flagged.setdefault(it["id"], []).append("近さ")
        by_kind: dict[str, list[tuple[str, str | None]]] = {}
        for case_id, case in compare["cases"].items():
            kind = (case.get("kind") or {}).get(method) or "other"
            by_kind.setdefault(kind, []).append((case_id, case.get("variants", {}).get(name)))
        rows = []
        for code, kname in KINDS:
            items = sorted(by_kind.get(code, []))
            if not items:
                continue
            replies = [r for _, r in items if r is not None]
            lengths = [len(r) for r in replies]
            counter = Counter(replies)
            if replies:
                top, top_n = counter.most_common(1)[0]
                top_text = f"{esc(top) or '（空）'}（{top_n}/{len(replies)}・{top_n / len(replies):.0%}）"
                length_text = f"{sum(lengths) / len(lengths):.1f} / {max(lengths)}"
            else:
                top_text, length_text = "（返信しない）", "—"
            emoji = sum(bool(EMOJI_RE.search(r)) for r in replies)
            flags = Counter(f for cid, _ in items for f in flagged.get(cid, []))
            flag_text = "・".join(f"{k} {v}" for k, v in flags.items()) or "—"
            seen: list[str] = []
            for _, r in items:
                if r is not None and r not in seen:
                    seen.append(r)
                if len(seen) == 2:
                    break
            examples = "<br>".join(esc(r).replace("\n", " ⏎ ") for r in seen) or "—"
            rows.append([esc(kname), str(len(items)), length_text, str(len(counter)), top_text, str(emoji),
                         flag_text, examples])
        head = ["種別（この案の判定）", "件数", "字数 平均 / 最大", "異なる言い回し", "最も多い言い回し", "絵文字", "機械検査", "返信の例（最初の 2 通り）"]
        judge = "パターン 1（luna）" if method == "p1" else "パターン 2（Jev）"
        parts.append(
            f'<details class="cmp-kind"><summary>{esc(name)} {esc(m.get("label"))}</summary>'
            f'<p class="trend-note">種別は{judge}の判定（試行 8b）。機械検査は判定の食い違い（M2b）・CORE 語（M4）・近さの語（M6）の件数。</p>'
            f'{table(head, rows, "per-variant")}</details>'
        )
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
table.per-variant {{ font-size: .82rem; }}
table.per-variant td:nth-child(1) {{ white-space: nowrap; font-weight: 700; }}
table.per-variant td:nth-child(5), table.per-variant td:nth-child(8) {{ min-width: 14rem; }}
details.cmp-kind {{ margin: .5rem 0; border: 1px solid var(--border); border-radius: 8px; padding: 0 .6rem; }}
details.cmp-kind > summary {{ cursor: pointer; font-weight: 700; font-size: .95rem; padding: .5rem 0; min-height: 36px; }}
.cmp-card {{ border-top: 1px solid var(--border); padding: .5rem 0; }}
.cmp-q {{ margin: 0 0 .3rem; font-weight: 600; }}
.cmp-id {{ font-size: .75rem; color: var(--text-muted); margin-right: .5rem; font-weight: 400; }}
.cmp-diff {{ display: block; font-size: .78rem; color: var(--text-muted); font-weight: 400; }}
.cmp-dl {{ display: grid; grid-template-columns: 5.5rem 1fr; gap: .15rem .5rem; margin: 0; font-size: .9rem; }}
.cmp-dl dt {{ font-weight: 700; color: var(--text-muted); }}
.cmp-dl dd {{ margin: 0; overflow-wrap: anywhere; white-space: pre-line; }}
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
<h3 id="open">1.4 判断待ちの論点（基準は 2026-09-28 にすべて決定）</h3>
<ul>{decisions}</ul>

<h2 id="variants">2. 返信文の作り方の案</h2>
<div class="decision"><span class="callout-title">決定（2026-09-29、ユーザー）: 以降のステップは 1b・1d-luna・2b・2c-luna の 4 案から決める（方式の選定は 21-6e）</span>
小型モデル（Qwen3.5-9B・Qwen3.5-Flash・Gemma 4 26B-A4B）の書き手は、判定を書き換える食い違いが 3〜21 件出たため候補から外した。試走 2 回目（3.2）はこの 4 案だけを、差し替えた絵文字の一覧と ⑧ の返し方で作り直した。</div>
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
<h3 id="findings2">3.1 試走 2 回目で分かったこと（2026-09-29・4 案）</h3>
<ul>{"".join(f"<li>{f}</li>" for f in FINDINGS_RUN2)}</ul>
<p class="trend-note">上の表の 1b・1d-luna・2b・2c-luna は 2 回目、そのほかは 1 回目の結果（一覧外の絵文字は差し替えた一覧で数え直した）。</p>
<h3 id="findings">3.2 試走 1 回目で分かったこと（2026-09-28・13 案）</h3>
<ul>{"".join(f"<li>{f}</li>" for f in FINDINGS)}</ul>

<h2 id="compare">4. 種別ごとの見比べ</h2>
<p>同じコメントに対する案ごとの返信を並べる。種別は評価データの正解ラベルで分けた（判定が違った案は「判定が違う」と書く）。括弧内は ① の判定。</p>
{compare_section(compare, variant_names)}

<h2 id="per-variant">5. 案ごとの種別別の結果</h2>
<p>案を 1 つ開くと、その案の返信を種別ごとにまとめて見られる（4 章はコメントごとに案を並べる、この章は案ごとに種別を並べる）。種別はその案が使った判定（パターン 1 か 2）の結果で分けた。</p>
{per_variant_section(compare, metrics)}

<h2 id="next">6. 次の打ち手の候補（人間ゲートのあと）</h2>
<ul>
  <li>小型モデルを残すなら、判定語はコードが付けて、書き手には判定語のあとの一言（20 字以内）だけを書かせる形を試す（判定を書き換える余地をなくす。種別のコードやプロンプトの文面を返信に写す事故も、返信を一言に限れば見つけやすい）</li>
  <li>書き手の出力に機械の検査（判定語との食い違い・一覧外の絵文字・改行・種別のコード）をかけ、落ちたら定型文（2b）に差し替える安全網を試す</li>
  <li>1b（luna の手順 3 の作り直し）は、判定を含めた 1 回の呼び出しで試行 8b の判定品質が保たれるかを 21-6d で確かめる（今回は判定を固定したので、判定品質への影響は測っていない）</li>
  <li>方式の選定はしない（21-6e）</li>
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
