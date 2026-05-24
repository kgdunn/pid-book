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

Raw data
--------

Every number on this page comes from a single public JSON file:
`learnche.org/_stats/sparklines.json <https://learnche.org/_stats/sparklines.json>`_.
The wider GoAccess dashboard
(`learnche.org/_stats/ <https://learnche.org/_stats/>`_) shows the same
pageviews plus referrers, devices, and country breakdowns.
