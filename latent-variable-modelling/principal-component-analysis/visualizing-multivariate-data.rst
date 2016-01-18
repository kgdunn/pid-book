Visualizing multivariate data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The data, collected in a matrix |X|, contains rows that represent an *object* of some sort. We usually call each row an *observation*. The observations in |X| could be a collection of measurements from a chemical process at a particular point in time, various properties of a final product, or properties from a sample of raw material. The columns in |X| are the values recorded for each observation. We call these the *variables*. 

Which variables should you use, and how many observations do you require? We address this issue later. For now though we consider that you have your data organized in this manner:

.. figure:: ../../figures/data-types/X-matrix.png
	:alt:	../../figures/data-types/X-matrix.svg
	:align: center
	:scale: 35
	:width: 900px

Consider the case of 2 variables, :math:`K=2` (left) and :math:`K=3` variables (right) for the room thermometers example :ref:`from earlier <LVM_room_temperature_example>`:

.. figure:: ../../figures/examples/room-temperature/temperature-2d-and-3d-plot.png
	:alt:	../../figures/examples/room-temperature/temperature-data-combine.py
	:scale: 100
	:width: 900px
	:align: center

Each point in the plot represents one *object*, also called an *observation*. There are about 150 observations in each plot here. We sometimes call these plots *data swarms*, but they are really just ordinary scatterplots that we saw in the :ref:`visualization section <SECTION-data-visualization>`. Notice how the variables are correlated with each other, there is a definite trend. If we want to explain this trend, we could draw a line through the cloud swarm that *best explains* the data.  This line now represents our best summary and estimate of what the data points are describing. If we wanted to describe that relationship to our colleagues we could just give them the equation of the best-fit line.

.. raw:: latex

	\par

.. _LVM_visualization_scatterplot_matrix:

Another effective way to visualize small multivariate data sets is to use a scatterplot matrix. Below is an example for :math:`K = 5` measurements on :math:`N=50` observations. Scatterplot matrices require :math:`K(K-1)/2` plots and can be enhanced with univariate histograms (on the diagonal plots), and linear regressions and loess smoothers on the off-diagonals to indicate the level of correlation between any two variables.

.. image:: ../../figures/examples/food-texture/pca-on-food-texture-scatterplot-matrix.png
	:alt:	../../figures/examples/food-texture/pca-on-food-texture-data.R
	:scale: 100
	:width: 900px
	:align: center

