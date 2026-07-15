from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HANDBOOK_DIR = ROOT / "Employee Handbook"
OUTPUT_DIR = ROOT / "output" / "published_handbook"
OUTPUT_FILE = OUTPUT_DIR / "index.html"

ACTIVE_FILES = [
    "HR-MN-QM-01_員工管理手冊.md",
    "HR-PR-ATT-02_內勤人員出勤管理程序.md",
    "HR-PR-ATT-01_員工請假管理程序.md",
    "HR-FM-ATT-01_員工假別說明表.md",
    "HR-PR-ATT-04_加班申請作業程序.md",
    "HR-PR-TRV-01_員工差旅管理程序.md",
    "HR-PR-PAY-01_津貼加給及獎金發放程序.md",
    "HR-PR-PER-01_績效管理及獎懲程序.md",
    "HR-PR-SEP-01_員工離職管理程序.md",
]

NAV_GROUPS = [
    ("文件總覽", ["HR-MN-QM-01"]),
    ("出勤與請假", ["HR-PR-ATT-02", "HR-PR-ATT-01", "HR-FM-ATT-01", "HR-PR-ATT-04"]),
    ("差旅與薪酬", ["HR-PR-TRV-01", "HR-PR-PAY-01"]),
    ("績效與離職", ["HR-PR-PER-01", "HR-PR-SEP-01"]),
]

CATEGORY_LABELS = {
    "MN": "管理手冊",
    "PR": "管理程序",
    "FM": "表單與說明表",
    "WI": "作業指導書",
}

FUNCTION_LABELS = {
    "QM": "文件管理",
    "ATT": "出勤與請假",
    "PAY": "薪酬與獎金",
    "PER": "績效與獎懲",
    "SEP": "離職與交接",
    "TRV": "差旅與費用",
}


@dataclass
class Document:
    path: Path
    slug: str
    metadata: dict[str, str]
    body: str
    html_body: str

    @property
    def doc_id(self) -> str:
        return self.metadata.get("doc_id") or self.path.stem.split("_", 1)[0]

    @property
    def title(self) -> str:
        if self.metadata.get("title"):
            return self.metadata["title"]
        if "_" in self.path.stem:
            return self.path.stem.split("_", 1)[1]
        return self.path.stem

    @property
    def version(self) -> str:
        return self.metadata.get("version", "")

    @property
    def last_updated(self) -> str:
        return self.metadata.get("last_updated", "")

    @property
    def status(self) -> str:
        return self.metadata.get("status", "")

    @property
    def category(self) -> str:
        parts = self.doc_id.split("-")
        return CATEGORY_LABELS.get(parts[1], parts[1] if len(parts) > 1 else "")

    @property
    def function(self) -> str:
        parts = self.doc_id.split("-")
        return FUNCTION_LABELS.get(parts[2], parts[2] if len(parts) > 2 else "")


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---", 4)
    if end == -1:
        return {}, text

    raw_meta = text[4:end].strip()
    body = text[end + 4 :].lstrip("\r\n")
    metadata: dict[str, str] = {}

    current_key = ""
    for line in raw_meta.splitlines():
        if not line.strip() or line.lstrip().startswith("- "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key:
            metadata[key] = value
            current_key = key
        elif current_key:
            metadata[current_key] = f"{metadata[current_key]} {value}".strip()

    return metadata, body


def slugify(doc_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", doc_id).strip("-").lower()


def inline_markdown(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<span class="md-link">\1</span>', escaped)
    return escaped


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table(rows: list[str]) -> str:
    if len(rows) < 2:
        return "\n".join(f"<p>{inline_markdown(row)}</p>" for row in rows)

    header = split_table_row(rows[0])
    body_rows = [split_table_row(row) for row in rows[2:]]

    output = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    output.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    output.append("</tr></thead>")
    output.append("<tbody>")
    for row in body_rows:
        output.append("<tr>")
        output.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
        output.append("</tr>")
    output.append("</tbody></table></div>")
    return "\n".join(output)


def markdown_to_html(markdown: str) -> str:
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    table_rows: list[str] = []
    code_lines: list[str] = []
    in_code = False
    code_language = ""

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph if part.strip())
            output.append(f"<p>{inline_markdown(text)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            output.append("<ul>")
            output.extend(f"<li>{inline_markdown(item)}</li>" for item in list_items)
            output.append("</ul>")
            list_items = []

    def flush_table() -> None:
        nonlocal table_rows
        if table_rows:
            output.append(render_table(table_rows))
            table_rows = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_table()
            if in_code:
                language_class = f" language-{html.escape(code_language)}" if code_language else ""
                code = html.escape("\n".join(code_lines))
                if code_language == "mermaid":
                    output.append(f"<figure class=\"mermaid-block\"><pre class=\"mermaid\">{code}</pre></figure>")
                else:
                    output.append(f"<pre class=\"code-block\"><code class=\"{language_class}\">{code}</code></pre>")
                code_lines = []
                code_language = ""
                in_code = False
            else:
                in_code = True
                code_language = stripped.removeprefix("```").strip()
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            table_rows.append(stripped)
            continue

        if table_rows:
            flush_table()

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            flush_paragraph()
            flush_list()
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            output.append(f"<h{level}>{inline_markdown(text)}</h{level}>")
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            flush_list()
            quote = stripped.lstrip(">").strip()
            output.append(f"<blockquote>{inline_markdown(quote)}</blockquote>")
            continue

        bullet_match = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet_match:
            flush_paragraph()
            list_items.append(bullet_match.group(1).strip())
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_table()

    return "\n".join(output)


def load_documents() -> list[Document]:
    documents: list[Document] = []
    for file_name in ACTIVE_FILES:
        path = HANDBOOK_DIR / file_name
        text = path.read_text(encoding="utf-8")
        metadata, body = split_front_matter(text)
        doc_id = metadata.get("doc_id") or path.stem.split("_", 1)[0]
        documents.append(
            Document(
                path=path,
                slug=slugify(doc_id),
                metadata=metadata,
                body=body,
                html_body=markdown_to_html(body),
            )
        )
    return documents


def render_meta_items(document: Document) -> str:
    items = [
        ("文件編號", document.doc_id),
        ("版本", document.version),
        ("狀態", "已發行" if document.status == "active" else document.status),
        ("最後更新", document.last_updated),
        ("分類", f"{document.category} / {document.function}"),
    ]
    return "\n".join(
        f"<div class=\"meta-item\"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>"
        for label, value in items
        if value
    )


def render_nav(documents: list[Document]) -> str:
    documents_by_id = {document.doc_id: document for document in documents}
    groups: list[str] = []

    for label, doc_ids in NAV_GROUPS:
        links = []
        for doc_id in doc_ids:
            document = documents_by_id.get(doc_id)
            if not document:
                continue
            links.append(
                f"<a href=\"#{document.slug}\"><span>{html.escape(document.doc_id)}</span>{html.escape(document.title)}</a>"
            )
        if links:
            groups.append(
                f"""
                <section class="nav-group">
                  <h2>{html.escape(label)}</h2>
                  {"".join(links)}
                </section>
                """
            )

    return "\n".join(groups)


def build_html(documents: list[Document]) -> str:
    nav = render_nav(documents)
    cards = "\n".join(
        f"""
        <article class="summary-card">
          <span>{html.escape(document.function)}</span>
          <strong>{html.escape(document.doc_id)}</strong>
          <p>{html.escape(document.title)}</p>
        </article>
        """
        for document in documents
    )
    sections = "\n".join(
        f"""
        <section class="document" id="{document.slug}">
          <header class="document-cover">
            <p class="eyebrow">{html.escape(document.category)} · {html.escape(document.function)}</p>
            <h2>{html.escape(document.title)}</h2>
            <div class="document-meta">
              {render_meta_items(document)}
            </div>
          </header>
          <div class="document-content">
            {document.html_body}
          </div>
        </section>
        """
        for document in documents
    )

    return "\n".join(line.rstrip() for line in f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>已發行人事管理文件</title>
  <style>
    :root {{
      --paper: #fbfaf6;
      --surface: #ffffff;
      --ink: #1d2528;
      --muted: #637176;
      --line: #d9d2c3;
      --accent: #2f6f73;
      --accent-dark: #1f4f53;
      --warm: #efe7d5;
      --table-head: #f1eadc;
      --shadow: 0 16px 50px rgba(37, 43, 39, 0.12);
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Noto Serif TC", "Microsoft JhengHei", "PingFang TC", serif;
      font-size: 16px;
      line-height: 1.78;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    .layout {{
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      min-height: 100vh;
    }}

    .sidebar {{
      position: sticky;
      top: 0;
      align-self: start;
      height: 100vh;
      overflow: auto;
      padding: 28px 20px;
      background: #ebe4d3;
      border-right: 1px solid var(--line);
    }}

    .brand {{
      padding-bottom: 22px;
      border-bottom: 1px solid rgba(85, 78, 62, 0.24);
      margin-bottom: 22px;
    }}

    .brand strong {{
      display: block;
      font-size: 1.35rem;
      line-height: 1.35;
      color: var(--accent-dark);
    }}

    .brand span {{
      display: block;
      margin-top: 8px;
      color: #6a6252;
      font-size: 0.92rem;
    }}

    .nav {{
      display: grid;
      gap: 18px;
    }}

    .nav-group {{
      display: grid;
      gap: 6px;
    }}

    .nav-group h2 {{
      margin: 0 0 3px;
      padding: 0 12px 5px;
      color: #766d5b;
      border-bottom: 1px solid rgba(85, 78, 62, 0.18);
      font-family: "Segoe UI", "Microsoft JhengHei", sans-serif;
      font-size: 0.76rem;
      font-weight: 800;
      letter-spacing: 0.12em;
    }}

    .nav a {{
      display: grid;
      gap: 2px;
      padding: 10px 12px;
      border-radius: 6px;
      color: #293334;
      border: 1px solid transparent;
    }}

    .nav a:hover {{
      background: rgba(255, 255, 255, 0.56);
      border-color: rgba(47, 111, 115, 0.22);
    }}

    .nav span {{
      font-family: "Segoe UI", sans-serif;
      font-size: 0.75rem;
      letter-spacing: 0.06em;
      color: var(--accent-dark);
      font-weight: 700;
    }}

    .actions {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
      margin-top: 24px;
    }}

    button {{
      border: 1px solid var(--accent);
      background: var(--accent);
      color: white;
      border-radius: 6px;
      padding: 10px 12px;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }}

    main {{
      padding: 42px min(5vw, 72px) 80px;
    }}

    .hero {{
      max-width: 1100px;
      margin: 0 auto 34px;
      padding-bottom: 28px;
      border-bottom: 2px solid var(--accent-dark);
    }}

    .hero p {{
      max-width: 760px;
      margin: 12px 0 0;
      color: var(--muted);
    }}

    h1 {{
      margin: 0;
      color: var(--accent-dark);
      font-size: clamp(2rem, 4vw, 3.7rem);
      line-height: 1.12;
      font-weight: 800;
    }}

    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 12px;
      max-width: 1100px;
      margin: 0 auto 34px;
    }}

    .summary-card {{
      background: rgba(255, 255, 255, 0.72);
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 15px 16px;
    }}

    .summary-card span {{
      color: var(--accent-dark);
      font-size: 0.82rem;
      font-weight: 700;
    }}

    .summary-card strong {{
      display: block;
      margin-top: 8px;
      font-family: "Segoe UI", sans-serif;
      font-size: 0.9rem;
    }}

    .summary-card p {{
      margin: 4px 0 0;
      color: var(--muted);
      line-height: 1.5;
    }}

    .document {{
      max-width: 1100px;
      margin: 0 auto 34px;
      background: var(--surface);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }}

    .document-cover {{
      padding: 30px 34px 24px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #fffdf8 0%, #f5efe1 100%);
    }}

    .eyebrow {{
      margin: 0 0 8px;
      color: var(--accent-dark);
      font-family: "Segoe UI", sans-serif;
      font-size: 0.82rem;
      font-weight: 800;
      letter-spacing: 0.08em;
    }}

    .document h2 {{
      margin: 0;
      color: #172326;
      font-size: 2rem;
      line-height: 1.25;
    }}

    .document-meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin-top: 22px;
    }}

    .meta-item {{
      border-left: 3px solid var(--accent);
      padding-left: 10px;
    }}

    .meta-item span {{
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
    }}

    .meta-item strong {{
      display: block;
      line-height: 1.4;
    }}

    .document-content {{
      padding: 26px 34px 42px;
    }}

    .document-content h1 {{
      margin: 0 0 22px;
      font-size: 2rem;
      color: #172326;
    }}

    .document-content h2 {{
      margin: 34px 0 12px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--line);
      font-size: 1.42rem;
      color: var(--accent-dark);
    }}

    .document-content h3 {{
      margin: 24px 0 8px;
      font-size: 1.13rem;
      color: #2c3a3d;
    }}

    .document-content p {{
      margin: 10px 0;
    }}

    .document-content ul {{
      margin: 10px 0 18px 1.2em;
      padding: 0;
    }}

    .document-content li {{
      margin: 6px 0;
    }}

    .table-wrap {{
      width: 100%;
      overflow-x: auto;
      margin: 16px 0 24px;
      border: 1px solid var(--line);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      background: white;
      font-size: 0.95rem;
    }}

    th, td {{
      border: 1px solid var(--line);
      padding: 9px 10px;
      vertical-align: top;
      text-align: left;
    }}

    th {{
      background: var(--table-head);
      color: #273335;
      font-weight: 800;
    }}

    blockquote {{
      margin: 16px 0;
      padding: 12px 16px;
      border-left: 4px solid var(--accent);
      background: #f7f3ea;
      color: #354346;
    }}

    code {{
      font-family: "Cascadia Mono", Consolas, monospace;
      font-size: 0.92em;
      background: #f3efe6;
      padding: 0 4px;
      border-radius: 4px;
    }}

    .code-block {{
      overflow-x: auto;
      padding: 14px;
      background: #f3efe6;
      border: 1px solid var(--line);
      white-space: pre-wrap;
    }}

    .mermaid-block {{
      margin: 16px 0 24px;
      padding: 18px;
      overflow-x: auto;
      border: 1px solid var(--line);
      background: #fcfbf7;
    }}

    .mermaid {{
      margin: 0;
      background: transparent;
      font-family: inherit;
    }}

    .mermaid svg {{
      display: block;
      max-width: 100%;
      height: auto;
    }}

    .md-link {{
      color: var(--accent-dark);
      font-weight: 700;
    }}

    @media (max-width: 900px) {{
      .layout {{
        display: block;
      }}

      .sidebar {{
        position: relative;
        height: auto;
      }}

      main {{
        padding: 28px 18px 52px;
      }}

      .document-cover,
      .document-content {{
        padding-left: 20px;
        padding-right: 20px;
      }}
    }}

    @media print {{
      @page {{
        size: A4;
        margin: 14mm 12mm;
      }}

      body {{
        background: white;
        color: black;
        font-size: 11pt;
        line-height: 1.55;
      }}

      .layout {{
        display: block;
      }}

      .sidebar,
      .summary-grid,
      .actions {{
        display: none !important;
      }}

      main {{
        padding: 0;
      }}

      .hero {{
        margin: 0 0 10mm;
        padding-bottom: 7mm;
        border-bottom: 1.5pt solid #000;
      }}

      h1 {{
        color: black;
        font-size: 24pt;
      }}

      .hero p {{
        color: #333;
      }}

      .document {{
        margin: 0;
        border: 0;
        box-shadow: none;
        page-break-before: always;
        break-before: page;
      }}

      .document:first-of-type {{
        page-break-before: auto;
        break-before: auto;
      }}

      .document-cover {{
        padding: 0 0 6mm;
        background: white;
        border-bottom: 1pt solid #000;
      }}

      .document h2,
      .document-content h1 {{
        color: black;
      }}

      .document-content {{
        padding: 6mm 0 0;
      }}

      .document-content h2 {{
        color: black;
        page-break-after: avoid;
        break-after: avoid;
      }}

      .document-content h3,
      .document-content p,
      .document-content li {{
        orphans: 3;
        widows: 3;
      }}

      .table-wrap {{
        width: 100%;
        max-width: 100%;
        overflow: visible;
        border: 0;
        page-break-inside: avoid;
        break-inside: avoid;
      }}

      table {{
        width: 100%;
        max-width: 100%;
        table-layout: fixed;
        font-size: 9.5pt;
        page-break-inside: auto;
      }}

      tr {{
        page-break-inside: avoid;
        break-inside: avoid;
      }}

      th {{
        background: #efefef !important;
        color: black;
      }}

      th, td {{
        padding: 5pt 6pt;
        border: 0.6pt solid #777;
        overflow-wrap: anywhere;
      }}

      .mermaid-block {{
        padding: 4mm;
        overflow: visible;
        background: white;
        page-break-inside: avoid;
        break-inside: avoid;
      }}

      .meta-item {{
        border-left: 0;
        padding-left: 0;
      }}

      .meta-item span {{
        color: #333;
      }}

      a[href]::after {{
        content: "";
      }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <strong>已發行人事管理文件</strong>
        <span>Corporate HR Handbook · Published Set</span>
      </div>
      <nav class="nav" aria-label="文件目錄">
        {nav}
      </nav>
      <div class="actions">
        <button type="button" onclick="window.print()">列印 / 另存 PDF</button>
      </div>
    </aside>
    <main>
      <header class="hero">
        <h1>已發行人事管理文件</h1>
        <p>本頁彙整已審核、現行執行或已可發行之人事管理文件。螢幕版提供目錄快速跳轉；列印時將自動轉為 A4 友善版面，並以每份文件為分頁單位。</p>
      </header>
      <section class="summary-grid" aria-label="文件摘要">
        {cards}
      </section>
      {sections}
    </main>
  </div>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
    mermaid.initialize({{ startOnLoad: true, securityLevel: "strict" }});
  </script>
</body>
</html>
""".splitlines()) + "\n"


def main() -> None:
    documents = load_documents()
    inactive = [document.doc_id for document in documents if document.status != "active"]
    if inactive:
        raise SystemExit(f"These documents are not active: {', '.join(inactive)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(build_html(documents), encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
