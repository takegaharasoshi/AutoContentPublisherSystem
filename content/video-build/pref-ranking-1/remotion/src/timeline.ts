// 2 尺のタイムライン定数（方式設計書 ranking-prebuilt.html セクション 8.2 / 8.3）。
// 17-4a のデザインモックは 20 秒版のみを使う（30 秒版は本組み 17-4c で追加）。

export type Duration = "20s" | "30s";

export type RoundTiming = {
  /** スピン開始フレーム */
  start: number;
  /** スピン長（フレーム） */
  spin: number;
  /** 停止フラッシュ（= 確定）フレーム */
  stop: number;
  /** 地図上の県名ラベルが行へ飛び始めるフレーム */
  flyStart: number;
  /** 飛翔の長さ */
  flyDur: number;
  /** 順位行が現れるフレーム */
  rowAt: number;
};

export type Timeline = {
  fps: number;
  total: number;
  /** 煽りシーン（teaser）の開始 */
  teaserAt: number;
  /** 締めシーンの開始 */
  closingAt: number;
  rounds: Record<number, RoundTiming>;
};

const round = (start: number, spin: number, flyDelay: number, flyDur: number): RoundTiming => {
  const stop = start + spin;
  const flyStart = stop + flyDelay;
  return { start, spin, stop, flyStart, flyDur, rowAt: flyStart + flyDur - 2 };
};

/**
 * 20 秒版 = 600f。
 * オープニング 2.5s → 煽り 2.0s → 5〜2 位 各 2.0s（スピン 1.0s + 停止 1.0s）
 * → 1 位 4.5s（タメ 2.5s + 発表 2.0s）→ 締め 3.0s
 */
export const TIMELINE_20S: Timeline = {
  fps: 30,
  total: 600,
  teaserAt: 75,
  closingAt: 510,
  rounds: {
    5: round(135, 30, 8, 16),
    4: round(195, 30, 8, 16),
    3: round(255, 30, 8, 16),
    2: round(315, 30, 8, 16),
    // 1 位は発表の余韻（バースト）を挟んでから行へ落とす
    1: round(375, 75, 42, 18),
  },
};

export const TIMELINES: Record<Duration, Timeline> = {
  "20s": TIMELINE_20S,
  "30s": TIMELINE_20S, // 17-4c で差し替え
};
