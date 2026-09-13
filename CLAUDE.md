# Repository instructions for Claude Code

These instructions apply to any Claude Code session working in this
repository. Follow them in addition to the normal workflow.

## Replying in chat

These four rules govern what you write back to the user in the session. They are
separate from the book's prose voice below, which governs what goes into the RST.

- **Lead with the result.** Your first sentence answers "what happened" or
  "what's the answer".
- **Cut narration.** Do not restate the request, the plan, or each step you took.
  Report outcomes, decisions, and anything the user must act on.
- **Short by default.** Answer simple questions in 1 to 3 sentences of plain
  prose.
- **Never trade correctness for brevity.** Error reports, failing output, numbers
  the user will rely on, and caveats that change a decision keep their full
  content.

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

**Length and focus**

- Say it once, briefly. A passage that restates what a figure, a caption
  or a printed result already shows is cut, not trimmed. A first draft of
  a paragraph is usually two to five times too long; keep the claim, its
  reason and its consequence, and stop.
- Do not repeat numbers the reader can read off a plot or a table. Quote a
  number only when it is not on a figure (an average over several curves,
  the sample at which a curve crosses a threshold), and print it in the
  code with the value echoed in a comment, so the checker verifies it.
- Explain a principle in general terms and keep case-specific numbers for
  the results. "The early estimates scatter more widely than the final
  scores" belongs in the explanation; "fourteen times more after four
  samples" does not.
- Use bullets for a sequence of steps or a set of parallel facts, and do
  not dive into detail inside them.
- Cut method history, alternative methods and "prior experience" asides
  that the point does not need. The book is self-contained: never refer to
  course notes or other material the reader does not have.
- One metric where one will do (the leave-one-batch-out RMSEP, not RMSEE
  and RMSEP side by side).

**Section construction**

- A section states its claim first, and the claim is the one that survives a
  change of data. Open with the sentence a reader could carry to their own
  plant ("A batch can be unusual in one block and ordinary in the others, and
  the super score hides exactly that"), and only then name the batches, runs
  or values that show it.
- Never make the reader assemble the general claim out of particulars and meet
  it in the last line. If a passage ends on its point, move that line to the
  top and cut whatever no longer earns its place.
- The paragraph rule below is not enough on its own: five paragraphs that each
  run claim, reason, consequence can still sit in the wrong order, and the
  section then reads as a report of what was found rather than as an argument.
- Say what it means for someone running the process, in a clause or a
  sentence, with the number that carries it, then stop. A passage that ends at
  what happened is unfinished.
- Method is a subordinate clause, not a paragraph, unless the method is what
  the section is about. "Placing every batch with whichever of the two class
  centres is nearer, which is what the figure draws" replaced a paragraph.
- Delete the housekeeping: the case set aside, the caveat not pursued, the
  thing "not examined here". If it mattered, it would be examined.
- Numbers name things, or they support a claim already made. A run of values
  the reader has to turn into a conclusion is doing the conclusion's work.

**Paragraph construction**

- One idea per paragraph: claim, reason, consequence. Do not splice a
  second idea on with a colon or a semicolon.
- Keep the example fixed inside an argument: not "ten samples" in one
  sentence and "four samples" in the next for the same point.
- Reconcile statements a careful reader would set against each other (a
  list that "is not used to build the model" while its batches sit in the
  training set): say precisely what is used, and for what.
- A heading says what the section does for the reader ("The final model,
  used to verify the unusual batches detected above"), not its topic.

**Figures and captions**

- Every score plot carries the percent of variance explained per component
  on its axes, in square brackets.
- Annotate on the figure the thing the text discusses: an arrow for a
  contribution direction, with a marker at its origin; a batch marked and
  labelled when a later section uses it. Keep annotation text small.
- Markers must read on every background they cross (white face and dark
  edge on top of bars). Labels never sit on other points: move them to the
  other side of the marker, or onto a short leader line. Legends go where
  the data are not.
- Beside a derived statistic, show the raw data (raw trajectories in a 2x2
  panel beside contribution bars) rather than a second derived panel.
- Integer axis ticks for integer-like quantities; a band of one error, not
  two, unless the text says why.
- A caption says what the reader should see and what it means ("Dots help
  show how consistent each batch in the cluster is with the group").
- When the text claims that a quantity behaves in a certain way, show it
  in a figure.

**Process**

- When a wording or style fix may recur elsewhere in the file, ask before
  changing the other occurrences rather than assuming.
- For content edits, run `make text` and the code checker; do not run
  `make html` or rebuild a review rendering unless asked.

## Every Python case in the book runs in CI

The book demonstrates its computations with the companion package
`process-improve`. To keep the two in step, **every** `.. code-block:: python`
and every `.. literalinclude::` of a `.py` file is executed by
`tools/check_code_blocks.py`, locally with `make check-code` and in CI by
`.github/workflows/check-code.yml`. The CI gate runs against the PyPI release
(what readers install); an advisory job runs against the library's `main`
branch so a coming rename is visible before it ships.

The contract, which any new or edited code must satisfy:

- **A chapter is one linear script.** Blocks run in toctree order, across all
  the files of a chapter, sharing one namespace. A block may rely on names
  defined in earlier blocks of the same chapter (that is encouraged: load data
  once, fit once) and on nothing else. Imports go in the first block that needs
  them.
- **It must run against the released `process-improve[all]`**, on the data set
  URL the text shows, without user input. Plots are fine (`fig.show()` is a
  no-op under the checker); files written to disk are not.
- **No deprecated library names.** A `DeprecationWarning`, or any warning class
  the library defines (for instance `SpecificationWarning`), that points at the
  book's own line fails the block. When the library renames something, the book
  moves with it; do not paper over the warning.
- **Echoed results are checked, and a mismatch fails.** A comment right after a
  `print(...)` that repeats its output (`# [0.255, 0.367, ...]`) is compared with
  what the block printed. Every `make check-code…` target and CI run with
  `--strict-output`, so a number that stops reproducing fails the chapter even
  though the code still runs, and a per-chapter or per-file run is as trustworthy
  as the full one; invoking `tools/check_code_blocks.py` directly without the flag
  reports mismatches without failing, which is easier to work through when several
  are in flight. Use this idiom for every number the prose
  then quotes. Print the value in the shape the comment claims: a dict repr drops
  a trailing zero, and a Series or array repr carries full precision, so
  `print(f"{value:.2f}")` beats `print(value)` when the prose quotes two decimals.
- **Markers are the exception, not the rule.** An RST comment on the line before
  the directive (blank lines between are fine):

  ```rst
  .. code-check: skip pseudo-code showing the shape of the loop, not runnable
  .. code-block:: python

  .. code-check: requires pyoptex
  .. code-block:: python

  .. code-check: allow-warnings demonstrates the warning the reader will see
  .. code-block:: python
  ```

  `skip` is for an illustrative fragment that is not meant to run; give the
  reason. `requires` skips the block when the named module(s) are not
  installed (`pyoptex` cannot coexist with `process-improve[all]`); write the
  module names first and any explanation after a `--`. Never mark a block to
  hide a failure; fix the code or the prose instead.

  Written `.. code-check-file:` instead, on its own line anywhere in the file,
  the same three apply to **every** block in that file. That is the right
  granularity when one block's dependency decides the whole file: the blocks
  share a namespace, so a file whose first block cannot run has nothing later
  to run either. `mixed-level-profile-case-study.rst` uses it for `pyoptex`.
  A per-block marker still wins for the block it sits above.
- **Before pushing**, run the chapter you touched:
  `make check-code-chapter CHAPTER=<dir>` (verbose, one line per block), or
  `make check-code-file FILE=<path.rst>` for one file after the files that
  precede it. `make check-code` runs everything in parallel. The PR body
  reports the result. Always go through `make`: it resolves
  `process-improve[all]` the way a reader's `pip install` does. Running the
  checker inside a clone of the library instead uses that clone's dev
  environment, which carries dev-only packages (`pyoptex` among them) and will
  pass blocks that CI then fails.
- **When the library changes**, the book PR follows in the same cycle. A
  breaking rename in `process-improve` that reaches PyPI before the book is
  updated turns the CI gate red for every book PR.

## Version and citation metadata

The release version is `pyproject.toml` `version` (there is no `version.txt`).
Separately, `CITATION.cff` carries the citation's own calendar version, which is
what GitHub's "Cite this repository" button and Zenodo read.

**Whenever you plan a PR with substantive changes (content, new sections, build
changes: anything beyond a typo or link fix), update all three before
committing:**

1. `CITATION.cff` `version:` to today as `YYYY.MM.DD`.
2. `CITATION.cff` `date-released:` to today as `YYYY-MM-DD`.
3. The trailing year of the year range in the README's suggested attribution
   line (e.g. `2010-2026`), if it is not already current.

Skip this and the citation button keeps showing a stale revision.

## Cutting a release (Zenodo DOI archiving)

Releases are deliberate: not every merge to `main` warrants one, and they are
never created automatically. **After a PR with substantive changes merges to
`main`, ask whether to cut a release.** If the answer is no, do nothing.

The tag has to be pushed by the maintainer, because a Claude-on-the-web session's
git proxy accepts only the working branch. So prepare and hand over:

1. Confirm `main` is up to date with `origin/main`.
2. Write the release notes to a file; they become the Release body, so summarise
   what changed since the previous release.
3. Give the maintainer the commands, dated today:
   `git tag -a vYYYY.MM.DD origin/main -F <notes-file>` then
   `git push origin vYYYY.MM.DD`.

The tag without its `v` must equal the `CITATION.cff` `version:` already merged.
Pushing it triggers `.github/workflows/release.yml`, which creates the Release;
Zenodo archives that and mints a DOI. Add the concept DOI (the one that always
resolves to the latest release) to `CITATION.cff` in a follow-up PR, under an
`identifiers:` block of `type: doi`. Enabling the Zenodo archive itself is a
one-time manual step in the owner's Zenodo account.

## Build verification before claiming a build change works

If a PR touches the build (`Makefile`, `pyproject.toml`, `conf.py`,
`my-extensions/`, `_static/`, `_templates/`, or anything imported by them),
verify locally that **both** `make html` and `make latexpdf` still succeed
before opening the PR. A broken HTML build is usually obvious; a broken
LaTeX build often only surfaces in the PDF.

If you need a quick test `make text` MUST succeed: no warnings and no errors
allowed.

## URLs and HTML output: no `.html` extension, ever

The book at <https://learnche.org/pid> has always been served with extensionless
URLs (`/pid/contents`, not `/pid/contents.html`). Years of citations and external
links point there, so reverting would break them silently. Sphinx is configured to
match: `html_file_suffix = ""` (no extension on disk), `html_link_suffix = ""` (nor
in internal links), and `root_doc = "contents"`, so the entry page is
`_build/html/contents` and **not** `index.html`. `start_server.py` (`make serve`)
and the production webserver both serve extensionless files as `text/html`.

**Do not introduce code or config that assumes an `.html` suffix.** In particular:

- Build verification checks `_build/html/contents`, never `_build/html/index.html`.
- Pagefind's default glob is `**/*.html` and matches nothing here, which is why
  the `npx pagefind` line in `make html` is prefixed with `-` (best-effort).
  Sphinx's own `searchindex.js` is the real search; do not flip the file-suffix
  settings to make Pagefind happy.
- Rsync and deploy copy the whole tree; they never filter by `*.html`.
- External tooling that walks the site is configured to treat extensionless files
  as HTML, not the reverse.

## Figures repository

Figures live in <https://github.com/kgdunn/figures> and are symlinked in as
`figures/`. A content change that references a new or modified figure needs a
parallel PR there, with the two PRs linked in each other's description.

### The deploy order is figures first

`build-deploy.yml` checks out `kgdunn/figures` at its default branch, not at a
branch matching the book's. A book PR referencing a not-yet-merged figure
therefore fails the PDF step (`! Package pdftex.def Error: File
'figures-src/.../<name>.png' not found`, followed by a hundred knock-on
"undefined reference" lines because the run stops before `PID.toc` is written).
The HTML build passes in the same run; only `pdflatex` treats a missing image as
fatal.

**This is known and expected. Do not report it, do not diagnose it in the PR
thread, and do not propose a workflow change to resolve a matching figures
branch.** Merge the figures PR first, then re-run the book workflow and it goes
green. Carry on with the book work in the meantime.

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
search-query events, server-log-derived sidebar sparklines), production-only: gated on
`PID_BOOK_TELEMETRY=1`, set only for non-PR builds in `build-deploy.yml`.

**Hard rules** when touching this area:

- Local `make html` (no env vars) MUST produce HTML with no `goatcounter` string
  anywhere: verify with `grep -r goatcounter _build/html/contents` returning zero
  hits.
- PR builds MUST NOT enable telemetry. The workflow gates this; do not weaken it.
- Any code that calls home MUST short-circuit on `localhost`, `127.0.0.1`,
  `*.local` and `file://`, so CC BY-SA self-hosters do not leak data to our
  dashboard. See `_static/js/telemetry.js` Section 0.
- The reader-facing `/pid/privacy` page (`privacy.rst`) is the public contract. If
  you change what is collected, update that page in the **same** PR.

Design, build wiring, runtime behaviour, server pipeline and operations:
[`docs/telemetry/`](docs/telemetry/), starting at its `README.md`.

## Chapter rework playbook

Sweeping a chapter for technical accuracy and reproducible figures follows a
fixed order of operations, written out in
[`docs/development/chapter-rework.md`](docs/development/chapter-rework.md): read
the section, fact-check its field claims against current sources, put a code
block before every figure, verify, then open one non-draft PR per chapter. Read
it before starting a chapter sweep.
