/**
 * モーションのヘルパー。
 *
 * 周期モーションは必ず `LOOP_PERIODS` の周期を使い、`loopSin` / `loopPhase`
 * 経由で位相を取る。周期は 480 の約数に強制されている（timeline.ts）ため、
 * frame 480 の値は frame 0 の値と厳密に一致する = ループ継ぎ目で位相が飛ばない。
 */

import {
  FPS,
  HOP_AMPLITUDE,
  HOP_DECAY_PER_SECOND,
  HOP_DURATION,
  HOP_FRAMES,
  HOP_FREQUENCY_HZ,
  SEAM_FADE,
  SEAM_START,
} from "./timeline";

/** 周期 period フレームの正弦（-1..1）。frame=0 と frame=period で同値 */
export const loopSin = (frame: number, period: number): number =>
  Math.sin((2 * Math.PI * frame) / period);

/** 周期 period フレームの余弦（-1..1） */
export const loopCos = (frame: number, period: number): number =>
  Math.cos((2 * Math.PI * frame) / period);

/** 周期内の位置（0..1） */
export const loopPhase = (frame: number, period: number): number =>
  (((frame % period) + period) % period) / period;

/** 0..1 の三角波（0 → 1 → 0）。周期の半分で折り返す */
export const loopTriangle = (frame: number, period: number): number =>
  (1 - loopCos(frame, period)) / 2;

/** 線形補間（remotion の interpolate を使わない軽い場面用） */
export const lerp = (from: number, to: number, t: number): number =>
  from + (to - from) * t;

export const clamp01 = (value: number): number =>
  value < 0 ? 0 : value > 1 ? 1 : value;

/** ease-out cubic */
export const easeOut = (t: number): number => 1 - Math.pow(1 - clamp01(t), 3);

/** ease-in-out cubic */
export const easeInOut = (t: number): number =>
  clamp01(t) < 0.5
    ? 4 * Math.pow(clamp01(t), 3)
    : 1 - Math.pow(-2 * clamp01(t) + 2, 3) / 2;

/**
 * 現行 ffmpeg 版と同じ減衰ホップ（コーチ + 吹き出しの持ち上げ量 px。
 * 戻り値は「上に持ち上げる量」で、CSS では translateY(-value) にする）。
 * 発火は 8.0 秒（tick）と 13.0 秒（chime）の 2 箇所のみで、1 秒で収束する
 * = 16 秒末尾には残らない。
 */
export const hopLift = (frame: number): number => {
  let lift = 0;
  for (const start of HOP_FRAMES) {
    const local = frame - start;
    if (local < 0 || local > HOP_DURATION) continue;
    const seconds = local / FPS;
    lift +=
      HOP_AMPLITUDE *
      Math.exp(-HOP_DECAY_PER_SECOND * seconds) *
      Math.abs(Math.sin(2 * Math.PI * HOP_FREQUENCY_HZ * seconds));
  }
  return lift;
};

/**
 * ループ継ぎ目の減衰（0..1）。誘導カット固有の要素をここで落としきり、
 * frame 480 の見た目を frame 0 に一致させる（R-1-1 でループ視聴が
 * 実証されたため必須要件）。
 */
export const seamFade = (frame: number): number =>
  easeInOut(clamp01((frame - SEAM_START) / SEAM_FADE));
