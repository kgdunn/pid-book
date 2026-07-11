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
