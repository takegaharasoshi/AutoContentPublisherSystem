import { z } from "zod";

/**
 * コンポジションの props。build.py が work/props/<content_key>.json に書き出し、
 * `npx remotion render --props` で渡す。パスはすべて public/ からの相対パス（staticFile で解決）。
 */
export const umigameReelSchema = z.object({
  contentKey: z.string(),
  /** つかみ帯（フック文） */
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
    problem: z.object({ file: z.string(), frames: z.number().int() }),
    rule: z.object({ file: z.string(), frames: z.number().int() }),
  }),
  bgm: z.string(),
  bubbleSe: z.string(),
});

export type UmigameReelProps = z.infer<typeof umigameReelSchema>;
