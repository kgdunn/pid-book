.. _stats:

Readership statistics
=====================

This page shows aggregated, anonymous readership for the HTML edition of
the book. The numbers come from the server access logs, so they include
readers who block JavaScript trackers, and are bucketed into daily
unique-IP counts per page. The IPs are discarded after aggregation; only
the daily counts survive. The same dataset feeds the small sparkline you
see in the sidebar of every page.

See :ref:`privacy` for what is and isn't collected.

Only the pages of the current edition of the book are counted. The data
also records addresses that are not pages, such as a mistyped link, and
pages that have since been removed. Those are left out of every figure
on this page.

.. note::

   All the figures count **complete days only**. The nightly
   aggregator runs in the small hours, so the current day is still
   being logged when it runs; publishing it would put a partial count
   at the right-hand edge of every chart. The most recent day shown is
   therefore yesterday.

Daily reads, and the window of days to look at
----------------------------------------------

Total reads per day across the whole book, for the last 180 days. Each
daily bucket de-duplicates by IP, so two visits from the same reader on
the same day count once.

Drag the two handles on the horizontal axis, or use the buttons, to
select a window of days. The window is shaded in the chart, and the
summary and the three tables below the chart describe that window.

.. raw:: html

   <div id="pid-stats-daily">
     <p style="color:#777"><em>Statistics could not load. Common reasons:
     Do Not Track is enabled in your browser, a content blocker is
     hiding <code>/_stats/sparklines.json</code>, or the nightly
     aggregator hasn't produced data yet. The numbers will appear when
     the data file is reachable.</em></p>
   </div>

Summary of the window
---------------------

.. raw:: html

   <div id="pid-stats-summary" class="pid-stats-summary" style="display:none"></div>

Pages that changed most in the window
-------------------------------------

When the reads in the window are higher or lower than on the other days,
this table shows which pages account for the difference.

For each page, the reads in the window are compared with the reads that
the page would have had there at the daily rate it had on the other days
of the 180. The *change* is the difference between the two, in reads and
as a percentage. The changes of all the pages add up to the change for
the whole book, so the table lists the 10 pages that contribute most to
it, in either direction.

A rise that is spread over the whole book gives every page about the
same percentage. A page whose percentage is far from that of the other
pages has a cause of its own, such as a new link to it from another
site.

.. raw:: html

   <div id="pid-stats-movers" style="display:none"></div>

Most-read pages in the window
-----------------------------

The 20 pages with the most reads in the window. Page names are the
Sphinx page identifiers (e.g. ``data-visualization/box-plots``); click
through to read them. The small chart in each row is that page's daily
reads over the 180 days, with the window shaded.

.. raw:: html

   <div id="pid-stats-top" style="display:none"></div>

Least-read pages in the window
------------------------------

The 10 pages with the *fewest* reads in the window, lowest first. Pages
with the same number of reads in the window are ordered by their reads
over the 180 days. Useful for spotting sections that may need clearer
links, better discoverability, or a refresh.

.. note::

   Pages with **zero** hits in the 180 days do not appear in
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
