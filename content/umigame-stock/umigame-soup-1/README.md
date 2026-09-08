# umigame-soup-1 ストック資材（ウミガメのスープ参加型セット）

`umigame_stock_items`（V012）へ投入する問題ストックのバッチ別ソースと整備ツーリング。仕様の正は
[セット別設計書](../../../docs/app/sets/umigame-soup-1.html) セクション 4（素材 14 項目）、投入手順の正は
[運用設計](../../../docs/app/operation.html)。**作問の手順（コア宣言・動線・現実性の自己検査）の正はスキル `.claude/skills/umigame-problem-writer/SKILL.md`**（21-4a-2）。週次補充の手順はスキル `umigame-stock-replenish`（21-8 で新設予定。作問は umigame-problem-writer を呼ぶだけ）。

```
umigame-soup-1/
├── master_prompt.txt        # AI 出題者プロンプトのセット固定部分（正）。probe_test.py と 21-7 の prompt_configs INSERT が共有
├── common/umigame_common.py # セット既定文（ルール帯・台詞・ハッシュタグ）、イラスト / キャプションの組み立て、素材項目のキー一覧
└── batch-01/                # 第 1 バッチ（21-4a で 10 問。21-4a-2 のスキル試行で U11・U12 を追加し暫定 12 問。最終構成は 21-4a-3）。補充時はこの一式を新しいバッチディレクトリへコピーして回す
    ├── stock_items.py       #   単一ソース（1 問 = 素材 14 項目 + 管理項目〔core = コア宣言 等〕）
    ├── validate.py          #   機械検証（字数・件数・#AIart・画風固定行・プレイ例の「はい」・オリジナル宣言・コア宣言の様式・ナレーション推定長）
    ├── probe_test.py        #   プローブテスト（想定質問を gpt-5.6-luna の出題者に答えさせ work/review.html に並べる）
    ├── leak_count.py        #   補足の核心語漏れを数える（プロンプト改定の効果比較。核心語は手書き辞書）
    ├── generate.py          #   insert_umigame_stock.sql の生成 + ローカル MySQL でのドライラン（--dry-run）
    ├── research.md          #   リサーチ台帳（有名問題との構造照合用〔作問スキル工程 7〕+ オリジナル性の基準）
    ├── STATUS.md            #   進行状況（引き継ぎメモ）
    └── work/                #   probe_results.json / review.html（gitignore）
```

## バッチの回し方（21-4a で確立）

```bash
# 作問は 1 問ずつスキル umigame-problem-writer の工程で行い、作問ログを会話に貼る
cd content/umigame-stock/umigame-soup-1/batch-01
python3 validate.py                 # 全件 OK になるまで stock_items.py を直す
python3 probe_test.py               # OpenAI キーは Secrets Manager umigame-poc/credentials を boto3 で実行時に読む（値は出力しない）
python3 probe_test.py --only U03    # 直した問題だけ再実行（他はキャッシュ）
python3 leak_count.py               # 補足で正体を言った応答数（プロンプトを変えたら必ず前後で比べる）
python3 generate.py --dry-run       # insert SQL を生成し、ローカル MySQL でトランザクション内に流して ROLLBACK
```

- プローブテストの `[ERROR]` 行は API 失敗。`--only` で再実行する
- 機械判定の「不一致」は期待冒頭語（はい / いいえ / 関係ありません / 正解です）と実回答の冒頭が合わないもの。
  多くは確定事実シートの穴か期待回答の誤りなので、シートを直して再実行する（プロンプト側を直す場合は master_prompt.txt を直し、
  セット別設計書 5.1 に反映する）
- 投入（21-4b）はレビュー承認後、`insert_umigame_stock.sql` をローカル MySQL と Aurora の両環境へ流す
