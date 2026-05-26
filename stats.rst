.. _stats:

Readership statistics
=====================

This page shows aggregated, anonymous readership for the HTML edition of
the book. The numbers come from the server access logs — so they include
readers who block JavaScript trackers — and are bucketed into daily
unique-IP counts per page. The IPs are discarded after aggregation; only
the daily counts survive. The same dataset feeds the small sparkline you
see in the sidebar of every page.

See :ref:`privacy` for what is and isn't collected.

.. note::

   The in-book figures show the most recent **10 days** while the
   pipeline is still bedding in. Two server-side fixes only took
   effect recently, so wider windows are not yet representative:

   * **Real client IPs since 2026-05-24** (Apache ``mod_remoteip`` +
     Cloudflare ``CF-Connecting-IP``). Earlier data deduplicated by
     Cloudflare edge IPs and undercounted by ~10–50×.
   * **Access logs retained 5 years since 2026-05-26** (logrotate
     ``rotate 1825``). Earlier rotations purged everything after 4
     days, so almost nothing from Feb 2022 to May 2026 exists on
     disk.

   The backend keeps a full 365-day window in
   `sparklines.json <https://learnche.org/_stats/sparklines.json>`_;
   the in-book display is filtered to a shorter window so a young
   deployment doesn't look unread. The window will gradually widen
   over the next few weeks.

Summary
-------

.. raw:: html

   <div id="pid-stats-summary" class="pid-stats-summary">
     <p style="color:#777"><em>Statistics could not load. Common reasons:
     Do Not Track is enabled in your browser, a content blocker is
     hiding <code>/_stats/sparklines.json</code>, or the nightly
     aggregator hasn't produced data yet. The numbers will appear when
     the data file is reachable.</em></p>
   </div>

Daily reads (last 10 days)
--------------------------

Total reads per day across the whole book. Each daily bucket
de-duplicates by IP, so two visits from the same reader on the same day
count once.

.. raw:: html

   <div id="pid-stats-daily" style="width:100%; height:280px; display:none"></div>

Most-read pages (last 10 days)
------------------------------

The 20 pages with the most reads over the 10-day window. Page names
are the Sphinx page identifiers (e.g. ``data-visualization/box-plots``);
click through to read them.

.. raw:: html

   <div id="pid-stats-top" style="display:none"></div>

Least-read pages (last 10 days)
-------------------------------

The 10 pages with the *fewest* reads over the 10-day window, lowest
first. Useful for spotting sections that may need clearer links,
better discoverability, or a refresh.

.. note::

   Pages with **zero** hits in the window do not appear in
   ``sparklines.json`` and therefore never reach this table. So this
   is "least-read pages that got at least one reader", not "unread
   pages". To find truly unread pages, diff the Sphinx page list
   against the JSON keys (see
   ``docs/telemetry/operations.md``).

.. raw:: html

   <div id="pid-stats-bottom" style="display:none"></div>

Raw data
--------

Every number on this page comes from a single public JSON file:
`learnche.org/_stats/sparklines.json <https://learnche.org/_stats/sparklines.json>`_.
The wider GoAccess dashboard
(`learnche.org/_stats/ <https://learnche.org/_stats/>`_) shows the same
pageviews plus referrers, devices, and country breakdowns.
