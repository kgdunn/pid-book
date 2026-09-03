.. _APPS_batch_case_dupont:

Learning from batch trajectories: the DuPont polymerization reactor
=====================================================================

.. index::
	single: batch data; DuPont polymerization case study
	pair: batch PCA; outlier diagnosis
	pair: contribution plots; batch trajectories
	single: observability; batch data

This is the first of three case studies on batch data. A principal component model of the
batch trajectories is used to find the batches that differ from the rest, to name the
variables and the time in the batch at which they differ, and to show what such a model
cannot detect. The :ref:`second case study <APPS_batch_case_sbr>` adds a block of final
quality measurements and uses a PLS model; the :ref:`third <APPS_batch_case_fmc>` combines
several blocks of information about each batch in a multiblock model. All three follow the
same pattern: plot the raw trajectories, build a model with a small number of components,
examine the batches the model singles out, and confirm every finding in the raw data.

Nylon is made in an industrial batch polymerization reactor in two stages. In the first
stage, of about one hour, the ingredients are charged, the flows of the heating medium are
adjusted to control the pressure and the rate of temperature change, and the solvent that
conveyed the ingredients into the reactor is vaporized and removed. In the second stage the
ingredients react to the final polymer under a controlled pressure and temperature ramp, and
the batch ends when the polymer is pumped out of the vessel. A critical quality property of
the batch is measured in the laboratory about 12 hours after the batch has ended. Nothing
measured during a batch can therefore be used to correct that batch, and the disposition of
a batch is known only after the next few batches have started.

What the plant does record is the trajectory of ten process measurements over every batch:
three reactor temperatures, three pressures, two flow rates of material added to the
reactor, and the temperatures of the heating and of the cooling medium. The data are the
worked example of Nomikos and MacGregor (1995), supplied by DuPont: 55 batches, each already
aligned to 100 equal time intervals, with the values scaled for confidentiality. From the
laboratory records, batches 40, 41, 42, 50, 51, 53, 54 and 55 had a final quality well
outside the acceptable limit, and batches 38, 45, 46, 49 and 52 were above or very close to
it. That list is not used to build the model. It is kept aside and compared with what the
trajectories reveal on their own.

The data
~~~~~~~~

The `polymerization dataset <https://openmv.net/info/polymerization>`_ is a single table of
5500 rows, one per aligned sample of every batch, with a batch identifier and a time index.
The ``load_dupont`` function in the ``process_improve`` package downloads the table and
returns a dictionary with one data frame per batch, 100 samples by 10 tags.

.. code-block:: python

	import pandas as pd
	import plotly.graph_objects as go
	from process_improve.batch import BatchPCA, load_dupont, time_varying_loading_plot, unfolded_contribution_plot

	batches = load_dupont()                    # https://openmv.net/file/polymerization.csv
	first = next(iter(batches.values()))
	print(len(batches), "batches;", first.shape[0], "samples per batch;", list(first.columns))

Plotting one tag for every batch, with a few batches drawn on top in colour, is the first
check. The trajectories overlay well, which confirms that the alignment has already been
done, and a few batches are visibly unusual in the cooling-medium temperature ``TempC-1``
and in ``Press-1``. The two flow rates are noisy in every batch. A plot per tag cannot,
however, rank 55 batches on ten variables at once; that is what the model is for.

.. code-block:: python

	GREY, ORANGE, BLUE = "#c8c8c8", "#c55a11", "#1f3d7a"       # figure colours, reused below

	def overlay(batches, tag, highlight):
	    """One tag for every batch in grey, with the batches in `highlight` (id -> colour) drawn on top."""
	    fig = go.Figure()
	    for batch_id, batch in batches.items():
	        if batch_id not in highlight:
	            fig.add_trace(go.Scatter(y=batch[tag], mode="lines", line=dict(color=GREY, width=1), showlegend=False))
	    for batch_id, colour in highlight.items():
	        fig.add_trace(go.Scatter(y=batches[batch_id][tag], mode="lines", name=f"batch {batch_id}",
	                                 line=dict(color=colour, width=3)))
	    fig.update_layout(title=tag, xaxis_title="Sample [aligned time]", height=320)
	    return fig

	for tag in ("TempC-1", "Press-1", "Flow-1", "TempR-1"):
	    overlay(batches, tag, {49: ORANGE, 54: BLUE}).show()

.. figure:: ../figures/batch/batch-case-dupont-raw-trajectories.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Four tags of the 55 batches overlaid in grey with batch 49 in orange and batch 54 in blue; the cooling-medium temperature of batch 49 falls below the others after sample 60, and the pressure step of batch 54 comes later than in the other batches.
	:width: 900px
	:scale: 80
	:align: center

	Four of the ten tags for all 55 batches (grey), with batch 49 (orange) and batch 54
	(blue) drawn on top. The cooling-medium temperature of batch 49 falls away from the
	other batches after sample 60. The pressure step of batch 54 in ``Press-1`` comes later
	than in the other batches, and its reactor temperature ``TempR-1`` runs slightly below
	them over the first 20 samples.

A first model on all 55 batches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``BatchPCA`` class unfolds the batches batchwise, so that each batch becomes one row of
10 tags times 100 samples, 1000 columns in all. Every column is then centred and scaled to
unit variance, the :ref:`preprocessing <LVM_preprocessing>` used for any PCA model.
Centring removes the average trajectory of each tag, and scaling gives every (tag, time)
cell the same weight, so the components describe how the batches deviate from the average
batch. The first model, called model A on this page, uses two components and all 55
batches. The aim is not a final model, but a first look at which batches stand out.

.. code-block:: python

	model_a = BatchPCA(n_components=2).fit(batches)
	print("R2 per component:", model_a.r2_per_component_.round(3).tolist())
	print("R2 cumulative:", model_a.r2_cumulative_.round(3).tolist())
	model_a.score_plot(settings={"show_labels": True}).show()
	model_a.spe_plot(settings={"show_labels": True}).show()
	spe = model_a.spe_.iloc[:, -1]                          # SPE of every batch after the second component
	print(f"largest SPE: batch {spe.idxmax()} ({spe.max():.1f} against the 95% limit {model_a.spe_limit(conf_level=0.95):.1f})")

The two components explain 38.3% and 17.6% of the variance in the unfolded matrix, 55.9%
together. Two plots are enough to find the batches that differ.

.. figure:: ../figures/batch/batch-case-dupont-model-a-scores.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Score plot of model A with the 95% confidence ellipse; batches 50 to 55 lie far outside the ellipse and batch 49 sits near the origin among the other batches.
	:width: 600px
	:scale: 80
	:align: center

	Score plot of model A. Batches 50 to 55 (aqua) lie outside the 95% confidence ellipse,
	far from the other batches. Batch 49 (orange) sits among the normal batches.

The :ref:`score plot <LVM_interpreting_scores>` shows batches 50 to 55 far from the rest and
outside the 95% confidence ellipse. Batches this far out pull the components towards
themselves, so the model will have to be rebuilt without them once they have been
examined. The :ref:`SPE plot <LVM-interpreting-SPE-residuals>` flags a different batch, 49,
which sits in the score plot among the normal batches.

.. figure:: ../figures/batch/batch-case-dupont-model-a-spe.png
	:source: batch/batch-case-dupont-figures.py
	:alt: SPE of every batch after two components with the 95% limit; batch 49 has the largest value, and batch 51 is also above the limit.
	:width: 900px
	:scale: 80
	:align: center

	SPE of every batch after two components, with the 95% limit. Batch 49 (orange) has the
	largest SPE, 39.3 against a limit of 29.1; batch 51 is also above the limit.

Batch 49 has the largest SPE of all batches, 39.3 against a 95% limit of 29.1. Its problem
is not a large deviation along the main directions of variation, which is what the scores
measure, but a break in the correlation structure that the two components describe. The
scores and the SPE answer different questions, and both plots are needed.

Batch 49: which variables, and when
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The raw data are ambiguous about batch 49. ``Flow-1`` looks suspicious in the overlay, but
it is a noisy tag in every batch. The SPE :ref:`contributions <LVM_contribution_plots>`
settle the question. For a batch model the contribution vector has one entry per
(tag, time) cell, 1000 entries here: the residual of that cell after the two-component
reconstruction. ``process_improve`` reports the SPE of a batch as the length of its
residual vector, so the squared residuals of the cells add up to the squared SPE, and each
squared residual, divided by that total, is the share of the SPE carried by the cell.
Summing the shares per tag ranks the variables, and summing them per time sample locates
the event in the batch. ``unfolded_contribution_plot`` draws the full vector of 1000 bars
grouped by tag and, with ``by_tag=True``, the sum per tag.

.. code-block:: python

	scaled = model_a.unfold_and_scale(batches)                  # the 55 x 1000 matrix the model was fitted on
	squared = model_a.spe_contributions(scaled) ** 2            # squared residual of every cell; a row sums to SPE squared
	spe_share = squared.div(squared.sum(axis=1), axis=0) * 100  # ... as a percentage of that batch's total
	unfolded_contribution_plot(spe_share, batch_id=49).show()
	unfolded_contribution_plot(spe_share, batch_id=49, by_tag=True).show()
	by_time = spe_share.loc[49].groupby(level="sequence").sum()
	fig = go.Figure(go.Bar(x=by_time.index, y=by_time.values, marker_color=BLUE))
	fig.update_layout(title="Batch 49: share of the SPE per time sample", xaxis_title="Sample [aligned time]",
	                  yaxis_title="Share of SPE [%]", height=320)
	fig.show()
	print("share per tag [%]:", spe_share.loc[49].groupby(level="tag", sort=False).sum().round(0).to_dict())
	print("samples with the seven largest shares:", sorted(by_time.nlargest(7).index.tolist()))
	print(f"share of samples 55 to 65: {by_time.loc[55:65].sum():.0f}%")

.. figure:: ../figures/batch/batch-case-dupont-batch-49-spe-contributions.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Three panels for batch 49: the share of the SPE carried by each of the 1000 unfolded cells, grouped by tag; the shares summed per tag, led by TempC-1, Flow-2 and Press-2; and the shares summed per sample, a single narrow peak between samples 55 and 65.
	:width: 800px
	:scale: 80
	:align: center

	Share of the SPE of batch 49 carried by each (tag, time) cell (top), summed per tag
	(middle) and summed per sample (bottom). The residual is concentrated in a single
	window, samples 55 to 65, and in the heating- and cooling-medium temperatures, the
	pressures and ``Flow-2``.

``Flow-1`` carries 3% of the residual. The residual belongs to the cooling-medium
temperature (19%), ``Flow-2`` (18%), ``Press-2`` (15%), the heating-medium temperature
(14%) and ``Press-3`` (12%), and it is concentrated in a short window. The seven samples
with the largest shares are samples 57 to 63, and the eleven samples from 55 to 65 together
carry 80% of the total. A short disturbance in the heating, cooling and pressure systems
during that stretch of the batch broke the usual relationship between these tags. Nomikos
and MacGregor report that the final quality of batch 49 was barely acceptable, which is
consistent with a short event rather than a batch that was wrong throughout. In the raw
data the cooling-medium temperature of batch 49 does fall away from the other batches after
sample 60, a change that is easy to pass over until the contributions point at it.

The score outliers: batches 50 to 55
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Batches 50 to 55 are far out along the components, so the tool for them is the score
contribution: how much every (tag, time) cell contributes to :math:`t_1` or :math:`t_2`.
A score is the sum over the 1000 cells of the scaled value times the loading,
:math:`t_1 = \sum_k x_k p_{k,1}`, so a cell contributes strongly when its value is far from
average in the direction of the loading. The :ref:`loading <LVM_interpreting_loadings>`
:math:`\mathbf{p}_1` of a batch model has 1000 entries as well, and
``time_varying_loading_plot`` draws it as ten curves over the batch, one per tag, which
shows which parts of the batch the component describes.

.. code-block:: python

	time_varying_loading_plot(model_a, component=1).show()
	t1 = model_a.score_contributions(scaled, component=1)      # one contribution per cell; a row sums to t1
	unfolded_contribution_plot(t1, batch_id=54).show()
	unfolded_contribution_plot(t1, batch_id=54, by_tag=True).show()
	print("batch 54, t1 contributions per tag:", t1.loc[54].groupby(level="tag", sort=False).sum().round(1).to_dict())

.. figure:: ../figures/batch/batch-case-dupont-loadings-p1.png
	:source: batch/batch-case-dupont-figures.py
	:alt: The first loading of model A drawn over the batch, one panel per tag; most tags have loadings of both signs within the batch.
	:width: 1000px
	:scale: 80
	:align: center

	Loading :math:`\mathbf{p}_1` of model A over the batch, one panel per tag. Most tags
	have loadings of both signs within the batch, so the component describes a change in
	the shape of the trajectories rather than a uniform offset.

.. figure:: ../figures/batch/batch-case-dupont-batch-54-t1-contributions.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Three panels for batch 54: contributions to t1 of each unfolded cell, all positive; the sum per tag, between 4.6 and 8.7 for every tag; and the sum per sample, positive over the whole batch.
	:width: 800px
	:scale: 80
	:align: center

	Score contributions to :math:`t_1` of batch 54: every tag contributes in the same
	direction, and the contribution per sample stays positive over the whole batch.

Batch 54 has a high :math:`t_1` because every tag contributes in the same direction,
between 4.6 and 8.7 per tag, and the contribution per sample is positive from the first
sample to the last. The whole batch ran away from the average trajectory. The raw overlay
confirms it: in ``Press-1`` the pressure step of batch 54 and its later descent come later
than in the other batches, and its reactor temperature runs below them over the first 20
samples. Batches 50 and 52 also have large positive :math:`t_1` values and can be examined
in the same way. Batch 55, which has the highest :math:`t_2`, stands out through the
pressures ``Press-3`` and ``Press-2`` and the cooling-medium temperature.

Exclude and rebuild: a second group of batches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A reference model must describe normal operation. Batches 49 to 55 are therefore removed,
and a second model, model B, is fitted to the remaining 48 batches with three components.
Removing batches changes the model, so the plots are examined again.

.. code-block:: python

	kept_b = {batch_id: batch for batch_id, batch in batches.items() if batch_id < 49}
	model_b = BatchPCA(n_components=3).fit(kept_b)
	print("R2 per component:", model_b.r2_per_component_.round(3).tolist())
	model_b.score_plot(pc_horiz=2, pc_vert=3, settings={"show_labels": True}).show()
	t3 = model_b.score_contributions(model_b.unfold_and_scale(kept_b), component=3)
	unfolded_contribution_plot(t3, batch_id=39, by_tag=True).show()
	second_group = [37, 39, 43, 44, 45, 46, 47, 48]
	overlay(batches, "Press-3", {**{batch_id: ORANGE for batch_id in second_group}, 39: BLUE}).show()

.. figure:: ../figures/batch/batch-case-dupont-model-b-scores.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Scores of model B on components 2 and 3; batches 37, 39 and 43 to 48 form a group at the top right, away from the main cloud.
	:width: 600px
	:scale: 80
	:align: center

	Scores of model B on components 2 and 3. Batches 37, 39 and 43 to 48 (orange) form a
	group at the top right of the plot, away from the main cloud of batches.

The three components of model B explain 33.3%, 13.3% and 8.5% of the variance. With the
extreme batches gone, a second group separates in the plane of :math:`t_2` and
:math:`t_3`: batches 37, 39 and 43 to 48. Batch 39 is a representative member of the group.

.. figure:: ../figures/batch/batch-case-dupont-batch-39.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Left, the contributions of batch 39 to t3 summed per tag, led by Press-3, TempC-1 and Flow-2; right, Press-3 for all batches with the eight batches of the group in orange and batch 39 in blue, following a slightly different pressure profile.
	:width: 1000px
	:scale: 80
	:align: center

	Left: contributions of batch 39 to :math:`t_3`, summed per tag; ``Press-3``,
	``TempC-1`` and ``Flow-2`` lead. Right: ``Press-3`` for all batches, with the group of
	eight (orange) and batch 39 (blue) drawn on top. The group follows a slightly different
	pressure profile, a little lower over the first 40 samples and a little higher after
	sample 60.

The :math:`t_3` contributions of batch 39 point at ``Press-3``, ``TempC-1`` and ``Flow-2``,
and the raw overlay of ``Press-3`` shows what the model reacted to: the eight batches follow
a slightly different pressure profile, a little lower than the other batches over the first
40 samples and a little higher after sample 60. Of the eight, only batches 45 and 46 appear
in the list of batches with poor or borderline quality; the other six produced acceptable
product. They were operated differently, not badly. A model of normal operation can either
contain enough of them to describe that mode of operation or leave them out. The original
course notes leave them out, and so does the third model.

The reference model, and the batches it cannot see
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	kept_c = {batch_id: batch for batch_id, batch in kept_b.items() if batch_id not in second_group}
	model_c = BatchPCA(n_components=3).fit(kept_c)
	print("R2 per component:", model_c.r2_per_component_.round(3).tolist())
	model_c.score_plot(settings={"show_labels": True}).show()
	model_c.spe_plot(settings={"show_labels": True}).show()
	poor_quality = [38, 40, 41, 42]
	table = pd.DataFrame({"T2": model_c.hotellings_t2_.loc[poor_quality].iloc[:, -1],
	                      "T2 limit": model_c.hotellings_t2_limit(conf_level=0.95),
	                      "SPE": model_c.spe_.loc[poor_quality].iloc[:, -1],
	                      "SPE limit": model_c.spe_limit(conf_level=0.95)})
	print(table.round(2))

.. figure:: ../figures/batch/batch-case-dupont-model-c.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Scores and SPE of model C on 40 batches; batches 38, 40, 41 and 42 lie inside the confidence ellipse and below the SPE limit.
	:width: 1000px
	:scale: 80
	:align: center

	Scores (left) and SPE (right) of model C, built on 40 batches. Batches 38, 40, 41 and
	42 (orange), which produced poor product, lie inside the 95% confidence ellipse and
	below the SPE limit.

Model C, built on the 40 remaining batches, explains 37.5%, 11.4% and 6.4% of the variance
with its three components, and its scores are spread more evenly than those of the first
two models. A group of nine batches with :math:`t_1` values above 20 remains (batches 1, 6
to 10, 12, 28 and 31); they lie inside the 95% confidence ellipse and are not pursued here.

Batches 38, 40, 41 and 42 were among those with poor or borderline final quality, yet all
four sit inside the :ref:`Hotelling's T2 <LVM-Hotellings-T2>` limit and below the SPE limit
of model C:

=====  =============  =============  =====  =========
Batch  :math:`T^2`    T2 limit       SPE    SPE limit
=====  =============  =============  =====  =========
38     3.86           9.27           19.52  24.17
40     0.80           9.27           19.95  24.17
41     0.28           9.27           18.01  24.17
42     0.09           9.27           23.59  24.17
=====  =============  =============  =====  =========

Nothing in the ten trajectories distinguishes these four batches from the batches that
produced good product. This is the lesson the case study is built around, and it is worth
stating as a requirement. A model can only detect what the measurements contain. If the
cause of poor quality leaves no trace in the recorded variables, because the important
trajectory is not being measured or because the cause lies in the raw materials charged
before the batch started, then no modelling of these ten tags will reveal it. The
measurements must contain the information needed to classify a batch; in the language of
control engineering, the condition of the batch must be *observable* through them. The
remedy is to measure something else, for example the properties of the raw materials, and
the :ref:`third case study <APPS_batch_case_fmc>` shows how such blocks are added to a
batch model.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~

* Paul Nomikos and John F. MacGregor, "`Multivariate SPC charts for monitoring batch
  processes <https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_",
  *Technometrics*, **37**, 41-59, 1995. The source of the data and of the list of batches
  with poor final quality.

* Paul Nomikos and John F. MacGregor, "`Monitoring batch processes using multiway principal
  component analysis <https://literature.learnche.org/item/30/monitoring-batch-processes-using-multiway-principal-component-analysis>`_",
  *AIChE Journal*, **40**, 1361-1375, 1994. The batchwise unfolding used on this page.

* Paul Nomikos, `Statistical process control of batch processes <https://literature.learnche.org/item/154/statistical-process-control-of-batch-processes>`_,
  Ph.D thesis, McMaster University, 1995.

* The full list of readings on batch data is on the
  :ref:`batch process monitoring <APPS_batch_monitoring>` page.
