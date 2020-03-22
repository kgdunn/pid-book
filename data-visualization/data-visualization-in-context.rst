.. todo:: another scatter plot question
.. todo:: spectral data question
.. todo:: batch data question
.. todo:: add to slides: http://www.r-bloggers.com/one-liners-which-make-me-love-r-make-your-data-dance-hans-rosling-style-with-googlevis-rstats/

Data visualization in context
=============================

This is the first chapter in the book. Why? Many of you have heard the phrase "plot your data," but seldom are we shown what appropriate plots look like.

In this section we consider quantitative plots -- plots that show numbers. We cover various plots that will help you gain more insight from your data. We end with a list of tips for effective data visualization.

.. rubric:: Usage examples

.. AU: I am taking "section" to mean, e.g., "1.2 Usage examples". In the following sentence and elsewhere, I change it to "chapter" if appropriate.

You can use the material in this chapter when you must learn more about your system from the data. For example, you may get these questions:

	* *Co-worker*: Here are the yields (final output value) from a given system for the last 3 years (1256 data points). Can you help me:

		* effectively communicate what the time trends are in the data?
		* summarize the yield values?

	* *Manager*:  How can we effectively summarize the (a) number and (b) types of defects on our 17 products for the last 12 months?

	* *Yourself*: We produce products in a batchwise manner. For each batch we have 25 different sensors that we record a value for at a rate of 5 readings per minute, over a total interval of 300 minutes. How can we visualize these :math:`25 \times 5 \times 300 = 37500` data points?

.. rubric:: What we will cover

.. figure:: /figures/visualization/visualization-subject-mapping.png
	:alt:	../figures/visualization/visualization-subject-mapping.xmind
	:align: center
	:scale: 60

.. _visualization_references:

References and readings
========================

.. index::
	pair: references and readings; visualization

.. AU: Do you have publication dates for the Few books?

#. Edward Tufte, *Envisioning Information*, Graphics Press, 1990. (10th printing in 2005)
#. Edward Tufte, *The Visual Display of Quantitative Information*, Graphics Press, 2001.
#. Edward Tufte, *Visual Explanations: Images and Quantities, Evidence and Narrative*, 2nd edition, Graphics Press, 1997.
#. Stephen Few, *Show Me the Numbers* and *Now You See It: Simple Visualization Techniques for Quantitative Analysis*; both from Analytics Press.
#. William Cleveland, *Visualizing Data*, 1st edition, Hobart Press, 1993.
#. William Cleveland, *The Elements of Graphing Data*, 2nd edition, Hobart Press, 1994.
#. Su, `It's Easy to Produce Chartjunk Using Microsoft Excel 2007 but Hard to Make Good Graphs <https://dx.doi.org/10.1016/j.csda.2008.03.007>`_, *Computational Statistics and Data Analysis*, **52** (10), 4594-4601, 2008.
