.. _monitoring_EWMA:

EWMA charts
==============

.. index::
	see: exponentially weighted moving average; EWMA
	pair: EWMA; process monitoring

The two previous charts highlight 2 extremes of monitoring charts. On the one hand, a Shewhart chart assumes each subgroup sample is independent (unrelated) to the next - implying there is no "memory" in the chart. On the other hand, a CUSUM chart has an infinite memory, all the way back to the time the chart was started or reset at :math:`t=0` (see the :ref:`equation in the prior section <monitoring_eqn_CUSUM-derivation>`).

As an introduction to the exponentially weighted moving average (EWMA) chart, consider first the simple :index:`moving average` (MA) chart. This chart is used just like a Shewhart chart, except the samples that make up each subgroup are calculated using a moving window of width :math:`n`. The case of :math:`n=5` is shown below.

.. image:: ../figures/monitoring/explain-moving-average-data-source.png
	:width: 800px
	:align: left
	:scale: 50
	:alt: fake width

The MA chart plots values of :math:`\overline{x}_t`, calculated from groups of size :math:`n`, using equal weight for each of the :math:`n` most recent raw data.

.. math::

	\overline{x}_t = \frac{1}{n}x_{t} + \frac{1}{n}x_{t-1} + \ldots + \frac{1}{n}x_{t-n+1}

The EWMA chart is similar to the MA chart, but uses different weights; heavier weights for more recent observations, tailing off exponentially to very small weights further back in history. Let's take a look at a derivation.

Define the process target as :math:`T` and define :math:`x_t` as a new data measurement arriving now. We then try to *create an estimate of that incoming value, giving some weight*, :math:`\lambda`, *to the actual measured value, and the rest of the weight*, :math:`1-\lambda`, *to the prior estimate*.

Let us write this estimate as :math:`\hat{x}_t`, with the :math:`\wedge` mark above the :math:`x_t` to indicate that it is the EWMA estimate of the level at time :math:`t`: a smoothed value that blends the latest measurement with the running history. The prior estimate is therefore written as :math:`\hat{x}_{t-1}`. As shown below, this same smoothed value also serves as the one-step-ahead forecast of the next measurement.

So putting into equation form that "an estimate of that incoming value, is given by some weight, :math:`\lambda` and the rest of the weight, :math:`1-\lambda`, to the prior estimate":

.. math::
	:label: ewma-derivation-2

		\begin{array}{rcl}
			\hat{x}_{t} &=& \lambda x_t + \left(1-\lambda \right)\hat{x}_{t-1} \\
			\hat{x}_{t} &=& \hat{x}_{t-1} +\lambda \left( x_t -\hat{x}_{t-1} \right)   \\
			\hat{x}_{t+1} &=& \hat{x}_{t} +\lambda \left( x_{t+1} -\hat{x}_{t} \right)  \\
			\hat{x}_{t+1} &=& \lambda  x_{t+1} +\left(1-\lambda \right)  \hat{x}_{t}
		\end{array}

To start the EWMA sequence we define the value for :math:`\hat{x}_0 = T` and :math:`\hat{x}_1 = \lambda x_1 + T \left(1-\lambda \right)`. A worked example is given further on in this section.

The last line in the equation group above shows that a 1-step-ahead prediction for :math:`x` at time :math:`t+1` is a weighted sum of two components: the current measured value, :math:`x_t`, and secondly the predicted value, :math:`\hat{x}_t`, with the weights summing up to 1. This gives a way to experimentally find a suitable :math:`\lambda` value from historical data: adjust it up and down until the differences between :math:`\hat{x}_{t+1}` and the actual measured values of :math:`x_{t+1}` are small.

The next plot shows visually what happens as the weight of :math:`\lambda` is changed. In this example a shift of :math:`\Delta = 1\sigma = 3` units occurs abruptly at :math:`t=150`. This is of course not known in practice, but the purpose here is to illustrate the effects of choosing :math:`\lambda`. Prior to that change the process mean is :math:`\mu=20` and the raw data has :math:`\sigma = 3`.

The first chart is the raw data and also a Shewhart chart with subgroup size of 1; the control limits are at :math:`\pm 3` times the standard deviation, so at 11.0 and 29.0 units. This control chart barely picks up the shift, as was explained in a :ref:`prior section <monitoring_shewart_chart_slugishness>`.

The second, third and fourth charts are EWMA charts with different values of :math:`\lambda`; the line is the value on the left-hand side of equation :eq:`ewma-derivation-2`, in other words it is :math:`\hat{x}_{t+1}`, the EWMA value at time :math:`t`. We see that as :math:`\lambda` decreases, the charts are smoother, since the averaging effect is greater: more and more weight is given to the history, :math:`\hat{x}_{t}`, and less weight to the current data point, :math:`x_t`.  See equation :eq:`ewma-derivation-2` to understand that interpretation. Also note carefully how the control limits become narrower as the :math:`\lambda` decreases, as is explained shortly below.

To see why :math:`\hat{x}_{t}` represents historical data, you can recursively substitute and show that:

.. math::

	\hat{x}_{t+1} &= \sum_{i=0}^{i=t}{w_i x_i} = w_0x_0 + w_1x_1 + w_2x_2 + \ldots \\
	\text{where the weights are:} \qquad w_i &= \lambda (1-\lambda)^{t-i}

which emphasizes that the prediction is a just a weighted sum of the raw measurements, with weights declining in time.

The final chart of the sequence of 5 charts is a CUSUM chart, which is :ref:`the ideal chart <monitoring_CUSUM_charts>` for picking up such an abrupt shift in the level.

.. figure:: ../figures/monitoring/explain-EWMA.png
	:width: 750px
	:align: center
	:scale: 80

In the next figure, we show a comparison of the weights used in different monitoring charts studied so far.

From the above discussion and the weights shown for the 4 different charts, it should be clear now how an EWMA chart is a tradeoff between a Shewhart chart and a CUSUM chart. As :math:`\lambda \rightarrow 1`, the EWMA chart behaves more as a Shewhart chart, giving only weight to the most recent observation. While as :math:`\lambda \rightarrow 0` the EWMA chart starts to have an infinite memory (like a CUSUM chart). There are 12 data points used in the example, so the CUSUM 'weight' is one twelfth or :math:`\approx 0.0833`.

.. image:: ../figures/monitoring/explain-weights-for-process-monitoring.png
	:alt: ../figures/monitoring/explain-weights-for-process-monitoring.R
	:width: 900px
	:align: center
	:scale: 65

.. FAKE WIDTH ABOVE

The upper and lower control limits for the EWMA plot are plotted in the same way as the Shewhart limits, but calculated differently:

.. math::
	:label: ewma-limits

	\begin{array}{rcccl}
		 \text{LCL} = \overline{\overline{x}} - K \cdot \sigma_{\text{Shewhart}}\sqrt{\frac{\displaystyle \lambda}{\displaystyle 2-\lambda}} &&  &&  \text{UCL} = \overline{\overline{x}} + K \cdot \sigma_{\text{Shewhart}} \sqrt{\frac{\displaystyle \lambda}{\displaystyle 2-\lambda}}
	\end{array}

where :math:`\sigma_{\text{Shewhart}}` represents the standard deviation as calculated for the Shewhart chart; for individual observations (subgroup size 1, as in the example above) this is simply the process standard deviation :math:`\sigma`. :math:`K` is usually a value of 3, similar to the 3 standard deviations used in a Shewhart chart, but can of course be set to any level that balances the type I (false alarms) and type II errors (not detecting a deviation which is present already).

The limits in equation :eq:`ewma-limits` are the steady-state limits. For the first few points the exact standard deviation of :math:`\hat{x}_t` is smaller, by the factor :math:`\sqrt{1-(1-\lambda)^{2t}}`, so many software packages draw limits that start narrower and widen to the steady-state value within a handful of samples.

An interesting implementation can be to show both the Shewhart and EWMA plot on the same chart, with both sets of limits. The EWMA value plotted is actually the one-step ahead prediction of the next :math:`x`-value, which can be informative for slow-moving processes.

The code here shows one way of calculating the EWMA values for a vector of data. Once you have defined the function, use it as ``ewma(x, lam=..., target=...)``.

.. code-block:: python

	import numpy as np

	def ewma(x, lam, target=None):
	    if target is None:
	        target = x[0]
	    y = np.zeros(len(x))
	    previous = target
	    for k in range(len(x)):
	        y[k] = lam * x[k] + (1 - lam) * previous
	        previous = y[k]
	    return y

	# Try using this function now. It reproduces the
	# worked-example table below:
	x = np.array([200, 210, 190, 190, 190, 190])
	ewma(x, lam=0.3, target=200)

.. code-block:: r

	ewma <- function(x, lambda, target=x[1]){
	    N <- length(x)
	    y <- numeric(N)
	    previous <- target
	    for (k in 1:N){
	        y[k] = lambda*x[k] + (1 - lambda)*previous
	        previous = y[k]
	    }
	return(y)
	}

	# Try using this function now. It reproduces the
	# worked-example table below:
	x <- c(200, 210, 190, 190, 190, 190)
	ewma(x, lambda = 0.3, target = 200)


.. EWMA can detect both changes in level and changes in variance
.. TODO: After introducing concept, show why Shewhart fails with heavy autocorr. Have to increase Shewhart N, or widen the limits.

Here is a worked example, starting with the assumption the process is at the target value of :math:`T = 200` units, and :math:`\lambda=0.3`. We intentionally show what happens if the new value stays fixed at 190: you see the value plotted gets only a weight of 0.3, while the 0.7 weight is for the prior historical value. Slowly the value plotted catches up, but there is always a lag. The value plotted on the chart is from the first equation in the set of :eq:`ewma-derivation-2`, namely :math:`\hat{x}_t = \lambda x_t + (1-\lambda)\hat{x}_{t-1}`.

============= ==================== ==================================================
Sample number Raw data :math:`x_t` Value plotted on chart: :math:`\hat{x}_t`
============= ==================== ==================================================
0             NA                   200
1             200                  :math:`0.3 \times 200 + 0.7 \times 200 = 200`
2             210                  :math:`0.3 \times 210 + 0.7 \times 200 = 203`
3             190                  :math:`0.3 \times 190 + 0.7 \times 203 = 199.1`
4             190                  :math:`0.3 \times 190 + 0.7 \times 199.1 = 196.4`
5             190                  :math:`0.3 \times 190 + 0.7 \times 196.4 = 194.5`
6             190                  :math:`0.3 \times 190 + 0.7 \times 194.5 = 193.1`
============= ==================== ==================================================
