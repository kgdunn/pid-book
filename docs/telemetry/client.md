# Client-side: `_static/js/telemetry.js`

A walkthrough of the runtime telemetry script. The file is ~600 lines
of vanilla ES5 (no transpiler, no framework, no dependencies: the
charts are inline SVG that it draws itself); this doc explains why
each piece is the way it is.

The full source: [`_static/js/telemetry.js`](../../_static/js/telemetry.js).

## Lifecycle in one paragraph

The script is shipped as `<script src="_static/js/telemetry.js"
defer>` (see [`build-and-deploy.md`](build-and-deploy.md)). On HTML
parse the browser fetches it, defers execution until the document is
ready, then runs an IIFE that decides — through a series of
short-circuit checks — whether to do anything at all. If the answer
is yes, it (a) injects GoatCounter's `count.js`, (b) hooks the search
inputs, and (c) fetches the public sparkline JSON and draws the
sidebar sparkline from it. Anything that fails along the
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

On the stats page the snippet also carries `pages`, the names of every
page of the build. Phase 4b uses it.

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

The sparkline is the only feature that renders after a network round
trip. It works in four phases.

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
var statsPromise;
function fetchStats() {
  statsPromise = statsPromise ||
    fetch("/_stats/sparklines.json", { cache: "default" })
      .then(function (r) {
        if (!r.ok) throw new Error("sparklines.json " + r.status);
        return r.json();
      })
      .then(function (data) {
        data = data || {};
        if (!cfg.pages) return data;
        var book = {};
        cfg.pages.forEach(function (name) {
          if (Object.prototype.hasOwnProperty.call(data, name)) book[name] = data[name];
        });
        return book;
      });
  return statsPromise;
}
```

* **Only the book's pages, on the stats page.** The file has a key for
  every address the server answered with a 2xx. Some are not pages (a
  redirect stub such as `/pid/index`, a mistyped link such as
  `.../index'A=0`), and some are pages that were later removed. Where
  `cfg.pages` is present, only the keys in it are kept, so those rows
  do not fill the least-read table and do not count in the totals.
  Other pages have no list and read only their own key.

* **One fetch per page.** The sidebar sparkline and the stats page
  both call `fetchStats()` and share the promise.
* **Same-origin fetch** — `learnche.org/_stats/sparklines.json`.
  Same hostname as the book, so no CORS dance.
* **`cache: "default"`** — the JSON is regenerated nightly. Default
  HTTP caching honours the `Cache-Control: max-age=3600` we send,
  so the browser reuses the response for an hour and then
  revalidates. (Earlier versions used `force-cache`, which silently
  ignores `max-age` and pins the very first response forever — that
  one bit us: see the "Stats page shows data from a week ago" entry
  in [`operations.md`](operations.md).)
* **Catch-all on errors.** A network failure, malformed JSON or a
  server 500 all silently leave the block hidden. The page must not break
  because sparkline data was unavailable.

### Phase 4c: the days to show, and the empty state

```js
var days = displayDays(data);
var values = dense(data[pageKey], days);
var total = values.reduce(function (a, v) { return a + v; }, 0);
if (!total) return;
```

* `displayDays(data)` lists the calendar days the UI shows, oldest
  first: the `DISPLAY_DAYS` (180) complete days that end at the newest
  complete day in the file, or fewer while the logs hold less history.
  Every page is drawn over the same days, so two pages compare against
  the same date range.
* `dense(series, days)` gives the page's reads on each of those days.
  The JSON omits a day without a read; `dense` fills it with 0, so the
  x-axis is time. (Plotting only the days present would draw a page
  that was read on 10 of 180 days as 10 evenly spaced points.)
* A page with no reads on those days (e.g. a freshly added page) gets
  **no UI at all**: the block stays hidden. The alternative (showing a
  "0 hits" placeholder) would be misleading and visually noisy.

### Phase 4d: draw

```js
mount.innerHTML = sparkSvg(days.length, sparkPaths(values, Math.max.apply(null, values)));
if (totalEl) {
  var totalText = total.toLocaleString() + " reads";
  totalEl.textContent = totalText;
  onHover(mount, days.length, function (i) {
    totalEl.textContent = i < 0 ? totalText : formatDay(days[i]) + ": " + values[i].toLocaleString();
  });
}
if (block) block.style.display = "";
```

The chart is inline SVG, built as a string by two helpers that the
stats page shares:

* `sparkPaths(values, top)` returns two `<path>` elements, the line
  and the filled area under it. x is the day index and y is the reads
  as a fraction of `top`, so the drawing lives in a box that is
  `days - 1` wide and 1 high.
* `sparkSvg(nDays, inner)` wraps them in an `<svg>` whose `viewBox` is
  that box, with `preserveAspectRatio="none"`. CSS (`.pid-spark` in
  `theme-extended-kgd.css`) sets `width: 100%; height: 100%`, and
  `vector-effect: non-scaling-stroke` keeps the line 1.5 px thick
  under the stretch.

**The chart is sized by CSS, not by script.** It fills the sidebar at
every width, including when the sidebar is a drawer that opens after
the page has loaded, and there is no resize handler. This is the
reason the charts are hand-drawn: a charting library measures its
container when the chart is created, and both mounts are hidden at
that moment (see "What was rejected and why" in
[`architecture.md`](architecture.md)).

The `<span id="pid-sparkline-total">` ships from
`_templates/pid-sidebar-extra.html`, floated to the right of the
"Page views (180 days)" heading, and holds the page's total. While
the pointer is on the chart, `onHover` puts that day's date and views
there instead. The `if (totalEl)` guard makes this a no-op when an
older cached template doesn't have the span.

## Section 4b — stats page (`/pid/stats`)

`renderStatsPage()` runs on every page but exits immediately unless
`#pid-stats-daily` is in the DOM. Only [`stats.rst`](../../stats.rst)
ships that mount point, so the whole function is a no-op on every
other page.

When the mount is present, the function reads the same
`sparklines.json` the sidebar uses and fills five mounts:

| Mount point | What's rendered |
|---|---|
| `#pid-stats-daily` | The daily totals across all pages as a line chart, with a two-handle slider on its x-axis and buttons for the last 7, 30 and 90 days. The handles select a **window** of days, shaded in the chart. |
| `#pid-stats-summary` | Four "big number" cards for the window: reads, pages read, days, and the reads per day against the other days. |
| `#pid-stats-movers` | The 10 pages whose reads in the window differ most from what their other days predict. |
| `#pid-stats-top` | The 20 pages with the most reads in the window. |
| `#pid-stats-bottom` | The 10 pages with the fewest reads in the window. |

Each table row links to `/pid/<pagename>` (with `/index` stripped, so
`data-visualization/index` → `/pid/data-visualization/`) and carries a
sparkline of that page's daily reads over all the days, with the
window shaded. Page names are HTML-escaped: the keys come from request
paths, and a scraper can put anything in a path.

### The chart

The plot is the same stretched `sparkSvg` as the sidebar. Everything
with text in it is HTML laid over the SVG, positioned in percent, so
that the text keeps its shape while the drawing stretches:

* gridlines and their labels (`.pid-stats-tick`), at a round step
  from `axisStep()`;
* month labels (`.pid-stats-months`), one at the first day of each
  month;
* a cursor line and a readout that follow the pointer (`onHover`).

### The slider

The slider is two `<input type="range">` elements laid over the
x-axis. Each is one thumb wider than the plot, so the centre of a
thumb sits exactly on its day. Only the thumbs take the pointer
(`pointer-events`), because the body of one input would otherwise
cover the thumb of the other.

```js
function selectBetweenEdges() {
  var x = +edges[0].value;
  var y = +edges[1].value;
  select(Math.min(x, y), Math.max(x, y));
}
```

The window is whatever lies between the two thumbs, so they may cross
and neither can block the other. Native inputs bring keyboard support
(arrow keys) and touch support for free; `aria-valuetext` gives each
thumb its date.

### What the window is compared with

`select(a, b)` recomputes everything for the days `a..b`. For each
page:

```js
r.expected = outside ? ((p.total - r.reads) * inside) / outside : 0;
r.change = r.reads - r.expected;
```

* `inside` is the number of days in the window, `outside` the number
  of displayed days that are not in it.
* `expected` is the reads the page would have had in the window at
  the daily rate it had on the other days.
* `change` is how far the window is from that. The changes of all the
  pages add up to the change of the whole book, which is why ranking
  the pages by the size of their change answers "which pages account
  for this rise or fall".

When the window is all the days there is nothing to compare with: the
Change column and the fourth card are blank, and `#pid-stats-movers`
asks the reader to narrow the window.

The chart and the slider are built once. A move of the slider only
shifts the shaded band and rebuilds the cards and the three tables
(about 4 ms for 140 pages).

### Empty state

`stats.rst` ships `#pid-stats-daily` holding a "Statistics could not
load" note, and the other four mounts hidden. If the script never runs
(DNT, content blocker) the note stays. If `sparklines.json` is
missing, malformed, or empty, the note is replaced with "Statistics
aren't available yet…". Either way the four mounts stay hidden: the
page never appears broken, just empty.

CSS for the charts, cards and tables lives in
`_static/css/theme-extended-kgd.css` under the "Readership charts"
section; every selector is namespaced to `.pid-spark*` or
`.pid-stats-*` so it cannot leak into the rest of the book.

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
`#pid-stats-daily` is absent (which is all but the
[`/pid/stats`](https://learnche.org/pid/stats) page).

## Footprint

* **Wire bytes (gzip):** ~8 KB for `telemetry.js` itself, plus
  GoatCounter's `count.js` (~3 KB). There is no charting library.
* **Cookies:** zero.
* **localStorage / sessionStorage:** zero from the telemetry client. One
  unrelated key exists on the site, `pid:code-blocks:v1`, written by
  `_static/js/code-collapse.js` to remember whether the reader asked for code
  blocks to be shown; it is never read by telemetry and never transmitted.
  See `privacy.rst`.
* **Network requests in baseline (no sparkline mount):** one to
  `gc.zgo.at/count.js`, one to `<gc>.goatcounter.com/count`. No
  third-party.
* **Network requests with sparkline:** add one to
  `learnche.org/_stats/sparklines.json` (same-origin, cached).

## Failure modes (what happens when things break)

| Failure | What happens |
|---|---|
| GoatCounter is down | `gcScript.onload` never fires; no pageview recorded; no error in console; no UI impact. |
| `sparklines.json` 404 | `.catch` runs; the sidebar block stays hidden; the stats page shows its note. |
| `sparklines.json` malformed | Same as 404. |
| `pageKey` not in JSON | Empty-state path; the sidebar block stays hidden. |
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
