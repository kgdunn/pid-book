.. _SECTION_PCA:

Principal Component Analysis (PCA)
=================================================================================


.. Next sections must address:

	Which variables should you use, and how many observations do you require?
	
	Add a part about the biplot:
	
	*	Gabriel, K. R. (1971). The biplot graphical display of matrices with applications to principal component analysis. Biometrika, 58, 453–467.
	*	Gabriel, K. R. and Odoroff, C. L. (1990). Biplots in biomedical research. Statistics in Medicine, 9, 469–485.
	*	J.C. Gower and D.J. Hand. Biplots. Number 54 in Monographs on Statistics and Applied Probability. Chapman and Hall, London, UK, 1996.



Principal component analysis, PCA, builds a model for a matrix of data.

A model is always an approximation of the system from where the data came. The objectives for which we use that model :ref:`can be varied <LVM_extracting_value_from_data>`. 

In this section we will start by visualizing the data as well as consider a simplified, geometric view of what a PCA model look like. A mathematical analysis of PCA is also required to get a deeper understanding of PCA, so we go into some detail on that point, however it can be skipped on first reading.

The first part of this section emphasizes the general interpretation of a PCA model, since this is a required step that any modeller will have to perform. We leave to the :ref:`second half of this section <LVM_preprocessing>` the important details of how to preprocess the raw data, how to actually calculate the PCA model, and how to validate and test it. This "reverse" order may be unsatisfying for some, but it helpful to see how to use the model first, before going into details on its calculation.

.. toctree::
   :maxdepth: 1

   visualizing-multivariate-data
   geometric-explanation-of-pca
   mathematical-derivation-for-pca
   more-about-the-direction-vectors-loadings
   pca-example-food-texture-analysis
   interpreting-score-plots-and-loading-plots
   predicted-values-for-each-observation
   interpreting-the-residuals
   pca-example-analysis-of-spectral-data
   hotellings-t2-statistic
   preprocessing-the-data-before-building-a-model
   algorithms-to-calculate-build-pca-models
   testing-the-pca-model
   determining-the-number-of-components-to-use-in-the-model-with-cross-validation
   some-properties-of-pca-models
   latent-variable-contribution-plots
   using-indicator-variables-in-a-latent-variable-model
   visualization-latent-variable-models-with-linking-and-brushing
   pca-exercises
   
   
   
