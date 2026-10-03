"""Collapse every code block in the HTML book, so the prose reads as prose.

The book demonstrates its computations with real, runnable code, and there is a
lot of it: 388 blocks over 8809 lines, and on the case-study pages roughly three
quarters of the page is Python. A reader who came for the argument had to scroll
past all of it.

Each block is therefore wrapped, at build time, in a native ``<details>``
element that starts closed:

.. code-block:: html

    <details class="pid-code">
      <summary class="pid-code__bar" data-pagefind-ignore>
        <span class="pid-code__lang">Python</span>, <span class="pid-code__n">23 lines</span>
      </summary>
      <div class="highlight-python notranslate">...</div>
    </details>

``<details>`` was chosen over a button and a hidden ``<div>`` because the
browser already implements this widget: it is keyboard operable (Enter and
Space), the expanded and collapsed states are reflected to assistive technology
from the ``open`` attribute with no ARIA of our own, and, the point that
decides it here, **it works with JavaScript switched off**. That matches the
rule the rest of this book's front end follows (see ``figure_source.py``): the
markup carries the behaviour, and a script only adds convenience on top.

Two consequences of that choice are worth knowing.

The native disclosure triangle is kept. Suppressing it (``list-style: none``
plus a drawn ``::before`` marker) looks tidier, but several browser and
screen-reader pairings rely on the marker to announce the state at all, so the
stylesheet colours the marker rather than replacing it.

Whether find-in-page reaches text inside a closed block depends on the
browser. Chromium has opened the block and scrolled to the match for several
versions; Firefox and Safari have only recently followed, and do not always
scroll to it. A reader looking for a name that appears only in code may need
the page-level switch first, which is one more reason for that switch to exist.

``_static/js/code-collapse.js`` is that convenience. It drives the page-level
switch, remembers the reader's choice, and opens everything before printing.
None of it is needed for the collapse itself to work.

Where the markup is produced, and why here
------------------------------------------

A post-transform restricted **by builder name** runs on the resolved doctree,
at write time, once per page written. The LaTeX, text, man and epub builders
never run it, so they never construct the wrapper node at all: the PDF and
``make text`` keep the code in full without a line of special-casing.

The gate is on the builder's *name*, not on ``builder.format``, because
``sphinx.builders.epub3.Epub3Builder`` inherits ``StandaloneHTMLBuilder`` and
with it ``format = "html"``. A format gate therefore also rewrites the EPUB
edition, where a collapsed block is at the mercy of the reading system.

Post-transform output is applied by ``get_and_resolve_doctree`` at write time
and is never written back into the pickled ``.doctrees`` cache, so the wrapper
cannot go stale there and cannot leak into another builder's run. This is the
same mechanism ``pdf_exclude.py`` uses for the mirror-image problem, with
``formats = ("latex",)``.

Configuration
-------------

``code_collapse_min_lines`` (default 0)
    Blocks shorter than this stay expanded, with no bar. 0 collapses every
    block, which is the book's setting. Raise it to leave one-liners open.

``code_collapse_labels``
    Maps a Pygments language name to what the bar should say. A language not in
    the map is title-cased.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform

if TYPE_CHECKING:
    from sphinx.application import Sphinx

#: Builders that get the collapse, named one by one. Not a ``formats`` gate:
#: the epub builder subclasses the HTML one and reports ``format = "html"``.
HTML_BUILDERS = ("html", "dirhtml", "singlehtml")

#: Languages whose title-cased name is not what a reader would call them.
DEFAULT_LABELS = {
    "bash": "Shell",
    "console": "Console",
    "default": "Code",
    "ipython3": "IPython",
    "matlab": "MATLAB",
    "none": "Output",
    "pycon": "Python session",
    "python": "Python",
    "python3": "Python",
    "r": "R",
    "rst": "reStructuredText",
    "s": "S",
    "text": "Output",
}


class collapsible_code(nodes.General, nodes.Element):
    """Wrapper around one literal block. Built for the HTML builders only."""


def _line_count(node: nodes.Element) -> int:
    """Lines of source in the block, ignoring any trailing blank line."""
    return len(node.rawsource.rstrip("\n").splitlines()) or 1


class CollapseCodeBlocks(SphinxPostTransform):
    """Put every highlighted literal block inside a collapsed wrapper."""

    builders = HTML_BUILDERS
    # Late, so the reference resolver and Sphinx's own output post-transforms
    # have already run and nothing downstream is still looking for a
    # literal_block in its original parent.
    default_priority = 900

    def run(self, **kwargs: Any) -> None:
        minimum = self.config.code_collapse_min_lines
        labels = {**DEFAULT_LABELS, **self.config.code_collapse_labels}

        for literal in list(self.document.findall(nodes.literal_block)):
            parent = literal.parent
            if parent is None or isinstance(parent, collapsible_code):
                continue
            # A parsed-literal is not highlighted and is not a code block;
            # Sphinx hands it to docutils. This is the same test
            # HTML5Translator.visit_literal_block applies. Leave those alone.
            if literal.rawsource != literal.astext():
                continue
            lines = _line_count(literal)
            if lines < minimum:
                continue

            language = literal.get("language") or "default"
            wrapper = collapsible_code(
                "",
                label=labels.get(language, language.title()),
                lines=lines,
            )
            index = parent.index(literal)
            parent.remove(literal)
            wrapper += literal
            parent.insert(index, wrapper)


def visit_collapsible_code(self, node: collapsible_code) -> None:
    """Open the disclosure and write the bar that stands in for the code."""
    lines = node["lines"]
    # The separator is in the markup, not in a CSS `gap`: the bar's accessible
    # name is computed from its text, and a flex gap contributes nothing to it.
    # data-pagefind-ignore keeps 388 copies of "Python, 23 lines" out of the
    # Pagefind index that `make html` builds over the output tree. Sphinx's own
    # searchindex.js is built from the doctree, where the label is a node
    # attribute rather than a Text node, so it never saw the label anyway.
    self.body.append(
        '<details class="pid-code">'
        '<summary class="pid-code__bar" data-pagefind-ignore>'
        f'<span class="pid-code__lang">{self.encode(node["label"])}</span>, '
        f'<span class="pid-code__n">{lines} {"line" if lines == 1 else "lines"}</span>'
        "</summary>"
    )


def depart_collapsible_code(self, node: collapsible_code) -> None:
    self.body.append("</details>\n")


def _passthrough(self, node: collapsible_code) -> None:
    """Emit nothing and keep walking, so the code itself still comes through.

    No builder outside :data:`HTML_BUILDERS` ever sees this node, because the
    post-transform is gated on the builder name. These visitors exist so that
    if that gate is ever widened by mistake, the LaTeX or text build produces
    the code unwrapped instead of failing with ``Unknown node``.
    """


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("code_collapse_min_lines", 0, "html")
    app.add_config_value("code_collapse_labels", {}, "html")
    app.add_node(
        collapsible_code,
        html=(visit_collapsible_code, depart_collapsible_code),
        latex=(_passthrough, _passthrough),
        text=(_passthrough, _passthrough),
        man=(_passthrough, _passthrough),
        texinfo=(_passthrough, _passthrough),
    )
    app.add_post_transform(CollapseCodeBlocks)
    return {
        "version": "2.0",
        # Bumping this discards a stale environment.pickle, so an edit to this
        # file cannot leave already-written pages carrying the previous markup.
        # The book's own SPHINXOPTS already carries -E, which has the same
        # effect; this covers anyone building without it.
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
