import React from "react";
import { Composition } from "remotion";

import { MOCK_PROPS } from "./mockProps";
import { QuizVideo } from "./QuizVideo";
import { FPS, TOTAL_FRAMES } from "./timeline";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Quiz16s"
      component={QuizVideo}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={TOTAL_FRAMES}
      defaultProps={MOCK_PROPS}
    />
  );
};
