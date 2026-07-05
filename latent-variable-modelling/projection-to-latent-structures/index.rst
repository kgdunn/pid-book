
.. _SECTION_PLS:

Introduction to Projection to Latent Structures (PLS)
========================================================

.. index::
	single: projection to latent structures (PLS)
	pair: projection to latent structures (PLS); latent variable modelling
	single: X-block
	single: Y-block
	pair: predictor block; projection to latent structures (PLS)
	pair: response block; projection to latent structures (PLS)
	single: multivariate calibration

Projection to Latent Structures (PLS) is the first step we will take to extending latent variable methods to using more than one block of data. In the PLS method we divide our variables (columns) into two blocks: called |X| and |Y|.

Learning how to choose which variables go in each block will become apparent later, but for now you may use the rule of thumb that says |X| takes the variables which are always available when using the model, while |Y| takes the variables that are *not always available*. Both |X| and |Y| must be available when building the model, but later, when using the model, only |X| is required. As you can guess, one of the major uses of PLS is for predicting variables in |Y| using variables in |X|, but this is not its only purpose as a model. It is a very good model for process understanding and troubleshooting.

PLS can be used for process monitoring and for optimizing the performance of a process. It is also widely used for new product development, or for improving existing products. In all these cases the |Y| block most often contains the outcome, or quality properties.

However, PLS is most commonly used for prediction. And this is also a good way to introduce PLS. In (chemical) engineering processes we use it to develop software sensors (also known as inferential sensors) that predict time-consuming lab measurement in real-time, using the on-line data from our processes. In laboratories we use spectral data (e.g. NIR spectra) to predict the composition of a liquid; this is known as the :index:`calibration problem <single: multivariate calibration>`; once calibrated with samples of known composition we can predict the composition of future samples.

But why use the PLS method at all?


.. toctree::
   :maxdepth: 1

   advantages-of-projection-to-latent-structures
   conceptual-mathematical-and-geometric-interpretation-of-pls
   interpreting-pls-scores-and-loadings
   how-the-pls-model-is-calculated
   variability-explained-with-each-component
   coefficient-plots-in-pls
   analysis-of-designed-experiments-using-pls-models
   pls-exercises


..	Comparison of linear regression and projection to latent structures

	Linear regression:
		* Assumes no noise in X
		* No missing data
		* Correlation: resort to variable selection
		* Correlation in X inflates regression coefficient’s confidence interval
		* Single Y-variable only

	Projection to latent structures:
		* No such assumptions
		* Handles missing data
		* No need for variable selection
		* Handles correlated data
		* Handles multiple correlated Y’s

	X-space model: allows us to judge if the X-data are reasonable:
		*	Hotelling’s T2 (on-the-plane metric)
		*	SPE (off-the-plane metric)
		*	If T2 and SPE value are below their limits, then we go ahead and make our prediction with confidence from the new X-vector.

	* MLR shortcomings
