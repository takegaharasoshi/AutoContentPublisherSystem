# 17-5b セット登録（pref-ranking-1）の状態

手順の正は [docs/app/operation.html](../../../../docs/app/operation.html) セクション 2.1（セット追加手順）、
値の正は [docs/app/sets/pref-ranking-1.html](../../../../docs/app/sets/pref-ranking-1.html)。
`batch_sets` 行は 17-3 で登録済み（ローカル `set_id=140` / Aurora `set_id=3`。`is_active=0` のまま。
稼働開始〔17-5c〕で 1 にする）。

| # | 対象 | ファイル | 状態 |
|---|---|---|---|
| 1 | `prompt_configs` + `caption_templates` | [01_prompt_caption.sql](01_prompt_caption.sql) | **完了（2026-08-26）**。両環境へ適用済み。`caption_templates.template_text` の MD5 `d861cebf75c7ff0f49c89b83a321c9de` が両環境で一致 |
| 2 | Instagram アカウント開設 + Secret 作成 | （ユーザー作業。operation.html セクション 5.1） | 未 |
| 3 | `sns_accounts` | [02_sns_account.sql](02_sns_account.sql) | 未（**Secret 作成後に適用する**） |
| 4 | BGM 調達・前処理・S3 配置 | `content/video-build/pref-ranking-1/prepare_bgm.py` | 未 |
| 5 | `audio_assets` | `03_audio_assets.sql`（`prepare_bgm.py` が生成） | 未 |

Scheduler 追加（画像生成 1 件 + インサイト収集 2 件）・バックログ 0 件確認・手動実行確認は 17-5c。

## 適用コマンド

```bash
cd content/ranking-stock/pref-ranking-1
# ローカル MySQL（--default-character-set=utf8mb4 は必須。落とすと日本語が二重エンコードで壊れる）
docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps \
  < set-registration/01_prompt_caption.sql
# Aurora（Data API。自動一時停止からの復帰は apply_aurora.py がリトライする）
python3 common/apply_aurora.py set-registration/01_prompt_caption.sql
```

本適用の前に、ローカルで `START TRANSACTION;` … `ROLLBACK;` に挟んだドライランを行い、
文字化けと投入行の内容を確認する（[../WRITING-NOTES.md](../WRITING-NOTES.md) の投入手順と同じ）。

## 適用後の確認

```sql
SELECT p.id, p.parameters, c.id, MD5(c.template_text), s.account_code, COUNT(a.id)
FROM batch_sets b
LEFT JOIN prompt_configs p ON p.set_id = b.id
LEFT JOIN caption_templates c ON c.set_id = b.id
LEFT JOIN sns_accounts s ON s.set_id = b.id
LEFT JOIN audio_assets a ON a.set_id = b.id AND a.asset_type = 'bgm' AND a.is_active = 1
WHERE b.set_code = 'pref-ranking-1'
GROUP BY p.id, p.parameters, c.id, s.account_code;
```

両環境で同じ結果になること・BGM が 3〜5 件（`time_slot IS NULL`）あることを確認する。
