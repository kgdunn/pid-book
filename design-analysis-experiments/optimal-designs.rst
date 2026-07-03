.. _DOE-optimal-and-omars-designs:

.. index::
    pair: optimal design; experiments
    pair: information matrix; experiments
    pair: candidate set; optimal designs
    pair: coordinate-exchange algorithm; optimal designs
    see: exchange algorithm; coordinate-exchange algorithm

Optimal designs of experiments: D-, A-, and G-optimality and the information matrix
====================================================================================

Every design we have built so far has been a *template*. You decide how many factors
:math:`k` you are studying, and the recipe (:ref:`full factorial <DOE-two-level-factorials>`,
:ref:`fractional factorial <DOE-fractional-factorials>`, :ref:`central composite
<DOE_central_composite_designs>`, :ref:`Box-Behnken <DOE-box-behnken-designs>`) then fixes the
runs for you. Templates are superb when your problem happens to match their shape. This
section, and the two that follow it, are about what to do when it does not, and about a family
of designs that lets a computer build the experiment for you.

The thread running through all three sections is the same: state the model you want to fit, the
region you are allowed to explore, and a single number that measures how good a design is, and
then let an algorithm choose the runs that make that number as good as possible. This first
section develops that idea as *optimal designs*. Making "how good a design is" precise forces us
to introduce one object, the information matrix, that the rest of this section (and the
:ref:`next one <DOE-judging-and-comparing-designs>`) uses throughout. The
:ref:`second section <DOE-definitive-screening-designs>` then covers definitive screening
designs, and the :ref:`third <DOE-omars-designs>` the OMARS family they belong to: structured,
economical designs that do the work of a screening experiment and a response surface experiment
in a single set of runs.

When the classical designs do not fit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is worth being clear about why the templates are good before we discuss leaving them.
A full factorial spans the largest possible space for the :math:`k` factors. We know from
least squares modelling that pushing the runs far from the centre of the model reduces the
variance of the parameter estimates, and a factorial moves every factor independently of
the others, so we can estimate every effect independently as well. Those are genuinely
optimal properties, and for most problems a factorial or a central composite design is
exactly the right choice.

The templates start to chafe only when your problem violates the assumptions baked into
them: a tidy run count, a cuboidal region you may roam freely, and continuous factors you
can reset at will. Real experiments routinely break at least one of these. A few common
situations:

    *   **The region is constrained.** Some factor combinations are unsafe, infeasible, or
        simply not of interest, so the cuboid has a corner or an edge sliced off. A template
        that insists on running that corner cannot be used.

    *   **The budget is an awkward number.** You can afford fourteen runs, which is not a
        power of two and does not match any standard factorial or composite design.

    *   **The factors are of mixed type.** Some are continuous, some are categorical (a
        catalyst chosen from three suppliers, say), and no single classical template covers
        the combination cleanly.

    *   **Some factors are hard to change.** Resetting an oven temperature between every run
        is slow or expensive, so you would like a design that changes it as seldom as
        possible. (This leads to *split-plot* structures, a topic beyond the scope of this chapter.)

    *   **You already have a fixed list of candidate runs**, or you have already run several
        experiments and want to add a few more to sharpen the estimates.

Two modern responses meet these situations. The first is to let a computer choose the runs
by optimizing a criterion: an *optimal design*, the subject of the rest of this section. The
second is to use a purpose-built, economical design that screens and models curvature at once:
the :ref:`definitive screening design <DOE-definitive-screening-designs>` and its
generalization, the :ref:`OMARS family <DOE-omars-designs>`, taken up in the two sections that
follow.

.. _DOE-optimal-designs:

The idea of an optimal design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you read the modern literature on experimental methods you will quickly meet the idea of
an *optimal* design. The name is provocative: it implies the designs we have used so far are
somehow sub-optimal, which, as we just argued, they usually are not. So what does an optimal
design actually do?

All an optimal design does is **select the experimental runs by optimizing some criterion,
subject to constraints.** Some examples of the kinds of problem it solves:

    *   The design region is a cube with a diagonal slice cut off two corners because of a
        constraint. What design spans the remaining region best?

    *   The experimenter wants to estimate a non-standard model, for example
        :math:`y = b_0 + b_\mathrm{A}x_\mathrm{A} + b_\mathrm{B}x_\mathrm{B} +
        b_\mathrm{AB}x_\mathrm{A}x_\mathrm{B}` together with some bespoke nonlinear term.

    *   For a central composite or constrained factorial, find a *smaller* set of runs than
        the full design needs, say fourteen runs (not a power of two).

    *   The user wants more than two levels in each factor.

    *   The experimenter has already run :math:`n` experiments and wants to add a few more to
        decrease the variance of the parameters. A D-optimal augmentation finds the extra
        run(s) that most increase :math:`\det\left(\mathbf{X}^T\mathbf{X}\right)`.

The general procedure is always the same:

    #.  The user specifies the **model** (which is to say, the parameters to be estimated).

    #.  The computer enumerates every combination of factor levels that satisfies the
        constraints, including centre points. This long list is the
        :index:`candidate set <pair: candidate set; optimal designs>`. The user may add any
        particular runs they want to be considered.

    #.  The user states how many runs they can actually afford.

    #.  An algorithm selects that many runs from the candidate set so as to optimize the
        chosen criterion.

There are two things to notice. First, the user must specify the model. This feels like an
extra burden, but it is no different from a factorial or a central composite design, where
the model is simply *implicit* in the template. An optimal design only makes the assumption
explicit. Second, "optimize a criterion" presumes we have agreed on a criterion. The usual
ones carry single-letter names, A-, D-, G- and V-optimality, and a full :math:`2^k` factorial
turns out to be A-, D-, G- and V-optimal all at once for the main-effects-and-interactions
model. To say what those letters mean, and why they can disagree for the economical designs of
the :ref:`next two sections <DOE-definitive-screening-designs>`, we need the information matrix,
which is the subject of the next subsection.

**Readings**

* St. John and Draper: "`D-Optimality for Regression Designs: A Review
  <https://www.jstor.org/stable/1267995>`_", *Technometrics*, **17**, 15--23, 1975.
  `doi:10.1080/00401706.1975.10489266 <https://doi.org/10.1080/00401706.1975.10489266>`__

The information matrix and the optimality criteria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A criterion is a single number computed from the design, and every criterion we use is built
from one matrix. Before we define it, one quantity deserves to be pinned down, because it runs
through everything that follows: the noise standard deviation :math:`\sigma`. It is the
irreducible, run-to-run variability of the response, the scatter you would still see if you
held every factor fixed and simply repeated the experiment. Every variance below is
:math:`\sigma^2` multiplied by something that depends only on the design, and a design controls
only that second part, the geometry. It can do nothing about :math:`\sigma` itself; pinning that
down, by replication or from prior knowledge of the process, is the experimenter's job.

Everything starts with the :math:`\mathbf{X}` matrix from least squares
(:ref:`multiple linear regression <LS_multiple_X_MLR>`). The point that trips people up:
**the columns of** :math:`\mathbf{X}` **are the terms of the model you intend to fit, not just
the factors.** Each row is one experimental run; each column is one term in the model.

For the full second-order model in :math:`k` factors,

.. math::

    y = b_0 + \sum_i b_i x_i + \sum_i b_{ii} x_i^2 + \sum_{i<j} b_{ij} x_i x_j + e

the columns of :math:`\mathbf{X}` are: a column of ones (the intercept), one column per main
effect :math:`x_i`, one column per pure quadratic :math:`x_i^2`, and one column per two-factor
interaction :math:`x_i x_j`. The same physical design produces a *different* :math:`\mathbf{X}`
for a different model. A single row of :math:`\mathbf{X}` is the *model expansion* of that run:
a run at settings :math:`(x_1, x_2, \ldots)` becomes the row
:math:`\mathbf{x}_m^T = [\,1,\ x_1,\ x_2,\ \ldots,\ x_1^2,\ \ldots,\ x_1 x_2,\ \ldots\,]`.

The **information matrix** is

.. math::

    \mathbf{M} = \mathbf{X}^T \mathbf{X}

It earns its name from the least squares result for the covariance of the estimated coefficients
(:ref:`confidence intervals for the parameters <LS-CI-for-model-parameters>`):

.. math::

    \text{Var}(\mathbf{b}) = \sigma^2 \left(\mathbf{X}^T \mathbf{X}\right)^{-1}
                           = \sigma^2 \mathbf{M}^{-1}

So :math:`\mathbf{M}^{-1}`, scaled by :math:`\sigma^2`, *is* the variance-covariance matrix of the
coefficient estimates. More information (a "larger" :math:`\mathbf{M}`) means a smaller
:math:`\mathbf{M}^{-1}`, and therefore more precise estimates. This is exactly the quantity an
optimal design manipulates: by choosing the runs, it chooses :math:`\mathbf{X}`, and so it shapes
:math:`\mathbf{M}`.

Read :math:`\mathbf{M}` entry by entry. Because :math:`\mathbf{M} = \mathbf{X}^T\mathbf{X}`, the
entry :math:`M_{jk}` is the dot product of model columns :math:`j` and :math:`k`:

    *   the **diagonal** :math:`M_{jj}` is the squared length of column :math:`j`: how hard the
        design exercises that term. Bigger means more information about that coefficient;

    *   the **off-diagonal** :math:`M_{jk}` measures how *entangled* terms :math:`j` and
        :math:`k` are. Zero means the two effects are orthogonal and are estimated independently;
        a large value means their estimates are correlated and their variances inflate.

If a design is fully orthogonal, :math:`\mathbf{M}` is diagonal and every coefficient is estimated
on its own with variance :math:`\sigma^2 / M_{jj}`. If two columns are linearly dependent (one
effect :ref:`confounded <DOE-design-resolution>` with another) then :math:`\mathbf{M}` is singular,
cannot be inverted, and that coefficient is simply not estimable.

With :math:`\mathbf{M}` in hand, the optimality criteria are nothing more than different scalar
summaries of it. They are easiest to understand through the eigenvalues
:math:`\lambda_1, \ldots, \lambda_p` of :math:`\mathbf{M}`, remembering that the coefficient
variances live in the reciprocals :math:`1/\lambda`.

    *   **D-optimality** maximizes :math:`\det(\mathbf{M}) = \prod_j \lambda_j`. The joint
        confidence region for all the coefficients is an ellipsoid whose volume is proportional to
        :math:`1/\sqrt{\det(\mathbf{M})}`, so a large determinant means the smallest *overall,
        joint* uncertainty. Because the determinant is a *product*, a design that distributes
        information unevenly across coefficients (one estimated very precisely, another less so)
        can still score well, provided the precise directions compensate. D-optimality is the
        natural criterion when the goal is to estimate the full set of model coefficients
        together, as in screening, where the joint confidence ellipsoid matters.

    *   **A-optimality** minimizes :math:`\text{trace}(\mathbf{M}^{-1}) = \sum_j 1/\lambda_j`,
        which is exactly the sum of the individual coefficient variances (the diagonal entries of
        :math:`\mathbf{M}^{-1}`). Because it is a *sum* rather than a product, every coefficient
        contributes equally: a design that lets one variance become large is penalised even when
        all others are small. A-optimality asks for the smallest total estimation error across all
        terms, so it tends to produce more balanced designs than D-optimality when some
        coefficients are inherently harder to estimate. Where D-optimality would let a
        hard-to-estimate coefficient's variance balloon if doing so improves the product,
        A-optimality resists that trade-off. Mnemonic: D for the Determinant of the joint
        confidence ellipsoid; A for the Average individual variance.

    *   **E-optimality** maximizes the smallest eigenvalue of :math:`\mathbf{M}`. The eigenvectors
        of :math:`\mathbf{M}` are directions in coefficient space; the eigenvalues are the
        information available in each direction. The smallest eigenvalue corresponds to the linear
        combination of coefficients that is hardest to estimate, the direction in which the
        confidence ellipsoid stretches furthest. E-optimality is a minimax criterion: it forces
        the design to strengthen whichever direction is weakest, even at the cost of being
        suboptimal elsewhere. It is appropriate when a poorly-estimated contrast would invalidate
        the experiment, but it is rarely the primary criterion in practice because strengthening a
        single worst-case direction can degrade the average (A) and joint (D) measures noticeably.
        Mnemonic: E for the Eigenvalue of the worst-Estimated direction.

    *   **G-**, **I-**, and **V-optimality** are about the variance of the *predictions* rather than
        the coefficients directly. G-optimality minimizes the largest prediction variance anywhere in
        the region. I-optimality (also called *IV-optimality*) minimizes the *average* prediction
        variance over the whole region. V-optimality is the closely related criterion that averages
        the prediction variance over a chosen finite set of points instead of over the whole region.
        All three are built on the prediction variance, which we develop in
        :ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>`.

D multiplies the eigenvalues, A sums their reciprocals, E looks at the extreme one: the same
matrix, aggregated differently. That is why a design can score well on one criterion and poorly on
another, and why the choice of criterion should follow the purpose of the experiment. The criteria
agree completely for a full :math:`2^k` factorial, and only begin to disagree once we economize on
runs or move to the three-level designs of the :ref:`next two sections
<DOE-definitive-screening-designs>`.

.. _DOE-information-matrix-worked-example:

A worked example: the information matrix of a small design
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The mechanics are clearest on the smallest design that still has curvature: a single factor run at
three levels, :math:`x = -1, 0, +1`, fitting the quadratic model
:math:`y = b_0 + b_1 x + b_2 x^2 + e`. Each point expands to :math:`\mathbf{x}_m = [\,1,\ x,\ x^2\,]`,
so

.. math::

    \mathbf{X} = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix},
    \qquad
    \mathbf{M} = \mathbf{X}^T\mathbf{X}
        = \begin{bmatrix} 3 & 0 & 2 \\ 0 & 2 & 0 \\ 2 & 0 & 2 \end{bmatrix}

The off-diagonal :math:`M_{01} = M_{12} = 0` tells us the linear term is orthogonal to both the
intercept and the quadratic, so :math:`b_1` is estimated cleanly. But :math:`M_{02} = 2 \neq 0`: the
intercept and quadratic columns are entangled (both have a positive mean), so :math:`b_0` and
:math:`b_2` will be correlated. Inverting,

.. math::

    \mathbf{M}^{-1} = \begin{bmatrix} 1 & 0 & -1 \\ 0 & 0.5 & 0 \\ -1 & 0 & 1.5 \end{bmatrix}

The diagonal gives the coefficient variances in units of :math:`\sigma^2`:
:math:`\text{Var}(b_0) = 1.0\,\sigma^2`, :math:`\text{Var}(b_1) = 0.5\,\sigma^2`, and
:math:`\text{Var}(b_2) = 1.5\,\sigma^2`. The quadratic is the least precise (curvature is the hardest
thing to pin down from only three points), and the :math:`-1` off-diagonal is the
intercept-quadratic correlation we anticipated from :math:`M_{02}`. Every optimality criterion above
is just a one-number summary of these same two matrices.

For this design those summaries are easy to read off. The D-criterion is
:math:`\det(\mathbf{M}) = 4`. The A-criterion is
:math:`\text{trace}(\mathbf{M}^{-1}) = 1.0 + 0.5 + 1.5 = 3.0`, the sum of the three coefficient
variances. The E-criterion is the smallest eigenvalue of :math:`\mathbf{M}`, here about
:math:`0.44`. The prediction-based G- and V-criteria need the prediction variance, which we develop
in :ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>`. We also return to this
very design there: in :ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>` we
add two more runs to it and watch every one of these numbers change, which is the starting point for
learning how to compare designs.

How the algorithms search: exchange algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choosing the best :math:`n` runs is a combinatorial problem: from a candidate set of hundreds of
points, which handful makes :math:`\det(\mathbf{M})` (or whichever criterion) largest? Checking every
subset is hopeless for all but trivial cases, so we use iterative search, and two families dominate.

    *   **Point-exchange** algorithms (Fedorov; Wynn-Mitchell; the DETMAX procedure) start from an
        initial design drawn from the candidate set and then repeatedly swap a point that is *in* the
        design for one that is *out*, keeping the swap whenever it improves the criterion, until no
        swap helps.

    *   **Coordinate-exchange** (Meyer and Nachtsheim, 1995) dispenses with an explicit candidate set
        altogether. It walks through each coordinate of each run in turn and sets it to the value that
        most improves the criterion, cycling through all coordinates repeatedly until nothing improves.
        This scales to many factors and handles constrained regions gracefully, which is why it is the
        engine inside most modern software.

Both procedures climb to a *local* optimum, and the surface is bumpy, so in practice the algorithm is
restarted from many random initial designs and the best result is kept. A useful trick keeps this
affordable: for D-optimality the change in :math:`\det(\mathbf{M})` from a single exchange has a
closed-form update, so each candidate move is cheap to evaluate. This is exactly the machinery that
runs under the hood when you (or the code in this book) ask for an optimal design.

To see the contrast, watch both algorithms solve the same small problem: two factors, the model
:math:`y = b_0 + b_1 x_1 + b_2 x_2 + b_{12} x_1 x_2 + e`, four runs, and the region
:math:`[-1, +1]^2`, meaning each of the two coded factors may take any value from :math:`-1` to
:math:`+1`. The D-optimal answer is the :math:`2^2` factorial (the four corners), where
:math:`\mathbf{X}^T\mathbf{X} = 4\,\mathbf{I}` and :math:`\det(\mathbf{M}) = 4^4 = 256`. Here are
the two algorithms reaching it, side by side, with :math:`\det(\mathbf{M})` shown at each step.

.. list-table:: The two exchange algorithms on the same four-run problem.
    :header-rows: 1
    :widths: 50 50

    *   - Point-exchange (swaps whole runs)
        - Coordinate-exchange (adjusts one coordinate)
    *   - Candidate set: the nine points where each factor is :math:`-1`, :math:`0`, or :math:`+1`, namely :math:`(-1,-1)`, :math:`(-1,0)`, :math:`(-1,+1)`, :math:`(0,-1)`, :math:`(0,0)`, :math:`(0,+1)`, :math:`(+1,-1)`, :math:`(+1,0)`, :math:`(+1,+1)`.
        - No candidate set; each coordinate ranges freely over :math:`[-1, +1]`.
    *   - Start :math:`\{(-1,-1), (0,1), (1,0), (1,1)\}`, :math:`\det\mathbf{M} = 16`.
        - Start from four random points, :math:`\det\mathbf{M} = 0.3`.
    *   - Swap run 2: :math:`(0,1) \to (-1,1)`, giving :math:`\det\mathbf{M} = 64`.
        - Pass 1: each coordinate is driven to its best value, every one lands on :math:`\pm 1`, giving :math:`\det\mathbf{M} = 256`.
    *   - Swap run 3: :math:`(1,0) \to (1,-1)`, giving :math:`\det\mathbf{M} = 256`.
        - Pass 2: nothing changes; already converged.
    *   - Final: the four corners, :math:`\det\mathbf{M} = 256`.
        - Final: the four corners, :math:`\det\mathbf{M} = 256`.

Both land on the same design, which is reassuring, but they got there differently, and that
difference is the whole point. Point-exchange can only ever choose runs that are already in the
candidate set, so a coarse grid caps the quality of the result: had we offered it only the four corners
:math:`(-1,-1)`, :math:`(-1,+1)`, :math:`(+1,-1)`, :math:`(+1,+1)` it could not have explored at all,
and on a finer grid it has many more points
to sift through. Coordinate-exchange carries no candidate set; it slides each coordinate along its
continuous range, so it can place a run anywhere, including at points no grid would have listed.
That freedom is what makes it the natural choice for constrained regions and for many factors, and
the price, more criterion evaluations per move, is exactly what the determinant-update shortcut is
there to absorb.

**Readings**

* Meyer, R.K. and Nachtsheim, C.J.: "`The Coordinate-Exchange Algorithm for Constructing Exact
  Optimal Experimental Designs <https://www.jstor.org/stable/1269153>`_", *Technometrics*, **37**,
  60--69, 1995.
  `doi:10.1080/00401706.1995.10485889 <https://doi.org/10.1080/00401706.1995.10485889>`__

.. _DOE-constrained-optimal-example:

A worked example: a design the catalogue cannot give you
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose we are studying two continuous factors and want to fit the full quadratic model
:math:`y = b_0 + b_1 x_1 + b_2 x_2 + b_{11}x_1^2 + b_{22}x_2^2 + b_{12}x_1 x_2 + e`. Ordinarily a
:math:`3^2` grid or a face-centred central composite design would do the job. But suppose a safety
constraint forbids running both factors high at once, so in coded units the region is the square
:math:`[-1, +1]^2` with the top-right corner sliced off by :math:`x_1 + x_2 \le 1`.

Now the template fails outright: a :math:`3^2` factorial and a face-centred composite design both
*require* a run at :math:`(+1, +1)`, which we are not allowed to perform. There is no way to nudge the
template into the feasible region without abandoning what makes it a template.

The optimal-design recipe handles it without fuss. We specify the quadratic model, let the computer
build the candidate set from the feasible grid points (everything with :math:`x_1 + x_2 \le 1`), ask
for, say, ten runs, and let coordinate-exchange maximize :math:`\det(\mathbf{M})`. The resulting
D-optimal design is:

.. list-table:: A 10-run D-optimal design for the quadratic model on the constrained region.
    :header-rows: 1
    :widths: 30 30 40

    *   - :math:`x_1`
        - :math:`x_2`
        - runs
    *   - :math:`-1`
        - :math:`-1`
        - 2
    *   - :math:`-1`
        - :math:`0`
        - 1
    *   - :math:`-1`
        - :math:`+1`
        - 2
    *   - :math:`0`
        - :math:`-1`
        - 1
    *   - :math:`0`
        - :math:`0`
        - 1
    *   - :math:`0`
        - :math:`+1`
        - 1
    *   - :math:`+1`
        - :math:`-1`
        - 1
    *   - :math:`+1`
        - :math:`0`
        - 1

Read what the algorithm chose. It keeps the three feasible corners and replicates two of them, places
the centre point, and puts runs at :math:`(0, +1)` and :math:`(+1, 0)`, which sit exactly on the
constraint boundary :math:`x_1 + x_2 = 1`. In other words it pushes the runs to the edge of the
*allowed* region, just as a factorial pushes them to the edge of the cuboid, and it never asks for the
forbidden corner. The full quadratic model remains estimable throughout. No catalogue design could
have produced this; the optimal design simply read off the constraint and the model and did the
sensible thing.

A D-optimal design is not unique: several different run allocations can share the same maximum
:math:`\det(\mathbf{M})`. The table above is one such optimum; your own solver, or a different random
start for the coordinate-exchange search, may return a different allocation of the ten runs that is
equally D-optimal.

.. figure:: ../figures/doe/constrained-d-optimal-region.png
    :align: center
    :width: 600px
    :alt: constrained-d-optimal-region.py

    The feasible region (white) for the two-factor constrained example. The corner with
    :math:`x_1 + x_2 > 1` is infeasible (shaded), so the run at :math:`(+1, +1)` cannot be
    performed. The ten-run D-optimal design uses the eight feasible grid points, with the two
    larger markers run twice.

The optimal-design recipe is fully general, but it asks you to specify a model and run a search for
each new problem. The :ref:`next section <DOE-definitive-screening-designs>` turns to a structured
family of three-level designs that arrives ready-made, while keeping much of the same flexibility:
the definitive screening design.
