"""Is a second Louvain level worth drawing? Sub-groups per topic, and their stability across 30 seeds.

Run with: uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I check_levels.py doe_kg_map.json
"""
import json
import sys
from math import comb

import networkx as nx

LIGHT = {"DESCRIBED_IN": 0.2, "ILLUSTRATES": 0.5, "ANSWERED_BY": 0.5, "CONTRASTS_WITH": 0.6, "ALTERNATIVE_TO": 0.6}
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
ref = louvain(g, 7)
scores = [ari(ref, louvain(g, s)) for s in seeds]
print(f"TOP LEVEL: {len(ref)} topics; agreement with the published topics over 30 seeds: "
      f"median {sorted(scores)[15]:.2f}, min {min(scores):.2f}")
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
