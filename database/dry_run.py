"""Dry-run the DDL files on a throwaway database of the local MySQL.

A scratch database is created on the docker ``acps-mysql`` container, every
``V*.sql`` up to the target is applied in version order, the target's tables
and views are listed, and the scratch database is dropped. The working
``acps`` database is never touched (DDL commits implicitly, so a rollback-based
dry-run is not possible).

Usage:
    python3 database/dry_run.py --dry-run V016
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRATCH_DB = "acps_ddl_dry_run"
MYSQL = [
    "docker", "exec", "-i", "acps-mysql",
    "mysql", "--default-character-set=utf8mb4", "-uroot", "-proot",
]


def run_mysql(sql: str, database: str | None = None) -> subprocess.CompletedProcess[str]:
    """Run SQL text on the local MySQL container.

    Args:
        sql: SQL script passed on stdin.
        database: Database to select, or None for no default database.

    Returns:
        The completed process with captured output.
    """
    command = MYSQL + ["-t"] + ([database] if database else [])
    return subprocess.run(command, input=sql, capture_output=True, text=True, timeout=300)


def ddl_files(target: str) -> list[Path]:
    """Return V001 .. target DDL files in version order.

    Args:
        target: Version prefix such as ``V016``.

    Returns:
        DDL paths sorted by version number.
    """
    limit = int(target.lstrip("Vv"))
    files = []
    for path in HERE.glob("V*__*.sql"):
        version = int(re.match(r"V(\d+)__", path.name).group(1))
        if 1 <= version <= limit:
            files.append((version, path))
    return [path for _, path in sorted(files)]


def main() -> int:
    """Apply the DDL chain to a scratch database and report OK / NG.

    Returns:
        Process exit code (0 = OK).
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", required=True, metavar="VERSION",
                        help="target version to verify (e.g. V016)")
    args = parser.parse_args()
    files = ddl_files(args.dry_run)
    reset = f"DROP DATABASE IF EXISTS {SCRATCH_DB}; CREATE DATABASE {SCRATCH_DB} " \
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    result = run_mysql(reset)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return 1
    try:
        for path in files:
            result = run_mysql(path.read_text(encoding="utf-8"), SCRATCH_DB)
            if result.returncode != 0:
                print(f"NG: {path.name}\n{result.stderr}", file=sys.stderr)
                return 1
            print(f"applied: {path.name}")
        result = run_mysql(
            "SELECT TABLE_NAME, TABLE_TYPE FROM information_schema.TABLES "
            f"WHERE TABLE_SCHEMA = '{SCRATCH_DB}' ORDER BY TABLE_TYPE, TABLE_NAME;",
        )
        print(result.stdout)
        print(f"OK: {len(files)} files applied to scratch database {SCRATCH_DB}")
        return 0
    finally:
        run_mysql(f"DROP DATABASE IF EXISTS {SCRATCH_DB};")


if __name__ == "__main__":
    sys.exit(main())
