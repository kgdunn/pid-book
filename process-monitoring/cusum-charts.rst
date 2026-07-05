.. _monitoring_CUSUM_charts:

CUSUM charts
==============

.. index::
	see: cumulative sum; CUSUM

We :ref:`showed earlier <monitoring_sluggish_shewhart_chart>` that the Shewhart chart is not too sensitive to detecting shifts in the mean. Depending on the subgroup size, :math:`n`, we showed that it can take several consecutive samples before a warning or action limit is triggered. The cumulative sum chart, or :index:`CUSUM chart <pair: CUSUM; process monitoring>`, allows more rapid detection of these shifts away from a target value, :math:`T`.

The following equation shows how this chart works.

.. _monitoring_eqn_CUSUM-derivation:

.. math::
	:label: CUSUM-derivation

	S_0 &= (x_0 - T) \\
	S_1 &= (x_0 - T) + (x_1 - T) = S_0 + (x_1 - T) \\
	S_2 &= (x_0 - T) + (x_1 - T) + (x_2 - T) = S_1 + (x_2 - T) \\
	\\
	\text{In general}\qquad S_t &= S_{t-1} + (x_t - T)

.. figure:: ../figures/monitoring/explain-CUSUM.png
	:alt:	../figures/monitoring/explain-CUSUM.R
	:width: 750px
	:align: center
	:scale: 90

Values of :math:`S_t` are the values plotted on the y-axis of a CUSUM chart. Imagine during a period of good, stable, in-control process operation around the target :math:`T`, then these :math:`S_t` numbers are just random errors, with mean of zero. The long-term sum of :math:`S_t` is also zero, as the positive and negative errors keep cancelling out.

So imagine a CUSUM chart where at some time point the process mean shifts up by :math:`\Delta` units, causing future values of :math:`x_t` to be :math:`x_t + \Delta` instead. Now the summation in the last equation of :eq:`CUSUM-derivation` has an extra :math:`\Delta` term added at each step to :math:`S_t`. Every point will build up an accumulation of :math:`\Delta`, which shows up as a positive or negative slope in the CUSUM chart.

The CUSUM chart is extremely sensitive to small changes. The example chart is shown here for a process where the mean is :math:`\mu=20`, and :math:`\sigma=3`. A small shift of :math:`0.4 \times 3 = 1.2` units (i.e from 20 to 21.2) occurs at :math:`t=150`. This shift is almost imperceptible in the raw data (see the 3rd row in the figure). However, the CUSUM chart rapidly picks up the shift by showing a consistent rising slope.

This figure also shows how the CUSUM chart is used with the 2 masks. Notice that there are no lower and upper bounds for :math:`S_t`. A process that is on target will show a "wandering" value of :math:`S`, moving up and down. In fact, as the second row in the figure shows, a surprising amount of movement up and down occurs even when the process is in control.

What is of interest however is a persistent change in slope in the CUSUM chart. The angle of the superimposed :index:`V-mask` is the control limit: the narrower the mouth of the mask, the more sensitive the CUSUM chart is to deviations from the target. Both the type I and II error are set by the angle of the V and the leading distance (the distance from the short vertical line to the apex of the V).

The process is considered in control as long as all points are within the arms of the V shape.  The mask in the second row of the plot shows "in control" behaviour, while the mask in the fourth row detects the process mean has shifted, and an alarm should be raised.

Once the process has been investigated the CUSUM value, :math:`S_t` is often reset to zero; though other resetting strategies exist. A tabular version of the CUSUM chart also exists, and it is the form used in most software systems. Rather than a single sum, it keeps two one-sided sums that accumulate only the deviations beyond a small reference value :math:`K`, and it signals when either sum exceeds a decision interval :math:`H`:

.. math::
	:label: CUSUM-tabular

	C_t^{+} &= \max\left(0,\ C_{t-1}^{+} + (x_t - T) - K\right) \\
	C_t^{-} &= \max\left(0,\ C_{t-1}^{-} - (x_t - T) - K\right)

The :index:`reference value <single: reference value (CUSUM)>` :math:`K` is usually set to half the shift you want to detect: :math:`K = \frac{1}{2}\,\delta\,\sigma` for a shift of :math:`\delta` standard deviations. The :index:`decision interval <single: decision interval (CUSUM)>` :math:`H` is commonly :math:`4\sigma` or :math:`5\sigma`, chosen to give an acceptable in-control average run length. An alarm is raised the first time :math:`C_t^{+} > H` or :math:`C_t^{-} > H`, after which the offending sum is reset to zero. These two parameters, :math:`K` and :math:`H`, play the same role as the angle and lead distance of the V-mask, and are what you will set in software such as Minitab or the R ``qcc`` package.

The purpose of this section is not to provide formulas for the V-mask, only to explain the CUSUM concept to put the next section on EWMA control charts in perspective.
