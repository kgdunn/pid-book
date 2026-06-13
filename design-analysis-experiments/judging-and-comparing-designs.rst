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

By this point we have several ways to build a design: full factorials, fractional
factorials, central composite designs (:ref:`central composite designs
<DOE_central_composite_designs>`), and the
more flexible :ref:`optimal designs <DOE-optimial-designs>`. A practical question
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

Both questions are answered by a single object built from the design: the
information matrix. This subchapter shows what that matrix is, how the
:ref:`optimality criteria <DOE-optimial-designs>` are simply different ways of
reading it, how prediction variance is derived from it, and how to read a
fraction-of-design-space plot. We close with a short checklist for choosing
between designs.

The model matrix and the information matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Everything starts with the :math:`\mathbf{X}` matrix from least squares
(:ref:`multiple linear regression <LS_multiple_X_MLR>`). The key point that trips
people up: **the columns of** :math:`\mathbf{X}` **are the terms of the model you
intend to fit, not just the factors.** Each row is one experimental run; each column
is one term in the model.

For the full second-order model in :math:`k` factors,

.. math::

    y = b_0 + \sum_i b_i x_i + \sum_i b_{ii} x_i^2 + \sum_{i<j} b_{ij} x_i x_j + e

the columns of :math:`\mathbf{X}` are: a column of ones (the intercept), one column
per main effect :math:`x_i`, one column per pure quadratic :math:`x_i^2`, and one
column per two-factor interaction :math:`x_i x_j`. The same physical design produces
a *different* :math:`\mathbf{X}` for a different model. A single row of
:math:`\mathbf{X}` is the *model expansion* of that run: a run at settings
:math:`(x_1, x_2, \ldots)` becomes the row
:math:`\mathbf{x}_m^T = [\,1,\ x_1,\ x_2,\ \ldots,\ x_1^2,\ \ldots,\ x_1 x_2,\ \ldots\,]`.
We will reuse :math:`\mathbf{x}_m(\mathbf{x})` shortly to mean this same expansion
evaluated at *any* point :math:`\mathbf{x}`, including points we never ran.

The **information matrix** is

.. math::

    \mathbf{M} = \mathbf{X}^T \mathbf{X}

It earns its name from the least squares result for the covariance of the estimated
coefficients (:ref:`confidence intervals for the parameters <LS-CI-for-model-parameters>`):

.. math::

    \text{Var}(\mathbf{b}) = \sigma^2 \left(\mathbf{X}^T \mathbf{X}\right)^{-1}
                           = \sigma^2 \mathbf{M}^{-1}

So :math:`\mathbf{M}^{-1}`, scaled by the noise variance :math:`\sigma^2`, *is* the
variance-covariance matrix of the coefficient estimates. More information (a "larger"
:math:`\mathbf{M}`) means a smaller :math:`\mathbf{M}^{-1}`, and therefore more
precise estimates.

Read :math:`\mathbf{M}` entry by entry. Because :math:`\mathbf{M} = \mathbf{X}^T\mathbf{X}`,
the entry :math:`M_{jk}` is the dot product of model columns :math:`j` and :math:`k`:

    *   the **diagonal** :math:`M_{jj}` is the squared length of column :math:`j`:
        how hard the design exercises that term. Bigger means more information about
        that coefficient;

    *   the **off-diagonal** :math:`M_{jk}` measures how *entangled* terms :math:`j`
        and :math:`k` are. Zero means the two effects are orthogonal and are
        estimated independently; a large value means their estimates are correlated
        and their variances inflate.

If a design is fully orthogonal, :math:`\mathbf{M}` is diagonal and every coefficient
is estimated on its own with variance :math:`\sigma^2 / M_{jj}`. If two columns are
linearly dependent (one effect :ref:`confounded <DOE-design-resolution>` with
another) then :math:`\mathbf{M}` is singular, cannot be inverted, and that
coefficient is simply not estimable.

Reading the optimality criteria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`optimality criteria <DOE-optimial-designs>` are nothing more than different
scalar summaries of :math:`\mathbf{M}`. They are easiest to understand through the
eigenvalues :math:`\lambda_1, \ldots, \lambda_p` of :math:`\mathbf{M}`, remembering
that the coefficient variances live in the reciprocals :math:`1/\lambda`.

    *   **D-optimality** maximizes :math:`\text{det}(\mathbf{M}) = \prod_j \lambda_j`.
        The joint confidence region for all the coefficients is an ellipsoid whose
        volume is proportional to :math:`1/\sqrt{\text{det}(\mathbf{M})}`, so a large
        determinant means the smallest *overall, joint* uncertainty. This is the
        natural criterion when the goal is to estimate the model coefficients well,
        as in screening.

    *   **A-optimality** minimizes :math:`\text{trace}(\mathbf{M}^{-1}) =
        \sum_j 1/\lambda_j`, which is exactly the sum (or average) of the individual
        coefficient variances. It is the most directly interpretable criterion.

    *   **E-optimality** maximizes the smallest eigenvalue of :math:`\mathbf{M}`, i.e.
        it controls the *worst-estimated* combination of coefficients.

    *   **G-optimality** minimizes the largest prediction variance anywhere in the
        region, and **V-optimality** (also called *I-* or *IV-optimality* in the
        literature) minimizes the *average* prediction variance over the region.
        These two are about prediction rather than the coefficients directly, which
        we develop next.

D multiplies the eigenvalues, A sums their reciprocals, E looks at the extreme one:
the same matrix, aggregated differently. That is precisely why a design can score well
on one criterion and poorly on another, and why the choice of criterion should follow
the purpose of the experiment. As noted in the :ref:`optimal designs <DOE-optimial-designs>`
section, a full :math:`2^k` factorial is simultaneously A-, D-, G- and V-optimal for the
main-effects-and-interactions model: the criteria only start to disagree once we
economize on runs or move to three-level designs.

.. _DOE-information-matrix-worked-example:

A worked example: the information matrix of a small design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The mechanics are clearest on the smallest design that still has curvature: a single
factor run at three levels, :math:`x = -1, 0, +1`, fitting the quadratic model
:math:`y = b_0 + b_1 x + b_2 x^2 + e`. Each point expands to
:math:`\mathbf{x}_m = [\,1,\ x,\ x^2\,]`, so

.. math::

    \mathbf{X} = \begin{bmatrix} 1 & -1 & 1 \\ 1 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix},
    \qquad
    \mathbf{M} = \mathbf{X}^T\mathbf{X}
        = \begin{bmatrix} 3 & 0 & 2 \\ 0 & 2 & 0 \\ 2 & 0 & 2 \end{bmatrix}

The off-diagonal :math:`M_{01} = M_{12} = 0` tells us the linear term is orthogonal to
both the intercept and the quadratic, so :math:`b_1` is estimated cleanly. But
:math:`M_{02} = 2 \neq 0`: the intercept and quadratic columns are entangled (both have
a positive mean), so :math:`b_0` and :math:`b_2` will be correlated. Inverting,

.. math::

    \mathbf{M}^{-1} = \begin{bmatrix} 1 & 0 & -1 \\ 0 & 0.5 & 0 \\ -1 & 0 & 1.5 \end{bmatrix}

The diagonal gives the coefficient variances in units of :math:`\sigma^2`:
:math:`\text{Var}(b_0) = 1.0\,\sigma^2`, :math:`\text{Var}(b_1) = 0.5\,\sigma^2`, and
:math:`\text{Var}(b_2) = 1.5\,\sigma^2`. The quadratic is the least precise (curvature
is the hardest thing to pin down from only three points), and the :math:`-1`
off-diagonal is the intercept-quadratic correlation we anticipated from
:math:`M_{02}`.

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

That is the entire derivation: it is just error propagation through the linear
predictor, using :math:`\text{Var}(\mathbf{b}) = \sigma^2 \mathbf{M}^{-1}`.

For the three-run example above, multiplying :math:`[1, x, x^2]` through
:math:`\mathbf{M}^{-1}` and contracting gives a tidy polynomial:

.. math::

    \text{Var}\big(\widehat{y}(x)\big) = \sigma^2 \left(1 - 1.5\,x^2 + 1.5\,x^4\right)

At the three design points (:math:`x = -1, 0, +1`) this equals :math:`\sigma^2`, as it
must: a saturated design interpolates its own data. Between the points it dips to a
minimum of :math:`0.625\,\sigma^2` at :math:`x = \pm 0.707`, and beyond :math:`x = 1` it
climbs steeply (already :math:`5.2\,\sigma^2` at :math:`x = 1.5`): a quantitative warning
against extrapolation.

To *compare designs* we strip out two nuisance factors. We divide by the unknown
:math:`\sigma^2` (a property of the process, not the design), and we multiply by the
number of runs :math:`N` (otherwise a design looks better merely for being larger:
replicate any design and :math:`\mathbf{M}` doubles, halving the variance). The result
is the :index:`scaled prediction variance <pair: scaled prediction variance; experiments>`:

.. math::

    \text{SPV}(\mathbf{x}) = N\, \mathbf{x}_m(\mathbf{x})^T \mathbf{M}^{-1} \mathbf{x}_m(\mathbf{x})
                           = \frac{N\,\text{Var}\big(\widehat{y}(\mathbf{x})\big)}{\sigma^2}

The SPV depends only on the geometry of the design. The G-optimal value is its maximum
over the region and the V-optimal (I-optimal) value is its average.

The fraction-of-design-space (FDS) plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A single design has a *different* SPV at every point in the factor region, so quoting one
number hides a lot. The :index:`fraction-of-design-space plot <pair: fraction of design space; experiments>`
(FDS plot) shows the whole distribution. It is built by sampling many points spread across
the region, computing the SPV at each, sorting those values from smallest to largest, and
plotting SPV (vertical axis) against the cumulative fraction of the region (horizontal
axis, running from 0 to 1).

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
designs are themselves the smallest members of that family.

.. figure:: ../figures/doe/fds-plot-dsd-vs-omars.png
    :align: center
    :width: 750px
    :alt: fds-plot-dsd-vs-omars.py

    FDS plot for a nine-run definitive screening design and a thirteen-run OMARS design,
    both in four factors on the main-effects-plus-quadratic model. The curves cross near a
    fraction of 0.75: the larger design predicts better on average but worse at the extreme
    corners.

The thirteen-run curve sits *below* the nine-run curve for roughly the first three
quarters of the region: it has lower best-case, median, and average prediction variance.
But the two curves **cross** near :math:`f \approx 0.75`, and the thirteen-run curve then
rises well above: its worst corner is noticeably worse. This crossing is the practical
tension between V- (average) and G- (worst-case) optimality, and it has a physical cause:
the larger design here places fewer runs at the extreme corners, so prediction there
behaves like mild extrapolation. The reading is concrete: if you care about prediction on
average across the space (typical optimization work), prefer the larger design; if you must
predict reliably even at the worst corner, the flatter nine-run curve is the safer choice.

Separability is not the same as precision
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The optimality criteria and the FDS plot all speak to *precision*. They are silent on the
other question, *separability*, which is governed by the off-diagonal structure of
:math:`\mathbf{M}`, i.e. how correlated the effects are with one another. For a design
where the main effects are guaranteed orthogonal to the second-order terms (the definitive
screening designs and their generalizations have this property), the only correlations
left are *among* the second-order terms. A useful single number is the largest absolute
correlation between any two second-order columns, computed after first removing the part of
each column that is explained by the intercept and the main effects (this centring matters,
because the quadratic columns :math:`x_i^2` have a positive mean that would otherwise
inflate every correlation). A value of 0 means perfectly separable; a value of 1 means the
two effects are statistically the same column and cannot be told apart.

It is essential to treat separability and precision as *two* axes, because a design can be
excellent on one and poor on the other. A one-factor-at-a-time design, for instance, has
almost no correlation between its effects (good separability) and yet very poor precision
(its information is spread thinly, giving a low determinant and high prediction variance).
Ranking designs on any single number (including a correlation summary) will eventually
recommend something you would never want to run. Look at both axes.

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
        the FDS plot and V-/I-optimality, then quadratic estimability, then how the design
        behaves when projected onto the subset of factors that turn out to be active. Favour a
        design whose FDS curve is low and flat.

Two rules of thumb close the loop. First, use **D for estimation and V/I for prediction**;
they frequently disagree, so choose by what you will actually do with the model. Second,
**compare D-efficiency only between designs of the same number of runs**: across
different run counts it always flatters the smaller design, so judge larger-versus-smaller on
the quantities that carry real units: average coefficient variance, prediction variance, power,
and the number of residual degrees of freedom.

**Readings**

* Box, Hunter and Hunter, *Statistics for Experimenters*, 2nd edition, for the factorial and
  response-surface groundwork.
* Myers, Montgomery and Anderson-Cook, *Response Surface Methodology*, for prediction variance,
  the scaled prediction variance, and FDS plots.
* Goos and Jones, *Optimal Design of Experiments: A Case Study Approach*, for the
  information-matrix view of the optimality criteria.
* Núñez Ares, Schoen and Goos, "Orthogonal Minimally Aliased Response Surface Designs", and the
  review by Goos, "OMARS Designs for Factor Screening and Response Surface Experimentation in One
  Step", for the OMARS family used in the comparison above.
