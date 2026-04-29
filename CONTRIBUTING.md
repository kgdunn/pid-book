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

1. Fork the repo and create a topic branch off `master`.
2. Build the book locally (see [README.md](README.md)) and verify your change
   renders correctly in **both HTML and PDF** if it touches content. Math,
   figures, and tables often render differently in the two backends.
3. Run `make linkcheck` if you added or changed external links.
4. Commit with a descriptive message. Reference an issue number when relevant
   (e.g. `Fix off-by-one in EWMA limit (#42)`).
5. Open a pull request against `master`. Describe what changed and, where
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
