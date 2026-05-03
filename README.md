# Process Improvement using Data

Source repository for the open-access book *Process Improvement using Data* by
Kevin Dunn. Actively written and updated since August 2010.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Read online](https://img.shields.io/badge/read-learnche.org%2Fpid-blue.svg)](https://learnche.org/pid)
[![Download PDF](https://img.shields.io/badge/download-PDF-red.svg)](https://learnche.org/pid/PID.pdf?2026-05-03)
[![Build status](https://img.shields.io/github/actions/workflow/status/kgdunn/pid-book/build-deploy.yml?branch=master&label=build)](https://github.com/kgdunn/pid-book/actions/workflows/build-deploy.yml)
[![Last commit](https://img.shields.io/github/last-commit/kgdunn/pid-book.svg)](https://github.com/kgdunn/pid-book/commits)
[![Issues](https://img.shields.io/github/issues/kgdunn/pid-book.svg)](https://github.com/kgdunn/pid-book/issues)

> **Just want to read it?** Go to **<https://learnche.org/pid>** (HTML) or
> grab the **[PDF](https://learnche.org/pid/PID.pdf?2026-05-03)**. This repository is for
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

## For instructors

You're welcome to use this book — and the course materials below — for your
own teaching. Everything is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), so you can
share, adapt, and even commercialize derivative work as long as you attribute
the original and license the result under the same terms. No permission
needed.

The book has been adopted at other universities (undergraduate and graduate)
and used inside companies as an internal training manual.

Course materials live on the original
[Learning Chemical Engineering: Courses](https://learnche.org/4C3/Main_Page)
site:

- [Suggested course structure](https://learnche.org/4C3/Course_outlines)
- [PDF slides](https://learnche.org/4C3/Main_Page) covering every section of
  the book
- [Assignments (with solutions)](https://learnche.org/4C3/Assignments_from_prior_years)
- [Midterms / tests](https://learnche.org/4C3/Midterms_from_prior_years)
- [Final exams](https://learnche.org/4C3/Final_exams_from_prior_years)
- Projects for
  [response surface optimization](https://learnche.org/4C3/Response_surface_project_from_prior_years)
  and
  [design of experiments](https://learnche.org/4C3/Designed_experiments_projects_from_prior_years)
- A [tutorial to learn R](https://learnche.org/4C3/Software_tutorial)
- [Video recordings](https://learnche.org/4C3/Course_videos_and_audio_from_previous_years)
  of the course on YouTube
- [Sample datasets](https://openmv.net/) for assignments, tests, and practice

**Teaching at a company?** Get in touch via the
[contact page](https://learnche.org/4C3/Statistics_for_Engineering:About) for
additional slides, worksheets, and tips.

Questions, comments, or "how did you make that figure?" enquiries are all
welcome through the same contact link.

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
| `make latexpdf` | Build the PDF (5–10 minutes; needs LaTeX). Output: `_build/latex/PID.pdf?2026-05-03` |
| `make linkcheck` | Verify external links |
| `make clean` | Remove build artifacts (`_build/`, caches) |
| `make distclean` | Also remove `.venv/` and `uv.lock` (forces a re-resolve on next `make setup`) |
| `make` | Default target is `latexpdf` |

Compare your PDF against <https://learnche.org/pid/PID.pdf?2026-05-03> to confirm a
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

## How this book is published

The book has a fairly typical static-site pipeline, with a couple of design
quirks worth knowing about.

```
RST sources ─┐
             ├─►  Sphinx  ─►  HTML (extensionless URLs) ─┐
figures/  ───┘                LaTeX ──pdflatex──► PDF    ├─► rsync ─► learnche.org/pid
                              text  (fed to Pagefind)    │
                                                         │
                       GitHub Actions (.github/workflows/build-deploy.yml)
```

1. **Sources.** Every chapter is reStructuredText in its own directory;
   [`contents.rst`](contents.rst) is the master table of contents. The custom
   Sphinx extension under `my-extensions/` adds the `.. youtube::` directive
   used in a handful of chapters.
2. **Figures (separate repo).** Images live in
   [`kgdunn/figures`](https://github.com/kgdunn/figures) and are pulled in
   through the `figures/` symlink. CI checks that repo out alongside this one
   and recreates the symlink before building. A content change that touches
   figures needs a parallel PR in the figures repo, with the two PRs cross-
   linked.
3. **Build.** `uv` resolves the Python toolchain (see Prerequisites above),
   then `make html` and `make latexpdf` produce the distributable outputs
   alongside a text build that feeds the search index. Outputs land in
   `_build/html/` (extensionless static pages), `_build/latex/PID.pdf?2026-05-03`
   (Tufte-styled, A4, Palatino, built via `pdflatex` / `latexmk`), and
   `_build/text/` (consumed by Pagefind, copied into the HTML tree as
   `_sources/`).
4. **Search.** Sphinx's own `searchindex.js` is the canonical search backend;
   [Pagefind](https://pagefind.app) is layered on top to power the Ctrl+K
   search box wired into the sidebar.
5. **CI/CD.**
   [`.github/workflows/build-deploy.yml`](.github/workflows/build-deploy.yml)
   runs on every push to and PR against `master`. It checks out both repos,
   sets up Python 3.12, `uv`, and Node.js, installs a full TeX Live, builds
   HTML and PDF, and asserts both artifacts exist. On pushes to `master`
   only, it then rsyncs `_build/html/` and `_build/latex/PID.pdf?2026-05-03` over SSH to
   the learnche.org host (using the `LEARNCHE_SSH_KEY` and
   `LEARNCHE_SSH_USER` repository secrets).

### Design choices worth knowing

* **Extensionless URLs are intentional.** Pages are served as
  `/pid/contents`, not `/pid/contents.html`. Years of citations and external
  links point at the extensionless form, so `conf.py` sets
  `html_file_suffix = ""` and `html_link_suffix = ""`, and both the
  production webserver and `start_server.py` serve the extensionless files
  as `text/html`. Reverting this would break inbound links silently.
* **Pull requests build but do not deploy.** PRs run the full HTML and PDF
  build to catch breakage, but the SSH and rsync steps are gated on
  `github.event_name != 'pull_request'`. Only pushes to `master` reach the
  server.
* **Pagefind needs a custom glob.** Because output files have no `.html`
  extension, Pagefind's default `**/*.html` glob would match nothing. The
  Makefile invokes Pagefind with `--glob "**"` and prefixes the call with
  `-` so an indexing failure doesn't break the build.

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

* `copy-html.sh` is a manual rsync fallback for `_build/html/` and the PDF —
  useful when CI is unavailable. Day-to-day deploys happen automatically via
  the GitHub Actions workflow described in
  [How this book is published](#how-this-book-is-published).
  Maintainer-only; assumes SSH access.
* `start_server.py` serves `_build/html/` locally on port 8080 with the MIME
  types Pagefind expects. It is invoked by `make serve`.
* The release version is tracked in [`pyproject.toml`](pyproject.toml).
* [`TODO.md`](TODO.md) is a working backlog. Migrating items to GitHub Issues
  is encouraged.

</details>
