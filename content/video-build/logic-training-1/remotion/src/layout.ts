/**
 * 版面（レイアウト）定数と、それらから導かれる矩形。
 *
 * R-1 の版面変更（ユーザー決定）: 上部（時間帯ピル・つかみ帯・見出し・問題文）は
 * 左右対称の余白でカード幅を使い切り、Instagram UI の右 12% 予約は
 * 下部（イラスト・コーチ・吹き出し）だけに残す。つまりセーフエリアを
 * 「高さに依存する 2 ゾーン」に変える。現行版は右 12% を全高で予約していたため、
 * 上部の本文が実効 797px 幅に閉じ込められていた（新: 902px）。
 */

/**
 * R-2 の版面変更（ユーザー決定 2026-09-19）: 配分順序を「問題文優先」から
 * **イラスト優先**へ入れ替える。イラストの箱に ILLUSTRATION_GUARANTEED_HEIGHT を
 * 先に確保し、残った高さに問題文を収める（上限 68px 据え置き・下限 44px・行送り 1.4）。
 * 原資はつかみ帯 64 → 52px・見出し 92 → 72px・見出しから問題文までの間隔 150 → 115px
 * の縮小で作る。問題の長さで問題文のサイズが変わることを許容する。
 */

import { LINE_END_PROHIBITED, LINE_START_PROHIBITED } from "./textUtils";

export const WIDTH = 1080;
export const HEIGHT = 1920;

export const CARD_MARGIN_X = 25;
export const CARD_MARGIN_Y = 41;
export const CARD_RADIUS = 42;

/** カード矩形（出力枠の一定インセット。現行版と同値） */
export const CARD = {
  left: CARD_MARGIN_X,
  top: CARD_MARGIN_Y,
  right: WIDTH - CARD_MARGIN_X,
  bottom: HEIGHT - CARD_MARGIN_Y,
} as const;

/** Instagram UI の予約域（現行版と同じ比率） */
export const IG_RIGHT_RESERVED_RATIO = 0.12;
export const IG_BOTTOM_RESERVED_RATIO = 0.15;
export const IG_RIGHT = Math.floor(WIDTH * (1 - IG_RIGHT_RESERVED_RATIO)); // 950
export const IG_BOTTOM = Math.floor(HEIGHT * (1 - IG_BOTTOM_RESERVED_RATIO)); // 1632

export const PADDING = 64;

/** 上部ゾーン: 左右対称。右 12% 予約を適用しない */
export const TOP_ZONE = {
  left: CARD.left + PADDING,
  right: CARD.right - PADDING,
} as const;

/** 下部ゾーン: 右 12% 予約あり（イラスト・コーチ・吹き出し） */
export const BOTTOM_ZONE = {
  left: CARD.left + PADDING,
  right: Math.min(CARD.right, IG_RIGHT) - PADDING,
} as const;

// ── 時間帯ピル ────────────────────────────────────────────────
export const LABEL_FONT_SIZE = 38;
export const PILL_HEIGHT = 74;
export const PILL_PADDING_X = 36;
export const PILL_DOT = 18;
export const PILL_DOT_GAP = 20;
export const PILL_TOP = CARD.top + 30;

// ── つかみ帯 ──────────────────────────────────────────────────
export const HOOK_GAP_ABOVE = 34;
export const HOOK_FONT_SIZE_MAX = 52;
export const HOOK_FONT_SIZE_MIN = 44;
export const HOOK_BAND_PADDING_X = 40;
export const HOOK_BAND_PADDING_Y = 24;
export const HOOK_BAND_RADIUS = 24;
export const HOOK_LINE_RATIO = 1.32;
export const HOOK_MAX_TEXT_HEIGHT = 200;
export const HOOK_GAP_BELOW = 40;

// ── 見出し「問題」 ───────────────────────────────────────────
export const HEADING_TEXT = "問題";
export const HEADING_FONT_SIZE = 72;
export const HEADING_BAR_WIDTH = 16;
export const HEADING_BAR_GAP = 28;
export const HEADING_BLOCK_HEIGHT = Math.round(HEADING_FONT_SIZE * 1.18);
export const HEADING_TO_QUESTION = 115;

// ── 問題文 ────────────────────────────────────────────────────
export const QUESTION_FONT_SIZE_MAX = 68;
export const QUESTION_FONT_SIZE_MIN = 44;
export const QUESTION_LINE_RATIO = 1.4;
/**
 * R-2: 問題文の最大高は定数で持たず、イラストの保証高から導く（design.ts）。
 * 旧 QUESTION_MAX_HEIGHT = 430 は廃止。
 */

// ── イラスト / コーチ / 吹き出し ─────────────────────────────
export const CONTENT_GAP = 48;
export const ILLUSTRATION_RADIUS = 28;
export const ILLUSTRATION_COACH_GAP = 16;
/** R-2: イラストの箱に先取りで確保する高さ（配分順序を決める要） */
export const ILLUSTRATION_GUARANTEED_HEIGHT = 500;
export const COACH_BOX = { width: 300, height: 430 } as const;
export const COACH_BOTTOM_MARGIN = 140;
/** コーチはカード下端基準で立たせる（現行版 _coach_top と同値） */
export const COACH_TOP = CARD.bottom - COACH_BOTTOM_MARGIN - COACH_BOX.height;
export const BUBBLE_PADDING = 28;
export const BUBBLE_TAIL_WIDTH = 28;
export const BUBBLE_TOP_OFFSET = 60;
export const BUBBLE_RADIUS = 32;
export const BUBBLE_FONT_SIZE_MAX = 44;
export const BUBBLE_FONT_SIZE_MIN = 30;
export const BUBBLE_LINE_RATIO = 1.4;
export const BUBBLE_MAX_TEXT_HEIGHT = 200;

// ── カウントダウンバッジ ─────────────────────────────────────
export const BADGE_DIAMETER = 150;
export const BADGE_RING_GAP = 8;
export const BADGE_RING_WIDTH = 12;
export const BADGE_OUTER = BADGE_DIAMETER + 2 * (BADGE_RING_GAP + BADGE_RING_WIDTH);
export const COUNT_FONT_SIZE = 96;

// ── 「考え中」ピル（3〜8 秒のビート） ───────────────────────
export const THINK_PILL_HEIGHT = 64;
export const THINK_PILL_PADDING_X = 28;
export const THINK_PILL_FONT_SIZE = 34;
export const THINK_DOT = 12;

export const INTRO_BUBBLE_TEXT = "わかったらコメントしてくれ！";
export const GUIDANCE_BUBBLE_TEXT = "答えは投稿のキャプションへ！";

export { LINE_END_PROHIBITED, LINE_START_PROHIBITED };
