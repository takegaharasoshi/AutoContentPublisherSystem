// 背景レビュー用の静止フレームを、動画をレンダリングせずに書き出す（background_sheet.py --stills から Docker で呼ぶ）。
// 使い方: node scripts/render_stills.mjs <job.json>
//   job.json = {"frames": {"intro": 45, ...}, "items": [{"props": "<props.json>", "out": "<出力の接頭辞>"}]}
//   出力: <out>_<label>.jpg
// バンドルは 1 回だけ作り、全問・全フレームで使い回す。
import { readFileSync } from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";

const COMPOSITION_ID = "UmigameReel24s";

const job = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const serveUrl = await bundle({
  entryPoint: path.join(root, "src/index.ts"),
  publicDir: path.join(root, "public"),
  rspack: true,
});

for (const item of job.items) {
  const inputProps = JSON.parse(readFileSync(item.props, "utf-8"));
  const composition = await selectComposition({ serveUrl, id: COMPOSITION_ID, inputProps });
  for (const [label, frame] of Object.entries(job.frames)) {
    await renderStill({
      composition,
      serveUrl,
      inputProps,
      frame,
      output: `${item.out}_${label}.jpg`,
      imageFormat: "jpeg",
      jpegQuality: 80,
      overwrite: true,
    });
  }
  console.log(`ok ${item.out}`);
}
