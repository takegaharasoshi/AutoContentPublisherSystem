import { Audio } from "@remotion/media";
import {
  AbsoluteFill,
  Easing,
  Img,
  Interactive,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { FONT_DISPLAY, FONT_TEXT } from "./fonts";
import type { UmigameReelProps } from "./props";
import {
  BEATS,
  BUBBLE_POP_FRAMES,
  BUBBLE_SE_FRAMES,
  LOOP_PERIODS,
  NARRATION_GAP,
  NARRATION_START,
  beatAt,
} from "./timeline";

/**
 * ウミガメのスープ参加型リール（PoC 版面）。
 *
 * 版面（21-1 決定の叩き台）:
 * - 全面: 問題の情景イラスト + 暗いオーバーレイ（ゆっくり横ドリフト。周期 = 総フレーム）
 * - 常時表示: つかみ帯（フック）/ 「問題」+ 問題文全文 / ルール帯
 * - 下部ゾーン（右 12% は Instagram UI に空ける）: 出題者（左）と質問者（右）が常駐し、
 *   吹き出しがビートごとにスナップで切り替わる（導入 → 3 往復 → 締め → 継ぎ目 = 導入と同じ状態）
 * - 音: BGM（ナレーション中はダッキング）/ 冒頭ナレーション（問題文 → ルール）/ 吹き出し出現の SE 1 種
 */
export const UmigameReel: React.FC<UmigameReelProps> = ({
  hook,
  problemText,
  ruleText,
  background,
  master,
  assistant,
  masterLines,
  playExample,
  narration,
  bgm,
  bubbleSe,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const beat = beatAt(frame);
  const answerText =
    beat.kind === "answer" ? playExample[beat.round * 2 + 1].text : "";
  const masterIsHappy = beat.kind === "answer" && answerText.includes("はい");

  // 周期アニメーション（周期は TOTAL_FRAMES の約数。フレーム 600 = フレーム 0）
  const masterBob = Math.sin((frame / LOOP_PERIODS.masterBob) * Math.PI * 2) * 6;
  const assistantBob = Math.sin((frame / LOOP_PERIODS.assistantBob) * Math.PI * 2 + Math.PI / 2) * 5;

  const narrationRuleStart = NARRATION_START + narration.problem.frames + NARRATION_GAP;
  const narrationEnd = narrationRuleStart + narration.rule.frames;

  return (
    <AbsoluteFill name="Reel" style={{ backgroundColor: "#07141b", fontFamily: FONT_TEXT }}>
      {/* 背景イラスト（少し拡大して横にドリフト。端が見えないよう 1.06 倍） */}
      <Img
        name="Background illustration"
        src={staticFile(background)}
        style={{
          position: "absolute",
          width: 1145,
          height: 2035,
          left: -32,
          top: -58,
          objectFit: "cover",
          translate: interpolate(frame, [0, durationInFrames / 2, durationInFrames], ["0px 0px", "-28px 0px", "0px 0px"], {
            easing: Easing.bezier(0.45, 0, 0.55, 1),
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      />
      <Interactive.Div
        name="Dark overlay"
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 1080,
          height: 1920,
          background:
            "linear-gradient(180deg, rgba(4,12,18,0.50) 0%, rgba(4,12,18,0.34) 45%, rgba(4,12,18,0.66) 100%)",
        }}
      />

      {/* つかみ帯（フック文）: 常時表示 */}
      <Interactive.Div
        name="Hook band"
        style={{
          position: "absolute",
          left: 60,
          top: 128,
          width: 900,
          boxSizing: "border-box",
          padding: "16px 36px",
          borderRadius: 24,
          backgroundColor: "#ffc42e",
          color: "#14202a",
          fontFamily: FONT_DISPLAY,
          fontSize: 74,
          lineHeight: 1.25,
          textAlign: "center",
          letterSpacing: 1,
          boxShadow: "0 10px 30px rgba(0,0,0,0.45)",
        }}
      >
        {hook}
      </Interactive.Div>

      {/* 問題カード: 見出し + 問題文全文 + ルール帯（常時表示） */}
      <Interactive.Div
        name="Problem card"
        style={{
          position: "absolute",
          left: 60,
          top: 292,
          width: 900,
          boxSizing: "border-box",
          padding: "36px 40px 36px 40px",
          borderRadius: 32,
          backgroundColor: "rgba(9, 22, 30, 0.84)",
          border: "2px solid rgba(255,255,255,0.16)",
          boxShadow: "0 16px 40px rgba(0,0,0,0.4)",
        }}
      >
        <Interactive.Div
          name="Problem label"
          style={{
            display: "inline-block",
            padding: "6px 22px",
            borderRadius: 999,
            backgroundColor: "rgba(255,196,46,0.18)",
            color: "#ffc42e",
            fontFamily: FONT_DISPLAY,
            fontSize: 40,
            lineHeight: 1.2,
            marginBottom: 16,
          }}
        >
          問題
        </Interactive.Div>
        <Interactive.Div
          name="Problem text"
          style={{
            color: "#ffffff",
            fontFamily: FONT_TEXT,
            fontWeight: 700,
            fontSize: 44,
            lineHeight: 1.5,
            textAlign: "left",
          }}
        >
          {problemText}
        </Interactive.Div>
        <Interactive.Div
          name="Rule band"
          style={{
            marginTop: 24,
            padding: "16px 22px",
            borderRadius: 16,
            borderLeft: "10px solid #ffc42e",
            backgroundColor: "rgba(255,196,46,0.14)",
            color: "#ffe9a8",
            fontFamily: FONT_TEXT,
            fontWeight: 700,
            fontSize: 34,
            lineHeight: 1.45,
          }}
        >
          {ruleText}
        </Interactive.Div>
      </Interactive.Div>

      {/* 下部ゾーン: キャラクター 2 体（常駐） */}
      <Img
        name="Master character"
        src={staticFile(masterIsHappy ? master.happy : master.base)}
        style={{
          position: "absolute",
          left: 20,
          top: 1165,
          width: 430,
          height: 473,
          translate: `0px ${masterBob}px`,
        }}
      />
      <Img
        name="Assistant character"
        src={staticFile(assistant.base)}
        style={{
          position: "absolute",
          left: 560,
          top: 1264,
          width: 340,
          height: 374,
          translate: `0px ${assistantBob}px`,
        }}
      />
      <Interactive.Div
        name="Master name tag"
        style={{
          position: "absolute",
          left: 40,
          top: 1150,
          padding: "4px 18px",
          borderRadius: 999,
          backgroundColor: "#ffc42e",
          color: "#14202a",
          fontFamily: FONT_DISPLAY,
          fontSize: 28,
          lineHeight: 1.3,
        }}
      >
        {master.name}
      </Interactive.Div>
      <Interactive.Div
        name="Assistant name tag"
        style={{
          position: "absolute",
          left: 760,
          top: 1250,
          padding: "4px 18px",
          borderRadius: 999,
          backgroundColor: "#8fd3ff",
          color: "#14202a",
          fontFamily: FONT_DISPLAY,
          fontSize: 28,
          lineHeight: 1.3,
        }}
      >
        {assistant.name}
      </Interactive.Div>

      {/* 吹き出し: ビートごとにスナップで切り替える（Sequence の from/duration がビート境界） */}
      {BEATS.map((b) => {
        const key = `${b.kind}-${"round" in b ? b.round : ""}-${b.from}`;
        if (b.kind === "intro" || b.kind === "seam") {
          return (
            <Sequence key={key} name={`Bubble ${b.kind}`} from={b.from} durationInFrames={b.to - b.from} layout="none">
              <MasterBubble text={masterLines.intro} pop={false} />
            </Sequence>
          );
        }
        if (b.kind === "outro") {
          return (
            <Sequence key={key} name="Bubble outro" from={b.from} durationInFrames={b.to - b.from} layout="none">
              <MasterBubble text={masterLines.outro} pop />
            </Sequence>
          );
        }
        const line = playExample[b.round * 2 + (b.kind === "question" ? 0 : 1)];
        return (
          <Sequence key={key} name={`Bubble ${b.kind} ${b.round + 1}`} from={b.from} durationInFrames={b.to - b.from} layout="none">
            {b.kind === "question" ? <QuestionerBubble text={line.text} /> : <MasterBubble text={line.text} pop />}
          </Sequence>
        );
      })}

      {/* 音: BGM（ナレーション中はダッキング）/ ナレーション 2 cue / 吹き出し SE */}
      <Audio
        name="BGM"
        src={staticFile(bgm)}
        volume={(f) =>
          interpolate(
            f,
            [NARRATION_START - 6, NARRATION_START, narrationEnd, narrationEnd + fps / 2],
            [0.32, 0.14, 0.14, 0.32],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
          )
        }
      />
      <Sequence name="Narration problem" from={NARRATION_START} durationInFrames={narration.problem.frames} layout="none">
        <Audio src={staticFile(narration.problem.file)} volume={1} />
      </Sequence>
      <Sequence name="Narration rule" from={narrationRuleStart} durationInFrames={narration.rule.frames} layout="none">
        <Audio src={staticFile(narration.rule.file)} volume={1} />
      </Sequence>
      {BUBBLE_SE_FRAMES.map((seFrame) => (
        <Sequence key={seFrame} name={`Bubble SE ${seFrame}`} from={seFrame} durationInFrames={8} layout="none">
          <Audio src={staticFile(bubbleSe)} volume={0.7} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

/** 出題者の吹き出し（左下のキャラへ向くしっぽ付き） */
const MasterBubble: React.FC<{ text: string; pop: boolean }> = ({ text, pop }) => {
  const frame = useCurrentFrame();
  return (
    <>
      <Interactive.Div
        name="Master bubble"
        style={{
          position: "absolute",
          left: 60,
          top: 985,
          maxWidth: 800,
          boxSizing: "border-box",
          padding: "20px 34px",
          borderRadius: 30,
          backgroundColor: "#ffffff",
          border: "5px solid #ffc42e",
          color: "#16232b",
          fontFamily: FONT_DISPLAY,
          fontSize: 42,
          lineHeight: 1.35,
          boxShadow: "0 10px 24px rgba(0,0,0,0.35)",
          transformOrigin: "60px 100%",
          scale: pop
            ? interpolate(frame, [0, BUBBLE_POP_FRAMES], [0.6, 1], {
                easing: Easing.bezier(0.16, 1, 0.3, 1),
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                output: "perceptual-scale",
              })
            : 1,
        }}
      >
        {text}
        <Interactive.Div
          name="Master bubble tail"
          style={{
            position: "absolute",
            left: 90,
            bottom: -22,
            width: 36,
            height: 36,
            backgroundColor: "#ffffff",
            borderRight: "5px solid #ffc42e",
            borderBottom: "5px solid #ffc42e",
            rotate: "45deg",
          }}
        />
      </Interactive.Div>
    </>
  );
};

/** 質問者の吹き出し（右下のキャラへ向くしっぽ付き。右 12% は空ける） */
const QuestionerBubble: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  return (
    <Interactive.Div
      name="Questioner bubble"
      style={{
        position: "absolute",
        right: 160,
        top: 985,
        maxWidth: 760,
        boxSizing: "border-box",
        padding: "20px 34px",
        borderRadius: 30,
        backgroundColor: "#e8f5ff",
        border: "5px solid #8fd3ff",
        color: "#16232b",
        fontFamily: FONT_DISPLAY,
        fontSize: 42,
        lineHeight: 1.35,
        boxShadow: "0 10px 24px rgba(0,0,0,0.35)",
        transformOrigin: "calc(100% - 60px) 100%",
        scale: interpolate(frame, [0, BUBBLE_POP_FRAMES], [0.6, 1], {
          easing: Easing.bezier(0.16, 1, 0.3, 1),
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          output: "perceptual-scale",
        }),
      }}
    >
      {text}
      <Interactive.Div
        name="Questioner bubble tail"
        style={{
          position: "absolute",
          right: 90,
          bottom: -22,
          width: 36,
          height: 36,
          backgroundColor: "#e8f5ff",
          borderRight: "5px solid #8fd3ff",
          borderBottom: "5px solid #8fd3ff",
          rotate: "45deg",
        }}
      />
    </Interactive.Div>
  );
};
