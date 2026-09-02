/**
 * 16 秒・30fps 固定のタイムライン。
 *
 * 不変条件（R-1 起票時のユーザー決定）: 尺 16 秒 / 3 カット / SE のタイミング
 * （tick 8.0 秒・chime 13.0 秒）は変えない。Remotion 化で変えるのは
 * カット内の動きと上部の余白だけ。
 *
 * ループ要件（R-1-1 で「平均再生時間 > 16 秒」= ループ視聴が実証された）:
 * 周期アニメーションの周期はすべて TOTAL_FRAMES (480) の約数とし、
 * 16 秒末尾の状態が 0 秒の状態に一致すること。約数でない周期を
 * LOOP_PERIODS に入れると、モジュール読み込み時に例外で落ちる。
 */

export const FPS = 30;
export const DURATION_SECONDS = 16;
export const TOTAL_FRAMES = FPS * DURATION_SECONDS; // 480

/** カット境界（フレーム）。SE の位置と一致させる */
export const INTRO_END = 8 * FPS; // 240 = 8.0s（tick SE）
export const COUNTDOWN_STEP = 1 * FPS; // 30 = 1.0s（5 → 1）
export const COUNTDOWN_COUNT = 5;
export const COUNTDOWN_END = INTRO_END + COUNTDOWN_STEP * COUNTDOWN_COUNT; // 390 = 13.0s（chime SE）
export const GUIDANCE_END = TOTAL_FRAMES; // 480 = 16.0s

/** 「考える」ビートの窓（3.0 秒 → カウントダウン開始） */
export const THINK_BEAT_IN = 3 * FPS; // 90
export const THINK_BEAT_FADE = 10;

/**
 * ループ継ぎ目の窓。ここで「誘導カットの状態 → 導入カットの状態」へ戻し、
 * frame 480 の見た目を frame 0 と一致させる。
 *
 * 表情と吹き出しの文言は**クロスフェードせずスナップで切り替える**
 * （SEAM_SWITCH）。別ポーズ・別文言の重ね合わせは二重露光に見えて
 * 不具合と区別がつかないため（試作 1 回目の frame 474 で確認）。
 * 消えるだけの要素（問題文・誘導の強調）は SEAM_FADE で淡く落とす。
 */
export const SEAM_START = TOTAL_FRAMES - 12; // 468 = 15.6s
export const SEAM_FADE = 6; // 468 → 474 で落としきる
export const SEAM_SWITCH = SEAM_START + SEAM_FADE; // 474 = 15.8s
/** 474〜479 は導入カットと同じ状態 = frame 0 と一致する */

/** 問題文の段階表示（1 行あたりの遅延と 1 行の立ち上がり） */
export const QUESTION_IN_START = 6;
export const QUESTION_LINE_DELAY = 9;
export const QUESTION_LINE_RISE = 14;

/** コーチ + 吹き出しの減衰ホップ（現行 ffmpeg 版と同じ 2 箇所・同じ諸元） */
export const HOP_AMPLITUDE = 150;
export const HOP_DURATION = 1 * FPS; // 30
export const HOP_FREQUENCY_HZ = 1.6;
export const HOP_DECAY_PER_SECOND = 3.0;
export const HOP_FRAMES = [INTRO_END, COUNTDOWN_END] as const;

/**
 * 周期アニメーションの周期（フレーム）。**すべて 480 の約数**。
 * 480 の約数: 1,2,3,4,5,6,8,10,12,15,16,20,24,30,32,40,48,60,80,96,120,160,240,480
 */
export const LOOP_PERIODS = {
  /** コーチの常時浮遊（上下） */
  coachFloat: 120,
  /** コーチの呼吸（微小スケール） */
  coachBreathe: 160,
  /** つかみ帯を渡る光沢 */
  bandSheen: 96,
  /** つかみ帯の微小スケール */
  bandBreathe: 120,
  /** 時間帯ピルのアクセントドットの脈動 */
  pillDot: 80,
  /** 見出し「問題」左のアクセントバーの伸縮 */
  headingBar: 160,
  /** イラストのゆっくりしたドリフト（拡大・平行移動） */
  illustrationDrift: 240,
  /** 背景の装飾オーブ */
  backgroundOrbs: 480,
  /** 吹き出しの微小な上下 */
  bubbleBob: 120,
  /** 「考え中」ドットの巡回 */
  thinkDots: 60,
  /** 誘導カットの矢印バウンド・縁の発光 */
  guidanceGlow: 96,
} as const;

export type LoopPeriodKey = keyof typeof LOOP_PERIODS;

/** 周期が 480 の約数であることをモジュール読み込み時に強制する */
const invalidPeriods = Object.entries(LOOP_PERIODS).filter(
  ([, period]) => TOTAL_FRAMES % period !== 0,
);
if (invalidPeriods.length > 0) {
  throw new Error(
    `周期アニメーションの周期は ${TOTAL_FRAMES} フレームの約数でなければならない: ` +
      invalidPeriods.map(([name, period]) => `${name}=${period}`).join(", "),
  );
}
