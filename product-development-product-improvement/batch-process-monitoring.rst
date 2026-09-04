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
first seeing that batches do not repeat even when the recipe does, then deciding whether the
process is one where acting during the batch can help, then predicting the outcome of a batch
*while it is still running*, and finally adjusting the remainder of the recipe when that
prediction falls short. The last step is called a **mid-course correction**. The section closes
with the procedure for applying it on a plant.

Every improvement claimed on this page is executed, not predicted: the adjusted batch is re-run
on a simulator whose disturbances repeat exactly. :ref:`The campaign comparison
<APPS_batch_monitoring_campaign>` measures how far the two differ.

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
every batch. :ref:`Alignment <APPS_batch_monitoring_requirements>` is revisited when the
modelling starts. All the code on this page runs top to bottom as one script; this first block
loads that dataset, aligns it, and measures the spread of each of the ten recorded variables
across the batches, as the average over time of the batch-to-batch standard deviation, relative
to the variable's average level:

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	from process_improve.batch import BatchPLS, load_nylon, resample_to_reference
	from process_improve.batch.control import MidCourseCorrector, evaluate_control_policies
	from process_improve.multivariate import MCUVScaler, PCA, PLS
	from process_improve.simulation import BioreactorSimulator, variance_decomposition

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
57 batches. These are evidently the variables the control layer holds: the recipe really is being
replayed, and the control layer really is delivering it. The other five spread between 1.9% and
7.4%. ``Tag10``, the widest, spreads 7.38%, about fourteen times more than ``Tag06``, in the same
57 batches under the same recipe. A variable that spreads this much under a fixed recipe is
responding to what happens inside the batch. The recipe repeats, but the batch does not.

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

Replaying the nominal schedule for 200 batches, with every disturbance channel at its realistic
default:

.. code-block:: python

	simulator = BioreactorSimulator()

	campaign = simulator.simulate_campaign(200, policy="replay", random_state=0)
	titer = campaign.quality["titer"]
	print(f"titer: mean {titer.mean():.2f} g/L, spread {titer.min():.2f} to {titer.max():.2f}, "
	      f"CV {100 * titer.std(ddof=1) / titer.mean():.1f}%")

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
layer delivered it to within a fraction of a degree. The final titers still range from 4.24 to
9.83 g/L, a 14.4% coefficient of variation, around a disturbance-free reference of 8.01 g/L (the
titer this schedule produces when every disturbance channel is switched off). This is the nylon
picture again, but now the causes can be separated and measured.

Because the simulator's channels can be switched off individually, the titer variance of a replay
campaign can be split into its sources. The decomposition below runs four campaigns of the same
size and schedule (one with all channels active, then one for each channel on its own) and reports
each source's share. The three single-channel variances do not add up to the total, because the
process is nonlinear; the difference is reported as a fourth share rather than folded into the
others:

.. code-block:: python

	print(variance_decomposition(simulator, n_batches=200, random_state=0).round(3))

.. _APPS_batch_monitoring_variance:

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
- The *interaction of the sources* accounts for the remaining 41%, the largest share. The two
  disturbances do not add: the titer a within-batch disturbance costs depends on the initial
  conditions it meets. In this process a batch from a poor feed lot grows slowly, and a
  disturbance that slows growth further costs it far more than the same disturbance costs a
  fast-growing batch. Acting on this share needs an intervention that knows which kind of batch
  it is acting on, a point that returns when the prediction models are built.

The two interventions built on this page are feedforward adaptation, which acts before the batch
starts, and mid-course correction, which acts while it runs. Each addresses a different share, so
neither covers the whole.

.. _APPS_batch_monitoring_when:

When is mid-course correction the right tool?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: mid-course correction; when to apply

The sections so far diagnose the problem. Before any model is built, the question is whether
mid-course correction fits the process at hand. Four conditions decide it, and each one can be
checked on a plant's own records.

**1. The final quality varies more than the recipe.** Compare the batch-to-batch spread of the
regulated variables with the spread of the responding variables and of the final quality, over
batches that ran the same recipe, as was done for the nylon batches. If the final quality repeats
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
outcome variance on this process is not predictable before the batch starts. That is the share a
method acting during the batch can address, and a plant can measure it without a simulator.

**3. Something can still be done once the batch has revealed itself.** There must be manipulated
variables with leverage left at the time a shortfall becomes visible. Process knowledge answers
this first. On this process the timing of the temperature shift decides how much biomass the
production phase starts with, so moving the shift later has a large effect for as long as the
growth phase is not over. A process whose quality is fixed by the charge, or whose adjustable
variables have lost their effect by the time the outcome can be predicted, has no such window.
:ref:`The decision-point sweep <APPS_batch_monitoring_window>` below measures the window on this
process.

**4. The history contains deliberate schedule variation, or can be made to.** A model fitted on
batches that all ran the same schedule can predict the outcome, but it has no information about
what a schedule *change* would do. The data requirement for control is history in which the
manipulated schedules actually moved, in shapes like the ones the controller will later use.
Flores-Cerrillo and MacGregor state this requirement in the paper this page's control method is
built on; their nylon controller was identified from 45 batches, 30 of which carried deliberate
moves at the two decision points, and they reported adequate control from as few as 15 batches,
10 of them with moves. If the records contain no such variation, a small designed campaign
supplies it.

These four conditions also place mid-course correction among the other things the same data
support. Each layer in the table needs more than the one before it, and each acts on something
the one before cannot.

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
<APPS_batch_monitoring_procedure>`, states the steps for a plant.

Predicting a batch while it runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: batch processes; monitoring
	single: trimmed score regression

The tool for relating the three layers is the batchwise-unfolded latent variable model of Nomikos
and MacGregor, with the pre-batch block joined onto the unfolded trajectories as Kourti, Nomikos
and MacGregor set out (see the :ref:`references below <APPS_batch_monitoring_further_reading>`).
Each batch becomes *one row*: its |Z| values, followed by every sample of every tag. On this
process a row has 11 pre-batch values and 20 samples of each of 5 tags, 111 columns in all, and
that long row is regressed onto the final titer with PLS. Centring each column removes the average
trajectory, so the model works with each batch's *deviations* from typical behaviour at each point
in time, and the loadings are free to weight a deviation at day 1 differently from the same
deviation at day 8. This is how a linear model captures a batch's time-varying behaviour. The
upper row of the figure below shows the layout; the lower row is explained shortly.

.. _APPS_batch_monitoring_row:

.. figure:: ../figures/batch/mcc-decision-point-row.png
	:source: batch/mcc-decision-point-row.py
	:alt: The unfolded row of one batch: 11 pre-batch values then 20 samples of each of five tags, 111 columns. Below it, the same row for a running batch at the day-4 decision point: the pre-batch values and the first eight samples of every tag are known, the future samples of the three responding tags are missing and estimated, and the future samples of pH and temperature are the schedule under consideration.
	:width: 900px
	:scale: 80
	:align: center

.. _APPS_batch_monitoring_requirements:

Two practical requirements come with this structure. The first is that the batches must be
*aligned*: the same number of samples per batch, with corresponding samples meaning the same
process phase. The simulator's batches are aligned by construction, and the package provides
resampling (used on the nylon data at the start of this section) and dynamic time warping for
plant data that is not.

The second is the identification requirement stated as :ref:`condition 4
<APPS_batch_monitoring_when>`: the training campaign must contain deliberate schedule variation.
The campaign below follows it: 200 historical batches whose pH and temperature schedules carry
deliberate smooth perturbations, of a size a plant's operating history plausibly spans. The
perturbations are drawn at five *knots*, a small number of anchor points in time, and interpolated
smoothly between them, so each batch's schedule is a gentle wander rather than a step change.

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

The batches come from three feed classes (in this plant's story: three supplier or campaign
combinations, labelled A, B and C, with 81, 71 and 48 batches in the training campaign). The
classes do not form separated clusters; they occupy overlapping ranges along the first score
direction, which orders the batches from favourable to unfavourable incoming material. Assigning
a batch to the nearest class centroid in the standardised |Z| variables recovers its label 85% of
the time, and when it misses, it assigns the neighbouring range. One prediction model is fitted
per class:

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

The reason for one model per feed class, rather than one global model, deserves stating, because
the global alternative was tried first and failed. A single global model fitted on all 200
batches predicts final titer acceptably. Used for *control*, however, its corrections moved some
batches in a direction that lowered their executed titer. The cause is the interaction that
:ref:`the variance decomposition <APPS_batch_monitoring_variance>` reported: the effect of a
schedule change depends on the feed class. Holding the reactor warm in mid-batch rescues a
slow-growing batch from a poor feed lot, and wastes productive time for a fast-growing one. A
single linear model has one gain direction to offer every batch, so it averages the two cases and
misdirects both. Fitting the model within a class range makes the gain locally right. The three
fits above reach :math:`R^2` values of 0.81, 0.90 and 0.94 on their own classes.

**Three kinds of column at a decision point.** With a fitted model, predicting a *running* batch
is a missing data problem. Call the moment at which the prediction is made, and at which an
adjustment could be applied, a **decision point**. The lower row of :ref:`the layout figure
<APPS_batch_monitoring_row>` shows the state of the unfolded row at the day-4 decision point,
when 8 of the 20 samples have been recorded. The |Z| values and the first 8 samples of every tag
are *known*. The remaining samples of the three responding tags (dissolved oxygen, offgas carbon
dioxide, volume) are *missing*, and are estimated by the model. The remaining samples of pH and
temperature, the two manipulated tags, are neither: they are the schedule under consideration.
For the question "what happens if nothing is changed?" they are set to the planned remaining
schedule, and for the correction they become the decision variables. Flores-Cerrillo and
MacGregor set the prediction up this way, and the implementation here follows them.

**Estimating the scores of a partial row.** A complete row's scores are a fixed linear
combination of its 111 columns, given by the model's weights. For a partial row the same
combination cannot be formed. The simplest estimate, the *trimmed score*
:math:`\boldsymbol{\tau}`, applies the combination to the known columns and leaves the missing
ones out; it is biased, because the missing columns' contributions are simply absent. *Trimmed
score regression* (Arteaga and Ferrer) corrects the trimmed score with a regression from trimmed
scores to true scores whose coefficients follow from the model's own loadings and score variances,
:math:`\hat{\mathbf{t}} = \mathbf{B}_k \boldsymbol{\tau}`, where the matrix :math:`\mathbf{B}_k`
depends only on which columns are known at decision point :math:`k`. García-Muñoz, Kourti and
MacGregor compared the available estimators on exactly this batch-so-far problem and found two of
them best, giving almost identical predictions: conditional mean replacement, and trimmed score
regression. The package implements the latter as ``PLS.project``, and the higher level functions
below use it. Two properties of the estimate carry the rest of this page:

- For a fixed pattern of known and unknown columns, the score estimate is a *fixed linear
  function* of the known columns, and therefore of the future setpoint columns. That is what
  turns the correction, later, into a small convex program.
- The regression inverts a small matrix built from the loadings of the known columns. When few
  columns are known, that matrix can be nearly singular, and its *condition number* (the ratio of
  its largest to its smallest scaling) says how much the estimate amplifies noise. A large
  condition number means the estimate at that decision point is not trustworthy, whatever the
  batch looks like. The package reports it with every projection.

**The prediction interval at a decision point.** The predicted titer is
:math:`\hat{y} = \mathbf{c}^T \hat{\mathbf{t}}`, with :math:`\mathbf{c}` the model's quality
loadings. Its uncertainty is not the model's uncertainty on complete rows: early in the batch the
score estimate rests on few columns and is far less certain than at the end. The interval used
here carries that. At decision point :math:`k`, the :math:`N` training batches are re-projected
under the same pattern of known columns, their predicted titers are compared with their measured
ones, and the resulting error :math:`s_k` replaces the full-row training error. The half-width is

.. math::

	\text{half-width}_k = t_{N-A-1} \; s_k \; \sqrt{1 + \frac{1}{N} + \frac{T^2_k}{N-1}}

where :math:`t_{N-A-1}` is the Student's t quantile for the confidence level, :math:`A` is the
number of components, and :math:`T^2_k` is Hotelling's :math:`T^2` of the estimated scores
(:ref:`their distance from the centre of the training data within the model plane
<LVM-Hotellings-T2>`), computed against the covariance of the training batches' score estimates
under the same pattern, as García-Muñoz, Kourti and MacGregor build their time-varying limits.
The SPE limit that later gates the correction is built the same way, from the training batches'
SPE under the pattern of known columns. The table gives :math:`s_k` for the three class models at
selected decision days, with the condition number of class A's estimator in parentheses.

============  ==============  ============  ============
Decision day  Class A [g/L]   Class B       Class C
============  ==============  ============  ============
1             10.9 (3 858)    2.35          2.15
2             211 (777 561)   2.37          1.56
3             17.1 (5 254)    2.36          0.92
4             3.15 (306)      1.22          0.85
5             1.11 (13)       0.99          0.72
6             1.04 (5)        1.03          0.79
8             0.71 (3)        0.81          0.55
10            0.58 (1)        0.52          0.43
============  ==============  ============  ============

Two things stand out. The error falls as the batch runs, by a factor of four or five between the
first day and the last for every class, which is the funnel a monitoring scheme should show. And
class A's model cannot be asked before day 4: its estimator is ill-conditioned, with a condition
number near :math:`8 \times 10^5` at day 2 against a few hundred from day 4 onward, and the
corresponding error of 211 g/L on a titer of 8 g/L says the projection is meaningless there. The
plain training error of the same model, on complete rows, is 0.56 g/L. An interval built from
that number would have declared the day-2 projections precise; the interval built at the decision
point does not.

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

.. _APPS_batch_monitoring_funnel:

.. figure:: ../figures/batch/mcc-monitoring-funnel.png
	:source: batch/midcourse-correction-figures.py
	:alt: Predicted final titer of one poor batch at every decision point with its prediction interval; the prediction sits near 3.2 grams per litre from the first day, the interval narrows from plus or minus 4 grams per litre at day 0.5 to plus or minus 1.75 at day 4, and the whole interval lies below the 8 grams per litre target from day 2.5 on.
	:width: 900px
	:scale: 80
	:align: center

This batch is headed for roughly 3.2 g/L against a target of 8 g/L, drawn across the figure as a
floor the plant would like every batch to clear (it is essentially the titer the nominal schedule
delivers when no disturbance acts, the 8.01 g/L reference measured earlier). The shortfall is
visible in the batch's own data from the first day: the poor feed lot shows in |Z| immediately,
and the slow growth it causes shows in the gas trajectories soon after. What the first days cannot
yet say is how sure that reading is. At day 0.5 the interval is ±4.0 g/L wide and reaches the
floor; by day 2.5 it has narrowed to ±2.0 g/L and its upper end has dropped below the floor; at
day 4 the interval is ±1.75 g/L and its upper end sits at 5.0 g/L, three grams below the floor.
The SPE of the batch so far stays under its limit throughout (4.8 against a limit of 7.2 at
day 4), so the model recognises this batch as one of the family it was built from. Knowing this
on day 4, what should the remaining six days of the schedule be?

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
	            checks.append({"day": k / 2, "error": float(p.y_hat.iloc[0]) - run.titer,
	                           "covered": abs(float(p.y_hat.iloc[0]) - run.titer) <= float(p.half_width.iloc[0])})
	checks = pd.DataFrame(checks)
	summary = checks.groupby("day").agg(rmsep=("error", lambda e: float(np.sqrt(np.mean(e**2)))),
	                                     bias=("error", "mean"), coverage=("covered", "mean"))
	print(summary.round(2))

============  ===============  ============  ===============
Decision day  RMSEP [g/L]      Bias [g/L]    Coverage (95%)
============  ===============  ============  ===============
1             2.61             -0.30         0.95
2             53.6             -15.1         0.97
3             5.40             2.03          0.98
4             0.96             -0.04         1.00
5             0.91             -0.44         0.95
6             1.02             -0.48         0.90
8             0.90             -0.57         0.85
9             0.87             -0.64         0.80
============  ===============  ============  ===============

The prediction becomes usable at day 4, where its root mean square error over the 40 batches is
0.96 g/L against a batch-to-batch standard deviation of 1.20 g/L, and stays there. Before day 4
the error is dominated by the class A batches whose estimator the table of :math:`s_k` showed to
be ill-conditioned: at day 2 one batch that finished at 8.2 g/L is projected at -139 g/L. The
interval knows this. Its coverage is at or above the nominal 95% on every day up to day 5, so
those absurd projections come with intervals wide enough to say they mean nothing, which is what
the dead band in the next section relies on. Later in the batch the interval becomes optimistic:
the model under-predicts the replay batches by about 0.5 g/L from day 5 on, and coverage falls to
80% by day 9. The training campaign's mean titer is 5.99 g/L, well below the replay mean of
7.57 g/L, because deliberate perturbations of a good recipe mostly cost titer; the nominal
schedule therefore lies toward the edge of the region the model was fitted on, and a model
extrapolating slightly acquires a bias. A plant would see the same effect in this check, and it
is one of the reasons the decision point should not be placed late.

Correcting mid-course
~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: mid-course correction
	pair: batch processes; control

The idea of a mid-course correction predates its latent variable form: Yabuki and MacGregor
formulated it for semi-batch reactors in 1997, predicting the final properties from on-line
measurements plus a few off-line samples, and correcting only when that prediction fell outside a
defined no-control region. Flores-Cerrillo and MacGregor gave it the latent variable form used
here in 2004. At each decision point the procedure is:

1. **Predict.** Estimate the final quality from |Z|, the samples so far and the planned remaining
   schedule, with its interval at this decision point, as in the previous section.
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
correlation structure automatically, but has no way to express an actuator limit; optimising the
columns states the engineering limits exactly, but has to add the terms that hold the answer
inside the model's region. Written in the setpoint columns, with :math:`\mathbf{u}` the future
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
figure <APPS_batch_monitoring_funnel>`. The correctors below extend the predictors with the
settings the decision needs: the target (8 g/L, treated as a floor, so batches predicted at or
above it are never touched), the dead band (1.0 half-widths: the whole interval must fall short),
the weights, the actuator bounds (tightened inward by about two control-error standard
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
	        weights={"target": 1.0, "movement": 0.1},
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
	:alt: Nominal and corrected temperature and pH schedules for the poor batch; the corrected schedule delays the downshift, holding the reactor warmer through day seven, and the executed titer rises from 3.66 to 5.79 grams per litre.
	:width: 900px
	:scale: 80
	:align: center

The printed decision reads: corrected; predicted 3.24 ± 1.75 g/L if nothing changes, 2.7
half-widths below the floor; SPE so far 4.84 against a limit of 7.22. Every gate passed. The
optimiser then found a schedule the model predicts at 5.04 g/L, with the candidate row's SPE at
6.3 against a cap of 9.1 and its :math:`T^2` at 1.0 against a cap of 11.3: neither cap was
active, nor any bound or rate limit, so the answer is the unconstrained optimum of the penalised
program, well inside the region the history covers.

The nominal schedule drops from the warm growth phase to the 29 °C production hold between days
3.5 and 4.5. The corrected schedule does not complete that drop on time: it holds at 34.7 °C at
day 4 and descends by about 1.1 °C per half-day, reaching the production hold only around day
7.5, with a small transient pH dip to 6.95 at day 4 that returns to nominal by day 6.5. The
physical reading is direct. This batch's poor feed lot made it grow slowly, so at day 4 it has not
yet built the biomass the production phase needs; cooling it on the nominal timetable would arrest
growth at a low cell density. The correction gives the batch more growing time. No such rule was
programmed anywhere: the behaviour emerges from a regression on historical batches whose schedules
were deliberately varied.

Executed with the identical disturbance history, the batch finishes at 5.79 g/L instead of
3.66 g/L, a 58% improvement on this single batch. The model predicted 5.04 g/L for the corrected
schedule: a latent variable prediction regresses toward the mean, so it *understated* the gain its
own correction delivered. The distinction between a predicted and an executed gain is worth
keeping in view. Simulation studies can execute their corrections, and do: Flores-Cerrillo and
MacGregor obtained the final qualities in their nylon case study by rerunning the non-linear
simulation model with the trajectories the controller had computed. On an operating plant that
step is not available, so results from industrial case studies are reported as model predictions.
On this page the simulator makes execution cheap, so every gain from here on is an executed one.

.. _APPS_batch_monitoring_campaign:

Does it work on the whole campaign?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One rescued batch is an anecdote. The test that matters runs many fresh batches through the full
procedure (predict at the decision point; check the model applies; apply the dead band; correct
when warranted; execute) and compares against the alternatives on the same batches with the same
disturbances. The package wraps that comparison, including two reference policies that bracket
what is achievable. The wrapper rebuilds the same pipeline assembled by hand above (the same
master seed, the same 200 training batches, the same per-class models, and correctors with the
settings listed above, correcting at day 4), so its corrected row is the configured procedure
measured on the same 40 test batches:

.. code-block:: python

	result = evaluate_control_policies(simulator, y_target=8.0, random_state=0)   # about 7 minutes
	print(result.summary.round(3))
	print(f"{result.n_corrected} corrected, {result.n_harmed} harmed")

============================  ==========  ========  =========  =========
Policy                        Mean [g/L]  Sd [g/L]  Min [g/L]  Max [g/L]
============================  ==========  ========  =========  =========
Replay (do nothing)           7.507       1.198     3.655      8.925
Mid-course correction         7.746       0.782     5.717      8.925
Oracle from the same day      7.866       0.626     6.108      8.925
Adapted (feedforward)         7.824       1.013     4.573      9.309
============================  ==========  ========  =========  =========

All four rows are executed titers over the same 40 fresh batches. Reading them one at a time:

- **Replay** is the golden batch policy: every batch runs the nominal schedule. Its spread is the
  cost of doing nothing.
- **Mid-course correction** corrected 5 of the 40 batches, all from the poorest feed class; the
  dead band left 34 alone and the SPE validity gate stopped one. Each corrected batch improved,
  by +1.48 to +2.67 g/L, and no batch was made worse. The campaign mean rises 0.24 g/L, and the
  standard deviation falls from 1.198 to 0.782 g/L, a 35% reduction. The policy acts on the low
  tail, where the largest losses are: the lowest replay batch (3.655 g/L, the single-batch
  demonstration) rises to 5.79 g/L, and the lowest batch in the whole corrected campaign finishes
  at 5.717 g/L. One of the five shows the dead band at its edge. Its no-change prediction was
  6.2 g/L with an interval whose upper end sat just under the floor, so it was corrected; it
  actually stood at 7.0 g/L, and the correction still raised it to 8.5 g/L. The model predicted
  5.0 to 6.9 g/L for the five corrected schedules; executed, they finished at 5.7 to 8.5 g/L, so
  the model understated four of its five gains and overstated the fifth by 0.1 g/L.
- **Oracle from the same day** answers "how much was achievable at that decision point at all?"
  For each corrected batch, the remaining schedule is optimised against the *simulator itself*
  (the true process), from the same day-4 state, with the same seed. No data-driven method can
  beat this row from the same starting point. The mid-course policy captured 67% of
  the oracle's mean improvement; the remainder is what is lost by steering with a regression
  restricted to the region its history explored, rather than with the true process equations.
- **Adapted (feedforward)** runs *every* batch on the true optimal schedule for its own measured
  |Z|, computed before the batch starts: perfect feedforward adaptation, again a ceiling rather
  than an implementable policy. It raises the mean and the best batches (its maximum, 9.31 g/L,
  is the table's highest), but its *minimum is worse than the corrected policy's*: 4.57 against
  5.72 g/L. A schedule fixed at time zero, however well chosen, cannot answer a
  disturbance that develops during the batch. :ref:`The variance decomposition
  <APPS_batch_monitoring_variance>` showed the outcome variance has a before-batch share and a
  during-batch share; the adapted row addresses the first, the mid-course row the second, and
  neither substitutes for the other.

.. figure:: ../figures/batch/mcc-policy-comparison.png
	:source: batch/midcourse-correction-figures.py
	:alt: Left panel: the corrected batches each jump by more than a gram per litre. Right panel: all forty batches under the four executed policies; correction removes the low tail.
	:width: 900px
	:scale: 80
	:align: center

.. _APPS_batch_monitoring_window:

Where to put the decision point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`The campaign comparison <APPS_batch_monitoring_campaign>` used a single decision point at
day 4 of 10. That choice matters. Sweeping it re-runs that whole executed comparison at each
decision day, changing only the ``decision_points`` argument of ``evaluate_control_policies``,
and shows a window:

============  ===========  =================  ==============================
Decision day  Corrected    Of which harmed    Mean gain, corrected batches
============  ===========  =================  ==============================
2             5            1                  +0.93 g/L
3             6            0                  +1.46 g/L
4             5            0                  +1.92 g/L
5             7            0                  +0.63 g/L
6             8            8                  -0.09 g/L
7             8            8                  -0.28 g/L
============  ===========  =================  ==============================

.. figure:: ../figures/batch/mcc-decision-point-window.png
	:source: batch/midcourse-correction-figures.py
	:alt: Mean executed gain of the corrected batches versus the decision day, rising to a peak around day four and falling from day six.
	:width: 900px
	:scale: 80
	:align: center

The two ends of the window are limited by different things. Early in the batch the prediction
cannot yet be trusted, as :ref:`the held-out check <APPS_batch_monitoring_funnel>` measured. The
interval carries that: the class A batches, whose projections are meaningless at day 2, arrive
with intervals hundreds of grams per litre wide, so the dead band never lets them through, and
what it does let through at day 2 is a smaller set of clearer shortfalls whose mean gain is half
of day 4's, with one batch harmed. By day 3 the estimators are conditioned well enough that none
of the six corrections harms its batch. Late in the batch the prediction is at its most accurate,
but the remaining schedule no longer has the leverage to act on it: the growth phase is over, and
what is left to act on is mostly model error, so every correction does slight damage. On this
process the window is days 3 to 5, with the largest gain at day 4: late enough that a struggling
batch has revealed itself in the gas trajectories, early enough that the growth phase can still
be extended. The window's location is a property of the process, not of the method; finding it
needs the held-out prediction check, process knowledge of where the leverage lies, and, where a
simulator exists, a sweep like this one.

How far should the model be trusted?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :math:`T^2` and SPE penalties and caps are the settings that keep the optimiser inside the
region the historical data supports, and they raise a sharper question: how far outside that
region should the optimiser be allowed to move? Relaxing the :math:`T^2` penalty (with the hard
caps removed) and re-running the executed comparison at each setting measures the answer for this
process:

.. figure:: ../figures/batch/mcc-exploration-dial.png
	:source: batch/midcourse-correction-figures.py
	:alt: Predicted and executed mean titers of the corrected batches as the T-squared penalty relaxes; both rise as the optimiser is freed, and the executed line sits above the predicted line throughout.
	:width: 900px
	:scale: 80
	:align: center

On this process, at this decision point, freeing the optimiser helped monotonically. The executed
mean titer of the five corrected batches rises from 6.30 g/L at the most conservative setting to
6.98 g/L with the penalty removed, each step of extra freedom produced a real improvement, and
the executed titer sat *above* the model's own prediction at every setting (the prediction rises
from 5.51 to 5.97 g/L over the same range). The reason is where the poorest class's best
schedule sits. It is not outside
the actuator range, which the training campaigns already span. It is an unusual *combination* of
setpoints: a warm hold carried well past the day the nominal recipe cools, which few training
batches did. That is exactly what :math:`T^2` measures, distance from the centre of the training
data within the model plane, so penalising :math:`T^2` holds the correction back from a schedule
that is physically available and, for these batches, better.

This does not show that the constraints are unnecessary. The same freedom, at the late decision
points in :ref:`the decision-day sweep <APPS_batch_monitoring_window>`, is what made corrections
harmful: there the model's apparent leverage was error, and the constraints are what would have
contained it. Taken together, the two figures show the trade-off: the validity limits exchange
reachable improvement for protection from model error, the balance depends on where the process's
true optimum sits relative to the explored region, and the balance can be *measured*, on batches
the model has never seen, before the scheme is trusted in production.

.. _APPS_batch_monitoring_procedure:

Applying it on a plant
~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: mid-course correction; procedure

Everything above was done on a simulator, where a corrected batch can be executed and its gain
measured. A plant cannot execute the counterfactual, so the procedure has to be arranged so that
each step is checked with what a plant *can* measure before the next step is trusted.

1. **Establish the case.** Work through the :ref:`four conditions
   <APPS_batch_monitoring_when>` on the plant's own records: the quality spread against the
   setpoint spread; the |Z|-only regression and its :math:`Q^2`; the manipulated variables that
   keep their leverage after the point where a shortfall becomes visible; and whether the history
   contains schedule variation in the shapes a correction would use. If it does not, plan the
   designed campaign that supplies it before going further.

2. **Assemble and align the data.** One row per batch: |Z|, the aligned trajectories of every
   tag, the final quality. Decide what the target means for this product: a floor (more is
   better, corrections act only on shortfalls), a ceiling, or a specification to be hit from
   both sides. That decision sets the dead band's direction.

3. **Fit and validate the prediction layer.** Fit the batchwise-unfolded PLS model on the
   historical campaign, with cross-validation choosing the number of components. Then run the
   held-out prediction check at every candidate decision point, on batches the model was not
   fitted on: the error, the bias and the interval coverage by decision day, as in :ref:`the
   held-out table <APPS_batch_monitoring_funnel>`, together with the condition number of the
   estimator. This check decides two things at once: the earliest decision point at which the
   prediction can be trusted, and whether the interval is calibrated there, which the dead band
   depends on. If the model predicts acceptably but its gain direction is suspect (an executed
   correction on the simulator helped one group and hurt another; on a plant, the sign of the
   schedule's effect differing between groups of batches in the history), fit local models, per
   feed class, grade or product, as this page did.

4. **Choose the decision points.** The prediction check says when the batch can be *seen*;
   process knowledge, and a sweep where a simulator exists, says when it can still be *steered*.
   The decision point goes where both hold. Two decision points sufficed in Flores-Cerrillo and
   MacGregor's nylon study; one sufficed here.

5. **Set the correction's constraints.** Actuator bounds tightened inward by about two
   control-error standard deviations, rate limits the control loops can follow, a knot
   parameterisation as smooth as the schedules the plant runs, and the SPE and :math:`T^2` caps
   at the limits computed for the decision point. Start conservative on the trust dial: the
   exploration figure was measured against the true process, which a plant cannot do.

6. **Validate what can be validated offline.** The prediction layer has been validated in
   step 3. The correction's *gain* cannot be validated on history, because no historical batch
   was run twice. What can be checked is consistency: for the historical batches that did carry
   schedule moves, whether the model's predicted effect of those moves agrees in sign and
   rough size with what those batches did compared with their neighbours. Disagreement here is
   the identification requirement failing, and more excitation data is the remedy.

7. **Deploy in stages, and keep the calibration record.** Begin with the dead band and caps at
   their conservative settings, so only the clearest shortfalls are corrected. For every corrected
   batch record three numbers: the no-change prediction at the decision point, the predicted
   outcome of the corrected schedule, and the realised outcome. The first two are the model's
   claim; the third is the plant's answer. Over time the predicted-versus-realised record is the
   plant's own version of :ref:`the exploration figure <APPS_batch_monitoring_window>`, and it
   is the evidence for loosening the settings, or for not doing so. The no-change prediction is
   also the closest thing a plant has to the counterfactual: a corrected batch that lands where
   its no-change prediction said it would have landed is a correction that did nothing.

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

The methods on this page are implemented in `process_improve
<https://github.com/kgdunn/process-improve>`_ (``BatchPLS``, ``PLS.project``,
``MidCourseCorrector`` with its ``predict`` and ``correct`` methods, and
``evaluate_control_policies``, with the simulator in ``process_improve.simulation``); the figure
sources carry the exact seeds, so every number on this page can be regenerated.

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
  `<https://doi.org/10.1002/cem.750>`_ The source of trimmed score regression.
* Salvador García-Muñoz, Theodora Kourti and John F. MacGregor, "`Model predictive monitoring for
  batch processes
  <https://literature.learnche.org/item/157/model-predictive-monitoring-for-batch-processes>`_",
  *Industrial and Engineering Chemistry Research*, **43**, 5929-5941, 2004.
  `<https://doi.org/10.1021/ie034020w>`_ The comparison of score estimators for a partially
  observed batch, and the time-varying limits built from the training batches re-projected at
  each time.

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
