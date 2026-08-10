"""Tests for prefecture ranking conversion."""

from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import convert  # noqa: E402
from kakei import ItemSeries, WorkbookData  # noqa: E402
from prefectures import CITY_TO_PREF_CODE  # noqa: E402


def city_values() -> dict[str, int]:
    """Return valid input values for all 52 published cities."""
    return {city: 1000 + index for index, city in enumerate(CITY_TO_PREF_CODE)}


def all_weights() -> dict[str, convert.HouseholdWeight]:
    """Return unit weights for every city that needs aggregation."""
    return {
        city: convert.HouseholdWeight(city, pref_code, 1)
        for city, pref_code in CITY_TO_PREF_CODE.items()
        if pref_code in {14, 22, 27, 40}
    }


def make_workbook(
    name: str = "菓子類", measure: str = "金額", unit: str = "円"
) -> WorkbookData:
    """Create a workbook data fixture containing one fully populated series."""
    values = city_values()
    series = ItemSeries(name, measure, unit, values, 999)
    return WorkbookData("2023年平均", "菓子類", {(name, measure): series})


def write_households_csv(path: Path) -> None:
    """Write a fixture CSV with the required nine city rows."""
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "city", "pref_code", "households", "data_year", "source_name",
                "source_url",
            ],
        )
        writer.writeheader()
        for city, weight in all_weights().items():
            writer.writerow(
                {
                    "city": city,
                    "pref_code": weight.pref_code,
                    "households": weight.households,
                    "data_year": "2025",
                    "source_name": "fixture",
                    "source_url": "https://example.test/households",
                }
            )


def test_convert_uses_weighted_average_and_round_half_up() -> None:
    """Multi-city values use household weights and 0.5 rounds upward."""
    values = city_values()
    values.update({"横浜市": 100, "川崎市": 101, "相模原市": 101})
    weights = all_weights()
    weights["横浜市"] = convert.HouseholdWeight("横浜市", 14, 2)
    weights["川崎市"] = convert.HouseholdWeight("川崎市", 14, 1)
    weights["相模原市"] = convert.HouseholdWeight("相模原市", 14, 1)

    prefecture_values, calculations = convert.convert_city_values(values, weights)

    assert prefecture_values[14] == 101
    assert prefecture_values[1] == values["札幌市"]
    kanagawa = next(item for item in calculations if item["pref_code"] == 14)
    assert kanagawa["raw_value"] == "100.5"
    assert kanagawa["rounded_value"] == 101


def test_load_household_weights_requires_csv_and_all_nine_cities(
    tmp_path: Path,
) -> None:
    """The local CSV error is clear and validates required aggregation rows."""
    with pytest.raises(FileNotFoundError, match="households.csv が見つかりません"):
        convert.load_household_weights(tmp_path / "households.csv")

    path = tmp_path / "households.csv"
    write_households_csv(path)
    weights = convert.load_household_weights(path)
    assert len(weights) == 9

    rows = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(rows[:-1]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="必要な市"):
        convert.load_household_weights(path)


def test_build_result_has_stock_json_shape() -> None:
    """Top-five payload contains only integer rank, code, and value fields."""
    workbook = make_workbook()

    result = convert.build_result(
        series=workbook.items[("菓子類", "金額")],
        workbook=workbook,
        rank_no=9,
        weights=all_weights(),
        suffix="円",
        retrieved_on=date(2026, 8, 10),
    )

    entries = result["ranking_data"]["entries"]
    assert len(entries) == 5
    assert all(set(entry) == {"rank", "pref_code", "value"} for entry in entries)
    assert all(
        all(isinstance(value, int) for value in entry.values())
        for entry in entries
    )
    assert len(result["full_ranking"]) == 47
    assert "神奈川県" in result["source_note_text"]
    assert result["meta"]["data_year_label"] == "2023年平均"
    assert result["meta"]["measure"] == "金額"
    assert result["meta"]["unit"] == "円"


def test_cli_convert_writes_json_without_network(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI can operate entirely from injected fixture data and CSV."""
    csv_path = tmp_path / "households.csv"
    json_path = tmp_path / "result.json"
    write_households_csv(csv_path)
    workbook = make_workbook()
    monkeypatch.setattr(convert, "HOUSEHOLDS_CSV", csv_path)
    monkeypatch.setattr(convert, "load_workbooks", lambda ranks: {9: workbook})

    assert convert.main(
        ["convert", "--item", "菓子", "--rank", "9", "--json", str(json_path)]
    ) == 0

    captured = capsys.readouterr()
    assert "ranking_data:" in captured.out
    saved = json.loads(json_path.read_text(encoding="utf-8"))
    assert set(saved) == {"ranking_data", "source_note_text", "full_ranking", "meta"}


def test_select_item_filters_measure_and_uses_series_unit() -> None:
    """Measure filters same-name series and default suffix follows its unit."""
    values = city_values()
    amount = ItemSeries("米", "金額", "円", values, 999)
    quantity = ItemSeries("米", "数量", "kg", values, 10)
    workbook = WorkbookData(
        "2023年平均", "穀類", {("米", "金額"): amount, ("米", "数量"): quantity}
    )

    rank_no, selected_workbook, selected = convert.select_item(
        {1: workbook}, "米", "数量"
    )
    result = convert.build_result(
        series=selected,
        workbook=selected_workbook,
        rank_no=rank_no,
        weights=all_weights(),
        suffix=None,
    )

    assert selected.measure == "数量"
    assert result["meta"]["suffix"] == "kg"
    with pytest.raises(ValueError, match="rank01.*米 / 金額 / 円"):
        convert.select_item({1: workbook}, "米")


def test_cli_reports_missing_households_before_loading_workbooks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """Missing local weight data produces the required clear error first."""
    monkeypatch.setattr(convert, "HOUSEHOLDS_CSV", tmp_path / "households.csv")
    monkeypatch.setattr(
        convert,
        "load_workbooks",
        lambda ranks: pytest.fail("workbook loading must not run"),
    )

    assert convert.main(["convert", "--item", "菓子", "--rank", "9"]) == 1
    assert "households.csv が見つかりません" in capsys.readouterr().err
