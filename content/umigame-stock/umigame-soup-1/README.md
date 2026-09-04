# umigame-soup-1 ストック資材（ウミガメのスープ参加型セット）

`umigame_stock_items`（V012）へ投入する問題ストックのバッチ別ソースと整備ツーリング。仕様の正は
[セット別設計書](../../../docs/app/sets/umigame-soup-1.html) セクション 4（素材 14 項目）、投入手順の正は
[運用設計](../../../docs/app/operation.html)。週次補充の手順はスキル `umigame-stock-replenish`（21-8 で新設予定）。

```
umigame-soup-1/
├── master_prompt.txt        # AI 出題者プロンプトのセット固定部分（正）。probe_test.py と 21-7 の prompt_configs INSERT が共有
├── common/umigame_common.py # セット既定文（ルール帯・台詞・ハッシュタグ）、イラスト / キャプションの組み立て、素材項目のキー一覧
└── batch-01/                # 第 1 バッチ 10 問（21-4a）。補充時はこの一式を新しいバッチディレクトリへコピーして回す
    ├── stock_items.py       #   単一ソース（1 問 = 素材 14 項目 + 管理項目）
    ├── validate.py          #   機械検証（字数・件数・#AIart・画風固定行・プレイ例の「はい」・オリジナル宣言・ナレーション推定長）
    ├── probe_test.py        #   プローブテスト（想定質問を gpt-5.6-luna の出題者に答えさせ work/review.html に並べる）
    ├── generate.py          #   insert_umigame_stock.sql の生成 + ローカル MySQL でのドライラン（--dry-run）
    ├── research.md          #   リサーチ台帳（Codex Web リサーチ + note 記事の作問法 + オリジナル性の基準）
    ├── STATUS.md            #   進行状況（引き継ぎメモ）
    └── work/                #   probe_results.json / review.html（gitignore）
```

## バッチの回し方（21-4a で確立）

```bash
cd content/umigame-stock/umigame-soup-1/batch-01
python3 validate.py                 # 全件 OK になるまで stock_items.py を直す
python3 probe_test.py               # OpenAI キーは Secrets Manager umigame-poc/credentials を boto3 で実行時に読む（値は出力しない）
python3 probe_test.py --only U03    # 直した問題だけ再実行（他はキャッシュ）
python3 generate.py --dry-run       # insert SQL を生成し、ローカル MySQL でトランザクション内に流して ROLLBACK
```

- プローブテストの `[ERROR]` 行は API 失敗。`--only` で再実行する
- 機械判定の「不一致」は期待冒頭語（はい / いいえ / 関係ありません / 正解です）と実回答の冒頭が合わないもの。
  多くは確定事実シートの穴か期待回答の誤りなので、シートを直して再実行する（プロンプト側を直す場合は master_prompt.txt を直し、
  セット別設計書 5.1 に反映する）
- 投入（21-4b）はレビュー承認後、`insert_umigame_stock.sql` をローカル MySQL と Aurora の両環境へ流す
