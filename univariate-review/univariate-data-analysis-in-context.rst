.. To add

	* see p 295 of Devore here for in-class example
	* Put "paired" tests under the main section of testing for differences
	* Explain more clearly when a paired test is required vs a test of differences
	* Chi-squared goodness of fit test for normality; also a way to introduce the chi-squared test

Univariate data analysis in context
====================================

This section gives a starting idea to the general area of data analysis. We cover concepts from univariate data analysis shown in the pictorial outline below. This section is only a *review of these concepts* for one single variable. If you have more than one variable, you can repeat the analysis for each one. Later, in the :ref:`multivariate chapter <SECTION_latent_variable_modelling>`, we learn how to extract information from multiple variables at the same time.

Some introductory statistics textbooks, for more detailed background, are recommend further down.

Usage examples
~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=-wPc24FT-2Y&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=4

.. index::
	pair: usage examples; univariate data

The material in this section is used whenever you want to learn more about a single variable in your data set. For example:

	- *Co-worker*: Here are the final output values, on a scale from 0 to 100%, from a batch system for the last 3 years (1256 data points).

		- What sort of distribution do the data have?
		- Yesterday our output value was less than 50%, what are the chances of that happening under typical conditions?

	- *Yourself*: We have historical failure rate data for certain equipment in our factories. What is the probability that 3 of the same type of equipment will fail this year?

	- *Manager*: We have 2 duplicate reactors. Does reactor 1 have better final product purity, on average, than reactor 2?

	- *Colleague*: What does the 95% confidence interval for the density of our powder ingredient really mean?



What we will cover
~~~~~~~~~~~~~~~~~~~~

.. image:: ../figures/mindmaps/univariate-section-mapping.png
  :align: center
  :scale: 92

.. Concepts
.. ========
..
.. Concepts that you must be familiar with by the end of this section:
..
.. .. tabularcolumns:: LLL
..
.. .. csv-table::
..    :widths: 10, 10, 10
..
.. 	, independence, outliers
.. 	"frequency histogram", probability, variation
.. 	"cumulative distribution", median, MAD
.. 	population, sample, error
.. 	"Central limit theorem", parameter, statistic
.. 	"confidence interval", outlier, "paired test"

References and readings
=======================

.. index::
	pair: references and readings; univariate data

Any standard statistics text book will cover the topics from this part of the book in much greater depth than these notes. Some that you might refer to:

#. **Recommended**: Box, Hunter and Hunter, *Statistics for Experimenters*, Chapter 2.
#. Hodges and Lehmann, *Basic Concepts of Probability and Statistics*.
#. Hogg and Ledolter, *Engineering Statistics*.
#. Montgomery and Runger, *Applied Statistics and Probability for Engineers*.
