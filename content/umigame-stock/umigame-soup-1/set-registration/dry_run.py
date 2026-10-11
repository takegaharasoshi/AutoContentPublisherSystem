"""Dry-run the umigame-soup-1 set registration SQL on the local MySQL.

The scripts run inside one transaction on the docker ``acps-mysql`` container,
the registered rows are printed, and the transaction is rolled back.
``03_audio_assets.sql`` is included only when the set has no BGM row yet
(it has no NOT EXISTS guard because ``prepare_bgm.py`` generates it).

Usage:
    python3 dry_run.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MYSQL = [
    "docker", "exec", "-i", "acps-mysql",
    "mysql", "--default-character-set=utf8mb4", "-uroot", "-proot", "acps",
]
CHECK_SQL = """
SELECT b.id AS set_id, b.generator_name, b.stories_enabled,
       b.problem_snapshot_enabled, b.is_active
FROM batch_sets b WHERE b.set_code = 'umigame-soup-1';
SELECT p.parameters, LEFT(p.prompt_text, 40) AS prompt_text_head
FROM prompt_configs p JOIN batch_sets b ON b.id = p.set_id
WHERE b.set_code = 'umigame-soup-1' AND p.is_active = 1;
SELECT c.template_text FROM caption_templates c JOIN batch_sets b ON b.id = c.set_id
WHERE b.set_code = 'umigame-soup-1' AND c.is_active = 1;
SELECT s.platform, s.account_code, s.account_name FROM sns_accounts s
JOIN batch_sets b ON b.id = s.set_id WHERE b.set_code = 'umigame-soup-1';
SELECT a.s3_key, a.asset_type, a.time_slot FROM audio_assets a
JOIN batch_sets b ON b.id = a.set_id
WHERE b.set_code = 'umigame-soup-1' AND a.is_active = 1;
SELECT COUNT(*) AS built_stock FROM umigame_stock_items u
JOIN batch_sets b ON b.id = u.set_id
WHERE b.set_code = 'umigame-soup-1' AND u.is_active = 1 AND u.video_s3_key IS NOT NULL;
"""


def run_mysql(sql: str) -> subprocess.CompletedProcess[str]:
    """Run SQL text on the local MySQL container.

    Args:
        sql: SQL script passed on stdin.

    Returns:
        The completed process with captured output.
    """
    return subprocess.run(
        MYSQL + ["-t"], input=sql, capture_output=True, text=True, timeout=120
    )


def main() -> int:
    """Run the dry-run and report OK / NG.

    Returns:
        Process exit code (0 on success).
    """
    probe = run_mysql(
        "SELECT COUNT(*) FROM audio_assets a JOIN batch_sets b ON b.id = a.set_id "
        "WHERE b.set_code = 'umigame-soup-1' AND a.asset_type = 'bgm';"
    )
    if probe.returncode != 0:
        print(f"dry-run: NG（BGM 確認の mysql 終了コード {probe.returncode}）")
        print(probe.stderr.strip())
        return 1
    has_bgm = any(line.strip("| ").strip() not in ("", "0") and line.strip("| ").strip().isdigit()
                  for line in probe.stdout.splitlines())
    files = ["01_prompt_caption.sql", "02_sns_account.sql"]
    if not has_bgm:
        files.append("03_audio_assets.sql")
    files.append("04_activate.sql")
    print(f"dry-run: 対象 {', '.join(files)}（BGM 登録済み: {has_bgm}）")

    parts = ["START TRANSACTION;"]
    parts += [(HERE / name).read_text(encoding="utf-8") for name in files]
    parts += [CHECK_SQL, "ROLLBACK;"]
    result = run_mysql("\n".join(parts))
    print(result.stdout)
    errors = [line for line in result.stderr.splitlines() if "Warning" not in line]
    if result.returncode != 0 or errors:
        print(f"dry-run: NG（mysql 終了コード {result.returncode}）")
        print("\n".join(errors))
        return 1
    print("dry-run: OK（ROLLBACK 済み）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
