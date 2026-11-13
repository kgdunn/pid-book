# Experimental design knowledge graph (draft)

A graph of the design and analysis of experiments in *Process Improvement using Data*, for the
factorial app: chapter 5, plus three design terms from chapter 7's mixed-level profile case study
(split-plot design, coding schemes for a categorical factor, the joint F-test of a categorical
interaction). 237 terms and 489 links of 35 kinds, grouped into 13 topics by consensus Louvain
clustering, three of which open into 13 sub-topics.

Chapter 7's multivariate sections (batch and multivariate monitoring, soft sensors, image
analysis, process understanding, troubleshooting, product development by model inversion) and the
chapter 6 anchors they needed were reviewed and then removed, because the app is about designed
experiments only; they are in the git history and in `audit/result_F.json` and `result_G.json`.

**Every term and every link cites the book**: a `file:line` in pid-book, and for each term the
words on that line it comes from. The build checks every quote against the book's current text and
stops if one no longer matches, so the graph cannot drift from the book unnoticed.

The map is drawn by the factorial app, at <https://factori.al/map/>: zoomed out it shows the
topics; zooming in opens the larger ones into named sub-topics, then names their terms; tapping a
term shows its definition, the book's own line, and its links. This folder holds the data; the
map's page (`web/map/index.html` and `web/map.js` in
[process-improve](https://github.com/kgdunn/process-improve/tree/main/web)) is its only viewer, so a
change to how the map looks is made there, once.

To do the same with your own texts, see [`HOWTO.md`](HOWTO.md).

## Files

| File | What it is |
|---|---|
| `graph.yaml` | **The source.** Terms (with their evidence) and links, one per line: `[source, VERB, target, evidence]`. A term's `aliases` are other names the book uses, shown on the map; its `found_as` are names other texts use: searched, matched, and listed on the term's card on a line of their own, "In other texts". |
| `build_kg.py` | Checks `graph.yaml` against the book; writes the generated files below. |
| `layout_kg.py` | Consensus Louvain topics and fixed positions for the map; writes `doe_kg_map.json`. |
| `check_levels.py` | How stable the topics are across Louvain seeds, and which get a second level, and why. |
| `check_anchors.py` | Checks every book link's `#anchor` on learnche.org (needs the network). |
| `doe_kg.json`, `doe_kg_map.json` | Generated: the graph, then with topics and positions (the data the map draws). |
| `doe_kg.cypher` | Generated: the graph as Cypher, for an empty Neo4j database. |
| `audit/` | The November 2026 accuracy review, and the one-off scripts that reshaped the graph. |

## Rebuild

From this folder, against the book it sits in:

```bash
uv run --no-project --with pyyaml==6.0.1 python -I build_kg.py ..
uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I layout_kg.py
```

`build_kg.py` stops, listing every problem, when a quote is not on its cited line, a book label
does not resolve, a verb is not in its list, a term has no links, a definition is over 32 words,
or a text contains an em-dash. The layout is reproducible: Louvain runs on integer node ids and each
topic's layout on a sorted graph.

Then check the result:

```bash
python3 check_anchors.py                 # the book links on learnche.org
uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I check_levels.py doe_kg_map.json
```

## Publish to the map

Once a change here is merged, copy `doe_kg_map.json` into process-improve as `web/map/graph.json`,
stamped with the pid-book commit it came from (the app's tests require the stamp), then open a
pull request there; its tests drive the map in Chromium on a phone and a desktop:

```bash
python3 -c 'import json, subprocess, sys
data = json.load(open("doe_kg_map.json"))
commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
source = {"repository": "kgdunn/pid-book", "path": "knowledge-graph/doe_kg_map.json", "commit": commit,
          "note": "Built and checked against the book there (build_kg.py, layout_kg.py); copy it again to update."}
json.dump({"source": source, **data}, open(sys.argv[1], "w"), separators=(",", ":"))' \
  path/to/process-improve/web/map/graph.json
```

## Reading levels

The map shows the graph at three levels: Beginner, Intermediate and Adventurous, each holding every level
below it. `build_kg.py` gives each term its level (`levels()`) from where chapter 5 introduces it, reading
the chapter in its own order (the toctree, as `tools/check_code_blocks.py` reads it):

- **Beginner**: up to the two-level full factorials and their analysis.
- **Intermediate**: from fractional factorials through blocking, response surface methods and several
  responses.
- **Adventurous**: from optimal designs on: DSD and OMARS designs, judging designs, mixtures, the general
  approach that ties the chapter together, and the specialised subsections on canonical analysis and EVOP.

A term is introduced at its first index entry or at the line the graph cites, whichever the reader meets
first; a `level:` on the term overrides that when the book teaches it earlier than either. A term that
another REQUIRES is pulled down to that term's level, and a term with no link at its level moves up until it
has one. Each term also carries its `order`, its rank in the book's order of introduction.

## What another text also states

`project_text.py` compares another book with the graph (`PROJECTION.md`). What a reviewed text shares with
the graph is listed under that text in `graph.yaml`'s `corroborated`, with the text itself in `sources`; the
text's own words stay out of this repository. An entry is a link the text also states, written as the link
is in `edges`, or the id of a term the text defines as the book does. `build_kg.py` checks that each entry
exists and gives every link and every term an `also` list of the texts that back it, which the map draws.

## When the book changes

A paragraph added near the top of a file moves every line below it. `graph.yaml` records the book
commit it was last checked against (`checked_against`), and `build_kg.py` follows each citation from
that commit to the book as it is now, with git and a line diff:

- a line that only moved is followed, and needs nothing;
- a term whose cited line was rewritten is found again by its quote, anywhere in its file;
- a link whose cited line was rewritten is listed (`check: ...`) for a person to read again, since a
  link has no quote to search for;
- a term whose quote is gone from the book stops the build.

`build_kg.py --relocate ..` writes the new line numbers, and the book's current commit, into
`graph.yaml`. The `Knowledge graph` workflow (`.github/workflows/knowledge-graph.yml`) runs the
check on every pull request that touches chapter 5, chapter 7 or this folder, and turns each link to
read again into a warning on the pull request.

## How the topics are found

One Louvain run depends on its random seed: single runs reproduce the published topics at a median
adjusted Rand index of 0.82, and as low as 0.65. So `layout_kg.py` uses consensus clustering
(Lancichinetti and Fortunato, 2012): it runs Louvain 200 times, links each pair of terms by the share
of runs that put them together (pairs under half are dropped), clusters that consensus graph the
same way, and repeats until all 200 runs agree. Consensus from four other seed batches reproduces the
published topics at 0.95 to 0.98; the terms that still move sit between two topics (for example
degrees of freedom, alias matrix). At 100 runs a round, a whole small topic could still flip.

**The second level** is found the same way, by consensus inside each topic, and drawn only where it
is worth reading: a topic gets sub-topics when it has at least 20 terms and two other seed batches
reproduce its split at an adjusted Rand index of 0.8 or better. Three topics qualify (13 sub-topics);
"Fractional factorials, aliasing, resolution and screening" has 30 terms but splits differently with
the seed (0.76), and the other nine have fewer than 20 terms and are read whole. A sub-topic is named after its most
connected term unless `SUB_NAMES` in `layout_kg.py` gives it a better heading; the layout says when
one of those names no longer has its term as a hub. Sub-topics are packed tightly, greedily, so a
chain of links does not stretch them into a line.

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

- USES still carries 97 of the 489 links; some could be sharper.
- A quote must sit on one source line for the mechanical check, so some are sentence fragments.
- The chapter exercises are not covered.
