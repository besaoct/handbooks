#!/usr/bin/env python3
"""
update_readme.py
Scans the docs/ directory, extracts metadata from each handbook HTML file,
and dynamically updates the README.md table and repository structure tree.
Also generates a production-quality, accessible index.html portal consuming
the centralized CSS design system in styles/.
"""

import os
import re
import html
import glob

REPO_OWNER = "besaoct"
REPO_NAME = "handbooks"
PAGES_BASE_URL = f"https://{REPO_OWNER}.github.io/{REPO_NAME}"
HANDBOOKS_DIR = "docs"
README_FILE = "README.md"
INDEX_FILE = "index.html"

# Curated metadata highlights and categories
CURATED_METADATA = {
    "db-sql.html": {
        "name": "SQL & Systems",
        "category": "backend data",
        "badge": "Databases & Scale",
        "description": "1000+ problems with solutions. Covers SELECT, Joins, Aggregation, Subqueries & CTEs, Window functions, DDL/DML, Transactions & Locking, Indexing & Query Plans, Database internals, Replication, Sharding, Caching, and Datastore tradeoffs."
    },
    "devops-and-git.html": {
        "name": "DevOps & Git",
        "category": "systems devops",
        "badge": "Infra & Pipelines",
        "description": "Git object database internals, Linux systems & networking, Containers & Docker, Kubernetes orchestration, CI/CD pipelines, Infrastructure as Code, Observability, Incident response, and Production safety."
    },
    "express-mongo.html": {
        "name": "Express & MongoDB",
        "category": "backend web",
        "badge": "Backend Runtime",
        "description": "Node.js runtime, Event loop, HTTP/TCP sockets, Express middleware pipeline, Routing, Authentication & JWT, Security hardening, MongoDB schema design, Aggregation pipeline, Mongoose internals, and API performance."
    },
    "flutter.html": {
        "name": "Flutter & Dart",
        "category": "frontend mobile",
        "badge": "Cross-Platform UI",
        "description": "Dart type system & runtime, Widget tree architecture, Element & RenderObject lifecycle, Layout constraints & hit testing, State management paradigms, Animations, Platform channels, and Performance profiling."
    },
    "go.html": {
        "name": "Go",
        "category": "backend systems languages",
        "badge": "Systems & Concurrency",
        "description": "Go compiler & type system, Memory layout & escape analysis, Goroutine scheduler internals (M:N), Channels & concurrency primitives, Sync package, Memory management & GC, HTTP services, Profiling (pprof), and Production patterns."
    },
    "javascript.html": {
        "name": "JavaScript & Node.js",
        "category": "languages frontend backend",
        "badge": "Language Internals",
        "description": "ECMAScript specifications, V8 engine internals, Memory management, Prototypes & inheritance, Scope & Closures, Async/Await & Promises, Microtasks vs Macrotasks, Node.js libuv event loop, and 2000+ drill questions."
    },
    "python.html": {
        "name": "Python",
        "category": "languages algorithms",
        "badge": "Core & Algorithms",
        "description": "Python 3 data structures & algorithms, CPython internals, Bytecode execution, Memory & GIL, Generators & Iterators, Decorators, Concurrency (asyncio, threading, multiprocessing), and Contest-level drills."
    },
    "react-nextjs.html": {
        "name": "React & Next.js",
        "category": "frontend web",
        "badge": "Frontend Architecture",
        "description": "JSX compilation, Virtual DOM & Reconciliation, Fiber architecture & work loops, Concurrent React, Hooks deep-dive, Server Components (RSC), Streaming SSR, Next.js App Router, Caching strategies, and Hydration."
    },
    "system-design.html": {
        "name": "System Design",
        "category": "systems backend",
        "badge": "Distributed Architecture",
        "description": "Large-scale distributed architectures, Horizontal scalability, Data partitioning & consistent hashing, High availability & failover, Caching tiers (Redis/Memcached), Message queues & streaming (Kafka/RabbitMQ), and 15 complete end-to-end system designs."
    }
}

def extract_metadata(file_path):
    basename = os.path.basename(file_path)
    curated = CURATED_METADATA.get(basename, {})
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
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

    # Determine Display Name & Badge
    slug = os.path.splitext(basename)[0]
    default_name = " ".join(word.capitalize() for word in re.split(r"[-_]", slug))
    name = curated.get("name", default_name)
    badge = curated.get("badge", "Handbook")
    category = curated.get("category", "general")

    # Determine Title & Subtitle (Avoid em dashes in UI copy)
    if raw_title:
        clean_title = raw_title.replace("—", ":").replace("–", ":")
        if ":" in clean_title:
            parts = clean_title.split(":", 1)
            display_title = parts[0].strip()
            display_subtitle = parts[1].strip()
        else:
            display_title = clean_title
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
        "badge": badge,
        "category": category,
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

    # 2. docs directory
    tree_lines.append("├── docs/")
    doc_files = sorted(os.listdir(HANDBOOKS_DIR)) if os.path.exists(HANDBOOKS_DIR) else []
    doc_htmls = [f for f in doc_files if f.endswith(".html")]
    for dh in doc_htmls:
        tree_lines.append(f"│   ├── {dh}")

    # 3. styles directory
    tree_lines.append("├── styles/")
    tree_lines.append("│   ├── components/")
    if os.path.exists("styles/components"):
        for cf in sorted(os.listdir("styles/components")):
            tree_lines.append(f"│   │   ├── {cf}")
    style_root = ["global.css", "main.css", "theme.css", "tokens.css", "typography.css"]
    for sf in style_root:
        if os.path.exists(f"styles/{sf}"):
            tree_lines.append(f"│   ├── {sf}")

    # 4. Top-level files
    top_level_files = [
        ".gitignore",
        "CODE_OF_CONDUCT.md",
        "LICENSE",
        "README.md",
        "index.html",
    ]
    existing_top = [f for f in top_level_files if os.path.exists(f)]
    for i, f in enumerate(existing_top):
        prefix = "└── " if i == len(existing_top) - 1 else "├── "
        tree_lines.append(f"{prefix}{f}")

    return "```text\n" + "\n".join(tree_lines) + "\n```"


def update_readme(handbooks):
    if not os.path.exists(README_FILE):
        return

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    table_content = generate_table(handbooks)
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
        catalog_header = "## 📚 Handbooks Catalog"
        if catalog_header in content:
            parts = content.split(catalog_header, 1)
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
    """Generates a production-quality, accessible landing page consuming styles/main.css."""
    total_count = len(handbooks)
    cards_html = []
    
    for h in handbooks:
        search_data = f"{h['name']} {h['title']} {h['subtitle']} {h['description']} {h['filename']}".lower()
        subtitle_block = f'<p class="card-subtitle">{html.escape(h["subtitle"])}</p>' if h["subtitle"] and h["subtitle"] != h["title"] else ""
        
        cards_html.append(f"""        <article class="handbook-card" data-category="{html.escape(h['category'])}" data-search="{html.escape(search_data)}">
          <div class="card-top">
            <span class="card-badge">{html.escape(h['badge'])}</span>
          </div>
          <h2 class="card-title">{html.escape(h['title'])}</h2>
          {subtitle_block}
          <p class="card-description">{html.escape(h['description'])}</p>
          <div class="card-footer">
            <a href="{html.escape(h['pages_url'])}" class="btn btn-primary btn-sm">
              Read Handbook
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
            <a href="https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/{HANDBOOKS_DIR}/{html.escape(h['filename'])}" class="card-source-link" target="_blank" rel="noopener">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
              Source
            </a>
          </div>
        </article>""")

    cards_joined = "\n".join(cards_html)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Engineering Handbooks: Production Reference &amp; Question Banks</title>
  <meta name="description" content="In-depth, interactive engineering handbooks covering Go, Python, JavaScript, React/Next.js, Flutter, DevOps, SQL, Express/MongoDB, and System Design." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="styles/main.css?v=8" />
</head>
<body>
  <!-- Global Navigation Header -->
  <header class="site-header">
    <div class="container site-header-inner">
      <a href="https://besaoct.github.io/handbooks/" class="brand" aria-label="Engineering Handbooks Home">
        <div class="brand-icon" aria-hidden="true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        </div>
        <span class="brand-title">Engineering Handbooks</span>
        <span class="brand-tag">{total_count} Volumes</span>
      </a>

      <div class="header-actions">
        <button id="themeToggle" class="theme-toggle-btn" aria-label="Toggle visual theme" title="Toggle theme">
          <svg id="themeIconSun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
          <svg id="themeIconMoon" class="hidden" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>

        <a href="https://github.com/{REPO_OWNER}/{REPO_NAME}" class="btn btn-secondary btn-sm" target="_blank" rel="noopener">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
          GitHub
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero-section">
    <div class="container">
      <h1 class="hero-title">Engineering Handbooks</h1>
      <p class="hero-description">A curated collection of deep, standalone technical manuals, architecture walkthroughs, and problem banks spanning systems, backend, frontend, and DevOps.</p>
    </div>
  </section>

  <!-- Toolbar & Filters -->
  <section class="toolbar-section">
    <div class="container search-container">
      <div class="search-input-wrapper">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" id="searchInput" class="search-input" placeholder="Search handbooks by title, topic, or keyword..." aria-label="Search handbooks" autocomplete="off" spellcheck="false" />
        <span class="search-kbd-hint" aria-hidden="true">/</span>
      </div>

      <nav class="category-filters" aria-label="Filter handbooks by category">
        <button class="filter-btn active" data-filter="all">All <span class="filter-count">({total_count})</span></button>
        <button class="filter-btn" data-filter="systems">Systems &amp; Infra</button>
        <button class="filter-btn" data-filter="backend">Backend &amp; Databases</button>
        <button class="filter-btn" data-filter="frontend">Frontend &amp; UI</button>
        <button class="filter-btn" data-filter="languages">Languages &amp; Core</button>
      </nav>

      <div class="toolbar-status">
        <span id="statusCounter" class="status-counter">Showing {total_count} of {total_count} handbooks</span>
        <button id="clearSearchBtn" class="clear-search-btn hidden">Clear search</button>
      </div>
    </div>
  </section>

  <!-- Cards Grid -->
  <main class="container">
    <section class="handbooks-grid" id="handbooksGrid" aria-label="Handbooks catalog">
{cards_joined}

      <div id="emptyState" class="empty-state hidden">
        <h3 class="empty-state-title">No handbooks match your filter</h3>
        <p class="empty-state-desc">Try searching for a different technology, keyword, or clear your current filter.</p>
        <button id="resetFiltersBtn" class="btn btn-secondary btn-sm">Reset All Filters</button>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-credits">
        Curated by <a href="https://github.com/{REPO_OWNER}" target="_blank" rel="noopener">{REPO_OWNER}</a> &bull; Handbooks are standalone offline-ready HTML documents.
      </div>
      <ul class="footer-links">
        <li><a href="https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/LICENSE">License (MIT)</a></li>
        <li><a href="https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/CODE_OF_CONDUCT.md">Code of Conduct</a></li>
        <li><a href="https://github.com/{REPO_OWNER}/{REPO_NAME}">GitHub Repository</a></li>
      </ul>
    </div>
  </footer>

  <!-- Application Logic -->
  <script>
    (function() {{
      const searchInput = document.getElementById('searchInput');
      const clearSearchBtn = document.getElementById('clearSearchBtn');
      const resetFiltersBtn = document.getElementById('resetFiltersBtn');
      const statusCounter = document.getElementById('statusCounter');
      const emptyState = document.getElementById('emptyState');
      const filterButtons = document.querySelectorAll('.filter-btn');
      const cards = Array.from(document.querySelectorAll('.handbook-card'));
      const totalCount = cards.length;

      let currentCategory = 'all';
      let currentQuery = '';

      function filterCards() {{
        let visibleCount = 0;

        cards.forEach(card => {{
          const cardCategories = (card.getAttribute('data-category') || '').split(' ');
          const cardSearchText = card.getAttribute('data-search') || '';

          const matchesCategory = (currentCategory === 'all') || cardCategories.includes(currentCategory);
          const matchesQuery = !currentQuery || cardSearchText.includes(currentQuery);
          const isVisible = matchesCategory && matchesQuery;

          card.classList.toggle('hidden', !isVisible);
          if (isVisible) visibleCount++;
        }});

        // Status update
        statusCounter.textContent = `Showing ${{visibleCount}} of ${{totalCount}} handbooks`;
        emptyState.classList.toggle('hidden', visibleCount > 0);
        clearSearchBtn.classList.toggle('hidden', !currentQuery);
      }}

      // Search input handler
      searchInput.addEventListener('input', (e) => {{
        currentQuery = e.target.value.toLowerCase().trim();
        filterCards();
      }});

      clearSearchBtn.addEventListener('click', () => {{
        searchInput.value = '';
        currentQuery = '';
        filterCards();
        searchInput.focus();
      }});

      resetFiltersBtn.addEventListener('click', () => {{
        searchInput.value = '';
        currentQuery = '';
        currentCategory = 'all';
        filterButtons.forEach(btn => btn.classList.toggle('active', btn.getAttribute('data-filter') === 'all'));
        filterCards();
        searchInput.focus();
      }});

      // Category filter buttons
      filterButtons.forEach(btn => {{
        btn.addEventListener('click', () => {{
          filterButtons.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentCategory = btn.getAttribute('data-filter');
          filterCards();
        }});
      }});

      // Keyboard shortcut: '/' to focus search input
      window.addEventListener('keydown', (e) => {{
        if (e.key === '/' && document.activeElement !== searchInput && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {{
          e.preventDefault();
          searchInput.focus();
        }}
      }});

      // Theme toggle functionality
      const themeToggle = document.getElementById('themeToggle');
      const sunIcon = document.getElementById('themeIconSun');
      const moonIcon = document.getElementById('themeIconMoon');

      function updateThemeIcons(isDark) {{
        sunIcon.classList.toggle('hidden', !isDark);
        moonIcon.classList.toggle('hidden', isDark);
      }}

      function getInitialTheme() {{
        const saved = localStorage.getItem('theme');
        if (saved) return saved;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }}

      function setTheme(theme) {{
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateThemeIcons(theme === 'dark');
      }}

      const initialTheme = getInitialTheme();
      setTheme(initialTheme);

      themeToggle.addEventListener('click', () => {{
        const current = document.documentElement.getAttribute('data-theme') || 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        setTheme(next);
      }});
    }})();
  </script>
</body>
</html>"""

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ Generated production index.html portal successfully.")


def bundle_styles():
    """Bundles modular CSS files into styles/main.css to avoid @import latency and cache issues."""
    order = [
        "styles/tokens.css",
        "styles/theme.css",
        "styles/typography.css",
        "styles/global.css",
        "styles/components/header.css",
        "styles/components/search.css",
        "styles/components/cards.css",
        "styles/components/buttons.css",
        "styles/components/footer.css"
    ]
    parts = []
    for path in order:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                parts.append(f"/* === {path} === */\n" + f.read())
    with open("styles/main.css", "w", encoding="utf-8") as out:
        out.write("\n\n".join(parts))
    print("✓ Bundled styles into styles/main.css successfully.")


def main():
    if not os.path.exists(HANDBOOKS_DIR):
        print(f"Error: {HANDBOOKS_DIR} directory does not exist.")
        return

    # Bundle modular CSS into main.css
    bundle_styles()

    html_files = sorted(glob.glob(os.path.join(HANDBOOKS_DIR, "*.html")))
    print(f"Found {len(html_files)} handbook(s) in {HANDBOOKS_DIR}/")

    handbooks = [extract_metadata(hf) for hf in html_files]

    # Generate or update README.md
    update_readme(handbooks)

    # Generate index.html portal
    generate_index_html(handbooks)


if __name__ == "__main__":
    main()
