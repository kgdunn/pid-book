#!/usr/bin/env python
"""Keep the web-only pages (Privacy, Readership statistics) out of the PDF.

The privacy policy and the live readership-statistics dashboard are HTML-only
pages: ``stats.rst`` is built almost entirely from ``.. raw:: html`` blocks fed
by JavaScript, and neither belongs in the printable book. They stay in the HTML
sidebar via the hidden toctree in ``contents.rst``, but the LaTeX builder would
otherwise render them as numbered chapters. Before this extension they appeared
as chapters 1 and 2 in the PDF, ahead of "Visualizing Process Data".

Wrapping the toctree in ``.. only:: html`` does not help here, because
``latex_documents`` uses ``toctree_only=True``: the LaTeX builder harvests every
toctree node directly (``sphinx.builders.latex.LaTeXBuilder.assemble_doctree``)
and discards the surrounding ``only`` wrapper. Instead we drop the pages after
the toctree has been inlined. ``inline_all_toctrees`` wraps each included
document in a ``start_of_file`` node carrying its docname, so we remove those
wrappers for the two web-only pages.

This runs as a post-transform restricted to the ``latex`` format, on the
assembled tree, so the shared doctree cache is untouched and the HTML sidebar is
unchanged.
"""

from __future__ import annotations

from typing import Any

from sphinx import addnodes
from sphinx.transforms.post_transforms import SphinxPostTransform

# Docnames that must never appear in the LaTeX / PDF edition.
PDF_EXCLUDED_DOCS = frozenset({"privacy", "stats"})


class DropWebOnlyPagesFromLaTeX(SphinxPostTransform):
    """Remove the Privacy and Readership-statistics pages from the PDF build."""

    # Only the LaTeX builder; HTML and text are left untouched.
    formats = ("latex",)
    # After references are resolved and toctrees inlined, before serialisation.
    default_priority = 400

    def run(self, **kwargs: Any) -> None:
        for start_of_file in list(self.document.findall(addnodes.start_of_file)):
            if start_of_file.get("docname") in PDF_EXCLUDED_DOCS:
                start_of_file.parent.remove(start_of_file)


def setup(app: Any) -> dict[str, Any]:
    app.add_post_transform(DropWebOnlyPagesFromLaTeX)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
