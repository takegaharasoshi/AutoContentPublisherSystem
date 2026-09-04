"""umigame-soup-1 ストック整備の共通定数・組み立てヘルパー。

セット固定の既定文（ルール帯・キャラクターの台詞・ハッシュタグ）と、イラストプロンプト・
キャプションの組み立て規則をここに置き、各バッチの ``stock_items.py`` / ``validate.py`` /
``probe_test.py`` / ``generate.py`` が共有する。仕様の正は
``docs/app/sets/umigame-soup-1.html`` セクション 4（素材 14 項目）・5.2（イラスト）・6（キャプション）。
"""

from __future__ import annotations

from pathlib import Path

SET_CODE = "umigame-soup-1"
SET_DIR = Path(__file__).resolve().parent.parent
MASTER_PROMPT_PATH = SET_DIR / "master_prompt.txt"

# ---------- セット固定の既定文（素材項目 #6 / #7 rule / #9 / #10） ----------
RULE_TEXT_DEFAULT = "「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します"
NARRATION_RULE_DEFAULT = "はい、いいえ、関係ない、で答えられる質問をコメントしてね。全部返事するよ。"
CHARACTER_LINES_DEFAULT = {
    "master": {"intro": "質問してみて！", "outro": "何度でも答えるよ。コメントで質問！"},
    "jr": {"outro": "面白かったら、いいね、フォローよろしくね！"},
}

# ---------- イラスト作成用プロンプト（5.2: 画風固定行 + 情景 + 禁止事項の 3 部構成） ----------
# 画風固定行は全問共通の定数。validate.py が illustration_prompt に含まれることを検査する。
STYLE_LINE = (
    "A stylized 1990s Japanese OVA anime background painting (hand-painted cel-era background art, "
    "poster-color textures, clean shapes, thick brush-like outlines on key objects). Mid-key lighting: "
    "moonlight, lamps or candlelight keep the whole scene clearly visible, NOT dark."
)
PROHIBITION_LINE = (
    "Vertical 9:16 composition (1024x1536). No text, no letters, no numbers, no logos, no signs. "
    "Depict only the scene described in the problem statement; do not depict any clue to the story's "
    "hidden truth. People: only the persons who appear in the problem, plus at most one distant "
    "silhouette. Keep the upper 55% of the image calm and simple (sky, wall, ceiling, window) so that "
    "text cards can be overlaid there."
)


def illustration_prompt(scene: str) -> str:
    """画風固定行・情景・禁止事項の 3 部構成でイラストプロンプトを組み立てる。

    Args:
        scene: 問題文にある情景だけを英語で描写した文（真相の手がかりを含めない）。

    Returns:
        imagegen に渡す完成プロンプト。
    """
    return f"{STYLE_LINE}\n\nScene: {scene.strip()}\n\n{PROHIBITION_LINE}"


# ---------- キャプション（6: 問題文の再掲 + 遊び方 + ハッシュタグ。「第 N 問」は書かない） ----------
CAPTION_HEADER = "【探偵カメロックのウミガメのスープ】"
CAPTION_PLAY = (
    "「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。"
    "出題者の探偵カメロックが全部返事します。正解が出るまで何度でもどうぞ。"
)
HASHTAGS = "#ウミガメのスープ #水平思考 #推理クイズ #なぞなぞ #謎解き #クイズ #AIart"


def caption(problem_text: str, lead: str = "") -> str:
    """キャプション本文を組み立てる。

    Args:
        problem_text: 問題文（版面と同じ全文）。
        lead: 問題固有の一言（任意。問題文の前に 1 行置く）。

    Returns:
        本文 + ハッシュタグの完成キャプション（#AIart 含む）。
    """
    parts = [CAPTION_HEADER]
    if lead:
        parts.append(lead)
    parts += ["", problem_text, "", CAPTION_PLAY, "", HASHTAGS]
    return "\n".join(parts)


# ---------- 出題者プロンプト（master_prompt.txt が正。probe_test と 21-7 の INSERT が共有） ----------
def render_master_prompt(problem_text: str, truth: str, fact_sheet: list[str]) -> str:
    """master_prompt.txt のプレースホルダを 1 問の内容で展開する。

    Args:
        problem_text: 問題文。
        truth: 真相。
        fact_sheet: 確定事実シート（文字列の配列）。

    Returns:
        AI 出題者に渡す system prompt 全文。
    """
    template = MASTER_PROMPT_PATH.read_text(encoding="utf-8")
    facts = "\n".join(f"- {f}" for f in fact_sheet)
    return (
        template.replace("{problem_text}", problem_text)
        .replace("{truth}", truth)
        .replace("{fact_sheet}", facts)
    )


# ---------- 素材項目の鍵一覧（stock_items.py の 1 問が持つキー） ----------
# 管理項目（no / content_key / title / puzzle_type / difficulty）+ 素材 14 項目（rule_text /
# character_lines は既定値で埋める）。puzzle_type はレビュー・在庫の偏り確認用で DB には入れない。
REQUIRED_KEYS = (
    "no",
    "content_key",
    "title",
    "puzzle_type",
    "difficulty",
    "problem_text",
    "truth",
    "fact_sheet",
    "expected_questions",
    "hook",
    "rule_text",
    "narration",
    "play_example",
    "character_lines",
    "illustration_prompt",
    "caption",
    "source_note",
)
PUZZLE_TYPES = ("story", "misdirection")
ANSWER_HEADS = ("はい", "いいえ", "関係ない", "正解")
