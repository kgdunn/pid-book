"""Keep chapter 5 and the three design terms of chapter 7's profile case study; drop the multivariate rest.

One-off record: ran on 2026-11-06 on graph.yaml at commit aa497bb (283 terms) to give commit deb4820
(217 terms), when the graph was narrowed to designed experiments for the factorial app.
"""
import sys
from pathlib import Path

import yaml

KEEP_CH7 = {"split_plot_design", "coding_schemes_for_a_categorical_factor", "joint_f_test_of_a_categorical_interaction"}
p = Path(sys.argv[1])
text = p.read_text(encoding="utf-8")
head = text[: text.index("nodes:")]
g = yaml.safe_load(text)
keep = [n for n in g["nodes"] if n["book_label"].startswith("file:design-analysis-experiments/")
        or n["evidence"].startswith("design-analysis-experiments/") or n["id"] in KEEP_CH7]
ids = {n["id"] for n in keep}
edges = [e for e in g["edges"] if e[0] in ids and e[2] in ids]
dropped = sorted(n["id"] for n in g["nodes"] if n["id"] not in ids)
nodes_yaml = yaml.safe_dump({"nodes": keep}, sort_keys=False, allow_unicode=True, width=110)
edge_lines = "".join(f'- [{s}, {r}, {t}, "{ev}"]\n' if ev else f"- [{s}, {r}, {t}]\n" for s, r, t, *rest in edges
                     for ev in [rest[0] if rest else ""])
p.write_text(head + nodes_yaml + "\nedges:\n" + edge_lines, encoding="utf-8")
print(f"kept {len(keep)} terms and {len(edges)} links; dropped {len(dropped)} terms, {len(g['edges']) - len(edges)} links")
