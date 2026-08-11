// 17-4a の版面デザイン確認用サンプル（第 1 バッチ 001 ぎょうざ）。
// 実データは content/ranking-stock/pref-ranking-1/2026-08-initial/stock_items.py が正。

import { DEFAULT_LABELS, PrefRankingProps } from "./PrefRankingVideo";

export const MOCK_PROPS: PrefRankingProps = {
  title: "ぎょうざ大好き都道府県",
  subtitle: "年間1,984円",
  sourceDisplay:
    "総務省 家計調査 2023〜25年平均／二人以上世帯の年間支出（政令市等を世帯数加重で県換算）",
  valuePrefix: "年間",
  valueSuffix: "円",
  backgroundSrc: "bg/001-gyoza-spend.jpg",
  entries: [
    { rank: 1, prefCode: 45, prefName: "宮崎県", value: 3478 },
    { rank: 2, prefCode: 9, prefName: "栃木県", value: 3192 },
    { rank: 3, prefCode: 22, prefName: "静岡県", value: 3091 },
    { rank: 4, prefCode: 25, prefName: "滋賀県", value: 2455 },
    { rank: 5, prefCode: 11, prefName: "埼玉県", value: 2412 },
  ],
  cues: {
    intro: { id: "intro", text: "ぎょうざ大好き都道府県！", audioSrc: null, startFrame: 0 },
    teaser: { id: "teaser", text: "みんなはどこだと思う？", audioSrc: null, startFrame: 75 },
    r5: { id: "r5", text: "まずは5位、埼玉県！", audioSrc: null, startFrame: 135 },
    r4: { id: "r4", text: "つぎは4位、滋賀県！", audioSrc: null, startFrame: 195 },
    r3: { id: "r3", text: "3位は、静岡県！", audioSrc: null, startFrame: 255 },
    r2: { id: "r2", text: "惜しくも2位、栃木県！", audioSrc: null, startFrame: 315 },
    r1_call: { id: "r1_call", text: "さあ、栄えある1位は！", audioSrc: null, startFrame: 375 },
    r1_name: { id: "r1_name", text: "宮崎県ーっ！", audioSrc: null, startFrame: 450 },
    outro: { id: "outro", text: "みんなはわかったかな？", audioSrc: null, startFrame: 510 },
  },
  labels: DEFAULT_LABELS,
};
