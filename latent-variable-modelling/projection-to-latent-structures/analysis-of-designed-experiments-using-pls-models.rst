.. _LVM_DOE_data:

Analysis of designed experiments using PLS models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: designed experiments; projection to latent structures (PLS)

.. NOTE: you already have some of these ideas in the section "LVM-preprocessing": combine them; cross reference them?

Data from a designed experiment, particularly factorial experiments, will have independent columns in |X|. These data tables are adequately analyzed using :ref:`multiple linear regression <LS_multiple_X_MLR>` (MLR) least squares models.

These factorial and fractional factorial data are also well suited to analysis with PLS. Since factorial models support interaction terms, these additional interactions should be added to the |X| matrix. For example, a full factorial design with variables **A**, **B** and **C** will also support the **AB**, **AC**, **BC** and **ABC** interactions. These four columns should be added to the |X| matrix so that the loadings for these variables are also estimated. If a :ref:`central composite design <DOE_central_composite_designs>`, or some other design that supports quadratic terms has been performed, then these columns should also be added to |X|, e.g.: :math:`\mathbf{\text{A}}^2`, :math:`\mathbf{\text{B}}^2` and :math:`\mathbf{\text{C}}^2`.


The PLS loadings plots from analyzing these DOE data are interpreted in the usual manner; and the coefficient plot is informative if :math:`A>2`.

.. EXAMPLE: Carlos' thesis.

There are some other advantages of using and interpreting a PLS model built from DOE data, rather than using the MLR approach:

	*	If *additional data* (not the main factors) are captured during the experiments, particularly measurable disturbances, then these additional columns can, and should, be included in |X|. These extra data are called covariates in other software packages. These additional columns will remove some of the orthogonality in |X|, but this is why a PLS model would be more suitable.

	*	If multiple |Y| measurements were recored as the response, and particularly if these |Y| variables are correlated, then a PLS model would be better suited than building |K| separate MLR models. A good example is where the response variable from the experiment is a complete spectrum of measurements, such as from a NIR probe.

One other point to note when analyzing DOE data with PLS is that the |Q2| values from cross-validation are often very small. This makes intuitive sense: if the factorial levels are suitably spaced, then each experiment is at a point in the process that provides new information. It is unlikely that cross-validation, when leaving out one or more experiments, is able to accurately predict each corner in the factorial.

With a single response, a PLS model of data from a two-level factorial needs one component, and
that component is the least-squares model. The reason is the :ref:`orthogonality <DOE_orthogonality>`
of the design. When no two columns of |X| are aliased with each other, the centred and scaled columns,
interactions included, satisfy :math:`\mathbf{X}'\mathbf{X} = (N-1)\mathbf{I}`. As in any PLS model
with one response, the first weight vector is proportional to :math:`\mathbf{X}'\mathbf{y}` (the
:ref:`NIPALS algorithm <LVM_PLS_calculation>` converges in one round). With this |X| the least-squares
coefficients, :math:`\mathbf{b} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y} =
\mathbf{X}'\mathbf{y}/(N-1)`, point in the same direction, so the one-component prediction from
:math:`\mathbf{t}_1 = \mathbf{X}\mathbf{w}_1` is the least-squares prediction :math:`\mathbf{X}\mathbf{b}`.
What is left of :math:`\mathbf{y}` is the least-squares residual, which is orthogonal to every column of
|X|, so a second component has nothing in :math:`\mathbf{y}` left to explain.

The same algebra says how to read the first component. The weights :math:`\mathbf{w}_1` are the
least-squares coefficients rescaled to unit length, so a bar plot of :math:`\mathbf{w}_1` ranks the
terms as the :ref:`Pareto plot <DOE-Pareto-plot>` of the effects does, with their signs. The loadings
equal the weights, :math:`\mathbf{p}_1 = \mathbf{X}'\mathbf{t}_1/(\mathbf{t}'_1\mathbf{t}_1) =
\mathbf{X}'\mathbf{X}\mathbf{w}_1/(N-1) = \mathbf{w}_1`: no column of |X| varies with any other, so
regressing the columns back onto the score returns the weights and nothing more.

The :math:`2^4` factorial of that Pareto plot confirms each of these properties. Its four main effects
and six two-factor interactions are the columns of |X|; the higher-order interactions are left out, so
that the least-squares fit is not exact.

.. code-check: allow-warnings demonstrates the warning the reader will see for a second component
.. code-block:: python

	import itertools

	import numpy as np
	import pandas as pd
	from process_improve.multivariate import PLS

	# The 2^4 factorial in standard order (A changes fastest), with its four main
	# effects and six two-factor interactions as the columns of X.
	runs = np.array(list(itertools.product([-1, 1], repeat=4)))[:, ::-1]
	doe_X = pd.DataFrame(runs, columns=["A", "B", "C", "D"])
	for first, second in itertools.combinations("ABCD", 2):
	    doe_X[first + second] = doe_X[first] * doe_X[second]
	doe_y = pd.DataFrame({"y": [45, 71, 48, 65, 68, 60, 80, 65,
	                            43, 100, 45, 104, 75, 86, 70, 96]})

	doe_pls = PLS(n_components=2).fit(doe_X, doe_y)   # warns: the data support 1 component
	print(doe_pls.r2_cumulative_.round(3).to_list())
	# [0.978, 0.978]

	# Least-squares coefficients of the ten coded terms; the intercept is dropped.
	intercept_and_X = np.column_stack([np.ones(16), doe_X])
	b = np.linalg.lstsq(intercept_and_X, doe_y["y"], rcond=None)[0][1:]
	w1 = doe_pls.x_weights_.iloc[:, 0].to_numpy()    # unit length
	p1 = doe_pls.x_loadings_.iloc[:, 0].to_numpy()
	b_pls = doe_pls.beta_coefficients_["y"].to_numpy()
	print(f"cos(w1, b) = {w1 @ b / np.linalg.norm(b):.3f}")
	# cos(w1, b) = 1.000
	print(f"largest |p1 - w1| = {np.abs(p1 - w1).max():.3f}")
	# largest |p1 - w1| = 0.000
	print(f"largest |b_PLS - b| = {np.abs(b_pls - b).max():.3f}")
	# largest |b_PLS - b| = 0.000

A second component therefore adds nothing for a single response from an orthogonal design. Once
covariates are added to |X|, its columns are no longer orthogonal, and further components can then
improve the prediction.

With |M| responses, each response has its own vector of least-squares coefficients, and the same
argument gives one component for each linearly independent direction among those vectors. The number of
components that improve the fit is the rank of :math:`\mathbf{X}'\mathbf{Y}`, at most |M|, so two
responses whose effects are proportional to each other share one component.

Lastly, models built from DOE data allow a much stronger interpretation of the loading vectors, :math:`\mathbf{R:C}`. This time we can infer cause-and-effect behaviour; normally in PLS models the best we can say is that the variables in |X| and |Y| are correlated. Experimental studies that are run in a factorial manner will break happenstance correlation structures; so if any correlation that is present, then this truly is causal in nature.


.. Analysis with additional first-principles knowledge
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..
.. We rarely only have data from a process; as engineers we also have additional, first-principles knowledge about the system being investigated. We can always embed this information in the data.
..
.. An example that was mentioned in the :ref:`section of data preprocessing <LVM_preprocessing>` was that of a distillation column. The inverse temperature is known to more correlated to the vapour pressure, known from first-principles modelling. Using the temperature variable by itself will lead to an adequate model, but the transformed variable can lead to a better model. We sometimes leave both variables in the model: the temperature and the calculated inverted temperature.
