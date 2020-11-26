.. _monitoring_shewhart_chart:

Shewhart charts
===============

.. For the mean: p174 to p186 of Barnes. KGD: what does "Barnes" refer to?

.. youtube:: https://www.youtube.com/watch?v=8Ln3emiwQzU&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=60

A :index:`Shewhart chart <pair: Shewhart chart; process monitoring>`, named after Walter Shewhart from Bell Telephone and Western Electric, monitors that a process variable remains on target and within given upper and lower limits. It is a monitoring chart for *location*. It answers the question whether the variable's :index:`location <single: location (process monitoring)>` is stable over time. It does not track anything else about the measurement, such as its standard deviation. Looking ahead: :ref:`we show later <monitoring_shewart_chart_slugishness>` that a pure Shewhart chart needs extra rules to help monitor the location of a variable effectively.

The defining characteristics of a Shewhart chart are: a target, upper and lower control limits (:index:`UCL <single: upper control limit>` and :index:`LCL <single: lower control limit>`). These action limits are defined so that no action is required as long as the variable plotted remains within the limits. In other words a special cause is not likely present if the points remain within the UCL and LCL.

Derivation using theoretical parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define the variable of interest as :math:`x`, and assume that we have samples of :math:`x` available in sequence order. No assumption is made regarding the distribution of :math:`x`. The average of :math:`n` of these :math:`x`-values is defined as :math:`\overline{x}`, which from the :ref:`Central limit theorem <central_limit_theorem>` we know will be more normally distributed with unknown population mean :math:`\mu` and unknown population variance :math:`\sigma^2/n`, where :math:`\mu` and :math:`\sigma` refer to the distribution that samples of :math:`x` came from. The figure here shows the case for :math:`n=5`.

.. image:: ../figures/monitoring/explain-Shewhart-data-source.png
	:align: left
	:scale: 50
	:width: 800px
	:alt: fake width

So by taking :index:`subgroups <single: subgroups (monitoring charts)>` of size :math:`n` values, we now have for each subgroup a newly calculated variable, :math:`\overline{x}` and we will define a shorthand symbol for its standard deviation: :math:`\sigma_{\overline{X}} = \sigma/\sqrt{n}`. Writing a :math:`z`-value for :math:`\overline{x}`, and its associated confidence interval for :math:`\mu` is now easy after studying :ref:`the section on confidence intervals<univariate_confidence_intervals>`:

.. math::

	z = \frac{\displaystyle \overline{x} - \mu}{\displaystyle \sigma_{\overline{X}}}

Assuming we know :math:`\sigma_{\overline{X}}`, which we usually do not in practice, we can invoke the normal distribution and calculate the probability of finding a value of :math:`z` between :math:`c_n = -3` to :math:`c_n = +3`:

.. math::
	:label: shewhart-theoretical
	
	\begin{array}{rcccl} 
		  - c_n                                              &\leq& \dfrac{\overline{x} - \mu}{\sigma_{\overline{X}}} &\leq&  +c_n\\ \\
		\overline{x}  - c_n\sigma_{\overline{X}}             &\leq&  \mu                                              &\leq& \overline{x}  + c_n\sigma_{\overline{X}} \\ \\
		\text{LCL}                                           &\leq&  \mu                                              &\leq& \text{UCL}
	\end{array}

The reason for :math:`c_n = \pm 3` is that the total area between that lower and upper bound spans 99.73% of the area (in R: ``pnorm(+3) - pnorm(-3)`` gives 0.9973). So it is highly unlikely, a chance of 1 in 370, that a data point, :math:`\overline{x}`, calculated from a subgroup of :math:`n` raw :math:`x`-values, will lie outside these bounds.

The following illustration should help connect the concepts: the raw data's distribution happens to have a mean of 6 and standard deviation of 2, while it is clear the distribution of the subgroups of 5 samples (thicker line) is much narrower.

.. image:: ../figures/monitoring/explain-shewhart.png
	:alt:	../figures/monitoring/explain-shewhart.R
	:scale: 70
	:width: 750px
	:align: right


Using estimated parameters instead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The derivation in equation :eq:`shewhart-theoretical` requires knowing the population variance, :math:`\sigma`, and assuming that our target for :math:`x` is :math:`\mu`. The latter assumption is reasonable, but we will estimate a value for :math:`\sigma` instead, using the data.

.. index:: ! phase 1 (monitoring charts)

Let's take a look at phase 1, the step where we are building the monitoring chart's limits from historical data. Create a new variable |xdb| :math:`= \displaystyle \frac{1}{K} \sum_{k=1}^{K}{ \overline{x}_k}`, where :math:`K` is the number of :math:`\overline{x}` samples we have available to build the monitoring chart, called the :index:`phase 1 <single: phase 1 (monitoring charts)>` data. Note that |xdb| is sometimes called the *grand mean*. Alternatively, just set |xdb| to the desired target value for :math:`x` or use a long portion of stable data to estimate a suitable target

The next hurdle is :math:`\sigma`. Define :math:`s_k` to be the standard deviation of the :math:`n` values in the :math:`k^\text{th}` subgroup. We do not show it here, but for a subgroup of :math:`n` samples, an unbiased estimator of :math:`\sigma` is given by :math:`\displaystyle \frac{\overline{S}}{a_n}`, where :math:`\overline{S} =  \displaystyle \frac{1}{K} \displaystyle \sum_{k=1}^{K}{s_k}` is simply the average standard deviation calculated from :math:`K` subgroups. Values for :math:`a_n` are looked up from a table, or using the formula below, and depend on the number of samples we use within each subgroup.

===========  ====== ====== ====== ====== ====== ====== ====== ====== ======
:math:`n`    2      3      4      5      6      7      8      10     15
-----------  ------ ------ ------ ------ ------ ------ ------ ------ ------
:math:`a_n`  0.7979 0.8862 0.9213 0.9400 0.9515 0.9594 0.9650 0.9727 0.9823
===========  ====== ====== ====== ====== ====== ====== ====== ====== ======

..	See Devore, page 683

More generally, using the :math:`\Gamma(...)` function, for example ``gamma(...)`` in R or MATLAB, or ``math.gamma(...)`` in Python, you can reproduce the above :math:`a_n` values.

.. math::

	a_n = \frac{\sqrt{2}\,\,\Gamma(n/2)}{\sqrt{n-1}\,\,\Gamma(n/2 - 0.5)}

Notice how the :math:`a_n` values tend to 1.0 the larger the subgroup size, indicating we need less of a correction to make the standard deviation less biased. Once we have this unbiased estimator for the standard deviation from these :math:`K` subgroups, we can write down suitable :index:`lower <single: lower control limit>` and :index:`upper control limits <single: upper control limit>` for the Shewhart chart:

.. math::
	:label: shewhart-limits
	
	\begin{array}{rcccl} 
		 \text{LCL} = \overline{\overline{x}} - 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} &&  &&  \text{UCL} = \overline{\overline{x}} + 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} 
	\end{array}
	
It is highly unlikely that all the data chosen to calculate the phase 1 limits actually lie within these calculated LCL and UCLs. Those portions of data not from stable operation, which are outside the limits, should not have been used to calculate these limits. Those unstable data bias the limits to be wider than required.

Exclude these :index:`outlier` data points and recompute the LCL and UCLs. Usually this process is repeated 2 to 3 times. It is wise to investigate the data being excluded to ensure they truly are from unstable operation. If they are from stable operation, then they should not be excluded. These data may be :ref:`violating the assumption of independence <monitoring_mistakes_to_avoid>`. One may consider using wider limits, or use an :ref:`EWMA control chart <monitoring_EWMA>`. 

.. rubric:: Example

Bales of rubber are being produced, with every 10th bale automatically removed from the line for testing. Measurements of colour intensity are made on 5 sides of that bale, using calibrated digital cameras under controlled lighting conditions. The rubber compound is used for medical devices, so it needs to have the correct colour, as measured on a scale from 0 to 255. The average of the 5 colour measurements is to be plotted on a Shewhart chart. So we have a new data point appearing on the monitoring chart after every 10th bale. 

In the above example the raw data are the bale's colour. There are :math:`n = 5` values in each subgroup. Collect say :math:`K=20` samples of good production bales considered to be from stable operation. No special process events occurred while these bales were manufactured.

The data below represent the average of the :math:`n=5` samples from each bale, there are :math:`K=20` of these subgroups.

.. math::
 	\overline{x} = [245, 239, 239, 241, 241, 241, 238, 238, 236, 248, 233, 236, 246, 253, 227, 231, 237, 228, 239, 240]

The overall average is :math:`\overline{\overline{x}} = 238.8` and :math:`\overline{S} = 9.28`. The raw data are `available on this website <https://openmv.net/info/rubber-colour>`_ and you can verify the values of :math:`\overline{\overline{x}}` and :math:`\overline{S}` were correctly calculated.


*	Calculate the lower and upper control limits for this Shewhart chart. 
*	Were there any points in the phase 1 data (training phase) that exceeded these limits?

	*	LCL = :math:`\overline{\overline{x}} - 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} = 238.8 - 3 \cdot \displaystyle \frac{9.28}{(0.94)(\sqrt{5})} = 225.6` 
	*	UCL = :math:`\overline{\overline{x}} + 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} = 238.8 + 3 \cdot \displaystyle \frac{9.28}{(0.94)(\sqrt{5})} = 252.0` 
	*	The group with :math:`\overline{x}` = 253 exceeds the calculated upper control limit. 
	*	That :math:`\overline{x}` point should be excluded and the limits recomputed. You can show the new :math:`\overline{\overline{x}} = 238.0` and :math:`\overline{S} = 9.68` and the new LCL = 224 and UCL = 252.
	
	
In source code:

.. dcl:: R

	# Given information (but calculate yourself
	# from https://openmv.net/info/rubber-colour)
	xbar = c(245, 239, 239, 241, 241, 241, 238,
	         238, 236, 248, 233, 236, 246, 253,
	         227, 231, 237, 228, 239, 240)

	# Number of measurements per subgroup
	N.sub = 5

	# Average of the 20 standard deviations 
	# of the 20 subgroups
	S = 9.28

	# xdb = x double bar = overall mean =
	#       mean of the means
	xdb = mean(xbar)

	num.an = sqrt(2) * gamma(N.sub/2)
	den.an = sqrt(N.sub-1) * gamma((N.sub-1)/2)
	an = num.an / den.an

	LCL = xdb - (3 * S/(an * sqrt(N.sub)))
	UCL = xdb + (3 * S/(an * sqrt(N.sub)))
	paste0('Control limits: [', round(LCL, 2),
	       '; ', round(UCL,2), ']')

	paste0('Number > UCL: ', sum(xbar > UCL))
	paste0('Number < LCL: ', sum(xbar < LCL))

	# Exclude the one subgroup above the UCL.
	# Do this by setting it to 'NA' (missing)
	xbar[xbar > UCL] = NA

	# Calculate the mean, removing missing
	# values (ignore it).
	xdb = mean(xbar, na.rm=TRUE)

	# 'S' will change also. If you download the
	# raw data (link above), you can prove
	# that the new 'S' will be:
	S = 9.68

	# The 'an' and 'N.sub' will not change.

	LCL = xdb - (3 * S/(an * sqrt(N.sub)))
	UCL = xdb + (3 * S/(an * sqrt(N.sub)))
	paste0('Control limits: [', round(LCL, 0),
	       '; ', round(UCL,0), ']')
	

.. TODO: in the future, describe more clearly the difference between phase 1 and phase 2. Students were asking a lot of questions around this.

.. _monitoring_judging_performance:

Judging the chart's performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=vHbjFQSOiNQ&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=61

There are 2 ways to :index:`judge performance of a monitoring chart <single: monitoring chart assessment>`. In particular here we discuss the Shewhart chart:

.. rubric:: 1. Error probability. 

We define two types of errors, Type I and Type II, which are a function of the lower and upper control limits (LCL and UCL).

You make a **type I error** when your sample is typical of normal operation, yet, it falls outside the UCL or LCL limits. We showed in the theoretical derivation that the area covered by the upper and lower control limits is 99.73%. The probability of making a type I error, usually denoted as :math:`\alpha` is then :math:`100 - 99.73 = 0.27\%`.

*Synonyms* for a **type I error**: false alarm, false positive (used mainly for testing of diseases), producer's risk (used for acceptance sampling, because here as the producer you will be rejecting an acceptable sample), false rejection rate, or alpha.

You make a **type II error** when your sample really is abnormal, but falls within the the UCL and LCL limits and is therefore not detected. This error rate is denoted by :math:`\beta`, and it is a function of the degree of abnormality, which we derive next.

*Synonyms* for a **type II error**: false negative (used mainly for testing of diseases), consumer's risk (used for acceptance sampling, because your consumer will be receiving available product which is defective), false acceptance rate, or beta.

To quantify the probability :math:`\beta`, recall that a Shewhart chart is for monitoring location, so we make an assumption that the new, abnormal sample comes from a distribution which has shifted its location from :math:`\mu` to :math:`\mu + \Delta\sigma` (e.g. :math:`\Delta` can be positive or negative). Now, what is the probability this new sample, which come from the shifted distribution, will fall within the existing LCL and UCL? This figure shows the probability is :math:`\beta = (1 - \text{the shaded area})`.

.. math::

	\alpha &= Pr\left(\overline{x}\,\,\text{is in control, but lies outside the limits}\right) = \text{type I error rate}\\
	\beta &= Pr\left(\overline{x}\,\,\text{is not in control, but lies inside the limits}\right) = \text{type II error rate}

.. figure:: ../figures/monitoring/show-shift-beta-error.png
	:width: 800px
	:align: center
	:scale: 70
	:alt: fake width

.. todo  How did Devore calculate these numbers: see p 667 of his book - it doesn't make sense to me. See my attempt in "show-shift-typeII-error.R"

..	See Montgomery and Runger, Second edition, p 313, for a possible derivation
.. \beta = pnorm(3-delta*sqrt(n)) - pnorm(-3 - delta*sqrt(n))

.. _monitoring_sluggish_shewhart_chart:

The table highlights that :math:`\beta` is a function of the amount by which the process shifts = :math:`\Delta`, where :math:`\Delta=1` implies the process has shifted up by :math:`1\sigma`. The table was calculated for :math:`n=4` and used critical limits of :math:`\pm 3 \sigma_{\overline{X}}`. You can calculate your own values of :math:`\beta` using this line of R code: ``beta <- pnorm(3 - delta*sqrt(n)) - pnorm(-3 - delta*sqrt(n))``

==============================  ====== ====== ====== ====== ====== ====== 
:math:`\Delta`                  0.25   0.50   0.75   1.00   1.50   2.00   
------------------------------  ------ ------ ------ ------ ------ ------ 
:math:`\beta` when :math:`n=4`  0.9936 0.9772 0.9332 0.8413 0.5000 0.1587
==============================  ====== ====== ====== ====== ====== ======

.. dcl:: R
	:height: 250px
	
	delta <- 1
	n <- 4
	beta <- pnorm(+3 - delta*sqrt(n)) - 
	        pnorm(-3 - delta*sqrt(n))

	paste0('When delta=', delta, ' and n=', n, 
	       ' then beta = ', round(beta, 4))

.. _monitoring_shewart_chart_slugishness:

The key point you should note from the table is that a Shewhart chart is *not good* (it is slow) at detecting a change in the location (level) of a variable. This is surprising given the intention of the plot is to monitor the variable's location. Even a moderate shift of :math:`0.75\sigma` units :math:`(\Delta=0.75)` will only be detected around 6.7% of the time (:math:`100-93.3\%`) when :math:`n=4`. We will discuss :ref:`CUSUM charts <monitoring_CUSUM_charts>` and the Western Electric rules, next, as a way to overcome this issue.

It is straightforward to see how the type I, :math:`\alpha`, error rate can be adjusted - simply move the LCL and UCL up and down, as required, to achieve your desired error rates. There is nothing wrong in arbitrarily shifting these limits - :ref:`more on this later <monitoring_adjust_limits>` in the section on adjusting limits.

However what happens to the type II error rate as the LCL and UCL bounds are shifted away from the target?  Imagine the case where you want to have :math:`\alpha \rightarrow 0`. As you make the UCL higher and higher, the value for :math:`\alpha` drops, but the value for :math:`\beta` will also increase, since the control limits have become wider!  **You cannot simultaneously have low type I and type II error**, or as said more colloquially, "there is no free lunch".

.. rubric:: 2. Using the average run length (ARL)

The :index:`average run length` (ARL) is defined as the average number of sequential samples we expect before seeing an out-of-bounds, or out-of-control signal. This is given by the inverse of :math:`\alpha`, as ARL = :math:`\frac{1}{\alpha}`. Recall for the theoretical distribution we had :math:`\alpha = 0.0027`, so the ARL = 370. Thus we expect a run of 370 samples before we get an out-of-control signal.


Extensions to the basic Shewhart chart to help monitor stability of the location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :index:`Western Electric rules`: we saw above how sluggish the Shewhart chart is in detecting a small shift in the process mean, from :math:`\mu` to :math:`\mu + \Delta\sigma`. The **Western Electric rules** are an attempt to more rapidly detect a process shift, by raising an alarm when these *improbable* events occur:

#. Two out of 3 points lie beyond :math:`2\sigma` on the same side of the centre line
#. Four out of 5 points lie beyond :math:`1\sigma` on the same side of the centre line
#. Eight successive points lie on the same side of the center line

However, an alternative chart, the CUSUM chart is more effective at detecting a shift in the mean. Notice also that the theoretical ARL, :math:`1/\alpha`, is reduced by using these rules in addition to the LCL and UCL bounds.

**Adding robustness**: the phase I derivation of a monitoring chart is iterative. If you find a point that violates the LCL and UCL limits, then the approach is to remove that point, and recompute the LCL and UCL values. That is because the LCL and UCL limits would have been biased up or down by these unusual points :math:`\overline{x}_k` points.

	This iterative approach can be tiresome with data that has spikes, missing values, outliers, and other problems typical of data pulled from a process database (:index:`historian <single: data historian>`). Robust monitoring charts are procedures to calculate the limits so the LCL and UCL are resistant to the effect of outliers. For example, a robust procedure might use the medians and MAD instead of the mean and standard deviation. An examination of various robust procedures, especially that of the interquartile range, is given in the paper by D. M. Rocke, `Robust Control Charts <https://dx.doi.org/10.2307/1268815>`_, *Technometrics*, **31** (2), p 173 - 184, 1989.

	*Note*: do not use robust methods to calculate the values plotted on the charts during phase 2, only use robust methods to calculate the chart limits in phase 1!
	
**Warning limits**: it is common to see warning limits on a monitoring chart at :math:`\pm 2 \sigma`, while the :math:`\pm 3\sigma` limits are called the action limits. Real-time computer systems usually use a colour scheme to distinguish between the warning state and the action state. For example, the chart background changes from green, to orange to red as the deviations from target become more severe.

.. _monitoring_adjust_limits:

**Adjusting the limits**: The :math:`\pm 3\sigma` limits are not set in stone. Depending on the degree to which the source data obey the assumptions, and the frequency with which spikes and outliers contaminate your data, you may need to adjust your limits, usually wider, to avoid frequent false alarms. Nothing makes a monitoring chart more useless to operators than frequent false alarms ("`crying wolf <https://en.wikipedia.org/wiki/The_Boy_Who_Cried_Wolf>`_"). However, :ref:`recall that there is no free lunch <monitoring_judging_performance>`: you cannot simultaneously have low type I and type II error.

**Changing the subgroup size**: It is perhaps a counterintuitive result that increasing the subgroup size, :math:`n`, leads to a more sensitive detection system for shifts in the mean, because the control limits are pulled in tighter. However, the larger :math:`n` also means that it will take longer to see the detection signal as the subgroup mean is averaged over more raw data points. So there is a trade-off between subgroup size and the run length (time to detection of a signal).

.. _monitoring_mistakes_to_avoid:

Mistakes to avoid
~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: check if the assumption of independence within each subgroup is required

#.	Imagine you are monitoring an aspect of the final product's quality, e.g. viscosity, and you have a product specification that requires that viscosity to be within, say 40 to 60 cP. It is a mistake to place those **specification limits** on the monitoring chart as a guide when to take action. It is also a mistake to use the required specification limits instead of the LCL and UCL. The monitoring chart is to detect abnormal variation in the process and gives a signal on when to take action, not to inspect for quality specifications. You can certainly have another chart for that, but the process monitoring chart's limits are intended to monitor process stability, and these Shewhart stability limits are calculated differently. Ideally the specification limits lie beyond the LCL and UCL action limits.

#.	Shewhart chart limits were calculated with the assumption of **independent subgroups** (e.g. subgroup :math:`i` has no effect on subgroup :math:`i+1`). For a process with mild autocorrelation, the act of creating subgroups, with :math:`n` samples in each group, removes most, if not all, of the relationship between subgroups. However processes with heavy autocorrelation (slow moving processes sampled at a high rate, for example), will have LCL and UCL calculated from equation :eq:`shewhart-limits` that will raise false alarms too frequently. In these cases you can widen the limits, or remove the autocorrelation from the signal. More on this in the later section on :ref:`exponentially weighted moving average (EWMA) charts <monitoring_EWMA>`.

#.	Using Shewhart charts on two or more **highly correlated quality variables**, usually on your final product measurement, can increase your type II (consumer's risk) dramatically. We will come back to this very important topic in the section on :ref:`latent variable models <LVM_monitoring>`, where we will counterintuitively prove that even having individual charts each within their respective limits can result where it is outside the joint limits.

