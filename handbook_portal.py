import streamlit as st
import os
import re
from pathlib import Path

# --- Configuration ---
HANDBOOK_DIR = Path(r"c:\Users\fordi\antigravity\Personal Project\IDE_new_workstyle_test\HR\employee_handbook\Employee Handbook")
APP_TITLE = "企業員工手冊入口網站"
APP_SUBTITLE = "Corporate HR Handbook Portal"

# Category mapping based on filename prefixes
CATEGORIES = {
    "MN": "📚 員工手冊 (Manuals)",
    "PR": "⚙️ 流程程序 (Procedures)",
    "WI": "📝 作業指南 (Instructions)",
    "FM": "📋 表單附件 (Forms)",
}

CATEGORY_ORDER = list(CATEGORIES.values()) + ["💡 其他文件"]

DOC_GROUPS = {
    "ATT": "出勤與請假",
    "GEN": "通用、會議與申訴",
    "PAY": "薪資、津貼與獎金",
    "PER": "績效與獎懲",
    "REC": "招募與任用",
    "SEP": "離職與交接",
    "TRA": "教育訓練",
    "TRV": "差旅管理",
}


def get_category(filename):
    for prefix, name in CATEGORIES.items():
        if f"HR-{prefix}-" in filename:
            return name
    return "💡 其他文件"


def get_doc_group(filename):
    match = re.match(r"HR-(?:FM|PR)-([A-Z]+)-", filename)
    if not match:
        return "其他"
    code = match.group(1)
    return DOC_GROUPS.get(code, code)


def format_title(filename):
    # Remove extension
    name = filename.replace(".md", "")
    if "_" in name:
        parts = name.split("_")
        return f"[{parts[0]}] {parts[1]}"
    return name


def dot_quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_mermaid_node(expr, nodes):
    expr = expr.strip().rstrip(";")
    match = re.match(r"^([A-Za-z0-9_]+)\s*(?:\[([^\]]+)\]|\{([^}]+)\})?$", expr)
    if not match:
        return expr

    node_id = match.group(1)
    label = match.group(2) or match.group(3)
    shape = "diamond" if match.group(3) else "box"
    if label or node_id not in nodes:
        nodes[node_id] = {
            "label": label or node_id,
            "shape": shape,
        }
    return node_id


def mermaid_to_dot(code):
    nodes = {}
    edges = []
    rankdir = "TB"

    for raw_line in code.strip().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("%%"):
            continue
        if line.startswith("flowchart") or line.startswith("graph"):
            parts = line.split()
            if len(parts) > 1 and parts[1] == "LR":
                rankdir = "LR"
            continue

        style = "solid"
        label = ""
        source = target = None

        if "-.->" in line:
            source, target = line.split("-.->", 1)
            style = "dotted"
        else:
            labelled = re.match(r"^(.*?)\s+--\s+(.*?)\s+-->\s+(.*?)$", line)
            if labelled:
                source, label, target = labelled.groups()
            elif "-->" in line:
                source, target = line.split("-->", 1)

        if source is None or target is None:
            continue

        source_id = parse_mermaid_node(source, nodes)
        target_id = parse_mermaid_node(target, nodes)
        edges.append((source_id, target_id, label.strip(), style))

    lines = [
        "digraph G {",
        f"  rankdir={rankdir};",
        '  graph [bgcolor="transparent", pad="0.25", nodesep="0.45", ranksep="0.75"];',
        '  node [fontname="Microsoft JhengHei", fontsize="13", color="#2563eb", penwidth="1.4", style="rounded,filled", fillcolor="#e0f2fe", fontcolor="#0f172a", margin="0.14,0.08"];',
        '  edge [fontname="Microsoft JhengHei", fontsize="11", color="#475569", fontcolor="#334155", arrowsize="0.8"];',
    ]

    for node_id, node in nodes.items():
        shape = "diamond" if node["shape"] == "diamond" else "box"
        lines.append(f"  {dot_quote(node_id)} [label={dot_quote(node['label'])}, shape={shape}];")

    for source_id, target_id, label, style in edges:
        attrs = []
        if label:
            attrs.append(f"label={dot_quote(label)}")
        if style == "dotted":
            attrs.append('style="dotted"')
        attr_text = f" [{', '.join(attrs)}]" if attrs else ""
        lines.append(f"  {dot_quote(source_id)} -> {dot_quote(target_id)}{attr_text};")

    lines.append("}")
    return "\n".join(lines)


def render_mermaid(code, index):
    try:
        st.graphviz_chart(mermaid_to_dot(code), use_container_width=True)
    except Exception as error:
        st.error(f"流程圖渲染失敗：{error}")
        st.code(code, language="mermaid")


def render_content_with_mermaid(text):
    pattern = r"```mermaid\n(.*?)\n```"
    parts = re.split(pattern, text, flags=re.DOTALL)
    is_mermaid = False
    mermaid_index = 0
    for part in parts:
        if is_mermaid:
            mermaid_index += 1
            render_mermaid(part, mermaid_index)
        else:
            if part.strip():
                st.markdown(part, unsafe_allow_html=True)
        is_mermaid = not is_mermaid

# --- Page Setup ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look and STRICT CROSS-BROWSER CONSISTENCY
st.markdown("""
<style>
    /* 1. Global Reset & Theme Forcing */
    :root {
        --st-bg-color: #f1f5f9;
        --st-text-color: #1e293b;
        --st-sidebar-bg: #ffffff;
        --st-primary: #2563eb;
    }

    /* Force background and text color everywhere */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .stApp {
        background-color: var(--st-bg-color) !important;
        color: var(--st-text-color) !important;
    }
    
    /* 2. Sidebar Hardening */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], section[data-testid="stSidebar"] > div {
        background-color: var(--st-sidebar-bg) !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Force Sidebar Text to be dark */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] strong, [data-testid="stSidebar"] .stMarkdown {
        color: #334155 !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(241, 245, 249, 0.9) !important;
        backdrop-filter: blur(12px);
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* 3. Typography & Headers */
    .main-header {
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        color: #1e3a8a !important;
        margin-bottom: 0.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        color: #64748b !important;
        font-size: 1rem;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }

    .stMarkdown h1 {
        color: #0f172a !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        border-bottom: 4px solid #3b82f6;
        padding-bottom: 12px;
        margin-top: 2.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    .stMarkdown h2 {
        color: #1e40af !important;
        background: linear-gradient(90deg, #e0f2fe 0%, #f1f5f9 100%);
        padding: 12px 20px;
        border-left: 6px solid #2563eb;
        border-radius: 0 8px 8px 0;
        margin-top: 2.5rem !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    
    .stMarkdown h3 {
        color: #2563eb !important;
        font-weight: 600 !important;
        margin-top: 1.8rem !important;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 5px;
    }
    
    /* Force paragraph and list text colors */
    .stMarkdown p, .stMarkdown li {
        color: #334155 !important;
        line-height: 1.6;
    }

    /* 4. Interactive Elements */
    .stButton button {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton button:hover {
        border-color: #3b82f6 !important;
        color: #2563eb !important;
        background-color: #f0f9ff !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    [data-testid="stTextInput"] input {
        border-radius: 8px !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
    }

    .sidebar-group-label {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        margin: 14px 0 6px;
        padding: 6px 8px;
        background: #f8fafc;
        border-left: 3px solid #3b82f6;
        border-radius: 4px;
    }

    /* 5. Tables & Forms - Optimized for Physical Writing */
    .stMarkdown table {
        width: 100% !important;
        border-collapse: collapse !important;
        margin: 25px 0 !important;
        background-color: white !important;
        border: 1px solid #cbd5e1 !important;
        table-layout: auto !important;
    }
    
    .stMarkdown th {
        background-color: #f8fafc !important;
        color: #475569 !important;
        font-weight: 700 !important;
        padding: 12px !important;
        border: 1px solid #cbd5e1 !important;
        text-align: center !important;
    }
    
    .stMarkdown td {
        padding: 20px 12px !important; /* Large vertical padding for signing */
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
        vertical-align: middle !important;
    }
    
    /* Make the second to last column (usually 'Signature') much wider */
    .stMarkdown td:nth-last-child(2), .stMarkdown th:nth-last-child(2) {
        min-width: 180px !important;
    }

    /* 6. Print Optimization */
    @media print {
        header, [data-testid="stSidebar"], .stButton, .print-box, .stCaption, [data-testid="stHeader"], .no-print {
            display: none !important;
        }
        [data-testid="stAppViewContainer"] {
            background-color: white !important;
            padding: 0 !important;
        }
        .main, .stApp {
            background-color: white !important;
        }
        .stMarkdown h2 {
            background: none !important;
            border-left: 5px solid #000 !important;
        }
        /* Pagination optimization */
        tr {
            page-break-inside: avoid !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Logic ---
st.sidebar.image("https://img.icons8.com/fluency/96/business-building.png", width=70)
st.sidebar.title("文檔導覽")

search_query = st.sidebar.text_input("🔍 搜尋關鍵字", placeholder="例如：假別、加班...")

all_files = sorted([f for f in os.listdir(HANDBOOK_DIR) if f.endswith(".md")])
grouped_files = {}

for f in all_files:
    cat = get_category(f)
    if cat not in grouped_files:
        grouped_files[cat] = []
    
    if not search_query or search_query.lower() in f.lower():
        try:
            with open(HANDBOOK_DIR / f, "r", encoding="utf-8") as file_content:
                if not search_query or search_query.lower() in file_content.read().lower():
                    grouped_files[cat].append(f)
        except: pass

st.sidebar.markdown("---")

default_file = "HR-MN-QM-01_員工管理手冊.md"
if 'current_file' not in st.session_state:
    st.session_state.current_file = default_file if os.path.exists(HANDBOOK_DIR / default_file) else (all_files[0] if all_files else None)

for cat_name in CATEGORY_ORDER:
    files = grouped_files.get(cat_name, [])
    if not files: continue
    with st.sidebar.expander(cat_name, expanded=(cat_name == "📚 員工手冊 (Manuals)")):
        if cat_name in {"📋 表單附件 (Forms)", "⚙️ 流程程序 (Procedures)"}:
            grouped_by_function = {}
            for f in files:
                grouped_by_function.setdefault(get_doc_group(f), []).append(f)

            for group_name in sorted(grouped_by_function):
                st.markdown(f"<div class='sidebar-group-label'>{group_name}</div>", unsafe_allow_html=True)
                for f in grouped_by_function[group_name]:
                    if st.button(format_title(f), key=f, use_container_width=True):
                        st.session_state.current_file = f
        else:
            for f in files:
                if st.button(format_title(f), key=f, use_container_width=True):
                    st.session_state.current_file = f

# --- Main Area ---
if st.session_state.current_file:
    try:
        with open(HANDBOOK_DIR / st.session_state.current_file, "r", encoding="utf-8") as f:
            full_content = f.read()

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<h1 class='main-header no-print'>{APP_TITLE}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p class='sub-header no-print'>{APP_SUBTITLE}</p>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='portal-meta no-print' style='text-align: right; color: #64748b; font-size: 0.8rem;'>版本: 2026.04<br>人力資源部發布</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="print-box no-print" style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 18px; border-radius: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.2rem;">🖨️</span>
            <div style="color: #166534; font-size: 0.95rem;"><strong>需要公告或列印嗎？</strong> 直接按下 <kbd>Ctrl</kbd>+<kbd>P</kbd>，系統已優化排版，可直接存成 PDF。</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='no-print'>", unsafe_allow_html=True)
        render_content_with_mermaid(full_content)
        st.markdown("---")
        st.markdown(f"<div style='color: #94a3b8; font-size: 0.75rem;'>文件編號: {st.session_state.current_file}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"讀取失敗: {e}")
else:
    st.info("請從左側選擇文件。")

st.sidebar.markdown("---")
st.sidebar.info("💡 MD 原始檔妥善保存在 Git 中，本站僅供查閱。")
