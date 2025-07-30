# Synapso

[![PyPI version](https://img.shields.io/pypi/v/synapso.svg)](https://pypi.org/project/synapso/)
[![Development Status](https://img.shields.io/badge/status-active-yellowgreen.svg)](#)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](#)
[![License: Proprietary](https://img.shields.io/badge/license-proprietary-red.svg)](#license)
[![Project Stage: Pre-MVP](https://img.shields.io/badge/stage-pre--MVP-orange)](#)
[![Last Commit](https://img.shields.io/github/last-commit/ganesh-palanikumar/synapso)](https://github.com/ganesh-palanikumar/synapso/commits/main)

**Synapso** is a local-first, privacy-focused semantic search engine for your personal knowledge base. It’s built to work seamlessly with `.txt` and `.md` files, making it ideal for Obsidian, Logseq, and other markdown-based note-taking workflows.

Synapso enables semantic search over local documents without sending data to the cloud. Your ideas stay on your machine — but your ability to find and connect them gets smarter.

---

## 🚀 Why Synapso?

- **Local-First:** Your data never leaves your machine by default.
- **Markdown-Native:** Works with plain `.md` and `.txt` files.
- **CLI-Focused:** Designed for developers and power users who prefer terminal workflows.
- **Modular:** Future-ready architecture to support Bring Your Own Model (BYOM), file watchers, and custom storage backends.
- **Open-Core:** Core is open source. Future monetization will be built around multi-device and premium features.

---

## 🧠 Project Vision

Synapso aims to become a trusted, local alternative to cloud-based knowledge systems. The goal is to build an extensible foundation for semantic search that integrates with your existing tools, works offline, and respects your privacy.

---

## 🔧 Installation

```bash
pip install synapso
```

> Requires Python 3.9+

---

## 🛠️ Usage (Coming Soon)

The CLI will follow this general structure:

```bash
synapso cortex add /path/to/notes
synapso cortex index
synapso cortex list
synapso query "What did I write about knowledge graphs?"
```

---

## 🗺️ Roadmap

| Version | Feature                                       | Status        |
|---------|-----------------------------------------------|----------------|
| v0.1.0  | Namespace claimed, CLI scaffold               | ✅ Released     |
| v0.1.1  | Bug fixes, CLI polishing                      | 🚧 In progress |
| v0.2.0  | File watcher                                  | Planned        |
| v0.3.0  | Data stores and corresponding models          | Planned        |
| v0.4.0  | Chunking, vectorization for `.txt`            | Planned        |
| v0.5.0  | Markdown file support                         | Planned        |
| v0.6.0  | CLI search/query interface                    | Planned        |

---

## 📦 PyPI

Available on PyPI: [https://pypi.org/project/synapso/](https://pypi.org/project/synapso/)

Install using:

```bash
pip install synapso
```

---

## 🪪 License

## 🪪 License

This project is currently **closed source and proprietary**.

> ⚠️ Synapso is not open for public use or contribution at this time. All code is protected by a custom license that prohibits copying, modification, distribution, or reuse without explicit permission.

If the project becomes open-source post-MVP, a proper license (such as MIT or MPL-2.0) will be chosen and applied.

See the [`LICENSE`](./LICENSE) file for full terms.

---

## 📓 Devlog & Documentation

Full devlog and vision notes are maintained in Obsidian.  
For now, see: [Notion roadmap site (coming soon)](#)

---

## 💬 Feedback & Contributions

Feedback is welcome! Contributions will open post-MVP (~v0.6.0). Until then, feel free to watch the repo and follow along.

---