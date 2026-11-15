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
 *   3. Pageview sparkline in the sidebar, with the per-page total written
 *      into #pid-sparkline-total.
 *   4. The /pid/stats page: a daily-totals chart with a two-handle window
 *      slider, and a summary and page tables that follow the window, all
 *      sourced from the same /_stats/sparklines.json.
 *
 * The charts are inline SVG drawn here; there is no charting library.
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
  // keeps a rolling 365-day window in /_stats/sparklines.json. That is
  // the ceiling, not the current contents: the access-log history only
  // starts in May 2026 (see stats.rst), so the file holds however many
  // days have accumulated since then and grows by one per night.
  //
  // The in-book UI is intentionally narrower than the backend window:
  // showing 365-day totals while the history is still filling in makes
  // pages look unread when they are actually being read every day.
  //
  // Change DISPLAY_DAYS in lockstep with the labels that mention "N
  // days" in:
  //   - _templates/pid-sidebar-extra.html   ("Page views (N days)")
  //   - stats.rst                            (the body text)
  // and the backend (365) stays the same.
  // -------------------------------------------------------------------
  var DISPLAY_DAYS = 180;

  // The newest day that can possibly be complete, in UTC. The nightly
  // builder already stops at yesterday (lag_days), but a server still
  // running the older script publishes a bucket for the running day
  // holding only a few hours of traffic, which plots as a near-zero
  // cliff at the right-hand edge. Bounding the window here keeps the
  // charts correct regardless of which build of the script is deployed.
  function lastCompleteDate() {
    var d = new Date();
    d.setUTCDate(d.getUTCDate() - 1);
    return d.toISOString().slice(0, 10);
  }

  // Find the most recent *complete* date present anywhere in the JSON.
  // Used as the anchor for the rolling display window. Series are sorted
  // ascending in the producer, so we walk back from the end and take the
  // first point that is not the running day. Returns "" when the file
  // holds nothing but a partial day (or nothing at all).
  function globalAnchorDate(data) {
    var limit = lastCompleteDate();
    var max = "";
    for (var page in data) {
      var s = data[page];
      if (!s) continue;
      for (var i = s.length - 1; i >= 0; i--) {
        var d = s[i][0];
        if (d > limit) continue;
        if (d > max) max = d;
        break;
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

  // The days the UI shows, oldest first: the DISPLAY_DAYS complete days
  // that end at the anchor, or fewer while the logs hold less history
  // than that. Empty when the file holds no complete day.
  function displayDays(data) {
    var anchor = globalAnchorDate(data);
    if (!anchor) return [];
    var first = anchor;
    for (var page in data) {
      var s = data[page];
      if (s && s.length && s[0][0] < first) first = s[0][0];
    }
    var cutoff = cutoffDateString(anchor, DISPLAY_DAYS);
    if (first < cutoff) first = cutoff;
    var days = [];
    var d = new Date(first + "T00:00:00Z");
    while (days.length < DISPLAY_DAYS) {
      var iso = d.toISOString().slice(0, 10);
      days.push(iso);
      if (iso >= anchor) break;
      d.setUTCDate(d.getUTCDate() + 1);
    }
    return days;
  }

  // One page's reads on each of `days`. The JSON omits days without a
  // read; filling them with 0 keeps the x-axis of every chart in time.
  function dense(series, days) {
    var at = {};
    (series || []).forEach(function (p) {
      at[p[0]] = p[1] | 0;
    });
    return days.map(function (d) {
      return at[d] || 0;
    });
  }

  // "14 Nov" from "2026-11-14", in the reader's locale. No year: the days
  // shown span less than one.
  function formatDay(iso, weekday) {
    return new Date(iso + "T00:00:00Z").toLocaleDateString(undefined, {
      weekday: weekday ? "short" : undefined,
      day: "numeric",
      month: "short",
      timeZone: "UTC",
    });
  }

  // The data file, fetched once per page however many widgets read it.
  // `cache: "default"` honours the server's max-age=3600.
  var statsPromise;
  function fetchStats() {
    statsPromise =
      statsPromise ||
      fetch("/_stats/sparklines.json", { cache: "default" })
        .then(function (r) {
          if (!r.ok) throw new Error("sparklines.json " + r.status);
          return r.json();
        })
        .then(function (data) {
          return data || {};
        });
    return statsPromise;
  }

  // The line and the filled area of a sparkline, as SVG paths. x is the
  // day index and y the reads as a fraction of `top`. sparkSvg() lets CSS
  // stretch both to the container, so a chart is the right size at every
  // width and needs no resize handler.
  function sparkPaths(values, top) {
    var line = values
      .map(function (v, i) {
        return (i ? "L" : "M") + i + "," + (1 - v / (top || 1)).toFixed(3);
      })
      .join("");
    return (
      '<path class="pid-spark-area" d="' + line + "L" + (values.length - 1) + ',1L0,1Z"/>' +
      '<path class="pid-spark-line" d="' + line + '"/>'
    );
  }
  function sparkSvg(nDays, inner) {
    return (
      '<svg class="pid-spark" viewBox="0 0 ' + Math.max(nDays - 1, 1) + ' 1" ' +
      'preserveAspectRatio="none" aria-hidden="true">' + inner + "</svg>"
    );
  }

  // Tell `report` which day is under the pointer: its index while the
  // pointer is over `el`, and -1 once it has left.
  function onHover(el, nDays, report) {
    function move(e) {
      // Dragging a slider thumb inside `el` is not pointing at a day.
      if (e.target.tagName === "INPUT") return report(-1);
      var box = el.getBoundingClientRect();
      var i = Math.round(((e.clientX - box.left) / box.width) * (nDays - 1));
      report(Math.max(0, Math.min(nDays - 1, i)));
    }
    function leave() {
      report(-1);
    }
    el.addEventListener("pointerdown", move);
    el.addEventListener("pointermove", move);
    el.addEventListener("pointerleave", leave);
    el.addEventListener("pointercancel", leave);
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

  // 4. Sidebar sparkline. The template ships the whole block (heading +
  // chart) hidden via `<div id="pid-sparkline-block" style="display:none">`.
  // It is revealed only once the chart is drawn, so a blocked fetch, DNT
  // or a page without reads never leaves an orphan heading visible.
  function renderSparkline() {
    var mount = document.getElementById("pid-sparkline");
    if (!mount) return;
    var block = document.getElementById("pid-sparkline-block");
    var totalEl = document.getElementById("pid-sparkline-total");
    var pageKey = mount.getAttribute("data-page") || "";
    if (!pageKey) {
      // Fallback: derive from the URL when the template didn't supply one.
      pageKey = location.pathname
        .replace(/^\/pid\//, "")
        .replace(/\/+$/, "")
        .replace(/\.html?$/i, "");
      if (!pageKey) pageKey = "contents";
    }

    fetchStats()
      .then(function (data) {
        // Every page is drawn over the same days, so that two pages
        // compare against the same date range.
        var days = displayDays(data);
        var values = dense(data[pageKey], days);
        var total = values.reduce(function (a, v) {
          return a + v;
        }, 0);
        // No reads for this page on those days: the block stays hidden.
        if (!total) return;
        mount.innerHTML = sparkSvg(days.length, sparkPaths(values, Math.max.apply(null, values)));
        if (totalEl) {
          var totalText = total.toLocaleString() + " reads";
          totalEl.textContent = totalText;
          // While the pointer is on the chart, the heading reads that day.
          onHover(mount, days.length, function (i) {
            totalEl.textContent = i < 0 ? totalText : formatDay(days[i]) + ": " + values[i].toLocaleString();
          });
        }
        if (block) block.style.display = "";
      })
      .catch(function () {
        /* network/JSON error or content blocker: the block stays hidden. */
      });
  }

  // A round axis step (1, 2 or 5 times a power of ten) that puts two to
  // five gridlines under `peak`.
  function axisStep(peak) {
    var rough = Math.max(peak, 1) / 5;
    var pow = Math.pow(10, Math.floor(Math.log(rough) / Math.LN10));
    var lead = rough / pow;
    return Math.max(1, (lead > 5 ? 10 : lead > 2 ? 5 : lead > 1 ? 2 : 1) * pow);
  }

  function escapeHtml(text) {
    return String(text).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // "+1,234" or "-56": a whole number that always carries its sign.
  function signed(x) {
    var r = Math.round(x);
    return (r > 0 ? "+" : "") + r.toLocaleString();
  }

  // 4b. Stats page. Runs only where stats.rst put #pid-stats-daily. That
  // mount gets the daily-totals chart with its two-handle window slider.
  // Four more mounts describe the window the slider selects:
  //   #pid-stats-summary  big-number cards
  //   #pid-stats-movers   the pages whose reads changed most
  //   #pid-stats-top      the most-read pages
  //   #pid-stats-bottom   the least-read pages
  function renderStatsPage() {
    var daily = document.getElementById("pid-stats-daily");
    if (!daily) return;
    var mounts = {};
    ["summary", "movers", "top", "bottom"].forEach(function (k) {
      mounts[k] = document.getElementById("pid-stats-" + k);
    });

    function note(text) {
      return '<p style="color:#777"><em>' + text + "</em></p>";
    }
    // stats.rst ships the four mounts hidden, so a page whose data never
    // arrives shows its headings and the note in #pid-stats-daily, not
    // empty boxes. A mount is revealed when it is first filled.
    function fill(el, html) {
      if (!el) return;
      el.innerHTML = html;
      el.style.display = "";
    }
    function showEmpty() {
      daily.innerHTML = note(
        "Statistics aren't available yet. The nightly aggregator may not have run, or this is a local build."
      );
    }

    fetchStats()
      .then(function (data) {
        var days = displayDays(data);
        var n = days.length;

        // Every page with a read on those days, and the book's daily totals.
        var site = days.map(function () {
          return 0;
        });
        var pages = [];
        Object.keys(data).forEach(function (name) {
          var values = dense(data[name], days);
          var total = 0;
          values.forEach(function (v, i) {
            total += v;
            site[i] += v;
          });
          if (!total) return;
          pages.push({
            name: name,
            values: values,
            total: total,
            spark: sparkPaths(values, Math.max.apply(null, values)),
          });
        });
        if (!pages.length) {
          showEmpty();
          return;
        }

        // The chart. Gridlines, month labels and the slider are HTML laid
        // over the stretched SVG, so text keeps its shape at any width.
        var step = axisStep(Math.max.apply(null, site));
        var top = Math.ceil(Math.max.apply(null, site) / step) * step;
        var ticks = "";
        for (var t = 0; t <= top; t += step) {
          ticks +=
            '<div class="pid-stats-tick" style="bottom:' + (t / top) * 100 + '%"><span>' +
            t.toLocaleString() + "</span></div>";
        }
        var months = "";
        days.forEach(function (iso, i) {
          if (iso.slice(8) !== "01") return;
          var label = new Date(iso + "T00:00:00Z").toLocaleDateString(undefined, {
            month: "short",
            year: iso.slice(5, 7) === "01" ? "numeric" : undefined,
            timeZone: "UTC",
          });
          months += '<span style="left:' + (i / (n - 1 || 1)) * 100 + '%">' + label + "</span>";
        });
        var presets = [7, 30, 90, n]
          .filter(function (d, i) {
            return d < n || i === 3;
          })
          .map(function (d) {
            return (
              '<button type="button" class="btn btn-sm btn-outline-secondary" data-days="' + d + '">' +
              (d < n ? d + " days" : "All") + "</button>"
            );
          })
          .join("");
        var edge = '<input type="range" min="0" max="' + (n - 1) + '" aria-label="Edge of the window of days">';
        daily.innerHTML =
          '<div class="pid-stats-bar"><span class="pid-stats-presets">' + presets + "</span>" +
          '<span class="pid-stats-readout"></span></div>' +
          '<div class="pid-stats-plot">' + ticks +
          sparkSvg(n, '<rect class="pid-spark-band" y="0" height="1"/>' + sparkPaths(site, top)) +
          '<div class="pid-stats-cursor" style="display:none"></div>' + edge + edge + "</div>" +
          '<div class="pid-stats-months">' + months + "</div>";
        daily.style.display = "";

        var band = daily.querySelector(".pid-spark-band");
        var cursor = daily.querySelector(".pid-stats-cursor");
        var readout = daily.querySelector(".pid-stats-readout");
        var edges = daily.querySelectorAll("input");
        var buttons = daily.querySelectorAll("button");
        var windowText = "";

        // Describe the days a..b (indexes into `days`, inclusive) in the
        // chart, the summary and the three tables.
        function select(a, b) {
          var inside = b - a + 1; // days in the window
          var outside = n - inside; // the other days: what the window is compared with

          // A day owns the half step on either side of its point.
          var x0 = Math.max(a - 0.5, 0);
          var x1 = Math.min(b + 0.5, n - 1);
          band.setAttribute("x", x0);
          band.setAttribute("width", outside ? x1 - x0 : 0);
          var rowBand = outside
            ? '<rect class="pid-spark-band" x="' + x0 + '" width="' + (x1 - x0) + '" y="0" height="1"/>'
            : "";

          windowText =
            (a === b ? formatDay(days[a]) : formatDay(days[a]) + " to " + formatDay(days[b])) +
            " (" + inside + (inside === 1 ? " day)" : " days)");
          readout.textContent = windowText;
          [].forEach.call(buttons, function (btn) {
            var active = b === n - 1 && inside === +btn.getAttribute("data-days");
            btn.classList.toggle("active", active);
            btn.setAttribute("aria-pressed", active);
          });

          // `expected` is the reads a page would have had in the window at
          // the daily rate it had on the other days, and `change` is how
          // far the window is from that. The changes of all the pages add
          // up to the change of the book.
          var reads = 0;
          var expected = 0;
          var rows = pages.map(function (p) {
            var r = { page: p, reads: 0 };
            for (var i = a; i <= b; i++) r.reads += p.values[i];
            r.expected = outside ? ((p.total - r.reads) * inside) / outside : 0;
            r.change = r.reads - r.expected;
            reads += r.reads;
            expected += r.expected;
            return r;
          });
          function percent(got, usual) {
            return usual ? signed((got / usual - 1) * 100) + "%" : "from 0";
          }

          function card(number, label) {
            return (
              '<div class="pid-stats-card"><div class="pid-stats-num">' + number +
              '</div><div class="pid-stats-label">' + label + "</div></div>"
            );
          }
          fill(
            mounts.summary,
            card(reads.toLocaleString(), "reads") +
              card(rows.filter(function (r) { return r.reads; }).length, "pages read") +
              card(inside, inside === 1 ? "day" : "days") +
              (outside
                ? card(percent(reads, expected), "reads per day, against the other " + outside + " days")
                : card("&ndash;", "no other days to compare with"))
          );

          function table(list) {
            return (
              '<table class="pid-stats-table"><thead><tr><th class="pid-stats-rank">#</th>' +
              '<th>Page</th><th class="pid-stats-trend">Daily reads</th>' +
              '<th class="pid-stats-count">Reads</th>' +
              (outside ? '<th class="pid-stats-count pid-stats-change">Change</th>' : "") +
              "</tr></thead><tbody>" +
              list
                .map(function (r, i) {
                  // Sphinx pagename to URL: an /index page is its directory.
                  var href = "/pid/" + r.page.name.replace(/\/index$/, "/");
                  return (
                    '<tr><td class="pid-stats-rank">' + (i + 1) + "</td>" +
                    // <wbr>: a long name wraps after a slash before it wraps inside a word.
                    '<td><a href="' + escapeHtml(href) + '">' +
                    escapeHtml(r.page.name).replace(/\//g, "/<wbr>") + "</a></td>" +
                    '<td class="pid-stats-trend">' + sparkSvg(n, rowBand + r.page.spark) + "</td>" +
                    '<td class="pid-stats-count">' + r.reads.toLocaleString() + "</td>" +
                    (outside
                      ? '<td class="pid-stats-count pid-stats-change">' + signed(r.change) +
                        " <small>" + percent(r.reads, r.expected) + "</small></td>"
                      : "") +
                    "</tr>"
                  );
                })
                .join("") +
              "</tbody></table>"
            );
          }

          var movers = rows
            .filter(function (r) { return Math.round(r.change); })
            .sort(function (x, y) { return Math.abs(y.change) - Math.abs(x.change); });
          fill(
            mounts.movers,
            !outside
              ? note("Narrow the window to see which pages changed against the other days.")
              : movers.length
                ? table(movers.slice(0, 10))
                : note("No page is more than half a read from what its other days predict.")
          );
          fill(
            mounts.top,
            table(rows.slice().sort(function (x, y) { return y.reads - x.reads; }).slice(0, 20))
          );
          // Pages level on reads in the window are ordered by their reads
          // on all the days, so a short window still lists the pages that
          // are read least in general.
          fill(
            mounts.bottom,
            table(
              rows
                .slice()
                .sort(function (x, y) { return x.reads - y.reads || x.page.total - y.page.total; })
                .slice(0, 10)
            )
          );
        }

        // The two thumbs may cross: the window is whatever lies between
        // them, so neither can block the other. Their values are written
        // only by a button, never during a drag.
        function selectBetweenEdges() {
          var x = +edges[0].value;
          var y = +edges[1].value;
          edges[0].setAttribute("aria-valuetext", formatDay(days[x]));
          edges[1].setAttribute("aria-valuetext", formatDay(days[y]));
          select(Math.min(x, y), Math.max(x, y));
        }
        function setEdges(a, b) {
          edges[0].value = a;
          edges[1].value = b;
          selectBetweenEdges();
        }
        edges[0].addEventListener("input", selectBetweenEdges);
        edges[1].addEventListener("input", selectBetweenEdges);
        [].forEach.call(buttons, function (btn) {
          btn.addEventListener("click", function () {
            setEdges(n - btn.getAttribute("data-days"), n - 1);
          });
        });
        onHover(daily.querySelector(".pid-stats-plot"), n, function (i) {
          cursor.style.display = i < 0 ? "none" : "";
          cursor.style.left = (i / (n - 1 || 1)) * 100 + "%";
          readout.textContent =
            i < 0 ? windowText : formatDay(days[i], true) + ": " + site[i].toLocaleString() + " reads";
        });
        setEdges(0, n - 1);
      })
      .catch(showEmpty);
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
