import { Audio } from "@remotion/media";
import {
  AbsoluteFill,
  Easing,
  Img,
  Interactive,
  Sequence,
  interpolate,
  spring,
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
  OPENING_END,
  OPENING_FADE_FRAMES,
  OPENING_HOP_PERIOD,
  OPENING_JR_BUBBLE_IN,
  OPENING_MASTER_BUBBLE_IN,
  OPENING_NARRATION_START,
  OPENING_SHEEN_PERIOD,
  beatAt,
  hopLift,
  loopPhase,
  loopSin,
} from "./timeline";

const HOOK_MAX_FONT_SIZE = 74;
const HOOK_INNER_WIDTH = 828;
/** 導入シーンの hook（1 行。最大 14 字 = validate.py の HOOK_MAX で 57px） */
const OPENING_HOOK_MAX_FONT_SIZE = 60;
const OPENING_HOOK_INNER_WIDTH = 800;
/** 導入シーンの自己紹介の吹き出しの上端（カメロックが上・Jr. が下。R-1-2 で決定） */
const OPENING_MASTER_BUBBLE_TOP = 920;
const OPENING_JR_BUBBLE_TOP = 1075;

/**
 * ウミガメのスープ参加型リール（PoC 第 2 稿。2026-09-04 の人間ゲートの指摘を反映）。
 *
 * 版面:
 * - 導入シーン（先頭 5.0 秒。セット改修 R-1-1・版面は R-1-2 で決定）: 「新体験」スタンプ → 黄色の 2 行見出し
 *   → 説明文（「真相」を朱色・「質問」を黄色のタグで強調）→ 「今日の謎」の暗いカードに hook → キャラの自己紹介の
 *   吹き出し（カメロックが上・Jr. が下）。終わりの 8 フレームで本編の版面へクロスフェードする。
 *   動き: スタンプが跳ねながらフェードイン / 見出しと「質問」タグに光沢スイープ / 「真相」が小さく跳ねる /
 *   自己紹介の吹き出しはカメロック → Jr. の順に後から入る（SE 付き）。見出しだけナレーションで読み上げる
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
  opening,
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

  // 周期アニメーション
  const masterFloat = loopSin(frame, LOOP_PERIODS.masterFloat) * 8;
  const masterBreathe = 1 + loopSin(frame, LOOP_PERIODS.masterBreathe) * 0.008;
  const jrFloat = loopSin(frame, LOOP_PERIODS.jrFloat, 0.25) * 7;
  const hop = hopLift(frame);
  const sheenPhase = loopPhase(frame, LOOP_PERIODS.hookSheen);
  const hookBreathe = 1 + loopSin(frame, LOOP_PERIODS.hookBreathe) * 0.006;
  // つかみ帯は 1 行固定。内寸 828px（900 - 左右 36px）に収まるよう、11 字を超えたら字数に応じて縮める（上限 74px）
  const hookFontSize = Math.min(HOOK_MAX_FONT_SIZE, Math.floor(HOOK_INNER_WIDTH / [...hook].length) - 1);
  const headingBar = 1 + loopSin(frame, LOOP_PERIODS.headingBar) * 0.09;
  const tagDot = (loopSin(frame, LOOP_PERIODS.tagDot) + 1) / 2;

  // 導入シーン → 本編のクロスフェード（導入シーンは最初のフレームから完成した状態で見せる）
  const mainOpacity = interpolate(frame, [OPENING_END, OPENING_END + OPENING_FADE_FRAMES], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const openingVisible = frame < OPENING_END + OPENING_FADE_FRAMES;
  const openingHookFontSize = Math.min(OPENING_HOOK_MAX_FONT_SIZE, Math.floor(OPENING_HOOK_INNER_WIDTH / [...hook].length));

  const narrationRuleStart = NARRATION_START + narration.problem.frames + NARRATION_GAP;
  const narrationEnd = narrationRuleStart + narration.rule.frames;
  const openingNarrationEnd = OPENING_NARRATION_START + narration.opening.frames;

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

      {/* 本編の版面（導入シーンの後にクロスフェードで出る） */}
      <Interactive.Div name="Main layer" style={{ position: "absolute", inset: 0, opacity: mainOpacity }}>
        {/* つかみ帯（フック文）: 常時表示 + 光沢スイープ + 呼吸 */}
        <Interactive.Div
          name="Hook band"
          style={{
            position: "absolute",
            left: 90,
            top: 100,
            width: 900,
            boxSizing: "border-box",
            padding: "16px 36px",
            borderRadius: 24,
            backgroundColor: "#ffc42e",
            color: "#14202a",
            fontFamily: FONT_DISPLAY,
            fontSize: hookFontSize,
            lineHeight: 1.25,
            whiteSpace: "nowrap",
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
            left: 90,
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
      </Interactive.Div>

      {/* 導入シーン: 新体験スタンプ・見出し・説明文・今日の謎（キャラは下部ゾーンに常駐） */}
      {openingVisible ? (
        <OpeningLayer opening={opening} hook={hook} hookFontSize={openingHookFontSize} opacity={1 - mainOpacity} frame={frame} fps={fps} />
      ) : null}

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

      {/* 導入シーンの自己紹介の吹き出し（導入シーンと一緒にフェードアウトする） */}
      {openingVisible ? (
        <Interactive.Div name="Opening self intro" style={{ position: "absolute", inset: 0, opacity: 1 - mainOpacity }}>
          <Sequence
            name="Opening master bubble"
            from={OPENING_MASTER_BUBBLE_IN}
            durationInFrames={OPENING_END + OPENING_FADE_FRAMES - OPENING_MASTER_BUBBLE_IN}
            layout="none"
          >
            <MasterBubble
              top={OPENING_MASTER_BUBBLE_TOP}
              text={opening.selfIntro.master}
              tag={master.name}
              tagDot={tagDot}
              pop
              glow={false}
              lift={hop}
            />
          </Sequence>
          <Sequence
            name="Opening jr bubble"
            from={OPENING_JR_BUBBLE_IN}
            durationInFrames={OPENING_END + OPENING_FADE_FRAMES - OPENING_JR_BUBBLE_IN}
            layout="none"
          >
            <JrBubble
              top={OPENING_JR_BUBBLE_TOP}
              text={opening.selfIntro.jr}
              tag={jr.name}
              tagDot={tagDot}
              pop
              glow={false}
              lift={hop}
            />
          </Sequence>
        </Interactive.Div>
      ) : null}

      {/* 吹き出し: ビートごとにスナップで切り替える。返答ビートでは質問を残したまま返答を追加表示 */}
      {BEATS.map((b) => {
        const key = `${b.kind}-${"round" in b ? b.round : ""}-${b.from}`;
        const duration = b.to - b.from;
        if (b.kind === "opening") {
          return null;
        }
        if (b.kind === "intro") {
          return (
            <Sequence key={key} name={`Bubble ${b.kind}`} from={b.from} durationInFrames={duration} layout="none">
              <MasterBubble text={masterLines.intro} tag={master.name} tagDot={tagDot} pop glow={false} lift={hop} />
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
            [0, openingNarrationEnd, openingNarrationEnd + 4, NARRATION_START - 6, NARRATION_START, narrationEnd, narrationEnd + fps / 2],
            [0.14, 0.14, 0.24, 0.24, 0.14, 0.14, 0.32],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
          )
        }
      />
      <Sequence
        name="Narration opening"
        from={OPENING_NARRATION_START}
        durationInFrames={narration.opening.frames}
        layout="none"
      >
        <Audio src={staticFile(narration.opening.file)} volume={1} />
      </Sequence>
      {[OPENING_MASTER_BUBBLE_IN, OPENING_JR_BUBBLE_IN].map((seFrame) => (
        <Sequence key={`opening-se-${seFrame}`} name={`Opening SE ${seFrame}`} from={seFrame} durationInFrames={8} layout="none">
          <Audio src={staticFile(bubbleSe)} volume={0.6} />
        </Sequence>
      ))}
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

/** 導入シーンの文字の縁取り（背景の上でも読めるよう濃紺の影を四方に） */
const OPENING_OUTLINE =
  "0 4px 0 #0b1720, 0 -2px 0 #0b1720, 3px 0 0 #0b1720, -3px 0 0 #0b1720, 0 10px 26px rgba(0,0,0,0.6)";

/** 導入シーンの文字（新体験スタンプ・見出し・説明文・今日の謎）。背景の上半分を沈めて文字を読ませる */
const OpeningLayer: React.FC<{
  opening: UmigameReelProps["opening"];
  hook: string;
  hookFontSize: number;
  opacity: number;
  frame: number;
  fps: number;
}> = ({ opening, hook, hookFontSize, opacity, frame, fps }) => {
  // スタンプ: 上から落ちて跳ねながらフェードイン（減衰の弱いばね）
  const stampSpring = spring({ frame, fps, config: { damping: 7, mass: 0.6, stiffness: 140 } });
  const stampOpacity = interpolate(frame, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  // 見出しの光沢: 導入中に 2 回、左から右へ通す
  const sheen = loopPhase(frame + OPENING_SHEEN_PERIOD / 2, OPENING_SHEEN_PERIOD);
  return (
  <Interactive.Div name="Opening layer" style={{ position: "absolute", inset: 0, opacity }}>
    <Interactive.Div
      name="Opening dim"
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: 1080,
        height: 1920,
        background: "linear-gradient(180deg, rgba(4,12,18,0.62) 0%, rgba(4,12,18,0.40) 45%, rgba(4,12,18,0.05) 70%)",
      }}
    />
    <Interactive.Div
      name="Opening badge"
      style={{
        position: "absolute",
        left: 70,
        top: 100,
        padding: "11px 37px",
        borderRadius: 999,
        backgroundColor: "#e8452c",
        color: "#ffffff",
        fontFamily: FONT_DISPLAY,
        fontSize: 88,
        lineHeight: 1.15,
        letterSpacing: 4,
        boxShadow: "0 8px 22px rgba(0,0,0,0.45), inset 0 0 0 4px rgba(255,255,255,0.35)",
        rotate: "-8deg",
        opacity: stampOpacity,
        translate: `0px ${(1 - stampSpring) * -120}px`,
        scale: `${1 + (1 - stampSpring) * 0.35}`,
      }}
    >
      {opening.badge}
    </Interactive.Div>
    <Interactive.Div
      name="Opening headline"
      style={{
        position: "absolute",
        left: 60,
        top: 235,
        width: 960,
        textAlign: "center",
        fontFamily: FONT_DISPLAY,
        fontSize: 104,
        lineHeight: 1.18,
        color: "#ffc42e",
        textShadow: OPENING_OUTLINE,
        whiteSpace: "nowrap",
      }}
    >
      {opening.headline.map((line) => (
        <div key={line} style={{ position: "relative" }}>
          {line}
          {/* 光沢: 同じ文字を白いグラデーションで切り抜いて重ね、位置を流す */}
          <span
            aria-hidden
            style={{
              position: "absolute",
              inset: 0,
              color: "transparent",
              textShadow: "none",
              backgroundImage:
                "linear-gradient(100deg, transparent 0%, transparent 38%, rgba(255,255,255,0.95) 50%, transparent 62%, transparent 100%)",
              backgroundSize: "300% 100%",
              backgroundRepeat: "no-repeat",
              backgroundPosition: `${100 - sheen * 100}% 0%`,
              WebkitBackgroundClip: "text",
              backgroundClip: "text",
            }}
          >
            {line}
          </span>
        </div>
      ))}
    </Interactive.Div>
    <Interactive.Div
      name="Opening lead"
      style={{
        position: "absolute",
        left: 60,
        top: 500,
        width: 960,
        textAlign: "center",
        fontFamily: FONT_DISPLAY,
        fontSize: 48,
        lineHeight: 1.5,
        color: "#ffffff",
        textShadow: OPENING_OUTLINE,
        whiteSpace: "nowrap",
      }}
    >
      {opening.lead.map((line, index) => (
        <div key={index}>
          {line.map((piece, pieceIndex) => (
            <LeadPiece key={pieceIndex} text={piece.text} em={piece.em} frame={frame} />
          ))}
        </div>
      ))}
    </Interactive.Div>
    <Interactive.Div
      name="Opening hook card"
      style={{
        position: "absolute",
        left: 110,
        top: 690,
        width: 860,
        boxSizing: "border-box",
        padding: "18px 30px 20px",
        borderRadius: 26,
        backgroundColor: "rgba(9,22,30,0.88)",
        border: "3px solid #ffc42e",
        color: "#ffffff",
        textAlign: "center",
        boxShadow: "0 12px 30px rgba(0,0,0,0.45)",
      }}
    >
      <Interactive.Div
        name="Opening hook label"
        style={{ fontFamily: FONT_DISPLAY, fontSize: 32, lineHeight: 1.2, color: "#ffc42e", marginBottom: 6, letterSpacing: 2 }}
      >
        {opening.hookLabel}
      </Interactive.Div>
      <Interactive.Div
        name="Opening hook"
        style={{ fontFamily: FONT_DISPLAY, fontSize: hookFontSize, lineHeight: 1.25, whiteSpace: "nowrap" }}
      >
        {hook}
      </Interactive.Div>
    </Interactive.Div>
  </Interactive.Div>
  );
};

/** 説明文の文字片（accent = 朱色の文字で小さく跳ねる・tag = 黄色の小さなタグで光沢が通る） */
const LeadPiece: React.FC<{ text: string; em?: "accent" | "tag"; frame: number }> = ({ text, em, frame }) => {
  if (em === "accent") {
    const t = loopPhase(frame + OPENING_HOP_PERIOD - 10, OPENING_HOP_PERIOD);
    const lift = t < 0.5 ? Math.sin(t * 2 * Math.PI) * 12 : 0;
    return (
      <span style={{ display: "inline-block", color: "#ff7a5c", fontSize: 54, translate: `0px ${-lift}px` }}>{text}</span>
    );
  }
  if (em === "tag") {
    return (
      <span
        style={{
          display: "inline-block",
          padding: "0 18px 4px",
          margin: "0 10px 0 0",
          borderRadius: 12,
          backgroundColor: "#ffc42e",
          color: "#14202a",
          textShadow: "none",
          fontSize: 50,
          lineHeight: 1.3,
          rotate: "-3deg",
          boxShadow: "0 6px 16px rgba(0,0,0,0.45)",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {text}
        <span
          aria-hidden
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            width: "60%",
            left: `${-60 + loopPhase(frame, OPENING_SHEEN_PERIOD) * 180}%`,
            background: "linear-gradient(100deg, transparent 0%, rgba(255,255,255,0.75) 50%, transparent 100%)",
          }}
        />
      </span>
    );
  }
  return <span>{text}</span>;
};

type BubbleProps = {
  /** 吹き出しの上端（省略時は本編の位置。導入シーンの自己紹介だけ指定する） */
  top?: number;
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
const MasterBubble: React.FC<BubbleProps> = ({ top = 1040, text, tag, tagDot, pop, glow, lift }) => {
  const frame = useCurrentFrame();
  const glowPulse = (loopSin(frame, LOOP_PERIODS.outroGlow) + 1) / 2;
  return (
    <Interactive.Div
      name="Master bubble"
      style={{
        position: "absolute",
        left: 60,
        top,
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
const JrBubble: React.FC<BubbleProps> = ({ top = 905, text, tag, tagDot, pop, glow, lift }) => {
  const frame = useCurrentFrame();
  const glowPulse = (loopSin(frame, LOOP_PERIODS.outroGlow) + 1) / 2;
  return (
    <Interactive.Div
      name="Jr bubble"
      style={{
        position: "absolute",
        right: 160,
        top,
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
