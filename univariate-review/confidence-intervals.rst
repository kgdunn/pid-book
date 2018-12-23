.. _univariate_confidence_intervals:

Confidence intervals
====================

.. See code in yield-exercise.R for the R source code

.. index:: confidence interval

So far we have calculated point estimates of parameters, called statistics. In the last section in the :math:`t`-distribution we already calculated a confidence interval. In this section we formalize the idea, starting with an example.

*Example*: a new customer is evaluating your product, they would like a confidence interval for the impurity level in your sulphuric acid. You can tell them: "*the range from 429ppm to 673ppm contains the true impurity level with 95% confidence*". This is a compact representation of the impurity level. You could have told your potential customer that

	- the sample mean from the last year of data is 551 ppm
	- the sample standard deviation from the last year of data is 102 ppm
	- the last year of data are normally distributed

But a confidence interval conveys a similar concept, in a useful manner. It gives an estimate of the location and spread and uncertainty associated with that parameter (e.g. impurity level in this case).

Let's return to the previous viscosity example, where we had the 9 viscosity measurements ``23, 19, 17, 18, 24, 26, 21, 14, 18``. The sample average was :math:`\overline{x} = 20.0` and the standard deviation was :math:`s = 3.81`. The :math:`z`-value is: :math:`z = \dfrac{\overline{x} - \mu}{s/\sqrt{n}}`. And we showed this was distributed according to the :math:`t`-distribution with 8 degrees of freedom. 

Calculating a confidence interval requires we find a range within which that :math:`z`-value occurs. Most often we are interested in symmetrical confidence intervals, so the procedure is:

.. math::
	:label: CI-mean-variance-unknown-repeated
		
		\begin{array}{rcccl} 
		      - c_t                                  &\leq& z                                                   &\leq &  +c_t\\
			  - c_t                                  &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
			\overline{x}  - c_t \dfrac{s}{\sqrt{n}}  &\leq&  \mu                                                &\leq& \overline{x}  + c_t\dfrac{s}{\sqrt{n}} \\
			  \text{LB}                              &\leq&  \mu                                                &\leq& \text{UB}
		\end{array}
	
The critical values of :math:`c_t` are ``qt(1 - 0.05/2, df=8) = 2.306004`` when we used the 95% confidence interval (2.5% in each tail). We calculated that LB = 20.0 - 2.92 = 17.1 and that UB = 20.0 + 2.92 = 22.9.  

Interpreting the confidence interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: confidence interval; interpreting

.. youtube:: https://www.youtube.com/watch?v=H_7dZRYSBGw&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=13

-	The expression in :eq:`CI-mean-variance-unknown-repeated` should not be interpreted to mean that the viscosity is 20 units and lies inside the LB (lower-bound) to UB (upper-bound) range of 17.1 to 22.9 with a 95% probability. In fact, the sample mean lies exactly at the mid-point of the range with 100% certainty - that is how the range was calculated.

-	What the expression in :eq:`CI-mean-variance-unknown-repeated` **does imply** is that :math:`\mu` lies in this interval. The confidence interval is a range of possible values for :math:`\mu`, not for :math:`\overline{x}`. Confidence intervals are for parameters, not for statistics.
	
-	Notice that the upper and lower bounds are a function of the data sample used to calculate :math:`\overline{x}` and the number of points, :math:`n`. If we take a different sample of data, we will get different upper and lower bounds.
	
-	What does the level of confidence mean?  

		It is the probability that the true population viscosity, :math:`\mu` is in the given range. At 95% confidence, it means that 5% of the time the interval *will not contain* the true mean. So if we collected 20 sets of :math:`n` samples, 19 times out of 20 the confidence interval range **will contain** the true mean, but one of those 20 confidence intervals is expected not to contain the true mean.

-	What happens if the level of confidence changes?  Calculate the viscosity confidence intervals for 90%, 95%, 99%.

		.. csv-table:: 
		   :header: Confidence, LB, UB
		   :widths: 33, 33, 33

			90%, 17.6, 22.4
			95%, 17.1, 22.9
			99%, 15.7, 24.2			
			
		As the confidence level is *increased*, our interval widens, indicating that we have a more reliable region, but it is less precise. With a wider interval we have greater confidence that the true parameter will be inside that region.
		
		Try it out:
		
		.. dcl:: R

			# Try varying this value:
			conf.level <- 0.90
			
			viscosity <- c(23, 19, 17, 18, 
			               24, 26, 21, 14, 18)
			n <- length(viscosity)
			x.avg <- mean(viscosity)
			x.sd <- sd(viscosity)
			dof <- n - 1
			c.t <- qt(p = 1-(1-conf.level)/2, 
			          df = dof) 
			LB <- x.avg - c.t * x.sd / sqrt(n)
			UB <- x.avg + c.t * x.sd / sqrt(n)
			paste0('The ', round(conf.level*100, 0),
			       '% confidence interval is: ')
			paste0('[', round(LB, 1), '; ', round(UB, 1), ']')
			
..	TODO: show the confidence ranges, like BHH, p114 (2nd edition)

-	What happens if the level of confidence is 100%?

		The confidence interval is then infinite. We are 100% certain this infinite range contains the population mean, however this is not a useful interval. Test it out in the code above; also try creating an interval with 99.9% confidence, and then 99.99% confidence.

-	What happens if we increase the value of :math:`n`?

		As intuitively expected, as the value of :math:`n` increases, the confidence interval decreases in width.
		
-	Returning to the case above, where at the 95% level we found the confidence interval was :math:`[17.1; 22.9]` for the bale's viscosity. What if we were to analyze the bale thoroughly, and found the population viscosity to be 23.2. What is the probability of that occurring?

		Less than 5% of the time.

Confidence interval for the mean from a normal distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=yyK1O3JKd1U&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=14

The aim here is to formalize the calculations for the confidence interval of :math:`\overline{x}`, given a sample of :math:`n` 

	a)	independent points, taken from 
	b)	the normal distribution. 

Be sure to check those two assumptions before going ahead.

There are 2 cases: one where you know the population standard deviation (unlikely), and one where you do not (the usual case). It is safer to use the confidence interval for the case when you do not know the standard deviation, as it is a more conservative (i.e. wider) interval.

The detailed derivation for the two cases was covered in earlier sections.

Case A. Variance is known
^^^^^^^^^^^^^^^^^^^^^^^^^^

When the variance is known, the confidence interval is given by :eq:`CI-mean-variance-known-again` below, derived from this :math:`z`-deviate:  :math:`z = \dfrac{\overline{x} - \mu}{\sigma/\sqrt{n}}` back in the :ref:`section on the normal distribution <univariate_eqn_CI-mean-variance-known>`. 

.. _univariate_eqn_CI-mean-variance-known-again:

.. math::
		:label: CI-mean-variance-known-again
		
		\begin{array}{rcccl} 
			  - c_n                                      &\leq& z                                                        &\leq &  +c_n\\
			  - c_n                                      &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}} &\leq &  +c_n\\
			\overline{x}  - c_n \dfrac{\sigma}{\sqrt{n}} &\leq&  \mu                                                     &\leq& \overline{x}  + c_n\dfrac{\sigma}{\sqrt{n}} \\
			  \text{LB}                                  &\leq&  \mu                                                     &\leq& \text{UB}
		\end{array}

The values of :math:`c_n` are ``qnorm(1 - 0.05/2) = 1.96`` when we happen to use the 95% confidence interval (2.5% in each tail). 

Case B. Variance is unknown
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
	single: confidence interval; unknown variance

In the more realistic case when the variance is unknown we use the equation :ref:`derived in the section on the t-distribution <univariate_eqn_CI-mean-variance-unknown>`, and repeated here below. This is derived from the :math:`z`-deviate: :math:`z = \dfrac{\overline{x} - \mu}{s/\sqrt{n}}`:

.. math::
	:label: CI-mean-variance-unknown-again
		
	\begin{array}{rcccl} 
		  - c_t                                 &\leq& z                                                   &\leq &  +c_t\\
		  - c_t                                 &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
		\overline{x}  - c_t \dfrac{s}{\sqrt{n}} &\leq& \mu                                                 &\leq& \overline{x}  + c_t\dfrac{s}{\sqrt{n}} \\
		  \text{LB}                             &\leq& \mu                                                 &\leq& \text{UB}
	\end{array}
		
The values of :math:`c_t` are ``qt(1 - 0.05/2, df=...)`` when we use the 95% confidence interval (2.5% in each tail). This :math:`z`-deviate is distributed according to the :math:`t`-distribution, since we have additional uncertainty when using the standard deviation estimate, :math:`s`, instead of the population standard deviation, :math:`\sigma`.

Comparison
^^^^^^^^^^

If we have the fortunate case where our estimated variance, :math:`s^2`, is equal to the population variance, :math:`\sigma^2`, then we can compare the 2 intervals in equations :eq:`CI-mean-variance-known-again` and :eq:`CI-mean-variance-unknown-again`. The only difference would be the value of the :math:`c_n` from the normal distribution and :math:`c_t` from the :math:`t`-distribution. For typical values used as confidence levels, 90% to 99.9%, values of :math:`c_t > c_n` for any degrees of freedom. 

This implies the confidence limits are wider for the case when the standard deviation is unknown, leading to more conservative results, reflecting our uncertainty of the standard deviation parameter, :math:`\sigma`.

.. Plot these in R to verify:  plot(seq(0,1,0.01), qt(seq(0,1,0.01), df=2)); lines(seq(0,1,0.01), qnorm(seq(0,1,0.01)))
