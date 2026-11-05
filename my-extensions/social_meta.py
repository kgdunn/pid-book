"""Tell link previews and search engines what each page of the book is.

A link to the book shared on LinkedIn, in Slack or Teams, or in a mail client that unfurls
links gets its preview from Open Graph tags in the page's ``<head>``: a title, a sentence and
an image. Search engines read the page description, and a sitemap tells them which pages
exist. Sphinx writes none of these, so this extension adds them, for the HTML builders only.

On every page
-------------
``og:title``, ``og:description``, ``og:url``, ``og:type``, ``og:image`` (with its size and
alt text) and ``og:site_name``, ``twitter:card`` (X reads the ``og:`` tags for the rest), and
``<meta name="description">``. The description is the page's first paragraph of prose, cut at
a word boundary; the landing page uses ``social_meta_description`` instead.

The image is ``social_meta_image``, unless the page sits in a chapter listed in
``social_meta_chapter_images``: then it is that chapter's card, so a shared link to a section
shows a figure from that chapter. ``scripts/render_hero.py`` and
``scripts/render_chapter_images.py`` draw the images.

On the landing page
-------------------
The schema.org record in ``social_meta_jsonld`` (a ``Book``: free to read, its license, its
author), which search engines use to describe the result.

After the build
---------------
``sitemap.xml`` in the output directory, with the address of every page.

Every address is absolute, built from Sphinx's ``html_baseurl``; without it the extension adds
nothing, because a preview cannot follow a relative image link. Nothing here runs in the
reader's browser or contacts any server.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from docutils import nodes

HTML_BUILDERS = {"html", "dirhtml"}
DESCRIPTION_LIMIT = 200  # characters; previews show about this much
MIN_PARAGRAPH = 60  # a shorter first paragraph ("The equation is:") does not describe the page

# Paragraphs inside these are asides, exercises or captions, not the page's opening prose.
ASIDES = (
    nodes.Admonition,
    nodes.sidebar,
    nodes.topic,
    nodes.table,
    nodes.figure,
    nodes.legend,
    nodes.footnote,
    nodes.citation,
    nodes.field_list,
    nodes.block_quote,
)

# LaTeX commands that read naturally as one character in a plain-text description.
MATH_SYMBOLS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "Delta": "Δ", "epsilon": "ε",
    "lambda": "λ", "mu": "μ", "pi": "π", "rho": "ρ", "sigma": "σ", "Sigma": "Σ", "tau": "τ",
    "theta": "θ", "times": "×", "pm": "±", "leq": "≤", "geq": "≥", "approx": "≈",
}  # fmt: skip


def plain_math(latex: str) -> str:
    """Render inline LaTeX as plain text: ``\\sigma`` becomes σ, other markup is dropped."""
    text = re.sub(r"\\([A-Za-z]+)", lambda m: MATH_SYMBOLS.get(m.group(1), ""), latex)
    return " ".join(re.sub(r"[{}_^$\\]", "", text).split())


def node_text(node: nodes.Node) -> str:
    """The text of ``node``, with inline maths rendered by ``plain_math``."""
    if isinstance(node, nodes.math):
        return plain_math(node.astext())
    if isinstance(node, nodes.Text):
        return str(node)
    return "".join(node_text(child) for child in node.children)


def shorten(text: str, limit: int = DESCRIPTION_LIMIT) -> str:
    """Cut ``text`` at the last word boundary within ``limit`` characters, marking the cut."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(",;:")
    return f"{cut}…"


def description(doctree: nodes.Node, limit: int = DESCRIPTION_LIMIT) -> str:
    """The page's first paragraph of prose, shortened; empty if the page has none."""
    for paragraph in doctree.findall(nodes.paragraph):
        if any(isinstance(parent, ASIDES) for parent in _ancestors(paragraph)):
            continue
        text = " ".join(node_text(paragraph).split())
        if len(text) >= MIN_PARAGRAPH:
            return shorten(text, limit)
    return ""


def _ancestors(node: nodes.Node):
    parent = node.parent
    while parent is not None:
        yield parent
        parent = parent.parent


def meta_tags(
    *,
    title: str,
    summary: str,
    url: str,
    image_url: str,
    image_alt: str,
    image_size: tuple[int, int],
    site_name: str,
    page_type: str,
) -> str:
    """The ``<meta>`` tags for one page, with every value HTML-escaped."""
    properties = [
        ("og:title", title),
        ("og:description", summary),
        ("og:url", url),
        ("og:type", page_type),
        ("og:site_name", site_name),
        ("og:image", image_url),
        ("og:image:width", str(image_size[0])),
        ("og:image:height", str(image_size[1])),
        ("og:image:alt", image_alt),
    ]
    lines = [
        f'<meta property="{key}" content="{html.escape(value)}" />'
        for key, value in properties
        if value
    ]
    lines.append('<meta name="twitter:card" content="summary_large_image" />')
    if summary:
        lines.append(f'<meta name="description" content="{html.escape(summary)}" />')
    return "\n".join(lines) + "\n"


def json_ld(record: dict[str, Any]) -> str:
    """``record`` as a JSON-LD ``<script>``; ``</`` is escaped so the text cannot end the element."""
    text = json.dumps(record, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{text}\n</script>\n'


def sitemap(urls: list[str]) -> str:
    """A sitemap (sitemaps.org protocol 0.9) listing ``urls``."""
    entries = "".join(f"  <url><loc>{html.escape(url)}</loc></url>\n" for url in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n"
    )


def _base_url(app) -> str:
    base = app.config.html_baseurl
    return base if not base or base.endswith("/") else f"{base}/"


def _image_for(app, pagename: str) -> tuple[str, str]:
    """The image path (relative to the output directory) and alt text for ``pagename``."""
    config = app.config
    chapter = pagename.split("/", 1)[0]
    image = config.social_meta_chapter_images.get(chapter)
    if image and f"{chapter}/index" in app.env.titles:
        heading = app.env.titles[f"{chapter}/index"].astext()
        return image, f"{heading}: an example from {config.html_title}, a free online textbook."
    return config.social_meta_image, config.social_meta_image_alt


def _add_tags(app, pagename: str, templatename: str, context: dict, doctree) -> None:
    base = _base_url(app)
    if app.builder.name not in HTML_BUILDERS or not base or doctree is None:
        return
    config = app.config
    is_root = pagename == config.root_doc
    title = html.unescape(re.sub(r"<[^>]+>", "", context.get("title", "")))
    if not is_root:
        title = f"{title} | {config.html_title}"
    summary = (
        config.social_meta_description
        if is_root
        else description(doctree) or config.social_meta_description
    )
    image, alt = _image_for(app, pagename)
    tags = meta_tags(
        title=title,
        summary=summary,
        url=base + app.builder.get_target_uri(pagename),
        image_url=base + image if image else "",
        image_alt=alt,
        image_size=tuple(config.social_meta_image_size),
        site_name=config.html_title,
        page_type="website" if is_root else "article",
    )
    if is_root and config.social_meta_jsonld:
        tags += json_ld(config.social_meta_jsonld)
    context["metatags"] = context.get("metatags", "") + tags


def _write_sitemap(app, exception: Exception | None) -> None:
    base = _base_url(app)
    if exception is not None or app.builder.name not in HTML_BUILDERS or not base:
        return
    urls = [base + app.builder.get_target_uri(docname) for docname in sorted(app.env.found_docs)]
    Path(app.outdir, "sitemap.xml").write_text(sitemap(urls), encoding="utf-8")


def setup(app):
    app.add_config_value("social_meta_image", "", "html")
    app.add_config_value("social_meta_image_alt", "", "html")
    app.add_config_value("social_meta_image_size", (2560, 1280), "html")
    app.add_config_value("social_meta_chapter_images", {}, "html")
    app.add_config_value("social_meta_description", "", "html")
    app.add_config_value("social_meta_jsonld", {}, "html")

    app.connect("html-page-context", _add_tags)
    app.connect("build-finished", _write_sitemap)

    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
