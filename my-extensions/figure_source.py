"""Record, for every figure, the script that drew it.

Readers who want to reproduce a figure need the code behind it. This
extension carries that link from the source tree into the built HTML,
without putting it in the ``:alt:`` field, which belongs to screen readers
and to people whose images failed to load.

Where the link comes from, in order of precedence:

1. An explicit ``:source:`` option on an ``image`` or ``figure`` directive::

       .. figure:: ../figures/doe/COST-contours.png
           :source: doe/doe_chapter_figures.py
           :alt: Contour plot illustrating the one-factor-at-a-time search path

   The path is relative to the root of the figures repository.

2. A scan of the figures repository, used for every image with no
   ``:source:``. Each generator names the files it writes, so reading the
   scripts recovers the mapping for the whole tree at once, and keeps
   recovering it as figures are replaced. See :func:`build_manifest`.

Where the link ends up:

* On the ``<img>`` itself, as ``data-figure-source``. This is the one that
  matters: it is part of the page, so it needs no script, no network and no
  second request. With JavaScript disabled, offline, or reading a
  ``file://`` copy, the link is still there in the markup.
* In ``_static/figure-sources.json``, an index of every mapping in the
  build. The page does not read it; it is there for tooling, and for anyone
  who wants the whole list at once.

Nothing is emitted for the LaTeX, text or epub builders.

``figure_source_show_link = True`` additionally puts a real link after each
figure, out of the way until it receives keyboard focus. That gives a route
to the source with no JavaScript at all, at the cost of one more thing for a
screen reader to announce per figure. It is off by default.

The companion ``_static/js/figure-source.js`` is a convenience on top of the
attribute, not a dependency of it.
"""

from __future__ import annotations

import html
import json
import pathlib
import re

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Figure, Image
from sphinx.util import logging

logger = logging.getLogger(__name__)

__all__ = ["setup", "build_manifest"]

# A quoted image filename inside a generator script.
IMAGE_IN_SOURCE = re.compile(r"""['"]([\w./-]+\.(?:png|jpg|jpeg|svg))['"]""")

# ... except where the line reads that image rather than writing it. The
# scripts that join panels side by side open their inputs by name, and
# should not be mistaken for the script that drew them.
READ_CONTEXT = re.compile(r"\b(?:Image\.open|imread|imageio\.\w+|readPNG|read_png)\b")

# One generator naming another means the named one has been superseded: the
# replacements say so in their docstrings. Used only to break ties.
SCRIPT_NAME = re.compile(r"([\w-]+\.(?:py|R|r|m))\b")

GENERATOR_SUFFIXES = (".py", ".R", ".r", ".m")

# Directories in the figures repository that hold no generators worth
# scanning, or that would slow the scan down for nothing.
SKIP_DIRECTORIES = {".git", "__pycache__", ".ipynb_checkpoints"}


class SourceMixin:
    """Adds a ``:source:`` option that records the generating script."""

    def run(self):
        nodes_out = super().run()
        source = self.options.get("source")
        if source:
            for node in nodes_out:
                for image in node.findall(nodes.image):
                    image["figure_source"] = source
                if isinstance(node, nodes.image):
                    node["figure_source"] = source
        return nodes_out


class ImageWithSource(SourceMixin, Image):
    option_spec = dict(Image.option_spec, source=directives.unchanged)


class FigureWithSource(SourceMixin, Figure):
    option_spec = dict(Figure.option_spec, source=directives.unchanged)


def build_manifest(figures_root: pathlib.Path) -> dict[str, str]:
    """Map each image to the script that writes it.

    A script claims an image when it names that image, on a line that does
    not read it. The scripts that join panels side by side open their inputs
    by name, so excluding read lines keeps a script that consumes a figure
    from being mistaken for the one that drew it.

    Claims are resolved per image *path*, not per filename, so two
    directories holding an image of the same name each resolve to their own
    generator. Where more than one script claims the same image, the ranking
    is: a script sitting in the image's own directory beats one elsewhere; a
    script no other script mentions beats one that is named inside another,
    since a replacement says which script it replaces; and Python beats R or
    MATLAB, because the Python is what runs today.

    The result is keyed both by path relative to the figures root and, where
    a filename is unambiguous across the tree, by that filename alone.
    """
    if not figures_root.is_dir():
        return {}

    claims: dict[str, list[pathlib.Path]] = {}
    mentioned: set[str] = set()
    for script in sorted(figures_root.rglob("*")):
        if script.suffix not in GENERATOR_SUFFIXES or not script.is_file():
            continue
        if SKIP_DIRECTORIES & set(script.parts):
            continue
        try:
            text = script.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        mentioned |= {n for n in SCRIPT_NAME.findall(text) if n != script.name}
        for line in text.splitlines():
            if READ_CONTEXT.search(line):
                continue
            for match in IMAGE_IN_SOURCE.findall(line):
                name = pathlib.PurePosixPath(match).name
                beside = script.parent / name
                found = [beside] if beside.exists() else list(figures_root.rglob(name))
                for image in found:
                    key = image.relative_to(figures_root).as_posix()
                    claims.setdefault(key, []).append(script)

    def rank(script: pathlib.Path, image_path: str) -> tuple[int, int, int, str]:
        own_directory = script.parent == (figures_root / image_path).parent
        superseded = script.name in mentioned
        runnable = script.suffix == ".py"
        return (
            0 if own_directory else 1,
            1 if superseded else 0,
            0 if runnable else 1,
            str(script),
        )

    by_path = {
        image_path: min(scripts, key=lambda s: rank(s, image_path))
        .relative_to(figures_root)
        .as_posix()
        for image_path, scripts in claims.items()
    }

    manifest = dict(by_path)
    seen: dict[str, set[str]] = {}
    for image_path, generator in by_path.items():
        seen.setdefault(pathlib.PurePosixPath(image_path).name, set()).add(generator)
    for image_path, generator in by_path.items():
        name = pathlib.PurePosixPath(image_path).name
        if len(seen[name]) == 1:
            manifest[name] = generator
    return manifest


def _manifest_for(app) -> dict[str, str]:
    """The scan result, computed once per build."""
    cached = getattr(app, "_figure_source_manifest", None)
    if cached is None:
        root = (pathlib.Path(app.confdir) / app.config.figure_source_root).resolve()
        cached = build_manifest(root)
        app._figure_source_manifest = cached
    return cached


def _within_figures(app, uri: str) -> str:
    """The image's path relative to the figures repository root.

    Sphinx records the path as written in the source, so a document in a
    subdirectory contributes leading ``../`` segments.
    """
    prefix = app.config.figure_source_root.strip("/") + "/"
    within = re.sub(r"^(?:\.\./)+", "", uri.lstrip("/"))
    return within[len(prefix):] if within.startswith(prefix) else within


def _lookup(app, uri: str) -> str | None:
    manifest = _manifest_for(app)
    return manifest.get(_within_figures(app, uri)) or manifest.get(
        pathlib.PurePosixPath(uri).name
    )


def _stamp_sources(app, doctree, docname) -> None:
    """Give every image its generator, from the option or from the scan."""
    if app.builder.format != "html":
        return
    for node in doctree.findall(nodes.image):
        source = node.get("figure_source") or _lookup(app, node["uri"])
        if not source:
            continue
        node["figure_source"] = source
        if app.config.figure_source_show_link:
            _append_focus_link(node, source, app.config.figure_source_base)


def _append_focus_link(image: nodes.image, source: str, base: str) -> None:
    """A link to the source, out of the way until it is focused.

    Raw HTML, so only the HTML builder sees it.
    """
    parent = image.parent
    if parent is None:
        return
    label = html.escape(source)
    if base:
        href = html.escape(base + source, quote=True)
        markup = f'<a class="figure-source-fallback" href="{href}">Figure source: {label}</a>'
    else:
        markup = f'<span class="figure-source-fallback">Figure source: {label}</span>'
    parent.insert(parent.index(image) + 1, nodes.raw("", markup, format="html"))


def _install_translator(app) -> None:
    """Add ``data-figure-source`` to the ``<img>`` tags this build writes."""
    if app.builder.format != "html":
        return

    base = app.registry.translators.get(app.builder.name) or getattr(
        app.builder, "default_translator_class", None
    )
    if base is None:
        return

    class FigureSourceTranslator(base):  # type: ignore[valid-type, misc]
        def visit_image(self, node):
            super().visit_image(node)
            source = node.get("figure_source")
            # `visit_image` has just appended the <img ...> tag; annotate
            # that tag and nothing else.
            if source and self.body and self.body[-1].lstrip().startswith("<img"):
                attribute = f' data-figure-source="{html.escape(source, quote=True)}"'
                self.body[-1] = self.body[-1].replace("<img", "<img" + attribute, 1)

    app.set_translator(app.builder.name, FigureSourceTranslator, override=True)


def _expose_base(app, pagename, templatename, context, doctree) -> None:
    """Tell the page what prefix turns a script path into a link."""
    if app.builder.format != "html":
        return
    base = html.escape(app.config.figure_source_base, quote=True).replace("'", "")
    snippet = f"<script>window.__PID_FIGURE_SOURCE={{base:'{base}'}};</script>"
    context["metatags"] = context.get("metatags", "") + snippet


def _write_index(app, exception) -> None:
    """Write the whole mapping out, for tooling rather than for the page."""
    if exception is not None or app.builder.format != "html":
        return

    sources = {}
    for source_path, destination in getattr(app.builder, "images", {}).items():
        found = _lookup(app, source_path)
        if found:
            sources[destination] = found

    payload = {
        "base": app.config.figure_source_base,
        "sources": dict(sorted(sources.items())),
    }
    out = pathlib.Path(app.outdir) / "_static" / "figure-sources.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    total = len(getattr(app.builder, "images", {}))
    logger.info(f"figure sources: {len(sources)} of {total} images mapped to a generator")


def setup(app):
    app.add_directive("image", ImageWithSource, override=True)
    app.add_directive("figure", FigureWithSource, override=True)

    # Where the figures repository sits, relative to conf.py.
    app.add_config_value("figure_source_root", "figures", "env")
    # Prefix that turns a script path into a link. Empty means the path is
    # shown with nothing to click.
    app.add_config_value(
        "figure_source_base",
        "https://github.com/kgdunn/figures/blob/main/",
        "html",
    )
    # Add a keyboard-reachable link after each figure, hidden until focused.
    app.add_config_value("figure_source_show_link", False, "html")

    app.connect("builder-inited", _install_translator)
    app.connect("doctree-resolved", _stamp_sources)
    app.connect("html-page-context", _expose_base)
    app.connect("build-finished", _write_index)

    return {"version": "1.1", "parallel_read_safe": True, "parallel_write_safe": True}
