"""Convert Household Survey city rankings into prefecture rankings."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import sys
from typing import Iterable
import unicodedata

from kakei import (
    RANK_URL_TEMPLATE,
    ItemSeries,
    WorkbookData,
    download,
    parse,
)
from prefectures import (
    CITY_TO_PREF_CODE,
    MULTI_CITY_PREFECTURE_CODES,
    PREFECTURES,
    PREFECTURE_BY_CODE,
    cities_for_prefecture,
)


COMMON_DIR = Path(__file__).resolve().parent
CACHE_DIR = COMMON_DIR / ".cache"
HOUSEHOLDS_CSV = COMMON_DIR / "households.csv"
# 家計調査のランキング表は「1 世帯当たり年間支出金額 / 年間購入数量」のため、
# 本ツールが換算したネタの value_prefix は既定で「年間」になる（--prefix "" で無効化）。
DEFAULT_PREFIX = "年間"


@dataclass(frozen=True)
class HouseholdWeight:
    """A household count used to combine cities within a prefecture."""

    city: str
    pref_code: int
    households: int


def load_household_weights(path: Path) -> dict[str, HouseholdWeight]:
    """Load and validate household weights for the nine multi-city locations.

    Args:
        path: Headered households CSV file.

    Returns:
        Weights keyed by city name.

    Raises:
        FileNotFoundError: If the CSV does not exist.
        ValueError: If required columns or required city rows are invalid.
    """
    if not path.is_file():
        raise FileNotFoundError(f"households.csv が見つかりません: {path}")
    required_columns = {
        "city", "pref_code", "households", "data_year", "source_name", "source_url",
    }
    weights: dict[str, HouseholdWeight] = {}
    with path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if (
            reader.fieldnames is None
            or not required_columns.issubset(reader.fieldnames)
        ):
            raise ValueError("households.csv のヘッダが不正です")
        for row in reader:
            city = (row.get("city") or "").strip()
            if city not in CITY_TO_PREF_CODE:
                continue
            try:
                pref_code = int(row["pref_code"])
                households = int(row["households"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"households.csv の数値が不正です: {city}") from exc
            if pref_code != CITY_TO_PREF_CODE[city] or households <= 0:
                raise ValueError(f"households.csv の行が不正です: {city}")
            if city in weights:
                raise ValueError(f"households.csv の市名が重複しています: {city}")
            weights[city] = HouseholdWeight(city, pref_code, households)

    required_cities = {
        city
        for code in MULTI_CITY_PREFECTURE_CODES
        for city in cities_for_prefecture(code)
    }
    missing = required_cities - set(weights)
    if missing:
        raise ValueError(
            "households.csv に必要な市がありません: " + ", ".join(sorted(missing))
        )
    return weights


def convert_city_values(
    city_values: dict[str, int | Decimal],
    weights: dict[str, HouseholdWeight],
) -> tuple[dict[int, int | Decimal], list[dict[str, object]]]:
    """Convert city values to one value per prefecture.

    Args:
        city_values: Values keyed by the 52 published city names.
        weights: Household weights keyed by city name.

    Returns:
        Prefecture values and calculation details for multi-city prefectures.
    """
    if set(city_values) != set(CITY_TO_PREF_CODE):
        raise ValueError("換算には 52 市すべての値が必要です")
    # 加重平均の丸め桁は公表値の桁数に合わせる（金額は整数、数量は kg 等で小数を持つ）。
    exponent = Decimal(1).scaleb(-_source_decimal_places(city_values))
    pref_values: dict[int, int | Decimal] = {}
    calculations: list[dict[str, object]] = []
    for prefecture in PREFECTURES:
        cities = cities_for_prefecture(prefecture.code)
        if prefecture.code not in MULTI_CITY_PREFECTURE_CODES:
            pref_values[prefecture.code] = city_values[cities[0]]
            continue
        components = []
        numerator = Decimal(0)
        denominator = 0
        for city in cities:
            weight = weights.get(city)
            if weight is None:
                raise ValueError(f"households.csv に必要な市がありません: {city}")
            value = city_values[city]
            numerator += Decimal(str(value)) * weight.households
            denominator += weight.households
            components.append(
                {"city": city, "value": value, "weight": weight.households}
            )
        raw_value = numerator / Decimal(denominator)
        quantized = raw_value.quantize(exponent, rounding=ROUND_HALF_UP)
        rounded_value: int | Decimal = (
            int(quantized) if exponent == 1 else quantized
        )
        pref_values[prefecture.code] = rounded_value
        calculations.append(
            {
                "pref_code": prefecture.code,
                "pref_name": prefecture.name,
                "components": components,
                "numerator": str(numerator),
                "denominator": denominator,
                "raw_value": str(raw_value),
                "rounded_value": rounded_value,
            }
        )
    return pref_values, calculations


def build_result(
    *,
    series: ItemSeries,
    workbook: WorkbookData,
    rank_no: int,
    weights: dict[str, HouseholdWeight],
    suffix: str | None,
    prefix: str | None = DEFAULT_PREFIX,
    retrieved_on: date | None = None,
) -> dict[str, object]:
    """Build ranking and source-note output for one selected item."""
    output_suffix = series.unit if suffix is None else suffix
    pref_values, calculations = convert_city_values(series.values, weights)
    ranked_codes = sorted(pref_values, key=lambda code: (-pref_values[code], code))
    full_ranking = [
        {
            "rank": rank,
            "pref_code": code,
            "pref_name": PREFECTURE_BY_CODE[code].name,
            "value": _json_number(pref_values[code]),
        }
        for rank, code in enumerate(ranked_codes, start=1)
    ]
    ranking_data = {
        "entries": [
            {
                "rank": entry["rank"],
                "pref_code": entry["pref_code"],
                "value": entry["value"],
            }
            for entry in full_ranking[:5]
        ]
    }
    source_note_text = format_source_note(calculations, output_suffix)
    source_date = (retrieved_on or date.today()).isoformat()
    return {
        "ranking_data": ranking_data,
        "source_note_text": source_note_text,
        "full_ranking": full_ranking,
        "meta": {
            "item": series.name,
            "measure": series.measure,
            "unit": series.unit,
            "category": workbook.category,
            "data_year_label": workbook.data_year_label,
            "source_name": (
                "総務省統計局「家計調査 品目別都道府県庁所在市及び"
                "政令指定都市ランキング」"
            ),
            "retrieved_on": source_date,
            "url": RANK_URL_TEMPLATE.format(rank_no=rank_no),
            "suffix": output_suffix,
            # 数値の前置き（content_fields.value_prefix）。家計調査の値は「1 世帯当たり
            # 年間支出金額 / 年間購入数量」のため既定は「年間」。不要なネタは null。
            "prefix": prefix or None,
            # 全国値（順位 0 の行）。「全国平均の◯倍」のような小ネタの根拠に使う。
            "nationwide": _json_number(series.nationwide),
        },
    }


def format_source_note(calculations: list[dict[str, object]], suffix: str) -> str:
    """Format multi-city weighted-average details for a stock source note."""
    lines = ["都道府県換算（複数市は世帯数による加重平均）"]
    for calculation in calculations:
        components = calculation["components"]
        assert isinstance(components, list)
        terms = " + ".join(
            f"{component['city']} {component['value']}{suffix} × "
            f"{component['weight']}世帯"
            for component in components
        )
        raw_display = Decimal(str(calculation["raw_value"])).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        lines.append(
            f"{calculation['pref_name']}: ({terms}) ÷ {calculation['denominator']}世帯 "
            f"= {raw_display}{suffix} → "
            f"{calculation['rounded_value']}{suffix}（四捨五入）"
        )
    return "\n".join(lines)


def _source_decimal_places(city_values: dict[str, int | Decimal]) -> int:
    """Return the number of decimal places used by the published city values."""
    places = 0
    for value in city_values.values():
        if isinstance(value, Decimal):
            places = max(places, -value.normalize().as_tuple().exponent)
    return places


def _json_number(value: int | Decimal) -> int | float:
    """Convert Decimal values into JSON-compatible numeric values."""
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    return value


def load_workbooks(rank_numbers: Iterable[int]) -> dict[int, WorkbookData]:
    """Download (when needed) and parse requested workbooks."""
    return {
        rank_no: parse(download(rank_no, cache_dir=CACHE_DIR))
        for rank_no in rank_numbers
    }


def select_item(
    workbooks: dict[int, WorkbookData],
    query: str,
    measure: str | None = None,
) -> tuple[int, WorkbookData, ItemSeries]:
    """Find an item across workbook data, requiring one unambiguous result."""
    normalized_query = _normalize_for_search(query)
    if not normalized_query:
        raise ValueError("品目名を指定してください")
    if measure not in (None, "金額", "数量"):
        raise ValueError(f"未知の系列です: {measure}")
    matches: list[tuple[int, WorkbookData, ItemSeries]] = []
    for rank_no, workbook in workbooks.items():
        for series in workbook.items.values():
            if normalized_query not in _normalize_for_search(series.name):
                continue
            if measure is not None and series.measure != measure:
                continue
            matches.append((rank_no, workbook, series))
    if not matches:
        raise ValueError(f"品目が見つかりません: {query}")
    # 「パン」「外食」のように別品目の部分文字列になる名前があるため、
    # 完全一致が 1 件だけならそれを優先する。
    exact = [
        match
        for match in matches
        if _normalize_for_search(match[2].name) == normalized_query
    ]
    if len(exact) == 1:
        return exact[0]
    if len(matches) != 1:
        candidates = ", ".join(
            f"rank{rank_no:02d}（{workbook.category}: {series.name} / "
            f"{series.measure} / {series.unit}）"
            for rank_no, workbook, series in matches
        )
        raise ValueError(f"品目が複数のファイルに見つかりました: {candidates}")
    return matches[0]


def _normalize_for_search(value: str) -> str:
    """Normalize width variants and remove whitespace for item matching."""
    return "".join(unicodedata.normalize("NFKC", value).split())


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="家計調査市別ランキングを都道府県ランキングへ換算します"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="利用可能な品目を一覧表示")
    list_parser.add_argument("--rank", type=int, choices=range(1, 15))
    convert_parser = subparsers.add_parser("convert", help="品目を都道府県ランキングへ換算")
    convert_parser.add_argument("--item", required=True)
    convert_parser.add_argument("--rank", type=int, choices=range(1, 15))
    convert_parser.add_argument("--measure", choices=("金額", "数量"), default="金額")
    convert_parser.add_argument("--suffix")
    convert_parser.add_argument(
        "--prefix",
        default=DEFAULT_PREFIX,
        help=f"数値の前置き（既定: {DEFAULT_PREFIX}）。空文字を渡すと null になる",
    )
    convert_parser.add_argument("--json", type=Path, dest="json_path")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    parser = _make_parser()
    args = parser.parse_args(argv)
    ranks = [args.rank] if args.rank else list(range(1, 15))
    try:
        weights: dict[str, HouseholdWeight] = {}
        if args.command == "convert":
            weights = load_household_weights(HOUSEHOLDS_CSV)
        workbooks = load_workbooks(ranks)
        if args.command == "list":
            for rank_no, workbook in workbooks.items():
                for series in workbook.items.values():
                    print(
                        f"rank{rank_no:02d}\t{workbook.category}\t{series.name}\t"
                        f"{series.measure}\t{series.unit}"
                    )
            return 0
        rank_no, workbook, series = select_item(
            workbooks, args.item, args.measure
        )
        result = build_result(
            series=series,
            workbook=workbook,
            rank_no=rank_no,
            weights=weights,
            suffix=args.suffix,
            prefix=args.prefix,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    suffix = result["meta"]["suffix"]
    print(
        f"都道府県ランキング: {series.name}（{series.measure}・{series.unit} / "
        f"{workbook.data_year_label}）"
    )
    for entry in result["full_ranking"]:
        print(
            f"{entry['rank']}位\t{entry['pref_name']}\t"
            f"{entry['value']:,}{suffix}"
        )
    print("\nranking_data:")
    print(json.dumps(result["ranking_data"], ensure_ascii=False))
    print("\nsource_note:")
    print(result["source_note_text"])
    meta = result["meta"]
    print("\n出典:")
    print(
        f"{meta['source_name']} / {meta['data_year_label']} / "
        f"取得日 {meta['retrieved_on']} / {meta['url']}"
    )
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
