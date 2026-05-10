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

```
/etc/pid-book/
  goaccessrc                  # GoAccess config; see goaccessrc.example
  sparklines.conf             # build-sparklines.py config; see .example
  bots.txt                    # shared UA blocklist; see bots.txt.example

/usr/local/bin/
  run-goaccess.sh             # symlink → /opt/pid-book/scripts/server/run-goaccess.sh
  build-sparklines.py         # symlink → /opt/pid-book/scripts/server/build-sparklines.py

/opt/pid-book/                # git checkout of kgdunn/pid-book master
  scripts/server/             # owns the canonical scripts

/var/log/nginx/
  learnche.org.access.log     # current
  learnche.org.access.log.*   # rotated, possibly .gz

/var/log/learnche-archive/
  access.log*                 # archived pre-Hetzner Apache logs

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
apt-get install -y goaccess python3 git nginx
# python3 stdlib only — build-sparklines.py has no third-party deps.
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
ln -s /opt/pid-book/scripts/server/run-goaccess.sh      /usr/local/bin/run-goaccess.sh
ln -s /opt/pid-book/scripts/server/build-sparklines.py  /usr/local/bin/build-sparklines.py
chmod +x /opt/pid-book/scripts/server/run-goaccess.sh
chmod +x /opt/pid-book/scripts/server/build-sparklines.py
```

### 4. Pull pre-Hetzner Apache logs (one-shot)

The owner has the old Apache logs from before the Hetzner migration.
Pull them once and never touch again — they are immutable history.

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

The current nginx logs live in `/var/log/nginx/`; the rotation is
managed by the standard `/etc/logrotate.d/nginx`. Rotation **must**
keep at least 90 days for the sparkline window. Confirm:

```sh
grep -E '^\s*rotate' /etc/logrotate.d/nginx
# rotate 14 → not enough. Increase to at least 95.
```

If your distro defaults to a shorter retention, edit the rotate count
or pass `--days <n>` to `build-sparklines.py` to match what you
actually keep.

### 5. nginx config for /_stats/

Add to the `learnche.org` server block:

```nginx
# Public stats: GoAccess HTML report + sparklines.json.
location /_stats/ {
    alias /var/www/learnche.org/_stats/;
    autoindex off;
    add_header Cache-Control "public, max-age=3600";
    types {
        text/html  html;
        application/json json;
    }
    default_type text/html;
}
```

Reload:

```sh
nginx -t && systemctl reload nginx
mkdir -p /var/www/learnche.org/_stats
chown www-data:www-data /var/www/learnche.org/_stats
```

The `Cache-Control: max-age=3600` is the staleness budget for browser
caches — see [`sparklines-schema.md`](sparklines-schema.md). The cron
runs nightly, so worst-case staleness is ~25 hours.

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
2. Pipes them all through `zcat -f` into `goaccess -` so a single
   process sees the union.
3. Reads `/etc/pid-book/goaccessrc` (if present) for bot-filter and
   panel config — this file mirrors
   [`scripts/server/goaccessrc.example`](../../scripts/server/goaccessrc.example).
4. Writes to a `mktemp` file in the output directory and `mv`s into
   place, so the public file is never seen partial.
5. Logs the result line so the cron-mail tail is meaningful.

Common overrides via env (set in the cron line if you need them):

* `LOG_GLOBS` — space-separated globs.
* `OUTPUT_FILE` — full path of the HTML report (default
  `/var/www/learnche.org/_stats/index.html`).
* `GOACCESS_CONF` — alternative config path.

## How `build-sparklines.py` works

[`scripts/server/build-sparklines.py`](../../scripts/server/build-sparklines.py)
is stdlib-only Python. Algorithm:

1. Read config from `/etc/pid-book/sparklines.conf` (if present),
   override with CLI flags.
2. Expand log globs the same way `run-goaccess.sh` does.
3. Stream every line, parse the combined-format regex
   (`LOG_RE`), drop:
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

* **nginx access logs** rotate per `/etc/logrotate.d/nginx`. Keep at
  least 95 days (90 for the window + 5 days slack).
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

* Are the log globs matching? Add `--logs '/var/log/nginx/learnche.org.access.log*'`
  explicitly.
* Are all hits being dropped as bots? Try `--bot-list /dev/null` for
  a one-shot run that uses the fallback list — if that helps,
  `bots.txt` is over-broad.
* Are timestamps in a different timezone than the script expects?
  The combined-format `[10/May/2026:04:17:23 +0000]` is parsed with
  `%z`, so any TZ should work. Check that the log line actually
  matches `LOG_RE` — `--verbose` will show the parsed/matched counts.

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
