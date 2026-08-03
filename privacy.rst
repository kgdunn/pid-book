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
  `GoAccess <https://goaccess.io>`_. IPs are anonymised in the published
  reports, and the per-page counts are daily unique-IP totals from which the
  IPs are discarded after aggregation. The raw logs themselves are rotated by
  the webserver and retained for up to 5 years, so that the readership
  history survives; they are never published, and nothing derived from them
  identifies a reader.

The resulting aggregates (top pages, the 60-day per-page sparklines you see
in the sidebar, search queries, and an overview report) are **public** at
`learnche.org/_stats/ <https://learnche.org/_stats/>`_, in keeping with the
open spirit of this CC BY-SA 4.0 book. The same numbers are also surfaced
inside the book itself on the :ref:`stats` page, and as the 60-day reader
count next to the sparkline in the sidebar of every page. Every figure covers
complete days only, so the most recent day shown is yesterday.

Opt out
-------

The pixel honours your browser's *Do Not Track* setting: enable DNT and no
event of any kind is sent. Self-hosted copies of this book do not phone
home — the script short-circuits on ``localhost``, ``127.0.0.1``, and
``file://`` URLs.

Questions or concerns: please open an issue at
https://github.com/kgdunn/pid-book/issues.
