/**
 * 日本語の行分割（禁則処理つき）とフォントサイズの自動決定。
 *
 * ブラウザの自動折り返しに任せず自前で行に割るのは、**行ごとに段階表示する**
 * ため（R-1-2 の動きの内容 ③「問題文の読む速さに合わせた段階表示」）に
 * 行の配列が必要だから。禁則の文字集合は現行レンダラー
 * （gpt_quiz_multicut.LINE_START_PROHIBITED / LINE_END_PROHIBITED）と同じ。
 *
 * 文字幅は実測せず字種で見積もる。Noto Sans JP の CJK は 1em 固定なので
 * 日本語主体の文では誤差が出ない。ASCII は安全側（やや広め）に見積もる。
 */

export const LINE_START_PROHIBITED =
  "、。，．,.)）]］｝」』】〉》!！?？:：;；ー〜…‥・%％℃";
export const LINE_END_PROHIBITED = "（(「『【〈《[［｛";

/** 1 文字の推定幅（em 単位） */
export const charEm = (char: string): number => {
  const code = char.codePointAt(0) ?? 0;
  if (char === " ") return 0.28;
  if (code < 0x80) return 0.62; // ASCII は安全側に広く見積もる
  if (code >= 0xff61 && code <= 0xff9f) return 0.5; // 半角カナ
  return 1;
};

export const measureEm = (chars: readonly string[]): number =>
  chars.reduce((total, char) => total + charEm(char), 0);

/** 禁則を守って 1 つの font size で行に割る */
export const wrapLines = (
  text: string,
  fontSize: number,
  maxWidth: number,
): string[] => {
  const maxEm = maxWidth / fontSize;
  const lines: string[] = [];
  let current: string[] = [];
  let currentEm = 0;

  const flush = () => {
    lines.push(current.join(""));
    current = [];
    currentEm = 0;
  };

  for (const char of Array.from(text)) {
    if (char === "\n") {
      flush();
      continue;
    }
    const em = charEm(char);
    if (current.length > 0 && currentEm + em > maxEm) {
      if (LINE_START_PROHIBITED.includes(char)) {
        // 行頭禁止文字はぶら下げて、その行を閉じる
        current.push(char);
        flush();
        continue;
      }
      // 行末禁止文字は次の行へ送る
      const carry: string[] = [];
      while (
        current.length > 0 &&
        LINE_END_PROHIBITED.includes(current[current.length - 1])
      ) {
        carry.unshift(current.pop() as string);
      }
      const line = current.join("");
      current = [];
      currentEm = 0;
      lines.push(line);
      current = [...carry, char];
      currentEm = measureEm(current);
      continue;
    }
    current.push(char);
    currentEm += em;
  }
  if (current.length > 0) flush();
  return lines.length > 0 ? lines : [""];
};

export type FittedText = {
  fontSize: number;
  lines: string[];
  lineHeight: number;
  height: number;
};

/**
 * 枠に収まる最大のフォントサイズで行に割る。
 * `preferSingleLine` を立てると、1 行に収まるサイズを最優先する
 * （つかみ帯。「1％の人だけが30秒で解／ける」のような改行を避けるため）。
 */
export const fitText = (
  text: string,
  options: {
    maxWidth: number;
    maxHeight: number;
    maxFontSize: number;
    minFontSize: number;
    lineRatio: number;
    step?: number;
    preferSingleLine?: boolean;
  },
): FittedText => {
  const step = options.step ?? 2;
  let fallback: FittedText | null = null;
  for (
    let fontSize = options.maxFontSize;
    fontSize >= options.minFontSize;
    fontSize -= step
  ) {
    const lines = wrapLines(text, fontSize, options.maxWidth);
    const lineHeight = Math.round(fontSize * options.lineRatio);
    const height = lines.length * lineHeight;
    const fitted = { fontSize, lines, lineHeight, height };
    if (options.preferSingleLine && lines.length === 1) return fitted;
    if (height <= options.maxHeight) {
      if (options.preferSingleLine) {
        fallback = fallback ?? fitted;
        continue;
      }
      return fitted;
    }
  }
  if (fallback) return fallback;
  const fontSize = options.minFontSize;
  const lines = wrapLines(text, fontSize, options.maxWidth);
  const lineHeight = Math.round(fontSize * options.lineRatio);
  return { fontSize, lines, lineHeight, height: lines.length * lineHeight };
};
