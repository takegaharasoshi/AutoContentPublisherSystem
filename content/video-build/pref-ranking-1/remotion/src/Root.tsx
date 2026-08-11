import React from "react";
import { Composition } from "remotion";
import { PrefRankingVideo } from "./PrefRankingVideo";
import { MOCK_PROPS } from "./mockProps";
import { TIMELINE_20S } from "./timeline";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PrefRanking20s"
        component={PrefRankingVideo}
        durationInFrames={TIMELINE_20S.total}
        fps={TIMELINE_20S.fps}
        width={1080}
        height={1920}
        defaultProps={MOCK_PROPS}
      />
    </>
  );
};
