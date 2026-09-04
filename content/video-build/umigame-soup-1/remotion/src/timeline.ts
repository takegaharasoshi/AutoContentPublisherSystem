/**
 * umigame-prebuilt PoC のタイムライン（20 秒・600 フレーム・30fps・ループ前提）。
 *
 * 不変条件（logic-training-1 の timeline.ts を踏襲）:
 * - 末尾（SEAM_START 以降）は導入と同じ状態へ戻し、フレーム 600 とフレーム 0 が一致する
 * - 周期アニメーションの周期は TOTAL_FRAMES の約数
 * - 吹き出しの切替はスナップ（クロスフェードは二重露光に見える。R-1 で実測）
 *
 * ビート（21-1 決定の叩き台）: 導入 3 秒 → 3 往復 × 4 秒（質問 2 秒 → 返答 2 秒）→ 締め 4.6 秒 → 継ぎ目 0.4 秒。
 */

export const FPS = 30;
export const DURATION_SECONDS = 20;
export const TOTAL_FRAMES = FPS * DURATION_SECONDS; // 600

export const WIDTH = 1080;
export const HEIGHT = 1920;

/** 導入（出題者「質問してみて！」）の終端 */
export const INTRO_END = 3 * FPS; // 90
/** 1 往復の長さ（質問 2 秒 + 返答 2 秒） */
export const ROUND_FRAMES = 4 * FPS; // 120
export const QUESTION_FRAMES = 2 * FPS; // 60
export const ROUNDS = 3;
/** 締め（出題者の呼びかけ）の開始 */
export const OUTRO_START = INTRO_END + ROUND_FRAMES * ROUNDS; // 450
/** 継ぎ目: ここから末尾までは導入と同じ状態（フレーム 0 と一致させる） */
export const SEAM_START = TOTAL_FRAMES - Math.round(0.4 * FPS); // 588

/** 吹き出しのポップイン（スナップ表示後の軽い伸縮）に使うフレーム数 */
export const BUBBLE_POP_FRAMES = 8;

/** 周期アニメーション（すべて TOTAL_FRAMES の約数であること） */
export const LOOP_PERIODS = {
  /** 出題者の上下のゆれ */
  masterBob: 100,
  /** 質問者の上下のゆれ */
  assistantBob: 120,
  /** 背景のゆっくりした横ドリフト */
  backgroundDrift: 600,
} as const;

/** ナレーションの開始フレーム（0.5 秒）と cue 間の間 */
export const NARRATION_START = Math.round(0.5 * FPS); // 15
export const NARRATION_GAP = Math.round(0.5 * FPS); // 15
/** ナレーションはこのフレームまでに終わること（締めの呼びかけに重ならない範囲） */
export const NARRATION_DEADLINE = OUTRO_START + 2 * FPS; // 510

export type Beat =
  | { kind: "intro"; from: number; to: number }
  | { kind: "question"; round: number; from: number; to: number }
  | { kind: "answer"; round: number; from: number; to: number }
  | { kind: "outro"; from: number; to: number }
  | { kind: "seam"; from: number; to: number };

/** ビートの一覧（順序どおり・隙間なし・末尾が TOTAL_FRAMES） */
export const BEATS: readonly Beat[] = (() => {
  const beats: Beat[] = [{ kind: "intro", from: 0, to: INTRO_END }];
  for (let round = 0; round < ROUNDS; round += 1) {
    const start = INTRO_END + round * ROUND_FRAMES;
    beats.push({ kind: "question", round, from: start, to: start + QUESTION_FRAMES });
    beats.push({ kind: "answer", round, from: start + QUESTION_FRAMES, to: start + ROUND_FRAMES });
  }
  beats.push({ kind: "outro", from: OUTRO_START, to: SEAM_START });
  beats.push({ kind: "seam", from: SEAM_START, to: TOTAL_FRAMES });
  return beats;
})();

/** 吹き出しが新しく出るフレーム（SE を鳴らす位置。導入・継ぎ目は鳴らさない） */
export const BUBBLE_SE_FRAMES: readonly number[] = BEATS.filter(
  (beat) => beat.kind === "question" || beat.kind === "answer" || beat.kind === "outro",
).map((beat) => beat.from);

export const beatAt = (frame: number): Beat => {
  const found = BEATS.find((beat) => frame >= beat.from && frame < beat.to);
  return found ?? BEATS[BEATS.length - 1];
};

// モジュール読み込み時の不変条件チェック
for (const [name, period] of Object.entries(LOOP_PERIODS)) {
  if (TOTAL_FRAMES % period !== 0) {
    throw new Error(`LOOP_PERIODS.${name}=${period} は TOTAL_FRAMES=${TOTAL_FRAMES} の約数ではありません`);
  }
}
BEATS.forEach((beat, index) => {
  const expectedFrom = index === 0 ? 0 : BEATS[index - 1].to;
  if (beat.from !== expectedFrom) {
    throw new Error(`BEATS[${index}] の開始 ${beat.from} が前のビートの終端 ${expectedFrom} と一致しません`);
  }
});
if (BEATS[BEATS.length - 1].to !== TOTAL_FRAMES) {
  throw new Error("BEATS の終端が TOTAL_FRAMES と一致しません");
}
