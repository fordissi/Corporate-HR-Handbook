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


if __name__ == "__main__":
    unittest.main()
