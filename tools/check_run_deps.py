#!/usr/bin/env python3
"""Check that a "Run in browser" page leaves each example exactly as the whole chapter does.

A page's first click runs the page's prelude (``my-extensions/block_deps.py``): the earlier
examples, and single statements, that give the page's examples the names and state they
read. Each click then runs the page's own earlier examples, in reading order. This script
proves that on the book itself:

* the chapter runs once, start to end, and every example is fingerprinted: what it
  prints (with its last expression's repr, as the browser shows it), its error, and a
  hash of each Plotly and matplotlib figure it draws;
* each page then runs in a fresh interpreter, as a reader clicking down it would: its
  prelude, then its examples in order, each of which must match its fingerprint;
* the chapter runs a second time, in another interpreter, to find examples whose output
  is random (an unseeded draw, seaborn's bootstrap). For those only the error and the
  kinds of figure are compared.

Usage::

    python tools/check_run_deps.py                       # the chapters with buttons
    python tools/check_run_deps.py --chapter least-squares-modelling

Exit status is 1 when any example differs. ``make check-run-deps`` runs it in the same
environment as ``make check-code``.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import importlib
import importlib.util
import io
import json
import multiprocessing as mp
import os
import re
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
page_preludes = importlib.import_module("my-extensions.block_deps").page_preludes

ADDRESS = re.compile(r"0x[0-9a-fA-F]+")
# statsmodels' summary() prints the wall-clock date and time.
CLOCK = re.compile(r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{2} \w{3} \d{4}\b|\b\d{2}:\d{2}:\d{2}\b")
FIGURES: list[str] = []


def _checker():
    spec = importlib.util.spec_from_file_location(
        "pid_check_code_blocks", ROOT / "tools" / "check_code_blocks.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def chapter_sources(chapter: str) -> list[tuple[str, str, str]]:
    """(label, page, source) of the chapter's runnable examples, in reading order."""
    unit = next((u for u in _checker().build_units() if u.name == chapter), None)
    if unit is None:
        raise SystemExit(f"no chapter named {chapter!r} in contents.rst")
    return [
        (
            b.label,
            str(b.path),
            b.include.read_text(encoding="utf-8") if b.kind == "literalinclude" else b.source,
        )
        for b in unit.blocks
        if b.marker != "skip"
    ]


def _setup() -> None:
    os.chdir(tempfile.mkdtemp())  # a literalinclude-d script may write files
    _checker().configure_environment()
    import plotly.basedatatypes
    import plotly.io

    def show(fig, *args, **kwargs):
        # Sorted keys: Plotly orders some template keys by the per-process hash seed.
        canonical = json.dumps(json.loads(fig.to_json()), sort_keys=True)
        FIGURES.append("plotly:" + hashlib.md5(canonical.encode()).hexdigest())  # noqa: S324

    plotly.basedatatypes.BaseFigure.show = show
    plotly.io.show = show


def _flush_matplotlib() -> None:
    plt = sys.modules.get("matplotlib.pyplot")
    for num in plt.get_fignums() if plt else []:
        buffer = io.BytesIO()
        plt.figure(num).savefig(buffer, format="png", dpi=40)
        FIGURES.append("png:" + hashlib.md5(buffer.getvalue()).hexdigest())  # noqa: S324
    if plt:
        plt.close("all")


def _display(value) -> None:
    """Show a last expression as the browser does (keep in step with _display in the worker)."""
    first = (
        value.flat[0]
        if type(value).__name__ == "ndarray" and value.dtype == object and value.size
        else value
    )
    if value is None or type(first).__module__.partition(".")[0] in ("matplotlib", "seaborn"):
        return
    if isinstance(value, dict) and {"data", "layout"} <= value.keys():
        import plotly.graph_objects as go

        value = go.Figure(value)
    if hasattr(value, "to_plotly_json"):
        value.show()
    else:
        print(repr(value))


def _run(source: str, namespace: dict) -> dict:
    FIGURES.clear()
    out, error, started = io.StringIO(), None, time.perf_counter()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            tree = ast.parse(source)
            last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
            exec(compile(tree, "<example>", "exec"), namespace)  # noqa: S102
            if last is not None:
                _display(eval(compile(ast.Expression(last.value), "<example>", "eval"), namespace))  # noqa: S307
    except BaseException as exc:  # noqa: BLE001 (any failure is part of the fingerprint)
        error = f"{type(exc).__name__}: {exc}"
    _flush_matplotlib()
    stdout = CLOCK.sub("<clock>", ADDRESS.sub("0x?", out.getvalue()))
    return {
        "stdout": stdout,
        "error": error,
        "figures": list(FIGURES),
        "seconds": time.perf_counter() - started,
    }


def _page(job: tuple[str, list, list[int]]) -> dict[int, dict]:
    """A page's examples, run in this fresh interpreter after the page's prelude."""
    chapter, prelude, members = job
    sources = [s for _, _, s in chapter_sources(chapter)]
    _setup()
    namespace = {"__name__": "__main__"}
    for step in prelude:
        if isinstance(step, str):
            exec(step, namespace)  # noqa: S102 (an import, or a setting)
        else:
            _run(sources[step], namespace)
    return {i: _run(sources[i], namespace) for i in members}


def _whole_chapter(chapter: str) -> list[dict]:
    _setup()
    namespace = {"__name__": "__main__"}
    return [_run(s, namespace) for _, _, s in chapter_sources(chapter)]


def check(chapter: str) -> tuple[list[dict], str]:
    """The examples that differ when their page runs alone, and a one-line summary."""
    blocks = chapter_sources(chapter)
    pages = [page for _, page, _ in blocks]
    preludes = page_preludes([s for _, _, s in blocks], pages)
    members = {page: [i for i, p in enumerate(pages) if p == page] for page in preludes}
    jobs = [(chapter, preludes[page], members[page]) for page in preludes]
    # Every run, the whole-chapter ones included, gets a fresh interpreter: no state leaks.
    with mp.get_context("spawn").Pool(min(4, os.cpu_count() or 1), maxtasksperchild=1) as pool:
        full, again = (pool.apply_async(_whole_chapter, (chapter,)) for _ in range(2))
        results = {i: r for page in pool.imap_unordered(_page, jobs) for i, r in page.items()}
        full, again = full.get(), again.get()
    seconds = [f.pop("seconds") for f in full]
    for r in [*again, *results.values()]:
        r.pop("seconds")
    random_output = {i for i in range(len(blocks)) if again[i] != full[i]}

    def shape(r: dict) -> tuple:
        return r["error"], [f.partition(":")[0] for f in r["figures"]]

    bad = [
        {"example": blocks[i][0], "page_prelude": preludes[pages[i]],
         "whole_chapter": full[i], "page_alone": got}
        for i, got in sorted(results.items())
        if (shape(got) != shape(full[i]) if i in random_output else got != full[i])
    ]  # fmt: skip
    # The slowest first click: the page's last example, after its prelude and the page.
    before = max(sum(seconds[: m[-1]]) for m in members.values())
    after = max(
        sum(seconds[j] for j in preludes[page] if isinstance(j, int)) + sum(seconds[m[0] : m[-1]])
        for page, m in members.items()
    )
    summary = (
        f"{chapter}: {len(blocks)} examples on {len(preludes)} pages, {len(bad)} differ "
        f"({len(random_output)} with random output, compared by error and figure kinds); "
        f"slowest first click {before:.1f}s -> {after:.1f}s"
    )
    return bad, summary


def _enabled_chapters() -> list[str]:
    tree = ast.parse((ROOT / "conf.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and getattr(node.targets[0], "id", "") == "run_in_browser_chapters"
        ):
            return ast.literal_eval(node.value)
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--chapter", action="append", default=[], help="chapter directory name (repeatable)"
    )
    parser.add_argument(
        "--report", type=Path, help="write the differing examples to this JSON file"
    )
    args = parser.parse_args(argv)
    failures = []
    for chapter in args.chapter or _enabled_chapters():
        bad, summary = check(chapter)
        print(summary, flush=True)
        failures += bad
    for f in failures:
        print(f"DIFFERS {f['example']} after its plan {f['plan']}")
    if args.report:
        args.report.write_text(json.dumps(failures, indent=1), encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
