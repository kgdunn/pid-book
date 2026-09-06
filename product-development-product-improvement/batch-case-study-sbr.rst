.. _APPS_batch_case_sbr:

Diagnosing a known fault with batch PLS: the SBR reactor
=========================================================

.. index::
	single: batch data; SBR reactor case study
	pair: batch PLS; fault diagnosis
	pair: contribution plots; batch PLS
	single: simulated data; batch reactor

Styrene-butadiene rubber (SBR) is made by emulsion polymerization in a batch reactor. Six
trajectories are recorded during each batch: the reactor temperature, the cooling-water
temperature and the jacket temperature, the density of the latex, the conversion, and the
energy released by the reaction. Five quality attributes of the latex are measured at the end
of each batch: composition, particle size, branching, cross-linking and polydispersity. The
53 batches of this case study were simulated from a first-principles model of the reactor
(Nomikos, 1995), so the fault is known: batches 34 and 37 both received 30% more organic
impurity in the butadiene feed than the other batches, from the very start of batch 37 and
midway through batch 34. That is the value of simulated data. A model can be checked against
what is known to have happened before it is trusted on plant data, where nothing is known
for certain.

The :ref:`first case study <APPS_batch_case_dupont>` used a PCA model of the trajectories
alone. Here a block of final quality attributes is available, so the model is a
:ref:`PLS <SECTION_PLS>` model from the unfolded trajectories to the five quality
attributes. Three questions are asked of it: does the model single out the two faulty
batches, does it say what went wrong and when, and could it have said so while the batches
were still running.

The data
~~~~~~~~

The `SBR batch reactor dataset <https://openmv.net/info/sbr-batch-reactor>`_ is a workbook
with two sheets: the trajectories, 53 batches of 200 samples, and the quality attributes,
one row per batch. The workbook holds nine trajectories. The two feed flow rates are
constant in the simulation and the feed temperature barely moves, so the model uses the six
trajectories the original study modelled. The ``load_sbr`` function returns the batch
dictionary, the quality table and the list of those six tags.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.batch import (BatchMonitor, BatchPLS, contribution_at_time_plot, load_sbr, online_monitoring_plot,
	                                   time_varying_loading_plot, unfolded_contribution_plot)
	from process_improve.univariate import median_absolute_deviation

	sbr = load_sbr()                                # https://openmv.net/file/sbr-batch-reactor.xlsx
	trajectories = {batch_id: batch[sbr.trajectory_tags] for batch_id, batch in sbr.X.items()}
	quality = sbr.Y
	print(len(trajectories), "batches;", sbr.trajectory_tags, "; quality block", quality.shape)

.. code-block:: python

	GREY, ORANGE, AQUA, BLUE = "#c8c8c8", "#c55a11", "#1baf7a", "#1f3d7a"     # figure colours, reused below

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

	for tag in sbr.trajectory_tags:
	    overlay(trajectories, tag, {34: ORANGE, 37: AQUA}).show()

.. _APPS_batch_case_sbr_overlay:

.. figure:: ../figures/batch/batch-case-sbr-raw-trajectories.png
	:source: batch/batch-case-sbr-figures.py
	:alt: The six trajectories of the 53 batches in grey with batch 34 in orange and batch 37 in aqua; the conversion of batch 37 runs below the others from the start, and the cooling-water and jacket temperatures of batch 34 rise above the others after sample 100 while its energy released falls below them.
	:width: 1100px
	:scale: 80
	:align: center

	The six trajectories of all 53 batches (grey) with batch 34 (orange) and batch 37 (aqua)
	drawn on top. Batch 37 converts more slowly than the others from the start. Batch 34
	follows the others until about sample 100, after which its cooling-water and jacket
	temperatures rise above the band of the other batches and its energy released falls
	below it.

The overlay already shows both faults: batch 37 from the start, in the conversion, and
batch 34 from about sample 100, in the two service temperatures and the energy released.
Neither shows in the reactor temperature, which is held within a narrow range in every
batch.

The batch PLS model
~~~~~~~~~~~~~~~~~~~

``BatchPLS`` unfolds each batch batchwise, into one row of 6 tags times 200 samples, 1200
columns, centres and scales every column, and fits a PLS model from that row to the five quality
attributes, which are also centred and scaled. Two components are used. As in the first
case study, the aim of the first model is to see what is going on, not to settle the number
of components; the usual :ref:`cross-validation <LVM-PLS-number-of-components>` can follow.

.. code-block:: python

	model = BatchPLS(n_components=2).fit(trajectories, quality)
	r2y = np.diff([0.0, *model.r2_cumulative_])                     # R2 of the quality block, per component
	r2x = np.diff([0.0, *model.r2_per_variable_.mean(axis=0)])     # R2 of the trajectories, per component
	print("R2X per component:", r2x.round(3), " R2Y per component:", r2y.round(3))
	fig = model.score_plot(settings={"show_labels": True})
	fig.update_layout(xaxis_title=f"t1 [{r2x[0]:.1%}]", yaxis_title=f"t2 [{r2x[1]:.1%}]").show()
	for batch_id in (34, 37):
	    print(f"batch {batch_id}: T2 = {model.hotellings_t2_.loc[batch_id].iloc[-1]:.1f} (limit {model.hotellings_t2_limit(conf_level=0.95):.1f}),",
	          f"SPE = {model.spe_.loc[batch_id].iloc[-1]:.1f} (limit {model.spe_limit(conf_level=0.95):.1f})")

The first component explains 65.3% of the variance in the quality block and the second
6.9%; their shares of the variance in the trajectories are on the axes of the score plot.

.. figure:: ../figures/batch/batch-case-sbr-scores.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Scores of the batch PLS model with the 95% confidence ellipse; batch 37 has the lowest t1 of all batches and batch 34 the highest t2, both far outside the ellipse; batch 4, in purple, sits near the centre.
	:width: 600px
	:scale: 80
	:align: center

	Scores of the batch PLS model. Batch 37 (aqua) has the lowest :math:`t_1` of all
	batches and batch 34 (orange) the highest :math:`t_2`; both lie far outside the 95%
	confidence ellipse. Batch 4 (purple) is the batch nearest the average quality, used
	:ref:`below <APPS_batch_case_sbr_online_prediction>` to show the prediction while the
	batch runs.

The score plot flags both faulty batches: their :ref:`Hotelling's T2 <LVM-Hotellings-T2>`
values are 28.2 and 19.2 against a 95% limit of 6.6.

The SPE answers the other question a model can be asked about a batch: how far it sits
away from the components, in directions the model has not described. Drawing it against
:ref:`Hotelling's T2 <LVM-Hotellings-T2>`, which summarises how extreme the batch is along
the components, puts both questions in one figure. Each axis carries its own 95% limit.

.. code-block:: python

	def influence_plot(model, highlight, labels, conf_level=0.95):
	    """Hotelling's T2 against SPE, one dot per batch, with both limits drawn."""
	    t2, spe = model.hotellings_t2_.iloc[:, -1], model.spe_.iloc[:, -1]
	    others = [batch_id for batch_id in t2.index if batch_id not in highlight]
	    fig = go.Figure()
	    fig.add_trace(go.Scatter(x=t2.loc[others], y=spe.loc[others], mode="markers", showlegend=False,
	                             marker=dict(size=8, color=BLUE), text=others, hovertemplate="batch %{text}"))
	    for batch_id, colour in highlight.items():
	        fig.add_trace(go.Scatter(x=[t2.loc[batch_id]], y=[spe.loc[batch_id]], mode="markers",
	                                 name=f"batch {batch_id}", marker=dict(size=12, color=colour)))
	    fig.add_vline(x=model.hotellings_t2_limit(conf_level=conf_level), line_dash="dash", line_color=GREY)
	    fig.add_hline(y=model.spe_limit(conf_level=conf_level), line_dash="dash", line_color=GREY)
	    for batch_id in labels:
	        fig.add_annotation(x=t2.loc[batch_id], y=spe.loc[batch_id], text=str(batch_id),
	                           showarrow=False, xshift=13, yshift=9)
	    fig.update_layout(xaxis_title="Hotelling's T\u00b2", yaxis_title="SPE", height=420)
	    return fig

	spe, t2 = model.spe_.iloc[:, -1], model.hotellings_t2_.iloc[:, -1]
	above_spe = sorted(spe.index[spe > model.spe_limit(conf_level=0.95)])
	print("above the SPE limit:", above_spe, "  above the T2 limit:",
	      sorted(t2.index[t2 > model.hotellings_t2_limit(conf_level=0.95)]))
	influence_plot(model, highlight={34: ORANGE, 37: AQUA}, labels=[34, 37, *above_spe]).show()

.. figure:: ../figures/batch/batch-case-sbr-influence.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Hotelling's T2 against SPE for the 53 batches, with both 95% limits; batches 34 and 37 are far to the right beyond the T2 limit and below the SPE limit, while batches 8 and 16 are in the upper left above the SPE limit.
	:width: 620px
	:scale: 80
	:align: center

	Hotelling's :math:`T^2` against the SPE for every batch, with both 95% limits. Batches 34
	(orange) and 37 (aqua) are far to the right and below the SPE limit. The batches the SPE
	flags, 8, 15 and 16, are different batches, in the upper left.

The SPE flags different batches, 8, 15 and 16, all with ordinary :math:`T^2` values; three
batches at or above a limit set at 95% is within what that limit allows for among 53
batches. The SPE of a batch model is computed from the residuals of the whole batch, all
1200 cells, so a deviation the model can describe, a shift along its components, leaves
little residual behind. The scores say that a batch moved in a direction the model knows;
the SPE says that it moved in a direction the model does not know.

Where the model explains the trajectories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every unfolded column has its own :math:`R^2`, so the fit can be read per tag and per time
sample. The same applies to the weights :math:`\mathbf{w}_1` and :math:`\mathbf{w}_2` of
the two components, each a vector of 1200 entries, which ``time_varying_loading_plot``
draws as six curves over the batch. The weights of a PLS model play the role that the
loadings play in a PCA model; the section on :ref:`how the PLS model is calculated
<LVM_PLS_calculation>` explains the difference.

.. code-block:: python

	r2_grid = model.r2_per_variable_.iloc[:, -1].unstack(level="sequence")   # rows = tags, columns = time
	fig = go.Figure()
	for tag, row in r2_grid.iterrows():
	    fig.add_trace(go.Scatter(x=row.index, y=row.values, mode="lines", name=tag))
	fig.update_layout(title="R2 of each (tag, time) cell after two components", xaxis_title="Sample [aligned time]",
	                  yaxis_title="R2", height=360)
	fig.show()
	print("R2 per tag, averaged over time:", r2_grid.mean(axis=1).round(2).to_dict())
	time_varying_loading_plot(model, component=1).show()
	time_varying_loading_plot(model, component=2).show()

.. figure:: ../figures/batch/batch-case-sbr-r2-over-time.png
	:source: batch/batch-case-sbr-figures.py
	:alt: R2 of every (tag, time) cell after two components, one panel per tag; latex density and conversion rise to about 0.9, the two temperatures and the energy released reach 0.3 to 0.6 only in the second half of the batch, and the reactor temperature stays below 0.3.
	:width: 700px
	:scale: 80
	:align: center

	:math:`R^2` of every (tag, time) cell after two components, one panel per tag. Latex
	density and conversion are well explained from about sample 50 onwards; the two
	temperatures and the energy released only in the second half of the batch; the reactor
	temperature hardly at all.

Latex density and conversion are the trajectories the model uses most: their :math:`R^2`,
averaged over the batch, is 0.67 and 0.75, against 0.23 to 0.26 for the cooling-water
temperature, the jacket temperature and the energy released, and 0.08 for the reactor
temperature. Every :math:`R^2` curve is low at the start of the batch. All batches begin
alike, so after centring and scaling the first samples of every trajectory contain little
but noise, and there is nothing there for the model to explain.

.. figure:: ../figures/batch/batch-case-sbr-weights.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Time-varying weights of the two components, one panel per tag; w1 is large and positive for latex density and conversion over the whole batch, and w2 is positive for the two temperatures and negative for the energy released, latex density and conversion in the second half of the batch.
	:width: 700px
	:scale: 80
	:align: center

	Time-varying weights :math:`\mathbf{w}_1` (blue) and :math:`\mathbf{w}_2` (orange) of
	the two components, one panel per tag. The first is dominated by latex density and
	conversion over the whole batch; the second by the cooling-water and jacket
	temperatures, the energy released, the latex density and the conversion in the second
	half of the batch, with opposite signs.

The weights say what a score means. A batch with a low :math:`t_1` has a below-average latex
density and conversion throughout the batch. A batch with a high :math:`t_2` has
cooling-water and jacket temperatures above their average trajectories over the second half
of the batch, with the energy released, the latex density and the conversion below theirs;
the reactor temperature, the tag this component involves least, barely moves. The component
says that these tags move together; it does not say which of them drives the others. Those
are predictions about batches 37 and 34 respectively, and the contribution plots test them.

Batch 37: the fault from the start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	scaled = model.unfold_and_scale(trajectories)              # the 53 x 1200 matrix the model was fitted on
	t1 = model.score_contributions(scaled, component=1)
	unfolded_contribution_plot(t1, batch_id=37).show()
	unfolded_contribution_plot(t1, batch_id=37, by_tag=True).show()
	print("batch 37, t1 contributions per tag:", t1.loc[37].groupby(level="tag", sort=False).sum().round(1).to_dict())

	def share_per_fifth(row):
	    """Split a contribution vector into five equal time blocks and give each block's share of the total."""
	    by_time = row.groupby(level="sequence").sum()
	    fifths = by_time.groupby(np.arange(len(by_time)) * 5 // len(by_time)).sum()
	    return (fifths / fifths.sum()).round(2).tolist()

	print("batch 37: share of the t1 contribution per fifth of the batch:", share_per_fifth(t1.loc[37]))

.. figure:: ../figures/batch/batch-case-sbr-batch-37-contributions.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Three panels for batch 37: the contribution of each unfolded cell to t1, negative throughout and largest for conversion and latex density; the sum per tag; and the sum per sample, negative from the first sample to the last.
	:width: 800px
	:scale: 80
	:align: center

	Top: the contribution of each (tag, time) cell of batch 37 to :math:`t_1`. Middle: the
	same contributions summed per tag. Bottom: summed per sample. Conversion and latex
	density carry the contribution, and every part of the batch contributes.

As in the :ref:`first case study <APPS_batch_case_dupont>`, the contribution vector has one
entry per (tag, time) cell, here :math:`K = 6` tags by :math:`J = 200` time samples, and
summing it per tag or per sample says which trajectory and which part of the batch the score
came from.

Batch 37 sits at the low end of :math:`t_1` because its conversion and its latex density
were below average, and the contribution is spread over the whole batch: each fifth of the
batch carries between 15% and 26% of the total, which is what a fault that is present at
the start of the batch would look like. The
:ref:`raw trajectory overlay <APPS_batch_case_sbr_overlay>` at the start of this case
study agrees. The impurity slowed the reaction from the moment the batch began.

Batch 34: the same fault, from the middle of the batch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	t2 = model.score_contributions(scaled, component=2)
	unfolded_contribution_plot(t2, batch_id=34).show()
	contribution_at_time_plot(t2, k=120, batch_id=34).show()
	print("batch 34, t2 contributions per tag:", t2.loc[34].groupby(level="tag", sort=False).sum().round(1).to_dict())
	print("batch 34: share of the t2 contribution per fifth of the batch:", share_per_fifth(t2.loc[34]))

.. figure:: ../figures/batch/batch-case-sbr-batch-34-contributions.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Three panels for batch 34: the contribution of each unfolded cell to t2, largest for the energy released and the two temperatures; the sum per tag; and the sum per sample, small until sample 100 and large after it, with a maximum near sample 140.
	:width: 800px
	:scale: 80
	:align: center

	Top: the contribution of each (tag, time) cell of batch 34 to :math:`t_2`. Middle: the
	same contributions summed per tag. Bottom: summed per sample. The energy released and
	the two temperatures lead, and the contribution per sample is small until sample 100 and
	large after it.

Batch 34 is high on :math:`t_2` through the energy released and the two service
temperatures, with the conversion and the latex density behind them. The timing is what
distinguishes this batch from batch 37: the first two fifths of the batch carry 15% of the
:math:`t_2` contribution and the last two fifths 68%. ``contribution_at_time_plot`` shows
the same three tags carrying the deviation at a single sample, here sample 120.

The raw data can be asked the same question directly, tag by tag: at which sample does each
trajectory of a faulty batch leave the band of the other batches? The code below expresses
each trajectory of batches 34 and 37 as a distance from the mean of the other 51 batches,
in units of their standard deviation at that sample, and records the first sample from
which a tag stays more than two standard deviations away for 20 samples in a row, a tenth
of the batch. A single crossing is not informative on its own, because a noisy tag such as
the reactor temperature crosses the two-standard-deviation line now and then in every
batch. A robust version of the same distance uses the median of the other batches and
1.4826 times their median absolute deviation (MAD), which the factor makes equal to the
standard deviation for normally distributed values, smoothed with an EWMA
(:math:`\lambda = 0.3`, the value of the :ref:`EWMA chart <monitoring_EWMA>` example).

.. code-block:: python

	others = np.stack([batch.to_numpy() for batch_id, batch in trajectories.items() if batch_id not in (34, 37)])
	z = {batch_id: (trajectories[batch_id].to_numpy() - others.mean(axis=0)) / others.std(axis=0, ddof=1)
	     for batch_id in (37, 34)}
	spread = median_absolute_deviation(others, axis=0, scale="normal")             # 1.4826 x MAD
	z_robust = {batch_id: pd.DataFrame((trajectories[batch_id].to_numpy() - np.median(others, axis=0)) / spread)
	            .ewm(alpha=0.3, adjust=False).mean().to_numpy() for batch_id in (37, 34)}  # EWMA-smoothed

	def sustained_departure(z_batch, n_sd=2.0, run=20):
	    """First sample from which each tag stays more than `n_sd` scale units away for `run` samples in a row."""
	    outside = (np.abs(z_batch) > n_sd).astype(int)      # 1 where the tag is outside the band, 0 inside
	    onset = {}
	    for j, tag in enumerate(sbr.trajectory_tags):
	        # Convolving the 0/1 column with `run` ones is a moving sum over every window of `run`
	        # consecutive samples: entry i is how many of samples i to i+run-1 lie outside the band.
	        # "valid" keeps only the windows that fit entirely inside the batch, so entry i starts at
	        # sample i. A window summing to `run` is an unbroken stretch, and argmax finds the first
	        # True, which is the sample the stretch starts at. Without a True, argmax returns 0, so
	        # test `any()` first and report None instead.
	        runs = np.convolve(outside[:, j], np.ones(run, dtype=int), mode="valid") == run
	        onset[tag] = int(runs.argmax()) if runs.any() else None
	    return onset

	for batch_id in (37, 34):
	    print(f"batch {batch_id}, first sustained departure:", sustained_departure(z[batch_id]))
	    print("  robust, smoothed:", sustained_departure(z_robust[batch_id]))

	fig = make_subplots(rows=2, cols=6, subplot_titles=sbr.trajectory_tags, shared_yaxes=True)
	for row, (batch_id, colour) in enumerate([(37, AQUA), (34, ORANGE)], start=1):
	    for col in range(6):
	        # signed distances, not their absolute value: the sign says whether the tag ran above or below the others
	        fig.add_trace(go.Scatter(y=z_robust[batch_id][:, col], mode="lines", name=f"batch {batch_id}, robust",
	                                 line=dict(color=colour, width=1.5), showlegend=(col == 0)), row=row, col=col + 1)
	        fig.add_trace(go.Scatter(y=z[batch_id][:, col], mode="lines", name=f"batch {batch_id}, mean and sd",
	                                 line=dict(color=colour, width=1, dash="dash"), showlegend=(col == 0)), row=row, col=col + 1)
	        fig.add_hrect(y0=-2, y1=2, fillcolor=GREY, opacity=0.15, line_width=0, row=row, col=col + 1)
	        for level in (-2, 2):
	            fig.add_hline(y=level, line_dash="dot", line_color=GREY, row=row, col=col + 1)
	fig.update_layout(title="Distance from the other batches: robust (solid) and mean-and-sd (dashed)", height=420)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-departure.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Twelve small panels, one per tag for batch 37 in the top row and batch 34 in the bottom row, each with a solid robust distance and a dashed standard-deviation distance from the other batches and the band between plus and minus two shaded; batch 37 falls below the band in latex density and conversion early, and batch 34 rises above it in the two service temperatures and falls below it in the energy released at about sample 100, then in latex density and conversion later.
	:width: 1100px
	:scale: 80
	:align: center

	Signed distance of batch 37 (top, aqua) and batch 34 (bottom, orange) from the other
	batches for each of the six tags. Solid: the robust distance, the median and 1.4826 MAD
	of the others, EWMA-smoothed. Dashed: the distance from the mean of the others in units of
	their standard deviation. The band between plus and minus two is shaded.

Batch 37 leaves the band in the conversion and the latex density within the first 20
samples and stays out; batch 34 leaves it midway, first in the two service temperatures
and the energy released and some 20 samples later in the conversion and the latex density.
The robust distance moves the onsets by a few samples at most, and runs larger wherever one
of the other batches is itself unusual at that sample.

One fault, two places in the score plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same fault appears in two different places of the score plot because it started at two
different times. A batch model describes deviations in (tag, time) cells, so the time of an
event is part of its signature: a slow reaction from the start is a deviation along
:math:`\mathbf{w}_1`, and a slow reaction from the middle of the batch a deviation along
:math:`\mathbf{w}_2`. This is what makes batch models useful for diagnosis, and it is also a
caution. A library of known faults built in score space needs the time of onset as a
coordinate, and a fault that has been seen only at one onset time appears as a new fault
when it occurs at another. The :ref:`on-line section <APPS_batch_case_sbr_online>` below
returns to the two batches with a model that has never seen either fault, where the two
places become two statistics.

Predicted quality
~~~~~~~~~~~~~~~~~

A PLS model predicts the quality attributes as well, and the fitted values of the two faulty
batches show what the trajectories knew before the laboratory did.

.. code-block:: python

	for variable in ("Composition", "ParticleSize"):
	    model.predictions_vs_observed_plot(quality, variable=variable).show()
	faulty = [34, 37]
	table = pd.concat({"observed": quality.loc[faulty], "fitted": model.predictions_.loc[faulty],
	                   "rank of observed": quality.rank().loc[faulty].astype(int)}, names=["value", "batch_id"])
	print(table.to_string(float_format=lambda value: f"{value:.4g}"))

.. figure:: ../figures/batch/batch-case-sbr-observed-vs-fitted.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Observed against fitted composition and particle size for the 53 batches with batches 34 and 37 marked; both faulty batches lie at the low end of both attributes.
	:width: 900px
	:scale: 80
	:align: center

	Observed against fitted composition (left) and particle size (right) for the 53 batches,
	with batches 34 (orange) and 37 (aqua) marked.

==============  ===========  =============  =========  =============  ==============
Batch           Composition  Particle size  Branching  Cross-linking  Polydispersity
==============  ===========  =============  =========  =============  ==============
34, observed    0.4525       1244           1.234e-5   4.784e-5       3.599
34, fitted      0.4540       1245           1.228e-5   4.761e-5       3.577
34, rank        5            1              4          4              17
37, observed    0.4525       1247           1.173e-5   4.549e-5       3.462
37, fitted      0.4500       1250           1.183e-5   4.585e-5       3.491
37, rank        4            2              1          1              1
==============  ===========  =============  =========  =============  ==============

The rank is the position of the observed value among the 53 batches, with rank 1 the
lowest. Both batches produced poor latex, at or near the bottom of the 53 on most
attributes, and the fitted values place them at the same end, so a quality prediction from
the trajectories would have flagged both batches before the laboratory results arrived.

The two batches are not fitted equally well: the composition of batch 37 is fitted below
its observed value, that of batch 34 closer to the average batch than to its observed
value. The :math:`t_1` direction, which carries the fault of batch 37, explains 65.3% of the
quality block; the :math:`t_2` direction, which carries the fault of batch 34, explains
6.9%. A deviation along a component that explains little of the quality block moves the
prediction less.

.. _APPS_batch_case_sbr_online_prediction:

Predicting quality before the batch ends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The fitted values of the previous section used the whole batch. It is far more interesting
if it is possible to predict what its final quality will be while the batch is still
running:

* its unfolded row is complete up to the current sample and empty after it, and the scores
  are estimated from the observed cells alone, with the rest of the row treated as missing
  data (Wold and co-workers, 2009, Eqs. 2 and 5; the estimator is the trimmed score
  regression of Garcia-Munoz, Kourti and MacGregor, 2004);
* the model's regression from scores to quality turns those scores into a prediction;
* the prediction error after :math:`k` samples, RMSEP, comes from refitting the model
  without each batch in turn and tracing the held-out batch (``online_rmse``; the loop
  below takes about a minute).

.. code-block:: python

	squared = 0
	for held_out in trajectories:                                      # leave one batch out: about a minute
	    rest = {b: t for b, t in trajectories.items() if b != held_out}
	    model_wo = BatchPLS(n_components=2).fit(rest, quality.loc[list(rest)])
	    squared = squared + model_wo.online_rmse({held_out: trajectories[held_out]}, quality.loc[[held_out]]) ** 2
	rmsep_k = np.sqrt(squared / len(trajectories))                     # after 1, 2, ..., 200 samples
	relative = rmsep_k / quality.std()
	at = [10, 25, 50, 150, 200]
	print(relative.loc[at].mean(axis=1).round(2).tolist())              # RMSEP / sd averaged over the five attributes
	# [2.99, 1.39, 1.06, 0.62, 0.58]
	print((relative < 1).idxmax().tolist())                              # first sample with RMSEP below the sd, per attribute
	# [48, 129, 50, 50, 21]

	PURPLE, MAGENTA = "#6f42c1", "#b03a78"                                 # two more figure colours
	COLOURS = (BLUE, ORANGE, AQUA, PURPLE, MAGENTA)                        # one per attribute
	fig = go.Figure()
	for attribute, colour in zip(quality.columns, COLOURS):
	    fig.add_trace(go.Scatter(x=relative.index[9:], y=relative[attribute].iloc[9:], name=attribute,
	                             line=dict(color=colour)))
	fig.add_hline(y=1.0, line_color=GREY, annotation_text="as good as the average batch")
	fig.update_layout(xaxis_title="Samples observed", yaxis_title="RMSEP / standard deviation of the attribute", height=420)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-online-rmse.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Five curves, one per quality attribute, of the leave-one-batch-out root-mean-square error of the mid-batch prediction divided by the attribute's standard deviation against the number of samples observed; all start above one, the particle-size curve falls below one after about 120 samples, branching and cross-linking fall furthest, polydispersity changes little after 50 samples.
	:width: 800px
	:scale: 80
	:align: center

	Root-mean-square error of the leave-one-batch-out prediction after :math:`k` samples,
	divided by the standard deviation of each attribute. Branching and cross-linking
	coincide. A curve above 1 is worse than predicting the average batch.

The particle size becomes predictable only in the second half of the batch, where the
:math:`R^2` curves earlier on this page also placed the information. Branching and
cross-linking are predicted best; polydispersity is predicted about as well after 50
samples as at the end. The value of the curves is in their timing: polydispersity is
predicted with an error below one standard deviation of the attribute from about 20
samples on, composition, branching and cross-linking from about 50, and the particle size
from about 130, each with most of the batch still to run. Averaged over the five
attributes, the prediction error falls from three standard deviations after 10 samples to
1.4 after 25, 1.1 after 50 and 0.6 after 150, close to its value when the batch ends.

Batch 4, the batch nearest the average quality, shows what the curves summarise: its
prediction against the number of samples observed, with the prediction from the complete
batch dashed, the measured value solid, and a band of one prediction error at that sample
(from the RMSEP curve; it is not a prediction interval).

.. code-block:: python

	near_average = 4
	trace = model.predict_online_trace(trajectories[near_average])
	for attribute in ("ParticleSize", "Composition"):
	    band = rmsep_k[attribute]
	    fig = go.Figure()
	    fig.add_trace(go.Scatter(x=trace.time[4:], y=(trace.y_hat[attribute] + band).iloc[4:], line=dict(width=0),
	                             showlegend=False))
	    fig.add_trace(go.Scatter(x=trace.time[4:], y=(trace.y_hat[attribute] - band).iloc[4:], fill="tonexty",
	                             fillcolor="rgba(200, 200, 200, 0.35)", line=dict(width=0), name="one prediction error"))
	    fig.add_trace(go.Scatter(x=trace.time[4:], y=trace.y_hat[attribute].iloc[4:], name="prediction so far",
	                             line=dict(color=BLUE)))
	    fig.add_hline(y=model.predictions_.loc[near_average, attribute], line_dash="dash", line_color=GREY,
	                  annotation_text="final prediction")
	    fig.add_hline(y=quality.loc[near_average, attribute], line_color="black", annotation_text="measured")
	    fig.update_layout(title=f"Batch {near_average}: {attribute}", xaxis_title="Samples observed", height=380)
	    fig.show()
	print("batch 4, particle size: measured", round(quality.loc[4, "ParticleSize"], 1),
	      "final prediction", round(model.predictions_.loc[4, "ParticleSize"], 1))
	print("  prediction after 10, 25, 50, 100, 150 samples:", trace.y_hat["ParticleSize"].loc[[10, 25, 50, 100, 150]].round(1).tolist())
	print("batch 4, composition: measured", round(quality.loc[4, "Composition"], 4),
	      "final prediction", round(model.predictions_.loc[4, "Composition"], 4))

.. figure:: ../figures/batch/batch-case-sbr-online-prediction-batch-4.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Two panels of batch 4's evolving prediction against samples observed, with a shaded band of one prediction error, a dashed line at the final prediction and a solid line at the measured value; the particle-size prediction starts well below the final value and settles on it in the second half of the batch.
	:width: 1000px
	:scale: 80
	:align: center

	The prediction for batch 4 as the batch is observed, for the particle size (left) and
	the composition (right). Dashed: the prediction from the complete batch. Solid: the
	measured value. Band: one prediction error at that sample. For the particle size the two
	rules are 0.2 units apart and overlap at this scale; for the composition they are 0.0002
	apart and separate.

The prediction walks in from the average batch toward the final value as the samples that
carry the information arrive, and the band narrows with it.

.. _APPS_batch_case_sbr_online:

Would the model have caught it on-line?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model on this page was fitted with batches 34 and 37 inside it, which is the right
thing for diagnosing them after the fact and the wrong thing for monitoring. A monitoring
model must describe normal operation, as the :ref:`first case study <APPS_batch_case_dupont>`
says when it removes its outliers before building its reference model. The reference model
here is therefore fitted to the 51 batches without 34 and 37, and the two are then run
through it sample by sample, as if they were new batches on a running plant.

Two statistics are tracked. Hotelling's :math:`T^2` of the score estimate says how far the
batch so far sits *along* the model's components; the SPE of the newest sample says how far
that sample sits *away* from them.

The :math:`T^2` limit is the same at every sample, since it depends only on the number of
components and of reference batches. What changes with the samples seen is the spread of
the score estimates: a score estimated from the first few samples is fitted to a few of the
cells in the unfolded row, and across the reference batches such estimates scatter far more
widely than the final scores do, as the figure below shows. :math:`T^2` at each sample is
therefore computed against the covariance of the reference batches' estimates at that same
sample (Nomikos and MacGregor, 1995), which the monitor stores. The SPE limit is fitted
sample by sample from the reference batches' SPE at that sample.

.. code-block:: python

	normal = {b: t for b, t in trajectories.items() if b not in (34, 37)}
	reference = BatchPLS(n_components=2).fit(normal, quality.loc[list(normal)])
	monitor = BatchMonitor(reference, conf_level=0.99, spe_statistic="instantaneous").fit(normal)
	spread = np.sqrt(np.diagonal(monitor.score_covariance_over_time_, axis1=1, axis2=2))   # sd of the estimates, per sample
	spread = spread / reference.scores_.std(ddof=1).to_numpy()                           # relative to the final scores
	fig = go.Figure()
	for a, colour in enumerate((BLUE, ORANGE)):
	    fig.add_trace(go.Scatter(x=np.arange(1, len(spread) + 1), y=spread[:, a], name=f"t{a + 1}", line=dict(color=colour)))
	fig.add_hline(y=1.0, line_dash="dash", line_color=GREY, annotation_text="spread of the final scores")
	fig.update_layout(xaxis_title="Samples observed", yaxis_title="Spread relative to the final scores", yaxis_type="log",
	                  height=380)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-score-spread.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Two curves on a logarithmic axis, the standard deviation of the t1 and t2 estimates across the 51 reference batches divided by that of their final scores, against samples observed; both start far above one and fall to one at the end of the batch.
	:width: 600px
	:scale: 80
	:align: center

	The spread of the on-line score estimates across the 51 reference batches, divided by
	the spread of their final scores, against the number of samples observed (logarithmic
	axis). :math:`T^2` at each sample is scaled by this spread, which is what lets the limit
	stay the same throughout the batch.

The limits are set at 99%, and an alarm here means three consecutive samples above the
limit, the same kind of rule the departure analysis used.

.. code-block:: python

	def first_sustained(alarm, run=3):
	    """Number of samples observed when the alarm first holds for `run` consecutive samples, or None."""
	    runs = np.convolve(alarm.astype(int), np.ones(run, dtype=int), mode="valid") == run
	    return int(runs.argmax()) + 1 if runs.any() else None

	print(f"T2 limit at 99%: {monitor.t2_limit_over_time_[0]:.1f}")
	for batch_id in (37, 34, 4):
	    result = monitor.monitor(trajectories[batch_id])
	    print(f"batch {batch_id}: T2 alarm after {first_sustained(result.t2_alarm)} samples;",
	          f"SPE alarm after {first_sustained(result.spe_alarm)} samples")

	def longest_run(alarm):
	    """Longest stretch of consecutive samples above the limit."""
	    best = current = 0
	    for above in alarm:
	        current = current + 1 if above else 0
	        best = max(best, current)
	    return best

	traced = [monitor.monitor(t) for t in normal.values()]
	print(f"reference batches: {np.mean([r.t2_alarm.mean() for r in traced]):.2%} of T2 values and",
	      f"{np.mean([r.spe_alarm.mean() for r in traced]):.2%} of SPE values above their limits")
	for run in (3, 5, 10):
	    print(f"  with an SPE alarm of {run} consecutive samples somewhere:",
	          sum(first_sustained(r.spe_alarm, run) is not None for r in traced), "of 51;",
	          "T2:", sum(first_sustained(r.t2_alarm, run) is not None for r in traced), "of 51")
	print("  longest SPE alarm run in a reference batch:", max(longest_run(r.spe_alarm) for r in traced), "samples")
	print("batch 34: above the SPE limit for", int(monitor.monitor(trajectories[34]).spe_alarm[104:].sum()),
	      "of its last 96 samples; batch 37: longest T2 alarm run", longest_run(monitor.monitor(trajectories[37]).t2_alarm), "samples")
	online_monitoring_plot(monitor, trajectories[37], "t2").show()
	fig = online_monitoring_plot(monitor, trajectories[34], "spe")
	fig.add_vline(x=100, line_dash="dash", line_color=ORANGE, annotation_text="impurity enters")
	fig.show()
	alarm_k = first_sustained(monitor.monitor(trajectories[34]).spe_alarm)
	for k in (alarm_k, alarm_k + 4):
	    shares = reference.predict_online(trajectories[34], upto_k=k).residuals.xs(k - 1, level="sequence") ** 2
	    shares = (shares / shares.sum() * 100).round(0).astype(int)
	    print(f"batch 34 after {k} samples, share of the residual per tag [%]:", shares.to_dict())
	fig = go.Figure(go.Bar(x=shares.index, y=shares.values, marker_color=BLUE))
	fig.update_layout(title=f"Batch 34 after {alarm_k} samples", yaxis_title="Share of the residual [%]", height=320)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-online-monitoring.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Three panels: Hotelling's T2 of batch 37 against samples observed with the 99% limit dashed, crossing it after 23 samples and staying above; the SPE of the newest sample of batch 34 with its per-sample limit, a dashed vertical at 100 where the impurity enters, and the first sustained alarm after 105 samples; and the share of the residual per tag at that alarm sample, led by the reactor and cooling-water temperatures.
	:width: 1200px
	:scale: 80
	:align: center

	On-line monitoring of the two faulty batches against the reference model of 51 normal
	batches. Left: Hotelling's :math:`T^2` of batch 37 (aqua) with the 99% limit (dashed) and
	the reference-batch mean (grey); the first sustained alarm is after 23 samples. Middle:
	the SPE of the newest sample of batch 34 (orange) with its per-sample limit; the impurity
	enters at sample 100 (dashed vertical) and the first sustained alarm is after 105
	samples. Right: the share of the residual per tag at that alarm sample.

Batch 37 is caught by :math:`T^2` after 23 samples and stays above the limit; its SPE stays
inside its limit until 145 samples. Batch 34 is caught by the SPE after 105 samples, five
after the impurity enters; its :math:`T^2` stays inside its limit until 190 samples.

* The reference set is the definition of normal: the 51 batches are assumed to represent
  common-cause operation, with nothing wrong in any of them. Any alarm one of them raises
  is therefore a false alarm, and their alarm rate is the false-alarm rate to expect from
  normal batches on the plant.
* A limit set at 99% lets 1% of the values of a normal batch cross it by chance. The
  reference batches bear this out: 0.2% of their :math:`T^2` values and 1.2% of their SPE
  values lie above their limits.
* With 200 samples in a batch, 1% is about two crossings per normal batch, so a single
  crossing cannot count as an alarm. The rule used here is three consecutive samples above
  the limit.
* That rule holds for :math:`T^2`: one of the 51 reference batches raises a three-sample
  alarm. It does not hold for the SPE: 13 of the 51 do, a false-alarm rate of one normal
  batch in four.
* The difference is autocorrelation. The SPE of a single sample is the sum of six squared
  residuals, and a sample that fits the model poorly is usually followed by another that
  does, so the SPE of a batch runs above or below its limit in stretches, and a crossing
  that began by chance tends to last the three samples the rule asks for.
* The limit itself is not the cause. A smoother limit, fitted to the reference SPE of five
  neighbouring samples at once (``spe_window=2`` in ``BatchMonitor``), still lets about 1%
  of the values cross it, as any 99% limit does, and still gives a three-sample alarm in 15
  of the 51 reference batches: the crossings are as rare as they should be, and they still
  come in runs.
* The cumulative SPE, over every sample observed so far, averages the autocorrelation out:
  3 of the 51 reference batches raise an alarm. The price is a later detection, batch 34
  after 112 samples instead of 105.
* An alarm on a new batch can only be trusted once the false-alarm rate of the rule has
  been measured on the reference batches and made acceptable, by the choice of statistic
  or of run length. On this data the :math:`T^2` chart is used as it is; the SPE chart
  needs the cumulative statistic or a longer run, and either way batch 34 is still flagged
  with most of its second half to run.

.. code-block:: python

	pooled = BatchMonitor(reference, conf_level=0.99, spe_statistic="instantaneous", spe_window=2).fit(normal)
	pooled_traced = [pooled.monitor(t) for t in normal.values()]
	print(f"limit pooled over five samples: {np.mean([r.spe_alarm.mean() for r in pooled_traced]):.2%} of the reference",
	      f"SPE values above it; {sum(first_sustained(r.spe_alarm) is not None for r in pooled_traced)} of 51 batches",
	      f"with a three-sample run; batch 34 flagged after {first_sustained(pooled.monitor(trajectories[34]).spe_alarm)} samples")
	cumulative = BatchMonitor(reference, conf_level=0.99).fit(normal)        # the SPE over every sample observed so far
	print([sum(first_sustained(cumulative.monitor(t).spe_alarm) is not None for t in normal.values()),
	       first_sustained(cumulative.monitor(trajectories[34]).spe_alarm)])   # reference batches with an alarm; batch 34
	# [3, 112]

The two batches are caught by different statistics, and that is not an accident of the
data. The fault of batch 37 is a slower reaction from the start, and the direction of its
deviation is one the reference model already describes, because the normal batches vary
along it too, less severely: a batch far along a known direction has a large :math:`T^2` and
a small residual. The fault of batch 34 begins midway through a batch that had been normal,
in a combination of tags the reference model has no component for, so from that sample on
the newest samples stop fitting the model, which is what the SPE measures.

The residual shares say what changed. At the alarm sample the reactor temperature carries
the largest share of the residual, with the cooling-water and jacket temperatures next;
four samples later the two service temperatures and the energy released carry most of it
and the reactor temperature has dropped back: a transient in the reactor temperature and a
lasting change on the service side, in the same order the departure analysis found.

The same score estimate that predicts the quality also predicts the rest of the
trajectories: the model's reconstruction :math:`\hat{\boldsymbol{\tau}} \mathbf{P}^{T}`,
read off for the samples not yet seen (Wold and co-workers, 2009, Eq. 4). The forecast is
an interpolation along the model's components, not an extrapolation of the trend so far.
It is drawn in the z form of the departure analysis, each tag as a distance from the 51
normal batches at that sample in their standard deviations, so that the average batch is
the zero line and a departure reads directly.

.. code-block:: python

	def z_form(frame):
	    """Each tag as a distance from the 51 normal batches at that sample, in their standard deviations."""
	    return pd.DataFrame((frame.to_numpy() - others.mean(axis=0)) / others.std(axis=0, ddof=1),
	                        columns=frame.columns, index=frame.index)

	def forecast_panel(batch_id, tag, from_samples, colour):
	    """Every normal batch, what the batch did, and the model's forecast of the rest from two points, in z form."""
	    fig = overlay({b: z_form(t) for b, t in normal.items()}, tag, {})
	    z_actual = z_form(trajectories[batch_id])[tag]
	    fig.add_trace(go.Scatter(y=z_actual, mode="lines", name=f"batch {batch_id}, what happened",
	                             line=dict(color=colour, width=1), opacity=0.4))
	    for k, dash, line_colour, width in zip(from_samples, ("dash", "dot"), (colour, BLUE), (2, 3)):     # the later
	        forecast = z_form(reference.predict_online(trajectories[batch_id], upto_k=k).forecast)[tag]   # one apart
	        fig.add_trace(go.Scatter(x=forecast.index[k:], y=forecast.iloc[k:], mode="lines",
	                                 name=f"forecast from sample {k} onwards", line=dict(color=line_colour, width=width, dash=dash)))
	        fig.add_trace(go.Scatter(x=[k - 1, k - 1], y=[z_actual.iloc[k - 1], forecast.iloc[k]], mode="lines",   # the jump from
	                                 line=dict(color=line_colour, width=1.5), showlegend=False))              # the data used
	    fig.add_trace(go.Scatter(y=z_actual.iloc[:from_samples[0]], mode="lines",
	                             name=f"batch {batch_id}, observed", line=dict(color=colour, width=3)))
	    fig.add_hline(y=0, line_color=GREY)
	    fig.update_layout(title=f"Batch {batch_id}: {tag}", yaxis_title="Distance from the normal batches [sd]")
	    return fig

	forecast_panel(37, "Conversion", (30, 60), AQUA).show()
	forecast_panel(34, "CoolingTemp", (60, 115), ORANGE).add_vline(x=100, line_dash="dash", line_color=ORANGE).show()
	for batch_id, tag, k in ((37, "Conversion", 30), (37, "Conversion", 60), (34, "CoolingTemp", 60), (34, "CoolingTemp", 115)):
	    forecast = z_form(reference.predict_online(trajectories[batch_id], upto_k=k).forecast)[tag].iloc[k:]
	    print(f"batch {batch_id}, {tag}, from sample {k} onwards: forecast mean {forecast.mean():.2f} sd,",
	          f"actual {z_form(trajectories[batch_id])[tag].iloc[k:].mean():.2f} sd")

.. figure:: ../figures/batch/batch-case-sbr-forecast.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Two panels in z form, each tag as a distance from the normal batches in their standard deviations. Left, the conversion of the 51 normal batches in grey around zero, batch 37's observed conversion in aqua up to 30 samples, well below zero, and the model's forecasts of the rest from sample 30 onwards (dashed aqua) and from sample 60 onwards (dotted dark blue) that stay below zero, close to what happened. Right, the cooling-water temperature of batch 34 in orange with forecasts from sample 60 onwards (dashed orange) and from sample 115 onwards (dotted dark blue) that stay near zero and miss the rise after sample 100.
	:width: 1000px
	:scale: 80
	:align: center

	Forecast of the rest of the batch from the score estimate, in z form: each tag as a
	distance from the 51 normal batches (grey) at that sample, in their standard deviations,
	so the zero line is the average batch. Left: the conversion of batch 37 (aqua), observed
	for 30 samples, and the forecasts from sample 30 onwards (dashed aqua) and from sample 60
	onwards (dotted dark blue); what batch 37 did is the faint line. Right: the cooling-water
	temperature of batch 34 (orange) with the forecasts from sample 60 onwards (dashed
	orange) and from sample 115 onwards (dotted dark blue); the impurity enters at sample 100.
	A vertical line joins each forecast to the observed value at the sample it was made from:
	the forecast uses the batch's own data up to that sample, then continues along the
	model's components.

It is the same distinction as the two statistics. The model can forecast along its
components, so it forecasts the slow conversion of batch 37 from sample 30 onwards; the fault
of batch 34 lies off them, so the forecasts follow the average batch, and the model can flag
the fault but cannot forecast it.

Both faults are found with more than half the batch still to run, and the statistic that
finds each says which kind it is: a large :math:`T^2` with a small residual is a batch far
along a known direction, a large residual with a small :math:`T^2` is a batch doing
something the reference set never did. What the section rests on is the reference set. It
was easy to choose here, because the simulation says which batches are faulty; on plant
data the reference batches are the first thing to get right, and the
:ref:`first case study <APPS_batch_case_dupont>` shows how much of the work that is.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~

* Paul Nomikos, `Statistical process control of batch processes <https://literature.learnche.org/item/154/statistical-process-control-of-batch-processes>`_,
  Ph.D thesis, McMaster University, 1995. The source of the simulation and of the two
  faulty batches.

* Paul Nomikos and John F. MacGregor, "`Multi-way partial least squares in monitoring batch
  processes <https://literature.learnche.org/item/32/multi-way-partial-least-squares-in-monitoring-batch-processes>`_",
  *Chemometrics and Intelligent Laboratory Systems*, **30**, 97-108, 1995.

* Theodora Kourti, Paul Nomikos and John F. MacGregor, "`Analysis, monitoring and fault
  diagnosis of batch processes using multiblock and multiway PLS <https://literature.learnche.org/item/33/analysis-monitoring-and-fault-diagnosis-of-batch-processes-using-multiblock-and-multiway-pls>`_",
  *Journal of Process Control*, **5**, 277-284, 1995.

* Paul Nomikos and John F. MacGregor, "`Multivariate SPC charts for monitoring batch
  processes <https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_",
  *Technometrics*, **37**, 41-59, 1995. The on-line monitoring scheme, with the statistics
  compared with their limits at every sample.

* Salvador Garcia-Munoz, Theodora Kourti and John F. MacGregor, "`Model predictive
  monitoring for batch processes <https://doi.org/10.1021/ie034020w>`_", *Industrial and
  Engineering Chemistry Research*, **43**, 5929-5941, 2004. Trimmed score regression for the
  batch so far.

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process
  modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_",
  *Comprehensive Chemometrics*, **2.10**, 163-197, 2009. Mid-batch prediction of quality and
  of the remaining trajectories.

* The full list of readings on batch data is on the
  :ref:`batch process monitoring <APPS_batch_monitoring>` page.
