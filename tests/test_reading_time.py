"""The per-page reading-time estimate (my-extensions/reading_time.py).

The estimate is invisible until it is wrong: a page still builds, and still
shows a number, if a docutils or Sphinx upgrade renames the node type that
this module keys off. These tests pin the parts that would fail silently:
what counts as prose, what is skipped, and what a non-prose element adds.

Doctrees are assembled by hand rather than parsed from RST, so the tests
stay fast and depend only on the node classes themselves.
"""

import importlib
import sys
from pathlib import Path

import pytest
from docutils import nodes
from sphinx import addnodes

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
reading_time = importlib.import_module("my-extensions.reading_time")

WPM = 150
COSTS = reading_time.DEFAULT_COSTS


def page(*children):
    """A document holding one paragraph-level child per argument."""
    document = nodes.document(None, None)
    document += list(children)
    return document


def prose(word_count):
    return nodes.paragraph("", "", nodes.Text(" ".join(["word"] * word_count)))


def estimate(*children, min_words=50):
    return reading_time.estimate(page(*children), WPM, COSTS, min_words)


def test_prose_alone_is_words_over_the_rate():
    # 300 words at 150 wpm is two minutes exactly.
    assert estimate(prose(300)) == {"minutes": 2, "words": 300, "videos": 0}


def test_short_page_gets_no_estimate():
    assert estimate(prose(49)) is None


def test_never_reports_less_than_one_minute():
    assert estimate(prose(50))["minutes"] == 1  # 20 seconds of prose rounds to 0


@pytest.mark.parametrize(
    ("extra", "seconds"),
    [
        (nodes.math_block("", "y = mx + c"), COSTS["display_math"]),
        (nodes.image(uri="figure.png"), COSTS["images"]),
        (nodes.literal_block("", "a\nb\nc"), 3 * COSTS["code_lines"]),
    ],
)
def test_non_prose_elements_add_their_own_cost(extra, seconds):
    # 450 words is 3 minutes of prose; the element pushes it past 3.5.
    words = round((3.5 * 60 - seconds) / 60 * WPM) + 1
    assert estimate(prose(words))["minutes"] == 3
    assert estimate(prose(words), extra)["minutes"] == 4


def test_table_cells_are_not_read_as_prose():
    row = nodes.row("", nodes.entry("", prose(500)))
    table = nodes.table("", nodes.tgroup("", nodes.tbody("", row)))
    assert estimate(prose(300), table)["words"] == 300


def test_toctrees_and_comments_are_skipped():
    toctree = nodes.compound("", prose(500), classes=["toctree-wrapper"])
    comment = nodes.comment("", "a note to the author, 500 words long")
    assert estimate(prose(300), toctree, comment, addnodes.toctree())["words"] == 300
