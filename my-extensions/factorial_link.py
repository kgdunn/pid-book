"""``:factorial:`name``` links to one of the book's examples in Factorial, the designed-experiments app.

``:factorial:`pollutant``` renders as a link named "Factorial" to https://factori.al/?book=pollutant,
which opens the pollutant experiment with the book's factors, units, runs and results filled in,
and analysed. ``:factorial:`the purity results <multi-response-purity>``` names the link otherwise.

The names are those of the app's catalogue, ``web/book-examples.json`` in process-improve, where
each is checked against the numbers the book prints. ``tools/check_factorial_links.py`` checks
every name the book uses against the published app, and that the app links back to the page
that uses it. In the PDF the address appears as a footnote, as every external link's does
(``latex_show_urls``), and it is short enough to type.

In the HTML every link to Factorial, the role's and any written out, opens in one tab of its own:
the first click opens it and later ones reuse it, so a reader working down a chapter keeps one tab
of the app beside the book rather than one per example.
"""

import re

from docutils import nodes
from sphinx.util.docutils import ReferenceRole

APP = "https://factori.al/"

#: The tab every link to Factorial opens in. No ``rel="noopener"``: the browser finds the tab again
#: through the book page that opened it, which is what lets the next click reuse it.
TAB = "factorial"

#: A name the app can open: lowercase words and numbers joined by hyphens, as its page checks.
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def example_url(name: str) -> str:
    """Return the address that opens the book's example ``name`` in Factorial.

    The name goes in the query, not a fragment: on a page without sections the theme's
    scroll-spy reads every link's fragment as a CSS selector, and ``#book=name`` is not one.
    """
    return f"{APP}?book={name}"


class FactorialRole(ReferenceRole):
    """Link to a book example in Factorial; the link reads "Factorial" unless the role names it."""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        name = self.target
        if not NAME.fullmatch(name):
            message = self.inliner.reporter.error(
                f"{name!r} is not the name of an example Factorial opens", line=self.lineno
            )
            return [self.inliner.problematic(self.rawtext, self.rawtext, message)], [message]
        text = self.title if self.has_explicit_title else "Factorial"
        return [
            nodes.reference(
                self.rawtext, text, refuri=example_url(name), classes=["factorial-link"]
            )
        ], []


def one_tab(app, doctree, docname):
    """Send every link to Factorial on the page to its one tab, the role's and any written out."""
    for node in doctree.findall(nodes.reference):
        if node.get("refuri", "").startswith(APP):
            node["target"] = TAB


def setup(app):
    app.add_role("factorial", FactorialRole())
    app.connect("doctree-resolved", one_tab)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
