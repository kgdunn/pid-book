"""Check a reviewer's result file: every quote must appear on the line it cites, and every input node and edge must be covered."""
import json
import sys
from pathlib import Path

BOOK = Path("/home/user/pid-book")
AUDIT = Path("/tmp/claude-0/-home-user/f5de32d9-e9cf-527e-9ba3-c74ed25f6ef9/scratchpad/audit")
lines_of = {}


def quote_ok(evidence: str, quote: str) -> str | None:
    """None when the quote is on the cited line (or the line next to it), else the reason."""
    if not evidence or not quote:
        return "no evidence or quote"
    path, _, num = evidence.rpartition(":")
    if not path or not num.isdigit():
        return f"bad evidence {evidence!r}"
    f = BOOK / path
    if not f.exists():
        return f"no file {path}"
    if path not in lines_of:
        lines_of[path] = f.read_text(encoding="utf-8").splitlines()
    text = lines_of[path]
    i = int(num) - 1
    near = " ".join(text[max(0, i - 1): i + 2])
    norm = lambda s: " ".join(s.split())
    if norm(quote) in norm(near):
        return None
    return "quote not on that line" + (" (but elsewhere in file)" if norm(quote) in norm(" ".join(text)) else "")


def main(group: str) -> None:
    res = json.loads((AUDIT / f"result_{group}.json").read_text())
    bad, verdicts = [], {}
    for kind in ("nodes", "edges", "missing"):
        for item in res.get(kind, []):
            key = item.get("id") or item.get("name") or f"{item.get('source')} {item.get('relation')} {item.get('target')}"
            verdicts.setdefault(kind, {}).setdefault(item.get("verdict", "proposed"), 0)
            verdicts[kind][item.get("verdict", "proposed")] += 1
            why = quote_ok(item.get("evidence", ""), item.get("quote", ""))
            if why and item.get("verdict") != "not_in_book":
                bad.append(f"{kind}: {key}: {why}")
    if group in ("A", "B", "C", "D"):  # E, F and G propose new terms only
        inp = json.loads((AUDIT / f"input_{group}.json").read_text())
        seen_n = {n["id"] for n in res["nodes"]}
        seen_e = {(e["source"], e["relation"], e["target"]) for e in res["edges"]}
        bad += [f"node not covered: {n['id']}" for n in inp["nodes"] if n["id"] not in seen_n]
        bad += [f"edge not covered: {tuple(e)}" for e in inp["edges"] if tuple(e) not in seen_e]
    print(group, json.dumps(verdicts))
    print(f"  {len(bad)} problems" + "".join(f"\n  - {b}" for b in bad[:25]))


if __name__ == "__main__":
    for g in sys.argv[1:]:
        if (AUDIT / f"result_{g}.json").exists():
            main(g)
        else:
            print(g, "no result yet")
