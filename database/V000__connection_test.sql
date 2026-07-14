-- V000__connection_test.sql
-- Phase 6 接続確認用テーブル（本スキーマ V001__initial_schema.sql とは独立）
--
-- 用途: ECS タスク（image-batch / sns-post-batch）から Aurora への接続疎通確認
-- （INSERT / SELECT が成功すること）。Phase 6-3 で AWS Console の Query Editor から
-- Aurora に適用する。ローカル接続テスト（Phase 6-2）では MySQL コンテナの初期化にも使用する。

CREATE TABLE connection_test (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主キー',
    service_name VARCHAR(50) NOT NULL COMMENT '接続確認を実行したサービス名',
    executed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '実行日時（UTC）',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='接続確認用（Phase 6）。本スキーマとは独立で、Phase 10 以降に削除してよい';
