The t-distribution
=======================

.. index:: t-distribution

Suppose we have a quantity of interest from a process, such as the daily profit. In the preceding section we started to answer the useful and important question: 

	What is the range within which the true average value lies?  E.g. the range for the true, but unknown, daily profit.
	
But we got stuck, because the lower and upper bounds we calculated for the true average, :math:`\mu` were a function of the unknown population standard deviation, :math:`\sigma`. Repeating :ref:`the prior equation for confidence interval <univariate_eqn_CI-mean-variance-known-again>` where we know the variance: 

.. math::

		\begin{array}{rcccl} 
			  - c_n                                      &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}} &\leq &  +c_n\\
			\overline{x}  - c_n \dfrac{\sigma}{\sqrt{n}} &\leq&  \mu                                                     &\leq& \overline{x}  + c_n\dfrac{\sigma}{\sqrt{n}} \\
			  \text{LB}                                  &\leq&  \mu                                                     &\leq& \text{UB}
		\end{array}

which we derived by using the fact that :math:`\dfrac{\overline{x} - \mu}{\sigma/\sqrt{n}}` is normally distributed.

An obvious way out of our dilemma is to replace :math:`\sigma` by the sample standard deviation, :math:`s`, which is exactly what we will do, however, the quantity :math:`\frac{\overline{x} - \mu}{s/\sqrt{n}}` is not normally distributed, but is :math:`t`-distributed. Before we look at the details, it is helpful to see how similar in appearance the :math:`t` and normal distribution are: the :math:`t`-distribution peaks slightly lower than the normal distribution, but it has broader tails. The total area under both curves illustrated here is 1.0.

.. image:: ../figures/univariate/t-distribution-comparison.png
	:align: right
	:scale: 70
	:width: 900
	:alt: fake width

There is one other requirement we have to ensure in order to use the :math:`t`-distribution: the values that we sample, :math:`x_i` must come from a normal distribution (carefully note that in the previous section we didn't have this restriction!). Fortunately it is easy to check this requirement: just use the :ref:`q-q plot method described earlier <univariate_check_for_normality_qqplot>`. Another requirement, which we had before, was that we must be sure these measurements, :math:`x_i`, are independent.

.. image:: ../figures/univariate/t-distribution-derivation.png
	:align: center
	:scale: 75

So given our :math:`n` samples, which are independent, and from a normal distribution, we can now say: 

.. math::
	:label: distribution-for-sample-average

	\frac{\overline{x} - \mu}{s/\sqrt{n}} \sim t_{n-1}

Compare this to the previous case where our :math:`n` samples are independent, and we happen to know, by some unusual way, what the population standard deviation is, :math:`\sigma`:

.. math::

	\frac{\overline{x} - \mu}{\sigma/\sqrt{n}} \sim \mathcal{N} \left(0, 1\right)

So the more practical and useful case where :math:`z  = \frac{\overline{x} - \mu}{s/\sqrt{n}} \sim t_{n-1}` can now be used to construct an interval for :math:`\mu`. We say that :math:`z` follows the :math:`t`-distribution with :math:`n-1` degrees of freedom, where the degrees of freedom refer to those from the calculating the *estimated* standard deviation, :math:`s`. 
 
Note that the new variable :math:`z` only requires we know the population mean (:math:`\mu`), not the population standard deviation; rather we use our estimate of the standard deviation :math:`s/\sqrt{n}` in place of the population standard deviation.

We will come back to :eq:`distribution-for-sample-average` in a minute; let's first look at how we can calculate values from the :math:`t`-distribution in computer software.

.. 
	From Box, Hunter and Hunter, 1st edition, p 50-51
	To use the :math:`t`-distribution we must ensure that these 3 conditions are true:

	#. the sampled values :math:`y_i` are normally distributed around the mean :math:`\mu` and have variance :math:`\sigma` (note that we do not need to know the value of :math:`\sigma`)
	#. the variance estimate, :math:`s` is distributed independently of :math:`y`
	#. the quantity :math:`s^2` is calculated from normally and independently distributed observations having variance :math:`\sigma^2`.

.. TODO: see p 295 of Devore here for in-class example

Calculating the t-distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-	In R we use the function ``dt(x=..., df=...)`` to give us the values of the probability density values, :math:`p(x)`, of the :math:`t`-distribution (compare this to the ``dnorm(x, mean=..., sd=...)`` function for the normal distribution).

	.. dcl:: R
		:height: 350px
		
		x = 0.0
		
		# Recall, for the normal distribution:
		dnorm(x, mean=0, sd=1)    # 0.3989423
		
		# For the t-distribution we don't have
		# a sigma, but we do need to say how
		# many degrees of freedom we have:
		
		dof <- 8
		dt(x, df=dof)             # 0.386699
		
		# Shows that the t-distribution has a 
		# lower peak than the normal distribution.
		# Try it again, but with fewer and
		# greater degrees of freedom (`dof`).


-	The cumulative area from :math:`-\infty` to :math:`x` under the probability density curve gives us the probability that values less than or equal to :math:`x` could be observed. It is calculated in R using ``pt(q=..., df=...)``. For example, ``pt(1.0, df=8)`` is 0.8267. Compare this to the R function for the standard normal distribution: ``pnorm(1.0, mean=0, sd=1)`` which returns 0.8413.

	.. dcl:: R
		:height: 350px
		
		q = 1.0
		
		# Recall, for the normal distribution:
		pnorm(q, mean=0, sd=1) # 0.8413447
		
		# For the t-distribution we need to 
		# specify the degrees of freedom:
		
		dof <- 8
		pt(q, df=dof)          # 0.8267032
		
		# Shows that the t-distribution is  
		# similar, but the areas are slightly
		# different.

-	And similarly to the ``qnorm`` function which returns the ordinate for a given area under the normal distribution, the function ``qt(0.8267, df=8)`` returns 0.9999857, close enough to 1.0, which is the inverse of the previous example.

	.. dcl:: R
		:height: 300px
		
		p = 0.5
		
		# Recall, for the normal distribution:
		qnorm(p, mean=0, sd=1)   # 0.0
		
		# For the t-distribution:
		
		dof <- 8
		qt(p, df=dof)            # 0.0
		
		# Both distributions have their 50% 
		# quantile at p=0. But try it for
		# other values of probability, p.



.. _univariate_confidence_interval_t_distribution:

Using the t-distribution to calculate our confidence interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  But in R, we use the ``dt(x, df=...)`` function to give us the values of the :math:`t`-distribution for a given value of :math:`x` which has been computed with ``df`` degrees of freedom. We use the :math:`t`-distribution in calculations related to a sample *mean*, and it is the sample mean that we use as the :math:`z` value, on the :math:`x`-axis in the distribution. This is why the distribution is only a function of the degrees of freedom.

.. youtube:: https://www.youtube.com/watch?v=B22K3Fw49zo&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=12

Returning back to :eq:`distribution-for-sample-average` we stated that

.. math::
	
		\dfrac{\overline{x} - \mu}{s / \sqrt{n}} \sim t_{n-1}

We can plot the :math:`t`-distribution for a given value of :math:`n-1`, the degrees of freedom. Then we can locate vertical lines on the :math:`x`-axis at :math:`-c_t` and :math:`+c_t` so that the area between the verticals covers say 95% of the total distribution's area. The subscript :math:`t` refers to the fact that these are critical values from the :math:`t`-distribution.

.. _univariate_eqn_CI-mean-variance-unknown:

Then we write:

.. math::
	:label: CI-mean-variance-unknown

	\begin{array}{rcccl} 
		  - c_t                                  &\leq& z                                                   &\leq &  +c_t\\
		  - c_t                                  &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
		\overline{x}  - c_t \dfrac{s}{\sqrt{n}}  &\leq&  \mu                                                &\leq& \overline{x}  + c_t\dfrac{s}{\sqrt{n}} \\
		  \text{LB}                              &\leq&  \mu                                                &\leq& \text{UB}
	\end{array}

Now all the terms in the lower and upper bound are known, or easily calculated.

So we finish this section off with an example. We produce large cubes of polymer product on our process. We would like to estimate the cube's average viscosity, but measuring the viscosity is a destructive laboratory test. So using 9 independent samples taken from this polymer cube, we get the 9 lab values of viscosity: ``23, 19, 17, 18, 24, 26, 21, 14, 18``. 

If we repeat this process with a different set of 9 samples we will get a different average viscosity. So we recognize the average of a sample of data, is itself just a single estimate of the population's average. What is more helpful is to have **a range**, given by a lower and upper bound, that we can say the true population mean lies within.

#.	The average of these nine values is :math:`\overline{x} = 20` units.

#.	Using the Central limit theorem, what is the distribution from which :math:`\overline{x}` comes?

		:math:`\overline{x} \sim \mathcal{N}\left(\mu, \sigma^2/n \right)`
		
		This also requires the assumption that the samples are independent estimates of the population viscosity. We **don't** have to assume the :math:`x_i` are normally distributed.
		
#.	What is the distribution of the sample average?  What are the parameters of that distribution?

		The sample average is normally distributed as :math:`\mathcal{N}\left(\mu, \sigma^2/n \right)`
		
#.	Assume, for some hypothetical reason, that we know the population viscosity standard deviation is :math:`\sigma=3.5` units. Calculate a lower and upper bound for :math:`\mu`:

		The interval is calculated using from an :ref:`earlier equation when discussing the normal distribution <univariate_eqn_CI-mean-variance-known>`:
		
		.. math::
		
			\text{LB} &= \overline{x} - c_n \dfrac{\sigma}{\sqrt{n}} \\
			          &= 20 - 1.95996 \cdot \dfrac{3.5}{\sqrt{9}} \\
			          &= 20 - 2.286 = {\bf 17.7} \\
			\text{UB} &= 20 + 2.286 = {\bf 22.3}

#.	We can confirm these 9 samples are normally distributed by using a q-q plot (not shown, but you can use the code below to generate the plot). This is an important requirement to use the :math:`t`-distribution, next.

#.	Calculate an estimate of the standard deviation.

		:math:`s = 3.81`
	
#.	Now construct the :math:`z`-value for the sample average and from what distribution does this :math:`z` come from?

		It comes the :math:`t`-distribution with :math:`n-1 = 8` degrees of freedom, and is given by :math:`z = \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}}`

#.	Construct an interval, symbolically, that will contain the population mean of the viscosity. Also calculate the lower and upper bounds of the interval assuming the internal to span 95\% of the area of this distribution.

		The interval is calculated using :eq:`CI-mean-variance-unknown`:
		
		.. math::
		
			\text{LB} &= \overline{x}  - c_t \dfrac{s}{\sqrt{n}} \\
			          &= 20 - 2.306004 \cdot \dfrac{3.81}{\sqrt{9}} \\
			          &= 20 - 2.929 = 17.1 \\
			\text{UB} &= 20 + 2.929 = 22.9

		using from R that ``qt(0.025, df=8)`` and ``qt(0.975, df=8)``, which gives ``2.306004``
		
	.. dcl:: R
	
		# Step 0: the raw data
		viscosity <- c(23, 19, 17, 18, 
		               24, 26, 21, 14, 18)
		n <- length(viscosity)
		
		# Step 1:
		x.avg <- mean(viscosity)
		
		# Step 5: Verify the data are normal
		library(car)
		qqPlot(viscosity)
		
		# Step 6: 
		x.sd <- sd(viscosity)
		
		# Step 7: t-distribution 
		dof <- n - 1
		
		# Step 8:
		conf.level <- 0.95
		
		# Can be calculated at either
		# the lower tail
		c.t <- qt(p = (1-conf.level)/2, 
		          df = dof) 
				  
		# or the upper tail
		c.t <- qt(p = 1-(1-conf.level)/2, 
		          df = dof) 
				  
		LB <- x.avg - c.t * x.sd / sqrt(n)
		UB <- x.avg + c.t * x.sd / sqrt(n)
		paste0('The confidence interval is: ')
		paste0('[', round(LB, 1), '; ', round(UB, 1), ']')
		
		
			
Comparing the answers for parts 4 and 8 we see the interval, for the same level of 95% certainty, is wider when we have to estimate the standard deviation. This makes sense: the standard deviation is an estimate (meaning there is error in that estimate) of the true standard deviation. That uncertainty must propagate, leading to a wider interval within which we expect to locate the true population viscosity, :math:`\mu`.

We will interpret confidence intervals in more detail a :ref:`little later on <univariate_confidence_intervals>`.

.. sum((x-20) * (x-20)) = 116, DOF=8, s^2 = 116/8 = 14.5, s=3.81. Distribution is normal, mean=\mu, stddev=3.5/sqrt(9) = (3.5^2)/9 = 2.286
.. s/sqrt(n) = 3.81/sqrt(9) = 1.27

.. The value of :math:`\overline{x}` is not normally distributed, it is :math:`t`distributed. This means that if we had to repeatedly calculate :math:`\overline{x}`, those averages would follow a :math:`t`distribution, even though the source values, :math:`x_i` are normally distributed. 

.. another example
	

