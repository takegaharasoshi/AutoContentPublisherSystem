import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

/**
 * フォント（pref-ranking-1 と同じ Zen Kaku Gothic New / SIL OFL 1.1。build.py が public/fonts/ へ配置する）。
 * 見出しは 1 ファイルを専用 family 名で weight 400 として読み込む（同一 family に複数ウェイトを
 * 登録すると細い字面が選ばれる事象があったため。pref-ranking-1 17-4b）。
 * remotion-markup の local-fonts.md の指針どおり @remotion/fonts の loadFont を使う。
 */
loadFont({ family: "DisplayZenKakuBlack", url: staticFile("fonts/ZenKakuGothicNew-Black.ttf"), weight: "400" });
loadFont({ family: "ZenKakuGothicNew", url: staticFile("fonts/ZenKakuGothicNew-Medium.ttf"), weight: "400" });
loadFont({ family: "ZenKakuGothicNew", url: staticFile("fonts/ZenKakuGothicNew-Bold.ttf"), weight: "700" });

export const FONT_DISPLAY = "DisplayZenKakuBlack, sans-serif";
export const FONT_TEXT = "ZenKakuGothicNew, sans-serif";
