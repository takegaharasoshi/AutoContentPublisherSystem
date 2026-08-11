import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

/**
 * 版面のフォント。役割は 2 つだけ。
 * - FONT_DISPLAY: 見出し（タイトル帯・順位行の県名・実況の吹き出し）。書体の性格が出る場所
 * - FONT_TEXT:    それ以外（数値・出典行・全国平均プレート）。可読性を優先する場所
 *
 * 見出しは**ファイル 1 本を専用の family 名で weight 400 として読み込み、常に 400 で描く**。
 * 同一 family へ複数ウェイトを登録するとブラウザのウェイト解決に委ねることになり、
 * 太い字面を選んだつもりが細い方で描かれる（17-4b の比較で実際に起きた）。
 *
 * 組み合わせは FONT_SET で切り替える（環境変数 REMOTION_FONT_SET でも指定できる。
 * 比較レンダリング用）。読み込むのは選ばれた組み合わせのファイルだけ。
 */

/** 本文フォントの候補（family 名 → 読み込むファイル） */
const TEXT_FACES = {
  NotoSansJP: [
    { file: "fonts/NotoSansJP-Regular.otf", weight: "400" },
    { file: "fonts/NotoSansJP-Bold.otf", weight: "700" },
  ],
  ZenKakuGothicNew: [
    { file: "fonts/ZenKakuGothicNew-Medium.ttf", weight: "400" },
    { file: "fonts/ZenKakuGothicNew-Bold.ttf", weight: "700" },
  ],
} as const;

/** 見出しフォントの候補（専用の family 名 → ファイル 1 本） */
const DISPLAY_FACES = {
  notoBold: { family: "DisplayNotoBold", file: "fonts/NotoSansJP-Bold.otf" },
  zenKakuBlack: { family: "DisplayZenKakuBlack", file: "fonts/ZenKakuGothicNew-Black.ttf" },
  delaGothic: { family: "DisplayDelaGothic", file: "fonts/DelaGothicOne-Regular.ttf" },
  zenOldMinchoBlack: { family: "DisplayZenOldMinchoBlack", file: "fonts/ZenOldMincho-Black.ttf" },
} as const;

/** 比較した組み合わせ（17-4b） */
export const FONT_SETS = {
  /** A: 17-4a までの構成（すべて Noto Sans JP） */
  noto: { display: "notoBold", text: "NotoSansJP" },
  /** B: 和モダンの定番。見出しは Zen 角ゴシック New Black、本文は同 Medium/Bold */
  zenKaku: { display: "zenKakuBlack", text: "ZenKakuGothicNew" },
  /** C: 見出しだけ極太ディスプレイ（祭りのポスター感）。本文は Zen 角ゴシック New */
  dela: { display: "delaGothic", text: "ZenKakuGothicNew" },
  /** D: 見出しは明朝（和の品位）。本文は Zen 角ゴシック New */
  mincho: { display: "zenOldMinchoBlack", text: "ZenKakuGothicNew" },
} as const;

export type FontSetKey = keyof typeof FONT_SETS;

/** 採用する組み合わせ（17-4b で Fix） */
export const FONT_SET: FontSetKey =
  (process.env.REMOTION_FONT_SET as FontSetKey | undefined) ?? "zenKaku";

const SELECTED = FONT_SETS[FONT_SET];
const DISPLAY_FACE = DISPLAY_FACES[SELECTED.display];

// モジュールトップレベルで呼ぶ（コンポーネント内は不可）
loadFont({ family: DISPLAY_FACE.family, url: staticFile(DISPLAY_FACE.file), weight: "400" });
for (const face of TEXT_FACES[SELECTED.text]) {
  loadFont({ family: SELECTED.text, url: staticFile(face.file), weight: face.weight });
}

const FALLBACK = "sans-serif";

/** 見出し用（タイトル帯・県名・吹き出し） */
export const FONT_DISPLAY = `${DISPLAY_FACE.family}, ${FALLBACK}`;
/** 見出しのウェイト（見出しは 1 ファイル 1 ウェイトで持つため常に 400） */
export const FONT_DISPLAY_WEIGHT = 400;
/** 本文・数値用 */
export const FONT_TEXT = `${SELECTED.text}, ${FALLBACK}`;
