/*
 * Show which script drew a figure.
 *
 * Long-press a figure, or Alt-click it, and a small panel names the script
 * in the figures repository that produced it.
 *
 * This script is an convenience, not the mechanism. The link itself lives in
 * the markup, as `data-figure-source` on the <img>, written during the
 * build by `my-extensions/figure_source.py`. So:
 *
 *   - with JavaScript off, the page is exactly as it would otherwise be, and
 *     the link is still in the HTML for anyone who looks;
 *   - offline, or from a file:// copy, this works the same as online: there
 *     is no request to make, here or anywhere;
 *   - nothing is stored, sent or recorded.
 *
 * It also stays out of the way. The press has to be still: any movement
 * cancels it, so scrolling a page of figures never raises a panel. The
 * native long-press menu is not suppressed, the panel is positioned over the
 * figure rather than inserted into the text, so nothing reflows, and it
 * closes on the next scroll, tap, or Escape.
 */
(function () {
  "use strict";

  var PRESS_MILLISECONDS = 600;
  var MOVE_TOLERANCE_PIXELS = 10;
  var panel = null;

  function closePanel() {
    if (panel && panel.parentNode) {
      panel.parentNode.removeChild(panel);
    }
    panel = null;
  }

  function sourceFor(image) {
    return image.getAttribute("data-figure-source");
  }

  function linkBase() {
    // Set by the build; absent means show the path with nothing to click.
    return (window.__PID_FIGURE_SOURCE && window.__PID_FIGURE_SOURCE.base) || "";
  }

  function showPanel(image, script) {
    closePanel();

    panel = document.createElement("div");
    panel.className = "figure-source-panel";
    panel.setAttribute("role", "note");

    var label = document.createElement("span");
    label.className = "figure-source-label";
    label.textContent = "Drawn by";
    panel.appendChild(label);

    var base = linkBase();
    var target = document.createElement(base ? "a" : "span");
    if (base) {
      target.href = base + script;
      target.rel = "noopener";
      target.target = "_blank";
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

    // Anchored to the figure and taken out of the flow, so revealing it
    // never moves the text the reader is looking at.
    var host = image.closest("figure") || image.parentNode;
    if (host && window.getComputedStyle(host).position === "static") {
      host.style.position = "relative";
    }
    (host || document.body).appendChild(panel);
  }

  function attach(image) {
    var timer = null;
    var origin = null;

    function cancel() {
      if (timer !== null) {
        window.clearTimeout(timer);
        timer = null;
      }
      origin = null;
    }

    image.addEventListener("pointerdown", function (event) {
      if (!sourceFor(image) || event.button !== 0) {
        return;
      }
      origin = { x: event.clientX, y: event.clientY };
      timer = window.setTimeout(function () {
        timer = null;
        showPanel(image, sourceFor(image));
      }, PRESS_MILLISECONDS);
    });

    image.addEventListener("pointermove", function (event) {
      // A press that drifts is a scroll or a drag, not a request.
      if (!origin) {
        return;
      }
      var moved =
        Math.abs(event.clientX - origin.x) + Math.abs(event.clientY - origin.y);
      if (moved > MOVE_TOLERANCE_PIXELS) {
        cancel();
      }
    });

    ["pointerup", "pointerleave", "pointercancel", "contextmenu"].forEach(
      function (name) {
        image.addEventListener(name, cancel);
      }
    );

    image.addEventListener("click", function (event) {
      if (event.altKey && sourceFor(image)) {
        event.preventDefault();
        cancel();
        showPanel(image, sourceFor(image));
      }
    });
  }

  function init() {
    var images = document.querySelectorAll("img[data-figure-source]");
    Array.prototype.forEach.call(images, attach);

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closePanel();
      }
    });
    window.addEventListener("scroll", closePanel, { passive: true });
    document.addEventListener("pointerdown", function (event) {
      if (panel && !panel.contains(event.target)) {
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
