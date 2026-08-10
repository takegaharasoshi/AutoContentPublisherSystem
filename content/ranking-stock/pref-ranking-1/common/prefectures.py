"""Master data for Japanese prefectures and Household Survey cities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Prefecture:
    """A Japanese prefecture identified by its JIS X 0401 code.

    Attributes:
        code: JIS X 0401 prefecture code.
        name: Official Japanese prefecture name.
    """

    code: int
    name: str


PREFECTURES: tuple[Prefecture, ...] = (
    Prefecture(1, "北海道"),
    Prefecture(2, "青森県"),
    Prefecture(3, "岩手県"),
    Prefecture(4, "宮城県"),
    Prefecture(5, "秋田県"),
    Prefecture(6, "山形県"),
    Prefecture(7, "福島県"),
    Prefecture(8, "茨城県"),
    Prefecture(9, "栃木県"),
    Prefecture(10, "群馬県"),
    Prefecture(11, "埼玉県"),
    Prefecture(12, "千葉県"),
    Prefecture(13, "東京都"),
    Prefecture(14, "神奈川県"),
    Prefecture(15, "新潟県"),
    Prefecture(16, "富山県"),
    Prefecture(17, "石川県"),
    Prefecture(18, "福井県"),
    Prefecture(19, "山梨県"),
    Prefecture(20, "長野県"),
    Prefecture(21, "岐阜県"),
    Prefecture(22, "静岡県"),
    Prefecture(23, "愛知県"),
    Prefecture(24, "三重県"),
    Prefecture(25, "滋賀県"),
    Prefecture(26, "京都府"),
    Prefecture(27, "大阪府"),
    Prefecture(28, "兵庫県"),
    Prefecture(29, "奈良県"),
    Prefecture(30, "和歌山県"),
    Prefecture(31, "鳥取県"),
    Prefecture(32, "島根県"),
    Prefecture(33, "岡山県"),
    Prefecture(34, "広島県"),
    Prefecture(35, "山口県"),
    Prefecture(36, "徳島県"),
    Prefecture(37, "香川県"),
    Prefecture(38, "愛媛県"),
    Prefecture(39, "高知県"),
    Prefecture(40, "福岡県"),
    Prefecture(41, "佐賀県"),
    Prefecture(42, "長崎県"),
    Prefecture(43, "熊本県"),
    Prefecture(44, "大分県"),
    Prefecture(45, "宮崎県"),
    Prefecture(46, "鹿児島県"),
    Prefecture(47, "沖縄県"),
)

PREFECTURE_BY_CODE: dict[int, Prefecture] = {pref.code: pref for pref in PREFECTURES}

CITY_TO_PREF_CODE: dict[str, int] = {
    "札幌市": 1, "青森市": 2, "盛岡市": 3, "仙台市": 4, "秋田市": 5,
    "山形市": 6, "福島市": 7, "水戸市": 8, "宇都宮市": 9, "前橋市": 10,
    "さいたま市": 11, "千葉市": 12, "東京都区部": 13, "横浜市": 14,
    "川崎市": 14, "相模原市": 14, "新潟市": 15, "富山市": 16, "金沢市": 17,
    "福井市": 18, "甲府市": 19, "長野市": 20, "岐阜市": 21, "静岡市": 22,
    "浜松市": 22, "名古屋市": 23, "津市": 24, "大津市": 25, "京都市": 26,
    "大阪市": 27, "堺市": 27, "神戸市": 28, "奈良市": 29, "和歌山市": 30,
    "鳥取市": 31, "松江市": 32, "岡山市": 33, "広島市": 34, "山口市": 35,
    "徳島市": 36, "高松市": 37, "松山市": 38, "高知市": 39, "福岡市": 40,
    "北九州市": 40, "佐賀市": 41, "長崎市": 42, "熊本市": 43, "大分市": 44,
    "宮崎市": 45, "鹿児島市": 46, "那覇市": 47,
}

MULTI_CITY_PREFECTURE_CODES: frozenset[int] = frozenset({14, 22, 27, 40})


def cities_for_prefecture(pref_code: int) -> tuple[str, ...]:
    """Return Household Survey cities that belong to a prefecture."""
    return tuple(city for city, code in CITY_TO_PREF_CODE.items() if code == pref_code)


def validate_master_data() -> None:
    """Validate invariants of the prefecture and city master data.

    Raises:
        ValueError: If any master-data invariant is violated.
    """
    prefecture_codes = {pref.code for pref in PREFECTURES}
    city_codes = set(CITY_TO_PREF_CODE.values())
    if len(PREFECTURES) != 47 or prefecture_codes != set(range(1, 48)):
        raise ValueError("都道府県マスタはコード 1〜47 の 47 件である必要があります")
    if len(CITY_TO_PREF_CODE) != 52:
        raise ValueError("家計調査の市は 52 件である必要があります")
    if city_codes != prefecture_codes:
        raise ValueError("全都道府県コードに少なくとも 1 市を対応させる必要があります")
    if MULTI_CITY_PREFECTURE_CODES != {14, 22, 27, 40}:
        raise ValueError("複数市の都道府県コードが不正です")
