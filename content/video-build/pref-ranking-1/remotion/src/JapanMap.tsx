import React from "react";
import { INSET_FRAME_PATH, PREFECTURES } from "./japanPaths";
import { insetFocusTransform } from "./layout";
import { MapPalette } from "./palette";

/**
 * 白抜き日本地図。県ごとの塗り分けと発光を props で制御する。
 * - litCode: ルーレットで一時的に光っている県
 * - litIntensity: その発光の強さ（0〜1。予熱スピンを淡く出すため。R-1-1）
 * - flash: 停止フラッシュ中の県とその強度（1→0 で減衰）
 * - revealed: 確定済みの県 → 塗り色
 * - insetFocus: 南西諸島インセットの拡大（0 = 通常 / 1 = 拡大パネル）
 */

// 南西諸島インセット（沖縄県 + 鹿児島県のトカラ・奄美）は japanPaths.ts の生成時点で
// 移設済み（本土と同一投影のまま群として相似変換）。ここでは区切りの点線と、
// 1 位がインセットの県のときの一時的な拡大パネルを扱う。

// 拡大の基点・倍率は layout.ts の MAP_INSET_FOCUS が正（1 位の県名ラベルの起点も
// そこから算出するため、ジオメトリ定数として一箇所に置く）。

export const JapanMap: React.FC<{
  litCode: number | null;
  /**
   * ルーレットの発光強度（0〜1。既定 1 = 本番スピンの現行値）。
   * 塗りの不透明度と光の滲みだけを弱め、点滅の速さとは独立に扱う
   * （R-1-1「速さと眩しさの分離」。予熱区間は淡く出して 5.00 秒に変化点を残す）。
   */
  litIntensity?: number;
  flash: { code: number; intensity: number } | null;
  revealed: Record<number, string>;
  palette: MapPalette;
  /** 陸地に切り詰めた viewBox（layout.ts の MAP_VIEWBOX） */
  viewBox: string;
  /** 南西諸島インセットの拡大（0〜1） */
  insetFocus?: number;
}> = ({ litCode, litIntensity = 1, flash, revealed, palette, viewBox, insetFocus = 0 }) => {
  const shape = (p: (typeof PREFECTURES)[number], part: "d" | "dInset") => {
    const data = p[part];
    if (!data) return null;

    const isFlash = flash?.code === p.code;
    const isLit = !isFlash && litCode === p.code;
    const revealedFill = revealed[p.code];

    let fill = palette.baseFill;
    let stroke = palette.baseStroke;
    let fillOpacity = 1;
    let filter: string | undefined;

    if (revealedFill) {
      // 地図上に順位ラベルを置かない方針のため、確定県は塗り + 縁 + 淡い影で強調する
      // （小さい県・端の県でも「どこが確定したか」が塗りだけで分かるようにする）
      fill = revealedFill;
      stroke = palette.revealedStroke;
      filter = "drop-shadow(0 0 7px rgba(0,0,0,0.35))";
    }
    if (isLit) {
      // 強度 1 が本番スピンの現行値。予熱区間（強度 < 1）は塗りを透かし、光の滲みも
      // 比例して縮めることで、点滅の速さは同じまま眩しさだけを落とす。
      // 縁取りは強度に依らず残す（淡くしても「どの県が光ったか」が読めるようにするため）。
      const lit = Math.min(1, Math.max(0, litIntensity));
      fill = palette.litFill;
      stroke = palette.litStroke;
      fillOpacity = lit;
      filter = `drop-shadow(0 0 ${10 * lit}px ${palette.litGlow})`;
    }
    if (isFlash && flash) {
      const t = flash.intensity;
      fill = palette.litFill;
      stroke = palette.flashStroke;
      filter = `drop-shadow(0 0 ${8 + 26 * t}px ${palette.flashGlow})`;
    }

    return (
      <path
        key={`${p.code}-${part}`}
        d={data}
        fill={fill}
        fillOpacity={fillOpacity}
        stroke={stroke}
        strokeWidth={isLit || isFlash ? 2 : revealedFill ? 1.8 : 1}
        strokeLinejoin="round"
        fillRule="nonzero"
        style={filter ? { filter } : undefined}
      />
    );
  };

  return (
    <svg viewBox={viewBox} width="100%" height="100%">
      <path
        d={INSET_FRAME_PATH}
        fill="none"
        stroke={palette.baseStroke}
        strokeWidth={1.5}
        strokeDasharray="7 7"
        opacity={0.8 * (1 - insetFocus)}
      />
      {PREFECTURES.map((p) => shape(p, "d"))}

      {/* 南西諸島インセット。1 位が沖縄のときは島の群だけがその場で大きくなる */}
      <g transform={insetFocusTransform(insetFocus)}>
        {PREFECTURES.map((p) => shape(p, "dInset"))}
      </g>
    </svg>
  );
};
