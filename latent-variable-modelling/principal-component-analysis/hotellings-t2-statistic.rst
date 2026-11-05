.. _LVM-Hotellings-T2:

Hotelling's T²
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: Hotelling's T-squared statistic
	see: T-squared statistic; Hotelling's T-squared statistic
	pair: Hotelling's T-squared statistic; principal component analysis

The final quantity from a PCA model that we need to consider is called Hotelling's |T2| value. Some PCA models will have many components, :math:`A`, so an initial screening of these components using score scatterplots will require reviewing :math:`A(A-1)/2` scatterplots. The |T2| value for the :math:`i^\text{th}` observation is defined as:

.. math::
	T^2 = \sum_{a=1}^{a=A}{\left(\dfrac{t_{i,a}}{s_a}\right)^2}

where the :math:`s_a^2` values are constants, and are the variances of each component. The easiest interpretation is that |T2| is a scalar number that summarizes all the score values. Some other properties regarding |T2|:

*	It is a positive number, greater than or equal to zero.
*	It is the distance from the center of the (hyper)plane to the projection of the observation onto the (hyper)plane.
*	An observation that projects onto the model's center (usually the observation where every value is at the mean), has :math:`T^2 = 0`.
*	The limit for |T2| depends on which observations it judges. Below the 95% limit we expect,
	under normal conditions, to find 95% of the observations. For a model built from :math:`N`
	observations with :math:`A` components, the 95% limit for a new observation, one not used to build
	the model, comes from the :math:`F`-distribution:

	.. math::
		T^2_{A, 0.95, \text{new}} = \dfrac{A(N-1)(N+1)}{N(N-A)} \, F_{0.95}(A, N-A)

	where :math:`F_{0.95}(A, N-A)` is the 95th percentile of the :math:`F`-distribution with :math:`A`
	and :math:`N-A` degrees of freedom. The 95% limit for one of the :math:`N` observations used to
	build the model comes from the beta distribution, and is smaller:

	.. math::
		T^2_{A, 0.95, \text{fitted}} = \dfrac{(N-1)^2}{N} \, B_{0.95}\left(\dfrac{A}{2}, \dfrac{N-A-1}{2}\right)

	where :math:`B_{0.95}(a, b)` is the 95th percentile of the beta distribution with shape parameters
	:math:`a` and :math:`b`. Tracy, Young and Mason give both in "Multivariate control charts for
	individual observations", *Journal of Quality Technology*, **24** (2), 88-95, 1992. The section on
	:ref:`why a new observation needs a wider limit <LVM-Hotellings-T2-judged-rows>` explains the
	difference. The 460 tablets in the figure below were used to build the model, so they are drawn
	against the beta limit, at 95% and at 99%.

	.. image:: ../../figures/examples/tablet-spectra/spectral-data-T2-lineplot.png
		:alt: Hotelling's T-squared per tablet against the 95% and 99% limits
		:scale: 80
		:width: 750px
		:align: center

*	It is useful to consider the case when :math:`A=2`, and fix the |T2| value at its 95% limit, for example, call that :math:`T^2_{A=2, \alpha=0.95}`. Using the definition for |T2|:

	.. math::
		T^2_{A=2, \alpha=0.95} = \dfrac{t^2_{1}}{s^2_1} + \dfrac{t^2_{2}}{s^2_2}

	On a scatterplot of :math:`t_1` vs :math:`t_2` for all observations, this would be the equation of an ellipse, centered at the origin. You will often see this ellipse shown on :math:`t_i` vs :math:`t_j` scatterplots of the scores. Points inside this elliptical region are within the 95% confidence limit for |T2|.

*	The same principle holds for :math:`A>2`, except the ellipse is called a hyper-ellipse (think of a rugby-ball shaped object for :math:`A=3`). The general interpretation is that if a point is within this ellipse, then it is also below the |T2| limit, if |T2| were to be plotted on a line.

.. image:: ../../figures/examples/tablet-spectra/spectral-data-t1-t2-scoreplot.png
	:alt: Score plot of the tablet spectra with the 95% and 99% T-squared ellipses
	:scale: 80
	:width: 750px
	:align: center


.. _LVM-Hotellings-T2-judged-rows:

Why a new observation needs a wider T² limit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A new observation needs a wider |T2| limit than an observation used to build the model, because the
:math:`N` observations that build the model also set the centre and the spread that |T2| is measured
against. Each of them takes part in both estimates, and a new observation takes part in neither.

*	**The centre.** The model's centre is the average of the :math:`N` observations, so the variance
	of an observation's deviation from it is :math:`\sigma^2(N-1)/N` for one of them, and
	:math:`\sigma^2(N+1)/N` for a new one.
*	**The spread.** The score variances :math:`s_a^2` are estimated from the same :math:`N`
	observations, so an observation far out along a component raises that component's variance, which
	pulls its own |T2| back.

As a result, the |T2| of an observation used to build the model can never exceed
:math:`(N-1)^2/N`, and it follows the scaled beta distribution. Nothing bounds the |T2| of a new
observation, which follows the heavier tail of the :math:`F`-distribution. For the two limits to
flag the same 5% of observations, the limit for a new observation has to be the larger one.

For a model of :math:`N = 10` observations with :math:`A = 2` components, no observation used to
build it can have a |T2| above :math:`9^2/10 = 8.1`. The 95% limit for those observations is 4.66,
and for a new observation it is 11.04.

A third limit, :math:`A(N-1)/(N-A) \, F_{0.95}(A, N-A)`, is often drawn for the observations used to
build the model. It is the limit for an observation measured against a known centre and a spread
estimated from other observations, so it lies close to the limit for a new observation: 10.03 for
the model of 10 observations. That is more than 8.1, the largest |T2| any of those 10 observations
can have, so this limit can never flag one of them.

The code below computes the three 95% limits, and the largest |T2| of an observation used to build
the model, for three model sizes:

.. code-block:: python

	from scipy import stats

	def t2_limits(n_obs, n_comp, conf_level=0.95):
	    """The beta, middle and F limits for T2, and the largest T2 of a row in the model."""
	    largest = (n_obs - 1) ** 2 / n_obs
	    fitted = largest * stats.beta.ppf(conf_level, n_comp / 2, (n_obs - n_comp - 1) / 2)
	    middle = (n_comp * (n_obs - 1) / (n_obs - n_comp)
	              * stats.f.ppf(conf_level, n_comp, n_obs - n_comp))
	    new = middle * (n_obs + 1) / n_obs
	    return fitted, middle, new, largest

	for n_obs, n_comp in [(10, 2), (20, 2), (50, 3)]:
	    print(n_obs, n_comp, " ".join(f"{v:.2f}" for v in t2_limits(n_obs, n_comp)))
	    # 10 2 4.66 10.03 11.04 8.10
	    # 20 2 5.36 7.50 7.88 18.05
	    # 50 3 7.43 8.76 8.94 48.02

.. list-table:: The 95% limits for |T2|, and the largest |T2| that an observation used to build the
	model can have.
	:header-rows: 1
	:widths: 16 21 21 21 21

	*	- Model
		- Observation used to build the model (beta)
		- :math:`A(N-1)/(N-A) \, F_{0.95}(A, N-A)`
		- New observation (:math:`F`)
		- Largest |T2| of an observation used to build the model
	*	- :math:`N = 10`, :math:`A = 2`
		- 4.66
		- 10.03
		- 11.04
		- 8.10
	*	- :math:`N = 20`, :math:`A = 2`
		- 5.36
		- 7.50
		- 7.88
		- 18.05
	*	- :math:`N = 50`, :math:`A = 3`
		- 7.43
		- 8.76
		- 8.94
		- 48.02

Drawn against :math:`N` for :math:`A = 2`, the three limits show where the third one falls below the
largest |T2| an observation used to build the model can have:

.. code-block:: python

	import numpy as np
	import plotly.graph_objects as go

	# the beta limit needs N > A + 1
	n_obs_range = np.arange(4, 31)
	limit_curves = np.array([t2_limits(n_obs, 2) for n_obs in n_obs_range])
	fig = go.Figure()
	for column, name, dash in [(0, "Observation used to build the model (beta)", "solid"),
	                           (1, "A(N-1)/(N-A) F", "dash"),
	                           (2, "New observation (F)", "solid"),
	                           (3, "Largest T2 of an observation in the model", "dot")]:
	    fig.add_trace(go.Scatter(x=n_obs_range, y=limit_curves[:, column], mode="lines",
	                             name=name, line=dict(dash=dash)))
	fig.update_layout(xaxis_title="Observations used to build the model, N",
	                  yaxis_title="95% limit for T2, A = 2", yaxis_range=[0, 25])
	fig.show()
	# the largest N for which the third limit lies above that bound
	print(n_obs_range[limit_curves[:, 1] > limit_curves[:, 3]].max())
	# 11

.. figure:: ../../figures/pca/hotellings-t2-limits-against-N.png
	:source: pca/hotellings-t2-limits-against-N.py
	:alt: The three 95% limits for T-squared with two components, against the number of observations from 4 to 30, with the largest T-squared an observation used to build the model can have; the middle limit lies above that bound up to 11 observations.
	:scale: 80
	:width: 750px
	:align: center

	The three 95% limits for |T2| of a two-component model, against the number of observations
	:math:`N` used to build it, with the largest |T2| one of those observations can have (dotted).
	Up to :math:`N = 11` the :math:`A(N-1)/(N-A) \, F` limit lies above that bound, so it cannot
	flag any of them. As :math:`N` grows, the three limits approach each other.

The beta and :math:`F` limits are exact when the :math:`A` scores are a fixed set of normally
distributed variables. The scores of a PCA or PLS model are not fixed: the loadings that define them
are calculated from the same :math:`N` observations. For these scores both limits are close
approximations, which improve as :math:`N` grows, and the beta limit still respects the bound
:math:`(N-1)^2/N`.

In ``process_improve``, every function that returns or draws a |T2| limit (``hotellings_t2_limit``,
``ellipse_coordinates``, ``score_plot``, ``t2_plot`` and ``detect_outliers``) takes the argument
``judged_rows``, which says which observations the limit judges. ``judged_rows="fitted"`` gives the
beta limit, for the observations the model was fitted to, such as the points of a score plot or the
values in ``hotellings_t2_``. ``judged_rows="new"`` gives the :math:`F` limit, for observations the
model was not fitted to, such as those projected with ``diagnose``. Every example in this book
passes one of the two.

.. The PCA model as a way to extract information from noise
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..	We saw model is fit by minimizing error. Large error, poorer fit of the data:

		- little systematic (repeatable) variation in the data
		- we inspect the residuals to learn more about the system
			-structure in the residuals?


	X = TP' + E
	- data = information + error
