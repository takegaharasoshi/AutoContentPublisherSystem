"""Validate the second prefecture-ranking stock batch (17-5a, 30s only).

This module is intentionally dependency-free so it can be run before review
and imported by ``generate.py``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
COMMON_DIR = BASE_DIR.parent / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from prefectures import PREFECTURE_BY_CODE  # noqa: E402
from stock_items import ITEMS  # noqa: E402


REQUIRED_ITEM_KEYS = (
    "no",
    "slug",
    "data",
    "format",
    "title",
    "hook",
    "trivia",
    "source_display",
    "subtitle",
    "bg_motif",
    "narration",
)

NARRATION_KEYS_20S = (
    "intro",
    "teaser",
    "r5",
    "r4",
    "r3",
    "r2",
    "r1_call",
    "r1_name",
    "outro",
)

NARRATION_KEYS_30S = (
    "intro",
    "teaser",
    "r5",
    "r5_comment",
    "r4",
    "r4_comment",
    "r3",
    "r3_comment",
    "r2",
    "r2_comment",
    "r1_call",
    "r1_name",
    "closing",
)

LIMITS_20S = {
    "intro": 15,
    "teaser": 12,
    "r5": 12,
    "r4": 12,
    "r3": 12,
    "r2": 12,
    "r1_call": 15,
    "r1_name": 12,
    "outro": 18,
}

LIMITS_30S = {
    "intro": 21,
    "teaser": 12,
    "r5": 12,
    "r5_comment": 9,
    "r4": 12,
    "r4_comment": 9,
    "r3": 12,
    "r3_comment": 9,
    "r2": 12,
    "r2_comment": 9,
    "r1_call": 18,
    "r1_name": 15,
    # closing は結果総覧シーン（3.0s）と締めシーン（2.0s）をまたぐ 1 本の cue。
    # 予算は 5.0s × 6.0 モーラ/秒。県名の列挙をやめ、ネタの締めくくりを語る散文にしたため
    # 旧 recap の 7.0 モーラ/秒（列挙は速く読める）は適用しない。
    "closing": 30,
}

# 県名を含むべき cue（5〜2 位は呼び込みと県名を 1 本に統合した `r5`〜`r2`、
# 1 位のみタメ〔r1_call〕と発表〔r1_name〕を分ける）。
NAME_CUE_BY_RANK = {5: "r5", 4: "r4", 3: "r3", 2: "r2", 1: "r1_name"}

FIELD_LIMITS = {
    "title": 30,
    "hook": 60,
    "trivia": 200,
    "source_display": 120,
    "subtitle": 30,
    "bg_motif": 200,
}


# 都道府県コード順の「県／府／都を除いた表記」の実モーラ数（北海道のみ全体で 5）。
# 接尾語は「県」= けん = 2 モーラ、「府」= ふ / 「都」= と = 1 モーラで加算する。
PREFECTURE_SHORT_MORAS = (
    5, 4, 3, 3, 3, 4, 4, 4, 3, 3, 4, 2, 4, 4, 4, 3, 4, 3, 4, 3, 2,
    4, 3, 2, 2, 3, 4, 3, 2, 4, 4, 3, 4, 4, 4, 4, 3, 3, 3, 4, 2, 4,
    4, 4, 4, 4, 4,
)
PREFECTURE_SUFFIX_MORAS = {"県": 2, "府": 1, "都": 1}
SINGLE_DIGIT_MORAS = (2, 2, 1, 2, 2, 1, 2, 2, 2, 2)
SMALL_KANA = frozenset(
    "ぁぃぅぇぉゃゅょゎゕゖァィゥェォャュョヮヵヶ"
)
PREFECTURE_MORA_TOKENS: tuple[tuple[str, int], ...] = tuple(
    sorted(
        (
            token
            for pref, short_mora in zip(
                PREFECTURE_BY_CODE.values(), PREFECTURE_SHORT_MORAS
            )
            for token in (
                (
                    pref.name,
                    short_mora
                    + PREFECTURE_SUFFIX_MORAS.get(pref.name[-1], 0),
                ),
                # 「京都府」→「京都」。rstrip では「都」まで落ちるため末尾 1 文字だけ外す。
                (
                    pref.name[:-1]
                    if pref.name[-1] in PREFECTURE_SUFFIX_MORAS
                    else pref.name,
                    short_mora,
                ),
            )
        ),
        key=lambda value: len(value[0]),
        reverse=True,
    )
)


# 定型句の実モーラ数。漢字は既定で 1 文字 2 モーラの安全側フォールバックで数えるが、
# 全ネタの cue に必ず出る「書式の骨格」だけは過大評価が効きすぎるため実読みを与える
# （「大好き」= だいすき 4 / 「都道府県」= とどうふけん 6 / 「第」= だい 2 / 「位」= い 1）。
# 自由文の語は登録しない（安全側の見積もりを保つ）。
PHRASE_MORAS: tuple[tuple[str, int], ...] = tuple(
    sorted(
        {"都道府県": 6, "大好き": 4, "第": 2, "位": 1}.items(),
        key=lambda value: len(value[0]),
        reverse=True,
    )
)


def estimate_mora(text: str) -> int:
    """Estimate Japanese speech morae for a narration cue.

    Fixed format phrases, prefecture names, and ASCII number expressions are
    handled before the remaining characters because their written length
    differs substantially from their spoken length.

    Args:
        text: Cue text to estimate.

    Returns:
        Estimated mora count.
    """
    mora = 0
    index = 0
    while index < len(text):
        phrase = _matching_phrase_mora(text, index)
        if phrase is not None:
            token, token_mora = phrase
            mora += token_mora
            index += len(token)
            continue

        prefecture = _matching_prefecture_mora(text, index)
        if prefecture is not None:
            token, token_mora = prefecture
            mora += token_mora
            index += len(token)
            continue

        number = re.match(r"\d+(?:\.\d+)?", text[index:])
        if number is not None:
            mora += _number_mora(number.group())
            index += len(number.group())
            continue

        mora += _character_mora(text[index])
        index += 1
    return mora


def _matching_phrase_mora(text: str, index: int) -> tuple[str, int] | None:
    """Return a fixed format phrase beginning at an index, if any."""
    for token, mora in PHRASE_MORAS:
        if text.startswith(token, index):
            return token, mora
    return None


def _matching_prefecture_mora(text: str, index: int) -> tuple[str, int] | None:
    """Return a prefecture token beginning at an index, if any."""
    for token, mora in PREFECTURE_MORA_TOKENS:
        if text.startswith(token, index):
            return token, mora
    return None


def _number_mora(number_text: str) -> int:
    """Estimate morae for an integer up to 99999 or a decimal expression."""
    integer_text, separator, decimal_text = number_text.partition(".")
    integer = int(integer_text)
    if integer <= 99999:
        mora = _integer_mora(integer)
    else:
        mora = sum(SINGLE_DIGIT_MORAS[int(digit)] for digit in integer_text)
    if separator:
        mora += 2
        mora += sum(SINGLE_DIGIT_MORAS[int(digit)] for digit in decimal_text)
    return mora


def _integer_mora(value: int) -> int:
    """Estimate morae for an integer from zero through 99999."""
    if value == 0:
        return SINGLE_DIGIT_MORAS[0]

    mora = 0
    for divisor in (10000, 1000, 100, 10):
        digit, value = divmod(value, divisor)
        if digit:
            if divisor == 10000 or digit != 1:
                mora += SINGLE_DIGIT_MORAS[digit]
            mora += 2
    if value:
        mora += SINGLE_DIGIT_MORAS[value]
    return mora


def _character_mora(char: str) -> int:
    """Estimate morae for one character after special tokens are consumed."""
    if char == "％":
        return 5
    if char in {"ー", "〜"}:
        return 1
    if char in SMALL_KANA:
        return 0
    if "\u3040" <= char <= "\u309f" or "\u30a0" <= char <= "\u30ff":
        return 1 if char != "・" else 0
    if (
        "\u3400" <= char <= "\u4dbf"
        or "\u4e00" <= char <= "\u9fff"
        or "\uf900" <= char <= "\ufaff"
    ):
        return 2
    if char.isascii() and char.isalpha():
        return 2
    return 0


def prefecture_name_variants(pref_code: int) -> tuple[str, ...]:
    """Return acceptable official and suffix-free prefecture spellings.

    Args:
        pref_code: JIS X 0401 prefecture code.

    Returns:
        Accepted name variants, with duplicates removed.
    """
    name = PREFECTURE_BY_CODE[pref_code].name
    short_name = name.rstrip("県府都")
    return tuple(dict.fromkeys((name, short_name)))


def is_number(value: Any) -> bool:
    """Return whether a value is a JSON numeric value, excluding booleans."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def load_data(data_name: str, base_dir: Path = BASE_DIR) -> dict[str, Any]:
    """Load one data file.

    Args:
        data_name: Data file stem.
        base_dir: Batch directory containing ``data/``.

    Returns:
        Parsed JSON object.

    Raises:
        OSError: If the file cannot be read.
        json.JSONDecodeError: If the file is invalid JSON.
    """
    path = base_dir / "data" / f"{data_name}.json"
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def validate_items(
    items: list[dict[str, Any]] | tuple[dict[str, Any], ...] = ITEMS,
    base_dir: Path = BASE_DIR,
) -> list[str]:
    """Return every detected validation violation for the stock items.

    Args:
        items: Items from the single source of truth.
        base_dir: Batch directory containing the ``data`` directory.

    Returns:
        Human-readable violation messages. An empty list means valid.
    """
    errors: list[str] = []
    item_numbers: list[int] = []
    seen_numbers: set[str] = set()
    seen_content_keys: set[str] = set()

    for index, item in enumerate(items, start=1):
        label = f"item #{index}"
        if not isinstance(item, dict):
            errors.append(f"{label}: item must be an object")
            continue

        missing = [key for key in REQUIRED_ITEM_KEYS if key not in item]
        if missing:
            errors.append(f"{label}: missing required keys: {', '.join(missing)}")

        no = item.get("no")
        if not isinstance(no, str) or re.fullmatch(r"\d{3}", no) is None:
            errors.append(f"{label}: no must be a three-digit string")
        else:
            if no in seen_numbers:
                errors.append(f"{label}: duplicate no: {no}")
            seen_numbers.add(no)
            item_numbers.append(int(no))
        identifier = no if isinstance(no, str) else label

        slug = item.get("slug")
        if not isinstance(slug, str) or re.fullmatch(r"[a-z0-9-]+", slug) is None:
            errors.append(f"{identifier}: slug must match [a-z0-9-]+")
        elif isinstance(no, str) and re.fullmatch(r"\d{3}", no):
            content_key = f"{no}-{slug}"
            if len(content_key) > 64:
                errors.append(f"{identifier}: content_key exceeds 64 characters")
            if content_key in seen_content_keys:
                errors.append(f"{identifier}: duplicate content_key: {content_key}")
            seen_content_keys.add(content_key)

        for field, maximum in FIELD_LIMITS.items():
            value = item.get(field)
            if value is not None and not isinstance(value, str):
                errors.append(f"{identifier}: {field} must be a string")
            elif isinstance(value, str) and len(value) > maximum:
                errors.append(
                    f"{identifier}: {field} is {len(value)}/{maximum} characters"
                )

        if item.get("format") is not None and item.get("format") != "top5-map":
            errors.append(f"{identifier}: format must be top5-map")

        data_name = item.get("data")
        data: dict[str, Any] | None = None
        if not isinstance(data_name, str) or not data_name:
            errors.append(f"{identifier}: data must be a non-empty string")
        else:
            data_path = base_dir / "data" / f"{data_name}.json"
            if not data_path.is_file():
                errors.append(f"{identifier}: data file does not exist: {data_path.name}")
            else:
                try:
                    data = load_data(data_name, base_dir)
                except (OSError, json.JSONDecodeError) as exc:
                    errors.append(f"{identifier}: cannot load {data_path.name}: {exc}")

        entries = _validate_ranking_data(identifier, data, errors)
        _validate_full_ranking(identifier, data, errors)
        _validate_narration(identifier, item.get("narration"), entries, errors)

    # 第 2 バッチ以降はセット通し番号（011〜）のため、先頭番号からの連番を検査する
    if item_numbers:
        start = min(item_numbers)
        if sorted(item_numbers) != list(range(start, start + len(items))):
            errors.append("no values must be consecutive")
    return errors


def _validate_ranking_data(
    identifier: str,
    data: dict[str, Any] | None,
    errors: list[str],
) -> list[dict[str, Any]] | None:
    """Validate ranking_data and return its entries when usable."""
    if not isinstance(data, dict):
        return None
    ranking_data = data.get("ranking_data")
    if not isinstance(ranking_data, dict):
        errors.append(f"{identifier}: ranking_data must be an object")
        return None
    entries = ranking_data.get("entries")
    if not isinstance(entries, list):
        errors.append(f"{identifier}: ranking_data.entries must be a list")
        return None
    if len(entries) != 5:
        errors.append(f"{identifier}: ranking_data.entries must contain 5 entries")

    ranks: list[int] = []
    codes: list[int] = []
    valid_entries: list[dict[str, Any]] = []
    for position, entry in enumerate(entries, start=1):
        entry_label = f"{identifier}: ranking_data entry #{position}"
        if not isinstance(entry, dict):
            errors.append(f"{entry_label} must be an object")
            continue
        rank = entry.get("rank")
        code = entry.get("pref_code")
        value = entry.get("value")
        if not isinstance(rank, int) or isinstance(rank, bool) or not 1 <= rank <= 5:
            errors.append(f"{entry_label}: rank must be an integer from 1 to 5")
        else:
            ranks.append(rank)
        if not isinstance(code, int) or isinstance(code, bool) or not 1 <= code <= 47:
            errors.append(f"{entry_label}: pref_code must be an integer from 1 to 47")
        else:
            codes.append(code)
        if not is_number(value):
            errors.append(f"{entry_label}: value must be numeric")
        if (
            isinstance(rank, int)
            and not isinstance(rank, bool)
            and 1 <= rank <= 5
            and isinstance(code, int)
            and not isinstance(code, bool)
            and 1 <= code <= 47
        ):
            valid_entries.append(entry)
    if len(set(ranks)) != len(ranks):
        errors.append(f"{identifier}: ranking_data ranks must be unique")
    if len(set(codes)) != len(codes):
        errors.append(f"{identifier}: ranking_data pref_codes must be unique")
    return valid_entries


def _validate_full_ranking(
    identifier: str,
    data: dict[str, Any] | None,
    errors: list[str],
) -> None:
    """Reject rankings whose top six positions contain a tie."""
    if not isinstance(data, dict):
        return
    full_ranking = data.get("full_ranking")
    if not isinstance(full_ranking, list) or len(full_ranking) < 6:
        errors.append(f"{identifier}: full_ranking must contain at least 6 entries")
        return
    top_six = full_ranking[:6]
    values = [entry.get("value") for entry in top_six if isinstance(entry, dict)]
    if len(values) != 6 or not all(is_number(value) for value in values):
        errors.append(f"{identifier}: full_ranking top 6 must have numeric values")
        return
    if len(set(values)) != 6:
        errors.append(f"{identifier}: full_ranking top 6 contains a tie")


def _validate_narration(
    identifier: str,
    narration: Any,
    entries: list[dict[str, Any]] | None,
    errors: list[str],
) -> None:
    """Validate cue keys, budgets, and prefecture-name consistency."""
    if not isinstance(narration, dict):
        errors.append(f"{identifier}: narration must be an object")
        return
    for duration, expected_keys, limits in (
        ("20s", NARRATION_KEYS_20S, LIMITS_20S),
        ("30s", NARRATION_KEYS_30S, LIMITS_30S),
    ):
        if duration == "20s" and duration not in narration:
            continue
        cues = narration.get(duration)
        if not isinstance(cues, dict):
            errors.append(f"{identifier}: narration[{duration!r}] must be an object")
            continue
        if set(cues) != set(expected_keys):
            missing = [key for key in expected_keys if key not in cues]
            unexpected = sorted(set(cues) - set(expected_keys))
            details = []
            if missing:
                details.append(f"missing: {', '.join(missing)}")
            if unexpected:
                details.append(f"unexpected: {', '.join(unexpected)}")
            errors.append(
                f"{identifier}: narration[{duration!r}] cue keys are invalid"
                + (f" ({'; '.join(details)})" if details else "")
            )
        for cue, maximum in limits.items():
            text = cues.get(cue)
            if not isinstance(text, str):
                if cue in cues:
                    errors.append(f"{identifier}: {duration}.{cue} must be a string")
                continue
            mora = estimate_mora(text)
            if mora > maximum:
                errors.append(
                    f"{identifier}: {duration}.{cue} is {mora} mora / "
                    f"limit {maximum}: {text}"
                )

        if entries is not None:
            by_rank = {entry["rank"]: entry for entry in entries}
            for rank in range(1, 6):
                entry = by_rank.get(rank)
                cue = NAME_CUE_BY_RANK[rank]
                text = cues.get(cue)
                if entry is None or not isinstance(text, str):
                    continue
                expected = prefecture_name_variants(entry["pref_code"])
                if not any(name in text for name in expected):
                    errors.append(
                        f"{identifier}: {duration}.{cue} does not match "
                        f"rank {rank} prefecture {expected[0]}"
                    )

def print_mora_report() -> None:
    """Print each narration cue's estimated morae and its budget."""
    for item in ITEMS:
        for duration, keys, limits in (
            ("20s", NARRATION_KEYS_20S, LIMITS_20S),
            ("30s", NARRATION_KEYS_30S, LIMITS_30S),
        ):
            if duration not in item["narration"]:
                continue
            for cue in keys:
                text = item["narration"][duration][cue]
                print(
                    f"{item['no']} {duration} {cue} "
                    f"{estimate_mora(text)}/{limits[cue]} {text}"
                )


def run_selftest() -> bool:
    """Run the documented representative mora-estimation checks.

    Returns:
        True when every estimate is in its permitted expected range.
    """
    cases = (
        ("ぎょうざにお金を使う県", 13, 2),
        ("全国平均は1984円だ", 20, 4),
        ("12899円", 20, 2),
        ("宮崎県", 6, 0),
        ("鹿児島県", 6, 0),
        ("12.2％", 12, 2),
    )
    passed = True
    for text, expected, tolerance in cases:
        actual = estimate_mora(text)
        success = abs(actual - expected) <= tolerance
        print(
            f"{'OK' if success else 'ERROR'}: {text} -> {actual} mora "
            f"(expected {expected}±{tolerance})"
        )
        passed = passed and success
    return passed


def main() -> int:
    """Run validation, a mora report, or the mora-estimation self-test."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        action="store_true",
        help="print all narration cue mora counts and limits",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run representative estimate_mora checks",
    )
    args = parser.parse_args()

    if args.selftest:
        selftest_passed = run_selftest()
        if not args.report:
            return 0 if selftest_passed else 1

    if args.report:
        print_mora_report()

    errors = validate_items()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(ITEMS)} 件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
