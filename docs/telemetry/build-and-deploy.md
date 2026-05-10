# Build and deploy mechanics

How telemetry is wired into the Sphinx build and the GitHub Actions
deploy. Read this if you are changing the build, debugging why the
script tag is or isn't appearing, or trying to run a production-style
build locally.

## Environment variables

Two env vars control telemetry. Both are read by [`conf.py`](../../conf.py)
near line 240.

| Var | Default | Effect |
|---|---|---|
| `PID_BOOK_TELEMETRY` | `"0"` | Master gate. When **exactly** the string `"1"`, `conf.py` enables every telemetry feature. Any other value (including unset) keeps telemetry off. |
| `PID_BOOK_GC_CODE` | `""` | GoatCounter site code (the subdomain on `*.goatcounter.com`). When empty, the inline `<script>` still ships but `telemetry.js` short-circuits at the `if (!cfg.gc) return;` line — pageview tracking is disabled but the build still succeeds. |

**Default behaviour: off.** A developer running `make html` locally
gets exactly the same HTML as before this feature existed: no script
tag, no sparkline mount, no Privacy footer change beyond what's in
the static template. The Privacy *page* always builds because it's
in the toctree, but its sidebar link is only added when telemetry is
on (the link block lives outside the `{% if pid_telemetry %}` guard
in [`_templates/pid-sidebar-extra.html`](../../_templates/pid-sidebar-extra.html);
see "Sidebar template" below for the exact wiring).

## What `conf.py` does

The relevant block is roughly:

```python
TELEMETRY_ENABLED = os.environ.get("PID_BOOK_TELEMETRY", "0") == "1"
TELEMETRY_GC_CODE = os.environ.get("PID_BOOK_GC_CODE", "")

if TELEMETRY_ENABLED:
    html_js_files = [("js/telemetry.js", {"defer": "defer"})]

    html_context = {
        "pid_telemetry": True,
        "pid_gc_code": TELEMETRY_GC_CODE,
    }

    def _inject_telemetry_globals(app, pagename, templatename, context, doctree):
        gc = TELEMETRY_GC_CODE.replace('"', "")
        snippet = f'<script>window.__PID_TELEMETRY={{gc:"{gc}"}};</script>'
        context["metatags"] = context.get("metatags", "") + snippet

    def setup(app):
        app.connect("html-page-context", _inject_telemetry_globals)
        return {"parallel_read_safe": True, "parallel_write_safe": True}
```

What each piece does:

* **`html_js_files`** — Sphinx's HTML builder appends a `<script
  src="_static/js/telemetry.js" defer>` tag to every page. The tuple
  form `("path", {"defer": "defer"})` is supported on the pinned
  Sphinx ≥ 8.1.3. Critically, `html_js_files` is a *HTML builder*
  setting — the LaTeX, text, and ePub builders ignore it, so PDF and
  text builds are unaffected.
* **`html_context`** — passed to every Jinja template render. The
  sidebar template
  ([`_templates/pid-sidebar-extra.html`](../../_templates/pid-sidebar-extra.html))
  reads `pid_telemetry` to decide whether to render the sparkline
  mount point.
* **`html-page-context` handler** — Sphinx fires this event once per
  page during the HTML render. We append a one-line inline `<script>`
  to the per-page `metatags` context, which the
  `sphinx_book_theme` layout renders inside the page's `<head>`.
  This is the **theme-agnostic** way to add a HEAD script in Sphinx;
  it does not require overriding `layout.html`.
* **`setup(app)`** — Sphinx looks up a top-level `setup` function in
  `conf.py` at startup and calls it. We use this to register the
  page-context handler. The returned `parallel_*_safe = True` flags
  declare we don't introduce any cross-page state, so Sphinx may
  build pages in parallel.

The `gc.replace('"', "")` defence is intentional: even though
`TELEMETRY_GC_CODE` comes from a CI variable we control, stripping
quotes prevents an HTML-injection if someone ever wires a
user-controlled value into the env var.

## What the GitHub Actions workflow does

Two changes in [`.github/workflows/build-deploy.yml`](../../.github/workflows/build-deploy.yml):

### 1. Fetch ECharts at build time

```yaml
- name: Fetch ECharts (for sidebar sparklines)
  if: github.event_name != 'pull_request'
  run: |
    mkdir -p _static/js
    curl -fsSL --retry 3 \
      -o _static/js/echarts-min.js \
      https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.simple.min.js
    test -s _static/js/echarts-min.js
```

* The URL is **pinned** to `echarts@5.5.1/dist/echarts.simple.min.js`
  — the official "simple" build (line + bar + pie + tooltip + axes,
  no map/3D/treemap). Roughly 280 KB minified, ~80 KB gzip.
* `--retry 3` covers jsdelivr blips. `-fsSL` makes curl exit non-zero
  on HTTP errors and follow redirects silently.
* `test -s` asserts the file is non-empty. A zero-byte ECharts file
  would silently break the sparkline render.
* The file is **gitignored** (see `.gitignore` line 17: `_static/js/echarts-min.js`),
  so each CI run produces it fresh.
* `if: github.event_name != 'pull_request'` means PR builds skip the
  fetch — they don't need it, since they don't enable telemetry
  either. (This also avoids hitting jsdelivr from forks that don't
  trust our CI.)

### 2. Set telemetry env vars on the Build HTML step

```yaml
- name: Build HTML
  env:
    PID_BOOK_TELEMETRY: ${{ github.event_name != 'pull_request' && '1' || '0' }}
    PID_BOOK_GC_CODE: ${{ vars.GOATCOUNTER_CODE || 'learnche-pid' }}
  run: uv run make html
```

* The ternary `github.event_name != 'pull_request' && '1' || '0'`
  evaluates to `"1"` for `push` (master) and `workflow_dispatch`,
  and to `"0"` for `pull_request`. Belt-and-braces: even if this
  condition were wrong, the existing `if: github.event_name !=
  'pull_request'` on the Deploy step (line 126) prevents PR HTML
  from reaching the production server.
* `vars.GOATCOUNTER_CODE` is a repo-level GitHub Actions variable
  (Settings → Secrets and variables → Actions → Variables). When
  unset it falls back to `learnche-pid`. Use the variable mechanism,
  not a secret, because the site code is published in the rendered
  HTML anyway — it's a public identifier, not credentials.
* The site code only does anything if a matching site is actually
  registered on goatcounter.com. Until then, the pixel requests 404
  silently and the dashboard stays empty. See
  [`operations.md#first-time-setup-goatcounter-cloud-account`](operations.md#first-time-setup-goatcounter-cloud-account)
  for the one-time SaaS account walkthrough.

## What does **not** ship telemetry

* `make html` locally without env vars: no telemetry.
* `make latexpdf`: never. `html_js_files` is HTML-only.
* `make text`: never.
* `make epub`: never.
* PR preview builds in CI: env var is `"0"`, so no telemetry.
* `make serve` (which uses `start_server.py` on `localhost:8080`):
  even if you build with `PID_BOOK_TELEMETRY=1`, the script
  short-circuits on `localhost`. See [`client.md`](client.md) for the
  exact host check.

## Sidebar template

[`_templates/pid-sidebar-extra.html`](../../_templates/pid-sidebar-extra.html)
has two telemetry-related blocks:

```jinja
{% if pid_telemetry %}
<hr/>
<p style="color:#777; font-size:0.85em; margin:0.3em 0 0.1em">Page views (90 days)</p>
<div id="pid-sparkline" style="width:100%; height:38px"
     data-page="{{ pagename }}"></div>
{% endif %}
<hr/>
<p style="color:#777; font-size:0.85em">
  <a href="{{ pathto('privacy') }}">Privacy</a>
</p>
```

* The sparkline mount is **gated** on `pid_telemetry`, so it does not
  appear in dev or PR builds at all. This keeps local builds visually
  identical to a no-telemetry world.
* The Privacy link is **always rendered**. It points at
  `pathto('privacy')`, which produces an extensionless URL because
  `html_link_suffix = ""` is set in `conf.py`.
* `data-page="{{ pagename }}"` — `pagename` is the canonical
  Sphinx-relative slug like `data-visualization/box-plots`. This is
  the **key** into `sparklines.json`. See
  [`sparklines-schema.md`](sparklines-schema.md) for the contract.

## Running a production-style build locally

```sh
# Mimic CI exactly:
mkdir -p _static/js
curl -fsSL --retry 3 \
  -o _static/js/echarts-min.js \
  https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.simple.min.js

PID_BOOK_TELEMETRY=1 \
PID_BOOK_GC_CODE=learnche-pid \
make html

# Verify the script tag is present on a representative page:
grep -l 'telemetry.js'        _build/html/contents
grep -l '__PID_TELEMETRY'     _build/html/contents
grep -l 'pid-sparkline'       _build/html/data-visualization/box-plots
```

When you `make serve` and visit `http://localhost:8080`, the script
loads but does **not** call home — the host check inside
`telemetry.js` short-circuits on `localhost`. To verify, open
DevTools → Network and confirm there are no requests to `gc.zgo.at`.

To clean up afterwards:

```sh
rm -f _static/js/echarts-min.js  # gitignored, but just to be tidy
make clean
```

## Builder isolation matrix

| Builder | `html_js_files` consumed? | Telemetry shipped? |
|---|---|---|
| `html` (production) | yes, when env var `=1` | yes |
| `html` (local, no env var) | no (gated by `if TELEMETRY_ENABLED:`) | no |
| `latex` / `latexpdf` | no — LaTeX builder ignores `html_js_files` | no |
| `text` | no — same | no |
| `epub` | no — same | no |
| `linkcheck` | no — does not render templates | no |

This is why the CLAUDE.md "make text MUST succeed" rule is
unaffected: `text` never sees the telemetry config.

## Files map (build side)

| File | Purpose | Modified by this feature? |
|---|---|---|
| [`conf.py`](../../conf.py) | Sphinx config | yes — env-var gate, `setup()`, `html_context`, `html_js_files` |
| [`.github/workflows/build-deploy.yml`](../../.github/workflows/build-deploy.yml) | CI workflow | yes — ECharts fetch step, `Build HTML` env block |
| [`.gitignore`](../../.gitignore) | git ignore rules | yes — ignores `_static/js/echarts-min.js` |
| [`_templates/pid-sidebar-extra.html`](../../_templates/pid-sidebar-extra.html) | sidebar Jinja template | yes — sparkline mount + Privacy link |
| [`_static/js/telemetry.js`](../../_static/js/telemetry.js) | runtime client | new file |
| [`privacy.rst`](../../privacy.rst) | reader-facing disclosure | new file |
| [`contents.rst`](../../contents.rst) | book root | yes — adds `privacy` to hidden toctree |
| [`CITATION.cff`](../../CITATION.cff) | citation metadata | yes — `date-released` bumped |
| `_static/js/echarts-min.js` | ECharts bundle | new file, **gitignored**, fetched at CI time |
