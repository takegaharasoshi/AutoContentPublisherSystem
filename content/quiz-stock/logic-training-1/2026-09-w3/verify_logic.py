# 2026-09-w3 補充: 機械検証できる問題の答え合わせ
#
# なぞなぞ・とんち・水平思考の「想定解」は機械検証できない(人間レビューが唯一の砦)。
# ここではブルートフォース・全列挙・単純計算で確かめられるものだけを検証する。
# 今回のバッチに L3(フェルミ推定)は含まれないため、算数の検算セクションはない。
from __future__ import annotations

import math
import random
import sys
from itertools import combinations_with_replacement

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from stock_items import ITEMS

BY_NO = {it["no"]: it for it in ITEMS}
failures: list[str] = []


def check(no: str, label: str, ok: bool, detail: str) -> None:
    """1 件の検証結果を記録して表示する。

    Args:
        no: 問題番号。
        label: 検証項目名。
        ok: 検証が通ったか。
        detail: 表示する計算・列挙の要約。
    """
    mark = "OK " if ok else "NG "
    print(f"{mark}{no} {label}: {detail}")
    if not ok:
        failures.append(f"{no} {label}: {detail}")


# ---------------------------------------------------------------
# A40 5+5+5=550: 元の式が不成立で、「+」→「4」の置換後の式が成立すること(左右どちらの + でも)
# ---------------------------------------------------------------
if "A40" in BY_NO:
    check("A40", "元の式は不成立", (5 + 5 + 5) != 550, "5+5+5=15≠550")
    check("A40", "左の+を4に", 545 + 5 == 550, "545+5=550")
    check("A40", "右の+を4に(別解)", 5 + 545 == 550, "5+545=550")
    check("A40", "式は問題文に書かない(黒板で提示)", "5+5+5" not in BY_NO["A40"]["question"] and "5+5+5=550" in BY_NO["A40"]["illustration_scene"], "問題文に式なし・情景文に式あり")
    check("A40", "answer に 545+5=550", "545+5=550" in BY_NO["A40"]["answer"], BY_NO["A40"]["answer"])

# ---------------------------------------------------------------
# A41 日本語から英訳し、英単語のつづりを逆にして日本語へ戻す。
# 英訳の選択・法則の面白さ・任意の別法則の排除は機械検証の対象外。
# ---------------------------------------------------------------
if "A41" in BY_NO:
    pairs = [("犬", "dog", "神", "god"), ("網", "net", "十", "ten"),
             ("星", "star", "ネズミたち", "rats"), ("流れ", "flow", "オオカミ", "wolf")]
    for ja_src, en_src, ja_dst, en_dst in pairs:
        check("A41", f"英訳後の逆順 {ja_src}→{ja_dst}", en_src[::-1] == en_dst,
              f"{en_src} → {en_src[::-1]} = {en_dst}")
    kana_pairs = [("いぬ", "かみ"), ("あみ", "じゅう"), ("ほし", "ねずみたち")]
    check("A41", "日本語の逆さ読みでは成立しない",
          all(src[::-1] != dst for src, dst in kana_pairs), str(kana_pairs))
    it = BY_NO["A41"]
    lines = [f"{src} → {dst}" for src, _, dst, _ in pairs[:3]] + ["流れ → ?"]
    check("A41", "提示4行と順序", all(line in it["illustration_scene"] for line in lines)
          and [it["illustration_scene"].index(line) for line in lines]
          == sorted(it["illustration_scene"].index(line) for line in lines), str(lines))
    check("A41", "問題文に語の一覧なし", all(src not in it["question"] for src, _, _, _ in pairs), it["question"])
    check("A41", "答えと解説の整合", it["answer"].startswith("オオカミ")
          and all(en in it["explanation"] for _, a, _, b in pairs for en in (a, b)), it["answer"])
    check("A41", "情景指示に答え・英訳を含めない",
          all(word not in it["illustration_scene"] for word in ("オオカミ", "狼", "wolf", "flow", "dog")),
          "文字の対応だけを提示。完成画像の字形・答えバレは別途目視検品")

# ---------------------------------------------------------------
# A43 9点の一筆書き。左上=(0,0)、右・下を正とする。
# 解説の経路と回転・反転別解が全9点の中心を通り、線分を重複しないか検証。
# ---------------------------------------------------------------
if "A43" in BY_NO:
    dots = {(x, y) for x in range(3) for y in range(3)}
    route = [(0, 0), (3, 0), (0, 3), (0, 0), (2, 2)]

    def on_segment(point, start, end):
        """整数の外積と範囲から点が線分上にあるか判定する。"""
        x, y = point
        ax, ay = start
        bx, by = end
        return ((x-ax)*(by-ay) == (y-ay)*(bx-ax)
                and min(ax, bx) <= x <= max(ax, bx)
                and min(ay, by) <= y <= max(ay, by))

    segments = list(zip(route, route[1:]))
    hits = [{pt for pt in dots if on_segment(pt, a, b)} for a, b in segments]
    check("A43", "4線分で全9点の中心を通る",
          len(segments) == 4 and set.union(*hits) == dots, str(hits))
    # 各線分の方向が互いに平行でなければ、同一直線のなぞりはない。
    directions = [(b[0]-a[0], b[1]-a[1]) for a, b in segments]
    check("A43", "同じ線をなぞらない",
          all(u[0]*v[1] != u[1]*v[0] for i, u in enumerate(directions) for v in directions[i+1:]),
          str(directions))
    check("A43", "連続経路で点の並びの外へ出る",
          all(a != b for a, b in segments) and any(x > 2 or y > 2 for x, y in route), str(route))
    variants = []
    for reflect in (False, True):
        for turns in range(4):
            transformed = []
            for x, y in route:
                if reflect:
                    x = 2-x
                for _ in range(turns):
                    x, y = 2-y, x
                transformed.append((x, y))
            variants.append(transformed)
    check("A43", "回転・反転の8経路も正解",
          all({pt for a, b in zip(path, path[1:]) for pt in dots if on_segment(pt, a, b)} == dots
              for path in variants), f"{len(variants)}経路で全9点を通過(一意解とはしない)")
    it = BY_NO["A43"]
    # キャプションの番号付き配置図から座標を復元し、記載経路を検証する。
    diagram_lines = it["explanation"].splitlines()
    labels = {}
    for y, line in enumerate(diagram_lines[:4]):
        for x, token in enumerate(line.split()):
            labels[token[1:] if token.startswith("●") else token] = (x, y)
    expected_dots = {str(3*y+x+1): (x, y) for y in range(3) for x in range(3)}
    check("A43", "解説図の番号と折り返し位置",
          labels == {**expected_dots, "A": (3, 0), "B": (0, 3)}
          and all(f"●{n}" in it["explanation"] for n in range(1, 10)), str(labels))
    caption_path = diagram_lines[4].split("と一筆書き。")[0].split("→")
    check("A43", "解説図の経路は検証済み4線分と一致",
          [labels.get(label) for label in caption_path] == route
          and "点の間隔1つ分外" in it["explanation"], str(caption_path))
    check("A43", "全体を一続きに描く条件を先頭で明示",
          it["question"].startswith("ペンを一度も離さず、一筆書きで")
          and all(word in it["question"] for word in ("中心", "つながった4本の直線", "同じ線をなぞらず")), it["question"])
    check("A43", "図の指定は9点と余白、解答線は描かない",
          all(word in it["illustration_scene"] for word in ("縦3個・横3個", "縦横同じ間隔", "余白", "結ぶ線・矢印・枠線", "描かない")),
          "完成画像の個数・等間隔・余白・解答線の混入は目視検品が必要")

# ---------------------------------------------------------------
# A46 10個の磁石の三角形反転。xは横間隔の半分、yは段間隔を単位とする。
# 4段の等間隔配置を上下反転し、平行移動させた全候補の重なりを比較する。
# ---------------------------------------------------------------
if "A46" in BY_NO:
    original = {}
    number = 1
    for y in range(4):
        for x in range(-y, y + 1, 2):
            original[number] = (x, y)
            number += 1
    original_points = set(original.values())
    inverted = {(-x, -y) for x, y in original_points}
    # 3個のみ移動なら7個以上の一致が必要。1個でも一致する平行移動は
    # 元の点と反転した点の差で必ず列挙できるため、探索範囲の恣意的な制限はない。
    shifts = {(x-a, y-b) for x, y in original_points for a, b in inverted}
    candidates = {(dx, dy): {(x+dx, y+dy) for x, y in inverted} for dx, dy in shifts}
    best_overlap = max(len(original_points & pts) for pts in candidates.values())
    solutions = {shift: pts for shift, pts in candidates.items() if len(original_points & pts) == 7}
    check("A46", "最大7個を残せるため必要な移動は3個",
          best_overlap == 7, f"平行移動{len(shifts)}候補・最大共通点{best_overlap}個")
    check("A46", "3個で逆向きになる完成位置",
          set(solutions) == {(0, 4)}, f"解となる平行移動: {sorted(solutions)}")
    it = BY_NO["A46"]
    # キャプションの全角字下げと丸数字から完成図の座標を復元する。
    numerals = "①②③④⑤⑥⑦⑧⑨⑩"
    rows = it["explanation"].splitlines()[1:5]
    final = {}
    for y, row in enumerate(rows, start=1):
        indent = len(row) - len(row.lstrip("　"))
        for column, ch in enumerate(row.lstrip("　").split()):
            final[numerals.index(ch)+1] = (-3 + indent + 2*column, y)
    moved = {n for n in original if final.get(n) != original[n]}
    check("A46", "番号図は10個を重複なく使う下向き正三角形",
          set(final) == set(original) and len(set(final.values())) == 10
          and set(final.values()) == candidates[(0, 4)], str(final))
    check("A46", "動かすのは①⑦⑩だけ", moved == {1, 7, 10}, str(sorted(moved)))
    check("A46", "答えの移動先と図が一致",
          final[1] == (0, 4) and final[7] == (-3, 1) and final[10] == (3, 1)
          and it["answer"] == "①を一番下へ、⑦と⑩を②③の両外側へ", it["answer"])
    check("A46", "問題は数値計算でなく位置の変更を問う",
          all(t in it["question"] for t in ("3個だけ動かし", "10個全部", "同じ大きさ", "下向きの正三角形", "重ねたり", "黒板を回したり")), it["question"])
    check("A46", "提示図の番号と初期配置を指定",
          all(f"「{n}」" in it["illustration_scene"] for n in range(1, 11))
          and "上から1・2・3・4個" in it["illustration_scene"]
          and "完成形・他の文字・人物は描かない" in it["illustration_scene"],
          "完成画像の10個・字形・等間隔・初期配置は目視検品")

# ---------------------------------------------------------------
# A44 指の頭文字: 親指〜小指の読みの頭文字が「お ひ な く こ」になり、□(3 番目)が「な」であること
# ---------------------------------------------------------------
if "A44" in BY_NO:
    fingers = ["おやゆび", "ひとさしゆび", "なかゆび", "くすりゆび", "こゆび"]
    initials = "".join(f[0] for f in fingers)
    check("A44", "頭文字の並び", initials == "おひなくこ", f"{fingers} → {initials}")
    check("A44", "□ は 3 番目 = な", initials[2] == "な" and BY_NO["A44"]["answer"].startswith("な"), BY_NO["A44"]["answer"])
    check("A44", "情景文のカード 5 枚", all(f"「{c}」" in BY_NO["A44"]["illustration_scene"] for c in "おひ?くこ"), "お・ひ・?・く・こ を明示")
    check("A44", "5 文字は問題文に書かない(カードで提示)", "お、ひ" not in BY_NO["A44"]["question"] and "□" not in BY_NO["A44"]["question"], "問題文に文字列なし・情景文にカードあり")

# ---------------------------------------------------------------
# A45 母音送り: 提示 3 組 + 答えのすべてが「読みの各文字の母音を 1 段送った語」であること、
#      および単純な変換(逆順・循環並べ替え・濁点)では説明できないことを確認
# ---------------------------------------------------------------
if "A45" in BY_NO:
    ROWS = ["あいうえお", "かきくけこ", "さしすせそ", "たちつてと", "なにぬねの",
            "はひふへほ", "まみむめも", "らりるれろ"]
    POS = {ch: (r, i) for r, row in enumerate(ROWS) for i, ch in enumerate(row)}

    def shift_vowel(reading: str) -> str:
        """各文字の母音を 1 段送る(あ→い→う→え→お→あ)。"""
        out = []
        for ch in reading:
            r, i = POS[ch]
            out.append(ROWS[r][(i + 1) % 5])
        return "".join(out)

    pairs = [("かき", "きく", "柿→菊"), ("あめ", "いも", "雨→芋"), ("かに", "きぬ", "蟹→絹"), ("うま", "えみ", "馬→笑み")]
    for src, dst, label in pairs:
        check("A45", f"母音送りで対応 {label}", shift_vowel(src) == dst, f"{src} → {shift_vowel(src)}")
    # 他の単純変換では説明できないこと(逆順・循環並べ替え)
    other = [(src, dst) for src, dst, _ in pairs if src[::-1] == dst or src[1:] + src[0] == dst]
    check("A45", "逆順・循環では説明できない", not other, f"逆順/循環で一致する組: {other}")
    check("A45", "answer は えみ", BY_NO["A45"]["answer"].startswith("えみ"), BY_NO["A45"]["answer"])
    check("A45", "3 組は問題文に書かない(黒板で提示)",
          "柿" not in BY_NO["A45"]["question"] and "柿 → 菊" in BY_NO["A45"]["illustration_scene"],
          "問題文に組なし・情景文に 4 行あり")

# ---------------------------------------------------------------
# C48 ケーキを 3 回で 8 等分: 中心を通る直交 2 平面 + 高さ半分の水平面で 8 片の体積が等しいこと(モンテカルロ)
# ---------------------------------------------------------------
if "C48" in BY_NO:
    rng = random.Random(0)
    counts = [0] * 8
    n = 200_000
    for _ in range(n):
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y > 1:
            continue
        z = rng.uniform(0, 1)
        idx = (x > 0) + 2 * (y > 0) + 4 * (z > 0.5)
        counts[idx] += 1
    mean = sum(counts) / 8
    spread = max(abs(c - mean) / mean for c in counts)
    check("C48", "8 片の体積が等しい", spread < 0.03, f"各片の比率のばらつき {spread:.3%}(サンプル {sum(counts)})")

# ---------------------------------------------------------------
# 機械検証できない問題(想定解の妥当性は人間レビューが砦)
# ---------------------------------------------------------------
manual = [no for no in ("C42", "C43", "C44", "C45", "C46", "C47") if no in BY_NO]
print(f"-- 機械検証対象外(人間レビューが砦): {', '.join(manual)}")
print("   C45 は「同じ喫水線 = 同じ排水量 = 同じ重さ」(アルキメデスの原理)で成立。C42/C43/C44/C46/C47 は手順・一言の妥当性を人間が判断")

if failures:
    print(f"\nNG: {len(failures)} 件")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("\nOK: 機械検証できる問題はすべて答えと一致")
