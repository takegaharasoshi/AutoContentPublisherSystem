"""周期アニメーションの周期がすべて 480 フレームの約数であることを確かめる。

R-1-1 でループ視聴（平均再生時間 > 16 秒）が実証されたため、周期アニメーションは
16 秒末尾の状態が 0 秒の状態に一致していなければならない。周期が 480 の約数なら
sin / cos / phase の値は frame 0 と frame 480 で厳密に一致する。

同じ検査は `src/timeline.ts` のモジュール読み込み時にも入っている（レンダリングが
通れば違反していない）。本スクリプトは証跡を一覧で出すためのもの。
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

TOTAL_FRAMES = 480
TIMELINE = Path(__file__).resolve().parents[1] / "src" / "timeline.ts"
BLOCK = re.compile(r"export const LOOP_PERIODS = \{(.*?)\n\} as const;", re.S)
ENTRY = re.compile(r"^\s*(\w+):\s*(\d+),", re.M)


def main() -> int:
    """Print every declared period with its divisor check and fail on violations."""
    source = TIMELINE.read_text(encoding="utf-8")
    block = BLOCK.search(source)
    if block is None:
        raise RuntimeError("LOOP_PERIODS が timeline.ts に見つかりません")
    entries = ENTRY.findall(block.group(1))
    if not entries:
        raise RuntimeError("LOOP_PERIODS が空です")
    divisors = [n for n in range(1, TOTAL_FRAMES + 1) if TOTAL_FRAMES % n == 0]
    print(f"TOTAL_FRAMES = {TOTAL_FRAMES} (16s x 30fps)")
    print(f"約数: {', '.join(str(n) for n in divisors)}\n")
    violations = 0
    for name, value in entries:
        period = int(value)
        ok = TOTAL_FRAMES % period == 0
        violations += 0 if ok else 1
        seconds = period / 30
        print(
            f"  {'OK ' if ok else 'NG '} {name:<20} {period:>4} frames "
            f"({seconds:>5.2f}s)  480/{period} = {TOTAL_FRAMES / period:g}"
        )
    print(f"\n{len(entries)} 件中 違反 {violations} 件")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
