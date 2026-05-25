# Architecture: privacy-first telemetry for the HTML book

This document explains **why** the book is instrumented the way it is.
For *what* runs and *how* to operate it, see the sibling docs.

## The problem

The HTML book at <https://learnche.org/pid> historically shipped with
zero analytics. The maintainer wanted to know:

* Which sections are actually used? (Where should attention go?)
* What do readers search for?
* How does each page trend over time?

Without that signal, the book could only be improved on guesswork.

## Constraints that shape the design

Three constraints rule out the obvious answer (drop in Google Analytics):

1. **Audience runs ad-blockers.** Chemical-engineering students and
   professionals run uBlock Origin, Privacy Badger, AdGuard, and
   browser-level tracker blockers at high rates. JS analytics alone
   would systematically undercount the most engaged readers.
2. **CC BY-SA, educational content.** Adding cookies or a GDPR consent
   banner would degrade the reader experience and is unnecessary for
   the signal we need. The book has been published since 2010 with no
   tracking; adding intrusive instrumentation now would betray that
   posture.
3. **Free-only budget; full server ownership.** The owner runs
   `139.162.148.246` (Hetzner), has shell access, holds the
   pre-Hetzner Apache logs from earlier hosting. There is no business
   case for a paid SaaS like Plausible Cloud or Fathom.

## Layered design

Any single mechanism is wrong:

* **JS-only** undercounts ad-blocked readers and is fragile.
* **Logs-only** misses engagement (referrers, devices, time on page,
  in-book search).
* **Paid SaaS** violates the budget constraint and adds an external
  dependency for an open-access book.

So we layer four mechanisms, each correcting for the others' blind
spots.

### Layer A — GoAccess on access logs

* **Source:** Caddy access logs on the production server (JSON, the
  default Caddy encoder), plus the archived Apache logs from before
  the Hetzner migration. Both are fed through the same pipeline; a
  small filter ([`scripts/server/caddy-json-to-combined.py`](../../scripts/server/caddy-json-to-combined.py))
  converts the live JSON stream to Apache combined format so GoAccess
  sees one uniform input.
* **Strength:** captures **100 %** of HTTP hits, including ad-blocked
  readers, machine-to-machine fetches, and old-browser readers.
* **Output:** static HTML report at
  <https://learnche.org/_stats/>, regenerated nightly.
* **Privacy posture:** invoked with `--anonymize-ip`; raw logs rotate
  within 30 days; only aggregated daily roll-ups survive.
* **Limitations:** doesn't measure engagement (no time-on-page, no
  scroll depth), inflated by bots without filtering.

### Layer B — GoatCounter cookieless pixel

* **Source:** small (`<1 KB`) script tag injected into every HTML page
  in production builds.
* **Strength:** captures referrer, device class, country, time-on-site
  for the ~50–70 % of readers who don't ad-block. Server-side bot
  filtering by GoatCounter is decent.
* **Output:** GoatCounter dashboard (private to the maintainer).
* **Privacy posture:** **no cookies**, **no IP storage** (GoatCounter
  discards IPs server-side after deriving anonymous-day-bucket
  visitor IDs). Honours DNT — when `navigator.doNotTrack === "1"`
  the pixel never fires.
* **Limitations:** undercounts ad-block users; depends on a
  third-party SaaS (mitigated by the swap path documented in
  [`operations.md`](operations.md)).

### Layer C — Search-query events

* **Source:** the same telemetry script, which hooks **both** search
  inputs the book renders:
  1. Sphinx's built-in search (`<input name="q">` on `/search`).
  2. The Pagefind search box mounted by
     `_templates/pagefind-search.html`
     (`.pagefind-ui__search-input`).
* **Strength:** the highest-signal data we get — **what readers can't
  find** is more actionable than which page is most-viewed.
* **Output:** GoatCounter custom events with `path: /search?q=...`.
* **Privacy posture:** debounced 800 ms, never sends queries longer
  than 80 chars, drops anything matching an email-address regex
  client-side. Goes through GoatCounter so it inherits the same
  no-cookie / no-IP guarantees.
* **Limitations:** same ad-block undercounting as Layer B; the
  email-regex guard is heuristic, not bulletproof.

### Layer D — Per-page year-long sparkline

* **Source:** same access logs as Layer A, processed by
  [`scripts/server/build-sparklines.py`](../../scripts/server/build-sparklines.py)
  into a public JSON file
  `https://learnche.org/_stats/sparklines.json`.
* **Strength:** because it derives from server logs, it counts
  **ad-blocked readers** too — making it the *honest* signal in the
  sidebar. Each page shows its own trend.
* **Output:** ECharts SVG line chart in the sidebar, lazy-loaded only
  when a `#pid-sparkline` mount point exists.
* **Privacy posture:** the JSON is aggregate-only — daily unique-IP
  counts per page, no IPs, no UAs. The same nightly cron that runs
  GoAccess generates it.
* **Limitations:** schema is forward-compat (see
  [`sparklines-schema.md`](sparklines-schema.md)) but a misconfigured
  bot list inflates counts.

## What was rejected and why

| Option | Why not |
|---|---|
| Google Analytics 4 | Heavy script, requires cookie banner in EU, blocked by readers, blocked by some school IT, sends data to Google. Against the spirit of CC BY-SA educational content. |
| Plausible Cloud | Costs money (constraint 3 forbids it). Otherwise a fine choice. |
| Fathom Analytics | Costs money. |
| Self-hosted Plausible CE | Adds ops surface (Postgres, BEAM runtime) for marginal benefit over GoatCounter. Reconsider if the GoatCounter free tier is exceeded. |
| Self-hosted Umami | Same ops cost as Plausible CE. |
| Cloudflare Web Analytics | Requires fronting the site with Cloudflare. We don't, and shouldn't have to. |
| Server logs only | Misses referrers, devices, in-book search — Layer B and C exist for a reason. |
| JS-only (no logs) | Ad-blockers; Layer A is the floor that catches everyone else. |
| Inline ECharts in `html_js_files` (always loaded) | Pays the bytes on every page even when no sparkline is shown. We lazy-load it from the sparkline render path instead. |
| Commit ECharts as a binary blob | We did consider this. Curl'ing it at CI time from a pinned jsdelivr URL is cleaner, keeps the git history small, and lets dependabot-style scans flag updates. The drawback is build-time network dependency — acceptable for a hobby-scale book and mitigated by `--retry 3`. |
| Patch Sphinx's vendored `searchtools.js` | Sphinx regenerates it on every build; we'd be fighting upstream forever. We listen on the `<input>` element from outside. |
| Track scroll depth or click events | Too much instrumentation for the value. Pageviews + searches are enough to identify pages that need attention. |
| Add a consent banner | Not legally required for cookieless analytics with no IP storage; banners hurt the reader experience. The Privacy page (`/pid/privacy`) is the disclosure baseline. |

## Privacy posture

In one sentence: **we collect the minimum needed to know which
sections are read and which searches are useful, and nothing else.**

Concrete commitments, each enforced in code:

1. **No cookies are set, ever.** GoatCounter is configured cookieless;
   the sparkline render path uses `cache: "force-cache"` only against
   our own origin.
2. **No IP addresses are stored.** GoatCounter discards IPs after
   deriving daily visitor buckets; GoAccess runs with
   `--anonymize-ip`; `build-sparklines.py` keeps only daily counts
   per page and discards the source IPs.
3. **DNT is respected.** The very first thing
   [`telemetry.js`](../../_static/js/telemetry.js) does is check
   `navigator.doNotTrack`, `window.doNotTrack`, and
   `navigator.msDoNotTrack`. If any is `"1"` the function returns
   before any network call.
4. **Self-hosted reusers do not leak data.** The script also
   short-circuits on `localhost`, `127.0.0.1`, `*.local`, and
   `file://`. A user who clones the CC BY-SA source and serves it
   from their classroom server cannot accidentally send pageviews to
   the maintainer's dashboard unless they explicitly remove that
   guard.
5. **Search queries are sanitised client-side.** Empty strings,
   queries longer than 80 characters, and anything matching an
   email-address regex are dropped before the network call. The
   regex is not a privacy panacea — it's a heuristic that prevents
   the most common case of a reader pasting an email address into
   the search box.
6. **Public dashboards are aggregate-only.** The `/_stats/`
   directory exposes top-page counts and sparklines; it never
   exposes raw IPs, user-agents, or per-session detail.

## Threat model

We *do* defend against:

* **Cookie- or fingerprint-based tracking across sessions.** No
  cookies; no fingerprinting; same-origin assets only.
* **Ad-block undercounting biasing the popularity ranking.** Layer A
  and D (log-derived) are the source of truth; Layer B and C are
  supplementary.
* **PII leakage via search queries.** Client-side regex + length cap.
* **Self-hosted reusers polluting the maintainer's dashboard.** Host
  short-circuit in `telemetry.js`.
* **Misconfigured CI shipping telemetry to PR previews.** Three
  independent gates (env var, deploy step `if`, host short-circuit).

We do **not** defend against:

* **Network adversaries correlating GoatCounter requests with same-IP
  ECharts fetches.** Theoretically de-anonymising; practically
  irrelevant for an open educational site.
* **Sophisticated bot impersonation.** UA-based filters miss
  headless-Chrome-with-real-UA. Expect the first week of data to be
  noisier than reality.
* **Compromise of the GoatCounter SaaS.** If their data is leaked it
  contains anonymous pageview hits and search queries, no cookies, no
  IPs. Damage is bounded.
* **Compromise of the production webserver.** Raw logs exist for up
  to 30 days; an attacker with shell access could see IPs. Mitigated
  by standard server hardening (out of scope for this doc).

## Why not just one provider for everything

Using e.g. only GoatCounter would tie us to:

* Their bot filters (we want our own list shared with GoAccess and
  `build-sparklines.py`).
* Their UI (we want a public sidebar sparkline; their dashboard isn't
  public).
* Their pricing (their free tier is generous but capped).

Using e.g. only server logs would mean we can't see search queries,
referrers, or device classes, all of which are legitimately useful.

The layered design lets each layer do what it's best at and lets us
swap any one of them without touching the others (search-event
endpoint is one global; sparkline JSON is one fetch URL; GoatCounter
site code is one env var).

## Forward-compat notes

* If the GoatCounter free tier is exceeded, switch to a self-hosted
  GoatCounter on the same VPS — the JS code and env-var contract are
  unchanged. See [`operations.md`](operations.md).
* If we ever add a CSP, it must allow `https://gc.zgo.at` and
  `https://*.goatcounter.com` for `script-src` and `img-src`.
* If we ever change the URL scheme (e.g. add a real `.html` suffix),
  update the path-normalisation in `telemetry.js` so the sparkline
  key stays stable. See [`sparklines-schema.md`](sparklines-schema.md)
  for the contract.
* If we ever drop Pagefind, remove the `hookPagefindSearch` block in
  `telemetry.js` and the MutationObserver. The Sphinx hook still
  works.
