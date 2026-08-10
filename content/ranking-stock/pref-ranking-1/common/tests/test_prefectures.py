"""Tests for the prefecture master data."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prefectures import (  # noqa: E402
    CITY_TO_PREF_CODE,
    MULTI_CITY_PREFECTURE_CODES,
    PREFECTURES,
    cities_for_prefecture,
    validate_master_data,
)


def test_master_data_self_check() -> None:
    """The supplied city and prefecture master data is internally consistent."""
    validate_master_data()


def test_multi_city_prefectures_have_expected_cities() -> None:
    """The four aggregate prefectures expose every constituent city."""
    assert MULTI_CITY_PREFECTURE_CODES == {14, 22, 27, 40}
    assert cities_for_prefecture(14) == ("横浜市", "川崎市", "相模原市")
    assert cities_for_prefecture(40) == ("福岡市", "北九州市")
    assert len(PREFECTURES) == 47
    assert len(CITY_TO_PREF_CODE) == 52
