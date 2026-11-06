"""Merge the reviewers' results into graph.yaml: corrected terms, fixed links, merged overlaps, new terms.

Every judgment the reviewers left open is in one of the tables below, so the merge can be read
and argued with. Reads the original graph from build_kg.py (N, E) and audit/result_*.json.
"""

import json
import re
import sys
from pathlib import Path

import yaml

AUDIT = Path("/tmp/claude-0/-home-user/f5de32d9-e9cf-527e-9ba3-c74ed25f6ef9/scratchpad/audit")
KG = Path("/home/user/pid-book-pr22/knowledge-graph")
sys.argv = ["build_kg.py", "/home/user/pid-book"]
sys.path.insert(0, str(KG))
import build_kg  # noqa: E402

# Overlapping terms the reviewers found: the first is folded into the second (its name becomes an alias).
MERGE = {
    "equal_jumps": "plateau",  # the book calls two roughly equal responses "plateaued" (A)
    "alias": "confounding",  # the book uses aliased and confounded as synonyms (A)
    "steepest_descent": "steepest_ascent",  # descent appears only in parentheses (A)
    "half_range_effect": "coefficient",  # only restates the coefficient's scale (B)
}
DROP_NODES = {"independence"}  # defined only through randomization and the t-test (B)

# Links a reviewer marked unsupported: replaced (new triple, evidence) or kept as they are.
UNSUPPORTED = {
    ("resolution_iv", "SUITED_TO", "phase_sequential"): None,  # the book pairs resolution IV with characterizing
    ("resolution", "INTRODUCED_IN", "ref_box_hunter_1961"): ("fractional_factorial", "DESCRIBED_IN", "ref_box_hunter_1961"),
    ("block_on_highest", "RELIES_ON", "effect_sparsity"): ("block_on_highest", "RELIES_ON", "effect_hierarchy"),
    ("evop", "INTRODUCED_IN", "ref_box_1957"): ("evop", "DESCRIBED_IN", "ref_box_1957"),
    ("q_old_data", "ANSWERED_BY", "least_squares_model"): "keep",  # the chapter's way of reading old data
}
# New terms proposed twice under different names: the first is folded into the second.
MERGE_NEW = {
    "principal_component_analysis_pca": "pca",
    "projection_to_latent_structures_pls": "pls",
    "pseudocomponents": "pseudocomponent",
    "blocking_into_more_than_two_groups": "blocking_into_more_than_two_blocks",
    "desirability": "overall_desirability",
    "confirmation_run": "confirm_the_predicted_optimum",
}
# The longer, book-style names win for the merged anchors.
RENAME = {"pca": "Principal component analysis (PCA)", "pls": "Projection to latent structures (PLS)"}

# Link verbs, folded into a small vocabulary without joining opposite meanings:
# verb -> (canonical verb, swap direction).
CANON = {
    "IS_A", "PART_OF", "HAS_PROPERTY", "USES", "REQUIRES", "JUSTIFIES", "ESTIMATES", "MEASURES", "SHOWS",
    "LOCATES", "TESTS", "CAUSES", "ENABLES", "LIMITS", "PREVENTS", "KEEPS", "REMEDIED_BY", "INDICATES",
    "AGREES_WITH", "CONTRASTS_WITH", "ALTERNATIVE_TO", "COMPLEMENTS", "GENERALIZES", "CAN_AUGMENT_TO", "CAN_BE",
    "SUITED_TO", "APPLIES_TO", "PRECEDES", "ILLUSTRATES", "ANSWERED_BY", "DESCRIBED_IN", "CANNOT_SHOW",
    "EQUALS", "IS_HALF_OF", "MAY_HAVE",
}
FOLD = {
    **{v: (v, False) for v in CANON},
    # same direction
    "ADDS": ("CAUSES", False), "AFFECTS": ("CAUSES", False), "LEADS_TO": ("CAUSES", False), "LEAVES": ("CAUSES", False),
    "MOTIVATES": ("CAUSES", False), "PROVIDES": ("CAUSES", False), "RAISES": ("CAUSES", False),
    "SUFFERS_FROM": ("CAUSES", False), "DETERMINES": ("CAUSES", False), "GUARANTEES": ("CAUSES", False),
    "MAKES": ("CAUSES", False), "MAKES_APPLICABLE": ("ENABLES", False), "MAKES_COMPARABLE": ("ENABLES", False),
    "ADDS_CUTOFF_TO": ("APPLIES_TO", False), "ANALYSES": ("APPLIES_TO", False), "CHANGES": ("APPLIES_TO", False),
    "CHOOSES": ("APPLIES_TO", False), "CHOOSES_WITHIN": ("APPLIES_TO", False), "CONCERNS": ("APPLIES_TO", False),
    "GUARDS": ("APPLIES_TO", False), "MEANS_SMALL": ("APPLIES_TO", False), "PREFERS": ("APPLIES_TO", False),
    "QUALIFIES": ("APPLIES_TO", False), "SMOOTHS": ("APPLIES_TO", False), "SUPPORTS": ("APPLIES_TO", False),
    "HAS_ZERO_MAIN_EFFECT_ROWS_FOR": ("APPLIES_TO", False),
    "APPLIES": ("USES", False), "AVERAGES": ("USES", False), "BUILT_FROM": ("USES", False), "BUILT_ON": ("USES", False),
    "CLASSIFIES_AS_HARD_OR_EASY_TO_CHANGE": ("USES", False), "COMPUTED_FROM": ("USES", False),
    "DERIVED_FROM": ("USES", False), "DESIGN_STEP_USES": ("USES", False), "HAS_EFFECTS_OF": ("USES", False),
    "INVOLVES": ("USES", False), "ITERATES_BY": ("USES", False), "MAPS_ONTO": ("USES", False),
    "MAPS_PER_PIXEL": ("USES", False), "MEASURED_FROM": ("USES", False), "MEASURED_AS": ("USES", False),
    "MODELLED_WITH": ("USES", False), "MORE_INFORMATIVE_WITH": ("USES", False), "OPTIMIZES": ("USES", False),
    "OPTIONALLY_USES": ("USES", False), "PICKS_DESIGN_IN": ("USES", False), "PRECISION_MEASURED_BY": ("USES", False),
    "RATIOS_DESIGNED_WITH": ("USES", False), "SCALES": ("USES", False), "SEPARABILITY_MEASURED_BY": ("USES", False),
    "SPECIFIES": ("USES", False), "SPLIT_BY": ("USES", False), "TUNED_WITH": ("USES", False),
    "USES_SCORES_OF": ("USES", False), "REFINES": ("USES", False), "ESTIMATED_FROM": ("USES", False),
    "MAY_START_WITH": ("USES", False), "HELPS_BUILD": ("PART_OF", False), "MIRRORS": ("CONTRASTS_WITH", False),
    "COUNTS": ("MEASURES", False), "EQUALS_ONE_UNDER": ("MEASURES", False), "EXPRESSES": ("MEASURES", False),
    "QUANTIFIES_BIAS_FROM": ("MEASURES", False), "SUMMARIZES": ("MEASURES", False), "Z_RECORDS": ("MEASURES", False),
    "CONDITIONS_SHOW": ("SHOWS", False), "DECOMPOSES": ("SHOWS", False), "DESCRIBES": ("SHOWS", False),
    "EXPLAINS": ("SHOWS", False), "LISTS": ("SHOWS", False), "MAPS": ("SHOWS", False), "PLOTS": ("SHOWS", False),
    "PRODUCES": ("SHOWS", False), "RELATES": ("SHOWS", False), "REPORTS": ("SHOWS", False),
    "RIGHT_END_GIVES": ("SHOWS", False), "SHOWS_TRADE_OFF_WITH": ("SHOWS", False),
    "SEEKS": ("LOCATES", False), "TRACKS": ("LOCATES", False),
    "CHECKS": ("TESTS", False), "DECIDES": ("TESTS", False), "DETECTS": ("TESTS", False),
    "DETECTS_SHORTFALL_BELOW": ("TESTS", False), "VALIDATES": ("TESTS", False),
    "REDUCES": ("LIMITS", False), "RESTRICTS": ("LIMITS", False),
    "PROTECTS_AGAINST": ("PREVENTS", False), "REMOVES": ("PREVENTS", False),
    "RESOLVED_BY": ("REMEDIED_BY", False), "SUGGESTS": ("INDICATES", False),
    "APPROXIMATED_BY": ("AGREES_WITH", False),
    "COMPARED_WITH": ("CONTRASTS_WITH", False), "DIFFERS_FROM": ("CONTRASTS_WITH", False),
    "NEEDS_NO": ("CONTRASTS_WITH", False), "RELAXES_ASSUMPTION_OF": ("CONTRASTS_WITH", False),
    "REPORTS_ESTIMABILITY_NOT": ("CONTRASTS_WITH", False), "ANALOGUE_OF": ("CONTRASTS_WITH", False),
    "COMPANION_OF": ("COMPLEMENTS", False), "COMPLETES": ("COMPLEMENTS", False),
    "EXTENDS": ("GENERALIZES", False), "FORMALIZES": ("GENERALIZES", False),
    "SUITS": ("SUITED_TO", False), "USED_FOR": ("SUITED_TO", False),
    "IS_A_FORM_OF": ("IS_A", False), "IS_A_KIND_OF": ("IS_A", False), "MEMBER_OF": ("IS_A", False),
    "SPECIAL_CASE_OF": ("IS_A", False), "TYPE_OF": ("IS_A", False), "VARIANT_OF": ("IS_A", False),
    "BUILT_AS": ("IS_A", False),
    "COLUMN_OF": ("PART_OF", False), "COMBINED_INTO": ("PART_OF", False), "DEFINES": ("PART_OF", False),
    "DIAGNOSTIC_OF": ("PART_OF", False), "FRACTION_OF": ("PART_OF", False), "MARKS_FULL_CLASS_IN": ("PART_OF", False),
    "OPTION_IN": ("PART_OF", False), "RESIDUAL_OF": ("PART_OF", False), "CHOSEN_IN": ("PART_OF", False),
    "IS_DIAGONAL_UNDER": ("HAS_PROPERTY", False), "CANNOT_ESTIMATE": ("CANNOT_SHOW", False),
    "INTRODUCED_IN": ("DESCRIBED_IN", False), "CRITICIZED_IN": ("DESCRIBED_IN", False),
    "REVIEWED_IN": ("DESCRIBED_IN", False),
    # reversed: "A verb B" reads as "B canonical A"
    "HAS": ("PART_OF", True), "MADE_OF": ("PART_OF", True), "HAS_PHASE": ("PART_OF", True),
    "HAS_SETTING": ("PART_OF", True), "INCLUDES": ("PART_OF", True), "STARTS_WITH": ("PART_OF", True),
    "PROPERTY_OF": ("HAS_PROPERTY", True), "NEEDED_FOR": ("REQUIRES", True), "DEPENDS_ON": ("REQUIRES", False),
    "THRESHOLD_DEPENDS_ON": ("REQUIRES", False), "RELIES_ON": ("JUSTIFIES", True),
    "ANALYSED_BY": ("APPLIES_TO", True), "EXPLORED_BY": ("APPLIES_TO", True), "IS_FOLDED_OVER_BY": ("APPLIES_TO", True),
    "USED_BY": ("USES", True), "USED_IN": ("USES", True), "USED_AS": ("USES", True), "BUILDS": ("USES", True),
    "BUILT_BY": ("USES", True), "FEEDS": ("USES", True), "INPUT_TO": ("USES", True), "INVERTED_BY": ("USES", True),
    "MAXIMIZED_BY": ("USES", True), "MAXIMUM_GIVES": ("USES", True), "MAXIMUM_MINIMIZED_BY": ("USES", True),
    "AVERAGE_GIVES": ("USES", True), "MODEL_FOR": ("USES", True), "SCALED_INTO": ("USES", True),
    "UNFOLDED_BY": ("USES", True), "PERFORMS": ("USES", True),
    "SUMMARIZED_BY": ("MEASURES", True), "PLOTTED_IN": ("SHOWS", True), "SHOWN_BY": ("SHOWS", True),
    "DRAWN_BY": ("SHOWS", True), "GRAPHICAL_FORM_OF": ("SHOWS", True),
    "CAUSED_BY": ("CAUSES", True), "ARISES_FROM": ("CAUSES", True), "SHAPED_BY": ("CAUSES", True),
    "BOUNDED_BY": ("LIMITS", True), "CONSTRAINED_BY": ("LIMITS", True), "F_SUBJECT_TO": ("LIMITS", True),
    "RATIOS_SUBJECT_TO": ("LIMITS", True), "RESTRICTED_BY": ("LIMITS", True), "IS_ZERO_FOR": ("LIMITS", True),
    "HANDLES": ("REMEDIED_BY", True), "REMEDIES": ("REMEDIED_BY", True), "RESOLVES_PART_OF": ("REMEDIED_BY", True),
    "DETECTED_BY": ("INDICATES", True), "GENERALIZED_BY": ("GENERALIZES", True), "FOLLOWS": ("PRECEDES", True),
    "ILLUSTRATED_BY": ("ILLUSTRATES", True), "APPLIED_IN": ("ILLUSTRATES", True),
}
# Links whose folded form would read wrongly: replaced one by one (None drops the link).
OVERRIDE = {
    ("refit", "LEADS_TO", "residual_analysis"): ("refit", "PRECEDES", "residual_analysis"),
    ("optimum", "HAS", "curvature"): ("optimum", "HAS_PROPERTY", "curvature"),
    ("near_optimum", "HAS", "curvature"): ("near_optimum", "HAS_PROPERTY", "curvature"),
    # "the central composite and the Box-Behnken designs are themselves among the largest OMARS designs"
    ("omars_design", "INCLUDES", "box_behnken"): ("box_behnken", "IS_A", "omars_design"),
    ("invert_in_the_latent_variable_space", "REFINES", "model_inversion"):
        ("invert_in_the_latent_variable_space", "IS_A", "model_inversion"),
    ("projectivity", "COLLAPSES_TO", "full_factorial"): None,  # its definition says it
}
# Chapter 7 uses "troubleshooting" for analysing plant records, not for experimenting (G).
CH7_TROUBLESHOOTING = "troubleshooting_with_latent_variable_models"

# Reviewers whose definition wins when two rewrote the same term: the topic's owner first, then E.
OWNER_ORDER = "ABCDE"
# Proposed new terms are taken in this order; a later proposal of the same name only adds links.
NEW_ORDER = "EABCDFG"


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", name.lower().replace("'s", "")).strip()


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower().replace("'s", "")).strip("_")


def triple(fix) -> tuple[str, str, str] | None:
    """A reviewer's fix, written as a list or as 'source RELATION target', or 'drop'."""
    if not fix or fix == "drop":
        return None
    parts = fix if isinstance(fix, list) else fix.replace(",", " ").split()
    parts = [p.strip(" []'\"") for p in parts if p.strip(" []'\"")]
    if len(parts) != 3:
        raise ValueError(f"cannot read fix {fix!r}")
    return parts[0], parts[1].upper(), parts[2]


def main() -> None:
    results = {g: json.loads((AUDIT / f"result_{g}.json").read_text()) for g in "ABCDEFG"
               if (AUDIT / f"result_{g}.json").exists()}
    print("results:", "".join(results))
    nodes = {n[0]: {"id": n[0], "name": n[1], "type": n[2], "definition": n[4], "aliases": list(n[5]),
                    "book_label": build_kg.REFS[n[3]]} for n in build_kg.N}
    for n in nodes.values():  # file:... refs become book-root paths
        if n["book_label"].startswith("file:"):
            n["book_label"] = f"file:{build_kg.CHAPTER}/{n['book_label'][5:]}"

    # 1. Definitions, labels and evidence for existing terms.
    changed = []
    for g in OWNER_ORDER[::-1]:  # later wins, so walk the order backwards
        for v in results.get(g, {}).get("nodes", []):
            n = nodes.get(v["id"])
            if n is None:
                continue
            if v.get("evidence") and v.get("quote"):
                n["evidence"], n["quote"] = v["evidence"], v["quote"]
            if v["verdict"] in ("imprecise", "wrong") and v.get("definition"):
                n["definition"] = v["definition"]
                changed.append((v["id"], g, v["verdict"]))
            if v.get("book_label"):
                n["book_label"] = v["book_label"]

    # 2. Links: keep supported ones with their evidence, fix the wrong ones, decide the unsupported.
    edges, ev = [], {}
    reviewed = {}
    for g in "ABCD":
        for e in results.get(g, {}).get("edges", []):
            reviewed[(e["source"], e["relation"], e["target"])] = e
    for t in build_kg.E:
        r = reviewed.get(t)
        if r is None:
            raise SystemExit(f"link not reviewed: {t}")
        if r["verdict"] == "supported":
            new = t
        elif r["verdict"] == "wrong":
            new = triple(r.get("fix"))
        else:
            d = UNSUPPORTED[t]
            new = t if d == "keep" else d
        if new:
            edges.append(new)
            ev[new] = r.get("evidence", "") if new == t or r["verdict"] == "wrong" else ""

    # 3. Overlaps: fold merged terms into their partner, drop the dropped ones.
    for src, dst in MERGE.items():
        nodes[dst]["aliases"] += [nodes[src]["name"], *nodes[src]["aliases"]]
        del nodes[src]
    for d in DROP_NODES:
        del nodes[d]
    rename = lambda i: MERGE.get(i, i)
    edges = [(rename(s), r, rename(t)) for s, r, t in edges]
    ev = {(rename(s), r, rename(t)): v for (s, r, t), v in ev.items()}

    # 4. New terms, deduplicated by name against existing names and aliases and against each other.
    by_name = {norm(n["name"]): i for i, n in nodes.items()}
    by_name.update({norm(a): i for i, n in nodes.items() for a in n["aliases"]})
    proposals, pending_links = [], []
    for g in NEW_ORDER:
        for m in results.get(g, {}).get("missing", []):
            key = norm(m["name"])
            nid = by_name.get(key)
            if nid is None:
                nid = slug(m["name"])
                while nid in nodes:
                    nid += "_2"
                nodes[nid] = {"id": nid, "name": m["name"], "type": m["type"], "definition": m["definition"],
                              "aliases": [], "book_label": m["book_label"], "evidence": m.get("evidence", ""),
                              "quote": m.get("quote", ""), "source": g}
                by_name[key] = nid
                proposals.append((g, nid))
            for link in m.get("links", []):
                pending_links.append((nid, link["relation"].upper(), link["target"], link.get("evidence", ""), g))
    unresolved = []
    for s, r, target, evidence, g in pending_links:
        t = target if target in nodes else by_name.get(norm(target))
        if t is None:
            unresolved.append(f"{g}: {s} {r} {target}")
            continue
        e = (s, r, t)
        if s != t and e not in edges:
            edges.append(e)
            ev[e] = evidence

    # 5. Fold the duplicate new terms, then the link verbs.
    for src, dst in MERGE_NEW.items():
        nodes[dst]["aliases"] += [nodes[src]["name"], *nodes[src]["aliases"]]
        del nodes[src]
    for nid, name in RENAME.items():
        nodes[nid]["aliases"].append(nodes[nid]["name"])
        nodes[nid]["name"] = name
    for n in nodes.values():  # aliases: unique, and never the term's own name
        n["aliases"] = [a for a in dict.fromkeys(n["aliases"]) if norm(a) != norm(n["name"])]
    renew = lambda i: MERGE_NEW.get(i, i)
    proposed = {nid for _, nid in proposals}
    folded, fev, unknown = [], {}, set()
    for s, r, t in edges:
        e0 = (renew(s), r, renew(t))
        if e0 in OVERRIDE:
            e = OVERRIDE[e0]
        elif r in FOLD:
            verb, swap = FOLD[r]
            e = (e0[2], verb, e0[0]) if swap else (e0[0], verb, e0[2])
        else:
            unknown.add(r)
            continue
        if e is None:
            continue
        if e[2] == "troubleshooting" and e[0] in proposed:
            e = (e[0], e[1], CH7_TROUBLESHOOTING)
        if e not in fev:
            folded.append(e)
            fev[e] = ev.get((s, r, t), "")
    assert not unknown, f"verbs with no fold: {sorted(unknown)}"
    edges, ev = folded, fev

    # Drop links to removed terms, self-loops and duplicates.
    edges = list(dict.fromkeys(e for e in edges if e[0] in nodes and e[2] in nodes and e[0] != e[2]))
    linked = {e[0] for e in edges} | {e[2] for e in edges}
    print("terms with no links:", sorted(set(nodes) - linked) or "none")
    out = {
        "nodes": [{k: n.get(k, "") for k in ("id", "name", "type", "definition", "aliases", "book_label", "evidence", "quote")}
                  for n in nodes.values()],
        "edges": [[s, r, t, ev.get((s, r, t), "")] for s, r, t in edges],
    }
    (AUDIT / "graph_merged.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=110))
    verbs = {}
    for _, r, _ in edges:
        verbs[r] = verbs.get(r, 0) + 1
    print(f"{len(nodes)} terms ({len(proposals)} new), {len(edges)} links, {len(changed)} definitions changed")
    print("new by reviewer:", {g: sum(1 for p in proposals if p[0] == g) for g in NEW_ORDER})
    print("relations:", dict(sorted(verbs.items(), key=lambda kv: -kv[1])))
    print("no evidence:", [n["id"] for n in nodes.values() if not n.get("evidence")])
    print("unresolved links:", unresolved or "none")


if __name__ == "__main__":
    main()
