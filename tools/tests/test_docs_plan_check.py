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
    groups: str | None = None,
) -> str:
    """最小の正常ページ、または差し替え用の HTML を作る。"""
    body_attr = ' data-plan-format="1"' if format_attr else ""
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


if __name__ == "__main__":
    unittest.main()
