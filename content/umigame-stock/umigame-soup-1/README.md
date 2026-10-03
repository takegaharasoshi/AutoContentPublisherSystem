# umigame-soup-1 ストック資材（ウミガメのスープ参加型セット）

`umigame_stock_items`（V012）へ投入する問題ストックのバッチ別ソースと整備ツーリング。仕様の正は
[セット別設計書](../../../docs/app/sets/umigame-soup-1.html) セクション 4（素材 14 項目）、投入手順の正は
[運用設計](../../../docs/app/operation.html)。**作問の手順（コア宣言・動線・現実性の自己検査）の正はスキル `.claude/skills/umigame-problem-writer/SKILL.md`**。

```
umigame-soup-1/
├── common/umigame_common.py # セット既定文、イラスト / キャプションの組み立て、素材項目のキー一覧
└── batch-01/                # 第 1 バッチ（全 14 問 = story 7 / misdirection 7）
    ├── stock_items.py       #   単一ソース（素材 14 項目 + 管理項目）
    ├── validate.py          #   素材の機械検証
    ├── review_sheet.py      #   素材レビューシート生成（API キー不要）
    ├── leak_count.py        #   P1 漏れ候補の核心語辞書（probe_metrics.py が読む）
    ├── generate.py          #   insert_umigame_stock.sql の生成 + ローカル MySQL でのドライラン
    ├── research.md          #   リサーチ台帳
    ├── STATUS.md            #   進行状況（引き継ぎメモ）
    └── work/review.html     #   review_sheet.py が生成する素材レビューシート（gitignore）
```

## 素材の確認と投入準備

```bash
cd content/umigame-stock/umigame-soup-1/batch-01
python3 validate.py
python3 review_sheet.py       # work/review.html を生成。API キー不要
python3 generate.py --dry-run # SQL を生成し、ローカル MySQL でトランザクション内に流して ROLLBACK
```

本番経路の機械プローブは `services/comment-reply/tools/probe_run.py` を使う。評価ケースは
`judge-trial/data/eval_problems.json` に追加してから `--problems <no>` を指定する。
