"""読み取り専用 DB ユーザー report_ro を本番 Aurora に作る（Phase 34-1）。

``readonly_report.sql`` の文を、管理者の Secret を使って RDS Data API で 1 文ずつ流す。
パスワードは Secret ``acps/{env}/db/readonly-report`` から読み、画面・ログ・コマンド
ラインの引数に出さない（Data API への入力は権限 600 の一時ファイルで渡して消す）。
最後に ``SHOW GRANTS`` で付いた権限を表示する。

Usage:
    python3 database/users/apply_readonly_report.py --dry-run   # 流す文を伏せ字で表示するだけ
    python3 database/users/apply_readonly_report.py             # 本番に適用する
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQL_FILE = HERE / "readonly_report.sql"
DB = "acps"
DB_USER = "report_ro"
PLACEHOLDER = "{{PASSWORD}}"
MASK = "********"


def aws(args: list[str], timeout: int = 180) -> subprocess.CompletedProcess[str]:
    """aws cli を実行する（出力は取り込むだけで表示しない）。

    Args:
        args: ``aws`` に続く引数。
        timeout: 秒。

    Returns:
        実行結果。
    """
    return subprocess.run(["aws", *args], capture_output=True, text=True, timeout=timeout)


def must(result: subprocess.CompletedProcess[str], what: str) -> str:
    """失敗していたら理由を出して終わる。

    Args:
        result: aws cli の実行結果。
        what: 何をしようとしていたか。

    Returns:
        標準出力。

    Raises:
        SystemExit: 失敗したとき。
    """
    if result.returncode != 0:
        raise SystemExit(f"{what} に失敗しました: {result.stderr.strip()[:400]}")
    return result.stdout


def load_statements() -> list[str]:
    """SQL ファイルからコメントを除き、1 文ずつに分ける。

    Returns:
        文のリスト（末尾の ``;`` なし）。
    """
    text = "\n".join(
        line for line in SQL_FILE.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("--")
    )
    return [s.strip() for s in text.split(";") if s.strip()]


def check_select_only(statements: list[str]) -> None:
    """GRANT が SELECT だけであることを確かめる。

    Args:
        statements: 流す文。

    Raises:
        SystemExit: SELECT 以外の GRANT があるとき。
    """
    grants = [s for s in statements if s.upper().startswith("GRANT")]
    for grant in grants:
        if not re.fullmatch(r"GRANT SELECT ON `acps`\.\* TO 'report_ro'@'%'", grant):
            raise SystemExit(f"SELECT 以外の権限を付ける文があります: {grant}")
    if len(grants) != 1:
        raise SystemExit("GRANT は 1 文だけにしてください。")


def resolve(env: str) -> tuple[str, str, str]:
    """クラスター・管理者の Secret・読み取り専用の Secret の ARN を引く。

    Args:
        env: 環境名。

    Returns:
        (クラスター ARN, 管理者の Secret ARN, 読み取り専用の Secret ARN)。
    """
    cluster = must(aws(["rds", "describe-db-clusters", "--query",
                        "DBClusters[0].DBClusterArn", "--output", "text"]), "クラスターの取得").split()[0]

    def secret_arn(name: str) -> str:
        return must(aws(["secretsmanager", "describe-secret", "--secret-id", name,
                         "--query", "ARN", "--output", "text"]), f"Secret {name} の取得").strip()

    return cluster, secret_arn(f"acps/{env}/db/credentials"), secret_arn(f"acps/{env}/db/readonly-report")


def read_password(secret_arn: str) -> str:
    """読み取り専用の Secret からパスワードを読む（表示しない）。

    Args:
        secret_arn: Secret の ARN。

    Returns:
        パスワード。

    Raises:
        SystemExit: 形が想定と違うとき。
    """
    raw = must(aws(["secretsmanager", "get-secret-value", "--secret-id", secret_arn,
                    "--query", "SecretString", "--output", "text"]), "Secret の読み取り")
    value = json.loads(raw)
    if value.get("username") != DB_USER:
        raise SystemExit(f"Secret の username が {DB_USER} ではありません。")
    password = value.get("password", "")
    if not re.fullmatch(r"[A-Za-z0-9]{16,64}", password):
        raise SystemExit("Secret の password が英数字 16〜64 文字ではありません（引用符を含む値は流さない）。")
    return password


def execute(cluster: str, admin_secret: str, sql: str) -> dict:
    """1 文を Data API で流す（自動一時停止からの復帰を待つ）。

    Args:
        cluster: クラスター ARN。
        admin_secret: 管理者の Secret ARN。
        sql: 流す文（パスワードを含みうる）。

    Returns:
        Data API の応答。

    Raises:
        SystemExit: 失敗したとき。
    """
    payload = {"resourceArn": cluster, "secretArn": admin_secret, "database": DB, "sql": sql}
    fd, path = tempfile.mkstemp(prefix="apply-ro-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        for attempt in range(8):
            result = aws(["rds-data", "execute-statement", "--cli-input-json", f"file://{path}",
                          "--output", "json"])
            if result.returncode == 0:
                return json.loads(result.stdout)
            if "DatabaseResumingException" in result.stderr or "Communications link failure" in result.stderr:
                print(f"  (DB の起き上がり待ち {attempt + 1})", file=sys.stderr)
                time.sleep(20)
                continue
            break
    finally:
        os.unlink(path)
    # エラー文に流した文が含まれることがあるため、パスワードは伏せて出す
    raise SystemExit("SQL の実行に失敗しました: " + result.stderr.strip()[:400].replace(
        sql, "<sql>"))


def main() -> None:
    """読み取り専用 DB ユーザーを作り、付いた権限を表示する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", default="prod", help="環境名（既定 prod）")
    parser.add_argument("--dry-run", action="store_true", help="流す文を伏せ字で表示するだけ（AWS に触らない）")
    args = parser.parse_args()

    statements = load_statements()
    check_select_only(statements)
    print("流す文（パスワードは伏せ字）:")
    for statement in statements:
        print("  " + statement.replace(PLACEHOLDER, MASK) + ";")
    if args.dry_run:
        print("dry-run のため適用していません。")
        return

    cluster, admin_secret, readonly_secret = resolve(args.env)
    password = read_password(readonly_secret)
    for statement in statements:
        execute(cluster, admin_secret, statement.replace(PLACEHOLDER, password))
    grants = execute(cluster, admin_secret, f"SHOW GRANTS FOR '{DB_USER}'@'%'")
    print("付いた権限:")
    for record in grants.get("records", []):
        print("  " + re.sub(r"IDENTIFIED BY PASSWORD '[^']*'", "IDENTIFIED BY PASSWORD '<伏せ字>'",
                           str(record[0].get("stringValue", ""))))
    print("完了")


if __name__ == "__main__":
    main()
