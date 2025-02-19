#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import re
from docutils import nodes
from docutils.parsers.rst import directives

# from sphinx.util.compat import Directive
from docutils.parsers.rst import Directive

CONTROL_HEIGHT = 30


def get_size(d, key):
    if key not in d:
        return None
    m = re.match(r"(\d+)(|%|px)$", d[key])
    if not m:
        raise ValueError("invalid size %r" % d[key])
    return int(m.group(1)), m.group(2) or "px"


def css(d):
    return "; ".join(sorted("%s: %s" % kv for kv in d.items()))


class youtube(nodes.General, nodes.Element):
    pass


def visit_youtube_node_text(self, node):
    text_to_add = "[YouTube video: %s]" % node["id"]
    self.states[-1].append((-1, text_to_add))


def visit_youtube_node_latex(self, node):
    url = node["id"]  # "https://www.youtube.com/embed/%s" %
    text = (
        """
    \\begin{textblock*}{15mm}(-1.75cm,-1cm)
    \n\\href{%s}{\\scalebox{0.025}{\\includegraphics{1024px-High-contrast-camera-video.png}}\n {\\footnotesize Video for this section}}\n
    \\end{textblock*}
    """
        % url
    )
    self.body.append(text)


def visit_youtube_node_html(self, node):
    aspect = node["aspect"]
    width = node["width"]
    height = node["height"]

    if aspect is None:
        aspect = 16, 9

    if (height is None) and (width is not None) and (width[1] == "%"):
        style = {
            "padding-top": "%dpx" % CONTROL_HEIGHT,
            "padding-bottom": "%f%%" % (width[0] * aspect[1] / aspect[0]),
            "width": "%d%s" % width,
            "position": "relative",
        }
        self.body.append(self.starttag(node, "div", style=css(style)))
        style = {
            "position": "absolute",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "border": "0",
        }
        attrs = {
            "src": "https://www.youtube.com/embed/%s" % node["id"],
            "style": css(style),
        }
        self.body.append(self.starttag(node, "iframe", **attrs))
        self.body.append("</iframe></div>")
    else:
        if width is None:
            if height is None:
                width = 560, "px"
            else:
                width = height[0] * aspect[0] / aspect[1], "px"
        if height is None:
            height = width[0] * aspect[1] / aspect[0], "px"
        style = {
            "width": "%d%s" % width,
            "height": "%d%s" % (height[0] + CONTROL_HEIGHT, height[1]),
            "border": "0",
        }
        attrs = {
            "src": "https://www.youtube.com/embed/%s" % node["id"],
            "style": css(style),
        }
        self.body.append(self.starttag(node, "iframe", **attrs))
        self.body.append("</iframe>")


def depart_youtube_node(self, node):
    pass


class YouTube(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "width": directives.unchanged,
        "height": directives.unchanged,
        "aspect": directives.unchanged,
    }

    def run(self):
        if "aspect" in self.options:
            aspect = self.options.get("aspect")
            m = re.match(r"(\d+):(\d+)", aspect)
            if m is None:
                raise ValueError("invalid aspect ratio %r" % aspect)
            aspect = tuple(int(x) for x in m.groups())
        else:
            aspect = None
        width = get_size(self.options, "width")
        height = get_size(self.options, "height")
        return [youtube(id=self.arguments[0], aspect=aspect, width=width, height=height)]


def setup(app):
    app.add_node(
        youtube,
        html=(visit_youtube_node_html, depart_youtube_node),
        text=(visit_youtube_node_text, depart_youtube_node),
        latex=(visit_youtube_node_latex, depart_youtube_node),
    )
    app.add_directive("youtube", YouTube)

    return {"parallel_read_safe": True}
