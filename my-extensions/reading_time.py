"""Estimate how long each page takes to read, and hand it to the template.

The number is computed here, at build time, from the resolved doctree, and
put in the page context as ``pid_reading_time`` for
``_templates/pid-reading-time.html`` to render next to the sidebar toggle.
Doing it in Python rather than in the browser means the figure is in the
served HTML: it needs no script, it does not shift the header once the page
has painted, and it is visible to anyone reading a saved copy.

Why not the usual "words divided by 250":

* This book is read for understanding, not skimmed. Brysbaert's 2019
  meta-analysis puts silent reading of non-fiction English at about
  238 words per minute; reading technical material closely is slower, so
  the default here is ``reading_time_wpm = 150``.
* A page is not only prose. An equation stops the reader, a figure has to
  be looked at, and a code block is read a line at a time. Those carry a
  cost in seconds each (``reading_time_costs``), so a dense page comes out
  higher than its word count alone suggests, which is the point.

What is counted, per page:

===================  ===========================================
Prose                every word outside the categories below
Inline maths         one ``:math:`` role
Display maths        one ``.. math::`` block
Images               one image, including the one inside a figure
Tables               the table, plus a cost for each of its rows
Code                 one line of a literal block
===================  ===========================================

Toctrees, comments, raw blocks and substitution definitions are skipped.
Table cells are not read as prose: the per-row cost stands in for them.
Videos are counted but cost nothing, since their running time is not in the
source; a page carrying one says so in the tooltip instead.

Pages with less than ``reading_time_min_words`` words of prose (the chapter
index pages, which are a toctree and a sentence) get no estimate at all,
and the template then renders nothing.

Nothing is emitted for the LaTeX, text or epub builders.
"""

from __future__ import annotations

from collections import Counter

from docutils import nodes
from sphinx import addnodes

from .youtube import youtube

__all__ = ["setup", "estimate"]

# Words per minute of prose, for someone reading to understand rather than
# to skim. See the module docstring for where the number comes from.
DEFAULT_WPM = 150

# Seconds added for each thing that is not prose. Keys match the counter.
# Read them against the prose rate: at 150 wpm a word costs 0.4 s, so a line
# of code is priced at about five words, a display equation at fifty.
DEFAULT_COSTS = {
    "inline_math": 1.0,  # a symbol read in passing
    "display_math": 20.0,  # a set-out equation, read and parsed
    "images": 12.0,  # look at the figure, tie it to the caption
    "tables": 8.0,  # orient yourself in the table
    "table_rows": 3.0,  # per row scanned
    "code_lines": 2.0,  # code and printed output, a line at a time
    "videos": 0.0,  # running time is unknown; see the docstring
}

# Below this many words of prose, no estimate is shown.
DEFAULT_MIN_WORDS = 50

# Carry no reading cost and no text worth counting.
_SKIPPED = (
    addnodes.toctree,
    nodes.comment,
    nodes.raw,
    nodes.substitution_definition,
    nodes.system_message,
    nodes.target,
)


def _is_resolved_toctree(node) -> bool:
    """True for the list of links a ``toctree`` directive expands into."""
    return isinstance(node, nodes.compound) and "toctree-wrapper" in node["classes"]


def _tally(node, counts: Counter) -> None:
    """Add the cost of ``node`` and its children into ``counts``."""
    if isinstance(node, _SKIPPED) or _is_resolved_toctree(node):
        return
    if isinstance(node, nodes.Text):
        counts["words"] += len(node.astext().split())
    elif isinstance(node, nodes.math):
        counts["inline_math"] += 1
    elif isinstance(node, nodes.math_block):
        counts["display_math"] += 1
    elif isinstance(node, nodes.literal_block):
        counts["code_lines"] += node.astext().count("\n") + 1
    elif isinstance(node, nodes.image):
        counts["images"] += 1
    elif isinstance(node, nodes.table):
        counts["tables"] += 1
        counts["table_rows"] += len(list(node.findall(nodes.row)))
    elif isinstance(node, youtube):
        counts["videos"] += 1
    else:
        for child in node.children:
            _tally(child, counts)


def estimate(doctree, wpm: int, costs: dict[str, float], min_words: int) -> dict | None:
    """Reading time for one page, or ``None`` when the page is too short.

    Parameters
    ----------
    doctree : docutils.nodes.document
        The resolved doctree of the page.
    wpm : int
        Words of prose read per minute.
    costs : dict[str, float]
        Seconds added per non-prose element, keyed as in `DEFAULT_COSTS`.
    min_words : int
        Pages with fewer words of prose than this get no estimate.

    Returns
    -------
    dict | None
        ``{"minutes": int, "words": int, "videos": int}``, or ``None``.
    """
    counts: Counter = Counter()
    _tally(doctree, counts)
    if counts["words"] < min_words:
        return None

    seconds = counts["words"] / wpm * 60
    seconds += sum(cost * counts[key] for key, cost in costs.items())
    return {
        "minutes": max(1, round(seconds / 60)),
        "words": counts["words"],
        "videos": counts["videos"],
    }


def _add_to_context(app, pagename, templatename, context, doctree) -> None:
    """Put the estimate in the page context, for the template to render."""
    # No doctree on the generated pages (search, genindex): nothing to count.
    if doctree is None:
        return
    context["pid_reading_time"] = estimate(
        doctree,
        app.config.reading_time_wpm,
        {**DEFAULT_COSTS, **app.config.reading_time_costs},
        app.config.reading_time_min_words,
    )


def setup(app):
    app.add_config_value("reading_time_wpm", DEFAULT_WPM, "html")
    # Merged over DEFAULT_COSTS, so conf.py can override one entry alone.
    app.add_config_value("reading_time_costs", {}, "html")
    app.add_config_value("reading_time_min_words", DEFAULT_MIN_WORDS, "html")

    app.connect("html-page-context", _add_to_context)

    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
