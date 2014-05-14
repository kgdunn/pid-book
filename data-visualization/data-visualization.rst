.. todo:: another scatter plot question
.. todo:: spectral data question
.. todo:: batch data question

.. todo:: add to slides: http://www.r-bloggers.com/one-liners-which-make-me-love-r-make-your-data-dance-hans-rosling-style-with-googlevis-rstats/

Data visualization in context
=============================

This is the first chapter in the book. Why?  Every engineer has heard the phrase "plot your data," but seldom are we shown what appropriate plots look like.

In this section we consider quantitative plots -- plots that show numbers. We cover various plots that will help you learn more from your data, and we end with a list of tips for effective data visualization.

Usage examples
==============
.. AU: I am taking "section" to mean, e.g., "1.2 Usage examples". In the following sentence and elsewhere, I change it to "chapter" if appropriate.

You can use the material in this chapter when you must learn more about your system from the data. For example, you may get these questions:

	* *Co-worker*: Here are the yields from a batch system for the last 3 years (1256 data points). Can you help me

		* understand more about the time trends in the data?
		* efficiently summarize the batch yields?

	* *Manager*:  How can we effectively summarize the (a) number and (b) types of defects on our 17 aluminium grades for the last 12 months?

	* *Yourself*: We have 24 different measurements against time (5 readings per minute, over an interval of 300 minutes) for each batch we produce. How can we visualize these 36,000 data points?


What we will cover
==================

.. figure:: ../figures/visualization/visualization-subject-mapping.png
	:alt:	../figures/visualization/visualization-subject-mapping.xmind
	:width: 750px
	:align: center
	:scale: 60

References and readings
=======================

.. index::
	pair: references and readings; visualization

#. Edward Tufte, *Envisioning Information*, Graphics Press, 1990. (10th printing in 2005)
#. Edward Tufte, *The Visual Display of Quantitative Information*, Graphics Press, 2001.
#. Edward Tufte, *Visual Explanations: Images and Quantities, Evidence and Narrative*, 2nd edition, Graphics Press, 1997.
.. AU: Do you have publication dates for the Few books?
#. Stephen Few, *Show Me the Numbers* and *Now You See It: Simple Visualization Techniques for Quantitative Analysis*; both from Analytics Press.
#. William Cleveland, *Visualizing Data*, 1st edition, Hobart Press, 1993.
#. William Cleveland, *The Elements of Graphing Data*, 2nd edition, Hobart Press, 1994.
#. Su, `It's Easy to Produce Chartjunk Using Microsoft Excel 2007 but Hard to Make Good Graphs <http://dx.doi.org/10.1016/j.csda.2008.03.007>`_, *Computational Statistics and Data Analysis*, **52**(10), 4594-4601, 2008.

.. _visualization_time_series:

Time-series plots
=================

We start off by considering a plot most often seen in engineering applications: the :index:`time-series plot <pair: time-series plots; visualization>`. The time-series plot is a univariate plot (shows only one variable). It is a 2-dimensional plot in which one axis, the time-axis, shows graduations at an appropriate scale (seconds, minutes, weeks, quarters, years), while the other axis shows the data. Usually, the time-axis is displayed horizontally, but this is not a requirement: some interesting analysis can be done with time running vertically. 

Many statistical packages call this a line plot, as it can be used generally to display any sort of sequence, whether it is along time or some other ordering. The time-series plot is an excellent way to visualize long sequences of data. It tells a visual story along the sequence axis, and the human brain is incredibly adept at absorbing this high density of data, locating patterns in the data such as sinusoids, spikes, and outliers, and separating noise from signal.

Here are some tips for effective time-series plots:

-	The software should have horizontal and vertical zooming ability. Once zoomed in, there must be tools to scroll up, down, left and right.

-	Always label the *x*-axis appropriately with (time) units that make sense. 

	.. _visualization-bad-labels:

	.. image:: ../figures/visualization/CPU-temperature_-_from_www_aw_org_on_26_Dec_2009.png
		:width: 750px
		:align: center
		:scale: 50

	This plot, found on the Internet, shows a computer's CPU temperature with time. There are several problems with the plot, but the key issue here is the *x*-axis. This plot is probably the result of poor default settings in the software, but as you will start to realize, bad defaults are very common in most software packages. They waste your time when you have to repeatedly modify the charts. Good software will sensibly label the time-based axis for you.
	
.. AU: The last sentence in the following paragraph seemed a little convoluted. Please verify edits.
-	When plotting more than one trajectory (a vector of values) against time, it is helpful if the lines do not cross or jumble too much. This allows you to clearly see the relationship with other variables. The use of a second *y*-axis on the right-hand side is helpful when plotting two trajectories, but when plotting three or more trajectories that are in the same numeric range, it is better to use several parallel axes as shown later.

	.. _visualization-cluttered-trajectories:

	.. image:: ../figures/visualization/3_correlated_variables_-_badly_displayed_in_Numbers.png
		:width: 750px

.. AU: The term "here" is ambiguous. In the following paragraph, is "here" referring to the figures above and below?
	As shown in the previous figure, even using differently coloured lines and/or markers may work in selected instances, but this still leads to a clutter of lines and markers. The following chart shows this principle, created with the default settings from Apple iWork's *Numbers* (2009).

	Using different markers, improving the axis labelling, tightening up the axis ranges, and thinning out the ink improves the chart slightly. This took about 3 minutes extra in the software, because I had not used the software before and had to find the settings.

	.. figure:: ../figures/visualization/3_correlated_variables_-_slightly_better.png
		:width: 750px

	This final example with parallel axes is greatly improved, but took about 10 minutes to assemble and would likely take a similar amount of time to format in MATLAB, Excel, Python or other packages. The results are clearer to interpret: variables "Type A" and "Type B" move up and down together, while variable "Type C" moves in the opposite direction. Note how the *y*-axis for "Type C" is rescaled to start from its minimum value, rather than a value of zero. You should always use "tight" limits on the *y*-axis.

	.. _visualization-cleaned-trajectories:

	.. image:: ../figures/visualization/3_correlated_variables_-_better.png
		:width: 750px

-	Using the same data as in the previous tip, a much improved visualization technique is to use sparklines to represent the sequence of data.

		.. _visualization-sparkline-trajectories:

		.. figure:: ../figures/visualization/3-correlated-variables-as-sparklines.png
			:scale: 30

	Sparklines are small graphics that carry a high density of information. The human eye is easily capable of absorbing about 250 dots (points) per linear inch and 650 points per square inch. These :index:`sparklines` convey the same amount of information as the previous plots and are easy to consume on hand-held devices such as iPhones, cellphones and tablet computing devices that are common in chemical plants and other engineering facilities. Read more about them from `this hyperlink <http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0001OR>`_.

-	When plotting money values over time (e.g. sales of polymer composite over the past 10 years), adjust for inflation effects by dividing by the consumer price index or an appropriate factor. Distortions due to the time value of money can be very misleading, as this `example of car sales shows <http://www.duke.edu/~rnau/411infla.htm>`_.  A `Canadian inflation calculator <http://www.bankofcanada.ca/rates/related/inflation-calculator>`_ is available from the Bank of Canada.

-	If you ever ask yourself, "Why are we being shown so little?" then you must request more data before and after the time period or current sequence shown. A typical example is stock-price data (see :ref:`example figure of Apple's stock <visualization-apple-stock>`). There are numerous graphical "lies" in magazines and reports where the plot shows a drastic change in trend, but in the context of prior data, that trend is a small aberration. Again, this brings into play the brain's remarkable power to discern signal from noise, but to do this, our brains require context.

	.. _visualization-apple-stock:

	.. image:: ../figures/visualization/AAPL-stock-prices.png
		:width: 750px
		:scale: 80
		:align: center

Bar plots
=========

The :index:`bar plot <pair: bar plot; visualization>` is another univariate plot on a two-dimensional axis. The axes are not called *x*- or *y*-axes. Instead, one axis is called the *category axis*, while the other, the *value axis*, shows the value of each bar.

.. image:: ../figures/visualization/barplot-example-expenses.png
   :scale: 60

Here is some advice for bar plots:

-	Use a bar plot when there are many categories and interpretation of the plot does not differ if the category axis is reshuffled. (It might be easier to interpret the plot with a particular ordering; however, the interpretation won't be different with a different ordering.)

-	A time-series plot is more appropriate than a bar plot when there is a time-based ordering to the categories, because usually you want to imply some sort of trend with time-ordered data.

	.. image:: ../figures/visualization/quarterly-profit-barplot-vs-lineplot.png
		:alt:	../figures/visualization/quarterly-profit-barplot.R
		:width: 750px
		:align: center
		:scale: 100

-	Bar plots can be wasteful as each data point is repeated several times:

	#. Left edge (line) of each bar
	#. Right edge (line) of each bar
	#. The height of the colour in the bar
	#. The number's position (up and down along the *y*-axis)
    #. The top edge of each bar, just below the number
	#. The number itself

        .. note::

	    Maximize the data-ink ratio within reason.

	.. math::

		\text{Maximize data-ink ratio} &= \frac{\text{total ink for data}}{\text{total ink for graphics}}     \\
		                              &= 1 - \text{proportion of ink that can be erased without loss of data information}

-	Use a table for a handful of data points rather than a bar plot.

    .. image:: ../figures/visualization/profit-by-region.png
		:alt:	../figures/visualization/profit-by-region.numbers
		:width: 750px
		:align: center
		:scale: 100

-	Don't use cross-hatching, textures or unusual shading in the plots. This creates distracting visual vibrations.

	.. image:: ../figures/visualization/hatched-barplot.png
		:alt:	../figures/visualization/hatched-barplot.R
		:width: 600px
		:align: center
		:scale: 45

.. COMMENTS
  Stack bar plots are OK, they show breakdowns quite nicely, even though one has to read the accompanying text carefully to make sure the break down is what you think it is. Never underestimate the audience's intelligence.
  - My preference is to avoid stacked bar plots. I'm never sure, until I read the text carefully, or the plot annotations, whether the bars represent a cumulative amount or an incremental amount. Is the blue region showing 25% or 15%?

-	Use horizontal bars if

	- there is some ordering to the categories (it is often easier to read these from top-to-bottom), or
	- the labels do not fit side-by-side: don't make the reader have to rotate the page to interpret the plot; rotate the plot for the reader.

-	You can place the labels inside the bars.

-	You should start the noncategory axis at zero: the bar's area shows the magnitude. Starting bars at a nonzero value distorts the meaning.

..
  Exception to starting at zero: todo Few, p 189 (ranges)


Box plots
==========

:index:`Box plots <pair: box plot; visualization>` are an efficient summary of one variable (univariate chart), but can also be used effectively to compare like variables that are in the same units of measurement.

The box plot shows the so-called *five-number summary* of a univariate data series: 

1. Minimum sample value
2. 25th `percentile <http://en.wikipedia.org/wiki/Percentile>`_ (1st `quartile <http://en.wikipedia.org/wiki/Quartile>`_)
3. 50th percentile (median)
4. 75th percentile (3rd quartile)
5. Maximum sample value

The 25th percentile is the value below which 25% of the observations in the sample are found. The distance from the 3rd to the 1st quartile is also known as the interquartile range (IQR) and represents the data's spread, similar to the standard deviation.

The following data are thickness measurements of 2-by-6 boards, taken at six locations around the edge. Here is a sample of the measurements and a summary of the first 100 boards (created in ``R``):

.. code-block:: text

	    Pos1 Pos2 Pos3 Pos4 Pos5 Pos6
	1   1761 1739 1758 1677 1684 1692
	2   1801 1688 1753 1741 1692 1675
	3   1697 1682 1663 1671 1685 1651
	4   1679 1712 1672 1703 1683 1674
	5   1699 1688 1699 1678 1688 1705
        ....
	96  1717 1708 1645 1690 1568 1688
	97  1661 1660 1668 1691 1678 1692
	98  1706 1665 1696 1671 1631 1640
	99  1689 1678 1677 1788 1720 1735
	100 1751 1736 1752 1692 1670 1671

  > summary(boards[1:100, 2:7])
         Pos1           Pos2           Pos3           Pos4           Pos5           Pos6
    Min.  :1524   Min.  :1603   Min.  :1594   Min.  :1452   Min.  :1568   Min.  :1503
    1st Qu.:1671   1st Qu.:1657   1st Qu.:1654   1st Qu.:1667   1st Qu.:1662   1st Qu.:1652
    Median :1680   Median :1674   Median :1672   Median :1678   Median :1673   Median :1671
    Mean   :1687   Mean   :1677   Mean   :1677   Mean   :1679   Mean   :1674   Mean   :1672
    3rd Qu.:1705   3rd Qu.:1688   3rd Qu.:1696   3rd Qu.:1693   3rd Qu.:1685   3rd Qu.:1695
    Max.  :1822   Max.  :1762   Max.  :1763   Max.  :1788   Max.  :1741   Max.  :1765


.. _visualization_boxplot_example:

The following box plot is a graphical summary of these numbers.

.. image:: ../figures/visualization/boxplot-for-two-by-six-100-boards.png
	:align: left
	:width: 700px
	:scale: 55

Some variations for the box plot are possible:

- Use the mean instead of the median.
- Show outliers as dots, where an outlier is most commonly defined as any point 1.5 IQR distance units above and below the median (the upper and lower hinges).
- Use the 2% and 95% percentiles rather than the upper and lower hinge values.

.. _visualization_scatter_plots:

Relational graphs: scatter plots
================================
	
This is a plot many people are comfortable using. It helps you understand the relationship between two variables - a bivariate plot - as opposed to the previous charts that are univariate. A :index:`scatter plot <pair: scatter plot; visualization>` is a collection of points shown inside a box formed by two axes at 90 degrees to each other. The marker's position is located at the intersection of the values shown on the horizontal (*x*) axis and vertical (*y*) axis.

The unspoken intention of a scatter plot is usually to ask the reader to draw a causal relationship between the two variables. However, not all scatter plots actually show causal phenomena.

.. image:: ../figures/visualization/scatterplot-figures.png
	:width: 750px
	:scale: 80

Strive for graphical excellence by doing the following:

- Make each axis as tight as possible.
- Avoid heavy grid lines.
- Use the least amount of ink.
- Do not distort the axes.

There is an unfounded fear that others won't understand your 2D scatter plot. Tufte (*Visual Display of Quantitative Information*, p 83) shows that there are no scatter plots in a sample (1974 to 1980) of U.S., German and British dailies, despite studies showing that 12-year-olds can interpret such plots. (Japanese newspapers frequently use them.)

You will see this in industrial settings as well. The next time you go into the control room, try finding any scatter plots. The audience is not to blame: it is the producers of these charts who assume the audience is incapable of interpreting them.

.. note::

	Assume that if you can understand the plot, so will your audience.


Further improvements can be made to your scatter plots. For example, extend the frames only as far as your data:

	.. image:: ../figures/visualization/scatterplot-figures-with-regression-lines.png
		:width: 750px
		:scale: 75

You can add box plots and histograms to the side of the axes to aide interpretation:

	.. image:: ../figures/visualization/scatterplot-with-histograms-updated.png
		:width: 750px
		:scale: 42

Add a third variable to the plot by adjusting the marker size, and add a fourth variable with the use of colour:

    .. _reference_to_use_of_colour:

	.. image:: ../figures/visualization/scatterplot-with-2-extra-dimensions.png
		:scale: 80


    This example, from `http://gapminder.org <http://graphs.gapminder.org/world/#$majorMode=chart$is;shi=t;ly=2003;lb=f;il=t;fs=11;al=30;stl=t;st=t;nsl=t;se=t$wst;tts=C$ts;sp=6;ti=2007$zpv;v=0$inc_x;mmid=XCOORDS;iid=phAwcNAVuyj1jiMAkmq1iMg;by=ind$inc_y;mmid=YCOORDS;iid=phAwcNAVuyj0TAlJeCEzcGQ;by=ind$inc_s;uniValue=30;iid=phAwcNAVuyj0XOoBL_n5tAQ;by=ind$inc_c;uniValue=255;gid=CATID0;iid=phAwcNAVuyj2tPLxKvvnNPA;by=ind$map_x;scale=log;dataMin=194;dataMax=96846$map_y;scale=log;dataMin=0.855;dataMax=8.7$map_s;sma=49;smi=1.85$map_c;scale=lin$cd;bd=0$inds=>`_, shows data as of 2007 for income per person against fertility. The size of each data point is proportional to the country's population, and the marker colour shows life expectancy at birth (years). The GapMinder website allows you to "play" the graph over time, effectively adding a fifth dimension to the 2D plot. Use the hyperlink above to see how richer countries move towards lower fertility and higher income over time.

Tables 
======

.. index::
   pair: data table; visualization
   see: table; data table

The data table is an efficient format for comparative data analysis on categorical objects. Usually, the items being compared are placed in a column, while the categorical objects are in the rows.  The quantitative value is then placed at the intersection of the row and column, called the *cell*. The following examples demonstrate data tables.

This table compares monthly payments for buying or leasing various cars (categories). The first two columns are being compared; the other columns contain additional, secondary information.

	.. figure:: ../figures/visualization/table-car-payments.png
		:alt:	../figures/visualization/table-examples.numbers
		:align: center
		:scale: 75

The next table compares defect types (number of defects) for different product grades (categories).

	.. figure:: ../figures/visualization/table-defect-counts.png
		:alt:	../figures/visualization/table-examples.numbers
		:align: center
		:scale: 50

	This particular table raises more questions:

	-	Which defects cost us the most money?
	-	Which defects occur most frequently?  The table does not contain any information about production rate. For example, if there were 1850 lots of grade A4636 (first row) produced, then defect A occurs at a rate of 37/1850 = 1/50. And if 250 lots of grade A2610 (last row) were produced, then, again, defect A occurs at a rate of 1/50. Redrawing the table on a production-rate basis would be useful if we are making changes to the process and want to target the most problematic defect.
	
.. AU: These last two bullets aren't questions, so I turned them into paragraphs.
	If we are comparing a type of defect over different grades, then we are now comparing down the table, instead of across the table. In this case, the fraction of defects for each grade would be a more useful quantity to display.
	
	If we are comparing defects within a grade, then we are comparing across the table. Here again, the fraction of each defect type, weighted according to the cost of that defect, would be more appropriate.


Three common pitfalls to avoid:

#.	Using pie charts when tables will do

	Pie charts are tempting when we want to graphically break down a quantity into components. I have used them erroneously myself (here is an example on a website that I helped with: http://www.macc.mcmaster.ca/gradstudies.php). We won't go into details here, but I strongly suggest you read the convincing evidence of Stephen Few in: `"Save the pies for dessert" <http://www.perceptualedge.com/articles/08-21-07.pdf>`_. The key problem is that the human eye cannot adequately decode angles; however, we have no problem with linear data.

#.	Arbitrary ordering along the first column; usually, alphabetically or in time order

	Listing the car types alphabetically is trivial: instead, list them by some other third criterion of interest, perhaps minimum down payment required, typical lease duration, or total amount of interest paid on the loan. That way you get some extra context to the table for free.

#.	Using excessive grid lines

	Tabular data should avoid vertical grid lines, except when the columns are so close that mistakes will be made. The human eye will use the visual white space between the numbers to create its own columns.

	.. image:: ../figures/visualization/table-grid-comparison.png
		:scale: 65

To wrap up this section is a demonstration of tabular data in a different format, based on an idea of Tufte in *The Visual Display of Quantitative Information*, p. 158. Here we compare the corrosion resistance and roughness of a steel surface for two different types of coatings, A and B. 

A layout that you expect to see in a standard engineering report:

	+----------+-----------+-----------+-----------+-----------+
	| Product  | Corrosion | resistance| Surface   |roughness  |
	+----------+-----------+-----------+-----------+-----------+
	|          | Coating A |Coating B  | Coating A | Coating B |
	+==========+===========+===========+===========+===========+
	| K135     | 0.30      | 0.22      | 30        |   42      |
	+----------+-----------+-----------+-----------+-----------+
	| K136     | 0.45      | 0.39      | 86        |   31      |
	+----------+-----------+-----------+-----------+-----------+
	| P271     | 0.22      | 0.24      | 24        |   73      |
	+----------+-----------+-----------+-----------+-----------+
	| P275     | 0.40      | 0.44      | 74        |   52      |
	+----------+-----------+-----------+-----------+-----------+
	| S561     | 0.56      | 0.36      | 70        |   75      |
	+----------+-----------+-----------+-----------+-----------+
	| S567     | 0.76      | 0.51      | 63        |   70      |
	+----------+-----------+-----------+-----------+-----------+

And the layout advocated by Tufte:

	.. image:: ../figures/visualization/tables-recast-as-plots-both.png
	   :width: 750px
	   :scale: 75

Note how the slopes carry the information about the effect of changing the coating type. The rearranged row ordering shows the changes as well. This idea is effective for two treatments but could be extended to three or four treatments by adding extra "columns."

Topics of aesthetics and style
==============================

We won't cover these topics, but Tufte's books contain remarkable examples that discuss effective use of colour for good contrast, varying line widths, and graph layout (e.g. use more horizontal than vertical - an aspect ratio of about 1.4 to 2.0; and flow the graphics into the location in the text where discussed).

Data frames (axes)
===================

Frames are the basic containers that surround the data and give context to our numbers. Here are some tips:

#.	Use round numbers.
#.	Generally, tighten the axes as much as possible, except ...
#.	When showing comparison plots, all axes must have the same minima and maxima.

.. TODO: give an example of a bad visualization here that has unequal axes for comparison


Colour
======

:index:`Colour <pair: colour; visualization>` is very effective in all graphical charts. However, you must bear in mind that your readers might be colour-blind, or the document might be read from a grayscale printout. 

Note also that a standard colour progression does *not* exist. We often see dark blues and purples representing low numbers and reds the higher numbers, with greens, yellows and orange in-between. Also, there are several such colour schemes - there isn't a universal standard. The only safest colour progression is the grayscale axis, ranging from black to white at each extreme: this satisfies both colour-blind readers and users of your grayscale printed output.

See the :ref:`section on scatter plots <reference_to_use_of_colour>` for an example of the effective use of colour.

General summary: revealing complex data graphically
======================================================

There is no generic advice that applies in every instance. These tips are useful, though, in most cases:

-	If the question you want answered is causality, then show causality (the most effective way is with bivariate scatter plots). If trying to answer a question with alternatives, show comparisons (with tiles of plots or a simple table).

-	Words and graphics belong together. Add labels to plots for outliers, and explain interesting points. Add equations and even small summary tables on top of your plots. Remember that a graph should be like a paragraph of text, not necessarily just a graphical display of numbers that you discuss later on.

-	Avoid obscure coding on the graph. Don't label points as "A", "B", "C", .... and then put a legend: "A: grade TK133", "B: grade RT231", "C: grade TK134". Just put the labels directly on the plot.

-	Do not assume your audience is ignorant and won't understand a complex plot. Conversely, don't try to enliven a plot with decorations and unnecessary graphics (flip through a copy of almost any weekly news magazine for examples of this sort of embellishment). As Tufte mentions more than once in his books, "*If the statistics are boring, then you've got the wrong numbers.*". The graph should stand on its own.

-	When the graphics involve money and time, make sure you adjust the money for inflation.

-	Maximize the data-ink ratio = (ink for data) / (total ink for graphics). Maximizing this ratio, within reason, means you should (a) eliminate nondata ink and (b) erase redundant data-ink.

-	Maximize data density. Humans can interpret data displays of 250 data points per linear inch and 625 data points per square inch.
