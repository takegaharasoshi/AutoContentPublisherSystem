/**
 * umigame-prebuilt PoC のタイムライン（24 秒・720 フレーム・30fps・ループ前提）。
 *
 * 2026-09-04 のレビュー（第 1 稿の人間ゲート）で 20 秒 → 24 秒へ変更。理由: Polly Takumi 125% で
 * 問題文・ルール読み上げを削らずに収め、末尾に Jr. の締め（いいね・フォロー）を足すため。
 *
 * 不変条件（logic-training-1 の timeline.ts を踏襲）:
 * - 末尾（SEAM_START 以降）は導入と同じ状態へ戻し、フレーム 720 とフレーム 0 が一致する
 * - 周期アニメーションの周期は TOTAL_FRAMES の約数
 * - 吹き出しの切替はスナップ（クロスフェードは二重露光に見える。R-1 で実測）
 *
 * ビート: 導入 3 秒 → 3 往復 × 4 秒（質問 2 秒 → 質問 + 返答を並べて 2 秒）→ 出題者の締め 4 秒
 *       → Jr. の締め 4.6 秒 → 継ぎ目 0.4 秒。
 */

export const FPS = 30;
export const DURATION_SECONDS = 24;
export const TOTAL_FRAMES = FPS * DURATION_SECONDS; // 720

export const WIDTH = 1080;
export const HEIGHT = 1920;

export const INTRO_END = 3 * FPS; // 90
export const ROUND_FRAMES = 4 * FPS; // 120
export const QUESTION_FRAMES = 2 * FPS; // 60
export const ROUNDS = 3;
/** 出題者の締め（「何度でも答えるよ」）の開始 */
export const MASTER_OUTRO_START = INTRO_END + ROUND_FRAMES * ROUNDS; // 450
/** Jr. の締め（「いいね・フォロー」）の開始 */
export const JR_OUTRO_START = MASTER_OUTRO_START + 4 * FPS; // 570
/** 継ぎ目: ここから末尾までは導入と同じ状態（フレーム 0 と一致させる） */
export const SEAM_START = TOTAL_FRAMES - Math.round(0.4 * FPS); // 708

/** 吹き出しのポップイン（スナップ表示後の軽い伸縮）に使うフレーム数 */
export const BUBBLE_POP_FRAMES = 8;

/** 吹き出し切替時の小さな跳ね（logic-training-1 の 150px を 30px に抑えた。ユーザー指示） */
export const HOP_AMPLITUDE_PX = 30;
export const HOP_FREQUENCY_HZ = 1.8;
export const HOP_DECAY = 4.5;
export const HOP_SECONDS = 0.8;

/** 周期アニメーション（すべて TOTAL_FRAMES の約数であること） */
export const LOOP_PERIODS = {
  /** つかみ帯の光沢スイープ */
  hookSheen: 120,
  /** つかみ帯のごく小さな呼吸 */
  hookBreathe: 144,
  /** 「問題」見出しのアクセントバー伸縮 */
  headingBar: 144,
  /** 出題者の浮遊 */
  masterFloat: 120,
  /** 出題者の呼吸（拡縮） */
  masterBreathe: 180,
  /** Jr. の浮遊 */
  jrFloat: 90,
  /** 締めの吹き出しのグロー脈動 */
  outroGlow: 90,
  /** 名札のアクセント点の脈動 */
  tagDot: 80,
  /** 背景のゆっくりしたズーム呼吸 */
  backgroundBreathe: 720,
} as const;

/** ナレーションの開始フレーム（0.5 秒）と cue 間の間（1.2 秒。ユーザー指示） */
export const NARRATION_START = Math.round(0.5 * FPS); // 15
export const NARRATION_GAP = Math.round(1.2 * FPS); // 36
/** ナレーションはこのフレームまでに終わること（継ぎ目に掛からない範囲） */
export const NARRATION_DEADLINE = SEAM_START; // 708

export type Beat =
  | { kind: "intro"; from: number; to: number }
  | { kind: "question"; round: number; from: number; to: number }
  | { kind: "answer"; round: number; from: number; to: number }
  | { kind: "master_outro"; from: number; to: number }
  | { kind: "jr_outro"; from: number; to: number }
  | { kind: "seam"; from: number; to: number };

/** ビートの一覧（順序どおり・隙間なし・末尾が TOTAL_FRAMES） */
export const BEATS: readonly Beat[] = (() => {
  const beats: Beat[] = [{ kind: "intro", from: 0, to: INTRO_END }];
  for (let round = 0; round < ROUNDS; round += 1) {
    const start = INTRO_END + round * ROUND_FRAMES;
    beats.push({ kind: "question", round, from: start, to: start + QUESTION_FRAMES });
    beats.push({ kind: "answer", round, from: start + QUESTION_FRAMES, to: start + ROUND_FRAMES });
  }
  beats.push({ kind: "master_outro", from: MASTER_OUTRO_START, to: JR_OUTRO_START });
  beats.push({ kind: "jr_outro", from: JR_OUTRO_START, to: SEAM_START });
  beats.push({ kind: "seam", from: SEAM_START, to: TOTAL_FRAMES });
  return beats;
})();

/** 吹き出しが新しく出るフレーム（SE と跳ねの位置。導入・継ぎ目は鳴らさない） */
export const BUBBLE_SWITCH_FRAMES: readonly number[] = BEATS.filter(
  (beat) => beat.kind !== "intro" && beat.kind !== "seam",
).map((beat) => beat.from);

export const beatAt = (frame: number): Beat => {
  const found = BEATS.find((beat) => frame >= beat.from && frame < beat.to);
  return found ?? BEATS[BEATS.length - 1];
};

/** 周期 period でフレーム 0 と TOTAL_FRAMES が一致する正弦（-1..1） */
export const loopSin = (frame: number, period: number, phase = 0): number =>
  Math.sin(((frame / period) + phase) * Math.PI * 2);

/** 周期 period の位相（0..1） */
export const loopPhase = (frame: number, period: number): number => (frame % period) / period;

/** 直近の吹き出し切替からの減衰する跳ね（px。上向きが正）。フレーム 0 と 720 では 0 */
export const hopLift = (frame: number): number => {
  let last = -1;
  for (const f of BUBBLE_SWITCH_FRAMES) {
    if (f <= frame) last = f;
  }
  if (last < 0) return 0;
  const t = (frame - last) / FPS;
  if (t >= HOP_SECONDS) return 0;
  return HOP_AMPLITUDE_PX * Math.abs(Math.sin(t * HOP_FREQUENCY_HZ * Math.PI * 2)) * Math.exp(-HOP_DECAY * t);
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
if (Math.round(HOP_SECONDS * FPS) > TOTAL_FRAMES - JR_OUTRO_START) {
  throw new Error("跳ねが継ぎ目をまたぎます");
}
