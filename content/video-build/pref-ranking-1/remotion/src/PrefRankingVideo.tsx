import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { FONT_DISPLAY, FONT_DISPLAY_WEIGHT, FONT_TEXT } from "./fonts";
import { INSET_ONLY_PREF_CODES } from "./japanPaths";
import { JapanMap } from "./JapanMap";
import { MapPalette } from "./palette";
import { PREF_CENTROIDS } from "./prefCentroids";
import {
  BAND,
  BUBBLE,
  CHARACTER,
  LIST,
  LIST_TOP,
  MAP_BOX,
  MAP_INSET_PANEL,
  MAP_VIEWBOX,
  SAFE,
  SOURCE_BAND,
  mapPointZoomed,
  rowHeight,
  rowTop,
} from "./layout";
import { THEME, TOKENS, Theme } from "./theme";
import { TIMELINE_20S, Timeline } from "./timeline";

/**
 * 都道府県ランキング TOP5 地図ルーレット型（20 秒版）。
 * `variant` は 17-4a の色比較用（Fix 後に 1 本へ畳む）。
 *
 * 画面に出る文言はすべて props（entries / labels / title / subtitle / sourceDisplay /
 * valuePrefix / valueSuffix）から来る。コンポーネント内に日本語のハードコードを置かない
 * （英語圏展開の再利用要件②。方式設計書 ranking-prebuilt.html セクション 8.1）。
 */

export type Entry = {
  rank: number;
  prefCode: number;
  prefName: string;
  value: number;
};

export type Cue = {
  id: string;
  text: string;
  /** public/ 配下の相対パス。null なら無音（版面確認用） */
  audioSrc: string | null;
  /**
   * 音声の配置フレーム。ビルドツーリングが実測長から算出して渡す
   * （順位シーンは後ろ合わせ = 方式設計書セクション 8.3 の decision ①）。
   */
  startFrame: number;
};

export type Labels = {
  /** タイトル帯の上段に出すセット固定のラベル（「都道府県ランキング TOP5」） */
  setLabel: string;
  /** 順位の接尾辞（「位」） */
  rankSuffix: string;
  /** スピン中の吹き出し。{rank} を順位で置換する */
  searching: string;
  /** 全国平均プレートの見出し */
  averageLabel: string;
};

export const DEFAULT_LABELS: Labels = {
  setLabel: "都道府県ランキング TOP5",
  rankSuffix: "位",
  searching: "第{rank}位は…？",
  averageLabel: "全国平均",
};

export type PrefRankingProps = {
  title: string;
  /** 全国平均などの補足（表示文字列そのもの）。序盤のプレートに出す */
  subtitle: string | null;
  sourceDisplay: string;
  /** 数値の前置き（「年間」など。何の値なのかを行ごとに示す） */
  valuePrefix: string | null;
  valueSuffix: string;
  backgroundSrc: string | null;
  entries: Entry[];
  /** cue ID → セリフ（intro / teaser / r5..r2 / r1_call / r1_name / outro） */
  cues: Record<string, Cue>;
  labels: Labels;
};

const NOISE_URI =
  "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E\")";

/** 生成り地に沈む金・地図上の県名用の 8 方向縁取り */
const outline = (color: string, width: number): string =>
  [
    [-width, 0], [width, 0], [0, -width], [0, width],
    [-width, -width], [width, -width], [-width, width], [width, width],
  ]
    .map(([x, y]) => `${x}px ${y}px 0 ${color}`)
    .join(", ");

const formatValue = (value: number): string =>
  value.toLocaleString("ja-JP", { maximumFractionDigits: 2 });

const mapPalette = (theme: Theme): MapPalette => ({
  baseFill: theme.mapBaseFill,
  baseStroke: theme.mapBaseStroke,
  revealedStroke: theme.mapRevealedStroke,
  revealedFill: theme.mapRevealedFill,
  litFill: TOKENS.gold,
  litStroke: TOKENS.goldLight,
  litGlow: "rgba(217,166,46,0.72)",
  flashStroke: "#FFFFFF",
  flashGlow: "rgba(244,215,125,0.95)",
  focusPanelBg: theme.focusPanelBg,
  focusPanelBorder: theme.mapBaseStroke,
});

/** 減速するルーレットの点滅タイミング（ラウンド内ローカルフレーム） */
const spinTicks = (spinDur: number): number[] => {
  const ticks: number[] = [];
  let t = 0;
  while (t < spinDur) {
    ticks.push(t);
    t += 2 + Math.round(9 * Math.pow(t / spinDur, 2.2));
  }
  return ticks;
};

const spinCodeAt = (rank: number, local: number, spinDur: number): number => {
  const ticks = spinTicks(spinDur);
  let idx = 0;
  for (let i = 0; i < ticks.length; i++) {
    if (ticks[i] <= local) idx = i;
  }
  return 1 + Math.floor(random(`spin-${rank}-${idx}`) * 47);
};

const FLASH_DUR = 14;

/**
 * 地図の拡大率。順位行が積み上がるほど地図を少し縮め、序盤の空白を地図で埋める。
 * 上限 1.05 は「拡大しても日本全域がセーフ域と順位行スタックの外へ出ない」上限
 * （17-4a 第 2〜3 巡。1.15 では九州南部が順位行のゾーンへ押し出されていた）。
 */
const MAP_ZOOM_MAX = 1.04;

const mapZoomAt = (frame: number, tl: Timeline): number =>
  interpolate(
    frame,
    [
      0,
      tl.rounds[5].rowAt - 12,
      tl.rounds[5].rowAt + 16,
      tl.rounds[4].rowAt + 16,
      tl.rounds[3].rowAt + 16,
      tl.rounds[2].rowAt + 16,
      tl.rounds[1].rowAt + 16,
    ],
    [MAP_ZOOM_MAX, MAP_ZOOM_MAX, 1.04, 1.03, 1.02, 1.01, 1.0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

type Stage = {
  lit: number | null;
  flash: { code: number; intensity: number } | null;
  revealed: Record<number, string>;
  spinningRank: number | null;
};

const stageAt = (frame: number, entries: Entry[], tl: Timeline, theme: Theme): Stage => {
  let lit: number | null = null;
  let flash: Stage["flash"] = null;
  const revealed: Record<number, string> = {};
  let spinningRank: number | null = null;

  for (const entry of entries) {
    const t = tl.rounds[entry.rank];
    if (!t) continue;
    if (frame >= t.stop) {
      revealed[entry.prefCode] = theme.mapRevealedFill[entry.rank];
      if (frame < t.stop + FLASH_DUR) {
        flash = { code: entry.prefCode, intensity: 1 - (frame - t.stop) / FLASH_DUR };
      }
    } else if (frame >= t.start) {
      spinningRank = entry.rank;
      lit = spinCodeAt(entry.rank, frame - t.start, t.spin);
    }
  }
  return { lit, flash, revealed, spinningRank };
};

// ---------------------------------------------------------------- 背景

const Backdrop: React.FC<{ theme: Theme; backgroundSrc: string | null; total: number }> = ({
  theme,
  backgroundSrc,
  total,
}) => {
  const frame = useCurrentFrame();
  // ゆっくりした寄り（Ken Burns）。静止画に見えないための最低限の動き
  const zoom = interpolate(frame, [0, total], [1.0, 1.07], { extrapolateRight: "clamp" });
  return (
    <>
      <AbsoluteFill
        style={{ background: `linear-gradient(180deg, ${theme.pageTop}, ${theme.pageBottom})` }}
      />
      {backgroundSrc ? (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <Img
            src={staticFile(backgroundSrc)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${zoom})`,
            }}
          />
        </AbsoluteFill>
      ) : null}
      <AbsoluteFill style={{ background: theme.bgOverlay }} />
      <AbsoluteFill
        style={{
          backgroundImage: NOISE_URI,
          backgroundSize: "200px 200px",
          opacity: theme.noiseOpacity,
          mixBlendMode: "multiply",
        }}
      />
      <AbsoluteFill style={{ background: theme.vignette }} />
    </>
  );
};

// ---------------------------------------------------------------- タイトル帯

const TitleBand: React.FC<{ theme: Theme; title: string; setLabel: string }> = ({
  theme,
  title,
  setLabel,
}) => {
  // 0 秒時点で版面が空だとスキップされるため、タイトル帯は登場アニメを持たず最初から出す
  const hairline = `linear-gradient(90deg, ${TOKENS.goldDeep}, ${TOKENS.goldLight} 45%, ${TOKENS.gold})`;
  return (
    <div
      style={{
        position: "absolute",
        left: BAND.left,
        top: BAND.top,
        width: BAND.right - BAND.left,
        height: BAND.height,
        borderRadius: "0 28px 28px 0",
        background: theme.bandBg,
        boxShadow: "0 14px 30px rgba(12,18,34,0.22)",
        overflow: "hidden",
        display: "flex",
        alignItems: "center",
      }}
    >
      {/* 青海波を思わせる薄い地紋 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `repeating-radial-gradient(circle at 0 100%, rgba(0,0,0,0) 0 30px, ${theme.bandPattern} 30px 33px)`,
          backgroundSize: "66px 66px",
        }}
      />
      {/* 帯の下辺だけに細い金の見切り。上下 4px の金縁は浮いて見えるため廃止（17-4a 第 3 巡） */}
      <div
        style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 2, background: hairline, opacity: 0.5 }}
      />
      <div style={{ position: "relative", paddingLeft: 100, paddingRight: 36 }}>
        {/* 何のランキングかが一目で分かるようセット固定のラベルを上段に置く */}
        <div
          style={{
            fontSize: 26,
            fontWeight: 700,
            letterSpacing: 4,
            color: theme.bandEyebrow,
            marginBottom: 2,
          }}
        >
          {setLabel}
        </div>
        <div
          style={{
            fontFamily: FONT_DISPLAY,
            fontSize: 56,
            fontWeight: FONT_DISPLAY_WEIGHT,
            lineHeight: 1.06,
            letterSpacing: 1,
            whiteSpace: "nowrap",
            color: theme.bandText,
          }}
        >
          {title}
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- 全国平均プレート（序盤の受け皿）

const AveragePlate: React.FC<{ theme: Theme; subtitle: string; labels: Labels; tl: Timeline }> = ({
  theme,
  subtitle,
  labels,
  tl,
}) => {
  const frame = useCurrentFrame();
  const firstRow = tl.rounds[5].rowAt;
  // 0 秒時点で下半分が空にならないよう、登場アニメを持たず最初から出す
  const leave = interpolate(frame, [firstRow - 22, firstRow - 6], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  if (leave <= 0) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: LIST.left,
        right: 1080 - LIST.right,
        top: 1180,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 6,
        padding: "30px 0 36px",
        borderRadius: 28,
        background: theme.plateBg,
        border: `2px solid ${theme.rowBorder}`,
        opacity: leave,
        transform: `scale(${0.96 + 0.04 * leave})`,
      }}
    >
      <div style={{ fontSize: 32, fontWeight: 700, letterSpacing: 8, color: theme.plateLabel }}>
        {labels.averageLabel}
      </div>
      <div style={{ fontSize: 76, fontWeight: 700, color: theme.plateValue, lineHeight: 1.1 }}>
        {subtitle}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- 順位行

const RankRow: React.FC<{
  entry: Entry;
  theme: Theme;
  valuePrefix: string | null;
  valueSuffix: string;
  labels: Labels;
  tl: Timeline;
}> = ({ entry, theme, valuePrefix, valueSuffix, labels, tl }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = tl.rounds[entry.rank];
  const local = frame - t.rowAt;
  if (local < 0) return null;

  const isFirst = entry.rank === 1;
  const height = rowHeight(entry.rank);
  const enter = spring({
    frame: local,
    fps,
    config: isFirst ? { damping: 10, stiffness: 130, mass: 0.8 } : { damping: 15, stiffness: 150 },
  });
  // 締めの見せ場: 全行を順番にわずかに持ち上げる
  const closeLocal = frame - (tl.closingAt + (5 - entry.rank) * 5);
  const closePulse =
    closeLocal > 0 && closeLocal < 40
      ? Math.sin(interpolate(closeLocal, [0, 40], [0, Math.PI])) * (isFirst ? 1 : 0.6)
      : 0;
  const fg = isFirst ? theme.onGold : theme.rowText;

  return (
    <div
      style={{
        position: "absolute",
        left: LIST.left,
        right: 1080 - LIST.right,
        top: rowTop(entry.rank),
        height,
        borderRadius: 22,
        overflow: "hidden",
        background: isFirst
          ? `linear-gradient(100deg, ${TOKENS.goldDeep} 0%, ${TOKENS.gold} 46%, ${TOKENS.goldLight} 100%)`
          : theme.rowBg,
        border: `2px solid ${isFirst ? theme.mapRevealedStroke : theme.rowBorder}`,
        boxShadow: isFirst
          ? `${theme.rowShadow}, 0 0 ${44 + closePulse * 26}px rgba(217,166,46,${0.45 + 0.3 * closePulse})`
          : theme.rowShadow,
        transform: `translateX(${(1 - enter) * 90}px) translateY(${-closePulse * 6}px) scale(${0.98 + 0.02 * enter})`,
        opacity: Math.min(1, enter * 1.6),
        display: "flex",
        alignItems: "center",
        gap: 22,
        padding: "0 28px",
      }}
    >
      {/* 順位バッジ */}
      <div
        style={{
          flexShrink: 0,
          width: isFirst ? 74 : 60,
          height: isFirst ? 74 : 60,
          borderRadius: "50%",
          background: theme.badgeBg,
          border: `2px solid ${isFirst ? TOKENS.goldLight : "rgba(217,166,46,0.65)"}`,
          display: "flex",
          alignItems: "baseline",
          justifyContent: "center",
          gap: 1,
          color: theme.badgeText,
          paddingTop: isFirst ? 12 : 10,
          boxSizing: "border-box",
        }}
      >
        <span style={{ fontSize: isFirst ? 44 : 36, fontWeight: 700, lineHeight: 1 }}>
          {entry.rank}
        </span>
        <span style={{ fontSize: isFirst ? 20 : 17, fontWeight: 700 }}>{labels.rankSuffix}</span>
      </div>

      <div
        style={{
          flex: 1,
          fontFamily: FONT_DISPLAY,
          fontSize: isFirst ? 58 : 48,
          fontWeight: FONT_DISPLAY_WEIGHT,
          color: fg,
          letterSpacing: 1,
        }}
      >
        {entry.prefName}
      </div>

      {/* 数値。何の値かが分かるよう前置き（「年間」など）を数字の前に置く */}
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: 2,
          color: fg,
          fontVariantNumeric: "tabular-nums",
        }}
      >
        {valuePrefix ? (
          <span style={{ fontSize: isFirst ? 26 : 23, fontWeight: 700, opacity: 0.85, marginRight: 3 }}>
            {valuePrefix}
          </span>
        ) : null}
        <span style={{ fontSize: isFirst ? 46 : 38, fontWeight: 700 }}>{formatValue(entry.value)}</span>
        <span style={{ fontSize: isFirst ? 26 : 23, fontWeight: 700, opacity: 0.85 }}>{valueSuffix}</span>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- 地図 → 行へ飛ぶ県名

const FlyingName: React.FC<{
  entry: Entry;
  theme: Theme;
  tl: Timeline;
  zoom: number;
  /** 1 位がインセットの県で、拡大パネルが出ているか */
  insetFocused: boolean;
}> = ({ entry, theme, tl, zoom, insetFocused }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = tl.rounds[entry.rank];
  const local = frame - t.stop;
  const end = t.flyStart + t.flyDur - t.stop;
  if (local < 0 || local > end) return null;

  const isFirst = entry.rank === 1;
  const startSize = isFirst ? 148 : 92;
  const centroid = PREF_CENTROIDS[entry.prefCode] ?? { x: 500, y: 500 };
  const anchor = mapPointZoomed(centroid.x, centroid.y, zoom);
  // 1 位は地図中央下に大きく据えて見せ場にする。2〜5 位は該当県の真上に吹き出す
  // （重心に重ねると、塗られたばかりの県自体をラベルが隠してしまうため）。
  // ただし 1 位がインセットの県のときは拡大パネルが地図中央下に出るため、
  // ラベルはパネルの真上へ逃がす（せっかく拡大した島をラベルで隠さない）。
  const panelTop = mapPointZoomed(
    MAP_INSET_PANEL.x + MAP_INSET_PANEL.width / 2,
    MAP_INSET_PANEL.y,
    zoom
  );
  const from = isFirst
    ? insetFocused
      ? { x: panelTop.x, y: panelTop.y - startSize * 0.42 }
      : { x: (SAFE.left + SAFE.right) / 2, y: LIST_TOP - 190 }
    : { x: anchor.x, y: anchor.y - startSize * 0.72 };
  const to = { x: LIST.left + 300, y: rowTop(entry.rank) + rowHeight(entry.rank) / 2 };

  const pop = spring({ frame: local, fps, config: { damping: 9, stiffness: 170, mass: 0.6 } });
  const flyLocal = frame - t.flyStart;
  const fly = interpolate(flyLocal, [0, t.flyDur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (v) => v * v * (3 - 2 * v),
  });

  const size = interpolate(fly, [0, 1], [startSize, isFirst ? 58 : 48]);
  // 端の県（宮崎・沖縄など）でも文字が画面外へ出ないよう出発点を安全域に収める
  const halfWidth = (entry.prefName.length * startSize) / 2;
  const fromX = Math.min(Math.max(from.x, SAFE.left + halfWidth), SAFE.right - halfWidth);
  const fromY = Math.max(from.y, SAFE.top + startSize);
  const x = interpolate(fly, [0, 1], [fromX, to.x]);
  const y = interpolate(fly, [0, 1], [fromY, to.y]) - Math.sin(fly * Math.PI) * 60;
  const fade = interpolate(fly, [0.78, 1], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(-50%, -50%) scale(${0.5 + 0.5 * Math.min(1, pop)})`,
        fontFamily: FONT_DISPLAY,
        fontSize: size,
        fontWeight: FONT_DISPLAY_WEIGHT,
        lineHeight: 1,
        whiteSpace: "nowrap",
        color: isFirst ? TOKENS.goldLight : theme.flyText,
        textShadow: isFirst
          ? `${outline(theme.onGold, 6)}, 0 0 46px rgba(217,166,46,0.9), 0 0 96px rgba(217,166,46,0.7)`
          : `${outline(theme.flyOutline, 5)}, 0 8px 22px rgba(12,18,34,0.35)`,
        opacity: fade,
        zIndex: 8,
      }}
    >
      {entry.prefName}
    </div>
  );
};

/** 1 位発表の放射パーティクル */
const Burst: React.FC<{ at: number; origin: { x: number; y: number }; theme: Theme }> = ({
  at,
  origin,
  theme,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame - at;
  if (local < 0 || local > 46) return null;
  const p = spring({ frame: local, fps, config: { damping: 17 } });
  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 7 }}>
      {Array.from({ length: 18 }).map((_, i) => {
        const angle = (i / 18) * Math.PI * 2 + 0.2;
        const dist = 90 + p * (330 + random(`d-${i}`) * 220);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: origin.x + Math.cos(angle) * dist,
              top: origin.y + Math.sin(angle) * dist * 0.78,
              width: 18,
              height: 18,
              borderRadius: i % 2 ? "50%" : 3,
              background: i % 3 ? TOKENS.gold : theme.bubbleText,
              opacity: 1 - p,
              transform: `rotate(${p * 260}deg)`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 出典行帯

const SourceBand: React.FC<{ theme: Theme; text: string }> = ({ theme, text }) => {
  // 1 行に収める。全角換算の文字数から字送りを決める（36 文字以内が推奨・下限 20px）
  const fontSize = Math.max(
    20,
    Math.min(28, (SOURCE_BAND.right - SOURCE_BAND.left - 36) / (text.length * 0.99))
  );
  return (
    <div
      style={{
        position: "absolute",
        left: SOURCE_BAND.left,
        right: 1080 - SOURCE_BAND.right,
        top: SOURCE_BAND.top,
        height: SOURCE_BAND.height,
        borderRadius: 14,
        background: theme.sourceBg,
        display: "flex",
        alignItems: "center",
        padding: "0 18px",
        color: theme.sourceText,
        fontSize,
        whiteSpace: "nowrap",
        overflow: "hidden",
      }}
    >
      ※{text}
    </div>
  );
};

// ---------------------------------------------------------------- 本体

export const PrefRankingVideo: React.FC<PrefRankingProps> = ({
  title,
  subtitle,
  sourceDisplay,
  valuePrefix,
  valueSuffix,
  backgroundSrc,
  entries = [],
  cues = {},
  labels = DEFAULT_LABELS,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const theme = THEME;
  const tl = TIMELINE_20S;

  const stage = stageAt(frame, entries, tl, theme);
  const announceAt = tl.rounds[1].stop;
  const isAnnounced = frame >= announceAt;

  // 吹き出しに出すテキスト（順位シーンは停止フラッシュ以降のみ = 結果を先出ししない）
  const bubbleText = ((): string | null => {
    // 冒頭だけは音と字幕を対応させない（17-4a Fix）。ナレーションが intro（タイトル読み）を
    // 話している間も、吹き出しには teaser の問いかけを 0 秒から出しておく。
    // intro のテキストはタイトル帯と重複して情報量が増えないのに対し、問いかけを早く出すほど
    // 「予想させてから見届けさせる」時間が長くなるため。
    if (frame < tl.rounds[5].start) return cues.teaser?.text ?? null;
    for (const rank of [5, 4, 3, 2]) {
      const t = tl.rounds[rank];
      const next = rank === 2 ? tl.rounds[1].start : tl.rounds[rank - 1].start;
      if (frame >= t.start && frame < t.stop) {
        return labels.searching.replace("{rank}", String(rank));
      }
      if (frame >= t.stop && frame < next) return cues[`r${rank}`]?.text ?? null;
    }
    const one = tl.rounds[1];
    if (frame >= one.start && frame < one.stop) return cues.r1_call?.text ?? null;
    if (frame >= one.stop && frame < tl.closingAt) return cues.r1_name?.text ?? null;
    return cues.outro?.text ?? null;
  })();

  // ポーズ 3 種は共通キャンバス・共通倍率の正式アセット（17-4b。scripts/normalize_character.py）。
  // 3 枚とも同じ寸法・同じ立ち位置のため、切り替えてもキャラが伸縮・跳躍しない。
  const characterSrc = isAnnounced
    ? "char/goro_gunbai.png"
    : frame >= tl.rounds[1].start
      ? "char/goro_suspense.png"
      : "char/goro_base.png";
  // 1 位の確定がインセットの中だけで起きる県（= 沖縄）のときは、発表に合わせて
  // インセットを拡大パネルへ引き出す。島が小さく、そのままでは「1 位が金に光る」
  // 見せ場が成立しないため（17-4b のユーザー指摘）。鹿児島は本土側が主役なので出さない。
  const firstEntry = entries.find((entry) => entry.rank === 1);
  const focusesInset =
    firstEntry !== undefined && INSET_ONLY_PREF_CODES.includes(firstEntry.prefCode);
  const insetFocus = focusesInset
    ? spring({
        frame: frame - announceAt,
        fps,
        config: { damping: 20, stiffness: 120, mass: 0.8 },
      })
    : 0;
  const bob = Math.sin(frame / 9) * 5;
  const announcePop = isAnnounced
    ? spring({ frame: frame - announceAt, fps, config: { damping: 15, stiffness: 160, mass: 0.6 } })
    : 0;

  // 地図も 0 秒時点から出す（フェードインを入れると冒頭が空に見える）
  const breathe = 1 + Math.sin(frame / 46) * 0.006;
  const mapZoom = mapZoomAt(frame, tl) * breathe;

  return (
    <AbsoluteFill style={{ fontFamily: FONT_TEXT, backgroundColor: theme.pageTop }}>
      {/* ナレーション（ビルドツーリングが算出した startFrame へ配置する） */}
      {Object.values(cues)
        .filter((cue) => cue.audioSrc)
        .map((cue) => (
          <Sequence key={cue.id} from={cue.startFrame} durationInFrames={180} layout="none">
            <Audio src={staticFile(cue.audioSrc as string)} />
          </Sequence>
        ))}

      <Backdrop theme={theme} backgroundSrc={backgroundSrc} total={tl.total} />

      <TitleBand theme={theme} title={title} setLabel={labels.setLabel} />

      {/* 日本地図 */}
      <div
        style={{
          position: "absolute",
          left: MAP_BOX.left,
          top: MAP_BOX.top,
          width: MAP_BOX.width,
          height: MAP_BOX.height,
          transform: `scale(${mapZoom})`,
        }}
      >
        <JapanMap
          litCode={stage.lit}
          flash={stage.flash}
          revealed={stage.revealed}
          palette={mapPalette(theme)}
          viewBox={`${MAP_VIEWBOX.x} ${MAP_VIEWBOX.y} ${MAP_VIEWBOX.width} ${MAP_VIEWBOX.height}`}
          insetFocus={insetFocus}
        />
      </div>

      {/* 表彰台五郎 */}
      <Img
        src={staticFile(characterSrc)}
        style={{
          position: "absolute",
          left: CHARACTER.left,
          top: CHARACTER.top + bob,
          width: CHARACTER.width,
          height: "auto",
          zIndex: 5,
          transformOrigin: "center bottom",
          transform: `scale(${isAnnounced ? 0.92 + 0.12 * announcePop : 1})`,
          filter: "drop-shadow(0 14px 24px rgba(12,18,34,0.32))",
        }}
      />

      {/* 実況の吹き出し */}
      {bubbleText ? (
        <div
          style={{
            position: "absolute",
            left: BUBBLE.left,
            top: BUBBLE.top,
            zIndex: 6,
            maxWidth: BUBBLE.maxWidth,
          }}
        >
          <div
            style={{
              display: "inline-block",
              background: theme.bubbleBg,
              border: `5px solid ${theme.bubbleBorder}`,
              borderRadius: 28,
              padding: "14px 28px",
              fontFamily: FONT_DISPLAY,
              fontSize: 48,
              fontWeight: FONT_DISPLAY_WEIGHT,
              lineHeight: 1.28,
              color: theme.bubbleText,
              boxShadow: "0 12px 26px rgba(12,18,34,0.26)",
              opacity: stage.spinningRank !== null ? 0.82 + 0.18 * Math.abs(Math.sin(frame / 6)) : 1,
            }}
          >
            {bubbleText}
          </div>
          <div
            style={{
              position: "absolute",
              left: 78,
              bottom: -20,
              width: 0,
              height: 0,
              borderLeft: "17px solid transparent",
              borderRight: "17px solid transparent",
              borderTop: `23px solid ${theme.bubbleBorder}`,
            }}
          />
        </div>
      ) : null}

      {/* 序盤の受け皿（全国平均） */}
      {subtitle ? <AveragePlate theme={theme} subtitle={subtitle} labels={labels} tl={tl} /> : null}

      {/* 確定県が地図から順位行へ落ちる */}
      {entries.map((entry) => (
        <FlyingName
          key={`fly-${entry.rank}`}
          entry={entry}
          theme={theme}
          tl={tl}
          zoom={mapZoom}
          insetFocused={focusesInset}
        />
      ))}
      <Burst
        at={announceAt}
        origin={
          focusesInset
            ? mapPointZoomed(
                MAP_INSET_PANEL.x + MAP_INSET_PANEL.width / 2,
                MAP_INSET_PANEL.y + MAP_INSET_PANEL.height / 2,
                mapZoom
              )
            : { x: 540, y: LIST_TOP - 190 }
        }
        theme={theme}
      />

      {/* 順位行スタック（下端固定・5 位から上へ積み上がる） */}
      {entries.map((entry) => (
        <RankRow
          key={entry.rank}
          entry={entry}
          theme={theme}
          valuePrefix={valuePrefix}
          valueSuffix={valueSuffix}
          labels={labels}
          tl={tl}
        />
      ))}

      <SourceBand theme={theme} text={sourceDisplay} />
    </AbsoluteFill>
  );
};
