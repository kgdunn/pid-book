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

Saying which specific design is best, even once the run budget is fixed, requires the
quantitative tools of the next section: the information matrix, the prediction variance and its
fraction-of-design-space plot, the correlations among the effects, and the power. Those are
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

.. _DOE-analysing-economical-designs:

Analysing data from these designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One last point, and it is easy to get wrong. Because these designs are deliberately economical
and carry structured aliasing, you should *not* simply throw the data at a least squares fit of
the full second-order model. Two things go wrong if you do. The model often has more terms than
the design has runs, so it is not estimable at all: the :math:`\mathbf{X}^T\mathbf{X}` matrix is
singular and cannot be inverted. For four factors, for example, the full quadratic model has
:math:`1 + 4 + 4 + 6 = 15` terms (an intercept, four main effects, four quadratics, and six
two-factor interactions), while a definitive screening design has only nine runs and even the
thirteen-run OMARS design has only thirteen, so neither can fit the full model. And even when it
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
    (0)  enough spare error degrees of freedom?
         ( runs greater than the number of terms being fitted )
         if not  ->  stop; replicate or add runs first
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
         many are jointly estimable, and optionally guided by
         factor heredity ( an interaction is admitted only if its
           parent main effects are active )
             |
             v
    final model: the active main, quadratic, and interaction effects

Step 0 is not a formality. A *saturated* design, one with no spare runs, leaves nothing with
which to estimate the noise :math:`\sigma^2`, and without that estimate there are no standard
errors, no tests, and no power: the analysis simply cannot start. Step 1 is possible only
because of the orthogonality property: the main effects are unaliased with every second-order
term, so their estimates are unbiased no matter which interactions or quadratics are truly
active, which is what lets us analyse them on their own. Step 4 is where the design's one weakness is managed:
since the second-order effects are correlated among themselves, only a limited number can be
estimated together. Factor heredity (admitting an interaction only when its parent main effects
are active) is one rule for narrowing the candidates the data alone cannot fully separate; the
alternative is to keep every second-order effect as a candidate and let the F-tests choose.

This staged procedure is available in ``process_improve`` as ``analyze_omars()``: it takes any
coded two- or three-level design with its measured responses and carries out the stages above,
returning the clean main effects, the pooled error, the overall test for second-order activity,
and the selection among the second-order effects. One qualification concerns step 4: heredity is
an option, not the default. With the default settings (``interaction_heredity="none"`` and
``quadratic_heredity="none"``) every quadratic and every two-factor interaction is a candidate, and
a best-subset search adds terms until the remaining second-order variation is no longer
significant. Passing ``interaction_heredity="strong"`` gives the rule shown in the diagram,
admitting an interaction only if both of its parent main effects are active; ``"weak"`` requires
at least one active parent, and ``quadratic_heredity="strong"`` applies the same restriction to
the quadratic of each factor.

**Readings**

* Jones, B. and Nachtsheim, C.J.: "Effective Design-Based Model Selection for Definitive
  Screening Designs", *Technometrics*, **59**, 319--329, 2017.
  `doi:10.1080/00401706.2016.1234979 <https://doi.org/10.1080/00401706.2016.1234979>`__
* Hameed, M.S.I., Núñez Ares, J. and Goos, P.: "Analysis of data from orthogonal minimally
  aliased response surface designs", *Journal of Quality Technology*, **55**, 366--384, 2023.
  `doi:10.1080/00224065.2022.2151530 <https://doi.org/10.1080/00224065.2022.2151530>`__
