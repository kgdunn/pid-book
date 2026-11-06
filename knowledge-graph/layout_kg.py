"""Cluster the DOE graph with Louvain and fix every node's position, for a zoomable map.

Reads doe_kg.json, writes doe_kg_map.json: each node gains a cluster, x, y and degree, plus the
clusters (name, centre, radius) and the number of links between each pair of clusters. Then
writes experimental-design-graph.html: template.html with that data inlined.
Run with: uv run --no-project --with networkx==3.4.2 --with numpy==2.5.3 python -I layout_kg.py
(--no-project keeps uv out of the book's own environment, which has neither package.)
"""

import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx

HERE = Path(__file__).parent
SEED = 7
# Links that say where a term is taught or shown, not what it is: they should not pull topics together.
LIGHT = {"DESCRIBED_IN": 0.2, "ILLUSTRATES": 0.5, "ANSWERED_BY": 0.5, "CONTRASTS_WITH": 0.6, "ALTERNATIVE_TO": 0.6}
# A cluster is named by the anchor term it contains; the build fails if an anchor moves or two meet.
NAMES = {
    # anchor: (short name drawn on the map, full name)
    "full_factorial": ("Full factorials", "Full factorials, randomization, blocking and interactions"),
    "fractional_factorial": ("Fractional factorials", "Fractional factorials, aliasing, resolution and screening"),
    "rsm": ("Response surfaces", "Response surfaces, multiple responses and evolutionary operation"),
    "information_matrix": ("Judging designs", "Judging designs: information, prediction variance and optimality"),
    "omars_design": ("DSD and OMARS", "Definitive screening and OMARS designs"),
    "lenth_method": ("Significance", "Judging significance: Lenth's method, standard errors and t-tests"),
    "coefficient": ("Coefficients and coding", "Factors, coding, coefficients and steepest ascent"),
    "curvature": ("Curvature", "Curvature, center points and second-order designs"),
    "optimal_design": ("Optimal and mixture designs", "Optimal designs, constraints and mixtures"),
    "experiment": ("Causality", "Experiments, causality and happenstance data"),
}
TERM_GAP = 62  # least distance between two terms, in drawing units
CLUSTER_GAP = 70  # least gap between two cluster circles
SUB_GAP = 30  # least gap between two sub-topic circles
# A topic gets a second level only when it is large and other seed batches reproduce its split.
SUB_MIN_SIZE = 20
SUB_MIN_AGREEMENT = 0.8
# Sub-topics are named after their most connected term; these read better as headings (keyed by that term).
SUB_NAMES = {
    "resolution": "Resolution and projectivity", "alias_structure": "Aliasing", "screening": "Screening designs",
    "defining_relation": "Generators and the defining relation", "fractional_factorial": "Fractions of a factorial",
    "minimum_aberration": "Minimum aberration and words",
    "blocking": "Randomization and blocking", "full_factorial": "Main effects and the factorial",
    "interaction": "Interactions", "cost": "One factor at a time", "half_fraction": "Half fractions",
    "orthogonality": "Least squares and orthogonality", "d_optimal": "D-optimality and efficiency",
    "v_optimal": "Prediction variance", "optimality_criterion": "Optimality criteria",
    "variance_inflation_factor": "Correlated model terms",
    "confidence_interval": "Confidence, power and effect size", "lenth_method": "Lenth's method and effect plots",
    "two_group_comparison": "Comparing two conditions", "t_distribution": "Reference distributions",
    "se_significance": "Standard errors",
    "evop": "Sequential experimentation and EVOP", "overall_desirability": "Several responses",
    "optimum": "Response surface methods",
    "mirror_image_pair": "Foldover and estimability", "dsd": "DSD and OMARS designs",
    "fake_factor": "Degrees of freedom and refitting", "design_based_staged_analysis": "Staged analysis and heredity",
}
RUNS = 200  # Louvain runs per round of consensus; at 100, whole small topics could still flip
THRESHOLD = 0.5  # a pair of terms stays linked in the consensus graph if at least this share of runs joined them


def louvain(graph: nx.Graph, seed: int) -> list[list[int]]:
    """One Louvain partition, as sorted lists of integer node ids."""
    return sorted(sorted(c) for c in nx.community.louvain_communities(graph, weight="weight", resolution=1.0, seed=seed))


def consensus(g: nx.Graph, first_seed: int = 0) -> list[set[str]]:
    """Topics that do not depend on Louvain's random seed (consensus clustering, Lancichinetti and Fortunato, 2012).

    Run Louvain RUNS times and link each pair of terms by the share of runs that put them together,
    dropping pairs below THRESHOLD; cluster that consensus graph the same way, and repeat until all
    RUNS runs agree. A term left on its own joins the topic it was most often put in.
    """
    # Louvain iterates over sets of nodes; string ids hash differently on every run, integers do not.
    gi = nx.convert_node_labels_to_integers(g, label_attribute="id")
    graph, seed, first_round = gi, first_seed, None
    for _ in range(20):
        parts = [louvain(graph, seed + k) for k in range(RUNS)]
        seed += RUNS
        if all(p == parts[0] for p in parts):
            break
        together = Counter((a, b) for p in parts for c in p for a, b in combinations(c, 2))
        first_round = first_round or together
        graph = nx.Graph()
        graph.add_nodes_from(gi.nodes)
        graph.add_weighted_edges_from((a, b, k / RUNS) for (a, b), k in sorted(together.items()) if k / RUNS >= THRESHOLD)
    else:
        raise RuntimeError(f"consensus did not settle in 20 rounds of {RUNS} runs")
    topics = [c for c in parts[0] if len(c) > 1]
    for (lone,) in (c for c in parts[0] if len(c) == 1):
        share = lambda t: sum(first_round[(min(lone, m), max(lone, m))] for m in t) / len(t)
        max(topics, key=share).append(lone)
    return [{gi.nodes[i]["id"] for i in t} for t in topics]


def ari(a: list, b: list) -> float:
    """Adjusted Rand index of two partitions of the same nodes (1 = identical, about 0 = chance)."""
    la = {x: i for i, c in enumerate(a) for x in c}
    lb = {x: i for i, c in enumerate(b) for x in c}
    cont = Counter((la[x], lb[x]) for x in la)
    s_ij = sum(math.comb(v, 2) for v in cont.values())
    s_a = sum(math.comb(len(c), 2) for c in a)
    s_b = sum(math.comb(len(c), 2) for c in b)
    expected = s_a * s_b / math.comb(len(la), 2)
    top = (s_a + s_b) / 2 - expected
    return 1.0 if top == 0 else (s_ij - expected) / top


def subgraph(g: nx.Graph, members: list[str]) -> nx.Graph:
    """The links among some terms, built in sorted order: a subgraph view iterates a set, whose order changes."""
    sub = nx.Graph()
    sub.add_nodes_from(sorted(members))
    sub.add_weighted_edges_from(sorted((min(u, v), max(u, v), w) for u, v, w in g.edges(members, data="weight")
                                       if u in sub and v in sub))
    return sub


def second_level(sub: nx.Graph) -> tuple[list[list[str]], float]:
    """A topic's sub-topics, found by consensus, or none when the topic is small or its split is unstable."""
    if sub.number_of_nodes() < SUB_MIN_SIZE:
        return [], 0.0
    parts = consensus(sub, 0)
    if len(parts) < 2:
        return [], 0.0
    agreement = min(ari(parts, consensus(sub, first)) for first in (10_000, 20_000))
    return (sorted(sorted(p) for p in parts) if agreement >= SUB_MIN_AGREEMENT else []), agreement


def scatter(sub: nx.Graph, pad: float) -> tuple[dict[str, list[float]], float]:
    """Terms of one group: a spring layout scaled to its size, spaced out, centred; and the circle's radius."""
    pos = nx.spring_layout(sub, weight="weight", seed=SEED, k=1.2 / math.sqrt(len(sub)), iterations=200)
    scale = 34 * math.sqrt(len(sub))
    pts = {n: [float(x) * scale, float(y) * scale] for n, (x, y) in pos.items()}
    separate(pts, TERM_GAP)
    cx = sum(p[0] for p in pts.values()) / len(pts)
    cy = sum(p[1] for p in pts.values()) / len(pts)
    pts = {n: [x - cx, y - cy] for n, (x, y) in pts.items()}
    return pts, max(math.hypot(x, y) for x, y in pts.values()) + pad


def pack(radii: list[float], links: dict[tuple[int, int], int], gap: float, spread: float,
         gravity: int = 0) -> list[list[float]]:
    """Centres for circles: a spring layout of how they link, then pushed apart until none overlap.

    The layout starts `spread` times the largest radius wide. The push only separates circles, so a few
    circles linked in a chain stay in a line; `gravity` rounds of pulling every circle towards the
    middle, and pushing apart again, fold such a chain into a compact clump.
    """
    if len(radii) == 1:
        return [[0.0, 0.0]]
    graph = nx.Graph()
    graph.add_nodes_from(range(len(radii)))
    graph.add_weighted_edges_from((a, b, n) for (a, b), n in sorted(links.items()))
    centre = nx.spring_layout(graph, weight="weight", seed=SEED, iterations=300)
    width = spread * max(radii)
    ctr = {i: [float(x) * width, float(y) * width] for i, (x, y) in centre.items()}

    def push_apart() -> None:
        for _ in range(600):
            moved = False
            for a, b in combinations(range(len(radii)), 2):
                dx, dy = ctr[b][0] - ctr[a][0], ctr[b][1] - ctr[a][1]
                dist = math.hypot(dx, dy) or 1e-6
                need = radii[a] + radii[b] + gap
                if dist < need:
                    push = (need - dist) / 2 / dist
                    ctr[a] = [ctr[a][0] - dx * push, ctr[a][1] - dy * push]
                    ctr[b] = [ctr[b][0] + dx * push, ctr[b][1] + dy * push]
                    moved = True
            if not moved:
                return

    push_apart()
    for _ in range(gravity):
        mx = sum(x for x, _ in ctr.values()) / len(ctr)
        my = sum(y for _, y in ctr.values()) / len(ctr)
        ctr = {i: [mx + (x - mx) * 0.85, my + (y - my) * 0.85] for i, (x, y) in ctr.items()}
        push_apart()
    return [ctr[i] for i in range(len(radii))]


def pack_tight(radii: list[float], links: dict[tuple[int, int], int], gap: float) -> list[list[float]]:
    """Centres for a few circles packed as tightly as a greedy method can.

    The most linked circle goes first and the next beside it; each further one, in order of how strongly
    it links to the rest, takes the spot touching two placed circles that keeps the enclosing circle
    smallest. Chains of links do not stretch the pack into a line, as a spring layout does.
    """
    strength = Counter()
    for (a, b), n in links.items():
        strength[a] += n
        strength[b] += n
    order = sorted(range(len(radii)), key=lambda i: (-strength[i], -radii[i], i))
    pos = {order[0]: (0.0, 0.0)}
    if len(order) > 1:
        pos[order[1]] = (radii[order[0]] + radii[order[1]] + gap, 0.0)

    def enclosing(cand: dict[int, tuple[float, float]]) -> float:
        mx = sum(x for x, _ in cand.values()) / len(cand)
        my = sum(y for _, y in cand.values()) / len(cand)
        return max(math.hypot(x - mx, y - my) + radii[i] for i, (x, y) in cand.items())

    for k in order[2:]:
        best = None
        for a, b in combinations(sorted(pos), 2):
            (ax, ay), (bx, by) = pos[a], pos[b]
            ra, rb = radii[a] + radii[k] + gap, radii[b] + radii[k] + gap
            d = math.hypot(bx - ax, by - ay)
            if d == 0 or d > ra + rb or d < abs(ra - rb):
                continue
            along = (ra * ra - rb * rb + d * d) / (2 * d)  # the two points at distance ra from a and rb from b
            off = math.sqrt(max(ra * ra - along * along, 0.0))
            ux, uy = (bx - ax) / d, (by - ay) / d
            for sign in (1, -1):
                spot = (ax + along * ux - sign * off * uy, ay + along * uy + sign * off * ux)
                if all(math.hypot(spot[0] - x, spot[1] - y) >= radii[c] + radii[k] + gap - 1e-6 for c, (x, y) in pos.items()):
                    score = enclosing({**pos, k: spot})
                    if best is None or score < best[0] - 1e-9:
                        best = (score, spot)
        pos[k] = best[1]  # two placed circles always leave a free tangent spot outside the pack
    return [list(pos[i]) for i in range(len(radii))]


def crossing(edges: list[dict], group_of: dict[str, int]) -> dict[tuple[int, int], int]:
    """How many links join each pair of groups."""
    links = Counter()
    for e in edges:
        a, b = group_of.get(e["source"]), group_of.get(e["target"])
        if a is not None and b is not None and a != b:
            links[(min(a, b), max(a, b))] += 1
    return dict(links)


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

    communities = consensus(g)
    clusters = []
    for members in communities:
        anchors = [a for a in NAMES if a in members]
        assert len(anchors) == 1, f"cluster of {sorted(members)[:5]}... holds anchors {anchors}"
        short, name = NAMES[anchors[0]]
        clusters.append({"anchor": anchors[0], "short": short, "name": name, "members": sorted(members)})
    assert len(clusters) == len(NAMES), f"{len(clusters)} clusters for {len(NAMES)} names"
    clusters.sort(key=lambda c: -len(c["members"]))
    home = {m: i for i, c in enumerate(clusters) for m in c["members"]}

    # Inside each topic: its terms directly, or its sub-topics' circles, each holding its terms.
    local, sub_of, by_id = {}, {}, {n["id"]: n for n in data["nodes"]}
    for i, c in enumerate(clusters):
        sub = subgraph(g, c["members"])
        groups, c["agreement"] = second_level(sub)
        if not groups:
            pts, c["r"] = scatter(sub, pad=46)
            local.update(pts)
            c["subs"] = []
            continue
        placed = [scatter(subgraph(g, m), pad=30) for m in groups]
        group_of = {m: k for k, members in enumerate(groups) for m in members}
        centres = pack_tight([r for _, r in placed], crossing(data["edges"], group_of), SUB_GAP)
        mx = sum(x for x, _ in centres) / len(centres)
        my = sum(y for _, y in centres) / len(centres)
        centres = [[x - mx, y - my] for x, y in centres]
        c["r"] = max(math.hypot(x, y) + r for (x, y), (_, r) in zip(centres, placed)) + 40
        c["subs"] = []
        for k, (members, (pts, r), (x, y)) in enumerate(zip(groups, placed, centres)):
            hub = max(members, key=lambda m: (sub.degree(m, weight="weight"), m))
            c["subs"].append({"id": f"c{i}s{k}", "hub": hub, "name": SUB_NAMES.get(hub, by_id[hub]["name"]),
                              "x": x, "y": y, "r": round(r, 1), "size": len(members), "members": members})
            local.update({m: [x + px, y + py] for m, (px, py) in pts.items()})
            sub_of.update({m: f"c{i}s{k}" for m in members})

    # Topics: circles packed by how strongly they link.
    links = crossing(data["edges"], home)
    ctr = pack([c["r"] for c in clusters], links, CLUSTER_GAP, spread=2.2)

    for i, c in enumerate(clusters):
        c.update(id=f"c{i}", x=round(ctr[i][0], 1), y=round(ctr[i][1], 1), r=round(c["r"], 1), size=len(c["members"]))
        for s in c["subs"]:
            s.update(x=round(ctr[i][0] + s["x"], 1), y=round(ctr[i][1] + s["y"], 1))
    for n in data["nodes"]:
        i = home[n["id"]]
        lx, ly = local[n["id"]]
        n.update(cluster=f"c{i}", sub=sub_of.get(n["id"]), x=round(ctr[i][0] + lx, 1), y=round(ctr[i][1] + ly, 1),
                 degree=g.degree(n["id"]))
    # The most connected terms of each group (sub-topic, or topic without one) are labelled first as the map is zoomed.
    for c in clusters:
        for members in [s["members"] for s in c["subs"]] or [c["members"]]:
            for rank, m in enumerate(sorted(members, key=lambda m: -g.degree(m))):
                by_id[m]["rank"] = rank
        for s in c["subs"]:
            del s["members"]
        del c["members"]
    unused = sorted(set(SUB_NAMES) - {s["hub"] for c in clusters for s in c["subs"]})
    if unused:
        print("sub-topic names not used (their hub term is no longer a hub):", ", ".join(unused))
    data["clusters"] = clusters
    data["cluster_links"] = [{"a": f"c{a}", "b": f"c{b}", "n": n} for (a, b), n in sorted(links.items())]
    payload = json.dumps(data, separators=(",", ":"))
    (HERE / "doe_kg_map.json").write_text(payload, encoding="utf-8")
    page = (HERE / "template.html").read_text(encoding="utf-8").replace("__DATA__", payload)
    (HERE / "experimental-design-graph.html").write_text(page, encoding="utf-8")

    q = nx.community.modularity(g, communities, weight="weight")
    print(f"{len(clusters)} clusters, modularity {q:.3f}")
    for c in clusters:
        level = (f"{len(c['subs'])} sub-topics (agreement {c['agreement']:.2f})" if c["subs"]
                 else f"no second level ({'unstable split, %.2f' % c['agreement'] if c['agreement'] else 'too small'})")
        print(f"  {c['size']:3d}  {c['name']}: {level}")
        for s in c["subs"]:
            print(f"         {s['size']:3d}  {s['name']}")


if __name__ == "__main__":
    main()
