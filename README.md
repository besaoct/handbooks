# Engineering Handbooks

A comprehensive collection of in-depth, interactive engineering handbooks, reference manuals, and question banks covering modern software engineering across backend, frontend, systems, databases, and operations.

Each handbook is an independent, rich HTML guide packed with detailed diagrams, real-world patterns, deep architectural explanations, and interview-grade problem banks.

---

## 📚 Handbooks Catalog

| Handbook | Title & Subtitle | Key Topics Covered | File |
| :--- | :--- | :--- | :--- |
| **SQL & Systems** | **The SQL & Systems Question Book**<br>_1000+ problems with solutions_ | SELECT, Joins, Aggregation, Subqueries & CTEs, Window functions, DDL/DML, Transactions & Locking, Indexing & Query Plans, Database internals, Replication, Sharding, Caching, and Datastore tradeoffs. | [`db-sql.html`](db-sql.html) |
| **DevOps & Git** | **Commit to Deploy**<br>_Everything between a commit and a running system_ | Git object database internals, Linux systems & networking, Containers & Docker, Kubernetes orchestration, CI/CD pipelines, Infrastructure as Code, Observability, Incident response, and Production safety. | [`devops-and-git.html`](devops-and-git.html) |
| **Express & MongoDB** | **Request Pipeline Handbook**<br>_Everything between the socket and the document_ | Node.js runtime, Event loop, HTTP/TCP sockets, Express middleware pipeline, Routing, Authentication & JWT, Security hardening, MongoDB schema design, Aggregation pipeline, Mongoose internals, and API performance. | [`express-mongo.html`](express-mongo.html) |
| **Flutter & Dart** | **Widget Tree Handbook**<br>_Dart & Flutter, from the render tree up_ | Dart type system & runtime, Widget tree architecture, Element & RenderObject lifecycle, Layout constraints & hit testing, State management paradigms, Animations, Platform channels, and Performance profiling. | [`flutter.html`](flutter.html) |
| **Go** | **Compile, Schedule, Serve**<br>_Go, from the syntax to the scheduler to production_ | Go compiler & type system, Memory layout & escape analysis, Goroutine scheduler internals (`M:N`), Channels & concurrency primitives, Sync package, Memory management & GC, HTTP services, Profiling (`pprof`), and Production patterns. | [`go.html`](go.html) |
| **JavaScript & Node.js** | **The JavaScript & Node.js Handbook**<br>_2000+ problems with solutions_ | ECMAScript specifications, V8 engine internals, Memory management, Prototypes & inheritance, Scope & Closures, Async/Await & Promises, Microtasks vs Macrotasks, Node.js libuv event loop, and 2000+ drill questions. | [`javascript.html`](javascript.html) |
| **Python** | **The Python Handbook**<br>_Fundamentals, interviews, contests_ | Python 3 data structures & algorithms, CPython internals, Bytecode execution, Memory & GIL, Generators & Iterators, Decorators, Concurrency (`asyncio`, threading, multiprocessing), and Contest-level drills. | [`python.html`](python.html) |
| **React & Next.js** | **Render and Commit**<br>_React, from the JavaScript up_ | JSX compilation, Virtual DOM & Reconciliation, Fiber architecture & work loops, Concurrent React, Hooks deep-dive, Server Components (RSC), Streaming SSR, Next.js App Router, Caching strategies, and Hydration. | [`react-nextjs.html`](react-nextjs.html) |
| **System Design** | **Ten Systems Handbook**<br>_Fifteen systems, from whiteboard to production_ | Large-scale distributed architectures, Horizontal scalability, Data partitioning & consistent hashing, High availability & failover, Caching tiers (Redis/Memcached), Message queues & streaming (Kafka/RabbitMQ), and 15 complete end-to-end system designs. | [`system-design.html`](system-design.html) |

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

```text
handbooks/
├── .gitignore
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
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
