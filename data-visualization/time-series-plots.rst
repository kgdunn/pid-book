.. _visualization_time_series:

Time-series plots
=================

.. youtube:: https://www.youtube.com/watch?v=aU6eZuiG8ck&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=0

We start off by considering a plot most often seen in engineering applications: the :index:`time-series plot <pair: time-series plots; visualization>`. The time-series plot is a univariate plot (shows only one variable). It is a 2-dimensional plot in which one axis, the time-axis, shows graduations at an appropriate scale (seconds, minutes, weeks, quarters, years), while the other axis shows the data. Usually, the time-axis is displayed horizontally, but this is not a requirement: some interesting analysis can be done with time running vertically. 

Many statistical packages call this a line plot, as it can be used generally to display any sort of sequence, whether it is along time or some other ordering. The time-series plot is an excellent way to visualize long sequences of data. It tells a visual story along the sequence axis, and the human brain is incredibly adept at absorbing this high density of data, locating patterns in the data such as sinusoids, spikes, and outliers, and separating noise from signal.

Here are some tips for effective time-series plots:

-	The software should have horizontal and vertical zooming ability. Once zoomed in, there must be tools to scroll up, down, left and right.

-	Always label the *x*-axis appropriately with (time) units that make sense. 

	.. _visualization-bad-labels:

	.. image:: ../figures/visualization/CPU-temperature_-_from_www_aw_org_on_26_Dec_2009.png
		:align: left
		:width: 800px
		:scale: 70 %

	This plot, found on the Internet, shows a computer's CPU temperature with time. There are several problems with the plot, but the key issue here is the *x*-axis. This plot is probably the result of poor default settings in the software, but as you will start to realize, bad defaults are very common in most software packages. They waste your time when you have to repeatedly modify the charts. Good software will sensibly label the time-based axis for you.
	
.. AU: The last sentence in the following paragraph seemed a little convoluted. Please verify edits.

-	When plotting more than one trajectory (a vector of values) against time, it is helpful if the lines do not cross or jumble too much. This allows you to clearly see the relationship with other variables. The use of a second *y*-axis on the right-hand side is helpful when plotting two trajectories, but when plotting three or more trajectories that are in the same numeric range, it is better to use several parallel axes as shown later.

	.. _visualization-cluttered-trajectories:

	.. image:: ../figures/visualization/3_correlated_variables_-_badly_displayed_in_Numbers.png

.. AU: The term "here" is ambiguous. In the following paragraph, is "here" referring to the figures above and below?

	As shown in the previous figure, even using differently coloured lines and/or markers may work in selected instances, but this still leads to a clutter of lines and markers. The following chart shows this principle, created with the default settings from Apple iWork's *Numbers* (2009).

	Using different markers, improving the axis labelling, tightening up the axis ranges, and thinning out the ink improves the chart slightly. This took about 3 minutes extra in the software, because I had not used the software before and had to find the settings.

	.. figure:: ../figures/visualization/3_correlated_variables_-_slightly_better.png

	This final example with parallel axes is greatly improved, but took about 10 minutes to assemble and would likely take a similar amount of time to format in MATLAB, Excel, Python or other packages. The results are clearer to interpret: variables "Type A" and "Type B" move up and down together, while variable "Type C" moves in the opposite direction. Note how the *y*-axis for "Type C" is rescaled to start from its minimum value, rather than a value of zero. You should always use "tight" limits on the *y*-axis.

	.. _visualization-cleaned-trajectories:

	.. image:: ../figures/visualization/3_correlated_variables_-_better.png

-	Using the same data as in the previous tip, a much improved visualization technique is to use sparklines to represent the sequence of data.

	.. _visualization-sparkline-trajectories:

	.. figure:: ../figures/visualization/3-correlated-variables-as-sparklines.png
		:width: 400px
		:scale: 50 %
		:align: right

	Sparklines are small graphics that carry a high density of information. The human eye is easily capable of absorbing about 250 dots (points) per linear inch and 60,000 points per square inch. These :index:`sparklines` convey the same amount of information as the previous plots and are easy to consume on hand-held devices such as iPhones, cellphones and tablet computing devices that are common in chemical plants and other engineering facilities. Read more about them from `this hyperlink <http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0001OR>`_.
	
-	When plotting money values over time (e.g. sales of polymer composite over the past 10 years), adjust for inflation effects by dividing by the consumer price index or an appropriate factor. Distortions due to the time value of money can be very misleading, as this `example of car sales shows <http://people.duke.edu/~rnau/411infla.htm>`_.  A `Canadian inflation calculator <http://www.bankofcanada.ca/rates/related/inflation-calculator>`_ is available from the Bank of Canada.

-	If you ever ask yourself, "Why are we being shown so little?" then you must request more data before and after the time period or current sequence shown. A typical example is stock-price data (see :ref:`example figure of Apple's stock <visualization-apple-stock>`). There are numerous graphical "lies" in magazines and reports where the plot shows a drastic change in trend, but in the context of prior data, that trend is a small aberration. Again, this brings into play the brain's remarkable power to discern signal from noise, but to do this, our brains require context.

	.. _visualization-apple-stock:

	.. image:: ../figures/visualization/AAPL-stock-prices.png
		:scale: 70%
		:width: 900px
		:align: center
		:alt: fake width
