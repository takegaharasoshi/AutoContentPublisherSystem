-- umigame-soup-1 セット登録 (2/4): sns_accounts
-- **Secrets Manager に acps/prod/umigame-soup-1/sns/instagram/main-account を作ってから適用する**
-- （Secret より先に登録すると投稿バッチが認証情報を取得できず即失敗する。
--   docs/app/operation.html セクション 2.1 手順 1 / 5.1）。
-- 値の正は docs/app/sets/umigame-soup-1.html セクション 2。
-- 適用（ローカル）: docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps < set-registration/02_sns_account.sql
-- 適用（Aurora）:   python3 ../../ranking-stock/pref-ranking-1/common/apply_aurora.py set-registration/02_sns_account.sql

INSERT INTO sns_accounts (set_id, platform, account_code, account_name, is_active)
SELECT b.id, 'instagram', 'main-account', 'コメントで推理！探偵カメロックのウミガメのスープ', 1
FROM batch_sets b
WHERE b.set_code = 'umigame-soup-1'
  AND NOT EXISTS (
    SELECT 1 FROM sns_accounts s
    WHERE s.set_id = b.id AND s.platform = 'instagram' AND s.account_code = 'main-account'
  );
