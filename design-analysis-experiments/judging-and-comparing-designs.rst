.. _DOE-judging-and-comparing-designs:

.. index::
    pair: design evaluation; experiments
    pair: information matrix; experiments
    pair: prediction variance; experiments
    pair: scaled prediction variance; experiments
    pair: fraction of design space; experiments
    see: FDS plot; fraction of design space
    see: SPV; scaled prediction variance

Judging and comparing experimental designs
=============================================

By this point we have several ways to build a design: :ref:`full factorials
<DOE-two-level-factorials>`, :ref:`fractional factorials <DOE-fractional-factorials>`,
:ref:`central composite designs <DOE_central_composite_designs>`, and the
more flexible :ref:`optimal designs <DOE-optimal-designs>`. A practical question
follows almost immediately: when you are handed two or three candidate designs
(perhaps a small screening design, a slightly larger one, and a classical response
surface design), how do you decide which is *better*?

A good design has to do two separate jobs well, and it helps to keep them apart in
your mind:

    #.  **Separability.** Can we tell the effects apart, so that the estimate of one
        term is not confounded with another? This is the language of
        :ref:`aliasing and resolution <DOE-design-resolution>`.

    #.  **Precision.** Even when the effects are separable, how *precisely* can we
        estimate the coefficients and predict the response?

Both questions are answered by a single object built from the design: the information
matrix :math:`\mathbf{M} = \mathbf{X}^T\mathbf{X}`, together with the optimality criteria
that summarise it. Both are introduced in the previous section,
:ref:`Optimal designs and OMARS designs <DOE-optimal-and-omars-designs>`, so here we take
them as given. This subchapter shows how prediction variance is derived from
:math:`\mathbf{M}`, and how to read a fraction-of-design-space plot. We close with a short
checklist for choosing between designs.

Prediction variance
~~~~~~~~~~~~~~~~~~~~~~~

We rarely stop at the coefficients; in :ref:`response surface work <DOE-RSM>` we use the
model to *predict*, and to chase an optimum, so the variance of a prediction is what we
ultimately care about. The predicted response at any point :math:`\mathbf{x}` is
:math:`\widehat{y}(\mathbf{x}) = \mathbf{x}_m(\mathbf{x})^T \mathbf{b}`, where
:math:`\mathbf{x}_m(\mathbf{x})` is the model expansion of that point. Propagating the
variance through this linear combination, using the rule
:math:`\text{Var}(\mathbf{a}^T\mathbf{b}) = \mathbf{a}^T\,\text{Var}(\mathbf{b})\,\mathbf{a}`
with :math:`\mathbf{a} = \mathbf{x}_m(\mathbf{x})`,

.. math::

    \text{Var}\big(\widehat{y}(\mathbf{x})\big)
        = \mathbf{x}_m(\mathbf{x})^T \,\text{Var}(\mathbf{b})\, \mathbf{x}_m(\mathbf{x})
        = \sigma^2\, \mathbf{x}_m(\mathbf{x})^T \mathbf{M}^{-1} \mathbf{x}_m(\mathbf{x})

Read this as a product of three things. The variance of a prediction at a new point depends on
**where** you are predicting (the model expansion :math:`\mathbf{x}_m(\mathbf{x})`, which encodes
how far that point sits from the centre of the design in coded space), on **how the design is laid
out** (the inverse information matrix :math:`\mathbf{M}^{-1}`, the entire geometry of the runs
distilled into one matrix), and on **how noisy the system is** (the baseline variance
:math:`\sigma^2`). Only the middle term is in the experimenter's hands: the first is set by where
you happen to want a prediction, and the last is a property of the process.

That is the entire derivation: it is just error propagation through the linear
predictor, using :math:`\text{Var}(\mathbf{b}) = \sigma^2 \mathbf{M}^{-1}`.

For the three-run example from the :ref:`previous section <DOE-information-matrix-worked-example>`,
multiplying :math:`[1, x, x^2]` through :math:`\mathbf{M}^{-1}` and contracting gives a tidy
polynomial:

.. math::

    \text{Var}\big(\widehat{y}(x)\big) = \sigma^2 \left(1 - 1.5\,x^2 + 1.5\,x^4\right)

At the three design points (:math:`x = -1, 0, +1`) this equals :math:`\sigma^2`, as it
must: a saturated design interpolates its own data. Between the points it dips to a
minimum of :math:`0.625\,\sigma^2` at :math:`x = \pm 0.707`, and beyond :math:`x = 1` it
climbs steeply (already :math:`5.2\,\sigma^2` at :math:`x = 1.5`): a quantitative warning
against extrapolation.

This and every figure in this subchapter is reproducible with `process_improve
<https://github.com/kgdunn/process-improve>`_ (``pip install 'process-improve[expt]>=1.42'``).
Each block imports what it needs; the final figure also reuses the FDS helper and the designs
built in the two blocks before it, so paste them in order. The prediction variance of the
three-run quadratic design is a closed form:

.. code-block:: python

	import numpy as np
	import plotly.graph_objects as go

	# Single-factor quadratic design {-1, 0, +1}: the prediction variance is a closed form.
	x = np.linspace(-1.6, 1.6, 321)
	pred_var = 1 - 1.5 * x**2 + 1.5 * x**4              # Var(y_hat) / sigma^2

	fig = go.Figure(go.Scatter(x=x, y=pred_var, mode="lines"))
	fig.add_vrect(x0=-1.6, x1=-1, fillcolor="LightSalmon", opacity=0.2, line_width=0)
	fig.add_vrect(x0=1, x1=1.6, fillcolor="LightSalmon", opacity=0.2, line_width=0)
	fig.update_layout(xaxis_title="x (coded)", yaxis_title="Prediction variance / sigma^2")
	fig.show()

.. figure:: ../figures/doe/prediction-variance-extrapolation.png
    :align: center
    :width: 750px
    :alt: prediction-variance-extrapolation.py

    Prediction variance for the three-run quadratic design. It equals :math:`\sigma^2` at the three
    design points, dips to :math:`0.625\,\sigma^2` midway between them, and climbs steeply once
    :math:`x` leaves the design region :math:`[-1, +1]`. The shaded bands are the extrapolation
    zone, where predictions become rapidly less certain.

To *compare designs* we strip out two nuisance factors. We divide by the unknown
:math:`\sigma^2` (a property of the process, not the design), and we multiply by the
number of runs :math:`N` (otherwise a design looks better merely for being larger:
replicate any design and :math:`\mathbf{M}` doubles, halving the variance). The result
is the :index:`scaled prediction variance <pair: scaled prediction variance; experiments>`:

.. math::

    \text{SPV}(\mathbf{x}) = N\, \mathbf{x}_m(\mathbf{x})^T \mathbf{M}^{-1} \mathbf{x}_m(\mathbf{x})
                           = \frac{N\,\text{Var}\big(\widehat{y}(\mathbf{x})\big)}{\sigma^2}

The SPV depends only on the geometry of the design. The G-optimal value is its maximum
over the region, and the I-optimal value is its average over the region (V-optimality is the
same average taken over a chosen set of points rather than over the whole region).

A worked example: augmenting a small design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`previous section <DOE-information-matrix-worked-example>` worked out the information
matrix of the smallest design with curvature: a single factor at three levels,
:math:`x = -1, 0, +1`, fitting the quadratic model :math:`y = b_0 + b_1 x + b_2 x^2 + e`. That
single design is rarely the end of the story. Suppose the budget stretches to two more runs.
Two natural options present themselves, and they pull in different directions:

    *   add **two replicate centre points** (two more runs at :math:`x = 0`), or
    *   add **a point at** :math:`x = -1` **and one at** :math:`x = +1`, reinforcing the extremes.

Which is better? It depends entirely on what we ask of the design, and the optimality criteria turn
that vague question into an arithmetic one. The table below evaluates four designs on the same
quadratic model: the base three-run design, the base design with all three runs repeated, the base
plus two centre points, and the base plus two extreme points. The criteria are the raw,
unnormalised summaries of :math:`\mathbf{M}` from earlier (:math:`D = \det\mathbf{M}`,
:math:`A = \text{trace}\,\mathbf{M}^{-1}`, :math:`E = \lambda_{\min}(\mathbf{M})`), together with
the maximum and average of the prediction variance
:math:`d(x) = \mathbf{x}_m^T \mathbf{M}^{-1} \mathbf{x}_m` over :math:`x \in [-1, +1]` (these are the
:math:`G` and :math:`I` quantities, in units of :math:`\sigma^2`).

.. list-table:: Four candidate designs for the single-factor quadratic model.
    :header-rows: 1
    :widths: 34 8 12 16 14 8 8

    *   - design
        - :math:`N`
        - :math:`\uparrow\ D=\det\mathbf{M}`
        - :math:`\downarrow\ A=\text{trace}\,\mathbf{M}^{-1}`
        - :math:`\uparrow\ E=\lambda_{\min}`
        - :math:`\downarrow\ G`
        - :math:`\downarrow\ I`
    *   - base :math:`\{-1, 0, +1\}`
        - 3
        - 4
        - 3.00
        - 0.44
        - 1.0
        - 0.80
    *   - base, all three runs repeated
        - 6
        - 32
        - 1.50
        - 0.88
        - 0.5
        - 0.40
    *   - base + two centre points
        - 5
        - 12
        - 1.67
        - 1.00
        - 1.0
        - 0.44
    *   - base + two points at :math:`\pm 1`
        - 5
        - 16
        - 2.50
        - 0.47
        - 1.0
        - 0.67

It is worth seeing the matrices these summaries come from. Writing each run as
:math:`\mathbf{x}_m = [\,1,\ x,\ x^2\,]` and stacking the runs as the rows of :math:`\mathbf{X}`,
the base three-run design (row 1) gives the matrix already worked out in the
:ref:`previous section <DOE-information-matrix-worked-example>`,

.. math::

    \mathbf{X}_1 = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix},
    \qquad
    \mathbf{M}_1 = \mathbf{X}_1^T\mathbf{X}_1
        = \begin{bmatrix} 3 & 0 & 2 \\ 0 & 2 & 0 \\ 2 & 0 & 2 \end{bmatrix}

Repeating all three runs (row 2) stacks a second copy of every row, which simply doubles the
information matrix,

.. math::

    \mathbf{X}_2 = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 1 \\
        1 & -1 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix},
    \qquad
    \mathbf{M}_2 = \begin{bmatrix} 6 & 0 & 4 \\ 0 & 4 & 0 \\ 4 & 0 & 4 \end{bmatrix}
        = 2\,\mathbf{M}_1

Adding two centre points instead (row 3) repeats the centre run, feeding the intercept while
leaving the boundary runs unchanged,

.. math::

    \mathbf{X}_3 = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 1 \\
        1 & 0 & 0 \\ 1 & 0 & 0 \end{bmatrix},
    \qquad
    \mathbf{M}_3 = \begin{bmatrix} 5 & 0 & 2 \\ 0 & 2 & 0 \\ 2 & 0 & 2 \end{bmatrix}

while adding a point at each extreme (row 4) keeps the single centre run but doubles the two
boundary runs,

.. math::

    \mathbf{X}_4 = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 1 \\
        1 & -1 & 1 \\ 1 & 1 & 1 \end{bmatrix},
    \qquad
    \mathbf{M}_4 = \begin{bmatrix} 5 & 0 & 4 \\ 0 & 4 & 0 \\ 4 & 0 & 4 \end{bmatrix}

The :math:`D`, :math:`A`, and :math:`E` columns of the table are nothing more than the determinant,
the trace of the inverse, and the smallest eigenvalue of each of these :math:`\mathbf{M}` matrices,
and the prediction columns :math:`G` and :math:`I` follow from :math:`\mathbf{M}^{-1}` exactly as in
the previous section. Notice already how the two five-run designs compare: :math:`\mathbf{M}_3` and
:math:`\mathbf{M}_4` share the same intercept information (:math:`M_{00} = 5`, since each adds two
runs to the base), but the centre-point design holds the intercept-quadratic cross-term down at
:math:`M_{02} = 2`, whereas doubling the boundary runs drives it up to :math:`M_{02} = 4`. That
difference in entanglement, read straight off :math:`\mathbf{M}_3` and :math:`\mathbf{M}_4`, is the
seed of the comparison below.

Before reading the numbers, fix the direction each criterion should move towards. A design is better when
:math:`D` is **larger** (a bigger determinant is more joint information and a smaller confidence
ellipsoid), when :math:`A` is **smaller** (a smaller :math:`\text{trace}\,\mathbf{M}^{-1}` is a
lower average coefficient variance), when :math:`E` is **larger** (a bigger smallest eigenvalue
means the worst-estimated direction is better pinned down), and when :math:`G` and :math:`I` are
**smaller** (lower worst-case and lower average prediction variance). The arrow at the head of each
column marks that direction of improvement: :math:`\uparrow` where larger is better and
:math:`\downarrow` where smaller is better. "Better" points a different way in each column, which is
precisely why no single design is best in every column.

Now read the rows, and notice the run-count effect first. Going from the base design to the same
design with every run repeated, *every* criterion improves: :math:`D` jumps by a factor of
:math:`2^p` (here :math:`p = 3`, so :math:`4 \to 32`), :math:`A` halves, :math:`E` doubles, and
both :math:`G` and
:math:`I` halve. Nothing about the design got better; we only ran more experiments. This is the
warning to keep for later: the raw criteria scale with the number of runs :math:`N`, so they
cannot be used to compare designs of different size. We undo that scaling below. For the same
reason, the base design cannot be compared with either five-run design.

The fair comparison is between the two five-run designs, and here the criteria start to help make a
decision. Adding the two extreme points maximises :math:`D` (16 versus 12 when adding two replicate
centre points): spreading runs to the boundary buys more joint information on the coefficient
estimates, so it is the choice when the goal is to estimate the coefficients jointly.

Adding the two centre points instead reduces :math:`A` (1.67 versus 2.50) because it lowers the
average coefficient variance. The reason is visible in the information matrix. The weak spot of the
base design is the intercept-quadratic pair: the two are correlated (:math:`M_{02} = 2`) and the
quadratic is the least precise coefficient (:math:`\text{Var}(b_2) = 1.5\,\sigma^2`). A centre run
expands to :math:`\mathbf{x}_m = [\,1,\ 0,\ 0\,]`, so it adds information to the intercept alone:
it raises :math:`M_{00}` from 3 to 5 while leaving the entangling cross-term :math:`M_{02}`
untouched. Pinning the intercept down this way partly de-correlates it from :math:`b_2` and pulls
:math:`\text{Var}(b_2)` from :math:`1.5\,\sigma^2` down to :math:`0.83\,\sigma^2`, and that drop in
the largest coefficient variance is what lowers the average.

The centre points also maximise :math:`E` (1.00 versus 0.47), the smallest eigenvalue of
:math:`\mathbf{M}`, which gauges how well the *worst-estimated* direction in coefficient space is
pinned down. That weakest direction is the very same intercept-quadratic combination, so the runs
that de-correlate the pair are exactly the ones that strengthen it. The extreme points cannot help
here: their rows :math:`[\,1,\ -1,\ 1\,]` and :math:`[\,1,\ +1,\ 1\,]` *deepen* the entanglement
(the cross-term grows to :math:`M_{02} = 4`), which is why :math:`E` barely moves from the base
value of 0.44.

Finally the centre points minimise :math:`I` (0.44 versus 0.67), the average prediction variance
over the region: concentrating runs in the interior predicts better across the bulk of the factor
space, where the fitted model is most often used. The worst-case prediction variance :math:`G` is a
tie between the two five-run designs.

So the dilemma resolves based on your intentions: reinforce the extremes if you want the tightest
joint estimate of the coefficients, add centre runs if you care about average precision and
prediction. That is the :math:`D`-for-estimation, :math:`I`-for-prediction split we return to in
the closing checklist.

Return for a moment to the dilemma table. The base three-run design has
:math:`\text{SPV}(x) = 3\,(1 - 1.5\,x^2 + 1.5\,x^4)`, with a maximum of :math:`3` at the design
points and an average of :math:`2.4` over the region. Now scale the design that simply repeated all
three runs: it has :math:`N = 6` and half the prediction variance, so its SPV is
:math:`6 \times \tfrac{1}{2}(1 - 1.5\,x^2 + 1.5\,x^4)`, the *identical* curve. Scaling by :math:`N`
has exactly cancelled the artificial gain from pure replication: on the SPV scale the two designs
are correctly seen as one and the same. This is the fix promised earlier, and it is why the
fraction-of-design-space plot below is built from the SPV rather than from the raw prediction
variance.

The fraction-of-design-space (FDS) plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A single design has a *different* SPV at every point in the factor region, so quoting one
number hides a lot. The :index:`fraction-of-design-space plot <pair: fraction of design space; experiments>`
(FDS plot) shows the whole distribution. It is worth being precise about how it is built, because
the recipe is far less mysterious than the finished plot can look.

Start from the key fact that
:math:`\text{SPV}(\mathbf{x}) = N\,\mathbf{x}_m(\mathbf{x})^T \mathbf{M}^{-1} \mathbf{x}_m(\mathbf{x})`
is a *closed-form function of position*. A "point" here is not an experimental run: it is any
location :math:`\mathbf{x}` in the factor region, and once the design has fixed :math:`\mathbf{M}`
we can evaluate the SPV there by simply plugging :math:`\mathbf{x}` into the formula, with no data
and no experiment required. The whole plot is a property of the design's geometry alone.

So we sample the region. Scatter a large number of locations, tens of thousands of them (the figure
below uses 80,000), uniformly at random across the coded factor region: for :math:`k` factors that
means drawing each coordinate independently and uniformly on :math:`[-1, +1]`, so the points fill
the cube evenly. One point is easy to miss: uniform random sampling almost never lands exactly on a
corner of the cube, yet the prediction variance is usually largest at a vertex, where the G-optimal
worst case sits. Add the :math:`2^k` extreme vertices back to the sampled set explicitly, so the
worst-case (right-hand) tail of the curve is represented and the region is covered fairly. At every
one of those locations we evaluate the SPV formula. We now hold tens of thousands of SPV values, one
per sampled location, a dense picture of how precisely the fitted model would predict across the
entire region.

Finally we turn that cloud of numbers into a curve. Sort the SPV values from smallest to largest.
The :math:`i`-th value in the sorted list is plotted at horizontal position
:math:`f = i / (\text{number of points})`, and its height is the SPV itself. The horizontal axis is
therefore just the running fraction (percentiles), and the curve is the empirical cumulative
distribution of SPV over the region: with enough points it converges to the true distribution.

The horizontal axis is the part that confuses people on first sight: it is **not** a
factor axis. A point at horizontal position :math:`f` means "a fraction :math:`f` of the
design region is predicted at least this well (this SPV or lower)." So :math:`f = 0.5` is
the median SPV, and :math:`f = 1.0` is the single worst point in the region. Because the
values are sorted, the curve only rises: the familiar gently-rising-then-steepening
shape. What to read off it:

    *   the **left end** (:math:`f \to 0`): the best-predicted regions, usually near the
        centre;
    *   the **median** (:math:`f = 0.5`): the typical precision you will experience;
    *   the **right end** (:math:`f \to 1`): the worst SPV in the region, which is the
        G-optimal value, usually at a corner;
    *   the **overall height**: lower is more precise everywhere, and the area under the
        curve is essentially the V-/I-optimal (average) value;
    *   the **flatness**: a flat curve means uniform precision across the whole region,
        which is the response-surface ideal: you predict equally well everywhere. A
        curve that ramps up sharply at the right predicts well in the middle but poorly
        at the edges.

In short, you are looking for **low and flat**, and when comparing two designs, for which
curve sits underneath and which is flatter.

The figure below compares two designs in four factors on the
main-effects-plus-quadratic model: a nine-run :ref:`definitive screening design
<DOE-definitive-screening-designs>` and a thirteen-run *orthogonal minimally aliased
response surface* (OMARS) design that spends its four extra runs to buy two estimable
two-factor interactions. OMARS designs are a recent generalization of the definitive
screening design: they keep the main effects orthogonal to every second-order term while
trading a handful of runs for interaction estimability, and the definitive screening
designs are themselves a special case within that family.

The definitive screening design comes straight from ``process_improve``; the OMARS design
has no generator in the library, so it is given explicitly. The helpers defined here, the
model expansion, the prediction variance and the FDS curve, are reused for the omnibus
comparison further down.

.. code-block:: python

	import itertools
	import numpy as np
	import plotly.graph_objects as go
	from process_improve.experiments import Factor, generate_design

	def model_matrix(design):
	    """Main-effects-plus-pure-quadratics expansion [1 | x_i | x_i^2]."""
	    d = np.asarray(design, float)
	    k = d.shape[1]
	    return np.column_stack([np.ones(len(d))] + [d[:, i] for i in range(k)]
	                           + [d[:, i] ** 2 for i in range(k)])

	def prediction_variance(design, points):
	    """x'(X'X)^-1 x at each row of `points`, in sigma^2 units."""
	    xtx_inv = np.linalg.inv(model_matrix(design).T @ model_matrix(design))
	    P = model_matrix(points)
	    return np.einsum("ij,jk,ik->i", P, xtx_inv, P)

	def fds_curve(design, points, fractions, scaled=False):
	    """Sorted prediction variance as a fraction-of-design-space curve."""
	    pv = np.sort(prediction_variance(design, points))
	    if scaled:
	        pv = pv * len(np.asarray(design))
	    return np.quantile(pv, fractions)

	# 4-factor DSD (9 runs) from process_improve; the 13-run OMARS is given explicitly.
	dsd4 = np.asarray(generate_design([Factor(name=c, low=-1, high=1) for c in "ABCD"],
	                                  design_type="dsd").design[list("ABCD")], float)
	omars4 = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, -1, -1], [1, -1, -1, 0],
	                   [1, 0, 1, -1], [1, 1, 0, 1], [0, 0, 0, -1], [0, 0, -1, 0],
	                   [0, -1, 1, 1], [-1, 1, 1, 0], [-1, 0, -1, 1], [-1, -1, 0, -1],
	                   [0, 0, 0, 0]], float)

	# Sample the region uniformly and add the 2^4 vertices, where the worst case can sit.
	rng = np.random.default_rng(1)
	region4 = np.vstack([rng.uniform(-1, 1, size=(80_000, 4)),
	                     np.array(list(itertools.product([-1, 1], repeat=4)), float)])
	fraction_grid = np.linspace(0, 1, 200)

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=fraction_grid,
	                         y=fds_curve(dsd4, region4, fraction_grid, scaled=True),
	                         name="DSD (9 runs)"))
	fig.add_trace(go.Scatter(x=fraction_grid,
	                         y=fds_curve(omars4, region4, fraction_grid, scaled=True),
	                         name="OMARS (13 runs)"))
	fig.update_layout(xaxis_title="Fraction of design space",
	                  yaxis_title="Scaled prediction variance, SPV")
	fig.show()

.. figure:: ../figures/doe/fds-plot-dsd-vs-omars.png
    :align: center
    :width: 750px
    :alt: fds-plot-dsd-vs-omars.py

    FDS plot for a nine-run definitive screening design and a thirteen-run OMARS design,
    both in four factors on the main-effects-plus-quadratic model. The curves cross near a
    fraction of 0.75: the larger design predicts better on average but worse at the extreme
    corners.

The thirteen-run OMARS curve sits *below* the nine-run DSD curve for roughly the first three
quarters of the region: it has lower best-case, median, and average prediction variance.
But the two curves **cross** near :math:`f \approx 0.75`, and the thirteen-run OMARS curve then
rises well above: its worst-case prediction variance is noticeably higher. This crossing is the
practical tension between V- (average) and G- (worst-case) optimality, and it has a physical cause:
the larger design here places fewer runs out near the edge of the region, so prediction there
behaves like mild extrapolation. The reading is concrete: if you care about prediction on
average across the space (typical optimization work), prefer the larger design; if you must
predict reliably even in the worst spot, the flatter nine-run DSD curve is the safer choice.

One detail of method is worth stating, because it is easy to get wrong. The worst-case figure
:math:`G` is a maximum over the whole design region, and that maximum can sit exactly at an extreme
corner (a vertex of the :math:`[-1, 1]` cube), where random interior sampling rarely lands. The
evaluation here therefore includes the cube vertices explicitly alongside the interior sample. Doing
so lifts the nine-run DSD's :math:`G` from :math:`8.98` to :math:`9.00`, a maximum that turns out to
sit precisely at a corner, and leaves the thirteen-run OMARS value at :math:`12.50` because its
worst case lies in the interior. The shift is tiny, so it changes no conclusion here, but including
the extreme points is the correct procedure, and the omnibus comparison below relies on it.

Separability is not the same as precision
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The optimality criteria and the FDS plot all speak to *precision*. They are silent on the
other question, *separability*, which is governed by the off-diagonal structure of
:math:`\mathbf{M}`: how correlated the effects are with one another. The correlation between
two model-term columns, :math:`\mathbf{c}_a` and :math:`\mathbf{c}_b`, is just the cosine of
the angle between them once each has been centred:

.. math::

    r_{ab} = \frac{\widetilde{\mathbf{c}}_a^{\,T} \widetilde{\mathbf{c}}_b}
                  {\|\widetilde{\mathbf{c}}_a\| \, \|\widetilde{\mathbf{c}}_b\|}

where :math:`\widetilde{\mathbf{c}}` is the column after subtracting the part explained by the
intercept and the main effects. This residualizing step matters because the quadratic columns
:math:`x_i^2` have a positive mean that would otherwise inflate every correlation; removing the
intercept and main-effect content leaves only the genuine entanglement *between* the
second-order terms. (For a design whose main effects are already orthogonal to the second-order
terms, the definitive screening designs and their generalizations being the prime example, the
main-effect part is essentially zero and only the centring does any work.)

We report the *absolute* value of :math:`r` because its sign is an artefact of how the factor
levels happen to be coded: flip the direction of one factor and the sign of every term
containing it flips with it. The magnitude is the coding-invariant quantity, and it is what
governs separability. A value of :math:`|r| = 0` means the two effects are orthogonal and can be
estimated independently; :math:`|r| = 1` means they are the same column and cannot be told apart
at all. Two summaries are useful: the **maximum** :math:`|r|` over all pairs of second-order
effects (the quadratics and two-factor interactions, which is where a screening design's
entanglement lives) is the single tightest confounding anywhere in the design (the worst case you
would have to defend), while the **mean** :math:`|r|` is the overall level of entanglement. In the
comparison table, the definitive screening design has a worst-pair value of :math:`0.707` (a
structural hallmark of DSDs, and a confounding between two of its second-order effects), which the
thirteen-run OMARS design improves to :math:`0.570`; the mean values, :math:`0.322`
against :math:`0.307`, are much closer, telling us the extra runs help most with the *worst* pair
rather than with the average.

It is essential to treat separability and precision as *two* axes, because a design can be
excellent on one and poor on the other. A one-factor-at-a-time design, for instance, has
almost no correlation between its effects (good separability) and yet very poor precision
(its information is spread thinly, giving a low determinant and high prediction variance).
Ranking designs on any single number (including a correlation summary) will eventually
recommend something you would never want to run. Look at both axes.

.. _DOE-variance-inflation-factors:

.. index::
    pair: variance inflation factor; experiments
    see: VIF; variance inflation factor

Variance inflation factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The correlation :math:`r` above is a *pairwise* measure. Its multivariate cousin, which asks how
much a coefficient suffers from its entanglement with *all* the other terms at once, is the
:index:`variance inflation factor <pair: variance inflation factor; experiments>` (VIF). For term
:math:`j`,

.. math::

    \text{VIF}_j = \frac{1}{1 - R_j^2}

where :math:`R_j^2` is the coefficient of determination from regressing column :math:`j` of the
model matrix on all of the other columns. Equivalently, :math:`\text{VIF}_j` is the :math:`j`-th
diagonal element of the inverse of the correlation matrix of the model terms. It is the factor by
which the variance of :math:`b_j` is inflated relative to a perfectly orthogonal design:

.. math::

    \text{Var}(b_j) = \text{VIF}_j \cdot \frac{\sigma^2}{S_{jj}}

with :math:`S_{jj}` the corrected sum of squares of column :math:`j`. In an orthogonal design every
:math:`R_j^2 = 0`, so every :math:`\text{VIF}_j = 1`: the ideal. A value of 4 means the standard
error of that coefficient is doubled (:math:`\sqrt{4}`) by the correlation; a common rule of thumb
raises a flag past 5, and a serious one past 10.

The link to :math:`r` is direct: if a term were correlated with just one other term at level
:math:`r`, its VIF would be :math:`1/(1 - r^2)`. The VIF generalizes this to the joint effect of
every other term, and is computed on whichever model you actually intend to fit.

In the comparison table below, both summaries are reported for the main-effects-and-quadratic
model. The definitive screening design shows :math:`\text{VIF} = 1.0` throughout: on that model its
terms are mutually orthogonal. (This is not in tension with the worst-pair :math:`|r| = 0.707`
quoted above: that correlation involves the two-factor interactions, which this model leaves out.
Restricted to the main effects and quadratics, the DSD really is orthogonal.) The thirteen-run
OMARS design carries a maximum VIF of :math:`1.18`
and a mean of
:math:`1.08`, which inflates the worst standard error by only :math:`\sqrt{1.18} \approx 1.09`,
about nine percent. That is a mild and entirely acceptable price for the residual degrees of freedom
and the interaction estimates that the extra runs provide.

.. _DOE-alias-bias:

Bias from the terms left out: the alias matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The variance inflation factor measures entanglement *among the terms we fit*. A separate
question sits underneath the whole comparison: the model we have chosen leaves the
two-factor interactions out, and if any of them is not in fact zero, leaving it out pushes
its effect onto the coefficients we do estimate. How much, and onto which ones, is read
from the alias matrix.

Split the model terms into the ones we keep and the ones we drop. Let :math:`\mathbf{X}_1`
hold the eleven fitted columns (the intercept, the five linear terms, and the five pure
quadratics) and :math:`\mathbf{X}_2` hold the ten two-factor interaction columns
:math:`x_i x_j` left out. If the true response contains those interactions with
coefficients :math:`\boldsymbol{\beta}_2`, the least-squares estimates of the fitted
coefficients are biased by a fixed, design-dependent amount:

.. math::

    E[\mathbf{b}_1] = \boldsymbol{\beta}_1 + \mathbf{A}\,\boldsymbol{\beta}_2,
    \qquad
    \mathbf{A} = (\mathbf{X}_1^T\mathbf{X}_1)^{-1}\mathbf{X}_1^T\mathbf{X}_2

Each entry of the alias matrix :math:`\mathbf{A}` is the amount by which one omitted
interaction shifts one fitted coefficient: an entry of zero leaves that coefficient
untouched, an entry of one adds a full unit of the interaction to it. This is the same kind
of entanglement the VIF describes, turned outward. The VIF measures overlap among the terms
in the model; the alias matrix measures overlap between those terms and the terms the model
omits.

The two screening-oriented designs are built to control the rows of :math:`\mathbf{A}` that
matter most. A definitive screening design and an OMARS design keep every main effect
orthogonal to every second-order term, so the main-effect rows of :math:`\mathbf{A}` are
exactly zero: interactions that are present but omitted do not bias the estimated main
effects. That is what *minimally aliased* names. The price is carried by the quadratics,
whose rows are not zero. The omnibus comparison below reports the largest absolute entry of
:math:`\mathbf{A}` for each design, so this bias sits in the same table as the variance it
trades against.

.. _DOE-statistical-power:

.. index::
    pair: power; experiments
    pair: residual degrees of freedom; experiments
    pair: effect size; experiments

Statistical power
~~~~~~~~~~~~~~~~~~~~~

Everything so far describes how *precisely* a design estimates. Power asks the question the
experimenter actually cares about: if an effect is really there, how likely are we to detect it? We
are testing :math:`H_0\!: \beta_j = 0` against the alternative that :math:`\beta_j` equals some
effect size :math:`\delta` we consider practically important. Under that alternative the usual
:math:`t`- or :math:`F`-test statistic is no longer central; it follows a *non-central* distribution
whose non-centrality parameter is

.. math::

    \lambda = \frac{\delta^2}{\text{Var}(b_j)} = \frac{\delta^2}{\sigma^2\, c_{jj}},
    \qquad c_{jj} = \left[(\mathbf{X}^T\mathbf{X})^{-1}\right]_{jj}

The power is the probability that the statistic clears its critical value under this non-central
distribution, :math:`\text{power} = P\!\left(F_{1,\nu} > F_{\text{crit}} \mid \lambda\right)`, where
:math:`\nu` is the residual degrees of freedom. Anything that improves precision (a larger
:math:`1/c_{jj}`, i.e. more information about that term) raises :math:`\lambda` and therefore the
power, for a fixed effect size and significance level.

Two consequences deserve to be stated plainly. First, **power requires residual degrees of
freedom**: the non-central distribution needs an estimate of :math:`\sigma^2`, and a saturated
design with :math:`\nu = 0` supplies none. This is exactly why the definitive screening design's
power entries in the comparison table below are marked "n/a": with nine runs and nine terms in the
main-effects-and-quadratic model it has nothing left over to estimate the noise, so no test can be
run at all. The four extra runs of the thirteen-run OMARS design buy :math:`\nu = 4`, and with
them the ability to test.

Second, power is always quoted *for a stated effect size and* :math:`\alpha`. The table's values
assume an effect of one noise standard deviation (:math:`\delta = \sigma`) at :math:`\alpha = 0.05`.
Read that way, the thirteen-run OMARS design has a :math:`0.46` chance of flagging a true one-sigma
main effect as significant, but only :math:`0.25` for a quadratic of the same size. The gap is
expected:
quadratic effects are estimated with larger variance (we saw this in the worked example, where
:math:`\text{Var}(b_2)` was the largest of the three), so they are intrinsically harder to detect. A
screening study that must catch curvature will need either more runs or a larger assumed effect
size.

.. _DOE-design-comparison-table:

Putting the metrics side by side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collecting every measure we have defined into one place, here are the two designs from the FDS plot,
a nine-run definitive screening design and the thirteen-run OMARS design, evaluated on the
four-factor main-effects-and-quadratic model.

.. list-table:: Comparing the nine-run DSD with the thirteen-run OMARS design.
    :header-rows: 1
    :widths: 48 26 26

    *   - metric (and preferred direction)
        - DSD, 9 runs, 4 factors
        - OMARS, 13 runs, 4 factors
    *   - D-efficiency (higher is better)
        - 42.8 %
        - 39.0 %
    *   - :math:`A`, summed coefficient variance (lower)
        - 3.67
        - 2.52
    *   - :math:`I`, average SPV (lower)
        - 6.59
        - 6.19
    *   - :math:`G`, maximum SPV (lower)
        - 9.00
        - 12.50
    *   - maximum :math:`|r|` (lower)
        - 0.707
        - 0.570
    *   - mean :math:`|r|` (lower)
        - 0.322
        - 0.307
    *   - maximum VIF (lower)
        - 1.00
        - 1.18
    *   - mean VIF (lower)
        - 1.00
        - 1.08
    *   - residual degrees of freedom (higher)
        - 0
        - 4
    *   - power, main effect at :math:`\delta = \sigma` (higher)
        - n/a
        - 0.46
    *   - power, quadratic at :math:`\delta = \sigma` (higher)
        - n/a
        - 0.25
    *   - two-factor interactions estimable (higher)
        - 0
        - 2

No design wins every row, which is the entire point. The thirteen-run OMARS design is better on
average coefficient variance, average prediction, both correlation summaries, and is the only one
of the two
that can estimate interactions or test anything at all; the nine-run DSD holds a higher
D-efficiency and a lower worst-case prediction variance :math:`G`. Read the D-efficiency and the
per-run figures with care, though: as the dilemma table showed, these quantities shift with the
number of runs, so a head-to-head on :math:`D` across a nine-run DSD and a thirteen-run OMARS design
is not a
like-for-like comparison. The reading that carries weight leans on the quantities that carry real
meaning here,
separability (:math:`|r|`, VIF), prediction (:math:`I`, :math:`G`), and the ability to test at all
(residual degrees of freedom), and lets the purpose of the study break the ties.

.. _DOE-omnibus-comparison:

An omnibus comparison across design families
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two-design table makes its point on a narrow contest. Widen it now to the six families a
practitioner would actually shortlist for **five** factors on the same
main-effects-and-quadratic model (eleven terms: an intercept, five linear, and five pure
quadratic, with no two-factor interactions): a full :math:`2^5` factorial, a resolution-V
:math:`2^{5-1}` fractional factorial, a :ref:`central composite design <DOE_central_composite_designs>`,
a :ref:`Box-Behnken design <DOE-box-behnken-designs>`, a :ref:`definitive screening design
<DOE-definitive-screening-designs>`, and an :ref:`OMARS design <DOE-omars-designs>`. The run
counts differ, and we do not pad them to match: comparing designs at their natural sizes is the
whole point. Every design here is confined to the coded range :math:`[-1, 1]` on each factor, so
the contest is like-for-like on one fixed experimental region. The fuller second-order story, with
all the two-factor interactions, is where strong OMARS and composite designs really compete; the
script that backs this section builds that model too, but the comparison below holds to
main-effects-and-quadratics so it lines up with the rest of the chapter. Holding the
two-factor interactions out is an assumption: if they are in fact present, they bias the
eleven estimated coefficients by the :ref:`alias matrix <DOE-alias-bias>`, and the table
below records how large that bias can be for each design.

Start with the question that decides whether a design belongs in the contest at all: can it even
fit the model?

.. list-table:: Which designs can fit the five-factor main-effects-and-quadratic model.
    :header-rows: 1
    :widths: 34 12 22 32

    *   - design (5 factors)
        - runs
        - fits the 11-term model?
        - residual degrees of freedom
    *   - full factorial, :math:`2^5` + 2 centre
        - 34
        - no (rank 7)
        - 27, reduced model only
    *   - fractional, :math:`2^{5-1}` + 2 centre
        - 18
        - no (rank 7)
        - 11, reduced model only
    *   - CCD, face-centred
        - 32
        - yes
        - 21
    *   - Box-Behnken
        - 46
        - yes
        - 35
    *   - DSD
        - 13
        - yes
        - 2
    *   - OMARS
        - 25
        - yes
        - 14

Both two-level factorials fail outright, and adding centre points does not rescue them. At two
levels every :math:`x_i^2` column equals 1, and at the centre it equals 0, so all five quadratic
columns are *identical*: the eleven-term model collapses to rank 7 (the intercept, five linear
terms, and a single lumped curvature direction). The centre runs still earn their place, they
supply an estimate of :math:`\sigma^2`, a few residual degrees of freedom, a check on
between-run drift, and a one-degree-of-freedom test for *overall* curvature, but they cannot tell
the five quadratics apart. That single curvature signal is precisely the cue to augment the
factorial with axial runs, which is how the face-centred composite design in the same table is
born. The four remaining designs are full rank and carry the comparison from here.

**Lead with power, because it is what the experiment is for.** The figure below reads off the four
designs' ability to flag a true effect of one noise standard deviation
(:math:`\delta = \sigma`) at :math:`\alpha = 0.05`.

The four response-surface designs are built once here and reused for the table and the FDS
panels that follow. ``process_improve`` builds the Box-Behnken design and the DSD directly,
and builds the face-centred CCD on a resolution-V half-fraction cube with ``cube="fractional"``
(the standard five-factor CCD; the library's default cube is the full factorial). The 25-run
OMARS design has no library generator, so it is two permuted conference-matrix foldovers. The
power comes from ``evaluate_design``, given the eleven-term model as an explicit formula so
the library scores exactly this model and not the full second-order one:

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from process_improve.experiments import Factor, evaluate_design, generate_design

	def conference_matrix_order6():
	    """Order-6 conference matrix (C C' = 5 I) from the quadratic residues of GF(5):
	    the backbone of definitive screening and OMARS designs."""
	    q = 5
	    residues = {(a * a) % q for a in range(1, q)}
	    chi = [0] + [1 if a in residues else -1 for a in range(1, q)]
	    c = np.zeros((6, 6))
	    for i in range(1, 6):
	        c[0, i] = c[i, 0] = 1
	    for i in range(q):
	        for j in range(q):
	            if i != j:
	                c[1 + i, 1 + j] = chi[(j - i) % q]
	    return c

	names = list("ABCDE")
	factors = [Factor(name=c, low=-1, high=1) for c in names]
	model = " + ".join(names + [f"I({c}**2)" for c in names])   # 11 terms, no interactions

	def coded(result):
	    return np.asarray(result.design[names], float)

	bbd = coded(generate_design(factors, "box_behnken", center_points=6))
	dsd = coded(generate_design(factors, "dsd"))
	ccd = coded(generate_design(factors, "ccd", cube="fractional",
	                            alpha="face_centered", center_points=6))
	cm = conference_matrix_order6()[:, :5]
	cm2 = cm[:, [2, 4, 1, 3, 0]]
	omars = np.vstack([cm, -cm, cm2, -cm2, np.zeros((1, 5))])
	designs = {"Box-Behnken": bbd, "CCD": ccd, "OMARS": omars, "DSD": dsd}

	def power(design):
	    df = pd.DataFrame(np.asarray(design), columns=names)
	    p = evaluate_design(df, model=model, metric="power",
	                        effect_size=1.0, sigma=1.0)["power"]
	    return p["A"], p["I(A ** 2)"]          # one main effect, one pure quadratic

	power_main = [power(d)[0] for d in designs.values()]
	power_quad = [power(d)[1] for d in designs.values()]
	fig = go.Figure([go.Bar(name="main effect", x=list(designs), y=power_main),
	                 go.Bar(name="quadratic effect", x=list(designs), y=power_quad)])
	fig.update_layout(barmode="group",
	                  yaxis_title="Power (delta = sigma, alpha = 0.05)")
	fig.show()

.. figure:: ../figures/doe/power-comparison-six-designs.png
    :align: center
    :width: 750px
    :alt: power-comparison-six-designs.py

    Power to detect a one-sigma main effect and a one-sigma quadratic effect, for the four
    response-surface designs on the five-factor model. More runs buy more power, and curvature is
    the harder target.

The thirteen-run DSD is visibly underpowered: a :math:`0.42` chance on a one-sigma main effect and
only :math:`0.15` on a quadratic of the same size. The run-richer designs all clear :math:`0.97`
on main effects, and the Box-Behnken design, the largest at forty-six runs, is the only one with a
strong :math:`0.82` chance on curvature. Power rewards the larger designs, which is the practical
reading and exactly what an efficiency score that normalizes out the number of runs would have
hidden.

One caveat in the definitive screening design's favour, since its numbers look stark. A DSD is
built on an assumption of effect sparsity, not for this saturated eleven-term fit: its design
intent (Jones and Nachtsheim, 2011) is to project onto the few factors that turn out to be active
and estimate their quadratics cleanly, rather than to test all five quadratics at once on thirteen
runs. Held to the full model here it is being asked for more than it was built to give; the
comparison keeps it on the same model as the others to make that trade-off visible, not to mark it
a poor design.

.. list-table:: Quality metrics for the four response-surface designs (five factors).
    :header-rows: 1
    :widths: 40 15 15 15 15

    *   - Metric (and preferred direction)
        - BBD, 46 runs
        - CCD, 32 runs
        - OMARS, 25 runs
        - DSD, 13 runs
    *   - Power, main effect at :math:`\delta = \sigma` (higher)
        - 0.97
        - 0.98
        - 0.99
        - 0.42
    *   - Power, quadratic at :math:`\delta = \sigma` (higher)
        - 0.82
        - 0.32
        - 0.46
        - 0.15
    *   - Average prediction variance, :math:`\sigma^2` units (lower)
        - 0.18
        - 0.31
        - 0.51
        - 0.71
    *   - Maximum prediction variance, :math:`\sigma^2` units (lower)
        - 0.84
        - 0.77
        - 0.84
        - 1.05
    *   - Summed coefficient variance :math:`A` (lower)
        - 1.05
        - 2.39
        - 2.34
        - 3.70
    *   - :math:`E`, smallest eigenvalue of :math:`\mathbf{X}^T\mathbf{X}` (higher)
        - 2.54
        - 2.00
        - 0.93
        - 0.85
    *   - Maximum :math:`|r|` among model terms (lower)
        - 0.15
        - 0.75
        - 0.00
        - 0.13
    *   - Maximum VIF (lower)
        - 1.20
        - 3.20
        - 1.00
        - 1.05
    *   - Maximum alias :math:`|\mathbf{A}|`, omitted interactions (lower)
        - 0.00
        - 0.00
        - 1.00
        - 1.09
    *   - D-optimal information :math:`|\mathbf{X}^T\mathbf{X}|^{1/p}` (higher)
        - 14.0
        - 8.97
        - 9.82
        - 5.19
    *   - D-efficiency, per run (higher, but see note)
        - 30.5%
        - 28.0%
        - 39.3%
        - 39.9%

Let's focus on the last row first. Recall what D-efficiency measures: it takes the determinant of
the information matrix :math:`\mathbf{X}^T\mathbf{X}`, raises it to the power :math:`1/p` to put it
on a per-coefficient scale, and then divides by the run count :math:`N`, reported as a percentage.
Dividing by :math:`N` measures information *per experiment*, not total information, and that single
normalisation flips the ranking. One more point on the scale: for this absolute percentage, 100%
would be a hypothetical orthogonal design (:math:`|\mathbf{X}^T\mathbf{X}| = N^p`), not the
D-optimal design. That ceiling is out of reach for a model with pure-quadratic terms on the coded
cube, since the squared columns cannot be made orthogonal to the intercept, which is why even the
strongest designs here sit near 30 to 40%. (A separate *relative* D-efficiency convention instead
takes the D-optimal design as 100%, so it is worth checking which one a given package reports.)

The two D rows make this concrete. The **unscaled** D-optimal information
:math:`|\mathbf{X}^T\mathbf{X}|^{1/p}` ranks the designs as every other row does, the
Box-Behnken design highest at :math:`14.0` and the thirteen-run DSD lowest at :math:`5.19`. Divide
that same determinant through by the run count and the order reverses in the row directly beneath
it: per-run D-efficiency ranks the small DSD and OMARS designs *highest*, at :math:`39.9\,\%` and
:math:`39.3\,\%`, above the Box-Behnken and composite designs that predict better, test better, and
detect curvature far better. The number is not wrong; it is answering a different question. Dividing
by the run count rewards a design for spending few experiments, so a small design comes out ahead
even when it tests and predicts worse. Scaled prediction variance carries the same concern, and for
the same reason it has been questioned in the design literature (Anderson-Cook, Borror and
Montgomery, 2009, and its published discussion; Goos and Núñez Ares, 2025).

The quantities in real units, the **unscaled prediction variance** in :math:`\sigma^2`, the summed
coefficient variance :math:`A`, and the power, all reward the larger Box-Behnken design, which is
the reading that matches what the experiments can actually deliver.

The alias row makes the cost of the reduced model explicit. The model fits no two-factor
interactions, so any that are present bias the coefficients we keep, by the
:ref:`alias matrix <DOE-alias-bias>`. The Box-Behnken and composite designs hold that bias
at zero on this model (:math:`|\mathbf{A}| = 0`): their quadratics are balanced against the
omitted interactions, so a present interaction leaves the fitted coefficients untouched. The
definitive screening and OMARS designs instead protect the main effects, whose alias is
zero, but let a present interaction shift a quadratic by as much as a full unit. Whether that
matters is a question about the system rather than the design: it is the price of setting the
interactions aside, and it is why a follow-up design is run once a screening study has
flagged the active factors.

It is worth being clear about what the table compares. The model is already settled: we have
committed to the eleven-term main-effects-plus-quadratics model and are comparing point-placement
strategies, the designs, for estimating its coefficients and predicting from it. The criteria split
along exactly that line. For *estimation*, the determinant criterion :math:`D` (unscaled and per
run) and the summed coefficient variance :math:`A` summarise the whole parameter set, and
:math:`E`-optimality adds the worst single coefficient direction, the smallest eigenvalue of
:math:`\mathbf{X}^T\mathbf{X}`. It is the coefficient-space counterpart to the maximum prediction
variance, and it agrees with :math:`A` and the prediction rows: the Box-Behnken design first, the
DSD last. For *prediction*, the average and maximum prediction variance are the working analogues of
:math:`I`- and :math:`G`-optimality. A model-discrimination criterion such as :math:`T`-optimality
has no place here: it is defined only against a second, rival model, measuring the lack of fit of
one against the other, so once a single model is settled there is no rival curve to be far from.

Two design-specific cautions sit alongside this. The composite design here is **face-centred**
(axial runs at
:math:`\pm 1`) so that it stays on the same :math:`[-1, 1]` region as the others; a rotatable CCD
would place those runs at :math:`\pm 2`, scoring much better only by quietly spending experiments
on a region twice as wide, which is not a fair comparison and explains the face-centred design's
weaker curvature precision (its :math:`|r| = 0.75` and VIF of :math:`3.20`). And the families
overlap: a composite design built on a resolution-V fraction is itself a strong OMARS design, while
a definitive screening design is a special case within the OMARS family, so think of these as a
spectrum.

The two views of prediction variance are worth seeing side by side, because the scaling by run
count is exactly what leaves out the cost of running too few experiments.

Reusing the four designs and the ``fds_curve`` helper, the two panels are the same curves
on the two scales:

.. code-block:: python

	import itertools
	import numpy as np
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	# Reuses fds_curve (from the DSD-vs-OMARS block) and the designs dict (previous block).
	region5 = np.vstack([np.random.default_rng(1).uniform(-1, 1, size=(120_000, 5)),
	                     np.array(list(itertools.product([-1, 1], repeat=5)), float)])
	fds_fraction = np.linspace(0, 1, 200)

	fig = make_subplots(rows=1, cols=2,
	                    subplot_titles=("Scaled (per run)", "Unscaled (sigma^2 units)"))
	for label, d in designs.items():
	    fig.add_trace(go.Scatter(x=fds_fraction, y=fds_curve(d, region5, fds_fraction, scaled=True),
	                             name=label), row=1, col=1)
	    fig.add_trace(go.Scatter(x=fds_fraction, y=fds_curve(d, region5, fds_fraction, scaled=False),
	                             name=label, showlegend=False), row=1, col=2)
	fig.update_yaxes(title_text="Scaled prediction variance", row=1, col=1)
	fig.update_yaxes(title_text="Prediction variance / sigma^2", row=1, col=2)
	fig.show()

.. figure:: ../figures/doe/fds-plot-six-designs.png
    :align: center
    :width: 750px
    :alt: fds-plot-six-designs.py

    FDS curves for the four response-surface designs, scaled (left) and unscaled (right). Scaling
    by the run count lowers the small DSD's curve; in real :math:`\sigma^2` units the DSD curve is
    the highest and the larger Box-Behnken design's is the lowest.

Within either panel the rule from before still holds: a low and flat curve is what you want, and the
right tail (anchored at the cube vertices, where the maximum prediction variance usually lives) shows
the worst case. The two panels differ only in how they put the designs on a common footing. The left
panel is scaled, normalized by the number of runs, so it compares the designs per experiment; on
that footing the thirteen-run DSD curve sits among the rest. The right panel is unscaled, in real
:math:`\sigma^2` units, so it compares the variance actually obtained at the bench; there the DSD
curve is the highest and the forty-six-run Box-Behnken the lowest. The two views answer different
questions, and they diverge because adding runs lowers the variance you obtain while leaving the
per-run figure roughly fixed.

A checklist for choosing among designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let the purpose of the experiment set the priorities.

    *   **Screening** (which factors and effects matter): prioritize the power to detect a
        main effect, keep the correlations among any terms you might promote into the model
        low, and insist on a few residual degrees of freedom so that you can actually test
        significance. A saturated design with zero residual degrees of freedom fits its own
        data exactly and leaves *nothing* to estimate :math:`\sigma^2` with: no standard
        errors, no tests, no power. Favour D-optimality here.

    *   **Optimization / response surfaces** (map the surface and find the optimum): lead with
        the FDS plot and I-optimality (the average prediction variance over the region), then
        quadratic estimability, then how the design
        behaves when projected onto the subset of factors that turn out to be active. Favour a
        design whose FDS curve is low and flat.

Two rules of thumb close the loop. First, use **D for estimation and I for prediction**;
they frequently disagree, so choose by what you will actually do with the model. Second,
**compare D-efficiency only between designs of the same number of runs**: across
different run counts it favours the smaller design, so judge larger-versus-smaller on
the quantities that carry real units: average coefficient variance, prediction variance, power,
and the number of residual degrees of freedom.

**Readings**

* Box, Hunter and Hunter, *Statistics for Experimenters*, 2nd edition, for the factorial and
  response-surface groundwork.
* Myers, Montgomery and Anderson-Cook, *Response Surface Methodology*, for prediction variance,
  the scaled prediction variance, and FDS plots.
* Anderson-Cook, Borror and Montgomery, "Response surface design evaluation and comparison",
  *Journal of Statistical Planning and Inference*, **139**, 629--641, 2009
  (`doi:10.1016/j.jspi.2008.04.004 <https://doi.org/10.1016/j.jspi.2008.04.004>`__), and its
  published discussion, for the fraction-of-design-space comparison and the case for judging
  designs on prediction variance.
* Goos and Núñez Ares, "Response to Letter to the Editor", *Technometrics*, **67**, 189--191, 2025
  (`doi:10.1080/00401706.2024.2379849 <https://doi.org/10.1080/00401706.2024.2379849>`__), on why
  absolute efficiencies and scaled prediction variance mislead when designs differ in run size, and
  why power and unscaled prediction variance are the comparisons that hold up.
* Goos and Jones, *Optimal Design of Experiments: A Case Study Approach*, for the
  information-matrix view of the optimality criteria.
* Jones and Nachtsheim, "A Class of Three-Level Designs for Definitive Screening in the Presence of
  Second-Order Effects", *Journal of Quality Technology*, **43**, 1--15, 2011
  (`doi:10.1080/00224065.2011.11917841 <https://doi.org/10.1080/00224065.2011.11917841>`__), for the
  effect-sparsity and projection rationale behind definitive screening designs.
* Núñez Ares and Goos, "Enumeration and Multicriteria Selection of Orthogonal Minimally Aliased
  Response Surface Designs", *Technometrics*, **62**, 21--36, 2020
  (`doi:10.1080/00401706.2018.1549103 <https://doi.org/10.1080/00401706.2018.1549103>`__), and the
  review by Goos, "OMARS designs for factor screening and response surface experimentation in one
  step", *WIREs Computational Statistics*, **17**, e70018, 2025
  (`doi:10.1002/wics.70018 <https://doi.org/10.1002/wics.70018>`__), for the OMARS family used in
  the comparison above.
