"""Cluster the DOE graph with Louvain and fix every node's position, for a zoomable map.

Reads doe_kg.json, writes doe_kg_map.json: each node gains a cluster, x, y and degree, plus the
clusters (name, centre, radius) and the number of links between each pair of clusters. Then
writes experimental-design-graph.html: template.html with that data inlined.
Run with: uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I layout_kg.py
(--no-project keeps uv out of the book's own environment, which has neither package.)
"""

import json
import math
from itertools import combinations
from pathlib import Path

import networkx as nx

HERE = Path(__file__).parent
SEED = 7
# Links that say where a term is taught or shown, not what it is: they should not pull topics together.
LIGHT = {"CITED_IN": 0.2, "ILLUSTRATES": 0.5, "ANSWERED_BY": 0.5, "COMPARED_WITH": 0.6}
# A cluster is named by the anchor term it contains; the build fails if an anchor moves or two meet.
NAMES = {
    # anchor: (short name drawn on the map, full name)
    "fractional_factorial": ("Fractional factorials", "Fractional factorials and screening"),
    "full_factorial": ("Full factorials", "Full factorials, randomization and blocking"),
    "optimal_design": ("Optimal designs", "Least squares, constraints and optimal designs"),
    "experiment": ("Causality", "Experiments, factors and causality"),
    "rsm": ("Response surfaces", "Response surfaces and evolutionary operation"),
    "two_group_comparison": ("Significance", "Significance, standard errors and replicates"),
    "curvature": ("Curvature", "Curvature, center points and quadratic models"),
    "cost": ("Interactions", "Interactions, and changing one factor at a time"),
    "steepest_ascent": ("Steepest ascent", "Climbing to the optimum by steepest ascent"),
}
TERM_GAP = 62  # least distance between two terms, in drawing units
CLUSTER_GAP = 70  # least gap between two cluster circles


def separate(points: dict[str, list[float]], gap: float, rounds: int = 400) -> None:
    """Push points apart until no two are closer than gap."""
    ids = list(points)
    for _ in range(rounds):
        moved = False
        for a, b in combinations(ids, 2):
            (ax, ay), (bx, by) = points[a], points[b]
            dx, dy = bx - ax, by - ay
            dist = math.hypot(dx, dy) or 1e-6
            if dist < gap:
                push = (gap - dist) / 2 / dist
                points[a] = [ax - dx * push, ay - dy * push]
                points[b] = [bx + dx * push, by + dy * push]
                moved = True
        if not moved:
            return


def main() -> None:
    data = json.loads((HERE / "doe_kg.json").read_text(encoding="utf-8"))
    g = nx.Graph()
    g.add_nodes_from(n["id"] for n in data["nodes"])
    for e in data["edges"]:
        w = LIGHT.get(e["type"], 1.0)
        if g.has_edge(e["source"], e["target"]):
            g[e["source"]][e["target"]]["weight"] += w
        else:
            g.add_edge(e["source"], e["target"], weight=w)

    # Louvain iterates over sets of nodes; string ids hash differently on every run, integers do not.
    gi = nx.convert_node_labels_to_integers(g, label_attribute="id")
    found = nx.community.louvain_communities(gi, weight="weight", resolution=1.0, seed=SEED)
    communities = [{gi.nodes[i]["id"] for i in c} for c in found]
    clusters = []
    for members in communities:
        anchors = [a for a in NAMES if a in members]
        assert len(anchors) == 1, f"cluster of {sorted(members)[:5]}... holds anchors {anchors}"
        short, name = NAMES[anchors[0]]
        clusters.append({"anchor": anchors[0], "short": short, "name": name, "members": sorted(members)})
    assert len(clusters) == len(NAMES), f"{len(clusters)} clusters for {len(NAMES)} names"
    clusters.sort(key=lambda c: -len(c["members"]))
    home = {m: i for i, c in enumerate(clusters) for m in c["members"]}

    # Terms inside each cluster: a spring layout, scaled to the cluster's size, then spaced out.
    local = {}
    for c in clusters:
        # Built in sorted order: a subgraph view iterates a set of ids, whose order changes run to run.
        sub = nx.Graph()
        sub.add_nodes_from(c["members"])
        sub.add_weighted_edges_from(sorted((min(u, v), max(u, v), w) for u, v, w in g.edges(c["members"], data="weight")
                                           if u in sub and v in sub))
        pos = nx.spring_layout(sub, weight="weight", seed=SEED, k=1.2 / math.sqrt(len(sub)), iterations=200)
        scale = 34 * math.sqrt(len(sub))
        pts = {n: [float(x) * scale, float(y) * scale] for n, (x, y) in pos.items()}
        separate(pts, TERM_GAP)
        cx = sum(p[0] for p in pts.values()) / len(pts)
        cy = sum(p[1] for p in pts.values()) / len(pts)
        pts = {n: [x - cx, y - cy] for n, (x, y) in pts.items()}
        c["r"] = max(math.hypot(x, y) for x, y in pts.values()) + 46
        local.update(pts)

    # Clusters: a spring layout of the cluster graph, then circles pushed apart until none overlap.
    between = nx.Graph()
    between.add_nodes_from(range(len(clusters)))
    links = {}
    for e in data["edges"]:
        a, b = home[e["source"]], home[e["target"]]
        if a != b:
            key = (min(a, b), max(a, b))
            links[key] = links.get(key, 0) + 1
    for (a, b), n in links.items():
        between.add_edge(a, b, weight=n)
    centre = nx.spring_layout(between, weight="weight", seed=SEED, iterations=300)
    spread = 2.2 * max(c["r"] for c in clusters)
    ctr = {i: [float(x) * spread, float(y) * spread] for i, (x, y) in centre.items()}
    for _ in range(600):
        moved = False
        for a, b in combinations(range(len(clusters)), 2):
            dx, dy = ctr[b][0] - ctr[a][0], ctr[b][1] - ctr[a][1]
            dist = math.hypot(dx, dy) or 1e-6
            need = clusters[a]["r"] + clusters[b]["r"] + CLUSTER_GAP
            if dist < need:
                push = (need - dist) / 2 / dist
                ctr[a] = [ctr[a][0] - dx * push, ctr[a][1] - dy * push]
                ctr[b] = [ctr[b][0] + dx * push, ctr[b][1] + dy * push]
                moved = True
        if not moved:
            break

    for i, c in enumerate(clusters):
        c.update(id=f"c{i}", x=round(ctr[i][0], 1), y=round(ctr[i][1], 1), r=round(c["r"], 1), size=len(c["members"]))
    for n in data["nodes"]:
        i = home[n["id"]]
        lx, ly = local[n["id"]]
        n.update(cluster=f"c{i}", x=round(ctr[i][0] + lx, 1), y=round(ctr[i][1] + ly, 1), degree=g.degree(n["id"]))
    # The few most connected terms of each cluster are labelled first as the map is zoomed.
    for c in clusters:
        ranked = sorted(c["members"], key=lambda m: -g.degree(m))
        for rank, m in enumerate(ranked):
            next(n for n in data["nodes"] if n["id"] == m)["rank"] = rank
        del c["members"]
    data["clusters"] = clusters
    data["cluster_links"] = [{"a": f"c{a}", "b": f"c{b}", "n": n} for (a, b), n in sorted(links.items())]
    payload = json.dumps(data, separators=(",", ":"))
    (HERE / "doe_kg_map.json").write_text(payload, encoding="utf-8")
    page = (HERE / "template.html").read_text(encoding="utf-8").replace("__DATA__", payload)
    (HERE / "experimental-design-graph.html").write_text(page, encoding="utf-8")

    q = nx.community.modularity(g, communities, weight="weight")
    print(f"{len(clusters)} clusters, modularity {q:.3f}")
    for c in clusters:
        print(f"  {c['size']:3d}  {c['name']}  (r={c['r']:.0f})")


if __name__ == "__main__":
    main()
