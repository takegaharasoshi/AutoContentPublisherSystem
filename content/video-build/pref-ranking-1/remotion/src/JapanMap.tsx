import React from "react";
import {
  INNER_TRANSFORM,
  OUTER_TRANSFORM,
  PREFECTURES,
} from "./japanPaths";
import { MapPalette } from "./palette";

/**
 * 白抜き日本地図。県ごとの塗り分けと発光を props で制御する。
 * - litCode: ルーレットで一時的に光っている県
 * - flash: 停止フラッシュ中の県とその強度（1→0 で減衰）
 * - revealed: 確定済みの県 → 塗り色
 */
// 南西諸島インセット: 元データは日本海側（左上）に沖縄・奄美が対角チェーンで配置されていた。
// キャラ常駐スペース確保のため、元の相対配置・縮尺比を保ったまま全体を 0.75 倍で
// 地図右下（ランキング行の少し上の太平洋上）へ移設し、区切り線を添える（17-2 巡 1）。
// 奄美・トカラ（鹿児島の飛び地）側は japanPaths.ts 内のネスト transform で同じ写像を適用済み。
const OKINAWA_INSET_TRANSFORM =
  "translate(695.000000, 822.000000) scale(0.75)";

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
      <g transform={OUTER_TRANSFORM}>
        <g transform={INNER_TRANSFORM}>
          <path
            d="M686,960 L686,680 L1000,680"
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
              <g
                key={p.code}
                transform={
                  p.code === 47 ? OKINAWA_INSET_TRANSFORM : p.transform
                }
                fill={fill}
                stroke={stroke}
                strokeWidth={isLit || isFlash ? 2 : revealedFill ? 1.8 : 1}
                strokeLinejoin="round"
                fillRule="nonzero"
                style={filter ? { filter } : undefined}
                dangerouslySetInnerHTML={{ __html: p.shapes }}
              />
            );
          })}

        </g>
      </g>
    </svg>
  );
};
