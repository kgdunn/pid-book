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
``evaluate_design`` on the same quadratic model. The :ref:`D-efficiency
<DOE-judging-and-comparing-designs>` summarises the information determinant
:math:`|\mathbf{X}^T\mathbf{X}|`, higher being more information per run; the I-efficiency summarises
the prediction variance averaged over the whole factor region, and the :ref:`fraction-of-design-space
(FDS) curve <DOE-fds-plot>` shows how that prediction variance is distributed, from the best-predicted
point to the worst.

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

All six indicators cannot enter the model alongside the intercept: they sum to one in every row, so
one is redundant and :math:`\mathbf{X}^T\mathbf{X}` is singular (the :ref:`categorical-factor section
<DOE-categorical-factors>` sets this out). The redundancy is removed in one of two common ways, and
the choice fixes what each compound coefficient means:

- *Reference (treatment) coding* drops one level. Taking A as the reference leaves the five columns
  B to F; a run of compound A is all zeros across them, carried by the intercept. Each coefficient
  is then that compound's **difference from A**: the change in colour from switching the chemical to
  that compound while every continuous factor, the concentration included, is held at the same value.
- *Sum (effects) coding* keeps a contrast for each level but constrains the level effects to sum to
  zero. Each coefficient is then that compound's **departure from the average compound**, and a
  continuous factor's main effect is its average slope across the six compounds.

Either way five numbers describe the compound, and the two codings fit the same model: the same
predictions, the same :math:`R^2`, and the same interaction tests. Only the coefficients, and their
standard errors, move with the choice. The main-effects PLS just below uses reference coding (A
dropped); the interaction analysis later uses sum coding, and the coefficient comparison returns to
the difference the choice makes.

.. code-block:: python

    dummies = pd.get_dummies(design.design["compound"], prefix="cmp").astype(float)
    X = pd.concat([design.design[list(cont)].astype(float), dummies.drop(columns=["cmp_A"])], axis=1)

The four continuous factors keep their coded :math:`-1` to :math:`+1` values, and the compound
contributes the five indicators B to F. This is a main-effects model: each compound shifts the colour
by a fixed amount through its indicator, and the continuous factors act the same way for every
compound. The response columns are on different scales (the early points carry far less variance than
the plateau), so the blocks are standardized before fitting. ``PLS(scale=True)`` does this internally,
mean-centering and scaling both the factor block and the response block to unit variance, and returns
predictions on the original absorbance scale, so raw ``X`` and raw ``curves`` can be passed straight
in. Fitting it, and reading the scores and the :math:`\mathbf{W}^*`/:math:`\mathbf{C}` loadings:

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

Compound A has no indicator column, so it has no point in the loadings plot. It is the reference
level: each plotted compound weight, B to F, is that compound's difference from A (the main-effects
model uses reference coding), and a run of compound A is described by the continuous-factor weights
together with the block centre that ``scale=True`` removes. Compound A still appears in the score plot, since every run has a score
whichever compound it used; it is only the compound *weight* for A that is absent, because the
model measures the other five against it.

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

Testing the compound-by-factor interactions
--------------------------------------------

The first three questions are about interactions: does the co-solvent, the pH, or the temperature
move the colour differently for different compounds? Reducing each curve to its peak absorbance gives
a single response for an analysis-of-variance model with explicit compound-by-factor interaction
terms. The compound is written with sum-to-zero (effects) coding through ``C(compound, Sum)``, so
each compound effect is a departure from the average; the formula validator accepts the patsy
contrast helper directly. The interaction F-tests are the same whichever coding is used, since the
codings span the same model space.

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
interact with the compound, their fifteen interaction columns, and the concentration. The added
interaction terms raise the fit over the main-effects model's cumulative R2Y of 0.83, because the
compound-specific slopes on co-solvent, pH and temperature (the interactions the analysis of variance
found significant) are now in the factor block. PLS fits these terms to all ten time points at once,
returning a predicted development curve, where the analysis of variance fitted the same terms to a
single summary of each curve, its peak.

How many components to keep is a modelling choice, guided by the in-sample R2Y and the
cross-validated :math:`Q^2_Y`. The :math:`Q^2_Y` is the fraction of the response variation the model
predicts for runs it did not see: leave out each run in turn, refit, and predict the held-out curve.
``pls.cross_validate`` returns a per-response :math:`Q^2_Y`; averaged over the ten time points at
each number of components:

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

The regression and PLS can be compared on equal footing. Giving PLS the same single response the
regression used, the peak, and the same interaction terms, its ``beta_coefficients_`` line up against
the least-squares coefficients term by term:

.. code-block:: python

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

The two sets of coefficients differ by at most 0.03 across the 24 terms. The concentration coefficient
(about 0.40, it raises the peak for every compound) and the pH main effect (about :math:`-0.21`, the
average pH slope) match the regression closely; the three-component PLS pulls a few of the smaller
interaction terms toward zero, the shrinkage that comes from describing the response with fewer
directions than the model has terms. Every difference is small next to the least-squares standard
errors: the PLS coefficient lies within one standard error of the regression estimate for all but two
of the 24 terms (the largest gap is 1.4 standard errors), so on this data the two fits are
indistinguishable term by term. With all five components they are nearly identical.

How large that difference is depends on the coding. Under sum coding the compound contrast columns
are close to uncorrelated, so the low-rank PLS fit barely disturbs them. Reference coding (each
compound measured against A, as in the main-effects model) makes those columns correlated, and the
three-component PLS then shrinks the compound coefficients more: the PLS and least-squares
coefficients differ by up to 0.10 rather than 0.03. The fitted model, the predictions, and the
interaction tests are identical either way; what changes is how the coefficients divide the compound
effect between the levels, and how far the truncated PLS moves them.

The reason to use PLS here is not a different answer on the peak, but that the same model extends
directly to the full ten-point curve, and to responses with more columns than the design has runs,
where ordinary least squares cannot be fitted at all.

The full coefficient table, in the same order as the plot below (largest least-squares
coefficient first, smallest last), sets the three-component PLS coefficient beside the
least-squares one, with the least-squares standard error, t-statistic, and p-value:

.. list-table:: PLS and least-squares coefficients for the peak colour intensity, largest to smallest
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
    *   - ``cmpA:co_solvent``
        - +0.097
        - +0.111
        - 0.024
        - +4.6
        - <0.001
    *   - ``cmpB:pH``
        - +0.116
        - +0.107
        - 0.021
        - +5.1
        - <0.001
    *   - ``cmpC:temperature``
        - +0.083
        - +0.097
        - 0.021
        - +4.6
        - <0.001
    *   - ``cmpB:co_solvent``
        - +0.083
        - +0.081
        - 0.021
        - +3.8
        - <0.001
    *   - ``cmpE:pH``
        - +0.059
        - +0.069
        - 0.024
        - +2.9
        - 0.007
    *   - ``cmpC``
        - +0.064
        - +0.067
        - 0.019
        - +3.6
        - <0.001
    *   - ``temperature``
        - +0.058
        - +0.057
        - 0.010
        - +5.7
        - <0.001
    *   - ``cmpE:co_solvent``
        - +0.027
        - +0.034
        - 0.023
        - +1.5
        - 0.147
    *   - ``cmpE:temperature``
        - +0.014
        - +0.021
        - 0.024
        - +0.9
        - 0.372
    *   - ``cmpA:temperature``
        - -0.040
        - -0.038
        - 0.024
        - -1.6
        - 0.120
    *   - ``cmpB:temperature``
        - -0.035
        - -0.042
        - 0.023
        - -1.9
        - 0.071
    *   - ``cmpC:co_solvent``
        - -0.082
        - -0.066
        - 0.025
        - -2.7
        - 0.011
    *   - ``cmpB``
        - -0.072
        - -0.089
        - 0.018
        - -5.0
        - <0.001
    *   - ``cmpA``
        - -0.114
        - -0.135
        - 0.018
        - -7.3
        - <0.001
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

Most terms are significant at the 0.05 level. The exceptions are four of the temperature and
co-solvent interactions for individual compounds (``cmpE:co_solvent``, ``cmpE:temperature``,
``cmpA:temperature``, ``cmpB:temperature``, with p-values from 0.07 to 0.37): the interaction is
present for the set of compounds, which the analysis of variance tested jointly, but not resolved
for each compound on its own at this run count. Because this is sum coding, each ``cmp`` term is the
compound's departure from the average; the same fit read under reference coding would instead show
each compound's difference from A, and compound B would then stand out as close to A across the
range.

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

Scores and loadings of the interaction model
--------------------------------------------

The interaction model was fitted to the full ten-point curve once already, to read its
:math:`R^2_Y` and :math:`Q^2_Y` by component. The coefficient comparison that followed reduced the
response to the single peak, to line the coefficients up against ordinary least squares, and the
score and loading plots shown so far were for the main-effects model. Fitting the interaction model
to the full curve again, at the three components kept above, gives scores and loadings for the
expanded model on the whole profile:

.. code-block:: python

    pls_full = PLS(n_components=3, scale=True).fit(X_int, curves)
    print(pls_full.r2_cumulative_)             # 0.77, 0.85, 0.88

    tscore = np.asarray(pls_full.scores_)      # X scores, one row per run
    wstar = pls_full.direct_weights_           # W*: the 24 model terms
    cw = pls_full.y_weights_                   # C: the ten time points

    palette = ["#1f5fa8", "#c0392b", "#2e8b57", "#8e44ad", "#d68910", "#17a2b8"]
    colour_of = dict(zip(compounds, palette))

    # Score plot: four encodings on one point. Colour is the compound (as before); marker shape is
    # the pH level (down triangle low, circle high); marker size grows with the concentration; and
    # the co-solvent is an open, outline-only marker at the low setting and a filled marker at the
    # high setting (the "-open" symbol suffix draws the outline only).
    base = np.where(adf["pH"] < 0, "triangle-down", "circle")
    symbol = np.where(adf["co_solvent"] < 0, np.char.add(base, "-open"), base)
    size = 8 + 5 * (adf["concentration"] + 1)          # coded concentration in [-1, 1]

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
time point at a time, which ``r2y_per_variable_`` gives directly (its last column is the cumulative
:math:`R^2_Y` per response at the three-component model):

.. code-block:: python

    print(pls_full.r2y_per_variable_.iloc[:, -1].round(2))   # R2Y per time point, three components

.. list-table:: :math:`R^2_Y` per time point for the three-component model
    :widths: 30 20
    :header-rows: 1

    *   - Time point
        - :math:`R^2_Y`
    *   - t0
        - 0.16
    *   - t1
        - 0.95
    *   - t2
        - 0.96
    *   - t3
        - 0.97
    *   - t4
        - 0.97
    *   - t5
        - 0.97
    *   - t6
        - 0.97
    *   - t7
        - 0.96
    *   - t8
        - 0.94
    *   - t9
        - 0.92

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
mean first score moves from :math:`-0.96` at the low concentration to :math:`+0.55` at the high. The
down triangles (low pH) also lie to the right of the circles, because a lower pH raises the
colour for this chelate; the mean first score is :math:`+0.58` at low pH against :math:`-0.33` at
high. Reading shape and size together, the runs high on component 1 are the high-concentration,
low-pH runs, which is where the deepest colour is expected.

Component 2 carries only eight percent of the response variation, and the loadings place the
compound-by-temperature terms at one end of it and the pH and concentration terms at the other, so it
is a weaker, temperature-leaning direction. One run stands apart low on component 2: its encoding
reads as compound F at the low pH and high concentration, an unusual corner of the region for that
compound. A score plot is where such a run shows up, and the encoding names the run's settings
without a lookup.

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
relative to it. Two distances summarise that. Hotelling's :math:`T^2` measures how far a run lies
from the centre *within* the model plane, scaled by the score spread; the squared prediction error
(SPE) measures how far it lies *off* the plane, the part of the ten-point curve the three components
do not reconstruct. Each has a 95% limit, from ``hotellings_t2_limit`` and ``spe_limit``.

New rows are needed here and in the inversion that follows, so a small helper builds a model-matrix
row for one setting with the same coding as the fitted matrix:

.. code-block:: python

    from patsy import build_design_matrices

    info = dmatrix(rhs, adf, return_type="dataframe").design_info

    def encode(compound, concentration, co_solvent, pH, temperature):
        row = pd.DataFrame({"compound": [compound], "concentration": [concentration],
                            "co_solvent": [co_solvent], "pH": [pH], "temperature": [temperature]})
        return build_design_matrices([info], row, return_type="dataframe")[0].drop(columns=["Intercept"])

The fourth question asks which candidate develops colour like the reference chromogen A. To make that
precise, take chromogen A at the centre point, the nominal mid-range value of every continuous factor,
as the *goal*: the colour-development profile to reproduce. Projecting the goal onto the model gives
its score and its own SPE and :math:`T^2`, so it can be checked the same way as any run before it is
used. The projection is ``diagnose``, which returns the scores, SPE, :math:`T^2` and predicted curve
for new rows (SPE for a model with named columns reads correctly from process-improve 1.52.4 onward):

.. code-block:: python

    goal_x = encode("A", concentration=0, co_solvent=0, pH=0, temperature=0)
    goal = pls_full.diagnose(goal_x)
    print(float(goal.spe.iloc[0]), float(goal.hotellings_t2.iloc[0]))   # 1.7, 0.05

    t2 = pls_full.hotellings_t2_.iloc[:, -1]        # per-run T2 at three components
    spe = pls_full.spe_.iloc[:, -1]                 # per-run SPE at three components
    print(pls_full.hotellings_t2_limit(), pls_full.spe_limit())         # 8.7, 6.5

    fig = go.Figure()
    for c in compounds:
        m = (design.design["compound"] == c).to_numpy()
        fig.add_scatter(x=t2[m], y=spe[m], mode="markers", name=c)
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
:math:`T^2` limit and five beyond the SPE limit, are all compound F. That grouping is a property of
the sum coding used for the compound factor, not of F's chemistry: the :ref:`next section
<profile-categorical-coding>` writes the same model three ways and shows the flag move from F to
another level, or disappear, as the coding changes. The goal check is unaffected, because chromogen
A, the reference, is never the omitted level, so it projects to a low-leverage, well-reconstructed
point under every coding tried (its :math:`T^2` stays near or below 0.1 and its SPE between about 1
and 2).

.. figure:: ../figures/doe/colour-pls-t2-spe.png
    :align: center
    :width: 680px
    :alt: colour-pls-t2-spe.py

    Hotelling's :math:`T^2` against SPE for the sixty runs, with the 95% limits as dashed lines. A
    run in the lower-left rectangle is within both. Several compound-F runs cross the limits, a
    consequence of F being the omitted sum-coding level rather than a fault in those runs. The
    reference goal, chromogen A at the centre point (asterisk), sits well inside both limits, so its
    predicted profile can be used as an inversion target.

.. _profile-categorical-coding:

Coding the categorical factor
-----------------------------

The compound has entered every model so far through sum-to-zero coding, written
``C(compound, Sum)``. That is one of several ways to turn a categorical factor into numeric columns,
and the choice has stayed in the background: the interaction F-tests did not depend on it, and the
least-squares coefficients only divided the compound effect differently between the levels. The
diagnostics just raised it directly, with every flagged run belonging to the omitted level. This
section writes the same model three ways to separate what the coding changes from what it does not.

Three codings of a six-level factor are in common use:

- **Sum (effects) coding**, ``C(compound, Sum)``: each column is a compound's departure from the
  average of all six. One level is omitted and carried as the negative sum of the other five
  contrasts, so it has no column of its own and its runs sit at the corner of the contrast space
  farthest from the centre.
- **Treatment (reference) coding**, ``C(compound, Treatment)``: each column is a compound's
  difference from a chosen reference level, here A. The reference is the all-zero row.
- **Cell-means coding**, ``0 + C(compound)``: every compound has its own indicator column, with no
  intercept and no omitted level.

All three span the same model space: any fit written in one can be rewritten in the others, and a
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
    for a in (1, 2, 3):                 # three model terms, so three components is full rank
        p_sum = PLS(n_components=a, scale=True).fit(X_sum, ydf).predictions_
        p_trt = PLS(n_components=a, scale=True).fit(X_trt, ydf).predictions_
        print(a, float(np.max(np.abs(np.asarray(p_sum) - np.asarray(p_trt)))))
    # 1 -> 0.37, 2 -> 0.17, 3 -> 0.00

The full-rank ordinary least squares predictions match to :math:`10^{-15}` across the two codings. A
PLS kept at one or two components does not: its predictions differ by 0.37 and 0.17 between sum and
treatment coding, and only at three components, which is full rank for a three-term model, do they
agree. The reason is in how each method builds its fit. Ordinary least squares projects the response
onto the column space of the model, and that subspace is the same for every coding, so the fitted
values are identical. PLS builds its components to maximise the covariance between a score direction
and the response; the leading directions depend on the actual numbers in the model matrix, which the
coding sets, so a PLS truncated below full rank keeps a coding-specific summary. Centring and scaling
a component model shift its fit in the same way, and for the same reason (Bro and Smilde, 2003, on
centring and scaling in component analysis). At
full rank the truncation is gone and PLS spans the same space as least squares, so the dependence
disappears; below full rank it remains.

The interaction model here keeps three of a possible twenty-four components, well below full rank, so
the coding has an effect. Its cumulative :math:`R^2_Y` at three components is 0.88 under sum coding,
0.90 under treatment coding, and 0.91 under cell-means coding: the same model space, but a
rank-three truncation keeps a different part of it in each case.

The clearest place to see the effect is the leverage diagnostic. Refitting the three-component model
under each coding and reading Hotelling's :math:`T^2` per run:

.. code-block:: python

    rhs_sum = rhs                                       # C(compound, Sum)*... from earlier
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
The omitted level's runs are pushed out because sum coding places them at the :math:`(-1, \ldots, -1)`
corner and ``scale=True`` then gives that corner column unit variance, raising its leverage; the
effect belongs to the parameterization, and it moves with whichever level is omitted. This is why the
diagnostics flagged F: F is the level sum coding drops, not a run the chemistry sets apart.

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
projection stays inside both limits under every coding: chromogen A at the centre point is not an
omitted level in any of them, so its :math:`T^2` stays near or below 0.1 and its SPE between about 1
and 2. The goal check the inversion relies on does not depend on the choice.

The practical risk is a false alarm. A run past the :math:`T^2` or SPE limit is the usual signal to
set that run aside, and here that signal falls on every run of the omitted level for a reason that
has nothing to do with the response. Acting on it would set aside compound F, which the validation
below finds to be one of the closest matches to the reference, so a coding choice would remove a
leading candidate. The guard is to not read an exclusion off a single coding: before setting a
compound aside, refit under another coding, or check the raw curve, and keep the exclusion only if
the flag survives. A designed experiment also places its runs at the edges of the region on purpose,
so high leverage there is expected and is not by itself a reason to drop a run.

What else depends on the coding is any reading taken from the truncated score, including the model
inversion in the next section, where the reachable set of candidates changes with the coding.

Which compound matches the reference
------------------------------------

The fourth question is which candidate can be made to develop colour like the reference. With the
goal profile fixed, that becomes a model-inversion question: for each candidate chromogen, what
settings of the four continuous factors place its score on the goal? Inversion runs the model
backwards, from a target score to the factors that reach it. The :ref:`product-development chapter
<LVM_model_inversion_example>` sets this out for a PCA model, using the loadings to map a target score
to a recipe; here the same idea is applied to the PLS interaction model, with the compound held fixed
and the continuous factors as the manipulated variables. The starting point for the method is Jaeckle
and MacGregor's 1998 paper on product design through multivariate analysis of process data.

The forward map is ``pls_full.transform(X)``: it standardizes the model-matrix row and multiplies by
the direct weights :math:`\mathbf{W}^*`. Holding the compound fixed makes this map affine in the four
continuous factors, so matching the three-component goal score is a small linear system, built here
by reading the score at the centre and along each continuous factor in turn. Four factors against
three components leaves one free direction, the operating window; the least-squares solution is the
minimum adjustment from the nominal centre.

.. code-block:: python

    import numpy as np

    t_goal = pls_full.transform(goal_x).to_numpy().ravel()

    def compensate(compound):
        base = pls_full.transform(encode(compound, 0, 0, 0, 0)).to_numpy().ravel()
        step = np.column_stack([
            pls_full.transform(encode(compound, *[float(k == j) for k in range(4)])).to_numpy().ravel() - base
            for j in range(4)])
        coded, *_ = np.linalg.lstsq(step, t_goal - base, rcond=None)
        return coded            # coded [concentration, co_solvent, pH, temperature]

    for c in ["B", "C", "D", "E", "F"]:
        print(c, np.round(compensate(c), 2))

Converting each coded setting to real units gives the recipe that would make each candidate reproduce
the reference profile:

.. list-table:: Continuous-factor settings that reproduce the reference goal (chromogen A at centre)
    :widths: 16 20 18 12 18 24
    :header-rows: 1

    *   - Chromogen
        - Concentration (umol/L)
        - Co-solvent (% v/v)
        - pH
        - Temperature (degC)
        - Within studied ranges?
    *   - A (reference)
        - 5.0
        - 15.0
        - 5.5
        - 25.0
        - nominal centre
    *   - B
        - 4.9
        - 14.8
        - 5.4
        - 25.6
        - yes
    *   - C
        - 5.5
        - 13.5
        - 6.1
        - 27.7
        - yes
    *   - D
        - 5.1
        - 13.6
        - 6.1
        - 27.2
        - yes
    *   - E
        - 5.4
        - 6.9
        - 7.7
        - 31.0
        - no: pH above 7.0
    *   - F
        - 8.7
        - 15.5
        - 8.2
        - 28.0
        - no: concentration and pH above range

The studied ranges are concentration 2 to 8 umol/L, co-solvent 5 to 25% v/v, pH 4.0 to 7.0, and
temperature 15 to 35 degC. Chromogen B needs almost no change from the nominal centre. C and D need a
moderate move, a higher pH and temperature, but stay inside the ranges. E and F fall outside the
window: E at a pH of 7.7 and F at a pH of 8.2 and a concentration of 8.7 umol/L, beyond the values the
experiment explored. This table is the inversion read under sum coding. Because the three-component
score is coding-dependent, as the :ref:`coding section <profile-categorical-coding>` showed, so is
the reachable set, and the paragraphs below repeat the inversion under the other codings and under a
reading that does not depend on the coding at all.

.. figure:: ../figures/doe/colour-pls-inversion.png
    :align: center
    :width: 720px
    :alt: colour-pls-inversion.py

    The inverted continuous-factor settings that place each candidate on the reference goal, in coded
    units, one row per factor. The shaded band between the dashed lines at :math:`-1` and :math:`+1`
    is the studied range. B, C and D are reachable within the ranges; E and F need a pH (and, for F, a
    concentration) beyond the studied window, marked with a heavy outline.

The compensation figure shows the coded settings directly; a Plotly version, with the studied range
shaded:

.. code-block:: python

    factors = ["concentration", "co_solvent", "pH", "temperature"]
    coded = pd.DataFrame({c: compensate(c) for c in ["B", "C", "D", "E", "F"]}, index=factors)

    fig = go.Figure()
    fig.add_vrect(x0=-1, x1=1, fillcolor="#e8eef5", line_width=0)
    for c in coded.columns:
        fig.add_scatter(x=coded[c], y=factors, mode="markers", name=c)
    fig.update_layout(xaxis_title="coded setting to match the goal (0 = nominal centre)")
    fig.show()

Inversion is non-unique, and this reports one member of the operating window, the smallest move from
the nominal centre. A subject-matter expert might spend the free direction differently, for instance
holding one factor fixed and solving for the rest, as the :ref:`product-development worked example
<LVM_model_inversion_example>` does with a fixed hardness. That freedom is a property of the score
match under any coding; the reachable set, in contrast, moves with the coding.

Repeating the score match under treatment and cell-means coding gives a different reachable set each
time. Under sum coding B, C and D are inside the ranges; under treatment coding all five candidates
are; under cell-means coding B, C, D and F are, while E is not. B, C and D are reachable under every
coding, and E and F move in and out. The three codings answer the same question about the same data
and return three different candidate lists.

.. figure:: ../figures/doe/colour-coding-inversion.png
    :align: center
    :width: 720px
    :alt: colour-coding-inversion.py

    Which candidates can be brought onto the reference goal within the studied ranges, under four
    ways of posing the inversion. The first three match the three-component score, one per coding, and
    give three different reachable sets. The fourth matches the predicted ten-point curve at full
    rank, which is the same under any coding, and places only F inside the ranges.

A reading that does not depend on the coding matches the predicted curve rather than the score. The
predicted ten-point profile is a full-rank quantity, identical under every coding, so requiring a
candidate's predicted curve to reach the goal's gives one answer. The match is over-determined, ten
time points against four factors, so it returns the least-squares closest curve:

.. code-block:: python

    from patsy import build_design_matrices

    info_full = dmatrix(rhs, adf, return_type="dataframe")       # keep the intercept: full rank
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
        return coded            # coded [concentration, co_solvent, pH, temperature]

    for c in ["B", "C", "D", "E", "F"]:
        print(c, np.round(curve_match(c), 2))

The curve match keeps F inside the studied box, and places the others outside it: B needs a
co-solvent below 5% v/v and a pH below 4.0; C and D a pH near 8, with D also a co-solvent of 45% v/v;
E a temperature near :math:`-28` degC. A setting outside the box is not disqualifying here. The design
established the factor effects, so stepping a little past the studied region is a testable
extrapolation, the explore side of a response-surface search, paid for by a larger prediction variance
the farther out the setting sits. What a setting is worth is a separate question from whether it lies
inside the box, and it is checked directly below by putting the settings through the known ground
truth. The score match and the curve match ask different questions. Matching a three-component score
asks a candidate to reach a low-rank summary of the goal, which several candidates do with small
moves; matching the full curve asks it to reproduce the whole profile, which the continuous factors
mostly cannot, because they move the curve's amplitude while the compounds differ in late-time shape.
Shape, not amplitude, is the binding constraint, which returns to the shape-distance ranking that
opened the fourth question: B is closest to the reference in shape, then F.

Checking the inversion against the known ground truth
-----------------------------------------------------

Because the curves here are generated from a known ground truth, the inverted settings can be checked
against it directly: take each candidate's settings, in real units and including those outside the
box, put them back through the ground-truth curve, and measure how far the result sits from the
reference profile.

.. code-block:: python

    def true_curve(compound, coded):                     # the ground truth defined earlier
        drift, s_co, s_ph, s_tp = truth[compound]
        amp = max(1.0 + 0.35 * coded[0] + s_co * coded[1] + s_ph * coded[2] + s_tp * coded[3], 0.05)
        return amp * np.clip(ref + drift * tail, 0, None)

    goal_curve = true_curve("A", [0, 0, 0, 0])           # the reference profile to reproduce
    noise = 0.03                                          # measurement-noise standard deviation

    for c in ["B", "C", "D", "E", "F"]:
        got = true_curve(c, curve_match(c))              # curve_match(c) from the block above
        rmse = float(np.sqrt(np.mean((got - goal_curve) ** 2)))
        print(c, round(rmse, 3), round(rmse / noise, 1))

The continuous factors move only the amplitude, so the closest any setting can bring a candidate to
the reference is set by that candidate's fixed shape, its late-time drift. The best attainable
match, the smallest root-mean-square deviation from the reference reachable at any amplitude, orders
the candidates by drift:

.. list-table:: How close each candidate can be brought to the reference, limited by its fixed shape
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
        - 0.031
        - 1.0
    *   - C
        - +0.20
        - 0.055
        - 1.8
    *   - D
        - +0.30
        - 0.079
        - 2.6
    *   - E
        - +0.35
        - 0.090
        - 3.0

Running the curve-match settings through the ground truth reaches that best attainable match for the
near candidates: B lands at 0.016, F at 0.043, and C at 0.060, all within about two measurement-noise
standard deviations of the reference (and the in-range cell-means score match reaches them too, at B
0.018, C 0.056, F 0.031). D and E stay at 2.6 times the noise or worse whatever the factors are set
to, inside the box or outside it, because their shape gap is too large for amplitude to close.

.. figure:: ../figures/doe/colour-inversion-validation.png
    :align: center
    :width: 780px
    :alt: colour-inversion-validation.py

    Left: the reference curve (chromogen A at the centre point) with the closest emulation each
    candidate can reach, the best amplitude for its fixed shape. The candidates track the reference
    early and separate at the tail, by their late-time drift. Right: the emulation error against the
    measurement-noise scale, each candidate's best attainable match (open marker) and what the
    coding-invariant curve-match inversion reaches when its real-unit settings are put through the
    ground truth (filled marker), ordered by drift. B and F land within about one noise standard
    deviation of the reference, C within two; D and E cannot be brought closer than 2.6 times the
    noise.

So the inversion does its job: for each candidate it finds settings that bring the curve as close to
the reference as that candidate's shape allows, and the closed-loop check confirms this against the
known truth. The ordering it recovers, B then F then C then D then E, is the late-time-drift ordering,
the shape difference the fourth question was built around.

One variant of the inversion is worth ruling out. The inversions above hold each candidate on the
goal's projection, matching its three-component score or its predicted curve, so each solution sits
close to the model plane. Muteki and MacGregor (2007) instead pose the inversion as an optimization
that minimizes the distance to the target while keeping Hotelling's :math:`T^2` and the SPE below
their limits, letting the solution float off the plane rather than lie on it. Allowing that here,
with :math:`T^2` and SPE free to rise to their 95% limits, does not bring any candidate below its
best attainable match:

.. code-block:: python

    from scipy.optimize import minimize

    t2_lim, spe_lim = pls_full.hotellings_t2_limit(), pls_full.spe_limit()

    def t2_spe(compound, coded):                     # 3-component diagnostics of an inverted point
        d = pls_full.diagnose(encode(compound, *coded))
        return float(d.hotellings_t2.iloc[0]), float(d.spe.iloc[0])

    def relaxed_inversion(compound):                 # Muteki and MacGregor (2007), their equation 5
        objective = lambda c: float(np.sum((y_goal - curve_of(compound, c)) ** 2))
        limits = [{"type": "ineq", "fun": lambda c: t2_lim - t2_spe(compound, c)[0]},
                  {"type": "ineq", "fun": lambda c: spe_lim - t2_spe(compound, c)[1]}]
        return minimize(objective, np.zeros(4), method="SLSQP", constraints=limits).x

    for c in ["B", "C", "D", "E", "F"]:
        settings = relaxed_inversion(c)
        rmse = np.sqrt(np.mean((true_curve(c, settings) - goal_curve) ** 2))
        print(c, round(float(rmse), 3))              # 0.016  0.058  0.094  0.100  0.043

Each relaxed solution lands at or above its candidate's best attainable match (B at 0.016 and D at
0.094, whose best matches are 0.015 and 0.079), while its SPE rises to the 6.5 limit and its
settings leave the studied ranges. Pinning the two hard-to-change factors, temperature and co-solvent, at the
centre and re-optimizing over concentration and pH alone gives the same result. The off-plane
freedom the continuous factors can reach is amplitude, not shape, so it cannot close a compound's
late-time drift:
the closest attainable curve stays the projection of the target, which is Muteki and MacGregor's
feasibility condition.

Read together, the answer to which compound matches the reference is not one candidate but a graded
ranking, and it depends on how the question is posed. The score match returns a binary reachable set
that changes with the coding and with where the studied box is drawn, a statement about a low-rank
projection. The curve match, checked against the ground truth, gives the reading that holds: the
candidates line up by their fixed curve shape, with B and F reproducing the reference to within about
the measurement noise, C to within roughly twice it, and D and E not reproducible however the factors
are set. F is not singled out; it sits second behind B, which the shape-distance ranking said at the
start.

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
(objectives 1 to 3); inverting the model onto a reference goal, then checking the inverted settings
against the known ground truth, ranks the candidates by their fixed curve shape, with B and F
reproducing the reference to within about the measurement noise and C to within roughly twice it,
while the low-rank score match's binary reachable set was found to depend on the categorical coding
(objective 4); and the fitted model over the continuous factors locates settings for a target colour
intensity for the chosen compound (objective 5). The same design supported a scalar analysis of variance on the peak, a multivariate model of the
full curve, and the inversion of that model back to factor settings, because the design was chosen for
the model, not for a particular way of reducing the response.
