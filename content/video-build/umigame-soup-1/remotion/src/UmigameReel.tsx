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
  BUBBLE_SWITCH_FRAMES,
  LOOP_PERIODS,
  NARRATION_GAP,
  NARRATION_START,
  beatAt,
  hopLift,
  loopPhase,
  loopSin,
} from "./timeline";

/**
 * ウミガメのスープ参加型リール（PoC 第 2 稿。2026-09-04 の人間ゲートの指摘を反映）。
 *
 * 版面:
 * - 全面: 問題の情景イラスト（90 年代 OVA 塗り・中間調）+ 薄いオーバーレイ（ゆっくりズーム呼吸。周期 = 総フレーム）
 * - 常時表示: つかみ帯（光沢スイープ + 呼吸）/ 「問題」+ 問題文全文 / ルール帯
 * - 下部ゾーン（右 12% は Instagram UI に空ける）: 出題者カメロック（左）と Jr.（右）が常駐。
 *   吹き出しは「質問 → 質問 + 返答を並べて表示 → 両方消えて次の質問」の順（ユーザー指示）。
 *   切替はスナップ + 小さな跳ね（30px）。締めは出題者 → Jr.（いいね・フォロー）の 2 段
 * - 音: BGM（ナレーション中はダッキング）/ Polly ナレーション 2 cue / 吹き出し出現の SE 1 種
 *
 * 画面効果は logic-training-1 の Quiz16s から移植（光沢・呼吸・浮遊・跳ね・グロー・名札の点・背景呼吸・見出しバー）。
 */
export const UmigameReel: React.FC<UmigameReelProps> = ({
  hook,
  problemText,
  ruleText,
  background,
  master,
  jr,
  masterLines,
  jrLines,
  playExample,
  narration,
  bgm,
  bubbleSe,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const beat = beatAt(frame);
  const answerText = beat.kind === "answer" ? playExample[beat.round * 2 + 1].text : "";
  const masterIsHappy = beat.kind === "answer" && answerText.includes("はい");

  // 周期アニメーション（周期は TOTAL_FRAMES の約数。フレーム 720 = フレーム 0）
  const masterFloat = loopSin(frame, LOOP_PERIODS.masterFloat) * 8;
  const masterBreathe = 1 + loopSin(frame, LOOP_PERIODS.masterBreathe) * 0.008;
  const jrFloat = loopSin(frame, LOOP_PERIODS.jrFloat, 0.25) * 7;
  const hop = hopLift(frame);
  const sheenPhase = loopPhase(frame, LOOP_PERIODS.hookSheen);
  const hookBreathe = 1 + loopSin(frame, LOOP_PERIODS.hookBreathe) * 0.006;
  const headingBar = 1 + loopSin(frame, LOOP_PERIODS.headingBar) * 0.09;
  const tagDot = (loopSin(frame, LOOP_PERIODS.tagDot) + 1) / 2;

  const narrationRuleStart = NARRATION_START + narration.problem.frames + NARRATION_GAP;
  const narrationEnd = narrationRuleStart + narration.rule.frames;

  return (
    <AbsoluteFill name="Reel" style={{ backgroundColor: "#07141b", fontFamily: FONT_TEXT }}>
      {/* 背景イラスト（1.04〜1.075 倍でゆっくり呼吸。端が見えないよう常に拡大） */}
      <Img
        name="Background illustration"
        src={staticFile(background)}
        style={{
          position: "absolute",
          width: 1080,
          height: 1920,
          left: 0,
          top: 0,
          objectFit: "cover",
          transformOrigin: "50% 40%",
          scale: interpolate(frame, [0, durationInFrames / 2, durationInFrames], [1.04, 1.075, 1.04], {
            easing: Easing.bezier(0.45, 0, 0.55, 1),
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      />
      <Interactive.Div
        name="Overlay"
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 1080,
          height: 1920,
          background:
            "linear-gradient(180deg, rgba(4,12,18,0.34) 0%, rgba(4,12,18,0.18) 40%, rgba(4,12,18,0.30) 70%, rgba(4,12,18,0.62) 100%)",
        }}
      />

      {/* つかみ帯（フック文）: 常時表示 + 光沢スイープ + 呼吸 */}
      <Interactive.Div
        name="Hook band"
        style={{
          position: "absolute",
          left: 60,
          top: 100,
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
          overflow: "hidden",
          scale: `${hookBreathe}`,
        }}
      >
        {hook}
        <Interactive.Div
          name="Hook sheen"
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            width: "45%",
            left: `${-45 + sheenPhase * 145}%`,
            background: "linear-gradient(100deg, transparent 0%, rgba(255,255,255,0.45) 50%, transparent 100%)",
            pointerEvents: "none",
          }}
        />
      </Interactive.Div>

      {/* 問題カード: 見出し + 問題文全文 + ルール帯（常時表示） */}
      <Interactive.Div
        name="Problem card"
        style={{
          position: "absolute",
          left: 60,
          top: 250,
          width: 900,
          boxSizing: "border-box",
          padding: "34px 40px 34px 40px",
          borderRadius: 32,
          backgroundColor: "rgba(9, 22, 30, 0.86)",
          border: "2px solid rgba(255,196,46,0.35)",
          boxShadow: "0 16px 40px rgba(0,0,0,0.45), inset 0 0 0 1px rgba(255,255,255,0.08), 0 0 28px rgba(255,196,46,0.12)",
        }}
      >
        <Interactive.Div name="Problem heading" style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 14 }}>
          <Interactive.Div
            name="Heading accent bar"
            style={{
              width: 12,
              height: 44,
              borderRadius: 6,
              backgroundColor: "#ffc42e",
              transformOrigin: "50% 50%",
              scale: `1 ${headingBar}`,
            }}
          />
          <Interactive.Div
            name="Problem label"
            style={{
              display: "inline-block",
              padding: "4px 20px",
              borderRadius: 999,
              backgroundColor: "rgba(255,196,46,0.18)",
              color: "#ffc42e",
              fontFamily: FONT_DISPLAY,
              fontSize: 40,
              lineHeight: 1.2,
            }}
          >
            問題
          </Interactive.Div>
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
            marginTop: 22,
            padding: "14px 22px",
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

      {/* 下部ゾーン: キャラクター 2 体（常駐。浮遊 + 呼吸 + 切替時の小さな跳ね） */}
      <Img
        name="Master character"
        src={staticFile(masterIsHappy ? master.happy : master.base)}
        style={{
          position: "absolute",
          left: 10,
          top: 1180,
          width: 430,
          height: 473,
          transformOrigin: "50% 100%",
          translate: `0px ${masterFloat - hop}px`,
          scale: `${masterBreathe}`,
        }}
      />
      <Img
        name="Jr character"
        src={staticFile(jr.base)}
        style={{
          position: "absolute",
          left: 590,
          top: 1290,
          width: 320,
          height: 352,
          transformOrigin: "50% 100%",
          translate: `0px ${jrFloat - hop * 0.7}px`,
        }}
      />

      {/* 吹き出し: ビートごとにスナップで切り替える。返答ビートでは質問を残したまま返答を追加表示 */}
      {BEATS.map((b) => {
        const key = `${b.kind}-${"round" in b ? b.round : ""}-${b.from}`;
        const duration = b.to - b.from;
        if (b.kind === "intro" || b.kind === "seam") {
          return (
            <Sequence key={key} name={`Bubble ${b.kind}`} from={b.from} durationInFrames={duration} layout="none">
              <MasterBubble text={masterLines.intro} tag={master.name} tagDot={tagDot} pop={false} glow={false} lift={0} />
            </Sequence>
          );
        }
        if (b.kind === "master_outro") {
          return (
            <Sequence key={key} name="Bubble master outro" from={b.from} durationInFrames={duration} layout="none">
              <MasterBubble text={masterLines.outro} tag={master.name} tagDot={tagDot} pop glow lift={hop} />
            </Sequence>
          );
        }
        if (b.kind === "jr_outro") {
          return (
            <Sequence key={key} name="Bubble jr outro" from={b.from} durationInFrames={duration} layout="none">
              <JrBubble text={jrLines.outro} tag={jr.name} tagDot={tagDot} pop glow lift={hop} />
            </Sequence>
          );
        }
        const question = playExample[b.round * 2].text;
        const answer = playExample[b.round * 2 + 1].text;
        if (b.kind === "question") {
          return (
            <Sequence key={key} name={`Bubble question ${b.round + 1}`} from={b.from} durationInFrames={duration} layout="none">
              <JrBubble text={question} tag={jr.name} tagDot={tagDot} pop glow={false} lift={hop} />
            </Sequence>
          );
        }
        return (
          <Sequence key={key} name={`Bubble answer ${b.round + 1}`} from={b.from} durationInFrames={duration} layout="none">
            <JrBubble text={question} tag={jr.name} tagDot={tagDot} pop={false} glow={false} lift={0} />
            <MasterBubble text={answer} tag={master.name} tagDot={tagDot} pop glow={false} lift={hop} />
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
      {BUBBLE_SWITCH_FRAMES.map((seFrame: number) => (
        <Sequence key={seFrame} name={`Bubble SE ${seFrame}`} from={seFrame} durationInFrames={8} layout="none">
          <Audio src={staticFile(bubbleSe)} volume={0.7} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

type BubbleProps = {
  text: string;
  tag: string;
  tagDot: number;
  pop: boolean;
  glow: boolean;
  lift: number;
};

/** 吹き出し内の名札（キャラ名 + 脈動するアクセント点） */
const NameTag: React.FC<{ name: string; dot: number; color: string }> = ({ name, dot, color }) => (
  <Interactive.Div
    name="Name tag"
    style={{
      display: "flex",
      alignItems: "center",
      gap: 8,
      marginBottom: 4,
      color: "#56688a",
      fontFamily: FONT_DISPLAY,
      fontSize: 24,
      lineHeight: 1.2,
    }}
  >
    <Interactive.Div
      name="Tag dot"
      style={{
        width: 14,
        height: 14,
        borderRadius: 999,
        backgroundColor: color,
        scale: `${1 + dot * 0.35}`,
        boxShadow: `0 0 ${6 + dot * 10}px ${color}`,
      }}
    />
    {name}
  </Interactive.Div>
);

/** 出題者の吹き出し（左下のキャラへ向くしっぽ付き。返答ビートでは質問の下に出る） */
const MasterBubble: React.FC<BubbleProps> = ({ text, tag, tagDot, pop, glow, lift }) => {
  const frame = useCurrentFrame();
  const glowPulse = (loopSin(frame, LOOP_PERIODS.outroGlow) + 1) / 2;
  return (
    <Interactive.Div
      name="Master bubble"
      style={{
        position: "absolute",
        left: 60,
        top: 1040,
        maxWidth: 800,
        boxSizing: "border-box",
        padding: "14px 30px 18px 30px",
        borderRadius: 30,
        backgroundColor: "#ffffff",
        border: "5px solid #ffc42e",
        color: "#16232b",
        fontFamily: FONT_DISPLAY,
        fontSize: 42,
        lineHeight: 1.35,
        boxShadow: glow
          ? `0 10px 24px rgba(0,0,0,0.35), 0 0 ${18 + glowPulse * 26}px rgba(255,196,46,${0.45 + glowPulse * 0.4})`
          : "0 10px 24px rgba(0,0,0,0.35)",
        transformOrigin: "60px 100%",
        translate: `0px ${-lift}px`,
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
      <NameTag name={tag} dot={tagDot} color="#ffc42e" />
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
  );
};

/** Jr. の吹き出し（右下のキャラへ向くしっぽ付き。右 12% は空ける。質問ビートと返答ビートで同じ位置） */
const JrBubble: React.FC<BubbleProps> = ({ text, tag, tagDot, pop, glow, lift }) => {
  const frame = useCurrentFrame();
  const glowPulse = (loopSin(frame, LOOP_PERIODS.outroGlow) + 1) / 2;
  return (
    <Interactive.Div
      name="Jr bubble"
      style={{
        position: "absolute",
        right: 160,
        top: 905,
        maxWidth: 780,
        boxSizing: "border-box",
        padding: "14px 30px 18px 30px",
        borderRadius: 30,
        backgroundColor: "#e8f5ff",
        border: "5px solid #8fd3ff",
        color: "#16232b",
        fontFamily: FONT_DISPLAY,
        fontSize: 42,
        lineHeight: 1.35,
        boxShadow: glow
          ? `0 10px 24px rgba(0,0,0,0.35), 0 0 ${18 + glowPulse * 26}px rgba(143,211,255,${0.45 + glowPulse * 0.4})`
          : "0 10px 24px rgba(0,0,0,0.35)",
        transformOrigin: "calc(100% - 60px) 100%",
        translate: `0px ${-lift}px`,
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
      <NameTag name={tag} dot={tagDot} color="#8fd3ff" />
      {text}
      <Interactive.Div
        name="Jr bubble tail"
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
