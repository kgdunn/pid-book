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
that summarise it. Both were introduced in the earlier section on
:ref:`optimal designs <DOE-optimal-and-omars-designs>`, so here we take
them as given. This subchapter shows how prediction variance is derived from
:math:`\mathbf{M}`, how to read a fraction-of-design-space plot, and how the separability, bias,
and power measures play out on one running comparison of two designs. The
:ref:`companion page <DOE-omnibus-comparison>` then widens that comparison across the standard
design families and closes with a checklist for choosing among them.

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
<https://github.com/kgdunn/process-improve>`_ (``pip install 'process-improve[all]'``, which
installs every optional extra). Of those extras, ``expt`` (the ``pyDOE3`` package) is needed for
the Box-Behnken and central composite designs on the :ref:`companion page
<DOE-omnibus-comparison>`, and ``ilp`` (the ``pulp`` integer-programming solver) for the
twenty-five-run OMARS design there. The four-factor, thirteen-run OMARS design used on this page
is small enough for ``generate_omars`` to find by exhaustive enumeration (every feasible design
of that size is listed and scored), so it needs neither.
Each block imports what it needs and reuses variables defined in the blocks before it, so paste
them in order. The prediction variance of the three-run quadratic design is a closed form:

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

    *   - Design
        - :math:`N`
        - :math:`\uparrow\ D=\det\mathbf{M}`
        - :math:`\downarrow\ A=\text{trace}\,\mathbf{M}^{-1}`
        - :math:`\uparrow\ E=\lambda_{\min}`
        - :math:`\downarrow\ G`
        - :math:`\downarrow\ I`
    *   - Base :math:`\{-1, 0, +1\}`
        - 3
        - 4
        - 3.00
        - 0.44
        - 1.0
        - 0.80
    *   - Base, all three runs repeated
        - 6
        - 32
        - 1.50
        - 0.88
        - 0.5
        - 0.40
    *   - Base + two centre points
        - 5
        - 12
        - 1.67
        - 1.00
        - 1.0
        - 0.44
    *   - Base + two points at :math:`\pm 1`
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

That is as far as a single factor can take us. The one-factor example has supplied the working
vocabulary: prediction variance, the :math:`D`, :math:`A`, :math:`E`, :math:`G`, and :math:`I`
criteria, and the per-run (SPV) scaling that stops sheer replication from masquerading as quality.
The rest of this subchapter puts that vocabulary to work on a single running comparison of two
realistic multi-factor designs, introduced in the next section.

.. _DOE-dsd-omars-comparison:

A running comparison: a DSD and an OMARS design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The running example for the rest of the subchapter is a pair of four-factor designs, both fitted on
the main-effects-plus-quadratic model: a nine-run :ref:`definitive screening design
<DOE-definitive-screening-designs>` and a thirteen-run *orthogonal minimally aliased response
surface* (OMARS) design that spends its four extra runs to buy two estimable two-factor
interactions. OMARS designs are a recent generalization of the definitive screening design: they
keep the main effects orthogonal to every second-order term while trading a handful of runs for
interaction estimability, and the definitive screening designs are themselves a special case within
that family.

As each new metric is introduced (the FDS reading, then separability, the variance inflation factor,
the alias bias, and power), it is read off these same two designs, and :ref:`a single summary table
<DOE-design-comparison-table>` collects every value at the end.

Both designs come straight from ``process_improve``: ``generate_design`` builds the nine-run
definitive screening design, and ``generate_omars`` builds the thirteen-run OMARS member directly
(the DSD is the minimal member of the same foldover family), each confirmed with the library's
``is_omars`` verifier. The ``fds`` helper defined here wraps ``evaluate_design``, which integrates
the prediction variance over the design region and returns both the FDS curve and the average and
worst-case values; the next section uses it to draw the plot.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from process_improve.experiments import Factor, evaluate_design, generate_design, generate_omars, is_omars

	def fds(design, model, *, n_samples, seed=1):
	    """Region prediction-variance summary from ``evaluate_design``: the FDS
	    curve (fraction of the design space vs prediction variance, scaled and
	    unscaled) together with the average and worst-case values. The 2**k cube
	    vertices, where the worst case usually sits, are included by default."""
	    cols = [chr(ord("A") + i) for i in range(np.shape(design)[1])]
	    df = pd.DataFrame(np.asarray(design, float), columns=cols)
	    return evaluate_design(df, model=model, metric="fds", n_samples=n_samples,
	                           random_seed=seed, fds_resolution=200)["fds"]

	# Both four-factor designs come from process_improve: the 9-run DSD and the
	# precision-optimal (A-optimal) 13-run OMARS member of the same foldover family,
	# the latter carrying two estimable two-factor interactions. is_omars confirms each.
	factors4 = [Factor(name=c, low=-1, high=1) for c in "ABCD"]
	dsd4 = np.asarray(generate_design(factors4, design_type="dsd").design[list("ABCD")], float)
	omars4 = np.asarray(generate_omars(factors4, n_runs=13, model="main_quadratic",
	                                   selection_criterion="a_optimal").design[list("ABCD")], float)
	assert is_omars(dsd4) and is_omars(omars4)
	model4 = " + ".join(list("ABCD") + [f"I({c}**2)" for c in "ABCD"])

.. _DOE-fds-plot:

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

Applying that recipe to the running example reuses ``dsd4``, ``omars4``, ``model4`` and the ``fds``
helper from the previous section:

.. code-block:: python

	fig = go.Figure()
	for design, label in [(dsd4, "DSD [n=9]"), (omars4, "OMARS [n=13]")]:
	    curve = fds(design, model4, n_samples=80_000)["curve"]
	    fig.add_trace(go.Scatter(x=curve["fraction"],
	                             y=curve["scaled_prediction_variance"], name=label))
	fig.update_layout(xaxis_title="Fraction of design space",
	                  yaxis_title="Scaled prediction variance, SPV")
	fig.show()

.. figure:: ../figures/doe/fds-plot-dsd-vs-omars.png
    :align: center
    :width: 750px
    :alt: fds-plot-dsd-vs-omars.py

    FDS plot for a nine-run definitive screening design and a thirteen-run OMARS design,
    both in four factors on the main-effects-plus-quadratic model. The curves cross near a
    fraction of 0.73: the larger design predicts better on average but worse at the extreme
    corners.

The thirteen-run OMARS curve sits *below* the nine-run DSD curve for roughly the first three
quarters of the region: it has lower best-case, median, and average prediction variance.
But the two curves **cross** near :math:`f \approx 0.73`, and the thirteen-run OMARS curve then
rises well above: its worst-case prediction variance is noticeably higher. This crossing is the
practical tension between V- (average) and G- (worst-case) optimality, and it has a physical cause:
the larger design here places fewer runs out near the edge of the region, so prediction there
behaves like mild extrapolation. The reading is concrete: if you care about prediction on
average across the space (typical optimization work), prefer the larger design; if you must
predict reliably even in the worst spot, the flatter nine-run DSD curve is the safer choice.

One detail of method is worth stating, because it is easy to get wrong. The worst-case figure
:math:`G` is a maximum over the whole design region, and that maximum can sit exactly at an extreme
corner (a vertex of the :math:`[-1, 1]` cube), where random interior sampling rarely lands.
``evaluate_design`` therefore adds the cube vertices to its interior sample by default (its
``include_vertices`` argument). Including them lifts the nine-run DSD's :math:`G` from :math:`8.98`
to :math:`9.00`, a maximum that turns out to sit precisely at a corner, and leaves the thirteen-run
OMARS value at :math:`12.50` because its worst case does not sit at a vertex. The shift is tiny,
so it changes no conclusion here, but including the extreme points is the correct procedure, and
the :ref:`omnibus comparison <DOE-omnibus-comparison>` relies on it.

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

where :math:`\widetilde{\mathbf{c}}` is the column after regressing out the intercept and the
main-effect columns, that is, the residual

.. math::

    \widetilde{\mathbf{c}} = \mathbf{c}
        - \mathbf{X}_0\,(\mathbf{X}_0^T \mathbf{X}_0)^{-1}\,\mathbf{X}_0^T\,\mathbf{c},
    \qquad \mathbf{X}_0 = [\,\mathbf{1} \;\; \mathbf{x}_1 \;\; \cdots \;\; \mathbf{x}_k\,]

with :math:`\mathbf{X}_0` holding the intercept column :math:`\mathbf{1}` and the :math:`k`
main-effect columns. Two distinct pieces are removed here. Subtracting the intercept removes the
column's mean (this is the *centring*), which matters because the quadratic columns :math:`x_i^2`
have a positive mean that would otherwise inflate every correlation. Subtracting the main-effect
columns then removes any linear trend the column shares with the factors. What is left is the
genuine entanglement *between* the second-order terms. For a design whose main effects are already
orthogonal to every second-order term (the definitive screening designs and their generalizations
being the prime example), the main-effect part is already zero, so there only the centring does any
work; in general both pieces are removed.

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
every other term, and is computed on whichever model you actually intend to fit. The quadratic
columns :math:`x_i^2` have a nonzero mean, but because each column is centered when the factor is
formed (the corrected sum of squares :math:`S_{jj}` above reflects the same centering), that mean
does not by itself inflate the VIF; only genuine correlation with the other fitted terms does.

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

Split the model terms into the ones we keep and the ones we drop. For this four-factor running
example, let :math:`\mathbf{X}_1` hold the nine fitted columns (the intercept, the four linear
terms, and the four pure quadratics) and :math:`\mathbf{X}_2` hold the six two-factor interaction
columns :math:`x_i x_j` left out. If the true response contains those interactions with
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
whose rows are not zero. The :ref:`omnibus comparison <DOE-omnibus-comparison>` reports the largest
absolute entry of :math:`\mathbf{A}` for each design, so this bias sits in the same table as the
variance it trades against.

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
Here :math:`\delta` is the coefficient itself, so for a linear main effect :math:`\delta = \sigma`
means the response shifts by :math:`2\sigma` across a factor's :math:`-1` to :math:`+1` range, a
signal-to-noise ratio of 2. That is the default several design packages (for example Stat-Ease
Design-Expert) use for power calculations, so the entries here are directly comparable to them; a
larger assumed effect would raise every entry in the power rows.
Read that way, the thirteen-run OMARS design has roughly a :math:`0.46` chance of flagging a true
one-sigma main effect as significant (its main effects are not all estimated with equal precision,
so the exact figure varies from factor to factor, and the table reports the weakest), and about
:math:`0.25` for a quadratic of the same size. The gap is
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

    *   - metric (arrow shows the preferred direction)
        - DSD [n=9], 4 factors
        - OMARS [n=13], 4 factors
    *   - :math:`\uparrow` D-efficiency
        - 42.8 %
        - 39.0 %
    *   - :math:`\downarrow\ A`, summed coefficient variance
        - 3.67
        - 2.52
    *   - :math:`\downarrow\ I`, average SPV
        - 6.59
        - 6.19
    *   - :math:`\downarrow\ G`, maximum SPV
        - 9.00
        - 12.50
    *   - :math:`\downarrow` maximum :math:`|r|`
        - 0.707
        - 0.570
    *   - :math:`\downarrow` mean :math:`|r|`
        - 0.322
        - 0.307
    *   - :math:`\downarrow` maximum VIF
        - 1.00
        - 1.18
    *   - :math:`\downarrow` mean VIF
        - 1.00
        - 1.08
    *   - :math:`\uparrow` residual degrees of freedom
        - 0
        - 4
    *   - :math:`\uparrow` power, main effect at :math:`\delta = \sigma`
        - n/a
        - 0.46
    *   - :math:`\uparrow` power, quadratic at :math:`\delta = \sigma`
        - n/a
        - 0.25
    *   - :math:`\uparrow` two-factor interactions estimable
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

Read this for the method, not for a verdict on the design types. The rows rank these two particular
designs on one model; they do not say that an OMARS design is in general better or worse than a
definitive screening design. The thirteen-run design here is one member of a large family: for a
given factor count the OMARS catalogue holds many designs of different run sizes and aliasing
trade-offs, so a different member would sit differently on every row. What transfers to the next
study is the procedure, reading precision, separability, and power off the information matrix, not
the ranking of any one design.

That is the running comparison in full. The :ref:`next page <DOE-omnibus-comparison>` widens it from
two designs to a shortlist of six, comparing the standard design families for five factors on the
same model, and closes with a checklist for choosing among them.
