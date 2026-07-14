# acps_shared

AutoContentPublisherSystem のバッチサービスで共通利用する DB 接続モジュールです。Secrets Manager から Aurora MySQL 接続情報を取得し、PyMySQL 接続を安全に管理します。

## 提供 API

- `get_db_secret`: Secrets Manager から DB 接続情報を取得します。
- `parse_db_secret`: SecretString の JSON を `DbSecret` に変換します。
- `connect`: PyMySQL 接続を作成します。
- `open_connection`: 接続をコンテキストマネージャーとして提供し、終了時に close します。

## 使用例

```python
from acps_shared import get_db_secret, open_connection

secret = get_db_secret("arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:db")
with open_connection(secret) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
```

## 方針

本モジュールは接続リトライを持ちません。Aurora の起動待ちを含む接続リトライは、DB 準備確認タスク（`db-readiness-check`）の責務です。
