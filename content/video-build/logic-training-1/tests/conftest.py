"""logic-training-1 ビルドツールのテスト設定。"""

from pathlib import Path
import sys


BASE = Path(__file__).resolve().parent.parent
SCRIPTS = BASE / "remotion" / "scripts"
for source_root in (BASE, SCRIPTS):
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))
