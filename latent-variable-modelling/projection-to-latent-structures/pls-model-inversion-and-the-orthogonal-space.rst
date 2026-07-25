.. _LVM-PLS-model-inversion:

Using a PLS model backwards: model inversion and the null space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far we have used a PLS model in the forward direction: given the inputs in |X|, predict the
outputs in |Y|. Many design problems ask the reverse question. We fix the quality we want and
solve for the inputs that would achieve it. Finding the inputs that give a chosen output is called
*model inversion*, and it is the basis of latent-variable product and process design (`Jaeckle and
MacGregor, 2000
<https://literature.learnche.org/item/180/industrial-applications-of-product-design-through-the-inversion-of-latent-variable-models>`_).

We will use the same :ref:`cheddar-cheese data <LVM-cheddar-cheese-example>` as before: the taste of a
cheese predicted from three chemical measurements, acetic acid, hydrogen sulfide, and lactic acid. The
forward question was "what taste does this chemistry give?" The inversion question is "which chemistry
gives a target taste?"

.. figure:: ../../figures/examples/cheese/cheese-plots-no-random.png
	:alt: Scatterplot matrix of the cheddar-cheese data: acetic acid, hydrogen sulfide, lactic acid and taste
	:width: 600px
	:align: center

	The 30 cheeses in the raw data. The diagonal shows each variable's distribution; the off-diagonal
	panels are the pairwise scatter plots with a least-squares line. The three chemical measurements
	rise together, and each rises with Taste. It is these correlations that give the inverted model
	room to return more than one chemistry for a target taste.

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
	from process_improve.multivariate import PLS, OPLS, MCUVScaler

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

The null space: many recipes, one target
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Held-out cheese 2 has a taste of 20.9. We invert the model to find a chemistry that the model predicts
will give that taste.

.. code-block:: python

	result = pls.invert(y_desired=20.9)

	print(result.x_new.round(2).to_dict())
	# {'Acetic': 5.52, 'H2S': 5.56, 'Lactic': 1.40}
	print(result.null_space_dimension)        # 1

	# Compare the designed chemistry with what cheese 2 actually was.
	actual = holdout[x_columns].iloc[1]
	for label, chemistry in [("Actual", actual), ("Predicted", result.x_new)]:
	    d = pls.diagnose(chemistry.to_frame().T)
	    print(f"{label}: T2 = {float(d.hotellings_t2.iloc[0]):.2f}, "
	          f"SPE = {float(d.spe.iloc[0]):.2f}")
	# Actual: T2 = 0.21, SPE = 0.68
	# Predicted: T2 = 0.06, SPE = 0.00

The prediction at the designed chemistry is exactly 20.9, by construction. To judge whether that design
is a reasonable one, compare it with the cheese we held out. For this model the 99% limits are
:math:`T^2 = 12.14` and :math:`\text{SPE} = 1.60`.

.. list-table:: Cheese 2: its measured chemistry, and the chemistry the inversion returns for a taste of 20.9.
	:header-rows: 1
	:widths: 20 16 16 16 16 16

	*	- Row
		- Acetic
		- H2S
		- Lactic
		- :math:`T^2`
		- SPE
	*	- Actual
		- 5.16
		- 5.04
		- 1.53
		- 0.21
		- 0.68
	*	- Predicted
		- 5.52
		- 5.56
		- 1.40
		- 0.06
		- 0.00

Both rows sit well inside the two limits, so neither is an extrapolation. The predicted chemistry has an
SPE of exactly zero, because the inversion rebuilds the inputs from their scores: the result lies on the
model plane by construction, leaving no residual.

The two rows are close, but "close" in the raw units is hard to read: a gap of 0.5 in hydrogen sulfide
does not mean the same thing as a gap of 0.5 in lactic acid, because the three measurements are on
different scales. Centring and scaling each column puts them on a common footing, where one unit is one
standard deviation of that measurement. The *normalized deviation* is then the sum of the squared
differences between the two rows, in those units.

.. code-block:: python

	scaler = MCUVScaler().fit(X)
	a = scaler.transform(actual.to_frame().T).iloc[0]           # actual, in std deviations
	p = scaler.transform(result.x_new.to_frame().T).iloc[0]     # predicted, in std deviations

	print(a.round(2).to_list())                      # [-0.67, -0.46, 0.30]
	print(p.round(2).to_list())                      # [-0.04, -0.22, -0.15]
	print(round(float(((a - p) ** 2).sum()), 2))     # 0.66

Writing the three terms out, with acetic acid first, then hydrogen sulfide, then lactic acid:

.. math::

	\begin{aligned}
	\text{normalized deviation} &= \left(-0.67 - (-0.04)\right)^2 + \left(-0.46 - (-0.22)\right)^2
	  + \left(0.30 - (-0.15)\right)^2 \\
	&= (-0.63)^2 + (-0.24)^2 + (0.45)^2 \\
	&= 0.39 + 0.06 + 0.21 \\
	&= 0.66
	\end{aligned}

The square root of 0.66 is 0.81, so the cheese we held out sits about 0.8 standard deviations away from
the chemistry the inversion proposed, counting all three measurements together. Acetic acid accounts for
most of that gap.

The null space is the reason ``null_space_dimension`` is not zero. A two-component model has two score
directions, but a single taste value pins down only one of them. The other direction is free: we can move
along it and the predicted taste does not change at all. That free direction is the *null space*. Its
dimension is the number of components minus the rank of the response, here :math:`2 - 1 = 1`, so it is a
line. Every chemistry on that line gives the same predicted taste.

We can walk along the null space by passing coordinates along its basis. In the code and figure we take a
step of -1 and +1 along the basis. The predicted taste stays the same along this basis line. Hence the
name the null space. Only the input variables change, i.e. the chemistry, while the predicted output
remains fixed.

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
direct-inversion solution, and the orange line is the null space: the set of scores that all predict a
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
	                line={"color": "orange"})
	fig.add_scatter(x=[tau[0]], y=[tau[1]], mode="markers", name="direct inversion",
	                marker={"color": "black", "symbol": "square", "size": 10})
	fig.update_layout(xaxis_title="t_1", yaxis_title="t_2")
	fig.show()

.. _LVM-PLS-null-space-figure:

.. figure:: ../../figures/pls/pls-model-inversion-null-space.png
	:alt: Score plot showing the null space and the O-PLS orthogonal space overlapping
	:width: 700px
	:align: center

	Score plot of the two-component model (cheeses 5 to 30). The orange line is the null space for a
	target taste of 20.9, and the black square is the direct-inversion solution. The two orange triangles
	are the -1 step (pointing down) and the +1 step (pointing up) from the code above; both predict a
	taste of 20.9. The red dashed and purple dotted lines are the null spaces for two other target
	tastes, 47.9 and 12.3. All three are parallel: a single-response model has one null-space direction,
	and only the position shifts with the target. The green circles are the O-PLS orthogonal space,
	described in the section that follows.

.. _LVM-PLS-null-space-direction:

Where the null-space line comes from
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The line has to run somewhere, and its direction is not arbitrary. It is fixed entirely by the
:math:`y`-loadings, the two numbers that convert scores into a predicted taste.

Start from how the model predicts. For a two-component model the prediction is a weighted sum of the two
scores, with the :math:`y`-loadings :math:`q_1` and :math:`q_2` as the weights:

.. math::

	\hat{y} = q_1 t_1 + q_2 t_2

For this model :math:`q_1 = 0.546` and :math:`q_2 = -0.262`, both on the centred and scaled taste scale.
Asking for a particular taste sets that expression equal to a constant. Cheese 2's taste of 20.9 is
:math:`(20.9 - 23.69) / 16.4 = -0.17` in scaled units, so the inversion is asking for every pair
:math:`(t_1, t_2)` that satisfies:

.. math::

	0.546\, t_1 - 0.262\, t_2 = -0.17

That is one linear equation in two unknowns, which is the whole reason a line appears. One equation
cannot pin down two coordinates: it removes one degree of freedom and leaves the other free. Rearranged
into the familiar form, the free coordinate traces out

.. math::

	t_2 = -\frac{q_1}{q_2} t_1 + \frac{-0.17}{q_2}
	    = 2.08\, t_1 + 0.65

so the line climbs 2.08 units of :math:`t_2` for every unit of :math:`t_1`. That is the diagonal in the
score plot, and it comes from the ratio of the two :math:`y`-loadings alone, :math:`-q_1/q_2`. Their
absolute sizes do not matter, only their ratio: doubling both would give the same line.

There is a matching geometric statement. Take any two points on the line and subtract their equations.
The constant cancels, leaving

.. math::

	q_1 \Delta t_1 + q_2 \Delta t_2 = 0
	\qquad \text{or} \qquad
	\mathbf{q}^T \Delta \mathbf{t} = 0

Any step along the line is therefore perpendicular to the vector :math:`\mathbf{q} = (q_1, q_2)`. That
vector has a meaning: since :math:`\hat{y} = \mathbf{q}^T \mathbf{t}`, it is the gradient of the
prediction, the direction in the score plot along which the predicted taste changes fastest. Moving at
right angles to a gradient is what keeps a quantity constant, so the null space is a contour line of the
predicted taste drawn over the score plot. Every parallel line in the score plot is another contour, for
another target taste, which is why the three lines in the figure do not converge.

We can confirm both statements from the fitted model.

.. code-block:: python

	q = pls.y_loadings_.to_numpy().ravel()
	print(q.round(3))                      # [ 0.546 -0.262]
	print(round(-q[0] / q[1], 2))          # 2.08, the slope of the line
	print(round(float(g @ q), 12))         # 0.0, the direction is perpendicular to q

The direct-inversion solution fits the same picture. It is
:math:`\boldsymbol{\tau}_\text{DI} = y_\text{des}\, \mathbf{q} / (\mathbf{q}^T\mathbf{q})`, which points
along :math:`\mathbf{q}` itself, so it is the point where a perpendicular dropped from the origin meets
the line. That is what makes it the solution of smallest score norm. Here it is
:math:`(-0.253, 0.121)`, pointing opposite to :math:`\mathbf{q}` because the requested taste of 20.9
sits below the training average of 23.7.

Two further points are worth making. First, the perpendicularity is a statement about the score
coordinates, so it looks like a right angle on the page only when both axes are drawn to the same scale.
Second, the same reasoning is what the code performs in general. For one response,
``null_space_basis`` comes from a singular value decomposition of the :math:`y`-loadings: the first left
singular vector points along :math:`\mathbf{q}`, and the remaining :math:`A-1` span everything
perpendicular to it. With two components that leaves a single perpendicular direction, a line; with three
components it leaves a plane, and so on.

Finally, it is worth asking what that direction means in the chemistry, rather than in the scores.
Multiplying the direction by the |X|-loadings maps it back to the three measurements, and a step of
:math:`+1` moves acetic acid by :math:`+0.57`, hydrogen sulfide by :math:`-0.54`, and lactic acid by only
:math:`+0.06`, in the original units. Moving along the null space therefore trades acetic acid up against
hydrogen sulfide down, leaving lactic acid nearly alone. Both of those measurements rise with taste in
this data set, with correlations of 0.56 and 0.77, so raising one while lowering the other leaves the
predicted taste where it was. That trade-off is what the diagonal line is recording.

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
same way and span the same line. This is what the green circles in the
:ref:`score plot <LVM-PLS-null-space-figure>` show: they are the orthogonal space projected into the PLS
score plot, and they lie on the orange null-space line.

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

.. _LVM-PLS-specification-regions:

Turning the inversion around: a specification region
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Everything so far has aimed at a single target taste. In practice a product is rarely specified by one
number: it is accepted over a range. Once we ask for a range instead of a point, the inversion answers a
different and often more useful question. Rather than "which chemistry gives a taste of 20.9?", we ask
"which chemistries give a taste we would accept?" The set of inputs that answer it is called a
:index:`multivariate specification region <single: multivariate specification region>`, and for incoming
raw materials it is a statement of what we are prepared to buy.

Building it needs nothing new. Each acceptable taste has its own null space, and those null spaces are
parallel, as the :ref:`score plot <LVM-PLS-null-space-figure>` shows. Sweeping
the target across the acceptable range sweeps its null space across the score plot, and the swept lines
fill out a region.

Two boundaries close the region off. The acceptable range of taste bounds it in one direction. In the
other direction, along each null space, the region would run on without limit, so we bound it by the
Hotelling's :math:`T^2` limit: solutions beyond it are extrapolations, as
:ref:`the previous section <LVM-PLS-inversion-in-practice>` described. `Paris and co-workers (2021)
<https://literature.learnche.org/item/181/establishing-multivariate-specification-regions-for-incoming-raw-materials-using-projection-to-latent-structure-models-comparison-between-direct-mapping-and-model-inversion>`_
do exactly this, constraining the region by the 95% :math:`T^2` limit so it stays inside the space the
data support.

The idea is as old as the method. Jaeckle and MacGregor called the result a *window of process operating
conditions*: they moved along the null space over a range that kept the conditions within those seen in
the past, then applied engineering judgement to pick a point in that window, such as the most economical
or most energy-efficient one. Bounding by :math:`T^2` is a way of making "within the range of past
operating conditions" a single, testable number.

Suppose a taste between 20 and 40 is acceptable.

.. code-block:: python

	t2_limit = pls.hotellings_t2_limit(0.95)

	region = []
	for target in np.linspace(20.0, 40.0, 5):        # the range of taste we accept
	    for step in np.linspace(-6, 6, 2001):        # walk along that target's null space
	        candidate = pls.invert(target, null_space_coordinates=[step])
	        if candidate.hotellings_t2 <= t2_limit:
	            region.append(candidate.x_new)

	region = pd.DataFrame(region)
	print(round(t2_limit, 2))                        # 7.36
	print(region.agg(["min", "max"]).round(2))
	#      Acetic   H2S  Lactic
	# min    4.35  4.44    1.25
	# max    6.99  9.47    1.86

A cheese whose chemistry falls in this region is predicted to have an acceptable taste. Note that these
minima and maxima are the box that encloses the region, not the region itself: the region is a slanted
band in the three chemical measurements, and a lot may sit inside every one of the three ranges while
still lying outside the band. Note also that the enclosing box reaches slightly past the observed range
of acetic acid in the training cheeses (4.48 to 6.46). The :math:`T^2` limit bounds the joint distance
from the centre of the model, not each measurement separately, so a corner of the region can sit a little
outside the range of any one measurement.

Inversion is not the only route to a specification region. The inputs can also be mapped directly into a
region without inverting a model, an approach known as direct mapping. Paris and co-workers (2021)
compare the two on simulated data and find neither is better in every case: model inversion accepted more
of the genuinely good lots in their study, while direct mapping is simpler to compute and leaves more
freedom in the shape of the region. Which suits a given problem depends on the relative cost of accepting
a lot that turns out to be bad and rejecting one that would have been fine.

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

* C. M. Jaeckle and J. F. MacGregor, "`Industrial applications of product design through the inversion of
  latent variable models
  <https://literature.learnche.org/item/180/industrial-applications-of-product-design-through-the-inversion-of-latent-variable-models>`_",
  *Chemometrics and Intelligent Laboratory Systems*, **50** (2000): 199-210.

* J. Trygg and S. Wold, "Orthogonal projections to latent structures (O-PLS)", *Journal of Chemometrics*,
  16 (2002): 119-128, `doi:10.1002/cem.695 <https://doi.org/10.1002/cem.695>`_.

* A. Paris, C. Duchesne, and É. Poulin, "`Establishing multivariate specification regions for incoming
  raw materials using projection to latent structure models: comparison between direct mapping and model
  inversion
  <https://literature.learnche.org/item/181/establishing-multivariate-specification-regions-for-incoming-raw-materials-using-projection-to-latent-structure-models-comparison-between-direct-mapping-and-model-inversion>`_",
  *Frontiers in Analytical Science*, **1** (2021): 729732.

* S. García-Carrión, F. Sartori, J. Borràs-Ferrís, P. Facco, M. Barolo, and A. Ferrer, "On the equivalence
  between null space and orthogonal space in latent variable regression modeling", *Journal of
  Chemometrics*, 39 (2025): e70057, `doi:10.1002/cem.70057 <https://doi.org/10.1002/cem.70057>`_.
