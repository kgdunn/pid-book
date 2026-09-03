.. _DOE-omnibus-comparison:

An omnibus comparison across design families
============================================

The :ref:`two-design comparison <DOE-dsd-omars-comparison>` made its point on a narrow contest. Widen it now to the six families a
practitioner would actually shortlist for **five** factors on the same
main-effects-and-quadratic model (eleven terms: an intercept, five linear, and five pure
quadratic, with no two-factor interactions): a full :math:`2^5` factorial, a resolution-V
:math:`2^{5-1}` fractional factorial, a :ref:`central composite design <DOE_central_composite_designs>`,
a :ref:`Box-Behnken design <DOE-box-behnken-designs>`, a :ref:`definitive screening design
<DOE-definitive-screening-designs>`, and an :ref:`OMARS design <DOE-omars-designs>`. The run
counts differ, and we do not pad them to match: comparing designs at their natural sizes is the
whole point. Every design here is confined to the coded range :math:`[-1, 1]` on each factor, so
the contest is like-for-like on one fixed experimental region. The fuller second-order story, with
all the two-factor interactions, is where strong OMARS and composite designs really compete; the
script that backs this section builds that model too, but the comparison below holds to
main-effects-and-quadratics so it lines up with the rest of the chapter. Holding the
two-factor interactions out is an assumption: if they are in fact present, they bias the
eleven estimated coefficients by the :ref:`alias matrix <DOE-alias-bias>`, and the table
below records how large that bias can be for each design.

Can the design fit the model?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start with the question that decides whether a design belongs in the contest at all: can it even
fit the model?

.. list-table:: Which designs can fit the five-factor main-effects-and-quadratic model.
    :header-rows: 1
    :widths: 34 12 22 32

    *   - Design (5 factors)
        - Runs
        - Fits the 11-term model?
        - Residual degrees of freedom
    *   - Full factorial, :math:`2^5` + 2 centre
        - 34
        - no (rank 7)
        - 27, reduced model only
    *   - Fractional, :math:`2^{5-1}` + 2 centre
        - 18
        - no (rank 7)
        - 11, reduced model only
    *   - CCD, face-centred
        - 32
        - yes
        - 21
    *   - Box-Behnken
        - 46
        - yes
        - 35
    *   - DSD
        - 13
        - yes
        - 2
    *   - OMARS
        - 25
        - yes
        - 14

Both two-level factorials fail outright, and adding centre points does not rescue them. At two
levels every :math:`x_i^2` column equals 1, and at the centre it equals 0, so all five quadratic
columns are *identical*: the eleven-term model collapses to rank 7 (the intercept, five linear
terms, and a single lumped curvature direction). The centre runs still earn their place, they
supply an estimate of :math:`\sigma^2`, a few residual degrees of freedom, a check on
between-run drift, and a one-degree-of-freedom test for *overall* curvature, but they cannot tell
the five quadratics apart. That single curvature signal is precisely the cue to augment the
factorial with axial runs, which is how the face-centred composite design in the same table is
born. The four remaining designs are full rank and carry the comparison from here.

Power to detect an effect
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Lead with power, because it is what the experiment is for.** The figure below reads off the four
designs' ability to flag a true effect of one noise standard deviation
(:math:`\delta = \sigma`) at :math:`\alpha = 0.05`.

The four response-surface designs are built once here and reused for the table and the FDS
panels that follow. ``process_improve`` builds the Box-Behnken design and the DSD directly,
builds the face-centred CCD on a resolution-V half-fraction cube with ``cube="fractional"``
(the standard five-factor CCD; the library's default cube is the full factorial), and builds the
OMARS design with ``generate_omars``. We ask it for a twenty-five-run, five-factor member on the
main-effects-and-quadratic model, selected for precision (A-optimality); the definitive screening
design is the minimal member of the same foldover family, and the twenty-four design runs are
folded around one centre run. It has the defining OMARS property, main effects orthogonal to every
second-order term, which the library's ``is_omars`` verifier confirms. This is one member of a
large family: the :ref:`OMARS catalogue <DOE-omars-designs>` holds many twenty-five-run members
that place their runs differently and so score differently on the metrics below, and the generator
returns the one its A-optimality search settles on.

Each design carries its textbook number of center runs rather than padding added to equalize the
comparison: six for the Box-Behnken design (the canonical 46-run design is forty design runs plus
six center runs) and six for the face-centred CCD, against one each for the definitive screening and
OMARS designs. Those center runs set the pure-error degrees of freedom and steady the prediction
variance near the center of the region. In practice one might add two or three further center runs
for a firmer estimate of the noise; here each design is held to its textbook count. One consequence
is worth keeping in view when reading the table: the six-versus-one difference in center runs is
itself part of the contrast, not a controlled-for constant. The extra center replication lowers the
larger designs' prediction variance near the center and adds residual degrees of freedom, so some of
that advantage comes from the replication rather than from where the non-center points are placed.

The power comes from ``evaluate_design``, given the eleven-term model as an explicit formula so
the library scores exactly this model and not the full second-order one:

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from process_improve.experiments import Factor, evaluate_design, generate_design, generate_omars

	names = list("ABCDE")
	factors = [Factor(name=c, low=-1, high=1) for c in names]
	model = " + ".join(names + [f"I({c}**2)" for c in names])   # 11 terms, no interactions

	def coded(result):
	    return np.asarray(result.design[names], float)

	bbd = coded(generate_design(factors, "box_behnken", n_center_points=6))
	dsd = coded(generate_design(factors, "dsd"))
	ccd = coded(generate_design(factors, "ccd", cube="fractional",
	                            alpha="face_centered", n_center_points=6))
	omars = coded(generate_omars(factors, n_runs=25, model="main_quadratic",
	                             selection_criterion="a_optimal"))
	designs = {"Box-Behnken": bbd, "CCD": ccd, "OMARS": omars, "DSD": dsd}

	def power(design):
	    df = pd.DataFrame(np.asarray(design), columns=names)
	    p = evaluate_design(df, model=model, metric="power",
	                        effect_size=1.0, sigma=1.0)["power"]
	    return p["A"], p["I(A ** 2)"]          # one main effect, one pure quadratic

	power_main = [power(d)[0] for d in designs.values()]
	power_quad = [power(d)[1] for d in designs.values()]
	fig = go.Figure([go.Bar(name="main effect", x=list(designs), y=power_main),
	                 go.Bar(name="quadratic effect", x=list(designs), y=power_quad)])
	fig.update_layout(barmode="group",
	                  yaxis_title="Power (delta = sigma, alpha = 0.05)")
	fig.show()

.. figure:: ../figures/doe/power-comparison-six-designs.png
    :align: center
    :width: 750px
    :alt: power-comparison-six-designs.py

    Power to detect a one-sigma main effect and a one-sigma quadratic effect, for the four
    response-surface designs on the five-factor model. More runs buy more power, and curvature is
    the harder target.

The thirteen-run DSD is visibly underpowered: a :math:`0.42` chance on a one-sigma main effect and
only :math:`0.15` on a quadratic of the same size. The run-richer designs all clear :math:`0.96`
on main effects, and the Box-Behnken design, the largest at forty-six runs, has the strongest
chance on curvature at :math:`0.82`, with the twenty-five-run OMARS design next at :math:`0.53`.
Power rewards the larger designs, which is the practical reading and exactly what an efficiency
score that normalizes out the number of runs would have hidden.

One caveat in the definitive screening design's favour, since its numbers look stark. A DSD is
built on an assumption of effect sparsity, not for this saturated eleven-term fit: its design
intent (Jones and Nachtsheim, 2011) is to project onto the few factors that turn out to be active
and estimate their quadratics cleanly, rather than to test all five quadratics at once on thirteen
runs. Held to the full model here it is being asked for more than it was built to give; the
comparison keeps it on the same model as the others to make that trade-off visible, not to mark it
a poor design.

Quality metrics for the four designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Quality metrics for the four response-surface designs (five factors).
    :header-rows: 1
    :widths: 40 15 15 15 15

    *   - Metric (arrow shows the preferred direction)
        - BBD [n=46]
        - CCD [n=32]
        - OMARS [n=25]
        - DSD [n=13]
    *   - :math:`\uparrow` Power, main effect at :math:`\delta = \sigma`
        - 0.97
        - 0.98
        - 0.96
        - 0.42
    *   - :math:`\uparrow` Power, quadratic at :math:`\delta = \sigma`
        - 0.82
        - 0.32
        - 0.53
        - 0.15
    *   - :math:`\downarrow` Average prediction variance, :math:`\sigma^2` units
        - 0.18
        - 0.31
        - 0.29
        - 0.71
    *   - :math:`\downarrow` Maximum prediction variance, :math:`\sigma^2` units
        - 0.84
        - 0.77
        - 0.51
        - 1.05
    *   - :math:`\downarrow` Maximum scaled prediction variance :math:`G`
        - 38.8
        - 24.6
        - 12.7
        - 13.6
    *   - :math:`\downarrow` Summed coefficient variance :math:`A`
        - 1.05
        - 2.39
        - 1.61
        - 3.70
    *   - :math:`\uparrow\ E`, smallest eigenvalue of :math:`\mathbf{X}^T\mathbf{X}`
        - 2.54
        - 2.00
        - 2.64
        - 0.85
    *   - :math:`\downarrow` Maximum :math:`|r|` among model terms
        - 0.15
        - 0.75
        - 0.31
        - 0.13
    *   - :math:`\downarrow` Maximum VIF
        - 1.20
        - 3.20
        - 1.21
        - 1.05
    *   - :math:`\downarrow` Maximum alias :math:`|\mathbf{A}|`, omitted interactions
        - 0.00
        - 0.00
        - 0.77
        - 1.09
    *   - :math:`\uparrow` D-optimal information :math:`|\mathbf{X}^T\mathbf{X}|^{1/p}`
        - 14.0
        - 8.97
        - 10.0
        - 5.19
    *   - :math:`\uparrow` D-efficiency, per run (see note)
        - 30.5%
        - 28.0%
        - 40.1%
        - 39.9%

Let's focus on the last row first. Recall what D-efficiency measures: it takes the determinant of
the information matrix :math:`\mathbf{X}^T\mathbf{X}`, raises it to the power :math:`1/p` to put it
on a per-coefficient scale, and then divides by the run count :math:`N`, reported as a percentage.
Dividing by :math:`N` measures information *per experiment*, not total information, and that single
normalisation flips the ranking. One more point on the scale: for this absolute percentage, 100%
would be a hypothetical orthogonal design (:math:`|\mathbf{X}^T\mathbf{X}| = N^p`), not the
D-optimal design. That ceiling is out of reach for a model with pure-quadratic terms on the coded
cube, since the squared columns cannot be made orthogonal to the intercept, which is why even the
strongest designs here sit near 30 to 40%. (A separate *relative* D-efficiency convention instead
takes the D-optimal design as 100%, so it is worth checking which one a given package reports.)

The two D rows make this concrete. The **unscaled** D-optimal information
:math:`|\mathbf{X}^T\mathbf{X}|^{1/p}` puts the Box-Behnken design highest at :math:`14.0` and the
thirteen-run DSD lowest at :math:`5.19`, the ranking the real-unit rows broadly agree on. Divide
that same determinant through by the run count and the row directly beneath it tells a different
story: per-run D-efficiency puts the twenty-five-run OMARS and the thirteen-run DSD highest, at
:math:`40.1\,\%` and :math:`39.9\,\%`, ahead of the forty-six-run Box-Behnken at :math:`30.5\,\%`.
The number is not wrong; it is answering a different question. Dividing by the run count measures
information per experiment, so a design that spends few experiments scores well on this row even
when, like the DSD, it carries the least total information and the weakest power. Scaled prediction
variance carries the same concern, and for the same reason it has been questioned in the design
literature (Anderson-Cook, Borror and Montgomery, 2009, and its published discussion; Goos and
Núñez Ares, 2025).

The quantities in real units, the **unscaled prediction variance** in :math:`\sigma^2`, the summed
coefficient variance :math:`A`, and the power, all reward the larger Box-Behnken design, which is
the reading that matches what the experiments can actually deliver.

The two maximum-variance rows report the worst case under each scaling, and they disagree most for
the designs at the extremes of run count. In real :math:`\sigma^2` units the thirteen-run DSD has
the highest maximum (:math:`1.05`), the worst single-point prediction at the bench, while the OMARS
design has the lowest (:math:`0.51`). The scaled maximum :math:`G`, which divides the worst-case
variance through by the run count, moves the DSD from worst to nearly best: it sits at :math:`13.6`,
just above the OMARS design's :math:`12.7`, while the forty-six-run Box-Behnken, with a moderate
unscaled maximum of :math:`0.84`, has the highest :math:`G` at :math:`38.8`. The reversal for the
DSD and the Box-Behnken is the same per-run normalisation seen in the two D rows; dividing by the
run count rewards the design that spends fewer experiments. Read the unscaled maximum for the
variance obtained at the bench, and the scaled :math:`G` to compare worst cases per experiment.

Aliasing from the omitted interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The alias row makes the cost of the reduced model explicit. The model fits no two-factor
interactions, so any that are present bias the coefficients we keep, by the
:ref:`alias matrix <DOE-alias-bias>`. The Box-Behnken and composite designs hold that bias
at zero on this model (:math:`|\mathbf{A}| = 0`): their quadratics are balanced against the
omitted interactions, so a present interaction leaves the fitted coefficients untouched. The
definitive screening and OMARS designs instead protect the main effects, whose alias is
zero, but let a present interaction shift a quadratic by a large fraction of a unit, up to
:math:`0.77` here for the OMARS design and :math:`1.09` for the definitive screening design.
Whether that matters is a question about the system rather than the design: it is the price of
setting the interactions aside, and it is why a follow-up design is run once a screening study
has flagged the active factors.

The pattern is easier to see than to tabulate. The figure below shows the absolute alias matrix
for each design as a heatmap, the eleven fitted terms down the rows and the ten omitted two-factor
interactions across the columns:

.. code-block:: python

	import numpy as np
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	# Reuses the designs dict, names and model (from the power block). evaluate_design
	# returns the alias matrix A = (X1'X1)^-1 X1'X2 directly: its rows are the eleven fitted
	# terms (intercept, main effects, quadratics) and its columns the ten omitted two-factor
	# interactions.
	fitted = ["1", "A", "B", "C", "D", "E", "A^2", "B^2", "C^2", "D^2", "E^2"]
	pairs = [a + b for i, a in enumerate("ABCDE") for b in "ABCDE"[i + 1:]]

	def alias_abs(d):
	    df = pd.DataFrame(np.asarray(d, float), columns=names)
	    a = evaluate_design(df, model=model, metric="alias_matrix")["alias_matrix"]["matrix"]
	    return np.abs(np.asarray(a, float))

	fig = make_subplots(rows=2, cols=2, subplot_titles=list(designs))
	for k, d in enumerate(designs.values()):
	    fig.add_trace(go.Heatmap(z=alias_abs(d), x=pairs, y=fitted, zmin=0, zmax=1.1,
	                             colorscale="Blues", showscale=(k == 0)),
	                  row=k // 2 + 1, col=k % 2 + 1)
	fig.update_yaxes(autorange="reversed")
	fig.show()

.. figure:: ../figures/doe/alias-matrix-heatmaps-four-designs.png
    :align: center
    :width: 750px
    :alt: Absolute alias-matrix heatmaps for the four candidate designs

    Absolute alias matrix :math:`|\mathbf{A}|` for the four designs (rows: the eleven fitted terms;
    columns: the ten omitted two-factor interactions). The Box-Behnken and composite designs hold
    every entry at zero on this model; the OMARS and definitive screening designs keep the
    main-effect rows at zero and carry the bias on the quadratic rows, up to :math:`0.77` and
    :math:`1.09` respectively.

The same entanglement is a correlation rather than a directed bias. The figure below shows the
absolute correlation among the twenty model-effect columns, in three blocks separated by lines: the
five main effects, the five quadratics, and the ten two-factor interactions the model leaves out.
Pearson correlation centers each column, so the quadratics' positive mean does not inflate the
values:

.. code-block:: python

	import numpy as np
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	# Twenty model-effect columns in three blocks: main effects, quadratics, then the omitted
	# interactions (pairs, from the previous block). Lines at 4.5 and 9.5 separate the blocks.
	model_terms = list("ABCDE") + ["A^2", "B^2", "C^2", "D^2", "E^2"] + pairs

	def model_term_corr(d):
	    d = np.asarray(d, float)
	    cols = ([d[:, i] for i in range(5)] + [d[:, i] ** 2 for i in range(5)]
	            + [d[:, i] * d[:, j] for i in range(5) for j in range(i + 1, 5)])
	    C = np.corrcoef(np.column_stack(cols), rowvar=False)   # Pearson centers each column
	    return np.abs(np.nan_to_num(C))

	fig = make_subplots(rows=2, cols=2, subplot_titles=list(designs))
	for k, d in enumerate(designs.values()):
	    r, c = k // 2 + 1, k % 2 + 1
	    fig.add_trace(go.Heatmap(z=model_term_corr(d), x=model_terms, y=model_terms,
	                             zmin=0, zmax=1, colorscale="Blues", showscale=(k == 0)),
	                  row=r, col=c)
	    for b in (4.5, 9.5):   # block-separating lines
	        fig.add_vline(x=b, line_width=1, line_color="gray", row=r, col=c)
	        fig.add_hline(y=b, line_width=1, line_color="gray", row=r, col=c)
	fig.update_yaxes(autorange="reversed")
	fig.show()

.. figure:: ../figures/doe/correlation-colormap-four-designs.png
    :align: center
    :width: 750px
    :alt: Absolute correlation colour maps among model-effect columns for the four designs

    Absolute correlation among the twenty model-effect columns, in three blocks (the main effects,
    the quadratics, and the two-factor interactions the model omits), separated by lines. The
    main-effect block is orthogonal to everything for every design. The main-effect and quadratic
    blocks are the fitted terms, so their worst off-diagonal is the table's maximum :math:`|r|` row
    (:math:`0.15`, :math:`0.75`, :math:`0.31`, :math:`0.13`); the stronger correlations,
    :math:`0.83` for the OMARS design and :math:`0.50` for the definitive screening design, sit in
    the blocks that involve the omitted interactions, the same aliasing the matrix above measures.

What the table compares
~~~~~~~~~~~~~~~~~~~~~~~~~

It is worth being clear about what the table compares. The model is already settled: we have
committed to the eleven-term main-effects-plus-quadratics model and are comparing point-placement
strategies, the designs, for estimating its coefficients and predicting from it. The criteria split
along exactly that line. For *estimation*, the determinant criterion :math:`D` (unscaled and per
run) and the summed coefficient variance :math:`A` summarise the whole parameter set, and
:math:`E`-optimality adds the worst single coefficient direction, the smallest eigenvalue of
:math:`\mathbf{X}^T\mathbf{X}`. It is the coefficient-space counterpart to the maximum prediction
variance; like :math:`A` and the prediction rows it places the DSD clearly last (:math:`E = 0.85`),
though at the top it ranks the OMARS design marginally above the Box-Behnken (:math:`2.64` versus
:math:`2.54`). For *prediction*, the average and maximum prediction variance are the working analogues of
:math:`I`- and :math:`G`-optimality. A model-discrimination criterion such as :math:`T`-optimality
has no place here: it is defined only against a second, rival model, measuring the lack of fit of
one against the other, so once a single model is settled there is no rival curve to be far from.

Two design-specific cautions sit alongside this. The composite design here is **face-centred**
(axial runs at
:math:`\pm 1`) so that it stays on the same :math:`[-1, 1]` region as the others; a rotatable CCD
would place those runs at :math:`\pm 2`, scoring much better only by quietly spending experiments
on a region twice as wide, which is not a fair comparison and explains the face-centred design's
weaker curvature precision (its :math:`|r| = 0.75` and VIF of :math:`3.20`). And the families
overlap: a composite design built on a resolution-V fraction is itself a strong OMARS design, while
a definitive screening design is a special case within the OMARS family, so think of these as a
spectrum.

Two views of prediction variance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two views of prediction variance are worth seeing side by side, because the scaling by run
count is exactly what leaves out the cost of running too few experiments.

Reusing the four designs and the ``fds`` helper, the two panels are the same curves
on the two scales:

.. code-block:: python

	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	# Reuses the designs dict and the model formula from the power block above; numpy, pandas
	# and evaluate_design were imported there. The fds helper integrates the prediction
	# variance over the region and returns the FDS curve (scaled and unscaled).
	def fds(design, model, *, n_samples, seed=1):
	    cols = [chr(ord("A") + i) for i in range(np.shape(design)[1])]
	    df = pd.DataFrame(np.asarray(design, float), columns=cols)
	    return evaluate_design(df, model=model, metric="fds", n_samples=n_samples,
	                           random_seed=seed, fds_resolution=200)["fds"]

	fig = make_subplots(rows=1, cols=2,
	                    subplot_titles=("Scaled (per run)", "Unscaled (sigma^2 units)"))
	for label, d in designs.items():
	    result = fds(d, model, n_samples=120_000)
	    # result["average_prediction_variance"] and ["max_prediction_variance"] are
	    # the average and maximum prediction-variance rows in the table above.
	    curve = result["curve"]
	    fig.add_trace(go.Scatter(x=curve["fraction"],
	                             y=curve["scaled_prediction_variance"], name=label),
	                  row=1, col=1)
	    fig.add_trace(go.Scatter(x=curve["fraction"],
	                             y=curve["prediction_variance"], name=label,
	                             showlegend=False), row=1, col=2)
	fig.update_yaxes(title_text="Scaled prediction variance", row=1, col=1)
	fig.update_yaxes(title_text="Prediction variance / sigma^2", row=1, col=2)
	fig.show()

.. figure:: ../figures/doe/fds-plot-six-designs.png
    :align: center
    :width: 750px
    :alt: fds-plot-six-designs.py

    FDS curves for the four response-surface designs, scaled (left) and unscaled (right). Scaling
    by the run count lowers the small DSD's curve; in real :math:`\sigma^2` units the DSD curve is
    the highest and the larger Box-Behnken design's is the lowest.

Within either panel the rule from before still holds: a low and flat curve is what you want, and the
right tail (anchored at the cube vertices, where the maximum prediction variance usually lives) shows
the worst case. The two panels differ only in how they put the designs on a common footing. The left
panel is scaled, normalized by the number of runs, so it compares the designs per experiment; on
that footing the thirteen-run DSD curve sits among the rest rather than far above them, and the
lowest right-tail value, the scaled maximum :math:`G` reported in the table, belongs to the OMARS
design at :math:`12.7`, with the DSD just behind at :math:`13.6`. The right panel is
unscaled, in real
:math:`\sigma^2` units, so it compares the variance actually obtained at the bench; there the DSD
curve is the highest and the forty-six-run Box-Behnken the lowest. The two views answer different
questions, and they diverge because adding runs lowers the variance you obtain while leaving the
per-run figure roughly fixed.

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
        the FDS plot and I-optimality (the average prediction variance over the region), then
        quadratic estimability, then how the design
        behaves when projected onto the subset of factors that turn out to be active. Favour a
        design whose FDS curve is low and flat.

Two rules of thumb close the loop. First, use **D for estimation and I for prediction**;
they frequently disagree, so choose by what you will actually do with the model. Second,
**compare D-efficiency only between designs of the same number of runs**: across
different run counts it favours the smaller design, so judge larger-versus-smaller on
the quantities that carry real units: average coefficient variance, prediction variance, power,
and the number of residual degrees of freedom.

Read the whole comparison as an illustration of the process, not as a ranking of the design
families. The table orders these particular designs on one model and one region; it is not a claim
that a family is best. That is clearest for the OMARS row: the catalogue holds many OMARS designs
for five factors, of different run sizes and aliasing trade-offs, and the twenty-five-run design
here is just the one the generator's A-optimality search returns, so its numbers describe that
member rather than OMARS designs as a class. Change the member, the model, or the region and
the rows shift. What carries from one study
to the next is the method, building the information matrix and reading precision, separability,
bias, and power from it.

**Readings**

* Box, Hunter and Hunter, *Statistics for Experimenters*, 2nd edition, for the factorial and
  response-surface groundwork.
* Myers, Montgomery and Anderson-Cook, *Response Surface Methodology*, for prediction variance,
  the scaled prediction variance, and FDS plots.
* Anderson-Cook, Borror and Montgomery, "Response surface design evaluation and comparison",
  *Journal of Statistical Planning and Inference*, **139**, 629--641, 2009
  (`doi:10.1016/j.jspi.2008.04.004 <https://doi.org/10.1016/j.jspi.2008.04.004>`__), and its
  published discussion, for the fraction-of-design-space comparison and the case for judging
  designs on prediction variance.
* Goos and Núñez Ares, "Response to Letter to the Editor", *Technometrics*, **67**, 189--191, 2025
  (`doi:10.1080/00401706.2024.2379849 <https://doi.org/10.1080/00401706.2024.2379849>`__), on why
  absolute efficiencies and scaled prediction variance mislead when designs differ in run size, and
  why power and unscaled prediction variance are the comparisons that hold up.
* Goos and Jones, *Optimal Design of Experiments: A Case Study Approach*, for the
  information-matrix view of the optimality criteria.
* Jones and Nachtsheim, "A Class of Three-Level Designs for Definitive Screening in the Presence of
  Second-Order Effects", *Journal of Quality Technology*, **43**, 1--15, 2011
  (`doi:10.1080/00224065.2011.11917841 <https://doi.org/10.1080/00224065.2011.11917841>`__), for the
  effect-sparsity and projection rationale behind definitive screening designs.
* Núñez Ares and Goos, "Enumeration and Multicriteria Selection of Orthogonal Minimally Aliased
  Response Surface Designs", *Technometrics*, **62**, 21--36, 2020
  (`doi:10.1080/00401706.2018.1549103 <https://doi.org/10.1080/00401706.2018.1549103>`__), and the
  review by Goos, "OMARS designs for factor screening and response surface experimentation in one
  step", *WIREs Computational Statistics*, **17**, e70018, 2025
  (`doi:10.1002/wics.70018 <https://doi.org/10.1002/wics.70018>`__), for the OMARS family used in
  the comparison above.
