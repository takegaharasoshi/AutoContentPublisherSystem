import { z } from "zod";

/**
 * コンポジションの props。build.py が work/props/<content_key>.json に書き出し、
 * `npx remotion render --props` で渡す。パスはすべて public/ からの相対パス（staticFile で解決）。
 */
export const umigameReelSchema = z.object({
  contentKey: z.string(),
  /** 導入シーンの固定の文言（全問共通。assets/design.json の opening。R-1-2 で決定） */
  opening: z.object({
    /** 傾けたスタンプ（「新体験」） */
    badge: z.string(),
    /** 見出し（1〜2 行） */
    headline: z.array(z.string()).min(1).max(2),
    /** 説明文（行ごとの文字片。em = accent は朱色の文字、tag は黄色のタグ） */
    lead: z.array(z.array(z.object({ text: z.string(), em: z.enum(["accent", "tag"]).optional() }))).min(1).max(2),
    /** hook のカードのラベル（「今日の謎」） */
    hookLabel: z.string(),
    /** キャラの自己紹介の吹き出し */
    selfIntro: z.object({ master: z.string(), jr: z.string() }),
  }),
  /** つかみ帯（フック文）。導入シーンでは中央に大きく出す */
  hook: z.string(),
  /** 問題文（全文・段階表示しない） */
  problemText: z.string(),
  /** ルール帯（常時表示） */
  ruleText: z.string(),
  /** 背景イラスト（public/ 相対。JPEG） */
  background: z.string(),
  /** 出題者（カメロック）。happy は返答が「はい」のときのポーズ */
  master: z.object({
    name: z.string(),
    base: z.string(),
    happy: z.string(),
  }),
  /** 質問者（カメロック Jr.） */
  jr: z.object({
    name: z.string(),
    base: z.string(),
  }),
  /** 出題者の導入・締めのセリフ */
  masterLines: z.object({
    intro: z.string(),
    outro: z.string(),
  }),
  /** Jr. の締めのセリフ（いいね・フォロー） */
  jrLines: z.object({
    outro: z.string(),
  }),
  /** プレイ例（質問 → 返答の順で 3 往復 = 6 件）。返答に「はい」を含むと出題者が喜ぶポーズになる */
  playExample: z
    .array(z.object({ role: z.enum(["questioner", "master"]), text: z.string() }))
    .length(6),
  narration: z.object({
    /** 導入シーンの見出しの読み上げ（全問共通） */
    opening: z.object({ file: z.string(), frames: z.number().int() }),
    problem: z.object({ file: z.string(), frames: z.number().int() }),
    rule: z.object({ file: z.string(), frames: z.number().int() }),
  }),
  bgm: z.string(),
  bubbleSe: z.string(),
});

export type UmigameReelProps = z.infer<typeof umigameReelSchema>;
