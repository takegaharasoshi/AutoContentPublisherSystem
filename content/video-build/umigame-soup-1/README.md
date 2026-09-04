# umigame-soup-1 動画ビルド（21-2 PoC）

ウミガメのスープ参加型セット（`set_code = umigame-soup-1`・方式 `umigame-prebuilt`）のリール動画ビルド資材。
Phase 21-2（2026-09-04）で **完成版リール 1 本の PoC** として作ったもので、ストックからの本組み（`export_prompts.py` /
`intake.py` / `publish.py` 等）は 21-5a で整備する。21-1 の決定（版面・尺・ナレーション・キャラ構成）は
[docs/app/requirements-notes-set4.html](../../../docs/app/requirements-notes-set4.html)、ステップの定義は
[docs/plans/development-plan.html](../../../docs/plans/development-plan.html) Phase 21。

```
umigame-soup-1/
├── README.md                 # 本書
├── build.py                  # PoC ビルド（素材配置 → props → Docker レンダリング → ラウドネス → 静止フレーム → ffprobe → review.html）
├── scripts/
│   ├── narration.py          # VOICEVOX でナレーション 2 cue を合成し実測長を出す（話者比較にも使う）
│   └── prepare_assets.py     # 背景の 1080x1920 JPEG 化・キャラの共通キャンバス正規化（PIL。Docker で実行）
├── tests/test_timeline_sync.py  # build.py と timeline.ts の定数同期
├── poc/<content_key>/        # 1 問 = 1 ディレクトリの素材一式（下記）
├── remotion/                 # Remotion プロジェクト（Remotion Skills 2.0 の指針で作成）
└── work/                     # ビルド出力（git 管理外）: props/ out/ videos/ stills/ probe/ review.html
```

## 1. Remotion Skills 2.0 の導入記録（21-1 ③ の決定の実測）

| 項目 | 実測（2026-09-04） |
|---|---|
| 導入コマンド | `npx -y skills@1.5.23 add remotion-dev/skills --skill remotion-best-practices remotion-create remotion-markup remotion-render remotion-docs remotion-upgrade -a claude-code -a codex -y`（skills CLI 1.5.23） |
| 導入したスキル | `remotion-best-practices` / `remotion-create` / `remotion-markup` / `remotion-render` / `remotion-docs` / `remotion-upgrade` の 6 本（maps / captions / saas / interactivity / multimedia / studio は入れていない。ただし `remotion-best-practices/` 配下に全スキルの REFERENCE.md が同梱される） |
| スキルの版 | 各 SKILL.md の frontmatter `version: 4.0.520`（Remotion 4.0.520 と同じ版番号）。ソースは GitHub `remotion-dev/skills`、ハッシュはリポジトリルートの `skills-lock.json` |
| 配置 | 正本 `.agents/skills/remotion-*/`（Codex 用 = universal）、`.claude/skills/remotion-*` は **スキル単位の相対シンボリックリンク**（`../../.agents/skills/remotion-*`）。自前スキルの実ディレクトリ `.claude/skills/{step,idea,...}` と**そのまま共存できた**（21-1 の想定どおり。手動でのリンク切り替えは不要） |
| コミット対象 | `.agents/skills/remotion-*`（正本）+ `.claude/skills/remotion-*`（リンク）+ `skills-lock.json` |
| 更新 | `npx skills update`（版が上がったら本表と `skills-lock.json` を更新してコミット） |

導入直後の `ls`:

```
.agents/skills/: remotion-best-practices  remotion-create  remotion-docs  remotion-markup  remotion-render  remotion-upgrade
.claude/skills/: docs-mobile-view  idea  quiz-stock-replenish  ranking-stock-replenish  step
                 remotion-best-practices -> ../../.agents/skills/remotion-best-practices  （以下 remotion-* 5 本も同様のリンク）
```

## 2. PoC 素材（`poc/classic-umigame/`）= ストック 1 件分の素材一式（仮）

21-1 ⑧ の仮リストを 1 問分（古典「ウミガメのスープ」本編。PoC 限定使用）で実際に揃えたもの。
**この動画の人間レビューをもって、ストックの素材項目（何を執筆・生成・レビューするか）を確定する**（21-2 の人間ゲート）。

| ファイル | 内容 | 21-1 ⑧ の項目 |
|---|---|---|
| `problem.json` | 問題文（78 字）/ 真相 / 確定事実シート 10 件 / 想定質問 20 件と期待回答 / フック文 / プレイ例 3 往復 / 出題者の導入・締めセリフ / ナレーション cue（問題文 + ルール。**表示文とは別に読み上げ用に句読点を整えた文**）/ イラスト作成用プロンプト / キャプション + ハッシュタグ（`#AIart` 含む）/ 出典・オリジナル性メモ / 難易度 | 問題文・真相・確定事実シート・想定質問・イラストプロンプト・フック・プレイ例・ナレーション cue・キャプション・出典メモ・難易度 |
| `characters.json` | キャラ 2 体の設定（名前候補と採用名・役割・ベースプロンプト・ポーズ差分）と画風固定行 | （セット固定。ストック単位ではない） |
| `prompt_*.txt` | imagegen へ渡した実プロンプト（背景 1・出題者 2 ポーズ・質問者 1 ポーズ） | イラストプロンプト |
| `background.png` / `master_base.png` / `master_happy.png` / `assistant_base.png` | imagegen の生出力（背景 941x1672、キャラは透過 PNG 1024〜1254 px 角） | イラスト |
| `normalized/` | `background.jpg`（1080x1920 q88）/ キャラ 3 枚（共通キャンバス 1000x1100・bbox 高さ 1000 に統一）/ `bgm_20s.m4a` / `se_pop.wav` | — |
| `bgm_night_track01.m4a` | BGM の元（S3 `audio/logic-training-1/night/track01.m4a`。Pixabay Content License・クレジット不要。既存プールの流用で PoC 専用の新規調達はしていない） | BGM |
| `narration/speaker{11,12,14}/` | VOICEVOX 話者比較用の WAV と実測長（`narration.json`） | — |
| `gen_images.sh` | Codex CLI の `image_gen.imagegen` ツールで 1 枚生成する補助スクリプト | — |

### 素材の作り方（PoC で実際に踏んだ手順）

1. **イラスト**: `bash poc/classic-umigame/gen_images.sh <name> "<prompt>"`。Codex CLI（0.144.1）の `codex exec` から
   `image_gen.imagegen` ツールを呼べることを確認した（pref-ranking-1 の README にある「Codex 組み込み imagegen に貼る」手作業が
   **CLI から自動化できる**。生成 1 枚あたり 1〜2 分）。透過 PNG の指定も効いた。
2. **正規化**: リポジトリルートで
   `docker run --rm -u $(id -u):$(id -g) -v "$PWD:/repo" -w /repo/content/video-build/umigame-soup-1 --entrypoint python image-batch:ffmpeg-check scripts/prepare_assets.py poc/classic-umigame`
3. **BGM / SE**: BGM は S3 の既存プールから 20 秒ちょうどに切り出し（`ffmpeg -stream_loop -1 -t 20`）。吹き出し SE はライセンスの
   問題を避けるため ffmpeg の `sine` で合成した 0.14 秒の「ポン」（880 + 1320 Hz）。本番では `audio_assets` に SE として登録する。
4. **ナレーション**: VOICEVOX Engine を起動（`docker run -d --name voicevox-engine -p 50021:50021 voicevox/voicevox_engine:cpu-ubuntu20.04-latest`）し
   `python3 scripts/narration.py poc/classic-umigame/problem.json poc/classic-umigame/narration --speaker 11 --speaker 12 --speaker 14 --budget-seconds 17`

### VOICEVOX 話者の試聴候補と実測長（話速 1.2・抑揚 1.6・cue 間 0.5 秒）

| 話者（スタイル ID） | 問題文 | ルール | 合計 | 17 秒予算 |
|---|---|---|---|---|
| **玄野武宏 ノーマル（11）** ← PoC 採用 | 10.42 s | 5.45 s | **16.37 s** | OK |
| 白上虎太郎 ふつう（12。pref-ranking-1 の五郎） | 11.85 s | 6.07 s | 18.42 s | 超過 |
| 冥鳴ひまり ノーマル（14） | 11.39 s | 5.59 s | 17.48 s | 超過 |

- **青山龍星（13）は商用利用に VirVox Project への事前申請が要るため候補から外した**（`pref-ranking-1/LICENSES.md` セクション 2）。
  玄野武宏も VirVox Project の音源のため、採用時は同じ規約でクレジット表記「VOICEVOX:玄野武宏」をキャプションに常設する（21-3 で `LICENSES.md` を起こす）。
- pref の TTS アダプタの予測長 / 実測長の許容差（0.08 秒）は 2〜4 秒の短い cue で決めた値で、12 秒級の cue では 0.1 秒程度ずれる
  （話者 12 で実測）。`narration.py` は PoC として 0.3 秒に緩めている。本組みでは cue 長に比例した許容差にする。

## 3. ビルド手順（PoC）

事前準備: `remotion-render` / `image-batch:ffmpeg-check` の Docker イメージ（pref-ranking-1 README の手順で作成済みのもの）、
VOICEVOX Engine の起動、`pref-ranking-1/remotion/public/fonts/` に Zen Kaku Gothic New 3 ファイル、`remotion/` で `npm install`。

```bash
cd content/video-build/umigame-soup-1
python3 build.py classic-umigame --speaker 11
# → work/videos/classic-umigame.mp4, work/stills/classic-umigame_<label>.jpg, work/probe/classic-umigame.txt, work/review.html
```

`build.py` は既存 2 セットと同じく Remotion を `remotion-render` イメージへの bind-mount で実行し（`-e HOME=/tmp --user uid:gid`）、
ラウドネス正規化は pref-ranking-1 の `normalize_loudness.py`（-14 LUFS / -2 dBTP）をそのまま流用する。
静止フレームは最終 MP4 から ffmpeg で抜く（Remotion の `still` ではなく「配信物そのもの」を確認するため）。

## 4. Remotion プロジェクト（`remotion/`）

| ファイル | 役割 |
|---|---|
| `src/timeline.ts` | 600 フレームのビート定義（導入 90f → 質問 60f / 返答 60f × 3 → 締め 138f → 継ぎ目 12f）・周期・ナレーション期限。約数チェックとビート連続性チェックをモジュール読み込み時に行う |
| `src/props.ts` | Zod スキーマ（remotion-markup `parameters.md` の指針。Studio で props を編集できる） |
| `src/UmigameReel.tsx` | コンポジション本体。`Interactive.Div` + inline `interpolate()`、`<Img>`、`@remotion/media` の `<Audio>` |
| `src/fonts.ts` | `@remotion/fonts` の `loadFont`（`local-fonts.md` の指針） |
| `src/mockProps.ts` / `src/Root.tsx` | Studio 用既定 props と `Composition`（`UmigameReel20s`・1080x1920・30fps・600f） |
| `remotion.config.ts` | JPEG フレーム・CRF 20（既存 2 セットと同じ） |

タイムラインの不変条件は logic-training-1 と同じ（フレーム 600 = フレーム 0、周期は 600 の約数、吹き出しはスナップ切替）。
導入の吹き出しだけポップインさせず静止にしているのは、継ぎ目（588〜600f）で導入状態へ戻したときにフレーム 0 と完全一致させるため。

## 5. 所見（21-2 ④ / 人間ゲートの判断材料）

### 5.1 Remotion Skills の指針と既存の Docker 委譲手順との食い違い

- **`remotion-render` スキルは「`npx remotion render` を打つ」以上のことを書いていない**（SKILL.md は 470 バイト。詳細は
  `remotion-best-practices/remotion-render/REFERENCE.md`）。既存の Docker 委譲（bind-mount + `HOME=/tmp` + `--user`）と衝突する記述はなく、
  そのまま `build.py` から同じコマンドを流せた。食い違いは**なし**。
- `remotion-create` の指針は `npx create-video@latest --yes --blank --no-tailwind` だが、**`--no-tailwind` を付けても雛形に
  `@remotion/tailwind-v4` と `tailwindcss` が入り、`remotion.config.ts` に `enableTailwind` が書かれた**（create-video の挙動）。
  本セットでは使わないため手で外した（package.json と config）。また雛形の `tsconfig.json` は `lib: ["es2015"]` のみで
  `document` 等を使うと型エラーになるため `dom` を足した。
- `remotion-markup` は `<CanvasImage>` / `@remotion/media` の `<Audio>` / `Interactive.*` を推奨する。いずれも導入した Remotion 4.0.520
  に存在した（`@remotion/media` は ESM only。CJS からは require できないが bundler 経由では問題ない）。**pref-ranking-1（4.0.507）に
  同じ指針を当てると `Interactive` が無い可能性がある**ため、既存セットへの遡及適用は upgrade とセットになる。
- `remotion-create` は「Studio を開いてプレビュー」を前提にするが、本リポジトリのレンダリングは Docker 経由で Studio はホストで動く
  （`npm run studio`）。指針との衝突はないが、PoC では Studio を使わず `npx remotion still` の 1 フレーム確認（`remotion-markup` 末尾の
  "one-frame render check"）で版面を詰めた。これは Docker 経由でも問題なく使えた。
- `video-layout.md` の下限（見出し 84px・重要テキスト 44px）に対し、本版面はフック 74px・問題文 44px・ルール帯 34px・吹き出し 42px。
  ルール帯は下限を下回るが、常時表示の固定要素で 2 行に収める必要があり許容した（人間ゲートで判断）。

### 5.2 既存 2 セットの手組みコンポジションとの差

| 観点 | 所見 |
|---|---|
| 開発速度 | 素材生成（imagegen 4 枚・約 6 分）と VOICEVOX 話者比較を含めて、スキル導入から完成版 MP4 まで 1 セッション（約 1 時間）。既存セットの初回版面（17-4a・R-1）より速いが、要因の大半は**既存ツーリング（Docker 委譲・TTS アダプタ・ラウドネス正規化・五郎方式のキャラ正規化）の流用**であり、スキルの寄与は「API の選び方・書き方で迷わない」部分に限られる |
| 品質 | 版面の構成・可読性は既存セットと同等。スキルの効果として `Interactive.Div` + inline style + inline `interpolate()` で書いたため、Studio で要素を選択・調整できる構造になっている（既存 2 セットは定数化したスタイルが多く Studio で編集しにくい） |
| 指針との乖離 | 周期アニメーション（sin のゆれ）は `interpolate()` で書けないため `translate` 文字列で書いた（Studio では計算値扱い）。ループ前提（末尾 = 先頭）は Remotion の指針に無い本リポジトリ固有の制約で、`timeline.ts` の不変条件チェックで担保する |
| 保守性 | `create-video` 雛形（eslint / prettier 設定つき）に乗ったため、既存 2 セットより lint 環境が整っている。一方で雛形の Tailwind 混入・tsconfig の `dom` 欠落のような「雛形の手直し」が要る |

### 5.3 素材項目の確定に向けた気づき（人間ゲートで決めること）

- **吹き出しの 1 行上限**: 出題者のセリフは 17 字（幅 800px・42px）、質問者のセリフは 16 字（幅 760px）まで 1 行に収まる。2 行になると出題者の名札に重なるため、ストックの `validate.py` で字数を検査する。
- **問題文の字数上限はナレーションの予算で決まる**。玄野武宏・話速 1.2 で 78 字 + ルール 30 字 = 16.4 秒。20 秒尺で締めのセリフ
  （15 秒〜）に食い込ませないなら **問題文は 75〜80 字が上限**。ストックの `validate.py` に字数 + 実測長の検査を入れる。
- 表示用の問題文と読み上げ用の cue は分けて持つ（読み上げは括弧・記号を落として句読点で間を作る）。
- プレイ例の「はい」返答で出題者が喜ぶポーズに切り替わるため、**プレイ例 3 往復のうち 1 つは「はい」にする**のが版面上の約束事になる。
- キャプションには `#AIart` に加えて VOICEVOX のクレジット行が要る（pref-ranking-1 と同じ常設要素）。
- 背景イラストは「暗めの単色トーン・シルエット寄り」の指示に対し imagegen は写実寄りの暗い絵を返した（本 PoC の背景）。
  オーバーレイを弱めて成立させたが、画風はレビューで決める。

## 6. 人間ゲート（21-2）

`work/review.html` を開いて、フック・版面・テンポ・イラストの画風・キャプション・話者を確認する。
修正はレビュー中に反復し、この動画をもって (a) ストックの素材項目の確定 (b) フォーマットの go / no-go
(c) Remotion Skills を本セットの標準ツーリングとして続けるか、を決める。
