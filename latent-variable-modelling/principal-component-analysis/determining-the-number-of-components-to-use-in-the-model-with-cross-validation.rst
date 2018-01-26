.. _LVM_number_of_components:

Determining the number of components to use in the model with cross-validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..	Any recorded values we have from a system, in |X|, can be broken down into 2 parts: the data structure that is systematic, :math:`\mathbf{TP}'`, and an error component, :math:`\textbf{E}`.

.. The problem of determining "*how many components*" is related to knowing when we have extracted all the systematic variables from the data, |X|, into the latent variable model, :math:`\mathbf{TP}'`. Step back for a minute and think what that means: it says we should stop adding latent variables to the model when there is no more systematic correlation remaining between the variables in |X|. That's all the PCA does: extract the variability in |X|. We should stop adding components when we have extracted, *reproducibly*, all systematic variation.

..	- scree plot
..	- size of eigenvalue: :math:`\sum_a^{a=K}{\lambda_a} = K`
..	- cross-validation: page 49 of pencil notes
	
.. Review the ICS-L newsgroup postings around September 2009.

.. Check Q2 values: in ProMV they keep increasing, never decreasing.

:index:`Cross-validation <single: cross-validation>` is a general tool that helps to avoid over-fitting - it can be applied to any model, not just latent variable models.

As we add successive components to a model we are increasing the size of the model, |A|, and we are explaining the model-building data, |X|, better and better. (The equivalent in least squares models would be to add additional :math:`\mathbf{X}`-variable terms to the model.) The model's :math:`R^2` value will increase with every component. As the following equation shows, the variance of the :math:`\widehat{\mathbf{X}}` matrix increases with every component, while the residual variance in matrix :math:`\mathbf{E}` must decrease.

.. math::
	\mathbf{X} &= \mathbf{TP'} + \mathbf{E}  \\
	\mathbf{X} &= \widehat{\mathbf{X}} + \mathbf{E}  \\
	\mathcal{V}(\mathbf{X}) &= \mathcal{V}(\widehat{\mathbf{X}}) + \mathcal{V}(\mathbf{E})

This holds for any model where the :math:`\widehat{\mathbf{X}}` and :math:`\mathbf{E}` matrices are completely orthogonal to each other: :math:`\widehat{\mathbf{X}}'\mathbf{E} = \mathbf{0}` (a matrix of zeros), such as in PCA, PLS and least squares models.

.. Also see "../../figures/pca/testing-orthogonality-of-Xhat-and-E.R" for a quick test of this

There comes a point for any real data set where the number of components, |A| = the number of columns in :math:`\mathbf{T}` and :math:`\mathbf{P}`, extracts all systematic variance from :math:`\mathbf{X}`, leaving unstructured residual variance in :math:`\mathbf{E}`. Fitting any further components will start to fit this noise, and unstructured variance, in :math:`\mathbf{E}`.

Cross-validation for multivariate data sets was described by Svante Wold in his paper on `Cross-validatory estimation of the number of components in factor and principal components models <http://www.jstor.org/stable/1267639>`_, in *Technometrics*, **20**, 397-405, 1978. 

The general idea is to divide the matrix |X| into :math:`G` groups of rows. These rows should be selected randomly, but are often selected in order: row 1 goes in group 1, row 2 goes in group 2, and so on. We can collect the rows belonging to the first group into a new matrix called :math:`\mathbf{X}_{(1)}`, and leave behind all the other rows from all other groups, which we will call group :math:`\mathbf{X}_{(-1)}`. So in general, for the :math:`g^\text{th}` group, we can split matrix |X| into :math:`\mathbf{X}_{(g)}` and :math:`\mathbf{X}_{(-g)}`.

Wold's cross-validation procedure asks to build the PCA model on the data in :math:`\mathbf{X}_{(-1)}` using |A| components. Then use data in :math:`\mathbf{X}_{(1)}` as new, testing data. In other words, we preprocess the :math:`\mathbf{X}_{(1)}` rows, calculate their score values, :math:`\mathbf{T}_{(1)} = \mathbf{X}_{(1)} \mathbf{P}`, calculate their predicted values, :math:`\widehat{\mathbf{X}}_{(1)} = \mathbf{T}_{(1)} \mathbf{P'}`, and their residuals, :math:`\mathbf{E}_{(1)} = \mathbf{X}_{(1)} - \widehat{\mathbf{X}}_{(1)}`.  We repeat this process, building the model on :math:`\mathbf{X}_{(-2)}` and testing it with :math:`\mathbf{X}_{(2)}`, to eventually obtain :math:`\mathbf{E}_{(2)}`.

After repeating this on :math:`G` groups, we gather up :math:`\mathbf{E}_{1}, \mathbf{E}_{2}, \ldots, \mathbf{E}_{G}` and assemble a type of residual matrix, :math:`\mathbf{E}_{A,\text{CV}}`, where the |A| represents the number of components used in each of the :math:`G` PCA models. The :math:`\text{CV}` subscript indicates that this is not the usual error matrix, :math:`\mathbf{E}`. From this we can calculate a type of :math:`R^2` value. We don't call this :math:`R^2`, but it follows the same definition for an :math:`R^2` value. We will call it :math:`Q^2_A` instead, where |A| is the number of components used to fit the :math:`G` models.

.. math::
	Q^2_A = 1 - \dfrac{\text{Var}(\mathbf{E}_{A, \text{CV}})}{\text{Var}(\mathbf{X})}
	
We also calculate the usual PCA model on all the rows of |X| using |A| components, then calculate the usual residual matrix, :math:`\mathbf{E}_A`. This model's :math:`R^2` value is:

.. math::
	R^2_A = 1 - \dfrac{\text{Var}(\mathbf{E}_A)}{\text{Var}(\mathbf{X})}
	
The :math:`Q^2_A` behaves exactly as :math:`R^2`, but with two important differences. Like :math:`R^2`, it is a number less than 1.0 that indicates how well the testing data, in this case testing data that was generated by the cross-validation procedure, are explained by the model. The first difference is that :math:`Q^2_A` is always less than the :math:`R^2` value. The other difference is that :math:`Q^2_A` will not keep increasing with each successive component, it will, after a certain number of components, start to decrease. This decrease in :math:`Q^2_A` indicates the new component just added is not systematic: it is unable to explain the cross-validated testing data. We often see plots such as this one:

.. image:: ../../figures/pca/barplot-for-R2-and-Q2.png
	:alt:	../../figures/pca/barplot-for-R2-and-Q2.R
	:scale: 60
	:width: 750px
	:align: center

This is for a real data set, so the actual cut off for the number of components could be either :math:`A =2` or :math:`A=3`, depending on what the 3rd component shows to the user and how interested they are in that component. Likely the 4th component, while boosting the :math:`R^2` value from 66% to 75%, is not really fitting any systematic variation. The :math:`Q^2` value drops from 32% to 25% when going from component 3 to 4. The fifth component shows :math:`Q^2` increasing again. Whether this is fitting actual variability in the data or noise is for the modeller to determine, by investigating that 5th component. These plots show that for this data set we would use between 2 and 5 components, but not more.

Cross-validation, as this example shows is never a precise answer to the number of components that should be retained when trying to learn more about a dataset. Many studies try to find the "true" or "best" number of components. This is a fruitless exercise; each data set means something different to the modeller and the objective for which the model was intended to assist.

The number of components to use should be judged by the relevance of each component. Use cross-validation as guide, and always look at a few extra components and step back a few components; then make a judgement that is relevant to your intended use of the model.

However, cross-validation's objective is useful for predictive models, such as PLS, so we avoid over-fitting components. Models where we intend to learn from, or optimize, or monitor a process may well benefit from fewer or more components than suggested by cross-validation.


.. Determining the number of components by randomization 
.. 
.. *	Concept of randomization is not new: Fisher's example of 5!6! playing cards for randomization of A/B fertilizer testing
.. *	The key is contrast a particular (statistical) outcome against a large body of data which could have only occurred by pure chance. We then calculate a risk value -- the risk of accepting the statistical outcome relative to the data occurring by chance. 
.. *	In many cases our statistical outcome is clearly different to the randomized body of data <IMAGE OF histogram with a line to the far right>
.. *	In other cases it is clear the statistical outcome is quite similar to what could have occurred from chance alone.
.. *	There is obviously a transitionary area where the data analyst/modeller must make an informed decision. However, transferring the statistical value to a risk value is more interpretable in many cases, and can be understood even by non-experts (colleagues, managers and so forth, who are not statistically trained.)
..  
.. *	Any statistic can be used: t's covariance with u (PLS objective function)
.. *	Eigenvalue in PCA?  
.. 
.. *	PCA models?
.. *	Multiblock methods?
.. *	PLS-DA models? DOI:  10.1007/s11306-007-0099-6  (also see other paper by Westerhuis on this topic)
.. *	Batch data?
.. *	Does it work well for DOE data (the usual shortcoming for Q2 calculations)
.. *	Use a robust correlation estimate to guard against outliers in score correlations
.. 	*	http://www.eric.ed.gov/ERICWebPortal/search/detailmini.jsp?_nfpb=true&_&ERICExtSearch_SearchValue_0=ED201658&ERICExtSearch_SearchType_0=no&accno=ED201658
.. 	*	http://www.jstor.org/stable/2349088
.. 	*	``covRob`` function in ``robust`` package in R
.. 	*	http://www.unt.edu/benchmarks/archives/2001/december01/rss.htm
.. 
.. *	Risk metric more interpretably for automated model fitting (quite common nowadays)
.. *	Helpful to see the risk metric on a per-component basis, even if it is not used to determine the number of components.
.. 
.. *	Drawbacks: for dataset with large N, large K (batch datasets) the model rebuilding with :math:`G` in the order of 50 to 500 can be substantial. Contrast this to cross validation where the number of groups typically used is :math:`G = 7`.  Fortunately, this model rebuilding can be trivially parallelized, which is attractive on multicore CPUs, common on desktop computers.
.. 
.. PLS models
.. 
.. *	Statistic used: correlation between the :math:`t`-score and the :math:`u`-score
.. *	Details:
.. 
.. 	#.	Deflate the |X| and |Y| matrices from the previous component (for the first component, this would just be the data after preprocessing)
.. 	#.	Calculate the current component, called :math:`a`: we are going to test whether this :math:`a^\text{th}` additional component is significant or not
.. 	#.	Calculate the correlation between the :math:`t_a` and the :math:`u_a` score vectors: it is a number between 0 and 1, because these scores are positively correlated.
.. 	#.	Repeat a certain number, say :math:`G=1000` times:
.. 		
.. 		*	randomize the rows in |X|, but not in |Y| (these are the same |X| and |Y| matrices that were just used to calculate the :math:`t_a` and the :math:`u_a` score vectors)
.. 		*	fit a PLS component to calculate the :math:`t_{a,g}` and the :math:`u_{a,g}` score vectors, where :math:`g = 1, 2, \ldots, G`
.. 		*	calculate the :math:`G` correlation values, in the same was as was done in step 3.
.. 	
.. 	#.	Use the reference :math:`t_a` vs :math:`u_a` correlation, call it :math:`S_0`, and compare it to the :math:`G` other randomized correlation values, called :math:`S_1, S_2, \ldots, S_g, \ldots, S_G`. Determine whether or not to retain this :math:`a^\text{th}` component by assessing the risk. 
.. 	
.. 	One way to assess the risk that provides a clear signal whether or not to retain the component is to use a risk count of violations. We use two factors to make up the risk evaluation: the number of randomization trials that exceed the base statistic under test (:math:`S_0`), and the strength of the correlation, which is related to the PLS objective function.
.. 	
.. 		*	Let risk = \frac{\text{number of}\,\,S_g\,\,\text{values exceeding}\,\,S_0}{G}
.. 		
.. 			*	If risk :math:`\geq 0.08`, then ``points = points + 2``, as there is a high risk, one in 12 chance, we are accepting a component that should not be accepted.
.. 		
.. 			*	or, if :math:`0.03 \leq \text{risk} < 0.08` then ``points = points + 1``  (moderately risky to accept this component) 
.. 		
.. 			*	or, if :math:`0.01 \leq \text{risk} < 0.03` then we accept the component without accumulating any points, however, but we might still add some points if the correlation, :math:`S_0` is small (see next step). 
.. 			
.. 			*	finally, if :math:`risk \leq 0.01` then accept the component unconditionally, since the risk is very low. 
.. 			
.. 			
.. 				..	I'm reluctant to implement this: more complexity, hard to justify (ad hoc)
.. 				
.. 					In addition, remove 1.0 risk points, or fewer if currently less than 1.0, from the current risk count. The reason is that sometimes we just cumulate half points (below) over several components, leading to early termination. See for example, the ISO_brightness.mat data file (Wiklund et al, 2007, J. Chemometrics paper DOI:10.1002/cem.1086) 
.. 		
.. 		*	Note that :math:`S_0` represents the correlation between :math:`t_a` and the :math:`u_a`, which is nothing more than a scaled version of the objective function of the PLS model, which each component is trying to maximize, subject to certain constraints. We accumulate risk based on the strength of this correlation as follows:
.. 		
.. 			*	If :math:`S_0 \geq 0.50`, then we do not augment our risk, as this is a strong correlation
.. 		
.. 			*	Or, if :math:`0.35 \leq S_0 < 0.50`, then ``points = points + 0.5`` (weak correlation between :math:`t_a` and :math:`u_a`)
.. 		
.. 			*	Or, if :math:`S_0 \leq 0.35` then ``points = points + 1.0`` (very weak correlation between :math:`t_a` and :math:`u_a`)
.. 
.. 		We stop adding components when the total risk points *accumulated on the current and all previous components* equals or exceeds 2.0. We revert to the component where we had a risk points of 1.0 or less and stop adding components.
.. 		
.. 	#.	Once we decide to accept this :math:`a^\text{th}` component then we deflate the |X| and |Y| matrices; increment the value of :math:`a` by one and repeat the process to decide whether the next component is significant.
.. 
.. 
.. Fitting :math:`G=1000` models can be prohibitive on some data sets, however this can be easily mitigated as follows. Fit :math:`G=200` permutations; if the risk is between 0.5% and 10%, then fit the greater number, say :math:`G=1000` permutations. Risk values outside this range will not likely change by using more permutations. The numbers of :math:`G=200` (fast) and :math:`G=1000` (slow) are just an example, and should obviously be adjusted in proportion to the size of the dataset.

