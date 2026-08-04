# Repository instructions for Claude Code

These instructions apply to any Claude Code session working in this
repository. Follow them in addition to the normal workflow.

## Writing style: never use em-dashes

Do not use em-dashes (`—`) in any prose you write or edit: README, RST
source, commit messages, PR descriptions, or code comments. Use a colon, a
comma, parentheses, or two separate sentences instead. En-dashes (`–`) in
numeric ranges such as the `2010–2026` year range are correct and should
stay.

## Writing style: the author's voice

When writing or editing prose for this book, match the author's voice.
These rules are distilled from repeated corrections; follow them so the
same edits do not have to be made again.

**Tone**

- Compare, do not advocate. When weighing designs, methods, or options,
  lay out the trade-offs neutrally and let the reader (or the purpose of
  the study) decide. Do not argue that one option is better or worse,
  crown a winner, or tell the reader what they "should" do.
- No dramatic or loaded framing. Avoid words like "trap", "flatters",
  "lying", "the whole story". Say plainly what happens.
- Do not moralize. Never label a quantity, reading, or comparison as
  "honest" (it implies the alternatives are dishonest). Cut editorial or
  sarcastic asides such as "as they should" or "a number nobody asked
  for".
- Do not overstate. Avoid "always", "never", "obviously", "the whole
  story" unless the claim is literally true; prefer measured wording.
- No cute or colourful adjectives standing in for precision (e.g.
  "thrifty"). Use plain, exact language.
- Avoid idioms and colloquialisms; prefer plain, literal phrasing. For
  example "shore it up" (use "strengthen it") or "top them all" (use "is
  best in every column").
- Prefer concrete, reader-directed phrasing over an abstract
  nominalisation. For example "the dilemma resolves based on your
  intentions", not "resolves by purpose".

**Technical rigour**

- Define before you use. Introduce a term or metric in plain words
  before leaning on it; never name-drop a concept (an optimality
  criterion, for instance) that has not been set up. If you add a metric,
  explain what it measures and why it belongs here.
- Use terms correctly. Do not stretch a name to cover something it does
  not mean (e.g. T-optimality is model discrimination, not total
  information). Verify the definition; if unsure, flag it rather than
  bluff.
- Re-explain at the point of use. Briefly restate what a term means
  where it appears again, rather than relying on the reader to scroll
  back to an earlier definition. Likewise, name the object at each
  mention (the "nine-run DSD", the "thirteen-run OMARS design"), not a
  bare "the nine-run design", so the reader need not scroll back to
  recall which is which.
- Prefer the exact technical term to a loose paraphrase. For example
  "estimate the coefficients jointly", not "estimate them as a set"; and
  "the running fraction (percentiles)", not "the running fraction of
  sampled locations".
- State the scenario first. Make the assumptions explicit before drawing
  a conclusion (for example: the model is already fixed, and we are
  comparing where the runs are placed).

**Formatting**

- Numbers: keep a consistent number of significant figures (do not
  blanket-round to a fixed number of decimals); attach units ("46 runs",
  not "46"); no space before "%".
- Tables: capitalise the first-column labels, and order the columns
  meaningfully, keeping any related figure in the same order.
- Keep paragraphs short; split a long one at its natural seam.
- Cross-reference with an explicit ``:ref:`` link, not a positional word.
  The HTML edition splits sections onto separate pages, so "the example
  above" may sit on a different page; link to the labelled target rather
  than writing "above" or "earlier".
- Do not refer to a table or figure before it appears in the text. If a
  forward reference is unavoidable, point to it explicitly as "below".

**Process**

- When a wording or style fix may recur elsewhere in the file, ask before
  changing the other occurrences rather than assuming.

## Bump the version and citation date whenever you plan a PR

This repository ships release metadata in three places that reusers and
GitHub's "Cite this repository" button depend on:

- `CITATION.cff` `version:`, a calendar version written as `YYYY.MM.DD`.
- `CITATION.cff` `date-released:`, written as `YYYY-MM-DD`.
- `README.md`, the suggested attribution line, which carries a year range
  ending in the most recent update (e.g. `2010–2026`).

**Whenever you are planning a pull request that contains substantive changes
(content edits, new sections, build changes, anything beyond a pure typo or
link fix), update all three before committing:**

1. Set `CITATION.cff` `version:` to today's date as `YYYY.MM.DD`.
2. Set `CITATION.cff` `date-released:` to today's date (`YYYY-MM-DD`).
3. Update the trailing year of the year range in the README's suggested
   attribution line to the current year, if it isn't already.

The `CITATION.cff` `version:` is the citation's own calendar version. It is
independent of the `pyproject.toml` `version` covered under "Where the
canonical version lives" below. When a release is cut, this `version:` value
must equal the release tag with the leading `v` removed (see "Cutting a
release" below).

If you skip this step, the "Cite this repository" button keeps showing a
stale version and date, and reusers of the book undercredit the latest
revision.

## Cutting a release (Zenodo DOI archiving)

GitHub Releases of this book are archived by Zenodo, which mints a DOI for
each one. Releases are deliberate: not every merge to `main` warrants one,
so they are never created automatically.

**After a pull request with substantive changes merges to `main`, ask the
user whether to cut a release.** If they decline, do nothing. If they agree,
the tag has to be pushed by the maintainer: a Claude-on-the-web session
cannot push tags, because its git proxy accepts only the working branch.
Claude's job is to prepare everything and hand over the commands:

1. Make sure `main` is up to date with `origin/main`.
2. Write the release notes to a file. They become the GitHub Release body,
   so summarise what changed since the previous release.
3. Give the maintainer an annotated, calendar-versioned tag command to run,
   using today's date:
   `git tag -a vYYYY.MM.DD origin/main -F <notes-file>`
   followed by `git push origin vYYYY.MM.DD`.

Pushing a `vYYYY.MM.DD` tag triggers `.github/workflows/release.yml`, which
creates the GitHub Release automatically. Zenodo then archives that release
and issues a DOI. The tag version without the `v` must match the
`CITATION.cff` `version:` already merged in the PR.

Once Zenodo has minted the concept DOI (the one that always resolves to the
latest release), add it to `CITATION.cff` in a follow-up PR under an
`identifiers:` block of `type: doi`, so the citation metadata is complete.

Enabling the Zenodo archive itself is a one-time manual step the repository
owner performs in their Zenodo account; it cannot be scripted here.

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

### The two repositories are decoupled, and the deploy order is figures first

`.github/workflows/build-deploy.yml` checks out `kgdunn/figures` at its default
branch, not at a branch matching the book's. A book PR that references a
not-yet-merged figure therefore fails the PDF step:

```
LaTeX Warning: File `{figures-src/least-squares/<name>}.png' not found
! Package pdftex.def Error: File `figures-src/least-squares/<name>.png' not found
! Emergency stop.
```

The HTML build passes in the same run; only `pdflatex` treats a missing image as
fatal, and the 100-plus "undefined reference" lines that follow are a knock-on of
the run stopping before `PID.toc` is written, not a second problem.

**This is known and expected. Do not report it, do not diagnose it in the PR
thread, and do not propose a workflow change to make PR builds resolve a matching
figures branch.** The working practice is to merge the figures PR first, then the
book PR. Once the figures PR has merged, re-run the book workflow and it goes
green. Treat the failure as a scheduling artifact of that order, and carry on
with the book work in the meantime.

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

## Chapter rework playbook

A repeatable pattern for sweeping a chapter (or numbered subsection)
for technical accuracy and reproducible figures. Work on one chapter
per PR, on the assigned `claude/<slug>` branch, opened as a single
non-draft PR against `main`.

### Step 1 — Read the section end-to-end

While reading, note three categories:

1. **Technical claims that depend on field knowledge** — measurement
   timing, sampling frequency, typical plant numbers, "every shift /
   once an hour" phrasing, instrument capabilities, method names.
2. **Figures that appear without code that would reproduce them.** A
   reader pasting the chapter top-to-bottom should be able to
   regenerate every plot from scratch.
3. **Internal inconsistencies and typos noticed in passing** (e.g. a
   number that disagrees with itself across paragraphs). Fold trivial
   fixes into the same PR — don't open a separate one.

### Step 2 — Fact-check technical claims against external sources

**Do not just take the chapter at its word, even if it sounds
authoritative.** The book has been continuously edited since 2010 and
some claims reflect 1990s-vintage equipment or older field practice.
For every claim from Step 1, run a couple of targeted external
searches (`WebSearch` and `WebFetch`) against current literature,
vendor documentation, and standards. Revise the prose to match what
the searches actually show. The fix might be:

- a worst-case anecdote softened to a typical range,
- an outdated method replaced or supplemented by the modern equivalent
  (e.g. on-line NIR analyser alongside the wet-chemistry titration),
- a misremembered number corrected,
- a standard, instrument, or vendor named explicitly so the reader can
  verify.

Anchor each revised claim to a named standard, instrument, or vendor
when one exists (e.g. ISO 302 for Kappa titration). The motivation for
the chapter's technique must still hold up after the rewrite — just
don't let it rest on a worst case that turns out not to be typical.

### Step 3 — Make every figure reproducible inline

For each `.. figure::` directive, insert a small
`.. code-block:: python` block **immediately before** it. Rules:

- **Plotly only** in chapter code, matching the rest of the book:
  `import plotly.graph_objects as go` and
  `from plotly.subplots import make_subplots`. No matplotlib in
  learner-facing code blocks.
- **Reuse variables already defined earlier in the chapter.** The
  chapter must read top-to-bottom as a single linear script — no
  redundant data loads, no refitting the same model twice.
- **Common imports in the first block only** — `numpy`, `pandas`,
  plotly, the `process_improve` symbols.
- **Define a helper once when a plot type repeats** (e.g.
  `plot_obs_pred(...)` reused at two evaluation points).
- **Static PNGs in `kgdunn/figures` stay generated by a matplotlib
  script committed alongside them in the same `kgdunn/figures`
  subdirectory** (e.g. `monitoring/adaptive-softsensor-figures.py`
  next to the `monitoring/adaptive-softsensor-*.png` it writes).
  These scripts import `process_improve` for the modelling but live
  in the figures repo, not in `process-improve`. The chapter shows
  plotly code; the embedded image is the committed matplotlib PNG.
  Only touch the script when the underlying analysis itself changes.

### Step 4 — Verify before committing

1. Drop the chapter's code blocks into a `/tmp/check_*.py` script and
   run it against the actual dataset (use the local CSV under
   `/home/user/` or `/tmp/` if the sandbox blocks the external URL).
2. Confirm every number quoted in the prose (R², RMSEP, row counts,
   table values) reproduces exactly.
3. `make text` MUST succeed with **zero warnings**.
4. `make html` MUST succeed AND
   `grep -r goatcounter _build/html/contents` MUST return zero hits.

### Step 5 — Mechanics

- Bump `CITATION.cff` `date-released:` to today (see the rule at the
  top of this file).
- Commit with a descriptive message focused on the *why*. Never
  mention the model identifier.
- Push to the assigned `claude/...` branch.
- Open a single non-draft PR per chapter against `main`. Body
  covers: what changed, what didn't, headline numbers verified,
  `make text` / `make html` results. If the underlying analysis is
  unchanged, say so explicitly.
- Subscribe to PR activity via
  `mcp__github__subscribe_pr_activity`. Respond to review comments
  and CI failures as they arrive; push small follow-up commits to
  the same PR. Unsubscription happens automatically on merge.

### Pitfalls seen so far

- **Figure appeared in §A before the data-loading code in §B.** Move
  the data load into §A so the first figure's code block can stand
  alone, and shrink the §B code block to only the modelling steps.
- **Helper returned only what the prose needed** (e.g. `rmsep`) but
  the plotting blocks also need the y-vectors. Extend the signature
  once (`return rmsep, y_obs, y_hat`) and update every call site in
  the same commit.
- **Section reorder request mid-PR.** The toctree change in
  `<chapter>/index.rst` is one line; before pushing, run
  `grep -rn -E '\b[0-9]+\.[0-9]+\b' --include='*.rst' .` to confirm
  no prose hard-codes the old numbers.
