"""Which earlier examples of a chapter one example needs, read from the code.

A chapter is one linear script (see ``CLAUDE.md``), so the "Run in browser" button of a
late example used to run every earlier example of the chapter first: minutes, on the
pages after chapter 5's OMARS study, most of it for names the example never reads. This
module works out, from the source alone, a shorter *plan* that leaves the example the
same names and state the whole prefix would:

* A name is needed if the example reads it before binding it. The latest earlier
  example that binds it unconditionally (a top-level statement, not inside ``if``,
  ``for`` or ``try``) provides it and is run, after what it needs in turn; so is every
  example in between that may change the object in place (``x.attr = ...``,
  ``x[...] = ...``, ``x.method(...)``, ``f(x)``, or a call to a chapter function whose
  body does that).
* A function reads its free names when it runs, so they are needed wherever the
  function is referenced. Lambdas and functions defined inside ``if``/``for`` are
  resolved at every point up to the example, which is always safe.
* A module (a name the chapter binds only by import) is stateless, so only its import
  statement is run, not the example it came from.
* Global state set through a module (``pd.options.plotting.backend = "plotly"``,
  ``np.random.seed(...)``, ``set_option``, ``style.use``) is read by library code without
  the example naming it (``series.plot()``), so every example needs its latest setting.
  A setting that is a plain constant runs as that one statement; any other runs its
  example. Draws from the legacy ``np.random`` generator are needed by an example that
  draws from it too.

A plan runs those examples and statements in reading order, from a fresh interpreter.
In the browser a page's examples share one interpreter, so the page uses
:func:`page_preludes`: the plans of all its examples, merged and cut to what comes before
the page, then the page's examples in order. ``tools/check_run_deps.py`` checks that on
the book's chapters: each page, run that way in a fresh interpreter, must leave every one
of its examples printing and drawing exactly what it does after the whole chapter.
"""

from __future__ import annotations

import ast
import builtins
from dataclasses import dataclass, field

BUILTINS = frozenset(dir(builtins))
#: Calls on a module that change state other examples can see.
STATEFUL_CALLS = frozenset(
    {
        "filterwarnings", "register", "reset_option", "rc", "seed", "set_context", "set_option",
        "set_palette", "set_printoptions", "set_state", "set_style", "set_theme", "simplefilter", "use",
    }
)  # fmt: skip
#: Pseudo-names stand for global state, which code reads without naming it.
STATE = "state:"
GLOBAL_RNG = "state:legacy np.random"
RNG_FACTORIES = frozenset(
    {"BitGenerator", "Generator", "PCG64", "RandomState", "SeedSequence", "default_rng"}
)
SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)
COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


@dataclass
class _Facts:
    """What one example does with names, read from its code."""

    #: Bound unconditionally at top level, and bound anywhere at module scope.
    kills: set[str] = field(default_factory=set)
    binds: set[str] = field(default_factory=set)
    #: May be changed in place.
    touches: set[str] = field(default_factory=set)
    #: Read before the example binds them; and every name read, even after binding it.
    uses: set[str] = field(default_factory=set)
    refs: set[str] = field(default_factory=set)
    #: Free names of each top-level def or class, and of every other nested scope.
    functions: dict[str, set[str]] = field(default_factory=dict)
    late: set[str] = field(default_factory=set)
    #: What each function's body may change, and the names the example calls directly.
    changes: dict[str, set[str]] = field(default_factory=dict)
    calls: set[str] = field(default_factory=set)
    #: Name -> (line, statement) for an import, or a constant setting of global state.
    statements: dict[str, tuple[int, str]] = field(default_factory=dict)


def _root(node: ast.AST) -> str | None:
    """The base name of ``x``, ``x.a.b``, ``x[...].c``, ``x.f().g``."""
    while isinstance(node, (ast.Attribute, ast.Subscript, ast.Call)):
        node = node.func if isinstance(node, ast.Call) else node.value
    return node.id if isinstance(node, ast.Name) else None


def _targets(target: ast.AST) -> set[str]:
    """Names an assignment target binds; attribute and subscript targets mutate instead."""
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        return set().union(*(_targets(t) for t in target.elts))
    if isinstance(target, ast.Starred):
        return _targets(target.value)
    return set()


def _imported(stmt: ast.Import | ast.ImportFrom) -> set[str]:
    return {(a.asname or a.name).split(".")[0] for a in stmt.names if a.name != "*"}


def _modules(trees: list[ast.Module]) -> frozenset[str]:
    """Names the chapter binds only by import."""
    imported, other = set(), set()
    for node in (n for tree in trees for n in ast.walk(tree)):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported |= _imported(node)
        elif isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
            other.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            other.add(node.name)
    return frozenset(imported - other)


def _free(scope: ast.AST) -> set[str]:
    """Names a function, lambda, class or comprehension reads without binding them itself."""
    bound, loaded = set(), set()
    if isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        a = scope.args
        bound |= {x.arg for x in [*a.posonlyargs, *a.args, *a.kwonlyargs, a.vararg, a.kwarg] if x}
    body = [scope] if isinstance(scope, COMPREHENSIONS) else scope.body
    for node in (
        n for stmt in (body if isinstance(body, list) else [body]) for n in ast.walk(stmt)
    ):
        if isinstance(node, ast.Name):
            (loaded if isinstance(node.ctx, ast.Load) else bound).add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bound |= _imported(node)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
    return loaded - bound - BUILTINS


def _outer(node: ast.AST):
    """ast.walk, but a nested scope yields itself and only what runs when it is defined."""
    todo = [node]
    while todo:
        n = todo.pop()
        yield n
        if isinstance(n, SCOPES):  # its body runs when called, not now
            todo += [*getattr(n, "decorator_list", []), *getattr(n, "bases", [])]
            if not isinstance(n, ast.ClassDef):
                todo += [*n.args.defaults, *(d for d in n.args.kw_defaults if d)]
        elif not isinstance(n, COMPREHENSIONS):  # a comprehension is read whole, by _free
            todo.extend(ast.iter_child_nodes(n))


def _changes(node: ast.AST, modules: frozenset[str]) -> set[str]:
    """Names whose objects the code in ``node`` may change in place, or rebinds globally."""
    changed: set[str | None] = set()
    for n in ast.walk(node):
        if isinstance(n, (ast.Attribute, ast.Subscript)) and not isinstance(n.ctx, ast.Load):
            changed.add(_root(n))
        elif isinstance(n, ast.Call):
            if isinstance(n.func, ast.Attribute):
                changed.add(_root(n.func))
            changed |= {
                a.id for a in [*n.args, *(k.value for k in n.keywords)] if isinstance(a, ast.Name)
            }
        elif isinstance(n, ast.Global):
            changed |= set(n.names)
    return {c for c in changed if c and c not in modules}


def _facts(tree: ast.Module, modules: frozenset[str]) -> _Facts:
    f = _Facts()
    for stmt in tree.body:
        new: set[str] = set()
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            new = _imported(stmt)
            f.statements |= dict.fromkeys(new, (stmt.lineno, ast.unparse(stmt)))
        elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            new = {stmt.name}
            f.functions[stmt.name] = _free(stmt) - f.kills
        elif isinstance(stmt, ast.Assign):
            new = set().union(*(_targets(t) for t in stmt.targets))
        elif isinstance(stmt, (ast.AnnAssign, ast.AugAssign)):
            new = _targets(stmt.target)
        for node in _outer(stmt):
            if isinstance(node, SCOPES):
                if node is not stmt:
                    f.late |= _free(node) - f.kills
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    f.changes[node.name] = _changes(node, modules)
                    f.touches |= f.changes[node.name]  # conservative: at the definition too
            elif isinstance(node, COMPREHENSIONS):
                f.uses |= _free(node) - f.kills  # runs now
                f.refs |= {
                    n.id
                    for n in ast.walk(node)
                    if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
                }
            elif isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Load):
                    f.refs.add(node.id)
                if isinstance(node.ctx, ast.Load) and node.id not in f.kills:
                    f.uses.add(node.id)
                elif not isinstance(node.ctx, ast.Load):
                    f.binds.add(node.id)
                    if isinstance(stmt, ast.AugAssign) and node.id not in f.kills:
                        f.uses.add(node.id)  # x += 1 reads x
            elif isinstance(node, (ast.Attribute, ast.Subscript)) and not isinstance(
                node.ctx, ast.Load
            ):
                root = _root(node)
                if root in modules:  # global state: its own pseudo-name
                    state = STATE + ast.unparse(node)
                    f.binds.add(state)
                    if isinstance(stmt, ast.Assign) and any(node is t for t in stmt.targets):
                        new = new | {state}
                        if isinstance(stmt.value, ast.Constant) and len(stmt.targets) == 1:
                            # A constant setting: the plan can run this statement alone.
                            f.statements[state] = (stmt.lineno, ast.unparse(stmt))
                elif root:
                    f.touches.add(root)
            elif isinstance(node, ast.Call):
                root = _root(node.func)
                if isinstance(node.func, ast.Name):
                    f.calls.add(node.func.id)
                if isinstance(node.func, ast.Attribute) and root:
                    if root not in modules:
                        f.touches.add(root)  # obj.method(...) may change obj
                    elif ".random." in f".{ast.unparse(node.func)}.":
                        if node.func.attr == "seed":
                            new = new | {GLOBAL_RNG}  # a seed sets the state outright
                        elif node.func.attr not in RNG_FACTORIES:
                            f.touches.add(GLOBAL_RNG)
                            if GLOBAL_RNG not in f.kills | new:
                                f.uses.add(GLOBAL_RNG)  # a draw continues from the state
                    elif node.func.attr in STATEFUL_CALLS:
                        f.touches.add(STATE + ast.unparse(node.func))
                for arg in [*node.args, *(k.value for k in node.keywords)]:
                    if isinstance(arg, ast.Name) and arg.id not in modules:
                        f.touches.add(arg.id)  # f(x) may change x
        f.binds |= new
        f.kills |= new
    f.uses -= BUILTINS
    return f


Step = tuple[int, int, str | None]  # (example, line, statement), statement None: run it all


def _plan(facts: list[_Facts], i: int, modules: frozenset[str]) -> list[Step]:
    """Resolve each needed name as it stood just before the position that reads it."""
    writers: dict[str, list[int]] = {}
    for j, f in enumerate(facts[:i]):
        for name in f.binds | f.touches:
            writers.setdefault(name, []).append(j)
    state = {n for n in writers if n.startswith(STATE) and n != GLOBAL_RNG}
    blocks: set[int] = set()
    statements: set[tuple[int, int, str]] = set()
    todo = [(n, i) for n in facts[i].uses | facts[i].late | state]
    todo += [
        (n, i) for name, free in facts[i].functions.items() if name in facts[i].refs for n in free
    ]
    seen: set[tuple[str, int]] = set()

    def run(j: int) -> None:
        if j not in blocks:
            blocks.add(j)
            todo.extend((n, j) for n in facts[j].uses | state)
            todo.extend(
                (n, j)
                for name, free in facts[j].functions.items()
                if name in facts[j].refs
                for n in free
            )
            todo.extend((n, k) for n in facts[j].late for k in range(j + 1, i + 1))

    while todo:
        name, pos = todo.pop()
        if (name, pos) in seen:
            continue
        seen.add((name, pos))
        for j in reversed([j for j in writers.get(name, ()) if j < pos]):
            if name in facts[j].functions:  # read wherever it is referenced
                todo.extend((n, pos) for n in facts[j].functions[name])
            if (
                name in facts[j].statements
                and name in facts[j].kills
                and (name in modules or name in state)
            ):
                line, source = facts[j].statements[name]
                statements.add((j, line, source))
                if name.startswith(STATE):  # a setting needs its module imported first
                    module = name.removeprefix(STATE).split(".")[0]
                    imported = facts[j].statements.get(module)
                    if imported and imported[0] < line:  # by its own example
                        statements.add((j, *imported))
                    else:
                        todo.append((module, j))
            else:
                run(j)
            if name in facts[j].kills:
                break
    plan = {(j, 0, None) for j in blocks} | {step for step in statements if step[0] not in blocks}
    return sorted(plan, key=lambda step: step[:2])


def _plans(sources: list[str]) -> list[list[Step]]:
    trees: list[ast.Module] = []
    for source in sources:
        try:
            trees.append(ast.parse(source))
        except SyntaxError:
            break
    modules = _modules(trees)
    facts = [_facts(tree, modules) for tree in trees]
    # A call to a function the chapter defines changes what that function's body changes.
    changes: dict[str, set[str]] = {}
    for f in facts:
        for name, changed in f.changes.items():
            changes.setdefault(name, set()).update(changed)
    for f in facts:
        f.touches |= set().union(*(changes[c] for c in f.calls if c in changes))
    return [
        _plan(facts, i, modules) if i < len(facts) else [(j, 0, None) for j in range(i)]
        for i in range(len(sources))
    ]


def _simple(steps) -> list[int | str]:
    return [source if source is not None else j for j, _, source in steps]


def dependencies(sources: list[str]) -> list[list[int | str]]:
    """For each example of a chapter, what to run before it, from a fresh interpreter.

    Parameters
    ----------
    sources : list of str
        The chapter's runnable examples, in reading order.

    Returns
    -------
    list of list of int or str
        One plan per example: in reading order, the index of an earlier example to run
        whole, or a single statement to run (an import, or a constant setting of global
        state). An example that does not parse, and every example after it, needs the
        whole prefix: what it binds is unknown.
    """
    return [_simple(plan) for plan in _plans(sources)]


def page_preludes(sources: list[str], pages: list[str]) -> dict[str, list[int | str]]:
    """For each page, what its first click runs before the page's own examples.

    A page's examples share one interpreter, and a click also runs the page's earlier
    examples, as a reader working down the page would. Running a skipped earlier example
    after a later one could undo what the later one set, so execution stays in reading
    order: the first click runs the merged plans of all the page's examples, cut to the
    steps before the page, and then the page's examples in order.

    Parameters
    ----------
    sources : list of str
        The chapter's runnable examples, in reading order.
    pages : list of str
        The page of each example; a page's examples are consecutive.

    Returns
    -------
    dict of str to list of int or str
        Per page, steps as in :func:`dependencies`, all before the page's first example.
    """
    plans = _plans(sources)
    preludes: dict[str, list[int | str]] = {}
    for page in dict.fromkeys(pages):
        members = [i for i, p in enumerate(pages) if p == page]
        steps = {step for i in members for step in plans[i] if step[0] < members[0]}
        whole = {j for j, _, source in steps if source is None}
        steps = {step for step in steps if step[2] is None or step[0] not in whole}
        preludes[page] = _simple(sorted(steps, key=lambda step: step[:2]))
    return preludes
