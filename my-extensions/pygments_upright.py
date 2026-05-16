"""Pygments style for the PDF theme harness.

A copy of Sphinx's built-in ``sphinx`` style with ``italic`` swapped to
``noitalic`` on every comment token, so code-listing comments render upright.
Used only by the ``business-ragged`` PDF theme — see the PID_PDF_THEME block
in ``conf.py``. Nothing else (the full book, the HTML build) is affected.
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
