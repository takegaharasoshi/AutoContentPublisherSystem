// 定数の正は scripts/build_timeline.py。timeline.json は生成物なので手で編集しない。

import timelineJson from "./timeline.json";

export type Duration = "20s" | "30s";

export type RoundTiming = {
  /** スピン開始フレーム */
  start: number;
  /** スピン長（フレーム） */
  spin: number;
  /** 停止フラッシュ（= 確定）フレーム */
  stop: number;
  /** 地図上の県名ラベルが行へ飛び始めるフレーム */
  flyStart: number;
  /** 飛翔の長さ */
  flyDur: number;
  /** 順位行が現れるフレーム */
  rowAt: number;
  /** 順位コメントの開始。コメントがない尺は null */
  commentAt: number | null;
  /** 当該順位シーンの終了 */
  end: number;
};

export type CueAnchor = {
  id: string;
  align: "head" | "name";
  anchor: number;
  budgetStart: number;
  budgetEnd: number;
};

export type Timeline = {
  duration: Duration;
  fps: number;
  total: number;
  /** 煽りシーン（teaser）の開始 */
  teaserAt: number;
  /** 結果総覧シーンの開始。総覧がない尺は null */
  recapAt: number | null;
  /** 締め区間（結果総覧を含む）の開始 */
  closingAt: number;
  rounds: Record<number, RoundTiming>;
  cueAnchors: CueAnchor[];
};

type GeneratedTimeline = Omit<Timeline, "rounds"> & {
  rounds: Record<string, RoundTiming>;
};

const loadTimeline = (duration: Duration): Timeline => {
  const generated = timelineJson.durations[duration] as GeneratedTimeline;
  return {
    ...generated,
    rounds: Object.fromEntries(
      Object.entries(generated.rounds).map(([rank, timing]) => [Number(rank), timing])
    ) as Record<number, RoundTiming>,
  };
};

export const TIMELINES: Record<Duration, Timeline> = {
  "20s": loadTimeline("20s"),
  "30s": loadTimeline("30s"),
};

export const TIMELINE_20S = TIMELINES["20s"];
export const TIMELINE_30S = TIMELINES["30s"];

export const cueAnchorFrame = (tl: Timeline, cueId: string): number =>
  tl.cueAnchors.find((cue) => cue.id === cueId)?.anchor ?? 0;
