-- umigame-soup-1 セット登録 (4/4): 稼働開始（batch_sets の有効化）
-- **cdk deploy（SnsPostBatchStack のスナップショット PUT 権限・ImageBatchStack / InsightsBatchStack の
--   Scheduler）の後、1 本目の手動実行の直前に適用する**。適用した時点から 20:00 の定時実行も動く
-- （Scheduler は CDK で有効のまま置き、is_active を稼働の切り替えにする。21-7 の決定）。
-- 適用前に下の (0) でバックログ 0 件を確認する（課題体系 I-017。operation.html セクション 2.1 チェックリスト）。
-- 適用（ローカル）: docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps < set-registration/04_activate.sql
-- 適用（Aurora）:   python3 ../../ranking-stock/pref-ranking-1/common/apply_aurora.py set-registration/04_activate.sql

-- (0) 確認（適用前に単独で流す。0 件であること）: 投稿が終わっていない生成実行
--   SELECT COUNT(*) FROM generation_runs gr JOIN batch_sets b ON b.id = gr.set_id
--   WHERE b.set_code = 'umigame-soup-1'
--     AND NOT EXISTS (SELECT 1 FROM posts p WHERE p.generation_run_id = gr.id
--                     AND p.status IN ('success','failed','published_unconfirmed'))

-- (1) 方式・ストーリーズ無効・スナップショット出力を確定し、セットを有効化する
UPDATE batch_sets
SET generator_name = 'umigame-prebuilt',
    stories_enabled = 0,
    problem_snapshot_enabled = 1,
    is_active = 1
WHERE set_code = 'umigame-soup-1';
