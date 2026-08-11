// 本組みの版面確認用サンプル（第 1 バッチ 001 ぎょうざ）。
// 実データは content/ranking-stock/pref-ranking-1/2026-08-initial/stock_items.py が正。

import { Cue, DEFAULT_LABELS, PrefRankingProps } from "./PrefRankingVideo";
import { cueAnchorFrame, Timeline, TIMELINE_20S, TIMELINE_30S } from "./timeline";

const COMMON_PROPS: Omit<PrefRankingProps, "duration" | "cues"> = {
  title: "ぎょうざ大好き都道府県",
  subtitle: "全国平均は1,984円",
  sourceDisplay:
    "総務省 家計調査 2023〜25年平均／二人以上世帯の年間支出（政令市等を世帯数加重で県換算）",
  valuePrefix: "年間",
  valueSuffix: "円",
  backgroundSrc: "bg/001-gyoza-spend.jpg",
  bgmSrc: null,
  entries: [
    { rank: 1, prefCode: 45, prefName: "宮崎県", value: 3478 },
    { rank: 2, prefCode: 9, prefName: "栃木県", value: 3192 },
    { rank: 3, prefCode: 22, prefName: "静岡県", value: 3091 },
    { rank: 4, prefCode: 25, prefName: "滋賀県", value: 2455 },
    { rank: 5, prefCode: 11, prefName: "埼玉県", value: 2412 },
  ],
  labels: DEFAULT_LABELS,
};

const mockCues = (tl: Timeline, texts: Record<string, string>): Record<string, Cue> =>
  Object.fromEntries(
    Object.entries(texts).map(([id, text]) => [
      id,
      {
        id,
        text,
        audioSrc: null,
        // モックは音声がなく県名開始位置を実測できないため、name cue もアンカー値を置く。
        // 本番は build_timeline.resolve_cue_frames が後ろ合わせした startFrame を渡す。
        startFrame: cueAnchorFrame(tl, id),
      },
    ])
  );

export const MOCK_PROPS_20S: PrefRankingProps = {
  ...COMMON_PROPS,
  duration: "20s",
  cues: mockCues(TIMELINE_20S, {
    intro: "ぎょうざ大好き都道府県！",
    teaser: "みんなはどこだと思う？",
    r5: "まずは5位、埼玉県！",
    r4: "つぎは4位、滋賀県！",
    r3: "3位は、静岡県！",
    r2: "惜しくも2位、栃木県！",
    r1_call: "さあ、栄えある1位は！",
    r1_name: "宮崎県ーっ！",
    outro: "みんなはわかったかな？",
  }),
};

export const MOCK_PROPS_30S: PrefRankingProps = {
  ...COMMON_PROPS,
  duration: "30s",
  cues: mockCues(TIMELINE_30S, {
    intro: "ぎょうざ大好き都道府県、トップ5！",
    teaser: "1位はどこだと思う？",
    r5: "第5位は、埼玉県！",
    r5_comment: "関東から来た！",
    r4: "第4位は、滋賀県！",
    r4_comment: "まさかの近江！",
    r3: "第3位は、静岡県！",
    r3_comment: "浜松の力だ！",
    r2: "第2位は、栃木県！",
    r2_comment: "本場の意地！",
    r1_call: "さあ第1位、ぎょうざ王は！",
    r1_name: "宮崎県ーっ！",
    closing: "宇都宮と浜松をおさえて、宮崎が王座だ！",
  }),
};
