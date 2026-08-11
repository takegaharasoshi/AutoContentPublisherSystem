import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// モジュールトップレベルで呼ぶ（コンポーネント内は不可）
loadFont({
  family: "NotoSansJP",
  url: staticFile("fonts/NotoSansJP-Regular.otf"),
  weight: "400",
});

loadFont({
  family: "NotoSansJP",
  url: staticFile("fonts/NotoSansJP-Bold.otf"),
  weight: "700",
});

export const FONT_FAMILY = "NotoSansJP, sans-serif";
