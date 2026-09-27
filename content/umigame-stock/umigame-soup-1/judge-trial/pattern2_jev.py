"""Jev API を段階利用し、定型文で返信するパターン 2。"""

from __future__ import annotations

import json
import math
import os
import re
import time
import unicodedata
from urllib import error, request

from judge_contract import JudgeResult, KINDS, Problem
import templates


JEV_URL = "https://api.typesafe.ai/v1/systemone"
T_POINT = 0.5
T_CLOSE = 0.35  # 惜しい判定だけに使う（正解側の T_POINT は下げない。試行 4）
CORRECT_FRACTION = 0.75  # 要点のこの割合以上が T_POINT 以上なら正解（試行 5・ユーザー承認）
T_RECHECK = 0.5  # A2 が q_open のとき、問題文つきで答えられる質問か確かめ直す（試行 5・ユーザー指示）
T_QUALITY = 0.2
T_ANSWER = 0.55
MAX_RETRIES = 3
_URL_RE = re.compile(r"(?:https?://|www\.)|\b[\w-]+(?:\.[\w-]+)+\b", re.IGNORECASE)
_JAPANESE_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
_LATIN_RE = re.compile(r"[A-Za-z]")
_LATIN_WORD_RE = re.compile(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b")


KIND_CRITERIA = {
    "q_yesno": "One clear question that can be answered yes or no.",
    "q_multi": "The comment contains two or more questions.",
    "q_open": "An open question, or an unclear question that cannot be answered uniquely with yes or no.",
    "guess": "A claim or hypothesis about the hidden truth, including a question-form guess.",
    "ask_hint": "The commenter asks for a hint.",
    "ask_spoiler": "The commenter asks for the answer or a spoiler.",
    "ask_howto": "The commenter asks how to play or asks whether this account is a bot.",
    "impression": "A reaction or impression about the puzzle.",
    "greeting": "A greeting.",
    "cheer": "Words of support or encouragement.",
    "chat": "Casual conversation unrelated to solving the puzzle.",
    "request": "A request for a future puzzle or topic.",
    "complaint": "A criticism, correction, or complaint about the puzzle.",
    "mention": "A tag or mention inviting a friend to solve the puzzle.",
    "troll": "Meaningless text or repeated disruptive comments.",
    "abuse": "Abusive, hateful, discriminatory, sexual, or attacking content.",
    "spam": "Advertising, a link, or a follow-for-follow promotion.",
    "personal_info": "Personal identifying information such as a phone number, address, or full name.",
    "foreign": "A comment written in a language other than Japanese.",
}
_A_KEYS = (
    "q_yesno",
    "q_multi",
    "q_open",
    "guess",
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
    "troll",
    "abuse",
    "spam",
    "personal_info",
    "foreign",
)
_A_CRITERIA = {key: KIND_CRITERIA[key] for key in _A_KEYS}

# 段 A1（大分類）: 問題文は渡さず、「水平思考クイズへの SNS コメント」という説明とコメントだけで 6 択にする。
# 具体例は評価データ（data/）の文面をそのまま使わない。
A_CONTEXT = (
    "A lateral-thinking quiz (Umigame no Soup) was posted on Instagram. Players ask yes/no questions "
    "or post guesses about the hidden story in the comments. This is one comment from that post."
)
MAJOR_CRITERIA = {
    "question": (
        "Question about the puzzle story: a yes/no question, several questions in one comment, or an open "
        "question (why / who / what / how) or a vague question. "
        "Examples: 「その人は男の家族？」「場所は海の近く？」「なぜ男は笑ったの？」「時間は夜？季節は冬？」"
    ),
    "guess": (
        "Guess: the commenter states their own explanation of the hidden story, even when it ends with ？ "
        "(〜ってこと？ / 〜でしょ？). Correct, partly correct and wrong guesses all belong here. "
        "Examples: 「男は実は医者だったんだ」「犯人は弟ってこと？」「写真に写ってたのは昔の自分でしょ」"
    ),
    "request": (
        "Request to the account instead of a question about the story: asking for a hint, for the answer or "
        "a spoiler, or how to play / whether replies are automatic. "
        "Examples: 「ヒントほしいです」「真相はよ」「どうやって参加するの？」「返事してるのAI？」"
    ),
    "reaction": (
        "Reaction: impression, greeting, support, casual chat unrelated to the story, a request for future "
        "puzzles, criticism of the puzzle itself (including calling it boring or bad), tagging a friend. "
        "Examples: 「今日のは難しかった」「おはよう」「毎日楽しみ」「雨やばい」「次は学校ものがいい」"
        "「今回のはつまらない」「@friend 解いてみて」"
    ),
    "inappropriate": (
        "Inappropriate: meaningless strings or spam-like repetition, insults or attacks against a person "
        "(the author or other users), discriminatory or sexual content, advertising / links / follow-for-follow, "
        "personal information such as phone numbers, addresses or real names. "
        "Examples: 「hjkl;;;;」「管理人は性格悪い」「稼げる方法教えます→プロフ」「住所は〇〇市〇〇町です」"
    ),
    "other": "A comment not written in Japanese. Examples: 'nice puzzle', '太难了', '어려워요'",
}
SUB_CRITERIA = {
    "question": {
        "q_yesno": "Exactly one question that can be answered yes or no. Examples: 「その人は男の家族？」「夜の出来事？」",
        "q_multi": "Two or more questions in one comment. Examples: 「場所は家？時間は朝？」「誰が来たの？何を持ってたの？」",
        "q_open": (
            "An open question (why / who / what / how) that cannot be answered with yes or no, or a question whose "
            "subject is unclear (それ / あれ / 彼 / あの人). Examples: 「なぜ笑ったの？」「あれはいつのこと？」"
        ),
    },
    "request": {
        "ask_hint": "Asks for a hint. Examples: 「ヒントほしいです」「手がかりちょうだい」",
        "ask_spoiler": "Asks for the answer, the truth or an explanation. Examples: 「真相はよ」「結局どういう話？」",
        "ask_howto": "Asks how to play, what to comment, or whether replies are automatic / a bot. Examples: 「どうやって参加するの？」「返事してるのAI？」",
    },
    "reaction": {
        "impression": "Impression of the puzzle (positive or mixed). Examples: 「今日のは難しかった」「ゾクッとした」",
        "greeting": "A greeting. Examples: 「おはよう」「はじめまして」",
        "cheer": "Support or encouragement for the account. Examples: 「毎日楽しみ」「これからも頑張って」",
        "chat": "Casual talk unrelated to the puzzle. Examples: 「雨やばい」「昼休みに見てる」",
        "request": "A request for future puzzles or themes. Examples: 「次は学校ものがいい」「ホラー回希望」",
        "complaint": (
            "Criticism of the puzzle itself, including disparaging it (boring, no sense, stupid puzzle), "
            "pointing out a contradiction or saying it is too hard. Examples: 「今回のはつまらない」「設定に無理がある」"
        ),
        "mention": "Tags a friend with @ to invite them. Examples: 「@friend 解いてみて」「@aki これ好きそう」",
    },
    "inappropriate": {
        "troll": "Meaningless strings or repeated characters. Examples: 「hjkl;;;;」「ほほほほほほ」",
        "abuse": (
            "Insults or attacks against a person (the author or other users), discriminatory or sexual content. "
            "Criticism of the puzzle itself is not abuse. Examples: 「管理人は性格悪い」「こんなの作るやつ気持ち悪い」"
        ),
        "spam": "Advertising, links, follow-for-follow or money-making invitations. Examples: 「稼げる方法教えます→プロフ」",
        "personal_info": "Contains personal information such as a phone number, address or real name. Examples: 「住所は〇〇市〇〇町です」",
    },
}


class JevError(RuntimeError):
    """Jev API request or response error."""


def _rule_kind(text: str) -> str | None:
    """仕様段 0 の URL・記号・英語コメント判定。"""
    if _URL_RE.search(text):
        return "spam"
    nonspace = [char for char in text if not char.isspace()]
    if nonspace and all(
        unicodedata.category(char)[0] in {"P", "S", "C"}
        or char in {"\ufe0e", "\ufe0f"}
        for char in nonspace
    ):
        return "emoji_only"
    # 英字だけのコメントは、空白で区切られた英単語が 2 つ以上あるときだけ外国語とする（試行 5）。
    # 「QWERTYZZZ」のような 1 語の羅列は段 A1 に任せる（試行 4 で英字の規則を丸ごと外したら英文が反応などに流れた）。
    if not _JAPANESE_RE.search(text) and len(_LATIN_WORD_RE.findall(text)) >= 2:
        return "foreign"
    return None


def _jev_request(api_key: str, state: dict, questions: dict[str, dict]) -> dict:
    """SystemOne を呼び、429/529 のみ指数バックオフで再試行する。"""
    payload = {"model": "jev-latest", "state": state, "questions": questions}
    req = request.Request(
        JEV_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(MAX_RETRIES + 1):
        try:
            with request.urlopen(req, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))
            if not isinstance(result, dict) or not isinstance(result.get("answers"), dict):
                raise JevError("応答に answers オブジェクトがありません")
            return result
        except error.HTTPError as exc:
            if exc.code in {429, 529} and attempt < MAX_RETRIES:
                time.sleep(2**attempt)
                continue
            detail = exc.read().decode("utf-8", "replace")[:300]
            raise JevError(f"HTTP {exc.code}: {detail}") from exc
        except (json.JSONDecodeError, error.URLError) as exc:
            raise JevError(f"Jev API 応答を読めません: {exc}") from exc
    raise JevError("Jev API の再試行回数を超えました")


def _probability_map(answer: dict) -> dict:
    probabilities = answer.get("probabilities", {})
    if isinstance(probabilities, dict):
        return probabilities
    return {}


def _noul_true(answer: dict) -> float:
    value = answer.get("noul")
    if isinstance(value, dict):
        value = value.get("true")
    if value is None:
        value = _probability_map(answer).get("true")
    return float(value)


def _choice(answer: dict, keys: tuple[str, ...]) -> str:
    choice = answer.get("choice")
    if isinstance(choice, dict):
        choice = choice.get("key", choice.get("choice"))
    if isinstance(choice, str) and choice in keys:
        return choice
    probabilities = _probability_map(answer)
    candidates = [(key, float(probabilities[key])) for key in keys if key in probabilities]
    if candidates:
        return max(candidates, key=lambda entry: entry[1])[0]
    raise JevError(f"有効な choice がありません: {choice!r}")


def _record_call(api_key: str, state: dict, questions: dict[str, dict], debug: dict) -> dict:
    started = time.monotonic()
    result = _jev_request(api_key, state, questions)
    elapsed = time.monotonic() - started
    usage = result.get("usage", {})
    input_tokens = result.get("input_tokens", usage.get("input_tokens", 0))
    debug["input_tokens"] += int(input_tokens or 0)
    debug["latency_s"] = round(debug["latency_s"] + elapsed, 6)
    debug["calls"] += 1
    return result["answers"]


def _error_result(exc: Exception, debug: dict) -> JudgeResult:
    return JudgeResult(kind="error", answer=None, reply=None, method="p2", debug={**debug, "error": str(exc)})


def judge(
    comment_id: str,
    text: str,
    problem: Problem,
    *,
    api_key: str,
    t_point: float = T_POINT,
    t_close: float = T_CLOSE,
    correct_fraction: float = CORRECT_FRACTION,
    t_recheck: float = T_RECHECK,
    t_quality: float = T_QUALITY,
    t_answer: float = T_ANSWER,
) -> JudgeResult:
    """段階判定を行い、全ての返信をコード定型文から作る。"""
    debug = {"input_tokens": 0, "latency_s": 0.0, "calls": 0, "probabilities": {}}
    rule_kind = _rule_kind(text)
    if rule_kind is not None:
        reply = templates.pick(rule_kind, comment_id)
        return JudgeResult(rule_kind, None, reply, "p2", debug)

    try:
        state_a = {"context": A_CONTEXT, "comment": text}
        a1_answers = _record_call(
            api_key,
            state_a,
            {
                "major": {
                    "type": "choice",
                    "instructions": "Classify the Japanese comment into one broad category by its main intent.",
                    "criteria": MAJOR_CRITERIA,
                }
            },
            debug,
        )
        major = _choice(a1_answers["major"], tuple(MAJOR_CRITERIA))
        debug["probabilities"]["A1"] = _probability_map(a1_answers["major"])
        if major == "guess":
            a_kind = "guess"
        elif major == "other":
            a_kind = "foreign"
        else:
            sub = SUB_CRITERIA[major]
            a2_answers = _record_call(
                api_key,
                state_a,
                {
                    "kind": {
                        "type": "choice",
                        "instructions": "Classify the Japanese comment into the most fitting detailed type.",
                        "criteria": sub,
                    }
                },
                debug,
            )
            a_kind = _choice(a2_answers["kind"], tuple(sub))
            debug["probabilities"]["A2"] = _probability_map(a2_answers["kind"])
            if a_kind == "q_open":
                # A2 は問題文を見ないので、主語が消去法で決まる質問まで q_open にしうる。問題文を渡して確かめ直す。
                recheck_answers = _record_call(
                    api_key,
                    {"problem_text": problem.problem_text, "comment": text},
                    {
                        "recheck": {
                            "type": "noul",
                            "instructions": (
                                "Given the puzzle text, decide whether the comment can be read as exactly one question "
                                "that can be answered with yes or no. Every pronoun or demonstrative (それ / あれ / 彼 / "
                                "彼女 / あの人 / その子) must refer to exactly one person or thing in the puzzle text, "
                                "possibly by elimination. Why / who / what / how questions cannot be answered with yes or no."
                            ),
                            "criteria": {
                                "true": "It is one yes-or-no question whose subject and target are determined by the puzzle text.",
                                "false": "It is an open question, or a pronoun cannot be resolved from the puzzle text.",
                            },
                        }
                    },
                    debug,
                )
                recheck = _noul_true(recheck_answers["recheck"])
                debug["probabilities"]["A3"] = recheck
                if recheck >= t_recheck:
                    a_kind = "q_yesno"
        debug["major"] = major
        kind: str
        answer: str | None = None
        if a_kind in {"guess", "q_yesno"}:
            # 要点ごとの noul を 1 リクエストにまとめる（試行 5。試行 4 は要点ごとに 1 回ずつ呼んで遅くなった）
            point_questions = {
                f"point_{index}": {
                    "type": "noul",
                    "instructions": (
                        "Estimate whether the commenter explicitly states this truth point. "
                        f"The truth point is: {point!r}. Use true only when its meaning is clearly present."
                    ),
                    "criteria": {
                        "true": "The comment clearly states this truth point.",
                        "false": "The comment does not clearly state this truth point.",
                    },
                }
                for index, point in enumerate(problem.truth_points)
            }
            point_answers = _record_call(api_key, {"comment": text}, point_questions, debug)
            point_probs = {point_id: _noul_true(point_answers[point_id]) for point_id in point_questions}
            debug["probabilities"]["B"] = point_probs
            hits = sum(value >= t_point for value in point_probs.values())
            all_points = bool(point_probs) and hits >= math.ceil(correct_fraction * len(point_probs))
            some_points = any(value >= t_close for value in point_probs.values())
            if all_points:
                kind = "guess_correct"
            elif a_kind == "guess":
                kind = "guess_close" if some_points else "guess_wrong"
            else:
                quality_answers = _record_call(
                    api_key,
                    {"comment": text, "problem_text": problem.problem_text},
                    {
                        "quality": {
                            "type": "noul",
                            "instructions": (
                                "Estimate whether this question is specific to the puzzle and can be "
                                "answered uniquely with yes or no, with a clear subject and target. "
                                "If a pronoun or demonstrative (それ / あれ / 彼 / 彼女 / あの人 / その子) could refer to "
                                "more than one person or thing in the puzzle text, or refers to nothing in it, "
                                "the question is not uniquely answerable."
                            ),
                            "criteria": {
                                "true": "It is a clear, relevant, uniquely answerable yes-or-no question.",
                                "false": "It is open-ended, vague, has an unclear pronoun, or is not uniquely answerable yes or no.",
                            },
                        }
                    },
                    debug,
                )
                quality = _noul_true(quality_answers["quality"])
                debug["probabilities"]["C"] = quality
                if quality < t_quality:
                    kind = "q_open"
                else:
                    kind = "q_yesno"
                    d_answers = _record_call(
                        api_key,
                        {
                            "problem_text": problem.problem_text,
                            "truth": problem.truth,
                            "fact_sheet": problem.fact_sheet,
                            "question": text,
                        },
                        {
                            "answer": {
                                "type": "choice",
                                "instructions": (
                                    "Answer the question only from the supplied facts. Do not infer missing facts."
                                ),
                                "criteria": {
                                    "yes": "The supplied facts support answering yes.",
                                    "no": "The supplied facts support answering no.",
                                    "irrelevant": "The question is unrelated to the puzzle facts.",
                                },
                            }
                        },
                        debug,
                    )
                    d_answer = d_answers["answer"]
                    d_probs = _probability_map(d_answer)
                    debug["probabilities"]["D"] = d_probs
                    if d_probs:
                        best_key, best_probability = max(
                            ((key, float(d_probs.get(key, 0))) for key in ("yes", "no", "irrelevant")),
                            key=lambda entry: entry[1],
                        )
                    else:
                        best_key, best_probability = _choice(d_answer, ("yes", "no", "irrelevant")), 0.0
                    answer = best_key if best_probability >= t_answer else "unknown"
        else:
            kind = a_kind

        if kind in templates.NO_REPLY_KINDS:
            reply = None
        elif kind in {"troll", "abuse"}:
            reply = templates.pick(kind, comment_id)
        elif kind == "guess_correct":
            reply = templates.correct_reply(problem.reveal_text)
        elif kind == "q_yesno":
            reply = templates.yesno_reply(answer or "unknown", comment_id)
        else:
            reply = templates.pick(kind, comment_id)
        return JudgeResult(kind, answer, reply, "p2", debug)
    except Exception as exc:  # noqa: BLE001 - API/応答異常を試走結果として残す
        return _error_result(exc, debug)
