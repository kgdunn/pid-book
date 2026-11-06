"""How stable are the map's topics, and which get a second level?

Top level: how well single Louvain runs, and consensus runs from other seed batches, reproduce the
published topics. Second level: for each topic, the sub-topics layout_kg.py would draw and how well
other seed batches reproduce them, by the same rule the layout applies.

Run with: uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I check_levels.py doe_kg_map.json
"""
import json
import sys
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I leaves the script's folder off the path
from layout_kg import LIGHT, SUB_MIN_AGREEMENT, SUB_MIN_SIZE, ari, consensus, second_level, subgraph  # noqa: E402

d = json.load(open(sys.argv[1]))
g = nx.Graph()
g.add_nodes_from(n["id"] for n in d["nodes"])
for e in d["edges"]:
    w = LIGHT.get(e["type"], 1.0)
    u, v = e["source"], e["target"]
    g.add_edge(u, v, weight=g[u][v]["weight"] + w if g.has_edge(u, v) else w)
name = {n["id"]: n["name"] for n in d["nodes"]}
topic = {n["id"]: n["cluster"] for n in d["nodes"]}
short = {c["id"]: c["name"] for c in d["clusters"]}


def louvain(graph, seed):
    gi = nx.convert_node_labels_to_integers(graph, label_attribute="id")
    return [{gi.nodes[i]["id"] for i in c} for c in nx.community.louvain_communities(gi, weight="weight", seed=seed)]


seeds = range(30)
published = [{m for m in topic if topic[m] == c} for c in short]
single = sorted(ari(published, louvain(g, s)) for s in seeds)
batches = [ari(published, consensus(g, first)) for first in (10_000, 20_000, 30_000, 40_000)]
print(f"TOP LEVEL: {len(published)} topics. Agreement with the published topics:")
print(f"  single Louvain runs, 30 seeds: median {single[15]:.2f}, min {single[0]:.2f}")
print(f"  consensus, 4 other seed batches: {', '.join(f'{b:.2f}' for b in batches)}")
print()
for cid in sorted(short, key=lambda c: -sum(1 for t in topic.values() if t == c)):
    members = sorted(m for m in topic if topic[m] == cid)
    groups, agreement, _ = second_level(subgraph(g, members))
    if groups:
        verdict = f"{len(groups)} sub-topics; other seed batches agree at {agreement:.2f} at worst"
    elif len(members) < SUB_MIN_SIZE:
        verdict = f"no second level: fewer than {SUB_MIN_SIZE} terms"
    else:
        verdict = f"no second level: other seed batches agree at only {agreement:.2f} (needs {SUB_MIN_AGREEMENT})"
    print(f"{short[cid]} ({len(members)} terms): {verdict}")
    for grp in groups:
        print("    ", len(grp), ", ".join(name[m] for m in sorted(grp, key=lambda m: -g.degree(m, weight="weight"))[:6]))
