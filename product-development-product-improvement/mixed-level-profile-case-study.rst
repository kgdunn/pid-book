.. _APPS_mixed_level_profile_case_study:

A mixed-level split-plot design with a profile response
=======================================================

This case study draws the :ref:`design-and-analysis-of-experiments
<SECTION-design-analysis-experiments>` and :ref:`latent-variable-modelling
<SECTION_latent_variable_modelling>` chapters together on one problem and carries it from the first
design decision to the final answer. A laboratory has a working colour reagent, under review on cost
and stability, and five candidate replacements. **The question is which candidate develops colour the
same way as the incumbent, and at what process settings.** Answering it needs both halves of the book:
a design that can support the model, and a model that fits a curve rather than a single number.

The design is a sixty-run split-plot over a six-level categorical factor, the compound, and four
continuous process factors, built with the :ref:`information matrix <DOE-optimal-designs>`, the
:ref:`coordinate-exchange search <DOE-exchange-algorithms>`, a :ref:`categorical factor with several
levels <DOE-categorical-factors>`, and hard-to-change factors that force the run order. The response
is a ten-point colour-development curve, modelled with projection to latent structures so the
correlated time points are fitted jointly. From there the study tests the compound-by-factor
interactions, inverts the model, including a constrained inversion that lets the target float off the
model plane, to read which candidate reaches the incumbent's curve and at what settings, and closes
on what it would take to bring a seventh compound into the same model.

The worked example runs end to end with the ``process_improve`` library. The response here is
simulated from a known ground truth, so the effects the analysis recovers can be checked against the
values that were put in; in a real study the same code reads measured data in place of the simulation.

The problem
-----------

An analytical laboratory develops a coloured metal-chelate complex using an arylazo *chromogen*,
and reads the depth of colour as absorbance at the complex's maximum-absorbance wavelength. The
colour is not read once: it is followed as it develops, logging absorbance at ten time points from
mixing to plateau, so each run yields a ten-point **colour-development curve**. Two reagents can
reach the same final absorbance yet differ in how quickly the colour forms and whether it keeps
drifting at long times, so the whole curve, not its endpoint, is the response.

The incumbent chromogen works but is under review on cost and shelf-stability grounds. Five
candidate analogs are screened against it. The categorical factor is therefore the compound
identity, at six levels, a reference plus five single-substituent analogs of one scaffold:

.. list-table:: The six chromogens (categorical factor ``compound``)
    :widths: 12 60
    :header-rows: 1

    *   - Level
        - Chromogen
    *   - A
        - 4-(2-pyridylazo)benzene-1,3-diol (reference / incumbent)
    *   - B
        - 4-(2-pyridylazo)-6-methylbenzene-1,3-diol
    *   - C
        - 4-(2-thiazolylazo)benzene-1,3-diol
    *   - D
        - 4-(2-pyridylazo)-6-chlorobenzene-1,3-diol
    *   - E
        - 4-(5-methyl-2-pyridylazo)benzene-1,3-diol
    *   - F
        - 4-(2-quinolylazo)benzene-1,3-diol

Four continuous process factors act alongside the compound. Two of them, the co-solvent fraction
and the temperature, are slow to reset between runs (the co-solvent needs re-equilibration, the
bath needs to settle), so a fully randomized order is impractical and the design is run as a
split-plot: the two hard-to-change factors are held over a block of runs (a whole plot) while the
easy-to-change factors are reset within it.

.. list-table:: The four continuous factors
    :widths: 22 20 22 20
    :header-rows: 1

    *   - Factor
        - Low
        - High
        - Change cost
    *   - Concentration
        - 2 umol/L
        - 8 umol/L
        - easy
    *   - Co-solvent fraction
        - 5% v/v
        - 25% v/v
        - hard
    *   - pH
        - 4.0
        - 7.0
        - easy
    *   - Temperature
        - 15 degC
        - 35 degC
        - hard

The study has five questions. The first three ask whether a process factor acts *differently*
depending on which compound is used, that is, whether there is a compound-by-factor interaction on
colour intensity, for the co-solvent, the pH, and the temperature in turn. The fourth asks which
candidate's colour-development *shape* stays closest to the reference. The fifth asks what settings
deliver a target colour intensity for the chosen compound.

Building the design
-------------------

A categorical factor enters the model through indicator columns, as set out in the
:ref:`categorical-factor section <DOE-categorical-factors>`, and a squared term on such a factor is
meaningless (an indicator equals its own square). The library builds the right model automatically
when the factor is declared categorical: the continuous factors get their quadratic terms, the
compound enters as a main effect plus its interactions, and no square is attempted on the compound.
The whole design is one call to ``generate_design`` with ``design_type="i_optimal"``, a run
``budget``, the ``hard_to_change`` factors, and ``model_type="quadratic"``.

The worked example uses ``process_improve`` (``pip install 'process-improve[expt]'``); the
coordinate-exchange optimiser it calls for the I-optimal and split-plot construction is ``pyoptex``,
installed separately with ``pip install pyoptex``.

.. code-block:: python

    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    from process_improve.experiments import Factor, generate_design

    compounds = list("ABCDEF")
    cont = {"concentration": (2.0, 8.0), "co_solvent": (5.0, 25.0),
            "pH": (4.0, 7.0), "temperature": (15.0, 35.0)}
    factors = [Factor(name="compound", type="categorical", levels=compounds)] + [
        Factor(name=n, type="continuous", low=lo, high=hi) for n, (lo, hi) in cont.items()]

    np.random.seed(42)  # the coordinate exchange draws its restarts from the global RNG
    design = generate_design(factors, design_type="i_optimal", budget=60,
                             hard_to_change=["co_solvent", "temperature"],
                             model_type="quadratic")

    print(design.n_runs)  # 60
    print(design.design["compound"].value_counts())  # 9 to 11 runs per compound

    order = design.design.sort_values("RunOrder").reset_index(drop=True)
    x = np.arange(len(order))
    fig = go.Figure()
    for name in ["co_solvent", "temperature", "concentration", "pH"]:
        fig.add_scatter(x=x, y=order[name], mode="lines", line_shape="hv", name=name)
    fig.update_layout(xaxis_title="run order", yaxis_title="coded level")
    fig.show()

The sixty runs spread evenly across the six compounds, nine to eleven per compound, and the
continuous factors fill the coded range. The run order shows the split-plot structure directly. The
hard-to-change factors hold their level over long stretches, the whole plots, exactly the grouping a
split-plot is meant to produce.

.. figure:: ../figures/doe/colour-split-plot-run-order.png
    :align: center
    :width: 750px
    :alt: colour-split-plot-run-order.py

    The split-plot run order. The two hard-to-change factors (top) hold their level over blocks of
    runs, changing 8 and 10 times across the sixty runs; the two easy-to-change factors (bottom)
    are reset almost every run, changing 46 and 44 times.

Judging the design before running it
-------------------------------------

Before any colour is measured, the design can be scored on how well it will support the model, using
``evaluate_design`` on the same quadratic model. The :ref:`D-efficiency
<DOE-judging-and-comparing-designs>` summarises the information determinant
:math:`|\mathbf{X}^T\mathbf{X}|`, higher being more information per run; the I-efficiency summarises
the prediction variance averaged over the whole factor region, and the G-efficiency the single
worst-predicted point in it. The :ref:`fraction-of-design-space (FDS) curve <DOE-fds-plot>` shows how
that prediction variance is distributed, from the best-predicted point to the worst. Higher is better
for all three, but they are normalized differently and are read down a column rather than across the
row: D-efficiency scales as :math:`100\,|\mathbf{X}^T\mathbf{X}|^{1/p}/N`, while I- and G-efficiency
scale as :math:`100\,p/(N\bar{v})` with :math:`p` model terms, :math:`N` runs, and :math:`\bar{v}`
the average (or maximum) prediction variance, so the I-efficiency can read above 100 when the average
variance is small.

.. code-block:: python

    from process_improve.experiments import evaluate_design

    def score(criterion, budget):
        np.random.seed(42)
        d = generate_design(factors, design_type=criterion, budget=budget,
                            hard_to_change=["co_solvent", "temperature"],
                            model_type="quadratic")
        m = evaluate_design(d, model="quadratic",
                            metric=["d_efficiency", "i_efficiency", "g_efficiency", "fds"])
        return d, m

    fig = go.Figure()
    for criterion, colour in [("i_optimal", "#1f5fa8"), ("d_optimal", "#c0392b")]:
        for budget, dash, width in [(60, "solid", 4), (48, "dash", 2)]:
            _, m = score(criterion, budget)
            q = m["fds"]["quantiles"]
            fig.add_scatter(x=[float(k) for k in q], y=list(q.values()), mode="lines+markers",
                            line=dict(color=colour, dash=dash, width=width),
                            name=f"{criterion}, n={budget}")
    fig.update_layout(xaxis_title="Fraction of design space",
                      yaxis_title="Scaled prediction variance")
    fig.show()

Scoring the :ref:`I-optimal and D-optimal designs <DOE-optimal-designs>` at 48 and 60 runs lays out
the trade-off. The
I-optimal criterion minimizes the average prediction variance, and the D-optimal criterion
maximizes the information determinant, so each design leads on its own criterion: the D-optimal
design has the higher D-efficiency, and the I-optimal design has the higher I-efficiency and the
lower prediction variance across the region.

.. list-table:: Design quality by criterion and run count (quadratic model)
    :widths: 26 14 14 14 16 16
    :header-rows: 1

    *   - Design
        - :math:`\uparrow` D-eff
        - :math:`\uparrow` I-eff
        - :math:`\uparrow` G-eff
        - :math:`\downarrow` FDS median
        - :math:`\downarrow` FDS max
    *   - I-optimal, n = 60
        - 15.4
        - 159
        - 51.8
        - 0.40
        - 1.29
    *   - I-optimal, n = 48
        - 13.9
        - 132
        - 19.6
        - 0.57
        - 4.26
    *   - D-optimal, n = 60
        - 17.9
        - 106
        - 63.0
        - 0.63
        - 1.06
    *   - D-optimal, n = 48
        - 16.8
        - 80
        - 27.1
        - 1.01
        - 3.07

.. figure:: ../figures/doe/colour-fds-curves.png
    :align: center
    :width: 720px
    :alt: colour-fds-curves.py

    Fraction-of-design-space curves. Each curve reads as the fraction of the region (horizontal)
    whose scaled prediction variance is at or below a given level (vertical). The I-optimal design
    at 60 runs is lowest over most of the region; near the worst-case (right) end the D-optimal
    design at 60 runs edges below it, matching its higher G-efficiency. The D-optimal design at 48
    runs is highest, with a long tail of poorly-predicted points near the region's edge.

The purpose here is to predict and compare colour across the whole factor region, not to estimate
a single coefficient as precisely as possible, so the I-optimal criterion matches the goal, and the
sixty-run design is carried forward. The forty-eight-run designs cost twelve fewer runs but leave
only 8 residual degrees of freedom against 20, and their worst-case prediction variance is several
times higher: the choice between them is the usual one between budget and precision.

The colour-development response
-------------------------------

Each run produces a ten-point curve. For this worked example the curves are generated from a known
ground truth: the colour amplitude is a compound-specific linear function of the coded factors, and
the curve shape is a common rise-to-plateau plus a compound-specific late drift. Compound A, the
reference, has no late drift; the analogs drift by varying amounts.

.. code-block:: python

    time_points = np.arange(10)
    noise_sd = 0.03  # measurement-noise standard deviation
    ref = 1.0 - np.exp(-time_points / 2.0);        ref = ref / ref.max()
    tail = np.clip((time_points - 4) / 5.0, 0, None);  tail = tail / tail.max()

    # ground truth: late-time drift, and amplitude slopes for co-solvent, pH, temperature
    truth = {
        "A": (0.00, -0.05, -0.06, +0.02),
        "B": (0.05, -0.08, -0.10, +0.03),
        "C": (0.20, -0.20, -0.28, +0.12),
        "D": (0.30, -0.25, -0.30, +0.14),
        "E": (0.35, -0.10, -0.08, +0.05),
        "F": (-0.10, -0.15, -0.22, -0.10)}

    rng = np.random.default_rng(20260710)
    rows = []
    for _, r in design.design.iterrows():
        drift, s_co, s_ph, s_tp = truth[r["compound"]]
        amp = max(1.0 + 0.35 * r["concentration"] + s_co * r["co_solvent"]
                  + s_ph * r["pH"] + s_tp * r["temperature"], 0.05)
        rows.append(amp * np.clip(ref + drift * tail, 0, None)
                    + rng.normal(0, noise_sd, time_points.size))
    curves = pd.DataFrame(np.vstack(rows), columns=[f"t{t}" for t in time_points],
                          index=design.design.index)

    mean_curve = pd.concat([design.design["compound"], curves], axis=1).groupby("compound").mean()
    fig = go.Figure()
    for c in compounds:
        fig.add_scatter(x=time_points, y=mean_curve.loc[c], mode="lines+markers", name=c)
    fig.update_layout(xaxis_title="time point", yaxis_title="mean absorbance")
    fig.show()

The mean curves share the early rise and separate at long times. Compounds A and B plateau together
and stay flat, while D and E keep climbing and F settles slightly lower. That late-time spread is
the shape difference the fourth question is about, and it is invisible in the endpoint alone.

.. figure:: ../figures/doe/colour-development-curves.png
    :align: center
    :width: 720px
    :alt: colour-development-curves.py

    Mean colour-development curve for each chromogen (A to C solid, D to F dashed). The curves rise
    together to about the fifth time point, then diverge: the reference A and the analog B level off
    together, while D and E keep developing colour and F drifts down.

Modelling the profile with PLS
------------------------------

A ten-point curve has ten correlated responses, so a separate regression per time point would
ignore that the points move together. A projection-to-latent-structures (PLS) model regresses all
ten at once against the factors, using a few latent components that capture the shared movement.

The factor block ``X`` has to be fully numeric, so the six-level compound is expanded into indicator
columns, one per level: each run takes a single 1 in the column for its compound and 0 in the others.

.. code-block:: python

    pd.get_dummies(pd.Series(compounds, name="compound")).astype(int)

.. list-table:: Indicator coding of the six compound levels
    :widths: 20 10 10 10 10 10 10
    :header-rows: 1
    :stub-columns: 1

    *   - Compound
        - A
        - B
        - C
        - D
        - E
        - F
    *   - A
        - 1
        - 0
        - 0
        - 0
        - 0
        - 0
    *   - B
        - 0
        - 1
        - 0
        - 0
        - 0
        - 0
    *   - C
        - 0
        - 0
        - 1
        - 0
        - 0
        - 0
    *   - D
        - 0
        - 0
        - 0
        - 1
        - 0
        - 0
    *   - E
        - 0
        - 0
        - 0
        - 0
        - 1
        - 0
    *   - F
        - 0
        - 0
        - 0
        - 0
        - 0
        - 1

.. _profile-coding-intro:

All six indicators cannot enter the model alongside the intercept: they sum to one in every row, so
one is redundant and :math:`\mathbf{X}^T\mathbf{X}` is singular (the :ref:`categorical-factor section
<DOE-categorical-factors>` sets this out). The redundancy is removed in one of two common ways, and
the choice fixes what each compound coefficient means:

- *Reference (treatment) coding* drops one level. Taking A as the reference leaves the five columns
  B to F; a run of compound A is all zeros (that is, carried by the intercept) across all columns for
  B, C, D, E and F. Each coefficient is then that compound's **difference from A**: the change in
  colour from switching the chemical to that compound while every continuous factor, the concentration
  included, is held at the same value.
- *Sum (effects) coding* keeps a contrast for all levels except one (so five of the six compounds
  here), with the compound effects constrained to sum to zero across the six levels, so the omitted
  compound is the negative sum of the other five. Each compound's coefficient is then its effect
  expressed as a difference from a hypothetical average compound (the mean of all six), and a
  continuous factor's main effect is its average slope across the six compounds.

Either way five numbers describe the compound, and the two codings fit the same model: the same
predictions, the same :math:`R^2`, and the same interaction tests. Only the coefficients, and their
standard errors, move with the choice. The main-effects PLS just below uses reference coding (where
we drop A); in the interaction analysis later we will use and show the sum coding, and in a
:ref:`later section <profile-categorical-coding>` we compare the difference the choice makes.

.. code-block:: python

    dummies = pd.get_dummies(design.design["compound"], prefix="cmp").astype(float)
    X = pd.concat([design.design[list(cont)].astype(float), dummies.drop(columns=["cmp_A"])], axis=1)

The four continuous factors keep their coded :math:`-1` to :math:`+1` values, and the compound
contributes via the five indicators B to F. This is called a main-effects model: each compound shifts
the colour by a fixed amount through its indicator, and the continuous factors act the same way for
every compound. The response columns are on different scales (the early points carry far less variance
than the plateau), so the blocks are standardized before fitting. ``PLS(scale=True)`` does this
internally, mean-centering and scaling both the factor block and the response block to unit variance,
but we return and show predictions on the original absorbance scale, so raw ``X`` and raw ``curves``
can be passed straight in. Fitting it, and reading the scores and the
:math:`\mathbf{W}^*`/:math:`\mathbf{C}` loadings:

.. code-block:: python

    from plotly.subplots import make_subplots
    from process_improve.multivariate.methods import PLS

    pls = PLS(n_components=5, scale=True).fit(X, curves)
    print(pls.r2_cumulative_)  # cumulative R2Y by component: 0.78, 0.81, 0.82, 0.82, 0.83

    scores = np.asarray(pls.scores_)  # X scores, one row per run
    wstar = pls.direct_weights_  # W*: X-space weights, indexed by factor
    cw = pls.y_weights_  # C: Y-space weights, indexed by time point

    fig = make_subplots(rows=1, cols=2, subplot_titles=("scores", "W* and C loadings"))
    for c in compounds:
        m = (design.design["compound"] == c).to_numpy()
        fig.add_scatter(x=scores[m, 0], y=scores[m, 1], mode="markers", name=c, row=1, col=1)
    fig.add_scatter(x=wstar.iloc[:, 0], y=wstar.iloc[:, 1], mode="markers+text",
                    text=list(wstar.index), name="factor (W*)", row=1, col=2)
    fig.add_scatter(x=cw.iloc[:, 0], y=cw.iloc[:, 1], mode="lines+markers+text",
                    text=list(cw.index), name="time point (C)", row=1, col=2)
    fig.show()

The model reports its own goodness of fit through ``pls.r2_cumulative_``, the cumulative
:math:`R^2_Y` as each component is added: 0.78 after the first component and 0.83 after five, so one
component already
captures most of the response variation, and the ten time points move together along a single main
direction.

The score plot places each run in the latent space. The runs spread across it rather than clustering
by compound, because the optimal design was chosen to fill the factor region. The relationship
between the factors and the response is read instead from the loadings plot, which places the factor
weights :math:`\mathbf{W}^*` and the response-point weights :math:`\mathbf{C}` on the same axes. The
first component is an amplitude direction: the concentration sits with all ten time points at high
values in the first component, because raising the concentration lifts the whole curve. The second
component is
a late-development direction: the compound indicators spread along it, with E and D (which keep
developing colour) opposite F and B, and the late time point ``t9`` falls on the same side as the
compounds that drift upward. A factor and a response point lying in the same direction means that
factor raises the colour at those times.

Since reference (treatment) coding is used here, compound A is the baseline: a run of A is all zeros
across the columns for B to F, absorbed into the intercept, so A has no indicator column and no marker
in the loadings plot. Each plotted compound weight, B to F, is that compound's difference from A.
Compound A still appears in the score plot, since every run has a score; only its compound *weight* is
absent.

.. figure:: ../figures/doe/colour-pls-scores-loadings.png
    :align: center
    :width: 760px
    :alt: colour-pls-scores-loadings.py

    Left: the first two PLS scores, one point per run, coloured by chromogen. Right: the factor
    weights :math:`\mathbf{W}^*` and the response-point weights :math:`\mathbf{C}` on the same axes.
    Component 1 is an amplitude direction (concentration with all ten time points); component 2
    separates the compounds by late-time development, with ``t9`` on the side of the compounds that
    keep developing colour. Compound A, the reference level, has no indicator column and so no point
    in the loadings panel.

Testing the compound-by-factor interactions for colour peak, using two models
-----------------------------------------------------------------------------

Now we can ask how the co-solvent, the pH, or the temperature moves the colour for different
compounds. Reducing each curve to its peak absorbance gives a single response, and two models are
fitted to it: an analysis of variance and a PLS regression, both with explicit compound-by-factor
interaction terms. The compound is written with sum-to-zero (effects) coding through
``C(compound, Sum)``, so each compound effect is a departure from a hypothetical average compound;
the formula validator accepts the patsy contrast helper directly. F-tests on the interaction terms
answer the first three questions, and the two fits are then set side by side on the peak to show they
agree.

.. code-block:: python

    from process_improve.experiments import analyze_experiment

    adf = design.design[["compound"] + list(cont)].copy()
    adf["compound"] = adf["compound"].astype(str)
    adf["peak"] = curves.max(axis=1).to_numpy()

    rhs = ("C(compound, Sum)*co_solvent + C(compound, Sum)*pH "
           "+ C(compound, Sum)*temperature + concentration")
    res = analyze_experiment(adf, response_column="peak", model="peak ~ " + rhs,
                             analysis_type=["anova"], coding="coded")
    print(res["model_summary"]["r_squared"])  # 0.989
    print(pd.DataFrame(res["anova_table"]))

The model explains 99% of the variation in peak colour. All three interaction terms are significant:
the compound-by-pH term is the strongest (:math:`F = 28`, :math:`p = 2 \times 10^{-11}`), then
compound-by-temperature (:math:`F = 18`) and compound-by-co-solvent (:math:`F = 15`), each with
:math:`p < 10^{-7}`.

Each of those interaction terms is not a single coefficient but five. Sum-to-zero coding gives each of
the six compounds a departure from the average, and the sixth is fixed by the other five, so a
compound-by-factor interaction carries five free coefficients, one short of the six compounds. The
F-test is a single joint test of all five at once: it weighs the drop in the residual sum of squares
when the five interaction coefficients are added against the residual that remains, so a significant F
says the compounds' slopes on that factor are not all equal, without pointing to which compound
differs. There is no universal F cutoff: the threshold depends on the numerator degrees of freedom
(five here), the residual degrees of freedom, and the significance level. All three joint tests clear
it well. This answers the first three questions: the process factors do act differently across
compounds, which is how the response was constructed. As the :ref:`categorical-factor section
<DOE-categorical-factors>` noted, these interaction terms are also what make a robust operating point
reachable, a setting where the compounds give nearly the same colour, which the fifth question would
search for.

The same interaction terms can be handed to PLS with the peak as its single response. Building the
model matrix from the formula right-hand side (dropping the intercept, since ``PLS`` centres the
columns) and fitting three components, its ``beta_coefficients_`` line up against the least-squares
coefficients term by term:

.. code-block:: python

    from patsy import dmatrix

    X_int = dmatrix(rhs, adf, return_type="dataframe").drop(columns=["Intercept"])
    print(X_int.shape)  # (60, 24): 24 model terms

    ols = analyze_experiment(adf, response_column="peak", model="peak ~ " + rhs,
                             analysis_type=["coefficients"])["coefficients"]
    ols = {c["term"]: c["coefficient"] for c in ols}

    pls_peak = PLS(n_components=3, scale=True).fit(X_int, adf[["peak"]])
    beta = pls_peak.beta_coefficients_.iloc[:, 0]

    coef = pd.DataFrame({"OLS": [ols[t] for t in X_int.columns], "PLS": beta.to_numpy()},
                        index=X_int.columns).sort_values("OLS")
    fig = go.Figure()
    fig.add_scatter(x=coef["OLS"], y=coef.index, mode="markers", name="least squares")
    fig.add_scatter(x=coef["PLS"], y=coef.index, mode="markers", name="PLS")
    fig.show()

The expanded model matrix ``X_int`` has 24 terms: the five compound contrasts, the three continuous
factors that interact with the compound, their fifteen interaction columns, and the concentration.
Three components is well short of that full rank, yet on the single peak response the PLS and
least-squares coefficients differ by at most about 0.03 across the 24 terms. The concentration
coefficient (about 0.40, it raises the peak for every compound) and the pH main effect (about
:math:`-0.21`, the average pH slope) match closely; the three-component PLS pulls a few of the smaller
interaction terms toward zero, the shrinkage from describing the response with fewer directions than
the model has terms.

The five largest and five smallest least-squares coefficients, with the three-component PLS estimate
beside each and the least-squares standard error, t-statistic, and p-value (the fourteen middle terms
are omitted):

.. list-table:: PLS and least-squares coefficients for the peak colour intensity (largest and smallest)
    :widths: 26 12 16 14 10 14
    :header-rows: 1

    *   - Term
        - PLS
        - Least squares
        - Std. error
        - t
        - p-value
    *   - ``concentration``
        - +0.401
        - +0.395
        - 0.010
        - +40.8
        - <0.001
    *   - ``cmpE``
        - +0.209
        - +0.215
        - 0.019
        - +11.5
        - <0.001
    *   - ``cmpD``
        - +0.151
        - +0.143
        - 0.020
        - +7.3
        - <0.001
    *   - ``cmpA:pH``
        - +0.128
        - +0.123
        - 0.021
        - +5.8
        - <0.001
    *   - ``cmpD:temperature``
        - +0.094
        - +0.112
        - 0.022
        - +5.0
        - <0.001
    *   - (14 terms omitted)
        -
        -
        -
        -
        -
    *   - ``cmpC:pH``
        - -0.134
        - -0.146
        - 0.021
        - -7.0
        - <0.001
    *   - ``co_solvent``
        - -0.152
        - -0.157
        - 0.011
        - -14.9
        - <0.001
    *   - ``cmpD:pH``
        - -0.134
        - -0.166
        - 0.023
        - -7.1
        - <0.001
    *   - ``cmpD:co_solvent``
        - -0.151
        - -0.177
        - 0.026
        - -6.8
        - <0.001
    *   - ``pH``
        - -0.205
        - -0.209
        - 0.010
        - -21.1
        - <0.001

.. figure:: ../figures/doe/colour-coefficient-comparison.png
    :align: center
    :width: 620px
    :alt: colour-coefficient-comparison.py

    Coefficients for the peak colour intensity from ordinary least squares and from PLS with three
    components, fitted to the same interaction model under sum coding. The bands are :math:`\pm` one
    standard error on the least-squares estimate; the PLS point falls inside the band for all but two
    terms, so the shrinkage is small next to the estimation uncertainty. Terms are sorted by the
    least-squares coefficient; the ``cmp`` prefix marks a compound's departure from the average under
    sum coding. Reference coding, measuring each compound against A, would widen the gap between the
    two fits.

The PLS point falls inside the :math:`\pm` one-standard-error band for all but two of the 24 terms
(the largest gap is 1.4 standard errors), so the low-rank shrinkage is small next to the estimation
uncertainty. On this single peak response least squares and PLS are interchangeable. Among the terms
not shown, four compound-specific temperature and co-solvent slopes are not resolved individually at
this run count (p-values from 0.07 to 0.37), though the joint F-test found the interaction present for
the set.

The interaction model on the full curve
---------------------------------------

When multiple correlated responses are worth modelling, fitting a separate model to each is laborious,
and it throws away the fact that the responses move together. PLS builds one model with the entire
colour profile as the response. The interaction terms just fitted to the peak are handed to PLS again,
now against all ten time points at once, so the model returns a predicted development curve rather than
a single number:

.. code-block:: python

    pls_int = PLS(n_components=5, scale=True).fit(X_int, curves)
    print(pls_int.r2_cumulative_)  # 0.77, 0.85, 0.88, 0.90, 0.91

Fitted to the full curve, the interaction model's cumulative :math:`R^2_Y` rises from 0.77 at one
component to 0.91 at five, above the main-effects model's 0.83, because the compound-specific slopes on
co-solvent, pH and temperature, the interactions the analysis of variance found significant, are now in
the factor block. PLS fits these terms to all ten time points at once, returning a predicted
development curve, where the analysis of variance fitted the same terms to the single peak of each
curve.

How many components to keep is a modelling choice, guided by the in-sample :math:`R^2_Y` and the
cross-validated :math:`Q^2_Y`. The :math:`Q^2_Y` is the fraction of the response variation the model
predicts for runs it did not see: leave out each run in turn, refit, and predict the held-out curve.
``pls.cross_validate`` returns a per-response :math:`Q^2_Y`; averaged over the ten time points at
each number of components:

.. code-block:: python

    q2 = []
    for a in range(1, 6):
        cv = PLS(n_components=a, scale=True).fit(X_int, curves).cross_validate(X_int, curves, cv="loo")
        q2.append(float(cv["q_squared"].mean()))
    print(np.round(q2, 2))  # 0.52, 0.78, 0.78, 0.77, 0.80

.. list-table:: In-sample :math:`R^2_Y` and leave-one-out :math:`Q^2_Y` by component
    :widths: 22 26 26
    :header-rows: 1

    *   - Component
        - :math:`R^2_Y` (cumulative)
        - :math:`Q^2_Y` (leave-one-out)
    *   - 1
        - 0.77
        - 0.52
    *   - 2
        - 0.85
        - 0.78
    *   - 3
        - 0.88
        - 0.78
    *   - 4
        - 0.90
        - 0.77
    *   - 5
        - 0.91
        - 0.80

:math:`R^2_Y` rises with every component, as it must: each component can only reduce the residual on
the data the model is fitted to. The :math:`Q^2_Y` here should be read with caution, because this is
a designed experiment. A design places its runs to span the whole factor region, with few or no
repeats, so leaving a run out removes a location the remaining runs do not surround, and predicting
it is closer to extrapolation than to interpolation. A low :math:`Q^2_Y` then reflects the spread of
the design as much as any fault in the model. Where a design has replicate runs at some locations,
cross-validating over those replicates is informative, though still to be read with care; with no
replicates, as here, a modest :math:`Q^2_Y` is expected.

Read with that caution, the table still shows :math:`R^2_Y` rising with every added component while
:math:`Q^2_Y` changes little beyond the second: the later components raise the in-sample fit without
improving prediction for held-out runs. Three components are kept for the analysis that follows,
enough to carry the interactions without adding directions the cross-validation does not support. At
three components the interaction model's :math:`R^2_Y` is 0.88.

Scores and loadings of the interaction model
--------------------------------------------

The full-curve fit above settled on three components; the score and loading plots shown before that
were for the main-effects model. Refitting the interaction model to the whole profile at three
components gives its scores and loadings for the expanded model:

.. code-block:: python

    pls_full = PLS(n_components=3, scale=True).fit(X_int, curves)
    print(pls_full.r2_cumulative_)  # 0.77, 0.85, 0.88

    tscore = np.asarray(pls_full.scores_)  # X scores, one row per run
    wstar = pls_full.direct_weights_  # W*: the 24 model terms
    cw = pls_full.y_weights_  # C: the ten time points

    palette = ["#1f5fa8", "#c0392b", "#2e8b57", "#8e44ad", "#d68910", "#17a2b8"]
    colour_of = dict(zip(compounds, palette))

    # Score plot: four encodings on one point. Colour is the compound (as before); marker shape is
    # the pH level (down triangle low, circle high); marker size grows with the concentration; and
    # the co-solvent is an open, outline-only marker at the low setting and a filled marker at the
    # high setting (the "-open" symbol suffix draws the outline only).
    base = np.where(adf["pH"] < 0, "triangle-down", "circle")
    symbol = np.where(adf["co_solvent"] < 0, np.char.add(base, "-open"), base)
    size = 8 + 5 * (adf["concentration"] + 1)  # coded concentration in [-1, 1]

    fig = make_subplots(rows=1, cols=2, subplot_titles=("scores", "W* and C loadings"))
    for c in compounds:
        m = (adf["compound"] == c).to_numpy()
        fig.add_scatter(x=tscore[m, 0], y=tscore[m, 1], mode="markers", name=c, row=1, col=1,
                        marker=dict(color=colour_of[c], symbol=symbol[m], size=size[m],
                                    line=dict(width=1, color=colour_of[c])))

    # Loadings: each compound term (main effect or interaction) takes its compound's colour, the
    # other factor terms are black, and the ten time points are red.
    def term_colour(name):
        for c in compounds:
            if f"[S.{c}]" in name:
                return colour_of[c]
        return "black"

    fig.add_scatter(x=wstar.iloc[:, 0], y=wstar.iloc[:, 1], mode="markers+text",
                    text=list(wstar.index), name="model term (W*)", row=1, col=2,
                    marker=dict(color=[term_colour(t) for t in wstar.index]))
    fig.add_scatter(x=cw.iloc[:, 0], y=cw.iloc[:, 1], mode="markers+text",
                    text=list(cw.index), name="time point (C)", row=1, col=2,
                    marker=dict(color="#c0392b"))
    fig.show()

The model keeps three components, the number chosen from the leave-one-out :math:`Q^2_Y` above:
enough to carry the interactions without adding directions the cross-validation does not support.
Taken over the ten time points jointly, its :math:`R^2_Y` is 0.88. A single joint number can hide a
profile that is fitted well in some places and poorly in others, so it is worth reading the fit one
time point at a time. ``r2y_per_variable_`` gives the in-sample :math:`R^2_Y` per response (its last
column, at three components), and the leave-one-out :math:`Q^2_Y` per response comes from
``cross_validate``:

.. code-block:: python

    r2y = pls_full.r2y_per_variable_.iloc[:, -1]  # cumulative R2Y per time point, three components
    q2y = pls_full.cross_validate(X_int, curves, cv="loo")["q_squared"]  # leave-one-out Q2Y per point
    print(pd.DataFrame({"R2Y": np.round(r2y, 2), "Q2Y": np.round(q2y, 2)}))

.. list-table:: :math:`R^2_Y` and leave-one-out :math:`Q^2_Y` per time point (three-component model)
    :widths: 26 18 22
    :header-rows: 1

    *   - Time point
        - :math:`R^2_Y`
        - :math:`Q^2_Y`
    *   - t0
        - 0.16
        - -0.27
    *   - t1
        - 0.95
        - 0.89
    *   - t2
        - 0.96
        - 0.91
    *   - t3
        - 0.97
        - 0.90
    *   - t4
        - 0.97
        - 0.91
    *   - t5
        - 0.97
        - 0.92
    *   - t6
        - 0.97
        - 0.91
    *   - t7
        - 0.96
        - 0.90
    *   - t8
        - 0.94
        - 0.89
    *   - t9
        - 0.92
        - 0.86

From ``t1`` onward every point is explained to between 0.92 and 0.97; only ``t0`` is low, at 0.16. At
``t0`` the colour has barely begun to form, so the absorbance is near zero and mostly measurement
noise, with little systematic variation for any factor to explain. The developed part of the curve,
which is what the study is about, is fitted well throughout; the joint 0.88 is held down by that one
near-zero point.

Colour still marks the compound, so the six chromogens are told apart as before. The added encoding
puts three more factors on the same axes: the marker shape is the pH level (a down triangle for the
low setting, a circle for the high setting), the marker size is proportional to the concentration (a
larger marker is a higher concentration), and the marker fill marks the co-solvent (an open,
outline-only marker at the low setting, a filled marker at the high). A single run now shows its
compound together with its pH, concentration, and co-solvent at a glance, so the score plot can be
read against the factors
directly rather than by cross-referencing a separate table of run settings. In the loadings panel each
compound term carries its compound's colour, so a compound and its interaction terms are followed
across the plot; the continuous-factor terms are black and the response points red.

Component 1 is again the amplitude direction, and the encoding shows what drives it. The
concentration weight sits far out on component 1 with all ten time points, so a run's component-1
score tracks how high its whole curve rises. The large markers (high concentration) fall to the right
and the small markers to the left: the concentration and the first score correlate at 0.74, and the
mean first score moves from :math:`-0.96` at the low concentration to :math:`+0.92` at the high. The
down triangles (low pH) also lie to the right of the circles, because a lower pH raises the
colour for this chelate; the mean first score is :math:`+0.58` at low pH against :math:`-0.53` at
high. Reading shape and size together, the runs high on component 1 are the high-concentration,
low-pH runs, which is where the deepest colour is expected.

Component 2 carries only eight percent of the response variation, and the loadings place the
compound-by-temperature terms at one end of it and the pH and concentration terms at the other, so it
is a weaker, temperature-leaning direction. One run stands apart low on component 2: its encoding
reads as compound F at the low pH and high concentration, an unusual corner of the region for that
compound and a borderline outlier (Hotelling's :math:`T^2` of 26) that later sections discuss. A score
plot is where such a run shows up, and the encoding names the run's settings without a lookup.

.. figure:: ../figures/doe/colour-pls-interaction-scores-loadings.png
    :align: center
    :width: 780px
    :alt: colour-pls-interaction-scores-loadings.py

    Left: the first two PLS scores of the interaction model on the full curve, one point per run.
    Colour is the chromogen, marker shape is the pH level (down triangle low, circle high), marker
    size is proportional to the concentration, and the marker fill marks the co-solvent (open,
    outline-only low; filled high). High-concentration and low-pH runs sit
    to the right along component 1, the amplitude direction. Right: the W* weights for the 24 model
    terms and the C weights for the ten time points on the same axes. Each compound term is coloured
    like its compound in the score plot, the continuous-factor terms are black, and the time points
    are red. Concentration and all ten time points sit together at high component 1; the
    compound-by-temperature terms separate along component 2.

A related route to a curve response takes a different order of operations. Functional data analysis,
as offered in JMP Pro's Functional Data Explorer and its functional design of experiments, first
fits each measured curve with a basis expansion (B-splines by default, with P-splines, a Fourier
basis, or wavelets as alternatives), then reduces the fitted curves to a few *functional principal
components*: uncorrelated shape functions whose per-curve scores summarise the profile. Those scores
are modelled against the design factors, and because the components reconstruct the curve,
predicting the scores predicts the whole profile. PLS reaches the profile in one step, finding
latent directions that are at once predictable from the factors and descriptive of the response. The
functional-data route separates the two steps: describe the curve shape first from the responses
alone, then relate that description to the factors. Which is more convenient depends on the study;
both return a model that maps the factors to a predicted curve.

Model diagnostics: SPE and Hotelling's T2
-----------------------------------------

Before the model is used to answer the fourth question, it is worth checking where its own runs sit
relative to it. Two diagnostics summarise that. Hotelling's :math:`T^2` measures how far a run lies
from the centre *within* the model plane, scaled by the score spread. The squared prediction error
(SPE) is the summed squared residual *off* the plane, the part of the ten-point curve the three
components do not reconstruct; ``process_improve`` reports its square root in ``spe_``, so the SPE
values quoted here are the run's off-plane distance on the absorbance scale. Each has a 95% limit,
from ``hotellings_t2_limit`` and ``spe_limit``.

New rows are needed here and in the inversion that follows, so a small helper builds a model-matrix
row for one setting with the same coding as the fitted matrix:

.. code-block:: python

    from patsy import build_design_matrices

    info = dmatrix(rhs, adf, return_type="dataframe").design_info

    def encode(compound, concentration, co_solvent, pH, temperature):
        row = pd.DataFrame({"compound": [compound],
                            "concentration": [concentration],
                            "co_solvent": [co_solvent],
                            "pH": [pH],
                            "temperature": [temperature]})
        return build_design_matrices([info], row, return_type="dataframe")[0].drop(columns=["Intercept"])

The fourth question asks which candidate develops colour like the reference chromogen A. To make that
precise, take chromogen A at the centre point, the nominal mid-range value of every continuous factor,
as the *goal*: the colour-development profile to reproduce. Projecting the goal onto the model gives
its score and its own SPE and :math:`T^2`, so it can be checked the same way as any run before it is
used. The projection is ``diagnose``, which returns the scores, SPE, :math:`T^2` and predicted curve
for new rows:

.. code-block:: python

    goal_x = encode("A", concentration=0, co_solvent=0, pH=0, temperature=0)
    goal = pls_full.diagnose(goal_x)
    print(float(goal.spe.iloc[0]))  # SPE: 1.7
    print(float(goal.hotellings_t2.iloc[0]))  # T2: 0.05

    t2 = pls_full.hotellings_t2_.iloc[:, -1]  # per-run T2 at three components
    spe = pls_full.spe_.iloc[:, -1]  # per-run SPE at three components
    print(pls_full.hotellings_t2_limit(), pls_full.spe_limit())  # 8.7, 6.5

    # Same four-way encoding as the score plot (colour_of, symbol, size defined above), so the same
    # run is trackable across the two figures: colour = compound, shape = pH, size = concentration,
    # open/filled = co-solvent.
    fig = go.Figure()
    for c in compounds:
        m = (design.design["compound"] == c).to_numpy()
        fig.add_scatter(x=t2[m], y=spe[m], mode="markers", name=c,
                        marker=dict(color=colour_of[c], symbol=symbol[m], size=size[m],
                                    line=dict(width=1, color=colour_of[c])))
    fig.add_scatter(x=[float(goal.hotellings_t2.iloc[0])], y=[float(goal.spe.iloc[0])],
                    mode="markers", name="goal: A at centre",
                    marker=dict(symbol="star", size=16, color="black"))
    fig.add_vline(x=pls_full.hotellings_t2_limit(), line_dash="dash")
    fig.add_hline(y=pls_full.spe_limit(), line_dash="dash")
    fig.update_layout(xaxis_title="Hotelling's T2", yaxis_title="SPE")
    fig.show()

The goal's SPE is 1.7 and its :math:`T^2` is 0.05, both well inside the 95% limits of 6.5 and 8.7. It
sits in the region the design covered, so the model's prediction there can be used as an inversion
target. Most of the sixty runs also fall inside both limits. The exceptions, four beyond the
:math:`T^2` limit and five beyond the SPE limit, are all compound F. Those outliers are, somewhat
surprisingly, a property of the sum-based coding used for the compound, not of F particularly. The
:ref:`next section <profile-categorical-coding>` writes the same model in three different ways and
shows the outliers move from F to another level, or disappear, as the coding changes. No matter which
coding is used, we find chromogen A projects to a low-leverage, well-reconstructed point (its
:math:`T^2` stays near or below 0.1 and its SPE between about 1 and 2).

.. figure:: ../figures/doe/colour-pls-t2-spe.png
    :align: center
    :width: 680px
    :alt: colour-pls-t2-spe.py

    Hotelling's :math:`T^2` against SPE for the sixty runs, with the 95% limits as dashed lines. Each
    run carries the same encoding as the interaction score plot (colour = chromogen, shape = pH, size
    = concentration, open/filled = co-solvent), so the same run can be tracked across the two figures.
    A run in the lower-left rectangle is within both limits. Several compound-F runs cross the limits,
    a consequence of F being the omitted sum-coding level rather than a fault in those runs. The
    reference goal, chromogen A at the centre point (star), sits well inside both limits, so its
    predicted profile can be used as an inversion target.

.. _profile-categorical-coding:

Coding the categorical factor
-----------------------------

The compound factor has entered the models through two codings already: reference coding (where A is
dropped) for the main-effects PLS model, and sum-to-zero coding, written ``C(compound, Sum)``, in the
interaction analysis. The diagnostics here raised it because it seemed suspicious that every outlier
belonged to the omitted sum-coding level. So we write the model with other codings to verify if it was
truly F, or the choice of coding.

Sum coding and treatment coding were both set out :ref:`earlier <profile-coding-intro>`: sum coding
makes each column a compound's departure from the average of all six, with one level omitted and
carried as the negative sum of the other five; treatment coding makes each column a compound's
difference from a reference level, here A, the all-zero row. A third coding is added here for the
comparison:

- **Cell-means coding**, ``0 + C(compound)``: every compound has its own indicator column, with no
  intercept and no omitted level.

The UCLA statistical consulting group's `coding systems for categorical variables
<https://stats.oarc.ucla.edu/spss/faq/coding-systems-for-categorical-variables-in-regression-analysis/>`__
page lays out these and further schemes with worked contrast matrices.

As an aside, all three span the same model space: any fit written in one can be rewritten in the
others, and a
full-rank ordinary least squares fit returns the same predictions whichever is used. A small
illustration, a three-level factor and one continuous factor, makes the point and shows where it
stops holding:

.. code-block:: python

    rng = np.random.default_rng(0)
    n = 30
    g = np.array(["A"] * 11 + ["B"] * 10 + ["C"] * 9); rng.shuffle(g)
    xcol = rng.normal(size=n)
    truth = {"A": 0.0, "B": 1.0, "C": -0.5}
    y = np.array([truth[v] for v in g]) + 0.7 * xcol + 0.1 * rng.normal(size=n)
    demo = pd.DataFrame({"g": g, "x": xcol}); ydf = pd.DataFrame({"y": y})

    X_sum = dmatrix("C(g, Sum) + x", demo, return_type="dataframe").drop(columns=["Intercept"])
    X_trt = dmatrix("C(g, Treatment) + x", demo, return_type="dataframe").drop(columns=["Intercept"])
    for a in (1, 2, 3):  # three model terms, so three components is full rank
        p_sum = PLS(n_components=a, scale=True).fit(X_sum, ydf).predictions_
        p_trt = PLS(n_components=a, scale=True).fit(X_trt, ydf).predictions_
        print(a, float(np.max(np.abs(np.asarray(p_sum) - np.asarray(p_trt)))))
    # 1 -> 0.37, 2 -> 0.17, 3 -> 0.00

The full-rank ordinary least squares predictions match to :math:`10^{-15}` across the two codings. A
PLS kept at one or two components does not: its predictions differ by 0.37 and 0.17 between sum and
treatment coding, and only at three components, which is full rank for a three-term model, do they
agree. The reason is in how each method builds its fit. Ordinary least squares projects the response
onto the column space of the model, and that subspace is the same for every coding, so the fitted
values are identical.

.. admonition:: Projection onto the column space

    The columns of the model matrix span a flat subspace, a "plane" through the origin, inside the
    space in which each of the runs is one axis. That plane holds every fitted-value vector the model
    can produce. The data vector :math:`\mathbf{y}` usually lies off it, so least squares takes the
    fitted values :math:`\hat{\mathbf{y}}` as the closest point on the plane: the foot of the
    perpendicular dropped from :math:`\mathbf{y}`, the residual being that perpendicular. Sum,
    treatment, and cell-means coding are three bases for the *same* plane, and a perpendicular
    projection depends only on the plane, not on the basis. So :math:`\hat{\mathbf{y}}` is identical
    under all three codings; only the coefficients, its coordinates in the chosen basis, change.

PLS builds its components to :ref:`maximise the covariance <LVM_PLS_mathematical_interpretation>`
between a score direction and the response; the leading directions depend on the actual numbers in the
model matrix, which the coding sets, so a PLS truncated below full rank keeps a coding-specific
summary. Scaling the columns changes their relative variance, and so changes which covariance
directions the early components take up; that centring and scaling are consequential choices in a
component model, not neutral preprocessing, is the subject of `Bro and Smilde (2003)
<https://literature.learnche.org/item/36/centering-and-scaling-in-component-analysis>`__. At full rank
the truncation is gone and PLS spans the same space as least squares, so the dependence disappears;
below full rank it remains.

The interaction model here keeps three of a possible twenty-four components, well below full rank, so
the coding has an effect. Its cumulative :math:`R^2_Y` at three components is 0.88 under sum coding,
0.90 under treatment coding, and 0.91 under cell-means coding: the same model space, but a
rank-three truncation keeps a different part of it in each case.

The clearest place to see the effect is the leverage diagnostic. Refitting the three-component model
under each coding and reading Hotelling's :math:`T^2` per run:

.. code-block:: python

    rhs_sum = rhs  # C(compound, Sum)*... from earlier
    rhs_trt = rhs.replace("Sum", "Treatment")
    rhs_cell = ("0 + C(compound)*co_solvent + C(compound)*pH "
                "+ C(compound)*temperature + concentration")

    def fit_coding(formula, order=("A", "B", "C", "D", "E", "F")):
        frame = adf.copy()
        frame["compound"] = pd.Categorical(frame["compound"].astype(str), categories=list(order))
        X = dmatrix(formula, frame, return_type="dataframe").drop(columns=["Intercept"], errors="ignore")
        return PLS(n_components=3, scale=True).fit(X, curves)

    panels = [("sum, F omitted", rhs_sum, ("A", "B", "C", "D", "E", "F")),
              ("sum, A omitted", rhs_sum, ("F", "E", "D", "C", "B", "A")),
              ("treatment, A reference", rhs_trt, ("A", "B", "C", "D", "E", "F")),
              ("cell-means", rhs_cell, ("A", "B", "C", "D", "E", "F"))]

    fig = make_subplots(rows=2, cols=2, subplot_titles=[p[0] for p in panels])
    for k, (title, formula, order) in enumerate(panels):
        model = fit_coding(formula, order)
        t2 = model.hotellings_t2_.iloc[:, -1]
        r, c = divmod(k, 2)
        for comp in compounds:
            sel = (adf["compound"] == comp).to_numpy()
            fig.add_scatter(x=[comp] * int(sel.sum()), y=t2[sel], mode="markers",
                            marker=dict(color=colour_of[comp]), row=r + 1, col=c + 1, showlegend=False)
        fig.add_hline(y=model.hotellings_t2_limit(), line_dash="dash", row=r + 1, col=c + 1)
    fig.show()

Under sum coding with F omitted, the four runs past the 95% :math:`T^2` limit of 8.7 are all compound
F, and the largest reaches 26. Omit A instead, by reversing the level order, and the flagged runs
become compound A, at a :math:`T^2` up to 18, while F now sits inside. Under treatment or cell-means
coding, where no level is written at the far corner of the contrast space, no run crosses the limit.
The omitted level's runs carry :math:`-1` in every sum contrast, which places them at the
:math:`(-1, \ldots, -1)` corner of the contrast space; ``scale=True`` puts the contrasts on a common
scale, so those runs sit farthest from the centre and take the highest leverage. The effect belongs
to the parameterization and moves with whichever level is omitted. This is why the diagnostics
flagged F as outlying, not because of its chemical features, but artificially because of the coding
choice.

.. figure:: ../figures/doe/colour-coding-diagnostics.png
    :align: center
    :width: 760px
    :alt: colour-coding-diagnostics.py

    Hotelling's :math:`T^2` for each run at three components, under four codings of the same
    interaction model. The dashed line is the 95% limit (8.7). The runs over the limit follow the
    omitted sum-coding level, F when F is dropped and A when A is dropped; treatment and cell-means
    coding, which place no level at the far corner of the contrast space, flag none. The leverage is
    a property of the coding, not of the chemistry.

Two things do not move with the coding. The interaction F-tests and the full-rank least-squares
coefficients are the same under all three, because they use the whole column space. And the goal
projection stays inside both limits under all three: A is omitted by none of them, so chromogen A at
the centre point keeps its :math:`T^2` near or below 0.1 and its SPE between about 1 and 2. (Omit A
instead, as the second panel does, and it would be flagged like any omitted level.) The goal check
the inversion relies on does not depend on the choice among the three.

The practical risk is a false alarm. A run past the :math:`T^2` or SPE limit is the usual signal to
set that run aside, and here that signal falls on every run of the omitted level for a reason that
has nothing to do with the response. Dropping compound F would be unfortunate, since the validation
reveals it to be one of the closest matches to the reference. So a coding choice would remove a
leading candidate.

The advice is then to try an alternative coding when unsure about removing outliers involved with
coded columns in the model. Alternatively verify in the raw data, which is a step that should be done
in any case when identifying an outlier. Recall designed experiments are in general sparse datasets
that place runs at the edges of the region on purpose, so high leverage there is expected and is not
by itself a reason to drop data. This is in contrast to analysing regular datasets that include a high
degree of redundancy.

What else depends on the coding is any reading taken from the truncated score, including the model
inversion in the next section, where the reachable set of candidates changes with the coding.

Which compound matches the reference
------------------------------------

We see the six compounds behave differently, yet we want to compensate in the four continuous factors
to make each compound behave with the same output as compound A. As you might expect, as long as you
have degrees of freedom, there are multiple ways you can achieve this.

Yet, if there is one key theme from this book, it is this: do not do this by trial and error. Let us
use a systematic approach, which we call model inversion.

Run the models backwards, going from the desired output (or goal) to the input factors needed.

The :ref:`product-development chapter <LVM_model_inversion_example>` sets this out for a PCA model,
using the loadings to map a target score to a recipe; here the same idea is applied to the PLS
interaction model, with the compound held fixed and the continuous factors as the manipulated
variables. The starting point for the method is Jaeckle and MacGregor's 1998 paper on `product design
through multivariate statistical analysis of process data
<https://literature.learnche.org/item/61/product-design-through-multivariate-statistical-analysis-of-process-data>`__.

There is one nuance though. We do not go backwards from the ten-dimensional raw output; those ten time
points are not ten independent specifications. As Jaeckle and MacGregor (1998) put it, the correlation
among the outputs has to be respected: a latent-variable model turns the correlated outputs into a
smaller set of independent directions, and the number of significant components is the number of
quality dimensions that can be specified independently. So we invert in the latent-variable space:
find the goal as a three-dimensional vector in the score space (three components, and PLS constructs
these score directions to be orthogonal). Three independent targets against four continuous factors,
so the match is solvable with one free direction to spare.

The forward map is ``pls_full.transform(X)``: it standardizes the model-matrix row and multiplies by
the direct weights :math:`\mathbf{W}^*`. Holding the compound fixed makes this map *affine* in the
four continuous factors, a linear map plus a constant offset. With the compound fixed, its contrast
columns become constants and its interaction columns become constants times a continuous factor, so
the score is :math:`\mathbf{t} = \mathbf{A}\mathbf{x} + \mathbf{b}`: a matrix :math:`\mathbf{A}` times
the four coded factors :math:`\mathbf{x}`, plus an offset :math:`\mathbf{b}`, with no factor squared.
Matching the three-component goal score is then a small linear system, :math:`\mathbf{A}\mathbf{x}`
equal to the goal score minus :math:`\mathbf{b}`: three equations in four unknowns, solved in one
step. The code builds :math:`\mathbf{A}` and :math:`\mathbf{b}` without algebra, by reading the score
at the centre (which gives the offset :math:`\mathbf{b}`) and along each continuous factor in turn
(each unit step gives one column of :math:`\mathbf{A}`). Four factors against three components leaves
one free direction, the operating window; the least-squares solution is the minimum adjustment from
the nominal centre.

.. code-block:: python

    import numpy as np

    t_goal = pls_full.transform(goal_x).to_numpy().ravel()

    def compensate(compound):
        base = pls_full.transform(encode(compound, 0, 0, 0, 0)).to_numpy().ravel()
        step = np.column_stack([
            pls_full.transform(encode(compound, *[float(k == j) for k in range(4)])).to_numpy().ravel() - base
            for j in range(4)])
        coded, *_ = np.linalg.lstsq(step, t_goal - base, rcond=None)
        return coded  # coded [concentration, co_solvent, pH, temperature]

    for c in ["B", "C", "D", "E", "F"]:
        print(c, np.round(compensate(c), 2))

Converting each coded setting to real units gives the recipe that would make each candidate reproduce
the reference profile as closely as possible. Because the response here is simulated, each recipe can
also be run back through the true simulator to measure how close it actually gets, reported as a
root-mean-square error on the developed curve (``t1`` onward, since ``t0`` is noise) alongside the best
attainable match, the closest any amplitude of that compound's fixed shape can reach (the
:ref:`ground-truth check <profile-ground-truth-check>` below sets this out). The first two rows give
the low and high level of each factor:

.. list-table:: Continuous-factor settings that reproduce the reference goal (chromogen A at centre)
    :widths: 18 15 15 10 15 15 15
    :header-rows: 1

    *   - Chromogen
        - Concentration (umol/L)
        - Co-solvent (% v/v)
        - pH
        - Temperature (degC)
        - Best match RMSE (t1-t9)
        - Validated RMSE (t1-t9)
    *   - Low level
        - 2
        - 5
        - 4.0
        - 15
        -
        -
    *   - High level
        - 8
        - 25
        - 7.0
        - 35
        -
        -
    *   - A (reference)
        - 5.0
        - 15.0
        - 5.5
        - 25.0
        - 0
        - 0
    *   - B
        - 4.9
        - 14.8
        - 5.4
        - 25.6
        - 0.015
        - 0.023
    *   - C
        - 5.5
        - 13.5
        - 6.1
        - 27.7
        - 0.058
        - 0.100
    *   - D
        - 5.1
        - 13.6
        - 6.1
        - 27.2
        - 0.083
        - 0.112
    *   - E
        - 5.4
        - 6.9
        - 7.7
        - 31.0
        - 0.095
        - 0.211
    *   - F
        - 8.7
        - 15.5
        - 8.2
        - 28.0
        - 0.033
        - 0.049

Chromogen B needs almost no change while C and D need a moderate move, a higher pH and temperature,
but stay inside the ranges. Compounds E and F fall outside the window where we experimented. This
table is the inversion read under sum coding. Because the three-component score is coding-dependent, as
the :ref:`coding section <profile-categorical-coding>` showed, so is the reachable set, and the
paragraphs below repeat the inversion under the other codings and under a reading that does not depend
on the coding at all. The validated column shows the score-match recipe reaching its low-rank target
but not the best attainable match (C at 0.100 against 0.058, E at 0.211 against 0.095); the
coding-invariant curve match below closes most of that gap.

.. figure:: ../figures/doe/colour-pls-inversion.png
    :align: center
    :width: 720px
    :alt: colour-pls-inversion.py

    The inverted continuous-factor settings that place each candidate on the reference goal, in coded
    units, one row per factor, with light dashed separators between the rows. The shaded band between
    the dashed lines at :math:`-1` and :math:`+1` is the studied range. B, C and D are reachable within
    the ranges; E and F need a pH (and, for F, a concentration) beyond the studied window, marked with
    a heavy outline.

The compensation figure shows the coded settings directly; a Plotly version, with the studied range
shaded and light separators between the factor rows:

.. code-block:: python

    factors = ["concentration", "co_solvent", "pH", "temperature"]
    coded = pd.DataFrame({c: compensate(c) for c in ["B", "C", "D", "E", "F"]}, index=factors)

    fig = go.Figure()
    fig.add_vrect(x0=-1, x1=1, fillcolor="#e8eef5", line_width=0)
    for ysep in (0.5, 1.5, 2.5):  # separate each factor into its own lane
        fig.add_hline(y=ysep, line=dict(color="#cccccc", dash="dash", width=0.7))
    for c in coded.columns:
        fig.add_scatter(x=coded[c], y=factors, mode="markers", name=c)
    fig.update_layout(xaxis_title="coded setting to match the goal (0 = nominal centre)")
    fig.show()

Inversion is non-unique, and this reports one member of the operating window, the smallest move from
the nominal centre. A subject-matter expert might spend the free direction differently, for instance
holding one factor fixed and solving for the rest, as the :ref:`product-development worked example
<LVM_model_inversion_example>` does with a fixed hardness, or as we do :ref:`later, when we introduce
constraints <profile-constrained-inversion>`. That freedom is a property of the score match under any
coding; the reachable set, in contrast, moves with the coding.

Repeating the score match under treatment and cell-means coding gives a different reachable set each
time. Under sum coding B, C and D are inside the ranges; under treatment coding all five candidates
are; under cell-means coding B, C, D and F are, while E is not. B, C and D are reachable under every
coding, and E and F move in and out. The three codings answer the same question about the same data
and return three different candidate lists.

.. figure:: ../figures/doe/colour-coding-inversion.png
    :align: center
    :width: 720px
    :alt: colour-coding-inversion.py

    For each candidate and each way of posing the inversion, whether the recipe stays within the
    studied ranges or, where it does not, which factors leave the window and by how much (in real
    units, with the crossed bound in brackets). The first three columns match the three-component
    score, one per coding, and give three different recipes; the fourth matches the predicted ten-point
    curve at full rank, the same under any coding, and keeps only F within the ranges. A modest step
    outside the coded box is the extrapolation a designed experiment supports, so a crossed bound is a
    flag, not a disqualification.

A reading that does not depend on the coding matches the model's **predicted** ten-point curve rather
than the score, built from the measured runs, so no ground truth is needed here (the ground truth
enters only in the validation below). Matching all ten points is over-determined against the four
factors, which is exactly why the inversion above worked in the reduced three-component score; the
trade is that the predicted curve, unlike the score, does not depend on the coding, so its
least-squares closest match gives a coding-invariant reading:

.. code-block:: python

    from patsy import build_design_matrices

    info_full = dmatrix(rhs, adf, return_type="dataframe")  # keep the intercept: full rank
    beta = np.linalg.lstsq(info_full.to_numpy(), curves.to_numpy(), rcond=None)[0]

    def curve_of(compound, coded):
        row = pd.DataFrame({"compound": [compound], "concentration": [coded[0]],
                            "co_solvent": [coded[1]], "pH": [coded[2]], "temperature": [coded[3]]})
        x = build_design_matrices([info_full.design_info], row, return_type="dataframe")[0]
        return x.to_numpy().ravel() @ beta

    y_goal = curve_of("A", [0, 0, 0, 0])

    def curve_match(compound):
        y0 = curve_of(compound, [0, 0, 0, 0])
        step = np.column_stack([
            curve_of(compound, [float(k == j) for k in range(4)]) - y0 for j in range(4)])
        coded, *_ = np.linalg.lstsq(step, y_goal - y0, rcond=None)
        return coded  # coded [concentration, co_solvent, pH, temperature]

    for c in ["B", "C", "D", "E", "F"]:
        print(c, np.round(curve_match(c), 2))

The curve match keeps F inside the studied box and places the others outside it; the grid above gives
each factor and the bound it crosses. A modest step outside is not disqualifying: it is the
extrapolation a designed experiment is built to support, paid for by a larger prediction variance. But
some settings land far out, D at 45% v/v co-solvent and E near :math:`-28` degC (below freezing for an
aqueous system), which itself signals that the amplitude-only factors cannot reproduce those shapes.
Whether a setting is worth using is separate from whether it sits in the box, and is checked below
against the ground truth. The score match and curve match ask different things: the three-component
score is a low-rank summary several candidates reach with small moves, while the full curve asks for
the whole profile, which the factors mostly cannot give, since they move amplitude while the compounds
differ in late-time shape. Shape, not amplitude, is the binding constraint, returning to the
shape-distance ranking: B is closest to the reference, then F.

Adding a new chromogen
----------------------

The six chromogens were fixed when the design was built. Suppose a seventh, G, becomes available
after the study. Two practical questions follow: how does each of the three coding options we have
seen take a new level in, and how many runs does it take to place G in the model. Writing the
seven-level factor three ways shows what each coding does with it:

.. code-block:: python

    seven = pd.DataFrame({"compound": ["A", "B", "C", "D", "E", "F", "G"],
                          "co_solvent": 0.0, "pH": 0.0, "temperature": 0.0, "concentration": 0.0})
    for label, formula in [("sum", "C(compound, Sum)"), ("treatment", "C(compound, Treatment)"),
                           ("cell-means", "0 + C(compound)")]:
        print(label, list(dmatrix(formula, seven, return_type="dataframe").columns))

.. list-table:: Does adding compound G force any re-coding of the existing sixty runs?
    :widths: 12 14 12 14 12 14 12
    :header-rows: 2

    *   - Compound
        - Sum (effects)
        - Sum (effects)
        - Treatment
        - Treatment
        - Cell-means
        - Cell-means
    *   -
        - existing (1-60)
        - after G
        - existing (1-60)
        - after G
        - existing (1-60)
        - after G
    *   - A
        - own
        - own
        - baseline
        - baseline
        - own
        - own
    *   - B
        - own
        - own
        - own
        - own
        - own
        - own
    *   - C
        - own
        - own
        - own
        - own
        - own
        - own
    *   - D
        - own
        - own
        - own
        - own
        - own
        - own
    *   - E
        - own
        - own
        - own
        - own
        - own
        - own
    *   - F
        - omitted
        - own
        - own
        - own
        - own
        - own
    *   - G
        - -
        - omitted
        - -
        - own
        - -
        - own

In the table, "own" is that compound's own contrast (sum, treatment) or indicator (cell-means),
"baseline" is the treatment reference, and "-" marks a compound not yet in the model. Where a
compound's entry changes between its two columns, the existing sixty rows must be re-coded.

Each coding now has one more column, but they differ in what happens to the six compounds already in
the model. Under cell-means a column for G appears, its own indicator, and the A-to-F indicators keep
their values. Under treatment coding a column for G appears too, the contrast of G against the
reference A, and the existing contrasts keep their meaning. Under sum coding no column for G appears
at all: G becomes the omitted level, carried as the negative sum of the others, and the new column
belongs to F, which the six-level model had omitted. Every existing departure is now measured against
an average that includes G, so all six are redefined. For carrying the fitted results forward,
treatment and cell-means leave what is already known untouched; sum coding rewrites it.

The efficient route is to augment the existing design rather than start again. The number of new runs
follows from how many terms G brings. The model gives each compound its own mean and its own slopes on
co-solvent, pH and temperature, while the concentration slope is shared across compounds. So in the interaction model G carries four terms of its own: a mean and three
interaction slopes. Four terms need at least four runs of G, placed so co-solvent, pH and temperature
are not confounded (a four-run resolution-III fraction in the three factors, with concentration held
at the centre since its slope is borrowed). Four runs estimate the four terms and leave nothing over
to check them; six to eight give a residual degree of freedom or two to test the fit and show any
curvature.

Those runs have to use G. None of the sixty existing runs did, so G's own mean and slopes cannot be
read from them. What the sixty runs still provide is the shared concentration slope and a pooled
estimate of the measurement error, and G borrows both: the shared slope carries over, and the pooled
error tightens the tests on G's four terms from only a handful of runs. Holding the sixty runs fixed
and adding a small G block is the ``fixed_runs`` (prior) path of the optimal-design construction: the
new runs are placed to estimate G's terms with the least added variance, given what the sixty already
cover. Under cell-means or treatment coding the sixty runs enter the refit unchanged; under sum coding
the matrix is re-referenced first.

To see what the extra runs buy, hold the sixty runs fixed and add a G block of two sizes, the four-run
minimum and the eight-run full factorial, then score each augmented design against the seven-level
interaction model:

.. code-block:: python

    import itertools

    base = design.design[["compound"] + list(cont)].astype({"compound": str})
    res3 = [(-1, -1, 1), (1, -1, -1), (-1, 1, -1), (1, 1, 1)]  # four-run resolution-III fraction
    full = list(itertools.product([-1, 1], repeat=3))  # eight-run full factorial (2**3)

    def g_block(rows):  # compound G at the centre concentration
        return pd.DataFrame([{"compound": "G", "concentration": 0.0,
                              "co_solvent": a, "pH": b, "temperature": c} for a, b, c in rows])

    for label, block in [("base", base.iloc[:0]),  # base has no G: patsy fits the six-level model
                         ("+4", g_block(res3)), ("+8", g_block(full))]:
        aug = pd.concat([base, block], ignore_index=True)
        m = evaluate_design(aug, model=rhs,
                            metric=["d_efficiency", "i_efficiency", "g_efficiency", "fds"])
        q = m["fds"]["quantiles"]
        print(label, len(aug), round(m["d_efficiency"], 1), round(m["i_efficiency"]),
              round(m["g_efficiency"], 1), round(q["0.5"], 2), round(q["1"], 2))
    # base 60 23.6 159 56.3 0.25 0.74
    # +4   64 19.4 152 44.3 0.27 1.02
    # +8   68 20.1 163 57.6 0.25 0.74

.. list-table:: Design quality before and after adding compound G (interaction model)
    :widths: 30 16 16 16
    :header-rows: 1

    *   - Criterion
        - Base (60, A-F)
        - 60 + 4 G (64)
        - 60 + 8 G (68)
    *   - :math:`\uparrow` D-efficiency
        - 23.6\*
        - 19.4
        - 20.1
    *   - :math:`\uparrow` I-efficiency
        - 159
        - 152
        - 163
    *   - :math:`\uparrow` G-efficiency
        - 56.3
        - 44.3
        - 57.6
    *   - :math:`\downarrow` FDS median
        - 0.25
        - 0.27
        - 0.25
    *   - :math:`\downarrow` FDS max
        - 0.74
        - 1.02
        - 0.74

The base column scores the six-level interaction model (24 terms); with no G runs it cannot estimate
the seven-level model at all, which is the reason to augment rather than start again. The +4 and +8
columns score that seven-level model (28 terms), so the base and augmented columns carry a different
number of parameters and are not directly comparable.

The asterisk on the base D-efficiency marks that gap: the apparent fall from 23.6 to 20.1 is the move
from 24 to 28 parameters, not a design that got worse. It is worth recalling what the two criteria
measure. D-optimality maximizes the information determinant :math:`|\mathbf{X}^T\mathbf{X}|`, which
sharpens the coefficient estimates; I-optimality minimizes the prediction variance averaged over the
factor region. The aim here is to predict the colour-development curve across that region, not to pin
down coefficients as precisely as possible, so the I-efficiency is the column to watch.

On the I-efficiency the eight-run block (163) edges the four-run block (152); it also lowers the
worst-case prediction variance (FDS max 0.74 against 1.02) and buys residual degrees of freedom to
check G's fit. These numbers use the interaction model throughout, so they are not comparable to the
quadratic-model scores of the six-level design; the four-run count itself is a property of the smaller
interaction model.

One route needs no runs at all. If the chromogens carried measured molecular descriptors, a
property-to-property model could place G from its structure, the statistical-molecular-design approach
of `Muteki and MacGregor
<https://literature.learnche.org/item/170/sequential-design-of-mixture-experiments-for-the-development-of-new-products>`__.
Here the compounds are unordered categories with no descriptors, so each one is independent and G is
known only once it is run.

.. _profile-ground-truth-check:

Checking the inversion against the known ground truth
-----------------------------------------------------

Because the curves here are generated from a known ground truth, the inverted settings can be checked
against it directly: take each candidate's settings, in real units and including those outside the
box, put them back through the ground-truth curve, and measure how far the result sits from the
reference profile on the developed part (``t1`` onward, since ``t0`` is near-zero noise).

.. code-block:: python

    def true_curve(compound, coded):  # the ground truth defined earlier
        drift, s_co, s_ph, s_tp = truth[compound]
        amp = max(1.0 + 0.35 * coded[0] + s_co * coded[1] + s_ph * coded[2] + s_tp * coded[3], 0.05)
        return amp * np.clip(ref + drift * tail, 0, None)

    goal_curve = true_curve("A", [0, 0, 0, 0])  # the reference profile to reproduce
    noise = 0.03  # measurement-noise standard deviation

    for c in ["B", "C", "D", "E", "F"]:
        got = true_curve(c, curve_match(c))  # curve_match(c) from the block above
        rmse = float(np.sqrt(np.mean((got[1:] - goal_curve[1:]) ** 2)))  # developed curve, t1 onward
        print(c, round(rmse, 3), round(rmse / noise, 1))

The continuous factors move only the amplitude, so the closest any setting can bring a candidate to
the reference is set by that candidate's fixed shape, its late-time drift. The best attainable
match, the smallest root-mean-square deviation from the reference reachable at any amplitude, orders
the candidates by drift:

.. list-table:: How close each candidate can be brought to the reference (developed curve, t1 onward)
    :widths: 20 20 22 26
    :header-rows: 1

    *   - Chromogen
        - Late-time drift
        - Best emulation RMSE
        - In units of the noise (0.03)
    *   - A (reference)
        - 0.00
        - 0
        - 0
    *   - B
        - +0.05
        - 0.015
        - 0.5
    *   - F
        - -0.10
        - 0.033
        - 1.1
    *   - C
        - +0.20
        - 0.058
        - 1.9
    *   - D
        - +0.30
        - 0.083
        - 2.8
    *   - E
        - +0.35
        - 0.095
        - 3.2

Running the curve-match settings through the ground truth reaches close to that best attainable match
for the near candidates: B lands at 0.017, F at 0.046, and C at 0.063, within roughly half, one and a
half, and two times the measurement noise. D and E stay at 2.8 times the noise or worse whatever the
factors are set to, inside the box or outside it, because their shape gap is too large for amplitude to
close.

.. figure:: ../figures/doe/colour-inversion-validation.png
    :align: center
    :width: 780px
    :alt: colour-inversion-validation.py

    Left: the reference curve (chromogen A at the centre point) with the closest emulation each
    candidate can reach, the best amplitude for its fixed shape. The candidates track the reference
    early and separate at the tail, by their late-time drift. Right: the emulation error against the
    measurement-noise scale, each candidate's best attainable match (open marker) and what the
    coding-invariant curve-match inversion reaches when its real-unit settings are put through the
    ground truth (filled marker), ordered by drift. B lands within about half a noise standard
    deviation of the reference and F within one and a half, C just over two; D and E no closer than
    2.8 times the noise.

The developed part of the curve makes the accuracy plainer. Dropping the first time point, where
every curve is near zero, and tightening the vertical axis to the plotted range (so it does not start
at zero) shows each candidate's best inverted solution against the reference at the scale of the
differences that remain:

.. code-block:: python

    def best_emulation(compound):  # best amplitude for the compound's shape
        shape = np.clip(ref + truth[compound][0] * tail, 0, None)  # truth[c][0] is the drift
        return float(shape[1:] @ goal_curve[1:] / (shape[1:] @ shape[1:])) * shape  # fit on t1 onward

    fig = go.Figure()
    fig.add_scatter(x=time_points[1:], y=goal_curve[1:], mode="lines+markers",
                    name="A (reference)", line=dict(width=4, color="black"))
    for c in ["B", "F", "C", "D", "E"]:  # ordered by drift, closest first
        fig.add_scatter(x=time_points[1:], y=best_emulation(c)[1:], mode="lines+markers", name=c)
    fig.update_layout(xaxis_title="time point (t0 omitted)", yaxis_title="absorbance")
    fig.show()

At this scale B and F sit on the reference through the developed curve, and C stays within a narrow
band; D and E separate at the tail, the late-time drift amplitude cannot remove.

.. figure:: ../figures/doe/colour-emulation-detail.png
    :align: center
    :width: 680px
    :alt: colour-emulation-detail.py

    The developed part of the curve (t0 omitted, vertical axis tightened to the plotted range so it
    excludes zero), showing each candidate's best inverted solution against the reference. B and F
    track the reference across the whole developed curve; C stays close; D and E lift away at the
    tail, by their late-time drift. The legend gives each candidate's RMSE to the reference.

So the inversion does its job: for each candidate it finds the settings that bring the curve as close
to the reference as that candidate's shape allows, recovering the drift ordering B, F, C, D, E.

.. _profile-constrained-inversion:

One variant of the inversion is worth ruling out. The inversions above hold each candidate on the
goal's projection, matching its three-component score or its predicted curve, so each solution sits
close to the model plane. `Muteki and MacGregor (2007)
<https://literature.learnche.org/item/170/sequential-design-of-mixture-experiments-for-the-development-of-new-products>`__
pose the inversion as a constrained optimization: minimize the distance to the target subject to
Hotelling's :math:`T^2` and the SPE staying below their limits, so the solution may float off the
model plane. Their objective drives the
latent score to the target; here it drives the predicted curve, under the same :math:`T^2` and SPE
constraints. With both free to rise to their 95% limits, it does not bring any candidate below its
best attainable match:

.. code-block:: python

    from scipy.optimize import minimize

    t2_lim, spe_lim = pls_full.hotellings_t2_limit(), pls_full.spe_limit()

    def t2_spe(compound, coded):  # 3-component diagnostics of an inverted point
        d = pls_full.diagnose(encode(compound, *coded))
        return float(d.hotellings_t2.iloc[0]), float(d.spe.iloc[0])

    def relaxed_inversion(compound):  # constrained inversion (Muteki-MacGregor 2007)
        objective = lambda c: float(np.sum((y_goal - curve_of(compound, c)) ** 2))
        limits = [{"type": "ineq", "fun": lambda c: t2_lim - t2_spe(compound, c)[0]},
                  {"type": "ineq", "fun": lambda c: spe_lim - t2_spe(compound, c)[1]}]
        return minimize(objective, np.zeros(4), method="SLSQP", constraints=limits).x

    for c in ["B", "C", "D", "E", "F"]:
        settings = relaxed_inversion(c)
        rmse = np.sqrt(np.mean((true_curve(c, settings)[1:] - goal_curve[1:]) ** 2))  # t1 onward
        print(c, round(float(rmse), 3))  # 0.016  0.061  0.100  0.105  0.048

Each relaxed solution lands at or above its candidate's best attainable match (B at 0.016 and D at
0.100, against best matches of 0.015 and 0.083), while its SPE rises to the 6.5 limit and its
settings leave the studied ranges. Pinning the two hard-to-change factors, temperature and
co-solvent, at the centre and re-optimizing over concentration and pH alone gives the same result.
The off-plane freedom the continuous factors reach is amplitude, not shape, so it cannot close a
compound's late-time drift: the closest attainable curve stays the projection of the target onto the
model plane, which is Muteki and MacGregor's feasibility condition.

Read together, the answer to which compound matches the reference is not one candidate but a graded
ranking, and it depends on how the question is posed. The score match returns a binary reachable set
that changes with the coding and with where the studied box is drawn, a statement about a low-rank
projection. The curve match, checked against the ground truth, gives the reading that holds: the
candidates line up by their fixed curve shape, with B reproducing the reference to within about half
the measurement noise and F to within roughly one and a half times it, C to just over twice, and D and
E not reproducible however the factors are set. F is not singled out; it sits second behind B, which
the shape-distance ranking said at the start.

The model that generated the data
---------------------------------

Because the study was simulated, the model that generated the curves is known, and the recovered
results can be set against it. Each curve was built from three parts: a common rise-to-plateau shape,
a compound-specific late-time drift added to that shape, and an amplitude that scales the whole curve.
The amplitude is linear in the coded factors, with a concentration slope shared by every compound and
per-compound slopes on co-solvent, pH and temperature. Compound A, the reference, has zero drift; the
analogs drift by the amounts set at the start:

.. code-block:: python

    gen = pd.DataFrame(truth, index=["drift", "co_solvent", "pH", "temperature"]).T
    gen["concentration"] = 0.35  # shared amplitude slope, identical for every compound
    print(gen[["drift", "concentration", "co_solvent", "pH", "temperature"]])

.. list-table:: The generative model: late-time drift and the amplitude slopes on the coded factors
    :widths: 18 16 16 16 12 16
    :header-rows: 1

    *   - Compound
        - Late-time drift
        - Concentration
        - Co-solvent
        - pH
        - Temperature
    *   - A (reference)
        - 0.00
        - 0.35
        - -0.05
        - -0.06
        - +0.02
    *   - B
        - +0.05
        - 0.35
        - -0.08
        - -0.10
        - +0.03
    *   - C
        - +0.20
        - 0.35
        - -0.20
        - -0.28
        - +0.12
    *   - D
        - +0.30
        - 0.35
        - -0.25
        - -0.30
        - +0.14
    *   - E
        - +0.35
        - 0.35
        - -0.10
        - -0.08
        - +0.05
    *   - F
        - -0.10
        - 0.35
        - -0.15
        - -0.22
        - -0.10

Set against what the analysis recovered, the generative model lines up on the readings the study
leaned on. The drift column orders the compounds B, F, C, D, E by distance from the reference, the
same order the shape-distance ranking and the ground-truth inversion check produced, and A's zero
drift is why it serves as the reference. The concentration slope is shared and positive, matching the
single amplitude direction the first PLS component picked out. Across the six compounds the
per-compound slopes spread most on pH and least on co-solvent, the same order (pH, then temperature,
then co-solvent) as the interaction F-tests. The recovered coefficients are departures from the
average compound rather than the raw slopes, so they do not equal the table entries term for term, but
their signs and relative sizes track it.

A single design, several questions
----------------------------------

One run of ``generate_design`` produced a sixty-run split-plot design over a six-level categorical
factor and four continuous factors, scored for prediction variance with ``evaluate_design``, and the
ten-point response was modelled with ``PLS`` and reduced to interaction tests with
``analyze_experiment``, all through the documented public interface with no manual coding.

The study answered several questions from a single design:

- all interactions of the chemical compound with the continuous process variables are significant
  (objectives 1 to 3);
- inverting the model onto a reference goal, then checking the recovered settings against the known
  ground truth, ranked the candidates by their fixed curve shape: compound B matched to within about
  half the measurement noise and compound F to within one and a half (objective 4);
- the choice of categorical coding changed which candidates the low-rank score match declared
  reachable, so we compared the sum, reference, and cell-means codings and how each is interpreted;
- a new compound was introduced as an extra level of the categorical factor, augmenting the original
  sixty runs rather than repeating them.

The same design supported a scalar analysis of variance on the peak, a multivariate model of the full
curve, and the inversion of that model back to factor settings, because the design was chosen for the
model, not for a particular way of reducing the response. Choose the design for the model, not for one
reading of the response, and one set of runs will answer questions you have not yet thought to ask.
