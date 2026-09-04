import type { UmigameReelProps } from "./props";

/**
 * Studio プレビュー用の既定 props（build.py が書く work/props/*.json と同じ形）。
 * public/ に PoC 素材が配置されている前提（README「事前準備」）。
 */
export const mockProps: UmigameReelProps = {
  contentKey: "classic-umigame",
  hook: "この男はなぜ死んだ？",
  problemText:
    "ある男が海辺のレストランでウミガメのスープを注文した。ひと口飲んだ男は店員に本当にウミガメのスープかと確かめ、「はい」と聞くと店を出て自ら命を絶った。なぜ？",
  ruleText: "「はい / いいえ / 関係ない」で答えられる質問をコメントしてね。出題者が全部返事します",
  background: "bg/classic-umigame.jpg",
  master: { name: "カメロック", base: "char/master_base.png", happy: "char/master_happy.png" },
  assistant: { name: "クマ助", base: "char/assistant_base.png" },
  masterLines: {
    intro: "質問してみて！",
    outro: "何度でも答えるよ。コメントで質問！",
  },
  playExample: [
    { role: "questioner", text: "スープに毒が入ってた？" },
    { role: "master", text: "いいえ。" },
    { role: "questioner", text: "男は昔、海で何かあった？" },
    { role: "master", text: "はい！" },
    { role: "questioner", text: "店員が犯人？" },
    { role: "master", text: "関係ありません。" },
  ],
  narration: {
    problem: { file: "narration/classic-umigame/problem.wav", frames: 313 },
    rule: { file: "narration/classic-umigame/rule.wav", frames: 164 },
  },
  bgm: "audio/bgm.m4a",
  bubbleSe: "audio/se_pop.wav",
};
