# Telemetry — engineering documentation

This directory documents how the HTML book at <https://learnche.org/pid>
collects readership signal so the maintainers can tell which pages get
used, what readers search for, and how each page trends over time.

For the **reader-facing** privacy disclosure see
[`/pid/privacy`](https://learnche.org/pid/privacy)
(source: [`privacy.rst`](../../privacy.rst)). The page below is the
**engineering and operations** view: it explains the design, every file
that ships telemetry-related code, the build-time wiring, the runtime
behaviour, and the server-side pipeline that produces the public
dashboards.

## Quick map

| Concern | Read |
|---|---|
| Why this design (and what was rejected) | [`architecture.md`](architecture.md) |
| Build-time wiring: env vars, CI, conf.py | [`build-and-deploy.md`](build-and-deploy.md) |
| Runtime behaviour of `_static/js/telemetry.js` | [`client.md`](client.md) |
| Server-side pipeline (GoAccess, cron, Caddy) | [`server-runbook.md`](server-runbook.md) |
| `sparklines.json` schema and key normalisation | [`sparklines-schema.md`](sparklines-schema.md) |
| First-time GoatCounter Cloud account setup | [`operations.md`](operations.md#first-time-setup-goatcounter-cloud-account) |
| Day-to-day operations (verify, disable, switch providers, troubleshoot) | [`operations.md`](operations.md) |

## What ships in the repo

```
.github/workflows/build-deploy.yml   # ECharts fetch step + telemetry env vars
.gitignore                           # ignores _static/js/echarts-min.js
_static/js/telemetry.js              # the entire client; ~220 lines
_templates/pid-sidebar-extra.html    # sparkline mount, total-count, Stats + Privacy links
conf.py                              # env-var gate + html-page-context hook
contents.rst                         # adds privacy + stats to hidden toctree
privacy.rst                          # reader-facing disclosure page
stats.rst                            # in-book readership dashboard (filled by JS)
scripts/server/build-sparklines.py        # nightly JSON builder for sparklines
scripts/server/run-goaccess.sh            # nightly GoAccess wrapper
scripts/server/caddy-json-to-combined.py  # filter: Caddy JSON → Apache combined
scripts/server/goaccessrc.example         # GoAccess config template
scripts/server/sparklines.conf.example    # build-sparklines.py config template
scripts/server/bots.txt.example           # shared UA blocklist seed
docs/telemetry/                           # everything you are reading
```

The ECharts JS bundle (`_static/js/echarts-min.js`) is **not** in git; it
is curl'd from jsdelivr at CI time, pinned to v5.5.1 simple build, and
served same-origin so the runtime never touches a third-party CDN.

## What ships at runtime

Three signals layered for resilience against ad-blockers, bots, and
self-hosting reusers.

1. **Server access logs → GoAccess** — 100 % of HTTP hits, including
   readers behind uBlock Origin. The production webserver is **Caddy**,
   which writes JSON access logs by default; the pipeline pipes them
   through `caddy-json-to-combined.py` so GoAccess (which understands
   Apache combined natively) can ingest the same stream as the
   archived pre-Hetzner Apache logs. Daily static HTML report at
   <https://learnche.org/_stats/>.
2. **GoatCounter cookieless pixel** — engagement signal (referrers,
   devices, time-on-site) for the ad-block-free subset. Free tier;
   no cookies; no IP storage; honours DNT; ~1 KB script tag.
3. **Search-query events** — what readers type into the sidebar
   search box, debounced and PII-stripped, sent to GoatCounter as
   custom events.
4. **Per-page 90-day sparkline + reader count** — derived from the
   access logs by `scripts/server/build-sparklines.py` into a public
   `sparklines.json`, rendered with a same-origin ECharts build in
   the sidebar of every page. The 90-day total reads for the current
   page are written next to the heading. Because it is log-derived it
   counts ad-blocked readers — the *honest* signal.
5. **In-book stats page** — [`/pid/stats`](https://learnche.org/pid/stats)
   reads the same `sparklines.json` and shows three site-wide
   widgets: a summary (total reads / pages with traffic / days of
   data), a daily totals chart across the whole book, and a top-20
   most-read pages table. All filled by `telemetry.js` at runtime;
   empty-state hides the widgets cleanly when no data is available.

## Operating principles

* **Production-only.** Telemetry is gated on `PID_BOOK_TELEMETRY=1`,
  which the deploy workflow sets only for non-PR builds. Local
  builds, PR previews, and self-hosted CC BY-SA forks never phone
  home. Three independent gates protect this:
  1. `conf.py` only injects the script when the env var is `"1"`.
  2. The CI workflow only sets the env var on non-PR events.
  3. `telemetry.js` itself short-circuits on `localhost`,
     `127.0.0.1`, `*.local`, and `file://`.
* **Cookieless.** No cookie of any kind is set, ever. No GDPR consent
  banner is required.
* **No IPs stored.** GoatCounter discards IPs server-side; GoAccess is
  invoked with `--anonymize-ip`; `build-sparklines.py` keeps only daily
  unique-IP counts and discards IPs after aggregation.
* **DNT honoured.** Browser Do-Not-Track silences the pixel entirely.
* **Same-origin.** Every JS asset (telemetry pixel, ECharts, sparklines
  data) is served from `learnche.org`. The only third-party network
  call is GoatCounter's `count.js` and its tracking endpoint — both
  cookieless and IP-stripped.
* **Open by default.** The aggregate dashboards (top pages,
  sparklines, search queries) are public, in keeping with the open
  spirit of the book.

## Threat model in one paragraph

We trust GoatCounter to discard IPs and not set cookies (their public
docs and code make this checkable). We trust our own webserver to
rotate access logs within 30 days. We do not protect against a
network adversary correlating the GoatCounter request with the ECharts
fetch on the same TLS connection (theoretically possible, practically
irrelevant for an open educational site). We do not run our own
bot-detection beyond UA blocklists shared between GoAccess and the
sparkline builder; sophisticated bot impersonation will leak through
and slightly inflate counts during the first week before our bot list
catches up.

## Where to start

* If you are a contributor wondering what's safe to change, read
  [`build-and-deploy.md`](build-and-deploy.md) and
  [`client.md`](client.md).
* If you are operating the server (cron, Caddy, log archive), read
  [`server-runbook.md`](server-runbook.md) and
  [`operations.md`](operations.md).
* If you are the maintainer reviewing whether the design still makes
  sense, read [`architecture.md`](architecture.md).
