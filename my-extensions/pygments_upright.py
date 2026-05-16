"""Pygments style with no slanted code.

A copy of Sphinx's built-in ``sphinx`` style with ``italic`` swapped to
``noitalic`` on every token, so nothing in a code listing renders slanted
(the stock style italicises comments, docstrings and string interpolation).
Wired up as ``pygments_style`` in ``conf.py`` for the PDF build. The HTML
build uses the theme's own Pygments styles; it is kept upright by a CSS rule
in ``_static/css/theme-extended-kgd.css``.
"""

from sphinx.pygments_styles import SphinxStyle


def _upright(value):
    """Return *value* with the standalone ``italic`` keyword turned upright.

    Word-wise so that ``noitalic`` (which contains ``italic``) is left alone.
    """
    return " ".join("noitalic" if word == "italic" else word for word in value.split())


class UprightSphinxStyle(SphinxStyle):
    """The ``sphinx`` style, but with every token rendered upright."""

    styles = {token: _upright(value) for token, value in SphinxStyle.styles.items()}
