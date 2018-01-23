.. _monitoring_CUSUM_charts:

CUSUM charts
==============

We :ref:`showed earlier <monitoring_sluggish_shewhart_chart>` that the Shewhart chart is not too sensitive to detecting shifts in the mean. Depending on the subgroup size, :math:`n`, we showed that it can take several consecutive samples before a warning or action limit is triggered. The cumulative sum chart, or :index:`CUSUM chart <pair: CUSUM; process monitoring>`, allows more rapid detection of these shifts away from a target value, :math:`T`.

.. _monitoring_eqn_CUSUM-derivation:

.. math::
	:label: CUSUM-derivation
	
	S_0 &= (x_0 - T) \\
	S_1 &= (x_0 - T) + (x_1 - T) = S_0 + (x_1 - T) \\
	S_2 &= (x_0 - T) + (x_1 - T) + (x_2 - T) = S_1 + (x_2 - T) \\
	\\
	\text{In general}\qquad S_t &= S_{t-1} + (x_t - T) 

.. TODO: should add Shewhart chart to this to prove its sluggishness

.. figure:: ../figures/monitoring/explain-CUSUM.png
	:alt:	../figures/monitoring/explain-CUSUM.R
	:width: 750px
	:align: center
	:scale: 90
	
Values of :math:`S_t` for an in-control process should really just be random errors, with mean of zero. The long-term sum of :math:`S_t` is also zero, as the positive and negative errors keep cancelling out.

So imagine a CUSUM chart where at some time point the process mean shifts up by :math:`\Delta` units, causing future values of :math:`x_t` to be :math:`x_t + \Delta` instead. Now the summation in the last equation of :eq:`CUSUM-derivation` has an extra :math:`\Delta` term added at each step to :math:`S_t`. Every point will build up an accumulation of :math:`\Delta`, which shows up as a positive or negative slope in the CUSUM chart. 

The CUSUM chart is extremely sensitive to small changes. The example chart is shown here for a process where the mean is :math:`\mu=20`, and :math:`\sigma=3`. A small shift of :math:`0.4 \times 3 = 1.2` units (i.e from 20 to 21.2) occurs at :math:`t=150`. This shift is almost imperceptible in the raw data (see the 3rd row in the figure). However, the CUSUM chart rapidly picks up the shift by showing a consistent rising slope.

This figure also shows how the CUSUM chart is used with the 2 masks. Notice that there are no lower and upper bounds for :math:`S_t`. A process that is on target will show a "wandering" value of :math:`S`, moving up and down. In fact, as the second row shows, a surprising amount of movement up and down occurs even when the process is in control.

What is of interest however is a persistent change in slope in the CUSUM chart. The angle of the superimposed V-mask is the control limit: the narrower the mouth of the mask, the more sensitive the CUSUM chart is to deviations from the target. Both the type I and II error are set by the angle of the V and the leading distance (the distance from the short vertical line to the apex of the V).

The process is considered in control as long as all points are within the arms of the V shape.  The mask in the second row of the plot shows "in control" behaviour, while the mask in the fourth row detects the process mean has shifted, and an alarm should be raised.

Once the process has been investigated the CUSUM value, :math:`S_t` is often reset to zero; though other resetting strategies exist. A tabular version of the CUSUM chart also exists which tends to be the version used in software systems.

The purpose of this section is not to provide formulas for the V-mask or tabular CUSUM charts, only to explain the CUSUM concept to put the next section in perspective.

