"""Put a "Run in browser" button under the book's Python examples.

The reader clicks, and the example runs in their own browser tab with
`Pyodide <https://pyodide.org>`_ (CPython compiled to WebAssembly). Nothing to
install, and nothing leaves the reader's machine. Output, plots and errors appear
under the code.

Which blocks, in which order
----------------------------
The button runs exactly what ``tools/check_code_blocks.py`` runs in CI, because
this extension asks the checker for the blocks rather than finding them again.
That contract (see ``CLAUDE.md``) says a chapter is one linear script: blocks
share one namespace and may use names that earlier blocks, on earlier pages of
the chapter, defined. A reader who lands on a later page and clicks the fifth
example would otherwise hit a ``NameError``. So the page runs, first and
quietly, every earlier block of the chapter that has not run yet in this tab,
and says it did. ``.. code-check: skip`` blocks get no button and are never run.

What is built
-------------
* ``_static/run/<chapter>.json``: the chapter's blocks in reading order, with
  the source of each ``literalinclude``-d script inlined, and the echoed print
  results the checker compares (``# 0.255``), so the page can say whether the
  reader's run reproduced the book.
* ``_static/run/data/<name>``: a copy of every ``openmv.net`` data file the
  chapter reads. Pyodide has no sockets, so the worker sends
  ``pd.read_csv("https://openmv.net/...")`` through the browser's own fetch;
  openmv.net answers with CORS headers, so the file comes from there and counts
  as a download. The same-origin copy is used only when that request fails (an
  outage, say).
* A button, as raw HTML, after each runnable literal block. The post-transform
  runs before ``code_collapse`` (priority 880 < 900), so the collapse wraps the
  code alone and the button stays visible while the code is folded away.

Like ``code_collapse``, the transform is gated on the builder *name*, so the
LaTeX, text and epub builds never see a button.

Loading Python from a CDN happens only when a reader clicks: a page that is
only read downloads nothing extra. See ``privacy.rst``.

Configuration
-------------
``run_in_browser_chapters`` (default ``[]``)
    Chapter directory names (as in ``contents.rst``) that get buttons.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING, Any

from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging

if TYPE_CHECKING:
    from types import ModuleType

    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)

HTML_BUILDERS = ("html", "dirhtml", "singlehtml")
OPENMV_URL_RE = re.compile(r"https?://openmv\.net/file/[\w.-]+")

#: Filled at builder-inited: chapter name -> manifest dict, and docname -> chapter.
_CHAPTERS: dict[str, dict[str, Any]] = {}
_DOC_CHAPTER: dict[str, str] = {}


def _checker(srcdir: Path) -> ModuleType:
    """Import ``tools/check_code_blocks.py``, the single source of truth for blocks."""
    spec = importlib.util.spec_from_file_location(
        "pid_check_code_blocks", srcdir / "tools" / "check_code_blocks.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # its dataclasses look their module up here
    spec.loader.exec_module(module)
    return module


def _key(source: str) -> list[str]:
    """Compare code by its lines, ignoring indentation, tabs and blank lines."""
    text = textwrap.dedent(source.expandtabs(8))
    return [line.rstrip() for line in text.splitlines() if line.strip()]


def collect(app: Sphinx) -> None:
    """Ask the checker for each enabled chapter's blocks, in reading order."""
    if app.builder.name not in HTML_BUILDERS or not app.config.run_in_browser_chapters:
        return
    srcdir = Path(app.srcdir)
    checker = _checker(srcdir)
    wanted = set(app.config.run_in_browser_chapters)
    for unit in checker.build_units():
        if unit.name not in wanted:
            continue
        blocks = []
        for block in unit.blocks:
            if block.kind == "literalinclude":
                if block.include is None or not block.include.exists():
                    logger.warning("run_in_browser: %s includes a missing script", block.label)
                    continue
                source = block.include.read_text(encoding="utf-8")
            else:
                source = block.source
            docname = block.path.resolve().relative_to(srcdir.resolve()).with_suffix("").as_posix()
            blocks.append(
                {
                    "doc": docname,
                    "line": block.line,
                    "source": source,
                    "skip": block.marker == "skip",
                    "requires": block.marker_arg if block.marker == "requires" else "",
                    "expected": checker.expected_output_lines(source),
                }
            )
            _DOC_CHAPTER[docname] = unit.name
        urls = sorted({url for b in blocks for url in OPENMV_URL_RE.findall(b["source"])})
        _CHAPTERS[unit.name] = {
            "chapter": unit.name,
            "blocks": blocks,
            "datasets": {url: f"data/{url.rsplit('/', 1)[1]}" for url in urls},
            "_fetch": checker.fetch_dataset,
        }
        wanted.discard(unit.name)
    for missing in sorted(wanted):
        logger.warning("run_in_browser: no chapter named %r in contents.rst", missing)


class AddRunButtons(SphinxPostTransform):
    """Insert a run button after every runnable Python block of an enabled chapter."""

    builders = HTML_BUILDERS
    default_priority = 880  # before code_collapse (900), which then wraps only the code

    def run(self, **kwargs: Any) -> None:
        docname = self.env.docname
        chapter = _DOC_CHAPTER.get(docname)
        if chapter is None:
            return
        # (index in chapter, comparison key) for this page's runnable blocks, in order.
        todo = [
            (i, _key(b["source"]))
            for i, b in enumerate(_CHAPTERS[chapter]["blocks"])
            if b["doc"] == docname and not b["skip"]
        ]
        for literal in list(self.document.findall(nodes.literal_block)):
            key = _key(literal.astext())
            match = next((pos for pos, (_, k) in enumerate(todo) if k == key), None)
            if match is None:
                continue
            index, _ = todo.pop(match)
            html = (
                '<div class="pid-run" data-pagefind-ignore>'
                f'<button type="button" class="pid-run__button" data-chapter="{chapter}" data-block="{index}">'
                "Run in browser</button>"
                '<div class="pid-run__out" aria-live="polite" hidden></div></div>'
            )
            parent = literal.parent
            parent.insert(parent.index(literal) + 1, nodes.raw("", html, format="html"))
        for index, _ in todo:
            block = _CHAPTERS[chapter]["blocks"][index]
            logger.warning(
                "run_in_browser: no rendered block matched %s.rst:%s", block["doc"], block["line"]
            )


def add_assets(
    app: Sphinx, pagename: str, templatename: str, context: dict, doctree: nodes.document
) -> None:
    """Load the runner's script and stylesheet only on pages that have a button."""
    if pagename in _DOC_CHAPTER:
        app.add_js_file("js/run-in-browser.js", defer="defer")
        app.add_css_file("css/run-in-browser.css")


def write_manifests(app: Sphinx, exception: Exception | None) -> None:
    """Write each chapter's block list and copy the data files it reads."""
    if exception is not None or app.builder.name not in HTML_BUILDERS:
        return
    out = Path(app.outdir) / "_static" / "run"
    for name, chapter in _CHAPTERS.items():
        (out / "data").mkdir(parents=True, exist_ok=True)
        for url, rel in chapter["datasets"].items():
            try:
                shutil.copyfile(chapter["_fetch"](url), out / rel)
            except OSError as exc:
                logger.warning(
                    "run_in_browser: could not fetch %s for the browser runner (%s)", url, exc
                )
        public = {k: v for k, v in chapter.items() if not k.startswith("_")}
        (out / f"{name}.json").write_text(json.dumps(public), encoding="utf-8")


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("run_in_browser_chapters", [], "html")
    app.connect("builder-inited", collect)
    app.connect("html-page-context", add_assets)
    app.connect("build-finished", write_manifests)
    app.add_post_transform(AddRunButtons)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
