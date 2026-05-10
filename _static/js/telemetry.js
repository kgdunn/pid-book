/*
 * pid-book telemetry: privacy-first, cookieless, opt-out-friendly.
 *
 * Loaded only when conf.py sees PID_BOOK_TELEMETRY=1 (production deploys
 * from GitHub Actions). Honours Do-Not-Track. Skips localhost / file://
 * so that CC BY-SA reusers self-hosting the source never phone home.
 *
 * Three responsibilities:
 *   1. Pageview pixel via GoatCounter (loaded async).
 *   2. Search-query event capture from BOTH Sphinx and Pagefind boxes.
 *   3. 90-day pageview sparkline in the sidebar (ECharts, lazy-loaded).
 *
 * The ECharts asset (`_static/js/echarts-min.js`) is fetched at build time
 * by .github/workflows/build-deploy.yml; it is NOT in git. If absent the
 * sparkline is silently skipped — pageview/search tracking still works.
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
                smooth: true,
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
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
