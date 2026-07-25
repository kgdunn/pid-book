# Contributing to *Process Improvement using Data*

Thanks for taking the time to contribute. The book has been improved
continuously since 2010 thanks to readers like you. The notes below describe
the smoothest path for getting your change merged.

## What kinds of contributions help

* **Typos, grammar, broken links** — open a PR directly; no issue needed.
* **Technical corrections** (mistakes in derivations, code, plots, captions) —
  open an issue first if the fix may be debatable, otherwise PR directly.
* **New exercises and worked examples** — very welcome. Open an issue to
  discuss scope before writing a long contribution.
* **New sections or chapters** — please open an issue first so we can discuss
  scope, fit, and notation before you invest time.
* **Build / tooling improvements** — open a PR.

For free-form feedback (course adoption, broad suggestions) you can also use
the [Google Form](https://docs.google.com/forms/d/1IpO-bvJwQwhK64eid4YXwJBvGxN5cfyYDv81G-YgWrM/viewform).

## Workflow

1. Fork the repo and create a topic branch off `main`.
2. Build the book locally (see [Building the book locally](#building-the-book-locally)
   below) and verify your change renders correctly in **both HTML and PDF** if
   it touches content. Math, figures, and tables often render differently in
   the two backends.
3. Run `make linkcheck` if you added or changed external links.
4. Commit with a descriptive message. Reference an issue number when relevant
   (e.g. `Fix off-by-one in EWMA limit (#42)`).
5. Open a pull request against `main`. Describe what changed and, where
   useful, attach a before/after screenshot of the rendered page.

Small, focused PRs are reviewed faster than sweeping ones. If you have a large
change in mind, split it.

## Building the book locally

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
| `make latexpdf` | Build the PDF (5–10 minutes; needs LaTeX). Output: `_build/latex/PID.pdf?2026-05-19` |
| `make epub` | Build the EPUB into `_build/epub/` |
| `make linkcheck` | Verify external links |
| `make clean` | Remove build artifacts (`_build/`, caches) |
| `make clean-all` | Also remove `.venv/` and `uv.lock` (forces a re-resolve on next `make setup`) |
| `make` | Default target is `latexpdf`. Run `make help` for the full list |

Compare your PDF against <https://learnche.org/pid/PID.pdf?2026-05-19> to confirm a
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

## How the book is published

The book has a fairly typical static-site pipeline:

```
RST sources ─┐
             ├─►  Sphinx  ─►  HTML (extensionless URLs) ─┐
figures/  ───┘                LaTeX ──pdflatex──► PDF    ├─► rsync ─► learnche.org/pid
                              text  (fed to Pagefind)    │
                                                         │
                       GitHub Actions (.github/workflows/build-deploy.yml)
```

Each chapter is reStructuredText in its own directory, with
[`contents.rst`](contents.rst) as the master table of contents. `uv` resolves
the Python toolchain, then `make html` and `make latexpdf` produce the
distributable HTML and PDF alongside a text build that feeds the search index.
[`.github/workflows/build-deploy.yml`](.github/workflows/build-deploy.yml) runs
the full HTML and PDF build on every push and PR; on pushes to `main` it then
rsyncs the outputs over SSH to the learnche.org host. Figures live in a
separate repository — see [Working with the figures
repository](#working-with-the-figures-repository) — and the in-book telemetry
has its own invariants — see [Telemetry and privacy](#telemetry-and-privacy).

### Design choices worth knowing

* **Extensionless URLs are intentional.** Pages are served as
  `/pid/contents`, not `/pid/contents.html`. Years of citations and external
  links point at the extensionless form, so `conf.py` sets
  `html_file_suffix = ""` and `html_link_suffix = ""`, and both the
  production webserver and `start_server.py` serve the extensionless files
  as `text/html`. Reverting this would break inbound links silently.
* **Pull requests build but do not deploy.** PRs run the full HTML and PDF
  build to catch breakage, but the SSH and rsync steps are gated on
  `github.event_name != 'pull_request'`. Only pushes to `main` reach the
  server.
* **Pagefind needs a custom glob.** Because output files have no `.html`
  extension, Pagefind's default `**/*.html` glob would match nothing. The
  Makefile invokes Pagefind with `--glob "**"` and prefixes the call with
  `-` so an indexing failure doesn't break the build.

## Working with the figures repository

Figures live in a separate repository: <https://github.com/kgdunn/figures>.
If your change adds or modifies figures, please open a parallel PR there and
link the two PRs.

### Linking a figure to the code that drew it

Long-pressing a figure in the HTML book (or Alt-clicking it) shows which
script in the figures repository drew it. Nothing needs to be added to a
figure for this to work: `my-extensions/figure_source.py` scans the figures
repository at build time, matching each image against the script that names
it in a line that writes a file, and puts the answer on the `<img>` itself as
`data-figure-source`.

That attribute is the mechanism; the JavaScript is only a convenience on top
of it. With JavaScript off, offline, or reading a `file://` copy, the page is
unchanged and the link is still in the markup. The build also writes
`_static/figure-sources.json`, the whole mapping in one file, for tooling;
the page never reads it.

Setting `figure_source_show_link = True` in `conf.py` adds a real link after
each figure, off screen until it receives keyboard focus, in the manner of a
skip link. That is a keyboard route to the source with no JavaScript at all;
the cost is one more thing for a screen reader to announce per figure, which
is why it is off by default.

Two things keep that mapping correct as figures are replaced:

* **A replacement names what it replaces.** When a new generator supersedes
  an older script, say so in its module docstring, naming the old file.
  Where two scripts claim the same image, a script that another script names
  loses, so the replacement wins automatically.
* **Reads are not claims.** A script that opens an image (the ones that join
  panels side by side, for instance) is not treated as its author. Only
  lines that write count.

To pin a figure explicitly, or to record a generator the scan cannot infer,
add a `:source:` option with the path inside the figures repository:

```rst
.. figure:: ../figures/monitoring/adaptive-softsensor-motivation.png
    :source: monitoring/adaptive-softsensor-figures.py
    :alt: Static soft-sensor prediction and laboratory values over time.
```

An explicit `:source:` always beats the scan. Keep `:alt:` for what it is
for: a description of the image for anyone who cannot see it.

## RST style notes

* Source files are reStructuredText (`.rst`), processed by Sphinx.
* Use the existing heading underline conventions in the chapter you are
  editing — they are not uniform across all chapters, but they are consistent
  within a chapter.
* Keep lines reasonably short (≤ 100 chars) so diffs are easy to review. Hard
  wrapping is preferred to soft wrapping.
* Math: prefer `:math:` for inline and `.. math::` for displayed equations.
* Cross-references should use `:ref:` with explicit labels rather than raw
  section names.
* Do not start a bullet or list item with a bare author initial
  (`J. Smith`, `S. Wold`): reStructuredText reads the leading `letter.` as
  an enumerated-list marker and mis-indents the entry. Escape the initial
  with a backslash (`\J. Smith`), or spell the first name out.
* Code blocks: use `.. code-block:: python` (or `r`, `matlab`, `text`) so the
  PDF backend syntax-highlights correctly.

## Pre-commit hooks

The repository ships a [pre-commit](https://pre-commit.com/) configuration
(`.pre-commit-config.yaml`) that catches trivial problems before they reach a
PR: trailing whitespace, missing final newlines, mixed line endings, malformed
YAML/TOML, merge-conflict markers, and obvious Python issues via
[Ruff](https://docs.astral.sh/ruff/). It also runs
[rstcheck](https://github.com/rstcheck/rstcheck) over the `.rst` sources.

Set it up once:

    make pre-commit-install

After that the hooks run automatically on every `git commit`. To sweep the
whole tree on demand — useful before opening a PR — run:

    make pre-commit-run

Ruff is scoped to the repository's own Python (`conf.py`, `start_server.py`,
`my-extensions/`); the chapter gists are left alone. rstcheck only *reports*
problems — it never rewrites the book. Both tools also install via
`uv sync --all-extras`, which pulls in the `dev` optional dependencies.

## Building with `just` (optional)

The repository also ships a [`just`](https://just.systems) recipe file
(`justfile`) that mirrors the Makefile's build commands with a friendlier
menu. It is **entirely optional** — the `Makefile` remains the canonical
entry point and is what CI uses.

`just` is a separate tool to install — see the
[install instructions](https://just.systems/man/en/packages.html), or, since
this project already uses `uv`:

    uv tool install rust-just

Then run `just` with no arguments for the menu of recipes:

    just            # list all recipes
    just html       # build the HTML book
    just pdf        # build the PDF
    just all        # build HTML, PDF and EPUB

The recipe names match the Makefile targets (`just` uses `pdf` where the
Makefile says `latexpdf`).

## Telemetry and privacy

The HTML book carries cookieless telemetry in production (pageviews,
in-book search queries, sidebar sparklines). It is **disabled by default
in local builds** — running `make html` without setting
`PID_BOOK_TELEMETRY=1` produces HTML with no script tag and no
sparkline mount. Do not enable it locally unless you are specifically
testing the production code path.

If your PR touches anything under `_static/js/`, `_templates/`,
`scripts/server/`, the `Build HTML` workflow step, or `privacy.rst`,
read [`docs/telemetry/README.md`](docs/telemetry/README.md) first —
the design has invariants (production-only, no cookies, no IPs stored,
DNT respected, self-hosters short-circuit) that are easy to break
inadvertently.

## Reporting build problems

If `make html` or `make latexpdf` fails for you on a clean checkout, please
open an issue with:

* OS and Python version (`python --version`)
* `uv --version` and `node --version`
* The full error message
* Whether the `figures/` symlink is set up

Build problems that reproduce on a clean clone are treated as bugs.

## Maintainer notes

<details>
<summary>Deployment and release</summary>

* `copy-html.sh` is a manual rsync fallback for `_build/html/` and the PDF —
  useful when CI is unavailable. Day-to-day deploys happen automatically via
  the GitHub Actions workflow described in
  [How the book is published](#how-the-book-is-published).
  Maintainer-only; assumes SSH access.
* `start_server.py` serves `_build/html/` locally on port 8080 with the MIME
  types Pagefind expects. It is invoked by `make serve`.
* The release version is tracked in [`pyproject.toml`](pyproject.toml).
* [`TODO.md`](TODO.md) is a working backlog. Migrating items to GitHub Issues
  is encouraged.

</details>

## Code of conduct

Be kind. Assume good faith. The goal is a better book for everyone who is
trying to learn this material.

## License of contributions

By submitting a contribution you agree that it will be licensed under the
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license, the
same license the book is distributed under.
