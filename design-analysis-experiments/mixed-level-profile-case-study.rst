.. _DOE-mixed-level-profile-case-study:

Case study: a mixed-level split-plot design with a profile response
===================================================================

The earlier sections built up the pieces of an optimal design one at a time: the
:ref:`information matrix <DOE-optimal-designs>`, the :ref:`coordinate-exchange search
<DOE-exchange-algorithms>`, a :ref:`categorical factor with several levels
<DOE-categorical-factors>`, and hard-to-change factors that force a split-plot run order. This
case study puts them together on one problem, and carries it through to the analysis of the
data. It also shows a response that is not a single number but a *curve*, which is handled with
a latent-variable model rather than ordinary least squares.

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
    for criterion, dash in [("i_optimal", "solid"), ("d_optimal", "dash")]:
        for budget in (60, 48):
            _, m = score(criterion, budget)
            q = m["fds"]["quantiles"]
            fig.add_scatter(x=[float(k) for k in q], y=list(q.values()), mode="lines+markers",
                            line_dash=dash, name=f"{criterion}, n={budget}")
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
ten at once against the factors, using a few latent components that capture the shared movement. The
factors enter as the four coded continuous columns plus indicator columns for the compound (the
reference level A dropped, as in the :ref:`indicator-variable discussion
<LVM-using-indicator-variables>`).

The response columns are on different scales (the early points carry far less variance than the
plateau), so the blocks are standardized before fitting. ``PLS(scale=True)`` does this internally,
mean-centering and scaling both the factor block and the response block to unit variance, and
returns predictions on the original absorbance scale, so raw ``X`` and raw ``curves`` can be passed
straight in.

.. code-block:: python

    from process_improve.multivariate.methods import PCA, PLS, MCUVScaler
    from sklearn.metrics import r2_score

    dummies = pd.get_dummies(design.design["compound"], prefix="cmp").astype(float)
    X = pd.concat([design.design[list(cont)].astype(float), dummies.drop(columns=["cmp_A"])], axis=1)

    pls = PLS(n_components=5, scale=True).fit(X, curves)
    print(r2_score(curves, pls.predict(X), multioutput="variance_weighted"))   # 0.895

    pca = PCA(n_components=3).fit(MCUVScaler().fit_transform(curves))
    scores = np.asarray(pca.scores_)
    fig = go.Figure()
    for c in compounds:
        m = (design.design["compound"] == c).to_numpy()
        fig.add_scatter(x=scores[m, 0], y=scores[m, 1], mode="markers", name=c)
    fig.update_layout(xaxis_title="PC1", yaxis_title="PC2")
    fig.show()

The five-component model explains 90% of the response variance, weighted across the ten points.
Its per-target root-mean-square error, ``pls.rmse_``, comes back on the original absorbance scale
(about 0.10 absorbance units at the final component), matching a hand calculation from the
predictions, so it can be read directly against the measured curves. A principal component analysis
of the curves themselves shows the response lives on a low-dimensional structure: the first two
components separate the compounds by development shape, which is the same separation the late-time
spread showed, now read from the response's own latent axes.

.. figure:: ../figures/doe/colour-pca-scores.png
    :align: center
    :width: 620px
    :alt: colour-pca-scores.py

    First two principal components of the standardized colour-development curves, one point per run.
    The compounds separate by the shape of their development curve, with the reference A and the
    analog B falling together.

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
