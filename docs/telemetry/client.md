# Client-side: `_static/js/telemetry.js`

A walkthrough of the runtime telemetry script. The file is ~220 lines
of vanilla ES5 (no transpiler, no framework, no dependencies); this
doc explains why each piece is the way it is.

The full source: [`_static/js/telemetry.js`](../../_static/js/telemetry.js).

## Lifecycle in one paragraph

The script is shipped as `<script src="_static/js/telemetry.js"
defer>` (see [`build-and-deploy.md`](build-and-deploy.md)). On HTML
parse the browser fetches it, defers execution until the document is
ready, then runs an IIFE that decides — through a series of
short-circuit checks — whether to do anything at all. If the answer
is yes, it (a) injects GoatCounter's `count.js`, (b) hooks the search
inputs, and (c) renders the sparkline by lazy-loading ECharts and
fetching the public sparkline JSON. Anything that fails along the
way is caught silently; the script never throws into the page.

## Section 0 — short-circuit guards

```js
if (
  navigator.doNotTrack === "1" ||
  window.doNotTrack === "1" ||
  navigator.msDoNotTrack === "1"
) return;
```

The first thing we do is honour Do-Not-Track, before reading the URL,
before parsing config, before any side effect. Three forms exist
because browser history left us three flavours of the API.

```js
var host = location.hostname;
if (
  location.protocol === "file:" ||
  host === "localhost" ||
  host === "127.0.0.1" ||
  host === "" ||
  /\.local$/.test(host)
) return;
```

Self-hosted-reuser guard. Anyone who clones the CC BY-SA source and
serves it from `localhost`, an `*.local` mDNS hostname, or a
`file://` URL will not phone home. The empty-string check covers
edge cases where `location.hostname` is missing entirely (some
embedded WebViews).

This guard is **important.** The build-time gate
(`PID_BOOK_TELEMETRY=1`) protects the canonical build, but if a
self-hoster set the env var to `1` themselves and rebuilt, only this
runtime check would protect their classroom from leaking pageviews
to our dashboard.

```js
var cfg = window.__PID_TELEMETRY || {};
if (!cfg.gc) return;
```

The `<script>window.__PID_TELEMETRY={gc:"..."};</script>` snippet is
written into `<head>` by the `html-page-context` handler in
`conf.py`. If the build did not provide a GoatCounter site code (e.g.
`PID_BOOK_GC_CODE` was empty), we silently exit. This is the
"telemetry shipped but unconfigured" path; the build still produced
valid HTML, the script still loaded, it just doesn't do anything.

## Section 1 — path normalisation

```js
function normPath() {
  var p = location.pathname.replace(/\/+$/, "") || "/";
  p = p.replace(/\.html?$/i, "").replace(/\/index$/, "");
  return p + location.search;
}
```

Required because the book uses **extensionless URLs** (`html_file_suffix
= ""` in `conf.py`). All three of these paths point to the same page:

* `/pid/contents` (canonical)
* `/pid/contents/` (user added a trailing slash)
* `/pid/contents.html` (some scraper guessed an extension)

Normalising means the GoatCounter dashboard records one canonical
path per page, not three. The `|| "/"` clause prevents the homepage
collapsing to an empty string.

`location.search` is preserved so query-string-parameterised pages
(if we ever add any) are distinguishable.

## Section 2 — GoatCounter pixel

```js
window.goatcounter = { no_onload: true, path: normPath };
```

`no_onload: true` tells GoatCounter's `count.js` not to fire its own
pageview-on-load logic. We want to call `goatcounter.count()`
manually after `count.js` has finished loading. `path: normPath`
overrides the default `location.pathname` getter so our
canonicalised version is what gets logged.

```js
var gcScript = document.createElement("script");
gcScript.async = true;
gcScript.setAttribute(
  "data-goatcounter",
  "https://" + cfg.gc + ".goatcounter.com/count"
);
gcScript.src = "//gc.zgo.at/count.js";
gcScript.onload = function () {
  try { window.goatcounter.count(); } catch (e) { /* ignore */ }
};
document.head.appendChild(gcScript);
```

* `gc.zgo.at` is GoatCounter's hosted-script CDN. The actual hit
  endpoint is `<gc>.goatcounter.com/count`, which `count.js` POSTs to.
* `async = true` means script fetch and execution don't block the
  parser. By the time it runs, the rest of telemetry.js has already
  finished its synchronous work.
* The `try/catch` defends against `count.js` changing its API or
  throwing because of, e.g., a network error. The page must never
  break because telemetry broke.

## Section 3 — search instrumentation

The book has **two** search inputs and we hook both.

### Sphinx built-in search (`<input name="q">`)

Lives on `/search`. Hooked via `document.querySelector('input[name="q"]')`.
This input is rendered server-side, so it exists at `DOMContentLoaded`.

### Pagefind search (`.pagefind-ui__search-input`)

Mounted in the sidebar by
[`_templates/pagefind-search.html`](../../_templates/pagefind-search.html).
The Pagefind UI is loaded asynchronously and the input element
*does not exist* at `DOMContentLoaded`. We watch for it with a
MutationObserver:

```js
function boot() {
  hookSphinxSearch();
  if (!hookPagefindSearch()) {
    var mo = new MutationObserver(function () {
      if (hookPagefindSearch()) mo.disconnect();
    });
    mo.observe(document.body, { childList: true, subtree: true });
    setTimeout(function () { mo.disconnect(); }, 15000);
  }
  renderSparkline();
}
```

* If `hookPagefindSearch()` succeeds on first try, no observer is
  started.
* Otherwise we observe the whole body subtree for child-list changes.
  As soon as the input appears, we hook it and disconnect.
* The 15 000 ms safety timeout disconnects the observer no matter
  what — Pagefind is loaded best-effort by `make html` (the `npx
  pagefind` line is prefixed with `-`), so it can legitimately be
  missing in production.

### Idempotent hooking

```js
if (el && !el.__pidHooked) {
  el.__pidHooked = true;
  el.addEventListener("input", debounce(sendQuery));
}
```

A `__pidHooked` flag on the DOM node prevents double-binding if the
boot sequence is somehow run twice (e.g. if a future Sphinx version
re-renders the sidebar without a full page load).

### Debouncing and PII guards

```js
var DEBOUNCE_MS = 800;
var lastSent = "";
function sendQuery(q) {
  q = (q || "").trim();
  if (!q || q === lastSent || q.length > 80) return;
  if (/[\w.+-]+@[\w-]+\.[\w.-]+/.test(q)) return;
  lastSent = q;
  try {
    window.goatcounter.count({
      path: "/search?q=" + encodeURIComponent(q),
      event: true,
    });
  } catch (e) { /* ignore */ }
}
```

* **800 ms debounce** so rapid typing produces one event, not one per
  keystroke.
* **Empty queries dropped** — typing then deleting must not log
  anything.
* **`q === lastSent` dedupe** — defends against `input` events that
  fire without a value change (some IMEs).
* **80-char cap** — Pagefind has a 30-ish char practical limit; 80
  gives some headroom while bounding payload size and reducing
  accidental-PII risk.
* **Email regex** — heuristic but catches the most common case
  (someone pasting their own email into the search box). The regex
  is intentionally lax (allows `+` and `.` in the local part) so
  false positives bias toward dropping potentially sensitive
  queries.
* **`event: true`** tells GoatCounter to record the path as a custom
  event rather than a pageview, so search queries show up in their
  Events tab not the Pages tab.
* The `try/catch` mirrors the count.js call.

### Why we hook the `<input>` and not Sphinx's search code

Sphinx's vendored `searchtools.js` is **regenerated on every
`make html`** by the Sphinx build. If we patched it, our patch would
disappear every build. By listening on the standard
`<input name="q">` element from outside, we are stable against any
internal Sphinx churn. The cost is that we capture *what was typed*,
not *which results were clicked* — which is the more useful signal
anyway.

## Section 4 — sparkline render

The sparkline is the only feature that can render after a network
round trip. It works in three phases.

### Phase 4a — find the mount point

```js
var mount = document.getElementById("pid-sparkline");
if (!mount) return;
var pageKey = mount.getAttribute("data-page") || "";
if (!pageKey) {
  pageKey = location.pathname
    .replace(/^\/pid\//, "")
    .replace(/\/+$/, "")
    .replace(/\.html?$/i, "");
  if (!pageKey) pageKey = "contents";
}
```

* If there's no `#pid-sparkline` div on the page (e.g. dev build, or
  a future page that opted out), we exit. No sparkline, no harm.
* `data-page` is supplied by the Jinja template as `{{ pagename }}`,
  which is the canonical Sphinx-relative slug. **This must match
  exactly the keys in `sparklines.json`** — see
  [`sparklines-schema.md`](sparklines-schema.md).
* The fallback URL-derivation is defensive: if a future template
  forgets to set `data-page`, we still try to recover by stripping
  the `/pid/` prefix and any trailing slash or `.html`. Treating an
  empty key as `"contents"` matches the homepage's pagename.

### Phase 4b — fetch sparklines.json

```js
fetch("/_stats/sparklines.json", { cache: "force-cache" })
  .then(...)
  .catch(function () { /* leave the empty mount; do not break */ });
```

* **Same-origin fetch** — `learnche.org/_stats/sparklines.json`.
  Same hostname as the book, so no CORS dance.
* **`cache: "force-cache"`** — the JSON is regenerated nightly, so
  we let the browser reuse the response across the whole site visit.
  The HTTP cache headers on the JSON (1 hour `max-age` per the
  Caddyfile `/_stats/*` handle) bound staleness.
* **Catch-all on errors** — network failure, malformed JSON, server
  500 — all silently leave the empty mount. The page must not break
  because sparkline data was unavailable.

### Phase 4c — empty-state handling

```js
var series = data && data[pageKey];
if (!series || !series.length) {
  var heading = mount.previousElementSibling;
  if (heading && heading.tagName === "P") heading.style.display = "none";
  mount.style.display = "none";
  return;
}
```

A page with no historical data (e.g. a freshly added page like
`privacy` itself) gets **no UI at all** — we hide both the mount
and the "Page views (90 days)" heading. The alternative (showing a
"0 hits" placeholder) would be misleading and visually noisy.

### Phase 4c.5 — 90-day reader count in the heading

After confirming the series is non-empty, but before any ECharts
work, we compute the sum and write it into the sidebar heading:

```js
var totalEl = document.getElementById("pid-sparkline-total");
if (totalEl) {
  var total = series.reduce(function (a, p) { return a + p[1]; }, 0);
  totalEl.textContent = total.toLocaleString() + " reads";
}
```

The `<span id="pid-sparkline-total">` ships from
`_templates/pid-sidebar-extra.html`, floated to the right of the
"Page views (90 days)" heading. Tabular-numeric CSS keeps the digits
aligned across pages. The `if (totalEl)` guard makes this a no-op
when an older cached template doesn't have the span — pageview
tracking and the sparkline still work.

### Phase 4d — render

```js
loadECharts(function (echarts) {
  if (!echarts) return;
  // ...
  chart = echarts.init(mount, null, { renderer: "svg" });
  chart.setOption({
    grid: { left: 0, right: 0, top: 2, bottom: 0 },
    xAxis: { type: "category", show: false, data: dates },
    yAxis: { type: "value", show: false },
    tooltip: { trigger: "axis", formatter: ... },
    series: [{
      type: "line", data: values, showSymbol: false,
      smooth: true, lineStyle: { width: 1.5 },
      areaStyle: { opacity: 0.15 },
    }],
  });
  window.addEventListener("resize", function () { chart.resize(); });
});
```

* **SVG renderer** — sharper at small sizes than the canvas renderer
  and prints better.
* **No axes shown** — it's a sparkline, not a chart. The numbers come
  from the tooltip on hover.
* **`showSymbol: false`** — no per-point dots; the line itself is the
  signal.
* **Smooth + 15% area fill** — at this size the smoothing reads as
  "trend" not "data points"; the area fill makes the trend visible
  even when the line is one or two pixels tall.
* **Resize handler** — needed because `sphinx_book_theme`
  collapses/expands the sidebar on viewport changes.

The `chart.init(...)` call is wrapped in `try/catch` because some
older browsers (or unusual CSP settings) reject SVG rendering; in
that case we silently leave the mount blank.

### Phase 4e — lazy-load ECharts

```js
function loadECharts(cb) {
  if (window.echarts) return cb(window.echarts);
  var s = document.createElement("script");
  s.src = "/pid/_static/js/echarts-min.js";
  s.async = true;
  s.onload  = function () { cb(window.echarts); };
  s.onerror = function () { cb(null); };
  document.head.appendChild(s);
}
```

* ECharts is fetched **on demand**, only when a sparkline mount
  actually exists. Pages without the mount (which is
  every page in non-production builds, by design) never pay the
  ~80 KB gzip download.
* `/pid/_static/js/echarts-min.js` is a same-origin path — no
  third-party hit at runtime. The CI workflow drops the file there
  via the curl step (see [`build-and-deploy.md`](build-and-deploy.md)).
* `onerror` is non-fatal: if ECharts is somehow missing we just don't
  render the sparkline. Pageview tracking is unaffected.

## Section 4b — stats page (`/pid/stats`)

`renderStatsPage()` runs on every page but exits immediately unless
`#pid-stats-summary` is in the DOM. Only [`stats.rst`](../../stats.rst)
ships that mount point, so the whole function is a no-op on every
other page.

When the mount is present, the function fetches the same
`sparklines.json` the sidebar uses and fills three widgets:

| Mount point | What's rendered |
|---|---|
| `#pid-stats-summary` | Three "big number" cards: total reads in the window, number of pages with at least one read, number of distinct days in the data. |
| `#pid-stats-daily` | A daily-totals line chart — sum of reads across all pages per day, smoothed, with an area fill and axis-trigger tooltip. ECharts SVG renderer; lazy-loaded via the same `loadECharts()` the sparkline uses. |
| `#pid-stats-top` | A table of the top-20 pages by 90-day total. Each row links to `/pid/<pagename>` (with `/index` stripped, so `data-visualization/index` → `/pid/data-visualization/`). |

Aggregation is a single pass over `Object.keys(data)`:

```js
pages.forEach(function (page) {
  var series = data[page] || [];
  var pageTotal = 0;
  series.forEach(function (p) {
    var date = p[0], count = p[1] | 0;
    totalReads += count;
    pageTotal += count;
    dailyMap[date] = (dailyMap[date] || 0) + count;
  });
  if (pageTotal > 0) pageTotals.push([page, pageTotal]);
});
pageTotals.sort(function (a, b) { return b[1] - a[1]; });
```

The `| 0` coerces to int (defends against a future schema change
that emits floats). Pages whose 90-day total is zero are dropped
from the top-N consideration but still count in `totalReads`.

Empty-state behaviour is uniform across all three widgets: if
`sparklines.json` is missing, malformed, or empty, the summary is
replaced with an italic "Statistics aren't available yet…" message
and the chart + table mounts are hidden via `style.display = "none"`.
The page never appears broken — just empty.

CSS for the cards and table lives in
`_static/css/theme-extended-kgd.css` under the "stats page widgets"
section; every selector is namespaced to `.pid-stats-*` so it cannot
leak into the rest of the book.

## Section 5 — boot

```js
function boot() {
  hookSphinxSearch();
  if (!hookPagefindSearch()) { /* MutationObserver */ }
  renderSparkline();
  renderStatsPage();
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", boot);
} else {
  boot();
}
```

The `defer` attribute on the script tag means the browser waits to
execute until parsing is done, but `defer` doesn't fire its callback
**after** `DOMContentLoaded` in every browser; we use the
`readyState` check as belt-and-braces.

`renderStatsPage()` runs on every page but cheaply early-returns when
`#pid-stats-summary` is absent (which is all but the
[`/pid/stats`](https://learnche.org/pid/stats) page).

## Footprint

* **Wire bytes (gzip):** ~1.3 KB for `telemetry.js` itself, plus
  GoatCounter's `count.js` (~3 KB), plus ECharts (~80 KB) **only on
  pages with a sparkline mount**.
* **Cookies:** zero.
* **localStorage / sessionStorage:** zero.
* **Network requests in baseline (no sparkline mount):** one to
  `gc.zgo.at/count.js`, one to `<gc>.goatcounter.com/count`. No
  third-party.
* **Network requests with sparkline:** add one to
  `learnche.org/_stats/sparklines.json` (same-origin, cached) and one
  to `learnche.org/pid/_static/js/echarts-min.js` (same-origin,
  cached).

## Failure modes (what happens when things break)

| Failure | What happens |
|---|---|
| GoatCounter is down | `gcScript.onload` never fires; no pageview recorded; no error in console; no UI impact. |
| `sparklines.json` 404 | `.catch` runs; mount stays empty; no UI impact. |
| `sparklines.json` malformed | Same as 404. |
| ECharts file missing | `loadECharts` calls `cb(null)`; sparkline silently skipped. |
| `pageKey` not in JSON | Empty-state path; heading and mount hidden. |
| Browser blocks all third-party JS | `count.js` blocked → no pageview. Sparkline still renders (same-origin). |
| Browser has DNT enabled | Whole script returns at line 1; no pixel, no sparkline, no search hooks. |
| User typing rapidly | Debounce coalesces into one event after 800 ms idle. |
| User pastes an email into the search box | Regex catches it; nothing sent. |

## Testing the client manually

```js
// In DevTools console on a production page:

// 1. Verify the inline globals were injected
console.log(window.__PID_TELEMETRY);
// → { gc: "learnche-pid" }

// 2. Verify the GoatCounter wrapper was set up
console.log(window.goatcounter);
// → { no_onload: true, path: ƒ normPath() }

// 3. Verify path normalisation
console.log(window.goatcounter.path());
// → "/pid/contents" (no trailing slash, no .html)

// 4. Manually fire a search event (won't appear if DNT is on)
window.goatcounter.count({ path: "/search?q=test", event: true });

// 5. Inspect the sparkline mount
document.getElementById("pid-sparkline");
```

For automated coverage we rely on the CI build assertions
(`grep -l 'goatcounter' _build/html/contents`) plus a daily smoke check
of the dashboards.
