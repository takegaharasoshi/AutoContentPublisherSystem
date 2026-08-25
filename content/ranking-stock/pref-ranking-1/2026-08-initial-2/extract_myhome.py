"""Extract the owner-occupied housing-rate ranking from the Statistics Bureau PDF."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent
COMMON_DIR = BASE_DIR.parent / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from prefectures import PREFECTURES  # noqa: E402


DEFAULT_OUTPUT_PATH = BASE_DIR / "data" / "myhome.json"
SOURCE_NAME = "総務省統計局「令和5年住宅・土地統計調査 結果の概要(付表 都道府県別の主な指標)」"
LAST_COLUMNS = re.compile(
    r"(?P<home_count>\d{1,2},\s*\d{3}|\d{3,4})\s+"
    r"(?P<rate>[4-8]\d\.\d)\s*$"
)


def competition_rank(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort rows by value and assign competition ranks."""
    ranked_rows: list[dict[str, Any]] = []
    previous_value: float | None = None
    previous_rank = 0
    for index, row in enumerate(
        sorted(rows, key=lambda item: (-item["value"], item["pref_code"])), start=1
    ):
        rank = previous_rank if row["value"] == previous_value else index
        ranked_rows.append({"rank": rank, **row})
        previous_value = row["value"]
        previous_rank = rank
    return ranked_rows


def require_unique_top_six(ranking: list[dict[str, Any]]) -> None:
    """Reject an item whose first six published values contain a tie."""
    top_six = ranking[:6]
    values = [entry["value"] for entry in top_six]
    if len(set(values)) != len(values):
        raise ValueError(f"TOP6 に同値があります: {top_six}")


def appendix_page_text(input_path: Path) -> str:
    """Return the extracted text of the prefecture-indicator appendix page."""
    reader = PdfReader(input_path)
    appendix_pages = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        # The table of contents also contains the appendix title.  The table
        # itself additionally contains these first two data rows.
        if (
            "付表 都道府県別の主な指標" in page_text
            and "全 国" in page_text
            and "北 海 道" in page_text
        ):
            appendix_pages.append(page_text)
    if len(appendix_pages) != 1:
        raise ValueError(f"付表ページを一意に特定できません: {len(appendix_pages)} 件")
    return appendix_pages[0]


def parse_indicator_line(raw_line: str, pref_name: str) -> dict[str, Any] | None:
    """Parse an appendix row ending in home count and rate."""
    compact_line = re.sub(r"\s+", "", raw_line)
    if not compact_line.startswith(pref_name):
        return None
    match = LAST_COLUMNS.search(raw_line)
    if match is None:
        raise ValueError(f"持ち家数・持ち家住宅率を読めません: {compact_line}")
    return {
        "home_count": int(re.sub(r"[,\s]", "", match.group("home_count"))),
        "value": float(match.group("rate")),
    }


def extract_rows(input_path: Path) -> list[dict[str, Any]]:
    """Extract owner-occupied housing rates for all prefectures from the PDF.

    The PDF text separates many Japanese characters with spaces.  Each line is
    compacted before matching the master prefecture names, then its final two
    values are read as ``持ち家数, 持ち家住宅率``.
    """
    page_text = appendix_page_text(input_path)
    pref_by_name = {pref.name: pref for pref in PREFECTURES}
    parsed: dict[str, dict[str, Any]] = {}
    nationwide: dict[str, Any] | None = None
    names = sorted(pref_by_name, key=len, reverse=True)

    for raw_line in page_text.splitlines():
        compact_line = re.sub(r"\s+", "", raw_line)
        if compact_line.startswith("全国"):
            nationwide = parse_indicator_line(raw_line, "全国")
            continue
        for pref_name in names:
            parsed_line = parse_indicator_line(raw_line, pref_name)
            if parsed_line is not None:
                if pref_name in parsed:
                    raise ValueError(f"都道府県行が重複しています: {pref_name}")
                parsed[pref_name] = parsed_line
                break

    if nationwide != {"home_count": 33876, "value": 60.9}:
        raise ValueError(f"全国のクロスチェックに失敗しました: {nationwide}")
    if parsed.get("北海道") != {"home_count": 1381, "value": 57.0}:
        raise ValueError(f"北海道のクロスチェックに失敗しました: {parsed.get('北海道')}")
    if parsed.get("青森県") != {"home_count": 349, "value": 71.4}:
        raise ValueError(f"青森県のクロスチェックに失敗しました: {parsed.get('青森県')}")
    if len(parsed) != 47 or set(parsed) != set(pref_by_name):
        raise ValueError(f"都道府県行は 47 件必要です: {len(parsed)}")

    rows = [
        {
            "pref_code": pref_by_name[pref_name].code,
            "pref_name": pref_name,
            "value": data["value"],
        }
        for pref_name, data in parsed.items()
    ]
    if not all(40.0 <= row["value"] <= 85.0 for row in rows):
        raise ValueError("持ち家住宅率が想定範囲 40〜85% を外れています")
    return rows


def build_data(input_path: Path) -> dict[str, Any]:
    """Build the canonical ranking JSON from a downloaded PDF file."""
    ranking = competition_rank(extract_rows(input_path))
    require_unique_top_six(ranking)

    return {
        "ranking_data": {
            "entries": [
                {
                    "rank": entry["rank"],
                    "pref_code": entry["pref_code"],
                    "value": entry["value"],
                }
                for entry in ranking[:5]
            ]
        },
        "source_note_text": (
            "都道府県値をそのまま使用（県換算なし）。値は主世帯に占める持ち家の割合"
            "（持ち家住宅率）。概要 PDF の付表 47 行を機械抽出し、TOP6 に同値がないことを"
            "検査済み。"
        ),
        "full_ranking": [
            {
                "rank": entry["rank"],
                "pref_code": entry["pref_code"],
                "pref_name": entry["pref_name"],
                "value": entry["value"],
            }
            for entry in ranking
        ],
        "meta": {
            "item": "持ち家住宅率",
            "category": "住宅",
            "measure": "割合",
            "unit": "%",
            "data_year_label": "2023年(令和5年)10月1日現在",
            "source_name": SOURCE_NAME,
            "retrieved_on": "2026-08-24",
            "url": "https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf",
            "suffix": "%",
            "prefix": None,
            "nationwide": 60.9,
        },
    }


def main() -> None:
    """Parse CLI arguments and write the generated JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path, help="入力の kihon_gaiyou.pdf")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    data = build_data(args.input_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
