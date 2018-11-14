Other types of monitoring charts
================================

You may encounter other charts in practice:

	*	The *S chart* is for monitoring the subgroup's standard deviation. Take the group of :math:`n` samples and show their standard deviation on a Shewhart-type chart. The limits for the chart are calculated using similar correction factors as were used in the derivation for the :math:`\overline{x}` Shewhart chart. This chart has a LCL :math:`\geq 0`.
	
	*	The *R chart* was a precursor for the *S chart*, where the *R* stands for range, the subgroup's maximum minus minimum. It was used when charting was done manually, as standard deviations were tedious to calculate by hand.
	
	*	The *np chart* and *p chart* are used when monitoring the proportion of defective items using a pass/fail criterion. In the former case the sample size taken is constant, while in the latter the proportion of defective items is monitored. These charts are derived using the binomial distribution.

	*	The *exponentially weight moving variance* (EWMV) chart is an excellent chart for monitoring for an increase in product variability. Like the :math:`\lambda` from an EWMA chart, the EWMV also has a sliding parameter that can balance current information and historical information to trade-off sensitivity. More information is available in the paper by J.F. MacGregor, and T.J. Harris, "`The Exponentially Weighted Moving Variance <https://learnche.org/literature/item/178/the-exponentially-weighted-moving-variance>`_", *Journal of Quality Technology*, **25**, p 106-118, 1993.


