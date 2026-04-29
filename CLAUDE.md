# Repository instructions for Claude Code

These instructions apply to any Claude Code session working in this
repository. Follow them in addition to the normal workflow.

## Bump the citation date whenever you plan a PR

This repository ships citation metadata in two places:

- `CITATION.cff` — the `date-released:` field
- `README.md` — the suggested attribution line, which carries a year range
  ending in the most recent update (e.g. `2010–2026`)

**Whenever you are planning a pull request that contains substantive changes
(content edits, new sections, build changes, anything beyond a pure
typo / link fix), update both fields before committing:**

1. Set `CITATION.cff` `date-released:` to today's date (`YYYY-MM-DD`).
2. Update the trailing year of the year range in the README's suggested
   attribution line to the current year, if it isn't already.

If you skip this step, GitHub's "Cite this repository" button will keep
showing a stale year and reusers of the book will undercredit the latest
revision.

## Where the canonical version lives

The release version is `pyproject.toml` `version`. There is no `version.txt`.
If you need to bump the version, edit `pyproject.toml`.

## Build verification before claiming a build change works

If a PR touches the build (`Makefile`, `pyproject.toml`, `conf.py`,
`my-extensions/`, `sphinx_rtd_theme_kgdmod/`, or anything imported by them),
verify locally that **both** `make html` and `make latexpdf` still succeed
before opening the PR. A broken HTML build is usually obvious; a broken
LaTeX build often only surfaces in the PDF.

## Figures repository

Figures live in a separate repo (<https://github.com/kgdunn/figures>) and are
symlinked in as `figures/`. If a content change references a new or modified
figure, open a parallel PR there and link the two PRs in the descriptions.

## Style for RST source

See `CONTRIBUTING.md` for the full RST style notes. Key points:

- Hard-wrap lines at ~100 characters.
- Use `:ref:` with explicit labels for cross-references, not raw section
  names.
- Use `:math:` / `.. math::` for equations.
- Use `.. code-block:: <lang>` so the LaTeX backend syntax-highlights
  correctly.
