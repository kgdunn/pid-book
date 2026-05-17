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
2. Build the book locally (see [README.md](README.md)) and verify your change
   renders correctly in **both HTML and PDF** if it touches content. Math,
   figures, and tables often render differently in the two backends.
3. Run `make linkcheck` if you added or changed external links.
4. Commit with a descriptive message. Reference an issue number when relevant
   (e.g. `Fix off-by-one in EWMA limit (#42)`).
5. Open a pull request against `main`. Describe what changed and, where
   useful, attach a before/after screenshot of the rendered page.

Small, focused PRs are reviewed faster than sweeping ones. If you have a large
change in mind, split it.

## Working with the figures repository

Figures live in a separate repository: <https://github.com/kgdunn/figures>.
If your change adds or modifies figures, please open a parallel PR there and
link the two PRs.

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

## Code of conduct

Be kind. Assume good faith. The goal is a better book for everyone who is
trying to learn this material.

## License of contributions

By submitting a contribution you agree that it will be licensed under the
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license, the
same license the book is distributed under.
