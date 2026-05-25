# `sparklines.json` schema

The contract between the **producer**
([`scripts/server/build-sparklines.py`](../../scripts/server/build-sparklines.py),
running nightly on the server) and the **consumer**
([`_static/js/telemetry.js`](../../_static/js/telemetry.js), running in
every reader's browser).

If you change either side without updating the other, the sidebar
sparkline goes blank. This file is the single source of truth for the
contract.

## Public URL

```
https://learnche.org/_stats/sparklines.json
```

* Same origin as the book → no CORS concern from `learnche.org/pid/*`.
* Served by Caddy with `Cache-Control: public, max-age=3600` (1 hour)
  so browsers reuse the response across a reading session. The cron
  refreshes the file once a day, so the worst-case staleness is
  about 25 hours.
* Anyone may read it. Aggregate-only, no IPs, no UAs, no referrers.

## Top-level shape

A flat JSON object whose keys are page identifiers and whose values
are time series:

```json
{
  "<pagename>": [
    ["<YYYY-MM-DD>", <count>],
    ["<YYYY-MM-DD>", <count>],
    ...
  ],
  ...
}
```

* The producer writes JSON with no whitespace and `sort_keys=True`.
  The consumer must not depend on key order.
* Top-level value is **always an object** (never an array, never
  null). An empty book would yield `{}`.

## Page-key contract

The page key is the **Sphinx pagename** — the same value you get from
`{{ pagename }}` in a Jinja template, or `pagename` in a sphinx
extension event.

Examples:

| Reader URL | `pagename` (= JSON key) |
|---|---|
| `https://learnche.org/pid/contents` | `contents` |
| `https://learnche.org/pid/` | `contents` |
| `https://learnche.org/pid/data-visualization/box-plots` | `data-visualization/box-plots` |
| `https://learnche.org/pid/data-visualization/` | `data-visualization/index` |
| `https://learnche.org/pid/privacy` | `privacy` |
| `https://learnche.org/pid/preface/index` | `preface/index` |

Rules the producer follows (see `normalise_pagename` in
[`build-sparklines.py`](../../scripts/server/build-sparklines.py)):

* Drop the leading `/pid/` prefix.
* `/pid` and `/pid/` both fold to `contents` (the `master_doc`).
* A trailing slash means an index page → append `/index`.
  `/pid/data-visualization/` → `data-visualization/index`.
* Strip any `.html` or `.htm` suffix that a scraper might have
  guessed. Real readers never see `.html` URLs (`html_file_suffix
  = ""` in `conf.py`), but scrapers may invent them.
* Strip query strings and fragments (`?utm=...`, `#section`).
* Drop `/_static/...`, `/_sources/...`, `/_images/...`, `/pagefind/...`,
  `/search`, `/genindex`, `/py-modindex` — these are infrastructure
  endpoints, not pages.

Rules the consumer follows (see `renderSparkline` in
[`telemetry.js`](../../_static/js/telemetry.js)):

* Read the key from `data-page` on the `#pid-sparkline` mount, which
  the Jinja template populates from `{{ pagename }}`.
* Fallback: derive from `location.pathname` by stripping `/pid/`,
  trailing slash, and `.html?` — should match the producer rules
  above. If everything strips to empty, use `contents`.
* If the key is **not** in the JSON, hide the mount. **Do not** show a
  zero-height chart, "0 hits" placeholder, or error message.

## Time-series contract

Each value is an array of `[date, count]` pairs.

```json
"data-visualization/box-plots": [
  ["2026-02-10", 12],
  ["2026-02-11", 9],
  ["2026-02-12", 14],
  ...
]
```

* `date` is an **ISO 8601 calendar date** in `YYYY-MM-DD` form, in
  the server's local timezone (UTC on Hetzner).
* `count` is a **non-negative integer**: the number of distinct
  client IPs that hit that page on that date, after bot filtering and
  excluding static assets and non-2xx responses.
* The array is **sorted ascending by date**.
* The array is **dense** — every day in the window where there was
  at least one hit appears exactly once. **Days with zero hits are
  omitted.** The consumer should not assume the array length equals
  the window length.
* The window is **the most recent 365 days** (configurable via the
  producer's `[windows] days` setting, but the JS assumes 90 in its
  layout). If you change the window length on the server, also
  update the sidebar heading text in
  `_templates/pid-sidebar-extra.html` (`"Page views (365 days)"`).
* If a page got at least one hit in the window, its entry exists.
* If a page got **zero hits** in the window, it is **not** in the
  JSON. The consumer treats missing keys and empty arrays
  identically (hide the mount).

## Why daily unique IPs, not raw hits

Two readers refreshing the page should not double-count. Daily unique
IPs is the rough proxy for "distinct readers per day" used by most
log analytics tools. We deliberately do **not** persist IPs — they are
collected only long enough to deduplicate within a `(pagename, date)`
bucket and are then discarded. The output JSON contains only
counts.

This means a single user reading on weekday morning and weekday
evening counts once for that day; a user who reads on Monday and
again on Tuesday counts once per day. Privacy- and CGNAT-related
caveats:

* Two roommates sharing a NAT will look like one reader.
* A user on a mobile network whose IP rotates across the day will
  look like multiple readers.

These distortions are inherent to log-based analytics; we do not try
to correct them with cookies or fingerprinting.

## Bot exclusion

UAs matching any substring in `/etc/pid-book/bots.txt` (or the
producer's `FALLBACK_BOT_SUBSTRINGS` if no file is present) are
dropped. The list covers search-engine crawlers, AI training bots,
SEO crawlers, archive bots, social-media unfurlers, and headless
browsers / HTTP libraries.

The list is shared with GoAccess via
[`scripts/server/goaccessrc.example`](../../scripts/server/goaccessrc.example)
so both pipelines exclude the same UAs.

## Forward-compatibility

The schema is **append-only**. The consumer (`telemetry.js`)
reads `data[pageKey]`, expects an array of `[string, number]` pairs,
and ignores anything it doesn't recognise. Safe forward changes:

* **Adding new top-level keys.** Old browsers ignore them.
* **Lengthening the window** (e.g. to 180 days). Old browsers render
  whatever they receive; the heading text in the sidebar is the only
  thing that becomes stale.
* **Adding fields inside each point** (e.g. `[date, count, country_count]`).
  The consumer reads `point[0]` and `point[1]`, so a third element is
  silently ignored. **Do not** repurpose `point[1]` for anything
  other than a single non-negative integer count.

Breaking changes that would require a coordinated client release:

* **Renaming page keys.** If we ever change Sphinx's `master_doc` from
  `contents` or rename a chapter directory, the producer naming and
  consumer fallback must change together. **Both sides reference
  `pagename` for this reason — keep that as the single contract
  point.**
* **Changing the date format.** ISO 8601 only.
* **Switching to per-hour buckets.** Would need a different filename
  (`sparklines-hourly.json`) so the existing daily consumers don't
  break.

## Atomicity

The producer writes to a temporary file in the same directory as the
output and uses `os.replace()` to move it into place. On Linux with a
single filesystem this is **atomic** — readers either see the previous
file or the new one, never a partial. The 0644 permissions are set
before the rename so the rename itself is the only critical step.

## Example file

```json
{
  "contents": [
    ["2026-02-10", 87],
    ["2026-02-11", 92],
    ["2026-02-13", 64]
  ],
  "data-visualization/box-plots": [
    ["2026-02-10", 12],
    ["2026-02-11", 9],
    ["2026-02-12", 14]
  ],
  "preface/index": [
    ["2026-02-12", 3]
  ]
}
```

(The producer writes this with no whitespace; pretty-print it for
debugging by piping through `python -m json.tool`.)

## Diagnostics

Quick checks the maintainer can run:

```sh
# Does the file exist and is it valid JSON?
curl -sf https://learnche.org/_stats/sparklines.json | python -m json.tool >/dev/null && echo OK

# How many pages have data?
curl -sf https://learnche.org/_stats/sparklines.json | python -c "
import json, sys
d = json.load(sys.stdin)
print(len(d), 'pages,', sum(len(v) for v in d.values()), 'total points')"

# Top 10 most-active pages by sum-of-counts in the window:
curl -sf https://learnche.org/_stats/sparklines.json | python -c "
import json, sys
d = json.load(sys.stdin)
top = sorted(d.items(), key=lambda kv: -sum(p[1] for p in kv[1]))[:10]
for k, v in top:
    print(sum(p[1] for p in v), k)"

# Spot-check a known page:
curl -sf https://learnche.org/_stats/sparklines.json |
  python -c "import json,sys; print(json.load(sys.stdin).get('data-visualization/box-plots'))"
```

If `sparklines.json` ever becomes a bottleneck (e.g. > 1 MB), revisit
the schema — but for a book with O(100) pages and 365 days of daily
counts, the file is ~50–200 KB depending on activity, well below any
problematic threshold.
