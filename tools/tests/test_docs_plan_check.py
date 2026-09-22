"""docs_plan_check の回帰テスト。"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import docs_plan_check as checker  # noqa: E402


def page(
    steps: str | None = None, *, format_attr: bool = True, legacy: str = "",
    groups: str | None = None, plan_steps: str | None = None,
) -> str:
    """最小の正常ページ、または差し替え用の HTML を作る。"""
    body_attr = ' data-plan-format="1"' if format_attr else ""
    if plan_steps is not None:
        body_attr += f' data-plan-steps="{plan_steps}"'
    if groups is None:
        content = step() if steps is None else steps
        groups = f'<div data-plan-group="active">{content}</div>'
    return f"""<!doctype html><html><body{body_attr}>
    <section class="plan-phase" data-plan-phase="1">{groups}</section>{legacy}
    </body></html>"""


def step(
    step_id: str = "1", *, status: str = "todo", kind: str = "",
    completed: str | None = None, record: str | None = None,
    acceptance_tag: str = "ul", extra: str = "",
) -> str:
    """通常形式の最小ステップを作る。"""
    completed_attr = f' data-completed="{completed}"' if completed else ""
    kind_attr = f' data-kind="{kind}"' if kind else ""
    record_html = record if record is not None else (
        '<details data-field="record"><summary>記録</summary><p>作業前</p></details>'
    )
    label = "ゴール対象外" if kind == "decision" else ""
    stop = "ゴールにしない" if kind == "decision" else "停止点"
    return f"""<article class="plan-step" id="step-{step_id}"
    data-step-id="{step_id}" data-status="{status}"{completed_attr}{kind_attr}>
    <div data-field="overview">概要 {label}</div>
    <p data-field="prerequisites">なし</p>
    <p data-field="constraints">なし</p>
    <{acceptance_tag} data-field="acceptance"><li>確認</li></{acceptance_tag}>
    <p data-field="gate">なし</p><p data-field="stop">{stop}</p>
    <p data-field="result">未着手</p>{record_html}{extra}</article>"""


def rules(html: str) -> set[str]:
    """検査結果から規則 ID の集合を返す。"""
    return {finding.rule for finding in checker.check_text("test.html", html)}


class DocsPlanCheckTests(unittest.TestCase):
    """正例と個別の構造違反を検査する。"""

    def test_template_is_valid(self) -> None:
        """唯一の正例テンプレートが検査を通る。"""
        findings = checker.check_file(REPO_ROOT / "docs/plans/_templates/step.html")
        self.assertEqual([], findings)

    def test_minimal_normal_page_and_statuses_are_valid(self) -> None:
        """最小ページと全ステータスを受け入れる。"""
        statuses = "".join([
            step("todo", status="todo"), step("doing", status="doing"),
            step("blocked", status="blocked"),
        ])
        done = step("done", status="done", completed="2026-09-21")
        groups = (
            f'<details data-plan-group="done">{done}</details>'
            f'<div data-plan-group="active">{statuses}</div>'
        )
        self.assertEqual(set(), rules(page(groups=groups)))

    def test_exception_forms_and_section_record_are_valid(self) -> None:
        """decision、legacy-completed、section 記録を受け入れる。"""
        legacy_record = (
            '<section data-field="record"><a href="log.html">記録</a></section>'
        )
        legacy = step("old", status="done", completed="2026-09-01",
                      kind="legacy-completed", record=legacy_record)
        decision = step("decision", kind="decision")
        groups = (
            f'<details data-plan-group="done">{legacy}</details>'
            f'<div data-plan-group="active">{decision}</div>'
        )
        self.assertEqual(set(), rules(page(groups=groups)))

    def test_field_missing_and_empty(self) -> None:
        """必須欄の欠落と空欄を報告する。"""
        missing = step().replace('<p data-field="gate">なし</p>', "")
        empty = step("2").replace('概要 ', "")
        self.assertIn("field-missing", rules(page(missing)))
        self.assertIn("field-empty", rules(page(empty)))

    def test_duplicates_reported(self) -> None:
        """ステップ ID、HTML ID、欄の重複を報告する。"""
        duplicate = step() + step("1", extra='<p data-field="gate">重複</p>')
        found = rules(page(duplicate))
        self.assertIn("step-duplicate", found)
        self.assertIn("field-duplicate", found)

    def test_open_folds_and_group_reported(self) -> None:
        """初期展開の折りたたみと完了グループを報告する。"""
        open_step = step(
            record='<details data-field="record" open><p>記録</p></details>',
            extra='<details data-field="implementation" open><p>詳細</p></details>',
        )
        groups = f'<details data-plan-group="done" open>{open_step}</details>'
        found = rules(page(groups=groups))
        self.assertIn("fold-open", found)
        self.assertIn("group-open", found)

    def test_required_field_in_fold_reported(self) -> None:
        """折りたたみ内の必須欄を報告する。"""
        broken = step().replace(
            '<div data-field="overview">概要 </div>',
            (
                '<details data-field="implementation">'
                '<div data-field="overview">概要</div></details>'
            ),
        )
        self.assertIn("field-in-fold", rules(page(broken)))

    def test_step_group_mismatch_both_directions(self) -> None:
        """完了と未完了のグループ取り違えを報告する。"""
        done = step(status="done", completed="2026-09-01")
        todo = step("2", status="todo")
        groups = (
            f'<details data-plan-group="done">{todo}</details>'
            f'<div data-plan-group="active">{done}</div>'
        )
        self.assertIn("step-group", rules(page(groups=groups)))

    def test_group_tag_and_order(self) -> None:
        """完了グループのタグと順序を報告する。"""
        groups = (
            f'<div data-plan-group="active">{step()}</div>'
            + (
                '<div data-plan-group="done">'
                f'{step("2", status="done", completed="2026-09-01")}</div>'
            )
        )
        found = rules(page(groups=groups))
        self.assertIn("group-tag", found)
        self.assertIn("group-order", found)

    def test_page_level_rules(self) -> None:
        """ページ形式、空ページ、旧形式混在を報告する。"""
        self.assertIn("page-format", rules(page(format_attr=False)))
        self.assertIn("page-empty", rules(page(steps="")))
        self.assertIn("page-legacy-mixed", rules(page(legacy="<li>✅ 古い行</li>")))
        self.assertNotIn(
            "page-legacy-mixed",
            rules(page(legacy="<li><code>✅ 例</code></li>")),
        )

    def test_step_less_page_declaration(self) -> None:
        """ステップ 0 件の宣言（25-5）を検査する。"""
        declared_empty = page(steps="", plan_steps="none")
        self.assertNotIn("page-empty", rules(declared_empty))
        self.assertIn(
            "page-steps-declared", rules(page(plan_steps="none"))
        )
        self.assertIn(
            "page-steps-unknown", rules(page(steps="", plan_steps="few"))
        )
        self.assertIn("page-empty", rules(page(steps="", plan_steps="few")))

    def test_status_completion_and_acceptance_rules(self) -> None:
        """状態、完了日、完了条件タグを報告する。"""
        malformed = step().replace('id="step-1"', 'id="wrong"')
        self.assertIn("step-attrs", rules(page(malformed)))
        self.assertIn("step-status", rules(page(step(status="later"))))
        self.assertIn("step-completed", rules(page(step(status="done"))))
        self.assertIn("acceptance-tag", rules(page(step(acceptance_tag="p"))))

    def test_record_rules(self) -> None:
        """記録の欠落、section リンク不足、legacy リンク不足を報告する。"""
        no_record = step(record="")
        section = step(record='<section data-field="record">記録</section>')
        empty = step(record='<details data-field="record"></details>')
        legacy = step(status="done", completed="2026-09-01", kind="legacy-completed",
                      record='<details data-field="record">記録</details>')
        self.assertIn("record-missing", rules(page(no_record)))
        self.assertIn("record-link", rules(page(section)))
        self.assertIn("record-empty", rules(page(empty)))
        self.assertIn(
            "kind-legacy-record",
            rules(page(groups=f'<details data-plan-group="done">{legacy}</details>')),
        )

    def test_phase_group_fold_and_kind_rules(self) -> None:
        """残る個別規則を報告する。"""
        outside = '<body data-plan-format="1">' + step() + '</body>'
        self.assertIn("phase-missing", rules(outside))
        self.assertIn("group-missing", rules(outside))
        nested = step(extra=(
            (
                '<details data-field="implementation">'
                '<details data-field="record">x</details></details>'
            )
        ))
        self.assertIn("fold-separate", rules(page(nested)))
        self.assertIn(
            "fold-tag",
            rules(page(step(extra='<div data-field="implementation">x</div>'))),
        )
        decision = step(kind="decision").replace("ゴール対象外", "判断")
        self.assertIn("kind-decision-label", rules(page(decision)))
        self.assertIn(
            "kind-decision-stop",
            rules(page(step(kind="decision").replace("ゴールにしない", "停止"))),
        )
        legacy = step(status="todo", kind="legacy-completed")
        self.assertIn("kind-legacy-status", rules(page(legacy)))
        unknown = step(kind="other")
        self.assertIn("kind-unknown", rules(page(unknown)))

    def test_missing_file_registered_and_formatting(self) -> None:
        """存在しないファイルと API の整形結果を確認する。"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = checker.REGISTERED_PAGES
            try:
                checker.REGISTERED_PAGES = ("missing.html",)
                found = checker.check_registered(root)
            finally:
                checker.REGISTERED_PAGES = original
        self.assertEqual(["page-missing"], [item.rule for item in found])
        self.assertEqual(
            ["x.html / - / page-missing: ありません"],
            checker.format_findings([
                checker.PlanFinding("x.html", "-", "page-missing", "ありません")
            ]),
        )


class PlanLifecycleTests(unittest.TestCase):
    """日常更新の一巡（追加 → 追記 → 完了移動 → 記録リンク）を検査する。"""

    RECORD_TODO = '<details data-field="record"><summary>作業記録</summary>' \
        "<p>着手前のため記録なし。</p></details>"
    RECORD_DOING = '<details data-field="record"><summary>作業記録</summary>' \
        "<p>2026-09-21: 下書きを作成。</p></details>"
    RECORD_LINK = '<section data-field="record">' \
        '<a href="development-log.html#step-00-9">開発記録</a></section>'

    def stage_new(self) -> str:
        """1. テンプレートの枠をコピーして未着手ステップを足した状態。"""
        return page(groups='<div data-plan-group="active">' + step(
            "00-9", record=self.RECORD_TODO) + "</div>")

    def stage_doing(self) -> str:
        """2. 作業中に記録へ追記し、状態と現況を更新した状態。"""
        return page(groups='<div data-plan-group="active">' + step(
            "00-9", status="doing", record=self.RECORD_DOING) + "</div>")

    def stage_done(self) -> str:
        """3. 完了日を付け、同フェーズの完了済みグループへ移した状態。"""
        done = step("00-9", status="done", completed="2026-09-21",
                    record=self.RECORD_DOING)
        return page(groups=(
            f'<details data-plan-group="done">{done}</details>'
            f'<div data-plan-group="active">{step("00-10")}</div>'
        ))

    def stage_migrated(self) -> str:
        """4. 計画整理で記録本文を log へ移し、リンクへ置き換えた状態。"""
        done = step("00-9", status="done", completed="2026-09-21",
                    record=self.RECORD_LINK)
        return page(groups=(
            f'<details data-plan-group="done">{done}</details>'
            f'<div data-plan-group="active">{step("00-10")}</div>'
        ))

    def test_each_stage_passes(self) -> None:
        """一巡の各段階がそのまま検査を通る。"""
        for name, html in (
            ("new", self.stage_new()), ("doing", self.stage_doing()),
            ("done", self.stage_done()), ("migrated", self.stage_migrated()),
        ):
            with self.subTest(stage=name):
                self.assertEqual(set(), rules(html))

    def test_new_stage_rejects_missing_field(self) -> None:
        """1. 完了条件を書き忘れた追加は NG。"""
        broken = self.stage_new().replace(
            '<ul data-field="acceptance"><li>確認</li></ul>', "")
        self.assertIn("field-missing", rules(broken))

    def test_doing_stage_rejects_fold_violations(self) -> None:
        """2. 追記時に記録を初期展開・完了条件を折りたたみへ入れるのは NG。"""
        opened = self.stage_doing().replace(
            '<details data-field="record">', '<details data-field="record" open>')
        self.assertIn("fold-open", rules(opened))
        buried = self.stage_doing().replace(
            '<ul data-field="acceptance"><li>確認</li></ul>',
            '<details data-field="implementation">'
            '<ul data-field="acceptance"><li>確認</li></ul></details>',
        )
        self.assertIn("field-in-fold", rules(buried))

    def test_done_stage_rejects_placement_and_date(self) -> None:
        """3. 完了済みを進行中に残す・完了日を付け忘れるのは NG。"""
        stay = page(groups='<div data-plan-group="active">' + step(
            "00-9", status="done", completed="2026-09-21",
            record=self.RECORD_DOING) + "</div>")
        self.assertIn("step-group", rules(stay))
        undated = self.stage_done().replace(' data-completed="2026-09-21"', "")
        self.assertIn("step-completed", rules(undated))

    def test_migrated_stage_rejects_link_less_record(self) -> None:
        """4. 記録本文を移した後にリンクを張らないのは NG。"""
        broken = self.stage_migrated().replace(
            '<a href="development-log.html#step-00-9">開発記録</a>', "開発記録")
        self.assertIn("record-link", rules(broken))


if __name__ == "__main__":
    unittest.main()
