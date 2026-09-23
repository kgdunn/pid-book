Variability explained with each component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can calculate :math:`R^2` values, since PLS explains both the |X|-space and the |Y|-space. We use the :math:`\mathbf{E}_a` matrix to calculate the cumulative variance explained for the |X|-space.

.. math::
	R^2_{\mathbf{X}, a, \text{cum}} = 1 - \dfrac{\text{Var}(\mathbf{E}_a)}{\text{Var}(\mathbf{X}_{a=1})}

Before the first component is extracted we have :math:`R^2_{\mathbf{X}, a=0} = 0.0`, since :math:`\mathbf{E}_{a=0} = \mathbf{X}_{a=1}`. After the second component, the residuals, :math:`\mathbf{E}_{a=1}`, will have decreased, so :math:`R^2_{\mathbf{X}, a}` would have increased.

We can construct similar :math:`R^2` values for the |Y|-space using the :math:`\mathbf{Y}_a` and :math:`\mathbf{F}_a` matrices. Furthermore, we construct in an analogous manner the :math:`R^2` values for each column of :math:`\mathbf{X}_a` and :math:`\mathbf{Y}_a`, exactly as :ref:`we did for PCA <LVM_PCA_R2_values>`.

These :math:`R^2` values help us understand which components best explain different sources of variation. Bar plots of the :math:`R^2` values for each column in |X| and |Y|, after a certain number of |A| components are one of the best ways to visualize this information.

.. _LVM-PLS-number-of-components:

How many components?
^^^^^^^^^^^^^^^^^^^^^^

For PLS the number of components is chosen by how well the model predicts the |Y|-space on data it has
not yet seen, rather than by how much variance it explains in |X|. The tool is the same
cross-validation described for :ref:`PCA <LVM_number_of_components>`, but the residuals that matter are
those of |Y|. Leaving out one group of rows at a time, we predict the held-out |Y| values and gather
their prediction error into :math:`Q^2_Y`, the cross-validated :math:`R^2` of the |Y|-space. As with
PCA, :math:`Q^2_Y` is smaller than :math:`R^2_Y`, and it stops rising, then falls, once a component no
longer improves prediction.

The ``process_improve`` package computes this with ``PLS.select_n_components``. It re-derives the
centring and scaling inside each cross-validation fold, so the held-out rows do not enter the model
that predicts them, and it applies the one-standard-error rule described for
:ref:`PCA <LVM_number_of_components>`: keep the fewest components whose cross-validated error is within
one standard error of the best.

.. code-block:: python

	import pandas as pd
	from process_improve.multivariate import PLS

	# Cheddar-cheese data: predict the sensory Taste (Y) from three
	# chemical measurements (X). The same data set is used in the PLS
	# exercises at the end of this section.
	cheese = pd.read_csv("https://openmv.net/file/cheddar-cheese.csv")
	Y = cheese[["Taste"]]
	X = cheese[["Acetic", "H2S", "Lactic"]]

	# Raw X and Y may be passed: the scaling is fit inside every fold.
	result = PLS.select_n_components(X, Y, random_state=0)
	print(result.n_components)                     # 1
	print(result.rmsecv["total"].round(2))         # A=1: 10.88, A=2: 11.02, A=3: 11.08
	print(result.r2y_validated["total"].round(3))  # A=1: 0.537, A=2: 0.525, A=3: 0.519

For this small data set cross-validation retains a single component. The cross-validated
:math:`Q^2_Y` is highest at :math:`A = 1` (0.54) and edges down as further components are added, so the
second and third components do not improve the prediction of Taste.

There is one column per target, and two that summarise them. With a single target, as here,
they agree. With several they need not: ``total`` pools the targets on their original scale,
so a target with a wide range decides it almost alone, while ``scaled_total`` averages the
per-target values and gives each the same weight. Which to read follows from the question:
``scaled_total`` treats the targets as equally important, and is the one to compare against a
fitted :math:`R^2_Y` computed on scaled data. The
:ref:`multiblock case study <APPS_batch_case_fmc>` shows a block where the two disagree on
which set of predictors is better. Here the one-standard-error rule
and the plain minimum of the error curve agree; on data sets where the error curve is flat near its
minimum the one-standard-error rule returns the more parsimonious model.

Cross-validation on |Y| stops adding components once the prediction of |Y| stops improving. When the
|X|-space itself must also be well described, for example to monitor the squared prediction error of a
process, one or two components beyond the cross-validated number are sometimes retained so that |X| is
modelled as well.

.. _LVM-PLS-dropped-component:

Why a component that points the right way can still be dropped
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A component lowers the cross-validated prediction error only when, on the held-out rows, its effect is
more than half as large as the effect the model fitted. A component can therefore point the right way
on new rows and still be dropped, because the rows it was fitted on made its effect look larger than it
is.

Adding component :math:`a` changes the prediction of each held-out row :math:`i` by an amount
:math:`g_i`, computed by the fold model that did not see that row. Call :math:`r_i` the part of the
row's |Y| value that the first :math:`a-1` components left unexplained, and :math:`s_a` the
least-squares slope of :math:`r_i` on :math:`g_i` through the origin. The slope is 1 when the held-out
rows follow the fitted effect exactly, and 0 when they do not follow it at all. The prediction error
sum of squares, PRESS, then changes by

.. math::

	\text{PRESS}_{a-1} - \text{PRESS}_a = \sum_i r_i^2 - \sum_i \left(r_i - g_i\right)^2
	= \left(2 s_a - 1\right) \sum_i g_i^2

so the prediction error falls, and :math:`Q^2_Y` rises, only when :math:`s_a` is above one half.

The ``compare_cv_criteria`` function runs one cross-validation and reports :math:`s_a` for every
component, among other checks. The block below also computes it from the fold models directly, one
held-out cheese at a time, which is what the figure draws.

.. code-block:: python

	import numpy as np
	from process_improve.multivariate import compare_cv_criteria

	checks = compare_cv_criteria(X, Y, max_components=2, random_state=0)
	print(checks.table["slope_ratio"].round(2).tolist())  # [0.93, 0.36]

	# For every held-out cheese: what component a adds to its predicted taste
	# (g in the text), and the taste the first a - 1 components left unexplained (r).
	contribution = np.zeros((len(X), 2))
	unexplained = np.zeros((len(X), 2))
	fold_weights = []
	for fit_rows, held_out in checks.cv_splits:
	    before = np.full(len(held_out), Y.iloc[fit_rows, 0].mean())  # a = 0: the fold mean
	    for a in (1, 2):
	        fold_model = PLS(n_components=a).fit(X.iloc[fit_rows], Y.iloc[fit_rows])
	        after = fold_model.predict(X.iloc[held_out]).to_numpy().ravel()
	        contribution[held_out, a - 1] = after - before
	        unexplained[held_out, a - 1] = Y.iloc[held_out, 0].to_numpy() - before
	        before = after
	    fold_weights.append(fold_model.x_weights_.to_numpy())

	held_out_slope = (contribution * unexplained).sum(axis=0) / (contribution**2).sum(axis=0)
	print(held_out_slope.round(2))  # [0.93 0.36]

.. code-block:: python

	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	fig = make_subplots(rows=1, cols=2, subplot_titles=["Component 1", "Component 2"])
	for a in (0, 1):
	    reach = 1.08 * np.abs(contribution[:, a]).max()
	    ends = np.array([-reach, reach])
	    for slope, name, style in ((1.0, "fitted effect", {"color": "black"}),
	                               (0.5, "break-even", {"color": "orange", "dash": "dot"}),
	                               (held_out_slope[a], "held-out slope", {"color": "darkblue", "dash": "dash"})):
	        fig.add_scatter(x=ends, y=slope * ends, mode="lines", name=name, line=style,
	                        showlegend=(a == 0), row=1, col=a + 1)
	    fig.add_scatter(x=contribution[:, a], y=unexplained[:, a], mode="markers",
	                    name="held-out cheese", marker={"color": "darkblue"},
	                    showlegend=(a == 0), row=1, col=a + 1)
	    fig.update_xaxes(title_text=f"change in predicted taste from component {a + 1}", row=1, col=a + 1)
	fig.update_yaxes(title_text="taste still unexplained before the component", row=1, col=1)
	fig.show()

.. _LVM-PLS-heldout-slope-figure:

.. figure:: ../../figures/pls/pls-heldout-slope-ratio.png
	:alt: Held-out cheeses: change in predicted taste from each component against the taste still unexplained
	:width: 750px
	:align: center

	Each point is one cheese, predicted by the fold model that did not see it. A component lowers the
	prediction error only when the points follow a slope above the dotted break-even line at one half.
	The cheeses follow nearly all of the first component's fitted effect. They follow the second
	component in direction, but at less than half its fitted effect.

This is why cross-validation keeps one component for this data set: the second component makes the
predictions of new cheeses worse, although it points the right way.

Whether the second component is only noise is a separate question. Its held-out correlation, between
the component's score and the taste it has left to explain, is positive. With 30 cheeses, though, it
cannot be told apart from chance: when the tastes are shuffled among the cheeses, which removes any real
relation, a correlation at least this large turns up in about 6% of the shuffles. Its weights, on the
other hand, are much the same in every fold model, so its direction in |X| does not depend on which
cheeses were used to fit it.

.. code-block:: python

	print(checks.table["r_cv"].round(2).tolist())    # [0.76, 0.36]
	print(checks.table["r_cv_p"].round(2).tolist())  # [0.01, 0.06]

	full_weights = checks.global_model.x_weights_.to_numpy()
	fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
	                    subplot_titles=["Weights of component 1", "Weights of component 2"])
	for a in (0, 1):
	    fig.add_bar(x=list(X.columns), y=full_weights[:, a], name="all 30 cheeses",
	                marker_color="lightgrey", showlegend=(a == 0), row=1, col=a + 1)
	    for k, weights in enumerate(fold_weights):
	        # The sign of a component is arbitrary: align each fold's to the full model.
	        aligned = weights[:, a] * np.sign(weights[:, a] @ full_weights[:, a])
	        fig.add_scatter(x=list(X.columns), y=aligned, mode="markers", name="fold models",
	                        marker={"color": "white", "line": {"color": "darkblue", "width": 1.5}},
	                        showlegend=(a == 0 and k == 0), row=1, col=a + 1)
	fig.show()

.. _LVM-PLS-fold-weights-figure:

.. figure:: ../../figures/pls/pls-fold-weights.png
	:alt: Weights of components 1 and 2 in the full model and in each of the seven fold models
	:width: 700px
	:align: center

	The bars are the weights of the model fitted to all 30 cheeses, and the dots those of the seven fold
	models. Every fold model gives the second component a positive weight on Acetic and a negative weight
	on H2S; its small weight on Lactic changes sign from fold to fold.

The second component is a contrast of Acetic against H2S that recurs in every fold model, but it
carries too little of the taste for 30 cheeses to show that it improves the prediction. A model used
only to predict taste has no use for it. A model that must also describe the chemistry of the cheeses,
as :ref:`inverting the model <LVM-PLS-inversion-components>` requires, keeps it, and its direction can
be relied on even though its effect on taste is not established.


.. Common questions about PLS models
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
..
.. .. _LVM-PLS-what-in-X-and-Y:
..
.. What goes in |X| and what goes in |Y| ?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..
.. .. Still to come.
..
.. .. 	* handles collinear variables
.. .. 	* handles multiple Y
.. .. 	* PLS1 vs PLS2
.. ..
.. .. Uses:
.. ..
.. .. 	* Predictive modelling; QSAR
.. .. 	* Monitoring
..
..
.. One Y or many Y's?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..
.. .. Still to come.
..
.. .. Do PLS2 first, then do PLS1 if the Y's are relatively orthogonal.
..
.. .. Wold 2001, p 116
..
..
.. .. _LVM-PLS-number-of-components:
..
.. How many components?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..
.. .. Still to come.
..
.. .. One technique to estimate Q2 is by cross-validation. This method consists of dividing the data into a number of groups. Models are built with a group of data left out – one group at a time. With each model, the corresponding omitted data are predicted and the total prediction error sum of squares calculated. Q2, like R2, varies between 0 and 1, where values closer to 1 indicate better prediction ability. The Q2 value will always be smaller than R2. Finally, Q2 is used to select the number of principal components (model complexity) to avoid over-fitting. PLS models can be converted to a standard linear regression form as given by the following equation:
..
.. .. Almost all software packages will use cross-validation for PLS to determine the number of components. The cross-validation for PLS only considers the predictive capability of |Y|; in other words the cross-validation criterion stops adding components once the variance explained in |Y| starts to drop off.
..
.. .. This is perfectly adequate in many cases; but is certain instances we would also like the |X|-space to be well explained. For example, when building a monitoring model, we would like to also monitor the SPE from the |X|-space. Fortunately, in many cases, just adding one or two components manually, beyond the number from cross-validation will achieve the objective of additionally modelling the |X|-space.
..
.. .. * Wold 2001, p 116
.. .. * Why can we have more than 1 PC when there is only a single y?
..
.. .. _LVM-PLS-on-new-data:
..
.. How do I use a PLS model on new data?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..
.. .. Still to come.


.. What is the difference between |W| and |P|?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..
.. This question is best answered by first reading the subsection above called ":ref:`How do I use a PLS model on new data <LVM-PLS-on-new-data>`". After that, please read the description of deflation in the section on the :ref:`NIPALS algorithm for PLS <LVM_PLS_calculation>`.

.. Comparison to MLR (using R)
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
..
.. .. Still to come.
..
.. The properties of PLS
.. ~~~~~~~~~~~~~~~~~~~~~~~~
..
.. For reference, we list some properties of the PLS model structure:
..
.. *	The |A| vectors in the columns on :math:`\mathbf{W}` are orthogonal to each other: :math:`w_i \perp w_j` where :math:`i \neq j`, and :math:`i, j = 1, 2, \ldots, A`.
.. *	The vectors :math:`t_i` in the scores, |T|, are mutually orthogonal.
.. *	The vectors :math:`w_i` are orthogonal to the vectors :math:`p_j`, only for :math:`i \leq j`.
..
.. More still to come.
..
.. ..	u't = (c'c)^{-1}(c'Y') t
.. .. * Is c'c = 1 for each component?  I.e. can we see the u's as an orthogonal projection onto the loadings for Y?  They are not unit length and they are not orthogonal. So we cannot make that claim.
