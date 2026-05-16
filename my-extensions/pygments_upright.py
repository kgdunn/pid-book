"""Pygments style with upright code comments.

A copy of Sphinx's built-in ``sphinx`` style with ``italic`` swapped to
``noitalic`` on every comment token, so code-listing comments render upright
rather than slanted. Wired up as ``pygments_style`` in ``conf.py``; it applies
to both the HTML and the PDF builds.
"""

from sphinx.pygments_styles import SphinxStyle


def _upright(value):
    """Return *value* with the standalone ``italic`` keyword turned upright.

    Word-wise so that ``noitalic`` (which contains ``italic``) is left alone.
    """
    return " ".join(
        "noitalic" if word == "italic" else word for word in value.split()
    )


class UprightCommentSphinxStyle(SphinxStyle):
    """The ``sphinx`` style, but with non-italic comments."""

    styles = {
        token: (_upright(value) if "Comment" in str(token) else value)
        for token, value in SphinxStyle.styles.items()
    }
