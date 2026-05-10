#!/usr/bin/env python3
"""Convert Caddy JSON access-log lines (stdin) to Apache combined format (stdout).

GoAccess understands Apache combined natively but not Caddy's JSON
format. This script is a thin filter so the same `goaccess` invocation
can consume both the live Caddy logs and the archived pre-Hetzner
Apache logs in the same pipeline.

Lines that are not Caddy JSON are passed through unchanged, so a mix of
JSON and combined files can be cat'd together and piped here.

Usage:
    zcat -f /var/log/caddy/access.log* /var/log/learnche-archive/access.log* |
        caddy-json-to-combined.py |
        goaccess - --log-format=COMBINED ...

No external dependencies — stdlib only.
"""

from __future__ import annotations

import datetime as dt
import json
import sys


def _strip_port(addr: str) -> str:
    """Return the IP portion of a Caddy `remote_addr` value.

    Handles IPv4 (``a.b.c.d:port``), bracketed IPv6 (``[::1]:port``),
    and bare values. Imperfect on bare IPv6 with no brackets, but Caddy
    always brackets IPv6 addresses, so the imperfection never triggers.
    """
    if not addr:
        return ""
    if addr.startswith("["):
        end = addr.find("]")
        if end > 0:
            return addr[1:end]
        return addr
    if addr.count(":") == 1:
        return addr.rsplit(":", 1)[0]
    return addr


def _convert(line: str) -> str | None:
    """Return a combined-format line, or None to pass `line` through."""
    if not line or line[0] != "{":
        return None
    try:
        obj = json.loads(line)
    except ValueError:
        return None
    if not isinstance(obj, dict):
        return None
    msg = obj.get("msg")
    if msg is not None and msg != "handled request":
        return ""  # drop non-request log lines (errors, startup, etc.)

    req = obj.get("request") or {}
    if not isinstance(req, dict):
        return None
    ip = req.get("remote_ip") or _strip_port(req.get("remote_addr") or "") or "-"
    method = req.get("method") or "-"
    path = req.get("uri") or "-"
    status = obj.get("status")
    if status is None:
        return None

    headers = req.get("headers") or {}
    ua_list = headers.get("User-Agent") or headers.get("user-agent") or []
    ua = ua_list[0] if isinstance(ua_list, list) and ua_list else "-"
    ref_list = headers.get("Referer") or headers.get("referer") or []
    referer = ref_list[0] if isinstance(ref_list, list) and ref_list else "-"

    size = obj.get("size")
    if size is None:
        size = "-"

    ts_raw = obj.get("ts")
    try:
        ts = dt.datetime.fromtimestamp(float(ts_raw), tz=dt.timezone.utc)
    except (TypeError, ValueError, OSError):
        return None
    when = ts.strftime("%d/%b/%Y:%H:%M:%S +0000")

    # Quote-escape anything that could break the combined format. Caddy
    # already URL-encodes the URI, but UA / Referer can contain quotes.
    ua = ua.replace('"', "%22")
    referer = referer.replace('"', "%22")

    return (f'{ip} - - [{when}] "{method} {path} HTTP/1.1" '
            f'{status} {size} "{referer}" "{ua}"')


def main() -> None:
    out = sys.stdout
    for raw in sys.stdin:
        line = raw.rstrip("\n")
        converted = _convert(line)
        if converted is None:
            # Pass through (probably already combined).
            out.write(line + "\n")
        elif converted == "":
            # Drop (non-request log message).
            continue
        else:
            out.write(converted + "\n")


if __name__ == "__main__":
    main()
