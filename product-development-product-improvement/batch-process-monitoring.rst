.. _APPS_batch_monitoring:

Batch process monitoring and improvement
=========================================

.. index::
	single: batch process monitoring
	pair: batch processes; applications

Batch processes make a product in a finite run: charge the raw materials, execute a recipe over
hours or days, and discharge the product. Fermentation, polymerization, crystallization, spray
coating and pharmaceutical granulation are all run this way. The quality that matters is usually
measured once, at the end of the batch, and by then the batch is finished: whatever happened along
the way is already in the product.

That end-of-batch structure is why the data from a batch process form the three layers introduced
in the :ref:`section on extracting value from data <LVM_extracting_value_from_data>`:

- |Z|: measurements known *before* the batch starts, one row per batch: raw material properties,
  charge amounts, the age of the catalyst, supplier certificates of analysis.
- |X|: the trajectories recorded *during* the batch: temperatures, pressures, flows, pH, gas
  analysers, sampled at regular intervals. One batch contributes a whole time history, not a row.
- |Y|: the final quality, one row per batch, measured after discharge.

This section works through what those layers support, in the order a plant usually needs them:
first seeing that batches do not repeat even when the recipe does, then predicting the outcome of
a batch *while it is still running*, and finally adjusting the remainder of the recipe when that
prediction falls short. The last step is called a **mid-course correction**. Everything is
demonstrated with runnable code, and every claimed improvement is *executed*: the adjusted batch
is actually run (on a simulator whose disturbances repeat exactly), not just predicted to improve.
The distinction matters more than it may seem, and we return to it.

The golden batch
~~~~~~~~~~~~~~~~~~

.. index::
	single: golden batch

Most batch automation systems can store the recipe and setpoint schedules of a particularly good
batch, and replay them for every future batch. The stored run is often called the **golden
batch**, and replaying it is an appealing policy: the good outcome happened once, so running the
identical schedule again looks like the way to get it again. Alarm limits are often derived the
same way, as a band around the golden batch's trajectories.

The difficulty is what replaying can and cannot hold constant. A setpoint schedule fixes what the
*controllers aim for*; it does not fix the raw material lot, the seed culture, the fouling state
of the equipment, or the dozens of small disturbances that arrive while the batch runs. The golden
batch's outcome was produced jointly by its schedule *and* by the conditions it happened to enjoy.
Replaying reproduces only the schedule.

How closely does a plant actually repeat its recipe? The book's software package,
`process_improve <https://github.com/kgdunn/process-improve>`_, bundles the trajectory data of 57
batches from an industrial nylon polymerization autoclave, a dataset used throughout the batch
monitoring literature. All the code on this page runs top to bottom as one script; this first
block loads that dataset and measures the spread of each recorded variable across the batches:

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	from process_improve.batch import BatchPLS, load_nylon, resample_to_reference
	from process_improve.batch.control import (
	    MidCourseCorrector,
	    evaluate_control_policies,
	    midcourse_correction,
	)
	from process_improve.simulation import (
	    BioreactorSimulator,
	    sample_initial_conditions,
	    variance_decomposition,
	)

	nylon = load_nylon()
	tags = list(next(iter(nylon.values())).columns)
	aligned = resample_to_reference(nylon, columns_to_align=tags, reference_batch=1)

	for tag in ("Tag06", "Tag10"):
	    matrix = np.array([b[tag].to_numpy() for b in aligned.values()])
	    spread = 100 * np.mean(matrix.std(axis=0, ddof=1)) / np.mean(np.abs(matrix.mean(axis=0)))
	    print(f"{tag}: average relative spread across the 57 batches = {spread:.1f}%")

	fig = make_subplots(rows=1, cols=2, subplot_titles=("Tag06: 0.5% spread", "Tag10: 7.4% spread"))
	for col, tag in ((1, "Tag06"), (2, "Tag10")):
	    for batch in aligned.values():
	        fig.add_trace(go.Scatter(y=batch[tag], mode="lines", opacity=0.25,
	                                 line_color="#0072B2" if col == 1 else "#D55E00",
	                                 showlegend=False), row=1, col=col)
	fig.update_layout(xaxis_title="Time [sample]", xaxis2_title="Time [sample]")
	fig.show()

.. figure:: ../figures/batch/golden-batch-nylon-spread.png
	:source: batch/golden-batch-figures.py
	:alt: All 57 nylon batches overlaid for two recorded variables; Tag06 repeats within 0.5% while Tag10 spreads 7.4%.
	:width: 900px
	:scale: 80
	:align: center

The two variables answer the question. ``Tag06``, one of the tightly regulated variables, repeats
to an average relative spread of 0.5% across all 57 batches: the recipe really is being replayed,
and the control layer really is delivering it. ``Tag10`` spreads 7.4%, fourteen times wider, in
the same 57 batches under the same recipe. The variables the controllers hold, hold; the variables
that *respond* to the batch's chemistry and biology spread. The recipe repeats. The batch does
not.

Why replaying does not repeat the outcome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The nylon data show the spread but cannot say what caused it, and no historical dataset can: for
any recorded batch we observe one outcome under one set of disturbances, never the same batch
again under different handling. To take the argument further we use a simulator, and this is a
deliberate choice rather than a retreat from real data. A simulator can run the *same batch
twice*: identical raw material properties and identical disturbance history, once with one
schedule and once with another. Differences in the outcome are then attributable to the schedule
alone. That counterfactual is exactly what a claimed improvement needs, and it is the one thing
plant data cannot provide.

The simulator here (``process_improve.simulation.BioreactorSimulator``) is a ten-day
fed-batch bioreactor producing a protein, sampled twice a day. The recipe is a pH schedule and a
temperature schedule: warm growth days to build biomass, then a downshift to a cooler
production hold, the biphasic profile used industrially in mammalian cell culture. The recorded
tags are pH, temperature, dissolved oxygen, offgas carbon dioxide and volume; the quality |Y| is
the final product concentration (titer, in g/L). Three disturbance channels can be scaled
independently: an 11-variable measured pre-batch block |Z| (nutrient lots, seed-culture
viability measures, trace metals, moisture), an unmeasured disturbance that develops while the
batch runs, and control-loop plus measurement noise at realistic instrument scales. Its full
equations and the measurements behind its calibration are documented with the package; for this
page it plays the role of the plant.

Replaying the nominal schedule for 40 batches, with every disturbance channel at its realistic
default:

.. code-block:: python

	simulator = BioreactorSimulator()

	campaign = simulator.simulate_campaign(40, policy="replay", random_state=0)
	titer = campaign.quality["titer"]
	print(f"titer: mean {titer.mean():.2f} g/L, spread {titer.min():.2f} to {titer.max():.2f}, "
	      f"CV {100 * titer.std(ddof=1) / titer.mean():.1f}%")

	fig = make_subplots(rows=1, cols=2, column_widths=[0.65, 0.35],
	                    subplot_titles=("Recorded temperature", "Final titer"))
	for batch in campaign.batches.values():
	    fig.add_trace(go.Scatter(x=batch.index, y=batch["temperature"], mode="lines",
	                             opacity=0.25, line_color="#0072B2", showlegend=False), row=1, col=1)
	fig.add_trace(go.Histogram(x=titer, nbinsx=12, marker_color="#56B4E9", showlegend=False),
	              row=1, col=2)
	fig.update_layout(xaxis_title="Time [day]", xaxis2_title="Final titer [g/L]")
	fig.show()

.. figure:: ../figures/batch/golden-batch-replay-spread.png
	:source: batch/golden-batch-figures.py
	:alt: Forty simulated batches under the identical requested schedule; the recorded temperatures form a narrow band while the final titers spread with a 9.6 percent coefficient of variation.
	:width: 900px
	:scale: 80
	:align: center

Every batch requested the identical schedule, and the recorded temperatures confirm the control
layer delivered it to within a fraction of a degree. The final titers still range from 6.29 to
9.19 g/L, a 9.6% coefficient of variation, around a disturbance-free reference of 8.01 g/L (the
titer this schedule produces when every disturbance channel is switched off). This is the nylon
picture again, but now with the cause available for dissection.

Because the simulator's channels can be switched off individually, the titer variance of a replay
campaign can be split into its sources. The decomposition below runs four campaigns (all channels;
each channel alone; all channels with one held out) and reports each source's share, with the
interaction of the sources through the nonlinear process reported explicitly rather than forced
into the other buckets:

.. code-block:: python

	print(variance_decomposition(simulator, n_batches=200, random_state=0).round(3))

.. figure:: ../figures/batch/golden-batch-variance-decomposition.png
	:source: batch/golden-batch-figures.py
	:alt: Shares of the replay-campaign titer variance: measured initial conditions, within-batch disturbance, control and measurement noise, and the interaction of the sources.
	:width: 900px
	:scale: 80
	:align: center

The reading that matters for the rest of this page: a substantial share of the outcome variance
traces to the *measured initial conditions*, information available before the batch starts; a
comparably substantial share traces to the *within-batch disturbance*, which no pre-batch
measurement can reveal; and the noise floor is negligible. The first share is addressable by
adapting the schedule before the batch (feedforward). The second is addressable only by watching
the batch and reacting while it runs. Those are the two interventions this page builds, and the
decomposition says neither one alone can reach everything.

One more look at the pre-batch block |Z| before modelling it. The eleven measured variables are
correlated (they reflect a few underlying causes: how viable the seed culture is, how rich the
medium lot is, how much of a growth inhibitor came in with a supplier stream), so a two-component
PCA summarises them well:

.. code-block:: python

	from process_improve.multivariate import MCUVScaler, PCA

	drawn = sample_initial_conditions(200, random_state=0)
	z_model = PCA(n_components=2).fit(MCUVScaler().fit_transform(drawn.z))
	scores = z_model.scores_

	fig = go.Figure()
	for label, colour in (("A", "#0072B2"), ("B", "#E69F00"), ("C", "#D55E00")):
	    mask = np.asarray(drawn.classes) == label
	    fig.add_trace(go.Scatter(x=scores.iloc[mask, 0], y=scores.iloc[mask, 1],
	                             mode="markers", name=f"class {label}", marker_color=colour))
	fig.update_layout(xaxis_title="t1", yaxis_title="t2")
	fig.show()

.. figure:: ../figures/batch/golden-batch-z-scores.png
	:source: batch/golden-batch-figures.py
	:alt: PCA score plot of the upstream Z block; the three feed classes occupy overlapping ranges along the first component.
	:width: 750px
	:scale: 80
	:align: center

The batches come from three feed classes (in this plant's story: three supplier or campaign
combinations, labelled A, B and C). The classes do not form separated clusters; they occupy
overlapping ranges along the first score direction, which orders the batches from favourable to
unfavourable incoming material. Assigning a fresh batch to the nearest class centroid in the
standardised |Z| variables recovers its label about 80% of the time, and when it misses, it
assigns the neighbouring range. We will use these class ranges shortly, as local modelling
regions along that axis.

Predicting a batch while it runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: batch processes; monitoring
	single: trimmed score regression

The tool for relating the three layers is the batchwise-unfolded latent variable model of Nomikos
and MacGregor, with the pre-batch block joined onto the unfolded trajectories as Kourti, Nomikos
and MacGregor set out (see the :ref:`references below <APPS_batch_monitoring_further_reading>`):
each batch becomes *one row* containing its |Z| values followed by every trajectory sample of
every tag, and that long row is regressed onto the final quality with PLS. Centring each column
removes the average trajectory, so the model works with each batch's *deviations* from typical behaviour
at each point in time, and the loadings are free to weight a deviation at hour 10 differently
from the same deviation at hour 100. This is how a linear model captures a batch's time-varying
behaviour.

Two practical requirements come with this structure. The batches must be *aligned* (the same
number of samples per batch, with corresponding samples meaning the same process phase); the
simulator's batches are aligned by construction, and the package provides resampling and dynamic
time warping for plant data that is not. And the training campaign must contain *deliberate
schedule variation*. A model built only on batches that all ran the same schedule can predict,
but it has no information about what a schedule *change* would do; the data requirement for
control is history in which the manipulated schedules actually moved, in shapes like the ones the
controller will later use. Flores-Cerrillo and MacGregor state this requirement plainly in the
paper this section's control method is built on, and the campaign below follows it: 200 historical
batches whose pH and temperature schedules carry deliberate smooth perturbations (drawn at five
knots and interpolated), of a size a plant's operating history plausibly spans.

.. code-block:: python

	rng = np.random.default_rng(0)                    # one master seed drives every number on this page
	train_seed = int(rng.integers(2**31))
	test_seed = int(rng.integers(2**31))
	batch_seeds = rng.integers(2**31, size=40)        # per-batch execution seeds, reused later

	train = simulator.simulate_campaign(200, policy="historical", mv_variation=2.5,
	                                    random_state=train_seed)
	z_train = train.initial_conditions
	labels = np.asarray(list(train.classes))
	z_mean, z_sd = z_train.mean(), z_train.std(ddof=1)

	models = {}
	for group in ("A", "B", "C"):
	    ids = [i for i, c in zip(train.batches, labels) if c == group]
	    models[group] = BatchPLS(n_components=4).fit(
	        {i: train.batches[i] for i in ids},
	        train.quality.loc[ids],
	        initial_conditions=z_train.loc[ids],
	    )
	    print(f"class {group}: {len(ids)} batches, R2 = {models[group].r2_cumulative_.iloc[-1]:.2f}")

One model per feed class, rather than one global model, and the choice needs its reason stated
because it was learned the expensive way. A single global model fitted on all 200 batches
predicts final titer acceptably. Used for *control*, however, it failed when executed: its
corrections moved some batches in a direction that lowered their realised titer. The cause is an
interaction the variance decomposition already hinted at: the effect of a schedule change depends
on the feed class. Holding the reactor warm in mid-batch rescues a slow-growing batch from a poor
feed lot, and wastes productive time for a fast-growing one. A single linear model has one gain
direction to offer every batch, so it averages the two cases and misdirects both. Fitting the
model within a class range makes the gain locally right. The three fits above reach
:math:`R^2` values of 0.81, 0.90 and 0.94 on their own classes.

With a fitted model, predicting a *running* batch is a missing data problem. At decision time,
|Z| and the trajectory samples up to now are known, and the row's two kinds of future column are
handled differently. The future *measured* trajectories are genuinely unknown, and are estimated.
The future *setpoint* columns are not unknown: they are set to whichever schedule is being
considered, which for the question "what happens if nothing is changed?" is the nominal remaining
schedule. Flores-Cerrillo and MacGregor set the prediction up this way, and the implementation
here follows them.

The model's correlation structure spans the whole batch, so the scores (and from them, the
predicted final quality) follow from the filled row. García-Muñoz, Kourti and MacGregor compared
the available estimators on exactly this problem and found two of them best, giving almost
identical predictions: conditional mean replacement, and trimmed score regression. This package
implements the second: take the *trimmed scores* (the score formula applied with missing entries
simply left out), then correct them with a regression, fitted on the training data, from trimmed
scores to true scores. It is available as ``PLS.project``, and everything below uses it through
higher level functions.

The figure shows the resulting picture for one batch from the poorest feed class: the predicted
final titer at every possible decision point, with its 95% prediction interval, as the batch
runs.

.. figure:: ../figures/batch/mcc-monitoring-funnel.png
	:source: batch/midcourse-correction-figures.py
	:alt: Predicted final titer of one poor batch at every decision point with its prediction interval; the prediction sits near 3.3 grams per litre from the first day, far below the 8 grams per litre target.
	:width: 900px
	:scale: 80
	:align: center

This batch is headed for roughly 3.3 g/L against a target of 8 g/L, and its own data say so from
the first day: the poor feed lot is visible in |Z| immediately, and the slow growth it causes
shows in the gas trajectories soon after. The batch announces its shortfall while most of the
batch is still ahead. The question this page has been building toward: knowing this on day 4,
what should the remaining six days of the schedule be?

Correcting mid-course
~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: mid-course correction
	pair: batch processes; control

The idea of a mid-course correction predates its latent variable form: Yabuki and MacGregor
formulated it for semi-batch reactors in 1997, predicting the final properties from on-line
measurements plus a few off-line samples, and correcting only when that prediction fell outside a
defined no-control region. At a small number of *decision points* during the batch, predict the
final quality from everything measured so far. If the prediction is acceptable, do nothing. If it
falls short by more than the prediction's own uncertainty, compute an adjustment to the remaining
manipulated variables and implement it. Two gates carry most of the practical value, and both are
easy to omit:

- **A no-correction dead band**, which is Yabuki and MacGregor's no-control region. Every
  prediction carries uncertainty, and a correction computed from noise adds variance instead of
  removing it. Correct only when the predicted shortfall is large relative to the prediction
  interval; leave well-predicted batches alone.
- **A model validity check**, which arrives with the latent variable form of the method.
  Flores-Cerrillo and MacGregor compute the SPE of the batch-so-far at each decision point,
  against limits of the kind Nomikos and MacGregor established, before any correction is
  computed. The prediction is only trustworthy for a batch that resembles the data the model was
  built from. If the batch-so-far has an unusually large SPE (its measurements do not fit the
  model's correlation structure; see :ref:`interpreting the SPE
  <LVM-interpreting-SPE-residuals>`), a correction computed from that model is a guess, and the
  safer action is to not correct.

Flores-Cerrillo and MacGregor compute the correction in the *score* space. Their decision
variable is :math:`\Delta \mathbf{t}`, an adjustment to the batch's latent variable scores,
chosen by a quadratic program with three terms: how far the predicted quality lands from its set
point, a movement suppression term on :math:`\Delta \mathbf{t}`, and a soft penalty on
Hotelling's :math:`T^2` that keeps the answer within the region past operation covered. The
remaining setpoint trajectories are then recovered by inverting the PLS model, and that inversion
is what makes them smooth and consistent with how the plant has operated historically.

The implementation on this page makes a different choice: it optimises the future setpoint
columns directly, and keeps the schedule plausible with stated constraints rather than through
model inversion. The two routes trade off differently. Inversion inherits the historical
correlation structure automatically, but has no way to express an actuator limit; optimising the
columns states the engineering limits exactly, but has to add the terms that hold the answer
inside the model's region. Written in the setpoint columns, every term has a plain language
reading:

- **Hit the target**: the predicted final quality, as a function of the candidate future
  schedule, should come as close to the target as the model believes possible. This is
  Flores-Cerrillo and MacGregor's set-point term.
- **Move as little as necessary**: deviations from the nominal remaining schedule are penalised,
  so of the many schedules the model scores equally, the least disruptive is chosen. This is
  their movement suppression term.
- **Stay where the model has data**: the candidate row's Hotelling's :math:`T^2` (:ref:`its
  distance from the centre of the training data within the model plane <LVM-Hotellings-T2>`) and
  its SPE (its distance off the plane) are penalised, and can be capped. The :math:`T^2` penalty
  is theirs. The SPE term is added here, because a candidate written directly in the setpoint
  columns can leave the model plane in a way an adjustment to the scores cannot. The two limits
  do different jobs: the :math:`T^2` limit keeps the correction inside the region the history
  explored, and the SPE limit keeps the candidate row's *combination* of values consistent with
  how the variables move together.
- **Respect the actuators**: bounds on each setpoint, and rate-of-change limits between
  consecutive samples, including the seam between the last implemented sample and the first
  corrected one. The corrected schedule is also parameterised by a few knots (a small number of
  anchor points, with the schedule interpolated between them), so it stays as smooth as the
  schedules the plant actually runs. These constraints are added here; Flores-Cerrillo and
  MacGregor obtain smoothness from the model inversion, and bound the score adjustment rather
  than the setpoints.

Because the score estimate of a partially known row is a *linear* function of the candidate
future columns (the missing data estimator, for a fixed pattern of known and unknown columns, is
a fixed matrix), every term above is a quadratic or linear function of the decision variables.
With the two validity terms as penalties, the problem is a small convex quadratic program: a few
dozen unknowns, solved in milliseconds, with a unique answer. Turning the :math:`T^2` and SPE
limits into hard caps makes them quadratic constraints, so the problem becomes a quadratically
constrained one; it is solved here by returning the caps to the objective and raising their
weights until the caps are respected. Either way, no plant model in differential equation form is
required, only the historical data the plant already has.

Here is the whole workflow on the batch from the funnel figure. The corrector below carries the
target (8 g/L, treated as a floor: batches predicted at or above it are never touched), the dead
band (2.5 prediction-interval half-widths), the validity gate, the limits, the actuator bounds
(tightened inward by about two control-error standard deviations, so an optimised setpoint does
not sit on a rail the control loop then clips), and the knot parameterisation:

.. code-block:: python

	nominal = simulator.nominal_trajectory().reset_index(drop=True)
	config = simulator.config
	correctors = {}
	for group in ("A", "B", "C"):
	    correctors[group] = MidCourseCorrector(
	        models[group],
	        nominal,
	        mv_tags=["pH", "temperature"],
	        mode="target",
	        y_target=8.0,
	        target_side="below",              # the target is a floor, not a setpoint
	        dead_band=2.5,                    # correct only clear, significant shortfalls
	        weights={"target": 1.0, "movement": 0.1},
	        bounds={"temperature": (config.temp_bounds[0] + 0.3, config.temp_bounds[1] - 0.3),
	                "pH": (config.ph_bounds[0] + 0.04, config.ph_bounds[1] - 0.04)},
	        rate_limits={"temperature": 3.0, "pH": 0.5},
	        spe_cap="limit", t2_cap="limit",  # per-decision-point limits from the training batches
	        n_knots=4,
	    )

	def nearest_class(z_row):
	    z_std = (z_row - z_mean) / z_sd
	    centroids = {g: ((z_train.loc[labels == g] - z_mean) / z_sd).mean() for g in "ABC"}
	    return min(centroids, key=lambda g: float(((z_std - centroids[g]) ** 2).sum()))

	test = simulator.simulate_campaign(40, policy="replay", random_state=test_seed)
	z_test = test.initial_conditions

	batch_id = 28                                          # the batch in the funnel figure
	seed = int(batch_seeds[list(z_test.index).index(batch_id)])
	z_row = z_test.loc[batch_id]
	base = simulator.simulate_batch(z_row, random_state=seed)

	outcome = correctors[nearest_class(z_row)].correct(
	    base.tags.iloc[:8].reset_index(drop=True),          # the first 8 samples: days 0 to 4
	    initial_conditions=z_row,
	    k=8,
	)
	corrected = outcome.schedule.copy()
	corrected.index = simulator.nominal_trajectory().index
	redo = simulator.simulate_batch(z_row, corrected, random_state=seed)   # identical disturbances
	print(f"replay {base.titer:.2f} g/L -> corrected {redo.titer:.2f} g/L "
	      f"(model predicted {float(outcome.y_hat.iloc[0]):.2f})")

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=corrected.index, y=nominal["temperature"], mode="lines",
	                         line_shape="hv", name="nominal", line_color="#666666"))
	fig.add_trace(go.Scatter(x=corrected.index, y=corrected["temperature"], mode="lines",
	                         line_shape="hv", name="corrected at day 4", line_color="#D55E00"))
	fig.update_layout(xaxis_title="Time [day]", yaxis_title="Temperature setpoint [°C]")
	fig.show()

.. figure:: ../figures/batch/mcc-correction-at-k.png
	:source: batch/midcourse-correction-figures.py
	:alt: Nominal and corrected temperature and pH schedules for the poor batch; the corrected schedule delays the downshift, holding the reactor warmer through day seven, and the executed titer rises from 3.66 to 5.79 grams per litre.
	:width: 900px
	:scale: 80
	:align: center

The nominal schedule drops from the warm growth phase to the 29 °C production hold between days
3.5 and 5. The corrected schedule refuses to complete that drop on time: it holds near 34.7 °C at
day 4 and descends to the production hold only around day 7.5, with a small transient pH
adjustment. The physical reading is direct. This batch's poor feed lot made it grow slowly, so at
day 4 it has not yet built the biomass the production phase needs; cooling it on the nominal
timetable would freeze it at a low cell density. The correction buys the batch more growing time.
No such rule was programmed anywhere: the behaviour emerges from a regression on historical
batches whose schedules were deliberately varied.

Executed with the identical disturbance history, the batch finishes at 5.79 g/L instead of
3.66 g/L, a 58% improvement on this single batch. The model predicted 5.04 g/L for the
corrected schedule: a latent variable prediction regresses toward the mean, so it *understated*
the gain its own correction delivered. The distinction between a predicted and an executed gain
is worth keeping in view. Simulation studies can execute their corrections, and do:
Flores-Cerrillo and MacGregor obtained the final qualities in their nylon case study by rerunning
the non-linear simulation model with the trajectories the controller had computed. On an
operating plant that step is not available, so results from industrial case studies are reported
as model predictions. On this page the simulator makes execution cheap, so every gain from here
on is an executed one.

Does it work on the whole campaign?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One rescued batch is an anecdote. The test that matters runs many fresh batches through the full
policy (predict at the decision point; gate; correct when warranted; execute) and compares
against the alternatives on the same batches with the same disturbances. The package wraps that
comparison, including two reference policies that bracket what is achievable:

.. code-block:: python

	result = evaluate_control_policies(simulator, y_target=8.0, random_state=0)   # about 7 minutes
	print(result.summary.round(3))
	print(f"{result.n_corrected} corrected, {result.n_harmed} harmed")

============================  =======  ======  ======  ======
Policy                        Mean     Sd      Min     Max
============================  =======  ======  ======  ======
Replay (do nothing)           7.507    1.198   3.655   8.925
Mid-course correction         7.709    0.781   5.717   8.925
Oracle from the same day      7.828    0.631   6.108   8.925
Adapted (feedforward)         7.824    1.013   4.573   9.309
============================  =======  ======  ======  ======

All four rows are executed titers over the same 40 fresh batches, in g/L. Reading them one at a
time:

- **Replay** is the golden batch policy: every batch runs the nominal schedule. Its spread is the
  cost of doing nothing.
- **Mid-course correction** corrected 4 of the 40 batches, all from the poorest feed class; the
  dead band left 35 alone and the SPE validity gate stopped one. Each corrected batch improved,
  by +1.53 to +2.67 g/L, and no batch was made worse. The campaign mean rises 0.20 g/L, and the
  standard deviation falls from 1.20 to 0.78 g/L, a 35% reduction. The policy works where the
  money is: the low tail. The lowest replay batch (3.66 g/L, the single-batch demonstration)
  rises to 5.79 g/L, and the lowest batch in the whole corrected campaign finishes at 5.72 g/L.
- **Oracle from the same day** answers "how much was achievable at that decision point at all?"
  For each corrected batch, the remaining schedule is optimised against the *simulator itself*
  (the true process), from the same day-4 state, with the same seed. No data-driven method can
  beat this row from the same starting point. The mid-course policy captured 63% of the oracle's
  mean improvement; the remainder is the price of steering with a regression restricted to the
  region its history explored, rather than with the true process equations.
- **Adapted (feedforward)** runs *every* batch on the true optimal schedule for its own measured
  |Z|, computed before the batch starts: perfect feedforward adaptation, again a ceiling rather
  than an implementable policy. It raises the mean and the best batches (its maximum, 9.31 g/L,
  is the table's highest), but its *minimum is worse than the corrected policy's*: 4.57 against
  5.72 g/L. A schedule fixed at time zero, however well chosen, cannot answer a disturbance that
  develops during the batch. The variance decomposition said the outcome variance has a
  before-batch share and a during-batch share; the adapted row addresses the first, the
  mid-course row the second, and neither substitutes for the other.

.. figure:: ../figures/batch/mcc-policy-comparison.png
	:source: batch/midcourse-correction-figures.py
	:alt: Left panel: the four corrected batches each jump by 1.5 to 2.7 grams per litre. Right panel: all forty batches under the four executed policies; correction removes the low tail.
	:width: 900px
	:scale: 80
	:align: center

Where to put the decision point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The comparison above used a single decision point at day 4 of 10. That choice matters, and
sweeping it (re-running the whole executed comparison with the decision point moved) shows a
window:

============  ===========  =================  =======================
Decision day  Corrected    Of which harmed    Mean executed gain
============  ===========  =================  =======================
2             21           8                  +0.32 g/L
3             8            3                  +0.82 g/L
4             4            0                  +2.02 g/L
5             6            0                  +0.67 g/L
6             7            7                  -0.05 g/L
7             7            7                  -0.28 g/L
============  ===========  =================  =======================

.. figure:: ../figures/batch/mcc-decision-point-window.png
	:source: batch/midcourse-correction-figures.py
	:alt: Mean executed gain of the corrected batches versus the decision day, rising to a peak at day four and turning negative from day six.
	:width: 900px
	:scale: 80
	:align: center

Both ends of the window fail for identifiable reasons. Correcting at day 2, the predictions are
still uncertain, so the dead band passes 21 batches, including ones that needed nothing, and the
model misdirects several (8 harmed). Correcting at day 6 or later, the predictions are at their
best, but the remaining schedule no longer has the leverage to act on them: the growth phase is
over, and small model errors are all that remains, so every correction does slight damage. On
this process the window is days 4 to 5: late enough that a struggling batch has revealed itself
in the gas trajectories, early enough that the growth phase can still be extended. The window's
location is a property of the process, not of the method; finding it needs either process
understanding or a sweep like this one.

How far should the model be trusted?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :math:`T^2` and SPE penalties and caps are the knobs that keep the optimiser inside the
region the historical data supports, and they are also the natural place to ask a sharper
question: how far *should* it be allowed to roam? Relaxing the :math:`T^2` penalty (with the hard
caps removed) and re-running the executed comparison at each setting measures the answer for this
process:

.. figure:: ../figures/batch/mcc-exploration-dial.png
	:source: batch/midcourse-correction-figures.py
	:alt: Predicted and executed mean titers of the corrected batches as the T-squared penalty relaxes; both rise as the optimiser is freed, and the executed line sits above the predicted line throughout.
	:width: 900px
	:scale: 80
	:align: center

On this process, at this decision point, freeing the optimiser helped monotonically: the poorest
class's true optimum lies well outside the historical operating envelope (the oracle's schedules
reach 5 °C above anything in the training campaigns), so every step of extra freedom bought a
real improvement, and the executed titer sat *above* the model's own prediction at every setting.
It would be wrong to conclude that the constraints are unnecessary. The same freedom, at the late
decision points of the previous table, is what turned corrections harmful: there the model's
apparent leverage was error, and the constraints are what would have contained it. The two
figures together are the fair statement: the validity limits trade reachable improvement against
protection from model error, the balance depends on where the process's true optimum sits
relative to the explored region, and the balance can be *measured*, on batches the model has
never seen, before the scheme is trusted in production.

Practical notes
~~~~~~~~~~~~~~~~~

A few points that decide whether this works outside a demonstration:

- **The history must contain deliberate schedule variation**, in shapes the controller will use.
  A first version of the simulator's historical campaign varied its schedules only by a constant
  offset plus a ramp; a model fitted on it could not identify the effect of a
  second-half-only move, and its corrections failed when executed. Smooth local perturbations
  (the knot basis used here) fixed exactly that. Flores-Cerrillo and MacGregor identified their
  nylon controller from 45 batches, 30 of which carried deliberate moves at the two decision points,
  and reported adequate control from as few as 15 batches (10 of them with moves);
  identification-quality data is a modest but real requirement.
- **Local models where the gain direction changes.** The per-class models here are the simplest
  form of local modelling; the same role is played in other applications by models per grade, per
  product, or locally weighted models. The symptom that demands them is specific: predictions
  look fine globally, but executed corrections help one group of batches and hurt another.
- **Models are identified on recorded trajectories but output setpoints.** The regression sees
  the control error as part of its input; the resulting attenuation is small at realistic noise
  levels, and the executed evaluation absorbs it, but it is one more reason predicted gains and
  realised gains differ.
- **What mid-course correction cannot do.** It cannot recover a batch the validity gate excludes
  (an out-of-family batch needs diagnosis, not optimisation); it cannot act on the share of
  variance that only materialises after the last decision point; and it cannot exceed the
  information in the historical data, which is what the gap to the oracle row measures. The
  :ref:`monitoring chart <LVM_monitoring>` and :ref:`troubleshooting <APPS_multivariate_monitoring>`
  tools remain the right response to the batches this page's method correctly refuses to touch.

The methods on this page are implemented in `process_improve
<https://github.com/kgdunn/process-improve>`_ (``BatchPLS``, ``PLS.project``,
``MidCourseCorrector`` and ``evaluate_control_policies``, with the simulator in
``process_improve.simulation``); the figure sources carry the exact seeds, so every number on
this page can be regenerated.

.. _APPS_batch_monitoring_further_reading:

Further reading
~~~~~~~~~~~~~~~~~

The methods used on this page, in their original sources:

* Yuichi Yabuki and John F. MacGregor, "Product quality control in semibatch reactors using
  midcourse correction policies", *Industrial and Engineering Chemistry Research*, **36**,
  1268-1275, 1997. `<https://doi.org/10.1021/ie960536m>`_ The no-correction dead band used here
  is their no-control region.
* Jesus Flores-Cerrillo and John F. MacGregor, "`Control of batch product quality by trajectory
  manipulation using latent variable models
  <https://literature.learnche.org/item/39/control-of-batch-product-quality-by-trajectory-manipulation-using-latent-variable-models>`_",
  *Journal of Process Control*, **14**, 539-553, 2004.
  `<https://doi.org/10.1016/j.jprocont.2003.09.008>`_ The source of the correction problem, the
  SPE validity gate and the identification requirement. Their optimisation is over the score
  adjustment, with the trajectories recovered by model inversion; this page optimises the
  setpoint columns directly, as described in the text.
* Francisco Arteaga and Alberto Ferrer, "Dealing with missing data in MSPC: several methods,
  different interpretations, some examples", *Journal of Chemometrics*, **16**, 408-418, 2002.
  `<https://doi.org/10.1002/cem.750>`_
* Salvador García-Muñoz, Theodora Kourti and John F. MacGregor, "`Model predictive monitoring for
  batch processes
  <https://literature.learnche.org/item/157/model-predictive-monitoring-for-batch-processes>`_",
  *Industrial and Engineering Chemistry Research*, **43**, 5929-5941, 2004.
  `<https://doi.org/10.1021/ie034020w>`_ The comparison of score estimators for a partially
  observed batch.

Foundational multiway PCA / PLS for batches:

* Paul Nomikos and John F. MacGregor, "`Monitoring batch processes using multiway principal component analysis <https://literature.learnche.org/item/30/monitoring-batch-processes-using-multiway-principal-component-analysis>`_", *AIChE Journal*, **40**, 1361-1375, 1994.
* Paul Nomikos and John F. MacGregor, "`Multi-way partial least squares in monitoring batch processes <https://literature.learnche.org/item/32/multi-way-partial-least-squares-in-monitoring-batch-processes>`_", *Chemometrics and Intelligent Laboratory Systems*, **30**, 97-108, 1995.
* Theodora Kourti, Paul Nomikos and John F. MacGregor, "`Analysis, monitoring and fault diagnosis of batch processes using multiblock and multiway PLS <https://literature.learnche.org/item/33/analysis-monitoring-and-fault-diagnosis-of-batch-processes-using-multiblock-and-multiway-pls>`_", *Journal of Process Control*, **5**, 277-284, 1995.
* Paul Nomikos and John F. MacGregor, "`Multivariate SPC charts for monitoring batch processes <https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_", *Technometrics*, **37**, 41-59, 1995.
* Paul Nomikos, "`Detection and diagnosis of abnormal batch operations based on multi-way principal component analysis <https://literature.learnche.org/item/64/detection-and-diagnosis-of-abnormal-batch-operations-based-on-multi-way-principal-component-analysis>`_", *ISA Transactions*, **35**, 259-266, 1996.
* Karlene A. Kosanovich, Kenneth S. Dahl and Michael J. Piovoso, "`Improved process understanding using multiway principal component analysis <https://literature.learnche.org/item/156/improved-process-understanding-using-multiway-principal-component-analysis>`_", *Industrial and Engineering Chemistry Research*, **35**, 138-146, 1996.
* Johan A. Westerhuis, Theodora Kourti and John F. MacGregor, "`Comparing alternative approaches for multivariate statistical analysis of batch process data <https://literature.learnche.org/item/162/comparing-alternative-approaches-for-multivariate-statistical-analysis-of-batch-process-data>`_", *Journal of Chemometrics*, **13**, 397-413, 1999.
* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_", *Comprehensive Chemometrics*, **2.10**, 163-197, 2009.

Control, optimization and product quality:

* Masoud Golshan, John F. MacGregor, Mark-John Bruwer and Prashant Mhaskar, "Latent Variable
  Model Predictive Control (LV-MPC) for trajectory tracking in batch processes", *Journal of
  Process Control*, **20**, 538-550, 2010. `<https://doi.org/10.1016/j.jprocont.2010.01.007>`_
* Carl Duchesne and John F. MacGregor, "`Multivariate analysis and optimization of process variable trajectories for batch processes <https://literature.learnche.org/item/92/multivariate-analysis-and-optimization-of-process-variable-trajectories-for-batch-processes>`_", *Chemometrics and Intelligent Laboratory Systems*, **51**, 125-137, 2000.
* Carl Duchesne, Theodora Kourti and John F. MacGregor, "`Multivariate SPC for startups and grade transitions <https://literature.learnche.org/item/91/multivariate-spc-for-startups-and-grade-transitions>`_", *AIChE Journal*, **48**, 2890-2901, 2002.
* Jesus Flores-Cerrillo and John F. MacGregor, "`Multivariate monitoring of batch processes using batch-to-batch information <https://literature.learnche.org/item/163/multivariate-monitoring-of-batch-processes-using-batch-to-batch-information>`_", *AIChE Journal*, **50**, 1219-1228, 2004.

Performance, alignment, and spectroscopy:

* Stephen P. Gurden, Johan A. Westerhuis and Age K. Smilde, "`Monitoring of batch processes using spectroscopy <https://literature.learnche.org/item/140/monitoring-of-batch-processes-using-spectroscopy>`_", *AIChE Journal*, **48**, 2283-2297, 2002.
* Henk-Jan Ramaker, Eric N. M. Van Sprang, Johan A. Westerhuis, Stephen P. Gurden, Age K. Smilde and Frank H. Van Der Meulen, "`Performance assessment and improvement of control charts for statistical batch process monitoring <https://literature.learnche.org/item/164/performance-assessment-and-improvement-of-control-charts-for-statistical-batch-process-monitoring>`_", *Statistica Neerlandica*, **60**, 339-360, 2006.
* José M. González-Martínez, Alberto J. Ferrer and Johan A. Westerhuis, "`Real-time synchronization of batch trajectories for on-line multivariate statistical process control using Dynamic Time Warping <https://literature.learnche.org/item/158/real-time-synchronization-of-batch-trajectories-for-on-line-multivariate-statistical-process-control-using-dynamic-time-warping>`_", *Chemometrics and Intelligent Laboratory Systems*, **105**, 195-206, 2011.

Theses (McMaster University):

* Paul Nomikos, `Statistical process control of batch processes <https://literature.learnche.org/item/154/statistical-process-control-of-batch-processes>`_, Ph.D thesis, 1995.
* Christiane M. Jaeckle, `Product and process improvement using latent variable methods <https://literature.learnche.org/item/167/product-and-process-improvement-using-latent-variable-methods>`_, Ph.D thesis, 1998.
* Jesus Flores-Cerrillo, `Quality control for batch processes using multivariate latent variable methods <https://literature.learnche.org/item/51/quality-control-for-batch-processes-using-multivariate-latent-variable-methods>`_, Ph.D thesis, 2003.
* Salvador García-Muñoz, `Batch process improvement using latent variable methods <https://literature.learnche.org/item/3/batch-process-improvement-using-latent-variable-methods>`_, Ph.D thesis, 2004.
* Cecilia Pereira Rodrigues, `Industrial batch data analysis using latent variable methods <https://literature.learnche.org/item/161/industrial-batch-data-analysis-using-latent-variable-methods>`_, Masters thesis, 2006.
