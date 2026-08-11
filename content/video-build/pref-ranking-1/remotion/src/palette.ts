// 地図の塗り分けトークンの型。版面全体のトークンは theme.ts が正（17-4a で分離）。

export type MapPalette = {
  baseFill: string;
  baseStroke: string;
  revealedStroke: string;
  /** 順位 → 確定県の塗り色 */
  revealedFill: Record<number, string>;
  litFill: string;
  litStroke: string;
  litGlow: string;
  flashStroke: string;
  flashGlow: string;
};
