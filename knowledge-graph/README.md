# Experimental design knowledge graph (draft)

A hand-built graph of the core of the Design and Analysis of Experiments chapter: 171 terms, 253
links of 20 kinds, grouped into 9 topics by Louvain clustering. Every term links to the section of
the book that teaches it. It was written from `../doe_extracted_text.txt`, the chapter text this
pull request extracted in December 2025.

Open `experimental-design-graph.html` in a browser to explore it: zoomed out it shows the topics,
zooming in names their terms, and tapping a term shows its links.

## Files

| File | What it is |
|---|---|
| `build_kg.py` | The terms and links, written by hand, and the checks on them. Source of truth. |
| `layout_kg.py` | Louvain topics and fixed positions for the map; writes the page. |
| `template.html` | The page, without its data. |
| `doe_kg.json` | Generated: terms and links. |
| `doe_kg_map.json` | Generated: the same, with topics and positions. |
| `doe_kg.cypher` | Generated: the graph as Cypher, to load into an empty Neo4j database. |
| `experimental-design-graph.html` | Generated: the page with its data inlined. |

## Rebuild

The book links point at the current book, so build against a checkout of `main`; against this
branch's older chapter, 22 links do not resolve and the build stops.

```bash
python3 build_kg.py ../../pid-book            # path to a checkout of main
uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I layout_kg.py
```

The output is reproducible: Louvain runs on integer node ids and each topic's layout on a sorted
graph, because networkx iterates sets of string ids in an order that changes from run to run.

## Known problems, to fix before trusting it

Content:
- Wrong links: "center point prevents lost orthogonality" (lost orthogonality is about
  constraints); "steepest descent is a kind of steepest ascent"; "a word uses the identity column"
  (a word equals I).
- Folded links lose meaning: SHOWS absorbed 14 verbs (tests, locates, seeks, ...); COMPARED_WITH
  joins "agrees with" and "contrasts with", which mean opposite things; USES is a catch-all.
- Effect sparsity and effect hierarchy are two principles merged into one node.
- "A definitive screening design is a kind of optimal design" repeats the old text; DSDs are
  built from conference matrices.

Structure and provenance:
- "Concept" holds 78 of 171 terms, so the type says little. Some terms overlap (phase 1 and
  screening; optimum and near an optimum).
- Definitions come from the December 2025 text but link to the current book, which has changed
  since; they may no longer match. Line numbers were not kept.
- The checks cover ids, orphans and book links, not meaning: the wrong links above pass them.
- Newer chapter topics are missing: OMARS, desirability, Lenth's method, power, lack of fit.
- There are now three sets of definitions: `web/glossary.js` in process-improve (80 terms), the
  package's `experiments/knowledge` YAML (31 entries), and this graph.

Page:
- The `#section` part of each book link is derived from the label name and not yet checked on
  learnche.org.
- The topics follow the links, so wrong links also move terms between topics.
