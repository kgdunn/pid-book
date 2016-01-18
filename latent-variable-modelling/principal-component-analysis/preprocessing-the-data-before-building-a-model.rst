.. _LVM_preprocessing:

Preprocessing the data before building a model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The previous sections of this chapter considered the interpretation of a PCA latent variable model. From this section onwards we return to filling important gaps in our knowledge. There are 3 major steps to building any latent variable models:

	#.	Preprocessing the data 
	#.	Building the latent variable model in the :ref:`algorithms section <LVM_algorithms_for_PCA>`
	#.	:ref:`Testing the model <LVM_testing_PCA_models>`, including testing for the number of components to use.
	
We discuss the first step in this section, and the next two steps after that.

There are a number of possibilities for data preprocessing. We mainly discuss centering and scaling in this section, but outline a few other tools first. These steps are usually univariate, i.e. they are applied separately to each column in the raw data matrix |Xraw|. We call the matrix of preprocessed data |X|, this is the matrix that is then presented to the algorithm to build the latent variable model. Latent variable algorithms seldom work on the raw data.

**Transformations**

	The columns in |Xraw| can be transformed: log, square-root and various powers (-1, -0.5, 0.5, 2) are popular options. These are used to reduce the effect of extreme measurements (e.g. log transforms), or because the transformed variable is known to be more correlated with the other variables. An example of this is in a distillation column: the inverse temperature is known to more correlated to the vapour pressure, which we know from first-principles modelling. Using the untransformed variable will lead to an adequate model, but the transformed variable, e.g. using the inverse temperature, can lead to a better model.
	
	The tools we considered earlier on visualization and univariate distributions (histograms) can help assess which variables require transformation. But one's knowledge of the system is the most useful guide for knowing which transformations to apply. Note: latent variable modes do not require each column in |Xraw| to be normally distributed: any type of quantitative variable may be used.

**Expanding the X-matrix**

	Additional columns can and should be added to the |X|-matrix.  This is frequently done in engineering systems where we can augment |Xraw| with columns containing heat, mass, and energy balances. It might be useful to add certain dimensionless numbers or other quantities that can be derived from the raw data. 

	Another step that is applied, usually to experimental data, is to add square and cross terms. For example, if 3 of the columns in |Xraw| were from a factorial designed experiment with center points, then augment |Xraw| with columns containing interaction terms: :math:`x_1x_2, \,\, x_1x_3, \,\, x_2x_3`. If face points or axial points (such as from a central composite design) were used, then also add the square terms to estimate the quadratic effects: :math:`x_1^2, \,\, x_2^2, \,\, x_3^2`. When studying experimental data with latent variable methods (PCA or PLS), also add columns related to measured disturbance variables, often called :index:`covariates`, and :index:`blocking` variables - you won't know if they are important if they are not included.

	The *general rule* is: add as many columns into |Xraw| as possible for the initial analysis. You can always prune out the columns later on if they are shown to be uninformative.

	..	** Shifting rows: lagging **

		COME BACK TO THIS LATER

		Recall that latent variable models such as PCA consider the data in each row of |Xraw| as one unit. But when considering data from chemical plants or larger scale systems, it is not uncommon that there are time-delays. This means that certain columns in |Xraw| will have 

		.. TODO lagging picture here

**Dealing with outliers**

	Users often go through a phase of pruning outliers prior to building a latent variable model.  There are often *uninteresting* outliers, for example when a temperature sensor goes off-line and provides a default reading of 0.0 instead of its usual values in the range of 300 to 400K.  The automated tools used to do this are known by names such as trimming and winsorizing. These tools remove the upper and lower :math:`\alpha` percent of the column's tails on the histogram. But care should be taken with these automated approaches, since the most interesting observations are often in the outliers. 

	The course of action when removing outliers is to always mark their values as missing just for that variable in |Xraw|, rather than removing the entire row in |Xraw|. We do this because we can use the algorithms to calculate the latent variable model when missing data are present within a row.

**Centering**

	:index:`Centering <single: centering>` moves the coordinate system to a new reference point, usually the origin of the coordinate system in :math:`K` variables (i.e. in :math:`K`-dimensional space). Mean centering is effective and commonly used: after mean centering the mean of every column in |Xraw| will be exactly 0.0. An example of mean centering was given in the :ref:`food texture example <LVM_food_texture_example>`.

	As we learned in the section on :ref:`univariate data analysis <SECTION-univariate-review>`, the mean has a low resistance to outliers: any large outlier will distort the value of the mean. So users often resort to trimming their data and then mean centering. In this regard, centering each column around its median is a better choice. We recommend :index:`median centering <single: centering, about median>` as it avoids the trimming step, and simultaneously highlights any outliers.
	
	In the paper by `Bro and Smilde on centering and scaling <http://dx.doi.org/10.1002/cem.773>`_ they show how centering is far more influential on the model than scaling. Centering can be seen as adding a new principal component to the model, while scaling has much less of an effect. 
	
**Scaling**

	:index:`Scaling <single: scaling>` is an important step in latent variable modelling. Scaling can be seen as a way of assigning weights, or relative importance, to each column in |Xraw|. If we don't know much about our data, then it is common to assign an equal weight to each column. We can do this by simply dividing each column by its standard deviation. After this scaling each column will have variance (and standard deviation) of exactly 1.0. This allows each column an equal opportunity of contributing to the model.

	This sort of scaling is called unit-variance scaling. When combined with mean centering you will see the terminology that the data have been :index:`autoscaled`. 

	Imagine a variable that is mostly constant, just noise. It will have a small standard deviation. When dividing by the standard deviation we artificially inflate its variance to the level of the other, truly-varying variables. These noisy, uninformative variables can be removed from |Xraw|, or they can simply be multiplied by a smaller weight, so that their variance after preprocessing is less than 1.0. Such variables will also have small loading coefficients in all components, so they will be discovered during model investigation, if not sooner.

	One could use the median absolute deviation (MAD) instead of the standard deviation to scale the columns, but it most cases, any approximate scaling vector will work adequately (see the Bro and Smilde paper referenced earlier).

