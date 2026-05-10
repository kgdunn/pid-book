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
`my-extensions/`, `_static/`, `_templates/`, or anything imported by them),
verify locally that **both** `make html` and `make latexpdf` still succeed
before opening the PR. A broken HTML build is usually obvious; a broken
LaTeX build often only surfaces in the PDF.

If you need a quick test `make text` MUST succeed: no warnings and no errors
allowed.

## URLs and HTML output: no `.html` extension, ever

The book at <https://learnche.org/pid> has always been served with
extensionless URLs (e.g. `/pid/contents`, not `/pid/contents.html`).
This is intentional and must not be reverted. Sphinx is configured to
match:

- `html_file_suffix = ""` — built files have no extension on disk
  (`_build/html/contents`, `_build/html/data-visualization/box-plots`,
  etc.).
- `html_link_suffix = ""` — internal links in the rendered HTML also
  omit the extension.
- `master_doc` / `root_doc = "contents"` — the entry page is
  `_build/html/contents`, **not** `index.html`.
- `start_server.py` (used by `make serve`) already serves extensionless
  files as `text/html`; the production webserver does the same.

**Do not introduce code or config that assumes `.html`-suffixed
filenames.** This includes:

- Build verification: check `_build/html/contents`, never
  `_build/html/index.html`.
- Search/indexers: Pagefind's default glob is `**/*.html` and matches
  nothing here — that's why the `npx pagefind` line in `make html` is
  prefixed with `-` (best-effort). Sphinx's own `searchindex.js` is the
  real search; do not flip the file-suffix settings to make Pagefind
  happy.
- Rsync / deploy: don't filter by `*.html`; copy the whole tree.
- External tooling that walks the site: configure it to treat
  extensionless files as HTML, not the reverse.

Years of citations and external links point at the extensionless URLs.
Reverting would break them silently.

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

## Telemetry

The HTML book ships privacy-first telemetry (cookieless GoatCounter pixel,
search-query events, server-log-derived sidebar sparklines). It is
production-only — gated on `PID_BOOK_TELEMETRY=1`, set only for non-PR
builds in `.github/workflows/build-deploy.yml`.

**Hard rules** when touching anything in this area:

- Local `make html` (no env vars) MUST produce HTML with no `goatcounter`
  string anywhere — verify with
  `grep -r goatcounter _build/html/contents` returning zero hits.
- PR builds MUST NOT enable telemetry. The workflow gates this; do not
  weaken the gate.
- Any code that calls home MUST short-circuit on `localhost`,
  `127.0.0.1`, `*.local`, and `file://` so CC BY-SA self-hosters do not
  leak data to our dashboard. See `_static/js/telemetry.js` Section 0.
- The reader-facing `/pid/privacy` page (`privacy.rst`) is the public
  contract. If you change what is collected, update that page in the
  **same** PR.

The full design, build wiring, runtime behaviour, server pipeline, and
operations cookbook live in [`docs/telemetry/`](docs/telemetry/). Read
`docs/telemetry/README.md` first; it links to the rest.
