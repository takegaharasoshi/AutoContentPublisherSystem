/**
 * 版面の導出値を JSON で吐く検査用エントリ。
 *
 * 版面の導出（design.ts）は TypeScript 側にしか無いため、pytest からは
 * esbuild でこのファイルを束ねて node で実行し、出力値を突き合わせる
 * （tests/test_layout_design.py）。Remotion のコンポジションからは参照しない。
 *
 * 使い方: 標準入力に QuizProps の配列を渡すと、同じ順で導出値の要約を返す。
 */

import { readFileSync } from "node:fs";

import { deriveDesign, type QuizProps } from "./design";

const propsList = JSON.parse(readFileSync(0, "utf8")) as QuizProps[];

const summary = propsList.map((props) => {
  const design = deriveDesign(props);
  return {
    hook: {
      fontSize: design.band.text.fontSize,
      lineCount: design.band.text.lines.length,
    },
    question: {
      fontSize: design.question.text.fontSize,
      lineCount: design.question.text.lines.length,
      lines: design.question.text.lines,
      top: design.question.top,
      height: design.question.text.height,
    },
    illustrationBox: design.illustrationBox,
    illustration: {
      ...design.illustration,
      width: design.illustration.right - design.illustration.left,
      height: design.illustration.bottom - design.illustration.top,
    },
  };
});

console.log(JSON.stringify(summary));
