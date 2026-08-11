// 版面のカラートークン。17-4a で Fix した「生成り地 × 淡墨茶 × 金」。
// 17-2 の wamodernA（生成り × 藍 × 朱 × 金）から、もう一色を藍 → 淡墨茶へ差し替えたもの
// （藍は生成りと合わないというユーザー判断。えんじ・松葉・墨茶・香色との比較を経て確定）。
// セット別設計書 pref-ranking-1.html セクション 8 のトークン表はこの値を正とする。

/** 地色・アクセント（生成りと金は 17-2 から据え置き） */
export const TOKENS = {
  cream: "#F6F0E1",
  creamDeep: "#EFE4CC",
  gold: "#D9A62E",
  goldDeep: "#C08618",
  goldLight: "#F4D77D",
  /** 淡墨茶: 帯・順位バッジの地（最も濃い） */
  sumiDeep: "#544A3C",
  /** 淡墨茶: 本文・輪郭 */
  sumiBase: "#63594A",
  /** 朱: 強調語・吹き出しの文字 */
  vermilion: "#B23A31",
} as const;

const RGB: [number, number, number] = [84, 74, 60];
const rgba = (alpha: number): string => `rgba(${RGB[0]},${RGB[1]},${RGB[2]},${alpha})`;

/** 確定県の塗り（1 位のみ金・2〜5 位は淡墨茶の階調） */
export const MAP_REVEALED_FILL: Record<number, string> = {
  1: TOKENS.gold,
  2: "#9C8F79",
  3: "#8C806C",
  4: "#7C7160",
  5: "#6C6254",
};

export const THEME = {
  pageTop: TOKENS.cream,
  pageBottom: TOKENS.creamDeep,
  // 減光 3 層（上帯・中央・下帯）。中央は 30% で背景イラストを活かす
  bgOverlay:
    "linear-gradient(180deg, rgba(246,240,225,0.90) 0%, rgba(246,240,225,0.80) 11%, rgba(246,240,225,0.30) 30%, rgba(246,240,225,0.30) 52%, rgba(243,236,218,0.86) 62%, rgba(239,228,204,0.92) 100%)",
  noiseOpacity: 0.1,
  vignette: `radial-gradient(120% 78% at 50% 42%, rgba(0,0,0,0) 52%, ${rgba(0.16)} 100%)`,
  bandBg: `linear-gradient(180deg, ${TOKENS.sumiBase} 0%, ${TOKENS.sumiDeep} 100%)`,
  bandText: TOKENS.cream,
  bandEyebrow: TOKENS.goldLight,
  bandPattern: "rgba(246,240,225,0.07)",
  rowBg: "linear-gradient(180deg, rgba(255,253,245,0.97) 0%, rgba(244,236,219,0.97) 100%)",
  rowText: TOKENS.sumiDeep,
  rowBorder: rgba(0.22),
  rowShadow: `0 10px 22px ${rgba(0.16)}`,
  badgeBg: TOKENS.sumiDeep,
  badgeText: TOKENS.cream,
  sourceBg: rgba(0.8),
  sourceText: "rgba(246,240,225,0.94)",
  bubbleBg: "#FFFDF5",
  bubbleBorder: TOKENS.sumiDeep,
  bubbleText: TOKENS.vermilion,
  plateBg: "rgba(255,253,245,0.86)",
  plateLabel: TOKENS.vermilion,
  plateValue: TOKENS.sumiDeep,
  mapBaseFill: rgba(0.14),
  mapBaseStroke: rgba(0.72),
  mapRevealedStroke: rgba(0.78),
  mapRevealedFill: MAP_REVEALED_FILL,
  flyText: TOKENS.sumiDeep,
  flyOutline: "#FFFDF5",
  /** 金の面の上に載せる文字色 */
  onGold: TOKENS.sumiDeep,
} as const;

export type Theme = typeof THEME;
