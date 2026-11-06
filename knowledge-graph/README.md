# Experimental design knowledge graph (draft)

A graph of the design and analysis of experiments in *Process Improvement using Data*, for the
factorial app: chapter 5, plus three design terms from chapter 7's mixed-level profile case study
(split-plot design, coding schemes for a categorical factor, the joint F-test of a categorical
interaction). 217 terms and 411 links of 35 kinds, grouped into 10 topics by consensus Louvain clustering.

Chapter 7's multivariate sections (batch and multivariate monitoring, soft sensors, image
analysis, process understanding, troubleshooting, product development by model inversion) and the
chapter 6 anchors they needed were reviewed and then removed, because the app is about designed
experiments only; they are in the git history and in `audit/result_F.json` and `result_G.json`.

**Every term and every link cites the book**: a `file:line` in pid-book, and for each term the
words on that line it comes from. The build checks every quote against the book's current text and
stops if one no longer matches, so the graph cannot drift from the book unnoticed.

Open `experimental-design-graph.html` in a browser: zoomed out it shows the topics, zooming in
names their terms, and tapping a term shows its definition, the book's own line, and its links.

## Files

| File | What it is |
|---|---|
| `graph.yaml` | **The source.** Terms (with their evidence) and links, one per line: `[source, VERB, target, evidence]`. |
| `build_kg.py` | Checks `graph.yaml` against the book; writes the generated files below. |
| `layout_kg.py` | Consensus Louvain topics and fixed positions for the map; writes the page. |
| `template.html` | The page, without its data. |
| `check_levels.py` | How stable the topics, and possible sub-topics, are across Louvain seeds. |
| `check_map.mjs` | Drives the map in headless Chromium at phone and tablet widths; fails on any misbehaviour. |
| `check_anchors.py` | Checks every book link's `#anchor` on learnche.org (needs the network). |
| `doe_kg.json`, `doe_kg_map.json` | Generated: the graph, then with topics and positions. |
| `doe_kg.cypher` | Generated: the graph as Cypher, for an empty Neo4j database. |
| `experimental-design-graph.html` | Generated: the page with its data inlined. |
| `audit/` | The November 2026 accuracy review, and the one-off scripts that reshaped the graph. |

## Rebuild

Build against a checkout of pid-book `main`: the links point at the current book.

```bash
uv run --no-project --with pyyaml==6.0.1 python -I build_kg.py ../../pid-book
uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I layout_kg.py
```

`build_kg.py` stops, listing every problem, when a quote is not on its cited line, a book label
does not resolve, a verb is not in its list, a term has no links, a definition is over 32 words,
or a text contains an em-dash. The layout is reproducible: Louvain runs on integer node ids and each
topic's layout on a sorted graph.

Then check the result:

```bash
node check_map.mjs                       # the map, in headless Chromium (needs Playwright)
python3 check_anchors.py                 # the book links on learnche.org
uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I check_levels.py doe_kg_map.json
```

## How the topics are found

One Louvain run depends on its random seed: single runs reproduce the published topics at a median
adjusted Rand index of 0.82, and as low as 0.65. So `layout_kg.py` uses consensus clustering
(Lancichinetti and Fortunato, 2012): it runs Louvain 200 times, links each pair of terms by the share
of runs that put them together (pairs under half are dropped), clusters that consensus graph the
same way, and repeats until all 200 runs agree. Consensus from four other seed batches reproduces the
published topics at 0.95 to 0.98; the terms that still move sit between two topics (for example
degrees of freedom, alias matrix). At 100 runs a round, a whole small topic could still flip.

## The accuracy review (November 2026)

The first draft was written by hand from the December 2025 chapter text. Seven reviewers checked
it against the book as it is now (`audit/BRIEF.md` is their brief; `audit/result_*.json` their
verdicts, each with an exact quote). Every quote was then verified mechanically
(`audit/verify_audit.py`), and `audit/merge_audit.py` applied the verdicts once, with every judgment
it made in named tables at its top.

- Reviewers A to D checked the 171 original terms and 255 links: 37 definitions corrected,
  17 links wrong and fixed or dropped, 5 unsupported and decided case by case.
- Reviewer E proposed the terms of chapter 5's newer sections: OMARS, definitive screening as an
  OMARS design (not an optimal design), Lenth's method, power, lack of fit, desirability, mixtures.
- Reviewers F and G proposed the terms of chapter 7 and the chapter 6 anchors it needs; all but
  three design terms were later removed, to keep the graph to designed experiments.
- Six terms were folded into others (for example alias into confounding, steepest descent into
  steepest ascent) and six duplicate proposals merged; 123 terms are new.

Some of what it found: the book now prints 79.4% and 69.7% where the old text had 79.3% and
69.5%; hand-calculated effects in the book are full-range, like Box, Hunter and Hunter's, and only
least squares coefficients are half-range; "large interactions" signal an optimum, as distinct from
curvature; and folding the link verbs had turned the book's "a word equals I" into "uses".

## Known limits

- USES still carries 88 of the 411 links; some could be sharper.
- A quote must sit on one source line for the mechanical check, so some are sentence fragments.
- The chapter exercises are not covered.

## Next steps

1. A second level, only where a topic is large and its split is stable. Find the sub-groups by
   consensus too: single Louvain runs inside a topic are as seed-dependent as at the top level
   (`check_levels.py`: fractional factorials splits at a median agreement of only 0.67).
