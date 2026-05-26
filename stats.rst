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

   Two unrelated server-side issues distort the historical portion of
   the year-long window. The post-fix data (roughly **2026-05-22
   onward**) is accurate; everything before that has caveats:

   * **Real client IPs only since 2026-05-24.** Until then every
     reader behind Cloudflare appeared as one of a handful of edge
     IPs per region per day, and the script's daily-unique-IP
     deduplication collapsed real reader counts ~10–50×. The visible
     step-up in late May 2026 is a measurement artefact, not real
     growth. (Fixed by configuring Apache ``mod_remoteip`` to honour
     the ``CF-Connecting-IP`` header.)
   * **No access logs from Feb 2022 to May 2026.** Debian's default
     Apache ``logrotate`` configuration kept only 4 days of history.
     For ~4 years that quietly purged the access logs the next day,
     so we have nothing to aggregate for that period. (Fixed by
     bumping the ``rotate`` count to 1825.)

   The 2021/2022 archive *does* exist in the log directory but falls
   outside the 365-day window so doesn't appear here. Bumping the
   window to 5 years would surface it as a "valley" of empty days
   between two dense regions.

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

Daily reads (last 365 days)
---------------------------

Total reads per day across the whole book. Each daily bucket
de-duplicates by IP, so two visits from the same reader on the same day
count once.

.. raw:: html

   <div id="pid-stats-daily" style="width:100%; height:280px; display:none"></div>

Most-read pages (last 365 days)
-------------------------------

The 20 pages with the most reads over the 365-day window. Page names
are the Sphinx page identifiers (e.g. ``data-visualization/box-plots``);
click through to read them.

.. raw:: html

   <div id="pid-stats-top" style="display:none"></div>

Least-read pages (last 365 days)
--------------------------------

The 10 pages with the *fewest* reads over the 365-day window, lowest
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
