.. _LVM-Hotellings-T2:

Hotelling's T²
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final quantity from a PCA model that we need to consider is called Hotelling's |T2| value. Some PCA models will have many components, :math:`A`, so an initial screening of these components using score scatterplots will require reviewing :math:`A(A-1)/2` scatterplots. The |T2| value for the :math:`i^\text{th}` observation is defined as:

.. math::
	T^2 = \sum_{a=1}^{a=A}{\left(\dfrac{t_{i,a}}{s_a}\right)^2}
	
where the :math:`s_a^2` values are constants, and are the variances of each component. The easiest interpretation is that |T2| is a scalar number that summarizes all the score values. Some other properties regarding |T2|:

*	It is a positive number, greater than or equal to zero.
*	It is the distance from the center of the (hyper)plane to the projection of the observation onto the (hyper)plane.
*	An observation that projects onto the model's center (usually the observation where every value is at the mean), has :math:`T^2 = 0`.
*	The |T2| statistic is distributed according to the :math:`F`-distribution and is calculated by the multivariate software package being used. For example, we can calculate the 95% confidence limit for |T2|, below which we expect, under normal conditions, to locate 95% of the observations.

	.. image:: ../../figures/examples/tablet-spectra/spectral-data-T2-lineplot.png
		:alt:	../../figures/examples/tablet-spectra/spectral-data.R
		:scale: 80
		:width: 750px
		:align: center

*	It is useful to consider the case when :math:`A=2`, and fix the |T2| value at its 95% limit, for example, call that :math:`T^2_{A=2, \alpha=0.95}`. Using the definition for |T2|:

	.. math::
		T^2_{A=2, \alpha=0.95} = \dfrac{t^2_{1}}{s^2_1} + \dfrac{t^2_{2}}{s^2_2}
		
	On a scatterplot of :math:`t_1` vs :math:`t_2` for all observations, this would be the equation of an ellipse, centered at the origin. You will often see this ellipse shown on :math:`t_i` vs :math:`t_j` scatterplots of the scores. Points inside this elliptical region are within the 95% confidence limit for |T2|. 
	
*	The same principle holds for :math:`A>2`, except the ellipse is called a hyper-ellipse (think of a rugby-ball shaped object for :math:`A=3`). The general interpretation is that if a point is within this ellipse, then it is also below the |T2| limit, if |T2| were to be plotted on a line.

.. image:: ../../figures/examples/tablet-spectra/spectral-data-t1-t2-scoreplot.png
	:alt:	../../figures/examples/tablet-spectra/spectral-data.R
	:scale: 80
	:width: 750px
	:align: center
	
	
.. Take a look at Anderson, 1958 (An introduction to multivariate statistical analysis). Paper by MacGregor (http://dx.doi.org/10.1002/aic.690400509) cites this as the distribution for T2, with F as 2 and 48 DOF (2=because PC1 and PC2, and 48 = 50-2, where N=50 and A=2).
	

.. The PCA model as a way to extract information from noise
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..	We saw model is fit by minimizing error. Large error, poorer fit of the data:

		- little systematic (repeatable) variation in the data
		- we inspect the residuals to learn more about the system
			-structure in the residuals?
		

	X = TP' + E
	- data = information + error
