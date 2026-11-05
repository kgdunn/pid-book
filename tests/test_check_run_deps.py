"""The report of the page-by-page gate (tools/check_run_deps.py).

Running a chapter takes minutes, so `check` is replaced by a stub that returns one
differing example: what is pinned here is that the gate names it and writes it out.
"""

import json

import check_run_deps


def test_a_differing_example_is_named_and_written_to_the_report(monkeypatch, capsys, tmp_path):
    bad = {
        "example": "chapter/page.rst:12",
        "page_prelude": [0, "import numpy as np"],
        "whole_chapter": {"stdout": "1\n"},
        "page_alone": {"stdout": "2\n"},
    }
    monkeypatch.setattr(check_run_deps, "check", lambda chapter: ([bad], f"{chapter}: 1 differs"))
    report = tmp_path / "report.json"

    assert check_run_deps.main(["--chapter", "chapter", "--report", str(report)]) == 1
    out = capsys.readouterr().out
    assert "DIFFERS chapter/page.rst:12 after its page prelude [0, 'import numpy as np']" in out
    assert json.loads(report.read_text(encoding="utf-8")) == [bad]
