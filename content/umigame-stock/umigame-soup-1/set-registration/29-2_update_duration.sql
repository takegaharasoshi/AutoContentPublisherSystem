-- 開発 29-2 (2/3): umigame-soup-1 の尺の宣言値を 29 へ揃える（I-041。画像バッチは 29-1 で 24 / 29 を許容済み）
-- 適用（ローカル）: docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps < set-registration/29-2_update_duration.sql
-- 適用（Aurora）:   python3 ../../ranking-stock/pref-ranking-1/common/apply_aurora.py set-registration/29-2_update_duration.sql
-- 流す前に 29-2_select_targets.sql で (3) の対象を確かめ、流した後に 29-2_check.sql で結果を確かめる。何度流しても結果は同じ。

-- (1) テンプレートの宣言値（次の生成から generated_media.duration_seconds に 29 が入る）
UPDATE prompt_configs p
JOIN batch_sets b ON b.id = p.set_id AND b.set_code = 'umigame-soup-1'
SET p.parameters = JSON_OBJECT('duration_seconds', 29)
WHERE p.is_active = 1 AND JSON_EXTRACT(p.parameters, '$.duration_seconds') = 24;

-- (2) BGM の尺（R-1 で 29 秒版に差し替え済みの音源に記録を合わせる）
UPDATE audio_assets a
JOIN batch_sets b ON b.id = a.set_id AND b.set_code = 'umigame-soup-1'
SET a.duration_seconds = 29,
    a.license_note = REPLACE(a.license_note, '先頭から 24 秒を使用（2026-09-24 ユーザー選曲）',
                             '先頭から 29 秒を使用（2026-09-24 ユーザー選曲。2026-10-17 の R-1 で 24 秒から延長）')
WHERE a.s3_key = 'audio/umigame-soup-1/track01.m4a' AND a.duration_seconds = 24;

-- (3) 新版面の動画で生成され 24 で記録された行（条件は 29-2_select_targets.sql と同じ）。
--     parameters_snapshot は生成時点のテンプレートの写しなので 24 のまま残す。
UPDATE generated_media gm
JOIN batch_sets b ON b.id = gm.set_id AND b.set_code = 'umigame-soup-1'
JOIN umigame_items ui ON ui.set_id = gm.set_id AND ui.generation_run_id = gm.generation_run_id
JOIN umigame_stock_items s ON s.set_id = ui.set_id AND s.id = ui.stock_item_id
SET gm.duration_seconds = 29
WHERE gm.duration_seconds = 24
  AND s.video_built_at >= '2026-10-16 17:27:41'
  AND gm.generated_at >= '2026-10-17 02:56:00';
