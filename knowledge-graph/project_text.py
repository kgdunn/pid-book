"""Project another text onto the graph: which terms it uses, which links it supports, and what it adds.

Three steps, each a subcommand; everything they read and write sits in a folder of projections/, which git
ignores, because the text is usually someone else's copyright:

candidates  Reads the text (a PDF's text from pdftotext, pages split by form feeds) and graph.yaml, and writes
            candidates.json: each term the text names (by name or alias), each link whose two terms share a
            sentence or two adjacent ones, the pairs of terms that share sentences with no link between them,
            and the phrases the text defines or repeats that match no term. This step only finds things.
verify      Reads reviews.json, the reviewers' verdicts on those candidates (PROJECTION.md is their brief),
            and checks every quote word for word against the text; a verdict whose quote is not there is
            dropped and listed.
report      Writes report.md from the verified verdicts: the links the text supports, the places it
            disagrees with the graph, and the few terms that are truly new.
unify       Merges the verified verdicts of several projections into projections/review.md: each item
            once, with every place that supports it, for one review.

Run, from this folder:
  pdftotext book.pdf projections/NAME/text.txt
  uv run --no-project --with pyyaml==6.0.1 python -I project_text.py candidates projections/NAME --pages 18-45
  (reviewers write projections/NAME/reviews.json)
  uv run --no-project --with pyyaml==6.0.1 python -I project_text.py verify projections/NAME
  uv run --no-project --with pyyaml==6.0.1 python -I project_text.py report projections/NAME
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STOP = set("""a an and are as at be been by can could do does each for from has have how if in into is it its may
more most must no not of on one or other our such than that the their them then there these this those to two
under use used using was we were what when where which while who will with would also only same some any all
both between however therefore thus very much many first second further given see shown shall figure figures
table tables chapter chapters section even""".split())
# A sentence that may say what a term is: "X is a ...", "by X we mean", "X, that is, ...".
DEFINING = re.compile(r"\b(?:is|are) (?:a|an|the|called|defined)\b|\bwe (?:mean|call|define)\b|\bthat is\b|\bi\.e\.",
                      re.IGNORECASE)
QUOTE_WORDS = 25  # a quote stays a short citation of someone else's text, never a passage


# ---------- the text, as sentences with their page


def read_pages(folder: Path, pages: str | None) -> list[tuple[str, str]]:
    """Return (page label, text) for each page: the printed page number when the page shows one."""
    raw = (folder / "text.txt").read_text(encoding="utf-8").split("\f")
    first, last = (int(p) for p in pages.split("-")) if pages else (1, len(raw))
    out = []
    for index in range(first, last + 1):
        lines = [line.strip() for line in raw[index - 1].splitlines() if line.strip()]
        label = f"pdf {index}"
        # Running heads are a short capitalised title and the page number, in either order: drop them.
        while lines and (lines[0].isdigit() or (lines[0].isupper() and len(lines[0]) < 80)):
            if lines[0].isdigit():
                label = f"p. {lines[0]}"
            lines.pop(0)
        out.append((label, "\n".join(lines)))
    return out


def sentences_of(pages: list[tuple[str, str]]) -> list[dict]:
    """Split each page into sentences, joining words broken across lines (most line-end hyphens are breaks)."""
    out = []
    for label, text in pages:
        flat = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
        flat = re.sub(r"\s+", " ", flat).strip()
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z(])", flat):
            if len(sentence.split()) >= 4:
                out.append({"page": label, "text": sentence})
    return out


# ---------- the graph's terms, found in the text


def term_patterns(nodes: list[dict]) -> list[tuple[str, re.Pattern]]:
    """A (term, pattern) per name and alias, longest name first: case, plural and hyphen-or-space do not matter.

    Longest first, so a sentence that says "response surface" names that term and not also "response"."""
    names = [(n["id"], name) for n in nodes for name in [n["name"], *(n.get("aliases") or [])]
             if len(name) >= 4 or name.isupper()]  # "y", "X": too short to find in prose
    out = []
    for term, name in sorted(names, key=lambda tn: -len(tn[1])):
        words = [re.escape(w) for w in re.split(r"[\s-]+", name.strip())]
        out.append((term, re.compile(r"\b" + r"[\s-]+".join(words) + r"(?:s|es)?\b", re.IGNORECASE)))
    return out


def name_terms(text: str, patterns: list[tuple[str, re.Pattern]]) -> tuple[list[str], str]:
    """The terms a text names, and the text with each mention blanked out."""
    named = set()
    for term, pattern in patterns:
        text, n = pattern.subn(" | ", text)
        if n:
            named.add(term)
    return sorted(named), text


def candidates(folder: Path, pages: str | None) -> None:
    graph = yaml.safe_load((HERE / "graph.yaml").read_text(encoding="utf-8"))
    sentences = sentences_of(read_pages(folder, pages))
    patterns = term_patterns(graph["nodes"])
    named = {n["id"]: n["name"] for n in graph["nodes"]}
    meaning = {n["id"]: n["definition"] for n in graph["nodes"]}
    found: dict[str, list[int]] = {}
    for i, s in enumerate(sentences):
        s["terms"], s["rest"] = name_terms(s["text"], patterns)
        for t in s["terms"]:
            found.setdefault(t, []).append(i)

    def near(a: str, b: str) -> list[int]:
        """Sentences naming both terms, or the first of two adjacent sentences that name one each."""
        hits = [i for i in found.get(a, []) if b in sentences[i]["terms"]]
        hits += [i for i in found.get(a, []) if i + 1 < len(sentences) and b in sentences[i + 1]["terms"]]
        hits += [i for i in found.get(b, []) if i + 1 < len(sentences) and a in sentences[i + 1]["terms"]]
        return sorted(set(hits))

    def cite(i: int, both: bool = False) -> dict:
        text = sentences[i]["text"] + (" " + sentences[i + 1]["text"] if both and i + 1 < len(sentences) else "")
        return {"page": sentences[i]["page"], "text": text}

    links, linked = [], set()
    for source, verb, target, _ in graph["edges"]:
        linked |= {(source, target), (target, source)}
        hits = near(source, target)
        if hits:
            links.append({"link": [source, verb, target], "sentences": [cite(i, both=True) for i in hits[:6]]})

    pairs = Counter()
    for s in sentences:
        for k, a in enumerate(s["terms"]):
            for b in s["terms"][k + 1 :]:
                if (a, b) not in linked:
                    pairs[a, b] += 1
    unlinked = [
        {"pair": [a, b], "names": [named[a], named[b]], "times": n,
         "sentences": [cite(i) for i in found[a] if b in sentences[i]["terms"]][:4]}
        for (a, b), n in pairs.most_common() if n >= 2
    ]

    out = {
        "sentences": len(sentences),
        "terms": [{"term": t, "name": named[t], "times": len(ix), "pages": sorted({sentences[i]["page"] for i in ix}),
                   "graph_says": meaning[t],
                   "defining": [cite(i) for i in ix if DEFINING.search(sentences[i]["text"])][:3]}
                  for t, ix in sorted(found.items(), key=lambda kv: -len(kv[1]))],
        "links": links,
        "unlinked": unlinked,
        "unknown": unknown_phrases(sentences),
    }
    (folder / "candidates.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    # Every term in one line each, for reviewers who judge an alias or a new term against the whole graph.
    index = [f"{n['id']} | {n['name']} | {', '.join(n.get('aliases') or [])} | {n['definition']}" for n in graph["nodes"]]
    (folder.parent / "graph-terms.txt").write_text("id | name | other names | definition\n" + "\n".join(index) + "\n",
                                                   encoding="utf-8")
    print(f"{len(sentences)} sentences; {len(found)} of {len(named)} terms named; "
          f"{len(links)} of {len(graph['edges'])} links with sentences to read; "
          f"{len(unlinked)} unlinked pairs named together at least twice; {len(out['unknown'])} phrases to judge")


def unknown_phrases(sentences: list[dict]) -> list[dict]:
    """Phrases that match no term: those the text defines ("called X"), and those it repeats at least three times."""
    defined = re.compile(r"\b(?:called|termed|known as|referred to as|we call|defined as)\s+(?:an?\s+|the\s+)?"
                         r"([a-z][\w-]*(?:\s+[a-z][\w-]*){0,3})", re.IGNORECASE)
    counts, where, definitions = Counter(), {}, set()
    for i, s in enumerate(sentences):
        text = s["rest"]  # a known term is never part of an unknown phrase
        for m in defined.finditer(text):
            phrase = " ".join(w for w in m.group(1).lower().split() if w not in STOP)
            if len(phrase) >= 4:
                definitions.add(phrase)
                where.setdefault(phrase, i)
        words = re.findall(r"[a-z][a-z-]+|\|", text.lower())
        for n in (2, 3):
            for k in range(len(words) - n + 1):
                gram = words[k : k + n]
                if "|" in gram or gram[0] in STOP or gram[-1] in STOP:
                    continue
                phrase = " ".join(gram)
                counts[phrase] += 1
                where.setdefault(phrase, i)
    keep = {p for p, n in counts.items() if n >= 3} | definitions
    return [{"phrase": p, "times": counts[p], "defined": p in definitions,
             "page": sentences[where[p]]["page"], "text": sentences[where[p]]["text"]}
            for p in sorted(keep, key=lambda p: (-(p in definitions), -counts[p]))]


# ---------- the reviewers' verdicts, checked, then reported


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)).strip().lower()


def verify(folder: Path) -> None:
    text = squash((folder / "text.txt").read_text(encoding="utf-8"))
    reviews = json.loads((folder / "reviews.json").read_text(encoding="utf-8"))
    kept, dropped = [], []
    for v in reviews:
        quote = v.get("quote", "")
        if quote and len(quote.split()) <= QUOTE_WORDS and squash(quote) in text:
            kept.append(v)
        else:
            dropped.append(v)
    (folder / "verified.json").write_text(json.dumps(kept, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(kept)} verdicts kept, {len(dropped)} dropped (quote missing, too long, or not in the text)")
    for v in dropped:
        print("  dropped:", v.get("kind"), v.get("item"), "|", v.get("quote", "")[:80])


def report(folder: Path) -> None:
    verdicts = json.loads((folder / "verified.json").read_text(encoding="utf-8"))
    graph = yaml.safe_load((HERE / "graph.yaml").read_text(encoding="utf-8"))
    named = {n["id"]: n["name"] for n in graph["nodes"]}
    found = json.loads((folder / "candidates.json").read_text(encoding="utf-8"))["terms"]

    def label(item: list | str) -> str:
        return " ".join(named.get(w, w.replace("_", " ").lower()) for w in item) if isinstance(item, list) else item

    def rows(kind: str, verdict: str) -> list[str]:
        return [f"| {label(v['item'])} | {v['page']} | \"{v['quote']}\" | {v.get('note', '')} |"
                for v in verdicts if v["kind"] == kind and v["verdict"] == verdict]

    head = "| Item | Page | The text says | Note |\n|---|---|---|---|"
    sections = [
        ("Links the text supports", rows("link", "supports")),
        ("Links the text contradicts", rows("link", "contradicts")),
        ("Definitions that differ", rows("definition", "differs")),
        ("Links the graph is missing", rows("pair", "missing_link")),
        ("New terms, truly new", rows("unknown", "new_term")),
        ("Other names for terms already in the graph", rows("unknown", "alias")),
    ]
    lines = [f"# Projection of {folder.name} onto the graph", "",
             f"{len(found)} of {len(named)} terms are named in the text; the most often: "
             + ", ".join(f"{t['name']} ({t['times']})" for t in found[:12]) + ".", ""]
    for title, body in sections:
        lines += [f"## {title} ({len(body)})", ""] + ([head, *body] if body else ["None."]) + [""]
    (folder / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", folder / "report.md", "|", "; ".join(f"{t}: {len(b)}" for t, b in sections))


def unify(folders: list[Path]) -> None:
    """One list for a single review: every verified verdict of every projection, grouped by item, most cited first."""
    groups: dict[tuple, list[dict]] = {}
    for folder in folders:
        for v in json.loads((folder / "verified.json").read_text(encoding="utf-8")):
            item = v["item"] if v["kind"] != "unknown" else v["item"].lower()
            key = (v["kind"], v["verdict"], json.dumps(item))
            groups.setdefault(key, []).append({**v, "source": folder.name})
    order = ["new_term", "differs", "contradicts", "missing_link", "alias", "supports"]
    title = {"new_term": "New terms", "differs": "Definitions that differ", "contradicts": "Links contradicted",
             "missing_link": "Links the graph is missing", "alias": "Other names for existing terms",
             "supports": "Links supported"}
    lines = [f"# One review: {len(folders)} projections, {sum(map(len, groups.values()))} verdicts", "",
             "Each item once, with every place that supports it. Decide each: accept, reword, or reject.", ""]
    for verdict in order:
        items = sorted(((k, vs) for k, vs in groups.items() if k[1] == verdict), key=lambda kv: -len(kv[1]))
        lines += [f"## {title[verdict]} ({len(items)})", ""]
        for (_, _, item), vs in items:
            lines.append(f"- [ ] **{', '.join(json.loads(item)) if item.startswith('[') else json.loads(item)}**"
                         f" ({len(vs)} place{'s' if len(vs) > 1 else ''})")
            for v in vs:
                lines.append(f"  - {v['source']}, {v['page']}: {v.get('note', '')} *\"{v['quote']}\"*")
        lines.append("")
    out = folders[0].parent / "review.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", out, "|", "; ".join(f"{title[o]}: {sum(1 for k in groups if k[1] == o)}" for o in order))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("step", choices=["candidates", "verify", "report", "unify"])
    parser.add_argument("folder", type=Path, nargs="+", help="a folder of projections/ holding text.txt (unify: several)")
    parser.add_argument("--pages", help="the PDF pages to read, for example 18-45 (default: all)")
    args = parser.parse_args()
    if args.step == "unify":
        unify(args.folder)
    elif args.step == "candidates":
        candidates(args.folder[0], args.pages)
    elif args.step == "verify":
        verify(args.folder[0])
    else:
        report(args.folder[0])


if __name__ == "__main__":
    main()
