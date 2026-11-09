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

- Your texts as plain text files (Markdown, reStructuredText or `.txt`) in a folder of a git
  repository, committed. For a PDF, `pdftotext` gives the text.
- An AI coding agent that can read files and run commands in that repository.
- Python 3.11 or later: `pip install pyyaml networkx numpy scipy`.

## The steps, with the prompt for each

Each step has a prompt to paste into your agent. Replace the words in capitals: `TEXTS` is the folder
that holds your texts, and `SUBJECT` is what they are about ("bread baking", "our safety procedures").
Finish one step before starting the next.

### 0. Copy the tools in

Run this yourself, in your repository:

```bash
git clone --depth 1 https://github.com/kgdunn/pid-book /tmp/pid-book
git clone --depth 1 https://github.com/kgdunn/process-improve /tmp/process-improve
mkdir -p kg viewer/map
cp /tmp/pid-book/knowledge-graph/{build_kg.py,layout_kg.py,project_text.py,PROJECTION.md} kg/
cp /tmp/pid-book/knowledge-graph/graph.yaml kg/example-graph.yaml
cp -r /tmp/process-improve/web/{map.js,logic.js,style.css,favicon.svg,vendor} viewer/
cp /tmp/process-improve/web/map/index.html viewer/map/
git add -A && git commit -m "Concept map tools"
```

### 1. Fit the scripts to your texts

```text
The scripts in kg/ were written for one textbook. Change them so that they run on my texts in
TEXTS/, and change nothing else. They cannot run yet: kg/graph.yaml comes in the next step.

kg/build_kg.py:
1. Set CHAPTERS to the top-level folders that hold my texts.
2. Remove the reading levels: do not call levels(); leave "level" and "order" out of every term it
   writes, in the JSON file and in the Cypher file; and remove the line that prints the terms shown
   at each level.
Keep every check in check() as it is.

kg/layout_kg.py:
3. Remove NAMES and the two asserts that use it. Give each topic its most connected term (the
   highest weighted degree in the whole graph; a tie goes to the id that sorts first) as "anchor",
   and that term's name as both "short" and "name".
4. Set SUB_NAMES to {}, so that each sub-topic is named after its hub term.
5. Make code_url() return an empty string.
```

### 2. Draft the graph

```text
Read every file in TEXTS/. Then write kg/graph.yaml: a concept graph of SUBJECT as these texts
teach it. Use the format of the "nodes:" and "edges:" in kg/example-graph.yaml, without its
"level:" lines and without its "sources:" and "corroborated:" sections. That example is about
another subject: copy its format, not its content.

The first line of the file is "checked_against: " and the output of "git rev-parse HEAD".

Terms. Aim for the 30 to 40 ideas a reader most needs; fewer is fine.
- A term is an idea the text names, and explains or uses repeatedly. A passing example is not one.
- id: lowercase with underscores. name: as the text writes it, in the singular. type: one of
  TYPES in kg/build_kg.py.
- definition: at most 32 words, in your own words, saying only what the text says. No em-dashes.
- aliases: other names the text uses for the same idea, or []. Never an everyday word (such as
  "axes"): a later step finds terms in other texts by these names.
- book_label: "file:" and the file's path.
- evidence: PATH:LINE, the one line that best says what the term is. quote: words copied exactly
  from that line. Where a sentence runs over several lines, cite the line that carries its key
  words, and quote only what is on it.

Links.
- One per line: [source, VERB, target, "PATH:LINE"], with a verb from VERBS in kg/build_kg.py.
- A link must read as a true sentence, "source VERB target", and the line it cites must carry the
  key words of that relation. Two terms on one line is not enough.
- Every term needs at least one link.

Then run "python kg/build_kg.py ." and correct kg/graph.yaml until it prints "checks passed".
Never change kg/build_kg.py to make it pass. Commit kg/graph.yaml with the two files the check
writes, kg/doe_kg.json and kg/doe_kg.cypher.
```

The check is what makes the map trustworthy: no term is in it whose quoted words are not on the line
it cites. For a link the script checks only that the cited line exists, so the links are yours to
read in the next step. When your texts change later, `python kg/build_kg.py . --relocate` follows
each citation to its new line, and lists the terms and links to read again.

### 3. Review it

An AI draft gets most terms and links right and a few subtly wrong, and only someone who knows the
subject can tell which. Ask for a list you can read:

```text
List kg/graph.yaml for my review in kg/review.md: for each file of my texts, one table of its terms
(the name, the definition, the quote) and one of its links (the sentence "A verb B", and the words
of the line it cites). Then name the ten you are least sure of, and say why for each.
```

Then give your corrections in your own words:

```text
Apply these corrections to kg/graph.yaml, then run "python kg/build_kg.py ." until it passes:
- YOUR CORRECTIONS, one per line
```

### 4. Lay it out and view it

`BASE-URL` is where your files can be read. For a repository on GitHub it is
`https://github.com/YOU/REPOSITORY/blob/main/`.

```text
Run "python kg/layout_kg.py", then copy kg/doe_kg_map.json to viewer/map/graph.json.

Then make the viewer mine, in viewer/map.js and viewer/map/index.html:
- The title, the heading, the line under it and the description say "SUBJECT concept map".
- Remove what belongs to the site it came from: the canonical link, the social-card tags, the
  "Back to Factorial" link, and the "How this map was made" guide with its link.
- bookUrl() returns where a term's line can be read: BASE-URL, then the term's file path, then
  "#L" and its line number (a term's "evidence" is PATH:LINE). (Or: no such address exists, so
  remove the "Read it in the book" link.)
- Rename the five kinds of term in FAMILIES to suit my terms, and tell me which of my types falls
  under each.
- The search box's hint names three of my terms.

Start "python -m http.server 8000 --directory viewer". If you can drive a browser, open
http://localhost:8000/map/ and tell me about any error in its console; otherwise tell me to open it.
```

### 5. Compare with another text (optional)

Put the second text at `kg/projections/NAME/text.txt`.

```text
I put a second text at kg/projections/NAME/text.txt. Compare it with my graph:

1. Run "python kg/project_text.py candidates kg/projections/NAME".
2. Judge the candidates as kg/PROJECTION.md says, with SUBJECT as the graph's subject, and write
   kg/projections/NAME/reviews.json.
3. Run "python kg/project_text.py verify kg/projections/NAME", then
   "python kg/project_text.py report kg/projections/NAME".

Show me kg/projections/NAME/report.md. Change nothing in kg/graph.yaml yet.
```

The report lists what the second text supports, where it defines a term differently, the links your
graph lacks, and the terms that are new. Every line carries a short quote that the `verify` step
checked word for word. Decide each one, then:

```text
Here are my decisions on kg/projections/NAME/report.md:
- YOUR DECISIONS, one per item: accept, reword (and how), or reject

Apply them to kg/graph.yaml:
- another name for a term: add it to that term's aliases;
- a definition that differs: reword it as I say, within 32 words;
- a missing link or a new term: add it only with a line of MY texts that states it. If no line
  does, tell me, and suggest the sentence my text would need.

Then run the check and the layout again, and copy the map file to the viewer.
```

**Run this step twice.** The script finds a term in the second text only under a name the graph
already knows, and another author often uses another name. So the first report holds mostly other
names and new terms, and few links. Accept the names, apply them, and run the comparison again: the
second report shows the links the two texts share.

## How well this works

The prompts were tried as written, by an agent that had only this page's prompts and the files:

- **Chapter 1 of this book (data visualization, about 9,500 words).** A graph of 40 terms and 55
  links that passed the check at the first attempt, drawn as 8 topics with no error in the browser.
  The agent's own list of the ten items it was least sure of named real problems: a term the text
  never defines in words, and an everyday word used as another name. Against a short second text,
  the first comparison found one other name, one new term and one definition that differs, and no
  links: hence "run this step twice".
- **Two short notes on baking (8 terms).** The scripts, edited as in step 1, checked every quote,
  caught a wrong one, and followed the citations after the notes were edited.

Steps 1 and 4 ask the agent to edit code, and are the least certain: read what it changed. In the
trial the first versions of those two prompts left gaps the agent had to fill by guessing; the
prompts above name what it had to work out.

## What is specific to this book

| Script | As it is, on other texts | What step 1 or 4 changes |
|---|---|---|
| `build_kg.py` | Stops | The list of chapter folders, and the reading levels, which read this book's table of contents. |
| `layout_kg.py` | Stops | The topic names, which are written out for this book. |
| The map viewer | Draws the map | Its title, its guide, its kinds of term and its "Read it in the book" links. |
| `project_text.py` | Works unchanged | Nothing. |

Other things to know:

- The link verbs (`VERBS`) and the kinds of term (`TYPES`) suit a technical subject. Change the
  lists to suit yours, before step 2.
- By itself, the comparison proposes a new term only when a phrase of two or three words is repeated
  at least three times, or is introduced with words like "called". The reviewer can add others.

If you try this on your own texts, an issue on this repository saying where it broke is welcome.
