# Operations: verify, switch, disable, troubleshoot

Day-to-day operations cookbook. The other docs explain the design and
the code; this one is the procedure manual.

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
  scrolls out of the 90-day window. This is fine — just expected.

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

Push to master. The next deploy ships HTML with no script tag and no
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

# Front-end via nginx, on a subdomain or path. Subdomain is simpler:
# add an A record for stats.learnche.org → 139.162.148.246, then:
cat >/etc/nginx/sites-available/stats.learnche.org <<'EOF'
server {
    listen 443 ssl http2;
    server_name stats.learnche.org;

    ssl_certificate     /etc/letsencrypt/live/stats.learnche.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/stats.learnche.org/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
ln -s /etc/nginx/sites-available/stats.learnche.org /etc/nginx/sites-enabled/
certbot --nginx -d stats.learnche.org
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

Symptoms: sidebar shows the "Page views (90 days)" heading but no
chart underneath, or shows no heading at all when the page does have
hits.

Diagnose:

```sh
# 1. Is the JSON serving?
curl -sf -o /dev/null -w '%{http_code}\n' https://learnche.org/_stats/sparklines.json
# 200 expected. 404 → check nginx /_stats/ block. 403 → check directory perms.

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

Most often: the log format doesn't match `--log-format=COMBINED`.
Check a sample line:

```sh
head -1 /var/log/nginx/learnche.org.access.log
```

If the format is different (e.g. you customised nginx's log_format),
either revert that customisation, or change `LOG_RE` and the
`--log-format` flag together. Both pipelines must agree.

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
