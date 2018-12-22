Box plots
==========

.. youtube:: https://www.youtube.com/watch?v=LumUy2F_DRc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=2

:index:`Box plots <pair: box plot; visualization>` are an efficient summary of one variable (univariate chart), but can also be used effectively to compare like variables that are in the same units of measurement.

The box plot shows the so-called *five-number summary* of a univariate data series: 

1. Minimum sample value
2. 25th `percentile <https://en.wikipedia.org/wiki/Percentile>`_ (1st `quartile <https://en.wikipedia.org/wiki/Quartile>`_)
3. 50th percentile (median)
4. 75th percentile (3rd quartile)
5. Maximum sample value

The 25th percentile is the value below which 25% of the observations in the sample are found. The distance from the 3rd to the 1st quartile is also known as the interquartile range (IQR) and represents the data's spread, similar to the standard deviation.

The following data are thickness measurements of 2-by-6 boards, taken at six locations around the edge. Here is a sample of the measurements and a summary of the first 100 boards (created in ``R``):

.. dcl:: R

	all.boards <- read.csv('http://openmv.net/file/six-point-board-thickness.csv')
	boards <- all.boards[1:100, 2:7]
	
	# Look at the start and end of the data 
	# Examine and summarize your data before
	# doing anything else
	head(boards)
	tail(boards)
	
	summary(boards)
	
	boxplot(boards)	


.. _visualization_boxplot_example:

The following box plot is a graphical summary of these numbers.

.. image:: ../figures/visualization/boxplot-for-two-by-six-100-boards.png
	:align: right
	:scale: 40
	:width: 900px
	:alt: fake width

Some variations for the box plot are possible:

- Show outliers as dots, where an outlier is most commonly defined as any point 1.5 IQR distance units away from the box. The box's upper bound is at the 25th percentile, and the boxes lower bound is at the 75th percentile.
- The whiskers on the plots are drawn *at most* 1.5 IQR distance units away from the box, however, if the whisker is to be drawn beyond the bound of the data vector, then it is redrawn at the edge of the data instead (i.e. it is clamped, to avoid it exceeding).
- Use the mean instead of the median [*not too common*].
- Use the 2% and 98% percentiles rather than the upper and lower hinge values.
