/*
 * pid-book telemetry: privacy-first, cookieless, opt-out-friendly.
 *
 * Loaded only when conf.py sees PID_BOOK_TELEMETRY=1 (production deploys
 * from GitHub Actions). Honours Do-Not-Track. Skips localhost / file://
 * so that CC BY-SA reusers self-hosting the source never phone home.
 *
 * Four responsibilities:
 *   1. Pageview pixel via GoatCounter (loaded async).
 *   2. Search-query event capture from BOTH Sphinx and Pagefind boxes.
 *   3. Yearly pageview sparkline in the sidebar (ECharts, lazy-loaded),
 *      with the per-page total written into #pid-sparkline-total.
 *   4. The /pid/stats page: site-wide summary, daily-totals chart, and
 *      top-N table sourced from the same /_stats/sparklines.json.
 *
 * The ECharts asset (`_static/js/echarts-min.js`) is fetched at build time
 * by .github/workflows/build-deploy.yml; it is NOT in git. If absent the
 * sparkline / stats charts are silently skipped — pageview/search tracking
 * still works.
 *
 * What is collected and what is not is described at /pid/privacy.
 */
(function () {
  // 0. Bail-outs (run before any network)
  if (
    navigator.doNotTrack === "1" ||
    window.doNotTrack === "1" ||
    navigator.msDoNotTrack === "1"
  )
    return;

  var host = location.hostname;
  if (
    location.protocol === "file:" ||
    host === "localhost" ||
    host === "127.0.0.1" ||
    host === "" ||
    /\.local$/.test(host)
  )
    return;

  var cfg = window.__PID_TELEMETRY || {};
  if (!cfg.gc) return;

  // -------------------------------------------------------------------
  // Front-end display window.
  //
  // The backend (build-sparklines.py + /etc/pid-book/sparklines.conf)
  // keeps a 365-day window in /_stats/sparklines.json. The in-book UI
  // is intentionally narrower: showing 365-day totals on a young
  // deployment (or one with historical log gaps) makes pages look
  // unread when they are actually being read every day.
  //
  // Change DISPLAY_DAYS in lockstep with the labels that mention "N
  // days" in:
  //   - _templates/pid-sidebar-extra.html   ("Page views (N days)")
  //   - stats.rst                            ("(last N days)" x3 + body)
  // and the backend (365) stays the same.
  // -------------------------------------------------------------------
  var DISPLAY_DAYS = 15;
  var DISPLAY_LABEL = DISPLAY_DAYS + " days";

  // Find the most recent date present anywhere in the JSON. Used as
  // the anchor for the rolling display window. Series are sorted
  // ascending in the producer, so the last element holds the latest.
  function globalAnchorDate(data) {
    var max = "";
    for (var page in data) {
      var s = data[page];
      if (s && s.length) {
        var last = s[s.length - 1][0];
        if (last > max) max = last;
      }
    }
    return max;
  }

  // "YYYY-MM-DD" arithmetic: return the date `days-1` days before
  // anchor, so a window of `days` includes the anchor day itself.
  function cutoffDateString(anchor, days) {
    if (!anchor) return "";
    var d = new Date(anchor + "T00:00:00Z");
    d.setUTCDate(d.getUTCDate() - days + 1);
    return d.toISOString().slice(0, 10);
  }

  function filterToWindow(series, cutoff) {
    if (!series || !cutoff) return series || [];
    return series.filter(function (p) { return p[0] >= cutoff; });
  }

  // 1. Path normalisation: extensionless URLs, fold trailing slash and /index.
  function normPath() {
    var p = location.pathname.replace(/\/+$/, "") || "/";
    p = p.replace(/\.html?$/i, "").replace(/\/index$/, "");
    return p + location.search;
  }

  // 2. GoatCounter pixel.
  window.goatcounter = { no_onload: true, path: normPath };
  var gcScript = document.createElement("script");
  gcScript.async = true;
  gcScript.setAttribute(
    "data-goatcounter",
    "https://" + cfg.gc + ".goatcounter.com/count"
  );
  gcScript.src = "//gc.zgo.at/count.js";
  gcScript.onload = function () {
    try {
      window.goatcounter.count();
    } catch (e) {
      /* ignore */
    }
  };
  document.head.appendChild(gcScript);

  // 3. Search instrumentation. Debounced; never sends PII or empties.
  var DEBOUNCE_MS = 800;
  var lastSent = "";
  function sendQuery(q) {
    q = (q || "").trim();
    if (!q || q === lastSent || q.length > 80) return;
    if (/[\w.+-]+@[\w-]+\.[\w.-]+/.test(q)) return; // crude email guard
    lastSent = q;
    try {
      window.goatcounter.count({
        path: "/search?q=" + encodeURIComponent(q),
        event: true,
      });
    } catch (e) {
      /* ignore */
    }
  }
  function debounce(fn) {
    var t;
    return function (e) {
      clearTimeout(t);
      var v = e.target.value;
      t = setTimeout(function () {
        fn(v);
      }, DEBOUNCE_MS);
    };
  }

  function hookSphinxSearch() {
    var el = document.querySelector('input[name="q"]');
    if (el && !el.__pidHooked) {
      el.__pidHooked = true;
      el.addEventListener("input", debounce(sendQuery));
    }
  }
  function hookPagefindSearch() {
    var el = document.querySelector(".pagefind-ui__search-input");
    if (el && !el.__pidHooked) {
      el.__pidHooked = true;
      el.addEventListener("input", debounce(sendQuery));
      return true;
    }
    return false;
  }

  // 4. Sparkline. Lazy-loads ECharts only if the mount point exists.
  // The sidebar template ships the whole block (heading + chart) hidden
  // by default via `<div id="pid-sparkline-block" style="display:none">`.
  // We only unhide it after the chart actually renders, so a blocked
  // fetch / DNT / empty data path never leaves an orphan heading visible.
  function renderSparkline() {
    var mount = document.getElementById("pid-sparkline");
    if (!mount) return;
    var block = document.getElementById("pid-sparkline-block");
    var pageKey = mount.getAttribute("data-page") || "";
    if (!pageKey) {
      // Fallback: derive from the URL when the template didn't supply one.
      pageKey = location.pathname
        .replace(/^\/pid\//, "")
        .replace(/\/+$/, "")
        .replace(/\.html?$/i, "");
      if (!pageKey) pageKey = "contents";
    }

    fetch("/_stats/sparklines.json", { cache: "default" })
      .then(function (r) {
        if (!r.ok) throw new Error("sparklines.json " + r.status);
        return r.json();
      })
      .then(function (data) {
        // The JSON is the full 365-day window; the UI shows only
        // the most recent DISPLAY_DAYS days from the global anchor
        // (so different pages compare against the same date range).
        var anchor = globalAnchorDate(data);
        var cutoff = cutoffDateString(anchor, DISPLAY_DAYS);
        var series = filterToWindow(data && data[pageKey], cutoff);
        if (!series || !series.length) {
          // No history for this page in the display window (fresh
          // page, content blocker tampering, or genuinely unread for
          // DISPLAY_DAYS). Block stays hidden — nothing to do.
          return;
        }
        // Write the total-reads-in-window into the sidebar heading, if
        // its span is present (template ships it; older builds may not).
        var totalEl = document.getElementById("pid-sparkline-total");
        if (totalEl) {
          var total = series.reduce(function (a, p) { return a + p[1]; }, 0);
          totalEl.textContent = total.toLocaleString() + " reads";
        }
        loadECharts(function (echarts) {
          if (!echarts) return;
          var dates = series.map(function (p) {
            return p[0];
          });
          var values = series.map(function (p) {
            return p[1];
          });
          var chart;
          try {
            chart = echarts.init(mount, null, { renderer: "svg" });
          } catch (e) {
            return;
          }
          chart.setOption({
            grid: { left: 0, right: 0, top: 2, bottom: 0 },
            xAxis: { type: "category", show: false, data: dates },
            yAxis: { type: "value", show: false },
            tooltip: {
              trigger: "axis",
              formatter: function (params) {
                var p = params[0];
                return p.name + "<br/>" + p.value + " views";
              },
            },
            series: [
              {
                type: "line",
                data: values,
                showSymbol: false,
                smooth: false,
                lineStyle: { width: 1.5 },
                areaStyle: { opacity: 0.15 },
              },
            ],
          });
          // Reveal the whole block now that the chart is actually drawn.
          if (block) block.style.display = "";
          window.addEventListener("resize", function () {
            chart.resize();
          });
        });
      })
      .catch(function () {
        /* network/JSON error or content blocker: block stays hidden;
           the page never shows an orphan "Page views" heading. */
      });
  }

  // 4b. Stats page widgets. Run only if the /pid/stats page is loaded,
  // detected by the presence of #pid-stats-summary in the DOM. Four
  // mounts are filled from the same sparklines.json the sidebar uses:
  //   #pid-stats-summary  — three big-number cards (reads, pages, days)
  //   #pid-stats-daily    — daily-totals line chart across all pages
  //   #pid-stats-top      — top-20 most-read pages table
  //   #pid-stats-bottom   — bottom-10 least-read pages table
  function renderStatsPage() {
    var summary = document.getElementById("pid-stats-summary");
    if (!summary) return;

    var dailyMount = document.getElementById("pid-stats-daily");
    var topMount = document.getElementById("pid-stats-top");
    var bottomMount = document.getElementById("pid-stats-bottom");

    function showEmpty(msg) {
      // Replace whatever the page shipped (could be the "Statistics
      // could not load" placeholder, or a previous render's content)
      // with a JS-specific message. The chart/table mounts are already
      // hidden by default in stats.rst — re-hide just in case.
      summary.innerHTML =
        '<p style="color:#777"><em>' +
        (msg || "Statistics aren't available yet. The nightly aggregator " +
               "may not have run, or this is a local build.") +
        "</em></p>";
      if (dailyMount) dailyMount.style.display = "none";
      if (topMount) topMount.style.display = "none";
      if (bottomMount) bottomMount.style.display = "none";
    }

    // Build a [rank, page-link, count] HTML table from an array of
    // [pagename, count] entries already in display order.
    function buildPageTable(entries) {
      var rows = entries.map(function (kv, i) {
        var page = kv[0], count = kv[1];
        // Sphinx pagename → URL. /index suffix means the directory
        // landing page; other pages are direct.
        var href = "/pid/" + page.replace(/\/index$/, "/");
        return '<tr><td class="pid-stats-rank">' + (i + 1) +
          '</td><td><a href="' + href + '">' + page + "</a></td>" +
          '<td class="pid-stats-count">' + count.toLocaleString() +
          "</td></tr>";
      }).join("");
      return '<table class="pid-stats-table"><thead><tr>' +
        '<th class="pid-stats-rank">#</th><th>Page</th>' +
        '<th class="pid-stats-count">Reads</th></tr></thead>' +
        "<tbody>" + rows + "</tbody></table>";
    }

    fetch("/_stats/sparklines.json", { cache: "default" })
      .then(function (r) {
        if (!r.ok) throw new Error("sparklines.json " + r.status);
        return r.json();
      })
      .then(function (data) {
        var pages = data && Object.keys(data);
        if (!pages || !pages.length) { showEmpty(); return; }

        // The JSON holds 365 days; the UI shows the most recent
        // DISPLAY_DAYS days only. Compute the cutoff once and filter
        // every per-page series through it before aggregating.
        var anchor = globalAnchorDate(data);
        var cutoff = cutoffDateString(anchor, DISPLAY_DAYS);

        var totalReads = 0;
        var dailyMap = {};
        var pageTotals = [];
        pages.forEach(function (page) {
          var series = filterToWindow(data[page], cutoff);
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
        var dailyDates = Object.keys(dailyMap).sort();

        // If the window has no data at all, fall back to the empty UI.
        if (!pageTotals.length) { showEmpty(); return; }

        // Summary cards.
        summary.innerHTML =
          '<div class="pid-stats-card"><div class="pid-stats-num">' +
            totalReads.toLocaleString() +
          '</div><div class="pid-stats-label">reads (' + DISPLAY_LABEL + ')</div></div>' +
          '<div class="pid-stats-card"><div class="pid-stats-num">' +
            pageTotals.length.toLocaleString() +
          '</div><div class="pid-stats-label">pages with traffic</div></div>' +
          '<div class="pid-stats-card"><div class="pid-stats-num">' +
            dailyDates.length +
          '</div><div class="pid-stats-label">days of data</div></div>';

        // Daily totals chart. Mount is hidden by default in stats.rst
        // (so it doesn't show a 280px-tall blank area when JS is blocked
        // or the fetch fails); unhide after the chart actually renders.
        if (dailyMount && dailyDates.length) {
          loadECharts(function (echarts) {
            if (!echarts) return;
            var chart;
            try { chart = echarts.init(dailyMount, null, { renderer: "svg" }); }
            catch (e) { return; }
            chart.setOption({
              grid: { left: 50, right: 16, top: 16, bottom: 36 },
              xAxis: { type: "category", data: dailyDates,
                       axisLabel: { hideOverlap: true } },
              yAxis: { type: "value", name: "Reads / day" },
              tooltip: {
                trigger: "axis",
                formatter: function (params) {
                  var p = params[0];
                  return p.name + "<br/>" + p.value.toLocaleString() +
                         " reads";
                },
              },
              series: [{
                type: "line",
                smooth: false,
                showSymbol: false,
                data: dailyDates.map(function (d) { return dailyMap[d]; }),
                lineStyle: { width: 1.5 },
                areaStyle: { opacity: 0.15 },
              }],
            });
            dailyMount.style.display = "";
            window.addEventListener("resize", function () { chart.resize(); });
          });
        }

        // Top-N table (most-read pages).
        if (topMount) {
          topMount.innerHTML = buildPageTable(pageTotals.slice(0, 20));
          topMount.style.display = "";
        }

        // Bottom-N table (least-read pages — ascending, lowest first).
        // Pages with zero hits never reach the JSON, so this only
        // surfaces pages with at least one read in the window.
        if (bottomMount) {
          var bottom = pageTotals.slice(-10).reverse();
          bottomMount.innerHTML = buildPageTable(bottom);
          bottomMount.style.display = "";
        }
      })
      .catch(function () { showEmpty(); });
  }

  function loadECharts(cb) {
    if (window.echarts) return cb(window.echarts);
    var s = document.createElement("script");
    s.src = "/pid/_static/js/echarts-min.js";
    s.async = true;
    s.onload = function () {
      cb(window.echarts);
    };
    s.onerror = function () {
      cb(null);
    };
    document.head.appendChild(s);
  }

  // 5. Boot once the DOM is ready.
  function boot() {
    hookSphinxSearch();
    if (!hookPagefindSearch()) {
      var mo = new MutationObserver(function () {
        if (hookPagefindSearch()) mo.disconnect();
      });
      mo.observe(document.body, { childList: true, subtree: true });
      // Safety: stop observing after 15 s no matter what.
      setTimeout(function () {
        mo.disconnect();
      }, 15000);
    }
    renderSparkline();
    renderStatsPage();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
