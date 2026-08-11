import React from "react";
import { INSET_FRAME_PATH, PREFECTURES } from "./japanPaths";
import { MapPalette } from "./palette";

/**
 * 白抜き日本地図。県ごとの塗り分けと発光を props で制御する。
 * - litCode: ルーレットで一時的に光っている県
 * - flash: 停止フラッシュ中の県とその強度（1→0 で減衰）
 * - revealed: 確定済みの県 → 塗り色
 */
// 南西諸島インセット（沖縄県 + 鹿児島県のトカラ・奄美）は japanPaths.ts の生成時点で
// 移設済み（本土と同一投影のまま群として相似変換）。ここでは区切りの点線だけを描く。
export const JapanMap: React.FC<{
  litCode: number | null;
  flash: { code: number; intensity: number } | null;
  revealed: Record<number, string>;
  palette: MapPalette;
  /** 陸地に切り詰めた viewBox（layout.ts の MAP_VIEWBOX） */
  viewBox: string;
}> = ({ litCode, flash, revealed, palette, viewBox }) => {
  return (
    <svg viewBox={viewBox} width="100%" height="100%">
      <path
        d={INSET_FRAME_PATH}
        fill="none"
        stroke={palette.baseStroke}
        strokeWidth={1.5}
        strokeDasharray="7 7"
        opacity={0.8}
      />
      {PREFECTURES.map((p) => {
        const isFlash = flash?.code === p.code;
        const isLit = !isFlash && litCode === p.code;
        const revealedFill = revealed[p.code];

        let fill = palette.baseFill;
        let stroke = palette.baseStroke;
        let filter: string | undefined;

        if (revealedFill) {
          // 地図上に順位ラベルを置かない方針のため、確定県は塗り + 縁 + 淡い影で強調する
          // （小さい県・端の県でも「どこが確定したか」が塗りだけで分かるようにする）
          fill = revealedFill;
          stroke = palette.revealedStroke;
          filter = "drop-shadow(0 0 7px rgba(0,0,0,0.35))";
        }
        if (isLit) {
          fill = palette.litFill;
          stroke = palette.litStroke;
          filter = `drop-shadow(0 0 10px ${palette.litGlow})`;
        }
        if (isFlash && flash) {
          const t = flash.intensity;
          fill = palette.litFill;
          stroke = palette.flashStroke;
          filter = `drop-shadow(0 0 ${8 + 26 * t}px ${palette.flashGlow})`;
        }

        return (
          <path
            key={p.code}
            d={p.d}
            fill={fill}
            stroke={stroke}
            strokeWidth={isLit || isFlash ? 2 : revealedFill ? 1.8 : 1}
            strokeLinejoin="round"
            fillRule="nonzero"
            style={filter ? { filter } : undefined}
          />
        );
      })}
    </svg>
  );
};
