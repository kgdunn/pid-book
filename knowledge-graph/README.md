# Experimental design knowledge graph (draft)

A graph of the core of *Process Improvement using Data*: chapter 5 (design and analysis of
experiments) and chapter 7 (its applications), with the few chapter 6 ideas that chapter 7 rests
on. 283 terms (214 from chapter 5, 62 from chapter 7, 7 chapter 6 anchors) and 571 links of 35
kinds, grouped into 12 topics by Louvain clustering.

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
| `layout_kg.py` | Louvain topics and fixed positions for the map; writes the page. |
| `template.html` | The page, without its data. |
| `check_levels.py` | How stable the topics, and possible sub-topics, are across 30 Louvain seeds. |
| `doe_kg.json`, `doe_kg_map.json` | Generated: the graph, then with topics and positions. |
| `doe_kg.cypher` | Generated: the graph as Cypher, for an empty Neo4j database. |
| `experimental-design-graph.html` | Generated: the page with its data inlined. |
| `audit/` | The November 2026 accuracy review (see below). |

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
- Reviewers F and G proposed the terms of chapter 7 and the chapter 6 anchors it needs.
- Six terms were folded into others (for example alias into confounding, steepest descent into
  steepest ascent) and six duplicate proposals merged; 123 terms are new.

Some of what it found: the book now prints 79.4% and 69.7% where the old text had 79.3% and
69.5%; hand-calculated effects in the book are full-range, like Box, Hunter and Hunter's, and only
least squares coefficients are half-range; "large interactions" signal an optimum, as distinct from
curvature; and folding the link verbs had turned the book's "a word equals I" into "uses".

## Known limits

- USES still carries 136 of the 571 links; some could be sharper.
- A quote must sit on one source line for the mechanical check, so some are sentence fragments.
- Two chapter 7 links are inferred rather than stated: soft sensors are built from happenstance
  data (chapter 7 never uses that word), and the design-build-test-learn cycle is a form of
  sequential experimentation.
- Chapter 6 is present only as the seven anchors chapter 7 needs; the exercises are not covered.

## Next steps

1. Consensus topics. Across 30 Louvain seeds the 12 topics agree with the published ones at a
   median adjusted Rand index of 0.70 (worst 0.60). Run Louvain about 100 times, count how often
   each pair of terms shares a topic, and cluster those counts.
2. A second level, only where a topic is large and its split is stable (`check_levels.py`). On the
   current graph: PCA and PLS in practice (46 terms, median agreement 0.86), full factorials (34,
   0.84), optimal designs (29, 1.00), coefficients and coding (25, 0.83) and significance (20, 1.00).
   Fractional factorials (34 terms, 0.67) and DSD and OMARS (22, 0.77) split differently with each
   seed. Recheck after step 1, since consensus topics change what each topic holds.
