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
*	The limit for |T2| comes from the :math:`F`-distribution. Below the 95% limit we expect, under normal conditions, to find 95% of the observations. For a model built from :math:`N` observations with :math:`A` components, the 95% limit for a new observation, one not used to build the model, is

	.. math::
		T^2_{A, 0.95} = \dfrac{A(N-1)(N+1)}{N(N-A)} \, F_{0.95}(A, N-A)

	where :math:`F_{0.95}(A, N-A)` is the 95th percentile of the :math:`F`-distribution with :math:`A` and :math:`N-A` degrees of freedom. This is the limit the ``hotellings_t2_limit`` method of a fitted ``process_improve`` model returns. The observations used to build the model are often plotted against the slightly smaller :math:`A(N-1)/(N-A) \, F_{0.95}(A, N-A)` instead, as in the figure below. Strictly, those observations follow a scaled beta distribution, whose limit is lower still. The first two limits differ only by the factor :math:`(N+1)/N`. The beta limit lies further below, by more when :math:`A` is large relative to :math:`N`. Tracy, Young and Mason derive the new-observation limit and the beta distribution in "Multivariate control charts for individual observations", *Journal of Quality Technology*, **24** (2), 88-95, 1992.

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


.. The PCA model as a way to extract information from noise
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..	We saw model is fit by minimizing error. Large error, poorer fit of the data:

		- little systematic (repeatable) variation in the data
		- we inspect the residuals to learn more about the system
			-structure in the residuals?


	X = TP' + E
	- data = information + error
