.. _APPS_batch_mcc:

Correcting a batch mid-course: predicting a running batch and adjusting its remaining schedule
================================================================================================

.. index::
	single: batch process control
	pair: batch processes; mid-course correction

The three case studies before this page fit their batch models after the batches ended, and the
:ref:`monitoring page <APPS_batch_monitoring>` sets out what each model is given and what it can
answer. This page uses the same models to act. It predicts the final quality of a batch *while it
is still running* and, when the prediction falls short, changes the remainder of the recipe. The
moment during the batch at which the prediction is made and the remainder may be adjusted is a
**decision point**, and the adjustment is a **mid-course correction**. The data are the three
layers of the :ref:`section on extracting value from data <LVM_extracting_value_from_data>`: the
pre-batch block |Z|, the trajectories |X| and the final quality |Y|.

The page runs in the order a plant needs: the evidence that batches do not repeat even when the
recipe does, the conditions under which acting during the batch can help, the prediction at a
decision point with its uncertainty, the correction, and the procedure for a plant. Every
improvement claimed is executed, not predicted: the adjusted batch is re-run on a simulator whose
disturbances repeat exactly, and :ref:`the campaign comparison <APPS_batch_mcc_campaign>` measures
how far the two differ.

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
batch's outcome was produced jointly by its schedule *and* by the conditions present during that
run. Replaying reproduces only the schedule.

How closely does a plant actually repeat its recipe? The book's software package,
`process_improve <https://github.com/kgdunn/process-improve>`_, bundles the trajectory data of 57
batches from an industrial nylon polymerization autoclave, a dataset used throughout the batch
monitoring literature. Real batches do not all run for the same length of time, so before their
trajectories can be compared sample by sample they are *aligned*: each batch is resampled onto a
common time base (here, batch 1's), so that sample *i* means the same point in the recipe for
every batch. :ref:`Alignment <APPS_batch_mcc_requirements>` is revisited when the
modelling starts. All the code on this page runs top to bottom as one script; this first block
loads that dataset, aligns it, and measures the spread of each of the ten recorded variables
across the batches, as the average over time of the batch-to-batch standard deviation, relative
to the variable's average level:

.. code-block:: python

	import dataclasses

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	from process_improve.batch import BatchPLS, load_nylon, resample_to_reference
	from process_improve.batch.control import MidCourseCorrector, evaluate_control_policies
	from process_improve.multivariate import MCUVScaler, PCA, PLS
	from process_improve.simulation import BioreactorConfig, BioreactorSimulator, variance_decomposition

	nylon = load_nylon()
	tags = list(next(iter(nylon.values())).columns)
	aligned = resample_to_reference(nylon, columns_to_align=tags, reference_batch=1)

	for tag in tags:
	    matrix = np.array([b[tag].to_numpy() for b in aligned.values()])
	    spread = 100 * np.mean(matrix.std(axis=0, ddof=1)) / np.mean(np.abs(matrix.mean(axis=0)))
	    print(f"{tag}: average relative spread across the 57 batches = {spread:.2f}%")

	fig = make_subplots(rows=1, cols=2, subplot_titles=("Tag06: 0.54% spread", "Tag10: 7.38% spread"))
	for col, tag in ((1, "Tag06"), (2, "Tag10")):
	    for batch in aligned.values():
	        fig.add_trace(go.Scatter(y=batch[tag], mode="lines", opacity=0.25,
	                                 line_color="#0072B2" if col == 1 else "#D55E00",
	                                 showlegend=False), row=1, col=col)
	fig.update_layout(xaxis_title="Time [sample]", xaxis2_title="Time [sample]")
	fig.show()

.. figure:: ../figures/batch/golden-batch-nylon-spread.png
	:source: batch/golden-batch-figures.py
	:alt: All 57 nylon batches overlaid for two recorded variables; Tag06 repeats within 0.54% while Tag10 spreads 7.38%.
	:width: 900px
	:scale: 80
	:align: center

The ten variables split into two groups. Five of them (``Tag02``, ``Tag03``, ``Tag04``,
``Tag06`` and ``Tag08``) repeat to an average relative spread between 0.54% and 0.68% across all
57 batches. These are presumably the variables the control layer holds: the recipe is being
replayed, and the control layer is delivering it. The other five spread between 1.9% and
7.4%. ``Tag10``, the widest, spreads 7.38%, about fourteen times more than ``Tag06``, in the same
57 batches under the same recipe. A variable that spreads this much under a fixed recipe is
responding to what happens inside the batch. The recipe repeats, but the batch does not.

The golden batch also serves as a monitoring reference: the average trajectory of a set of good
batches with a band around it, and a running batch flagged when it leaves the band. In the
multivariate form of :ref:`the monitoring page <APPS_batch_monitoring>` the band is the pair of
limits on the SPE and on Hotelling's :math:`T^2` of the batch so far, built from a reference set
of batches with acceptable operation and acceptable product, and :ref:`the second case study
<APPS_batch_case_sbr_online>` runs two faulty batches through it. That reference tells a plant
that a batch is unusual. It does not say how the batch will end, and it does not say what to
change; those are the two questions this page adds.

Why replaying does not repeat the outcome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The nylon data show the spread but cannot say what caused it, and no historical dataset can: each
recorded batch was run once, under one set of disturbances, and was never run again with
different handling. From here on we use a simulator, because it can run the *same batch twice*:
identical raw material properties and identical disturbance history, once under one schedule and
once under another. Any difference in the outcome then comes from the schedule alone. A measured
improvement requires that second run of the same batch, and recorded plant data do not contain
it.

The simulator here (``process_improve.simulation.BioreactorSimulator``) is a ten-day fed-batch
bioreactor producing a protein, sampled twice a day. The recipe is a pH schedule and a
temperature schedule: warm growth days at 36.8 °C to build biomass, then a ramp between days 3.5
and 4.5 down to a cooler production hold at 29.05 °C, the biphasic profile used industrially in
mammalian cell culture. The recorded tags are pH, temperature, dissolved oxygen, offgas carbon
dioxide and volume; the quality |Y| is the final product concentration (titer, in g/L). Three
disturbance channels can be scaled independently: an 11-variable measured pre-batch block |Z|
(nutrient lots, seed-culture viability measures, trace metals, moisture), an unmeasured
disturbance that develops while the batch runs, and control-loop plus measurement noise at
realistic instrument scales. Its full equations and the measurements behind its calibration are
documented with the package; for this page it plays the role of the plant.

.. _APPS_batch_mcc_replay:

Replaying the nominal schedule for 200 batches, with every disturbance channel at its realistic
default, and once more with every channel switched off, which gives the titer the schedule
produces when nothing disturbs it:

.. code-block:: python

	simulator = BioreactorSimulator()

	campaign = simulator.simulate_campaign(200, policy="replay", random_state=0)
	titer = campaign.quality["titer"]
	print(f"titer: mean {titer.mean():.2f} g/L, spread {titer.min():.2f} to {titer.max():.2f}, "
	      f"CV {100 * titer.std(ddof=1) / titer.mean():.1f}%")

	quiet = dataclasses.replace(BioreactorConfig(), ic_scale=0.0, within_batch_scale=0.0, noise_scale=0.0)
	reference = BioreactorSimulator(quiet).simulate_batch(None).titer
	print(f"disturbance-free reference: {reference:.2f} g/L")

	fig = make_subplots(rows=1, cols=2, column_widths=[0.65, 0.35],
	                    subplot_titles=("Recorded temperature", "Final titer"))
	for batch in campaign.batches.values():
	    fig.add_trace(go.Scatter(x=batch.index, y=batch["temperature"], mode="lines",
	                             opacity=0.12, line_color="#0072B2", showlegend=False), row=1, col=1)
	fig.add_trace(go.Histogram(x=titer, nbinsx=12, marker_color="#56B4E9", showlegend=False),
	              row=1, col=2)
	fig.update_layout(xaxis_title="Time [day]", xaxis2_title="Final titer [g/L]")
	fig.show()

.. figure:: ../figures/batch/golden-batch-replay-spread.png
	:source: batch/golden-batch-figures.py
	:alt: Two hundred simulated batches under the identical requested schedule; the recorded temperatures form a narrow band while the final titers spread with a 14.4 percent coefficient of variation.
	:width: 900px
	:scale: 80
	:align: center

Every batch requested the identical schedule, and the recorded temperatures confirm the control
layer delivered it to within a fraction of a degree. The final titers still average 7.57 g/L and
range from 4.24 to 9.83 g/L, a 14.4% coefficient of variation, around the disturbance-free
reference of 8.01 g/L. This is the nylon picture again, but now the causes can be separated and
measured.

Because the simulator's channels can be switched off individually, the titer variance of a replay
campaign can be split into its sources. The decomposition below runs four campaigns of the same
size and schedule (one with all channels active, then one for each channel on its own) and reports
each source's share. The three single-channel variances do not add up to the total, because the
process is nonlinear; the difference is reported as a fourth share rather than folded into the
others. The four campaigns are independent draws, so that fourth share also absorbs the sampling
error of four variance estimates, roughly a tenth of the total at 200 batches:

.. code-block:: python

	print(variance_decomposition(simulator, n_batches=200, random_state=0).round(3))

.. _APPS_batch_mcc_variance:

.. figure:: ../figures/batch/golden-batch-variance-decomposition.png
	:source: batch/golden-batch-figures.py
	:alt: Shares of the replay-campaign titer variance: measured initial conditions 31 percent, within-batch disturbance 27 percent, control and measurement noise 0 percent, and the interaction of the sources 41 percent.
	:width: 900px
	:scale: 80
	:align: center

The four shares are read one at a time.

- The *measured initial conditions* account for 31% of the titer variance. They are known before
  the batch starts, so a schedule chosen for each batch's own initial conditions, which is
  **feedforward adaptation**, can act on this share.
- The *within-batch disturbance* accounts for 27%. It cannot be seen before the batch starts.
  Only watching the batch and reacting while it runs can act on this share.
- *Control and measurement noise* contributes 0.03%. At realistic instrument scales the noise is
  not where the variance comes from.
- The *interaction of the sources* accounts for the remaining 41%, a share comparable to the initial
  conditions'. The two disturbances do not add: the titer a within-batch disturbance costs depends
  on the initial conditions it meets. In this process a batch from a poor feed lot grows slowly, and
  a disturbance that slows growth further costs it far more than the same disturbance costs a
  fast-growing batch. Acting on this share needs an intervention that knows which kind of batch it
  is acting on, a point that returns when the prediction models are built.

The two interventions built on this page are feedforward adaptation, which acts before the batch
starts, and mid-course correction, which acts while it runs. Each addresses a different share, so
neither covers the whole.

.. _APPS_batch_mcc_when:

When is mid-course correction the right tool?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: mid-course correction; when to apply

The sections so far diagnose the problem. Before any model is built, the question is whether
mid-course correction fits the process at hand. Four conditions decide it, and each one can be
checked on a plant's own records.

**1. The final quality varies more than the recipe.** Compare the batch-to-batch spread of the
regulated variables with the spread of the responding variables and of the final quality, over
batches that ran the same recipe, as was done for the nylon batches. Two numbers make this
concrete on a plant: the fraction of batches whose final quality falls short of its floor by more
than the assay's repeatability, and the product lost to those shortfalls in a year. The spread of
a regulated variable is judged against its alarm band or operating range rather than against its
mean, since a relative spread depends on where the unit's zero sits. If the final quality repeats
as closely as the setpoints do, there is nothing for a correction to recover.

**2. A useful part of that variation is not visible before the batch starts.** The decomposition
separated the shares on the simulator by switching disturbance channels off, which a plant cannot
do. A plant can run the regression that stands in for it: fit the final quality on the pre-batch
block |Z| alone, over batches that ran one recipe, and read the fit :math:`R^2` and its
cross-validated counterpart :math:`Q^2` (the fraction of the variance predicted for batches the
model was not fitted on; see :ref:`the cross-validation notes <LVM_q2_across_packages>`). The
share |Z| explains is the share a feedforward policy can act on, either by adapting the schedule
before the batch starts or by tightening the raw material specifications. The remainder is what
only the running batch reveals, plus noise. On the replay campaign:

.. code-block:: python

	z_only = PLS(n_components=2).fit(campaign.initial_conditions, campaign.quality[["titer"]])
	cv = z_only.cross_validate(campaign.initial_conditions, campaign.quality[["titer"]])
	print(f"Z alone: R2 = {float(z_only.r2_cumulative_.iloc[-1]):.2f}, "
	      f"Q2 = {float(cv.q_squared.iloc[0]):.2f}")

Two components of |Z| explain 27% of the titer variance in the fit and 23% in cross-validation,
consistent with the decomposition's 31% for the initial conditions. Roughly three quarters of the
outcome variance on this process is not predictable before the batch starts. That remainder is an
upper bound on what a method acting during the batch can address: it also contains the quality
assay's own repeatability (measured from duplicate assays, and subtracted) and whatever arrives
after the last decision point. How much of it the trajectories reveal in time is what the
held-out check in :ref:`the prediction section <APPS_batch_mcc_predicting>` measures. All
of this a plant can compute without a simulator.

**3. Something can still be done once the batch has revealed itself.** There must be manipulated
variables with leverage left at the time a shortfall becomes visible. Process knowledge answers
this first. On this process the timing of the temperature shift decides how much biomass the
production phase starts with, so moving the shift later has a large effect for as long as the
growth phase is not over. A process whose quality is fixed by the charge, or whose adjustable
variables have lost their effect by the time the outcome can be predicted, has no such window.
:ref:`The decision-point sweep <APPS_batch_mcc_window>` below measures the window on this
process.

**4. The history contains deliberate schedule variation, or can be made to.** A model fitted on
batches that all ran the same schedule can predict the outcome, but it has no information about
what a schedule *change* would do. The data requirement for control is history in which the
manipulated schedules actually moved, in shapes like the ones the controller will later use:
moves that extend past the intended decision point, since only the remainder of the schedule is
ever changed, and moves at least as large as the corrections the optimiser will be allowed.
Flores-Cerrillo and MacGregor's nylon controller was identified from 45 batches, 30 of which
carried deliberate moves at the two decision points, and they reported adequate control from as
few as 15 batches, 10 of them with moves; for a model identified from historical data alone,
which may carry no such moves, they suggest updating it from batch to batch. If the records
contain no such variation, a small designed campaign supplies it, at the cost of the product
those batches would otherwise have made.

These four conditions also place mid-course correction among the other things the same data
support. Each layer in the table below needs more than the one before it, and each acts on
something the one before cannot. Monitoring uses the two statistics of :ref:`the latent variable
monitoring section <LVM_monitoring>`: the SPE (squared prediction error, a batch's distance off
the model plane) and Hotelling's :math:`T^2` (its distance from the centre of the training data
within the plane).

======================  ==========================================  =============================================
Layer                   Acts on                                     Cannot reach
======================  ==========================================  =============================================
Monitoring              A batch leaving the family of past          The outcome: it flags an unusual batch, it
                        operation, flagged by its SPE and            does not say how the batch will end
                        :math:`T^2` while it runs
End-point prediction    Knowing the outcome before the batch        Changing the outcome
                        ends, from |Z| and the trajectory so far
Feedforward adaptation  The share of the variation visible in       Disturbances that develop while the batch
                        |Z| before the batch starts                 runs
Mid-course correction   The share that develops during the batch,   Batches the model does not recognise, and the
                        while there is leverage left to act         share that arrives after the last decision
                                                                    point
======================  ==========================================  =============================================

Monitoring needs only aligned trajectories of good batches. End-point prediction needs the final
quality as well. The two acting layers need, in addition, a history in which the schedule moved,
and mid-course correction needs leverage after the decision point. The rest of this page builds
the prediction and the correction on the simulator, and then, in :ref:`the procedure
<APPS_batch_mcc_procedure>`, states the steps for a plant.

.. _APPS_batch_mcc_predicting:

Predicting a batch while it runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: batch processes; monitoring
	single: trimmed score regression

The model is the batchwise-unfolded PLS of :ref:`the second case study <APPS_batch_case_sbr>`,
with the pre-batch block joined onto the unfolded trajectories as :ref:`the third
<APPS_batch_case_fmc>` does. Each batch becomes *one row*: its |Z| values, followed by every
sample of every tag. On this process a row has 11 pre-batch values and 20 samples of each of 5
tags, 111 columns in all, and that long row is regressed onto the final titer. Centring each
column removes the average trajectory, so the loadings weight each batch's *deviation* from
typical behaviour at each point in time. Of the ways of arranging the three-way array that
Westerhuis, Kourti and MacGregor compare (batchwise; observation-wise, with one row per sample;
and the lagged form that appends each tag's preceding samples as extra columns to describe local
dynamics), the batchwise row is the one a running batch fills in from left to right, which is
what a decision point needs. The upper row of the figure below shows the layout; the lower row
is explained shortly.

.. _APPS_batch_mcc_row:

.. figure:: ../figures/batch/mcc-decision-point-row.png
	:source: batch/mcc-decision-point-row.py
	:alt: The unfolded row of one batch: 11 pre-batch values then 20 samples of each of five tags, 111 columns. Below it, the same row for a running batch at the day-4 decision point: the pre-batch values and the first eight samples of every tag are known, the future samples of the three responding tags are missing and estimated, and the future samples of pH and temperature are the schedule under consideration.
	:width: 900px
	:scale: 80
	:align: center

.. _APPS_batch_mcc_requirements:

Two practical requirements come with this structure. The first is that the batches must be
*aligned*: the same number of samples per batch, with corresponding samples meaning the same
process phase. The simulator's batches are aligned by construction, and the package provides
resampling (used on the nylon data at the start of this section) and dynamic time warping for
plant data that is not. For on-line use the alignment has to be computable while the batch runs.
A fixed-duration recipe aligns on clock time, as this page's does. Where the phases vary in
length, align on an indicator variable that is monotone during the batch and available in real
time (cumulative feed, integrated offgas carbon dioxide, cumulative base addition): a decision
point is then the moment the indicator reaches a set value, and the corrected schedule, which
comes back indexed by aligned sample, is mapped to clock time through the same indicator.

The second is the identification requirement stated as :ref:`condition 4
<APPS_batch_mcc_when>`: the training campaign must contain deliberate schedule variation.
The campaign below follows it: 200 historical batches whose pH and temperature schedules carry
deliberate smooth perturbations. The perturbations are drawn at five *knots*, a small number of
anchor points in time, as independent offsets with a standard deviation of 2.5 °C for temperature
and 0.25 pH units for pH, interpolated linearly between the knots and clipped to the operating
range, so each batch's schedule is a gentle wander rather than a step change. Variation of that
size costs product: the campaign's batches average 5.99 g/L against 7.57 g/L for the replay
campaign. A plant would choose a smaller amplitude and a shorter campaign; :ref:`the sample-size
comparison <APPS_batch_mcc_size>` below shows what a smaller history gives up. The batches
come from three feed classes (in this plant's story: three supplier or campaign combinations,
labelled A, B and C), which the simulator records with each batch as a plant would record a
supplier or a seed lot; the campaign has 81, 71 and 48 batches of each.

.. code-block:: python

	rng = np.random.default_rng(0)                    # one master seed drives every number on this page
	train_seed = int(rng.integers(2**31))
	test_seed = int(rng.integers(2**31))
	batch_seeds = rng.integers(2**31, size=40)        # per-batch execution seeds, reused later

	# simulate_campaign draws its per-batch seeds from the master generator in this
	# order, so batch_seeds[i] reproduces the i-th test batch exactly. That is what
	# makes the corrected re-run below a same-batch counterfactual.

	train = simulator.simulate_campaign(200, policy="historical", mv_variation=2.5,
	                                    random_state=train_seed)
	z_train = train.initial_conditions
	labels = np.asarray(list(train.classes))
	z_mean, z_sd = z_train.mean(), z_train.std(ddof=1)
	print(f"training campaign: mean titer {train.quality['titer'].mean():.2f} g/L")

One more look at the pre-batch block |Z| before modelling it. The eleven measured variables are
correlated (they reflect a few underlying causes: how viable the seed culture is, how rich the
medium lot is, how much of a growth inhibitor came in with a supplier stream), so a two-component
PCA summarises them well:

.. code-block:: python

	z_pca = PCA(n_components=2).fit(MCUVScaler().fit_transform(z_train))
	scores = z_pca.scores_

	fig = go.Figure()
	for label, colour in (("A", "#0072B2"), ("B", "#E69F00"), ("C", "#D55E00")):
	    mask = labels == label
	    fig.add_trace(go.Scatter(x=scores.iloc[mask, 0], y=scores.iloc[mask, 1],
	                             mode="markers", name=f"class {label}", marker_color=colour))
	fig.update_layout(xaxis_title="t1", yaxis_title="t2")
	fig.show()

.. figure:: ../figures/batch/golden-batch-z-scores.png
	:source: batch/golden-batch-figures.py
	:alt: PCA score plot of the training campaign's Z block; the three feed classes occupy overlapping ranges along the first component.
	:width: 750px
	:scale: 80
	:align: center

The three classes do not form separated clusters; they occupy overlapping ranges along the first
score direction, which orders the batches from favourable to unfavourable incoming material.
Assigning a batch to the nearest class centroid in the standardised |Z| variables recovers its
recorded class 84.5% of the time on the training campaign, and when it misses, it assigns the
neighbouring range. On a plant the class is usually known from the batch's own records; the
nearest-centroid assignment is the fallback when it is not. One prediction model is fitted per
class:

.. code-block:: python

	models = {}
	for group in ("A", "B", "C"):
	    ids = [i for i, c in zip(train.batches, labels) if c == group]
	    models[group] = BatchPLS(n_components=4).fit(
	        {i: train.batches[i] for i in ids},
	        train.quality.loc[ids],
	        initial_conditions=z_train.loc[ids],
	    )
	    print(f"class {group}: {len(ids)} batches, R2 = {models[group].r2_cumulative_.iloc[-1]:.2f}")

	def nearest_class(z_row):
	    z_std = (z_row - z_mean) / z_sd
	    centroids = {g: ((z_train.loc[labels == g] - z_mean) / z_sd).mean() for g in "ABC"}
	    return min(centroids, key=lambda g: float(((z_std - centroids[g]) ** 2).sum()))

	agreement = np.mean([nearest_class(z_train.loc[i]) == c for i, c in zip(train.batches, labels)])
	print(f"nearest-centroid assignment agrees with the recorded class {100 * agreement:.1f}% of the time")

The reason for one model per feed class, rather than one global model, deserves stating, because
the global alternative was tried first and failed. A single global model fitted on all 200
batches predicts final titer acceptably. Used for *control*, however, its corrections moved some
batches in a direction that lowered their executed titer. The cause is the interaction that
:ref:`the variance decomposition <APPS_batch_mcc_variance>` reported: the effect of a
schedule change depends on the feed class. Holding the reactor warm in mid-batch rescues a
slow-growing batch from a poor feed lot, and wastes productive time for a fast-growing one. A
single linear model has one gain direction to offer every batch, so it averages the two cases and
misdirects both. Fitting the model within a class range makes the gain locally right. The three
fits above reach :math:`R^2` values of 0.81, 0.90 and 0.94 on their own classes. Four components
are used throughout, and the held-out check later in this section is the test of that choice; the
eleven |Z| columns are scaled like the trajectory columns, with no extra block weighting, so they
carry 11 of the 111 columns' weight.

On a plant the groups come from a recorded categorical variable (a raw material supplier, a seed
lot, a campaign) or, failing that, from a partition along the first score of the |Z| block. The
test of whether local models are needed at all is the sign of the model's predicted effect of one
fixed reference move of the remaining schedule, delaying the temperature downshift by a day, say:
fit the model on each candidate group and compare the predicted effects. If the sign differs
between groups, a single model averages them and misdirects some.

**Three kinds of column at a decision point.** With a fitted model, predicting a *running* batch
is a missing data problem. Call the moment at which the prediction is made, and at which an
adjustment could be applied, a **decision point**. The lower row of :ref:`the layout figure
<APPS_batch_mcc_row>` shows the state of the unfolded row at the day-4 decision point,
when 8 of the 20 samples have been recorded. The |Z| values and the first 8 samples of every tag
are *known*. The remaining samples of the three responding tags (dissolved oxygen, offgas carbon
dioxide, volume) are *missing*, and are estimated by the model. The remaining samples of pH and
temperature, the two manipulated tags, are neither: they are the schedule under consideration.
For the question "what happens if nothing is changed?" they are set to the planned remaining
schedule, and for the correction they become the decision variables. Flores-Cerrillo and
MacGregor set the prediction up this way, and the implementation here follows them. The model's
pH and temperature columns hold the *recorded* trajectories, so the known samples of the two
manipulated tags are recorded values while the future samples are setpoints. The two differ by
the control error, which the regression treats as input noise; that attenuates slightly the gain
the model attributes to a schedule change, and the substitution is sound only where the control
loops track their setpoints. Where a loop can saturate (a base pump at its limit), the setpoint
and the recorded value part company, and the bounds handed to the optimiser must keep it out of
that region.

**Estimating the scores of a partial row.** The scores of the batch so far are estimated by
trimmed score regression, as in :ref:`the second case study's on-line prediction
<APPS_batch_case_sbr_online_prediction>`: the model's weights applied to the known columns alone
give a trimmed score, :math:`\boldsymbol{\tau}`, and a regression fitted on the training batches,
from their trimmed scores to their complete-row scores, corrects it,
:math:`\hat{\mathbf{t}} = \mathbf{B}_k \boldsymbol{\tau}`, where :math:`\mathbf{B}_k` depends only on
which columns are known at decision point :math:`k`. The regression carries the spread of the
training batches around the model plane as well as the plane itself, which is what holds the
estimate near the average training batch while the known columns say little and lets it move out
as they say more. García-Muñoz, Kourti and MacGregor found it, with conditional mean replacement,
the best of the estimators on this batch-so-far problem; the package implements it as
``PLS.project``. Two properties of the estimate carry the rest of this page:

- For a fixed pattern of known and unknown columns, the score estimate is a *fixed linear
  function* of the known columns, and therefore of the future setpoint columns. That is what
  turns the correction, later, into a small convex program.
- The regression inverts a small matrix built from the known columns, and its *condition number*
  (the ratio of its largest to its smallest scaling) says how much the estimate amplifies noise.
  The package reports it with every projection, and the table below gives it for one class.

**The prediction interval at a decision point.** The predicted titer is
:math:`\hat{y} = \mathbf{c}^T \hat{\mathbf{t}}`, with :math:`\mathbf{c}` the model's quality
loadings. Its uncertainty is not the model's uncertainty on complete rows: early in the batch the
score estimate rests on few columns and is far less certain than at the end. The interval used
here carries that. At decision point :math:`k`, the :math:`N` training batches are re-projected
under the same pattern of known columns, their predicted titers are compared with their measured
ones, and the root mean square of those :math:`N` prediction errors, on :math:`N - A - 1` degrees
of freedom, is :math:`s_k`, the model's prediction error at decision point :math:`k`. It replaces
the full-row training error. The half-width is

.. math::

	\text{half-width}_k = t_{N-A-1} \; s_k \; \sqrt{1 + \frac{1}{N} + \frac{T^2_k}{N-1}}

where :math:`t_{N-A-1}` is the Student's t quantile for the confidence level, :math:`A` is the
number of components, and :math:`T^2_k` is Hotelling's :math:`T^2` of the estimated scores
(:ref:`their distance from the centre of the training data within the model plane
<LVM-Hotellings-T2>`), computed against the covariance of the training batches' score estimates
under the same pattern: the time-varying covariance Nomikos and MacGregor introduced for batch
monitoring, which García-Muñoz, Kourti and MacGregor apply to missing-data score estimates. For
:math:`s_k` and that covariance the future setpoint columns count as known, as they do when the
prediction is made, each training batch supplying its own recorded values there. The SPE that
later gates the correction is computed differently: on the |Z| values and the first :math:`k`
samples only, with the whole remaining trajectory missing, and its limit comes from the training
batches' SPE under that same pattern. A second SPE limit, under the pattern that includes the
future setpoint columns, caps the candidate row in the optimisation, which is why two SPE limits
appear at the day-4 decision point in :ref:`the correction section
<APPS_batch_mcc_correcting>`. The table below gives :math:`s_k` for the three class models
at selected decision days, with the condition number of class A's estimator in parentheses.

============  ==============  ============  ============
Decision day  Class A [g/L]   Class B       Class C
============  ==============  ============  ============
1             1.10 (71)       1.28          1.04
2             1.10 (41)       1.20          0.97
3             1.10 (27)       1.16          0.80
4             0.96 (23)       0.99          0.77
5             0.85 (7)        0.90          0.64
6             0.84 (5)        0.92          0.66
8             0.69 (3)        0.78          0.54
10            0.58 (1)        0.52          0.43
============  ==============  ============  ============

The error falls by half or more between the first day and the last for every class, so the
prediction interval narrows as more of the batch is observed: the funnel shape expected of a
batch monitoring scheme. The condition number falls with it, from below 200 on the first day to 1
when every column is known, so no decision point on this process asks the estimator for more
than it can give. The day-10 entry is the model's error with every column known. An interval
built from that number would declare the first day's predictions twice as precise as they are;
the interval built at the decision point does not.

**Watching one batch.** The object that later computes corrections also answers the monitoring
question. Built with only the model, the nominal schedule and the list of manipulated tags, it can
predict but not correct. The code below builds one per class, takes one batch from the poorest
feed class in a fresh campaign of 40 batches, and asks for the prediction at every decision point:

.. code-block:: python

	nominal = simulator.nominal_trajectory().reset_index(drop=True)
	predictors = {g: MidCourseCorrector(models[g], nominal, mv_tags=["pH", "temperature"])
	              for g in "ABC"}

	test = simulator.simulate_campaign(40, policy="replay", random_state=test_seed)
	z_test = test.initial_conditions

	batch_id = 28
	seed = int(batch_seeds[list(z_test.index).index(batch_id)])
	z_row = z_test.loc[batch_id]
	base = simulator.simulate_batch(z_row, random_state=seed)
	predictor = predictors[nearest_class(z_row)]

	rows = []
	for k in range(1, 20):
	    p = predictor.predict(base.tags.iloc[:k].reset_index(drop=True), initial_conditions=z_row, k=k)
	    rows.append({"day": k / 2, "y_hat": float(p.y_hat.iloc[0]),
	                 "half_width": float(p.half_width.iloc[0]),
	                 "spe": p.spe_so_far, "spe_limit": p.spe_limit_monitor})
	funnel = pd.DataFrame(rows)
	print(funnel.round(2).to_string(index=False))

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=funnel["day"], y=funnel["y_hat"] + funnel["half_width"],
	                         mode="lines", line_color="#56B4E9", showlegend=False))
	fig.add_trace(go.Scatter(x=funnel["day"], y=funnel["y_hat"] - funnel["half_width"],
	                         mode="lines", line_color="#56B4E9", fill="tonexty",
	                         name="95% prediction interval"))
	fig.add_trace(go.Scatter(x=funnel["day"], y=funnel["y_hat"], mode="lines+markers",
	                         line_color="#0072B2", name="predicted final titer"))
	fig.add_hline(y=8.0, line_dash="dash", line_color="#009E73")
	fig.add_hline(y=base.titer, line_dash="dot", line_color="#D55E00")
	fig.update_layout(xaxis_title="Decision point [day]", yaxis_title="Predicted final titer [g/L]")
	fig.show()

.. _APPS_batch_mcc_funnel:

.. figure:: ../figures/batch/mcc-monitoring-funnel.png
	:source: batch/midcourse-correction-figures.py
	:alt: Predicted final titer of one poor batch at every decision point with its prediction interval; the prediction sits near 3.5 grams per litre from the first day, the interval narrows from plus or minus 2.3 grams per litre at day 0.5 to plus or minus 1.6 at day 4 and plus or minus 0.9 at day 9.5, and the whole interval lies below the 8 grams per litre target at every decision point.
	:width: 900px
	:scale: 80
	:align: center

This batch is headed for roughly 3.5 g/L against a target of 8 g/L, drawn across the figure as a
floor the plant would like every batch to clear (it is essentially the 8.01 g/L disturbance-free
reference from :ref:`the replay campaign <APPS_batch_mcc_replay>`). The shortfall is visible in
the batch's own data from the first day: the poor feed lot shows in |Z| immediately, and the slow
growth it causes shows in the gas trajectories soon after. What the first days cannot yet say is
how sure that reading is, and the interval carries it: ±2.3 g/L at day 0.5, ±1.6 g/L at day 4 and
±0.9 g/L at day 9.5. Its upper end sits below the floor at every decision point, by 2.2 g/L at
day 0.5 and by 2.9 g/L at day 4. The SPE of the batch so far stays under its limit throughout
(5.1 against a limit of 7.6 at day 4), so the model recognises this batch as one of the family it
was built from. Knowing this on day 4, what should the remaining six days of the schedule be?

.. _APPS_batch_mcc_heldout:

**Checking the prediction layer on held-out batches.** One batch shows the shape; the plant-side
check runs every held-out batch through the same prediction at every decision point and compares
with what the batches actually did. Any plant can run this on its own history, because it needs
no execution, only recorded batches with known outcomes. Here it uses the 40 fresh test batches:

.. code-block:: python

	checks = []
	for position, bid in enumerate(z_test.index):
	    z_i = z_test.loc[bid]
	    run = simulator.simulate_batch(z_i, random_state=int(batch_seeds[position]))
	    for k in (2, 4, 6, 8, 10, 12, 16, 18):
	        p = predictors[nearest_class(z_i)].predict(run.tags.iloc[:k].reset_index(drop=True),
	                                                  initial_conditions=z_i, k=k)
	        if p.in_control:                       # the SPE gate would have refused the rest
	            checks.append({"batch": bid, "day": k / 2, "titer": run.titer,
	                           "y_hat": float(p.y_hat.iloc[0]), "half_width": float(p.half_width.iloc[0])})
	checks = pd.DataFrame(checks)
	checks["error"] = checks["y_hat"] - checks["titer"]
	checks["covered"] = checks["error"].abs() <= checks["half_width"]
	summary = checks.groupby("day").agg(rmsep=("error", lambda e: float(np.sqrt(np.mean(e**2)))),
	                                     bias=("error", "mean"), coverage=("covered", "mean"))
	print(summary.round(2))
	worst = checks.loc[checks["error"].abs().idxmax()]
	print(f"worst projection: batch {worst['batch']} at day {worst['day']}: finished at {worst['titer']:.2f}, "
	      f"projected {worst['y_hat']:.0f} ± {worst['half_width']:.0f} g/L")

============  ===============  ============  ===============
Decision day  RMSEP [g/L]      Bias [g/L]    Coverage (95%)
============  ===============  ============  ===============
1             1.70             -1.40         0.92
2             1.44             -1.12         0.92
3             1.10             -0.84         0.95
4             0.80             -0.53         0.95
5             0.86             -0.57         0.95
6             0.92             -0.60         0.88
8             0.90             -0.66         0.88
9             0.89             -0.68         0.80
============  ===============  ============  ===============

The prediction becomes usable at day 4, where its root mean square error over the 40 batches is
0.80 g/L against a batch-to-batch standard deviation of 1.20 g/L, and stays there. Before day 4
the error is mostly bias. The estimator holds a batch near the average training batch while the
known columns say little, and the average training batch is a poor one: the training campaign's
mean titer is 5.99 g/L against 7.57 g/L for the 200-batch replay campaign, because deliberate
perturbations of a good recipe mostly cost titer. An early prediction of a replay batch is
therefore pulled low, by 1.4 g/L on average at day 1; the worst projection, printed last, is a
batch that finished at 8.3 g/L and was projected at day 1 to 4 ± 2 g/L. The interval carries
most of this: coverage is 92% on days 1 and 2 and at the nominal 95% from day 3 to day 5, which
is what the no-correction rule (the dead band, defined in :ref:`the correction section
<APPS_batch_mcc_correcting>`) relies on. Later in the batch the bias remains, at 0.5 to 0.7 g/L,
while the interval keeps narrowing, and coverage falls to 80% by day 9: the nominal schedule lies
toward the edge of the region the model was fitted on, and a model extrapolating slightly keeps
its bias. A plant would see the same effect in this check, and it is one of the reasons the
decision point should not be placed late.

.. _APPS_batch_mcc_correcting:

Correcting mid-course
~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: mid-course correction
	pair: batch processes; control

The idea of a mid-course correction predates its latent variable form: Yabuki and MacGregor
formulated it for semi-batch reactors in 1997, predicting the final properties from on-line
measurements plus a few off-line samples, and correcting only when that prediction fell outside a
defined no-control region. Flores-Cerrillo and MacGregor had used latent variable models for it
with a few discrete moves of the manipulated variables; their 2004 paper, the one this page builds
on, extended it to adjusting the complete remaining trajectories, with the correction computed in
the score space of a PLS model. At each decision point the procedure is:

1. **Predict.** Estimate the final quality from |Z|, the samples so far and the planned remaining
   schedule, with its interval at this decision point, as in :ref:`the prediction section
   <APPS_batch_mcc_predicting>`.
2. **Check that the model applies.** Compare the SPE of the batch so far with its limit for this
   decision point. Flores-Cerrillo and MacGregor compute this check before any correction is
   computed: the prediction is only trustworthy for a batch that resembles the data the model was
   built from, and if the batch-so-far has an unusually large SPE (its measurements do not fit the
   model's correlation structure; see :ref:`interpreting the SPE <LVM-interpreting-SPE-residuals>`),
   a correction computed from that model is a guess, and the safer action is to not correct.
3. **Apply the dead band.** This is Yabuki and MacGregor's no-control region. Every prediction
   carries uncertainty, and a correction computed from noise adds variance instead of removing it.
   Correct only when the predicted shortfall is large relative to the prediction interval. The
   setting used on this page asks that the *whole* interval fall short of the target: the upper
   end of the interval must lie below the floor.
4. **Compute the correction.** Solve for the remaining schedule, as described next.
5. **Implement it** for the remainder of the batch, and return to step 1 at the next decision
   point, if there is one.

Flores-Cerrillo and MacGregor compute the correction in the *score* space. Their decision
variable is :math:`\Delta \mathbf{t}`, an adjustment to the batch's latent variable scores,
chosen by a quadratic program with three terms: how far the predicted quality lands from its set
point, a movement suppression term on :math:`\Delta \mathbf{t}`, and a soft penalty on
Hotelling's :math:`T^2` that keeps the answer within the region past operation covered. The
remaining setpoint trajectories are then recovered by :ref:`inverting the PLS model
<LVM-PLS-model-inversion>`, and that inversion is what makes them smooth and consistent with how
the plant has operated historically.

The implementation on this page makes a different choice: it optimises the future setpoint
columns directly, and keeps the schedule plausible with stated constraints rather than through
model inversion. The two routes trade off differently. Inversion inherits the historical
correlation structure automatically; because the reconstructed trajectory is linear in the
scores, an actuator limit can be imposed only indirectly, as a constraint on the score adjustment
(Flores-Cerrillo and MacGregor bound the score adjustment itself; Golshan and co-workers project
the manipulated-variable constraints into the score space). Optimising the columns states the
engineering limits directly, but has to add the terms that hold the answer inside the model's
region. Written in the setpoint columns, with :math:`\mathbf{u}` the future
setpoint values in the model's scaled units and :math:`\mathbf{u}_\text{nom}` their planned
values, the correction is

.. math::

	\min_{\mathbf{u}} \quad
	w_1 \big(\hat{y}(\mathbf{u}) - y_\text{sp}\big)^2
	+ w_2 \,\|\mathbf{u} - \mathbf{u}_\text{nom}\|^2
	+ w_3 \,\text{SPE}(\mathbf{u})^2
	+ w_4 \,T^2(\mathbf{u})

subject to bounds on each setpoint and on its change between samples, and, when wanted, caps on
:math:`\text{SPE}(\mathbf{u})` and :math:`T^2(\mathbf{u})`. Because the score estimate of a
partial row is a fixed linear function of the known columns, the scores of the candidate row are
:math:`\hat{\mathbf{t}}(\mathbf{u}) = \mathbf{b} + \mathbf{A}\mathbf{u}`, so the predicted
quality :math:`\hat{y}(\mathbf{u})`, the SPE and the :math:`T^2` are all quadratic or linear in
:math:`\mathbf{u}`. Each term has a plain language reading:

- **Hit the target** (:math:`w_1`): the predicted final quality, as a function of the candidate
  future schedule, should come as close to the target as the model believes possible. This is
  Flores-Cerrillo and MacGregor's set-point term.
- **Move as little as necessary** (:math:`w_2`): deviations from the planned remaining schedule
  are penalised, so of the many schedules the model scores equally, the least disruptive is
  chosen. This is their movement suppression term.
- **Stay where the model has data** (:math:`w_3`, :math:`w_4`, and the caps): the candidate
  row's :math:`T^2` (its distance from the centre of the training data within the model plane)
  and its SPE (its distance off the plane) are penalised, and can be capped at the limits
  computed for this decision point. The :math:`T^2` penalty is theirs. The SPE term is added
  here, because a candidate written directly in the setpoint columns can leave the model plane in
  a way an adjustment to the scores cannot. The two limits do different jobs: the :math:`T^2`
  limit keeps the correction inside the region the history explored, and the SPE limit keeps the
  candidate row's *combination* of values consistent with how the variables move together.
- **Respect the actuators**: bounds on each setpoint, and rate-of-change limits between
  consecutive samples, including the seam between the last implemented sample and the first
  corrected one. The corrected schedule is also parameterised by a few knots (a small number of
  anchor points, with the schedule interpolated between them), so it stays as smooth as the
  schedules the plant actually runs. These constraints are added here; Flores-Cerrillo and
  MacGregor obtain smoothness from the model inversion, and bound the score adjustment rather
  than the setpoints.

With the two validity terms as penalties, the problem is a small convex quadratic program: a few
dozen unknowns, solved in milliseconds, with a unique answer. Turning the :math:`T^2` and SPE
limits into hard caps makes them quadratic constraints, so the problem becomes a quadratically
constrained one; it is solved here by returning the caps to the objective and raising their
weights until the caps are respected. Either way, no plant model in differential equation form is
required, only the historical data the plant already has.

Here is the whole procedure on the batch whose predictions are shown in :ref:`the monitoring
figure <APPS_batch_mcc_funnel>`. The correctors below extend the predictors with the
settings the decision needs: the target (8 g/L, treated as a floor, so batches predicted at or
above it are never touched), the dead band (1.0 half-widths: the whole interval must fall short),
the weights (tracking 1.0, movement 0.1, and no soft SPE or :math:`T^2` penalty, since the caps
do that job here), the actuator bounds (tightened inward by about two control-error standard
deviations, so an optimised setpoint does not sit on a rail the control loop then clips), the
rate limits, the caps at this decision point's limits, and the knot parameterisation:

.. code-block:: python

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
	        dead_band=1.0,                    # correct only when the whole interval falls short
	        weights={"target": 1.0, "movement": 0.1, "spe": 0.0, "t2": 0.0},
	        bounds={"temperature": (config.temp_bounds[0] + 0.3, config.temp_bounds[1] - 0.3),
	                "pH": (config.ph_bounds[0] + 0.04, config.ph_bounds[1] - 0.04)},
	        rate_limits={"temperature": 3.0, "pH": 0.5},
	        spe_cap="limit", t2_cap="limit",  # per-decision-point limits from the training batches
	        n_knots=4,
	    )

	outcome = correctors[nearest_class(z_row)].correct(
	    base.tags.iloc[:8].reset_index(drop=True),          # the first 8 samples: days 0 to 4
	    initial_conditions=z_row,
	    k=8,
	)
	print(f"decision: {outcome.reason}; predicted {float(outcome.y_hat_no_change.iloc[0]):.2f} "
	      f"± {float(outcome.half_width.iloc[0]):.2f} g/L if nothing changes, "
	      f"{float(outcome.dead_band_margin.iloc[0]):.1f} half-widths below the floor; "
	      f"SPE so far {outcome.spe_so_far:.2f} against a limit of {outcome.spe_limit_monitor:.2f}")
	corrected = outcome.schedule.copy()
	corrected.index = simulator.nominal_trajectory().index
	redo = simulator.simulate_batch(z_row, corrected, random_state=seed)   # identical disturbances
	print(f"replay {base.titer:.2f} g/L -> corrected {redo.titer:.2f} g/L "
	      f"(model predicted {float(outcome.y_hat.iloc[0]):.2f})")

	fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
	                    subplot_titles=("Temperature setpoint", "pH setpoint"))
	for row, tag in ((1, "temperature"), (2, "pH")):
	    fig.add_trace(go.Scatter(x=corrected.index, y=nominal[tag], mode="lines",
	                             line_shape="hv", name="nominal", line_color="#666666",
	                             showlegend=row == 1), row=row, col=1)
	    fig.add_trace(go.Scatter(x=corrected.index, y=corrected[tag], mode="lines",
	                             line_shape="hv", name="corrected at day 4", line_color="#D55E00",
	                             showlegend=row == 1), row=row, col=1)
	fig.update_layout(xaxis2_title="Time [day]", yaxis_title="Temperature [°C]", yaxis2_title="pH")
	fig.show()

.. figure:: ../figures/batch/mcc-correction-at-k.png
	:source: batch/midcourse-correction-figures.py
	:alt: Nominal and corrected temperature and pH schedules for the poor batch; the corrected schedule delays the downshift, holding the reactor warmer through day seven, and the executed titer rises from 3.66 to 5.65 grams per litre.
	:width: 900px
	:scale: 80
	:align: center

The printed decision reads: corrected; predicted 3.51 ± 1.59 g/L if nothing changes, 2.8
half-widths below the floor; SPE so far 5.08 against a limit of 7.65. Every gate passed. The
optimiser then found a schedule the model predicts at 4.84 g/L, with the candidate row's SPE at
6.1 against a cap of 9.1 and its :math:`T^2` at 1.0 against a cap of 11.3: neither cap was
active, nor any bound or rate limit, so the answer is the unconstrained optimum of the penalised
program, well inside the region the history covers. The two SPE limits at this decision point are
different quantities: the gate compared the SPE of the known columns only with the limit for that
pattern (7.65), whereas the cap applies to the SPE of the complete candidate row, known columns
plus the estimated and proposed future columns, and comes from the training batches under that
pattern (9.1).

The nominal schedule drops from the warm growth phase to the 29 °C production hold between days
3.5 and 4.5. The corrected schedule does not complete that drop on time: it holds at 34.1 °C at
day 4 and descends by about 1 °C per half-day until day 5.5 and more slowly after that, reaching
the production hold only around day 7.5, with a small pH excursion (a dip to 7.00 at day 4, back
through nominal near day 7, a peak of 7.11 at day 7.5). The physical reading is direct. This
batch's poor feed lot made it grow slowly, so at day 4 it has not yet built the biomass the
production phase needs; cooling it on the nominal timetable would arrest growth at a low cell
density. The correction gives the batch more growing time. No such rule was programmed anywhere:
the behaviour emerges from a regression on historical batches whose schedules were deliberately
varied.

Executed with the identical disturbance history, the batch finishes at 5.65 g/L instead of
3.66 g/L, a 55% improvement on this single batch. The model predicted 4.84 g/L for the corrected
schedule: a latent variable prediction regresses toward the mean, so it *understated* the gain its
own correction delivered. The distinction between a predicted and an executed gain is worth
keeping in view. Simulation studies can execute their corrections, and do: Flores-Cerrillo and
MacGregor obtained the final qualities in their nylon case study by rerunning the non-linear
simulation model with the trajectories the controller had computed. On an operating plant that
step is not available, so results from industrial case studies are reported as model predictions.
On this page the simulator makes execution cheap, so every gain from here on is an executed one.

.. _APPS_batch_mcc_campaign:

Does it work on the whole campaign?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One corrected batch is a single case. The campaign test runs many fresh batches through the full
procedure (predict at the decision point; check the model applies; apply the dead band; correct
when warranted; execute) and compares against the alternatives on the same batches with the same
disturbances. The package wraps that comparison, including two reference policies that bracket
what is achievable. The wrapper rebuilds the pipeline assembled by hand in :ref:`the correction
section <APPS_batch_mcc_correcting>` (the same master seed, the same 200 training batches,
the same per-class models, and correctors with the same settings, correcting at day 4), so its
corrected row is the configured procedure measured on the same 40 test batches:

.. code-block:: python

	result = evaluate_control_policies(simulator, y_target=8.0, random_state=0)   # about 7 minutes
	print(result.summary.round(3))
	print(f"{result.n_corrected} corrected, {result.n_harmed} harmed")

============================  ==========  ========  =========  =========
Policy                        Mean [g/L]  Sd [g/L]  Min [g/L]  Max [g/L]
============================  ==========  ========  =========  =========
Replay (do nothing)           7.507       1.198     3.655      8.925
Mid-course correction         7.786       0.750     5.652      8.925
Oracle from the same day      7.984       0.509     6.392      8.925
Adapted (feedforward)         7.824       1.013     4.573      9.309
============================  ==========  ========  =========  =========

All four rows are executed titers over the same 40 fresh batches. Reading them one at a time:

- **Replay** is the golden batch policy: every batch runs the nominal schedule. Its spread is the
  cost of doing nothing.
- **Mid-course correction** corrected 8 of the 40 batches, six from the poorest feed class and
  two from the middle one; the dead band left 31 alone and the SPE validity gate stopped one.
  Each corrected batch improved, by +0.48 to +2.45 g/L, and no batch was made worse. The
  campaign mean rises 0.28 g/L, and the standard deviation falls from 1.198 to 0.750 g/L, a 37%
  reduction. The policy acts on the low tail, where the largest losses are: the lowest replay
  batch (3.655 g/L, the single-batch demonstration) rises to 5.65 g/L and remains the lowest
  batch of the corrected campaign. One of the eight shows the dead band at its edge. Its
  no-change prediction was 6.0 g/L with an interval whose upper end sat 0.4 g/L under the floor,
  so it was corrected; it actually stood at 7.0 g/L, and the correction still raised it to
  8.5 g/L. The model predicted 4.8 to 6.7 g/L for the eight corrected schedules; executed, they
  finished at 5.7 to 8.5 g/L, so the model understated every one of its gains.
- **Oracle from the same day** answers "how much was achievable at that decision point at all?"
  For each corrected batch, the remaining schedule is optimised against the *simulator itself*
  (the true process), from the same day-4 state, with the same seed. Because the objective is the
  true process, this row estimates the ceiling for any mid-course scheme from that starting point
  (it is a local direct search over the same four-knot parameterisation, so it is a lower bound
  on the true ceiling). The mid-course policy captured 58% of
  the oracle's mean improvement; the remainder is what is lost by steering with a regression
  restricted to the region its history explored, rather than with the true process equations.
- **Adapted (feedforward)** runs *every* batch on the true optimal schedule for its own measured
  |Z|, computed before the batch starts: perfect feedforward adaptation, again a ceiling rather
  than an implementable policy. It raises the mean and the best batches (its maximum, 9.31 g/L,
  is the table's highest), but its *minimum is worse than the corrected policy's*: 4.57 against
  5.65 g/L. A schedule fixed at time zero, however well chosen, cannot answer a
  disturbance that develops during the batch. :ref:`The variance decomposition
  <APPS_batch_mcc_variance>` showed the outcome variance has a before-batch share and a
  during-batch share; the adapted row addresses the first, the mid-course row the second, and
  neither substitutes for the other.

.. figure:: ../figures/batch/mcc-policy-comparison.png
	:source: batch/midcourse-correction-figures.py
	:alt: Left panel: each corrected batch rises, by half a gram per litre to two and a half. Right panel: all forty batches under the four executed policies; correction removes the low tail.
	:width: 900px
	:scale: 80
	:align: center

.. _APPS_batch_mcc_size:

Two hundred training batches with deliberate moves is several years of one reactor's history.
Re-running the comparison with smaller training campaigns, changing only the ``n_train`` argument
of ``evaluate_control_policies`` (the ceilings switched off, the same 40 test batches), measures
what a shorter history gives up:

=================  ==========================  ===========  =================  ==============================
Training batches   Fit :math:`R^2` (A, B, C)   Corrected    Of which harmed    Mean gain, corrected batches
=================  ==========================  ===========  =================  ==============================
60                 0.95, 0.99, 1.00            10           4                  +0.11 g/L
100                0.83, 0.92, 0.97            6            0                  +1.04 g/L
200                0.81, 0.90, 0.94            8            0                  +1.40 g/L
=================  ==========================  ===========  =================  ==============================

With 60 batches, about 20 per class, four components fit the training batches almost perfectly
(:math:`R^2` of 0.95 to 1.00 on 111 columns), which is over-fitting: the intervals built from
those residuals are too narrow, the dead band admits ten batches, four are harmed, and the mean
gain is close to nothing. With 100 batches the scheme works at about three quarters of the gain
it reaches with 200. The fit :math:`R^2` cannot tell these cases apart; the held-out check of
:ref:`the prediction section <APPS_batch_mcc_heldout>` can, which is why it is the arbiter
in :ref:`the procedure <APPS_batch_mcc_procedure>`. Flores-Cerrillo and MacGregor's
15-batch result was obtained with one global model on a process with two manipulated variables;
the per-class models here divide the history three ways.

.. _APPS_batch_mcc_window:

Where to put the decision point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`The campaign comparison <APPS_batch_mcc_campaign>` used a single decision point at
day 4 of 10. That choice matters. Sweeping it re-runs that whole executed comparison at each
decision day, changing only the ``decision_points`` argument of ``evaluate_control_policies``,
and shows a window:

============  ===========  =================  ==============================
Decision day  Corrected    Of which harmed    Mean gain, corrected batches
============  ===========  =================  ==============================
2             9            2                  +1.12 g/L
3             9            1                  +1.42 g/L
4             8            0                  +1.40 g/L
5             8            0                  +0.49 g/L
6             8            7                  -0.04 g/L
7             8            8                  -0.23 g/L
============  ===========  =================  ==============================

.. figure:: ../figures/batch/mcc-decision-point-window.png
	:source: batch/midcourse-correction-figures.py
	:alt: Mean executed gain of the corrected batches versus the decision day, highest at days three and four and negative from day six.
	:width: 900px
	:scale: 80
	:align: center

The two ends of the window are limited by different things. Early in the batch the prediction
cannot yet separate the batches that will fall short from those that will not, as :ref:`the
held-out check <APPS_batch_mcc_heldout>` measured: at day 2 its error is 1.4 g/L, above the
batch-to-batch spread, with a bias of 1.1 g/L toward the training campaign's poor average batch,
so the dead band admits nine batches and the correction harms two of them. By day 3 the error has
fallen to 1.1 g/L and one of nine corrections harms its batch; by day 4 none does. Late in the
batch the prediction is at its most accurate, but the remaining schedule no longer has the
leverage to act on it: the growth phase is over, and what is left to act on is mostly model
error, so nearly every correction does slight damage. On this process the window is days 3 to 5.
Days 3 and 4 give the same mean gain, about +1.4 g/L, and day 4 harms no batch: late enough that
a struggling batch has revealed itself in the gas trajectories, early enough that the growth
phase can still be extended. The window's location is a property of the process, not of the method; finding it
needs the held-out prediction check, process knowledge of where the leverage lies, and, where a
simulator exists, a sweep like this one.

A plant without a simulator has a data-only version of the leverage half of this picture. The
model's predicted effect of one fixed reference move of the remaining schedule, at each candidate
decision day, is a single number per day. Here the reference move raises the temperature setpoint
by 2 °C for the next two days, for the batch of :ref:`the correction section
<APPS_batch_mcc_correcting>`:

.. code-block:: python

	leverage = []
	for k in range(2, 19, 2):
	    moved = nominal.copy()
	    moved.loc[k:k + 3, "temperature"] = np.minimum(moved.loc[k:k + 3, "temperature"] + 2.0, 38.7)
	    so_far = base.tags.iloc[:k].reset_index(drop=True)
	    y_nominal = float(predictor.predict(so_far, initial_conditions=z_row, k=k).y_hat.iloc[0])
	    y_moved = float(predictor.predict(so_far, initial_conditions=z_row, schedule=moved, k=k).y_hat.iloc[0])
	    leverage.append({"day": k / 2, "predicted effect [g/L]": round(y_moved - y_nominal, 2)})
	print(pd.DataFrame(leverage).to_string(index=False))

The model's predicted effect of that move is zero at day 1, rises to +0.84 g/L at day 3, is
+0.72 g/L at day 4 and +0.31 g/L at day 5, and is zero or negative from day 6 on. Executed on
the same batch with the same seed, the move actually gives -0.55 g/L at day 1 (warming a batch
that is already at its growth optimum slows it), +0.45 g/L at day 3, +0.82 g/L at day 5 and
still +0.60 g/L at day 7. The model locates the front of the window and understates the leverage
that remains late in the batch; that understatement is the same model error that turns the late
corrections harmful. The data-only measure therefore says where the model can still be *trusted
to steer*, which is the quantity the decision point should be placed on, rather than where the
process could still be moved.

.. _APPS_batch_mcc_trust:

How far should the model be trusted?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :math:`T^2` and SPE penalties and caps are the settings that keep the optimiser inside the
region the historical data supports, and they raise a sharper question: how far outside that
region should the optimiser be allowed to move? Relaxing the :math:`T^2` penalty (the
``weights["t2"]`` setting, swept from 3.0 down to 0, with the hard caps removed) and re-running
the executed comparison at each setting measures the answer for this process. The table gives the
mean titer of the eight corrected batches, predicted by the model and executed, and the figure
below, the exploration figure, plots it:

=====================  =================  ================
:math:`T^2` weight     Predicted [g/L]    Executed [g/L]
=====================  =================  ================
3.0                    5.62               6.76
1.0                    5.73               6.85
0.3                    5.82               6.98
0.1                    5.86               7.04
0.03                   5.88               7.05
0                      5.89               7.06
=====================  =================  ================

.. figure:: ../figures/batch/mcc-exploration-dial.png
	:source: batch/midcourse-correction-figures.py
	:alt: Predicted and executed mean titers of the corrected batches as the T-squared penalty relaxes; both rise as the optimiser is freed, and the executed line sits above the predicted line throughout.
	:width: 900px
	:scale: 80
	:align: center

On this process, at this decision point, freeing the optimiser helped monotonically. The executed
mean titer of the eight corrected batches rises from 6.76 g/L at the most conservative setting
to 7.06 g/L with the penalty removed, each step of extra freedom produced a real improvement, and
the executed titer sat *above* the model's own prediction at every setting (the prediction rises
from 5.62 to 5.89 g/L over the same range). The reason is where the poorest class's best
schedule sits. It is not outside
the actuator range, which the training campaigns already span. It is an unusual *combination* of
setpoints: a warm hold carried well past the day the nominal recipe cools, which few training
batches did. That is exactly what :math:`T^2` measures, distance from the centre of the training
data within the model plane, so penalising :math:`T^2` holds the correction back from a schedule
that is physically available and, for these batches, better.

This does not show that the constraints are unnecessary. The same freedom, at the late decision
points in :ref:`the decision-day sweep <APPS_batch_mcc_window>`, is what made corrections
harmful: there the model's apparent leverage was error, and the constraints are what would have
contained it. Taken together, the two figures show the trade-off: the validity limits exchange
reachable improvement for protection from model error, the balance depends on where the process's
true optimum sits relative to the explored region, and the balance can be *measured*, on batches
the model has never seen, before the scheme is trusted in production.

.. _APPS_batch_mcc_procedure:

Applying it on a plant
~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: mid-course correction; procedure

Every result on this page up to this point was obtained on a simulator, where a corrected batch can
be executed and its gain measured. A plant cannot execute the counterfactual, so the procedure has
to be arranged so that each step is checked with what a plant *can* measure before the next step is
trusted.

1. **Establish the case.** Work through the :ref:`four conditions
   <APPS_batch_mcc_when>` on the plant's own records: the quality spread against the
   setpoint spread; the |Z|-only regression and its :math:`Q^2`; the manipulated variables that
   keep their leverage after the point where a shortfall becomes visible; and whether the history
   contains schedule variation in the shapes a correction would use. If it does not, plan the
   designed campaign that supplies it before going further.

2. **Assemble and align the data.** One row per batch: |Z|, the aligned trajectories of every
   tag, the final quality, with an alignment that can be computed while a batch runs (clock time
   for a fixed-duration recipe, otherwise a real-time indicator variable, as described in
   :ref:`the prediction section <APPS_batch_mcc_predicting>`). Decide what the target
   means for this product: a floor (more is
   better, corrections act only on shortfalls), a ceiling, or a specification to be hit from
   both sides. That decision sets the dead band's direction.

3. **Fit and validate the prediction layer.** Fit the batchwise-unfolded PLS model on the
   historical campaign, with cross-validation choosing the number of components. Then run the
   held-out prediction check at every candidate decision point, on batches the model was not
   fitted on: the error, the bias and the interval coverage by decision day, as in :ref:`the
   held-out table <APPS_batch_mcc_heldout>`, together with the condition number of the
   estimator. This check decides two things at once: the earliest decision point at which the
   prediction can be trusted, and whether the interval is calibrated there, which the dead band
   depends on; it is also the test of the number of components and of the size of the history,
   as :ref:`the sample-size comparison <APPS_batch_mcc_size>` showed. If the model
   predicts acceptably but the sign of its predicted effect of a fixed reference move differs
   between groups of batches (the test described in :ref:`the prediction section
   <APPS_batch_mcc_predicting>`), fit local models, per feed class, grade or product, as
   this page did.

4. **Choose the decision points.** The prediction check says when the batch can be *seen*. For
   when it can still be *steered*, the fitted model gives the data-only measure of :ref:`the
   decision-point section <APPS_batch_mcc_window>`: its predicted effect of a fixed
   reference move at each candidate decision day. Process knowledge, and a sweep where a
   simulator exists, confirm it. The decision point goes where the held-out error has reached its
   plateau and the predicted leverage is still a useful fraction of the typical shortfall. Two
   decision points sufficed in Flores-Cerrillo and MacGregor's nylon study; one sufficed here.

5. **Set the correction's constraints.** Bounds: the narrower of the actuator limits and the
   permitted operating range for the product, tightened inward by about two control-error
   standard deviations, and excluding any region where a control loop saturates. Rate limits the
   control loops can follow, a knot parameterisation as smooth as the schedules the plant runs,
   and the SPE and :math:`T^2` caps at the limits computed for the decision point. Begin with a
   strong :math:`T^2` penalty, the conservative end of :ref:`the exploration figure
   <APPS_batch_mcc_trust>` where the weight is 3.0: the executed gains in that figure were
   measured against the true process, which a plant cannot do.

6. **Validate what can be validated offline.** The prediction layer has been validated in
   step 3. The correction's *gain* cannot be validated on history, because no historical batch
   was run twice. What can be checked is consistency. For each historical batch that carried a
   schedule move, predict its quality at the decision point twice, once with its actual
   remaining schedule and once with the nominal schedule in its place; the difference is the
   model's predicted effect of the move. Over those batches the prediction with the actual
   schedule should have the lower error, and the sign of the predicted effect should agree with
   the sign of the batch's outcome relative to the nominal-schedule prediction in most of them.
   Disagreement here is the identification requirement failing, and more excitation data is the
   remedy.

7. **Deploy in stages, and keep the calibration record.** Begin with the dead band and caps at
   their conservative settings, so only the clearest shortfalls are corrected. For every corrected
   batch record three numbers: the no-change prediction at the decision point, the predicted
   outcome of the corrected schedule, and the realised outcome. The first two are the model's
   claim; the third is the plant's answer. Over time the predicted-versus-realised record is the
   plant's own version of :ref:`the exploration figure <APPS_batch_mcc_trust>`, and it
   is the evidence for loosening the settings, or for not doing so. The no-change prediction is
   also the closest thing a plant has to the counterfactual: a corrected batch that lands where
   its no-change prediction said it would have landed is a correction that did nothing. Alarm
   bands derived from the golden batch on the manipulated tags will trip on a corrected schedule;
   re-base them on the corrected schedule, or replace them with the model's SPE and :math:`T^2`
   monitoring, before the first corrected batch runs.

8. **Keep the model current.** Batches the validity gate refuses are handed to the
   :ref:`monitoring chart <LVM_monitoring>` and :ref:`troubleshooting
   <APPS_multivariate_monitoring>` tools: an out-of-family batch needs diagnosis, not
   optimisation. As the process drifts, the model ages in the way the :ref:`adaptive soft sensor
   <APPS_adaptive_soft_sensor>` section describes, and the held-out check of step 3 is repeated on
   recent batches to decide when to re-identify.

Three limits of the method are worth stating plainly. It cannot recover a batch the validity gate
excludes. It cannot act on the share of variance that only materialises after the last decision
point. And it cannot exceed the information in the historical data, which is what the gap to the
oracle row measures.

The third limit is the one a hybrid model addresses: a mechanistic model of the balances and
kinetics, with an empirical latent variable model for what the balances leave out, can
extrapolate past the region the history explored in a way a regression cannot. This page does
not build one. The simulator plays the plant and is never part of the controller, and the oracle
row of :ref:`the campaign comparison <APPS_batch_mcc_campaign>` is the most such a model could
reach from the same decision point.

The methods on this page are implemented in `process_improve
<https://github.com/kgdunn/process-improve>`_ (``BatchPLS``, ``PLS.project``,
``MidCourseCorrector`` with its ``predict`` and ``correct`` methods, and
``evaluate_control_policies``, with the simulator in ``process_improve.simulation``); the figure
sources carry the exact seeds, so every number on this page can be regenerated.

.. _APPS_batch_mcc_further_reading:

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
  SPE validity gate and the data-requirement study. Their optimisation is over the score
  adjustment, with the trajectories recovered by model inversion; this page optimises the
  setpoint columns directly, as described in the text.
* Francisco Arteaga and Alberto Ferrer, "Dealing with missing data in MSPC: several methods,
  different interpretations, some examples", *Journal of Chemometrics*, **16**, 408-418, 2002.
  `<https://doi.org/10.1002/cem.750>`_ The source of trimmed score regression.
* Salvador García-Muñoz, Theodora Kourti and John F. MacGregor, "`Model predictive monitoring for
  batch processes
  <https://literature.learnche.org/item/157/model-predictive-monitoring-for-batch-processes>`_",
  *Industrial and Engineering Chemistry Research*, **43**, 5929-5941, 2004.
  `<https://doi.org/10.1021/ie034020w>`_ The comparison of score estimators for a partially
  observed batch, and the per-time score covariance limits of Nomikos and MacGregor applied to
  re-projected training batches.

* Masoud Golshan, John F. MacGregor, Mark-John Bruwer and Prashant Mhaskar, "Latent Variable
  Model Predictive Control (LV-MPC) for trajectory tracking in batch processes", *Journal of
  Process Control*, **20**, 538-550, 2010. `<https://doi.org/10.1016/j.jprocont.2010.01.007>`_ Their projection of the manipulated-variable constraints into
  the score space is the alternative to the setpoint-column formulation used here.

The foundational multiway papers, the alignment and spectroscopy references and the theses behind
them are listed with :ref:`the monitoring page <APPS_batch_readings>`.
