# Process Improvement using Data

Source repository for the open-access book *Process Improvement using Data* by
Kevin Dunn. Actively written and updated since August 2010.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Read online](https://img.shields.io/badge/read-learnche.org%2Fpid-blue.svg)](https://learnche.org/pid)
[![Download PDF](https://img.shields.io/badge/download-PDF-red.svg)](https://learnche.org/pid/PID.pdf)
[![Issues](https://img.shields.io/github/issues/kgdunn/pid-book.svg)](https://github.com/kgdunn/pid-book/issues)

> **Just want to read it?** Go to **<https://learnche.org/pid>** (HTML) or
> grab the **[PDF](https://learnche.org/pid/PID.pdf)**. This repository is for
> readers who want to compile, modify, or contribute to the book.

## What the book covers

The book teaches statistical methods for engineers and scientists who work
with process data — how to visualize it, model it, monitor it, and use it to
improve products and processes. It is suitable for upper-undergraduate or
introductory-graduate courses, and for self-study by practitioners.

| Chapter | Topic |
|---|---|
| 1 | Data visualization |
| 2 | Univariate review (probability, distributions, confidence intervals, hypothesis tests) |
| 3 | Process monitoring (Shewhart, CUSUM, EWMA charts) |
| 4 | Least-squares modelling (linear and multiple regression) |
| 5 | Design and analysis of experiments (DOE) |
| 6 | Latent variable modelling (PCA, PLS, batch data analysis) |
| 7 | Product development and product improvement |

The full table of contents lives in [`contents.rst`](contents.rst).

## Compiling the book yourself

### Prerequisites

* **Python ≥ 3.12**
* **[uv](https://docs.astral.sh/uv/)** — installed automatically by `make setup`
* **Node.js / `npx`** — used to run [Pagefind](https://pagefind.app/) for the
  HTML search index
* **A LaTeX distribution** (TeX Live, MacTeX, MiKTeX) — only required for the
  PDF build
* **The figures repository** — clone <https://github.com/kgdunn/figures> and
  symlink it into this repo (see below)
* About **2 GB** of disk space for the build tree, intermediate files, and
  illustrations

Python dependencies (Sphinx ≥ 8.1.3, sphinx-book-theme, sphinxcontrib-jquery)
are pinned in [`pyproject.toml`](pyproject.toml) and resolved by uv.

### One-time setup

```sh
# 1. Clone this repo
git clone https://github.com/kgdunn/pid-book.git
cd pid-book

# 2. Clone the figures repo somewhere outside this one and symlink it in
git clone https://github.com/kgdunn/figures.git ../figures
ln -s "$(cd ../figures && pwd)" figures

# 3. Bootstrap the toolchain (installs uv, creates .venv, syncs deps)
make setup
```

### Build targets

| Command | What it does |
|---|---|
| `make setup` | Bootstrap the toolchain: install `uv`, create `.venv`, sync deps |
| `make html` | Build the HTML book into `_build/html/` and run Pagefind for search |
| `make serve` | Serve `_build/html/` at <http://localhost:8080> for local preview |
| `make latexpdf` | Build the PDF (5–10 minutes; needs LaTeX). Output: `_build/latex/PID.pdf` |
| `make linkcheck` | Verify external links |
| `make clean` | Remove build artifacts (`_build/`, caches) |
| `make distclean` | Also remove `.venv/` and `uv.lock` (forces a re-resolve on next `make setup`) |
| `make` | Default target is `latexpdf` |

Compare your PDF against <https://learnche.org/pid/PID.pdf> to confirm a
clean build.

## Repository layout

```
pid-book/
├── preface/                                  Front matter
├── data-visualization/                       Ch 1
├── univariate-review/                        Ch 2
├── process-monitoring/                       Ch 3
├── least-squares-modelling/                  Ch 4
├── design-analysis-experiments/              Ch 5
├── latent-variable-modelling/                Ch 6
├── product-development-product-improvement/  Ch 7
├── my-extensions/                            Custom Sphinx extensions
│                                             (youtube)
├── _static/                                  Custom CSS and favicon (sphinx-book-theme)
├── _templates/                               Custom Jinja2 templates (Pagefind search)
├── figures/                                  Symlink to the figures repo
├── conf.py, contents.rst                     Sphinx config + master ToC
├── Makefile                                  Build entry points
└── pyproject.toml, uv.lock                   Python dependencies
```

## Contributing

Contributions, corrections, and exercises are welcome. The fastest channels:

1. **Open an [issue](https://github.com/kgdunn/pid-book/issues)** for typos,
   technical errors, broken links, or build problems.
2. **Open a pull request** for content changes — see
   [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and RST style notes.
3. **Long-form feedback**, course adoption stories, and exercise contributions
   can also go through [this Google Form](https://docs.google.com/forms/d/1IpO-bvJwQwhK64eid4YXwJBvGxN5cfyYDv81G-YgWrM/viewform).

## License and citation

The book is licensed under the
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
license. You are free to copy, adapt, and redistribute it — including for
courses you teach — provided you attribute the original author and license
your derivative work under the same terms.

Suggested attribution:

> Dunn, K. G. (2010–2026). *Process Improvement using Data.* learnche.org/pid (CC BY-SA 4.0).

Machine-readable citation metadata is available in
[`CITATION.cff`](CITATION.cff).

## Maintainer notes

<details>
<summary>Deployment and release</summary>

* `copy-html.sh` rsyncs `_build/html/` and the PDF to the learnche.org server.
  Maintainer-only; assumes SSH access.
* `start_server.py` serves `_build/html/` locally on port 8080 with the MIME
  types Pagefind expects. It is invoked by `make serve`.
* The release version is tracked in [`pyproject.toml`](pyproject.toml).
* `to-add.txt` is a working backlog. Migrating items to GitHub Issues is
  encouraged.

</details>
