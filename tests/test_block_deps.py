"""What a "Run in browser" click runs before its example (my-extensions/block_deps.py).

Each test is a tiny chapter: examples in reading order. The last example's plan is what a
click on it runs first: earlier examples by index, or single statements. The cases pin
the rules; tools/check_run_deps.py checks the same plans on the book's chapters by running
them.
"""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
block_deps = importlib.import_module("my-extensions.block_deps")
dependencies, page_preludes = block_deps.dependencies, block_deps.page_preludes


def plan(*chapter: str) -> list:
    """The last example's plan."""
    return dependencies(list(chapter))[-1]


def test_unrelated_examples_are_skipped():
    assert plan("slow = expensive()", "x = 1", "print(x)") == [1]


def test_the_latest_binding_wins_and_brings_its_own_needs():
    assert plan("x = 1", "y = 2", "x = y + 1", "print(x)") == [1, 2]


def test_a_binding_inside_if_does_not_hide_an_earlier_one():
    assert plan("x = 1", "if flag:\n    x = 2", "print(x)") == [0, 1]


def test_in_place_changes_between_binding_and_use_are_needed():
    chapter = [
        "model = PLS()",
        "model.fit(X, y)",
        "model.n_components = 3",
        "show(model)",
        "print(model)",
    ]
    assert plan(*chapter) == [0, 1, 2, 3]


def test_a_name_bound_earlier_in_the_same_example_needs_nothing():
    assert plan("x = 1", "x = 2\nprint(x)") == []


def test_a_function_reads_its_globals_where_it_is_called():
    # y was computed while RATE was 1, so the later RATE = 2 is not needed for print(y) ...
    chapter = ["RATE = 1", "def f(t):\n    return RATE * t", "y = f(3)", "RATE = 2"]
    assert plan(*chapter, "print(y)") == [0, 1, 2]
    # ... but calling f now reads RATE as it is now.
    assert plan(*chapter, "print(f(1))") == [1, 3]


def test_a_function_called_inside_a_comprehension_of_its_own_example_reads_its_globals():
    # Chapter 5's worked study calls its own function inside a list comprehension.
    chapter = [
        "from lib import build",
        "def f(n):\n    return build(n)\nprint([f(n) for n in (1, 2)])",
    ]
    assert plan(*chapter) == ["from lib import build"]


def test_defining_a_function_needs_nothing_it_reads():
    assert plan("RATE = 1", "def f(t):\n    return RATE * t") == []


def test_a_call_to_a_chapter_function_counts_as_its_changes():
    chapter = ["data = []", "def add(v):\n    data.append(v)", "add(1)", "print(data)"]
    assert plan(*chapter) == [0, 1, 2]


def test_a_module_is_imported_rather_than_its_example_run():
    chapter = ["import numpy as np\nslow = np.linalg.svd(big)", "print(np.pi)"]
    assert plan(*chapter) == ["import numpy as np"]


def test_module_state_is_needed_without_being_named():
    # series.plot() reads pd.options.plotting.backend; the example never names pd.
    chapter = [
        'import pandas as pd\npd.options.plotting.backend = "plotly"\nslow = run()',
        "s.plot()",
    ]
    assert plan(*chapter) == ["import pandas as pd", "pd.options.plotting.backend = 'plotly'"]


def test_a_setting_before_its_own_import_uses_the_earlier_import():
    chapter = [
        "import pandas as pd",
        'pd.options.plotting.backend = "plotly"\nimport pandas as pd',
        "s.plot()",
    ]
    assert plan(*chapter) == ["import pandas as pd", "pd.options.plotting.backend = 'plotly'"]
    assert dependencies(chapter)[2][0] == "import pandas as pd"  # from example 0, first


def test_a_setting_that_is_not_a_constant_runs_its_example():
    chapter = [
        "import pandas as pd\nBACKEND = 'plotly'",
        "pd.options.plotting.backend = BACKEND",
        "s.plot()",
    ]
    assert plan(*chapter) == [0, 1]


def test_steps_keep_reading_order_between_settings_and_examples():
    chapter = [
        "import pandas as pd\nmode = 'matplotlib'",
        "pd.options.plotting.backend = mode",  # runs whole: not a constant
        'import pandas as pd\npd.options.plotting.backend = "plotly"',
        "s.plot()",
    ]
    assert plan(*chapter) == ["import pandas as pd", "pd.options.plotting.backend = 'plotly'"]


def test_legacy_random_draws_since_the_seed_are_needed():
    chapter = [
        "import numpy as np\nnp.random.seed(1)",
        "a = np.random.normal()",
        "b = np.random.normal()",
    ]
    assert plan(*chapter) == [0, 1]


def test_a_generator_object_is_not_global_state():
    chapter = [
        "import numpy as np",
        "rng = np.random.default_rng(1)",
        "other = np.random.default_rng(2)",
        "rng.normal()",
    ]
    assert plan(*chapter) == ["import numpy as np", 1]


def test_a_page_prelude_keeps_reading_order_across_its_examples():
    # Example 4 needs `slow` from 1, example 5 needs `names` from 2. Run per click, 1
    # would run after 2 and leave names == ["mid"] for example 5: the failure a real tab
    # showed on chapter 5's worked study. The page's prelude runs both, in order.
    chapter = ["names = ['old']", "slow = 1\nnames = ['mid']", "names = ['new']"]
    chapter += ["u = names", "v = slow", "print(names)"]
    pages = ["A", "A", "A", "B", "B", "B"]
    assert dependencies(chapter)[3:] == [[2], [1], [2]]
    assert page_preludes(chapter, pages) == {"A": [], "B": [1, 2]}


def test_a_page_prelude_merges_statements_and_drops_those_of_examples_it_runs():
    chapter = [
        'import pandas as pd\npd.options.plotting.backend = "plotly"\nx = 1',
        "s.plot()",
        "print(x)",
    ]
    preludes = page_preludes(chapter, ["A", "B", "B"])
    assert preludes["B"] == [0]  # example 0 runs whole, so its statements are not repeated


def test_an_example_that_does_not_parse_falls_back_to_the_whole_prefix():
    assert dependencies(["x = 1", "def broken(:", "y = 2", "print(y)"])[3] == [0, 1, 2]
