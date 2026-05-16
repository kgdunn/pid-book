.. This is the root document for the PDF theme-comparison harness.
.. It is NOT part of the book: the normal html / text / epub builds exclude
.. it (see conf.py, the PID_PDF_THEME block). It is rendered only when the
.. LaTeX build is run with the PID_PDF_THEME environment variable set, in
.. which case it carves off a small sample — this preface plus the
.. process-monitoring chapter — so alternative PDF themes can be compared
.. without recompiling the whole book.
..
.. Build it with, e.g.:   make theme-pdf THEME=academic
..
.. Cross-references from the monitoring chapter into chapters that are not
.. part of the sample cannot resolve and render as plain text. That is
.. expected: this is a layout preview, not a navigable book.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Process Improvement Using Data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. toctree::
   :hidden:

   preface/index


.. toctree::
   :titlesonly:
   :numbered:
   :maxdepth: 3
   :caption: Table of Contents

   process-monitoring/index
