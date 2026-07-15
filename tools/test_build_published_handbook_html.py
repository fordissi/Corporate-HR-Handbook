"""Regression checks for the printable handbook HTML."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_published_handbook_html as handbook


class PrintTableLayoutTests(unittest.TestCase):
    def test_print_tables_stay_within_the_printable_page_width(self) -> None:
        html = handbook.build_html(handbook.load_documents())

        self.assertIn("table-layout: fixed;", html)
        self.assertIn("overflow-wrap: anywhere;", html)
        self.assertIn("max-width: 100%;", html)


class MermaidRenderingTests(unittest.TestCase):
    def test_mermaid_blocks_include_the_runtime_renderer(self) -> None:
        html = handbook.build_html(handbook.load_documents())

        self.assertIn('<pre class="mermaid">', html)
        self.assertIn('import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";', html)
        self.assertIn('mermaid.initialize({ startOnLoad: true, securityLevel: "strict" });', html)


class SourceTableTests(unittest.TestCase):
    def test_pay_procedure_preserves_both_salary_tables(self) -> None:
        path = handbook.HANDBOOK_DIR / "HR-PR-PAY-01_津貼加給及獎金發放程序.md"
        rendered = handbook.markdown_to_html(path.read_text(encoding="utf-8"))

        self.assertEqual(rendered.count("<th>職系</th>"), 2)
        self.assertEqual(rendered.count("<td>NT$19,000</td>"), 2)

    def test_pay_procedure_preserves_both_performance_factor_tables(self) -> None:
        path = handbook.HANDBOOK_DIR / "HR-PR-PAY-01_津貼加給及獎金發放程序.md"
        rendered = handbook.markdown_to_html(path.read_text(encoding="utf-8"))

        self.assertGreaterEqual(rendered.count("<th>績效考核分數</th>"), 3)
        self.assertEqual(rendered.count("<td>95以上</td>"), 2)

    def test_performance_procedure_preserves_both_goal_quality_tables(self) -> None:
        path = handbook.HANDBOOK_DIR / "HR-PR-PER-01_績效管理及獎懲程序.md"
        rendered = handbook.markdown_to_html(path.read_text(encoding="utf-8"))

        self.assertEqual(rendered.count("<th>項目＼適用</th>"), 2)
        self.assertEqual(rendered.count("<td>業績達成率</td>"), 2)


if __name__ == "__main__":
    unittest.main()
