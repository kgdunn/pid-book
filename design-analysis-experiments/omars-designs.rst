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
interactions. The only aliasing that remains is *among the second-order effects*, and the
designs are catalogued so as to keep that aliasing minimal, which is what the name records:
**o**\ rthogonal (clean main effects), **m**\ inimally **a**\ liased (the residual entanglement,
held down), **r**\ esponse **s**\ urface (a full second-order model is the target).

The important shift in thinking is this: OMARS is not a single design but a whole *catalogue*.
The 2020 enumeration found 7,933 basic designs, which become 55,531 in total once zero to six
centre runs are added to each. For a given number of factors there are many OMARS designs of
different run sizes, and they
trade off against one another: a larger design estimates more of the second-order effects, with
lower correlation among them and more power, at the cost of more runs. The
:ref:`definitive screening design <DOE-definitive-screening-designs>` turns out to be the
smallest member of the family; at the other extreme, the classical
face-centred central composite and Box-Behnken designs are themselves OMARS designs, so the
largest members coincide with the standard response surface designs. Choosing among them is
therefore a genuine multi-criteria decision, not a lookup, which is the subject of the
:ref:`spectrum below <DOE-design-spectrum>` and of :ref:`Judging and comparing designs
<DOE-judging-and-comparing-designs>`.

The original catalogue was produced by an enumeration based on integer programming that is
complete for three to five factors up to 44 runs, and partial for six and seven factors up to 70
runs, where the seven-factor search was restricted to foldover designs. Many of these designs are foldover
designs, built as the DSD was by folding over a base matrix whose columns are orthogonal. The
orthogonality of the main effects, however, comes from the construction itself: all odd design
moments through order three are set to zero, so the non-foldover designs in the catalogue have
equally clean main effects. The family has since been extended to mixed-level designs (three-level
quantitative factors together with two-level categorical factors) and to orthogonally blocked
designs. Larger OMARS designs can also be built by folding over and combining orthogonal building
blocks such as conference, weighing, and Hadamard matrices, the same mechanism that turns a single
conference matrix into a definitive screening design.

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
more runs buy more estimable second-order effects, lower correlation among them, and more power.
At the rich end sit the classical response surface designs, the :ref:`central composite
<DOE_central_composite_designs>` and :ref:`Box-Behnken <DOE-box-behnken-designs>` designs: enough
runs to estimate the full
second-order model with little or no aliasing, often with the near-rotatable prediction
behaviour those designs are prized for. In the face-centred case these classical designs are
themselves OMARS designs, the strongest and largest members of the family, so the spectrum is
really one continuous family rather than three separate boxes.

The axis along which they are arranged is the trade-off between three things: how many runs you
spend, how much of the second-order model you can estimate, and how cleanly (how free of
aliasing) you can estimate it. Spending more runs moves you to the right, buying estimability and
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
fit it is more common to change the model class than to raise the degree. That choice matters here
because the aliasing and the efficiency measures are properties of the design *together with* the
model: they are read from the model matrix, so a different model gives a different alias structure
and different efficiencies. Re-expressing the same quadratic in an orthogonal-polynomial basis (a
re-parameterisation that leaves the fitted surface unchanged) lowers the correlations among the
terms; a mechanistic model that is nonlinear in its parameters, or a flexible surrogate such as a
Gaussian process or a spline fit, would call instead for a design optimal for that model, or a
space-filling one. The spectrum here, and the measures that rank it, therefore describe the
second-order case, and the model itself is one of the choices rather than a fixed backdrop.

.. _DOE-omars-trade-off-table:

A trade-off table for OMARS designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`two-level trade-off table <DOE_design_trade_off_BHH_272>` answers a question of the form
"I have sixteen runs available and seven factors on the list, what do I give up?". Its currency is
:ref:`resolution <DOE-design-resolution>`: what is given up as more factors are studied in fewer
runs is the ability to tell main effects apart from interactions. Resolution III, IV and V form a
single ordered scale, and the table maps a budget onto it.

The natural thing to want is the same table for OMARS designs. It does not carry over, and the
reason is worth following, because repairing it turns on a question about run counts that has a
surprising answer.

An OMARS design has its main effects orthogonal to each other *and* to every second-order term, at
every size in the family: that is the defining property, and it is what the "orthogonal" in the
name records. There is no smaller OMARS design in which the main effects are dirtier, and no larger
one in which they are cleaner. Resolution is constant across the family, so it cannot be what the
table reports.

What varies instead is *which model the run count makes estimable at all*. That question turns out
to have a different answer from the one the usual parameter count gives, and the rest of this
section works it out before returning to the table itself.

.. _DOE-omars-estimability-frontier:

How many runs a second-order model needs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take the full
second-order model in :math:`k` factors: an intercept, :math:`k` main effects, :math:`k` pure
quadratics, and :math:`k(k-1)/2` two-factor interactions, so

.. math::

	p = 1 + 2k + \frac{k(k-1)}{2}

parameters in total. Count the parameters and spend at least that many runs. That rule sizes
factorial, central composite, Box-Behnken and optimal designs correctly, and it is how designs are
sized elsewhere in this chapter. Foldover designs are the exception, and this section works out by
how much.

A foldover stacks a half-design :math:`\mathbf{H}` of :math:`h` runs on its own sign-flipped copy,
then adds a centre run:

.. math::

	\mathbf{D} = \begin{bmatrix} \mathbf{H} \\ -\mathbf{H} \\ \mathbf{0} \end{bmatrix},
	\qquad N = 2h + 1

so :math:`N` is always odd. A row of :math:`\mathbf{H}` and its sign-flipped copy are called a
:index:`mirror-image pair <pair: mirror-image pair; experiments>`. This is the construction behind
the :ref:`definitive screening design <DOE-definitive-screening-designs>`, where
:math:`\mathbf{H}` is a conference matrix, and behind most of the OMARS catalogue.

Sort the model terms by what a mirror-image pair does to them. Flip the sign of *every* factor at
once: a term either changes sign or it does not. Terms that change sign are **odd**; terms that do
not are **even**. A term of total degree :math:`d` picks up a factor :math:`(-1)^d`, so the split
is simply the parity of the degree:

.. list-table:: Model terms sorted by parity.
	:header-rows: 1
	:widths: 14 44 22 20

	*   - Degree
	    - Terms
	    - Under a full sign flip
	    - Parity
	*   - 0
	    - Intercept
	    - unchanged
	    - even
	*   - 1
	    - Main effects, :math:`x_i`
	    - changes sign
	    - odd
	*   - 2
	    - Quadratics :math:`x_i^2` and interactions :math:`x_i x_j`
	    - unchanged
	    - even

This is the same odd/even split as the *odd design moments* named in the
:ref:`introduction to OMARS designs <DOE-omars-designs>`, and it explains the "through order
three" qualifier used there: degree three is odd again.

One point to fix before going on, because the words invite a different reading. Odd and even here
describe the *term*, not the factor. Both :math:`x_1` and :math:`x_2` are odd; :math:`x_1^2` and
:math:`x_1 x_2` are both even. Relabelling the factors, or reversing the direction of any of them,
changes nothing, which is why the constraint below holds for every foldover whatever
:math:`\mathbf{H}` is.

Now the consequence. A run and its mirror image differ only in sign, so they take *identical*
values in every even term. Five runs in two factors show the whole effect:

.. code-block:: text

	 run     x1  x2 |   1   x1²  x2²  x1x2     <- the even columns
	  H  1   +1  +1 |   1    1    1    +1
	  H  2   +1  -1 |   1    1    1    -1
	 -H  3   -1  -1 |   1    1    1    +1      identical to run 1
	 -H  4   -1  +1 |   1    1    1    -1      identical to run 2
	  0  5    0   0 |   1    0    0     0

Runs 3 and 4 are the mirror images of runs 1 and 2. In the odd columns they change sign, which is
what lets the design estimate main effects. In the even columns they repeat their partners exactly,
and add nothing. The even terms therefore see only :math:`h + 1` distinct rows, the :math:`h` rows
of :math:`\mathbf{H}` plus the centre run, no matter how many runs the foldover contains. Here that
is three distinct rows against four even columns, and indeed :math:`x_1^2` and :math:`x_2^2` are
the same column: those two quadratics cannot be told apart. More mirrors will never separate them;
only more distinct rows in :math:`\mathbf{H}` will.

Counting both parts, the even terms contribute at most :math:`\min\left(h + 1,\, 1 + k(k+1)/2\right)`
independent directions and the odd terms at most :math:`k`, so for every foldover design

.. math::
	:label: eq-omars-rank-bound

	\text{rank}(\mathbf{X}) \le k + \min\left(h + 1, \; 1 + \frac{k(k+1)}{2}\right)

This is an upper bound rather than an identity. Reaching it requires the :math:`h + 1` even rows to
be distinct and linearly independent, and :math:`\mathbf{H}` to have full column rank. A design
that repeats a run falls short, and so does one whose runs all happen to satisfy a single
second-degree equation: a two-level design is the standard example, since every run there has
:math:`x_i^2 = 1`, which is why two levels can never separate the quadratics. The three levels of a
foldover are what avoid this. Designs in the OMARS catalogue reach the bound.

Equation :eq:`eq-omars-rank-bound` puts the full second-order model out of reach until
:math:`h + 1 \ge 1 + k(k+1)/2`, that is :math:`h \ge k(k+1)/2`, and therefore until

.. math::
	:label: eq-omars-frontier

	N \; \ge \; k^2 + k + 1

There is no established name for this threshold, so we will call it the **estimability frontier**:
the smallest foldover design in which all :math:`p` coefficients of the full second-order model can
be estimated jointly.

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

The last two columns hold the same number, and that is not a coincidence. Subtracting the parameter
count from the frontier gives

.. math::

	\left(k^2 + k + 1\right) - \left(1 + 2k + \frac{k(k-1)}{2}\right) = \frac{k(k-1)}{2}

exactly the number of two-factor interactions. Two things follow from it.

The first is the exception to the sizing rule. For a foldover, having more runs than the model has
parameters does not establish that the model can be fitted. At four factors a
nineteen-run foldover has four spare runs against a fifteen-parameter model and still cannot
estimate it. Every other design family in this chapter sizes correctly on the parameter count; this
one needs :math:`k(k-1)/2` runs beyond it.

The second is that at the frontier the degrees of freedom left over for error also come to
:math:`k(k-1)/2`. The smallest design that can fit the full second-order model therefore arrives
with enough spare runs to test it, which is not true of a design sized on the parameter count.

The four-factor case can be checked directly. Build the coded design at nineteen runs and again at
twenty-one, form the full second-order model matrix, and take its rank:

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
estimability from the rank of the model matrix, not from the determinant of the information
matrix. The designs here were asked for with ``model="main_quadratic"``, because ``generate_omars``
refuses to size for the full second-order model below its frontier.

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
	design. The shaded band is where a design has more runs than the model has parameters
	and still cannot estimate it; the band is :math:`k(k-1)/2` runs deep. The marked point
	is the four-factor case checked in the code above.

.. _DOE-omars-inside-the-band:

Running a design from inside the band
"""""""""""""""""""""""""""""""""""""""

Suppose the nineteen-run design is run anyway. At the bench nothing goes wrong: nineteen runs give
nineteen measurements, and none of the data is wasted. What is missing appears at the analysis
stage, and it is a question of uniqueness rather than of noise.

Fitting the full second-order model to those nineteen runs leaves one direction in the coefficients
that the data cannot see, a fixed combination of two of the quadratic terms and three of the
interactions. Adding any amount of that combination changes the coefficients while leaving all
nineteen fitted values exactly as they were. The situation is the one where two numbers are known
to add up to ten and each is asked for separately: every pair that sums to ten agrees with what is
known, so the information is not wrong, it simply does not single out an answer.

Software asked for "the" answer will still return one. Two coefficient sets differing by up to 8.5
units in individual terms give identical fitted values at all nineteen runs, the same residual sum
of squares, and the same :math:`R^2`; the residual plots are identical too. Where they differ is in
prediction away from the runs that were made: at three untried settings the two sets disagreed by
8.5 units, by 3.2 units, and at the third by nothing at all. Some directions are unaffected and
some are not, and the usual summaries do not indicate which one is in play.

What stays sound is worth stating just as plainly. Predictions at the settings that were actually run
are unaffected. The main effects remain orthogonal to every second-order term, so they are
estimated cleanly. And the smaller model of main effects and pure quadratics is comfortably
supported: nineteen runs fit its nine parameters with ten degrees of freedom left for error. The
decision is therefore between answering the smaller question well with nineteen runs and spending
two more to reach twenty-one, not between a good experiment and a ruined one.

The literature usually states this capability the other way round, as a projection property: a
definitive screening design in six or more factors supports a full second-order model in any three
of its factors, and one of eighteen runs or more in any four. That is the same arithmetic asked
from the other end, "how many factors can I get a full second-order model in?" rather than "how
many runs until I get it in all :math:`k`?".

If the frontier is beyond the budget, the remaining option is to fit a smaller model rather than
accept a design that cannot fit the larger one. Main effects and pure quadratics need
:math:`1 + 2k` parameters, which a foldover reaches at :math:`2k + 1` runs and clears with degrees
of freedom to spare at :math:`2k + 3`. That is the choice the table sets out cell by cell.


.. _DOE-omars-reading-the-table:

Reading the table
^^^^^^^^^^^^^^^^^^^^^

With the frontier settled, the cells can say something useful. Three capability classes follow from
it, tagged with four characters so that they line up in a table:

``Full``
	:math:`N \ge k^2 + k + 1`, the estimability frontier. Main effects, pure quadratics and
	every two-factor interaction are estimable jointly, so a response surface can be fitted
	from this one design without a follow-up.

``Quad``
	:math:`N \ge 2k + 3`. Main effects and the pure quadratics are estimable, with degrees of
	freedom left over to test them, so curvature can be judged factor by factor. The two-factor
	interactions are present in the *design*, and they are still orthogonal to the main effects,
	but they are not in the *model*.

``Satd``
	:math:`N = 2k + 1`. Saturated: the parameters of the main-effects-plus-quadratics model can
	be estimated, but nothing is left with which to estimate :math:`\sigma^2`, so there are point
	estimates and no standard errors, no tests, and no power.

The three tags sort alphabetically in decreasing order of capability, ``Full`` before ``Quad``
before ``Satd``, which makes the table easy to read down a column. The table itself, and the
report for a single cell, come from ``process_improve``:

.. code-block:: python

	from process_improve.experiments import (
	    get_omars_trade_off_table_entry,
	    omars_trade_off_table,
	)

	omars_trade_off_table()                          # the whole table
	get_omars_trade_off_table_entry(17, 4)           # one cell, reported in words

.. code-block:: text

	runs  k=3        k=4        k=5        k=6        k=7
	-------------------------------------------------------------
	9     Quad df=2  Satd df=0
	13    Full 3     Quad 4     Quad df=2  Satd df=0
	17    Full 7     Quad 8     Quad 6     Quad 4     Quad df=2
	21    Full 11    Full 6     Quad 10    Quad 8     Quad 6
	25    Full 15    Full 10    Quad 14    Quad 12    Quad 10
	31    Full 21    Full 16    Full 10    Quad 18    Quad 16
	37    Full 27    Full 22    Full 16    Quad 24    Quad 22
	43    Full 33    Full 28    Full 22    Full 15    Quad 28
	57    Full 47    Full 42    Full 36    Full 29    Full 21

Each cell carries the capability class and the number of error degrees of freedom the budget
leaves over, which is what the model is tested with. Five things are worth reading off the table:

	*	**Down a column, capability only improves; across a row, it only worsens.** More runs
		never buy less, and more factors never cost less, so the boundary between the classes
		is a staircase.

	*	**The step up to** ``Full`` **in each column is the estimability frontier**
		:math:`N = k^2 + k + 1` derived in :ref:`How many runs a second-order model
		needs <DOE-omars-estimability-frontier>`: 13, 21, 31, 43 and 57 runs for three to
		seven factors. Every cell from there down the column is ``Full``.

	*	**Blank cells are not designs at all**, rather than poor ones. A foldover has
		:math:`N = 2h + 1` runs, so an even budget cannot be one, and a budget below
		:math:`2k + 1` cannot hold the main effects and the quadratics.

	*	**Error degrees of freedom are not comparable across the classes**, because the model
		differs. At 43 runs, six factors show ``Full df=15`` and seven factors show
		``Quad df=28``: the seven-factor cell has more spare runs precisely because it is
		fitting the smaller model.

	*	**The definitive screening design sits in the top live cell of each column.** For an
		even number of factors a DSD has :math:`2k+1` runs and lands in ``Satd``, which is
		another way of saying a nine-run, four-factor DSD is exactly saturated for main effects
		and quadratics. For an odd number of factors the conference-matrix construction needs
		:math:`2k+3` runs, so the three-, five- and seven-factor DSDs (nine, thirteen and
		seventeen runs) arrive with two spare degrees of freedom and land in ``Quad df=2``.

.. code-block:: python

	import plotly.graph_objects as go
	from process_improve.experiments import get_omars_trade_off_table_entry
	from process_improve.experiments.omars_trade_off import DEFAULT_FACTORS, DEFAULT_RUNS

	shade = {"full": 3, "quad": 2, "satd": 1, "none": 0}
	cells = [[get_omars_trade_off_table_entry(n, k, display=False) for k in DEFAULT_FACTORS] for n in DEFAULT_RUNS]

	fig = go.Figure(go.Heatmap(
	    z=[[shade[c.capability] for c in row] for row in cells],
	    x=[f"k = {k}" for k in DEFAULT_FACTORS], y=[str(n) for n in DEFAULT_RUNS],
	    text=[[f"{c.tag}<br>df = {c.error_df}" if c.exists else "" for c in row] for row in cells],
	    texttemplate="%{text}", showscale=False, xgap=3, ygap=3,
	    colorscale=[[0.0, "#F4F4F4"], [0.33, "#E69F00"], [0.67, "#56B4E9"], [1.0, "#0072B2"]]))
	fig.update_layout(xaxis_title="Number of factors", yaxis_title="Number of runs",
	                  xaxis=dict(side="top"), yaxis=dict(autorange="reversed"))
	fig.show()

.. figure:: ../figures/doe/omars-capability-staircase.png
	:align: center
	:width: 640px
	:alt: omars-capability-staircase.py

	The OMARS trade-off table, drawn as a capability staircase. Each cell gives the largest
	model the run budget makes estimable and the error degrees of freedom left to test it.
	The outlined cells are the estimability frontier :math:`N = k^2 + k + 1`, the first
	``Full`` cell in each column. Blank cells are budgets that are not a foldover design.

For a single budget the same information is reported in words, including what the neighbouring
thresholds are, so a cell that is not the one you wanted still tells you what it would take:

.. code-block:: text

	>>> get_omars_trade_off_table_entry(17, 4)
	OMARS: 17 runs, 4 factors
	  Quad: main effects and pure quadratics, with error degrees of freedom to test them
	  Model: main_quadratic (9 parameters), 8 error df
	  Thresholds for 4 factors: Satd 9, Quad 11, Full 21 runs.
	  4 more runs would reach Full (all two-factor interactions estimable).

.. _DOE-omars-worked-examples:

Three worked readings
^^^^^^^^^^^^^^^^^^^^^^^^

The table earns its place before any runs are made, when the design is still a plan on paper.
Three readings show the kinds of question it settles.

**Six factors in seventeen runs.** This is the size of a published extraction study: six solvent
and process factors, seventeen runs. The cell is ``Quad df=4``. All six main effects and all six
quadratics are estimable, with four degrees of freedom left over to test them, so curvature can be
judged factor by factor. The cell also says what is not on offer: ``Full`` for six factors begins at
43 runs. The two-factor interactions are in the design, and they are orthogonal to the main effects,
but they are not in the fitted model, so an interaction that matters has to be found by the staged
analysis of :ref:`Analysing data from these designs <DOE-analysing-economical-designs>` and then
confirmed in a follow-up.

**Four factors, with a response surface wanted from one design.** The full second-order model in
four factors has fifteen parameters, so the parameter count suggests that nineteen runs is
comfortable. The table gives ``Quad df=10`` at nineteen runs, and puts ``Full`` at twenty-one. Those
two extra runs are the difference between a model that can be fitted and one that cannot, and the
cheapest place to discover that is here, rather than after the runs are made.

**Five factors, with a budget that might stretch.** Reading down the :math:`k = 5` column sets out
the decision. Thirteen runs give ``Quad df=2``, which is estimable and testable, but on two degrees
of freedom. Seventeen runs give ``Quad df=6``: the same model, with more power behind the tests.
Thirty-one runs give ``Full df=10``, with every two-factor interaction estimable. Those are three
different studies rather than three sizes of one, and the middle one is often the right answer,
since four runs beyond the minimum triple the degrees of freedom without extending the model.

Every number in this table is closed-form: the capability classes come from
equation :eq:`eq-omars-frontier` and the degrees of freedom from a subtraction, so the table is
exact and instant, while building an actual design at one of these sizes runs an integer program
that takes about 0.1 seconds at three factors and about 980 seconds at seven.

Quality metrics are absent for a related reason. D-efficiency, the largest correlation among the
second-order effects and the projection properties all describe one particular design at a given
size rather than the size itself, so they belong to ``generate_omars`` and to
:ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>`.

Asking for the design at the four-factor frontier shows how the two fit together. With no run
count given, ``generate_omars`` sizes the design at the frontier for the model it is asked for,
and reports the rank it achieved alongside the degrees of freedom that leaves:

.. code-block:: python

	design = generate_omars([Factor(name=c, low=-1, high=1) for c in "ABCD"], random_seed=42)
	print(design.n_runs)                                  # 21
	print(design.metadata["model_rank"])                  # 15, so the model is estimable
	print(design.metadata["min_runs_for_model"])          # 21, the frontier
	print(design.metadata["expected_error_df"])           # 6, which is k(k-1)/2

.. _DOE-omars-what-a-cell-reports:

What a cell in either table reports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is worth being explicit about what a cell of the :ref:`two-level table
<DOE_design_trade_off_BHH_272>` has been saying all along, because it is not quite what it appears
to say. Take the sixteen-run, seven-factor cell worked through in :ref:`DOE-trade-off-table-in-code`.
Three generators define such a design, chosen from the eleven products of two or more of the four
base factors, which gives 165 distinct designs. Of those, 161 have resolution III. Four reach
resolution IV. The numeral in the cell is therefore not a description of a design: it is a
statement about the *size*, that no sixteen-run design in seven factors does better than resolution
IV, and that at least one achieves it. The table is the result of a search, presented as a lookup.

Read that way, what an OMARS cell should report becomes clear: the best quality obtainable at that
size. Three obstacles stand in the way. Each is a property of the designs themselves rather than a
shortcoming of any particular measure, which is why none of them is repaired by choosing a
different one.

**A run count does not pin down the experiment.** An OMARS design of :math:`N` runs splits its
budget between design points and replicates of the centre point, and the split is free. Take twelve
design runs in three factors and add one, three or five centre runs. The largest absolute
correlation between any two second-order terms, which is the usual measure of how entangled they
are, is then :math:`0.300`, :math:`0.071` and :math:`0.056` respectively, for exactly the same
twelve design points. A cell indexed on the run count alone cannot say which of these it means.

**A measure divided by the run count need not improve as runs are added.** Searching every OMARS
design of each size in three factors, the least entangled design at seventeen runs reaches
:math:`0.056`, and at nineteen runs the best possible is :math:`0.136`. More runs, a worse design,
and not by a small margin. Reversals of this kind occur throughout the range and do not die out as
the designs grow. A column that can go backwards cannot be read to choose a budget, which is the
one thing a trade-off table is for.

**A measure not divided by the run count mostly restates the run count.** The alphabetic optimality
criteria avoid the previous problem, and provably so: adding a run to a design adds a positive
semi-definite term to :math:`\mathbf{X}^T\mathbf{X}`, which can only grow, so none of
:math:`A`, :math:`D`, :math:`E`, :math:`I` or :math:`G` can worsen. The difficulty is the other way
around. The average variance of an estimated coefficient falls roughly as :math:`1/N`, so a column
of those values tracks the run count that already labels the row.

Resolution escapes all three because it is not a magnitude. It is a combinatorial statement about
which effects are confounded with which, and two-level fractions nest, so a larger design contains
a smaller one and extra runs can only break confounding, never create it. Neither of those holds
for OMARS designs: they do not nest in the same way, and every quality measure is a magnitude.

This is why the cells of the OMARS table report a capability class and the error degrees of
freedom, and no measure of design quality. Those two are statements about *estimability*, the same
species of statement as resolution, and they are monotone in the run count for the same reason.
Quality metrics still matter for choosing among designs of a given size, and
:ref:`DOE-omnibus-comparison` compares several designs on exactly those grounds. They simply
cannot be reduced to one number per cell.

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
and bias, the main-effect estimates, throwing away the very orthogonality the design worked so
hard to provide.

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
