# -*- coding: utf-8 -*-
"""
    sphinxcontrib.whoosh
    ~~~~~~~~~~~~~~~~~~~~

    Whoosh search index builder.

    :copyright: Copyright 2009 Pauli Virtanen
    :license: BSD, see LICENSE for details.
"""

import os

from sphinx.util import SEP
from sphinx.builders.html import StandaloneHTMLBuilder

import whoosh.index
import whoosh.fields
import whoosh.analysis

# Searching the document text
# ---------------------------
def sanitize_search_text(text):
    """
    Cleans the RST source code to remove:

    * .. ucomment:: directives
    * Underlines for headings: e.g. "-----"
    * inline math roles :math:`....` (leaves the part inside the role beind
    * cross-references: e.g.  .. _my-cross-reference:
    * .. rubric:: XYZ is left just as XYZ

    TODO(KGD):
    * table_row = re.compile(r'(={2,})|(\+-{2,})')
    * figure and image directives; and the options that go with them

    """
    text_list = text.split("\n")
    ucomment_lines = re.compile(r"^\s*\.\. ucomment::\s*(.*?):")
    VALID_TITLES = [
        "!",
        '"',
        "#",
        "$",
        "%",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "_",
        "`",
        r"{",
        "|",
        "}",
        "~",
    ]

    div_re_str = r"^"
    for entry in VALID_TITLES:
        if entry in ["^", "*", "+", "$", "(", ")", "-", ".", "?", "[", "]", "\\", "{", "}", "|"]:
            entry = "\\" + entry

        div_re_str += entry + r"{3,}|"
    div_re_str = div_re_str[0:-1] + "$"
    div_re = re.compile(div_re_str)

    crossref_re = re.compile(r"^\s*\.\. _(.*?):")
    rubric_re = re.compile(r"^\s*(\.\. rubric:: )(.*?)")

    # Remove the :math:`...` part, leaving only the ... portion behind.
    math_role = re.compile(r"(:math:`)(.*?)(`)")

    out = []
    for line in text_list:
        line = math_role.sub("\g<2>", line)
        line = rubric_re.sub("\g<2>", line)
        out.append(line)
        if ucomment_lines.match(line):
            out.pop()
            continue
        if div_re.match(line):
            out.pop()
            continue
        if crossref_re.match(line):
            out.pop()
            continue

    return "\n".join(out)


# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class WhooshBuilder(StandaloneHTMLBuilder):
    """
    Builds Whoosh index.

    """

    name = "whoosh"
    format = "whoosh"

    def init(self):
        self.config_hash = ""
        self.tags_has = ""
        self.theme = None  # no theme
        self.templates = None  # no templates
        self.init_translator_class()
        self.init_highlighter()

        self.schema = whoosh.fields.Schema(
            name=whoosh.fields.ID(stored=True),
            title=whoosh.fields.TEXT(stored=True),
            body=whoosh.fields.TEXT(analyzer=whoosh.analysis.StemmingAnalyzer(), stored=True),
        )
        self.index = whoosh.index.create_in(self.outdir, self.schema)
        self.writer = self.index.writer()

    def get_target_uri(self, docname, typ=None):
        if docname == "index":
            return ""

        if docname.endswith(SEP + "index"):
            return docname[:-5]  # up to sep
        return docname + SEP

    def handle_page(
        self, pagename, ctx, templatename="page.html", outfilename=None, event_arg=None
    ):
        ctx["current_page_name"] = pagename
        sidebarfile = self.config.html_sidebars.get(pagename)
        if sidebarfile:
            ctx["customsidebar"] = sidebarfile

        self.app.emit("html-page-context", pagename, templatename, ctx, event_arg)

        # KGD: I don't want the main TOC file to appear in search results
        if pagename.endswith("contents") or pagename.endswith("index"):
            return

        else:
            body_text = strip_tags(unicode(ctx.get("body", "")))

        self.writer.add_document(
            name=unicode(ctx["current_page_name"]),
            title=unicode(ctx.get("title", "")),
            body=body_text,
        )

        # print('=============')
        print(r"Added {0}".format(unicode(ctx.get("title", ""))))
        # print('=============')
        # print(r"Added {0}".format(body_text.encode('utf-8')))
        # print('-----------')

    def finish(self):
        self.writer.commit()


def setup(app):
    app.add_builder(WhooshBuilder)
