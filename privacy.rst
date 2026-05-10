.. _privacy:

Privacy
=======

This site collects the bare minimum needed to know which sections are read
and which searches are useful — no more.

What is collected
-----------------

* **Aggregate pageviews** via `GoatCounter <https://www.goatcounter.com>`_,
  loaded as a small cookieless script on every HTML page. No cookies are set,
  no IP address is stored, no third-party trackers are loaded, and no
  cross-site identifiers exist.
* **In-book search queries** — what you type into the sidebar search box —
  are sent the same way. Queries are debounced, queries longer than 80
  characters are dropped, and anything that looks like an email address is
  dropped client-side before sending.
* **Server access logs**, processed locally with
  `GoAccess <https://goaccess.io>`_. IPs are anonymised and only daily
  aggregates are kept; raw logs rotate within 30 days.

The resulting aggregates — top pages, the 90-day per-page sparklines you see
in the sidebar, search queries, and an overview report — are **public** at
`learnche.org/_stats/ <https://learnche.org/_stats/>`_, in keeping with the
open spirit of this CC BY-SA 4.0 book.

Opt out
-------

The pixel honours your browser's *Do Not Track* setting: enable DNT and no
event of any kind is sent. Self-hosted copies of this book do not phone
home — the script short-circuits on ``localhost``, ``127.0.0.1``, and
``file://`` URLs.

Questions or concerns: please open an issue at
https://github.com/kgdunn/pid-book/issues.
