.. _LVM-PLS-model-inversion:

Using a PLS model backwards: model inversion and the null space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far we have used a PLS model in the forward direction: given the inputs in |X|, predict the
outputs in |Y|. Many design problems ask the reverse question. We fix the quality we want and
solve for the inputs that would achieve it. Finding the inputs that give a chosen output is called
*model inversion*, and it is the basis of latent-variable product and process design
(Jaeckle and MacGregor, 2000).

We will use the same :ref:`cheddar-cheese data <LVM-cheddar-cheese-example>` as before: the taste of a
cheese predicted from three chemical measurements, acetic acid, hydrogen sulfide, and lactic acid. The
forward question was "what taste does this chemistry give?" The inversion question is "which chemistry
gives a target taste?"

.. _LVM-PLS-inversion-components:

Why inversion needs more than the predictive number of components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When we chose the number of components for prediction in
:ref:`the section above <LVM-PLS-number-of-components>`, cross-validation kept a single component: one
component is enough to predict Taste. Inversion places a second demand on the model. To reconstruct an
input vector from a target output, the model must describe the |X|-space well enough to map a score
back to a full set of chemistry values, not only the |Y|-space. A one-component model spans only a line
in the input space, so it can return just one chemistry for a target taste. Keeping a second component
lets the model describe the plane on which the calibration cheeses actually lie, and, as we will see, it
opens up a whole set of equivalent designs. We therefore fit a two-component model here, even though the
second component did not improve prediction.

Following the request to design toward cheeses the model has not seen, we hold out the first four cheeses
and fit the model on the remaining twenty-six.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from process_improve.multivariate import PLS, OPLS

	cheese = pd.read_csv("https://openmv.net/file/cheddar-cheese.csv")
	x_columns = ["Acetic", "H2S", "Lactic"]

	train = cheese.iloc[4:]        # cheeses 5 to 30: used to build the model
	holdout = cheese.iloc[:4]      # cheeses 1 to 4: the targets we design toward
	X = train[x_columns]
	Y = train[["Taste"]]

	pls = PLS(n_components=2).fit(X, Y)
	print(round(float(pls.r2_cumulative_.iloc[-1]), 3))   # R2 on Taste: 0.672

The two-component model explains about 67% of the variation in Taste. It is a moderate predictor, which
is fine for what follows: the null space is a property of the model's geometry, not of how accurately it
predicts.

.. _LVM-PLS-null-space:

The null space: many recipes, one prediction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Held-out cheese 2 has a taste of 20.9. We invert the model to find a chemistry that the model predicts
will give that taste.

.. code-block:: python

	result = pls.invert(y_desired=20.9)

	print(result.x_new.round(2).to_dict())
	# {'Acetic': 5.52, 'H2S': 5.56, 'Lactic': 1.40}
	print(result.null_space_dimension)        # 1
	print(round(result.hotellings_t2, 2))     # 0.06

The model returns a chemistry of about (Acetic 5.52, H2S 5.56, Lactic 1.40). The prediction at this point
is exactly 20.9, by construction. Two other quantities are reported. The ``null_space_dimension`` is 1,
and the Hotelling's :math:`T^2` of the solution is 0.06, far inside the 99% limit of 12.1, so this design
sits comfortably among the calibration cheeses rather than being an extrapolation.

The null space is the reason ``null_space_dimension`` is not zero. A two-component model has two score
directions, but a single taste value pins down only one of them. The other direction is free: we can move
along it and the predicted taste does not change at all. That free direction is the *null space*. Its
dimension is the number of components minus the rank of the response, here :math:`2 - 1 = 1`, so it is a
line. Every chemistry on that line gives the same predicted taste.

We can walk along the null space by passing coordinates along its basis. The prediction stays fixed while
the chemistry changes.

.. code-block:: python

	for step in (-1.0, 1.0):
	    moved = pls.invert(y_desired=20.9, null_space_coordinates=[step])
	    taste = float(pls.predict(moved.x_new.to_frame().T).iloc[0, 0])
	    print(moved.x_new.round(2).to_list(), "->", round(taste, 2))
	# [4.95, 6.10, 1.33] -> 20.9
	# [6.09, 5.02, 1.46] -> 20.9

Both of these chemistries, and the whole line between and beyond them, predict a taste of 20.9. The
freedom to choose among them is what makes inversion useful in practice: it can be spent on a secondary
goal such as cost, safety, or keeping within a supplier's specification, without moving the predicted
quality. As a check on the held-out cheese, its actual chemistry (Acetic 5.16, H2S 5.04, Lactic 1.53)
predicts a taste of 20.7, close to its measured 20.9, and it lies near the null-space line we just traced.

A score plot shows the picture directly. The calibration cheeses are the points, the black square is the
direct-inversion solution, and the purple line is the null space: the set of scores that all predict a
taste of 20.9.

.. code-block:: python

	scores = pls.scores_
	tau = result.scores.to_numpy()               # direct-inversion score
	g = result.null_space_basis.to_numpy().ravel()  # null-space direction
	line = np.array([tau + s * g for s in np.linspace(-4, 4, 50)])

	fig = go.Figure()
	fig.add_scatter(x=scores.iloc[:, 0], y=scores.iloc[:, 1], mode="markers",
	                name="calibration cheeses")
	fig.add_scatter(x=line[:, 0], y=line[:, 1], mode="lines", name="null space",
	                line={"color": "purple"})
	fig.add_scatter(x=[tau[0]], y=[tau[1]], mode="markers", name="direct inversion",
	                marker={"color": "black", "symbol": "square", "size": 10})
	fig.update_layout(xaxis_title="t_1", yaxis_title="t_2")
	fig.show()

.. _LVM-PLS-orthogonal-space:

The same space, reached a different way: O-PLS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Orthogonal projections to latent structures (O-PLS) was developed in a separate line of work, for a
different reason: to make a model easier to interpret. O-PLS splits the systematic variation in |X| into
two parts. One *predictive* component carries the variation that is related to |Y|; the remaining
*Y-orthogonal* components carry systematic variation in |X| that has no bearing on |Y|. Filtering out the
orthogonal part leaves a model with the same predictions as ordinary PLS, but with the response-relevant
variation gathered into a single component.

The subspace holding the orthogonal components is called the *orthogonal space*. By construction, moving
an input along the orthogonal space changes |X| but not the predicted |Y|. That description should sound
familiar: it is the same property that defines the null space of the inverted PLS model. García-Carrión
and co-authors (2025) proved that, for a single response, the two subspaces are the same linear space.
The null space that arises when a PLS model is inverted and the orthogonal space that O-PLS isolates while
fitting are one and the same. The reason is short: both are exactly the set of score directions the model
maps to no change in the response.

The ``process_improve`` package fits O-PLS with the same total number of components, here one predictive
and one orthogonal, and inverts it. Because O-PLS has already separated the single predictive direction,
its inversion is one division rather than the solution of an underdetermined system.

.. code-block:: python

	opls = OPLS(n_orthogonal_components=1).fit(X, Y)
	opls_result = opls.invert(y_desired=20.9)

	print(opls_result.x_new.round(2).to_list())   # [5.46, 5.62, 1.39]
	print(round(opls_result.y_hat, 2))            # 20.9

The O-PLS design, (Acetic 5.46, H2S 5.62, Lactic 1.39), is a different chemistry from the PLS
direct-inversion design, but it lies on the same null-space line and gives the same predicted taste. The
two methods return different representative points: PLS reports the point of smallest score norm, while
O-PLS reports the point whose orthogonal score is zero. The set of solutions, the line itself, is
identical. We can confirm the two subspaces coincide by reconstructing each basis into the input space and
comparing their directions.

.. code-block:: python

	ns_input = result.null_space_basis.to_numpy().T @ pls.x_loadings_.to_numpy().T
	os_input = opls_result.orthogonal_space_basis.to_numpy().T
	cosine = np.abs(ns_input @ os_input.T) / (
	    np.linalg.norm(ns_input) * np.linalg.norm(os_input)
	)
	print(float(cosine))    # 1.0

The cosine between the two directions is 1.0: the PLS null space and the O-PLS orthogonal space point the
same way and span the same line.

.. _LVM-PLS-inversion-in-practice:

Reading the result: how far is the design from the data?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inversion always returns a chemistry, whatever taste we ask for, so we need a way to judge whether that
chemistry is a reasonable one. Hotelling's :math:`T^2` of the solution answers this: it measures how far
the design sits from the centre of the calibration data, in the same units as the
:ref:`score diagnostics <LVM-Hotellings-T2>` used elsewhere. Designing toward each of the four
held-out cheeses in turn shows the pattern.

.. code-block:: python

	for i in range(4):
	    target = float(holdout["Taste"].iloc[i])
	    t2 = pls.invert(target).hotellings_t2
	    print(f"taste {target:5.1f} -> T2 {t2:.2f}")
	# taste  12.3 -> T2 1.07
	# taste  20.9 -> T2 0.06
	# taste  39.0 -> T2 1.93
	# taste  47.9 -> T2 4.82

The moderate tastes near the middle of the calibration range give designs with small :math:`T^2`; the
more extreme tastes push the design further from the data, and :math:`T^2` grows. A large :math:`T^2` does
not make a design wrong, but it flags that the model is extrapolating and that the predicted taste rests
on less support from the data.

For a single response, then, PLS model inversion and O-PLS model inversion lead to the same set of
designs. They differ in how they reach it: PLS inversion solves an underdetermined system and returns the
minimum-norm point, while O-PLS inversion is a single division once the orthogonal space has been
separated during fitting. The equivalence has been proved for one response; the multiple-response case
remains open (García-Carrión et al., 2025).

.. _LVM-PLS-inversion-multiple-responses:

More than one response
^^^^^^^^^^^^^^^^^^^^^^^^

The equivalence above is for a single response. Model inversion itself is not limited to one output.
Consider the `solvents data set <https://openmv.net/info/solvents>`_: 103 solvents described by seven
physical properties, with two further properties we might want to target, the octanol-water partition
coefficient (:math:`\log P`) and an aqueous solubility. We invert the model to ask which physical
properties give a solvent with a chosen :math:`\log P` and solubility.

.. code-block:: python

	solvents = pd.read_csv("https://openmv.net/file/solvents.csv").dropna()
	x_columns = ["MeltingPoint", "BoilingPoint", "Dielectric", "DipoleMoment",
	             "RefractiveIndex", "ET30", "Density"]
	y_columns = ["logP", "Solubility"]

	model = PLS(n_components=3).fit(solvents[x_columns], solvents[y_columns])
	design = model.invert(pd.Series({"logP": 0.5, "Solubility": 0.0}))

	print(design.null_space_dimension)          # 1
	print(round(design.hotellings_t2, 2))       # 2.46
	print(model.predict(design.x_new.to_frame().T).round(2).to_dict("records")[0])
	# {'logP': 0.5, 'Solubility': -0.0}

Two things change with two responses. First, the target now pins down two score directions instead of
one, so the null space has dimension :math:`A - \text{rank}(\mathbf{Y})`. Here that is
:math:`3 - 2 = 1`: a line of solvent designs, all giving the same :math:`\log P` and solubility. With
only two components the null space would collapse to a single point, because both score directions would
be fixed by the two targets. Second, the O-PLS route does not carry over. O-PLS separates a single
predictive component, so its one-division inversion is defined for one response; with two responses we
solve the inversion directly, as above. The proof that the null space and the orthogonal space coincide
was given for the single-response case; extending it to several responses is noted as open work by
García-Carrión et al. (2025).

.. rubric:: References

* C. M. Jaeckle and J. F. MacGregor, "Industrial applications of product design through the inversion of
  latent variable models", *Chemometrics and Intelligent Laboratory Systems*, 50 (2000): 199-210,
  `doi:10.1016/S0169-7439(99)00058-1 <https://doi.org/10.1016/S0169-7439(99)00058-1>`_.

* J. Trygg and S. Wold, "Orthogonal projections to latent structures (O-PLS)", *Journal of Chemometrics*,
  16 (2002): 119-128, `doi:10.1002/cem.695 <https://doi.org/10.1002/cem.695>`_.

* S. García-Carrión, F. Sartori, J. Borràs-Ferrís, P. Facco, M. Barolo, and A. Ferrer, "On the equivalence
  between null space and orthogonal space in latent variable regression modeling", *Journal of
  Chemometrics*, 39 (2025): e70057, `doi:10.1002/cem.70057 <https://doi.org/10.1002/cem.70057>`_.
