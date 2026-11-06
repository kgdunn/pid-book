"""Write one input file per reviewer: its terms, the links that start at them (in the original verbs), and the label map.

One-off record: ran on 2026-11-06 against build_kg.py at commit e99d98e, when the graph was still Python
tuples (N, E); it cannot run against the current graph.yaml. Paths are those of the session that ran it.
"""
import json
import re
import sys
from pathlib import Path

sys.argv = ["build_kg.py", "/home/user/pid-book"]
sys.path.insert(0, "/home/user/pid-book-pr22/knowledge-graph")
import build_kg  # noqa: E402  (N and E as written, before folding)

out = Path("/tmp/claude-0/-home-user/f5de32d9-e9cf-527e-9ba3-c74ed25f6ef9/scratchpad/audit")
mapped = json.loads(Path("/home/user/pid-book-pr22/knowledge-graph/doe_kg_map.json").read_text())
topic = {n["id"]: n["cluster"] for n in mapped["nodes"]}
names = {c["id"]: c["name"] for c in mapped["clusters"]}
labels = {}
for rst in Path("/home/user/pid-book/design-analysis-experiments").rglob("*.rst"):
    for i, line in enumerate(rst.read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^\.\. _([^:]+):", line)
        if m:
            labels[m.group(1)] = f"{rst.relative_to('/home/user/pid-book')}:{i}"
groups = {"A": ["c0", "c8"], "B": ["c1", "c7", "c5"], "C": ["c2", "c6"], "D": ["c3", "c4"]}
for g, cs in groups.items():
    ids = {n[0] for n in build_kg.N if topic[n[0]] in cs}
    nodes = [{"id": n[0], "name": n[1], "type": n[2], "definition": n[4], "aliases": n[5],
              "book_label": build_kg.REFS[n[3]]} for n in build_kg.N if n[0] in ids]
    edges = [list(e) for e in build_kg.E if e[0] in ids]
    (out / f"input_{g}.json").write_text(json.dumps({"topics": [names[c] for c in cs], "nodes": nodes, "edges": edges}, indent=1))
    print(g, len(nodes), "terms", len(edges), "links")
(out / "labels.json").write_text(json.dumps(labels, indent=1))
(out / "all_terms.json").write_text(json.dumps([{"id": n[0], "name": n[1]} for n in build_kg.N], indent=1))
print(len(labels), "labels")
