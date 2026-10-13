"""Links to the book's examples in Factorial (my-extensions/factorial_link.py, tools/check_factorial_links.py).

``:factorial:`name``` must render as a link to https://factori.al/?book=<name> in the HTML and,
through ``latex_show_urls``, as a footnote with that address in the PDF. The checker must find
every name the book uses, and say when the app does not publish it or links back elsewhere.
"""

import importlib
import re
import sys
from pathlib import Path

import pytest
from check_factorial_links import anchors, problems, uses
from sphinx.cmd.build import build_main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
factorial_link = importlib.import_module("my-extensions.factorial_link")

PAGE = """\
Pollutant
=========

.. _DOE-exercise-pollutant:

The runs open in :factorial:`pollutant`, or with :factorial:`their purity <multi-response-purity>`.
`Factorial <https://factori.al/>`__, the designed-experiments app, builds a design from scratch.
"""


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> dict[str, str]:
    """Build a one-page book with the role, as HTML, LaTeX and text, and return each page's text."""
    src = tmp_path_factory.mktemp("src")
    (src / "conf.py").write_text(
        f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
        "extensions = ['my-extensions.factorial_link']\n"
        "latex_show_urls = 'footnote'\n"
        "latex_documents = [('index', 'book.tex', 'Book', 'Author', 'manual')]\n"
    )
    (src / "index.rst").write_text(PAGE)
    out = tmp_path_factory.mktemp("out")
    found = {}
    for builder, name in (("html", "index.html"), ("latex", "book.tex"), ("text", "index.txt")):
        assert build_main(["-b", builder, "-W", "-q", str(src), str(out / builder)]) == 0, builder
        found[builder] = (out / builder / name).read_text(encoding="utf-8")
    return found


def test_the_link_opens_the_example_by_name(built):
    html = built["html"]
    assert 'href="https://factori.al/?book=pollutant" target="factorial">Factorial</a>' in html
    assert (
        'href="https://factori.al/?book=multi-response-purity" target="factorial">their purity</a>'
        in html
    )
    assert "factorial-link" in html


def test_every_link_to_factorial_opens_in_its_one_tab(built):
    """The first click opens the tab, the next reuses it: one tab of the app beside the book."""
    html = built["html"]
    links = re.findall(r'<a [^>]*href="https://factori\.al/[^"]*"[^>]*>', html)
    assert len(links) == 3, "the role's two and the one written out"
    assert all('target="factorial"' in link for link in links), links
    assert not any("noopener" in link for link in links), (
        "the opener is what lets the next click find the tab"
    )


def test_the_pdf_prints_the_address_as_a_footnote(built):
    tex = built["latex"]
    assert r"\sphinxhref{https://factori.al/?book=pollutant}{Factorial}" in tex
    assert r"\sphinxnolinkurl{https://factori.al/?book=pollutant}" in tex, (
        "the footnote a reader can type"
    )


def test_a_name_the_app_could_not_open_fails_the_build(tmp_path):
    (tmp_path / "conf.py").write_text(
        f"import sys\nsys.path.insert(0, {str(ROOT)!r})\nextensions = ['my-extensions.factorial_link']\n"
    )
    (tmp_path / "index.rst").write_text("Page\n====\n\nSee :factorial:`../demo`.\n")
    assert build_main(["-b", "html", "-W", "-q", str(tmp_path), str(tmp_path / "out")]) != 0


def test_the_role_s_names_are_the_app_s():
    """The app refuses a name that is not lowercase words and numbers joined by hyphens; so does the role."""
    assert factorial_link.NAME.fullmatch("breaded-chicken-half-fraction")
    for name in ("Pollutant", "a--b", "-a", "a_b", "a/b"):
        assert not factorial_link.NAME.fullmatch(name), name
    assert factorial_link.example_url("pollutant") == "https://factori.al/?book=pollutant"


def test_the_link_has_no_fragment_for_the_theme_to_read():
    """On a page without sections the theme's scroll-spy reads every link's fragment as a CSS selector.

    ``#book=web-sales`` is no selector, and the exercises page threw; the name rides in the query.
    """
    assert "#" not in factorial_link.example_url("web-sales")


# --------------------------------------------------------------------------- the checker
BOOK = {
    "design-analysis-experiments/exercises": PAGE,
    "design-analysis-experiments/other": "Other\n=====\n\nAgain in :factorial:`pollutant`.\n",
}


def index(*examples: tuple[str, str]) -> dict:
    """An index as the app publishes it: each example's name and the page it links back to."""
    return {
        "examples": [
            {"name": n, "title": n, "book": f"https://learnche.org/pid/{b}"} for n, b in examples
        ]
    }


def test_every_name_the_book_uses_is_found_with_its_pages():
    assert uses(BOOK) == {
        "pollutant": {"design-analysis-experiments/exercises", "design-analysis-experiments/other"},
        "multi-response-purity": {"design-analysis-experiments/exercises"},
    }


def test_a_page_s_anchors_are_its_labels_and_section_titles():
    assert anchors(PAGE) == {"doe-exercise-pollutant", "pollutant"}


def test_links_the_app_publishes_and_links_back_from_pass():
    published = index(
        ("pollutant", "design-analysis-experiments/exercises#doe-exercise-pollutant"),
        ("multi-response-purity", "design-analysis-experiments/exercises"),
    )
    assert problems(BOOK, published) == []


def test_a_name_the_app_does_not_publish_is_reported():
    published = index(("pollutant", "design-analysis-experiments/other"))
    assert problems(BOOK, published) == [
        "'multi-response-purity' (design-analysis-experiments/exercises): "
        "Factorial publishes no example by this name"
    ]


def test_a_link_back_to_the_wrong_page_or_anchor_is_reported():
    published = index(
        ("pollutant", "design-analysis-experiments/exercises#doe-exercise-chicken"),
        ("multi-response-purity", "design-analysis-experiments/other"),
    )
    found = problems(BOOK, published)
    assert len(found) == 2
    assert "links back to https://learnche.org/pid/design-analysis-experiments/other" in found[0]
    assert (
        "#doe-exercise-chicken, which design-analysis-experiments/exercises.rst has no label"
        in found[1]
    )
