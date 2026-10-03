"""試行 8b の Jev 段階判定を本番の共通契約へ移植した実装。"""

from __future__ import annotations

import json
import re
import time
import unicodedata
from urllib import error, request

from app.http_util import post_json_with_retry
from app.judge.contract import Judgement, Problem, bare_term_text


JEV_URL = "https://api.typesafe.ai/v1/systemone"
T_POINT = 0.5
T_CLOSE = 0.25  # 惜しい判定だけに使う（正解側の T_POINT は下げない。試行 4 で 0.35、試行 7b でコア基準に合わせて 0.25）
T_GUESS = 0.95  # 段 A1b で推理とする確率の下限（試行 6b。21-6d3 の全件 441 件で確かめ据え置き）
T_RECHECK = 0.6  # A2 が q_open のとき、問題文つきで答えられる質問か確かめ直す（試行 5・ユーザー指示。試行 8 で 0.5 → 0.6）
T_QUALITY = 0.2
T_ANSWER = 0.55
T_BARE_TERM = 0.5
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
    # 質問と推理は問題文なしでは見分けにくいので、A1 では 1 つにまとめ、段 A1b で問題文つきで振り分け直す（試行 6・ユーザー指示）
    "question_or_guess": (
        "About the hidden story of the puzzle: either a question to the quiz master (yes/no, several questions, "
        "why / who / what) or the commenter's own guess or explanation of what happened. "
        "Examples: 「その人は男の家族？」「なぜ男は笑ったの？」「時間は夜？季節は冬？」「男は実は医者だったんだ」"
        "「犯人は弟ってこと？」"
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
# 段 A1b（試行 6）: 問題文を渡して、質問か推理かを振り分け直す。例は評価データ（data/）の文面を使わない。
QG_CRITERIA = {
    "question": (
        "The comment asks the quiz master to confirm facts and is not itself an explanation of the puzzle. "
        "Short confirmations that check one word, one person or one action in the puzzle text are questions, "
        "even when they end with 〜ってこと？ / 〜って意味？ / 〜なの？. "
        "Examples: 「『箱』って普通の箱のこと？」「相手は同じ職場の人ってこと？」「その話は夜のことなの？」"
    ),
    "guess": (
        "The comment proposes its own answer to the puzzle: an explanation of why the strange situation happened "
        "(a cause, a hidden identity or a twist), even when it ends with ？. "
        "Examples: 「男は実は役者で、全部舞台の上の話だったってこと？」「手紙を書いたのは男の祖父で、昔から知っていたんだ」"
    ),
}
# 指示語・代名詞。A2 が ① を選んでも、これを含む質問は段 A3 で主語が決まるか確かめ直す（試行 6）
_DEMONSTRATIVE_RE = re.compile(r"それ|あれ|彼女|彼|あの人|その人|この人|その子|あの子|そいつ|あいつ")

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
    try:
        result = post_json_with_retry(
            req, retries=MAX_RETRIES, initial_backoff_s=1,
            retry_statuses={429, 529},
        )
    except error.HTTPError as exc:
        raise JevError(f"HTTP {exc.code}") from exc
    except (json.JSONDecodeError, error.URLError, ValueError) as exc:
        raise JevError(f"Jev API 応答を読めません: {exc}") from exc
    if not isinstance(result.get("answers"), dict):
        raise JevError("応答に answers オブジェクトがありません")
    return result


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
    debug["output_tokens"] += int(result.get("output_tokens", usage.get("output_tokens", 0)) or 0)
    debug["latency_s"] = round(debug["latency_s"] + elapsed, 6)
    debug["calls"] += 1
    return result["answers"]


def judge(
    comment_id: str,
    text: str,
    problem: Problem,
    *,
    api_key: str,
    t_point: float = T_POINT,
    t_close: float = T_CLOSE,
    t_recheck: float = T_RECHECK,
    t_guess: float = T_GUESS,
    t_quality: float = T_QUALITY,
    t_answer: float = T_ANSWER,
    t_bare_term: float = T_BARE_TERM,
) -> Judgement:
    """Run the trial-8b staged classifier, plus a bare-term check in stage A."""
    debug = {"model": "jev-latest", "input_tokens": 0, "output_tokens": 0,
             "latency_s": 0.0, "calls": 0, "probabilities": {}}
    rule_kind = _rule_kind(text)
    if rule_kind is not None:
        return Judgement("jev", rule_kind, reason=f"段0規則: {rule_kind}", debug=debug)

    try:
        _points_cache: dict = {}

        def core_probs() -> dict:
            """段 B（コアの要点ごとの noul）。段 A1b と正解判定で使い回すため 1 回だけ呼ぶ（試行 8）。"""
            if "B" not in _points_cache:
                # 要点ごとの noul を 1 リクエストにまとめる（試行 5。試行 4 は要点ごとに 1 回ずつ呼んで遅くなった）
                point_questions = {
                    f"point_{index}": {
                        "type": "noul",
                        "instructions": (
                            "Estimate whether the comment states the same content as this truth point, "
                            "including paraphrases or different wording with the same meaning. "
                            f"The truth point is: {point!r}."
                        ),
                        "criteria": {
                            "true": "The comment states this truth point, possibly in different words.",
                            "false": "The comment does not state this truth point.",
                        },
                    }
                    for index, point in enumerate(problem.core_points)
                }
                point_answers = _record_call(api_key, {"comment": text}, point_questions, debug)
                point_probs = {point_id: _noul_true(point_answers[point_id]) for point_id in point_questions}
                _points_cache["B"] = point_probs
                debug["probabilities"]["B"] = point_probs
            return _points_cache["B"]

        state_a = {"context": A_CONTEXT, "comment": text}
        a1_answers = _record_call(
            api_key,
            state_a,
            {
                "major": {
                    "type": "choice",
                    "instructions": "Classify the Japanese comment into one broad category by its main intent.",
                    "criteria": MAJOR_CRITERIA,
                },
                "bare_term": {
                    "type": "noul",
                    "instructions": (
                        "Is this comment only a noun or short noun phrase with no predicate "
                        "about a person or object in the puzzle? Punctuation or a question mark "
                        "does not make it a full question. A sentence with an omitted subject "
                        "but a predicate (e.g. 人形なの？ or 病気が治ったから？) is false. "
                        "Judge grammar only, regardless of whether the term matches the truth."
                    ),
                    "criteria": {
                        "true": "Only a bare noun or term, with no predicate.",
                        "false": "There is a predicate, a complete question, or another intent.",
                    },
                },
            },
            debug,
        )
        major = _choice(a1_answers["major"], tuple(MAJOR_CRITERIA))
        debug["probabilities"]["A1"] = _probability_map(a1_answers["major"])
        bare_probability = _noul_true(a1_answers["bare_term"])
        debug["probabilities"]["A_bare"] = bare_probability
        if major == "question_or_guess" and bare_probability >= t_bare_term:
            term = bare_term_text(text)
            if term:
                return Judgement(
                    "jev", "q_open", reason=f"段A語句のみ: {bare_probability:.2f}",
                    bare_term=term, debug=debug,
                )
        if major == "question_or_guess":
            qg_answers = _record_call(
                api_key,
                {"problem_text": problem.problem_text, "comment": text},
                {
                    "qg": {
                        "type": "choice",
                        "instructions": (
                            "The puzzle text is given. Decide whether the comment is a question to the quiz master "
                            "or the commenter's own explanation (guess) of the puzzle."
                        ),
                        "criteria": QG_CRITERIA,
                    }
                },
                debug,
            )
            qg_probs = _probability_map(qg_answers["qg"])
            debug["probabilities"]["A1b"] = qg_probs
            # 推理と言い切れるときだけ推理にし、迷ったら質問に倒す（質問の形の正解推理は段 B で拾える）。
            # 最大確率で選ぶと、理由を確かめる質問（〜したから？）が推理に流れた（試行 6）
            if qg_probs:
                major = "guess" if float(qg_probs.get("guess", 0)) >= t_guess else "question"
                # 推理にするのはコアの要点のどれかに少しでも触れているときだけ（試行 8・ユーザー指示）。
                # コアに全く触れない短い質問（「誰かのいたずらだった？」など）が推理の確率 0.95 を超えることがあった
                if major == "guess" and max(core_probs().values(), default=0.0) < t_close:
                    major = "question"
                    debug["guess_demoted"] = True
            else:
                major = _choice(qg_answers["qg"], tuple(QG_CRITERIA))
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
            if a_kind == "q_open" and debug.get("guess_demoted"):
                # 推理から質問に戻したが、はい / いいえの質問でもない → コアに触れない推理 = ⑥（試行 8b）
                a_kind = "guess"
            elif a_kind == "q_open" or (a_kind == "q_yesno" and _DEMONSTRATIVE_RE.search(text)):
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
                a_kind = "q_yesno" if recheck >= t_recheck else "q_open"
        debug["major"] = major
        kind: str
        answer: str | None = None
        if a_kind in {"guess", "q_yesno"}:
            point_probs = core_probs()
            hits = sum(value >= t_point for value in point_probs.values())
            # コア基準（試行 8b）: 全要点が T_POINT 以上なら正解。
            all_points = bool(point_probs) and hits == len(point_probs)
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

        reason = f"段A={major}→{kind}"
        point_values = debug["probabilities"].get("B", {}).values()
        if point_values:
            reason += f", 要点最低={min(point_values):.2f}"
        elif "A3" in debug["probabilities"]:
            reason += f", 再確認={debug['probabilities']['A3']:.2f}"
        return Judgement("jev", kind, answer=answer, reason=reason, debug=debug)
    except Exception as exc:
        raise JevError(f"Jev judgement failed: {exc}") from exc
