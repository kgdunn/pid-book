# Build a concept map from your own texts

This folder turned one chapter of a textbook into the map at <https://factori.al/map/>, and then
compared that map with a second textbook. This page says how to do the same with your own documents:
course notes, procedures, a manual, a standard.

## Is it automatic?

Not fully, and partly by design. You cannot yet drop a folder of texts somewhere and get a map back.
An AI coding agent (we used Claude Code) does the reading and drafting, scripts do the checking, and
a person decides what is right.

| Step | Who does it |
|---|---|
| Read the texts and draft the terms and links | An AI agent, from a short brief |
| Check that every term and link really is in the text | A script, with no judgement involved |
| Decide what stays, what is reworded, what is wrong | You |
| Group the terms into topics and lay out the map | A script |
| Compare with a second text | A script finds candidates, an AI agent judges them, a script checks its quotes, you decide |

The scripts here were written for this book. To use them on other texts, expect to adapt them; the
last section lists what is specific to the book.

## What you need

- Your texts as plain text files (Markdown, reStructuredText or `.txt`) in a git repository. For a
  PDF, `pdftotext` gives the text.
- An AI coding agent that can read files and run commands.
- Python 3.11 or later, with `pyyaml`, `networkx` and `numpy`.

## The steps

1. **Draft the graph.** Ask the agent to read your texts and write a `graph.yaml` in the format of
   the one in this folder. Each term has a name, a definition of at most 32 words in your own words,
   the `file:line` it comes from, and the exact words quoted from that line. Each link is one line,
   `[source, VERB, target, file:line]`, and reads as a sentence: "fractional factorial SUITED_TO
   screening". Start with one chapter or one document, not everything.

2. **Check it against the text.** `build_kg.py` reads `graph.yaml` and your files, and stops if a
   quote is not on the line it cites, a term has no links, or a verb is not in its list. This is
   what makes the map trustworthy: nothing is in it that the text does not say. When the text
   changes later, the same check tells you which terms and links to look at again.

3. **Review it.** Read the terms and links. An AI draft gets most of them right and a few subtly
   wrong, and only someone who knows the subject can tell which.

4. **Lay it out and view it.** `layout_kg.py` groups the terms into topics and gives each a fixed
   position. The viewer is one web page plus one script (`web/map/index.html` and `web/map.js` in
   [process-improve](https://github.com/kgdunn/process-improve/tree/main/web)); it draws whatever
   graph file you give it.

5. **Compare with another text (optional).** `project_text.py` finds where a second text names your
   terms, and an AI reviewer following `PROJECTION.md` says, for each place, whether the text
   supports a link, defines a term differently, or adds something new. Every verdict carries a short
   quote, and `project_text.py verify` drops any verdict whose quote is not in the text word for
   word. You then accept, reword or reject each one. Keep the second text out of your repository if
   it is someone else's copyright; only your decisions go in.

## What is specific to this book

Tried on a small set of unrelated notes (two Markdown files, eight terms), this is what happened:

| Script | As it is | What it needed |
|---|---|---|
| `build_kg.py` | Stops | Two edits: the list of chapter folders (`CHAPTERS`), and the reading levels, which read this book's table of contents (`levels()`). With those it checked every quote, caught a wrong one, and followed the citations after the notes were edited. |
| `layout_kg.py` | Stops | One edit: the topic names are written out for this book (`NAMES`). Naming each topic after its most connected term made it run. |
| The map viewer | Draws the map | Its title, its "Read it in the book" links and its search hint still point at this book. |
| `project_text.py` | Works unchanged | Nothing. It found the terms and links in a second text, and dropped a verdict whose quote was not in it. |

Other things to know:

- No script drafts the graph, and `PROJECTION.md` briefs the agent for the comparison only. For the
  draft, give the agent `graph.yaml` as the format to follow.
- The link verbs (`VERBS`) suit a technical subject. Change the list to suit yours.
- The comparison only proposes a new term by itself when a phrase of two or three words is repeated
  at least three times, or is introduced with words like "called". A reviewer can still add others.

If you try this on your own texts, an issue on this repository saying where it broke is welcome.
