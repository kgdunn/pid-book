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
 *   3. 90-day pageview sparkline in the sidebar (ECharts, lazy-loaded),
 *      with the per-page 90-day total written into #pid-sparkline-total.
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
  function renderSparkline() {
    var mount = document.getElementById("pid-sparkline");
    if (!mount) return;
    var pageKey = mount.getAttribute("data-page") || "";
    if (!pageKey) {
      // Fallback: derive from the URL when the template didn't supply one.
      pageKey = location.pathname
        .replace(/^\/pid\//, "")
        .replace(/\/+$/, "")
        .replace(/\.html?$/i, "");
      if (!pageKey) pageKey = "contents";
    }

    fetch("/_stats/sparklines.json", { cache: "force-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("sparklines.json " + r.status);
        return r.json();
      })
      .then(function (data) {
        var series = data && data[pageKey];
        if (!series || !series.length) {
          // No history yet (e.g. a freshly added page). Hide silently.
          var heading = mount.previousElementSibling;
          if (heading && heading.tagName === "P") heading.style.display = "none";
          mount.style.display = "none";
          return;
        }
        // Write the 90-day total into the sidebar heading, if its span
        // is present (template ships it; older builds may not).
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
          window.addEventListener("resize", function () {
            chart.resize();
          });
        });
      })
      .catch(function () {
        /* network/JSON error: leave the empty mount; do not break the page */
      });
  }

  // 4b. Stats page widgets. Run only if the /pid/stats page is loaded,
  // detected by the presence of #pid-stats-summary in the DOM. Three
  // mounts are filled from the same sparklines.json the sidebar uses:
  //   #pid-stats-summary  — three big-number cards (reads, pages, days)
  //   #pid-stats-daily    — daily-totals line chart across all pages
  //   #pid-stats-top      — top-20 most-read pages table
  function renderStatsPage() {
    var summary = document.getElementById("pid-stats-summary");
    if (!summary) return;

    var dailyMount = document.getElementById("pid-stats-daily");
    var topMount = document.getElementById("pid-stats-top");

    function showEmpty(msg) {
      summary.innerHTML =
        '<p style="color:#777"><em>' +
        (msg || "Statistics aren't available yet. The nightly aggregator " +
               "may not have run, or this is a local build.") +
        "</em></p>";
      if (dailyMount) dailyMount.style.display = "none";
      if (topMount) topMount.style.display = "none";
    }

    fetch("/_stats/sparklines.json", { cache: "force-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("sparklines.json " + r.status);
        return r.json();
      })
      .then(function (data) {
        var pages = data && Object.keys(data);
        if (!pages || !pages.length) { showEmpty(); return; }

        // Aggregate.
        var totalReads = 0;
        var dailyMap = {};
        var pageTotals = [];
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
        var dailyDates = Object.keys(dailyMap).sort();

        // Summary cards.
        summary.innerHTML =
          '<div class="pid-stats-card"><div class="pid-stats-num">' +
            totalReads.toLocaleString() +
          '</div><div class="pid-stats-label">reads (90 days)</div></div>' +
          '<div class="pid-stats-card"><div class="pid-stats-num">' +
            pageTotals.length.toLocaleString() +
          '</div><div class="pid-stats-label">pages with traffic</div></div>' +
          '<div class="pid-stats-card"><div class="pid-stats-num">' +
            dailyDates.length +
          '</div><div class="pid-stats-label">days of data</div></div>';

        // Daily totals chart.
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
            window.addEventListener("resize", function () { chart.resize(); });
          });
        }

        // Top-N table.
        if (topMount) {
          var N = 20;
          var rows = pageTotals.slice(0, N).map(function (kv, i) {
            var page = kv[0], count = kv[1];
            // Sphinx pagename → URL. /index suffix means the directory
            // landing page; other pages are direct.
            var href = "/pid/" + page.replace(/\/index$/, "/");
            return '<tr><td class="pid-stats-rank">' + (i + 1) +
              '</td><td><a href="' + href + '">' + page + "</a></td>" +
              '<td class="pid-stats-count">' + count.toLocaleString() +
              "</td></tr>";
          }).join("");
          topMount.innerHTML =
            '<table class="pid-stats-table"><thead><tr>' +
            '<th class="pid-stats-rank">#</th><th>Page</th>' +
            '<th class="pid-stats-count">Reads</th></tr></thead>' +
            "<tbody>" + rows + "</tbody></table>";
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
