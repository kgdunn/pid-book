.. _DOE-multi-response-optimization:

Multi-response optimization: the sweet spot and desirability
==============================================================

.. index::
	pair: multi-response optimization; experiments
	pair: sweet spot; experiments
	pair: desirability; experiments
	single: Derringer-Suich desirability

The :ref:`response surface section <DOE-RSM>` optimized a single number. That number was
profit, and choosing it settled the trade-offs in advance: energy costs, raw material costs
and product value were folded into one figure before any modelling began. Working with one
response is what makes the contour plots and the path of steepest ascent straightforward.

Sometimes that folding is not available. The costs may not be known well enough to combine
the outcomes credibly, or a response may be a specification to be met rather than a quantity
to be traded, such as a purity that a customer contract fixes at 90%. In those cases the
responses are carried separately, each with its own model, and the settings are chosen with
all of them in view at once.

This section covers two ways of doing that. The first is to find the region of factor space
where every response meets its specification, which is commonly called the *sweet spot*. The
second is to convert each response to a score between 0 and 1 and combine those scores into
a single quantity that can be optimized, which is the *desirability* approach. They answer
different questions, and the last part of this section compares them against the
fold-into-one-number approach the response surface section used.

Continuing the bioreactor example
------------------------------------------------------

The :ref:`response surface section <DOE-RSM>` finished by identifying :math:`T` = 343 K and
:math:`S` = 1.60 g/L as the place to run the next experiments. We take that as the centre of
a new central composite design, with the same half-ranges as before, 4 K in temperature and
0.2 g/L in substrate concentration, and axial points 1.41 coded units out.

This time a second response is recorded alongside profit: the purity of the product stream,
as a percentage. Purity was being traded away inside the profit calculation; measuring
it separately makes that trade explicit. The nine runs, in coded and actual units:

.. tabularcolumns:: |c|c|c||c|c||c|c|

+------------+------------+------------+-------------+------------+---------------+------------+
| Experiment | :math:`x_T`| :math:`x_S`| T (actual)  | S (actual) | Profit [$/day]| Purity [%] |
+============+============+============+=============+============+===============+============+
| 1          | |-|        | |-|        | 339.0 K     | 1.40 g/L   | 720           | 90.3       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 2          | |+|        | |-|        | 347.0 K     | 1.40 g/L   | 734           | 82.3       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 3          | |-|        | |+|        | 339.0 K     | 1.80 g/L   | 721           | 95.3       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 4          | |+|        | |+|        | 347.0 K     | 1.80 g/L   | 726           | 87.2       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 5          | 0          | 0          | 343.0 K     | 1.60 g/L   | 738           | 89.8       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 6          | 0          | -1.41      | 343.0 K     | 1.32 g/L   | 718           | 83.9       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 7          | +1.41      | 0          | 348.7 K     | 1.60 g/L   | 738           | 83.7       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 8          | 0          | +1.41      | 343.0 K     | 1.88 g/L   | 713           | 90.9       |
+------------+------------+------------+-------------+------------+---------------+------------+
| 9          | -1.41      | 0          | 337.3 K     | 1.60 g/L   | 726           | 95.4       |
+------------+------------+------------+-------------+------------+---------------+------------+

Every figure in this section is reproducible with
`process_improve <https://github.com/kgdunn/process-improve>`_
(``pip install 'process-improve[all]'``). Each block imports what it needs and reuses
variables defined in the blocks before it, so paste them in order.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	import statsmodels.formula.api as smf
	from plotly.subplots import make_subplots

	from process_improve.experiments import optimize_responses
	from process_improve.experiments.visualization.plots.registry import create_plot

	alpha = 1.41
	design = pd.DataFrame({
	    "T": [-1, +1, -1, +1, 0, 0, +alpha, 0, -alpha],
	    "S": [-1, -1, +1, +1, 0, -alpha, 0, +alpha, 0],
	    "profit": [720, 734, 721, 726, 738, 718, 738, 713, 726],
	    "purity": [90.3, 82.3, 95.3, 87.2, 89.8, 83.9, 83.7, 90.9, 95.4],
	})

	# One full quadratic per response, on the coded factors.
	formula = " ~ T + S + T:S + I(T**2) + I(S**2)"
	fit_profit = smf.ols("profit" + formula, data=design).fit()
	fit_purity = smf.ols("purity" + formula, data=design).fit()

	print(fit_profit.rsquared, fit_purity.rsquared)   # -> 0.9915  0.9988

Each response gets its own model, and there is no requirement that the two models contain the
same terms. Fitting them on the coded factors keeps the coefficients comparable within a
model, for the reasons given in the section on
:ref:`generators and coded levels <DOE-generators>`:

.. math::

	\widehat{\text{profit}} &= 738.0 + 4.50 x_T - 1.76 x_S - 2.25 x_T x_S - 2.61 x_T^2 - 10.91 x_S^2 \\
	\widehat{\text{purity}} &= 89.8 - 4.09 x_T + 2.48 x_S - 0.03 x_T x_S - 0.05 x_T^2 - 1.13 x_S^2

The signs on :math:`x_T` are opposite. Profit rises with temperature; purity falls with it,
because the product degrades thermally. That is what makes this a trade-off rather than a
matter of reading two plots and finding they agree.

.. code-block:: python

	def surface(fit, n=80):
	    """Predict a fitted response over the coded region, in actual units."""
	    grid = np.linspace(-1, 1, n)
	    x_t, x_s = np.meshgrid(grid, grid)
	    frame = pd.DataFrame({"T": x_t.ravel(), "S": x_s.ravel()})
	    z = fit.predict(frame).to_numpy().reshape(x_t.shape)
	    return 343.0 + 4.0 * grid, 1.60 + 0.2 * grid, z

	temp_axis, subs_axis, z_profit = surface(fit_profit)
	_, _, z_purity = surface(fit_purity)

	fig = make_subplots(rows=1, cols=2, subplot_titles=("Profit [$/day]", "Purity [%]"))
	for col, (z, scale) in enumerate([(z_profit, "Blues"), (z_purity, "Reds")], start=1):
	    fig.add_trace(go.Contour(x=temp_axis, y=subs_axis, z=z, colorscale=scale,
	                             contours=dict(showlabels=True), showscale=False),
	                  row=1, col=col)
	fig.update_xaxes(title_text="Temperature [K]")
	fig.update_yaxes(title_text="Substrate concentration [g/L]", row=1, col=1)
	fig.show()

.. figure:: ../figures/doe/multi-response-two-contours.png
    :align: center
    :width: 750px
    :alt: multi-response-desirability-figures.py

    The two fitted response surfaces over the same factor space, with the nine experimental
    runs marked. Profit is highest towards the middle and right of the temperature range;
    purity is highest at the left. The two surfaces disagree about where to operate.

Optimizing either response on its own makes the conflict concrete. Within the region studied,
profit is highest at :math:`T` = 346.8 K and :math:`S` = 1.56 g/L, reaching $740 per day. At
that setting the fitted purity is 85.4%. Purity is highest at :math:`T` = 339.0 K and
:math:`S` = 1.80 g/L, reaching 95.2%, where the fitted profit is $720 per day.

So each response, optimized alone, lands on a setting the other one would reject. Neither
single-response answer is usable.

.. _DOE-sweet-spot:

The sweet spot
------------------------------------------------------

Suppose the requirements are that profit must be at least $725 per day for the unit to be
worth running, and purity must be at least 90% to meet the customer specification. Each
requirement divides the factor space in two: the settings that meet it, and those that do
not. The region where every requirement is met at once is the :index:`sweet spot`.

Drawing it is a matter of putting both boundaries on the same axes and shading the
intersection.

.. code-block:: python

	# Coefficients in the form the optimizer and the plots expect.
	def coefficients(fit):
	    return [{"term": t, "coefficient": float(v)} for t, v in fit.params.items()]

	overlay = create_plot(
	    "overlay",
	    analysis_results={"optimization": {"responses": [
	        {"name": "profit", "coefficients": coefficients(fit_profit), "low": 725, "high": 1e4},
	        {"name": "purity", "coefficients": coefficients(fit_purity), "low": 90, "high": 100},
	    ]}},
	    factors_to_plot=["T", "S"],
	)
	spec = overlay.to_spec()
	print(spec.metadata["sweet_spot_fraction"])   # -> 0.391
	print(spec.metadata["sweet_spot_empty"])      # -> False

	overlay.to_plotly()

.. figure:: ../figures/doe/multi-response-sweet-spot.png
    :align: center
    :width: 700px
    :alt: multi-response-desirability-figures.py

    The sweet spot. The two heavy lines are the specification limits, one per response, and
    the shaded region is where both are satisfied. The star marks the setting of highest
    overall desirability, defined in the next subsection.

About 39% of the region studied satisfies both requirements. That is the useful output here:
not a single point, but a set of settings among which the operator can choose on other
grounds, such as which is easiest to hold steady, which is furthest from a safety limit, or
which the unit happens to be running at already.

Two properties of the sweet spot are worth stating plainly. It does not rank the settings
inside it: every point in the shaded region meets both specifications, and the plot says
nothing about which is preferable. And it can be empty. Tightening the requirements to a
profit of at least $735 per day and a purity of at least 94% leaves no region at all:

.. code-block:: python

	strict = create_plot(
	    "overlay",
	    analysis_results={"optimization": {"responses": [
	        {"name": "profit", "coefficients": coefficients(fit_profit), "low": 735, "high": 1e4},
	        {"name": "purity", "coefficients": coefficients(fit_purity), "low": 94, "high": 100},
	    ]}},
	    factors_to_plot=["T", "S"],
	)
	print(strict.to_spec().metadata["sweet_spot_empty"])   # -> True

An empty sweet spot is an answer, not a failure of the method. It says that within the region
studied the requirements cannot be met together, and the next step is a decision rather than
a calculation: relax one of the requirements, or widen the factor ranges and run more
experiments, or change something about the process that the current factors do not describe.

.. _DOE-desirability:

Desirability
------------------------------------------------------

The sweet spot treats each requirement as pass or fail. Desirability instead grades how well
a response does, on a scale from 0 to 1, and then combines the grades. The approach is due to
:index:`Derringer <single: Derringer, George>` and :index:`Suich <single: Suich, Ronald>`.

For a response to be maximized, pick the value below which the result is of no use, and the
value at or above which nothing further is gained. Call them :math:`L` and :math:`U`. The
*individual desirability* :math:`d` is then 0 below :math:`L`, 1 above :math:`U`, and ramps
between them:

.. math::

	d = \begin{cases}
	0 & y \leq L \\
	\left(\dfrac{y - L}{U - L}\right)^{w} & L < y < U \\
	1 & y \geq U
	\end{cases}

The exponent :math:`w` is the :index:`weight <pair: weight; desirability>`. At :math:`w = 1`
the ramp is a straight line. Above 1 the ramp is pushed towards the top end, so only values
close to :math:`U` score well. Below 1 it is pulled towards the bottom, so anything inside
the range scores nearly as well as the best. A response to be minimized uses the same
expression with the ends exchanged. A response with a target value uses two ramps back to
back, rising from :math:`L` to the target and falling from the target to :math:`U`, and can
carry a different weight on each side.

.. figure:: ../figures/doe/multi-response-desirability-functions.png
    :align: center
    :width: 750px
    :alt: multi-response-desirability-figures.py

    Individual desirability for purity. Left: a maximize goal, scoring 0 at or below 90% and
    1 at or above 96%. Middle: a target goal at 93%. Right: the effect of the weight on a
    maximize goal, at :math:`w` = 0.3, 1 and 3.

For this example the ramps run from each specification limit to the best value the region can
deliver: profit from $725 to $740 per day, purity from 90% to 96%. Setting :math:`L` at the
specification limit means a setting that misses the specification scores zero, which ties the
desirability to the sweet-spot boundary already drawn.

The individual desirabilities are combined into an *overall desirability* :math:`D`, the
geometric mean of the individual values:

.. math::

	D = \left( d_1^{\,r_1} \times d_2^{\,r_2} \times \cdots \times d_k^{\,r_k} \right)^{1 / \sum r_i}

The exponents :math:`r_i` are the :index:`importances <pair: importance; desirability>`, and
they set how much each response counts relative to the others. The weight :math:`w` and the
importance :math:`r` are easy to confuse, so it is worth separating them: the weight shapes
one response's own ramp, and the importance sets how heavily that response's grade counts
when the grades are combined.

The geometric mean has a consequence that is the whole reason for using it rather than an
average. If any single :math:`d_i` is zero, :math:`D` is zero, whatever the others are. A
setting that misses one specification outright cannot be compensated for by doing well
elsewhere. An arithmetic mean would allow exactly that compensation.

.. code-block:: python

	models = [
	    {"response_name": "profit", "coefficients": coefficients(fit_profit),
	     "factor_names": ["T", "S"]},
	    {"response_name": "purity", "coefficients": coefficients(fit_purity),
	     "factor_names": ["T", "S"]},
	]
	goals = [
	    {"response": "profit", "goal": "maximize", "low": 725, "high": 740},
	    {"response": "purity", "goal": "maximize", "low": 90, "high": 96},
	]
	ranges = {"T": {"low": 339.0, "high": 347.0}, "S": {"low": 1.40, "high": 1.80}}

	best = optimize_responses(
	    models, goals=goals, method="desirability", factor_ranges=ranges,
	    fitted_results=[fit_profit, fit_purity],
	)["desirability"]

	print(best["optimal_actual"])            # -> T 339.8 K, S 1.64 g/L
	print(best["predicted_responses"])       # -> profit 732.2, purity 93.5
	print(best["individual_desirability"])   # -> profit 0.48, purity 0.59
	print(best["composite_desirability"])    # -> 0.531

The overall desirability is highest at :math:`T` = 339.8 K and :math:`S` = 1.64 g/L, where
the fitted profit is $732 per day and the fitted purity is 93.5%. Neither response is at its
own best there. Profit could reach $740 and purity could reach 95.2%, but not at the same
setting, and this is the compromise the chosen ramps and importances imply.

One detail about the region being searched. The search runs over the coded cube, from
:math:`-1` to :math:`+1` on each factor, which is the region the four corner runs span. The
axial runs of this central composite design sit further out, at 1.41 coded units, so the
experiment covers a little more ground than the cube. Passing
``search_bounds=(-1.41, 1.41)`` searches that wider region instead. Here it makes no
difference, because the optimum is already inside the cube, but it would matter for a
surface still rising at the cube face.

.. figure:: ../figures/doe/multi-response-composite-desirability.png
    :align: center
    :width: 700px
    :alt: multi-response-desirability-figures.py

    Overall desirability across the region. The flat pale area is where at least one response
    misses its specification, so :math:`D` = 0. The star marks the maximum. Compare the
    boundary of the coloured area with the sweet spot drawn earlier: they are the same
    boundary, because each ramp was started at its specification limit.

Because the ramps and importances are choices, it is worth seeing how much the answer depends
on them. Counting profit three times as heavily as purity, and then the reverse:

.. code-block:: python

	for importance in ([3, 1], [1, 3]):
	    out = optimize_responses(
	        models, goals=goals, method="desirability", factor_ranges=ranges,
	        response_importance=importance,
	    )["desirability"]
	    print(importance, out["optimal_actual"], out["predicted_responses"])

	# [3, 1] -> T 341.1 K, S 1.63 g/L: profit 735, purity 92.0
	# [1, 3] -> T 339.0 K, S 1.66 g/L: profit 730, purity 94.5

Both answers stay inside the sweet spot, and both move in the direction the importance would
suggest: favouring profit raises the temperature and gives up purity, and favouring purity
does the reverse. The spread between the two, about 2 K in temperature, is a measure of how
much the choice of importances matters here. Note that the value of :math:`D` cannot be
compared across different importance settings, since the exponents that define it have
changed.

.. _DOE-uncertainty-at-the-optimum:

How well is the optimum known?
------------------------------------------------------

The settings above come from fitted models, and the fitted values at those settings carry the
same uncertainty as any other prediction from a least squares model. The
:ref:`prediction interval <LS-prediction-interval>` at the optimum is the relevant
quantity, since it covers a future single run rather than the long-run mean.

.. code-block:: python

	for name, interval in best["response_intervals"].items():
	    print(name, round(interval["predicted"], 1),
	          [round(v, 1) for v in interval["confidence_interval"]],
	          [round(v, 1) for v in interval["prediction_interval"]])

	# profit 732.2  CI [729.0, 735.5]  PI [726.9, 737.6]
	# purity  93.5  CI [ 92.9,  94.2]  PI [ 92.4,  94.6]

Both prediction intervals stay on the acceptable side of their specifications, so the optimum
is not merely predicted to pass but is expected to pass on a single future run. The profit
interval is the tighter case: its lower bound of $727 per day sits only about $2 above the
$725 specification. A setting whose interval straddled a specification limit would be
predicted to meet it while being quite capable of missing it in practice, which is a
different situation from the point estimate alone.

As with any response surface result, the optimum is a prediction and the
:ref:`next step is to run it <DOE-general-approach>`. A confirmation run at the chosen
settings, compared against these intervals, is what turns the prediction into a result.

Comparing the three approaches
------------------------------------------------------

Three ways of handling several responses have now appeared in this chapter.

.. tabularcolumns:: |p{0.22\textwidth}|p{0.36\textwidth}|p{0.36\textwidth}|

+------------------------+---------------------------------------+---------------------------------------+
| Approach               | What it needs                         | What it gives back                    |
+========================+=======================================+=======================================+
| Combine into one       | The relative value of each outcome,   | A single response, so the ordinary    |
| response, such as      | in common units, known before the     | tools apply unchanged: contours,      |
| profit                 | analysis                              | steepest ascent, a single optimum     |
+------------------------+---------------------------------------+---------------------------------------+
| Sweet spot             | A specification limit for each        | A region of acceptable settings, with |
|                        | response                              | no ranking inside it; can be empty    |
+------------------------+---------------------------------------+---------------------------------------+
| Desirability           | A ramp for each response, and an      | A single setting, and a surface that  |
|                        | importance for each                   | ranks every point in the region       |
+------------------------+---------------------------------------+---------------------------------------+

The three differ in where the judgement is placed rather than in how much of it is required.
Combining into one response puts the judgement in the cost model, before any data are seen.
The sweet spot puts it in the specification limits, and then stops, leaving the final choice
within the region to the operator. Desirability puts it in the ramps and importances, and
carries it through to a single recommended setting.

Which fits depends on what is available and on what is wanted. When the costs are genuinely
known, combining into one response uses that knowledge and keeps the analysis simple. When
the requirements are contractual limits rather than values to be traded, the sweet spot
matches the question being asked. When a single recommendation is needed and the relative
priorities can be stated, desirability provides one, at the cost of making those priorities
explicit and, as shown above, of an answer that moves when they change.

Nothing prevents using more than one. Drawing the sweet spot before running the optimizer
costs one plot and shows whether a compromise exists at all, which is worth knowing before
interpreting any single recommended setting.

.. rubric:: References and readings

* George Derringer and Ronald Suich, "`Simultaneous Optimization of Several Response Variables
  <https://doi.org/10.1080/00224065.1980.11980968>`_", *Journal of Quality Technology*, **12**,
  214-219, 1980. The paper that introduced the desirability functions used here.

* George Derringer, "A Balancing Act: Optimizing a Product's Properties", *Quality Progress*,
  **27**, 51-58, 1994. A later, less formal account by the same author, with guidance on
  choosing the weights and importances.

* Raymond Myers, Douglas Montgomery and Christine Anderson-Cook, *Response Surface
  Methodology*, the chapter on multiple response optimization, which covers both the overlaid
  contour and desirability approaches, and the constrained-optimization alternative.

.. rubric:: Summary

#.	Several responses can be handled by folding them into one number, by finding the region
	where all of them meet specification, or by grading each one and optimizing the combined
	grade. Each moves the judgement to a different place; none removes it.

#.	The sweet spot is the set of settings meeting every specification at once. It ranks
	nothing inside it, and it can be empty, which is a useful finding rather than a failure.

#.	Individual desirability grades one response from 0 to 1 between a pair of limits, with a
	weight controlling the shape of the ramp. Overall desirability is the geometric mean of
	the individual grades, weighted by importances, so that a single failed specification
	drives the overall value to zero.

#.	The weight shapes one response's own ramp; the importance sets how heavily that response
	counts against the others. They are different parameters.

#.	The recommended setting is a prediction. Report the prediction interval for each response
	at that setting, and confirm it with a run before treating it as established.
