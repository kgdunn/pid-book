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

Summary
-------

.. raw:: html

   <div id="pid-stats-summary" class="pid-stats-summary">
     <p style="color:#777"><em>Loading…</em></p>
   </div>

Daily reads (last 90 days)
--------------------------

Total reads per day across the whole book. Each daily bucket
de-duplicates by IP, so two visits from the same reader on the same day
count once.

.. raw:: html

   <div id="pid-stats-daily" style="width:100%; height:280px"></div>

Most-read pages (last 90 days)
------------------------------

The 20 pages with the most reads over the 90-day window. Page names are
the Sphinx page identifiers (e.g. ``data-visualization/box-plots``);
click through to read them.

.. raw:: html

   <div id="pid-stats-top"></div>

Least-read pages (last 90 days)
-------------------------------

The 10 pages with the *fewest* reads over the 90-day window, lowest
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

   <div id="pid-stats-bottom"></div>

Raw data
--------

Every number on this page comes from a single public JSON file:
`learnche.org/_stats/sparklines.json <https://learnche.org/_stats/sparklines.json>`_.
The wider GoAccess dashboard
(`learnche.org/_stats/ <https://learnche.org/_stats/>`_) shows the same
pageviews plus referrers, devices, and country breakdowns.
