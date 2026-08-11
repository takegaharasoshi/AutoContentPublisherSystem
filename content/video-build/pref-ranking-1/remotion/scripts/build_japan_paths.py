"""Natural Earth（パブリックドメイン）から japanPaths.ts / prefCentroids.ts を生成する。

17-4b で、プロトタイプ由来の GFDL 素材（geolonia/japanese-prefectures）から
**Natural Earth 10m admin-1**（Public Domain）へ差し替えるために新設した。素材要件は
方式設計書 ranking-prebuilt.html セクション 8.2 の warn、ライセンス証跡は
content/video-build/pref-ranking-1/LICENSES.md セクション 3。

    python scripts/build_japan_paths.py            # .cache へ未取得ならダウンロードして生成
    python scripts/build_japan_paths.py --report   # 生成せず診断だけ出す

出力座標は viewBox "0 0 1000 1000" の最終座標（レンダラー側の transform 合成は無い）。
南西諸島は本土と同一投影で投影したうえで、群としてまとめて 1 つの相似変換
（INSET_SCALE 倍 + 平行移動）で関東沖へ移設する（実際の相対配置が自動的に保たれる）。
"""

from __future__ import annotations

import argparse
import io
import math
import struct
import urllib.request
import zipfile
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_DIR / ".cache" / "naturalearth"
SHAPE_STEM = "ne_10m_admin_1_states_provinces"
SOURCE_URL = f"https://naciscdn.org/naturalearth/10m/cultural/{SHAPE_STEM}.zip"

# ---------------------------------------------------------------- 投影・版面

# ランベルト正角円錐図法（標準緯線 30N / 45N・中央経線 137E）。日本地図で一般的な構成。
LCC_PHI1, LCC_PHI2, LCC_LON0 = 30.0, 45.0, 137.0

VIEW_SIZE = 1000.0
# 本土を viewBox に収めるときの余白（上下左右。単位は viewBox 座標）
MAINLAND_MARGIN = 2.0
# 南西諸島インセットの縮尺（本土に対する相対倍率）と配置枠。
# 枠は 17-4a で Fix した点線 L 字（角 = 686,680）の内側。素材差し替えで実ジオメトリに
# なったため、17-4a の 0.75 では枠に収まらない。見た目（L 字の角・占有領域）を正として
# 縮尺の方を実測で決め直した（17-4b）。
INSET_SCALE = 0.68
INSET_BOX = {"left": 690.0, "top": 686.0, "right": 998.0, "bottom": 958.0}
# 点線 L 字（インセットの領域を示す区切り）。17-4a の Fix 値をそのまま維持する。
INSET_FRAME_PATH = "M686,960 L686,680 L1000,680"

# ---------------------------------------------------------------- 素材の補正

# Natural Earth 10m は **奄美群島を沖縄県（JP-47）に割り当てている**（誤り。奄美群島は
# 鹿児島県）。緯度 27.0N 以北かつ経度 128.3E 以東のリングを鹿児島県へ付け替える
# （与論島 128.4E/27.04N は鹿児島、伊平屋島 127.75E/27.0N は沖縄で、経度で分離できる）。
AMAMI_REASSIGN = {"from": 47, "to": 46, "min_lat": 27.0, "min_lon": 128.3}

# 版面に載せない離島（17-4a で Fix した版面の再現。地図ボックスの外へ大きく外れるため）。
# 名称 → (lon_min, lon_max, lat_min, lat_max)
EXCLUDED_ISLANDS = {
    "伊豆諸島": (138.9, 140.2, 30.0, 35.0),
    "小笠原諸島・硫黄島・南鳥島": (140.2, 155.0, 20.0, 31.0),
    "大東諸島": (130.6, 132.0, 24.0, 26.5),
}
# これより小さいリングは点にしかならないため落とす（度²。約 12km² 相当。
# 隠岐・与論島・トカラ列島〔中之島・口之島〕が残る下限として決めた）
MIN_RING_AREA_DEG2 = 0.0012
# 南西諸島インセットへ移す鹿児島県のリング（トカラ列島・奄美群島）の緯度上限。
# 種子島（30.23N〜）・屋久島（30.34N〜）は本土側に残す。
KAGOSHIMA_INSET_MAX_LAT = 30.1

# ---------------------------------------------------------------- 出力の粒度

# 座標の量子化幅（viewBox 単位）。隣接県の共有境界は元データで同一頂点のため、
# 同じ格子へ丸めれば県境に隙間が出ない。
QUANTIZE = 0.25
# 頂点の間引き（前後の頂点を結ぶ線分からの距離がこの値未満なら落とす。viewBox 単位）
SIMPLIFY_EPS = 0.45

ROMAJI = {
    1: "hokkaido", 2: "aomori", 3: "iwate", 4: "miyagi", 5: "akita", 6: "yamagata",
    7: "fukushima", 8: "ibaraki", 9: "tochigi", 10: "gunma", 11: "saitama", 12: "chiba",
    13: "tokyo", 14: "kanagawa", 15: "niigata", 16: "toyama", 17: "ishikawa", 18: "fukui",
    19: "yamanashi", 20: "nagano", 21: "gifu", 22: "shizuoka", 23: "aichi", 24: "mie",
    25: "shiga", 26: "kyoto", 27: "osaka", 28: "hyogo", 29: "nara", 30: "wakayama",
    31: "tottori", 32: "shimane", 33: "okayama", 34: "hiroshima", 35: "yamaguchi",
    36: "tokushima", 37: "kagawa", 38: "ehime", 39: "kochi", 40: "fukuoka", 41: "saga",
    42: "nagasaki", 43: "kumamoto", 44: "oita", 45: "miyazaki", 46: "kagoshima",
    47: "okinawa",
}


# ---------------------------------------------------------------- 素材の読み込み


def ensure_source() -> Path:
    """Download and unzip the Natural Earth shapefile into the local cache.

    Returns:
        Path to the cached shapefile stem (without extension).
    """
    stem = CACHE_DIR / SHAPE_STEM
    if stem.with_suffix(".shp").exists():
        return stem
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"downloading {SOURCE_URL}")
    with urllib.request.urlopen(SOURCE_URL, timeout=300) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        archive.extractall(CACHE_DIR)
    return stem


def read_dbf(path: Path) -> list[dict[str, str]]:
    """Read a dBASE table into a list of string-valued records.

    Args:
        path: Path to the .dbf file (UTF-8 encoded, per the sidecar .cpg).

    Returns:
        One dict per record, keyed by field name.
    """
    blob = path.read_bytes()
    count, header_len, record_len = struct.unpack_from("<IHH", blob, 4)
    fields: list[tuple[str, int]] = []
    offset = 32
    while blob[offset] != 0x0D:
        name = blob[offset : offset + 11].split(b"\0")[0].decode("ascii")
        fields.append((name, blob[offset + 16]))
        offset += 32
    records: list[dict[str, str]] = []
    for index in range(count):
        cursor = header_len + index * record_len + 1
        record: dict[str, str] = {}
        for name, length in fields:
            raw = blob[cursor : cursor + length].decode("utf-8", "replace")
            record[name] = raw.replace("\0", "").strip()
            cursor += length
        records.append(record)
    return records


def read_shp(path: Path) -> dict[int, list[list[tuple[float, float]]]]:
    """Read polygon rings from an ESRI shapefile.

    Args:
        path: Path to the .shp file (shape type 5 = Polygon).

    Returns:
        Mapping of zero-based record index to its list of rings.
    """
    blob = path.read_bytes()
    shapes: dict[int, list[list[tuple[float, float]]]] = {}
    offset = 100
    while offset < len(blob):
        number, length = struct.unpack_from(">II", blob, offset)
        content = blob[offset + 8 : offset + 8 + length * 2]
        shape_type, = struct.unpack_from("<i", content, 0)
        rings: list[list[tuple[float, float]]] = []
        if shape_type == 5:
            part_count, point_count = struct.unpack_from("<ii", content, 36)
            parts = struct.unpack_from(f"<{part_count}i", content, 44)
            values = struct.unpack_from(f"<{point_count * 2}d", content, 44 + part_count * 4)
            for index, start in enumerate(parts):
                end = parts[index + 1] if index + 1 < part_count else point_count
                rings.append([(values[2 * i], values[2 * i + 1]) for i in range(start, end)])
        shapes[number - 1] = rings
        offset += 8 + length * 2
    return shapes


def ring_bbox(ring: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    """Return (lon_min, lon_max, lat_min, lat_max) of a ring."""
    lons = [p[0] for p in ring]
    lats = [p[1] for p in ring]
    return min(lons), max(lons), min(lats), max(lats)


def ring_area(ring: list[tuple[float, float]]) -> float:
    """Return the absolute shoelace area of a ring in squared source units."""
    total = 0.0
    for index in range(len(ring)):
        x1, y1 = ring[index]
        x2, y2 = ring[(index + 1) % len(ring)]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def load_prefecture_rings() -> dict[int, list[list[tuple[float, float]]]]:
    """Load Japanese prefecture rings with the Amami reassignment and island filters.

    Returns:
        Mapping of JIS prefecture code to the rings kept for rendering.
    """
    stem = ensure_source()
    records = read_dbf(stem.with_suffix(".dbf"))
    shapes = read_shp(stem.with_suffix(".shp"))
    rings: dict[int, list[list[tuple[float, float]]]] = {code: [] for code in ROMAJI}
    dropped: list[str] = []
    for index, record in enumerate(records):
        if record.get("adm0_a3") != "JPN":
            continue
        code = int(record["iso_3166_2"].split("-")[1])
        for ring in shapes[index]:
            lon_min, lon_max, lat_min, lat_max = ring_bbox(ring)
            target = code
            if (
                code == AMAMI_REASSIGN["from"]
                and lat_min >= AMAMI_REASSIGN["min_lat"]
                and lon_min >= AMAMI_REASSIGN["min_lon"]
            ):
                target = AMAMI_REASSIGN["to"]
            excluded = any(
                box[0] <= lon_min and lon_max <= box[1] and box[2] <= lat_min and lat_max <= box[3]
                for box in EXCLUDED_ISLANDS.values()
            )
            if excluded or ring_area(ring) < MIN_RING_AREA_DEG2:
                dropped.append(f"{code}:{lon_min:.2f},{lat_min:.2f}")
                continue
            rings[target].append(ring)
    missing = [code for code, value in rings.items() if not value]
    if missing:
        raise RuntimeError(f"リングが 1 つも残らなかった県がある: {missing}")
    check_landmarks(rings)
    print(f"採用リング {sum(len(v) for v in rings.values())} / 除外 {len(dropped)}")
    return rings


# 素材の取り違え・素材更新による退行を検出する目印（島 → 期待する県コード。None = 版面に載せない）。
# Natural Earth の奄美群島の誤割当（沖縄県）を補正できているかの検査を兼ねる。
LANDMARKS: dict[str, tuple[float, float, int | None]] = {
    "隠岐": (133.30, 36.25, 32),
    "佐渡": (138.40, 38.05, 15),
    "対馬": (129.30, 34.40, 42),
    "五島（福江島）": (128.75, 32.70, 42),
    "淡路島": (134.85, 34.35, 28),
    "小豆島": (134.25, 34.50, 37),
    "利尻島": (141.20, 45.18, 1),
    "種子島": (130.95, 30.60, 46),
    "屋久島": (130.50, 30.35, 46),
    "中之島（トカラ）": (129.86, 29.85, 46),
    "奄美大島": (129.40, 28.30, 46),
    "喜界島": (129.98, 28.32, 46),
    "徳之島": (128.95, 27.80, 46),
    "与論島": (128.43, 27.04, 46),
    "沖縄本島": (127.90, 26.50, 47),
    "宮古島": (125.30, 24.80, 47),
    "石垣島": (124.20, 24.40, 47),
    "伊豆大島": (139.40, 34.75, None),
    "八丈島": (139.80, 33.10, None),
    "父島（小笠原）": (142.15, 27.07, None),
    "南大東島": (131.24, 25.85, None),
}


def check_landmarks(rings: dict[int, list[list[tuple[float, float]]]]) -> None:
    """Fail loudly when a landmark island lands in the wrong prefecture.

    Args:
        rings: Rings kept per prefecture code (before projection).

    Raises:
        RuntimeError: If any landmark is missing or attached to another prefecture.
    """
    problems = []
    for name, (lon, lat, expected) in LANDMARKS.items():
        found = None
        for code, prefecture in rings.items():
            for ring in prefecture:
                lon_min, lon_max, lat_min, lat_max = ring_bbox(ring)
                if lon_min - 0.05 <= lon <= lon_max + 0.05 and lat_min - 0.05 <= lat <= lat_max + 0.05:
                    found = code
        if found != expected:
            problems.append(f"{name}: 期待 {expected} / 実際 {found}")
    if problems:
        raise RuntimeError("目印の島の割当が想定と違う: " + " / ".join(problems))
    print(f"目印の島 {len(LANDMARKS)} 件の割当を確認")


# ---------------------------------------------------------------- 投影・配置


def project(lon: float, lat: float) -> tuple[float, float]:
    """Project lon/lat with a Lambert conformal conic projection.

    Args:
        lon: Longitude in degrees.
        lat: Latitude in degrees.

    Returns:
        Projected (x, y) in arbitrary units, y already pointing down (screen order).
    """
    phi1, phi2 = math.radians(LCC_PHI1), math.radians(LCC_PHI2)
    phi, lam = math.radians(lat), math.radians(lon - LCC_LON0)
    n = math.log(math.cos(phi1) / math.cos(phi2)) / math.log(
        math.tan(math.pi / 4 + phi2 / 2) / math.tan(math.pi / 4 + phi1 / 2)
    )
    f = math.cos(phi1) * math.tan(math.pi / 4 + phi1 / 2) ** n / n
    rho = f / math.tan(math.pi / 4 + phi / 2) ** n
    return rho * math.sin(n * lam), rho * math.cos(n * lam)


def is_nansei_inset(code: int, ring: list[tuple[float, float]]) -> bool:
    """Return True when the ring belongs to the south-west islands inset."""
    if code == 47:
        return True
    if code == 46:
        return ring_bbox(ring)[3] < KAGOSHIMA_INSET_MAX_LAT
    return False


def quantize(value: float) -> float:
    """Snap a coordinate to the output grid (keeps shared borders gap-free)."""
    return round(value / QUANTIZE) * QUANTIZE


def simplify(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Drop vertices that sit within SIMPLIFY_EPS of the line through their neighbours.

    The filter is local so a shared border keeps matching vertices on both sides.

    Args:
        points: Closed ring vertices in viewBox coordinates.

    Returns:
        The ring with near-collinear vertices removed (at least 3 vertices kept).
    """
    result = list(points)
    changed = True
    while changed and len(result) > 3:
        changed = False
        index = 0
        while index < len(result) and len(result) > 3:
            prev = result[index - 1]
            current = result[index]
            following = result[(index + 1) % len(result)]
            dx, dy = following[0] - prev[0], following[1] - prev[1]
            length = math.hypot(dx, dy)
            if length == 0:
                distance = math.hypot(current[0] - prev[0], current[1] - prev[1])
            else:
                distance = abs(
                    dy * (current[0] - prev[0]) - dx * (current[1] - prev[1])
                ) / length
            if distance < SIMPLIFY_EPS:
                del result[index]
                changed = True
            else:
                index += 1
    return result


def build_geometry() -> tuple[dict[int, list[list[tuple[float, float]]]], dict[str, float]]:
    """Project every prefecture into final viewBox coordinates.

    Returns:
        A tuple of (rings per prefecture code, diagnostics).
    """
    source = load_prefecture_rings()
    projected: dict[int, list[tuple[bool, list[tuple[float, float]]]]] = {}
    for code, rings in source.items():
        projected[code] = [
            (is_nansei_inset(code, ring), [project(lon, lat) for lon, lat in ring])
            for ring in rings
        ]

    mainland = [p for entries in projected.values() for inset, ring in entries if not inset for p in ring]
    min_x = min(p[0] for p in mainland)
    max_x = max(p[0] for p in mainland)
    min_y = min(p[1] for p in mainland)
    max_y = max(p[1] for p in mainland)
    span = VIEW_SIZE - 2 * MAINLAND_MARGIN
    scale = min(span / (max_x - min_x), span / (max_y - min_y))
    offset_x = MAINLAND_MARGIN + (span - (max_x - min_x) * scale) / 2 - min_x * scale
    offset_y = MAINLAND_MARGIN + (span - (max_y - min_y) * scale) / 2 - min_y * scale

    def to_view(point: tuple[float, float]) -> tuple[float, float]:
        return point[0] * scale + offset_x, point[1] * scale + offset_y

    # 南西諸島は本土と同一投影のまま群としてまとめ、相似変換で関東沖の枠へ移す
    inset_points = [to_view(p) for entries in projected.values() for inset, ring in entries if inset for p in ring]
    inset_min_x = min(p[0] for p in inset_points)
    inset_max_x = max(p[0] for p in inset_points)
    inset_min_y = min(p[1] for p in inset_points)
    inset_max_y = max(p[1] for p in inset_points)
    box_w = INSET_BOX["right"] - INSET_BOX["left"]
    box_h = INSET_BOX["bottom"] - INSET_BOX["top"]
    inset_dx = (
        INSET_BOX["left"] + (box_w - (inset_max_x - inset_min_x) * INSET_SCALE) / 2
        - inset_min_x * INSET_SCALE
    )
    inset_dy = (
        INSET_BOX["top"] + (box_h - (inset_max_y - inset_min_y) * INSET_SCALE) / 2
        - inset_min_y * INSET_SCALE
    )

    final: dict[int, list[list[tuple[float, float]]]] = {}
    for code, entries in projected.items():
        rings = []
        for inset, ring in entries:
            points = [to_view(p) for p in ring]
            if inset:
                points = [
                    (x * INSET_SCALE + inset_dx, y * INSET_SCALE + inset_dy) for x, y in points
                ]
            snapped: list[tuple[float, float]] = []
            for x, y in points:
                point = (quantize(x), quantize(y))
                if not snapped or point != snapped[-1]:
                    snapped.append(point)
            if len(snapped) > 1 and snapped[0] == snapped[-1]:
                snapped.pop()
            reduced = simplify(snapped)
            if len(reduced) >= 3:
                rings.append(reduced)
        final[code] = rings

    diagnostics = {
        "mainland_scale": scale,
        "inset_scale_absolute": scale * INSET_SCALE,
        "inset_width": (inset_max_x - inset_min_x) * INSET_SCALE,
        "inset_height": (inset_max_y - inset_min_y) * INSET_SCALE,
    }
    return final, diagnostics


# ---------------------------------------------------------------- 出力


def path_data(rings: list[list[tuple[float, float]]]) -> str:
    """Render rings as a single SVG path definition."""
    parts = []
    for ring in rings:
        head = f"M{ring[0][0]:g} {ring[0][1]:g}"
        body = "".join(f"L{x:g} {y:g}" for x, y in ring[1:])
        parts.append(f"{head}{body}Z")
    return "".join(parts)


def centroid(code: int, rings: list[list[tuple[float, float]]]) -> tuple[float, float]:
    """Return the label anchor for a prefecture.

    Kagoshima uses its mainland part only (the inset islands would drag the anchor
    into the Pacific); every other prefecture uses the bounding-box centre of the
    rings as rendered.

    Args:
        code: JIS prefecture code.
        rings: Final viewBox rings for the prefecture.

    Returns:
        Anchor point in viewBox coordinates.
    """
    target = rings
    if code == 46:
        target = [ring for ring in rings if min(p[0] for p in ring) < INSET_BOX["left"]]
    xs = [p[0] for ring in target for p in ring]
    ys = [p[1] for ring in target for p in ring]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2


NAMES = {
    1: "北海道", 2: "青森", 3: "岩手", 4: "宮城", 5: "秋田", 6: "山形", 7: "福島",
    8: "茨城", 9: "栃木", 10: "群馬", 11: "埼玉", 12: "千葉", 13: "東京", 14: "神奈川",
    15: "新潟", 16: "富山", 17: "石川", 18: "福井", 19: "山梨", 20: "長野", 21: "岐阜",
    22: "静岡", 23: "愛知", 24: "三重", 25: "滋賀", 26: "京都", 27: "大阪", 28: "兵庫",
    29: "奈良", 30: "和歌山", 31: "鳥取", 32: "島根", 33: "岡山", 34: "広島", 35: "山口",
    36: "徳島", 37: "香川", 38: "愛媛", 39: "高知", 40: "福岡", 41: "佐賀", 42: "長崎",
    43: "熊本", 44: "大分", 45: "宮崎", 46: "鹿児島", 47: "沖縄",
}


def write_outputs(final: dict[int, list[list[tuple[float, float]]]]) -> None:
    """Write japanPaths.ts and prefCentroids.ts."""
    header = [
        "// 自動生成: scripts/build_japan_paths.py（手で編集しない）",
        "// 出典: Natural Earth 10m admin-1 states/provinces（**Public Domain**）",
        "//       https://www.naturalearthdata.com/downloads/10m-cultural-vectors/",
        "//       ライセンス証跡は ../../LICENSES.md セクション 3",
        "// 座標は viewBox 0 0 1000 1000 の最終座標。南西諸島は同一投影のまま群として",
        "// 相似変換で関東沖へ移設済み（インセット。詳細は生成スクリプトの定数）。",
        "",
        "export interface PrefPath {",
        "  code: number;",
        "  romaji: string;",
        "  name: string;",
        "  /** viewBox 座標の path d（県内の飛び地は同一 path のサブパス） */",
        "  d: string;",
        "}",
        "",
        'export const VIEW_BOX = "0 0 1000 1000";',
        "",
        "/** 南西諸島インセットの区切り（点線 L 字。17-4a で Fix した見た目） */",
        f'export const INSET_FRAME_PATH = "{INSET_FRAME_PATH}";',
        "",
        "export const PREFECTURES: PrefPath[] = [",
    ]
    body = []
    for code in sorted(final):
        body.append(
            "  { code: %d, romaji: %r, name: %r, d: %r },"
            % (code, ROMAJI[code], NAMES[code], path_data(final[code]))
        )
    body = [line.replace("'", '"') for line in body]
    lines = header + body + ["];", ""]
    (PROJECT_DIR / "src" / "japanPaths.ts").write_text("\n".join(lines), encoding="utf-8")

    centroid_lines = [
        "// 自動生成: scripts/build_japan_paths.py（japanPaths.ts と同時生成）",
        "// 確定県のラベルを飛ばす起点。viewBox 0 0 1000 1000 の座標。",
        "// 鹿児島は本土部分のみ、沖縄はインセットの位置で算出する。",
        "export const PREF_CENTROIDS: Record<number, { x: number; y: number }> = {",
    ]
    for code in sorted(final):
        x, y = centroid(code, final[code])
        centroid_lines.append(f"  {code}: {{ x: {x:.1f}, y: {y:.1f} }}, // {NAMES[code]}")
    centroid_lines += ["};", ""]
    (PROJECT_DIR / "src" / "prefCentroids.ts").write_text(
        "\n".join(centroid_lines), encoding="utf-8"
    )


def report(final: dict[int, list[list[tuple[float, float]]]], diagnostics: dict[str, float]) -> None:
    """Print geometry diagnostics for a build."""
    points = [p for rings in final.values() for ring in rings for p in ring]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    print(
        f"頂点 {len(points)} / リング {sum(len(r) for r in final.values())} / "
        f"陸地 bbox x {min(xs):.1f}..{max(xs):.1f} y {min(ys):.1f}..{max(ys):.1f}"
    )
    print(
        f"インセット枠 {diagnostics['inset_width']:.1f}x{diagnostics['inset_height']:.1f} "
        f"(枠 {INSET_BOX['right'] - INSET_BOX['left']:.0f}x{INSET_BOX['bottom'] - INSET_BOX['top']:.0f})"
    )
    for code in (13, 46, 47):
        x, y = centroid(code, final[code])
        print(f"  {NAMES[code]}: ラベル起点 ({x:.1f}, {y:.1f}) / リング {len(final[code])}")


def main() -> None:
    """Build the map assets."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true", help="生成せず診断のみ出力する")
    args = parser.parse_args()
    final, diagnostics = build_geometry()
    report(final, diagnostics)
    if not args.report:
        write_outputs(final)
        print("wrote src/japanPaths.ts, src/prefCentroids.ts")


if __name__ == "__main__":
    main()
