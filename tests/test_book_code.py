"""Every Python case in the book runs against the installed ``process_improve``.

One test per chapter, each in its own subprocess (the checker's unit of isolation),
so ``pytest -n auto`` executes the chapters in parallel and process-wide state set
by one chapter cannot leak into another. See ``tools/check_code_blocks.py`` for the
execution model and the ``.. code-check:`` markers.

``--strict-output`` is on here, so a comment that echoes a ``print`` result and no
longer matches what the block prints fails the chapter. That is the check that
catches a number going stale while the code around it still runs.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from check_code_blocks import ROOT, build_units

CHECKER = Path(ROOT) / "tools" / "check_code_blocks.py"
UNITS = [u for u in build_units() if u.blocks]


@pytest.mark.parametrize("unit", UNITS, ids=[u.name for u in UNITS])
def test_chapter_code_runs(unit):
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--chapter", unit.name, "--in-process", "--strict-output"],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    if result.returncode != 0:
        pytest.fail(result.stdout + result.stderr, pytrace=False)
