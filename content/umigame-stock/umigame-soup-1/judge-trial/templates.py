"""パターン 2 と安全な後処理で使う、状態を持たない定型文。"""

from __future__ import annotations

import hashlib


TEMPLATES: dict[str, tuple[str, ...] | None] = {
    "q_yesno": (
        "ふむ、次の質問をどうぞ。",
        "一歩ずつ確かめましょう。",
        "手掛かりを追ってみましょう。",
        "続きの推理もお待ちしています。",
        "捜査はまだ続きます。",
        "次の一手を聞かせてください。",
    ),
    "q_multi": ("質問は一つずつお願いします。", "まず一つ、順番にどうぞ。", "一問ずつ捜査しましょう。"),
    "q_open": ("はいかいいえで聞いてみてください。", "答えを絞れる形でどうぞ。", "一言で答えられる質問にしてみましょう。"),
    "guess_correct": ("正解です！", "正解です！見事な推理です。", "正解です！お見事です。"),
    "guess_close": ("惜しい！もう少し考えてみてください。", "惜しい！推理を続けてみましょう。", "惜しい！あと一歩です。"),
    "guess_wrong": ("残念、違います。", "残念ながら違います。", "その推理ではありません。"),
    "ask_hint": ("質問を重ねて絞ってみましょう。", "はいかいいえで探ってみてください。", "質問で手掛かりを集めましょう。"),
    "ask_spoiler": ("誰かが当てるまで秘密です。", "真相は名探偵の推理にお任せです。", "答えは当てた方のお楽しみです。"),
    "ask_howto": ("はいかいいえで答えられる質問をどうぞ。", "質問をコメントすると探偵が答えます。", "質問を重ねて真相に近づきましょう。"),
    "impression": ("感想をありがとうございます。", "楽しんでもらえて何よりです。", "読んでくれてありがとうございます。"),
    "greeting": ("ご挨拶ありがとうございます。", "こんにちは、捜査を始めましょう。", "声をかけてくれてありがとう。"),
    "cheer": ("応援ありがとうございます。", "心強い応援に感謝します。", "応援を受け取りました。"),
    "chat": ("なるほど、そうなんですね。", "お話しありがとうございます。", "ふむ、興味深いですね。"),
    "request": ("リクエストありがとうございます。", "ご希望を聞かせてくれてありがとう。", "次の題材の参考にします。"),
    "complaint": ("ご指摘ありがとうございます。確認します。", "お知らせありがとうございます。確認します。", "ご意見ありがとうございます。確認します。"),
    "mention": ("一緒に楽しんでください。", "お友達もようこそ。", "お二人で推理をどうぞ。"),
    "emoji_only": ("反応ありがとうございます。", "受け取りました。", "ふむ、承知しました。"),
    "troll": ("コメントを受け取りました。", "捜査資料として記録しました。", "次の手掛かりをお待ちしています。"),
    "abuse": ("この場では穏やかなやり取りをお願いします。", "攻撃的な言葉は控えてください。", "安心して楽しめる言葉でお願いします。"),
    "spam": None,
    "personal_info": None,
    "foreign": ("日本語で質問してね。", "日本語でコメントしてください。", "日本語の質問をお待ちしています。"),
}

NO_REPLY_KINDS = frozenset(("spam", "personal_info"))
CORRECT_PREFIX = "正解です！"
YESNO_OPENERS = {
    "yes": "はい。",
    "no": "いいえ。",
    "irrelevant": "関係ありません。",
    "unknown": "それは問題の答えに関わりません。",
}


def pick(kind: str, comment_id: str) -> str | None:
    """コメント ID の SHA-1 で定型文を選ぶ。"""
    options = TEMPLATES.get(kind)
    if options is None:
        return None
    digest = hashlib.sha1(str(comment_id).encode("utf-8")).digest()
    return options[int.from_bytes(digest[:8], "big") % len(options)]


def yesno_reply(answer: str, comment_id: str) -> str:
    """判定の冒頭語と 20 字以内の真相に触れない一言を組み立てる。"""
    opener = YESNO_OPENERS.get(answer, YESNO_OPENERS["unknown"])
    phrase = pick("q_yesno", comment_id) or "次の質問をどうぞ。"
    return opener + phrase


def correct_reply(reveal_text: str) -> str:
    """正解宣言に試走フィクスチャの開示文を付ける。"""
    return CORRECT_PREFIX + reveal_text
