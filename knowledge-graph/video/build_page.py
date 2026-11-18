"""Write the page that draws the video of the concept map: the map's data, set into template.html.

The video shows the map building itself, two other texts sweeping across it, a dive into one topic and one of its
sub-topics, and four links read out as sentences. Run, from this folder:

  python -I build_page.py                       (writes page.html: light theme, half speed)
  node render.js page.html frames               (one PNG a frame; needs Playwright and its Chromium)
  ffmpeg -framerate 30 -i frames/f_%05d.png -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \\
    -movflags +faststart out/concept-map.mp4

It reads ../doe_kg_map.json, the file the map itself draws, so build the graph first (see ../README.md).
"""

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The dive, by name, since a topic's id changes when the map is laid out again: the topic and the sub-topic the video
# opens, and the four links it reads out there. The four must differ in who else states them (no other text, the first,
# the second, both), so that the video shows each case once; the build stops, and lists the sub-topic's links, if not.
DIVE = {
    "topic": "Response surfaces",
    "sub": "Response surface methods",
    "read": [["contour_plot", "response_surface"], ["confirm_the_prediction", "optimum"],
             ["contour_plot", "optimum"], ["ex_rsm_profit", "rsm"]],
    "only": "Only this book states it: one of its worked examples.",   # said of the link no other text states
}
# A link's verb as the map reads it: the verb in lower case, but for these three.
READ = {"IS_A": "is a kind of", "CAN_AUGMENT_TO": "can be augmented to", "PRECEDES": "comes before"}
WHO = ["this book only", "the first text too", "the second text too", "both other texts"]


def page_data(slow: float) -> dict:
    """The map as the template wants it, with what each of the two other texts also has, and the dive."""
    d = json.loads((HERE.parent / "doe_kg_map.json").read_text(encoding="utf-8"))
    has = lambda item, text: text in item.get("also", [])   # noqa: E731
    on = {text: {i for e in d["edges"] if has(e, text) for i in (e["source"], e["target"])}
          for text in ("reviewed_text_1", "reviewed_text_2")}
    # A term is in a text when the text defines it as the book does, or states one of its links: as the map has it.
    nodes = [{"id": n["id"], "name": n["name"], "x": n["x"], "y": n["y"], "c": n["cluster"], "sub": n.get("sub"),
              "deg": n["degree"], "rank": n["rank"], "level": n["level"],
              "t1": has(n, "reviewed_text_1") or n["id"] in on["reviewed_text_1"],
              "t2": has(n, "reviewed_text_2") or n["id"] in on["reviewed_text_2"]} for n in d["nodes"]]
    edges = [{"s": e["source"], "t": e["target"], "verb": READ.get(e["type"], e["type"].lower().replace("_", " ")),
              "t1": has(e, "reviewed_text_1"), "t2": has(e, "reviewed_text_2")} for e in d["edges"]]
    clusters = [{"id": c["id"], "name": c["short"], "x": c["x"], "y": c["y"], "r": c["r"],
                 "subs": [{k: s[k] for k in ("id", "name", "x", "y", "r", "size") if k in s} for s in c.get("subs", [])]}
                for c in d["clusters"]]

    topic = next((c for c in clusters if c["name"] == DIVE["topic"]), None)
    sub = next((s for s in (topic or {}).get("subs", []) if s["name"] == DIVE["sub"]), None)
    if not sub:
        names = {c["name"]: [s["name"] for s in c["subs"]] for c in clusters if c["subs"]}
        raise SystemExit(f"DIVE: no sub-topic {DIVE['sub']!r} in a topic {DIVE['topic']!r}. The map has: {names}")
    home = {n["id"]: n["sub"] for n in nodes}
    inside = {(e["s"], e["t"]): e["t1"] + 2 * e["t2"] for e in edges if home[e["s"]] == home[e["t"]] == sub["id"]}
    cases = [inside.get(tuple(link)) for link in DIVE["read"]]
    if sorted(c for c in cases if c is not None) != [0, 1, 2, 3]:
        listing = "\n".join(f"  [{s}, {t}]: {WHO[case]}" for (s, t), case in sorted(inside.items(), key=lambda kv: kv[1]))
        raise SystemExit("DIVE: the four links to read must be in the sub-topic, one for each case. "
                         f"They are now {[WHO[c] if c is not None else 'not in the sub-topic' for c in cases]}.\n"
                         f"The links inside {DIVE['sub']!r}:\n{listing}")
    dive = {"topic": topic["id"], "sub": sub["id"], "read": DIVE["read"], "only": DIVE["only"]}
    return {"nodes": nodes, "edges": edges, "clusters": clusters, "dive": dive, "slow": slow}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--theme", choices=["light", "dark"], default="light")
    parser.add_argument("--slow", type=float, default=2, help="how many times slower than the first cut (default 2)")
    parser.add_argument("--out", type=Path, default=HERE / "page.html")
    args = parser.parse_args()
    data = page_data(args.slow)
    html = (HERE / "template.html").read_text(encoding="utf-8")
    for marker, value in (("/*DATA*/null", json.dumps(data, separators=(",", ":"))), ('/*THEME*/"light"', f'"{args.theme}"')):
        if html.count(marker) != 1:
            raise SystemExit(f"template.html: expected one {marker}")
        html = html.replace(marker, value)
    args.out.write_text(html, encoding="utf-8")
    count = lambda rows, a, b: sum(r["t1"] == a and r["t2"] == b for r in rows)   # noqa: E731
    for what, rows in (("links", data["edges"]), ("terms", data["nodes"])):
        print(f"{what}: {len(rows)}; this book only {count(rows, False, False)}, the first text too {count(rows, True, False)}, "
              f"the second {count(rows, False, True)}, both {count(rows, True, True)}")
    print(f"wrote {args.out.name}: {args.theme} theme, {args.slow:g} times slower than the first cut")


if __name__ == "__main__":
    main()
