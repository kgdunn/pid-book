.. _monitoring_EWMA:

EWMA charts
==============

.. index::
	see: exponentially weighted moving average; EWMA
	pair: EWMA; process monitoring

The two previous charts highlight 2 extremes of monitoring charts. On the one hand, a Shewhart chart assumes each subgroup sample is independent (unrelated) to the next - implying there is no "memory" in the chart. On the other hand, a CUSUM chart has an infinite memory, all the way back to the time the chart was started or reset at :math:`t=0` (see the :ref:`equation in the prior section <monitoring_eqn_CUSUM-derivation>`).

We will see that the EWMA (exponentially weighted moving average) chart spans these two extremes through a single adjustable weight, :math:`\lambda`, chosen between 0 and 1. As :math:`\lambda \rightarrow 1`, the EWMA chart behaves more as a Shewhart chart, giving only weight to the most recent observation. As :math:`\lambda \rightarrow 0`, the EWMA chart starts to have an infinite memory, like a CUSUM chart. Depending on the weight :math:`\lambda`, the user can pick where between these two extremes to operate. The rest of this section derives the chart, shows how :math:`\lambda` sets the weight given to past data, and gives the control limits.

From the moving average to the EWMA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As a stepping stone to the EWMA chart, consider first the simple :index:`moving average` (MA) chart. This chart is used just like a Shewhart chart, except the samples that make up each subgroup are calculated using a moving window of width :math:`n`. The case of :math:`n=5` is shown below.

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

To see why :math:`\hat{x}_{t}` represents historical data, you can recursively substitute and show that:

.. math::

	\hat{x}_{t+1} &= \sum_{i=0}^{i=t}{w_i x_i} = w_0x_0 + w_1x_1 + w_2x_2 + \ldots \\
	\text{where the weights are:} \qquad w_i &= \lambda (1-\lambda)^{t-i}

which emphasizes that the prediction is a just a weighted sum of the raw measurements, with weights declining in time.

The code here shows one way of calculating the EWMA values for a vector of data. Once you have defined the function, use it as ``ewma(x, lam=..., target=...)``. It is reused below, both to generate the comparison figures and in the worked example at the end of this section.

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
	# worked-example table at the end of this section:
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
	# worked-example table at the end of this section:
	x <- c(200, 210, 190, 190, 190, 190)
	ewma(x, lambda = 0.3, target = 200)

The EWMA weights
~~~~~~~~~~~~~~~~~

The next figure compares the weights each chart gives to past observations, for the four charts studied so far. There are 12 data points used in the example, so the CUSUM 'weight' is one twelfth, or :math:`\approx 0.0833`, spread equally over all points. The EWMA weights (here with :math:`\lambda=0.4`) decay geometrically, while the Shewhart chart places all its weight on the single most recent point. The figure makes concrete the trade-off previewed at the start of this section: :math:`\lambda` slides the EWMA between the Shewhart and CUSUM extremes.

.. code-block:: python

	import numpy as np
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	# Weight given to each past observation, newest at lag 0,
	# for the four charts, using 12 data points and lambda = 0.4.
	n_points, lam = 12, 0.4
	lags = np.arange(n_points)
	weights = {
	    "Shewhart": np.where(lags == 0, 1.0, 0.0),
	    "Moving average (n=5)": np.where(lags < 5, 1 / 5, 0.0),
	    f"EWMA (lambda={lam})": lam * (1 - lam) ** lags,
	    "CUSUM": np.full(n_points, 1 / n_points),  # 1/12 = 0.0833
	}

	fig = make_subplots(rows=2, cols=2, subplot_titles=list(weights))
	for i, (name, w) in enumerate(weights.items()):
	    row, col = divmod(i, 2)
	    fig.add_trace(go.Bar(x=lags, y=w), row=row + 1, col=col + 1)
	fig.update_layout(showlegend=False,
	                  title="Weight given to each past observation "
	                        "(lag 0 = most recent)")
	fig.show()

.. image:: ../figures/monitoring/explain-weights-for-process-monitoring.png
	:alt: ../figures/monitoring/explain-weights-for-process-monitoring.R
	:width: 900px
	:align: center
	:scale: 65

.. FAKE WIDTH ABOVE

Control limits for the EWMA chart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The upper and lower control limits for the EWMA plot are plotted in the same way as the Shewhart limits, but calculated differently:

.. math::
	:label: ewma-limits

	\begin{array}{rcccl}
		 \text{LCL} = \overline{\overline{x}} - L \cdot \sigma_{\text{Shewhart}}\sqrt{\frac{\displaystyle \lambda}{\displaystyle 2-\lambda}} &&  &&  \text{UCL} = \overline{\overline{x}} + L \cdot \sigma_{\text{Shewhart}} \sqrt{\frac{\displaystyle \lambda}{\displaystyle 2-\lambda}}
	\end{array}

where :math:`\sigma_{\text{Shewhart}}` represents the standard deviation as calculated for the Shewhart chart; for individual observations (subgroup size 1, as in the example below) this is simply the process standard deviation :math:`\sigma`. The multiplier :math:`L` is usually a value of 3, similar to the 3 standard deviations used in a Shewhart chart, but can of course be set to any level that balances the type I (false alarms) and type II errors (not detecting a deviation which is present already). We write :math:`L` rather than :math:`K` to avoid a clash with the CUSUM reference value :math:`K` of the :ref:`previous section <monitoring_CUSUM_charts>`.

The limits in equation :eq:`ewma-limits` are the steady-state limits. For the first few points the exact standard deviation of :math:`\hat{x}_t` is smaller, by the factor :math:`\sqrt{1-(1-\lambda)^{2t}}`, so many software packages draw limits that start narrower and widen to the steady-state value within a handful of samples.

The next plot shows visually what happens as the weight of :math:`\lambda` is changed. In this example a shift of :math:`\Delta = 1\sigma = 3` units occurs abruptly at :math:`t=150`. This is of course not known in practice, but the purpose here is to illustrate the effects of choosing :math:`\lambda`. Prior to that change the process mean is :math:`\mu=20` and the raw data has :math:`\sigma = 3`.

The first chart is the raw data and also a Shewhart chart with subgroup size of 1; the control limits are at :math:`\pm 3` times the standard deviation, so at 11.0 and 29.0 units. This control chart barely picks up the shift, as was explained in a :ref:`prior section <monitoring_shewart_chart_slugishness>`.

The second, third and fourth charts are EWMA charts with different values of :math:`\lambda`; the line is the value on the left-hand side of equation :eq:`ewma-derivation-2`, in other words it is :math:`\hat{x}_{t+1}`, the EWMA value at time :math:`t`. We see that as :math:`\lambda` decreases, the charts are smoother, since the averaging effect is greater: more and more weight is given to the history, :math:`\hat{x}_{t}`, and less weight to the current data point, :math:`x_t`. The control limits also become narrower as :math:`\lambda` decreases: the half-width in equation :eq:`ewma-limits` above is proportional to :math:`\sqrt{\lambda/(2-\lambda)}`, which shrinks as :math:`\lambda \rightarrow 0`.

The final chart of the sequence of 5 charts is a CUSUM chart, which is :ref:`the ideal chart <monitoring_CUSUM_charts>` for picking up such an abrupt shift in the level.

.. code-block:: python

	# Reuse the seeded series (base, mu, sigma, shift_at) from the
	# CUSUM section, now with a larger shift of 1 sigma = 3 units.
	data_shift = base.copy()
	data_shift[shift_at:] += 1.0 * sigma

	titles = ("Raw data (also a Shewhart chart, subgroup size 1)",
	          "EWMA with lambda = 0.8", "EWMA with lambda = 0.4",
	          "EWMA with lambda = 0.1", "CUSUM")
	fig = make_subplots(rows=5, cols=1, subplot_titles=titles)
	fig.add_trace(go.Scatter(y=data_shift, mode="lines"), row=1, col=1)
	fig.add_hline(y=mu - 3 * sigma, line_color="red", row=1, col=1)
	fig.add_hline(y=mu + 3 * sigma, line_color="red", row=1, col=1)
	for row, lam in ((2, 0.8), (3, 0.4), (4, 0.1)):
	    half_width = 3 * sigma * np.sqrt(lam / (2 - lam))
	    fig.add_trace(go.Scatter(y=ewma(data_shift, lam, target=mu),
	                             mode="lines"), row=row, col=1)
	    fig.add_hline(y=mu - half_width, line_color="red", row=row, col=1)
	    fig.add_hline(y=mu + half_width, line_color="red", row=row, col=1)
	fig.add_trace(go.Scatter(y=np.cumsum(data_shift - mu), mode="lines"),
	              row=5, col=1)
	for row in range(1, 6):
	    fig.add_vline(x=shift_at, line_dash="dash", row=row, col=1)
	fig.update_layout(height=1200, showlegend=False)
	fig.show()

.. figure:: ../figures/monitoring/explain-EWMA.png
	:width: 750px
	:align: center
	:scale: 80

An interesting implementation can be to show both the Shewhart and EWMA plot on the same chart, with both sets of limits. The EWMA value plotted is actually the one-step ahead prediction of the next :math:`x`-value, which can be informative for slow-moving processes.

.. EWMA can detect both changes in level and changes in variance
.. TODO: After introducing concept, show why Shewhart fails with heavy autocorr. Have to increase Shewhart N, or widen the limits.

Worked example
~~~~~~~~~~~~~~~

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
