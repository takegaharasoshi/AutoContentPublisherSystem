-- 読み取り専用 DB ユーザー report_ro（成長ノートの集計用。Phase 34-1）
--
-- このファイルは V*.sql（スキーマの版）ではない。パスワードを含む文を流すため、
-- 手で実行せず apply_readonly_report.py から適用する（{{PASSWORD}} はスクリプトが
-- シークレット acps/{env}/db/readonly-report の値に置き換える。値は画面に出さない）。
-- 何度流しても同じ結果になる（ユーザーが無ければ作り、あればパスワードをそろえる）。
--
-- 付ける権限はスキーマ acps への SELECT だけ。

CREATE USER IF NOT EXISTS 'report_ro'@'%' IDENTIFIED BY '{{PASSWORD}}';

ALTER USER 'report_ro'@'%' IDENTIFIED BY '{{PASSWORD}}';

GRANT SELECT ON `acps`.* TO 'report_ro'@'%';
