# Irodori-TTS PoC（21-5c・2026-09-27）

Gemini 3.8 Flash TTS の日次上限（Tier 1・100 リクエスト / 日）で 14 問の作り直しが止まったため、
ローカル GPU で動く [Irodori-TTS](https://github.com/Aratako/Irodori-TTS)（v4.1-Small・MIT）を試した記録。
**結論: Irodori・BF16・声 G4 のクローン（参照 = `assets/voice/kamerock-g4/`）で 14 問を作り直す**（ユーザー決定）。

## 環境（リポジトリ外）

- 本体: `~/tools/Irodori-TTS`（commit `89f9d8f`、`uv sync --extra cu128`）。モデルは HF `Aratako/Irodori-TTS-v4.1-Small`（snapshot `2b28324`）
- GPU: RTX 3050 Laptop（VRAM 4GB）。ドライバー 616.92（2026-09-27 に 511.81 から更新。CUDA 12.8 に必要）
- **必ず `--model-precision bf16 --codec-precision bf16 --model-device cuda --codec-device cuda`**。既定の fp32 は VRAM からあふれて 1 本 4〜7 分、bf16 は約 45 秒（モデル読み込み込み）。聞き比べで音質差なし（ユーザー確認）
- 生成音声には SilentCipher の透かしが自動で入る

## 決まったこと（聞き比べの結果）

- 声: G4「kamerock-chubby」のクローン。参照は Gemini G4 の 001・004・006 の problem / rule（話速調整なし）6 本に
  **息継ぎゲート**（`irodori_poc.py` の `breath_gate`: ピーク -18dB 未満が 80ms 以上続く区間を両端 20ms 残して -30dB）をかけたもの（①）。
  参照の息を下げると生成側の吸気音も減る。生成後の後処理（③）や説明文での指示（②）は不要と判断
- 説明文（caption）なし・絵文字なし。voice2（別話者のクローン）と演技指示つきの版も比較したが G4 に決定
- 問題文 + ルール文を 1 回で合成（`--seconds 20.0`）→ 無音で切り分け（`narration_gemini._split`）→ 前後の無音削り。
  2 問（016・008）とも 19.0〜20.8 秒で予算 21 秒内・話速調整なし。自然長（長さ指定なし）は 23〜25 秒で予算超過
- FP32 と BF16 は同じ seed でも別テイク相当に波形が変わる（拡散モデルのため）が品質差はない

## ファイル

- `irodori_poc.py`: 息継ぎゲート・参照音声の分割・①〜③ の試作
- `irodori_stage1.py`: Irodori の venv で合成（`cd ~/tools/Irodori-TTS && uv run --no-sync python <path>`）
- `irodori_stage2.py`: システムの python3 で切り分け → Remotion で比較動画（`work/irodori-poc/`・git 管理外）
