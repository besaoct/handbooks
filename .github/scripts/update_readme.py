#!/usr/bin/env python3
"""
update_readme.py
Scans the handbooks/ directory, extracts metadata from each handbook HTML file,
and dynamically updates the README.md table and repository structure tree.
Also generates an interactive index.html portal for GitHub Pages.
"""

import os
import re
import html
import glob

REPO_OWNER = "besaoct"
REPO_NAME = "handbooks"
PAGES_BASE_URL = f"https://{REPO_OWNER}.github.io/{REPO_NAME}"
HANDBOOKS_DIR = "handbooks"
README_FILE = "README.md"
INDEX_FILE = "index.html"

# Known curated metadata fallbacks / highlights for well-known handbooks
CURATED_METADATA = {
    "db-sql.html": {
        "name": "SQL & Systems",
        "description": "1000+ problems with solutions. Covers SELECT, Joins, Aggregation, Subqueries & CTEs, Window functions, DDL/DML, Transactions & Locking, Indexing & Query Plans, Database internals, Replication, Sharding, Caching, and Datastore tradeoffs."
    },
    "devops-and-git.html": {
        "name": "DevOps & Git",
        "description": "Git object database internals, Linux systems & networking, Containers & Docker, Kubernetes orchestration, CI/CD pipelines, Infrastructure as Code, Observability, Incident response, and Production safety."
    },
    "express-mongo.html": {
        "name": "Express & MongoDB",
        "description": "Node.js runtime, Event loop, HTTP/TCP sockets, Express middleware pipeline, Routing, Authentication & JWT, Security hardening, MongoDB schema design, Aggregation pipeline, Mongoose internals, and API performance."
    },
    "flutter.html": {
        "name": "Flutter & Dart",
        "description": "Dart type system & runtime, Widget tree architecture, Element & RenderObject lifecycle, Layout constraints & hit testing, State management paradigms, Animations, Platform channels, and Performance profiling."
    },
    "go.html": {
        "name": "Go",
        "description": "Go compiler & type system, Memory layout & escape analysis, Goroutine scheduler internals (M:N), Channels & concurrency primitives, Sync package, Memory management & GC, HTTP services, Profiling (pprof), and Production patterns."
    },
    "javascript.html": {
        "name": "JavaScript & Node.js",
        "description": "ECMAScript specifications, V8 engine internals, Memory management, Prototypes & inheritance, Scope & Closures, Async/Await & Promises, Microtasks vs Macrotasks, Node.js libuv event loop, and 2000+ drill questions."
    },
    "python.html": {
        "name": "Python",
        "description": "Python 3 data structures & algorithms, CPython internals, Bytecode execution, Memory & GIL, Generators & Iterators, Decorators, Concurrency (asyncio, threading, multiprocessing), and Contest-level drills."
    },
    "react-nextjs.html": {
        "name": "React & Next.js",
        "description": "JSX compilation, Virtual DOM & Reconciliation, Fiber architecture & work loops, Concurrent React, Hooks deep-dive, Server Components (RSC), Streaming SSR, Next.js App Router, Caching strategies, and Hydration."
    },
    "system-design.html": {
        "name": "System Design",
        "description": "Large-scale distributed architectures, Horizontal scalability, Data partitioning & consistent hashing, High availability & failover, Caching tiers (Redis/Memcached), Message queues & streaming (Kafka/RabbitMQ), and 15 complete end-to-end system designs."
    }
}

def extract_metadata(file_path):
    basename = os.path.basename(file_path)
    curated = CURATED_METADATA.get(basename, {})
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        # Read enough for headers and intro
        content = f.read(120000)

    # 1. Title
    title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    raw_title = html.unescape(title_match.group(1)).strip() if title_match else ""
    raw_title = re.sub(r"\s+", " ", raw_title)

    # 2. H1
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
    h1 = html.unescape(re.sub(r"<[^>]+>", "", h1_match.group(1))).strip() if h1_match else ""
    h1 = re.sub(r"\s+", " ", h1)

    # 3. Standfirst / Lead paragraph
    stand_match = re.search(r"<p[^>]*class=[\"'][^\"']*standfirst[^\"']*[\"'][^>]*>(.*?)</p>", content, re.IGNORECASE | re.DOTALL)
    stand = html.unescape(re.sub(r"<[^>]+>", "", stand_match.group(1))).strip() if stand_match else ""
    stand = re.sub(r"\s+", " ", stand)

    # Determine Display Name
    if curated.get("name"):
        name = curated["name"]
    else:
        # Derive from filename, e.g. "rust-lang.html" -> "Rust Lang"
        slug = os.path.splitext(basename)[0]
        name = " ".join(word.capitalize() for word in re.split(r"[-_]", slug))

    # Determine Title & Subtitle
    if raw_title:
        # If title contains separator like " — " or " - "
        if " — " in raw_title:
            parts = raw_title.split(" — ", 1)
            display_title = parts[0].strip()
            display_subtitle = parts[1].strip()
        elif " - " in raw_title:
            parts = raw_title.split(" - ", 1)
            display_title = parts[0].strip()
            display_subtitle = parts[1].strip()
        else:
            display_title = raw_title
            display_subtitle = h1
    else:
        display_title = name
        display_subtitle = h1

    # Determine Description
    if curated.get("description"):
        description = curated["description"]
    elif stand:
        description = stand
    elif display_subtitle:
        description = display_subtitle
    else:
        description = "Interactive engineering handbook and reference guide."

    pages_url = f"{PAGES_BASE_URL}/{HANDBOOKS_DIR}/{basename}"
    source_url = f"{HANDBOOKS_DIR}/{basename}"

    return {
        "filename": basename,
        "name": name,
        "title": display_title,
        "subtitle": display_subtitle,
        "description": description,
        "pages_url": pages_url,
        "source_url": source_url,
    }


def generate_table(handbooks):
    lines = [
        "| Handbook | Title & Description | 🌐 Read Live (GitHub Pages) | 📄 Source |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for h in handbooks:
        title_part = f"**{h['title']}**"
        if h['subtitle'] and h['subtitle'] != h['title']:
            title_part += f"<br>_{h['subtitle']}_"
        desc_part = f"<br>{h['description']}"
        title_and_desc = f"{title_part}{desc_part}"
        live_link = f"[**Open Handbook ↗**]({h['pages_url']})"
        source_link = f"[`{h['source_url']}`]({h['source_url']})"
        lines.append(f"| **{h['name']}** | {title_and_desc} | {live_link} | {source_link} |")
    return "\n".join(lines)


def generate_tree():
    """Generates an ASCII directory tree of the repository."""
    tree_lines = ["handbooks/"]
    
    # 1. .github directory
    tree_lines.append("├── .github/")
    tree_lines.append("│   ├── scripts/")
    script_files = sorted(os.listdir(".github/scripts")) if os.path.exists(".github/scripts") else []
    for sf in script_files:
        tree_lines.append(f"│   │   └── {sf}")
    tree_lines.append("│   └── workflows/")
    wf_files = sorted(os.listdir(".github/workflows")) if os.path.exists(".github/workflows") else []
    for wf in wf_files:
        tree_lines.append(f"│       └── {wf}")

    # 2. Top-level files
    top_level_files = [
        ".gitignore",
        "CODE_OF_CONDUCT.md",
        "LICENSE",
        "README.md",
        "index.html",
    ]
    existing_top = [f for f in top_level_files if os.path.exists(f)]
    for f in existing_top:
        tree_lines.append(f"├── {f}")

    # 3. handbooks directory
    tree_lines.append("└── handbooks/")
    hb_files = sorted(os.listdir(HANDBOOKS_DIR)) if os.path.exists(HANDBOOKS_DIR) else []
    hb_htmls = [f for f in hb_files if f.endswith(".html")]
    for i, hf in enumerate(hb_htmls):
        prefix = "    └── " if i == len(hb_htmls) - 1 else "    ├── "
        tree_lines.append(f"{prefix}{hf}")

    return "```text\n" + "\n".join(tree_lines) + "\n```"


def update_readme(handbooks):
    if not os.path.exists(README_FILE):
        return

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate new table
    table_content = generate_table(handbooks)
    # Generate new tree
    tree_content = generate_tree()

    # Markers for Table
    table_start_marker = "<!-- HANDBOOKS_TABLE_START -->"
    table_end_marker = "<!-- HANDBOOKS_TABLE_END -->"

    if table_start_marker in content and table_end_marker in content:
        pattern = re.compile(
            rf"{re.escape(table_start_marker)}.*?{re.escape(table_end_marker)}",
            re.DOTALL
        )
        content = pattern.sub(f"{table_start_marker}\n{table_content}\n{table_end_marker}", content)
    else:
        # Fallback if markers don't exist yet: replace existing table under ## 📚 Handbooks Catalog
        catalog_header = "## 📚 Handbooks Catalog"
        if catalog_header in content:
            parts = content.split(catalog_header, 1)
            # Find next header or delimiter
            next_section = re.search(r"\n---\n|\n## ", parts[1])
            if next_section:
                rest = parts[1][next_section.start():]
                content = f"{parts[0]}{catalog_header}\n\n{table_start_marker}\n{table_content}\n{table_end_marker}\n{rest}"

    # Markers for Structure Tree
    tree_start_marker = "<!-- REPO_STRUCTURE_START -->"
    tree_end_marker = "<!-- REPO_STRUCTURE_END -->"

    if tree_start_marker in content and tree_end_marker in content:
        pattern = re.compile(
            rf"{re.escape(tree_start_marker)}.*?{re.escape(tree_end_marker)}",
            re.DOTALL
        )
        content = pattern.sub(f"{tree_start_marker}\n{tree_content}\n{tree_end_marker}", content)
    else:
        struct_header = "## 🗂️ Repository Structure"
        if struct_header in content:
            parts = content.split(struct_header, 1)
            next_section = re.search(r"\n---\n|\n## ", parts[1])
            if next_section:
                rest = parts[1][next_section.start():]
                content = f"{parts[0]}{struct_header}\n\n{tree_start_marker}\n{tree_content}\n{tree_end_marker}\n{rest}"

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Updated README.md successfully.")


def generate_index_html(handbooks):
    """Generates an elegant landing page portal for GitHub Pages."""
    cards_html = []
    for h in handbooks:
        cards_html.append(f"""
      <article class="card">
        <div class="card-header">
          <span class="badge">{html.escape(h['name'])}</span>
          <span class="filename">{html.escape(h['filename'])}</span>
        </div>
        <h2 class="card-title">{html.escape(h['title'])}</h2>
        {f'<p class="card-subtitle">{html.escape(h["subtitle"])}</p>' if h["subtitle"] and h["subtitle"] != h["title"] else ''}
        <p class="card-desc">{html.escape(h['description'])}</p>
        <div class="card-footer">
          <a href="{html.escape(h['pages_url'])}" class="read-btn">
            Read Handbook
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </a>
        </div>
      </article>""")

    cards_joined = "\n".join(cards_html)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Engineering Handbooks Portal</title>
  <meta name="description" content="Comprehensive interactive engineering handbooks covering Go, Python, JavaScript, React/Next.js, Flutter, DevOps, SQL, Express/MongoDB, and System Design." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --text-main: #f0f6fc;
      --text-muted: #8b949e;
      --accent: #58a6ff;
      --accent-hover: #79c0ff;
      --card-bg: #161b22;
      --card-border: #30363d;
      --badge-bg: #1f6feb26;
      --badge-text: #58a6ff;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text-main);
      line-height: 1.6;
      padding: 2.5rem 1.5rem 5rem;
      min-height: 100vh;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    header {{
      text-align: center;
      margin-bottom: 3rem;
    }}
    .title {{
      font-size: 2.75rem;
      font-weight: 700;
      letter-spacing: -0.03em;
      margin-bottom: 0.75rem;
      background: linear-gradient(135deg, #58a6ff 0%, #bc8cff 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 1.15rem;
      max-width: 720px;
      margin: 0 auto 1.5rem;
    }}
    .actions {{
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-bottom: 2rem;
    }}
    .gh-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: #21262d;
      color: #c9d1d9;
      border: 1px solid var(--border);
      padding: 0.5rem 1.25rem;
      border-radius: 6px;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 600;
      transition: background 0.2s, border-color 0.2s;
    }}
    .gh-btn:hover {{
      background: #30363d;
      border-color: #8b949e;
      color: #fff;
    }}
    .search-wrapper {{
      max-width: 600px;
      margin: 0 auto 3rem;
      position: relative;
    }}
    .search-input {{
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-main);
      font-size: 1rem;
      padding: 0.75rem 1.25rem;
      border-radius: 8px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1.5rem;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .card:hover {{
      transform: translateY(-3px);
      border-color: #58a6ff66;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }}
    .badge {{
      background: var(--badge-bg);
      color: var(--badge-text);
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.25rem 0.6rem;
      border-radius: 999px;
      border: 1px solid rgba(88, 166, 255, 0.2);
    }}
    .filename {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
    .card-title {{
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 0.4rem;
      color: #fff;
    }}
    .card-subtitle {{
      font-size: 0.9rem;
      font-style: italic;
      color: #8b949e;
      margin-bottom: 0.75rem;
    }}
    .card-desc {{
      font-size: 0.9rem;
      color: #8b949e;
      flex-grow: 1;
      margin-bottom: 1.5rem;
    }}
    .card-footer {{
      margin-top: auto;
    }}
    .read-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--accent);
      color: #0d1117;
      font-size: 0.9rem;
      font-weight: 600;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      text-decoration: none;
      transition: background 0.2s;
    }}
    .read-btn:hover {{
      background: var(--accent-hover);
    }}
    footer {{
      margin-top: 5rem;
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      padding-top: 2rem;
    }}
    footer a {{
      color: var(--accent);
      text-decoration: none;
    }}
    footer a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1 class="title">Engineering Handbooks</h1>
      <p class="subtitle">A curated collection of in-depth, interactive reference guides, architecture walk-throughs, and question banks.</p>
      <div class="actions">
        <a href="https://github.com/{REPO_OWNER}/{REPO_NAME}" class="gh-btn" target="_blank" rel="noopener">
          <svg height="18" viewBox="0 0 16 16" width="18" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
          View on GitHub
        </a>
      </div>
      <div class="search-wrapper">
        <input type="text" id="searchInput" class="search-input" placeholder="Search handbooks by topic, keyword, or language..." />
      </div>
    </header>

    <main class="grid" id="handbooksGrid">
{cards_joined}
    </main>

    <footer>
      <p>Maintained by <a href="https://github.com/{REPO_OWNER}" target="_blank" rel="noopener">{REPO_OWNER}</a> &bull; Licensed under MIT &bull; Hosted on GitHub Pages</p>
    </footer>
  </div>

  <script>
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.card');

    searchInput.addEventListener('input', (e) => {{
      const query = e.target.value.toLowerCase().trim();
      cards.forEach(card => {{
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }});
  </script>
</body>
</html>"""

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ Generated index.html portal successfully.")


def main():
    if not os.path.exists(HANDBOOKS_DIR):
        print(f"Error: {HANDBOOKS_DIR} directory does not exist.")
        return

    html_files = sorted(glob.glob(os.path.join(HANDBOOKS_DIR, "*.html")))
    print(f"Found {len(html_files)} handbook(s) in {HANDBOOKS_DIR}/")

    handbooks = [extract_metadata(hf) for hf in html_files]

    # Generate or update README.md
    update_readme(handbooks)

    # Generate index.html portal
    generate_index_html(handbooks)


if __name__ == "__main__":
    main()
