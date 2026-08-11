"""pref-ranking-1 ビルドツールのテスト設定。"""

from pathlib import Path
import sys


BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
