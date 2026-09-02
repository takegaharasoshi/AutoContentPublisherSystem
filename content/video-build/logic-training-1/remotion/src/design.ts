/**
 * props から版面の実寸を導く。ここで決まるのは「静止した版面」で、
 * 動き（浮遊・段階表示・カウントダウン）は QuizVideo 側で上に乗せる。
 */

import {
  BADGE_OUTER,
  BOTTOM_ZONE,
  BUBBLE_FONT_SIZE_MAX,
  BUBBLE_FONT_SIZE_MIN,
  BUBBLE_LINE_RATIO,
  BUBBLE_MAX_TEXT_HEIGHT,
  BUBBLE_PADDING,
  BUBBLE_TAIL_WIDTH,
  BUBBLE_TOP_OFFSET,
  COACH_BOX,
  COACH_TOP,
  CONTENT_GAP,
  GUIDANCE_BUBBLE_TEXT,
  HEADING_BLOCK_HEIGHT,
  HEADING_TO_QUESTION,
  HOOK_BAND_PADDING_X,
  HOOK_BAND_PADDING_Y,
  HOOK_FONT_SIZE_MAX,
  HOOK_FONT_SIZE_MIN,
  HOOK_GAP_ABOVE,
  HOOK_GAP_BELOW,
  HOOK_LINE_RATIO,
  HOOK_MAX_TEXT_HEIGHT,
  ILLUSTRATION_COACH_GAP,
  INTRO_BUBBLE_TEXT,
  LABEL_FONT_SIZE,
  MIN_ILLUSTRATION_HEIGHT,
  PILL_DOT,
  PILL_DOT_GAP,
  PILL_HEIGHT,
  PILL_PADDING_X,
  PILL_TOP,
  QUESTION_FONT_SIZE_MAX,
  QUESTION_FONT_SIZE_MIN,
  QUESTION_LINE_RATIO,
  QUESTION_MAX_HEIGHT,
  TOP_ZONE,
} from "./layout";
import { FittedText, fitText, measureEm } from "./textUtils";

export type Rect = {
  left: number;
  top: number;
  right: number;
  bottom: number;
};

export type QuizProps = {
  /** パレットの選択に使うスロット（morning / noon / night） */
  slotCode: "morning" | "noon" | "night";
  /** 時間帯ラベル（例: 朝の脳みそトレ） */
  slotLabel: string;
  /** つかみ帯の文言（prompt_configs の slot_hook） */
  slotHook: string;
  /** 問題文 */
  question: string;
  /** カウントダウン中に吹き出しへ出すヒント */
  hint: string;
  /** public/ からの相対パス（例: illustrations/85.png） */
  illustrationSrc: string;
  illustrationWidth: number;
  illustrationHeight: number;
};

const size = (rect: Rect) => ({
  width: rect.right - rect.left,
  height: rect.bottom - rect.top,
});

/** 枠に比率を保って内接させた矩形（現行版 _paste_illustration と同じ扱い） */
const containRect = (
  box: Rect,
  contentWidth: number,
  contentHeight: number,
): Rect => {
  const { width, height } = size(box);
  const scale = Math.min(width / contentWidth, height / contentHeight, 1);
  const fittedWidth = Math.round(contentWidth * scale);
  const fittedHeight = Math.round(contentHeight * scale);
  const left = box.left + Math.round((width - fittedWidth) / 2);
  const top = box.top + Math.round((height - fittedHeight) / 2);
  return {
    left,
    top,
    right: left + fittedWidth,
    bottom: top + fittedHeight,
  };
};

export type Design = {
  pill: Rect;
  band: Rect & { text: FittedText };
  headingTop: number;
  badge: Rect;
  question: { left: number; top: number; width: number; text: FittedText };
  illustrationBox: Rect;
  illustration: Rect;
  bubble: Rect;
  bubbleTexts: Record<"intro" | "hint" | "guidance", FittedText>;
  coach: Rect;
};

export const deriveDesign = (props: QuizProps): Design => {
  // 時間帯ピル: 文字幅に合わせた幅で上部ゾーンの中央（= カード中央）に置く
  const labelWidth = measureEm(Array.from(props.slotLabel)) * LABEL_FONT_SIZE;
  const pillInner = PILL_DOT + PILL_DOT_GAP + labelWidth;
  const pillWidth = pillInner + 2 * PILL_PADDING_X;
  const pillLeft = Math.round((TOP_ZONE.left + TOP_ZONE.right - pillWidth) / 2);
  const pill: Rect = {
    left: pillLeft,
    top: PILL_TOP,
    right: pillLeft + pillWidth,
    bottom: PILL_TOP + PILL_HEIGHT,
  };

  // つかみ帯: 上部ゾーンの幅いっぱい。1 行に収まるサイズを最優先する
  const bandTop = pill.bottom + HOOK_GAP_ABOVE;
  const bandText = fitText(props.slotHook, {
    maxWidth: TOP_ZONE.right - TOP_ZONE.left - 2 * HOOK_BAND_PADDING_X,
    maxHeight: HOOK_MAX_TEXT_HEIGHT,
    maxFontSize: HOOK_FONT_SIZE_MAX,
    minFontSize: HOOK_FONT_SIZE_MIN,
    lineRatio: HOOK_LINE_RATIO,
    preferSingleLine: true,
  });
  const band = {
    left: TOP_ZONE.left,
    top: bandTop,
    right: TOP_ZONE.right,
    bottom: bandTop + bandText.height + 2 * HOOK_BAND_PADDING_Y,
    text: bandText,
  };

  const headingTop = band.bottom + HOOK_GAP_BELOW;

  // カウントダウンバッジ: 見出し行の右端。上部ゾーンなので右 12% 予約は掛けない
  const badgeTop = Math.round(headingTop + (HEADING_BLOCK_HEIGHT - BADGE_OUTER) / 2);
  const badge: Rect = {
    left: TOP_ZONE.right - BADGE_OUTER,
    top: badgeTop,
    right: TOP_ZONE.right,
    bottom: badgeTop + BADGE_OUTER,
  };

  const questionTop = headingTop + HEADING_TO_QUESTION;
  const questionWidth = TOP_ZONE.right - TOP_ZONE.left;
  const questionText = fitText(props.question, {
    maxWidth: questionWidth,
    maxHeight: QUESTION_MAX_HEIGHT,
    maxFontSize: QUESTION_FONT_SIZE_MAX,
    minFontSize: QUESTION_FONT_SIZE_MIN,
    lineRatio: QUESTION_LINE_RATIO,
  });
  const question = {
    left: TOP_ZONE.left,
    top: questionTop,
    width: questionWidth,
    text: questionText,
  };

  // イラストブロック: 問題文の下・コーチの真上。下部ゾーン（右 12% 予約あり）
  const illustrationBox: Rect = {
    left: BOTTOM_ZONE.left,
    top: questionTop + questionText.height + CONTENT_GAP,
    right: BOTTOM_ZONE.right,
    bottom: COACH_TOP - ILLUSTRATION_COACH_GAP,
  };
  if (illustrationBox.bottom - illustrationBox.top < MIN_ILLUSTRATION_HEIGHT) {
    throw new Error("問題文が長すぎて情景イラストの領域が残らない");
  }
  const illustration = containRect(
    illustrationBox,
    props.illustrationWidth,
    props.illustrationHeight,
  );

  const coach: Rect = {
    left: BOTTOM_ZONE.right - COACH_BOX.width,
    top: COACH_TOP,
    right: BOTTOM_ZONE.right,
    bottom: COACH_TOP + COACH_BOX.height,
  };

  // 吹き出し: コーチの左。3 種類の文言のうち最も高いものに箱を合わせ、
  // カットが変わっても箱の大きさが動かないようにする
  const bubbleLeft = BOTTOM_ZONE.left;
  const bubbleRight = coach.left - BUBBLE_TAIL_WIDTH;
  const fitBubble = (text: string) =>
    fitText(text, {
      maxWidth: bubbleRight - bubbleLeft - 2 * BUBBLE_PADDING,
      maxHeight: BUBBLE_MAX_TEXT_HEIGHT,
      maxFontSize: BUBBLE_FONT_SIZE_MAX,
      minFontSize: BUBBLE_FONT_SIZE_MIN,
      lineRatio: BUBBLE_LINE_RATIO,
    });
  const bubbleTexts = {
    intro: fitBubble(INTRO_BUBBLE_TEXT),
    hint: fitBubble(props.hint),
    guidance: fitBubble(GUIDANCE_BUBBLE_TEXT),
  };
  const bubbleTextHeight = Math.max(
    ...Object.values(bubbleTexts).map((fitted) => fitted.height),
  );
  const bubbleTop = COACH_TOP + BUBBLE_TOP_OFFSET;
  const bubble: Rect = {
    left: bubbleLeft,
    top: bubbleTop,
    right: bubbleRight,
    bottom: bubbleTop + bubbleTextHeight + 2 * BUBBLE_PADDING,
  };

  return {
    pill,
    band,
    headingTop,
    badge,
    question,
    illustrationBox,
    illustration,
    bubble,
    bubbleTexts,
    coach,
  };
};
