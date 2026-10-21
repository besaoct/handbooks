# Engineering Handbooks

A comprehensive collection of in-depth, interactive engineering handbooks, reference manuals, and question banks covering modern software engineering across backend, frontend, systems, databases, and operations.

Each handbook is an independent, rich HTML guide packed with detailed diagrams, real-world patterns, deep architectural explanations, and interview-grade problem banks.

---

## 📚 Handbooks Catalog

<!-- HANDBOOKS_TABLE_START -->
| Handbook | Title & Description | 🌐 Read Live (GitHub Pages) | 📄 Source |
| :--- | :--- | :--- | :--- |
| **SQL & Systems** | **The SQL & Systems Question Book**<br>_1000+ problems with solutions_<br>1000+ problems with solutions. Covers SELECT, Joins, Aggregation, Subqueries & CTEs, Window functions, DDL/DML, Transactions & Locking, Indexing & Query Plans, Database internals, Replication, Sharding, Caching, and Datastore tradeoffs. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/db-sql.html) | [`handbooks/db-sql.html`](handbooks/db-sql.html) |
| **DevOps & Git** | **Commit to Deploy**<br>_Everything between a commit and a running system_<br>Git object database internals, Linux systems & networking, Containers & Docker, Kubernetes orchestration, CI/CD pipelines, Infrastructure as Code, Observability, Incident response, and Production safety. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/devops-and-git.html) | [`handbooks/devops-and-git.html`](handbooks/devops-and-git.html) |
| **Express & MongoDB** | **Request Pipeline Handbook**<br>_Everything between the socket and the document_<br>Node.js runtime, Event loop, HTTP/TCP sockets, Express middleware pipeline, Routing, Authentication & JWT, Security hardening, MongoDB schema design, Aggregation pipeline, Mongoose internals, and API performance. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/express-mongo.html) | [`handbooks/express-mongo.html`](handbooks/express-mongo.html) |
| **Flutter & Dart** | **Widget Tree Handbook**<br>_Dart & Flutter, from the render tree up_<br>Dart type system & runtime, Widget tree architecture, Element & RenderObject lifecycle, Layout constraints & hit testing, State management paradigms, Animations, Platform channels, and Performance profiling. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/flutter.html) | [`handbooks/flutter.html`](handbooks/flutter.html) |
| **Go** | **Compile, Schedule, Serve**<br>_Go, from the syntax to the scheduler to production_<br>Go compiler & type system, Memory layout & escape analysis, Goroutine scheduler internals (M:N), Channels & concurrency primitives, Sync package, Memory management & GC, HTTP services, Profiling (pprof), and Production patterns. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/go.html) | [`handbooks/go.html`](handbooks/go.html) |
| **JavaScript & Node.js** | **The JavaScript & Node.js Handbook**<br>_2000+ problems with solutions_<br>ECMAScript specifications, V8 engine internals, Memory management, Prototypes & inheritance, Scope & Closures, Async/Await & Promises, Microtasks vs Macrotasks, Node.js libuv event loop, and 2000+ drill questions. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/javascript.html) | [`handbooks/javascript.html`](handbooks/javascript.html) |
| **Python** | **The Python Handbook**<br>_fundamentals, interviews, contests_<br>Python 3 data structures & algorithms, CPython internals, Bytecode execution, Memory & GIL, Generators & Iterators, Decorators, Concurrency (asyncio, threading, multiprocessing), and Contest-level drills. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/python.html) | [`handbooks/python.html`](handbooks/python.html) |
| **React & Next.js** | **Render and Commit**<br>_React, from the JavaScript up_<br>JSX compilation, Virtual DOM & Reconciliation, Fiber architecture & work loops, Concurrent React, Hooks deep-dive, Server Components (RSC), Streaming SSR, Next.js App Router, Caching strategies, and Hydration. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/react-nextjs.html) | [`handbooks/react-nextjs.html`](handbooks/react-nextjs.html) |
| **System Design** | **Ten Systems Handbook**<br>_Fifteen systems, from whiteboard to production_<br>Large-scale distributed architectures, Horizontal scalability, Data partitioning & consistent hashing, High availability & failover, Caching tiers (Redis/Memcached), Message queues & streaming (Kafka/RabbitMQ), and 15 complete end-to-end system designs. | [**Open Handbook ↗**](https://besaoct.github.io/handbooks/handbooks/system-design.html) | [`handbooks/system-design.html`](handbooks/system-design.html) |
<!-- HANDBOOKS_TABLE_END -->

---

## 🚀 How to Read & Use

The handbooks are self-contained HTML files with embedded styling, scripts, and interactive components. No build steps or package managers required.

### 1. Direct Browser Access
Simply open any handbook file in your favorite browser:
- Double-click the `.html` file in your file manager, or
- Run via terminal:
  ```bash
  # macOS
  open system-design.html

  # Linux
  xdg-open system-design.html

  # Windows
  start system-design.html
  ```

### 2. Local HTTP Server
If you prefer running a local development server for all handbooks:

```bash
# Using Python 3
python3 -m http.server 8080

# Using Node.js
npx serve .
```
Then navigate to `http://localhost:8080` in your browser.

---

## 🗂️ Repository Structure

<!-- REPO_STRUCTURE_START -->
```text
handbooks/
├── .github/
│   ├── scripts/
│   │   └── update_readme.py
│   └── workflows/
│       └── deploy.yml
├── .gitignore
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
├── index.html
└── handbooks/
    ├── db-sql.html
    ├── devops-and-git.html
    ├── express-mongo.html
    ├── flutter.html
    ├── go.html
    ├── javascript.html
    ├── python.html
    ├── react-nextjs.html
    └── system-design.html
```
<!-- REPO_STRUCTURE_END -->

---

## 🤝 Contributing

Contributions, fixes, and improvements are welcome!
- If you find a typo, outdated example, or bug, feel free to open an Issue or submit a Pull Request.
- Please make sure your contributions adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📜 Code of Conduct

This project is governed by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).

**Author:** [besaoct](https://github.com/besaoct)
