.. _APPS_mixed_level_profile_case_study:

A mixed-level split-plot design with a profile response
=======================================================

This case study draws the :ref:`design-and-analysis-of-experiments
<SECTION-design-analysis-experiments>` and :ref:`latent-variable-modelling
<SECTION_latent_variable_modelling>` chapters together on one problem, and carries it through to
the analysis of the data. The design side uses the pieces built up in the optimal-design section:
the :ref:`information matrix <DOE-optimal-designs>`, the :ref:`coordinate-exchange search
<DOE-exchange-algorithms>`, a :ref:`categorical factor with several levels
<DOE-categorical-factors>`, and hard-to-change factors that force a split-plot run order. The
analysis side uses a projection-to-latent-structures model, because the response is not a single
number but a *curve*: ten correlated measurements that move together, which a latent-variable model
handles directly where a separate regression per measurement would not.

The worked example runs end to end with the ``process_improve`` library. The coordinate-exchange
optimiser is provided by ``pyoptex``, installed separately (``pip install pyoptex``); the rest is
``pip install 'process-improve[expt]'``. The response here is simulated from a known ground truth
so that the effects the analysis recovers can be checked against the values that were put in. In a
real study the same code reads measured data in place of the simulation.

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

    np.random.seed(42)   # the coordinate exchange draws its restarts from the global RNG
    design = generate_design(factors, design_type="i_optimal", budget=60,
                             hard_to_change=["co_solvent", "temperature"],
                             model_type="quadratic")

    print(design.n_runs)                               # 60
    print(design.design["compound"].value_counts())    # 9 to 11 runs per compound

    order = design.design.sort_values("RunOrder").reset_index(drop=True)
    x = np.arange(len(order))
    fig = go.Figure()
    for name in ["co_solvent", "temperature", "concentration", "pH"]:
        fig.add_scatter(x=x, y=order[name], mode="lines", line_shape="hv", name=name)
    fig.update_layout(xaxis_title="run order", yaxis_title="coded level")
    fig.show()

The sixty runs spread evenly across the six compounds, nine to eleven each, and the continuous
factors fill the coded range. The run order shows the split-plot structure directly. Counting how
often each factor changes level between consecutive runs, the two hard-to-change factors move only
8 and 10 times across the sixty runs, while the two easy-to-change factors move 46 and 44 times.
The hard-to-change factors hold their level over long stretches, the whole plots, exactly the
grouping a split-plot is meant to produce.

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
``evaluate_design`` on the same quadratic model. The D-efficiency summarises the information
determinant :math:`|\mathbf{X}^T\mathbf{X}|`, higher being more information per run; the
I-efficiency summarises the prediction variance averaged over the whole factor region, and the
fraction-of-design-space (FDS) curve shows how that prediction variance is distributed, from the
best-predicted point to the worst.

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

Scoring the I-optimal and D-optimal designs at 48 and 60 runs lays out the trade-off. The
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
    at 60 runs is lowest and flattest; the D-optimal design at 48 runs is highest, with a long tail
    of poorly-predicted points near the region's edge.

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
    ref = 1.0 - np.exp(-time_points / 2.0);        ref = ref / ref.max()
    tail = np.clip((time_points - 4) / 5.0, 0, None);  tail = tail / tail.max()

    # ground truth: late-time drift, and amplitude slopes for co-solvent, pH, temperature
    truth = {
        "A": (0.00, -0.05, -0.06, +0.02), "B": (0.05, -0.08, -0.10, +0.03),
        "C": (0.20, -0.20, -0.28, +0.12), "D": (0.30, -0.25, -0.30, +0.14),
        "E": (0.35, -0.10, -0.08, +0.05), "F": (-0.10, -0.15, -0.22, -0.10)}

    rng = np.random.default_rng(20260710)
    rows = []
    for _, r in design.design.iterrows():
        drift, s_co, s_ph, s_tp = truth[r["compound"]]
        amp = max(1.0 + 0.35 * r["concentration"] + s_co * r["co_solvent"]
                  + s_ph * r["pH"] + s_tp * r["temperature"], 0.05)
        rows.append(amp * np.clip(ref + drift * tail, 0, None)
                    + rng.normal(0, 0.03, time_points.size))
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

    Mean colour-development curve for each chromogen. The curves rise together to about the fifth
    time point, then diverge: the reference A and the analog B level off together, while D and E
    keep developing colour and F drifts down.

Modelling the profile with PLS
------------------------------

A ten-point curve has ten correlated responses, so a separate regression per time point would
ignore that the points move together. A projection-to-latent-structures (PLS) model regresses all
ten at once against the factors, using a few latent components that capture the shared movement.

The factor block ``X`` has to be fully numeric, so the six-level compound is expanded into indicator
columns. Printing a few rows shows the coding:

.. code-block:: python

    dummies = pd.get_dummies(design.design["compound"], prefix="cmp").astype(float)
    X = pd.concat([design.design[list(cont)].astype(float), dummies.drop(columns=["cmp_A"])], axis=1)
    print(X.head(4))

The four continuous factors keep their coded :math:`-1` to :math:`+1` values. The compound becomes
five indicator columns, one per level with the reference level A dropped (the
:ref:`indicator coding <LVM-using-indicator-variables>` written out): a run using compound B has a
one in ``cmp_B`` and zeros elsewhere, and a run using the reference A has zeros in all five columns.

.. code-block:: text

       concentration  co_solvent   pH  temperature  cmp_B  cmp_C  cmp_D  cmp_E  cmp_F
    1           -1.0        -1.0 -1.0          1.0    1.0    0.0    0.0    0.0    0.0
    2           -1.0        -1.0  0.0          1.0    0.0    0.0    1.0    0.0    0.0
    3            1.0        -1.0 -1.0          1.0    0.0    1.0    0.0    0.0    0.0
    4            0.0        -1.0  0.0          1.0    0.0    0.0    0.0    1.0    0.0

This is a main-effects model: each compound shifts the colour by a fixed amount through its
indicator, and the continuous factors act the same way for every compound. The response columns are
on different scales (the early points carry far less variance than the plateau), so the blocks are
standardized before fitting. ``PLS(scale=True)`` does this internally, mean-centering and scaling
both the factor block and the response block to unit variance, and returns predictions on the
original absorbance scale, so raw ``X`` and raw ``curves`` can be passed straight in. Fitting it,
and reading the scores and the :math:`\mathbf{W}^*`/:math:`\mathbf{C}` loadings:

.. code-block:: python

    from plotly.subplots import make_subplots
    from process_improve.multivariate.methods import PLS

    pls = PLS(n_components=5, scale=True).fit(X, curves)
    print(pls.r2_cumulative_)          # cumulative R2Y by component: 0.78, 0.81, 0.82, 0.82, 0.83

    scores = np.asarray(pls.scores_)   # X scores, one row per run
    wstar = pls.direct_weights_        # W*: X-space weights, indexed by factor
    cw = pls.y_weights_                # C: Y-space weights, indexed by time point

    fig = make_subplots(rows=1, cols=2, subplot_titles=("scores", "W* and C loadings"))
    for c in compounds:
        m = (design.design["compound"] == c).to_numpy()
        fig.add_scatter(x=scores[m, 0], y=scores[m, 1], mode="markers", name=c, row=1, col=1)
    fig.add_scatter(x=wstar.iloc[:, 0], y=wstar.iloc[:, 1], mode="markers+text",
                    text=list(wstar.index), name="factor (W*)", row=1, col=2)
    fig.add_scatter(x=cw.iloc[:, 0], y=cw.iloc[:, 1], mode="lines+markers+text",
                    text=list(cw.index), name="time point (C)", row=1, col=2)
    fig.show()

The model reports its own goodness of fit through ``pls.r2_cumulative_``, the cumulative R2Y as each
component is added: 0.78 after the first component and 0.83 after five, so one component already
captures most of the response variation, and the ten time points move together along a single main
direction. The per-target root-mean-square error, ``pls.rmse_``, comes back on the original
absorbance scale (about 0.10 absorbance units at the final component), matching a hand calculation
from the predictions, so it reads directly against the measured curves.

The score plot places each run in the latent space. The runs spread across it rather than clustering
by compound, because the optimal design was chosen to fill the factor region. The relationship
between the factors and the response is read instead from the loadings plot, which places the factor
weights :math:`\mathbf{W}^*` and the response-point weights :math:`\mathbf{C}` on the same axes. The
first component is an amplitude direction: the concentration sits with all ten time points at a high
component-1 weight, because raising the concentration lifts the whole curve. The second component is
a late-development direction: the compound indicators spread along it, with E and D (which keep
developing colour) opposite F and B, and the late time point ``t9`` falls on the same side as the
compounds that drift upward. A factor and a response point lying in the same direction means that
factor raises the colour at those times.

.. figure:: ../figures/doe/colour-pls-scores-loadings.png
    :align: center
    :width: 760px
    :alt: colour-pls-scores-loadings.py

    Left: the first two PLS scores, one point per run, coloured by chromogen. Right: the factor
    weights :math:`\mathbf{W}^*` and the response-point weights :math:`\mathbf{C}` on the same axes.
    Component 1 is an amplitude direction (concentration with all ten time points); component 2
    separates the compounds by late-time development, with ``t9`` on the side of the compounds that
    keep developing colour.

Testing the compound-by-factor interactions
--------------------------------------------

The first three questions are about interactions: does the co-solvent, the pH, or the temperature
move the colour differently for different compounds? Reducing each curve to its peak absorbance gives
a single response for an analysis-of-variance model with explicit compound-by-factor interaction
terms. The compound is written with sum-to-zero (effects) coding through ``C(compound, Sum)``, so
each compound effect is a departure from the average; the formula validator accepts the patsy
contrast helper directly.

.. code-block:: python

    from process_improve.experiments import analyze_experiment

    adf = design.design[["compound"] + list(cont)].copy()
    adf["compound"] = adf["compound"].astype(str)
    adf["peak"] = curves.max(axis=1).to_numpy()

    formula = ("peak ~ C(compound, Sum)*co_solvent + C(compound, Sum)*pH "
               "+ C(compound, Sum)*temperature + concentration")
    res = analyze_experiment(adf, response_column="peak", model=formula,
                             analysis_type=["anova"], coding="coded")
    print(res["model_summary"]["r_squared"])          # 0.989
    print(pd.DataFrame(res["anova_table"]))

The model explains 99% of the variation in peak colour. All three interaction terms are significant:
the compound-by-pH term is the strongest (:math:`F = 28`, :math:`p = 2 \times 10^{-11}`), then
compound-by-temperature (:math:`F = 18`) and compound-by-co-solvent (:math:`F = 15`), each with
:math:`p < 10^{-7}`. This answers the first three questions: the process factors do act differently
across compounds, which was how the response was constructed. As the :ref:`categorical-factor
section <DOE-categorical-factors>` noted, these interaction terms are also what make a robust
operating point reachable, a setting where the compounds give nearly the same colour, which the
fifth question would search for.

The same model, fitted by PLS
-----------------------------

The analysis of variance used the compound-by-factor interaction terms, but the PLS model fitted
earlier used only the main effects and the compound indicators. The same interaction terms can be
given to PLS. Building the model matrix from the same formula right-hand side (with patsy, dropping
the intercept, since ``PLS`` centres the columns) and fitting it against the full ten-point curve:

.. code-block:: python

    from patsy import dmatrix

    rhs = ("C(compound, Sum)*co_solvent + C(compound, Sum)*pH "
           "+ C(compound, Sum)*temperature + concentration")
    X_int = dmatrix(rhs, adf, return_type="dataframe").drop(columns=["Intercept"])
    print(X_int.shape)                          # (60, 24): 24 model terms

    pls_int = PLS(n_components=5, scale=True).fit(X_int, curves)
    print(pls_int.r2_cumulative_)               # 0.77, 0.85, 0.88, 0.90, 0.91

The expanded model has 24 terms: the five compound contrasts, the three continuous factors that
interact with the compound, their fifteen interaction columns, and the concentration. Its cumulative
R2Y reaches 0.91 at five components, against 0.83 for the main-effects model, because the
compound-specific slopes on co-solvent, pH and temperature (the interactions the analysis of variance
found significant) are now in the factor block. PLS fits these terms to all ten time points at once,
returning a predicted development curve, where the analysis of variance fitted the same terms to a
single summary of each curve, its peak.

Five components were kept, but the number of components is itself a modelling choice, and
cross-validation is how it is made. Leaving out each run in turn, refitting, and predicting the
held-out curve gives the cross-validated :math:`Q^2_Y`, the fraction of the response variation the
model predicts for runs it did not see. ``pls.cross_validate`` returns a per-response
:math:`Q^2_Y`; averaged over the ten time points at each number of components:

.. code-block:: python

    q2 = []
    for a in range(1, 6):
        cv = PLS(n_components=a, scale=True).fit(X_int, curves).cross_validate(X_int, curves, cv="loo")
        q2.append(float(cv["q_squared"].mean()))
    print(np.round(q2, 2))                          # 0.52, 0.78, 0.78, 0.77, 0.80

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
the data the model is fitted to. :math:`Q^2_Y` behaves differently. It jumps from 0.52 to 0.78 with
the second component, then holds near 0.78 through the third, fourth, and fifth. The response
variation that can be predicted for unseen runs is captured by the first two components; the later
ones raise the in-sample fit without a matching rise in cross-validated prediction, the sign of a
component that describes noise in this data rather than structure that generalizes. On this evidence
a two- or three-component model predicts about as well as the five-component one. Five components are
used through the rest of this section so the score, loadings, and coefficient comparisons are read
at one component count, and because the coefficient comparison below is made against the full
least-squares fit; the gap in :math:`Q^2_Y` between two and five components is small.

The two fits can be compared on equal footing. Giving PLS the same single response the regression
used, the peak, and the same interaction terms, its ``beta_coefficients_`` line up against the
least-squares coefficients term by term:

.. code-block:: python

    ols = analyze_experiment(adf, response_column="peak", model="peak ~ " + rhs,
                             analysis_type=["coefficients"])["coefficients"]
    ols = {c["term"]: c["coefficient"] for c in ols}

    pls_peak = PLS(n_components=5, scale=True).fit(X_int, adf[["peak"]])
    beta = pls_peak.beta_coefficients_.iloc[:, 0]

    coef = pd.DataFrame({"OLS": [ols[t] for t in X_int.columns], "PLS": beta.to_numpy()},
                        index=X_int.columns).sort_values("OLS")
    fig = go.Figure()
    fig.add_scatter(x=coef["OLS"], y=coef.index, mode="markers", name="least squares")
    fig.add_scatter(x=coef["PLS"], y=coef.index, mode="markers", name="PLS")
    fig.show()

The two sets of coefficients differ by at most 0.01 across all 24 terms. The concentration carries
the largest coefficient (about 0.40, it raises the peak for every compound), the pH main effect the
largest negative one (about :math:`-0.21`), and the compound-by-factor terms fill in between. PLS
reproduces the least-squares fit when enough components are kept; with fewer components it pulls the
coefficients toward zero, trading a small bias for lower variance. The reason to use PLS here is not
a different answer on the peak, but that the same model extends directly to the full ten-point curve,
and to responses with more columns than the design has runs, where ordinary least squares cannot be
fitted at all.

The full least-squares coefficient table, in the same order as the plot below (largest coefficient
first, smallest last), with the standard error, t-statistic, and p-value for each term:

.. list-table:: Least-squares coefficients for the peak colour intensity, largest to smallest
    :widths: 30 16 14 12 14
    :header-rows: 1

    *   - Term
        - Coefficient
        - Std. error
        - t
        - p-value
    *   - ``concentration``
        - +0.395
        - 0.010
        - +40.8
        - <0.001
    *   - ``cmpE``
        - +0.215
        - 0.019
        - +11.5
        - <0.001
    *   - ``cmpD``
        - +0.143
        - 0.020
        - +7.3
        - <0.001
    *   - ``cmpA:pH``
        - +0.123
        - 0.021
        - +5.8
        - <0.001
    *   - ``cmpD:temperature``
        - +0.112
        - 0.022
        - +5.0
        - <0.001
    *   - ``cmpA:co_solvent``
        - +0.111
        - 0.024
        - +4.6
        - <0.001
    *   - ``cmpB:pH``
        - +0.107
        - 0.021
        - +5.1
        - <0.001
    *   - ``cmpC:temperature``
        - +0.097
        - 0.021
        - +4.6
        - <0.001
    *   - ``cmpB:co_solvent``
        - +0.081
        - 0.021
        - +3.8
        - <0.001
    *   - ``cmpE:pH``
        - +0.069
        - 0.024
        - +2.9
        - 0.007
    *   - ``cmpC``
        - +0.067
        - 0.019
        - +3.6
        - <0.001
    *   - ``temperature``
        - +0.057
        - 0.010
        - +5.7
        - <0.001
    *   - ``cmpE:co_solvent``
        - +0.034
        - 0.023
        - +1.5
        - 0.147
    *   - ``cmpE:temperature``
        - +0.021
        - 0.024
        - +0.9
        - 0.372
    *   - ``cmpA:temperature``
        - -0.038
        - 0.024
        - -1.6
        - 0.120
    *   - ``cmpB:temperature``
        - -0.042
        - 0.023
        - -1.9
        - 0.071
    *   - ``cmpC:co_solvent``
        - -0.066
        - 0.025
        - -2.7
        - 0.011
    *   - ``cmpB``
        - -0.089
        - 0.018
        - -5.0
        - <0.001
    *   - ``cmpA``
        - -0.135
        - 0.018
        - -7.3
        - <0.001
    *   - ``cmpC:pH``
        - -0.146
        - 0.021
        - -7.0
        - <0.001
    *   - ``co_solvent``
        - -0.157
        - 0.011
        - -14.9
        - <0.001
    *   - ``cmpD:pH``
        - -0.166
        - 0.023
        - -7.1
        - <0.001
    *   - ``cmpD:co_solvent``
        - -0.177
        - 0.026
        - -6.8
        - <0.001
    *   - ``pH``
        - -0.209
        - 0.010
        - -21.1
        - <0.001

Most terms are significant at the 0.05 level. The exceptions are four of the temperature and
co-solvent interactions for individual compounds (``cmpE:co_solvent``, ``cmpE:temperature``,
``cmpA:temperature``, ``cmpB:temperature``, with p-values from 0.07 to 0.37): the interaction is
present for the set of compounds, which the analysis of variance tested jointly, but not resolved
for each compound on its own at this run count.

.. figure:: ../figures/doe/colour-coefficient-comparison.png
    :align: center
    :width: 620px
    :alt: colour-coefficient-comparison.py

    Coefficients for the peak colour intensity from ordinary least squares and from PLS, fitted to
    the same interaction model. The two nearly coincide, so PLS reproduces the regression when the
    number of components is sufficient. Terms are sorted by the least-squares coefficient; the
    ``cmp`` prefix marks a compound contrast under sum-to-zero coding.

Which compound matches the reference
------------------------------------

The fourth question compares curve *shape*, not colour depth, so amplitude is divided out first:
each compound's mean curve is scaled to unit peak, and the Euclidean distance to the reference
compound A's scaled curve measures how differently the colour develops over time.

.. code-block:: python

    shapes = mean_curve.div(mean_curve.max(axis=1), axis=0)
    distance = ((shapes - shapes.loc["A"]) ** 2).sum(axis=1) ** 0.5
    print(distance.drop("A").sort_values())

    order_c = distance.drop("A").sort_values()
    fig = go.Figure(go.Bar(x=order_c.values, y=order_c.index, orientation="h"))
    fig.update_layout(xaxis_title="shape distance to reference A", yaxis_title="candidate")
    fig.show()

Compound B is closest to the reference, at a distance of 0.07, well ahead of the next candidate F at
0.15, with C, D and E progressively further. The ranking, B then F then C then D then E, is exactly
the order of the late-time drift that was built into each compound, so the analysis recovers the
shape ordering from the noisy data.

.. figure:: ../figures/doe/colour-shape-distance.png
    :align: center
    :width: 700px
    :alt: colour-shape-distance.py

    Shape distance from each candidate's colour-development curve to the reference A, with amplitude
    divided out. Compound B (highlighted) develops colour most like the reference; E is furthest.

What the design and the library carried
---------------------------------------

One run of ``generate_design`` produced a sixty-run split-plot design over a six-level categorical
factor and four continuous factors, scored for prediction variance with ``evaluate_design``, and the
ten-point response was modelled with ``PLS`` and reduced to interaction tests with
``analyze_experiment``, all through the documented public interface with no hand-built indicator
matrices or manual coding. The one piece that lives outside the standard install is the
coordinate-exchange optimiser, ``pyoptex``, which powers the I-optimal and split-plot construction
and is installed on its own.

The study answered its questions from a single design: the three interactions are significant
(objectives 1 to 3), compound B develops colour most like the reference (objective 4), and the
fitted model over the continuous factors locates settings for a target colour intensity for the
chosen compound (objective 5). The same design supported a scalar analysis of variance on the peak
and a multivariate model of the full curve, because the design was chosen for the model, not for a
particular way of reducing the response.
