"""The "Run in browser" buttons (my-extensions/run_in_browser.py).

A button is placed by matching the rendered code against the blocks the code
checker extracts. If that match silently stops working (a docutils change to
how tabs are expanded, say), the page still builds, just without buttons. These
tests pin the match and the manifest the page reads.
"""

import ast
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
run_in_browser = importlib.import_module("my-extensions.run_in_browser")


def test_key_ignores_indentation_tabs_and_blank_lines():
    in_rst = "\t\timport numpy as np\n\n\t\tx = np.arange(3)\n\t\tif x.any():\n\t\t    print(x)\n"
    rendered = "import numpy as np\nx = np.arange(3)\nif x.any():\n    print(x)"
    assert run_in_browser._key(in_rst) == run_in_browser._key(rendered)


def test_key_keeps_relative_indentation():
    assert run_in_browser._key("if a:\n    b()") != run_in_browser._key("if a:\nb()")


def configured_chapters():
    tree = ast.parse((ROOT / "conf.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and getattr(node.targets[0], "id", "") == "run_in_browser_chapters"
        ):
            return ast.literal_eval(node.value)
    return []


def test_manifest_lists_the_chapter_in_reading_order():
    chapters = configured_chapters()
    assert chapters, "conf.py enables at least one chapter"
    app = SimpleNamespace(
        builder=SimpleNamespace(name="html"),
        config=SimpleNamespace(run_in_browser_chapters=chapters),
        srcdir=str(ROOT),
    )
    run_in_browser.collect(app)
    for chapter in chapters:
        manifest = run_in_browser._CHAPTERS[chapter]
        blocks = manifest["blocks"]
        assert blocks, chapter
        assert all(b["doc"].startswith(f"{chapter}/") for b in blocks)
        # Every openmv.net read has a same-origin copy, used if openmv.net is unreachable.
        for url in (u for b in blocks for u in run_in_browser.OPENMV_URL_RE.findall(b["source"])):
            assert manifest["datasets"][url] == f"data/{url.rsplit('/', 1)[1]}"
