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
	
	\overline{x}_t = \frac{1}{n}x_{t-1} + \frac{1}{n}x_{t-2} + \ldots + \frac{1}{n}x_{t-n}

The EWMA chart is similar to the MA chart, but uses different weights; heavier weights for more recent observations, tailing off exponentially to very small weights further back in history. Let's take a look at a derivation. 

.. todo: Show a Shewhart chart in the second row; use lambda = 0.5 and 0.15 only, then a CUSUM at the bottom

.. figure:: ../figures/monitoring/explain-EWMA.png
	:width: 750px
	:align: center
	:scale: 80

Define the process target as :math:`T`.

.. math:: 
	:label: ewma-derivation-1
	
		\begin{array}{lcrcl}
			\text{Let}  \qquad\qquad && x_t                              &=& \text{new data measurement}\\
			\text{let}  \qquad\qquad && e_t                              &=& x_t - \hat{x}_t \\
			\text{where}			 && \hat{x}_t                        &=& \hat{x}_{t-1} + \lambda e_{t-1} \qquad\qquad \\
			\text{shifting everything one step forward:}&& \hat{x}_{t+1} &=& \hat{x}_{t}   + \lambda e_{t}    \\
		\end{array}

The reason for the :math:`\wedge` mark above the :math:`x_t`, as in :math:`\hat{x}_t`, is that :math:`\hat{x}_t` indicates that it is a prediction of the actual measured :math:`x_t` value. 
		
To start the EWMA sequence we define the value for :math:`\hat{x}_0 = T`, and :math:`e_0 = 0`, so that :math:`\hat{x}_1 = T`. 

An alternative way of writing the above equation gives a new insight into the value of the EWMA value:

.. math:: 
	:label: ewma-derivation-2
	
		\begin{array}{lcrclcl}
			x_t = \text{new data}\qquad		&& \hat{x}_{t+1} &=& \hat{x}_{t}   + \lambda e_{t}\qquad\qquad	& \text{where}\,\, e_t = x_t - \hat{x}_t \\
			\text{Substituting in the error}&& \hat{x}_{t+1} &=& \hat{x}_{t}   + \lambda \left(x_t - \hat{x}_t\right)     \\
											&& \hat{x}_{t+1} &=& \left(1-\lambda \right)\hat{x}_{t}   + \lambda x_t  \\
		\end{array}

That last line shows that a one-step-ahead prediction for :math:`x` at time :math:`t+1` is a weighted sum of two components: the predicted value, :math:`\hat{x}_t`, and the current measured value, :math:`x_t`, weighted to add up to 1. This predictor can be quite valuable in a slow-moving process, to estimate the next value one step into the future.

The plot below shows visually what happens as the weight of :math:`\lambda` is changed. In this example a shift of :math:`\Delta = 1\sigma = 3` units occurs at :math:`t=150`. Prior to that the process mean is :math:`\mu=20` and the raw data has :math:`\sigma = 3`. The EWMA plots show the one-step-ahead prediction value from equation :eq:`ewma-derivation-2`, :math:`\hat{x}_{t+1}` = EWMA value plotted at time :math:`t`.

As :math:`\lambda` gets smaller, the chart is smoother, because as equation :eq:`ewma-derivation-2` shows, less of the current data, :math:`x_t`, is used, and more historical data, :math:`\hat{x}_{t}`, is used. The "memory" of the EWMA statistic is increased. To see why :math:`\hat{x}_{t}` represents historical data, you can recursively substitute and show that:

.. math::
	
	\hat{x}_{t+1} &= \sum_{i=0}^{i=t}{w_i x_i} = w_0x_0 + w_1x_1 + w_2x_2 + \ldots \\
	\text{where the weights are:} \qquad w_i &= \lambda (1-\lambda)^{t-i}

which shows that the one-step-ahead prediction is a just a weighted sum of the raw measurements, with weights declining in time. In the next figure, we show a comparison of the weights used in 4 different monitoring charts studied so far.

From the above discussion and the weights shown for the 4 different charts, it should be clear now how an EWMA chart is a tradeoff between a  Shewhart chart and a CUSUM chart. As :math:`\lambda \rightarrow 1`, the EWMA chart behaves more as a Shewhart chart, giving only weight to the most recent observation. While as :math:`\lambda \rightarrow 0` the EWMA chart starts to have an infinite memory (like a CUSUM chart).

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

where :math:`\sigma_{\text{Shewhart}}` represents the standard deviation as calculated for the Shewhart chart. :math:`K` is usually a value of 3, similar to the 3 standard deviations used in a Shewhart chart, but can of course be set to any level that balances the type I (false alarms) and type II errors (not detecting a deviation which is present already). 

An interesting implementation can be to show both the Shewhart and EWMA plot on the same chart, with both sets of limits. The EWMA value plotted is actually the one-step ahead prediction of the next :math:`x`-value, which can be informative for slow-moving processes.

The R code here shows one way of calculating the EWMA values for a vector of data. Once you have pasted this function into R, use it as ``ewma(x, lambda=..., target=...)``.

.. dcl:: R
	:height: 450px

	ewma <- function(x, lambda, target=x[1]){
	    N <- length(x)
	    y <- numeric(N)
	    y[1] = target
	    for (k in 2:N){
	        error = x[k - 1] - y[k - 1]
	        y[k] = y[k - 1] + lambda*error
	    }
	return(y)
	}
	
	# Try using this function now:
	x <- c(5, 4, 5, 4, 5, 4, 5)
	ewma(x, lambda = 0.6, target = 5)


.. EWMA can detect both changes in level and changes in variance
.. TODO: After introducing concept, show why Shewhart fails with heavy autocorr. Have to increase Shewhart N, or widen the limits.


