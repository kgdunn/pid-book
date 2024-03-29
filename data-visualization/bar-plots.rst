Bar plots
=========

.. youtube:: https://www.youtube.com/watch?v=tb20hIQlEBU&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=2

The :index:`bar plot <pair: bar plot; visualization>` is another univariate plot on a two-dimensional axis. The two axes are not called *x*- or *y*-axes. Instead, one axis is called the *category axis* showing the category name, while the other, the *value axis*, shows the numeric value of that category, given by the length of the bar.

.. image:: ../figures/visualization/barplot-example-expenses.png
   :scale: 60

Here is some advice for bar plots:

-	Use a bar plot when there are many categories and interpretation of the plot does not differ if the category axis is reshuffled. (It might be easier to interpret the plot with a particular ordering; however, the interpretation won't be different with a different ordering of the categories.)

-	A time-series plot is more appropriate than a bar plot when there is a time-based ordering to the categories, because usually you want to imply some sort of trend with time-ordered data. Therefore do not use a bar plot for time trends, rather use a time-series plot.

	.. figure:: ../figures/visualization/quarterly-profit-barplot-vs-lineplot.png
		:alt:	../figures/visualization/quarterly-profit-barplot.R
		:align: center

	Use this R code to draw the figures:

	.. dcl:: R
		:codefile: data-visualization/gists/quarterly-profit-barplots.R

	or this Python code:

	.. dcl:: python
		:codefile: data-visualization/gists/quarterly-profit-barplots.py

-	Bar plots can be wasteful as each data point is repeated several times:

	#. Left edge (line) of each bar
	#. Right edge (line) of each bar
	#. The height of the colour in the bar
	#. The number's position (up and down along the *y*-axis)
	#. The top edge of each bar, just below the number
	#. The number itself

	To this end, Tufte defines the data ink ratio as:

	.. math::

		\text{Data-ink ratio} &= \frac{\text{total ink for data}}{\text{total ink for graphics}}     \\
		&= 1 - \text{proportion of ink that can be erased without loss of data information}

	The heuristic is to maximize this ratio as far as possible by using the ink (pixels) for only the data.

-	Rather use a table than a bar plot for a handful of data points.

    .. image:: ../figures/visualization/profit-by-region.png
		:alt:	../figures/visualization/profit-by-region.numbers
		:align: center
		:scale: 100

-	Don't use cross-hatching, textures or unusual shading in the plots. This creates distracting visual vibrations.

	.. image:: ../figures/visualization/hatched-barplot.png
		:alt:	../figures/visualization/hatched-barplot.R
		:align: center
		:scale: 35
		:width: 900px

.. FAKE WIDTH in the above image

.. COMMENTS
  Stack bar plots are OK, they show breakdowns quite nicely, even though one has to read the accompanying text carefully to make sure the break down is what you think it is. Never underestimate the audience's intelligence.
  - My preference is to avoid stacked bar plots. I'm never sure, until I read the text carefully, or the plot annotations, whether the bars represent a cumulative amount or an incremental amount. Is the blue region showing 25% or 15%?

-	Use horizontal bars if

	- there is some ordering to the categories (it is often easier to read the category labels from top-to-bottom), or
	- if the labels do not fit side-by-side: don't make the reader have to rotate the page to interpret the plot; rotate the plot for the reader.

-	You can place the labels inside the bars.

-	You should start the noncategory axis at zero: the bar's area shows the magnitude. Starting bars at a nonzero value distorts the meaning.

..
  Exception to starting at zero: todo Few, p 189 (ranges)
