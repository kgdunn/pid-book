"""Collapse every code block in the HTML book, so the prose reads as prose.

The book demonstrates its computations with real, runnable code, and there is a
lot of it: 388 blocks over 9155 lines, and on the case-study pages roughly three
quarters of the page is Python. A reader who came for the argument had to scroll
past all of it.

Each block is therefore wrapped, at build time, in a native ``<details>``
element that starts closed:

.. code-block:: html

    <details class="pid-code">
      <summary class="pid-code__bar">
        <span class="pid-code__lang">Python</span>
        <span class="pid-code__n">23 lines</span>
      </summary>
      <div class="highlight-python notranslate">...</div>
    </details>

``<details>`` was chosen over a button and a hidden ``<div>`` because the
browser already implements this widget: it is keyboard operable, it is
announced correctly by screen readers, and, the point that decides it here,
**it works with JavaScript switched off**. That matches the rule the rest of
this book's front end follows (see ``figure_source.py``): the markup carries
the behaviour, and a script only adds convenience on top.

One consequence to know about: whether find-in-page reaches text inside a
closed block depends on the browser. Recent Chrome and Firefox open the block
and scroll to the match; other engines do not search it at all. A reader
looking for a name that appears only in code may need the page-level switch
first, which is one more reason for that switch to exist.

``_static/js/code-collapse.js`` is that convenience. It adds the page-level
"show every block" switch, remembers the reader's choice, and opens everything
before printing. None of it is needed for the collapse itself to work.

Configuration
-------------

``code_collapse_min_lines`` (default 0)
    Blocks shorter than this stay expanded. 0 collapses every block, which is
    the book's setting. Raise it to leave one-liners and short fragments open.

``code_collapse_labels``
    Maps a Pygments language name to what the bar should say. A language not in
    the map is title-cased.

Only HTML builders are touched. LaTeX, text and epub never see this extension,
because the translator is installed behind a ``builder.format`` guard, exactly
as ``figure_source.py`` does it.
"""

from __future__ import annotations

import html

from docutils import nodes

#: Languages whose title-cased name is not what a reader would call them.
DEFAULT_LABELS = {
    "bash": "Shell",
    "console": "Console",
    "default": "Code",
    "ipython3": "IPython",
    "none": "Output",
    "pycon": "Python session",
    "python": "Python",
    "python3": "Python",
    "rst": "reStructuredText",
    "text": "Output",
}


def _label_for(language: str, labels: dict[str, str]) -> str:
    """What the collapsed bar calls this block's language."""
    return labels.get(language, language.title())


def _line_count(node: nodes.Element) -> int:
    """Lines of source in the block, ignoring any trailing blank line."""
    return len(node.rawsource.rstrip("\n").splitlines()) or 1


def _summary(language: str, lines: int, labels: dict[str, str]) -> str:
    """The one-line bar shown in place of a collapsed block."""
    label = html.escape(_label_for(language, labels), quote=True)
    plural = "line" if lines == 1 else "lines"
    return (
        '<summary class="pid-code__bar">'
        f'<span class="pid-code__lang">{label}</span>'
        f'<span class="pid-code__n">{lines} {plural}</span>'
        "</summary>"
    )


def _install_translator(app) -> None:
    """Wrap each highlighted block this build writes in a closed ``<details>``."""
    if app.builder.format != "html":
        return

    # Read whatever translator is registered and subclass it, so this composes
    # with the other local extensions rather than displacing one of them.
    base = app.registry.translators.get(app.builder.name) or getattr(
        app.builder, "default_translator_class", None
    )
    if base is None:
        return

    class CodeCollapseTranslator(base):  # type: ignore[valid-type, misc]
        def visit_literal_block(self, node):
            # A parsed-literal is not highlighted and is not a code block; Sphinx
            # hands it to docutils, which calls depart_literal_block normally.
            # Leave those alone.
            if node.rawsource != node.astext():
                return super().visit_literal_block(node)

            lines = _line_count(node)
            if lines < self.builder.config.code_collapse_min_lines:
                return super().visit_literal_block(node)

            mark = len(self.body)
            try:
                super().visit_literal_block(node)
            except nodes.SkipNode:
                # Sphinx appends the whole `<div class="highlight-...">...</div>`
                # as one entry and then raises, so depart is never reached: the
                # wrapping has to happen here, around what was just appended.
                language = node.get("language", "default")
                labels = self.builder.config.code_collapse_labels
                block = "".join(self.body[mark:])
                self.body[mark:] = [
                    '<details class="pid-code">',
                    _summary(language, lines, labels),
                    block,
                    "</details>\n",
                ]
                raise
            return None

    app.set_translator(app.builder.name, CodeCollapseTranslator, override=True)


def setup(app):
    app.add_config_value("code_collapse_min_lines", 0, "html")
    app.add_config_value("code_collapse_labels", DEFAULT_LABELS, "html")
    # Later than figure_source's own handler, so its translator is the base this
    # one subclasses and both annotations survive.
    app.connect("builder-inited", _install_translator, priority=600)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
