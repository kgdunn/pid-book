# Brief for a reviewer of a projection

`project_text.py candidates` has read a text that is not this book and listed, in
`projections/NAME/candidates.json`, the places where it meets the graph. Your job is to read each
candidate and say what the text actually says about it. The graph is `graph.yaml`: each term has a
`definition`, and each link reads as a sentence, `source VERB target`. `projections/graph-terms.txt`
lists every term on one line (id, name, other names, definition): check it before calling anything
new or an alias.

The text is usually someone else's copyright. Quote it only as a short citation, at most 25 words,
copied exactly; never paraphrase it into the graph, and never copy more than you need.

## What to judge

1. **`terms[].defining`**: sentences where the text may say what a term is. Compare with the
   graph's definition (`graph_says`). `agrees` when they are compatible; `differs` only when a reader
   of both would be told two different things (a narrower or wider meaning, a different condition).
   A text using a word loosely, or for something else entirely, is neither: skip it.
2. **`links[]`**: a graph link, with the sentences that name both its terms. `supports` when a
   sentence states the relation the link states; `contradicts` when it states something a reader
   could not hold together with the link. Two terms in one sentence is not support.
3. **`unlinked[]`**: two terms the text names together with no link between them in the graph.
   `missing_link` only when the text states a relation between them that the graph should carry;
   give it as `[source, VERB, target]` with a verb from `VERBS` in `build_kg.py`.
4. **`unknown[]`**: phrases that match no term. Most are not terms at all. Say `alias` when it is
   another name for an existing term (give the term's id), and `new_term` only when all four hold:
   - the text treats it as a named idea of its own, defined or used repeatedly as a technical term;
   - it is not another name for, a special case of, or an instance of an existing term;
   - a reader of the graph would need it to follow designed experiments, not to follow one example
     (the subject of an example, such as a yarn or a reaction, never qualifies);
   - it is about the design and analysis of experiments.

   Expect very few, often none. When unsure, it is not new.

## What to write

`projections/NAME/reviews.json`: a JSON list, with an entry only for `supports`, `contradicts`,
`differs`, `missing_link`, `alias` and `new_term` (skip everything else):

```json
{"kind": "link", "item": ["rsm", "SHOWS", "response_surface"], "verdict": "supports",
 "page": "p. 12", "quote": "exact words from the text, at most 25", "note": "one sentence: why"}
```

- `kind`: `definition`, `link`, `pair` or `unknown`; `item`: the term id, the link, the pair, or
  the phrase, as in `candidates.json`. For `new_term` and `alias`, name the idea as a singular,
  lowercase noun phrase ("region of interest"), so that the same idea found in two texts is one item;
  a new term may come from any sentence of the text, not only from `unknown[]`.
- `quote`: copied exactly from the sentence you judged (spacing aside); `project_text.py verify`
  drops any verdict whose quote is not in the text, word for word.
- `note`: why, in one sentence. For `missing_link`, start it with the link, `[a, VERB, b]`. For
  `alias`, start it with the term's id. For `new_term`, start it with a definition of at most 32
  words, then the two links that would join it to the graph.
