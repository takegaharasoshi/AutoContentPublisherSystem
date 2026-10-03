# ElevenLabs v4 聞き比べ PoC（21-5d・2026-10-03）

アイデア「[ElevenLabs v4 をナレーションに使う](../../../../../docs/ideas/umigame-tts-elevenlabs-v4.md)」の聞き比べ。
2 問（016・014）のナレーションを 4 通りで作り、本番と同じ Remotion で比較動画にする。採否はユーザーが聞き比べて決める
（基準: Irodori より**大幅に**良いこと。月 6 ドルの固定費が増えるため）。

| 案 | 声 | モデル |
|---|---|---|
| ① e1-irodori | 現行 Irodori（声 G4 のクローン。21-5c の承認済みビルドをそのまま使う） | — |
| ② e2-v4-clone | 声 G4 のインスタントボイスクローン（参照 = `assets/voice/kamerock-g4/` の 6 本。Irodori と同じ） | `eleven_v4` |
| ③ e3-v4-design | Voice Design（`eleven_ttv_v3`。説明文 3 版 × 候補 3 = 9 本から `design.pick` の 1 本） | `eleven_v4` |
| ④ e4-v3-design | ③ と同じ声 | `eleven_v3`（v4 で演技が控えめになるかの対照） |

## 使い方

```bash
python3 poc/elevenlabs-tts/run_poc.py --design-only  # Voice Design の候補だけ作る
python3 poc/elevenlabs-tts/run_poc.py                # 声の用意 + 合成 + レンダリング + 比較ページ
```

- API キーは `ELEVENLABS_API_KEY` か `~/.config/elevenlabs/api_key`（リポジトリに置かない）
- 出力（音声・動画・`compare.html`）は `out/`（git 管理外）。作った声の ID と説明文は `voices.lock.json`（git 管理）
- ③④ の声を別候補に替えるときは `variants.json` の `design.pick` を書き換え、`--force --variant e3-v4-design --variant e4-v3-design` で取り直す
- 演技指示は音声タグ（`[...]`）を問題文・ルール文の頭に付ける（`direction` / `rule_direction`）。**v4 は日本語のタグを読み上げないが、v3 は読み上げる**（タグ + 「はい。」で v3 = 7.5 秒・v4 = 0.7 秒。2026-10-03 に確認）ため、④ は英語のタグを variant 側で指定する
- 問題文とルール文は 1 回で合成し、無音で切り分ける。前後の無音を削り、21 秒予算を超える分だけ話速を上げて 19 秒に合わせる（Gemini PoC の `_split` / `_fit` を流用。21-5c と同じ扱い）
- 消費クレジットは TTS のレスポンスヘッダー `x-character-count`（音声タグの文字も数える）。`user/subscription` の累計は反映が数分遅れる
