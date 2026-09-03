import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";

import { Design, QuizProps, Rect, deriveDesign } from "./design";
import { FONT_STACK } from "./fonts";
import {
  BADGE_DIAMETER,
  BADGE_RING_GAP,
  BADGE_RING_WIDTH,
  BUBBLE_PADDING,
  BUBBLE_RADIUS,
  BUBBLE_TAIL_WIDTH,
  CARD,
  CARD_RADIUS,
  COUNT_FONT_SIZE,
  HEADING_BAR_GAP,
  HEADING_BAR_WIDTH,
  HEADING_BLOCK_HEIGHT,
  HEADING_FONT_SIZE,
  HEADING_TEXT,
  HOOK_BAND_RADIUS,
  ILLUSTRATION_RADIUS,
  LABEL_FONT_SIZE,
  PILL_DOT,
  PILL_DOT_GAP,
  PILL_PADDING_X,
  THINK_DOT,
  THINK_PILL_FONT_SIZE,
  THINK_PILL_HEIGHT,
  THINK_PILL_PADDING_X,
  HEIGHT,
  WIDTH,
} from "./layout";
import { Palette, SLOT_PALETTES } from "./palette";
import {
  clamp01,
  easeOut,
  hopLift,
  loopCos,
  loopPhase,
  loopSin,
  loopTriangle,
  seamFade,
} from "./motion";
import {
  COUNTDOWN_COUNT,
  COUNTDOWN_END,
  COUNTDOWN_STEP,
  INTRO_END,
  LOOP_PERIODS,
  SEAM_SWITCH,
  THINK_BEAT_FADE,
  THINK_BEAT_IN,
} from "./timeline";

const boxOf = (rect: Rect): React.CSSProperties => ({
  position: "absolute",
  left: rect.left,
  top: rect.top,
  width: rect.right - rect.left,
  height: rect.bottom - rect.top,
});

const COACH_SRC = {
  hook: "coach/coach_hook.png",
  question: "coach/coach_question.png",
  answer: "coach/coach_answer.png",
} as const;

type Pose = keyof typeof COACH_SRC;

/**
 * カットごとのコーチの表情と吹き出しの文言（現行版と同じ割り当て）。
 * SEAM_SWITCH 以降は導入カットの状態へスナップで戻し、frame 480 の見た目を
 * frame 0 に一致させる（クロスフェードにすると二重露光に見える）。
 */
const cutStateOf = (frame: number): { pose: Pose; bubble: FittedTextKey } =>
  frame < INTRO_END || frame >= SEAM_SWITCH
    ? { pose: "hook", bubble: "intro" }
    : frame < COUNTDOWN_END
      ? { pose: "question", bubble: "hint" }
      : { pose: "answer", bubble: "guidance" };

type FittedTextKey = "intro" | "hint" | "guidance";

/** 背景の装飾オーブ（カード内の余白にだけ置く。周期 480 で厳密にループ） */
const BackgroundOrbs: React.FC<{ frame: number; palette: Palette }> = ({
  frame,
  palette,
}) => {
  // 版面の要素が来ない帯（イラスト右のストリップと吹き出しの下）にだけ置く
  const orbs = [
    { x: 985, y: 980, r: 130, phase: 0 },
    { x: 995, y: 1430, r: 165, phase: 0.33 },
    { x: 120, y: 1665, r: 115, phase: 0.66 },
  ];
  return (
    <>
      {orbs.map((orb, index) => {
        const drift = loopSin(
          frame + orb.phase * LOOP_PERIODS.backgroundOrbs,
          LOOP_PERIODS.backgroundOrbs,
        );
        const swell = loopCos(
          frame + orb.phase * LOOP_PERIODS.backgroundOrbs,
          LOOP_PERIODS.backgroundOrbs,
        );
        return (
          <div
            key={index}
            style={{
              position: "absolute",
              left: orb.x - orb.r,
              top: orb.y - orb.r,
              width: orb.r * 2,
              height: orb.r * 2,
              borderRadius: "50%",
              background: palette.decoration,
              opacity: 0.45,
              transform: `translate(${drift * 18}px, ${swell * 26}px) scale(${
                1 + swell * 0.06
              })`,
            }}
          />
        );
      })}
    </>
  );
};

/** 時間帯ピル。アクセントドットだけが脈動する（周期 80） */
const SlotPill: React.FC<{
  frame: number;
  design: Design;
  palette: Palette;
  label: string;
}> = ({ frame, design, palette, label }) => {
  const pulse = loopTriangle(frame, LOOP_PERIODS.pillDot);
  return (
    <div
      style={{
        ...boxOf(design.pill),
        borderRadius: (design.pill.bottom - design.pill.top) / 2,
        background: palette.decoration,
        display: "flex",
        alignItems: "center",
        paddingLeft: PILL_PADDING_X,
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          width: PILL_DOT,
          height: PILL_DOT,
          borderRadius: "50%",
          background: palette.accent,
          marginRight: PILL_DOT_GAP,
          transform: `scale(${1 + pulse * 0.35})`,
          boxShadow: `0 0 ${8 + pulse * 14}px ${palette.accent}`,
        }}
      />
      <div
        style={{
          fontFamily: FONT_STACK,
          fontWeight: 700,
          fontSize: LABEL_FONT_SIZE,
          color: palette.text,
          whiteSpace: "nowrap",
        }}
      >
        {label}
      </div>
    </div>
  );
};

/** つかみ帯。文字は動かさず、帯の上を光沢が渡る（周期 96）+ 微小な呼吸（周期 120） */
const HookBand: React.FC<{ frame: number; design: Design; palette: Palette }> = ({
  frame,
  design,
  palette,
}) => {
  const width = design.band.right - design.band.left;
  const sheen = loopPhase(frame, LOOP_PERIODS.bandSheen);
  const breathe = loopSin(frame, LOOP_PERIODS.bandBreathe);
  return (
    <div
      style={{
        ...boxOf(design.band),
        borderRadius: HOOK_BAND_RADIUS,
        background: palette.accent,
        overflow: "hidden",
        transform: `scale(${1 + breathe * 0.006})`,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: -0.45 * width + sheen * 1.45 * width,
          width: 0.45 * width,
          background:
            "linear-gradient(100deg, transparent, rgba(255,255,255,0.35), transparent)",
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {design.band.text.lines.map((line, index) => (
          <div
            key={index}
            style={{
              fontFamily: FONT_STACK,
              fontWeight: 700,
              fontSize: design.band.text.fontSize,
              lineHeight: `${design.band.text.lineHeight}px`,
              color: palette.card,
              whiteSpace: "nowrap",
            }}
          >
            {line}
          </div>
        ))}
      </div>
    </div>
  );
};

/** 見出し「問題」。左のアクセントバーだけが伸縮する（周期 160） */
const Heading: React.FC<{ frame: number; design: Design; palette: Palette }> = ({
  frame,
  design,
  palette,
}) => {
  const barHeight = Math.round(HEADING_FONT_SIZE * 0.82);
  const stretch = 1 + loopSin(frame, LOOP_PERIODS.headingBar) * 0.09;
  return (
    <div
      style={{
        position: "absolute",
        left: design.question.left,
        top: design.headingTop,
        height: HEADING_BLOCK_HEIGHT,
        display: "flex",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: HEADING_BAR_WIDTH,
          height: barHeight,
          borderRadius: HEADING_BAR_WIDTH / 2,
          background: palette.accent,
          marginRight: HEADING_BAR_GAP,
          transform: `scaleY(${stretch})`,
        }}
      />
      <div
        style={{
          fontFamily: FONT_STACK,
          fontWeight: 700,
          fontSize: HEADING_FONT_SIZE,
          lineHeight: `${HEADING_BLOCK_HEIGHT}px`,
          color: palette.text,
          whiteSpace: "nowrap",
        }}
      >
        {HEADING_TEXT}
      </div>
    </div>
  );
};

/**
 * 問題文。フレーム 0 から全文を出し、最後まで消さない（R-1-3 のユーザー指摘）。
 * ループ視聴が常態のため、段階表示は 2 周目以降に「読み始めた文が無い」
 * 状態を作ってしまう。継ぎ目でも落とさない = frame 479 と frame 0 が一致する。
 */
const QuestionText: React.FC<{
  design: Design;
  palette: Palette;
}> = ({ design, palette }) => {
  const { text } = design.question;
  return (
    <div
      style={{
        position: "absolute",
        left: design.question.left,
        top: design.question.top,
        width: design.question.width,
      }}
    >
      {text.lines.map((line, index) => (
        <div
          key={index}
          style={{
            fontFamily: FONT_STACK,
            fontWeight: 400,
            fontSize: text.fontSize,
            lineHeight: `${text.lineHeight}px`,
            color: palette.text,
            whiteSpace: "nowrap",
          }}
        >
          {line}
        </div>
      ))}
    </div>
  );
};

/** 3〜8 秒の「考える」ビート。イラスト左上に小さく置く */
const ThinkBeat: React.FC<{ frame: number; design: Design; palette: Palette }> = ({
  frame,
  design,
  palette,
}) => {
  const opacity =
    clamp01((frame - THINK_BEAT_IN) / THINK_BEAT_FADE) *
    clamp01((INTRO_END - frame) / THINK_BEAT_FADE);
  if (opacity <= 0) return null;
  const phase = loopPhase(frame, LOOP_PERIODS.thinkDots);
  return (
    <div
      style={{
        position: "absolute",
        left: design.illustration.left + 18,
        top: design.illustration.top + 18,
        height: THINK_PILL_HEIGHT,
        borderRadius: THINK_PILL_HEIGHT / 2,
        background: `${palette.card}E6`,
        display: "flex",
        alignItems: "center",
        padding: `0 ${THINK_PILL_PADDING_X}px`,
        opacity,
        boxShadow: `0 6px 18px ${palette.text}22`,
      }}
    >
      <span
        style={{
          fontFamily: FONT_STACK,
          fontWeight: 700,
          fontSize: THINK_PILL_FONT_SIZE,
          color: palette.mutedText,
          marginRight: 14,
          whiteSpace: "nowrap",
        }}
      >
        考え中
      </span>
      {[0, 1, 2].map((index) => {
        const local = (phase - index / 3 + 1) % 1;
        const lit = Math.max(0, Math.cos(2 * Math.PI * local));
        return (
          <span
            key={index}
            style={{
              width: THINK_DOT,
              height: THINK_DOT,
              borderRadius: "50%",
              background: palette.accent,
              marginLeft: index === 0 ? 0 : 10,
              opacity: 0.35 + lit * 0.65,
              transform: `scale(${0.85 + lit * 0.4})`,
            }}
          />
        );
      })}
    </div>
  );
};

/** 8〜13 秒のカウントダウン。リング進行 + 数字のスケール + tick 同期のパルス */
const Countdown: React.FC<{ frame: number; design: Design; palette: Palette }> = ({
  frame,
  design,
  palette,
}) => {
  if (frame < INTRO_END || frame >= COUNTDOWN_END) return null;
  const elapsed = frame - INTRO_END;
  const total = COUNTDOWN_END - INTRO_END;
  const remaining = 1 - elapsed / total;
  const value = COUNTDOWN_COUNT - Math.floor(elapsed / COUNTDOWN_STEP);
  const inStep = elapsed % COUNTDOWN_STEP;
  // 数字は毎秒はじけて、そのあと静かに沈む
  const pop = 1 + 0.28 * (1 - easeOut(clamp01(inStep / 9)));
  // tick SE（8.0 秒）に合わせた 1 回だけのパルスリング
  const tick = clamp01(elapsed / 18);
  const appear = easeOut(clamp01(elapsed / 8));

  const outer = design.badge;
  const radius = BADGE_DIAMETER / 2 + BADGE_RING_GAP + BADGE_RING_WIDTH / 2;
  const circumference = 2 * Math.PI * radius;
  const size = outer.right - outer.left;

  return (
    <div style={{ ...boxOf(outer), opacity: appear }}>
      {/* tick に同期して外へ広がるパルス */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: "50%",
          border: `4px solid ${palette.accent}`,
          opacity: (1 - tick) * 0.8,
          transform: `scale(${1 + tick * 0.45})`,
        }}
      />
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        style={{ position: "absolute", inset: 0 }}
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={palette.decoration}
          strokeWidth={BADGE_RING_WIDTH}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={palette.accent}
          strokeWidth={BADGE_RING_WIDTH}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference * (1 - remaining)}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          left: (size - BADGE_DIAMETER) / 2,
          top: (size - BADGE_DIAMETER) / 2,
          width: BADGE_DIAMETER,
          height: BADGE_DIAMETER,
          borderRadius: "50%",
          background: palette.accent,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transform: `scale(${appear})`,
        }}
      >
        <span
          style={{
            fontFamily: FONT_STACK,
            fontWeight: 700,
            fontSize: COUNT_FONT_SIZE,
            lineHeight: `${COUNT_FONT_SIZE}px`,
            color: palette.card,
            transform: `scale(${pop})`,
          }}
        >
          {value}
        </span>
      </div>
    </div>
  );
};

/** 吹き出し（コーチのセリフ）。3 種類の文言を重ねて不透明度で切り替える */
const Bubble: React.FC<{
  frame: number;
  design: Design;
  palette: Palette;
  active: FittedTextKey;
  guidanceEmphasis: number;
}> = ({ frame, design, palette, active, guidanceEmphasis }) => {
  const bob = loopSin(frame, LOOP_PERIODS.bubbleBob) * 4;
  const glow = loopTriangle(frame, LOOP_PERIODS.guidanceGlow);
  const tailY = (design.bubble.top + design.bubble.bottom) / 2 - design.bubble.top;
  const height = design.bubble.bottom - design.bubble.top;
  return (
    <div
      style={{
        ...boxOf(design.bubble),
        transform: `translateY(${bob}px)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: BUBBLE_RADIUS,
          background: palette.decoration,
          boxShadow: `0 0 ${18 + glow * 26}px ${palette.accent}${
            guidanceEmphasis > 0 ? "AA" : "00"
          }`,
          outline: `${guidanceEmphasis * (2 + glow * 3)}px solid ${palette.accent}`,
          outlineOffset: 2,
        }}
      />
      {/* コーチへ向かうしっぽ */}
      <div
        style={{
          position: "absolute",
          right: -BUBBLE_TAIL_WIDTH,
          top: tailY - 26,
          width: 0,
          height: 0,
          borderTop: "26px solid transparent",
          borderBottom: "26px solid transparent",
          borderLeft: `${BUBBLE_TAIL_WIDTH}px solid ${palette.decoration}`,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: BUBBLE_PADDING,
          top: (height - design.bubbleTexts[active].height) / 2,
        }}
      >
        {design.bubbleTexts[active].lines.map((line, index) => (
          <div
            key={index}
            style={{
              fontFamily: FONT_STACK,
              fontWeight: 700,
              fontSize: design.bubbleTexts[active].fontSize,
              lineHeight: `${design.bubbleTexts[active].lineHeight}px`,
              color: palette.text,
              whiteSpace: "nowrap",
            }}
          >
            {line}
          </div>
        ))}
      </div>
    </div>
  );
};

export const QuizVideo: React.FC<QuizProps> = (props) => {
  const frame = useCurrentFrame();
  const design = deriveDesign(props);
  const palette = SLOT_PALETTES[props.slotCode];
  const seam = seamFade(frame);
  const { pose, bubble } = cutStateOf(frame);

  // コーチ + 吹き出しは 1 つのレイヤーとして持ち上がる（現行 ffmpeg 版と同じ）
  const lift = hopLift(frame);
  const float = loopSin(frame, LOOP_PERIODS.coachFloat) * 11;
  const breathe = 1 + loopSin(frame, LOOP_PERIODS.coachBreathe) * 0.008;
  const guidanceEmphasis =
    (frame >= COUNTDOWN_END && frame < SEAM_SWITCH
      ? easeOut(clamp01((frame - COUNTDOWN_END) / 10))
      : 0) *
    (1 - seam);
  const illustrationZoom = 1 + loopTriangle(frame, LOOP_PERIODS.illustrationDrift) * 0.018;

  return (
    <AbsoluteFill style={{ background: palette.background }}>
      <div
        style={{
          position: "absolute",
          left: CARD.left,
          top: CARD.top,
          width: CARD.right - CARD.left,
          height: CARD.bottom - CARD.top,
          borderRadius: CARD_RADIUS,
          background: palette.card,
          overflow: "hidden",
        }}
      />
      <AbsoluteFill
        style={{
          clipPath: `inset(${CARD.top}px ${WIDTH - CARD.right}px ${
            HEIGHT - CARD.bottom
          }px ${CARD.left}px round ${CARD_RADIUS}px)`,
        }}
      >
        <BackgroundOrbs frame={frame} palette={palette} />
      </AbsoluteFill>

      <SlotPill
        frame={frame}
        design={design}
        palette={palette}
        label={props.slotLabel}
      />
      <HookBand frame={frame} design={design} palette={palette} />
      <Heading frame={frame} design={design} palette={palette} />
      <QuestionText design={design} palette={palette} />

      {/* 情景イラスト: 枠に内接させた矩形の中でゆっくり呼吸する */}
      <div
        style={{
          ...boxOf(design.illustration),
          borderRadius: ILLUSTRATION_RADIUS,
          overflow: "hidden",
          boxShadow: `inset 0 0 0 2px ${palette.decoration}`,
        }}
      >
        <Img
          src={staticFile(props.illustrationSrc)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${illustrationZoom})`,
          }}
        />
      </div>

      <ThinkBeat frame={frame} design={design} palette={palette} />
      <Countdown frame={frame} design={design} palette={palette} />

      {/* コーチ + 吹き出しのレイヤー（減衰ホップは 8.0 秒 / 13.0 秒の 2 箇所） */}
      <AbsoluteFill style={{ transform: `translateY(${-lift}px)` }}>
        <Bubble
          frame={frame}
          design={design}
          palette={palette}
          active={bubble}
          guidanceEmphasis={guidanceEmphasis}
        />
        {guidanceEmphasis > 0 ? (
          <div
            style={{
              position: "absolute",
              left: design.bubble.left,
              top: design.bubble.bottom + 22,
              width: design.bubble.right - design.bubble.left,
              textAlign: "center",
              fontFamily: FONT_STACK,
              fontWeight: 700,
              fontSize: 46,
              color: palette.accent,
              opacity: guidanceEmphasis,
              transform: `translateY(${
                loopTriangle(frame, LOOP_PERIODS.guidanceGlow) * 14
              }px)`,
            }}
          >
            ▼
          </div>
        ) : null}
        <div
          style={{
            ...boxOf(design.coach),
            transform: `translateY(${float}px) scale(${breathe})`,
            transformOrigin: "bottom center",
          }}
        >
          <Img
            src={staticFile(COACH_SRC[pose])}
            style={{ width: "100%", height: "100%", objectFit: "contain" }}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
