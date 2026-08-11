import React from "react";
import { CalculateMetadataFunction, Composition } from "remotion";
import { PrefRankingProps, PrefRankingVideo } from "./PrefRankingVideo";
import { MOCK_PROPS_20S, MOCK_PROPS_30S } from "./mockProps";
import { TIMELINES } from "./timeline";

const calculateMetadata: CalculateMetadataFunction<PrefRankingProps> = ({ props }) => {
  const timeline = TIMELINES[props.duration];
  return {
    durationInFrames: timeline.total,
    fps: timeline.fps,
  };
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PrefRanking20s"
        component={PrefRankingVideo}
        width={1080}
        height={1920}
        defaultProps={MOCK_PROPS_20S}
        calculateMetadata={calculateMetadata}
      />
      <Composition
        id="PrefRanking30s"
        component={PrefRankingVideo}
        width={1080}
        height={1920}
        defaultProps={MOCK_PROPS_30S}
        calculateMetadata={calculateMetadata}
      />
    </>
  );
};
