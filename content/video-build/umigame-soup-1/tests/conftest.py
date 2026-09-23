"""テスト対象ディレクトリを import パスへ追加する。"""

from __future__ import annotations

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
