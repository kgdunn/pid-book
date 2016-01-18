
.. _SECTION_PLS:

Introduction to Projection to Latent Structures (PLS)
========================================================

Projection to Latent Structures (PLS) is the first step we will take to extending latent variable methods to using more than one block of data. In the PLS method we divide our variables (columns) into two blocks: called |X| and |Y|. 

Learning how to choose which variables go in each block will become apparent later, but for now you may use the rule of thumb that says |X| takes the variables which are always available when using the model, while |Y| takes the variables that are *not always available*. Both |X| and |Y| must be available when building the model, but later, when using the model, only |X| is required. As you can guess, one of the major uses of PLS is for predicting variables in |Y| using variables in |X|, but this is not its only purpose as a model. It is a very good model for process understanding and troubleshooting.

PLS can be used for process monitoring and for optimizing the performance of a process. It is also widely used for new product development, or for improving existing products. In all these cases the |Y| block most often contains the outcome, or quality properties.

However, PLS is most commonly used for prediction. And this is also a good way to introduce PLS. In (chemical) engineering processes we use it to develop software sensors (also known as inferential sensors) that predict time-consuming lab measurement in real-time, using the on-line data from our processes. In laboratories we use spectral data (e.g. NIR spectra) to predict the composition of a liquid; this is known as the calibration problem; once calibrated with samples of known composition we can predict the composition of future samples.

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
   
   
..	* page 52 of pencil notes

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
	

..	From Carlos' paper:
		
	Projection to Latent Structures (PLS) is a multivariate regression tool that helps to reveal correlation amongst input-variables or
	predictors (X-space) and also their impact on several responses (Y-space). This is done by separating regularities from noise in
	the data. PLS handles data with strong collinearity, noise and missing values in both the X- and Y-spaces. This tool reduces the
	dimension of the system to smaller number of ‘‘latent variables” (referred to as principal components or scores) that can simultaneously 
	explain the signifiant variance in X, and also predict Y. The higher the correlation in the data the fewer the principal components that 
	are computed. The scores are independent of each other and are a linear combination of the original predictors. The
	weight of each predictor that is used to calculate the scores is directly related to their level of influence on the measured Y-space
	properties. An important aspect of PLS is the ability to show the interrelationship among all predictors, the relationship among all
	responses, and simultaneously the predictors’ influence on the measured responses, all of them in a single plot, the w*c plot. All
	these calculations are usually carried out by first centering the data to have a mean of zero and then scaling to unit variance. 
	This process of mean centering and scaling is done in order to give each variable the same weight and importance prior to the analysis. 
	This is done to counteract the effect of scaling in different measurements units, and to allow each variable to contribute equally to
	the model. As a regression tool, PLS provides a measure of the goodness of ﬁt, R2. R2 is an indication of how much variance in
	the data is explained by the model. R2, for any regression tool, including PLS, can always be increased by adding more terms
	(complexity) to the hypothesized model. A far better metric to gauge model performance is by using the so-called Q2 metric. Q2
	is an indicator that measures how well the regression model can predict new data. One technique to estimate Q2 is by cross-validation. 
	This method consists of dividing the data into a number of groups. Models are built with a group of data left out – one group
	at a time. With each model, the corresponding omitted data are predicted and the total prediction error sum of squares calculated.
	Q2, like R2, varies between 0 and 1, where values closer to 1 indicate better prediction ability. The Q2 value will always be smaller
	than R2. Finally, Q2 is used to select the number of principal components (model complexity) to avoid over-fitting.
	PLS models can be converted to a standard linear regression form as given by the following equation:
	
	:math:`\hat{y} = b_0 + \sum{b_i x_i}`
	
	where k is a constant, bn is the coefﬁcient corresponding to the predictor xn and y is the predicted y-property. Details of the 
	PLS calculations can be found elsewhere [Wold S, Sjöström M, Eriksson L. PLS-regression: a basic tool of chemometrics.
	Chemom Intell Lab Syst 2001;58(2):109–30.]. Several software packages are available to create PLS models. The SIMCA-P software by Umetrics
	was used in this work.
	

