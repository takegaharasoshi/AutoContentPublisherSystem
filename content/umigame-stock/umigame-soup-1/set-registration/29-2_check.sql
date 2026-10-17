-- 開発 29-2 (3/3): 適用後の確認（読み取りのみ）
-- 期待: (1) parameters = {"duration_seconds": 29} (2) duration_seconds = 29 (3) 新版面の行がすべて 29・24 は旧版面の行だけ

-- (1) テンプレートの宣言値
SELECT p.id, p.parameters, p.is_active
FROM prompt_configs p JOIN batch_sets b ON b.id = p.set_id
WHERE b.set_code = 'umigame-soup-1';

-- (2) BGM の尺
SELECT a.id, a.s3_key, a.duration_seconds, a.license_note
FROM audio_assets a JOIN batch_sets b ON b.id = a.set_id
WHERE b.set_code = 'umigame-soup-1';

-- (3) 生成結果の尺を版面別に数える（S3 上書き 2026-10-17 02:56:00 UTC の前後）
SELECT IF(gm.generated_at >= '2026-10-17 02:56:00', 'new', 'old') AS layout,
       gm.duration_seconds, COUNT(*) AS n, MIN(gm.generated_at) AS first_at, MAX(gm.generated_at) AS last_at
FROM generated_media gm JOIN batch_sets b ON b.id = gm.set_id
WHERE b.set_code = 'umigame-soup-1'
GROUP BY layout, gm.duration_seconds
ORDER BY layout, gm.duration_seconds;
