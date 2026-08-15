.. _DOE-omars-designs:

OMARS designs: orthogonal minimally aliased response surface designs
=====================================================================

A :ref:`definitive screening design <DOE-definitive-screening-designs>` is excellent, but it is
also rather rigid: for a given number of
factors it is essentially one design, of one size, with one fixed compromise on how it handles
interactions. What if you can afford a few more runs and would like to estimate the
interactions better, or you want a design that sits deliberately between the bare economy of a
DSD and the full richness of a central composite design?

That spectrum is exactly what :index:`OMARS designs <pair: OMARS design; experiments>`
(Orthogonal Minimally Aliased Response Surface designs, Núñez Ares and Goos, 2020) provide. The
defining property generalises the property that makes the DSD work: in an OMARS design the main effects are
orthogonal to one another *and* to every second-order effect, both quadratics and two-factor
interactions. The name records exactly that: **o**\ rthogonal (main effects clean of each other),
**m**\ inimally **a**\ liased (main effects clean of the second-order effects), **r**\ esponse
**s**\ urface (a full second-order model is the target).

*Minimally aliased* is a statement of zero rather than of a small number. Two alias matrices carry
bias into the main-effect estimates, one from the two-factor interactions and one from the
quadratics, and both are zero by construction for every design in the catalogue. This is the same
property described from the other side in :ref:`Judging and comparing designs
<DOE-judging-and-comparing-designs>`, where the main-effect rows of the alias matrix are exactly
zero.

Aliasing does remain *among the second-order effects*. It is measured for each design in the
catalogue rather than minimised, and it varies widely from one design to the next, which is why
choosing the size is a separate question from choosing within that size.

The important shift in thinking is this: OMARS is not a single design but a whole *catalogue*.
Núñez Ares and Goos enumerated it in 2020 for three to seven factors, using integer programming to
find 7,933 basic designs, which become 55,531 once zero to six centre runs are added to each.

For a given number of factors the catalogue holds many designs of different run sizes, and they
trade off against one another: a larger design estimates more of the second-order effects, with
lower correlation among them and more power, at the cost of more runs. The
:ref:`definitive screening design <DOE-definitive-screening-designs>` is the smallest member of the
family; at the other extreme the face-centred central composite and Box-Behnken designs are
themselves OMARS designs, so the largest members coincide with the standard response surface
designs. There are many criteria that can be used to select between them. It is not a simple
lookup, and that is the topic of the :ref:`spectrum below <DOE-design-spectrum>` and of
:ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>`.

Most of the catalogue is foldover designs, built as the DSD was by folding a base matrix over its
own sign-flipped copy. The clean main effects do not depend on that construction: all odd design
moments through order three are set to zero, so the non-foldover members have equally clean main
effects. The family has since been extended to mixed-level designs, three-level quantitative
factors together with two-level categorical ones, and to orthogonally blocked designs.

**Readings**

* Núñez Ares, J. and Goos, P.: "Enumeration and Multicriteria Selection of Orthogonal Minimally
  Aliased Response Surface Designs", *Technometrics*, **62**, 21--36, 2020.
  `doi:10.1080/00401706.2018.1549103 <https://doi.org/10.1080/00401706.2018.1549103>`__
* Goos, P.: "OMARS designs for factor screening and response surface experimentation in one
  step: A review", *WIREs Computational Statistics*, **17**, e70018, 2025.
  `doi:10.1002/wics.70018 <https://doi.org/10.1002/wics.70018>`__

.. _DOE-design-spectrum:

A spectrum from screening to response surface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It helps to see the three families on one line rather than as separate boxes. At the economical
end sits the definitive screening design: the fewest runs, every main effect clean, curvature
detectable, but the interactions tangled together. In the middle sit the larger OMARS designs:
more runs give more estimable second-order effects, lower correlation among them, and more power.
At the rich end sit the classical response surface designs, the :ref:`central composite
<DOE_central_composite_designs>` and :ref:`Box-Behnken <DOE-box-behnken-designs>` designs: enough
runs to estimate the full
second-order model with little or no aliasing, often with the near-rotatable prediction
behaviour those designs are prized for. In the face-centred case these classical designs are
themselves OMARS designs, the strongest and largest members of the family, so the spectrum is
really one continuous family rather than three separate boxes.

The axis along which they are arranged is the trade-off between three things: how many runs you
spend, how much of the second-order model you can estimate, and how cleanly (how free of
aliasing) you can estimate it. Spending more runs moves you to the right, gaining estimability and
separability.

.. figure:: ../figures/doe/design-spectrum.png
    :align: center
    :width: 750px
    :alt: design-spectrum.py

    The three design families on a single axis. Moving from left to right spends more runs and
    reduces the aliasing among the second-order effects.

That immediately suggests how to choose:

    *   **Many factors, a tight budget, and a reasonable belief that only a few will matter**:
        a definitive screening design. Screen and glimpse curvature in one economical step.

    *   **A handful of factors, and a wish to estimate some interactions and curvature without
        committing to a full response surface design**: a mid-sized OMARS design.

    *   **Few factors and a genuine response-surface goal, predicting and optimizing over the
        region**: a central composite or Box-Behnken design, or one of the largest OMARS designs.

Saying which specific design is best, even once the run budget is fixed, requires quantitative
tools: the information matrix, the prediction variance and its fraction-of-design-space plot, the
correlations among the effects, and the power. Those are
exactly the measures developed in :ref:`Judging and comparing designs
<DOE-judging-and-comparing-designs>`, and they turn the choice along this spectrum from a matter
of taste into a matter of arithmetic.

This whole spectrum takes the second-order polynomial as the model to be estimated, which is worth
stating. It is the lowest-order polynomial that can place a stationary point inside the region, a
maximum, minimum, or saddle, so it is the simplest model able to describe an optimum; it stays
linear in its coefficients, and it needs only three levels per factor. Higher-degree polynomials
need more levels and tend to oscillate near the edges of the region, so when a quadratic does not
fit it is more common to change the model class than to raise the degree. The aliasing and the
efficiency measures are properties of the design and can be calculated before even acquiring a
single experimental result.

.. _DOE-omars-trade-off-table:

A trade-off table for OMARS designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`two-level trade-off table <DOE_design_trade_off_BHH_272>` answers "I have sixteen runs
available and seven factors on the list, what do I give up?". Its currency is :ref:`resolution
<DOE-design-resolution>`, the ability to tell main effects apart from interactions, and the table
maps a budget onto the ordered scale of resolution III, IV and V.

It is natural to want the same table for OMARS designs, but it is not possible. Working towards it,
however, leads to a surprising answer. An OMARS design has its main effects orthogonal to each
other *and* to every second-order term at every size in the family, which is what the "orthogonal"
in the name records, so resolution is constant and cannot be what the table reports.

What varies instead is the model. The run count decides how much of the second-order model can be
fitted at all, and it is not the count the parameters suggest.

.. _DOE-omars-estimability-frontier:

How many runs a second-order model needs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The full second-order model in :math:`k` factors has an intercept, :math:`k` main effects,
:math:`k` pure quadratics and :math:`k(k-1)/2` two-factor interactions:

.. math::

	p = 1 + 2k + \frac{k(k-1)}{2}

Count the parameters and spend at least that many runs. That rule sizes factorial, central
composite, Box-Behnken and optimal designs correctly. Foldover designs are the exception.

A foldover stacks a half-design :math:`\mathbf{H}` of :math:`h` runs on its own sign-flipped copy,
then adds a centre run:

.. math::

	\mathbf{D} = \begin{bmatrix} \mathbf{H} \\ -\mathbf{H} \\ \mathbf{0} \end{bmatrix},
	\qquad N = 2h + 1

so :math:`N` is always odd. A row of :math:`\mathbf{H}` and its sign-flipped copy are a
:index:`mirror-image pair <pair: mirror-image pair; experiments>`. This is the construction behind
most of the OMARS catalogue, and behind the :ref:`definitive screening design
<DOE-definitive-screening-designs>`, where :math:`\mathbf{H}` is a conference matrix.

Flipping the sign of *every* factor at once multiplies a term of total degree :math:`d` by
:math:`(-1)^d`, so terms of odd degree change sign and terms of even degree do not. The :math:`k`
main effects are the **odd** terms; the intercept, the quadratics :math:`x_i^2` and the
interactions :math:`x_i x_j` are the **even** ones. Odd and even describe the *term*, not the
factor. This is the same split as the *odd design moments* named in the :ref:`introduction to OMARS
designs <DOE-omars-designs>`, and it explains the "through order three" qualifier used there.

A run and its mirror image differ only in sign, so they take *identical* values in every even term.
Five runs in two factors show it:

.. code-block:: text

	 run     x1  x2 |   1   x1²  x2²  x1x2     <- the even columns
	  H  1   +1  +1 |   1    1    1    +1
	  H  2   +1  -1 |   1    1    1    -1
	 -H  3   -1  -1 |   1    1    1    +1      identical to run 1
	 -H  4   -1  +1 |   1    1    1    -1      identical to run 2
	  0  5    0   0 |   1    0    0     0

Runs 3 and 4 are the mirror images of runs 1 and 2. In the odd columns they change sign, which is
what lets the design estimate main effects. In the even columns they repeat their partners exactly,
so the even terms see only :math:`h + 1` distinct rows, however many runs the foldover contains.
Here that is three distinct rows against four even columns, and :math:`x_1^2` and :math:`x_2^2` are
the same column. Only more distinct rows in :math:`\mathbf{H}` will separate them.

The even terms therefore contribute at most :math:`\min\left(h + 1,\, 1 + k(k+1)/2\right)`
distinct pieces of information and the odd terms at most :math:`k`. The *rank* of the model matrix
counts the terms the data can tell apart, so for every foldover design

.. math::
	:label: eq-omars-rank-bound

	\text{rank}(\mathbf{X}) \le k + \min\left(h + 1, \; 1 + \frac{k(k+1)}{2}\right)

Reaching this bound requires the :math:`h + 1` even rows to be distinct and linearly independent,
and :math:`\mathbf{H}` to have full column rank. A two-level design fails the first condition,
since every run there has :math:`x_i^2 = 1`. Designs in the OMARS catalogue reach the bound.

Equation :eq:`eq-omars-rank-bound` puts the full second-order model out of reach until
:math:`h + 1 \ge 1 + k(k+1)/2`, that is :math:`h \ge k(k+1)/2`, and therefore until

.. math::
	:label: eq-omars-frontier

	N \; \ge \; k^2 + k + 1

There is no established name for this threshold, so we will call it the **estimability frontier**,
the smallest foldover in which all :math:`p` coefficients of the full second-order model can be
estimated jointly.

.. list-table:: The estimability frontier, against the parameter count it has to clear.
	:header-rows: 1
	:widths: 26 18 18 20 18

	*   - Factors, :math:`k`
	    - Parameters, :math:`p`
	    - Frontier, :math:`k^2+k+1`
	    - Shortfall, :math:`k(k-1)/2`
	    - Error df at the frontier
	*   - 3
	    - 10
	    - 13
	    - 3
	    - 3
	*   - 4
	    - 15
	    - 21
	    - 6
	    - 6
	*   - 5
	    - 21
	    - 31
	    - 10
	    - 10
	*   - 6
	    - 28
	    - 43
	    - 15
	    - 15
	*   - 7
	    - 36
	    - 57
	    - 21
	    - 21

The last two columns hold the same number. Subtracting the parameter count from the frontier gives

.. math::

	\left(k^2 + k + 1\right) - \left(1 + 2k + \frac{k(k-1)}{2}\right) = \frac{k(k-1)}{2}

exactly the number of two-factor interactions. Two things follow. For a foldover, having more runs
than the model has parameters does not establish that the model can be fitted: at four factors a
nineteen-run foldover has four spare runs against a fifteen-parameter model and still cannot
estimate it. And at the frontier the error degrees of freedom also come to :math:`k(k-1)/2`, so the
smallest design that can fit the full second-order model arrives with enough spare runs to test it.

Build the four-factor design at nineteen runs and again at twenty-one, form the full second-order
model matrix, and take its rank:

.. code-block:: python

	import itertools
	import numpy as np
	from process_improve.experiments import Factor, generate_omars

	def second_order_matrix(levels):
	    """Model matrix of the full second-order model: intercept, main effects,
	    pure quadratics, then every two-factor interaction."""
	    n_runs, k = levels.shape
	    columns = [np.ones(n_runs)]
	    columns += [levels[:, i] for i in range(k)]
	    columns += [levels[:, i] ** 2 for i in range(k)]
	    columns += [levels[:, i] * levels[:, j] for i, j in itertools.combinations(range(k), 2)]
	    return np.column_stack(columns)

	factors = [Factor(name=c, low=-1, high=1) for c in "ABCD"]
	for n_runs in (19, 21):
	    design = generate_omars(factors, n_runs=n_runs, model="main_quadratic", random_seed=42)
	    X = second_order_matrix(design.design[design.factor_names].to_numpy(float))
	    print(n_runs, X.shape, np.linalg.matrix_rank(X))

	# 19 (19, 15) 14
	# 21 (21, 15) 15

Nineteen runs give a model matrix with fifteen columns and rank fourteen, one short, so the model
cannot be fitted. Twenty-one runs, the frontier for four factors, give rank fifteen. Judge
estimability from the rank of the model matrix, not from the determinant of the information matrix.

.. code-block:: python

	import plotly.graph_objects as go

	k = np.arange(3, 8)
	series = [
	    ("Estimability frontier, k² + k + 1", k**2 + k + 1, "#D55E00"),
	    ("Parameters in the full second-order model", 1 + 2 * k + k * (k - 1) // 2, "#0072B2"),
	    ("Definitive screening design, 2k + 1 runs", 2 * k + 1, "#E69F00"),
	]
	fig = go.Figure()
	for name, values, colour in series:
	    fig.add_trace(go.Scatter(x=k, y=values, name=name, mode="lines+markers",
	                             line=dict(color=colour, width=3), marker=dict(size=10)))
	# Shade the band between the parameter count and the frontier: k(k-1)/2 runs deep.
	fig.add_trace(go.Scatter(x=np.r_[k, k[::-1]],
	                         y=np.r_[k**2 + k + 1, (1 + 2 * k + k * (k - 1) // 2)[::-1]],
	                         fill="toself", fillcolor="rgba(213, 94, 0, 0.13)",
	                         line=dict(width=0), showlegend=False, hoverinfo="skip"))
	fig.add_trace(go.Scatter(x=[4], y=[19], mode="markers", showlegend=False,
	                         marker=dict(symbol="x", size=14, color="#666666"),
	                         text=["19 runs, 15 parameters, model matrix rank 14"]))
	fig.update_layout(xaxis_title="Number of factors, k", yaxis_title="Number of runs, N",
	                  xaxis=dict(tickvals=k), legend=dict(x=0.02, y=0.98))
	fig.show()

.. figure:: ../figures/doe/omars-estimability-frontier.png
	:align: center
	:width: 700px
	:alt: omars-estimability-frontier.py

	The estimability frontier :math:`N = k^2 + k + 1` for a foldover design, against the
	parameter count of the full second-order model and the size of a definitive screening
	design. In the shaded band a design has more runs than the model has parameters and still
	cannot estimate it. The band is :math:`k(k-1)/2` runs deep, and the marked point is the
	four-factor case checked in the code.

.. _DOE-omars-reading-the-table:

Reading the table
^^^^^^^^^^^^^^^^^^^^^

Three capability classes follow from the frontier, tagged with four characters so they line up in a
table:

``Full``
	:math:`N \ge k^2 + k + 1`, the estimability frontier. Main effects, pure quadratics and
	every two-factor interaction are estimable jointly, so a response surface can be fitted
	from this one design.

``Quad``
	:math:`N \ge 2k + 3`. Main effects and pure quadratics are estimable, with degrees of freedom
	left over to test them. The two-factor interactions are in the *design*, still orthogonal to
	the main effects, but not in the fitted *model*.

``Satd``
	:math:`N = 2k + 1`. Saturated: the main-effects-plus-quadratics model can be estimated, but
	nothing is left with which to estimate :math:`\sigma^2`, so there are point estimates and no
	standard errors, tests or power.

Nothing falls between ``Satd`` at :math:`2k + 1` runs and ``Quad`` at :math:`2k + 3`. The run count
between them is even, and a foldover has :math:`N = 2h + 1` runs, so no design of that size exists.

``Quad`` does not mean the interactions have to stay out of the model, only that they cannot all
come in. Adding one to the model spends one of the distinct even rows, of which a foldover has
:math:`h + 1` against the :math:`1 + k` the intercept and quadratics already use, so

.. math::
	:label: eq-omars-spare-interactions

	\text{interactions that can be added} \; = \; h - k \; = \; \frac{N-1}{2} - k

A seventeen-run design in four factors can therefore carry four of its six interactions, and a
thirteen-run one only two. Which of them to bring in is the question the staged analysis of
:ref:`Analysing data from these designs <DOE-analysing-economical-designs>` answers, and the ones
left out still bias those that come in. Setting :math:`h - k \ge k(k-1)/2` recovers
:math:`N \ge k^2 + k + 1`, so ``Full`` is exactly the point where every interaction fits at once.

The tags sort alphabetically in decreasing order of capability. The table and the single-cell
report come from ``process_improve``:

.. code-block:: python

	from process_improve.experiments import (
	    get_omars_trade_off_table_entry,
	    omars_trade_off_table,
	)

	omars_trade_off_table(anchors=True)              # the whole table
	get_omars_trade_off_table_entry(17, 4)           # one cell, reported in words

.. code-block:: text

	runs  k=3              k=4              k=5              k=6              k=7
	-------------------------------------------------------------------------------------------
	9     Quad df=2 | DSD  Satd df=0 | DSD
	13    Full 3           Quad 4           Quad df=2 | DSD  Satd df=0 | DSD
	15    Full 5 | BBD     Quad 6           Quad 4           Quad 2           Satd df=0
	17                     Quad 8           Quad 6           Quad 4           Quad 2 | DSD
	21                     Full 6           Quad 10          Quad 8           Quad 6
	25                     Full 10          Quad 14          Quad 12          Quad 10
	27                     Full 12 | BBD    Quad 16          Quad 14          Quad 12
	31                                      Full 10          Quad 18          Quad 16
	37                                      Full 16          Quad 24          Quad 22
	43                                      Full 22          Full 15          Quad 28
	46                                      Full 25 | BBD
	54                                                       Full 26 | BBD
	57                                                                        Full 21
	62                                                                        Full 26 | BBD

Each cell carries the capability class and the error degrees of freedom: the spare runs left after
fitting, from which the run-to-run noise :math:`\sigma^2` is estimated, and on which every test and
confidence interval rests. Six points to read off the table:

	*	**A column runs from its ``DSD`` mark to its ``BBD`` mark**, which is the whole span
		of the family for that factor count: the definitive screening design is the smallest
		member and the Box-Behnken design is the standard response surface design that closes
		it. Below the ``BBD`` cell a column is blank, because every further row would say
		``Full`` again on more runs.

	*	**Down a column capability only improves, and across a row it only worsens**, so the
		boundary between the classes is a staircase.

	*	**The step up to** ``Full`` **in each column is the estimability frontier**: 13, 21,
		31, 43 and 57 runs for three to seven factors.

	*	**A blank above the** ``BBD`` **mark is not a design at all**, rather than a poor
		one. A foldover has :math:`N = 2h + 1` runs, so an even budget cannot be one, and a
		budget below :math:`2k + 1` cannot hold the main effects and the quadratics. A blank
		below the ``BBD`` mark is the closed column instead.

	*	**Error degrees of freedom are not comparable across the classes**, because the model
		differs. At 43 runs, six factors show ``Full df=15`` and seven factors show
		``Quad df=28``: the seven-factor cell has more spare runs because it fits the smaller
		model.

	*	**The two marks show what the standard designs cost.** For an even number of factors
		a DSD has :math:`2k+1` runs and lands in ``Satd``. For an odd number the
		conference-matrix construction needs :math:`2k+3` runs, so the three-, five- and
		seven-factor DSDs arrive with two spare degrees of freedom and land in ``Quad df=2``.
		Every Box-Behnken design is past the frontier and so ``Full``, but none is the
		smallest design that is: at five factors it takes 46 runs where 31 reach ``Full``.

.. code-block:: python

	import plotly.graph_objects as go
	from process_improve.experiments import (
	    box_behnken_runs, definitive_screening_runs, get_omars_trade_off_table_entry, omars_anchor_entry,
	)
	from process_improve.experiments.omars_trade_off import DEFAULT_FACTORS, DEFAULT_RUNS

	shade = {"none": 0, "satd": 1, "quad": 2, "full": 3, "bbd": 4}
	dsd_runs = {k: definitive_screening_runs(k) for k in DEFAULT_FACTORS}
	bbd_runs = {k: box_behnken_runs(k) for k in DEFAULT_FACTORS}

	# A Box-Behnken run count is not one of the budgets, so the table carries a row for it.
	runs = sorted(set(DEFAULT_RUNS) | set(bbd_runs.values()))

	def cell(n_runs, k):
	    """The (shade, label) of one cell, or the blank a closed column leaves behind."""
	    if n_runs > bbd_runs[k]:
	        return shade["none"], ""
	    if n_runs == bbd_runs[k]:
	        # Not the budget path: a Box-Behnken design carries six centre runs from five
	        # factors upwards, so its run count is even and no foldover budget matches it.
	        entry, mark = omars_anchor_entry("bbd", k), "<br>BBD"
	    else:
	        entry = get_omars_trade_off_table_entry(n_runs, k, display=False)
	        mark = "<br>DSD" if n_runs == dsd_runs[k] else ""
	    if not entry.exists:
	        return shade["none"], ""
	    key = "bbd" if mark == "<br>BBD" else entry.capability
	    return shade[key], f"{entry.tag}<br>df = {entry.error_df}{mark}"

	grid = [[cell(n, k) for k in DEFAULT_FACTORS] for n in runs]

	fig = go.Figure(go.Heatmap(
	    z=[[z for z, _ in row] for row in grid], text=[[t for _, t in row] for row in grid],
	    x=[f"k = {k}" for k in DEFAULT_FACTORS], y=[str(n) for n in runs],
	    texttemplate="%{text}", showscale=False, xgap=3, ygap=3,
	    colorscale=[[0.0, "#F4F4F4"], [0.25, "#E69F00"], [0.5, "#56B4E9"],
	                [0.75, "#0072B2"], [1.0, "#009E73"]]))
	fig.update_layout(xaxis_title="Number of factors", yaxis_title="Number of runs",
	                  xaxis=dict(side="top"), yaxis=dict(autorange="reversed", type="category"))
	fig.show()

.. figure:: ../figures/doe/omars-capability-staircase.png
	:align: center
	:width: 640px
	:alt: omars-capability-staircase.py

	The OMARS trade-off table, drawn as a capability staircase. Each cell gives the largest
	model the run budget makes estimable and the error degrees of freedom left to test it.
	The outlined cells are the estimability frontier :math:`N = k^2 + k + 1`, the first
	``Full`` cell in each column. Two standard designs are marked on the row of their own
	run count: ``DSD`` for the definitive screening design, the smallest member of the
	family, and ``BBD``, in green, for the Box-Behnken design. The Box-Behnken cell closes
	its column, since every row below it would repeat ``Full`` on more runs.

For a single budget the same information is reported in words, with the neighbouring thresholds:

.. code-block:: text

	>>> get_omars_trade_off_table_entry(17, 4)
	OMARS: 17 runs, 4 factors
	  Quad: main effects and pure quadratics, with error degrees of freedom to test them
	  Model: main_quadratic (9 parameters), 8 error df
	  Thresholds for 4 factors: Satd 9, Quad 11, Full 21 runs.
	  4 more runs would reach Full (all two-factor interactions estimable).

Quality metrics are absent from the table. D-efficiency, the largest correlation among the
second-order effects and the projection properties all describe one particular design at a given
size rather than the size itself, so they belong to ``generate_omars`` and to
:ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>`.

With no run count given, ``generate_omars`` sizes the design at the frontier for the model it is
asked for:

.. code-block:: python

	design = generate_omars([Factor(name=c, low=-1, high=1) for c in "ABCD"], random_seed=42)
	print(design.n_runs)                                  # 21
	print(design.metadata["model_rank"])                  # 15, so the model is estimable
	print(design.metadata["min_runs_for_model"])          # 21, the frontier
	print(design.metadata["expected_error_df"])           # 6, which is k(k-1)/2

.. _DOE-omars-worked-examples:

Worked examples
^^^^^^^^^^^^^^^^^^

The table is read while the design is still a plan on paper. Two readings show the kinds of
question it settles, and a third example works through a budget that lands short of the frontier.

**Six factors in seventeen runs**, the size of a published extraction study. The cell is
``Quad df=4``: all six main effects and all six quadratics are estimable, with four degrees of
freedom to test them, so curvature can be judged factor by factor. ``Full`` for six factors begins
at 43 runs. The two-factor interactions are in the design and orthogonal to the main effects, but
not in the fitted model, so one that matters has to be found by the staged analysis of
:ref:`Analysing data from these designs <DOE-analysing-economical-designs>`.

**Five factors, with a budget that might stretch.** Thirteen runs give ``Quad df=2``: estimable and
testable, but with two degrees of freedom a 95% confidence interval extends 4.30 standard errors
either side of the estimate. Seventeen runs give ``Quad df=6``, the same model with that multiplier
down to 2.45. Thirty-one runs give ``Full df=10``, with every two-factor interaction estimable.
Those are three different studies rather than three sizes of one.

.. rubric:: Example with 4 factors and 19 runs, inside the band

Nineteen runs in four factors sits inside the band: four runs more than the fifteen parameters of
the full second-order model, and two runs short of the twenty-one the frontier asks for. Nothing
goes wrong at the bench and none of the data is wasted. The shortfall shows up at the analysis
stage.

At nineteen runs two quadratics are confounded with three interactions, so the full second-order
model cannot be fitted. A least squares fit still returns an answer without complaint: coefficient
sets differing by 8.5 units are indistinguishable from these runs, and disagree by as much at
settings that were never run. What nineteen runs do support is main effects and pure quadratics,
nine parameters with ten degrees of freedom for error, and the main effects stay clean of every
second-order term.

Two more runs reach the frontier. At twenty-one all six two-factor interactions join the model,
fifteen parameters with six degrees of freedom to test them, and a response surface can be fitted
from the single design.

Both are sound experiments, so the choice is a budget one. Capped at nineteen runs, an interaction
that matters has to be found by the staged analysis of :ref:`Analysing data from these designs
<DOE-analysing-economical-designs>` and confirmed in a follow-up. With twenty-one it arrives with
the first design.

.. _DOE-omars-what-a-cell-reports:

What a cell in either table reports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section and the next explain why the cells carry what they carry; the table itself can be
used without them.

A cell of the :ref:`two-level table <DOE_design_trade_off_BHH_272>` says less than it appears to.
Of the 165 sixteen-run, seven-factor designs worked through in
:ref:`DOE-trade-off-table-in-code`, 161 have resolution III and four reach resolution IV. The
numeral in that cell is not a description of a design. It is a statement about the *size*, that no
sixteen-run design in seven factors does better than resolution IV and that at least one achieves
it, so the table is a search presented as a lookup.

The OMARS analogue would be the best quality obtainable at each size. Three obstacles stand in the
way, each a property of the designs rather than of any particular measure.

**A run count does not pin down the experiment.** An OMARS design of :math:`N` runs splits its
budget between design points and replicates of the centre point, and the split is free. Take the
largest absolute correlation between any two second-order terms, a quantity computed from the
design alone: the same twelve design points in three factors, with one, three or five centre runs
added, give :math:`0.300`, :math:`0.071` and :math:`0.056`.

**A measure divided by the run count need not improve as runs are added.** Across every OMARS
design of each size in three factors, the least entangled at seventeen runs reaches :math:`0.056`,
while at nineteen runs the best possible is :math:`0.136`. Reversals occur throughout the range,
and a column that goes backwards cannot be read to choose a budget.

**A measure not divided by the run count mostly restates the run count.** The alphabetic optimality
criteria avoid the previous problem: an added run adds information and never removes any, so none
of them can worsen. The difficulty is the other way around: they fall at close to the rate
:math:`1/N`. Both points are set out in :ref:`DOE-omars-metric-choice` below, which is where the
five criteria are defined.

Resolution avoids all three because it is not a magnitude. It is a combinatorial statement about
which effects are confounded with which, and two-level fractions nest, so a larger design contains
a smaller one and extra runs can only break confounding. Neither holds for OMARS designs.

The OMARS cells therefore report a capability class and the error degrees of freedom. Both are
statements about *estimability*, the same species as resolution, and both are monotone in the run
count for the same reason. Quality metrics still separate designs of a given size, which is what
:ref:`DOE-omnibus-comparison` does with them.

.. _DOE-omars-metric-choice:

Nine measures down one column
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fix the factor count at three, one column of the OMARS trade-off table, and read down it. At each
run count, take the best value any OMARS design of that size attains. Every design of a given size
can be listed, so each point is the true optimum rather than the best a search happened to find:
a foldover is described entirely by how many times each pattern of :math:`-1`, :math:`0` and
:math:`+1` appears in its half, and three factors admit only thirteen such patterns.

Write :math:`\mathbf{M} = \mathbf{X}^T\mathbf{X}` for the model matrix :math:`\mathbf{X}` of the
main-effects-and-quadratics model, which has :math:`p = 2k + 1` terms, and
:math:`\mathbf{f}(\mathbf{x})` for the row that model takes at a point :math:`\mathbf{x}` in the
experimental region. Six of the nine measures score that same model at every run count, and five
of those six are the *alphabetic optimality criteria*, each a single summary of
:math:`\mathbf{M}`:

* :math:`A/p`, the average coefficient variance. Each fitted coefficient has a variance, the
  square of the standard error a regression package prints beside it;
  :math:`A = \mathrm{tr}(\mathbf{M}^{-1})` sums those variances and :math:`A/p` averages them.
* :math:`D = |\mathbf{M}|^{1/p}`, the joint precision of all :math:`p` coefficients at once. It
  is inversely proportional to the volume of their joint confidence region, and it is the only
  one of the five that accounts for how the estimates covary.
* :math:`E = \lambda_{\min}(\mathbf{M})`, the smallest eigenvalue of :math:`\mathbf{M}`. Some
  combinations of the coefficients are estimated precisely and others poorly; the worst one has
  variance :math:`1/E`, so :math:`E` is the worst case matching the average :math:`A/p` reports.
* :math:`I = \mathrm{tr}(\mathbf{M}^{-1}\mathbf{B})`, the average prediction variance. A
  prediction at a setting :math:`\mathbf{x}` has variance
  :math:`\mathbf{f}^T\mathbf{M}^{-1}\mathbf{f}`, the quantity behind the error band around a
  fitted curve; :math:`I` averages it over the region, with :math:`\mathbf{B}` holding the
  averages of the model terms there.
* :math:`G = \max_{\mathbf{x}}\, \mathbf{f}(\mathbf{x})^T \mathbf{M}^{-1}\mathbf{f}(\mathbf{x})`,
  the same prediction variance at its worst point in the region, so the worst case matching
  :math:`I`.

These are in units of the run-to-run noise: multiplied by :math:`\sigma^2`, each of :math:`A/p`,
:math:`I` and :math:`G` is a variance, and its square root is a standard error.

The sixth is not an optimality criterion. Max :math:`|r|` is the largest absolute correlation
between any two of the six second-order terms, read off the correlation map of the design.

The remaining three are *power*, the measure a practitioner is most likely to reach for: the
probability that the test on a single coefficient comes out significant, given that the
coefficient really is a certain size. Power needs two things from you that the six above do not.
The first is the effect size worth detecting, written :math:`|\beta|/\sigma`, the coefficient
measured in units of the run-to-run noise. With coded levels running :math:`-1` to :math:`+1` a
main-effect coefficient :math:`\beta` moves the response by :math:`2\beta` from the low setting to
the high one, so :math:`|\beta|/\sigma = 1` means a low-to-high change of twice the noise standard
deviation. The second is the significance level :math:`\alpha`. Power also differs by type of
term, so it needs one panel each for a main effect, a two-factor interaction and a pure quadratic.

Those three panels score the *full* second-order model, :math:`p = 1 + 2k + k(k-1)/2` terms, not
the smaller model the six above use, because the interactions have to be in the model for the
middle panel to mean anything. The consequence is visible in the figure: the third row starts at
thirteen runs, the :ref:`estimability frontier <DOE-omars-estimability-frontier>`
:math:`N = k^2 + k + 1`, while the rows above start at seven or nine.

For a coefficient with variance :math:`\sigma^2 c` the test statistic follows a non-central
:math:`F` distribution with :math:`1` and :math:`N - p` degrees of freedom and non-centrality
:math:`\lambda = (|\beta|/\sigma)^2 / c`, where :math:`c` is the matching diagonal entry of
:math:`\mathbf{M}^{-1}`. Reading one value in full: at nineteen runs with one centre run the best
attainable :math:`c` for a quadratic is 0.262, so its standard error is
:math:`\sqrt{0.262}\,\sigma = 0.512\sigma`; the expected :math:`t` statistic for a one-sigma
curvature is :math:`1/0.512 = 1.95`, against a critical value of 2.26 at nine degrees of freedom,
so the test falls short more often than not and the power is 0.415.

.. code-block:: python

	def moment_matrix(k):
	    """Moments of the cuboidal region, E[f(x) f(x)'], evaluated exactly."""
	    B = np.zeros((2 * k + 1, 2 * k + 1))
	    B[0, 0] = 1.0
	    for i in range(k):
	        B[1 + i, 1 + i] = 1 / 3                                   # E[x_i^2]
	        B[0, 1 + k + i] = B[1 + k + i, 0] = 1 / 3
	        for j in range(k):
	            B[1 + k + i, 1 + k + j] = 1 / 5 if i == j else 1 / 9  # E[x_i^4], E[x_i^2 x_j^2]
	    return B

	def criteria(levels, grid_levels=7):
	    """The five alphabetic criteria for the main-effects-and-quadratics model, and the
	    largest absolute correlation between two second-order terms."""
	    n_runs, k = levels.shape
	    X = np.column_stack([np.ones(n_runs), levels, levels**2])
	    M = X.T @ X
	    p, M_inv = M.shape[1], np.linalg.inv(M)
	    grid = np.array(list(itertools.product(np.linspace(-1, 1, grid_levels), repeat=k)))
	    f = np.column_stack([np.ones(len(grid)), grid, grid**2])
	    second = [levels[:, i] ** 2 for i in range(k)]
	    second += [levels[:, i] * levels[:, j] for i, j in itertools.combinations(range(k), 2)]
	    C = np.abs(np.corrcoef(np.column_stack(second), rowvar=False))
	    return {"A/p": np.trace(M_inv) / p,
	            "D": np.linalg.det(M) ** (1 / p),
	            "E": np.linalg.eigvalsh(M).min(),
	            "I": np.trace(M_inv @ moment_matrix(k)),
	            "G": ((f @ M_inv) * f).sum(axis=1).max(),
	            "max |r|": C[~np.eye(len(C), dtype=bool)].max()}

	# The twelve design points behind the centre-run example given earlier, as six half-rows
	# and their negations, scored with one, three and five centre runs added.
	half = np.array([[0, 1, -1], [0, 1, 1], [1, -1, 0],
	                 [1, 0, -1], [1, 0, 1], [1, 1, 0]], dtype=float)
	points = np.vstack([half, -half])
	for n_centre in (1, 3, 5):
	    levels = np.vstack([points, np.zeros((n_centre, 3))])
	    values = criteria(levels)
	    print(f"N = {len(levels)}   " + "   ".join(f"{n} = {v:.4f}" for n, v in values.items()))

	# N = 13   A/p = 0.3839   D = 5.3836   E = 0.5626   I = 0.5125   G = 1.0000   max |r| = 0.3000
	# N = 15   A/p = 0.2173   D = 6.2984   E = 1.6346   I = 0.3014   G = 0.6458   max |r| = 0.0714
	# N = 17   A/p = 0.1839   D = 6.7753   E = 2.6346   I = 0.2592   G = 0.6125   max |r| = 0.0556

Power is computed from the same design, against the full second-order model:

.. code-block:: python

	from scipy import stats

	def power(levels, effect_size=1.0, alpha=0.05):
	    """Power for a main effect, an interaction and a quadratic, full second-order model."""
	    n_runs, k = levels.shape
	    pairs = list(itertools.combinations(range(k), 2))
	    X = np.column_stack([np.ones(n_runs), levels, levels**2]
	                        + [levels[:, i] * levels[:, j] for i, j in pairs])
	    df = n_runs - X.shape[1]
	    c = np.diag(np.linalg.inv(X.T @ X))
	    blocks = {"main effect": c[1:k + 1],
	              "interaction": c[2 * k + 1:],
	              "quadratic": c[k + 1:2 * k + 1]}
	    critical = stats.f.ppf(1 - alpha, dfn=1, dfd=df)
	    return {name: 1 - stats.ncf.cdf(critical, dfn=1, dfd=df,
	                                    nc=effect_size**2 / block.max())
	            for name, block in blocks.items()}

	# The same twelve points with three centre runs: the Box-Behnken design in three factors.
	print(power(np.vstack([points, np.zeros((3, 3))])))

	# {'main effect': 0.6228, 'interaction': 0.3682, 'quadratic': 0.345}

Running ``criteria`` and ``power`` on every OMARS design of every size in three factors, and
keeping the best value of each measure at each size, gives the nine curves below.

.. figure:: ../figures/doe/omars-metric-choice.png
	:align: center
	:width: 800px
	:alt: omars-metric-choice.py

	Nine candidate measures read down the three-factor column of the OMARS trade-off table. Each
	point is the best value attainable at that run count, found by listing every OMARS design of
	the size. In the first two rows the panel columns group the measures by how they summarise:
	the left pair averages, the middle pair takes a worst case of the same two quantities, the
	right pair does neither. Insets on the last panel of the second row are correlation maps of
	five of the plotted designs: in each map the rows and columns are the six second-order
	terms, the three quadratics then the three interactions, with a thin line between the two
	blocks, and darker squares are higher correlations, on a common scale from zero to one.
	Each map is outlined in the colour of its series, and the three on the left are the smallest
	design at each centre-run count. The third row is power, one panel per type of term, and it
	scores the full second-order model rather than the model the rows above use, which is why it
	begins at thirteen runs. Two standard designs are marked wherever they are defined: the
	nine-run definitive screening design as an orange circle and the fifteen-run Box-Behnken
	design as a green star, in the colours those two carry in the trade-off table.

:math:`A/p`, :math:`I` and :math:`D` restate the run count. The first two fall at close to the
rate :math:`1/N`, the product :math:`N \times A/p` moving only from 3.57 at nine runs to 3.15 at
thirty-one, and a straight line in :math:`N` fits :math:`D` from eleven runs upward to within 0.27
on values from 4.5 to 13.6. All three have their centre-run series almost on top of one another.

:math:`E`, the smallest eigenvalue, carries structure the run count does not. It rises as a
staircase with flat treads: exactly 2.000 at eleven, thirteen and fifteen runs on the
three-centre-run series, and exactly 4.000 at twenty-two, twenty-four and twenty-six runs on the
two-centre-run series. Over a tread, the combination of coefficients the data pin down worst is
pinned down no better after the extra runs.

:math:`G`, the worst prediction variance, has a floor that needs no design to compute. A classical
result of Kiefer and Wolfowitz says no design of :math:`N` runs, of any kind, can have :math:`G`
below :math:`p/N`, here :math:`7/N`. The best three-factor designs reach the floor exactly at nine
and twenty-seven runs with one centre run, and at eighteen runs with two.

Max :math:`|r|` reverses: four of the eleven steps along the one-centre-run series go backwards,
the largest from 0.050 at twenty-one runs to 0.179 at twenty-three. It also separates the
centre-run series widely, at fifteen runs giving 0.378 with one centre run against 0.071 with
three. The three insets on the left show why: those designs share the same four half-rows, and
adding centre runs lowers the correlation between a quadratic and an interaction, from 0.707 to
0.645 to 0.606, while raising the correlation between two quadratics from zero to 0.167 to 0.267.
Max :math:`|r|` reaches zero at one size only, twenty-seven runs with one centre run, where the
design is the full three-level factorial.

Power is monotone in all three panels, so on that test it belongs with the alphabetic criteria
rather than with max :math:`|r|`. What it adds is an ordering the other measures do not show. A
main effect of one sigma reaches 0.8 power at fifteen runs with one centre run, an interaction of
the same size at nineteen, and a quadratic of the same size reaches only 0.744 at thirty-one runs,
the largest design plotted. The interaction sits nearer the main effect than the quadratic
because :math:`x_i x_j` is a :math:`\pm 1` column like a main effect, while :math:`x_j^2` takes
only the values zero and one and shares most of its variation with the intercept. Read as a
budgeting rule, the quadratics set the run count.

The centre-run series also swap order between panels. Centre runs are not factorial runs, so they
cost main-effect and interaction power: at fifteen runs the one-centre-run design gives 0.845 and
0.679 against 0.789 and 0.623 for three centre runs. For the quadratics the ordering reverses,
0.257 against 0.345 at the same fifteen runs, and only returns to the usual direction past about
twenty-five runs. This is the clearest statement in the chapter of what the extra centre runs buy.

The two marked designs make the same point from the other direction. The definitive screening
design in three factors sits exactly on the frontier in all six panels of the first two rows,
:math:`A/p = 0.397`, :math:`D = 3.970`, :math:`E = 0.811`, :math:`I = 0.578`, :math:`G = 0.778`
and max :math:`|r| = 0.707`, so at its size it is not merely a good design but the best on every
one of those measures at once. It is absent from the power row because nine runs cannot fit a
ten-term model. Note that it has nine runs rather than :math:`2k + 1 = 7`: the construction folds
a conference matrix of order :math:`k`, which exists only for an even :math:`k`, so an odd
:math:`k` uses one of order :math:`k + 1` and drops a column, and the design arrives with two runs
to spare.

The Box-Behnken design lands on the frontier in five panels, :math:`A/p`, :math:`D`, :math:`I`,
max :math:`|r|` and quadratic power, and clearly off it in four. Its smallest eigenvalue is 1.63
against a best of 2.00 at fifteen runs, its worst prediction variance 0.646 against 0.600, its
main-effect power 0.623 against 0.789 and its interaction power 0.368 against 0.623. Each factor
is at :math:`\pm 1` in only eight of its twelve edge points, so it puts its runs into curvature,
and that shows up as five measures at the frontier and four away from it.

The six enumerated measures also disagree about which design is best. At twenty-one runs with one centre run there are
1859 OMARS designs, and the six single out four different ones: :math:`A`, :math:`E` and :math:`I`
agree, while :math:`D`, :math:`G` and max :math:`|r|` each choose their own. The design minimising
max :math:`|r|` reaches 0.050 but has a smallest eigenvalue of 1.20, against 3.42 for the design
:math:`A`, :math:`E` and :math:`I` select, whose own max :math:`|r|` is 0.222. The four-factor
column behaves the same way. A single number in a cell would therefore have to name which of the
six it is.

Power does not escape that either. It is well behaved down the column, but it needs an effect size
and a significance level before it returns a number at all, and it needs three numbers rather than
one, because the three types of term differ by a factor of two or more at the same run count. It
also changes shape with the model scored: the smallest design that can fit the full second-order
model is the one that estimates the quadratics worst, which is the opposite of what the same
panels show once the interactions are dropped from the model.

In practice the two tools divide the work. The trade-off table chooses the run count, from
capability and error degrees of freedom. At that size, candidate designs are compared with the
measure matched to the aim of the study: the precision of the coefficients (:math:`A`, :math:`E`),
prediction over the region (:math:`I`, :math:`G`), keeping the second-order effects
distinguishable (max :math:`|r|`), or the chance of detecting an effect of a stated size (power).

.. _DOE-analysing-economical-designs:

Analysing data from these designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One last point, and it is easy to get wrong. Because these designs are deliberately economical
and carry structured aliasing, you should *not* simply throw the data at a least squares fit of
the full second-order model. Two things go wrong if you do. The model is often not estimable at
all, so the :math:`\mathbf{X}^T\mathbf{X}` matrix is singular and cannot be inverted. For four
factors, for example, the full quadratic model has :math:`1 + 4 + 4 + 6 = 15` terms (an
intercept, four main effects, four quadratics, and six two-factor interactions), while the
nine-run definitive screening design has nine runs and the thirteen-run OMARS design has
thirteen, so neither can fit it. As :ref:`the estimability frontier
<DOE-omars-estimability-frontier>` shows, the run count is not the binding constraint either: a
nineteen-run foldover in four factors has four runs to spare against those fifteen terms and
still cannot estimate them, because twenty-one runs are needed. And even when the model
can be fitted, a generic stepwise or penalised
regression treats every column alike and can let the entangled second-order effects leak into,
and bias, the main-effect estimates, throwing away the orthogonality the design was constructed
to provide.

The remedy is a *design-based* analysis that exploits the structure we built in. It proceeds in
stages: estimate the main effects first, where the design guarantees they are clean; recover
degrees of freedom from the effects that turn out to be inactive; and only then test for, and
select among, the second-order effects, in their own subspace and respecting how few of them can
be told apart. The workflow is:

::

    design matrix  +  measured responses
             |
             v
    (0)  is the model ESTIMABLE, with error df to spare?
         ( rank of the model matrix equals the number of terms
           being fitted, and the run count exceeds it )
         if not  ->  stop; shrink the model, replicate, or add runs
             |
             v
    (1)  estimate the MAIN EFFECTS
         clean and unbiased: they are orthogonal to every
         second-order term, whichever of those are active
             |
             v
    (2)  test them; pool the INACTIVE effects back into the
         error estimate, recovering degrees of freedom
             |
             v
    (3)  one F-TEST: is any second-order effect active at all?
         if not  ->  report the main-effects model
             |
             v
    (4)  SELECT the active second-order effects, limited by how
         many are jointly estimable and guided by factor heredity
         ( an interaction is admitted only if its parent main
           effects are active )
             |
             v
    final model: the active main, quadratic, and interaction effects

Step 0 is not a formality, and it has two parts. A *saturated* design, one with no spare runs,
leaves nothing with which to estimate the noise :math:`\sigma^2`, and without that estimate there
are no standard errors, no tests, and no power: the analysis cannot start. Below the
:ref:`estimability frontier <DOE-omars-estimability-frontier>` the situation is more basic still,
since the coefficients themselves have no unique solution, which is why the check is on the rank
of the model matrix and not on the run count. Step 1 is possible only
because of the orthogonality property: the main effects are unaliased with every second-order
term, so their estimates are unbiased no matter which interactions or quadratics are truly
active, which is what lets us analyse them on their own. Step 4 is where the design's one weakness is managed:
since the second-order effects are correlated among themselves, only a limited number can be
estimated together, and factor heredity (preferring the interaction whose parent main effects
are active) is the principled way to choose among the candidates the data alone cannot fully
separate. This staged procedure is available in ``process_improve`` as ``analyze_omars()``: it
takes any coded two- or three-level design with its measured responses and carries out exactly the
stages above, returning the clean main effects, the pooled error, the overall test for second-order
activity, and the heredity-constrained selection among the second-order effects.

**Readings**

* Jones, B. and Nachtsheim, C.J.: "Effective Design-Based Model Selection for Definitive
  Screening Designs", *Technometrics*, **59**, 319--329, 2017.
  `doi:10.1080/00401706.2016.1234979 <https://doi.org/10.1080/00401706.2016.1234979>`__
* Hameed, M.S.I., Núñez Ares, J. and Goos, P.: "Analysis of data from orthogonal minimally
  aliased response surface designs", *Journal of Quality Technology*, **55**, 366--384, 2023.
  `doi:10.1080/00224065.2022.2151530 <https://doi.org/10.1080/00224065.2022.2151530>`__
