/**
 * 導入シーンの hook を 2 行に割る（R-1-1）。ブラウザの自動改行は語の途中で割れるため
 * （「子どもたちの行 / 動の真相は？」）、助詞・読点・形容詞の語尾「い」の直後のうち、長いほうの行が
 * 最も短くなる位置で割る（同じなら中央に近いほう）。割れる位置がなければ中央で割る。1 行に収まる長さ（maxPerLine 以下）なら割らない。
 */
const BREAK_AFTER = new Set(["の", "は", "が", "を", "に", "で", "と", "て", "い", "、", "　"]);

export const splitOpeningHook = (hook: string, maxPerLine: number): string[] => {
  const chars = [...hook];
  if (chars.length <= maxPerLine) return [hook];
  const middle = chars.length / 2;
  const longer = (at: number) => Math.max(at, chars.length - at);
  let best = -1;
  for (let i = 1; i < chars.length - 1; i += 1) {
    // 先頭の i 文字で割る。末尾の「？」だけが次行に残る割り方はしない（i < length - 1）
    if (!BREAK_AFTER.has(chars[i - 1])) continue;
    if (
      best < 0 ||
      longer(i) < longer(best) ||
      (longer(i) === longer(best) && Math.abs(i - middle) < Math.abs(best - middle))
    ) {
      best = i;
    }
  }
  const at = best < 0 ? Math.ceil(middle) : best;
  return [chars.slice(0, at).join(""), chars.slice(at).join("")];
};

/** 2 行（または 1 行）の最長行が内寸に収まる文字サイズ（上限 maxFontSize） */
export const openingHookFontSize = (lines: string[], innerWidth: number, maxFontSize: number): number =>
  Math.min(maxFontSize, Math.floor(innerWidth / Math.max(...lines.map((line) => [...line].length))));
