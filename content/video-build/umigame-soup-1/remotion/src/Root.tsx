import { Composition } from "remotion";
import { UmigameReel } from "./UmigameReel";
import { mockProps } from "./mockProps";
import { umigameReelSchema } from "./props";
import { FPS, HEIGHT, TOTAL_FRAMES, WIDTH } from "./timeline";

export const COMPOSITION_ID = "UmigameReel24s";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id={COMPOSITION_ID}
      component={UmigameReel}
      durationInFrames={TOTAL_FRAMES}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
      schema={umigameReelSchema}
      defaultProps={mockProps}
    />
  );
};
