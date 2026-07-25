"""Record, for every figure, the script that drew it.

Readers who want to reproduce a figure need the code behind it. This
extension carries that link from the source tree into the built HTML,
without putting it in the ``:alt:`` field, which belongs to screen readers
and to people whose images failed to load.

Two mechanisms, in order of precedence:

1. An explicit ``:source:`` option on an ``image`` or ``figure`` directive::

       .. figure:: ../figures/doe/COST-contours.png
           :source: doe/doe_chapter_figures.py
           :alt: Contour plot illustrating the one-factor-at-a-time search path

   The path is relative to the root of the figures repository.

2. A manifest derived from the figures repository itself, used for every
   image with no ``:source:`` option. Each generator script names the files
   it writes, so scanning the scripts for quoted image filenames recovers
   the mapping for the whole tree at once, and keeps recovering it as
   figures are added. See :func:`build_manifest`.

Both end up in ``_static/figure-sources.json``, written at the end of an
HTML build and keyed by the filename Sphinx gave the image in ``_images``,
so a browser can look up ``basename(img.src)``. Nothing is emitted for the
LaTeX, text or epub builders, and nothing about this makes a network
request: the JSON is a static asset served from the same site.

The companion ``_static/js/figure-source.js`` reads the file.
"""

from __future__ import annotations

import json
import pathlib
import re

from sphinx.util import logging

from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Figure, Image

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
                for image in node.findall(condition=lambda n: n.tagname == "image"):
                    image["figure_source"] = source
                if node.tagname == "image":
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
                    .relative_to(figures_root).as_posix()
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


def _collect_explicit(app, doctree, docname) -> None:
    """Remember any ``:source:`` option, keyed by the image's source path."""
    registry = _ensure_registry(app.env)
    for node in doctree.findall(condition=lambda n: n.tagname == "image"):
        source = node.get("figure_source")
        if source:
            registry[node["uri"]] = source


def _ensure_registry(env) -> dict[str, str]:
    """The per-build registry of explicit ``:source:`` options.

    Keyed by the image's path rather than by document, so rebuilding one
    document rewrites its entries rather than leaving stale ones behind.
    """
    if not hasattr(env, "figure_source_explicit"):
        env.figure_source_explicit = {}
    return env.figure_source_explicit


def _write_manifest(app, exception) -> None:
    if exception is not None or app.builder.format != "html":
        return

    figures_root = (pathlib.Path(app.confdir) / app.config.figure_source_root).resolve()
    by_name = build_manifest(figures_root)
    explicit = getattr(app.env, "figure_source_explicit", {})

    # Only ship the images this build actually copied: `builder.images` maps
    # the path used in the source tree to the filename written into
    # `_images`, which is what a browser sees in `src`.
    prefix = app.config.figure_source_root.strip("/") + "/"
    sources = {}
    for source_path, destination in getattr(app.builder, "images", {}).items():
        given = explicit.get(source_path) or explicit.get("/" + source_path)
        # Prefer the full path within the figures repository, falling back to
        # the filename alone for images the mapping only knows by name. The
        # builder records the path as written in the source, so a document in
        # a subdirectory contributes leading `../` segments.
        within = re.sub(r"^(?:\.\./)+", "", source_path.lstrip("/"))
        within = within[len(prefix):] if within.startswith(prefix) else within
        derived = by_name.get(within) or by_name.get(pathlib.PurePosixPath(source_path).name)
        if given or derived:
            sources[destination] = given or derived

    payload = {"base": app.config.figure_source_base, "sources": dict(sorted(sources.items()))}
    out = pathlib.Path(app.outdir) / "_static" / "figure-sources.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    total = len(getattr(app.builder, "images", {}))
    logger.info(
        f"figure sources: {len(sources)} of {total} images mapped to a generator"
    )


def setup(app):
    app.add_directive("image", ImageWithSource, override=True)
    app.add_directive("figure", FigureWithSource, override=True)

    # Where the figures repository sits, relative to conf.py.
    app.add_config_value("figure_source_root", "figures", "env")
    # Prefix for turning a script path into a link. Empty means the panel
    # shows the path only, with nothing to click.
    app.add_config_value(
        "figure_source_base",
        "https://github.com/kgdunn/figures/blob/main/",
        "html",
    )

    app.connect("doctree-resolved", _collect_explicit)
    app.connect("build-finished", _write_manifest)

    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
