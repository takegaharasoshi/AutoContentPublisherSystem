-- 開発 29-2 (1/3): 24 で記録された新版面の生成結果を抽出する（読み取りのみ。更新の前に件数と生成日時を確かめる）
-- 新版面の判定: R-1-5 は在庫行をその場で更新し S3 キーも変えていないため、stock_item_id だけでは旧版面と見分けられない。
--   (a) 使った在庫の video_built_at が R-1-3 の再ビルド以降（2026-10-16 17:27:41 UTC〜）
--   (b) 生成が R-1-5 の S3 上書きの後（2026-10-17 02:56:00 UTC = 11:56 JST〜）
--   の両方を満たす行だけを対象にする（旧版面の 24 秒動画で生成された行は直さない）。
-- 時刻はすべて UTC。2026-10-17 時点の想定は Aurora で generation_run 298（016・手動投稿）の 1 件
-- （29-2 の適用が 20:00 JST の定時より後になれば、その回の 001 も加わる）。
SELECT gm.id AS generated_media_id, gm.generation_run_id, ui.content_key,
       gm.duration_seconds, gm.generated_at, s.video_built_at
FROM generated_media gm
JOIN batch_sets b ON b.id = gm.set_id AND b.set_code = 'umigame-soup-1'
JOIN umigame_items ui ON ui.set_id = gm.set_id AND ui.generation_run_id = gm.generation_run_id
JOIN umigame_stock_items s ON s.set_id = ui.set_id AND s.id = ui.stock_item_id
WHERE gm.duration_seconds = 24
  AND s.video_built_at >= '2026-10-16 17:27:41'
  AND gm.generated_at >= '2026-10-17 02:56:00'
ORDER BY gm.generated_at;
