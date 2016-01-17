Other types of confidence intervals
====================================

There are several other confidence intervals that you might come across in your career. We merely mention them here and don't cover their derivation. What is important is that you understand *how* to interpret a confidence interval.  Hopefully the previous discussion achieved that.

.. _univariate_CI_variance:

Confidence interval for the variance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: confidence interval; for variance

This confidence interval finds a region in which the normal distribution's variance parameter, :math:`\sigma`, lies. The range is obviously positive, since variance is a positive quantity. For reference, this range is:

.. math::
	\left[\frac{(n-1)S^2}{\chi^2_{n-1, \alpha/2}} \quad\text{to}\quad \frac{(n-1)S^2}{\chi^2_{n-1, 1-\alpha/2}} \right]

-	:math:`n` is the number of samples
-	:math:`S^2` is the sample variance
-	:math:`\chi^2_{n-1, \alpha/2}` are values from the :math:`\chi^2` distribution with :math:`n-1` and :math:`\alpha/2` degrees of freedom 
-	:math:`1-\alpha`: is the level of confidence, usually 95%, so :math:`\alpha = 0.05` in that case.

.. todo: give some R code still

.. _univariate_pooled_variance:

Confidence interval for the ratio of two variances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: pooled variances
	
.. index:: 
	single: confidence interval; ratio of variances

One way to test whether we can pool (combine) two variances, taken from two different normal distributions, is to construct the ratio: :math:`\dfrac{s^2_1}{s^2_2}`. We can construct a confidence interval, and if this interval contains the value of 1.0, then we have no evidence to presume they are different (i.e. we can assume the two population variances are similar).

.. math::	
	:nowrap:
	
	\begin{alignat*}{4}
		  F_{\alpha/2, \nu_1, \nu_2}\dfrac{s_2^2}{s_1^2} &\qquad<\qquad& \dfrac{\sigma_2^2}{\sigma_1^2} &\qquad<\qquad& F_{1-\alpha/2, \nu_1, \nu_2}\dfrac{s_2^2}{s_1^2}
	\end{alignat*}

where we use :math:`F_{\alpha/2, \nu_1, \nu_2}` to mean the point along the cumulative :math:`F`-distribution which has area of :math:`\alpha/2` using :math:`\nu_1` degrees of freedom for estimating :math:`s_1` and :math:`\nu_2` degrees of freedom for estimating :math:`s_2`. For example, in R, the value of :math:`F_{0.05/2, 10, 20}` can be found from ``qf(0.025, 10, 20)`` as 0.2925. The point along the cumulative :math:`F`-distribution which has area of :math:`1-\alpha/2` is denoted as :math:`F_{1-\alpha/2, \nu_1, \nu_2}`,  and :math:`\alpha` is the level of confidence, usually :math:`\alpha = 0.05` to denote a 95% confidence level.

.. Source: Devore, Probability and Statistics, 5th edition, p.392-395

Confidence interval for proportions: the binomial proportion confidence interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: confidence interval; for proportions

Sometimes we measure the proportion of successes (passes). For example, if we take a sample of :math:`n` independent items from our production line, and with an inspection system we can judge pass or failure. The proportion of passes is what is important, and we wish to construct a confidence region for the population *proportion*. This allows one to say the population proportion of passes lies between the given range. As in *the proportion of packaged pizzas with 20 or more pepperoni slices is between 86 and 92\%*.

Incidentally, it is this confidence interval that is used in polls to judge the proportion of people that prefer a political party. One can run this confidence interval backwards and ask: how many independent people do I need to poll to achieve a population proportion that lies within a range of :math:`\pm 2\%`, 19 times out of 20?  The answer actually is function of the poll result!  But the worst case scenario is a split-poll, and that requires 2400 respondents.

.. Hypothesis tests; test of significance
	=======================================

	A confidence interval gives an engineer a sense of the precision of a parameter from a distribution. The engineer can then use their judgement to determine if that confidence interval is important to them or not. For example, knowing that your plastic product has a melting point of 455K to 495K, with 95% probability, can be used by your customer, e.g. 3M, to judge whether that product is suitable in their extruders. 

	A hypothesis test, or test of significance as it is also known, is use to make a statement, and then verify that statement. For example, 3M could say, we tried 8 samples of your plastic, and the average melting point for the 8 samples was 500K. Is that normal?  You product specification says your melting point is in the range 455K to 495K, with 95% probability. 

	 455K to 495K. So then you go perform a hypothesis test to verify if 500K is reasonable. Your hypothesis is that 500K is not unusual. The alternative hypothesis is that 500K is unusual.

	  What is the significance level?  How do you get to a test statistic?
	  You must present strong evidence to 

	reject that statement (hypothesis), otherwise it is accepted; sometimes we are prone to say this with a double-negative: "*there is no evidence to show that the melting point is not 472K*". 

	Hypothesis tests always work in this way:

		#. Specify your *null hypothesis*, a statement of what you want to test: the melting point is 472K. The null hypothesis will be accepted as long as there is no evidence to show otherwise.
		#. Specify an alternative hypothesis, which will be accepted if you do have evidence to reject (disprove) the null hypothesis. The alternative hypothesis is not always the opposite of the null hypothesis, though it may be. We'll see some examples shortly.
		#. Specify a level of significance, a low probability number that indicates the threshold between a significant and insignificant difference, e.g. :math:`p = 0.05`. This number represents the strength of evidence we require
		#. Then construct a test statistic, which is a function of the sampled data that ....
		#. And define a rejection region, which is a region for the test statistic's values that will result in you rejecting the null hypothesis.
	
		.. todo:: how does this level change our answer as it varies?

