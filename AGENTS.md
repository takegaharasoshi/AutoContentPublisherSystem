# AGENTS.md

Codex 向けのプロジェクト規約。全体像は `CLAUDE.md` と `docs/` の設計書を参照。

Codex は 2 つの使われ方をする。**どちらで起動されているかを最初に判定し、該当する節に従う**。

- **MCP ワーカー**: Claude Code から MCP サーバー `codex` 経由で呼ばれ、指示文に書かれた実装タスクをこなす（従来の使われ方）
- **直接セッション**: ユーザーが `codex` を起動し、スキル `$<name>` で定型作業を単独で回す（Phase 23〔2026-09-20〕で導入。運用の正は `docs/plans/index.html` セクション 2・3）

## プロジェクト概要

AutoContentPublisherSystem — AWS 上で動作する画像生成・SNS 自動投稿バッチシステム。
モノリポジトリ構成。サービスごとにコンテナイメージ・CDK スタック・CI/CD を分離する。

## リポジトリ構成

- `infra/` — AWS CDK プロジェクト（TypeScript）
- `services/db-readiness-check/` — DB 準備確認バッチ（Python）
- `services/image-batch/` — 画像生成バッチ（Python）
- `services/sns-post-batch/` — SNS 投稿バッチ（Python）
- `services/insights-batch/` — インサイト収集バッチ（Python）
- `shared/` — サービス間共通ライブラリ（Python）
- `database/` — DDL ファイル（スキーマ管理）
- `content/<set>/` — 事業コンテンツ資材（セット別のストック・ビルドツーリング・検証ツール）
- `docs/` — 設計書・計画・記録（HTML）。書き込みは下記「docs への書き込み条件」に従う（旧 Markdown 設計書は `docs/_archive/` にあり現役ではない）
- `.agents/skills/<name>/SKILL.md` — スキルの実体（Claude Code と共用。`.claude/skills/` は同じ実体へのシンボリックリンク）

## 技術スタック

- 言語: Python（バッチ処理）、AWS CDK は TypeScript
- DB: Aurora Serverless v2（MySQL 互換）
- 実行基盤: ECS Fargate RunTask（ECS Service は使用しない）
- ワークフロー: Step Functions Standard、スケジューラ: EventBridge Scheduler
- 既定の環境名は `prod`（CDK コマンドは `-c env=prod` を付ける）

## コーディング規約

- Python コードは PEP 8 に準拠し、型ヒントを使用する。docstring は Google スタイル
- CDK の命名は設計書（`docs/infra/stacks.html`）に合わせる（例: `FoundationStack`, `ImageBatchStack`, `SnsPostBatchStack`）
- テストは `services/<service>/tests/` に置き、`pytest` で実行する

## 共通の作業ルール

- 指示されたタスク・起動したスキルの範囲だけを実装する。関係ないファイルは変更しない
- シークレットや環境固有値はコミットしない。認証・秘密情報の規約は `docs/infra/security.html` に従う（Secrets Manager で管理）
- `cdk deploy`・本番 DDL 適用・SNS 投稿・Secrets Manager への書き込みは行わない（人間ゲート）

### サブエージェントの待機

- `wait_agent` を呼ぶたびに、`timeout_ms` には完了までの推定残り時間の 2 倍をミリ秒で明示する。ツール定義と設定の最短・最大待機時間の範囲に収め、見積もれない場合は既定時間の `120000`（120 秒）を明示する。
- 完了通知で待機は途中解除されるため、短い状態確認のために待機時間を縮めない。タイムアウト後は完了見込みを更新して同じ基準で待つ。
- 親が進められる別作業の有無は待機に入るかどうかの判断に使い、待機に入った後の時間指定には同じルールを適用する。

### docs への書き込み条件

`docs/` 配下への書き込みは、次の**どちらか**を満たすときだけ許可する。どちらでもなければ `docs/` は読み取り専用。

1. **スキル起動時**: 起動したスキルの SKILL.md がそのファイルの更新を手順に含めている（例: `$idea` の `docs/ideas/`、`$issue` の `docs/issues/`、`$quiz-stock-replenish` の `docs/plans/logic-training-1*.html`）
2. **指示文で明示**: 指示文が更新対象の docs ファイルを名指ししている

いずれの場合も、下記「直接セッションの許可パス / 禁止パス」の禁止パスには書き込まない。

## MCP ワーカー時のルール

- 指示文に書かれた対象ファイル・仕様・完了条件に従う。`docs/`・`CLAUDE.md`・`.claude/`・`.agents/` は指示文に明示がない限り変更しない
- git commit は指示された場合のみ行い、コミットメッセージは簡潔な日本語で書く（例: `設計書の参照先を整理`）。push は行わない

## 直接セッションのルール

### 許可レーン

直接セッションで扱えるのは**常に並行可のレーン**の定型作業だけ（レーンの定義は `docs/plans/index.html` セクション 2）。

- **アイデアレーン**: `$idea`（アイデアの捕捉・壁打ち・棚卸し）
- **課題レーン**: `$issue`（課題の起票・壁打ち・棚卸し）
- **セットレーン**: `$quiz-stock-replenish`（logic-training-1 の週次補充）。他セットの補充スキルは Codex 対応が済むまで対象外

**開発レーンは直接セッション禁止**（`services/` `shared/` `infra/` `database/`・共通設計書・開発計画に触れる作業。Claude Code 側の「開発レーンは常に 1 セッション」の制約はそのまま）。開発レーンに触れる必要が出たら、作業を止めて `$issue` で課題として起票し、ユーザーに報告する。

### 許可パス / 禁止パス

**許可パス**（書き込んでよい）:

- `docs/ideas/`
- `docs/issues/`
- `docs/plans/<set_code>.html` と `docs/plans/<set_code>-log.html`（セット計画書・記録。set_code は `logic-training-1` 等）
- `content/<set>/`
- `.agents/skills/`（スキル自体の修正は、スキルの手順が「スキルへ反映する」と定めた範囲に限る）

**禁止パス**（読むのはよいが書き込まない）:

- `docs/app/` `docs/infra/` `docs/strategy/` `docs/overview/` `docs/index.html`
- `docs/plans/development-plan.html` `docs/plans/development-log.html` `docs/plans/index.html`
- `services/` `shared/` `infra/` `database/`
- `CLAUDE.md` `AGENTS.md` `.claude/` `.mcp.json`

上に挙がっていないパスは禁止側として扱い、必要ならユーザーに確認する。

**例外**: ユーザーが指示文でファイルを名指しして更新を指示した場合は、禁止パスにも書き込んでよい（「docs への書き込み条件」2 と同じ扱い。指示文は本ファイルより優先される）。指示された範囲だけを変更し、ついでの修正はしない（2026-09-20 の `f335744`: ユーザー指示で `AGENTS.md` にサブエージェント待機ルールを追記した実例。23-4〔2026-09-21〕で明文化）。

### スキルの起動と実行

- スキルは `$<name>` で起動する（例: `$idea`、`$issue`、`$quiz-stock-replenish`）。手順・終了規律・ゴール行は各 `.agents/skills/<name>/SKILL.md` に従う。SKILL.md 冒頭に「Claude Code 専用」とあるスキルは起動しない
- SKILL.md の `/goal` 行は Codex でもそのまま使う。エージェント別の差分（`or stop after N turns` 句の扱い・完了申告前の再確認・リサーチとイラスト生成の手段）は各 SKILL.md 末尾の「エージェント別の差分」節に従う（23-2 で整備）
- スキルの終了規律（表の更新・コミット・push）まで完走してから終了する。途中で止める場合は、どこまで進んだかと未了の手順を報告する

### Git 運用ルール

`CLAUDE.md` の「Git 運用ルール」に従う（日本語メッセージ・`git pull --rebase origin main` を挟んで**その場で push まで**・`git add` はファイル指定・他セッションの変更を巻き込まない）。直接セッションが触るパスは CodePipeline を起動しないため、パイプライン完走確認は不要。

## 応答フォーマット

- 最終応答は簡潔にする。含めるのは「変更ファイル一覧」「実施内容の要約（5 行以内）」「実行したテスト・確認の結果」のみ
- 最終応答にコード全文や長い引用を貼らない（コードはファイルに書けば十分）
