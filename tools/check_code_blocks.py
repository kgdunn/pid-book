#!/usr/bin/env python3
"""Execute every Python case in the book against the installed ``process_improve``.

The book demonstrates its computations with the ``process-improve`` package. This
script is the contract that keeps the two in step: it extracts every
``.. code-block:: python`` and every ``.. literalinclude::`` of a ``.py`` file,
orders them by each chapter's toctree, and executes them.

Execution model
---------------
* One chapter is one unit. Its blocks share a namespace and run in reading
  order, because sections continue each other (a model fitted in one section is
  reused in the next). A chapter therefore has to read top-to-bottom as a single
  linear script, which is also what a reader pasting the code expects.
* A ``literalinclude`` script is part of the chapter too: the text refers to
  what it defines ("the ``boards`` frame loaded above"), so it runs in the same
  namespace. Its working directory is a temporary folder, so any file it writes
  lands outside the repository.
* Each chapter runs in its own subprocess, so process-wide state one chapter
  sets (a pandas plotting backend, a random seed, matplotlib rcParams) cannot
  leak into the next. Within a chapter that state is kept on purpose: it is what
  a reader who follows the chapter has.
* Blocks are compiled with the RST path as filename and the true line offset, so
  tracebacks and warnings point at the line in the book source.
* Plotting is headless: matplotlib uses the Agg backend and ``Figure.show`` is a
  no-op for both matplotlib and plotly.
* Data sets read from ``openmv.net`` are fetched once into a cache directory
  (``.cache/openmv`` by default, override with ``PID_BOOK_DATA_CACHE``) and read
  from disk afterwards.
* A ``DeprecationWarning``, or any warning class defined by ``process_improve``
  (for example ``SpecificationWarning``), that points at the book's own code
  fails the block. Warnings raised deep inside third-party code are not
  attributed to the book and do not fail it. ``FutureWarning`` pointing at the
  book is reported as a notice.
* Comment lines that echo a ``print`` result (the book's idiom, e.g.
  ``# [0.255, 0.367, ...]``) are compared with the captured output. Mismatches
  are advisory unless ``--strict-output`` is given.

Markers
-------
An RST comment on the line before a directive (blank lines allowed between)
changes how that one block is handled::

    .. code-check: skip <reason>            illustrative fragment; never executed
    .. code-check: requires <module ...>    run only when the module(s) import
    .. code-check: allow-warnings <reason>  attributed warnings do not fail it

The same three, written ``.. code-check-file:``, apply to every block in the file.
That is the right granularity when one block's dependency decides the whole file:
the blocks share a namespace, so a file whose first block cannot run has nothing
later to run either. A per-block marker still wins for the block it sits above.

Usage
-----
::

    python tools/check_code_blocks.py                      # every chapter
    python tools/check_code_blocks.py --chapter least-squares-modelling
    python tools/check_code_blocks.py --file least-squares-modelling/enrichment-topics.rst
    python tools/check_code_blocks.py --list
    python tools/check_code_blocks.py --strict-output -v

Exit status is 1 when any block fails. ``tests/test_book_code.py`` wraps the
same runner for pytest (one test per chapter, so ``pytest -n auto`` runs the
chapters in parallel).
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import importlib.util
import io
import os
import re
import sys
import tempfile
import textwrap
import time
import traceback
import urllib.request
import warnings
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENTS = ROOT / "contents.rst"
CACHE_DIR = Path(os.environ.get("PID_BOOK_DATA_CACHE", ROOT / ".cache" / "openmv"))

# Directories that hold RST but are not book content.
EXCLUDED_DIRS = {"_build", "_static", "_templates", "docs", "figures", ".venv", ".git", "other", "temp", "DELETE"}

MARKER_RE = re.compile(r"^\s*\.\.\s+code-check:\s*(?P<kind>skip|requires|allow-warnings)\b\s*(?P<arg>.*?)\s*$")
FILE_MARKER_RE = re.compile(
    r"^\s*\.\.\s+code-check-file:\s*(?P<kind>skip|requires|allow-warnings)\b\s*(?P<arg>.*?)\s*$"
)
CODE_BLOCK_RE = re.compile(r"^\s*\.\.\s+code-block::\s*python\s*$")
LITERALINCLUDE_RE = re.compile(r"^\s*\.\.\s+literalinclude::\s*(?P<target>\S+)\s*$")
OPTION_RE = re.compile(r"^\s*:(?P<name>[\w-]+):\s*(?P<value>.*?)\s*$")
TOCTREE_RE = re.compile(r"^\s*\.\.\s+toctree::")
TOCTREE_TARGET_RE = re.compile(r"^.*<(?P<target>[^>]+)>\s*$")
OPENMV_RE = re.compile(r"^https?://openmv\.net/file/(?P<name>[^/?#]+)$")
PRINT_RE = re.compile(r"^\s*print\(")


# --------------------------------------------------------------------------- data model
@dataclasses.dataclass
class Block:
    """One executable case from the book."""

    path: Path  # the RST file the case appears in
    line: int  # 1-based line of the first source line (or of the directive, for includes)
    kind: str  # "code-block" or "literalinclude"
    source: str = ""
    marker: str | None = None
    marker_arg: str = ""
    include: Path | None = None  # resolved script path for literalinclude

    @property
    def label(self) -> str:
        rel = _relative(self.path)
        if self.kind == "literalinclude" and self.include is not None:
            return f"{rel}:{self.line} -> {_relative(self.include)}"
        return f"{rel}:{self.line}"


@dataclasses.dataclass
class Unit:
    """A chapter: an ordered list of RST files sharing one namespace."""

    name: str
    files: list[Path]
    blocks: list[Block]


@dataclasses.dataclass
class Outcome:
    block: Block
    status: str  # "passed", "skipped", "failed"
    detail: str = ""
    stdout: str = ""
    seconds: float = 0.0
    notices: list[str] = dataclasses.field(default_factory=list)
    output_mismatches: list[str] = dataclasses.field(default_factory=list)


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _indent_width(line: str) -> int:
    """Indentation in columns, with tabs expanded the way docutils does (8)."""
    expanded = line.expandtabs(8)
    return len(expanded) - len(expanded.lstrip(" "))


# --------------------------------------------------------------------------- extraction
def _marker_before(lines: list[str], idx: int) -> tuple[str | None, str]:
    k = idx - 1
    while k >= 0 and not lines[k].strip():
        k -= 1
    if k >= 0:
        m = MARKER_RE.match(lines[k])
        if m:
            return m["kind"], m["arg"]
    return None, ""


def _file_marker(lines: list[str]) -> tuple[str | None, str]:
    """A ``.. code-check-file:`` directive applies to every block in the file.

    Use it when one block's dependency decides the whole file: the blocks share a
    namespace, so a file whose first block cannot run has nothing later to run either.
    A per-block ``.. code-check:`` marker still wins for the block it sits above.
    """
    for line in lines:
        m = FILE_MARKER_RE.match(line)
        if m:
            return m["kind"], m["arg"]
    return None, ""


def _resolve_include(rst_path: Path, target: str) -> Path:
    if target.startswith("/"):
        return (ROOT / target.lstrip("/")).resolve()
    return (rst_path.parent / target).resolve()


def extract_blocks(rst_path: Path) -> list[Block]:
    """Return the Python cases in one RST file, in document order."""
    lines = rst_path.read_text(encoding="utf-8").splitlines()
    n = len(lines)
    file_marker, file_marker_arg = _file_marker(lines)
    blocks: list[Block] = []
    i = 0
    while i < n:
        line = lines[i]
        m_code = CODE_BLOCK_RE.match(line)
        m_inc = LITERALINCLUDE_RE.match(line)
        if not (m_code or m_inc):
            i += 1
            continue
        directive_indent = _indent_width(line)
        marker, marker_arg = _marker_before(lines, i)
        if marker is None:
            marker, marker_arg = file_marker, file_marker_arg

        # Directive options (":emphasize-lines: 3", ":lines: 1-10", ...).
        j = i + 1
        while j < n and lines[j].strip() and _indent_width(lines[j]) > directive_indent and OPTION_RE.match(lines[j]):
            j += 1

        if m_inc:
            target = m_inc["target"]
            if target.endswith(".py"):
                blocks.append(
                    Block(
                        path=rst_path,
                        line=i + 1,
                        kind="literalinclude",
                        marker=marker,
                        marker_arg=marker_arg,
                        include=_resolve_include(rst_path, target),
                    )
                )
            i = j
            continue

        # Body: after the blank line(s), every line indented deeper than the
        # directive belongs to the block; blank lines inside are kept.
        while j < n and not lines[j].strip():
            j += 1
        body_start = j
        body: list[str] = []
        while j < n:
            cur = lines[j]
            if not cur.strip():
                body.append("")
                j += 1
                continue
            if _indent_width(cur) <= directive_indent:
                break
            body.append(cur.expandtabs(8))
            j += 1
        while body and not body[-1].strip():
            body.pop()
        source = textwrap.dedent("\n".join(body)) + "\n"
        blocks.append(
            Block(path=rst_path, line=body_start + 1, kind="code-block", source=source, marker=marker, marker_arg=marker_arg)
        )
        i = j
    return blocks


# --------------------------------------------------------------------------- toctree ordering
def toctree_targets(index_path: Path) -> list[str]:
    """The entries of every toctree in ``index_path``, in order, as written."""
    lines = index_path.read_text(encoding="utf-8").splitlines()
    targets: list[str] = []
    i = 0
    while i < len(lines):
        if not TOCTREE_RE.match(lines[i]):
            i += 1
            continue
        indent = _indent_width(lines[i])
        j = i + 1
        while j < len(lines):
            cur = lines[j]
            if not cur.strip():
                j += 1
                continue
            if _indent_width(cur) <= indent:
                break
            stripped = cur.strip()
            if not stripped.startswith(":"):
                m = TOCTREE_TARGET_RE.match(stripped)
                targets.append(m["target"].strip() if m else stripped)
            j += 1
        i = j
    return targets


def chapter_files(index_path: Path) -> list[Path]:
    """Every RST file reachable from ``index_path``, depth-first in toctree order."""
    files = [index_path]
    for target in toctree_targets(index_path):
        candidate = (index_path.parent / target).with_suffix(".rst")
        if candidate.name == "index.rst" and candidate.exists():
            files.extend(chapter_files(candidate))
        elif candidate.exists():
            files.append(candidate)
    return files


def chapter_indexes() -> list[Path]:
    """The chapter ``index.rst`` files listed in ``contents.rst``, in reading order."""
    indexes = []
    for target in toctree_targets(CONTENTS):
        candidate = (ROOT / target).with_suffix(".rst")
        if candidate.name == "index.rst" and candidate.exists():
            indexes.append(candidate)
    return indexes


def _all_content_rst() -> list[Path]:
    out = []
    for path in ROOT.rglob("*.rst"):
        rel_parts = path.relative_to(ROOT).parts
        if rel_parts[0] in EXCLUDED_DIRS:
            continue
        out.append(path)
    return sorted(out)


def build_units() -> list[Unit]:
    """Chapters from the table of contents, plus one unit per RST file not reached by it."""
    units: list[Unit] = []
    seen: set[Path] = set()
    for index in chapter_indexes():
        files = chapter_files(index)
        seen.update(f.resolve() for f in files)
        blocks = [b for f in files for b in extract_blocks(f)]
        units.append(Unit(name=index.parent.name, files=files, blocks=blocks))
    for path in _all_content_rst():
        if path.resolve() in seen:
            continue
        blocks = extract_blocks(path)
        if blocks:
            units.append(Unit(name=f"orphan:{_relative(path)}", files=[path], blocks=blocks))
    return units


# --------------------------------------------------------------------------- environment
def fetch_dataset(url: str) -> Path:
    """Return a local copy of an openmv.net file, downloading it on first use."""
    name = OPENMV_RE.match(url)["name"]
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    target = CACHE_DIR / name
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "pid-book-code-check"})
        with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310 (fixed host)
            data = response.read()
        tmp = target.with_suffix(target.suffix + ".part")
        tmp.write_bytes(data)
        tmp.replace(target)
    return target


def _install_dataset_cache() -> None:
    try:
        import pandas as pd
    except ImportError:
        return
    original = pd.read_csv
    if getattr(original, "_pid_book_cached", False):
        return

    def read_csv(filepath_or_buffer, *args, **kwargs):  # type: ignore[no-untyped-def]
        if isinstance(filepath_or_buffer, str) and OPENMV_RE.match(filepath_or_buffer):
            filepath_or_buffer = str(fetch_dataset(filepath_or_buffer))
        return original(filepath_or_buffer, *args, **kwargs)

    read_csv._pid_book_cached = True  # type: ignore[attr-defined]
    read_csv.__doc__ = original.__doc__
    pd.read_csv = read_csv


def configure_environment() -> None:
    """Make plotting headless and route openmv.net reads through the cache. Idempotent."""
    os.environ.setdefault("MPLBACKEND", "Agg")
    with contextlib.suppress(ImportError):
        import matplotlib

        matplotlib.use("Agg", force=True)
        import matplotlib.pyplot as plt

        plt.show = lambda *args, **kwargs: None
    with contextlib.suppress(ImportError):
        import plotly.basedatatypes as basedatatypes
        import plotly.io as pio

        basedatatypes.BaseFigure.show = lambda self, *args, **kwargs: None
        pio.show = lambda *args, **kwargs: None
    _install_dataset_cache()


# --------------------------------------------------------------------------- warnings
def _is_library_category(category: type[Warning]) -> bool:
    module = getattr(category, "__module__", "") or ""
    return module == "process_improve" or module.startswith("process_improve.")


def _classify_warnings(caught: Iterable[warnings.WarningMessage], filename: str) -> tuple[list[str], list[str]]:
    """Split captured warnings attributed to ``filename`` into (failures, notices)."""
    failures, notices = [], []
    for w in caught:
        if w.filename != filename:
            continue
        text = f"{w.category.__name__} at line {w.lineno}: {w.message}"
        if issubclass(w.category, DeprecationWarning) or _is_library_category(w.category):
            failures.append(text)
        elif issubclass(w.category, FutureWarning):
            notices.append(text)
    return failures, notices


# --------------------------------------------------------------------------- expected output
def expected_output_lines(source: str) -> list[str]:
    """Comment lines that echo a print result: ``print(...)`` followed by ``# 1.23``."""
    lines = source.splitlines()
    expected: list[str] = []
    i = 0
    while i < len(lines):
        if not PRINT_RE.match(lines[i]):
            i += 1
            continue
        depth, j = 0, i
        while j < len(lines):  # step over a multi-line print(...)
            depth += lines[j].count("(") - lines[j].count(")")
            j += 1
            if depth <= 0:
                break
        while j < len(lines) and lines[j].strip().startswith("#"):
            text = lines[j].strip()[1:].strip()
            if re.search(r"\d", text) and not _looks_like_prose(text):
                expected.append(text)
            j += 1
        i = j
    return expected


def _looks_like_prose(text: str) -> bool:
    """A comment with several plain words is an explanation, not an echoed result."""
    words = re.findall(r"[A-Za-z]{2,}", text)
    return len(words) >= 5


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def output_mismatches(source: str, stdout: str) -> list[str]:
    printed = _normalise(stdout)
    return [exp for exp in expected_output_lines(source) if _normalise(exp) not in printed]


# --------------------------------------------------------------------------- running
def _format_exception(exc: BaseException) -> str:
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename != __file__]
    text = "".join(traceback.format_list(frames)) if frames else ""
    return text + "".join(traceback.format_exception_only(type(exc), exc))


MODULE_NAME_RE = re.compile(r"^[A-Za-z_]\w*(\.[A-Za-z_]\w*)*$")


def _required_modules(spec: str) -> list[str]:
    """Module names of a ``requires`` argument; anything after ``--`` is the reason."""
    return spec.split("--", 1)[0].split()


def _missing_modules(spec: str) -> list[str]:
    return [name for name in _required_modules(spec) if importlib.util.find_spec(name) is None]


def run_block(block: Block, namespace: dict, *, strict_output: bool = False) -> Outcome:
    """Execute one block inside ``namespace`` and classify the result."""
    if block.marker == "skip":
        return Outcome(block, "skipped", f"skip: {block.marker_arg or 'no reason given'}")
    if block.marker == "requires":
        names = _required_modules(block.marker_arg)
        malformed = [name for name in names if not MODULE_NAME_RE.match(name)]
        if not names or malformed:
            detail = (
                "malformed `requires` marker: expected module names, optionally followed by "
                f"`-- <reason>`; got {block.marker_arg!r}"
            )
            return Outcome(block, "failed", detail)
        missing = _missing_modules(block.marker_arg)
        if missing:
            return Outcome(block, "skipped", f"requires {' '.join(missing)} (not installed)")

    if block.kind == "literalinclude":
        assert block.include is not None
        if not block.include.exists():
            return Outcome(block, "failed", f"literalinclude target does not exist: {block.include}")
        source = block.include.read_text(encoding="utf-8")
        filename = _relative(block.include)
        target_ns = namespace
        workdir: contextlib.AbstractContextManager = tempfile.TemporaryDirectory()
    else:
        source = "\n" * (block.line - 1) + block.source  # keep the book's line numbers
        filename = _relative(block.path)
        target_ns = namespace
        workdir = contextlib.nullcontext(None)

    buffer = io.StringIO()
    started = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            with workdir as tmp, contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                cwd = contextlib.chdir(tmp) if tmp else contextlib.nullcontext()
                with cwd:
                    code = compile(source, filename, "exec")
                    exec(code, target_ns)  # noqa: S102 (this is the point of the script)
        except KeyboardInterrupt:
            raise
        except BaseException as exc:  # noqa: BLE001 (any failure is a failed block)
            return Outcome(block, "failed", _format_exception(exc), buffer.getvalue(), time.perf_counter() - started)
    elapsed = time.perf_counter() - started
    failures, notices = _classify_warnings(caught, filename)
    if failures and block.marker != "allow-warnings":
        detail = "warnings attributed to the book's code:\n  " + "\n  ".join(failures)
        return Outcome(block, "failed", detail, buffer.getvalue(), elapsed, notices)
    mismatches = output_mismatches(block.source, buffer.getvalue()) if block.kind == "code-block" else []
    status = "failed" if (mismatches and strict_output) else "passed"
    detail = ""
    if mismatches and strict_output:
        detail = "expected output not found in what the block printed:\n  " + "\n  ".join(mismatches)
    return Outcome(block, status, detail, buffer.getvalue(), elapsed, notices, mismatches)


def run_unit(unit: Unit, *, strict_output: bool = False, verbose: bool = False) -> list[Outcome]:
    namespace: dict = {"__name__": "__pid_book__"}
    outcomes = []
    for block in unit.blocks:
        outcome = run_block(block, namespace, strict_output=strict_output)
        outcomes.append(outcome)
        if verbose:
            print(f"  [{outcome.status:7s}] {block.label}  ({outcome.seconds:.1f}s)", flush=True)
    return outcomes


# --------------------------------------------------------------------------- reporting
def format_report(unit: Unit, outcomes: list[Outcome], *, only_failures: bool = False) -> str:
    counts = {s: sum(1 for o in outcomes if o.status == s) for s in ("passed", "skipped", "failed")}
    total_seconds = sum(o.seconds for o in outcomes)
    lines = [
        f"{unit.name}: {len(outcomes)} blocks, {counts['passed']} passed, "
        f"{counts['skipped']} skipped, {counts['failed']} failed ({total_seconds:.0f}s)"
    ]
    reported_skips: set[tuple[str, str]] = set()
    for o in outcomes:
        if o.status == "failed":
            lines.append(f"\nFAILED {o.block.label}")
            if o.block.kind == "code-block":
                excerpt = o.block.source.rstrip().splitlines()
                shown = excerpt[:12] + (["    ..."] if len(excerpt) > 12 else [])
                lines.extend("    | " + s for s in shown)
            lines.append(textwrap.indent(o.detail.rstrip(), "    "))
            if o.stdout.strip():
                tail = o.stdout.rstrip().splitlines()[-15:]
                lines.append("    -- output --")
                lines.extend("    " + s for s in tail)
        elif not only_failures:
            if o.status == "skipped":
                same = (_relative(o.block.path), o.detail)
                if same not in reported_skips:
                    reported_skips.add(same)
                    count = sum(
                        1
                        for other in outcomes
                        if other.status == "skipped"
                        and (_relative(other.block.path), other.detail) == same
                    )
                    suffix = f" ({count} blocks)" if count > 1 else ""
                    where = _relative(o.block.path) if count > 1 else o.block.label
                    lines.append(f"SKIPPED {where}{suffix}: {o.detail}")
            if o.output_mismatches:
                lines.append(f"OUTPUT? {o.block.label}: expected but not printed: {o.output_mismatches}")
            for notice in o.notices:
                lines.append(f"NOTICE  {o.block.label}: {notice}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- CLI
def _select_units(units: list[Unit], chapters: list[str], file: str | None, alone: bool) -> list[Unit]:
    if file:
        wanted = (ROOT / file).resolve()
        if alone:
            return [Unit(name=_relative(wanted), files=[wanted], blocks=extract_blocks(wanted))]
        for unit in units:
            resolved = [f.resolve() for f in unit.files]
            if wanted in resolved:
                cut = resolved.index(wanted) + 1
                files = unit.files[:cut]
                blocks = [b for b in unit.blocks if b.path.resolve() in set(resolved[:cut])]
                return [Unit(name=f"{unit.name} (up to {_relative(wanted)})", files=files, blocks=blocks)]
        sys.exit(f"{file} is not part of any chapter; use --alone to run it by itself")
    if chapters:
        by_name = {u.name: u for u in units}
        unknown = [c for c in chapters if c not in by_name]
        if unknown:
            sys.exit(f"unknown chapter(s): {unknown}; known: {sorted(by_name)}")
        return [by_name[c] for c in chapters]
    return units


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--chapter", action="append", default=[], help="chapter directory name (repeatable)")
    parser.add_argument("--file", help="run one RST file, after the files that precede it in its chapter")
    parser.add_argument("--alone", action="store_true", help="with --file: run the file in a fresh namespace")
    parser.add_argument("--list", action="store_true", help="list chapters, files and blocks; do not run")
    parser.add_argument("--strict-output", action="store_true", help="fail when an echoed print result does not match")
    parser.add_argument("-v", "--verbose", action="store_true", help="print one line per block as it runs")
    parser.add_argument("--in-process", action="store_true", help=argparse.SUPPRESS)  # set by the parent process
    args = parser.parse_args(argv)

    units = _select_units(build_units(), args.chapter, args.file, args.alone)
    if args.list:
        for unit in units:
            print(f"{unit.name}: {len(unit.blocks)} blocks in {len(unit.files)} files")
            for block in unit.blocks:
                flag = f"  [{block.marker} {block.marker_arg}]".rstrip() if block.marker else ""
                print(f"    {block.kind:14s} {block.label}{flag}")
        return 0

    # Whole chapters run in a child process each, so nothing leaks between them.
    # A single file (or an explicit --in-process) runs here.
    if not args.in_process and not args.file:
        return _run_in_subprocesses(units, args)

    configure_environment()
    failed_total = 0
    for unit in units:
        if args.verbose:
            print(f"\n== {unit.name} ==", flush=True)
        outcomes = run_unit(unit, strict_output=args.strict_output, verbose=args.verbose)
        print(format_report(unit, outcomes), flush=True)
        print()
        failed_total += sum(1 for o in outcomes if o.status == "failed")
    if failed_total:
        print(f"{failed_total} block(s) failed.")
        return 1
    print("All blocks passed.")
    return 0


def _run_in_subprocesses(units: list[Unit], args: argparse.Namespace) -> int:
    import subprocess

    flags = ["--in-process"]
    if args.strict_output:
        flags.append("--strict-output")
    if args.verbose:
        flags.append("-v")
    failed = 0
    for unit in units:
        result = subprocess.run(  # noqa: S603 (arguments are our own)
            [sys.executable, __file__, "--chapter", unit.name, *flags], check=False, cwd=ROOT
        )
        failed += result.returncode != 0
    if failed:
        print(f"{failed} chapter(s) had failing blocks.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
