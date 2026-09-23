-- umigame-soup-1: 正式 BGM の audio_assets 登録 SQL
-- prepare_bgm.py が生成。provisional=true のトラックは含めない。

INSERT INTO audio_assets (set_id, s3_key, asset_type, time_slot,
  title, source_url, license_type, license_note, acquired_at, duration_seconds, is_active)
SELECT b.id, 'audio/umigame-soup-1/track01.m4a', 'bgm', NULL,
  'Strange Detectives', 'https://pixabay.com/music/cartoons-strange-detectives-182044/',
  'Pixabay Content License', 'HarumachiMusic。クレジット表記不要（2026-09-24 に配布ページで Pixabay Content License を確認）。配布ページに Content ID Registered の表示あり。先頭から 24 秒を使用（2026-09-24 ユーザー選曲）',
  '2026-09-24 00:00:00', 24, 1
FROM batch_sets b
WHERE b.set_code = 'umigame-soup-1';
