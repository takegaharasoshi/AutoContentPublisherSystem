-- pref-ranking-1 セット登録 (2/3): sns_accounts
-- **Secrets Manager に acps/prod/pref-ranking-1/sns/instagram/main-account を作ってから適用する**
-- （Secret より先に登録すると投稿バッチが認証情報を取得できず即失敗する。
--   docs/app/operation.html セクション 2.1 手順 1 / 5.1）。
-- 値の正は docs/app/sets/pref-ranking-1.html セクション 2。
-- 適用（ローカル）: docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps < 02_sns_account.sql
-- 適用（Aurora）:   python3 ../common/apply_aurora.py set-registration/02_sns_account.sql

INSERT INTO sns_accounts (set_id, platform, account_code, account_name, is_active)
SELECT b.id, 'instagram', 'main-account', '表彰台五郎の都道府県ランキング', 1
FROM batch_sets b
WHERE b.set_code = 'pref-ranking-1';
