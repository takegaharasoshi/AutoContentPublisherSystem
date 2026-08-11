// 版面のジオメトリ（1080x1920 / 30fps）。
// Instagram UI を避けるセーフボックスは前景基準で右 12% / 下 15%（project memory・15-x の運用と同じ）。

export const CANVAS = { width: 1080, height: 1920 } as const;

export const SAFE = {
  left: 60,
  right: 950, // 1080 - 130（右 12%）
  top: 60,
  bottom: 1668, // 1920 - 252（下 15% 弱）
} as const;

export const CONTENT_W = SAFE.right - SAFE.left; // 890

/** タイトル帯（左端は画面外へ抜けさせて帯らしく見せる） */
export const BAND = { left: -40, top: 96, right: SAFE.right, height: 128 } as const;

/**
 * 日本地図の描画ボックスと viewBox。
 * viewBox は素材の全域（0 0 1000 1000）をそのまま使う。陸地の実バウンディングボックスは
 * x 3.9〜996.7 / y 0.0〜1000.0 で余白がほぼ無く、切り詰めると九州南部（鹿児島の南端が
 * y=1000）と南西諸島インセットが欠ける（17-4a 第 3 巡で判明）。
 * 地図ボックスは「幅いっぱい（890）の正方形が順位行スタックの上に収まる」高さに合わせる。
 */
export const MAP_BOX = { left: 60, top: 232, width: 890, height: 866 } as const;
export const MAP_VIEWBOX = { x: 0, y: 0, width: 1000, height: 1000 } as const;

export const MAP_SCALE = Math.min(
  MAP_BOX.width / MAP_VIEWBOX.width,
  MAP_BOX.height / MAP_VIEWBOX.height
);
export const MAP_ORIGIN = {
  x: MAP_BOX.left + (MAP_BOX.width - MAP_VIEWBOX.width * MAP_SCALE) / 2,
  y: MAP_BOX.top + (MAP_BOX.height - MAP_VIEWBOX.height * MAP_SCALE) / 2,
};

/** viewBox 座標 → 画面座標 */
export const mapPoint = (x: number, y: number): { x: number; y: number } => ({
  x: MAP_ORIGIN.x + (x - MAP_VIEWBOX.x) * MAP_SCALE,
  y: MAP_ORIGIN.y + (y - MAP_VIEWBOX.y) * MAP_SCALE,
});

/** 地図コンテナの拡大（transform-origin: center top）の基準点 */
export const MAP_ZOOM_ORIGIN = {
  x: MAP_BOX.left + MAP_BOX.width / 2,
  y: MAP_BOX.top,
} as const;

/** viewBox 座標 → 画面座標（地図の拡大率を反映する。ピン・県名ラベル用） */
export const mapPointZoomed = (
  x: number,
  y: number,
  zoom: number
): { x: number; y: number } => {
  const p = mapPoint(x, y);
  return {
    x: MAP_ZOOM_ORIGIN.x + (p.x - MAP_ZOOM_ORIGIN.x) * zoom,
    y: MAP_ZOOM_ORIGIN.y + (p.y - MAP_ZOOM_ORIGIN.y) * zoom,
  };
};

/** 順位行スタック（下端を固定し、5 位から上へ積み上がる） */
export const ROW = { firstHeight: 104, height: 82, gap: 12 } as const;
export const LIST = {
  left: SAFE.left,
  right: SAFE.right,
  bottom: 1578,
  height: ROW.firstHeight + ROW.height * 4 + ROW.gap * 4, // 480
} as const;
export const LIST_TOP = LIST.bottom - LIST.height; // 1112

export const rowTop = (rank: number): number =>
  rank === 1
    ? LIST_TOP
    : LIST_TOP + ROW.firstHeight + ROW.gap + (rank - 2) * (ROW.height + ROW.gap);

export const rowHeight = (rank: number): number =>
  rank === 1 ? ROW.firstHeight : ROW.height;

/** 出典行帯 */
export const SOURCE_BAND = { left: SAFE.left, right: SAFE.right, top: 1612, height: 50 } as const;

/**
 * 表彰台五郎の常駐位置（日本海側）。
 * 値は正式アセット（1160x1220 の共通キャンバス。17-4b）に合わせたもので、
 * 17-4a で Fix した画面上の大きさ・立ち位置（ボディの「1」の高さ 51px・
 * 足元 y=718・「1」の中心 x=185）を維持する。キャンバスには軍配ポーズの
 * 腕を収める余白があるため left は負の値になる（透過部分が画面外へ出るだけ）。
 */
export const CHARACTER = { left: -6, top: 331, width: 381 } as const;
export const BUBBLE = { left: 40, top: 282, maxWidth: 620 } as const;
