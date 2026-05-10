#!/usr/bin/env python3
"""Build /var/www/learnche.org/_stats/sparklines.json from access logs.

Run nightly on the production webserver. Designed to be deployable as a
single file with no external dependencies (stdlib only) so it works on a
minimal server install.

Output schema is described in docs/telemetry/sparklines-schema.md.
The output file is consumed by _static/js/telemetry.js to render the
90-day pageview sparkline in the sidebar of every book page.

Inputs
------
The script auto-detects the log format on a per-line basis and supports:

* **Caddy JSON access logs** — the production webserver is Caddy, which
  emits one JSON object per line (the default `json` encoder). Fields
  used: ``ts`` (Unix seconds, may be float), ``request.remote_ip``
  (or ``request.remote_addr``), ``request.method``, ``request.uri``,
  ``request.headers.User-Agent`` (array), ``status``.
* **Apache / generic combined-format** — used by the archived
  pre-Hetzner Apache logs and as a fallback for any future webserver
  swap. Each line is parsed with ``LOG_RE``.

Each line is tried as JSON first; if that fails, we fall back to the
combined-format regex. Mixed-format inputs are fine.

Algorithm
---------
1. Stream every line from the configured log files (gzip-aware).
2. Parse: client_ip, timestamp, request line, status, user-agent.
3. Drop bots by user-agent substring match (shared list with
   /etc/pid-book/bots.txt — see scripts/server/bots.txt.example).
4. Drop static assets and non-2xx responses.
5. Drop hits outside the /pid/ prefix.
6. Normalise URL path → Sphinx pagename:
       /pid/                          → contents
       /pid/contents                  → contents
       /pid/data-visualization/       → data-visualization/index
       /pid/data-visualization/box-plots → data-visualization/box-plots
   (Trailing slash means index page.)
7. Aggregate (pagename, date) → set of unique IPs.
8. Convert to (pagename, date) → unique-IP count for the last 90 days.
9. Atomically write JSON to the output path.

Privacy
-------
IPs are used only to deduplicate within a single (pagename, date) bucket
and are then discarded. The on-disk JSON contains no IPs, no UAs, no
referrers — only counts.

Usage
-----
    build-sparklines.py [--config /etc/pid-book/sparklines.conf]

Default config path is /etc/pid-book/sparklines.conf if it exists,
otherwise the defaults below. The config is a tiny INI file:

    [paths]
    logs = /var/log/caddy/learnche.org.access.log* /var/log/learnche-archive/access.log*
    output = /var/www/learnche.org/_stats/sparklines.json
    bot_list = /etc/pid-book/bots.txt

    [windows]
    days = 90

The bot list is one user-agent substring per line; lines starting with
'#' are comments. Any UA containing one of the substrings (case-
insensitive) is dropped.
"""

from __future__ import annotations

import argparse
import configparser
import datetime as dt
import glob
import gzip
import io
import json
import logging
import os
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

LOG = logging.getLogger("build-sparklines")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = "/etc/pid-book/sparklines.conf"

DEFAULT_LOG_GLOBS = [
    # Caddy's default per-host log path on Debian/Ubuntu installs.
    "/var/log/caddy/learnche.org.access.log*",
    # Archived pre-Hetzner Apache logs (combined format).
    "/var/log/learnche-archive/access.log*",
]
DEFAULT_OUTPUT = "/var/www/learnche.org/_stats/sparklines.json"
DEFAULT_BOT_LIST = "/etc/pid-book/bots.txt"
DEFAULT_DAYS = 90

# Bot UA substrings used when no bot_list file is present. Keep in sync with
# scripts/server/goaccessrc.example.
FALLBACK_BOT_SUBSTRINGS = [
    "googlebot",
    "bingbot",
    "yandexbot",
    "duckduckbot",
    "baiduspider",
    "applebot",
    "petalbot",
    "ahrefsbot",
    "semrushbot",
    "mj12bot",
    "dotbot",
    "bytespider",
    "facebookexternalhit",
    "twitterbot",
    "linkedinbot",
    "slackbot",
    "discordbot",
    "telegrambot",
    "whatsapp",
    "gptbot",
    "ccbot",
    "claudebot",
    "anthropic-ai",
    "perplexitybot",
    "cohere-ai",
    "amazonbot",
    "google-extended",
    "archive.org_bot",
    "ia_archiver",
    "wayback",
    "headlesschrome",
    "phantomjs",
    "puppeteer",
    "python-requests",
    "curl/",
    "wget/",
    "go-http-client",
    "okhttp/",
    "axios/",
    "node-fetch",
]

# Static-asset extensions to ignore. The book serves these, but they aren't
# pageviews. Keep in sync with run-goaccess.sh's --static-file flags.
STATIC_EXTS = {
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
    ".ico", ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".pdf", ".zip", ".csv", ".tsv", ".xlsx", ".xls", ".tar", ".gz",
    ".map", ".txt",
}

# Combined-format regex (Apache / generic).
#
#   <ip> - <user> [<time>] "<method> <path> <proto>" <status> <bytes>
#   "<referer>" "<user-agent>"
#
# Tolerant of extra fields some webservers append (e.g. request_time).
LOG_RE = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<proto>[^"]+)"\s+'
    r'(?P<status>\d+)\s+(?P<bytes>\S+)\s+'
    r'"(?P<referer>[^"]*)"\s+'
    r'"(?P<ua>[^"]*)"'
)

# Apache's typical date format: 10/May/2026:04:17:23 +0000
TIME_FMT = "%d/%b/%Y:%H:%M:%S %z"


# ---------------------------------------------------------------------------
# Per-line record produced by either parser.
# ---------------------------------------------------------------------------


class Hit:
    """Minimal struct-like holder for a parsed log line."""
    __slots__ = ("ip", "method", "path", "status", "ua", "ts")

    def __init__(self, ip: str, method: str, path: str, status: str,
                 ua: str, ts: dt.datetime) -> None:
        self.ip = ip
        self.method = method
        self.path = path
        self.status = status
        self.ua = ua
        self.ts = ts


def parse_caddy_json(line: str) -> Hit | None:
    """Parse a Caddy JSON access-log line. Return None on any mismatch.

    Caddy's default JSON encoder emits one object per line with at least
    these fields when ``msg == "handled request"``:

        {"ts": 1746866243.123,
         "msg": "handled request",
         "request": {
            "remote_ip": "203.0.113.5",          # Caddy ≥ 2.7
            "remote_addr": "203.0.113.5:54321",  # older Caddy
            "method": "GET",
            "uri": "/pid/contents",
            "headers": { "User-Agent": ["Mozilla/5.0"] }
         },
         "status": 200,
         ...}

    See https://caddyserver.com/docs/json/logging/ for the full schema.
    """
    if not line or line[0] != "{":
        return None
    try:
        obj = json.loads(line)
    except ValueError:
        return None
    if not isinstance(obj, dict):
        return None
    # Most Caddy access entries have msg == "handled request"; tolerate
    # absence (some configs emit the message at debug level).
    msg = obj.get("msg")
    if msg is not None and msg != "handled request":
        return None
    req = obj.get("request") or {}
    if not isinstance(req, dict):
        return None

    ip = req.get("remote_ip") or ""
    if not ip:
        addr = req.get("remote_addr") or ""
        # remote_addr is "ip:port"; rsplit handles IPv6 forms like
        # "[2001:db8::1]:443".
        if addr.startswith("["):
            end = addr.find("]")
            if end > 0:
                ip = addr[1:end]
        elif ":" in addr:
            ip = addr.rsplit(":", 1)[0]
        else:
            ip = addr
    method = req.get("method") or ""
    path = req.get("uri") or ""
    status = obj.get("status")
    if status is None:
        return None
    headers = req.get("headers") or {}
    ua_list = headers.get("User-Agent") or headers.get("user-agent") or []
    ua = ua_list[0] if isinstance(ua_list, list) and ua_list else ""

    ts_raw = obj.get("ts")
    if ts_raw is None:
        return None
    try:
        ts = dt.datetime.fromtimestamp(float(ts_raw), tz=dt.timezone.utc)
    except (TypeError, ValueError, OSError):
        return None

    return Hit(ip=ip, method=method, path=path, status=str(status),
               ua=ua, ts=ts)


def parse_combined(line: str) -> Hit | None:
    """Parse an Apache / generic combined-format line."""
    m = LOG_RE.match(line)
    if not m:
        return None
    try:
        ts = dt.datetime.strptime(m["time"], TIME_FMT)
    except ValueError:
        return None
    return Hit(ip=m["ip"], method=m["method"], path=m["path"],
               status=m["status"], ua=m["ua"], ts=ts)


def parse_line(line: str) -> Hit | None:
    """Try Caddy JSON first; fall back to combined-format. None if neither."""
    return parse_caddy_json(line) or parse_combined(line)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def load_bot_substrings(path: str) -> list[str]:
    if not path or not os.path.exists(path):
        return list(FALLBACK_BOT_SUBSTRINGS)
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            out.append(s.lower())
    return out or list(FALLBACK_BOT_SUBSTRINGS)


def open_log(path: str) -> io.TextIOBase:
    """Open a log file, transparently handling .gz."""
    if path.endswith(".gz"):
        return io.TextIOWrapper(gzip.open(path, "rb"), encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")


def expand_globs(globs: list[str]) -> list[str]:
    out: list[str] = []
    for g in globs:
        out.extend(sorted(glob.glob(g)))
    # Deduplicate while preserving order.
    seen: set[str] = set()
    unique = []
    for p in out:
        if p in seen:
            continue
        seen.add(p)
        unique.append(p)
    return unique


def is_bot(ua: str, bot_substrings: list[str]) -> bool:
    if not ua:
        return True  # treat empty UA as bot
    ual = ua.lower()
    return any(b in ual for b in bot_substrings)


def is_static(path: str) -> bool:
    base = path.split("?", 1)[0].split("#", 1)[0].lower()
    _, ext = os.path.splitext(base)
    return ext in STATIC_EXTS


def normalise_pagename(path: str) -> str | None:
    """Return the canonical Sphinx pagename for a request URI, or None.

    Returns None for hits outside /pid/, for static assets, and for the
    Pagefind / Sphinx-search internal endpoints.
    """
    raw = path.split("?", 1)[0].split("#", 1)[0]
    if not raw.startswith("/pid"):
        return None
    rest = raw[len("/pid"):]
    # Strip leading slash. /pid -> "", /pid/ -> "", /pid/foo -> "foo"
    if rest.startswith("/"):
        rest = rest[1:]
    # /pid and /pid/ both map to the homepage = contents.
    if rest in ("", "/"):
        return "contents"
    # Drop trailing slash (treat /foo/ as /foo/index for clarity).
    if rest.endswith("/"):
        rest = rest[:-1] + "/index"
    # Strip any .html or .htm suffix that a scraper might have guessed.
    rest = re.sub(r"\.html?$", "", rest, flags=re.IGNORECASE)
    # Internal endpoints that aren't book pages.
    if rest in ("search", "genindex", "py-modindex"):
        return None
    if rest.startswith("_static/") or rest.startswith("_sources/") or rest.startswith("_images/"):
        return None
    if rest.startswith("pagefind/") or rest == "pagefind":
        return None
    return rest


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def build(
    log_globs: list[str],
    output_path: str,
    bot_list: str,
    days: int,
) -> None:
    bot_substrings = load_bot_substrings(bot_list)
    log_paths = expand_globs(log_globs)
    if not log_paths:
        LOG.error("no log files matched: %s", log_globs)
        sys.exit(2)

    today = dt.date.today()
    cutoff = today - dt.timedelta(days=days - 1)

    # (pagename, date) -> set[ip]
    buckets: dict[tuple[str, dt.date], set[str]] = defaultdict(set)
    parsed = matched = 0

    for path in log_paths:
        LOG.info("scanning %s", path)
        try:
            fh = open_log(path)
        except OSError as e:
            LOG.warning("skip %s: %s", path, e)
            continue
        with fh:
            for line in fh:
                parsed += 1
                hit = parse_line(line)
                if hit is None:
                    continue
                if hit.status not in ("200", "304"):
                    continue
                if hit.method not in ("GET", "HEAD"):
                    continue
                if is_bot(hit.ua, bot_substrings):
                    continue
                if is_static(hit.path):
                    continue
                pagename = normalise_pagename(hit.path)
                if pagename is None:
                    continue
                day = hit.ts.date()
                if day < cutoff or day > today:
                    continue
                buckets[(pagename, day)].add(hit.ip)
                matched += 1

    LOG.info("parsed %d lines, matched %d hits across %d buckets",
             parsed, matched, len(buckets))

    # Convert to per-page chronological [[date, count], ...] arrays.
    by_page: dict[str, list[tuple[dt.date, int]]] = defaultdict(list)
    for (page, day), ips in buckets.items():
        by_page[page].append((day, len(ips)))

    out: dict[str, list[list]] = {}
    for page, points in by_page.items():
        points.sort(key=lambda p: p[0])
        out[page] = [[d.isoformat(), n] for (d, n) in points]

    write_atomic(output_path, out)
    LOG.info("wrote %d pages to %s", len(out), output_path)


def write_atomic(output_path: str, payload: dict) -> None:
    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".sparklines-", suffix=".json", dir=out_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, separators=(",", ":"), sort_keys=True)
            f.write("\n")
        os.chmod(tmp, 0o644)
        os.replace(tmp, output_path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--config", default=DEFAULT_CONFIG,
                   help="Path to .conf file (INI format). Optional.")
    p.add_argument("--logs", nargs="+", default=None,
                   help="Override log globs.")
    p.add_argument("--output", default=None,
                   help="Override output JSON path.")
    p.add_argument("--bot-list", default=None,
                   help="Override bot UA substring list path.")
    p.add_argument("--days", type=int, default=None,
                   help="Override window length (default: 90).")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    cfg = configparser.ConfigParser()
    if os.path.exists(args.config):
        cfg.read(args.config)

    log_globs = (args.logs
                 or cfg.get("paths", "logs", fallback="").split()
                 or DEFAULT_LOG_GLOBS)
    output = (args.output
              or cfg.get("paths", "output", fallback="")
              or DEFAULT_OUTPUT)
    bot_list = (args.bot_list
                or cfg.get("paths", "bot_list", fallback="")
                or DEFAULT_BOT_LIST)
    days = (args.days
            or cfg.getint("windows", "days", fallback=0)
            or DEFAULT_DAYS)

    build(log_globs=log_globs, output_path=output,
          bot_list=bot_list, days=days)


if __name__ == "__main__":
    main()
