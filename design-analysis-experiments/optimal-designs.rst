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

.. _DOE-exchange-algorithms:

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

.. _DOE-augmenting-a-design:

Augmenting an existing design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Experimentation is sequential: a first experiment answers some questions and raises others. A
common situation is that a :ref:`screening design <DOE-saturated-screening-designs>` has
identified the important factors but has left several competing models that fit the data about
equally well, differing in which two-factor interactions they include. Rather than start over,
we add a few runs to the design we already have. This is design *augmentation*.

The runs already performed are not discarded, and they should not be ignored when choosing the
new ones. Write :math:`\mathbf{X}_1` for the model matrix of the original runs and
:math:`\mathbf{X}_2` for the model matrix of the runs still to be chosen, both expanded for the
*larger* model we now want to fit (the main effects, plus whichever interactions the competing
models disagree about). The information in the combined experiment is

.. math::

    \mathbf{M} = \mathbf{X}^T\mathbf{X}
               = \mathbf{X}_1^T\mathbf{X}_1 + \mathbf{X}_2^T\mathbf{X}_2

so the two experiments add their information. A D-optimal augmentation chooses the new runs
:math:`\mathbf{X}_2` to maximize :math:`\det\left(\mathbf{X}_1^T\mathbf{X}_1 +
\mathbf{X}_2^T\mathbf{X}_2\right)`, the determinant of the *total*. It does not maximize
:math:`\det\left(\mathbf{X}_2^T\mathbf{X}_2\right)` on its own. The distinction matters: the
original runs already carry a great deal of information about the main effects, so a follow-up
that ignored :math:`\mathbf{X}_1` would spend runs re-measuring them instead of placing the
runs where information is still scarce, on the interactions. The
:ref:`coordinate-exchange algorithm <DOE-exchange-algorithms>` does this by holding the rows of
:math:`\mathbf{X}_1` fixed and searching only over the new rows :math:`\mathbf{X}_2`. The worked
example in :ref:`Judging and comparing designs <DOE-judging-and-comparing-designs>` carries this
out on the smallest possible design: it starts from a single three-level factor and compares two
ways of spending two extra runs, scoring each by the determinant of the combined information
matrix.

Two practical points round this out.

*A block for drift between the experiments.* Time passes between the original experiment and the
follow-up, and the process mean may drift in the interim. Add a two-level
:ref:`blocking <DOE_blocking_section>` factor coded :math:`+1` for the original runs and
:math:`-1` for the new runs. Its estimated effect absorbs any shift between the two campaigns,
keeping that shift from biasing the factor effects of interest. This is the same device used to
protect a single experiment against a nuisance variable, with the passage of time playing the
part of the nuisance.

*How many runs to add.* The follow-up needs only as many runs as there are new terms to
estimate. If the enlarged model adds six interactions and one block effect to a model already
supported by the original runs, seven new runs suffice. This is where optimal augmentation
departs from the classical :ref:`foldover <DOE-foldover-designs>`, which reflects the signs of
the whole design and so doubles the run count. A foldover de-aliases a fixed set of effects (a
main effect from its two-factor interactions, for instance); optimal augmentation instead
de-aliases whatever set of effects the competing models actually disagree about, at the smaller
cost of only the runs that set requires. The choice among the competing models, once the extra
data are in, is made with a criterion that penalises extra terms: :math:`R^2` always rises as
terms are added and so is a poor guide, the root mean squared error is in the units of the
response but tends to favour models with too many terms, while the corrected Akaike information
criterion (AICc, smaller is better) rewards parsimony. Design augmentation and the choice of
follow-up runs are developed in :ref:`Goos and Jones <DOE_references>`.

.. _DOE-categorical-factors:

Categorical factors with several levels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every factor so far has been continuous or a two-level category coded :math:`-1` and
:math:`+1`. Optimal designs also accommodate a categorical factor with more than two levels,
such as a supplier chosen from three sources or a catalyst from four. This needs some care,
both in how the factor enters the model and in what we can then ask of the design.

A categorical factor with :math:`L` levels is written with *indicator* (dummy) columns, one per
level, the same construction used for :ref:`integer variables in a regression model
<LS-dummy-variables>`: :math:`s_1` is :math:`1` for runs at level 1 and :math:`0` otherwise,
:math:`s_2` is :math:`1` for level 2, and so on. All :math:`L` dummies cannot sit in the model alongside the
intercept, however: they sum to one in every row (:math:`s_1 + s_2 + \cdots + s_L = 1`), which
is the intercept column, so the columns are linearly dependent and
:math:`\mathbf{M} = \mathbf{X}^T\mathbf{X}` is singular and cannot be inverted. The usual
remedies each drop one redundant piece:

    *   drop the intercept, so each :math:`\delta_i` is the intercept for its own level;

    *   drop one dummy, making its level a reference against which the others are measured; or

    *   constrain the level effects to sum to zero (*effects coding*), so each
        :math:`\delta_i` is the departure of level :math:`i` from the average.

These are three ways of writing the same model, and neither the D-optimal nor the I-optimal
design depends on which one is used. The :math:`-1 / +1` coding used throughout this chapter for
a two-level factor is exactly effects coding for the case :math:`L = 2`.

To see that the coding does not change the chosen design, take a factor at four levels and, for
clarity, a design with one run at each level, fitting only the four level means. Dropping the
intercept makes the model matrix the four level indicators, :math:`\mathbf{X} = \mathbf{I}_4`, so
:math:`\mathbf{M} = \mathbf{X}^T\mathbf{X} = \mathbf{I}_4` and :math:`\det(\mathbf{M}) = 1`.
Reference coding, with level 4 as the baseline, uses the columns
:math:`[\,1,\ s_1,\ s_2,\ s_3\,]`:

.. math::

    \mathbf{X}_{\text{ref}} = \begin{bmatrix} 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\
    1 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0 \end{bmatrix},
    \qquad
    \mathbf{M}_{\text{ref}} = \mathbf{X}_{\text{ref}}^T\mathbf{X}_{\text{ref}}
    = \begin{bmatrix} 4 & 1 & 1 & 1 \\ 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\
    1 & 0 & 0 & 1 \end{bmatrix}, \quad \det = 1.

Effects coding, constraining the level effects to sum to zero so that level 4 is coded :math:`-1`
on every column, uses :math:`[\,1,\ e_1,\ e_2,\ e_3\,]`:

.. math::

    \mathbf{X}_{\text{eff}} = \begin{bmatrix} 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\
    1 & 0 & 0 & 1 \\ 1 & -1 & -1 & -1 \end{bmatrix},
    \qquad
    \mathbf{M}_{\text{eff}} = \begin{bmatrix} 4 & 0 & 0 & 0 \\ 0 & 2 & 1 & 1 \\
    0 & 1 & 2 & 1 \\ 0 & 1 & 1 & 2 \end{bmatrix}, \quad \det = 16.

The three determinants, :math:`1`, :math:`1`, and :math:`16`, are not equal, yet all three codings
fit the same four means. Any two of them are related by an invertible change of variables: writing
the effects-coded matrix in terms of the reference-coded one gives
:math:`\mathbf{X}_{\text{eff}} = \mathbf{X}_{\text{ref}}\,\mathbf{T}`, with

.. math::

    \mathbf{T} = \begin{bmatrix} 1 & -1 & -1 & -1 \\ 0 & 2 & 1 & 1 \\ 0 & 1 & 2 & 1 \\
    0 & 1 & 1 & 2 \end{bmatrix},
    \qquad \det(\mathbf{T}) = 4.

Then :math:`\mathbf{M}_{\text{eff}} = \mathbf{T}^T\mathbf{M}_{\text{ref}}\,\mathbf{T}`, so its
determinant follows without recomputing it:

.. math::

    \det(\mathbf{M}_{\text{eff}}) = \det(\mathbf{T})^2\,\det(\mathbf{M}_{\text{ref}})
                                  = 4^2 \times 1 = 16,

which matches the direct calculation. The factor :math:`\det(\mathbf{T})^2` depends only on the
coding :math:`\mathbf{T}`, not on the runs, so it cancels from any comparison of two designs: the
design that maximizes :math:`\det(\mathbf{M})` under one coding maximizes it under all of them, and
relative D-efficiencies (which are ratios of two determinants) come out identical. Only the absolute
value of the criterion moves with the coding. The same holds for the full model with the continuous
factors and their interactions, since the two codings are still related by a fixed invertible
:math:`\mathbf{T}`. And the fitted prediction :math:`\widehat{y}(\mathbf{x})` does not depend on the
coding at all, so the I-optimality comparison is unaffected too.

The reason to include a categorical factor is often *robustness*. Suppose the categorical factor is
a supplier whose material we cannot control, and we want the process to behave the same whatever
that supplier delivers. A model with only a main effect for supplier says the suppliers differ by a
fixed offset, the same at every setting of the continuous factors, so no choice of those settings can
bring the suppliers together. Including *interactions between the supplier and the continuous
factors* removes that limitation: each supplier then has its own slopes, so the gap between suppliers
changes as the continuous factors move.

What we search for afterwards is not a coefficient but an operating point. Write
:math:`\widehat{y}_s(\mathbf{x})` for the predicted response of supplier :math:`s` at the continuous
settings :math:`\mathbf{x}`, and look for the :math:`\mathbf{x}` that makes those predictions agree
across suppliers, that is, that drives the spread
:math:`\max_s \widehat{y}_s(\mathbf{x}) - \min_s \widehat{y}_s(\mathbf{x})` down to nearly zero. At
such a setting the process returns nearly the same result whichever supplier is used, so it is robust
to the supplier. The interaction terms are what make such a setting exist: were they all zero, the
supplier curves would stay parallel and the spread would be the same everywhere. A large
supplier-by-factor interaction is therefore what makes robustness reachable, not a term to be driven
to zero. Once a robust setting is found, a factor whose effect does not depend on supplier can move
the shared prediction onto the target value without reopening the gap. Locating that setting is
possible only because the interactions were estimated, which is the reason for including them in the
model.

A model with quadratic terms and these interactions is a
:ref:`response surface model <DOE-RSM>` estimated over a region that is part continuous and part
categorical. Because the aim there is prediction across that region, the average prediction
variance matters most, so I-optimality suits it better than D-optimality, whose focus on
estimating coefficients precisely is better matched to screening. This handling of categorical
factors, and the robustness strategy, are treated in :ref:`Goos and Jones <DOE_references>`.

The optimal-design recipe is fully general, but it asks you to specify a model and run a search for
each new problem. The :ref:`next section <DOE-definitive-screening-designs>` turns to a structured
family of three-level designs that arrives ready-made, while keeping much of the same flexibility:
the definitive screening design.
