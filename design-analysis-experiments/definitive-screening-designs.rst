.. _DOE-definitive-screening-designs:

Definitive screening designs (DSD): screen factors and detect curvature in one experiment
==========================================================================================

The :ref:`previous section <DOE-optimal-designs>` let a computer build a design to order, by
optimizing a criterion. This section turns to a structured, ready-made family that meets many of
the same needs without an optimization step: the definitive screening design.

The traditional way to run an investigation with many factors is in two phases. First you
*screen*: a two-level :ref:`fractional factorial <DOE-fractional-factorials>` or a
Plackett-Burman design with as few runs as possible, to find out which of the many factors
actually matter. Then, on the handful that survive, you run a separate *response surface*
experiment, a :ref:`central composite <DOE_central_composite_designs>` or Box-Behnken design,
to model the curvature and find an optimum. The logic is sound, but it has real friction. It
takes two rounds of experimentation, with the delay and overhead of stopping, analysing, and
restarting. The screening design is at two levels, so it cannot see curvature at all; you only
discover whether a factor bends the response in the second phase. And a low-resolution
screening design :ref:`aliases <DOE-design-resolution>` main effects with two-factor
interactions, so a large "main effect" may really be an interaction in disguise.

A :index:`definitive screening design <pair: definitive screening design; experiments>` (DSD),
introduced by Jones and Nachtsheim in 2011, collapses the two phases into one. It is a
three-level design, economical (about :math:`2k + 1` runs for :math:`k` factors), that screens
the main effects *and* lets you detect curvature, all from a single set of runs.

The foldover construction and its consequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The construction is a *foldover* of a conference matrix with a centre run added, a route to the DSD
due to Xiao, Lin, and Bai (2012). A conference
matrix :math:`\mathbf{C}` of order :math:`m` is an :math:`m \times m` matrix with zeros on the
diagonal and :math:`\pm 1` off it, whose columns are orthogonal:
:math:`\mathbf{C}^T\mathbf{C} = (m-1)\mathbf{I}`. The design stacks :math:`\mathbf{C}`, its
mirror image :math:`-\mathbf{C}`, and a row of zeros:

.. math::

    \mathbf{D} = \begin{bmatrix} \mathbf{C} \\ -\mathbf{C} \\ \mathbf{0} \end{bmatrix}

so that every factor is run at all three levels :math:`-1, 0, +1`.

The foldover is what gives the design its remarkable properties, and the reason is worth
understanding because it returns when we meet OMARS designs. Consider what happens when we
negate a run, flipping the sign of every factor at once, which is exactly what the
:math:`-\mathbf{C}` block does. A main effect, being linear in a single factor, reverses sign.
The intercept, a quadratic :math:`x_i^2`, and a two-factor interaction :math:`x_i x_j` (where
both factors flip together, so the product is unchanged) all stay exactly as they were. So when
a run is added to its negated mirror, every product between a main-effect column and a
second-order column cancels between the two halves, while the second-order columns reproduce
themselves identically. The consequences are:

    *   main effects are orthogonal to one another, and estimated as cleanly as in a two-level
        design;

    *   main effects are orthogonal to (unaliased with) *every* two-factor interaction and
        *every* quadratic effect, so a real interaction can never masquerade as a main effect;

    *   all :math:`k` quadratic effects are estimable, so curvature can be detected in every
        factor; and

    *   under effect sparsity (the common assumption that only a few of the many factors actually
        drive the response), a sufficiently large design has a further useful property. A three-factor
        full quadratic has ten parameters, so the design needs at least ten runs, a count the
        :math:`2k+1` runs already meet from :math:`k = 5`. Meeting the run count is necessary but not
        sufficient: Jones and Nachtsheim (2011) prove the stronger result that from six factors
        upward, restricted to *any* three of the factors, the runs form a design able to fit the full
        quadratic model in just those three factors. So if only a handful of factors turn out to matter, the same single set of runs
        supports a complete response-surface model in them. (A small DSD cannot do this: the
        nine-run, four-factor design used as the running example in
        :ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>` has fewer runs
        than that ten-parameter model requires.)

There is one limitation, and it comes from the very same mechanism. Folding cancels the
cross-products between the main effects and the second-order terms, but it does nothing to
separate the second-order terms from *one another*: a two-factor interaction column is identical
in :math:`\mathbf{C}` and in
:math:`-\mathbf{C}`. So the two-factor interactions remain correlated among themselves (and
partially with the quadratics), and you cannot estimate all of them cleanly at once. A DSD is
therefore at its best when only a few factors turn out to be active, so that only a few
second-order terms compete. That residual entanglement among the second-order effects is
precisely what the :ref:`next section, on OMARS designs <DOE-omars-designs>`, sets out to manage.

.. _DOE-dsd-worked-example:

A worked DSD: generating and reading the design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It helps to see a DSD as a concrete table of runs. The ``process_improve`` package builds one
from a list of factors: ask for the ``"dsd"`` design type and you get back the coded run matrix.
Here we take six continuous factors, :math:`A` through :math:`F`. Six factors give
:math:`2k + 1 = 13` runs; the centre run is part of the construction, so no extra centre points
are requested.

.. code-block:: python

    import numpy as np
    import plotly.graph_objects as go
    from process_improve.experiments import Factor, generate_design

    factors = [Factor(name=c, low=-1, high=1) for c in "ABCDEF"]   # six factors
    dsd = generate_design(factors, design_type="dsd", random_seed=42)
    print(dsd.n_runs, dsd.metadata["construction"])               # 13 paley_q=5

    # generate_design returns the runs in randomized execution order. Reorder them into
    # the construction pattern [C; -C; 0] so the foldover structure is visible: the rows
    # whose first non-zero entry is +1 form C, their sign-flipped mirrors form -C, and the
    # all-zero row is the centre run.
    levels = dsd.design[dsd.factor_names].to_numpy(dtype=float)
    top = [i for i, r in enumerate(levels) if r.any() and r[r != 0][0] > 0]
    mirror = [next(j for j, s in enumerate(levels) if np.array_equal(s, -levels[i])) for i in top]
    centre = [i for i, r in enumerate(levels) if not r.any()]
    matrix = levels[top + mirror + centre]

    fig = go.Figure(go.Heatmap(
        z=matrix, x=dsd.factor_names, zmid=0, showscale=False,
        colorscale=[[0, "#0072B2"], [0.5, "#EDEDED"], [1, "#D55E00"]]))
    fig.update_layout(xaxis_title="Factor", yaxis_title="Run (construction order)",
                      yaxis=dict(autorange="reversed"))
    fig.show()

Each cell is one factor at one of its three coded levels: :math:`-1` (blue), :math:`0` (grey),
or :math:`+1` (vermillion). The blue and vermillion are the colourblind-safe Okabe-Ito pair.
Reading the figure top to bottom, there is a light interpretation worth
making now, leaving the mechanics to the construction above and the quantitative comparison to
the :ref:`next sections <DOE-omars-designs>`:

    *   The runs come in *mirror-image pairs*. The lower block is the upper block with every
        sign flipped (each blue cell becomes vermillion and the reverse): this is the
        :math:`-\mathbf{C}` half folded under the :math:`\mathbf{C}` half. That mirror symmetry
        is the foldover, and it is what buys the clean, unaliased main effects.

    *   A single *centre run* sits at the bottom, every factor at :math:`0` (all grey). It
        anchors the curvature check: without a middle level there is no way to tell a bent
        response from a straight one.

    *   Every factor is exercised at all three levels, and exactly one factor sits at :math:`0`
        in each non-centre run (the grey staircase, which is the conference matrix's zero
        diagonal). Thirteen runs cover six factors at three levels each: the economy that makes
        a DSD attractive as a first experiment.

.. figure:: ../figures/doe/dsd-run-matrix.png
    :align: center
    :width: 520px
    :alt: dsd-run-matrix.py

    The run matrix of a six-factor definitive screening design (13 runs), shown in construction
    order. The top block is a conference matrix :math:`\mathbf{C}`; the middle block is its
    sign-flipped mirror :math:`-\mathbf{C}`; the final row is the centre run. Colours are the
    coded levels :math:`-1` (blue), :math:`0` (grey), and :math:`+1` (vermillion), using the
    colourblind-safe Okabe-Ito palette.

How to analyse the resulting data, once responses are measured, is a topic in its own right,
because the structured aliasing among the second-order effects means a naive least squares fit
is the wrong tool. That is taken up in :ref:`Analysing data from these designs
<DOE-analysing-economical-designs>`, after the OMARS family is introduced, since the same
staged analysis serves both.

**Readings**

* Jones, B. and Nachtsheim, C.J.: "`A Class of Three-Level Designs for Definitive Screening in
  the Presence of Second-Order Effects <https://yint.org/dsdesign>`_", *Journal of Quality
  Technology*, **43**, 1--15, 2011.
  `doi:10.1080/00224065.2011.11917841 <https://doi.org/10.1080/00224065.2011.11917841>`__
* Xiao, L., Lin, D.K.J. and Bai, F.: "Constructing Definitive Screening Designs Using Conference
  Matrices", *Journal of Quality Technology*, **44**, 2--8, 2012.
  `doi:10.1080/00224065.2012.11917877 <https://doi.org/10.1080/00224065.2012.11917877>`__
* John Lawson: "`DefScreen: Definitive Screening Designs, in package "daewr"
  <https://rdrr.io/cran/daewr/man/DefScreen.html>`_", *Design and Analysis of Experiments with
  R*.
