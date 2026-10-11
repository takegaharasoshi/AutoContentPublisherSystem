# プロフィール画像（探偵カメロック）

umigame-soup-1 の Instagram アカウント（umigame.soup.jp）のプロフィール画像。21-7a2（2026-10-12）で作成。

- 採用: **候補 C（上半身・虫眼鏡とスープ・ライトブルー）** → `profile.png`（1080×1080・文字なし）
- 元画像: `content/video-build/umigame-soup-1/assets/characters/master_base.png`（1000×1100 の透過 PNG）
- 切り抜き: 元画像上の正方形 中心 (590, 365)・一辺 780px → 1080×1080 へ拡大（範囲外は透明）
- 背景色: `#e8f5ff`（動画〔`remotion/`〕で使っている淡いライトブルー）
- 顔の位置: 顔の矩形の最遠点が円の半径の 0.57（基準: 円の内側 7 割 = 0.70 以内）

## 再現

リポジトリルートから:

```bash
python3 content/umigame-stock/umigame-soup-1/set-registration/profile/make_profile.py --pick C
```

引数なしで実行すると `candidates/` に全候補（A / B / C）と円形マスクの見え方（1080 / 320 / 110px）を出力する。`candidates/` は再生成できるので git に入れない（`.gitignore`）。切り抜き・背景色の値の正は `make_profile.py` の `CANDIDATES`。
