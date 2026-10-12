"""Check every Factorial link the book prints: the app opens each name, and links back to its page.

``:factorial:`name``` (my-extensions/factorial_link.py) links to https://factori.al/#book=<name>.
The app publishes its examples in ``book/index.json``: each name, its title, and the page of the
book it links back to ("Read it in the book"). This script reads every ``.rst`` file and fails
when a name the book uses is not published, or when the page the app links back to does not use
that name, or names an anchor the page does not have. The app is deployed from process-improve's
main branch, so a new name reaches factori.al before the book can link to it.

    make check-factorial-links                                       # against https://factori.al/
    uv run python tools/check_factorial_links.py --index dist/web-app/book/index.json
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from docutils.nodes import make_id

ROOT = Path(__file__).resolve().parents[1]
INDEX = "https://factori.al/book/index.json"
BOOK = "https://learnche.org/pid/"

#: ``:factorial:`name``` or ``:factorial:`text <name>```; the name is the last word before the backtick.
ROLE = re.compile(r":factorial:`(?:[^`<]*<)?([^`<>]+?)>?`")
#: A label, ``.. _DOE-lenth-method:``, whose anchor is ``doe-lenth-method``.
LABEL = re.compile(r"^\s*\.\. _([^:]+):\s*$", re.MULTILINE)
#: A section title: a line of text underlined by a line of one repeated punctuation character.
TITLE = re.compile(r"^(\S.*)\n([=\-~^\"'`#*+.:])\2{3,}\s*$", re.MULTILINE)
SKIP = {"_build", "figures", "figures-src", ".venv", "node_modules"}


def pages(root: Path = ROOT) -> dict[str, str]:
    """Return the text of every page of the book, by its path without ``.rst``: its address under the book."""
    found = {}
    for path in sorted(root.rglob("*.rst")):
        relative = path.relative_to(root)
        if not SKIP.intersection(relative.parts):
            found[relative.with_suffix("").as_posix()] = path.read_text(encoding="utf-8")
    return found


def uses(book: dict[str, str]) -> dict[str, set[str]]:
    """Return each name the book links to in Factorial, with the pages that link to it."""
    found: dict[str, set[str]] = {}
    for page, text in book.items():
        for name in ROLE.findall(text):
            found.setdefault(name.strip(), set()).add(page)
    return found


def anchors(text: str) -> set[str]:
    """Return the anchors a page has: one per label, and one per section title, as docutils names them."""
    return {make_id(label) for label in LABEL.findall(text)} | {
        make_id(t) for t, _ in TITLE.findall(text)
    }


def problems(book: dict[str, str], index: dict) -> list[str]:
    """Say what is wrong with the book's Factorial links, given the app's index; nothing when all is well."""
    published = {example["name"]: example for example in index["examples"]}
    found = []
    for name, used_on in sorted(uses(book).items()):
        where = ", ".join(sorted(used_on))
        if name not in published:
            found.append(f"{name!r} ({where}): Factorial publishes no example by this name")
            continue
        back = published[name]["book"]
        page, _, anchor = back.removeprefix(BOOK).partition("#")
        if not back.startswith(BOOK) or page not in used_on:
            found.append(
                f"{name!r} ({where}): Factorial links back to {back}, a page that does not use it"
            )
        elif anchor and anchor not in anchors(book[page]):
            found.append(
                f"{name!r} ({where}): Factorial links back to #{anchor}, which {page}.rst has no label for"
            )
    return found


def read_index(source: str) -> dict:
    """Read the app's index from its address, or from a file of a local build."""
    if source.startswith("https://"):
        try:
            with urllib.request.urlopen(source, timeout=30) as response:
                return json.load(response)
        except (urllib.error.URLError, json.JSONDecodeError) as error:
            raise SystemExit(
                f"Could not read Factorial's index of the book's examples, {source}: {error}"
            ) from error
    return json.loads(Path(source).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--index", default=INDEX, help="the app's book/index.json: an https address or a file"
    )
    args = parser.parse_args()
    book = pages()
    found = problems(book, read_index(args.index))
    for problem in found:
        print(problem, file=sys.stderr)
    used = uses(book)
    print(f"{len(used)} names, {sum(map(len, used.values()))} pages: {len(found)} problems")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
