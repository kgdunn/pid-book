"""Check that every term's book link lands on its section: each #anchor must exist on the live page.

build_kg.py checks the labels against the book's source; this checks what readers click, on
learnche.org, which is built from a release and can lag the source. It needs the network, so it is
kept out of the build. Each page is fetched once.

Run with: python3 check_anchors.py [doe_kg.json]
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

SITE = "https://learnche.org/pid"
HEADERS = {"User-Agent": "pid-book-knowledge-graph-check"}  # the site refuses Python's default client


def anchor(label: str) -> str:
    """The HTML id Sphinx gives a label: lower case, underscores as hyphens."""
    return label.lower().replace("_", "-")


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "doe_kg.json"
    nodes = json.loads(path.read_text(encoding="utf-8"))["nodes"]
    ids_on, problems = {}, []
    for n in nodes:
        page = n["book_file"].removesuffix(".rst")
        if page not in ids_on:
            try:
                with urllib.request.urlopen(urllib.request.Request(f"{SITE}/{page}", headers=HEADERS), timeout=30) as r:
                    ids_on[page] = set(re.findall(r'\bid="([^"]+)"', r.read().decode("utf-8", "replace")))
            except OSError as e:
                ids_on[page] = None
                problems.append(f"{page}: not fetched ({e})")
        if ids_on[page] is not None and n["book_label"] and anchor(n["book_label"]) not in ids_on[page]:
            problems.append(f"{n['id']}: #{anchor(n['book_label'])} is not on {SITE}/{page}")
    print(f"{len(nodes)} terms, {len(ids_on)} pages, {len(problems)} problems")
    for p in problems:
        print("  -", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
