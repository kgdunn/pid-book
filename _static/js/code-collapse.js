/*
 * Convenience on top of the collapsed code blocks.
 *
 * The collapsing itself is not done here. Every code block is written by
 * `my-extensions/code_collapse.py` as a native <details> that starts closed,
 * so with JavaScript off the page still reads as prose and every block still
 * opens on click or on Enter. That is the mechanism; this file only adds what
 * a browser cannot infer:
 *
 *   - a page-level switch that opens or closes every block at once;
 *   - a memory of which the reader preferred, so someone who wants the code
 *     asks once rather than on every page;
 *   - opening every block before printing, and closing them again after, so a
 *     printed page or a saved PDF carries the code in full;
 *   - the page's reading time, which is quoted without the code and moves to
 *     the with-code figure while every block is open. Both numbers are put in
 *     the markup by my-extensions/reading_time.py.
 *
 * Nothing is sent anywhere. The preference is a single key in localStorage,
 * read and written inside try/catch because a private window can refuse both.
 */
(function () {
  "use strict";

  var KEY = "pid.code.expanded";
  var OPEN_LABEL = "Show all code";
  var CLOSE_LABEL = "Hide all code";

  function readPreference() {
    try {
      return window.localStorage.getItem(KEY) === "1";
    } catch (e) {
      return false; // private mode, or storage blocked: the built-in default
    }
  }

  function writePreference(expanded) {
    try {
      window.localStorage.setItem(KEY, expanded ? "1" : "0");
    } catch (e) {
      /* the switch still works for this page; it just will not be remembered */
    }
  }

  function blocks() {
    return Array.prototype.slice.call(document.querySelectorAll("details.pid-code"));
  }

  function setAll(items, open) {
    items.forEach(function (item) {
      item.open = open;
    });
  }

  function updateReadingTime(allOpen) {
    // The header quotes the page without its code, since the blocks arrive
    // closed. Once they are all open the page really is the longer read.
    var badge = document.querySelector(".pid-reading-time");
    if (!badge) {
      return;
    }
    var value = badge.querySelector(".pid-reading-time__value");
    var minutes = badge.getAttribute(allOpen ? "data-minutes-with-code" : "data-minutes");
    if (value && minutes) {
      value.textContent = minutes + " min";
    }
  }

  function makeSwitch(items) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "pid-code-switch";

    function paint() {
      // "All open" is the honest reading of the switch: a reader who opened
      // two of nine blocks by hand has not asked for the page.
      var allOpen = items.every(function (item) {
        return item.open;
      });
      button.textContent = allOpen ? CLOSE_LABEL : OPEN_LABEL;
      button.setAttribute("aria-pressed", allOpen ? "true" : "false");
      updateReadingTime(allOpen);
    }

    button.addEventListener("click", function () {
      var allOpen = items.every(function (item) {
        return item.open;
      });
      setAll(items, !allOpen);
      writePreference(!allOpen);
      paint();
    });

    // A block opened or closed on its own bar changes what the switch should
    // say, so listen for that rather than letting the two drift apart.
    items.forEach(function (item) {
      item.addEventListener("toggle", paint);
    });

    paint();
    return button;
  }

  function insertSwitch(button) {
    var article = document.querySelector("article.bd-article") || document.querySelector("article");
    if (!article) {
      return;
    }
    // Below the page's title, where it is in the same place on every page,
    // rather than beside the first block, which can be a long way down. The
    // theme nests the <h1> inside a <section>, so insert next to the heading
    // itself rather than assuming it is a child of the article.
    var heading = article.querySelector("h1");
    if (heading) {
      heading.insertAdjacentElement("afterend", button);
    } else {
      article.insertBefore(button, article.firstChild);
    }
  }

  function wirePrinting(items) {
    var before = null;

    function open() {
      before = items.map(function (item) {
        return item.open;
      });
      setAll(items, true);
    }

    function restore() {
      if (!before) {
        return;
      }
      items.forEach(function (item, index) {
        item.open = before[index];
      });
      before = null;
    }

    if (typeof window.addEventListener === "function") {
      window.addEventListener("beforeprint", open);
      window.addEventListener("afterprint", restore);
    }
    // Safari has historically fired neither; it fires the media query instead.
    if (window.matchMedia) {
      var printing = window.matchMedia("print");
      var onChange = function (event) {
        return event.matches ? open() : restore();
      };
      if (printing.addEventListener) {
        printing.addEventListener("change", onChange);
      } else if (printing.addListener) {
        printing.addListener(onChange);
      }
    }
  }

  function start() {
    var items = blocks();
    if (!items.length) {
      return;
    }
    if (readPreference()) {
      setAll(items, true);
    }
    insertSwitch(makeSwitch(items));
    wirePrinting(items);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
