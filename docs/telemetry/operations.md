# Operations: set up, verify, switch, disable, troubleshoot

Day-to-day operations cookbook. The other docs explain the design and
the code; this one is the procedure manual.

## First-time setup: GoatCounter Cloud account

The pixel layer (Layer B in [`architecture.md`](architecture.md))
points at GoatCounter's hosted SaaS, not a self-hosted instance.
Until somebody registers a site on goatcounter.com, the
`learnche-pid.goatcounter.com/count` requests the pixel makes will
404 silently — the page still works, but the dashboard stays empty.

This is a **one-time** setup. The cron jobs
([`run-goaccess.sh`](../../scripts/server/run-goaccess.sh) and
[`build-sparklines.py`](../../scripts/server/build-sparklines.py))
are independent of GoatCounter; they read Caddy logs and produce the
public `/_stats/` dashboards even with no GoatCounter account.
Skipping the account loses only: search-query events, country /
device breakdowns, and engagement-time signal. The popularity
ranking and per-page sparklines are fully covered by the log-side
pipeline.

### What the workflow is wired to expect

`.github/workflows/build-deploy.yml` resolves the site code in this
order:

1. `vars.GOATCOUNTER_CODE` (a GitHub Actions repo-level **variable**,
   not a secret — the value ends up in public HTML anyway).
2. Falls back to the literal `learnche-pid`.

In other words: if you do nothing, the next deploy will tell every
reader's browser to hit `learnche-pid.goatcounter.com/count`. So
either register `learnche-pid` on goatcounter.com, or pick a different
code and override the GitHub variable.

### Steps

1. **Sign up** at <https://www.goatcounter.com/signup>.
   * Free tier: 100 000 pageviews/month, no credit card, no time
     limit.
   * The book qualifies as personal / non-commercial under the
     GoatCounter terms because of the CC BY-SA 4.0 license.
   * Pick a site code. Use `learnche-pid` to match the workflow
     default; if you choose anything else, see step 3.
2. **In the dashboard, configure the site:**
   * **Settings → Site code** — confirm it matches the value you
     intend `PID_BOOK_GC_CODE` to be.
   * **Settings → Domain** — set to `learnche.org/pid` (or just
     `learnche.org` — GoatCounter uses this for the dashboard
     header, not for filtering).
   * **Settings → Privacy** — confirm "Don't collect IP", "Don't
     store sessions", and any "Anonymise visitor IDs" toggles are
     **on**. The defaults are correct as of 2026; the
     [`privacy.rst`](../../privacy.rst) page promises these guarantees,
     so a drift here is a privacy-page bug.
   * **Settings → Advanced → Allow these origins** — add
     `https://learnche.org` so the `/count` endpoint accepts hits
     from the book.
3. **(Optional) override the site code in CI.** Only needed if you
   picked something other than `learnche-pid`:
   * GitHub repo → **Settings → Secrets and variables → Actions →
     Variables → New repository variable**.
   * Name: `GOATCOUNTER_CODE`. Value: your chosen code (e.g.
     `pid-book`).
   * Use a **variable**, not a secret. The site code is not
     credentials — it ends up in every page's HTML.
4. **Trigger a non-PR build.** Push a small commit to main, or use
   the **Actions → Build and deploy book → Run workflow** button on
   GitHub. PR builds intentionally ship with telemetry off, so you
   need a main push or a `workflow_dispatch` to verify.
5. **Verify** by opening any production page in a private window
   with extensions disabled, then watching the GoatCounter dashboard
   for 30 seconds. The hit should appear under "Pages". Type
   something into the sidebar Pagefind input and watch the "Events"
   tab — the search query should arrive as `path: /search?q=...`.

### Why the script also short-circuits

[`telemetry.js`](../../_static/js/telemetry.js) Section 0 has a guard:

```js
var cfg = window.__PID_TELEMETRY || {};
if (!cfg.gc) return;
```

If `PID_BOOK_GC_CODE` is empty, the script loads, runs the
short-circuit guards (DNT, `localhost`, `file://`), then exits
cleanly without injecting `count.js`. So shipping with
`vars.GOATCOUNTER_CODE` set to an empty string is a valid
"telemetry-disabled but Privacy page still present" mode. See
[Disabling telemetry, partially or fully](#disabling-telemetry-partially-or-fully)
below.

### Sanity check the wiring without leaving the office

```sh
# 1. What site code is the workflow currently set to?
gh -R kgdunn/pid-book variable list   # needs gh CLI; or check via the web UI

# 2. After deploy, what does the live HTML say?
curl -s https://learnche.org/pid/contents | grep -oE 'gc:"[^"]+"'
# → gc:"learnche-pid"  (or whatever you set it to)

# 3. Is the site code actually live on goatcounter.com?
curl -sf -o /dev/null -w '%{http_code}\n' https://learnche-pid.goatcounter.com/count
# → 200 or 405. 404 means the site isn't registered yet.
```

## Daily verification

### Is it working?

```sh
# 1. The pixel is in the production HTML.
curl -s https://learnche.org/pid/contents | grep -c 'goatcounter\|__PID_TELEMETRY'
# Expected: ≥ 2 (one inline globals, one count.js loader path)

# 2. The sparkline mount point is rendered on a normal page.
curl -s https://learnche.org/pid/data-visualization/box-plots | grep -c 'pid-sparkline'
# Expected: 1

# 3. The public stats endpoint is up.
curl -sf -o /dev/null -w '%{http_code}\n' https://learnche.org/_stats/
# Expected: 200

# 4. sparklines.json is fresh.
curl -sI https://learnche.org/_stats/sparklines.json | grep -i last-modified
# Expected: within the last 25 hours

# 5. The JSON parses and has data for a known page.
curl -s https://learnche.org/_stats/sparklines.json |
    python3 -c "import json,sys; d=json.load(sys.stdin);
print('pages:', len(d), '— sample:', d.get('contents', [])[-1:])"
```

### Are the dashboards meaningful?

* Open <https://learnche.org/_stats/> — GoAccess HTML report. Look at
  the "Requested Files" panel. Top entries should be book pages, not
  static assets or `/_static/...`. If static assets dominate, your
  `static-file` filters in `goaccessrc` are wrong — see
  [`server-runbook.md`](server-runbook.md).
* Open the GoatCounter dashboard (private). The "Pages" tab should
  show a similar top-N as GoAccess, but with substantially smaller
  absolute numbers (because of ad-blockers). The "Events" tab should
  show search queries with `path: /search?q=...`.
* Open any book page in a private window and confirm the sidebar
  sparkline renders. Hover for tooltip. If the page is brand-new (no
  history yet), the heading and mount should be **hidden** — not
  showing a flat zero line.

## Adding a new book page

The pipeline handles new pages automatically:

* The page builds and ships to `/var/www/learnche.org/pid/` via the
  normal rsync deploy.
* Day 1: zero entries in `sparklines.json`. The sidebar sparkline
  heading and mount are **hidden** by `telemetry.js` empty-state
  logic. No broken UI.
* Day 2 onwards: as soon as readers visit the page, the next nightly
  `build-sparklines.py` run aggregates the hits and the sparkline
  appears the next day.

There is **nothing** to update on the server when you add or rename
a book page. The pagename is derived from the request URL by the
producer, and matched by the consumer via the `data-page` attribute.

If you **rename or move** an existing page (e.g.
`data-visualization/box-plots` → `data-visualization/boxplots`):

* New pagename starts with empty history; sparkline mount is hidden.
* Old pagename keeps its history but no new hits accrue (because the
  URL no longer resolves). The orphan key stays in the JSON until it
  scrolls out of the 365-day window. This is fine — just expected.

## Disabling telemetry, partially or fully

### Disable globally for the next deploy

Edit [`.github/workflows/build-deploy.yml`](../../.github/workflows/build-deploy.yml)
and force the env var to `'0'`:

```yaml
- name: Build HTML
  env:
    PID_BOOK_TELEMETRY: '0'
    PID_BOOK_GC_CODE: ''
  run: uv run make html
```

Push to main. The next deploy ships HTML with no script tag and no
sparkline mount. The Privacy page remains (it's a published URL; we
don't 404 it on a whim).

To re-enable, revert the workflow edit.

### Disable just the pixel, keep the sparkline

The sparkline is fed by server logs and has no JS dependency on the
pixel. To disable just GoatCounter, set
`PID_BOOK_GC_CODE=''`. The script will load, then short-circuit at
`if (!cfg.gc) return;`, never injecting the GoatCounter loader.
Sparklines and search hooks **also stop working** because they live
in the same IIFE — see
[`client.md`](client.md). If you genuinely want sparklines without
any pixel/search, refactor `telemetry.js` so the early `return`
happens **after** the sparkline render call. (Not done by default
because in practice we want all three or none.)

### Disable just the sparkline, keep the pixel

Remove the `{% if pid_telemetry %}` block from
[`_templates/pid-sidebar-extra.html`](../../_templates/pid-sidebar-extra.html)
or change the template-side condition to `false`. The mount disappears
from every page. `telemetry.js` is unchanged; `renderSparkline()`
just finds no mount and returns.

### Permanently remove telemetry

If you ever want to fully delete the feature:

1. Revert all the files listed in [`README.md`](README.md) under
   "What ships in the repo".
2. Delete `/var/www/learnche.org/_stats/` on the server.
3. Remove the cron entry `/etc/cron.d/pid-book-stats`.
4. Update `privacy.rst` to say so, then deploy.

## Switching providers

### GoatCounter Cloud → self-hosted GoatCounter

Why: the Cloud free tier is generous (~100 k pageviews/month) but
capped. If we exceed it:

```sh
# On the server (assumes Docker is already installed):
docker run -d \
  --name goatcounter \
  --restart unless-stopped \
  -p 127.0.0.1:8081:8080 \
  -v goatcounter-data:/home/user \
  arp242/goatcounter:latest

# Front-end via Caddy, on a subdomain or path. Subdomain is simpler:
# add an A record for stats.learnche.org → 139.162.148.246, then add
# this site block to /etc/caddy/Caddyfile (Caddy auto-provisions the
# TLS cert via ACME; no certbot needed):
cat >>/etc/caddy/Caddyfile <<'EOF'

stats.learnche.org {
    reverse_proxy 127.0.0.1:8081
}
EOF
caddy validate --config /etc/caddy/Caddyfile && systemctl reload caddy
```

In GoatCounter, create a new site with code `learnche-pid` (any
code is fine, but matching the existing CI variable means the env
override is unchanged).

Then update [`telemetry.js`](../../_static/js/telemetry.js) where the
script loader URL is hard-coded:

```js
gcScript.src = "//gc.zgo.at/count.js";
```

Change to:

```js
gcScript.src = "//stats.learnche.org/count.js";
```

And the `data-goatcounter` attribute, which currently points at
`https://<gc>.goatcounter.com/count`, should become
`https://stats.learnche.org/count`. The `cfg.gc` env var is no longer
needed for routing but is still useful as a "feature is configured"
sentinel — keep it set to anything truthy.

Open a PR, merge, and the next deploy ships the swap. Old hits
remain in the SaaS dashboard until you manually export and import
them.

### GoatCounter → some other tracker (e.g. Plausible)

The wire format and event API differ; you'll rewrite Section 2 and
Section 3 of `telemetry.js`. Keep the same structure: short-circuits
first, lazy-load second, hooks third. Plausible's `plausible.js` has
a similar `<script defer data-domain="...">` form.

### Removing the pixel entirely, keeping logs only

If we want to operate fully without third-party dependencies:

1. Set `PID_BOOK_GC_CODE=''` in the workflow (pixel and search hooks
   short-circuit).
2. Optionally remove the inline `<script>` snippet from `conf.py` for
   cleanliness.
3. Sparklines and the GoAccess dashboard continue to work — they
   never depended on the pixel.

The cost is losing search-query data (logs don't capture in-book
search input) and country/device breakdowns (GoAccess can do these
from logs, but less precisely).

## Privacy complaints

If a reader contacts the maintainer via the GitHub issue tracker
saying they object to the data collection, the response process:

1. Verify what they actually saw. They may be confusing the cookie-
   less GoatCounter pixel with cookie-based analytics elsewhere on
   the web.
2. Confirm the [`/pid/privacy`](https://learnche.org/pid/privacy)
   page accurately describes current behaviour. If anything has
   drifted, fix the page in the same PR that fixes the drift.
3. If the complaint is "I don't want my browser to send the
   pageview" — point them at the DNT setting. We honour it.
4. If the complaint is "I don't want my IP to land in your logs at
   all" — there's nothing we can do short of running Tor exit-node
   filtering. This is the standard tradeoff of running a webserver.
   Be transparent.
5. If the complaint is structural ("I don't think you should collect
   anything") — engage in good faith. The book is open. They're
   welcome to fork it without the telemetry layer.

Reference the [`architecture.md`](architecture.md) "Privacy posture"
section for the canonical talking points.

## Troubleshooting cookbook

### "The sparkline shows nothing on a page that should have data."

Symptoms: sidebar shows the "Page views (365 days)" heading but no
chart underneath, or shows no heading at all when the page does have
hits.

Diagnose:

```sh
# 1. Is the JSON serving?
curl -sf -o /dev/null -w '%{http_code}\n' https://learnche.org/_stats/sparklines.json
# 200 expected. 404 → check the Caddyfile /_stats/* handle. 403 → check directory perms.

# 2. Does the JSON contain the page key?
curl -sf https://learnche.org/_stats/sparklines.json |
    python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data-visualization/box-plots'))"
# None → the page key is missing or misspelled. Compare with the
# data-page attribute in the rendered HTML.

# 3. What is the page actually asking for?
curl -s https://learnche.org/pid/data-visualization/box-plots |
    grep 'data-page' | head -1

# 4. Does ECharts load?
curl -sf -o /dev/null -w '%{http_code}\n' https://learnche.org/pid/_static/js/echarts-min.js
# 200 expected. 404 → the CI fetch step failed; check the workflow logs.
```

If `data-page` is wrong, the bug is in
`_templates/pid-sidebar-extra.html` (Jinja `{{ pagename }}` should
just work).

If the JSON is missing the key, the bug is in the producer's
`normalise_pagename` — likely a recently-renamed page whose URL
doesn't fold to the same key Sphinx is now using.

### "Pageviews are inflated this week."

A new bot is in the wild. Check GoAccess "Visitors" → top UAs. Anything
suspicious goes into `/etc/pid-book/bots.txt`; both pipelines pick
it up on the next nightly run. Mirror the entry into
[`scripts/server/bots.txt.example`](../../scripts/server/bots.txt.example)
in a follow-up PR so a fresh server install starts current.

### "GoatCounter shows zero hits since yesterday."

* Check <https://www.goatcounter.com/status> for outage.
* Open DevTools on a production page; in the Network tab confirm
  `gc.zgo.at/count.js` loads (200) and `<gc>.goatcounter.com/count`
  POSTs (204 expected).
* If both succeed but the dashboard still shows nothing, the site
  code in `PID_BOOK_GC_CODE` may have been changed in CI variables
  without updating GoatCounter, or vice versa.

### "Local `make html` build is shipping telemetry."

It shouldn't, unless you set `PID_BOOK_TELEMETRY=1` yourself. Check:

```sh
echo "${PID_BOOK_TELEMETRY-unset}"
grep -l 'goatcounter' _build/html/contents
```

If you intentionally enabled it for testing and want to disable:

```sh
unset PID_BOOK_TELEMETRY PID_BOOK_GC_CODE
make clean html
```

### "PR build is shipping telemetry."

Should be impossible — three independent gates protect against this.
But if `grep -l goatcounter _build/html/contents` returns a hit on
a PR build:

* Check `.github/workflows/build-deploy.yml`. Did someone change the
  ternary?
* Check the deploy gate (`if: github.event_name != 'pull_request'`).
  Even if the env var leaked, the rsync should have been skipped.
* Re-run the workflow and inspect logs for the `Build HTML` step.
  GitHub shows the resolved env values per step.

### "I changed the URL scheme to add `.html` and now sparklines are blank."

Update both:

1. `normPath` in [`telemetry.js`](../../_static/js/telemetry.js) — the
   normalisation must continue to fold `/pid/foo` and `/pid/foo.html`
   to the same key.
2. `normalise_pagename` in
   [`build-sparklines.py`](../../scripts/server/build-sparklines.py).

Then run `build-sparklines.py` once manually so the JSON keys match
the new scheme; subsequent nightly runs are correct.

### "ECharts download in CI fails."

Symptom: workflow fails on `Fetch ECharts` step with `curl: (22) ...`.

Causes:

* jsdelivr is intermittently down. `--retry 3` mitigates; if the
  failure persists, switch to a different CDN with the same path.
* The pinned version was unpublished. Bump the pin to the next
  release; verify the build still works locally.
* GitHub Actions runner has no outbound network (rare). Re-run the
  workflow.

The `test -s` after the curl asserts the file is non-empty, so a
silent zero-byte download is impossible.

### "GoAccess report has no entries despite the access log being non-empty."

Most often: the log format isn't what the pipeline expects. Caddy
should be writing JSON; the pipeline pipes it through
`caddy-json-to-combined.py` before handing it to GoAccess. Check a
sample line:

```sh
head -1 /var/log/caddy/learnche.org.access.log
```

It should be a single JSON object (starts with `{`). If it is plain
text, your Caddyfile has been switched away from the default `format
json` encoder — either restore it, or rewrite the JSON filter to match
your custom format.

To verify the filter end-to-end:

```sh
head -100 /var/log/caddy/learnche.org.access.log |
    /usr/local/bin/caddy-json-to-combined.py
```

You should see Apache combined-format lines on stdout. If you see the
same JSON echoed back, the filter is rejecting the input — inspect the
JSON shape against `parse_caddy_json` in
[`build-sparklines.py`](../../scripts/server/build-sparklines.py).

### "GoAccess writes 0 bytes despite parsing millions of log lines."

You'll see the progress counter complete (`Parsing... [N,NNN,NNN]`),
the wrapper print `wrote ... (0 bytes)`, and the report file is
empty. RC is 0 — silent failure.

Likely causes (in order of how often they bite):

1. **GoAccess 1.4 silently refuses any `--output` path whose final
   extension isn't `.html`, `.csv`, or `.json`.** `mktemp
   /tmp/run-goaccess.html.XXXXXX` produces filenames like
   `/tmp/run-goaccess.html.aBcDeF` — the last extension is `.aBcDeF`,
   not `.html`, and goaccess emits an error to stderr (often hidden by
   shell pipelines) and exits 0. The fix in `run-goaccess.sh` is to use
   `mktemp --suffix=.html /tmp/run-goaccess.XXXXXX` so the random part
   is in the middle.

2. **`--anonymize-ip` was added in GoAccess 1.6.** On 1.4 the flag is
   silently accepted but causes 0-byte output. Drop the flag (and the
   matching `anonymize-ip true` directive from `goaccessrc`) on 1.4;
   use `ignore-panel HOSTS` for equivalent privacy (raw IPs never reach
   the rendered HTML).

3. **`html-prefs` was added in GoAccess 1.6.** Same silent 0-byte
   failure on 1.4 if the directive is in the config file.

Confirm which by running goaccess against a single small log
**without** the wrapper:

```sh
sudo cat /var/www/logs/learnche.org/access.log \
  | /usr/local/bin/caddy-json-to-combined.py \
  | goaccess - --no-global-config --config-file=/dev/null \
      --log-format=COMBINED --output=/tmp/diag.html 2>&1
ls -la /tmp/diag.html
```

This bypasses the conf and uses an unambiguous `.html` filename. If
*this* produces a real file but the wrapper doesn't, the conf or the
mktemp template is the culprit — patch the relevant fix above.

### "Bottom-10 stats page shows weird URLs like `_downloads/...`"

`build-sparklines.py`'s `normalise_pagename()` filters out
`/_static/`, `/_sources/`, `/_images/`, `/_downloads/`, and
`/pagefind/` so Sphinx-generated download artifacts don't pollute the
page list. If a new Sphinx category appears (e.g. `/_modules/`), add
it to the filter list and re-run `build-sparklines.py` — the next
nightly rebuild will drop it.

### "Stats page shows data from a week ago, even though the cron is running."

Symptom: the on-disk `/var/www/learnche.org/_stats/sparklines.json`
has a fresh `mtime`, `curl -s 'https://learnche.org/_stats/sparklines.json'`
from any machine returns fresh data, but the chart in a reader's
browser keeps showing the old data day after day.

Cause we've actually hit: `_static/js/telemetry.js` used to call
`fetch("/_stats/sparklines.json", { cache: "force-cache" })`.
**`force-cache` is the Fetch API's most aggressive cache mode**: it
returns whatever is in the HTTP cache regardless of `max-age`, and
only refetches when the cache entry is evicted by the browser's own
quota. On iOS Safari that can mean weeks. We swapped to
`cache: "default"`, which honours the `Cache-Control: max-age=3600`
header and revalidates after an hour.

Diagnostic:

```sh
# Server side — should match curl-from-anywhere
sudo python3 -c "
import json
d = json.load(open('/var/www/learnche.org/_stats/sparklines.json'))
all_dates = sorted({p[0] for v in d.values() for p in v})
print(f'on-disk:   {all_dates[0]} -> {all_dates[-1]}')
"

# Cloudflare side — bypass any local cache with a unique query string
curl -s 'https://learnche.org/_stats/sparklines.json?v=test' | python3 -c "
import json, sys
d = json.load(sys.stdin)
all_dates = sorted({p[0] for v in d.values() for p in v})
print(f'CF:        {all_dates[0]} -> {all_dates[-1]}')
"

# Confirm CF isn't caching the JSON (it's marked DYNAMIC by default
# because .json is not on CF's auto-cache extension list).
curl -sI 'https://learnche.org/_stats/sparklines.json' | grep -iE 'cache|last-mod'
```

If on-disk and CF match (both fresh) but a reader's browser still
shows stale data, the bug is purely client-side: a reader whose JS
was loaded before the fix shipped is still using `force-cache`. They
can force-reload the page (Cmd+Shift+R, or in Safari iOS: pull-down
on the address bar → "Reload Without Content Blockers") to evict
their cache and pick up the new `telemetry.js`.

## Periodic maintenance

* **Quarterly**: review `/etc/pid-book/bots.txt` against current
  GoAccess top-UAs. Add new bots; never delete entries (they cost
  nothing).
* **Yearly**: bump the pinned ECharts version
  (`echarts@5.5.1` → next stable). Test in a PR (sparkline render
  visually unchanged) before merging.
* **As needed**: review [`/pid/privacy`](https://learnche.org/pid/privacy)
  for accuracy any time the pipeline changes. Discrepancies between
  what the page promises and what the code does are the worst-case
  failure mode here.
