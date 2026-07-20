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


class NavigationAndDisclosureTests(unittest.TestCase):
    def test_documents_are_grouped_and_collapsed_on_screen(self) -> None:
        html = handbook.build_html(handbook.load_documents())

        self.assertIn("出勤與請假", html)
        self.assertIn("辦公室自主管理規範", html)
        self.assertIn('<details class="document-details">', html)
        self.assertIn("HR-WI-OFF-01", html)
        self.assertIn("辦公室公共事務與值日輪值說明", html)

    def test_leave_explanation_is_nested_under_leave_procedure(self) -> None:
        html = handbook.build_html(handbook.load_documents())

        self.assertIn('<section class="related-documents" aria-label="相關文件">', html)
        self.assertIn('<details class="related-document" id="hr-fm-att-01">', html)
        self.assertEqual(html.count('id="hr-fm-att-01"'), 1)

    def test_print_styles_expand_collapsed_documents(self) -> None:
        html = handbook.build_html(handbook.load_documents())

        self.assertIn(".document-details:not([open]) > .document-content", html)
        self.assertIn(".related-document:not([open]) > .related-content", html)

    def test_document_links_open_the_target_from_the_url_hash(self) -> None:
        html = handbook.build_html(handbook.load_documents())

        self.assertIn("function openDocumentFromHash()", html)
        self.assertIn("window.addEventListener(\"hashchange\", openDocumentFromHash);", html)
        self.assertIn("details.open = true;", html)


class PublicationContentTests(unittest.TestCase):
    def test_published_html_excludes_conversion_trace_sections(self) -> None:
        html = handbook.build_html(handbook.load_documents())

        self.assertNotIn(">原始文件資訊<", html)
        self.assertNotIn(">原始文件履歷<", html)
        self.assertNotIn(">原始文件履歷 Document Revision History<", html)
        self.assertNotIn(">參考資料 Reference<", html)
        self.assertNotIn(">附錄 Appendices<", html)
        self.assertNotIn(">現行SOP表格<", html)
        self.assertNotIn(">現行SOP來源<", html)
        self.assertNotIn(">來源摘要<", html)
        self.assertNotIn(">原始相關文件<", html)
        self.assertNotIn(">現行SOP內容<", html)


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
