.. _LVM_number_of_components:

Determining the number of components to use in the model with cross-validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: Q-squared statistic
	pair: number of components; latent variable modelling
	single: over-fitting

..	Any recorded values we have from a system, in |X|, can be broken down into 2 parts: the data structure that is systematic, :math:`\mathbf{TP}'`, and an error component, :math:`\textbf{E}`.

.. The problem of determining "*how many components*" is related to knowing when we have extracted all the systematic variables from the data, |X|, into the latent variable model, :math:`\mathbf{TP}'`. Step back for a minute and think what that means: it says we should stop adding latent variables to the model when there is no more systematic correlation remaining between the variables in |X|. That's all the PCA does: extract the variability in |X|. We should stop adding components when we have extracted, *reproducibly*, all systematic variation.

..	- scree plot
..	- size of eigenvalue: :math:`\sum_a^{a=K}{\lambda_a} = K`
..	- cross-validation

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

Cross-validation for multivariate data sets was described by Svante Wold in his paper on `Cross-validatory estimation of the number of components in factor and principal components models <https://literature.learnche.org/item/12/cross-validatory-estimation-of-the-number-of-components-in-factor-and-principal-components-models>`_, in *Technometrics*, **20**, 397-405, 1978.

For a critical review of cross-validation procedures applied to component models, see `Bro, Kjeldahl, Smilde and Kiers (2008) <https://literature.learnche.org/item/110/cross-validation-of-component-models-a-critical-look-at-current-methods>`_, *Cross-validation of component models: A critical look at current methods*.

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
	:alt: Cumulative R-squared beside cumulative Q-squared, which stops rising after two components
	:scale: 60
	:width: 750px
	:align: center

This is for a real data set, so the actual cut off for the number of components could be either :math:`A =2` or :math:`A=3`, depending on what the 3rd component shows to the user and how interested they are in that component. Likely the 4th component, while boosting the :math:`R^2` value from 66% to 75%, is not really fitting any systematic variation. The :math:`Q^2` value drops from 32% to 25% when going from component 3 to 4. The fifth component shows :math:`Q^2` increasing again. Whether this is fitting actual variability in the data or noise is for the modeller to determine, by investigating that 5th component. These plots show that for this data set we would use between 2 and 5 components, but not more.

Cross-validation, as this example shows is never a precise answer to the number of components that should be retained when trying to learn more about a dataset. Many studies try to find the "true" or "best" number of components. This is a fruitless exercise; each data set means something different to the modeller and the objective for which the model was intended to assist.

The number of components to use should be judged by the relevance of each component. Use cross-validation as guide, and always look at a few extra components and step back a few components; then make a judgement that is relevant to your intended use of the model.

However, cross-validation's objective is useful for predictive models, such as PLS, so we avoid over-fitting components. Models where we intend to learn from, or optimize, or monitor a process may well benefit from fewer or more components than suggested by cross-validation.

**A caution: do not reconstruct a left-out row from its own values.** Wold's procedure above projects
each held-out row onto the loadings, :math:`\mathbf{T}_{(g)} = \mathbf{X}_{(g)} \mathbf{P}`, and then
reconstructs that same row from those scores. The scores used to predict the row are therefore
calculated from the very values we are trying to predict. As more components are added the loadings
span more of the measurement space, so the cross-validated reconstruction error tends to keep
shrinking even when the extra component is not real. As the number of components, |A|, approaches the
number of variables, :math:`K`, the held-out row is reproduced almost perfectly and :math:`Q^2_A`
becomes too optimistic. The effect is strongest when there are few variables, which is exactly the
situation in the small example above.

This weakness of the row-wise scheme is the central point of the Bro *et al.* (2008) review cited
earlier. They recommend instead leaving out individual *elements* of :math:`\mathbf{X}`, one scattered
group of cells at a time, and predicting each missing element from a model that never used it. This
element-wise scheme keeps the prediction genuinely independent of the value being predicted. It is the
approach recommended in that review and implemented in several chemometrics packages. The
interpretation of the resulting :math:`Q^2_A` curve is unchanged; only the way each held-out value is
predicted differs.

**Choosing the number of components robustly.** A single split of the rows into :math:`G` groups can
move the recommended number of components up or down by one or two, simply because of which rows
happened to land together. Three habits make the choice more reliable:

*	*Repeat the split.* Re-run the cross-validation several times with different random groupings and
	look at the spread of :math:`Q^2_A`, rather than trusting a single division of the data. A
	component that is real survives the reshuffling; one that is marginal does not.

*	*Avoid leaving out only one row at a time.* Leave-one-out cross-validation (:math:`G = N`) is
	tempting, but its :math:`N` models are nearly identical, so its :math:`Q^2` estimate is unstable
	and cannot be repeated. Groups of :math:`G = 7` to :math:`10`, repeated a few times, are a better
	default.

*	*Prefer the simpler model when the difference is small.* Instead of taking the absolute best
	:math:`Q^2_A`, keep the *fewest* components whose cross-validated error is within one standard
	error of the best value seen across the repeats. This "one standard error" rule guards against
	adding a component that wins by a margin smaller than the noise in the estimate itself.

A complementary approach avoids splitting the data at all. A *randomization* (permutation) test asks
whether the structure captured by a candidate component is stronger than what the same data produce
after their rows have been randomly shuffled. If a component is no better than the shuffled reference,
it is not retained. See Van der Voet (1994), *Chemometrics and Intelligent Laboratory Systems*,
**25**, 313-323, and Wiklund *et al.* (2007), *Journal of Chemometrics*, **21**,
`DOI: 10.1002/cem.1086 <https://doi.org/10.1002/cem.1086>`_, for the test applied to latent variable
models.

.. _LVM_q2_across_packages:

**The same data, both schemes.** The bar plot above is Simca-P's output, from the row-wise scheme. The
same LDPE data can be run through the ``process_improve`` package that accompanies this book, which
provides the element-wise scheme just described. Both work on the same 54 rows and 19 variables, and
fit the same eleven components. Their :math:`R^2` values agree to within :math:`5 \times 10^{-7}` at
every component, so whatever separates the :math:`Q^2` curves comes from the cross-validation and not
from the model underneath it.

.. code-block:: python

	import pandas as pd
	from process_improve.multivariate.methods import PCA, MCUVScaler

	ldpe = pd.read_csv("https://openmv.net/file/LDPE.csv").iloc[:, 1:]
	scaled = MCUVScaler().fit_transform(ldpe)

	# The centred, unit-variance block is passed so that PRESS, and with it
	# Q2, is on the same scale as the R2 values and as the Simca-P curve.
	# The package accumulates PRESS in the units of the block it is given;
	# on the raw block the Mw column alone holds 99.5% of the sum of
	# squares, and its residuals would set the whole curve.
	#
	# cv_scheme="ekf" is the element-wise k-fold scheme: scattered single
	# cells of X are held out, and each is predicted from a model that
	# never used it. n_repeats reshuffles the folds, so the spread of Q2
	# across the repeats can be reported alongside it.
	chosen = PCA.select_n_components(scaled, max_components=11, cv=7,
	                                 cv_scheme="ekf", n_repeats=5, random_state=42)
	print(chosen.q2.round(3).to_list())
	# [0.255, 0.367, 0.333, 0.3, 0.297, 0.186, 0.029, 0.126, 0.673, 0.844, 0.808]
	print(chosen.q2_se.round(3).to_list())
	# [0.015, 0.016, 0.022, 0.029, 0.04, 0.058, 0.067, 0.053, 0.017, 0.021, 0.014]

.. image:: ../../figures/pca/q2-across-packages.png
	:alt: Cross-validated Q-squared from three implementations on the same LDPE data
	:scale: 55
	:width: 800px
	:align: center

The shaded band on the element-wise curve is one standard error either side, taken across the five
fold permutations. That standard error, ``q2_se`` in the code block above, runs from 0.014 at eleven
components to 0.067 at seven components, and is widest in the dip between six and eight components.
Two features of the curve are large relative to it: the rise of 0.11 from one component to two, and
the fall of 0.34 from two components to seven. Neither depends on which cells happened to be held
out together. The gaps between two, three, four and five components (0.367, 0.333, 0.300 and 0.297)
are each no more than about one to two standard errors, so the curve on its own does not separate
those component counts from one another; it does place all of them well above the value at seven
components.

The two curves track each other over the first eight components. Both reach their highest value at two
components, 0.34 for Simca-P and 0.37 for the element-wise scheme, and neither exceeds it again. That
is the turnover described :ref:`earlier in this section <LVM_number_of_components>`, and it is why two
or three components is the reading these data support. The element-wise scheme, which does not let a
held-out value contribute to its own prediction, reaches the same conclusion here as the package the
figure above came from.

Past the eighth component both curves climb steeply. By the ninth component :math:`R^2` is 99.1%, so
there is very little left to hold out and predict, and the values in that region describe the
arithmetic more than they describe the process. The part of a :math:`Q^2` curve worth reading is the
part before the model has taken up the systematic variation.

That last point has a practical consequence for anyone using an automatic rule. Asking for the
component count with the best :math:`Q^2` returns **ten** on this curve, because the late rise beats
the peak at two. Two changes each recover the answer a reader would give from the plot:

*	Stop the search before the model runs out of variation to hold out. Capping the search at eight
	components, or anywhere below it, returns two.

*	Use the incremental criterion rather than the best value. Wold's original rule keeps a component
	only if it improves the cross-validated error by more than a set margin, so it stops at the first
	component that fails the test and never sees the late rise. In ``process_improve`` this is
	``selection_rule="q2_increment"``, and it returns two on this data.

A rule that hunts for the maximum of the whole curve will find whatever the tail happens to do. The
choice of *where to stop looking* matters as much as the choice of criterion.


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
.. 	*	https://www.jstor.org/stable/2349088
.. 	*	``covRob`` function in ``robust`` package in R
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
