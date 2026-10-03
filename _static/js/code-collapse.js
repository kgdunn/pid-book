/*
 * Convenience on top of the collapsed code blocks.
 *
 * The collapsing itself is not done here. Every code block is written by
 * `my-extensions/code_collapse.py` as a native <details> that starts closed,
 * so with JavaScript off the page still reads as prose and every block still
 * opens on click or on Enter. That is the mechanism; this file only adds what
 * a browser cannot infer:
 *
 *   - the page-level switch that opens or closes every block at once, whose
 *     markup comes from _templates/pid-code-switch.html already in the page
 *     and is revealed here;
 *   - a memory of which the reader preferred, so someone who wants the code
 *     asks once rather than on every page;
 *   - re-anchoring to the URL fragment after a bulk open, because opening the
 *     blocks above the target moves it down the page;
 *   - opening every block before printing, and closing them again after. The
 *     print stylesheet reveals the code on its own in current browsers; this
 *     is what reaches the older ones;
 *   - the page's reading time, which is quoted without the code and moves to
 *     the with-code figure while every block is open. Both numbers are put in
 *     the markup by my-extensions/reading_time.py.
 *
 * Nothing is sent anywhere. The preference is a single key in localStorage,
 * read and written inside try/catch because a private window can refuse both.
 */
(function () {
  "use strict";

  // Namespaced by site rather than by page, because learnche.org serves more
  // than /pid from this one origin, and versioned, so a later change in what
  // the value means cannot misread an old one.
  var KEY = "pid:code-blocks:v1";
  var EXPANDED = "expanded";
  var COLLAPSED = "collapsed";
  var OPEN_LABEL = "Show all code";
  var CLOSE_LABEL = "Hide all code";

  // Stands in for storage when storage is unavailable, so the switch still
  // works for the current page even though the choice is not kept.
  var remembered = null;

  function storage() {
    try {
      // The property access itself throws, not only getItem and setItem, in
      // Safari with website data blocked and in some embedded contexts.
      return window.localStorage;
    } catch (e) {
      return null;
    }
  }

  /* "expanded", "collapsed", or null when this reader has never chosen.
     Three states, not a boolean: a boolean cannot tell a first visit from a
     reader who chose to keep the code closed, so changing the default later
     would silently flip the second group. */
  function readPreference() {
    var store = storage();
    if (!store) {
      return remembered;
    }
    var value;
    try {
      value = store.getItem(KEY);
    } catch (e) {
      return remembered;
    }
    return value === EXPANDED || value === COLLAPSED ? value : null;
  }

  function writePreference(value) {
    remembered = value;
    var store = storage();
    if (!store) {
      return;
    }
    try {
      store.setItem(KEY, value);
    } catch (e) {
      /* quota, or a private window: this page still works, it is just not kept */
    }
  }

  function blocks() {
    return Array.prototype.slice.call(document.querySelectorAll("details.pid-code"));
  }

  // "All open" is the reading of the switch that matches what a reader sees: a
  // reader who opened two of nine blocks by hand has not asked for the page.
  function allOpen(items) {
    return items.every(function (item) {
      return item.open;
    });
  }

  /* Closing a block stops its subtree being rendered, so focus inside it (a
     copy button, a link) is discarded and a keyboard reader is returned to the
     top of the document. Move focus to the bar of the block that is closing. */
  function rescueFocus(items) {
    var active = document.activeElement;
    if (!active || active === document.body) {
      return;
    }
    for (var i = 0; i < items.length; i += 1) {
      if (items[i] !== active && items[i].contains(active)) {
        var bar = items[i].querySelector("summary.pid-code__bar");
        if (bar) {
          bar.focus();
        }
        return;
      }
    }
  }

  function setAll(items, open) {
    if (!open) {
      rescueFocus(items);
    }
    items.forEach(function (item) {
      item.open = open;
    });
  }

  /* A reader who followed a :ref: link arrives with the browser already
     scrolled to the fragment. Opening the blocks above the target pushes it
     thousands of pixels down the page, so put it back in view. */
  function reanchor() {
    if (!window.location.hash || window.location.hash.length < 2) {
      return;
    }
    var id;
    try {
      id = decodeURIComponent(window.location.hash.slice(1));
    } catch (e) {
      return; // a malformed fragment is not worth acting on
    }
    var target = document.getElementById(id) || document.getElementsByName(id)[0];
    if (target) {
      target.scrollIntoView();
    }
  }

  function updateReadingTime(isAllOpen) {
    // The header quotes the page without its code, since the blocks arrive
    // closed. Once they are all open the page really is the longer read.
    var badge = document.querySelector(".pid-reading-time");
    if (!badge) {
      return;
    }
    var value = badge.querySelector(".pid-reading-time__value");
    var minutes = badge.getAttribute(isAllOpen ? "data-minutes-with-code" : "data-minutes");
    if (value && minutes) {
      value.textContent = minutes + " min";
    }
  }

  function wireSwitch(items, wrap) {
    var button = wrap.querySelector(".pid-code-switch");
    var status = wrap.querySelector(".pid-code-status");
    if (!button) {
      return;
    }

    /* The label changes and nothing else does. Swapping the label and setting
       aria-pressed are the two correct designs for a toggle and they are
       mutually exclusive: together they announce the state twice, and
       contradictorily ("Hide all code, pressed"). */
    function paint() {
      var open = allOpen(items);
      button.textContent = open ? CLOSE_LABEL : OPEN_LABEL;
      updateReadingTime(open);
    }

    button.addEventListener("click", function () {
      var open = !allOpen(items);
      setAll(items, open);
      writePreference(open ? EXPANDED : COLLAPSED);
      paint();
      if (open) {
        reanchor();
      }
      if (status) {
        // Every block on the page changed with no focus move and nothing said,
        // which is what SC 4.1.3 asks to be announced. The count is the part
        // the button's own label does not carry.
        status.textContent =
          "All " + items.length + (open ? " code blocks shown." : " code blocks hidden.");
      }
    });

    // A block opened or closed on its own bar changes what the switch should
    // say, so listen for that rather than letting the two drift apart.
    items.forEach(function (item) {
      item.addEventListener("toggle", paint);
    });

    paint();
    wrap.hidden = false;
  }

  function wirePrinting(items) {
    var before = null;

    function open() {
      before = items.map(function (item) {
        return item.open;
      });
      items.forEach(function (item) {
        item.open = true;
      });
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
      return; // no code on this page: the switch stays hidden
    }

    // A return visit from a reader who asked for the code. A first visit, and a
    // reader who asked to keep the code closed, both write nothing and leave
    // the blocks as the build wrote them.
    if (readPreference() === EXPANDED) {
      setAll(items, true);
      reanchor();
    }

    var wrap = document.querySelector(".pid-code-switch-wrap");
    if (wrap) {
      wireSwitch(items, wrap);
    }
    wirePrinting(items);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
