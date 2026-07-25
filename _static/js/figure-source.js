/*
 * Show which script drew a figure.
 *
 * Long-press a figure (or Alt-click it, for a mouse) and a small panel
 * appears with the path of the generator in the figures repository, and a
 * link to it when one is configured.
 *
 * The mapping comes from `_static/figure-sources.json`, written during the
 * HTML build by `my-extensions/figure_source.py`. That single request is
 * to this same site: nothing here calls a third party, sets a cookie, or
 * records anything. The file is fetched lazily, on the first long-press of
 * a page, so a reader who never asks pays nothing for it.
 */
(function () {
  "use strict";

  var PRESS_MILLISECONDS = 550;
  var manifest = null;
  var manifestPromise = null;
  var panel = null;

  function staticRoot() {
    // Sphinx exposes the depth of the current page; DOCUMENTATION_OPTIONS
    // is defined on every page of this theme.
    var root = "";
    if (window.DOCUMENTATION_OPTIONS && window.DOCUMENTATION_OPTIONS.URL_ROOT) {
      root = window.DOCUMENTATION_OPTIONS.URL_ROOT;
    }
    return root + "_static/figure-sources.json";
  }

  function loadManifest() {
    if (manifestPromise) {
      return manifestPromise;
    }
    manifestPromise = fetch(staticRoot(), { credentials: "same-origin" })
      .then(function (response) {
        return response.ok ? response.json() : null;
      })
      .then(function (payload) {
        manifest = payload || { base: "", sources: {} };
        return manifest;
      })
      .catch(function () {
        manifest = { base: "", sources: {} };
        return manifest;
      });
    return manifestPromise;
  }

  function basename(url) {
    var path = String(url).split("?")[0].split("#")[0];
    return path.substring(path.lastIndexOf("/") + 1);
  }

  function closePanel() {
    if (panel && panel.parentNode) {
      panel.parentNode.removeChild(panel);
    }
    panel = null;
  }

  function showPanel(image, script, base) {
    closePanel();
    panel = document.createElement("div");
    panel.className = "figure-source-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Source code for this figure");

    var label = document.createElement("span");
    label.className = "figure-source-label";
    label.textContent = "Drawn by";
    panel.appendChild(label);

    var target;
    if (base) {
      target = document.createElement("a");
      target.href = base + script;
      target.rel = "noopener";
      target.target = "_blank";
    } else {
      target = document.createElement("span");
    }
    target.className = "figure-source-path";
    target.textContent = script;
    panel.appendChild(target);

    var dismiss = document.createElement("button");
    dismiss.type = "button";
    dismiss.className = "figure-source-close";
    dismiss.setAttribute("aria-label", "Close");
    dismiss.textContent = "×";
    dismiss.addEventListener("click", closePanel);
    panel.appendChild(dismiss);

    var host = image.closest("figure") || image.parentNode;
    host.appendChild(panel);
  }

  function reveal(image) {
    loadManifest().then(function (data) {
      var script =
        image.getAttribute("data-figure-source") ||
        (data.sources || {})[basename(image.getAttribute("src"))];
      if (script) {
        showPanel(image, script, data.base || "");
      }
    });
  }

  function attach(image) {
    var timer = null;

    function start() {
      timer = window.setTimeout(function () {
        timer = null;
        reveal(image);
      }, PRESS_MILLISECONDS);
    }

    function cancel() {
      if (timer !== null) {
        window.clearTimeout(timer);
        timer = null;
      }
    }

    image.addEventListener("pointerdown", start);
    image.addEventListener("pointerup", cancel);
    image.addEventListener("pointerleave", cancel);
    image.addEventListener("pointercancel", cancel);
    // A keyboard and mouse route to the same thing.
    image.addEventListener("click", function (event) {
      if (event.altKey) {
        event.preventDefault();
        cancel();
        reveal(image);
      }
    });
  }

  function init() {
    var images = document.querySelectorAll("main img, article img, div.body img");
    Array.prototype.forEach.call(images, attach);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closePanel();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
