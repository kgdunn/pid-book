# Server-side runbook

Everything that runs on the production server (`139.162.148.246`,
Hetzner) to make the telemetry layer work end to end. Read this if
you are setting up a new server, troubleshooting why
`/_stats/sparklines.json` is stale, or porting the pipeline to a
different host.

The reference scripts live in
[`scripts/server/`](../../scripts/server/) — pull them straight from
git rather than copy-pasting from this doc, so any future fix lands in
one place.

## Layout on the server

The production webserver is **Caddy**. Paths assume the standard Debian
package layout (`/etc/caddy/Caddyfile`, `/var/log/caddy/`); adjust if
your install differs.

```
/etc/pid-book/
  goaccessrc                  # GoAccess config; see goaccessrc.example
  sparklines.conf             # build-sparklines.py config; see .example
  bots.txt                    # shared UA blocklist; see bots.txt.example

/etc/caddy/
  Caddyfile                   # webserver config (snippet shown below)

/usr/local/bin/
  run-goaccess.sh             # symlink → /opt/pid-book/scripts/server/run-goaccess.sh
  build-sparklines.py         # symlink → /opt/pid-book/scripts/server/build-sparklines.py
  caddy-json-to-combined.py   # symlink → /opt/pid-book/scripts/server/caddy-json-to-combined.py

/opt/pid-book/                # git checkout of kgdunn/pid-book master
  scripts/server/             # owns the canonical scripts

/var/log/caddy/
  learnche.org.access.log     # current — JSON, one object per line
  learnche.org.access.log.*   # rotated by Caddy itself, possibly .gz

/var/log/learnche-archive/
  access.log*                 # archived pre-Hetzner Apache logs (combined)

/var/www/learnche.org/
  pid/                        # rsync'd from CI on master push
  _stats/                     # public dashboards
    index.html                # GoAccess output
    sparklines.json           # sparkline series

/etc/cron.d/pid-book-stats    # nightly cron entry
```

The git checkout at `/opt/pid-book` exists so the server uses the
**same** scripts that ship in the repo. To update the scripts:

```sh
cd /opt/pid-book && git pull --ff-only
```

No further deploy step needed — the symlinks pick up the new files
immediately.

## One-time setup

Run as root or via sudo. Everything assumes Debian/Ubuntu paths.

### 1. Install dependencies

```sh
apt-get update
apt-get install -y goaccess python3 git
# python3 stdlib only — build-sparklines.py has no third-party deps.
# Caddy is presumed already installed (it serves the book itself);
# if not: see https://caddyserver.com/docs/install.
```

`goaccess` ≥ 1.5 supports the flags we use; the Debian stable package
is fine.

### 2. Lay out config files

```sh
mkdir -p /etc/pid-book
git clone https://github.com/kgdunn/pid-book.git /opt/pid-book
cd /opt/pid-book

cp scripts/server/goaccessrc.example         /etc/pid-book/goaccessrc
cp scripts/server/sparklines.conf.example    /etc/pid-book/sparklines.conf
cp scripts/server/bots.txt.example           /etc/pid-book/bots.txt

# Edit if needed — defaults match this runbook.
```

### 3. Symlink the scripts onto PATH

```sh
ln -s /opt/pid-book/scripts/server/run-goaccess.sh           /usr/local/bin/run-goaccess.sh
ln -s /opt/pid-book/scripts/server/build-sparklines.py       /usr/local/bin/build-sparklines.py
ln -s /opt/pid-book/scripts/server/caddy-json-to-combined.py /usr/local/bin/caddy-json-to-combined.py
chmod +x /opt/pid-book/scripts/server/*.sh
chmod +x /opt/pid-book/scripts/server/*.py
```

`run-goaccess.sh` resolves `caddy-json-to-combined.py` relative to its
own directory, so the symlink on PATH is convenience for manual use,
not a load-bearing dependency.

### 4. Pull pre-Hetzner Apache logs (one-shot)

The owner has the old Apache logs from before the Hetzner migration.
Pull them once and never touch again — they are immutable history.
These are **Apache combined format**; the JSON filter in
`run-goaccess.sh` passes combined-format lines through unchanged, so a
single pipeline handles both archive (combined) and current (Caddy
JSON) sources.

```sh
mkdir -p /var/log/learnche-archive
chown root:adm /var/log/learnche-archive
chmod 750     /var/log/learnche-archive

# From a workstation with SSH access to both hosts:
ssh oldhost 'tar czf - /var/log/apache2/access.log*' \
  | ssh root@learnche.org 'tar xzf - -C /var/log/learnche-archive --strip-components=3'
```

After import:

```sh
ls -lh /var/log/learnche-archive/
# Should list access.log, access.log.1.gz, access.log.2.gz, ...
```

### 5. Caddy config for access logs and `/_stats/`

Caddy's default access log encoder is JSON, which is exactly what
`build-sparklines.py` and `caddy-json-to-combined.py` expect. The
relevant `learnche.org` site block in `/etc/caddy/Caddyfile`:

```caddyfile
learnche.org {
    # Site root — book lives under /pid/, dashboards under /_stats/.
    root * /var/www/learnche.org
    encode zstd gzip
    file_server

    # Public stats: GoAccess HTML report + sparklines.json.
    handle /_stats/* {
        header Cache-Control "public, max-age=3600"
        file_server
    }

    # Per-host access log. JSON encoder is the default; we keep it.
    log {
        output file /var/log/caddy/learnche.org.access.log {
            roll_size 50MiB
            roll_keep 95
            roll_keep_for 95d
        }
        format json
    }
}
```

Key points:

* **`format json`** — the default; explicit here for clarity. The
  pipeline depends on this; if you ever switch to a `transform` /
  `console` formatter, update `caddy-json-to-combined.py` or set the
  Caddyfile back to `json`.
* **`roll_size` / `roll_keep` / `roll_keep_for`** — Caddy rotates the
  log itself. The 95-day retention is ≥ the 90-day sparkline window
  with a few days slack. Increase if you want longer history.
* **`/_stats/*` handle** — same-origin under `learnche.org` so the
  sidebar `fetch("/_stats/sparklines.json")` does not need CORS
  headers. The 1-hour cache is the staleness budget for browser
  caches; the cron runs nightly so worst-case staleness is ~25 hours.

Reload:

```sh
caddy validate --config /etc/caddy/Caddyfile && systemctl reload caddy
mkdir -p /var/www/learnche.org/_stats
chown caddy:caddy /var/www/learnche.org/_stats
```

(The Caddy package on Debian/Ubuntu creates a `caddy` system user that
owns the served paths; substitute whatever user your install uses.)

### 6. Cron

```sh
cat >/etc/cron.d/pid-book-stats <<'EOF'
# Nightly readership pipeline for learnche.org/pid.
# Order matters: GoAccess first (longer-running), sparklines second.
17 4 * * *  root  /usr/local/bin/run-goaccess.sh && /usr/local/bin/build-sparklines.py >> /var/log/pid-book-stats.log 2>&1
EOF
chmod 644 /etc/cron.d/pid-book-stats
```

`04:17 UTC` was chosen to avoid the top-of-the-hour cron jam and to
fall during low-traffic hours (Hetzner is in Germany, so this is the
European pre-dawn).

To run once immediately and verify:

```sh
/usr/local/bin/run-goaccess.sh
/usr/local/bin/build-sparklines.py --verbose
ls -lh /var/www/learnche.org/_stats/
curl -sf https://learnche.org/_stats/sparklines.json | python3 -m json.tool | head
```

## How `run-goaccess.sh` works

[`scripts/server/run-goaccess.sh`](../../scripts/server/run-goaccess.sh):

1. Resolves log file paths from `LOG_GLOBS` (or its default), expanding
   shell globs to handle `.log` and `.log.gz` mixed.
2. Pipes them all through `zcat -f` into
   [`caddy-json-to-combined.py`](../../scripts/server/caddy-json-to-combined.py),
   which converts each Caddy JSON line to Apache combined format and
   passes already-combined lines (the archived Apache logs) through
   unchanged. The output stream is a uniform combined-format feed.
3. Pipes that into `goaccess -` so a single process sees the union.
4. Reads `/etc/pid-book/goaccessrc` (if present) for bot-filter and
   panel config — this file mirrors
   [`scripts/server/goaccessrc.example`](../../scripts/server/goaccessrc.example).
5. Writes to a `mktemp` file in the output directory and `mv`s into
   place, so the public file is never seen partial.
6. Logs the result line so the cron-mail tail is meaningful.

Common overrides via env (set in the cron line if you need them):

* `LOG_GLOBS` — space-separated globs.
* `OUTPUT_FILE` — full path of the HTML report (default
  `/var/www/learnche.org/_stats/index.html`).
* `GOACCESS_CONF` — alternative config path.
* `JSON_TO_COMBINED` — alternative path to the JSON filter (default is
  the sibling script in the same directory as `run-goaccess.sh`).

## How `caddy-json-to-combined.py` works

[`scripts/server/caddy-json-to-combined.py`](../../scripts/server/caddy-json-to-combined.py)
is a tiny stdlib-only stdin→stdout filter. For each input line:

* If the line starts with `{` and parses as a Caddy access-log JSON
  object (`msg == "handled request"` or absent, with a `request`
  field), emit one Apache combined-format line on stdout.
* If the line is JSON with a different `msg` (errors, startup, etc.),
  drop it silently.
* If the line is anything else (including non-JSON), pass it through
  unchanged.

The third behaviour is what lets us cat Caddy JSON and archived
Apache combined logs through the same pipe — the archived lines just
flow through and reach `goaccess` as-is.

IPv4 with port (`a.b.c.d:54321`) and bracketed IPv6
(`[2001:db8::1]:443`) are normalised to bare IPs. Bare IPv6 (no
brackets, no port) is left alone — Caddy always brackets IPv6
addresses, so this branch is never exercised in practice.

## How `build-sparklines.py` works

[`scripts/server/build-sparklines.py`](../../scripts/server/build-sparklines.py)
is stdlib-only Python. Algorithm:

1. Read config from `/etc/pid-book/sparklines.conf` (if present),
   override with CLI flags.
2. Expand log globs the same way `run-goaccess.sh` does.
3. Stream every line, dispatching through `parse_line()` which tries
   `parse_caddy_json()` first and falls back to `parse_combined()`.
   Lines that match neither (corrupt records, partial writes) are
   dropped silently. Drop also:
   * non-`200/304` responses,
   * non-`GET/HEAD` methods,
   * UAs matching the bot list (`/etc/pid-book/bots.txt` or fallback),
   * paths matching `STATIC_EXTS`,
   * paths outside `/pid/`,
   * timestamps outside the 90-day window.
4. For each surviving hit, normalise the URL to a Sphinx pagename
   via `normalise_pagename` (rules documented in
   [`sparklines-schema.md`](sparklines-schema.md)).
5. Bucket as `(pagename, date) -> set[ip]`.
6. Convert to `(pagename, date) -> count = len(ips)` and discard the
   IPs.
7. Build the per-page chronological array `[[date, count], ...]`.
8. `json.dump` to `<output>.tmp` then `os.replace()` into place
   atomically.

Key invariants:

* IPs are held in memory only long enough to deduplicate the daily
  bucket, then dropped. They never reach disk.
* The output file has 0644 permissions; the directory is writable
  only by root (and `www-data` for the rsync target — keep these
  separate).
* The script is idempotent — running it twice in a row produces
  byte-identical output (`json.dump(..., sort_keys=True,
  separators=(",", ":"))`).

## Bot filter maintenance

The bot list is the only piece of the pipeline that drifts over
time. Add a new entry whenever:

* GoAccess's "Visitors" panel shows a UA you don't recognise driving
  > 1 % of pageviews.
* A new AI-training bot is publicly announced (e.g. a new model
  vendor's crawler).
* A new search engine launches that you don't care about.

Edit `/etc/pid-book/bots.txt`. Both pipelines pick up the new entry
on the next run — no restart needed. Mirror entries you add into
[`scripts/server/bots.txt.example`](../../scripts/server/bots.txt.example)
in the repo so a future server reinstall starts from a current list.

## Log retention

* **Caddy access logs** rotate via Caddy's own `roll_size` /
  `roll_keep` / `roll_keep_for` directives in the Caddyfile (no
  `logrotate` involvement). Keep at least 95 days (90 for the window
  + 5 days slack); the example Caddyfile above sets exactly that.
* **`/var/log/learnche-archive/`** is the immutable pre-Hetzner
  history. **Do not** rotate or compress further; treat as
  append-only archival.
* **`/var/www/learnche.org/_stats/sparklines.json`** is regenerated
  nightly. No retention concern.
* **`/var/log/pid-book-stats.log`** is the cron output. Add to
  `logrotate` if it grows:

  ```
  /var/log/pid-book-stats.log {
      weekly
      rotate 4
      compress
      missingok
      notifempty
  }
  ```

The CLAUDE.md / Privacy promise is "raw logs rotate within 30 days".
We *exceed* that on purpose for the archived logs because they are
the data foundation for the multi-year sparkline view. The two are
not in conflict: the 30-day rule applies to **personally identifiable
data on the live system**; the archive contains historical IPs but is
behind a server-shell trust boundary, not a public endpoint.

If you ever decide you don't want even the archived IPs around, run:

```sh
zcat /var/log/learnche-archive/access.log* | \
    sed -E 's/^([0-9]{1,3}\.){3}[0-9]{1,3}/0.0.0.0/' | \
    gzip > /var/log/learnche-archive/anonymised.log.gz
rm /var/log/learnche-archive/access.log*
```

After that the sparkline counts will jump (every hit will look like
a different "unique IP" because they are all `0.0.0.0`) — accept
that one-time inflation or rebuild from the anonymised data with a
modified producer.

## Manual operations

### Smoke-test the JSON

```sh
sudo -u www-data /usr/local/bin/build-sparklines.py --verbose --output /tmp/sparklines.json
python3 -m json.tool /tmp/sparklines.json | head -40
```

If the output looks empty:

* Are the log globs matching? Add `--logs '/var/log/caddy/learnche.org.access.log*'`
  explicitly.
* Are all hits being dropped as bots? Try `--bot-list /dev/null` for
  a one-shot run that uses the fallback list — if that helps,
  `bots.txt` is over-broad.
* Are timestamps unparseable? Caddy JSON `ts` is a Unix epoch float
  parsed via `datetime.fromtimestamp(..., tz=UTC)`; the combined
  fallback's `[10/May/2026:04:17:23 +0000]` is parsed with `%z`. Both
  should work for any TZ. Check a sample line manually:
  `head -1 /var/log/caddy/learnche.org.access.log | python3 -c "import sys,json;print(json.loads(sys.stdin.read()))"`
  — the object should have `ts`, `request.method`, `request.uri`,
  `status`, and `request.headers["User-Agent"]`.

### Re-run GoAccess on demand

```sh
/usr/local/bin/run-goaccess.sh
ls -lh /var/www/learnche.org/_stats/index.html
```

### Inspect the cron mail

If `MAILTO` is set in `/etc/crontab`, errors arrive by email. To see
recent runs without mail:

```sh
tail -200 /var/log/pid-book-stats.log
```

### Rebuild from a different log set

E.g. reprocess a historical range:

```sh
/usr/local/bin/build-sparklines.py \
    --logs '/var/log/learnche-archive/access.log*' \
    --days 365 \
    --output /tmp/sparklines-historical.json
```

## What runs where, summary

| Component | Where it runs | Cadence |
|---|---|---|
| `make html` (Sphinx) | GitHub Actions runner | every push/PR |
| ECharts curl fetch | GitHub Actions runner | every non-PR push |
| rsync deploy | GitHub Actions runner | every non-PR push |
| GoatCounter pixel | reader's browser | every page load |
| Search-event hook | reader's browser | every keystroke (debounced) |
| Sparkline render | reader's browser | every page load with mount |
| `run-goaccess.sh` | webserver | nightly, 04:17 UTC |
| `build-sparklines.py` | webserver | nightly, 04:17 UTC, after GoAccess |
| Log rotation | webserver | per logrotate config |

Three different trust zones (CI, browser, server) collaborate; the
glue is the four files in [`_static/js/`](../../_static/js/),
[`scripts/server/`](../../scripts/server/), and `/_stats/`.
