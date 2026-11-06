# Accuracy review of a DOE knowledge graph against the book

A hand-built knowledge graph summarizes the Design and Analysis of Experiments chapter of the
open textbook *Process Improvement using Data*. Its terms and links were written from a December
2025 copy of the chapter; the chapter has grown a lot since. Your job is to check part of the
graph against the chapter **as it is now**, and to be skeptical: the author of the graph is not
the author of the book, and several links are already known to be wrong.

## Sources (read-only: do not modify any file outside the audit folder)

- Book: `/home/user/pid-book`, branch `main`. Chapter files: `design-analysis-experiments/**/*.rst`.
  Skip `design-analysis-experiments-exercises.rst` unless a term is taught only there.
- Section labels: `AUDIT/labels.json` maps every `.. _label:` in the chapter to `file:line`.
- All terms in the graph: `AUDIT/all_terms.json` (use it to avoid proposing duplicates).
- Your part of the graph: `AUDIT/input_<GROUP>.json`:
  - `nodes`: `id`, `name`, `type`, `definition`, `aliases`, `book_label` (`file:...` when the section has no label).
  - `edges`: `[source_id, RELATION, target_id]`, read as a sentence: "source RELATION target".

`AUDIT` is `/tmp/claude-0/-home-user/f5de32d9-e9cf-527e-9ba3-c74ed25f6ef9/scratchpad/audit`.

## What to check

**Every node.** Find where the current chapter defines or explains the term. Verdict:
- `correct`: the definition says what the book says, and claims nothing the book does not.
- `imprecise`: roughly right, but loses a qualification, overstates, or adds a claim the book does not make.
- `wrong`: contradicts the book, or is false in standard DOE practice.
- `not_in_book`: the current chapter does not teach this term or claim.

For `imprecise` and `wrong`, propose a replacement definition: at most 30 words, in the book's own
words where it has them, plain English, no em-dash characters. Also check `book_label`: if another
label in `labels.json` is clearly where the term is taught, give it.

**Every edge.** Verdict:
- `supported`: the book states it or it follows directly from what the book states.
- `unsupported`: plausibly true in DOE generally, but the book does not say it.
- `wrong`: false or misleading as a sentence.

For `wrong`, propose a fix: a replacement triple using existing ids (any clear UPPER_SNAKE verb),
or `drop`. If the relation verb is merely vague, say so in `note` and suggest a sharper verb.

**Within your group, also report:** pairs of nodes that duplicate or overlap, and at most 8
important terms the chapter teaches in your topics' sections that the graph lacks.

## Evidence rules

Every verdict, including `correct` and `supported`, needs evidence: `file:line` (path relative to
`/home/user/pid-book`) and a `quote` copied **exactly** from that one line, at most 30 words.
Quotes are checked mechanically against the files, so copy them; do not paraphrase or join lines.
Ignore RST markup differences only by quoting a stretch of the line that has none.

## Output

Write `AUDIT/result_<GROUP>.json`:

```json
{
  "nodes": [{"id": "", "verdict": "", "evidence": "", "quote": "", "definition": "", "book_label": "", "note": ""}],
  "edges": [{"source": "", "relation": "", "target": "", "verdict": "", "evidence": "", "quote": "", "fix": "", "note": ""}],
  "overlaps": [{"ids": ["", ""], "note": ""}],
  "missing": [{"name": "", "type": "", "definition": "", "book_label": "", "evidence": "", "quote": "",
               "links": [{"relation": "", "target": "", "evidence": ""}]}]
}
```

Leave `definition`, `fix` and `book_label` empty when nothing should change. Types for new terms:
Concept, Method, DesignType, Property, Criterion, Plot, Phase, Guideline, Diagnostic, Example,
Question, Reference. Cover every node and every edge in your input file.

Your final message: at most 150 words, with counts per verdict and the five most serious problems.
