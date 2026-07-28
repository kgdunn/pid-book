.. _LVM-PLS-model-inversion:

Using a PLS model backwards: model inversion and the null space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far we have used a PLS model in the forward direction: given the inputs in |X|, predict the
outputs in |Y|. Many design problems ask the reverse question. We fix the quality we want and
solve for the inputs that would achieve it. Finding the inputs that give a chosen output is called
*model inversion*, and it is the basis of latent-variable product and process design (`Jaeckle and
MacGregor, 2000
<https://literature.learnche.org/item/180/industrial-applications-of-product-design-through-the-inversion-of-latent-variable-models>`_).

The answer is more interesting than a single recipe. A PLS model compresses several correlated inputs
into a few latent directions, and one target value can pin down only one of them. Everything left over
is free, so inversion returns not *the* recipe but a flat set of them, every one of which the model
says will hit the target. Where that freedom comes from, what it is worth, and how much of it the data
support is the subject of this section.

That freedom lives in a part of the model few people look at: the systematic variation the model
captures and then finds has no bearing on the response. It is usually filtered out to make a model
easier to read. For these cheeses it is 18.3% of the variation in the inputs, none of which moves the
taste.

The running example is the same :ref:`cheddar-cheese data <LVM-cheddar-cheese-example>` as before, a
small and well-worn data set. Thirty cheddar cheeses were each measured for three things, the
concentrations of acetic acid, hydrogen sulfide and lactic acid, and each was given a taste score by a
panel. The forward question was "what taste do these three measurements imply?" The inversion question
is "which three measurements would give me a taste I have chosen?"

.. figure:: ../../figures/examples/cheese/cheese-plots-no-random.png
	:alt: Scatterplot matrix of the cheddar-cheese data: acetic acid, hydrogen sulfide, lactic acid and taste
	:width: 600px
	:align: center

	The 30 cheeses in the raw data. The diagonal shows each variable's distribution; the off-diagonal
	panels are the pairwise scatter plots with a least-squares line. The three inputs rise together,
	and each rises with Taste. It is these correlations that give the inverted model room to return
	more than one set of inputs for a target taste.

.. _LVM-PLS-inversion-components:

Why inversion needs more than the predictive number of components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When we chose the number of components for prediction in :ref:`the section above
<LVM-PLS-number-of-components>`, cross-validation kept a single component: one component is enough
to predict Taste, and a second does not improve prediction. Inversion places a second and different
demand on the model, though. To rebuild a complete set of three input values from one target number,
the model has to describe the |X|-space well enough to map a score back into it, not merely describe
the |Y|-space. A one-component model spans only a line in the input space, so it can return exactly
one recipe, and the whole question of equivalent designs never arises.

A second component lets the model describe the plane on which the calibration cheeses actually lie,
and that is what opens up the set of equivalent designs. So a two-component model is fitted here even
though the second did not earn its place on predictive grounds.

So that the targets stay independent of the model, the first four cheeses are set aside and never shown
to it. They become the targets: for each one we ask the model to design a cheese with that taste, then
compare what it proposes against what that cheese actually was. Their tastes span most of the range,
which matters later, because designing toward an extreme target turns out to cost more than designing
toward a middling one.

.. _LVM-PLS-holdout-table:

.. list-table:: The four held-out cheeses, used only as targets. The model is fitted on the other 26,
	whose tastes run from 0.7 to 57.2 with a mean of 23.7.
	:header-rows: 1
	:widths: 14 18 18 18 18

	*	- Cheese
		- Acetic
		- H2S
		- Lactic
		- Taste
	*	- 1
		- 4.54
		- 3.14
		- 0.86
		- 12.3
	*	- 2
		- 5.16
		- 5.04
		- 1.53
		- 20.9
	*	- 3
		- 5.37
		- 5.44
		- 1.57
		- 39.0
	*	- 4
		- 5.76
		- 7.50
		- 1.81
		- 47.9

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.multivariate import PLS, OPLS, MCUVScaler

	cheese = pd.read_csv("https://openmv.net/file/cheddar-cheese.csv")
	x_columns = ["Acetic", "H2S", "Lactic"]

	train = cheese.iloc[4:]        # cheeses 5 to 30: used to build the model
	holdout = cheese.iloc[:4]      # cheeses 1 to 4: the targets we design toward
	X = train[x_columns]
	Y = train[["Taste"]]

	pls = PLS(n_components=2).fit(X, Y)
	print(round(float(pls.r2_cumulative_.iloc[-1]), 3))   # R2 on Taste: 0.672

It explains about 67% of the variation in Taste, which is enough for what follows: the null space is a
property of the model's geometry rather than of its predictive accuracy. That geometry is itself
estimated from the same 26 cheeses, though, so it carries one caveat, which we return to
:ref:`once the geometry is on the table <LVM-PLS-null-space-uncertainty>`.

.. _LVM-PLS-null-space:

The null space: many recipes, one target
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Held-out cheese 2 has a taste of 20.9. We invert the model to find the inputs that the model
predicts will give that taste.

.. code-block:: python

	result = pls.invert(y_desired=20.9)

	print(result.x_new.round(2).to_dict())
	# {'Acetic': 5.52, 'H2S': 5.56, 'Lactic': 1.4}
	print(result.null_space_dimension)        # 1

	# Compare the designed inputs with what cheese 2 actually was.
	actual = holdout[x_columns].iloc[1]
	for label, inputs in [("Actual", actual), ("Predicted", result.x_new)]:
	    d = pls.diagnose(inputs.to_frame().T)
	    print(f"{label}: T2 = {float(d.hotellings_t2.iloc[0]):.2f}, "
	          f"SPE = {float(d.spe.iloc[0]):.2f}")
	# Actual: T2 = 0.21, SPE = 0.68
	# Predicted: T2 = 0.06, SPE = 0.00

A recipe comes back, which is unremarkable. The second line is the interesting one. The null space has
dimension 1, which is the model saying that this is not *the* answer but one point on a line of
answers. Two score directions, one target: the target fixes one of them and leaves the other free.
Anything we do along that free direction changes the recipe while leaving the prediction exactly where
it was. That free direction is the *null space*, and its dimension is the number of components minus
the rank of the response, here :math:`2 - 1 = 1`.

We can walk along it by passing coordinates along its basis. Stepping one unit either way:

.. code-block:: python

	for step in (-1.0, 1.0):
	    moved = pls.invert(y_desired=20.9, null_space_coordinates=[step])
	    taste = float(pls.predict(moved.x_new.to_frame().T).iloc[0, 0])
	    print(moved.x_new.round(2).to_list(), "->", round(taste, 2))
	# [4.95, 6.10, 1.33] -> 20.9
	# [6.09, 5.02, 1.46] -> 20.9

Collecting those points, and putting the measured cheese alongside for comparison:

.. code-block:: python

	scaler = MCUVScaler().fit(X)
	a = scaler.transform(actual.to_frame().T).iloc[0]           # actual, in std deviations

	designs = {
	    "Actual": actual,
	    "Predicted at step -1": pls.invert(20.9, null_space_coordinates=[-1.0]).x_new,
	    "Predicted at step 0": result.x_new,
	    "Predicted at step +1": pls.invert(20.9, null_space_coordinates=[+1.0]).x_new,
	}
	for label, inputs in designs.items():
	    d = pls.diagnose(inputs.to_frame().T)
	    v = scaler.transform(inputs.to_frame().T).iloc[0]
	    print(f"{label:<22}{inputs.round(2).to_list()}  "
	          f"T2 = {float(d.hotellings_t2.iloc[0]):.2f}, SPE = {float(d.spe.iloc[0]):.2f}, "
	          f"deviation = {float(((a - v) ** 2).sum()):.2f}")

.. _LVM-PLS-null-space-steps-table:

.. list-table:: Cheese 2, and three points along its null space. All four rows predict a taste of 20.9.
	:header-rows: 1
	:widths: 22 12 10 10 10 10 10 16

	*	- Row
		- Target taste
		- Acetic
		- H2S
		- Lactic
		- :math:`T^2`
		- SPE
		- Input-space deviation
	*	- Measured cheese
		- 20.9
		- 5.16
		- 5.04
		- 1.53
		- 0.21
		- 0.68
		- 0.00
	*	- Design, step -1
		- 20.9
		- 4.95
		- 6.10
		- 1.33
		- 1.63
		- 0.00
		- 0.82
	*	- Design, step 0
		- 20.9
		- 5.52
		- 5.56
		- 1.40
		- 0.06
		- 0.00
		- 0.66
	*	- Design, step +1
		- 20.9
		- 6.09
		- 5.02
		- 1.46
		- 2.44
		- 0.00
		- 2.66

Read down the three designs and the inputs move substantially. Acetic acid climbs from about 5 to 6
while hydrogen sulfide falls from 6.10 to 5.02, with lactic acid rising slightly. These are not small
adjustments, and yet every one of the three still reaches a taste of 20.9. That is the practical
content of the null space: if several recipes all hit the target, we are free to choose among them on
grounds the model never saw, such as cost, supplier availability, or whichever raw material happens to
be in the yard this week. This same trade-off comes back when we reach
:ref:`O-PLS <LVM-PLS-orthogonal-space>` below, where it appears directly as one of the model's axes.

Two columns need reading carefully. The SPE of exactly zero is a property of the arithmetic, not a
claim about cheese: the inversion rebuilds the inputs from their scores, so the result lies on the
model plane by construction. Every real cheese carries variation the two components miss, which is why
the measured row shows 0.68. So a design is an idealised point on the plane. A cheese later made to
that specification will land near the plane, not exactly on it, and its own SPE is what measures the
gap.

:math:`T^2` is the column that does change, and it measures how far each design sits from the centre of
the calibration data. Step 0, the direct-inversion solution, has the smallest at 0.06; stepping either
way moves the design outward, to 1.63 and 2.44. The freedom along the null space is free in terms of
predicted taste, but not in terms of how much the data support the design. All rows sit well inside the
99% limits of :math:`T^2 = 12.14` and :math:`\text{SPE} = 1.60`, which are the limits for a *new*
observation rather than for one of the 26 that built the model: the right choice when judging a
proposed design rather than summarising a calibration one.

.. _LVM-PLS-input-space-deviation:

One quantity is worth defining now, because it recurs. Comparing recipes in raw units is hard to read:
a gap of 0.5 in hydrogen sulfide does not mean what a gap of 0.5 in lactic acid means. Centring and
scaling each input puts them on a common footing where one unit is one standard deviation, and the sum
of squared differences in those units is the *input-space deviation*. For cheese 2 against its design
it is 0.66, so the held-out cheese sits about 0.8 standard deviations from the proposed recipe.

A score plot shows the picture directly. The calibration cheeses are the points, the orange square
is the direct-inversion solution, and the orange line is the null space: the set of scores that all
predict a taste of 20.9.

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
	                marker={"color": "orange", "symbol": "square", "size": 12,
	                        "line": {"color": "black", "width": 1}})
	fig.update_layout(xaxis_title="t_1", yaxis_title="t_2")
	fig.show()

.. _LVM-PLS-null-space-figure:

.. figure:: ../../figures/pls/pls-model-inversion-null-space.png
	:alt: Score plot showing the null space and the O-PLS orthogonal space overlapping
	:width: 700px
	:align: center

	Score plot of the two-component model (cheeses 5 to 30). Each cheese is drawn with an area
	proportional to its measured taste, the legend marker being the size for a taste of 20. The orange
	line is the null space for a
	target taste of 20.9, and the orange square is the direct-inversion solution. The two triangles are
	the -1 step (pointing down) and the +1 step (pointing up) from the code above; both predict a
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
score plot, and it comes from the ratio of the two :math:`y`-loadings alone, :math:`-q_1/q_2`.

There is a matching geometric statement. Take any two points on the line and subtract their equations.
The constant cancels, leaving

.. math::

	q_1 \Delta t_1 + q_2 \Delta t_2 = 0
	\qquad \text{or} \qquad
	\mathbf{q}^T \Delta \mathbf{t} = 0

Any step along the line is therefore perpendicular to the vector :math:`\mathbf{q} = (q_1, q_2)`.
That vector has a meaning: since :math:`\hat{y} = \mathbf{q}^T \mathbf{t}`, it is the gradient of
the prediction, the direction in the score plot along which the predicted taste changes fastest.
Moving at right angles to a gradient is what keeps a quantity constant. It is like walking a path on
a hill where you stay at exactly the same elevation (the output value) while your latitude and
longitude change (a different set of inputs). So the null space is that contour line: the predicted
taste stays the same even though you are at different coordinates in the score plot. Every parallel
line in the score plot is another contour, for another target taste, which is why the three lines in
the figure do not converge.

.. _LVM-PLS-null-space-geometry-figure:

.. figure:: ../../figures/pls/pls-null-space-geometry.png
	:alt: The gradient vector q with the null space and further contours drawn perpendicular to it
	:width: 620px
	:align: center

	Left: the same score plot, with the areas again proportional to taste and both axes drawn to the
	same scale so that angles are true. The maroon arrow is the gradient :math:`\mathbf{q}`, the
	direction in which the predicted taste rises fastest. The orange line is the null space for a taste
	of 20.9, at right angles to it, and the grey dotted lines are the contours for tastes of 10, 30 and
	40. The orange square is the direct-inversion solution and the two orange triangles are the -1 and
	+1 steps, the same points marked in the score plot above, so the two figures can be read against
	each other.

	Right: the boxed region enlarged, at the scale the next argument needs. The three arrows form a
	right triangle, from the origin to the direct-inversion solution, from there along the contour to
	the +1 step, and back to the origin.

We can confirm both the slope and the perpendicularity from the fitted model.

.. code-block:: python

	q = pls.y_loadings_.to_numpy().ravel()
	print(q.round(3))                      # [ 0.546 -0.262]
	print(round(-q[0] / q[1], 2))          # 2.08, the slope of the line
	print(g.round(3))                      # [0.433 0.902], the null-space direction
	print(round(float(g @ q), 12))         # 0.0, the direction is perpendicular to q

The particular solution the inversion returns is the shortest one, and the same picture shows where it
comes from. Split any candidate :math:`\boldsymbol{\tau}` into a part along :math:`\mathbf{q}` and a
part perpendicular to it. The perpendicular part contributes nothing to the prediction, since
:math:`\hat{y} = \mathbf{q}^T \boldsymbol{\tau}` ignores it, but it does add to the length of
:math:`\boldsymbol{\tau}`. The shortest solution therefore carries no perpendicular part at all, which
is to say it lies along :math:`\mathbf{q}`. Writing it as
:math:`\boldsymbol{\tau} = c\, \mathbf{q}` and requiring
:math:`\mathbf{q}^T \boldsymbol{\tau} = y_\text{des}` gives
:math:`c\, \mathbf{q}^T \mathbf{q} = y_\text{des}`, so that

.. math::

	\boldsymbol{\tau}_\text{DI} = \frac{y_\text{des}\, \mathbf{q}}{\mathbf{q}^T \mathbf{q}}

Geometrically that is the point where a perpendicular dropped from the origin meets the line. Here
:math:`\mathbf{q}^T \mathbf{q} = 0.367` and :math:`y_\text{des} = -0.17`, which gives
:math:`\boldsymbol{\tau}_\text{DI} = (-0.253, 0.121)`. It points opposite to :math:`\mathbf{q}` because
the requested taste of 20.9 sits below the training average of 23.7.

Calling it the smallest-norm solution takes two further steps that are easy to skip. The norm
:math:`\|\boldsymbol{\tau}\|` is the distance from the origin of the
score plot out to the point, so asking for the smallest norm is asking which design on the null-space
line sits closest to the origin. Writing a general solution as
:math:`\boldsymbol{\tau}_\text{DI} + s\,\mathbf{g}`, for a step of size :math:`s` along the unit
null-space direction :math:`\mathbf{g}`, the two parts are at right angles, so Pythagoras applies:

.. math::

	\left\| \boldsymbol{\tau}_\text{DI} + s\,\mathbf{g} \right\|^2
	  = \left\| \boldsymbol{\tau}_\text{DI} \right\|^2 + s^2

The step contributes :math:`s^2`, which is positive for every step other than none at all. The norm is
therefore smallest at :math:`s = 0`, and it grows in either direction. Here
:math:`\|\boldsymbol{\tau}_\text{DI}\| = 0.281`, while the :math:`-1` and :math:`+1` steps both sit at
:math:`\sqrt{0.281^2 + 1^2} = 1.039`. The right angle is the reason: had the null space met the
solution at any other angle, moving one way along it would have carried the design closer to the origin
than :math:`\boldsymbol{\tau}_\text{DI}`.

The score norm is not the only way to measure how far a design sits from the centre of the model.
Hotelling's :math:`T^2` measures the same thing, but it divides each score by that score's standard
deviation before squaring, so a component with little spread counts for more. It is a weighted sum of
squares rather than a plain one. Both can be plotted against the step size, which shows what the walk
along the null space costs.

.. code-block:: python

	sf = pls.scaling_factor_for_scores_.to_numpy()   # one standard deviation per score
	steps = np.linspace(-2, 2, 401)
	points = tau + steps[:, None] * g                # every design on the null space

	norm_squared = (points ** 2).sum(axis=1)
	t2 = ((points / sf) ** 2).sum(axis=1)

	fig = go.Figure()
	fig.add_scatter(x=steps, y=norm_squared, mode="lines", name="squared score norm",
	                line={"color": "orange"})
	fig.add_scatter(x=steps, y=t2, mode="lines", name="Hotelling's T2",
	                line={"color": "darkblue"})
	fig.update_layout(xaxis_title="step s along the null space",
	                  yaxis_title="squared distance from the model centre")
	fig.show()

	print(sf.round(3))                                        # [1.468 0.657]
	print(round(-float((tau / sf**2) @ g) / float((g / sf**2) @ g), 3))
	# -0.103, the step at which T2 is least

.. _LVM-PLS-null-space-distance-figure:

.. figure:: ../../figures/pls/pls-null-space-distance.png
	:alt: Squared score norm and Hotelling's T2 plotted against the step along the null space
	:width: 700px
	:align: center

	Two measures of how far a design sits from the centre of the model, as a step of size :math:`s` is
	taken along the null space from the direct-inversion solution. The predicted taste is 20.9 at every
	point on the horizontal axis. The orange curve is the squared score norm, least exactly at
	:math:`s = 0`. The blue curve is Hotelling's :math:`T^2`, least at :math:`s = -0.103`. The three
	blue markers are the rows tabulated earlier for steps of :math:`-1`, :math:`0` and :math:`+1`.

Both curves are parabolas in :math:`s`, but they are not the same parabola. The orange one is
:math:`\|\boldsymbol{\tau}_\text{DI}\|^2 + s^2` from the equation above, so its lowest point is exactly
the direct-inversion solution. The blue one is tilted, and reaches its lowest point at
:math:`s = -0.103` instead. The two scores have standard deviations of 1.468 and 0.657, so :math:`t_2`
counts for more in :math:`T^2` than in the plain norm, and the null-space direction
:math:`\mathbf{g} = (0.433, 0.902)` is mostly :math:`t_2`.

The distinction is worth keeping straight, because it says what the direct-inversion solution does and
does not give. It is the smallest-norm design, exactly. It is not quite the design of smallest
:math:`T^2`: a step of :math:`-0.103` would reach :math:`T^2 = 0.043` rather than 0.064. The gap is
small here and the direct-inversion solution is still the closest of the three tabulated steps, but the
two criteria are different questions and a model with more unequal score spreads would separate them
further.

Two further points are worth making. First, the perpendicularity is a statement about the score
coordinates, so it reads as a right angle on the page only when both axes are drawn to the same scale, as
they are in the figure above but not in the earlier
:ref:`score plot <LVM-PLS-null-space-figure>`, where the two scores have different spreads.
Second, the same reasoning is what the code performs in general. For one response,
``null_space_basis`` comes from a singular value decomposition of the :math:`y`-loadings: the first left
singular vector points along :math:`\mathbf{q}`, and the remaining :math:`A-1` span everything
perpendicular to it. With two components that leaves a single perpendicular direction, a line; with three
components it leaves a plane, and so on.

Finally, it is worth asking what that direction means for the inputs, rather than in the scores.
Multiplying the direction by the |X|-loadings maps it back to the three measurements, and a step of
:math:`+1` moves acetic acid by :math:`+0.57`, hydrogen sulfide by :math:`-0.54`, and lactic acid by only
:math:`+0.06`, in the original units. Moving along the null space therefore trades acetic acid up against
hydrogen sulfide down, leaving lactic acid nearly alone. Both of those measurements rise with taste,
correlating :math:`+0.55` and :math:`+0.76` across the thirty cheeses, as the scatterplot matrix at the
start of this section reports, so raising one while lowering the other leaves the predicted taste where
it was. That trade-off is what the diagonal line is recording.

.. _LVM-PLS-null-space-uncertainty:

How well is that direction determined?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the caveat promised earlier. Every number quoted so far comes from one model fitted to 26
cheeses, and the direction of the null
space rests on the second :math:`y`-loading, :math:`q_2 = -0.262`. That component was the one
cross-validation did not keep. It adds 3.0% to :math:`R^2Y`, against 64.3% for the first. It is worth
asking how much of the geometry survives if the 26 cheeses had come out slightly differently.

Refitting the model on bootstrap resamples of the calibration set answers that directly.

.. code-block:: python

	rng = np.random.default_rng(0)
	reference = np.array([0.948, -0.238, 0.211])         # the direction reported below
	reference = reference / np.linalg.norm(reference)

	q2, slopes, angles, designs, boot_lines = [], [], [], [], []
	for _ in range(2000):
	    sample = train.iloc[rng.integers(0, len(train), len(train))]
	    boot = PLS(n_components=2).fit(sample[x_columns], sample[["Taste"]])
	    q_b = boot.y_loadings_.to_numpy().ravel()
	    q2.append(q_b[1])
	    slopes.append(-q_b[0] / q_b[1])

	    result_b = boot.invert(20.9)
	    designs.append(result_b.x_new.to_numpy())
	    boot_lines.append((result_b.scores.to_numpy(),
	                       result_b.null_space_basis.to_numpy().ravel()))
	    d = result_b.null_space_basis.to_numpy().ravel() @ boot.x_loadings_.to_numpy().T
	    d = d / np.linalg.norm(d)
	    # A direction and its negative describe the same line, so compare without sign.
	    angles.append(np.degrees(np.arccos(np.clip(abs(d @ reference), 0, 1))))

	print(np.percentile(q2, [2.5, 97.5]).round(3))        # [-0.56   0.377]
	print(round(float(np.mean(np.array(q2) > 0)), 3))     # 0.244, the share that change sign
	print(np.percentile(slopes, [2.5, 97.5]).round(2))    # [-5.09  6.13]
	print(np.percentile(angles, [50, 90, 95]).round(1))   # [20.6 54.4 68.3]
	print(round(float(np.mean(np.array(angles) > 45)), 2))  # 0.15
	print(np.percentile(designs, [2.5, 97.5], axis=0).round(2))
	# [[5.24 4.97 1.3 ]
	#  [5.74 6.26 1.49]]

The direction is poorly determined. A 95% bootstrap interval for :math:`q_2` runs from
:math:`-0.56` to :math:`+0.38`, so it straddles zero, and in 24% of the resamples it changes sign. The
slope of the null-space line is a ratio with that near-zero quantity in the denominator, so its
interval, :math:`-5.1` to :math:`+6.1`, is wide enough to be of little use. Read as a line in the
inputs, the resampled null space sits a median of 21 degrees away from the direction reported here, and
more than 45 degrees away in 15% of the resamples.

The direct-inversion solution itself holds up much better. Its 95% intervals are 5.24 to 5.74 for
acetic acid, 4.97 to 6.26 for hydrogen sulfide, and 1.30 to 1.49 for lactic acid, each narrow next to
the spread of the calibration cheeses, which run from 4.48 to 6.46 in acetic acid and from 3.00 to
10.20 in hydrogen sulfide. The reason for the difference is worth seeing: the solution
depends mostly on :math:`q_1`, which is estimated well, while the null-space direction depends on the
ratio of :math:`q_1` to :math:`q_2`.

Drawing every one of those refits says the same thing without any percentiles. Each is a line, so
plotting all 2000 of them faintly enough to overlap turns the spread into a density.

.. code-block:: python

	fig = go.Figure()
	for tau_b, g_b in boot_lines:                      # one faint line per refit
	    segment = np.array([tau_b + s * g_b for s in (-9, 9)])
	    fig.add_scatter(x=segment[:, 0], y=segment[:, 1], mode="lines", showlegend=False,
	                    line={"color": "rgba(230, 130, 10, 0.03)"})
	fig.add_scatter(x=scores.iloc[:, 0], y=scores.iloc[:, 1], mode="markers",
	                name="calibration cheeses")
	fig.update_layout(xaxis_title="t_1", yaxis_title="t_2")
	fig.show()

.. _LVM-PLS-null-space-bootstrap-figure:

.. figure:: ../../figures/pls/pls-null-space-bootstrap.png
	:alt: A fan of bootstrap null-space lines, and a histogram of their angles
	:width: 700px
	:align: center

	Left: one faint line for each of 2000 refits, each the null space that refit would have returned.
	The fan pinches near the direct-inversion solution and spreads from there. Right: the same spread
	measured as an angle from the direction the full calibration set gives, compared without sign since
	a direction and its negative describe the same line. The shaded band holds the 15% of refits that
	land more than 45 degrees away.

That pinch is the point-and-direction asymmetry in one picture. The refits nearly agree on where the
solution sits, and disagree widely on which way the line runs through it.

So the two statements this section makes are not equally firm. That a set of inputs reaching a target
taste exists, and roughly where it sits, is supported by these data. Which direction one may then walk
without changing the prediction is not pinned down by 26 cheeses and a component that
cross-validation set aside. The null space is exactly what the algebra says it is for a *given* model;
what the algebra cannot supply is certainty that this model's second component points where the next
26 cheeses would point it. The figures that follow quote three decimals because that is what the
arithmetic returns, not because the data support that precision.

None of this makes the geometry wrong or the method unusable. It sets the terms on which to use it: a
design proposed at the direct-inversion solution rests on firmer ground than one reached by a long walk
along the null space, and a walk of any length is worth repeating on a refitted model before it is
acted on.

.. _LVM-PLS-orthogonal-space:

The same space, reached a different way: O-PLS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Orthogonal projections to latent structures (O-PLS) was developed in a separate line of work, for a
different reason: to make a model easier to interpret. What it does is quickest to see by starting
from the PLS model already fitted here, and taking one step at a time.

Start with a single PLS component, which carries two vectors rather than one. The weight
:math:`\mathbf{w}_1` is the direction we choose to look along, picked so that the score it produces
lines up with the response. The loading :math:`\mathbf{p}_1` is what we find afterwards: regress the
inputs back onto that score, and the loading records how strongly each input moved with it. The weight
is an instruction, the loading is a measurement.

For the first component of the cheese model those two vectors are close, but they are not the same.

.. _LVM-PLS-weight-loading-table:

.. list-table:: The two vectors of the first PLS component, their difference, and what that difference becomes. Entries are in the mean-centred, unit-variance units the model works in.
	:header-rows: 1
	:widths: 38 14 14 14 20

	*	- Vector
		- Acetic
		- H2S
		- Lactic
		- Angle to :math:`\mathbf{w}_1`, in degrees
	*	- Weight :math:`\mathbf{w}_1`
		- 0.474
		- 0.657
		- 0.586
		- 0
	*	- Loading :math:`\mathbf{p}_1`
		- 0.552
		- 0.600
		- 0.587
		- 5.49
	*	- Difference :math:`\mathbf{p}_1 - \mathbf{w}_1`
		- 0.078
		- -0.057
		- 0.001
		- 90
	*	- That difference, scaled to unit length
		- 0.808
		- -0.590
		- 0.008
		- 90

Why should they differ at all? The weight was aimed at taste. But it was not aimed only at taste, and
:ref:`the mathematical interpretation of PLS <LVM_PLS_mathematical_interpretation>` says why. Each
component is chosen to maximise the *covariance* between the |X|-score and the |Y|-score, and
covariance factors into three parts: the correlation between the two scores, the variation the score
captures in |X|, and the variation it captures in |Y|. Maximising covariance is therefore not the same
as maximising correlation. A direction that lines up slightly less well with taste, but which accounts
for more of the spread among the cheeses, can give the larger covariance, so the weight settles
somewhere between pointing at taste and pointing where the inputs vary most.

The score that direction produces consequently carries along whatever else happens to vary in that same
pattern across the cheeses. The loading is a plain regression of the inputs back onto that score, so it
records all of it, the part related to taste and the part not. The difference between the loading and
the weight is therefore the part of the variation that travelled with the score without being about
taste.

That difference is simpler to write down than it looks. For every PLS component the weight and its own
loading satisfy :math:`\mathbf{w}_a^T \mathbf{p}_a = 1`:

.. math::

	\mathbf{w}_a^T \mathbf{p}_a
	  = \mathbf{w}_a^T \left( \frac{\mathbf{X}^T \mathbf{t}_a}{\mathbf{t}_a^T \mathbf{t}_a} \right)
	  = \frac{\left(\mathbf{X} \mathbf{w}_a\right)^T \mathbf{t}_a}{\mathbf{t}_a^T \mathbf{t}_a}
	  = \frac{\mathbf{t}_a^T \mathbf{t}_a}{\mathbf{t}_a^T \mathbf{t}_a}
	  = 1

Taking away from the loading the part
of it that lies along the weight therefore leaves a plain subtraction, and what is left is exactly
perpendicular to the weight:

.. math::

	\left(\mathbf{p}_1 - \mathbf{w}_1\right)^T \mathbf{w}_1
	  = \mathbf{p}_1^T \mathbf{w}_1 - \mathbf{w}_1^T \mathbf{w}_1 = 1 - 1 = 0

That perpendicular difference is the orthogonal direction. The orthogonal direction is simply the
amount by which the first PLS loading misses the first PLS weight. For these cheeses the difference is
:math:`(0.078, -0.057, 0.001)`, which scaled to unit length is :math:`(0.808, -0.590, 0.008)`. Nothing
was searched for or optimised to get it: it is a subtraction between two vectors the PLS model had
already produced.

O-PLS is what follows from taking that direction seriously. Instead of leaving the non-taste variation
mixed into the first component, it removes that direction from |X| first, and computes the predictive
component afterwards, on what is left.

The fitted model reports the two directions as ``opls.predictive_weights_`` and
``opls.orthogonal_weights_``, the second carrying one column per orthogonal component asked for.

.. code-block:: python

	opls = OPLS(n_orthogonal_components=1).fit(X, Y)

	print(opls.predictive_weights_.round(3).to_numpy())           # [0.474 0.657 0.586]
	print(opls.orthogonal_weights_.round(3).to_numpy().ravel())   # [ 0.808 -0.59   0.008]
	print(opls.predictive_loadings_.round(3).to_numpy())          # [0.472 0.654 0.591]

	print(pls.x_weights_.to_numpy().round(3))    # the PLS weights, side by side
	# [[ 0.474  0.808]
	#  [ 0.657 -0.59 ]
	#  [ 0.586  0.008]]

The predictive weight :math:`\mathbf{w}_\text{p} = (0.474, 0.657, 0.586)` has three positive entries of
similar size, which restates the raw-data picture: the three inputs rise together, and each rises with
taste. The orthogonal weight :math:`\mathbf{w}_\text{o} = (0.808, -0.590, 0.008)` reads as a recipe:
raise acetic acid, lower hydrogen sulfide, leave lactic acid alone. That is the same trade-off the
:ref:`table of null-space steps <LVM-PLS-null-space-steps-table>` set out in the original units, arrived
at here without inverting anything.

The two methods are less different than they appear. The columns of ``pls.x_weights_`` *are* the two
O-PLS weights, in the same order and to the same digits, and both models return regression coefficients
agreeing to :math:`1.4 \times 10^{-13}`, so they predict a new cheese identically. What differs is the
order the directions are peeled off |X|: PLS removes the predictive component first, O-PLS the
orthogonal one, computing the predictive score on what is left. That score therefore absorbs all of the
taste information.

The consequence shows up in the scores, not the weights.

.. code-block:: python

	y_centred = (Y - Y.mean()).to_numpy().ravel()
	t_p = opls.predictive_scores_.to_numpy().ravel()
	t_o = opls.orthogonal_scores_.to_numpy().ravel()

	for name, score in [("PLS 1", scores.iloc[:, 0]), ("PLS 2", scores.iloc[:, 1]),
	                    ("O-PLS predictive", t_p), ("O-PLS orthogonal", t_o)]:
	    print(name, round(float(np.corrcoef(score, y_centred)[0, 1]), 3))
	# PLS 1 0.802
	# PLS 2 -0.172
	# O-PLS predictive 0.82
	# O-PLS orthogonal -0.0

	print(round(float(np.corrcoef(t_p, scores.iloc[:, 0])[0, 1]), 3))   # 0.978

	print(pls.r2_cumulative_.round(3).to_list())                        # [0.642, 0.672]
	print(round(float(np.corrcoef(t_p, y_centred)[0, 1]) ** 2, 3))      # 0.672

.. _LVM-PLS-score-correlation-table:

.. list-table:: How each score correlates with taste. The two predictive scores are close, correlating
	with each other at 0.978, but only O-PLS drives the second correlation to zero.
	:header-rows: 1
	:widths: 40 30

	*	- Score
		- Correlation with taste
	*	- PLS, first component
		- 0.802
	*	- PLS, second component
		- -0.172
	*	- O-PLS, predictive
		- 0.820
	*	- O-PLS, orthogonal
		- 0.000

Both models explain the same amount of taste; they differ in how many components it takes. PLS reaches
an :math:`R^2` of 0.672 with two: the first component gets to 0.642, and the second supplies the
remaining 0.030, which is why it still correlates with taste rather than sitting at zero. The O-PLS
predictive score reaches the same 0.672 on its own in one component, since :math:`0.820^2 = 0.672`.
Nothing has been created or lost, the same explained variance is packaged into one O-PLS component
instead of two.

What O-PLS ends up with is a single |X| matrix split three ways, the pieces adding back up to |X|. There
is one |X| here, not two blocks of data side by side:

.. math::

	\begin{aligned}
	\mathbf{X} &= \underbrace{\mathbf{t}_\text{p} \mathbf{p}_\text{p}^T}_{\text{predictive}}
	  \,+\, \underbrace{\mathbf{T}_\text{o} \mathbf{P}_\text{o}^T}_{Y\text{-orthogonal}}
	  \,+\, \underbrace{\mathbf{E}}_{\text{residual}} \\
	\mathbf{y} &= q_\text{p}\, \mathbf{t}_\text{p} + \mathbf{f}
	\end{aligned}

Here :math:`\mathbf{T}_\text{o}` and :math:`\mathbf{P}_\text{o}` carry one column per orthogonal
component, and :math:`\mathbf{E}` and :math:`\mathbf{f}` hold what no component explains. What the split
does not show is the order the pieces are found in. The orthogonal score comes first, from |X| itself,
then the predictive score from what is left, which is what lets it absorb all of the taste information:

.. math::

	\begin{aligned}
	\mathbf{t}_\text{o} &= \mathbf{X}\, \mathbf{w}_\text{o} \\
	\mathbf{t}_\text{p} &= \left(\mathbf{X} - \mathbf{t}_\text{o} \mathbf{p}_\text{o}^T\right)
	  \mathbf{w}_\text{p} \\
	\hat{\mathbf{y}} &= q_\text{p}\, \mathbf{t}_\text{p}
	\end{aligned}

Substituting this cheese model's coefficients, with |X| centred and scaled:

.. math::

	\begin{aligned}
	\mathbf{t}_\text{o} &= \mathbf{X}\, (0.808,\ -0.590,\ 0.008)^T \\
	\mathbf{t}_\text{p} &= \left(\mathbf{X} - \mathbf{t}_\text{o} \mathbf{p}_\text{o}^T\right)
	  (0.474,\ 0.657,\ 0.586)^T \\
	\hat{\mathbf{y}} &= 0.571\, \mathbf{t}_\text{p}
	\end{aligned}

In the scaled units the model works in, the predictive piece carries 68.7% of the sum of squares in |X|, the
orthogonal piece 18.3%, and the residual 13.0%. Those percentages describe |X| alone. The first is not
the share of the input variation that is about taste: most of it is the joint spread of three correlated
measurements, which would be there whether or not taste had been recorded. How much of taste the model
accounts for is the separate :math:`R^2` of 0.672.

The predictive loading closes the loop. In the PLS model the first weight and its loading sat 5.49
degrees apart, and that gap was the starting point. The O-PLS pair,
:math:`\mathbf{w}_\text{p} = (0.474, 0.657, 0.586)` and
:math:`\mathbf{p}_\text{p} = (0.472, 0.654, 0.591)`, sit 0.31 degrees apart: with the orthogonal
variation already out of |X|, there is almost nothing left for the loading to drift towards. That is the
interpretability O-PLS was built to deliver.

.. _LVM-PLS-opls-construction:

The zero in the table is exact rather than merely small, and it holds by algebra rather than by fitting.
The predictive weight is read straight off the response, :math:`\mathbf{w}_\text{p} = \mathbf{X}^T
\mathbf{y}` scaled to unit length, so each entry is the covariance between one input and taste (Trygg
and Wold, 2002); that direction is settled first and never revised. The subtraction that produced
:math:`\mathbf{w}_\text{o}` already makes it perpendicular to :math:`\mathbf{w}_\text{p}`, and the zero
correlation then follows in one line:

.. math::

	\mathbf{t}_\text{o}^T \mathbf{y} = \left(\mathbf{X} \mathbf{w}_\text{o}\right)^T \mathbf{y}
	  = \mathbf{w}_\text{o}^T \left(\mathbf{X}^T \mathbf{y}\right)
	  = \left\|\mathbf{X}^T \mathbf{y}\right\| \, \mathbf{w}_\text{o}^T \mathbf{w}_\text{p} = 0

Perpendicular in the space of the inputs therefore means uncorrelated with the response in the space of
the observations. The argument survives the removal step: what is taken out of |X| changes
:math:`\mathbf{X}^T\mathbf{y}` by :math:`\mathbf{p}_\text{o}(\mathbf{t}_\text{o}^T \mathbf{y})`, which
the line above makes zero, so the same reasoning applies at every further orthogonal component.

That difference between the two models is visible in the :math:`y`-loadings. PLS spread the response
across both components, :math:`\mathbf{q} = (0.546, -0.262)`, so predicting taste needed both scores.
O-PLS puts all of it on the first and none on the second, :math:`\hat{y} = 0.571\, t_\text{p}`, so the
gradient of the prediction points exactly along the predictive axis. Plotting the same cheeses in each
set of coordinates shows what that does to the geometry.

.. code-block:: python

	opls_result = opls.invert(y_desired=20.9)

	fig = make_subplots(rows=1, cols=2, subplot_titles=(
	    "PLS: response spread over both components",
	    "O-PLS: response all on one component"))
	fig.add_scatter(x=scores.iloc[:, 0], y=scores.iloc[:, 1], mode="markers", row=1, col=1)
	fig.add_scatter(x=line[:, 0], y=line[:, 1], mode="lines", row=1, col=1,
	                line={"color": "orange"})
	fig.add_scatter(x=t_p, y=t_o, mode="markers", row=1, col=2)
	fig.add_vline(x=opls_result.predictive_score, line={"color": "orange"}, row=1, col=2)
	fig.update_yaxes(scaleanchor="x", scaleratio=1)     # equal axes, so angles are true
	fig.show()

.. _LVM-PLS-opls-rotation-figure:

.. figure:: ../../figures/pls/pls-opls-rotation.png
	:alt: The same set of solutions drawn in PLS score coordinates and in O-PLS score coordinates
	:width: 700px
	:align: center

	The same 26 cheeses and the same set of designs reaching a taste of 20.9, drawn in each model's
	coordinates. Left: PLS spreads the response over both components, the gradient :math:`\mathbf{q}`
	points diagonally, and the solutions form a diagonal line, so inversion solves one equation in two
	unknowns. Right: O-PLS puts the whole response on the predictive component, so the gradient points
	along that axis and the same solutions become a line at a fixed predictive score. Only the axes have
	moved; the set of designs described is identical.

Fixing the taste in O-PLS coordinates therefore leaves one equation with one unknown, since the
orthogonal score does not appear in it, and the predictive score follows by division:

.. math::

	t_\text{p} = \frac{y_\text{des}}{q_\text{p}} = \frac{-0.17}{0.571} = -0.298

The orthogonal score is left free, to be chosen on any grounds we like. The subspace holding the
orthogonal components is called the *orthogonal space*, and by construction, moving along it changes |X|
but not the predicted |Y|. That is the same property that defines the null space of the inverted PLS
model. García-Carrión and co-authors (2025) proved that, for a single response, the two subspaces are
the same linear space: both are exactly the set of score directions the model maps to no change in the
response.

.. code-block:: python

	print(opls_result.x_new.round(2).to_list())   # [5.46, 5.62, 1.39]
	print(round(opls_result.y_hat, 2))            # 20.9

	ns_input = result.null_space_basis.to_numpy().T @ pls.x_loadings_.to_numpy().T
	os_input = opls_result.orthogonal_space_basis.to_numpy().T

	print((ns_input / np.linalg.norm(ns_input)).round(3))    # [[ 0.948 -0.238  0.211]]
	print((os_input / np.linalg.norm(os_input)).round(3))    # [[ 0.948 -0.238  0.211]]

	cosine = np.abs(ns_input @ os_input.T).item() / (
	    np.linalg.norm(ns_input) * np.linalg.norm(os_input)
	)
	print(round(cosine, 6))    # 1.0

The O-PLS design, (Acetic 5.46, H2S 5.62, Lactic 1.39), differs from the PLS direct-inversion design,
but lies on the same line and gives the same predicted taste. The two methods simply report different
representative points on it: PLS the point of smallest score norm, O-PLS the point whose orthogonal
score is zero. Written as unit vectors in the inputs both bases come out as
:math:`(0.948,\ -0.238,\ 0.211)`, with a cosine of 1.0 between them. This is what the green circles in
the :ref:`score plot <LVM-PLS-null-space-figure>` show: the orthogonal space projected into the PLS
score plot, lying on the orange null-space line.

What neither method settles is which point on that line to build. Every design on it predicts the same
taste, and the model has nothing further to say about them. Choosing between them means asking a
different question: how far each one sits from the cheeses the model was built on.

.. _LVM-PLS-inversion-in-practice:

Reading the result: how far is the design from the data?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inversion always returns a set of inputs, whatever taste we ask for, so we need a way to judge
whether those inputs are reasonable. Hotelling's :math:`T^2` answers this: it measures how far a point
sits from the centre of the calibration data, in the same units as the
:ref:`score diagnostics <LVM-Hotellings-T2>` used elsewhere. Let's take a look with all four held-out
cheeses, repeating for each of them what we did for cheese 2.

Two different :math:`T^2` values appear once we do that, and they are worth keeping apart. Each
held-out cheese was really made and really measured, so its three measurements can be projected onto
the model to give scores, and a :math:`T^2` from those scores. Call that the :math:`T^2` of the cheese:
it says how unusual that cheese is compared with the 26 cheeses the model was calibrated on. Inverting
toward the same target taste produces a different set of three inputs, the recipe the model proposes,
which has its own scores and its own :math:`T^2`. Call that the :math:`T^2` of the design: it says how
far the proposed recipe sits from the centre of the calibration data. The two are computed from
different points in the input space, so there is no reason for them to agree, and the table below shows
that they often do not.

A third quantity compares those two points with each other. It is the
:ref:`input-space deviation <LVM-PLS-input-space-deviation>` defined earlier: centre and scale the
three measurements, then sum the squared differences between the measured cheese and the proposed
recipe. Note that it is not a comparison of the two :math:`T^2` values. The two :math:`T^2` values are
distances in the score space, each measured from the centre of the calibration data; the input-space
deviation is a distance in the input space, measured between the two recipes themselves.

.. code-block:: python

	rows = []
	for i in range(len(holdout)):
	    target = float(holdout["Taste"].iloc[i])
	    design = pls.invert(target)
	    measured = holdout[x_columns].iloc[i]
	    a = scaler.transform(measured.to_frame().T).iloc[0]
	    p = scaler.transform(design.x_new.to_frame().T).iloc[0]
	    rows.append({
	        "Taste": target,
	        "T2 design": design.hotellings_t2,          # the proposed recipe
	        "T2 cheese": float(pls.diagnose(measured.to_frame().T).hotellings_t2.iloc[0]),
	        "Input dev": float(((a - p) ** 2).sum()),   # between the two recipes
	    })

	print(pd.DataFrame(rows).round(2))

.. list-table:: The four held-out cheeses. Each row compares the recipe the inversion proposes for that cheese's taste against the cheese as it was actually measured. The two :math:`T^2` columns are distances from the centre of the calibration data, one for each of those two points; the last column is the distance between the two points. The 99% limit on :math:`T^2` is 12.14.
	:header-rows: 1
	:widths: 12 14 22 22 30

	*	- Cheese
		- Taste
		- :math:`T^2` of the design
		- :math:`T^2` of the measured cheese
		- Input-space deviation
	*	- 1
		- 12.3
		- 1.07
		- 4.08
		- 4.50
	*	- 2
		- 20.9
		- 0.06
		- 0.21
		- 0.66
	*	- 3
		- 39.0
		- 1.93
		- 0.02
		- 2.65
	*	- 4
		- 47.9
		- 4.82
		- 0.94
		- 1.57

Reading down the :math:`T^2` of the design, the moderate tastes near the middle of the calibration range
give designs with small :math:`T^2`, while the more extreme tastes push the design further from the data:
asking for a
taste of 47.9 gives the largest value, 4.82. A large :math:`T^2` does not make a design wrong, but it
flags that the model is extrapolating and that the predicted taste rests on less support from the data.
All four are well inside the 99% limit of 12.14.

The input-space deviation compares each design with the cheese that actually had that taste. Cheese 2 is
the closest match, at 0.66, which is the case we worked through. Cheese 1 is the furthest, at 4.50, or
:math:`\sqrt{4.50} = 2.1` standard deviations. The :math:`T^2` of the measured cheese explains part of
that: cheese 1 has the largest :math:`T^2` of the four cheeses, 4.08, so it is an unusual cheese to begin
with, sitting well away from the centre of the calibration data while the design does not.

A large input-space deviation is not a failure of the inversion. The model returns the solution of
smallest score norm, whereas nature produced whichever inputs it produced, and the null space means both
can carry the same predicted taste while sitting some distance apart. The input-space deviation measures
how far apart the two recipes are, not how wrong either of them is.

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
different and often more useful question. Rather than "which inputs give a taste of 20.9?", we ask
"which inputs give a taste we would accept?" The set of inputs that answer it is called a
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

Suppose a taste between 20 and 30 is acceptable.

.. code-block:: python

	t2_limit = pls.hotellings_t2_limit(0.95)

	region = []
	for target in np.linspace(20.0, 30.0, 5):        # the range of taste we accept
	    for step in np.linspace(-6, 6, 2001):        # walk along that target's null space
	        candidate = pls.invert(target, null_space_coordinates=[step])
	        if candidate.hotellings_t2 <= t2_limit:
	            region.append(candidate.x_new)

	region = pd.DataFrame(region)
	print(round(t2_limit, 2))                        # 7.36
	print(region.agg(["min", "max"]).round(2))
	#      Acetic   H2S  Lactic
	# min    4.35  4.44    1.25
	# max    6.80  8.04    1.68

A cheese whose inputs fall in this region is predicted to have an acceptable taste. Note that these
minima and maxima are the box that encloses the region, not the region itself. The region is a slanted
band in the three inputs, so a lot may sit inside every one of the three ranges while still lying
outside the band. Note also that the enclosing box reaches slightly past the observed range of acetic
acid in the training cheeses (4.48 to 6.46). The :math:`T^2` limit bounds the joint distance from the
centre of the model, not each measurement separately, so a corner of the region can sit a little
outside the range of any one measurement.

Both the region and the box it is reported as can be drawn.

.. code-block:: python

	corners = np.array(np.meshgrid(*zip(region.min(), region.max()))).reshape(3, -1).T
	corner_taste = pls.predict(pd.DataFrame(corners, columns=x_columns)).to_numpy().ravel()
	print(np.sort(corner_taste).round(1))
	# [11.7 15.9 19.7 23.9 26.  30.2 34.  38.2]

	fig = go.Figure()
	fig.add_scatter3d(x=region["Acetic"], y=region["H2S"], z=region["Lactic"],
	                  mode="markers", marker={"size": 2, "color": "orange", "opacity": 0.3})
	fig.add_scatter3d(x=corners[:, 0], y=corners[:, 1], z=corners[:, 2], mode="markers+text",
	                  text=[f"{t:.0f}" for t in corner_taste], marker={"size": 5, "color": "darkred"})
	fig.update_layout(scene={"xaxis_title": "Acetic", "yaxis_title": "H2S",
	                         "zaxis_title": "Lactic"})
	fig.show()

.. _LVM-PLS-specification-region-figure:

.. figure:: ../../figures/pls/pls-specification-region.png
	:alt: The specification region in the score plot, and the same region inside the box of three ranges
	:width: 720px
	:align: center

	Left: sweeping the target taste from 20 to 30 sweeps its null space across the score plot, and the
	95% :math:`T^2` limit closes the region off along the other direction. Right: the same region in the
	three inputs, with the box of three ranges drawn around it. The region is flat, because every point
	on it is rebuilt from two scores, while the box is a solid. Each corner is labelled with the taste
	it is predicted to have.

The eight corners make the difference concrete. Every one of them satisfies all three ranges, since
each coordinate is either the reported minimum or the reported maximum, and not one of them predicts an
acceptable taste: they run from 11.7 to 38.2, against a window of 20 to 30. Three ranges are the
smallest box that contains the region, and a box that contains a flat, slanted set is mostly not that
set. This is why a multivariate specification is stated as a region rather than as a table of limits
per input: the limits are a summary of the region, and reading them as though they were the
specification accepts lots the model would reject.

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
	# {'logP': 0.5, 'Solubility': 0.0}

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
