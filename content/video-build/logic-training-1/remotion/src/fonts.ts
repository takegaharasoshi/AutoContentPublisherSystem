import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

/**
 * 書体は現行版（Pillow 組版）と同じ Noto Sans JP のままにする。
 * R-1 で変えるのはレンダラー・動き・上部の余白だけで、書体の変更は
 * 比較（現行版と並べて見る）を濁らせるため行わない。
 */
export const FONT_FAMILY = "NotoSansJP";

loadFont({
  family: FONT_FAMILY,
  url: staticFile("fonts/NotoSansJP-Regular.otf"),
  weight: "400",
});
loadFont({
  family: FONT_FAMILY,
  url: staticFile("fonts/NotoSansJP-Bold.otf"),
  weight: "700",
});

export const FONT_STACK = `${FONT_FAMILY}, sans-serif`;
