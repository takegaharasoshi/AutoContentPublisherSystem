-- pref-ranking-1 セット登録 (3/3): audio_assets（BGM）
-- prepare_bgm.py が work/bgm/tracks.json から生成する（手書きしない）。
-- 前処理済み音源を S3 の audio/pref-ranking-1/ へ配置してから適用する。
-- time_slot は NULL（スロット共通の汎用曲）。証跡 3 点は本テーブルに記録する
-- （docs/app/operation.html セクション 3。別ドキュメントで管理しない）。

-- (1) Japan Instrumental Background Music
INSERT INTO audio_assets (set_id, s3_key, asset_type, time_slot, title, source_url, license_type, license_note, acquired_at, duration_seconds, is_active)
SELECT b.id, 'audio/pref-ranking-1/track01.m4a', 'bgm', NULL,
       'Japan Instrumental Background Music',
       'https://pixabay.com/music/world-japan-instrumental-background-music-349763/',
       'Pixabay Content License',
       'Tunetank。クレジット表記不要（2026-08-26 に https://pixabay.com/service/license-summary/ で確認）。配布ページに Content ID Registered の表示あり',
       '2026-08-26 00:00:00',
       30, 1
FROM batch_sets b
WHERE b.set_code = 'pref-ranking-1';
