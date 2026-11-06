"""How stable are the map's topics, and is a second level worth drawing?

Top level: how well single Louvain runs, and consensus runs from other seed batches, reproduce the
published topics. Second level: the sub-groups single Louvain runs find inside each topic, and
their stability across 30 seeds.

Run with: uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I check_levels.py doe_kg_map.json
"""
import json
import sys
from math import comb
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I leaves the script's folder off the path
from layout_kg import LIGHT, consensus  # noqa: E402  (one source for the weights and the method)

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


def ari(a, b):
    """Adjusted Rand index of two partitions of the same nodes (1 = identical, about 0 = chance)."""
    la = {x: i for i, c in enumerate(a) for x in c}
    lb = {x: i for i, c in enumerate(b) for x in c}
    nodes = list(la)
    cont = {}
    for x in nodes:
        cont[(la[x], lb[x])] = cont.get((la[x], lb[x]), 0) + 1
    s_ij = sum(comb(v, 2) for v in cont.values())
    s_a = sum(comb(len(c), 2) for c in a)
    s_b = sum(comb(len(c), 2) for c in b)
    exp = s_a * s_b / comb(len(nodes), 2)
    top = (s_a + s_b) / 2 - exp
    return 1.0 if top == 0 else (s_ij - exp) / top


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
    sub = nx.Graph()
    sub.add_nodes_from(members)
    sub.add_weighted_edges_from(sorted((min(u, v), max(u, v), w) for u, v, w in g.edges(members, data="weight")
                                       if u in sub and v in sub))
    parts = louvain(sub, 7)
    q = nx.community.modularity(sub, parts, weight="weight")
    stab = [ari(parts, louvain(sub, s)) for s in seeds]
    print(f"{short[cid]} ({len(members)} terms): {len(parts)} sub-groups, modularity {q:.2f}, "
          f"seed agreement median {sorted(stab)[15]:.2f} min {min(stab):.2f}")
    if len(members) >= 20:
        for p in sorted(parts, key=len, reverse=True):
            print("    ", len(p), ", ".join(name[m] for m in sorted(p, key=lambda m: -sub.degree(m, weight="weight"))))
