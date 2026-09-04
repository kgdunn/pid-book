"""Every Python case in the book runs against the installed ``process_improve``.

One test per chapter (the unit of the checker), so ``pytest -n auto`` executes the
chapters in parallel. See ``tools/check_code_blocks.py`` for the execution model
and the ``.. code-check:`` markers.
"""

import pytest
from check_code_blocks import build_units, configure_environment, format_report, run_unit

UNITS = build_units()


@pytest.fixture(scope="session", autouse=True)
def _headless_plotting_and_data_cache():
    configure_environment()


@pytest.mark.parametrize("unit", UNITS, ids=[u.name for u in UNITS])
def test_chapter_code_runs(unit):
    outcomes = run_unit(unit)
    if any(o.status == "failed" for o in outcomes):
        pytest.fail(format_report(unit, outcomes, only_failures=True), pytrace=False)
