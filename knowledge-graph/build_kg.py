"""Check graph.yaml against the book, then write doe_kg.json and doe_kg.cypher.

graph.yaml is the source. Every term cites pid-book (evidence file:line, and a quote that must
appear on that line), and so does most of the links. The build checks all of it and stops with
the full list of problems, so the graph cannot drift from the book unnoticed.

Run with: python3 build_kg.py [--relocate] [path-to-pid-book]
(the default is this repository; build against a checkout of main, since the links point at the current book)

The book moves under the graph: a paragraph added near the top of a file shifts every line below it.
graph.yaml records the book commit it was last checked against (checked_against), and the build maps
each citation from that commit to the book as it is now, with git and a line diff, so moved lines need
nothing. A term whose cited line was rewritten is found again by its quote, anywhere in its file; a
link has no quote, so a link whose cited line was rewritten is listed for a person to check. A term
whose quote is gone from the book stops the build. --relocate writes the new line numbers, and the
book's current commit, back into graph.yaml.
"""

import difflib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).parent
ARGS = [a for a in sys.argv[1:] if a != "--relocate"]
RELOCATE = "--relocate" in sys.argv[1:]
BOOK = Path(ARGS[0]) if ARGS else HERE.parent
# The book's chapters in table-of-contents order (contents.rst): the position is the chapter number.
CHAPTERS = ["data-visualization", "univariate-review", "process-monitoring", "least-squares-modelling",
            "design-analysis-experiments", "latent-variable-modelling", "product-development-product-improvement"]
TYPES = {"Concept", "Method", "DesignType", "Property", "Criterion", "Plot", "Phase", "Guideline", "Diagnostic",
         "Example", "Question", "Reference"}
# Each verb reads "source VERB target"; template.html says how each reads in both directions.
VERBS = {
    "IS_A", "PART_OF", "HAS_PROPERTY", "USES", "REQUIRES", "JUSTIFIES", "ESTIMATES", "MEASURES", "SHOWS",
    "LOCATES", "TESTS", "CAUSES", "ENABLES", "LIMITS", "PREVENTS", "KEEPS", "REMEDIED_BY", "INDICATES",
    "AGREES_WITH", "CONTRASTS_WITH", "ALTERNATIVE_TO", "COMPLEMENTS", "GENERALIZES", "CAN_AUGMENT_TO", "CAN_BE",
    "SUITED_TO", "APPLIES_TO", "PRECEDES", "ILLUSTRATES", "ANSWERED_BY", "DESCRIBED_IN", "CANNOT_SHOW",
    "EQUALS", "IS_HALF_OF", "MAY_HAVE",
}
MAX_WORDS = 32
EM_DASH = "—"
lines_of: dict[str, list[str]] = {}


def book_labels() -> dict[str, str]:
    """Map every RST label in the book's chapters to the file that defines it."""
    found = {}
    for chapter in CHAPTERS:
        for rst in (BOOK / chapter).rglob("*.rst"):
            for label in re.findall(r"^\.\. _([^:]+):", rst.read_text(encoding="utf-8"), flags=re.M):
                found[label] = str(rst.relative_to(BOOK))
    return found


def book_line(evidence: str) -> tuple[list[str], int] | None:
    """The lines of the cited file and the 0-based index cited, or None when either does not exist."""
    path, _, num = evidence.rpartition(":")
    if not num.isdigit() or not (BOOK / path).is_file():
        return None
    if path not in lines_of:
        lines_of[path] = (BOOK / path).read_text(encoding="utf-8").splitlines()
    i = int(num) - 1
    return (lines_of[path], i) if 0 <= i < len(lines_of[path]) else None


def quote_found(evidence: str, quote: str) -> bool:
    """True when the quote is on the cited line, or straddles it and a neighbour (RST wraps lines)."""
    found = book_line(evidence)
    if found is None:
        return False
    lines, i = found
    squash = lambda s: " ".join(s.split())
    return squash(quote) in squash(" ".join(lines[max(0, i - 1): i + 2]))


def git(*args: str) -> str | None:
    """Run git in the book's checkout: its output, or None when that fails (no checkout, or an unknown commit)."""
    done = subprocess.run(["git", "-C", str(BOOK), *args], capture_output=True, text=True, check=False)
    return done.stdout if done.returncode == 0 else None


def line_maps(rev: str, paths: set[str]) -> dict[str, dict[int, int]] | None:
    """For each cited file changed since rev, where each of its lines then (1-based) is now; a rewritten line is absent."""
    changed = git("diff", "--name-only", rev, "--", *sorted(paths))
    if changed is None:
        return None
    maps = {}
    for path in changed.split():
        old = git("show", f"{rev}:{path}")
        if old is None or not (BOOK / path).is_file():
            continue
        new = (BOOK / path).read_text(encoding="utf-8").splitlines()
        blocks = difflib.SequenceMatcher(None, old.splitlines(), new, autojunk=False).get_matching_blocks()
        maps[path] = {a + k + 1: b + k + 1 for a, b, size in blocks for k in range(size)}
    return maps


def find_quote(evidence: str, quote: str) -> str | None:
    """The quote's line anywhere in the cited file, as file:line, when it is there once; else None."""
    path = evidence.rpartition(":")[0]
    found = book_line(f"{path}:1")
    hits = [i for i in range(len(found[0]))] if found else []
    hits = [i for i in hits if quote_found(f"{path}:{i + 1}", quote)]
    # A quote on one line is in three windows (the line and its neighbours); one over two lines, in two.
    return f"{path}:{hits[len(hits) // 2] + 1}" if hits and hits[-1] - hits[0] <= 2 else None


def follow_the_book(graph: dict) -> tuple[int, list[str], str | None]:
    """Move every citation to where its line is now; return how many moved, the links to check, and the book's commit."""
    rev = graph.get("checked_against")
    head = (git("rev-parse", "HEAD") or "").strip() or None
    cites = [n["evidence"] for n in graph["nodes"]] + [e[3] for e in graph["edges"]]
    maps = line_maps(rev, {c.rpartition(":")[0] for c in cites}) if rev else None
    if maps is None:
        return 0, [], head
    moved, recheck = 0, []

    def follow(evidence: str) -> str | None:
        path, _, num = evidence.rpartition(":")
        if path not in maps:
            return evidence
        line = maps[path].get(int(num))
        return f"{path}:{line}" if line else None

    for n in graph["nodes"]:
        now = follow(n["evidence"])
        if now is None or not quote_found(now, n["quote"]):
            now = find_quote(n["evidence"], n["quote"]) or n["evidence"]
        moved += now != n["evidence"]
        n["evidence"] = now
    for e in graph["edges"]:
        now = follow(e[3])
        if now is None:
            recheck.append(f"link {e[0]} {e[1]} {e[2]}: its line at {e[3]} was rewritten; check it still says so")
            continue
        moved += now != e[3]
        e[3] = now
    return moved, recheck, head


def write_back(graph: dict, head: str | None) -> None:
    """Put each citation's new line, and the book's commit, into graph.yaml, leaving the rest of the file as it is."""
    text = (HERE / "graph.yaml").read_text(encoding="utf-8")
    terms = iter(n["evidence"] for n in graph["nodes"])
    text = re.sub(r"(?m)^(  evidence: ).*$", lambda m: m[1] + next(terms), text)
    links = iter(e[3] for e in graph["edges"])
    text = re.sub(r'(?m)^(- \[[^\]]*, ")[^"]+("\])$', lambda m: m[1] + next(links) + m[2], text)
    if head:
        text = re.sub(r"(?m)^checked_against: .*$", f"checked_against: {head}", text)
    (HERE / "graph.yaml").write_text(text, encoding="utf-8")


def check(graph: dict, labels: dict[str, str]) -> list[str]:
    """Every problem in graph.yaml, as one line each."""
    problems = []
    nodes, edges = graph["nodes"], graph["edges"]
    ids = Counter(n["id"] for n in nodes)
    problems += [f"duplicate id {i}" for i, c in ids.items() if c > 1]
    for n in nodes:
        where = f"term {n['id']}"
        if n["type"] not in TYPES:
            problems.append(f"{where}: unknown type {n['type']}")
        if len(n["definition"].split()) > MAX_WORDS:
            problems.append(f"{where}: definition longer than {MAX_WORDS} words")
        if any(EM_DASH in s for s in (n["name"], n["definition"], *n["aliases"])):
            problems.append(f"{where}: em-dash")
        ref = n["book_label"]
        if ref.startswith("file:") and not (BOOK / ref[5:]).is_file() or not ref.startswith("file:") and ref not in labels:
            problems.append(f"{where}: book reference {ref} does not resolve")
        if not quote_found(n.get("evidence", ""), n.get("quote", "")):
            problems.append(f"{where}: quote not found at {n.get('evidence') or '(no evidence)'}")
    seen = Counter()
    for e in edges:
        s, r, t, *rest = e
        where = f"link {s} {r} {t}"
        seen[(s, r, t)] += 1
        if s not in ids or t not in ids:
            problems.append(f"{where}: unknown term")
        if r not in VERBS:
            problems.append(f"{where}: unknown verb")
        if s == t:
            problems.append(f"{where}: links a term to itself")
        if rest and rest[0] and book_line(rest[0]) is None:
            problems.append(f"{where}: evidence {rest[0]} does not exist")
    problems += [f"duplicate link {k}" for k, c in seen.items() if c > 1]
    linked = {e[0] for e in edges} | {e[2] for e in edges}
    problems += [f"term {i} has no links" for i in ids if i not in linked]
    return problems


def main() -> None:
    graph = yaml.safe_load((HERE / "graph.yaml").read_text(encoding="utf-8"))
    labels = book_labels()
    moved, recheck, head = follow_the_book(graph)
    problems = check(graph, labels)
    if problems:
        sys.exit(f"{len(problems)} problems in graph.yaml, checked against {BOOK}:\n  " + "\n  ".join(problems))
    if moved:
        print(f"{moved} citations moved with the book" + ("; written to graph.yaml" if RELOCATE else
              "; run with --relocate to write them to graph.yaml"))
    for line in recheck:
        print(f"check: {line}")
    if RELOCATE:
        write_back(graph, head)

    nodes = []
    for n in graph["nodes"]:
        ref = n["book_label"]
        label, path = (None, ref[5:]) if ref.startswith("file:") else (ref, labels[ref])
        nodes.append({**n, "book_label": label, "book_file": path, "chapter": CHAPTERS.index(path.split("/")[0]) + 1})
    edges = [{"source": s, "type": r, "target": t, "evidence": rest[0] if rest else ""} for s, r, t, *rest in graph["edges"]]
    (HERE / "doe_kg.json").write_text(json.dumps({"nodes": nodes, "edges": edges}, indent=1), encoding="utf-8")

    q = lambda v: "null" if v is None else json.dumps(v)
    lines = ["// Built from graph.yaml by build_kg.py. Load into an empty database.",
             "CREATE CONSTRAINT term_id IF NOT EXISTS FOR (n:Term) REQUIRE n.id IS UNIQUE;"]
    for n in nodes:
        props = ", ".join(f"{k}: {q(n[k])}" for k in ("id", "name", "definition", "aliases", "book_label", "book_file",
                                                       "chapter", "evidence", "quote"))
        lines.append(f"CREATE (:Term:{n['type']} {{{props}}});")
    for e in edges:
        lines.append(f"MATCH (a:Term {{id: {q(e['source'])}}}), (b:Term {{id: {q(e['target'])}}}) "
                     f"CREATE (a)-[:{e['type']} {{evidence: {q(e['evidence'])}}}]->(b);")
    (HERE / "doe_kg.cypher").write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_chapter = Counter(n["chapter"] for n in nodes)
    cited = sum(1 for e in edges if e["evidence"])
    print(f"{len(nodes)} terms, {len(edges)} links ({cited} with evidence), {len({e['type'] for e in edges})} verbs")
    print("terms by chapter:", dict(sorted(by_chapter.items())))
    print("checks passed: every quote on its line, every book reference resolves, no orphans")


if __name__ == "__main__":
    main()
