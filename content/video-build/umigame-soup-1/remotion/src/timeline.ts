/**
 * umigame-prebuilt のタイムライン（29 秒・870 フレーム・30fps・一本道）。
 *
 * 2026-09-04 のレビュー（第 1 稿の人間ゲート）で 20 秒 → 24 秒へ変更。理由: Polly Takumi 125% で
 * 問題文・ルール読み上げを削らずに収め、末尾に Jr. の締め（いいね・フォロー）を足すため。
 * 2026-10-17（セット改修 R-1-1）: 先頭に導入シーン 2.5 秒（固定コピー + hook を大きく）を足し、
 * ループの作り（末尾 = フレーム 0・周期を尺の約数にする・継ぎ目のビート）をやめて一本道にした。
 * 尺は中身で決めて 30 秒未満（29 秒）。導入シーンは R-1-2 の指摘で 2.5 秒 → 4.5 秒 → 5.0 秒に延ばした（切り替わりが早い・本編との間を空ける）。
 * 最後の 0.5 秒は尺を延ばさず Jr. の締め（5.5 → 5.0 秒）から回した。
 *
 * 不変条件:
 * - ビートは順序どおり・隙間なし・末尾が TOTAL_FRAMES に一致する
 * - ナレーションは予算（21 秒）を使い切っても尺の内側で終わる
 * - 吹き出しの切替はスナップ（クロスフェードは二重露光に見える。logic-training-1 R-1 で実測）
 *
 * ビート: 導入シーン 5.0 秒 → 出題 3 秒 → 3 往復 × 4 秒（質問 2 秒 → 質問 + 返答を並べて 2 秒）
 *       → 出題者の締め 4 秒 → Jr. の締め 5.0 秒。
 */

export const FPS = 30;
export const DURATION_SECONDS = 29;
export const TOTAL_FRAMES = FPS * DURATION_SECONDS; // 870

export const WIDTH = 1080;
export const HEIGHT = 1920;

/** 導入シーン（上に固定コピー・中央に hook を大きく・下にキャラ）の終わり */
export const OPENING_END = Math.round(5 * FPS); // 150
/** 導入シーンから本編へのクロスフェード */
export const OPENING_FADE_FRAMES = 8;
/** 導入シーンの見出しの読み上げの開始（スタンプが着地した後） */
export const OPENING_NARRATION_START = 6;
/** 導入シーンの自己紹介の吹き出しが出るフレーム（カメロック → Jr. の順に後から入る。導入を 4.5 秒に延ばした際に
 * 1 秒遅らせ、間隔を 16 → 26 フレームに広げた） */
export const OPENING_MASTER_BUBBLE_IN = 52;
export const OPENING_JR_BUBBLE_IN = 78;
/** 導入シーンの見出しと「質問」タグの光沢スイープの周期（導入中に 2 回通る） */
export const OPENING_SHEEN_PERIOD = 36;
/** 「真相」の小さな跳ねの周期 */
export const OPENING_HOP_PERIOD = 24;
/** 出題（「質問してみて！」の吹き出し）の終わり */
export const INTRO_END = OPENING_END + 3 * FPS; // 240
export const ROUND_FRAMES = 4 * FPS; // 120
export const QUESTION_FRAMES = 2 * FPS; // 60
export const ROUNDS = 3;
/** 出題者の締め（「何度でも答えるよ」）の開始 */
export const MASTER_OUTRO_START = INTRO_END + ROUND_FRAMES * ROUNDS; // 600
/** Jr. の締め（「いいね・フォロー」）の開始 */
export const JR_OUTRO_START = MASTER_OUTRO_START + 4 * FPS; // 720

/** 吹き出しのポップイン（スナップ表示後の軽い伸縮）に使うフレーム数 */
export const BUBBLE_POP_FRAMES = 8;

/** 吹き出し切替時の小さな跳ね（logic-training-1 の 150px を 30px に抑えた。ユーザー指示） */
export const HOP_AMPLITUDE_PX = 30;
export const HOP_FREQUENCY_HZ = 1.8;
export const HOP_DECAY = 4.5;
export const HOP_SECONDS = 0.8;

/** 周期アニメーション（一本道化で「尺の約数」の制約は外した。周期は 24 秒版のまま） */
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
  backgroundBreathe: TOTAL_FRAMES,
} as const;

/** ナレーションの開始フレーム（導入シーンの後 0.5 秒）と cue 間の間（1.2 秒。ユーザー指示） */
export const NARRATION_START = OPENING_END + Math.round(0.5 * FPS); // 165
export const NARRATION_GAP = Math.round(1.2 * FPS); // 36
/** ナレーションの予算（問題文 + 間 + ルール文）。21 秒は 24 秒版から据え置き */
export const NARRATION_BUDGET_FRAMES = 21 * FPS; // 630
/** ナレーションはこのフレームまでに終わること（尺の内側） */
export const NARRATION_DEADLINE = TOTAL_FRAMES; // 870

export type Beat =
  | { kind: "opening"; from: number; to: number }
  | { kind: "intro"; from: number; to: number }
  | { kind: "question"; round: number; from: number; to: number }
  | { kind: "answer"; round: number; from: number; to: number }
  | { kind: "master_outro"; from: number; to: number }
  | { kind: "jr_outro"; from: number; to: number };

/** ビートの一覧（順序どおり・隙間なし・末尾が TOTAL_FRAMES） */
export const BEATS: readonly Beat[] = (() => {
  const beats: Beat[] = [
    { kind: "opening", from: 0, to: OPENING_END },
    { kind: "intro", from: OPENING_END, to: INTRO_END },
  ];
  for (let round = 0; round < ROUNDS; round += 1) {
    const start = INTRO_END + round * ROUND_FRAMES;
    beats.push({ kind: "question", round, from: start, to: start + QUESTION_FRAMES });
    beats.push({ kind: "answer", round, from: start + QUESTION_FRAMES, to: start + ROUND_FRAMES });
  }
  beats.push({ kind: "master_outro", from: MASTER_OUTRO_START, to: JR_OUTRO_START });
  beats.push({ kind: "jr_outro", from: JR_OUTRO_START, to: TOTAL_FRAMES });
  return beats;
})();

/** 吹き出しが新しく出るフレーム（SE と跳ねの位置。導入シーンは別に持つ。出題の「質問してみて！」は R-1-2 の指摘で追加） */
export const BUBBLE_SWITCH_FRAMES: readonly number[] = BEATS.filter(
  (beat) => beat.kind !== "opening",
).map((beat) => beat.from);

/** キャラが小さく跳ねるフレーム（本編の吹き出しの切替 + 導入シーンの自己紹介の吹き出し） */
export const HOP_FRAMES: readonly number[] = [
  OPENING_MASTER_BUBBLE_IN,
  OPENING_JR_BUBBLE_IN,
  ...BUBBLE_SWITCH_FRAMES,
];

export const beatAt = (frame: number): Beat => {
  const found = BEATS.find((beat) => frame >= beat.from && frame < beat.to);
  return found ?? BEATS[BEATS.length - 1];
};

/** 周期 period の正弦（-1..1） */
export const loopSin = (frame: number, period: number, phase = 0): number =>
  Math.sin(((frame / period) + phase) * Math.PI * 2);

/** 周期 period の位相（0..1） */
export const loopPhase = (frame: number, period: number): number => (frame % period) / period;

/** 直近の吹き出し切替からの減衰する跳ね（px。上向きが正） */
export const hopLift = (frame: number): number => {
  let last = -1;
  for (const f of HOP_FRAMES) {
    if (f <= frame) last = f;
  }
  if (last < 0) return 0;
  const t = (frame - last) / FPS;
  if (t >= HOP_SECONDS) return 0;
  return HOP_AMPLITUDE_PX * Math.abs(Math.sin(t * HOP_FREQUENCY_HZ * Math.PI * 2)) * Math.exp(-HOP_DECAY * t);
};

// モジュール読み込み時の不変条件チェック
BEATS.forEach((beat, index) => {
  const expectedFrom = index === 0 ? 0 : BEATS[index - 1].to;
  if (beat.from !== expectedFrom) {
    throw new Error(`BEATS[${index}] の開始 ${beat.from} が前のビートの終端 ${expectedFrom} と一致しません`);
  }
  if (beat.to <= beat.from) {
    throw new Error(`BEATS[${index}] の長さが 0 以下です`);
  }
});
if (BEATS[BEATS.length - 1].to !== TOTAL_FRAMES) {
  throw new Error("BEATS の終端が TOTAL_FRAMES と一致しません");
}
if (NARRATION_START + NARRATION_BUDGET_FRAMES > NARRATION_DEADLINE) {
  throw new Error("ナレーションの予算が尺に収まりません");
}
if (OPENING_JR_BUBBLE_IN >= OPENING_END) {
  throw new Error("導入シーンの吹き出しが導入の終わりより後に出ます");
}
if (TOTAL_FRAMES >= 30 * FPS) {
  throw new Error("尺は 30 秒未満にします");
}
