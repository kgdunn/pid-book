.. _APPS_batch_case_sbr:

Diagnosing a known fault with batch PLS: the SBR reactor
=========================================================

.. index::
	single: batch data; SBR reactor case study
	pair: batch PLS; fault diagnosis
	pair: contribution plots; batch PLS
	single: simulated data; batch reactor

Styrene-butadiene rubber (SBR) is made by emulsion polymerization in a batch reactor. Six
trajectories of the reactor are used here: the reactor, cooling-water and jacket temperatures, the
latex density, the conversion, and the energy released.

Five quality attributes of the latex are measured at the end: composition, particle size, branching,
cross-linking and polydispersity. Branching and cross-linking are one measurement in two units, in a
fixed ratio, so the quality block carries four independent attributes rather than five.

The 53 batches were simulated from a first-principles model of the reactor (Nomikos and
MacGregor, 1994; Nomikos, 1995), so the fault is known. Batch 37 received 30% more organic
impurity in the butadiene feed from its very start, batch 34 received 50% more from midway
through.
Simulated data lets a model be checked against what is known to have happened, before it is
trusted on plant data.

The :ref:`first case study <APPS_batch_case_dupont>` used a PCA of the trajectories alone.
Here final quality is available too, so the model is a :ref:`PLS <SECTION_PLS>` from the
unfolded trajectories to the five attributes. Three questions are asked of it:

* Does it single out the two faulty batches?
* Does it say what went wrong, and when?
* Could it have said so while they were still running?

The data
~~~~~~~~

The `SBR batch reactor dataset <https://openmv.net/info/sbr-batch-reactor>`_ is a workbook of two
sheets: the trajectories of 53 batches over 200 samples, and the quality attributes, one row per
batch.

Three of its nine trajectories, the two feed flow rates and the feed temperature, carry only the
noise the simulation adds and nothing that differs between batches. Scaled to unit variance they
would weigh as much as the informative ones, so the model uses the six trajectories of the reactor
itself, which ``load_sbr`` reads from the workbook.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.batch import (
	    BatchMonitor, BatchPLS, contribution_at_time_plot, load_sbr,
	    online_monitoring_plot, time_varying_loading_plot, unfolded_contribution_plot)
	from process_improve.multivariate import PLS
	from process_improve.univariate import median_absolute_deviation

	# https://openmv.net/file/sbr-batch-reactor.xlsx
	sbr = load_sbr()
	trajectories = {batch_id: batch[sbr.trajectory_tags]
	                for batch_id, batch in sbr.X.items()}
	quality = sbr.Y
	print(len(trajectories), "batches;", sbr.trajectory_tags,
	      "; quality block", quality.shape)
	# 53 batches; ['ReactorTemp', 'CoolingTemp', 'JacketTemp', 'LatexDensity',
	# 'Conversion', 'EnergyReleased'] ; quality block (53, 5)

	ratio = quality["CrossLinking"] / quality["Branching"]
	print(f"CrossLinking / Branching: {ratio.min():.3f} to {ratio.max():.3f}")
	# CrossLinking / Branching: 3.877 to 3.878

.. code-block:: python

	# figure colours
	GREY, ORANGE, AQUA, BLUE, PURPLE = "#c8c8c8", "#c55a11", "#1baf7a", "#1f3d7a", "#6f42c1"

	def overlay(batches, tag, highlight):
	    """One tag for every batch in grey, with the batches in `highlight` (id -> colour)
	    drawn on top."""
	    fig = go.Figure()
	    for batch_id, batch in batches.items():
	        if batch_id not in highlight:
	            fig.add_trace(go.Scatter(y=batch[tag], mode="lines",
	                                     line=dict(color=GREY, width=1), showlegend=False))
	    for batch_id, colour in highlight.items():
	        fig.add_trace(go.Scatter(y=batches[batch_id][tag], mode="lines",
	                                 name=f"batch {batch_id}",
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
	drawn on top. Batch 37 converts more slowly than the others from the start. Batch 34,
	the one whose fault starts midway through, follows the others until about sample 100,
	after which its cooling-water and jacket temperatures rise above the band of the other
	batches and its energy released falls below it.

The overlay already shows both faults: batch 37 from the start, in the conversion, and
batch 34 from about sample 100, in the two service temperatures (cooling water and jacket)
and the energy released.
Neither shows in the reactor temperature, which is held within a narrow range in every
batch.

The batch PLS model
~~~~~~~~~~~~~~~~~~~

`BatchPLS <https://github.com/kgdunn/process-improve/blob/main/src/process_improve/batch/_batch_pls.py>`_ unfolds each batch batchwise into one row of 6 tags by 200 samples, 1200
columns, centres and scales every column, and fits a PLS from that row to the five quality
attributes, also centred and scaled. Two components are used. As in the first case study,
this first model is to see what is going on, not to settle the number of components; the
:ref:`predicted quality <APPS_batch_case_sbr_predicted>` section asks what the second one
buys, against the usual :ref:`cross-validation <LVM-PLS-number-of-components>`.

.. code-block:: python

	model = BatchPLS(n_components=2).fit(trajectories, quality)
	# R2 of the quality block, per component
	r2y = np.diff([0.0, *model.r2_cumulative_])
	# R2 of the trajectories, per component
	r2x = np.diff([0.0, *model.r2_per_variable_.mean(axis=0)])
	print("R2X per component:", r2x.round(3), " R2Y per component:", r2y.round(3))
	# R2X per component: [0.245 0.127]  R2Y per component: [0.653 0.069]
	spe = model.spe_.iloc[:, -1]
	t1, t2 = model.scores_.iloc[:, 0], model.scores_.iloc[:, 1]
	marked = {34: ORANGE, 37: AQUA, 4: PURPLE}
	others = [batch_id for batch_id in t1.index if batch_id not in marked]
	# The marker area is the batch's squared residual. `sizemode="area"` gives the area,
	# not the diameter, to the value; squaring spreads a factor of two in SPE over a factor
	# of four in area, and the sum of squared residuals is what adds up over the cells in
	# any case.
	area = dict(sizemode="area", sizeref=2 * (spe**2).max() / 26**2, sizemin=3)
	ex, ey = model.ellipse_coordinates(score_horiz=1, score_vert=2, conf_level=0.95)
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", name="95% confidence ellipse",
	                         line=dict(color=GREY, dash="dash")))
	fig.add_trace(go.Scatter(x=t1.loc[others], y=t2.loc[others], mode="markers",
	                         showlegend=False, text=others, hovertemplate="batch %{text}",
	                         marker=dict(size=spe.loc[others] ** 2, color=BLUE, **area)))
	for batch_id, colour in marked.items():
	    fig.add_trace(go.Scatter(x=[t1.loc[batch_id]], y=[t2.loc[batch_id]], mode="markers",
	                             name=f"batch {batch_id}",
	                             marker=dict(size=[spe.loc[batch_id] ** 2],
	                                         color=colour, **area,
	                                         line=dict(color="#404040", width=1.5))))
	fig.update_layout(xaxis_title=f"t1 [R2X {r2x[0]:.1%}]",
	                  yaxis_title=f"t2 [R2X {r2x[1]:.1%}]", height=520).show()
	print(f"SPE rank of batch 37: {int(spe.rank().loc[37])} of {len(spe)};",
	      f"batch 34: {int(spe.rank().loc[34])}")            # 1 = the smallest residual
	# SPE rank of batch 37: 1 of 53; batch 34: 12
	print(f"t1 rank of batch 37: {int(t1.rank().loc[37])} of {len(t1)};",
	      f"t2 rank of batch 34: {int(t2.rank().loc[34])}")   # 1 = the lowest score
	# t1 rank of batch 37: 1 of 53; t2 rank of batch 34: 53
	# the batch nearest the average quality
	standardised = (quality - quality.mean()) / quality.std(ddof=1)
	distance = (standardised ** 2).sum(axis=1).pow(0.5) / np.sqrt(quality.shape[1])
	print("nearest the average quality:", distance.nsmallest(2).round(2).to_dict())
	# nearest the average quality: {4: 0.16, 27: 0.26}
	for batch_id in (34, 37):
	    t2_end = model.hotellings_t2_.loc[batch_id].iloc[-1]
	    spe_end = model.spe_.loc[batch_id].iloc[-1]
	    t2_lim = model.hotellings_t2_limit(conf_level=0.95)
	    spe_lim = model.spe_limit(conf_level=0.95)
	    print(f"batch {batch_id}: T2 = {t2_end:.1f} (limit {t2_lim:.1f}),",
	          f"SPE = {spe_end:.1f} (limit {spe_lim:.1f})")
	    # batch 34: T2 = 28.2 (limit 6.6), SPE = 23.1 (limit 34.6)
	    # batch 37: T2 = 19.2 (limit 6.6), SPE = 18.7 (limit 34.6)

The first component explains 65.3% of the variance in the quality block and the second
6.9%; their shares of the variance in the trajectories are on the axes of the score plot.

.. figure:: ../figures/batch/batch-case-sbr-scores.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Scores of the batch PLS model with the 95% confidence ellipse, each marker's area set by the batch's squared residual; batch 37 has the lowest t1 of all batches and batch 34 the highest t2, both far outside the ellipse and both drawn small; batch 4, in purple, sits near the centre.
	:width: 600px
	:scale: 80
	:align: center

	Scores of the batch PLS model. Batch 37 (aqua) has the lowest :math:`t_1` of all
	batches and batch 34 (orange) the highest :math:`t_2`; both lie far outside the 95%
	confidence ellipse. The area of each marker is that batch's squared residual, on the scale
	of the three grey circles in the legend, so the plot answers both questions asked of a
	batch: the two faulty ones are extreme along the components and carry small residuals.
	Batch 4 (purple)
	is the batch nearest the average quality, used
	:ref:`below <APPS_batch_case_sbr_online_prediction>` to show the prediction while the
	batch runs.

What the plot cannot show is that both faulty batches are inside this fit. Each is extreme
along a component that its own deviation helped to define, which is why the fault lands in
the scores and leaves so little in the residual, and why the two largest values of
:math:`T^2` (:ref:`Hotelling's statistic <LVM-Hotellings-T2>`) belong to two of the smallest
residuals. The 95% limits inherit the same circularity, since they are computed from the 53
batches that include the two faults being judged.

The SPE answers the other question about a batch, how far it sits away from the components.
Drawing it against :math:`T^2` puts both questions in one figure, each axis carrying its own
95% limit.

.. code-block:: python

	def influence_plot(model, highlight, labels, conf_level=0.95):
	    """Hotelling's T2 against SPE, one dot per batch, with both limits drawn."""
	    t2, spe = model.hotellings_t2_.iloc[:, -1], model.spe_.iloc[:, -1]
	    others = [batch_id for batch_id in t2.index if batch_id not in highlight]
	    fig = go.Figure()
	    fig.add_trace(go.Scatter(x=t2.loc[others], y=spe.loc[others], mode="markers",
	                             showlegend=False, marker=dict(size=8, color=BLUE),
	                             text=others, hovertemplate="batch %{text}"))
	    for batch_id, colour in highlight.items():
	        fig.add_trace(go.Scatter(x=[t2.loc[batch_id]], y=[spe.loc[batch_id]],
	                                 mode="markers", name=f"batch {batch_id}",
	                                 marker=dict(size=12, color=colour)))
	    fig.add_vline(x=model.hotellings_t2_limit(conf_level=conf_level),
	                  line_dash="dash", line_color=GREY)
	    fig.add_hline(y=model.spe_limit(conf_level=conf_level),
	                  line_dash="dash", line_color=GREY)
	    for batch_id in labels:
	        fig.add_annotation(x=t2.loc[batch_id], y=spe.loc[batch_id], text=str(batch_id),
	                           showarrow=False, xshift=13, yshift=9)
	    fig.update_layout(xaxis_title="Hotelling's T\u00b2", yaxis_title="SPE", height=420)
	    return fig

	spe, t2 = model.spe_.iloc[:, -1], model.hotellings_t2_.iloc[:, -1]
	above_spe = sorted(spe.index[spe > model.spe_limit(conf_level=0.95)])
	print("above the SPE limit:", above_spe, "  above the T2 limit:",
	      sorted(t2.index[t2 > model.hotellings_t2_limit(conf_level=0.95)]))
	# above the SPE limit: [8, 15, 16]   above the T2 limit: [34, 37]
	influence_plot(model, highlight={34: ORANGE, 37: AQUA},
	               labels=[34, 37, *above_spe]).show()

.. figure:: ../figures/batch/batch-case-sbr-influence.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Hotelling's T2 against SPE for the 53 batches, with both 95% limits; batches 34 and 37 are far to the right beyond the T2 limit and below the SPE limit, while batches 8, 15 and 16 are in the upper left at or above the SPE limit.
	:width: 620px
	:scale: 80
	:align: center

	Hotelling's :math:`T^2` against the SPE for every batch, with both 95% limits. Batches 34
	(orange) and 37 (aqua) are far to the right and below the SPE limit. The batches the SPE
	flags, 8, 15 and 16, are different batches, in the upper left.

A 95% limit is crossed by about three of 53 batches when nothing is wrong, so the three the SPE
flags are what the limit allows, not evidence of a fault.

The figure cannot show why the two known faults are not among them. The SPE sums the residuals of
all 1200 cells of a batch after the components have taken their share. A deviation along a component
is absorbed by the scores, and a deviation confined to a few cells is small against a sum over 1200.

The scores say a batch moved in a direction the model knows; the SPE, that it moved in one the model
does not.

Where the model explains the trajectories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every unfolded column has its own :math:`R^2`, so the fit reads per tag and per time sample.
So do the weights :math:`\mathbf{w}_1` and :math:`\mathbf{w}_2`, each a vector of 1200
entries, which ``time_varying_loading_plot`` draws as six curves over the batch. PLS weights
play the role PCA loadings do, and :ref:`how the PLS model is calculated
<LVM_PLS_calculation>` explains the difference. The contribution plots later on the page are
built from the direct weights :math:`\mathbf{W}(\mathbf{P}'\mathbf{W})^{-1}`, the combination
the PLS chapter prefers for interpretation, rather than the :math:`\mathbf{w}` drawn here.

.. code-block:: python

	# rows = tags, columns = time
	r2_grid = model.r2_per_variable_.iloc[:, -1].unstack(level="sequence")
	fig = go.Figure()
	for tag, row in r2_grid.iterrows():
	    fig.add_trace(go.Scatter(x=row.index, y=row.values, mode="lines", name=tag))
	fig.update_layout(title="R2 of each (tag, time) cell after two components",
	                  xaxis_title="Sample [aligned time]", yaxis_title="R2", height=360)
	fig.show()
	print("R2 per tag, averaged over time:", r2_grid.mean(axis=1).round(2).to_dict())
	# R2 per tag, averaged over time: {'Conversion': 0.75, 'CoolingTemp': 0.23,
	# 'EnergyReleased': 0.26, 'JacketTemp': 0.24, 'LatexDensity': 0.67,
	# 'ReactorTemp': 0.08}
	time_varying_loading_plot(model, component=1).show()
	time_varying_loading_plot(model, component=2).show()

.. _APPS_batch_case_sbr_r2:

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

Latex density and conversion are the trajectories the model uses most, with an :math:`R^2`
averaged over the batch of 0.67 and 0.75, against 0.23 to 0.26 for the two service
temperatures and the energy released, and 0.08 for the reactor temperature. Every curve is
low at the start. All batches begin alike, so after centring and scaling the first samples
hold little but noise.

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

The weights say what a score means:

* a low :math:`t_1` is a below-average latex density and conversion throughout the batch;
* a high :math:`t_2` is cooling-water and jacket temperatures above their average
  trajectories over the second half, with the energy released, the latex density and the
  conversion below theirs, and the reactor temperature carrying weights that change sign from
  sample to sample, so the component says nothing consistent about it.

A component says these tags move together, not which of them drives the others. Those are
predictions about batches 37 and 34 respectively, and the contribution plots test them.

Batch 37: the fault from the start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	# the 53 x 1200 matrix the model was fitted on
	scaled = model.unfold_and_scale(trajectories)
	t1 = model.score_contributions(scaled, component=1)
	unfolded_contribution_plot(t1, batch_id=37).show()
	unfolded_contribution_plot(t1, batch_id=37, by_tag=True).show()
	print("batch 37, t1 contributions per tag:",
	      t1.loc[37].groupby(level="tag", sort=False).sum().round(1).to_dict())
	# batch 37, t1 contributions per tag: {'Conversion': -33.4, 'CoolingTemp': -4.2,
	# 'EnergyReleased': -5.2, 'JacketTemp': -4.3, 'LatexDensity': -25.5,
	# 'ReactorTemp': -1.3}

	def share_per_fifth(row):
	    """Split a contribution vector into five equal time blocks and give each block's
	    share of the total."""
	    by_time = row.groupby(level="sequence").sum()
	    fifths = by_time.groupby(np.arange(len(by_time)) * 5 // len(by_time)).sum()
	    return (fifths / fifths.sum()).round(2).tolist()

	print("batch 37: share of the t1 contribution per fifth of the batch:",
	      share_per_fifth(t1.loc[37]))
	# batch 37: share of the t1 contribution per fifth of the batch:
	# [0.15, 0.18, 0.19, 0.26, 0.22]

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

Batch 37 sits at the low end of :math:`t_1` because its conversion and latex density were
below average, and the contribution is spread over the whole batch. Each fifth carries
between 15% and 26% of the total, which is what a fault present from the start looks like.
The :ref:`raw trajectory overlay <APPS_batch_case_sbr_overlay>` agrees. The impurity slowed
the reaction from the moment the batch began.

Batch 34: the same fault, from the middle of the batch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	t2 = model.score_contributions(scaled, component=2)
	unfolded_contribution_plot(t2, batch_id=34).show()
	contribution_at_time_plot(t2, k=120, batch_id=34).show()
	print("batch 34, t2 contributions per tag:",
	      t2.loc[34].groupby(level="tag", sort=False).sum().round(1).to_dict())
	# batch 34, t2 contributions per tag: {'Conversion': 8.1, 'CoolingTemp': 12.2,
	# 'EnergyReleased': 14.3, 'JacketTemp': 12.3, 'LatexDensity': 7.2,
	# 'ReactorTemp': 4.0}
	print("batch 34: share of the t2 contribution per fifth of the batch:",
	      share_per_fifth(t2.loc[34]))
	# batch 34: share of the t2 contribution per fifth of the batch:
	# [0.06, 0.09, 0.17, 0.39, 0.29]

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
temperatures, with the conversion and latex density behind them. Timing distinguishes it
from batch 37. The first two fifths of the batch carry 15% of the :math:`t_2` contribution
and the last two fifths 68%. ``contribution_at_time_plot`` shows the same three tags
carrying the deviation at sample 120.

The raw data can be asked the same question directly, tag by tag: at which sample does each
trajectory of a faulty batch leave the band of the other batches?

The code below answers that for batches 34 and 37. Each tag becomes a :math:`z` value at every
sample: a distance from a centre, divided by a spread, both taken from the 51 batches with no known
fault. Two versions are shown:

* classical: centred on the mean of those 51 at that sample, divided by their standard   deviation;
* robustified: centred on their median, divided by their median absolute deviation, scaled to
  agree with the standard deviation on normally distributed values, then :ref:`EWMA-smoothed
  <monitoring_EWMA>`.

A tag has left the band when its :math:`z` value stays beyond plus or minus two for 20 samples in a
row, a tenth of the batch.

Twenty samples is longer than the reactor temperature ever stays outside the band in a normal
batch, but not longer than the other tags do: the latex density and the conversion of a normal
batch can stay outside it for 50 samples or more. A sustained departure therefore says where
to look, not that there is a fault.

.. code-block:: python

	others = np.stack([batch.to_numpy() for batch_id, batch in trajectories.items()
	                   if batch_id not in (34, 37)])
	z = {batch_id: (trajectories[batch_id].to_numpy() - others.mean(axis=0))
	               / others.std(axis=0, ddof=1)
	     for batch_id in (37, 34)}
	# 1.4826 x MAD
	spread = median_absolute_deviation(others, axis=0, scale="normal")
	# EWMA-smoothed
	z_robust = {batch_id: pd.DataFrame((trajectories[batch_id].to_numpy()
	                                    - np.median(others, axis=0)) / spread)
	            .ewm(alpha=0.3, adjust=False).mean().to_numpy()
	            for batch_id in (37, 34)}

	def sustained_departure(z_batch, n_sd=2.0, run=20):
	    """First sample, counting from one, from which each tag stays more than `n_sd`
	    scale units away for `run` samples."""
	    # 1 where the tag is outside the band, 0 inside
	    outside = (np.abs(z_batch) > n_sd).astype(int)
	    onset = {}
	    for j, tag in enumerate(sbr.trajectory_tags):
	        # Convolving the 0/1 column with `run` ones is a moving sum over every
	        # window of `run` consecutive samples: entry i is how many of samples i to
	        # i+run-1 lie outside the band. "valid" keeps only the windows that fit
	        # entirely inside the batch, so entry i starts at sample i. A window summing
	        # to `run` is an unbroken stretch, and argmax finds the first True, which is
	        # the sample the stretch starts at. The +1 counts samples from one, as the
	        # rest of the page does. Without a True, argmax returns 0, so test `any()`
	        # first and report None instead.
	        runs = np.convolve(outside[:, j], np.ones(run, dtype=int), mode="valid") == run
	        onset[tag] = int(runs.argmax()) + 1 if runs.any() else None
	    return onset

	for batch_id in (37, 34):
	    print(f"batch {batch_id}, first sustained departure:",
	          sustained_departure(z[batch_id]))
	    # batch 37, first sustained departure: {'ReactorTemp': None, 'CoolingTemp': None,
	    # 'JacketTemp': None, 'LatexDensity': 14, 'Conversion': 10,
	    # 'EnergyReleased': None}
	    # batch 34, first sustained departure: {'ReactorTemp': None, 'CoolingTemp': 104,
	    # 'JacketTemp': 105, 'LatexDensity': 130, 'Conversion': 124,
	    # 'EnergyReleased': 106}
	    print("  robust, smoothed:", sustained_departure(z_robust[batch_id]))
	    #   robust, smoothed: {'ReactorTemp': None, 'CoolingTemp': 1, 'JacketTemp': 1,
	    #   'LatexDensity': 16, 'Conversion': 1, 'EnergyReleased': None}
	    #   robust, smoothed: {'ReactorTemp': None, 'CoolingTemp': 106,
	    #   'JacketTemp': 108, 'LatexDensity': 135, 'Conversion': 127,
	    #   'EnergyReleased': 108}

	# Why 20: it has to outlast what the noise alone produces, and the answer must not
	# depend on it.
	def longest_run(flags):
	    """Length of the longest unbroken stretch of True."""
	    best = current = 0
	    for flag in flags:
	        current = current + 1 if flag else 0
	        best = max(best, current)
	    return best

	quiet = [np.abs((batch.to_numpy() - others.mean(axis=0))
	                / others.std(axis=0, ddof=1)) > 2
	         for batch_id, batch in trajectories.items() if batch_id not in (34, 37)]
	print("longest run outside the band with no fault:",
	      {tag: max(longest_run(batch[:, j]) for batch in quiet)
	       for j, tag in enumerate(sbr.trajectory_tags)})
	# longest run outside the band with no fault: {'ReactorTemp': 9, 'CoolingTemp': 36,
	# 'JacketTemp': 37, 'LatexDensity': 51, 'Conversion': 72, 'EnergyReleased': 18}
	print("run lengths giving the same onsets:",
	      [run for run in (15, 20, 25, 30, 40)
	       if all(sustained_departure(z[b], run=run) == sustained_departure(z[b])
	              for b in (37, 34))])
	# run lengths giving the same onsets: [20, 25, 30, 40]

	fig = make_subplots(rows=2, cols=6, subplot_titles=sbr.trajectory_tags,
	                    shared_yaxes=True)
	for row, (batch_id, colour) in enumerate([(37, AQUA), (34, ORANGE)], start=1):
	    for col in range(6):
	        # signed distances, not their absolute value: the sign says whether the tag
	        # ran above or below the others
	        fig.add_trace(go.Scatter(y=z_robust[batch_id][:, col], mode="lines",
	                                 name=f"batch {batch_id}, robust",
	                                 line=dict(color=colour, width=1.5),
	                                 showlegend=(col == 0)),
	                      row=row, col=col + 1)
	        fig.add_trace(go.Scatter(y=z[batch_id][:, col], mode="lines",
	                                 name=f"batch {batch_id}, mean and sd",
	                                 line=dict(color=colour, width=1, dash="dash"),
	                                 showlegend=(col == 0)),
	                      row=row, col=col + 1)
	        fig.add_hrect(y0=-2, y1=2, fillcolor=GREY, opacity=0.15, line_width=0,
	                      row=row, col=col + 1)
	        for level in (-2, 2):
	            fig.add_hline(y=level, line_dash="dot", line_color=GREY,
	                          row=row, col=col + 1)
	title = "Distance from the other batches: robust (solid) and mean-and-sd (dashed)"
	fig.update_layout(title=title, height=420)
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

Batch 37 leaves the band in the conversion and latex density within the first 20 samples and
stays out. Batch 34 leaves it midway, first in the two service temperatures and the energy
released, then some 20 samples later in the conversion and latex density. The robust distance
moves batch 34's onsets by two to five samples, and for batch 37 it also puts the
cooling-water and jacket temperatures outside the band from the first sample, where the
standard-deviation distance never holds them there long enough to count. This demonstrates the
added value of robust methods.

One fault, two places in the score plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same kind of fault appears in two places of the score plot because it started at two
different times. A batch model describes deviations in (tag, time) cells, so the time of an
event is part of its signature: a slow reaction from the start deviates along
:math:`\mathbf{w}_1`, one from the middle of the batch along :math:`\mathbf{w}_2`. The size of
the fault sets how far along that direction the batch lies, and the two differ there too: 30%
more impurity in batch 37 against 50% in batch 34.

That makes batch models useful for diagnosis, and is also a caution. A library of known faults
built in score space needs the onset time as a coordinate, since a fault seen at one onset
appears as a new fault at another. The :ref:`on-line section <APPS_batch_case_sbr_online>`
returns to both batches with a model that has seen neither fault, where the two places become
two statistics.

.. _APPS_batch_case_sbr_predicted:

Predicted quality
~~~~~~~~~~~~~~~~~

A PLS model predicts the quality attributes as well, and the predicted quality of the two
faulty batches, from a model fitted without each of them, shows what the trajectories knew
before the laboratory did.

.. code-block:: python

	# RMSEE measures the fitted values. RMSEP is the same error when each batch in turn
	# is left out of the fit and predicted by a model that never saw it: the loop takes
	# about two minutes. Both component counts are fitted in the same pass, to see what
	# the second one buys.
	rmsee = np.sqrt(((quality - model.predictions_) ** 2).mean())
	held_out, held_out_one = {}, {}
	for batch_id in trajectories:
	    rest = {b: t for b, t in trajectories.items() if b != batch_id}
	    left_out, target = {batch_id: trajectories[batch_id]}, quality.loc[list(rest)]
	    for components, store in ((2, held_out), (1, held_out_one)):
	        model_without = BatchPLS(n_components=components).fit(rest, target)
	        store[batch_id] = model_without.predict(left_out).y_hat.loc[batch_id]
	held_out = pd.DataFrame(held_out).T
	rmsep = np.sqrt(((held_out - quality) ** 2).mean())
	rmsep_one = np.sqrt(((pd.DataFrame(held_out_one).T - quality) ** 2).mean())
	sd = quality.std(ddof=1)
	for variable in ("Composition", "ParticleSize"):
	    fitted = rmsee[variable]
	    print(f"{variable}: RMSEE {fitted:.3g} ({fitted / sd[variable]:.2f} sd),",
	          f"RMSEP {rmsep[variable]:.3g} ({rmsep[variable] / sd[variable]:.2f} sd)")
	# Composition: RMSEE 0.00106 (0.71 sd), RMSEP 0.00122 (0.81 sd)
	# ParticleSize: RMSEE 1.87 (0.60 sd), RMSEP 2.42 (0.78 sd)
	print("RMSEP / sd, one component: ", (rmsep_one / sd).round(2).to_dict())
	# RMSEP / sd, one component:  {'Composition': 0.8, 'ParticleSize': 0.87,
	# 'Branching': 0.28, 'CrossLinking': 0.28, 'Polydispersity': 0.67}
	print("RMSEP / sd, two components:", (rmsep / sd).round(2).to_dict())
	# RMSEP / sd, two components: {'Composition': 0.81, 'ParticleSize': 0.78,
	# 'Branching': 0.28, 'CrossLinking': 0.28, 'Polydispersity': 0.73}
	# The RMSEP says by how far the model misses; the cross-validated R2 says how much
	# of the attribute it predicts. Five folds over whole batches, which takes about 40
	# seconds.
	unfolded = pd.DataFrame({b: t.to_numpy().ravel(order="F")
	                         for b, t in trajectories.items()}).T
	q2 = PLS.select_n_components(unfolded, quality.loc[unfolded.index], max_components=2,
	                             cv=5, random_state=0).r2y_validated.loc[2]
	print("Q2 per attribute:", q2[quality.columns].round(3).to_dict())
	# Q2 per attribute: {'Composition': 0.322, 'ParticleSize': 0.339, 'Branching': 0.914,
	# 'CrossLinking': 0.914, 'Polydispersity': 0.476}
	for variable in ("Composition", "ParticleSize"):
	    error = rmsep[variable]
	    fig = model.predictions_vs_observed_plot(quality, variable=variable)
	    fig.add_annotation(xref="paper", yref="paper", x=0.02, y=0.98,
	                       showarrow=False, align="left",
	                       text=f"RMSEP {error:.3g} ({error / sd[variable]:.2f} sd)"
	                            f"<br>Q² {q2[variable]:.3f}")
	    lo, hi = quality[variable].min(), quality[variable].max()
	    half = 2 * rmsep[variable]
	    # Two prediction errors either side of y = x, as a shape rather than a trace so that
	    # `layer="below"` keeps it behind the batches it is there to be read against.
	    fig.add_shape(type="path", layer="below", line_width=0,
	                  fillcolor="rgba(31, 61, 122, 0.10)",
	                  path=f"M {lo},{lo - half} L {hi},{hi - half}"
	                       f" L {hi},{hi + half} L {lo},{lo + half} Z")
	    fig.show()
	faulty = [34, 37]
	# Where the measured value ranks among the 53 batches, and where the prediction from
	# a model that never saw the batch ranks among the 53 predictions. Rank 1 is the
	# lowest.
	observed_rank, held_out_rank = quality.rank().astype(int), held_out.rank().astype(int)
	moves = pd.DataFrame({attribute: [f"{observed_rank.loc[b, attribute]} to"
	                                  f" {held_out_rank.loc[b, attribute]}"
	                                  for b in faulty]
	                      for attribute in quality.columns},
	                     index=[f"batch {b}" for b in faulty])
	print(moves.to_string())
	#          Composition ParticleSize Branching CrossLinking Polydispersity
	# batch 34     5 to 26       1 to 1    4 to 2       4 to 2        17 to 2
	# batch 37      4 to 1       2 to 2    1 to 1       1 to 1         1 to 1
	shift = (model.scores_.loc[faulty] * model.y_loadings_.loc["Composition"]).round(2)
	print("shift of the scaled composition per component:", shift.to_dict("index"))
	# shift of the scaled composition per component:
	# {34: {1: -1.39, 2: 0.99}, 37: {1: -2.89, 2: -0.14}}

.. figure:: ../figures/batch/batch-case-sbr-observed-vs-fitted.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Observed against fitted composition and particle size for the 53 batches with batches 34 and 37 marked; both faulty batches lie at the low end of both attributes, a band of two RMSEP is shaded either side of the y = x line, and each panel's legend lists its RMSEE, RMSEP and cross-validated R-squared.
	:width: 900px
	:scale: 80
	:align: center

	Observed against fitted composition (left) and particle size (right) for the 53 batches,
	with batches 34 (orange) and 37 (aqua) marked. Each panel lists two errors: RMSEE, the
	scatter of these fitted values about the :math:`y = x` line, and RMSEP, the same scatter
	when every batch is left out of the fit in turn, each in the attribute's own units and in
	standard deviations of it. Beside them is :math:`Q^2`, the cross-validated :math:`R^2` of
	that attribute: the errors say by how far the model misses, :math:`Q^2` how much of the
	attribute it predicts. The shaded band is two RMSEP either side of the line: the scatter to
	expect from a batch the model has not seen, and so wider than the scatter of the fitted values
	drawn here.

The two components explain 72% of the quality block when they are fitted to it. What they
predict in a batch they have not seen is the :math:`Q^2` beside each error, and the two
numbers carry the same information.

Write the prediction error as a fraction of the attribute's own standard deviation
:math:`s`, so :math:`f = \text{RMSEP}/s`. Predicting the average of every batch would give
:math:`f = 1`, and a model is worth having only below that. Squaring gives the share of the
variance the predictions still miss, :math:`f^2`, and what remains is the share the model
accounts for:

.. math::

	Q^2 \approx 1 - f^2

Both attributes here miss by about 0.8 standard deviations, so :math:`f^2` is about 0.64:
that is the share of the variance still missed, leaving :math:`1 - 0.64 = 0.36`, about a third
of each attribute predicted.

The relation is approximate, and writing both quantities over the same sums of squares shows
why. Both are built from the prediction error sum of squares, PRESS, against the total sum of
squares of the attribute, TSS:

.. math::

	Q^2 = 1 - \frac{\text{PRESS}}{\text{TSS}}
	\qquad\text{and}\qquad
	f^2 = \left(\frac{\text{RMSEP}}{s}\right)^2
	    = \frac{\text{PRESS}}{\text{TSS}} \cdot \frac{N-1}{N}

The two therefore differ by the factor :math:`(N-1)/N`, which is 52/53 here: the RMSEP divides
by :math:`N` and the standard deviation :math:`s` by :math:`N-1`. A second, larger difference
is deliberate: the RMSEP leaves out one batch at a time while the :math:`Q^2` uses five folds.

Composition and particle size are the two attributes the model predicts least well: branching
and cross-linking reach 0.91 and polydispersity 0.48.

The second component earns almost nothing in prediction: leaving each batch out and refitting
with one component gives the same average error over the five attributes, buying particle size
(0.87 down to 0.78) and losing polydispersity (0.67 up to 0.73). It is kept because it carries
the fault of batch 34, which a one-component model would push into the residual, and because a
score plot needs a second axis.

Both faulty batches were in the model, so their fitted values prove nothing on their own.
Leaving each one out and refitting is the test: batch 37 is measured lowest of the 53 on
branching, cross-linking and polydispersity, and a model that never saw it predicts it lowest
on all three. Either batch would have been flagged from the trajectories alone, before the
laboratory results arrived.

Batch 34 is the interesting one, because one attribute does not follow.

==============  ====================  =======================
Attribute       Measured rank, of 53  Held-out predicted rank
==============  ====================  =======================
Composition     5                     26
Particle size   1                     1
Polydispersity  17                    2
==============  ====================  =======================

Where batch 34 sits among the 53, rank 1 the lowest value, measured and as predicted by a
model fitted on the other 52. Branching and cross-linking are left out: they are one
measurement in two units, so they repeat the particle-size row exactly.

Composition is the exception, and the reason is in the scores rather than in the fault. Batch
34's two scores move its composition in opposite directions, :math:`t_1` by 1.4 standard
deviations down and :math:`t_2` by 1.0 up, so the prediction lands mid-pack while the
measurement sits near the bottom. A component's share of the quality block says how much it
explains across all batches, not how far it moves any one of them.

.. _APPS_batch_case_sbr_online_prediction:

Predicting quality before the batch ends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The fitted values of the previous section used the whole batch. It is far more interesting
if it is possible to predict what its final quality will be while the batch is still
running:

* the unfolded row is complete up to the current sample and empty after it, so the scores are
  estimated from the observed cells alone, the rest treated as missing data (Wold and
  co-workers, 2009, who set out the projection to the model plane and point to the literature
  for the other estimators);
* the model's regression from scores to quality turns those scores into a prediction;
* the prediction error after :math:`k` samples, RMSEP, comes from refitting without each
  batch in turn and tracing the held-out batch (``online_rmse``, about a minute).

The estimator used here is trimmed score regression (Arteaga and Ferrer, 2002), which García-Muñoz,
Kourti and MacGregor (2004) found stable from the first samples of a batch. Applying the loadings of
the measured cells to those cells alone gives a *trimmed score*: the score the row would have if
every cell still to come sat at its average.

It is biased, so the same trimming is done to every training batch, where the score from the
complete row is known as well, and those true scores are regressed on the trimmed ones. Applying
that regression to the new row is the estimate.

Fitting the regression over history is what keeps it steady early. While few cells have been
measured they say little about the final scores, the coefficients are small, and the estimate
stays near the average batch; as more cells arrive the same regression carries it out to
where the batch is.

.. code-block:: python

	squared = 0
	# leave one batch out: about a minute
	for held_out in trajectories:
	    rest = {b: t for b, t in trajectories.items() if b != held_out}
	    model_wo = BatchPLS(n_components=2).fit(rest, quality.loc[list(rest)])
	    squared = squared + model_wo.online_rmse({held_out: trajectories[held_out]},
	                                             quality.loc[[held_out]]) ** 2
	# after 1, 2, ..., 200 samples
	rmsep_k = np.sqrt(squared / len(trajectories))
	relative = rmsep_k / quality.std()
	at = [10, 25, 50, 150, 200]
	# RMSEP / sd averaged over the five attributes
	print(relative.loc[at].mean(axis=1).round(2).tolist())
	# [0.97, 0.89, 0.8, 0.62, 0.58]
	# The sample from which each curve stays below one standard deviation, which is not the
	# first sample it dips below: a curve that crosses and comes back has not settled.
	stays = {a: int(relative.index[np.flatnonzero((relative[a] >= 1).to_numpy())[-1] + 1])
	         if (relative[a] >= 1).any() else 1 for a in relative.columns}
	print("stays below the standard deviation from sample:", stays)
	# stays below the standard deviation from sample: {'Composition': 1,
	# 'ParticleSize': 125, 'Branching': 2, 'CrossLinking': 2, 'Polydispersity': 2}

	# one more figure colour
	MAGENTA = "#b03a78"
	# one per attribute; branching and cross-linking coincide, so they share aqua
	COLOURS = (BLUE, ORANGE, AQUA, AQUA, MAGENTA)
	fig = go.Figure()
	for attribute, colour in zip(quality.columns, COLOURS):
	    fig.add_trace(go.Scatter(x=relative.index[9:], y=relative[attribute].iloc[9:],
	                             name=attribute, line=dict(color=colour)))
	fig.add_hline(y=1.0, line_color=GREY, annotation_text="as good as the average batch")
	fig.update_layout(xaxis_title="Samples observed",
	                  yaxis_title="RMSEP / standard deviation of the attribute",
	                  height=420)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-online-rmse.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Four curves of the leave-one-batch-out root-mean-square error of the mid-batch prediction divided by the attribute's standard deviation against the number of samples observed, one per quality attribute except that branching and cross-linking coincide and share one line; all start just below one, the particle-size curve rises slightly above one over the first half and settles below it after about 125 samples, branching and cross-linking fall furthest, polydispersity changes little after 50 samples.
	:width: 800px
	:scale: 80
	:align: center

	Root-mean-square error of the leave-one-batch-out prediction after :math:`k` samples,
	divided by the standard deviation of each attribute. Branching and cross-linking
	coincide. A curve above 1 is worse than predicting the average batch.

No curve begins far above 1, because the estimator does not extrapolate from the few cells it
has: with little observed it falls back on the average batch, whose error is one standard
deviation by construction. What the curves show is therefore when each attribute becomes
predictable, not how badly it starts.

The particle size is the one attribute that does not settle early. Its error hovers at about one
standard deviation through the first half of the batch and stays below it only from sample 125,
where the :ref:`fit of every (tag, time) cell <APPS_batch_case_sbr_r2>` also placed the information.

Nomikos and MacGregor (1995) give the reason: particle size is set largely by the seed particles
charged before the batch starts, which the trajectories do not record. It was the attribute their
model explained least.

Kourti, Nomikos and MacGregor (1995) set out how such a block of before-the-batch measurements
enters the model beside the trajectories. The :ref:`third case study <APPS_batch_case_fmc>` does
that with two of them.

Two batches show what the curves summarise, both for the particle size: batch 4, nearest the average
quality, and batch 34, whose particle size is the lowest of the 53.

Each prediction is shown against the number of samples observed, the prediction from the complete
batch dashed and the measured value solid. The band is one prediction error at that sample, read off
the RMSEP curve; it is not a prediction interval. Unlike that curve, these two traces are of batches
the model was fitted to.

.. code-block:: python

	print("average particle size over the 53 batches:",
	      round(quality["ParticleSize"].mean(), 1))
	# average particle size over the 53 batches: 1257.1
	band = rmsep_k["ParticleSize"]
	for batch_id, colour in ((4, BLUE), (34, ORANGE)):
	    trace = model.predict_online_trace(trajectories[batch_id])
	    evolving = trace.y_hat["ParticleSize"]
	    fig = go.Figure()
	    fig.add_trace(go.Scatter(x=trace.time[4:], y=(evolving + band).iloc[4:],
	                             line=dict(width=0), showlegend=False))
	    fig.add_trace(go.Scatter(x=trace.time[4:], y=(evolving - band).iloc[4:],
	                             fill="tonexty", fillcolor="rgba(200, 200, 200, 0.35)",
	                             line=dict(width=0), name="one prediction error"))
	    fig.add_trace(go.Scatter(x=trace.time[4:], y=evolving.iloc[4:],
	                             name="prediction so far", line=dict(color=colour)))
	    fig.add_hline(y=model.predictions_.loc[batch_id, "ParticleSize"],
	                  line_dash="dash", line_color=GREY,
	                  annotation_text="final prediction")
	    fig.add_hline(y=quality.loc[batch_id, "ParticleSize"], line_color="black",
	                  annotation_text="measured")
	    # The printed figure puts the two panels on one axis; pinning the range here
	    # keeps this plot comparable with it, and the two batches with each other.
	    fig.update_layout(title=f"Batch {batch_id}: ParticleSize",
	                      xaxis_title="Samples observed", yaxis_range=[1242, 1261],
	                      height=380)
	    fig.show()
	    steps = evolving.loc[[10, 50, 100, 150]].round(1).tolist()
	    print(f"batch {batch_id}: measured {quality.loc[batch_id, 'ParticleSize']:.1f},",
	          f"final prediction {model.predictions_.loc[batch_id, 'ParticleSize']:.1f},",
	          f"after 10/50/100/150 samples {steps}")
	    # batch 4: measured 1256.9, final prediction 1257.1, after 10/50/100/150 samples
	    # [1256.8, 1256.5, 1256.4, 1257.4]
	    # batch 34: measured 1243.7, final prediction 1245.3, after 10/50/100/150 samples
	    # [1257.2, 1255.3, 1254.9, 1245.3]

	print(f"band: widest {band.max():.2f} at sample {band.idxmax()},",
	      f"narrowest {band.iloc[-1]:.2f} at the end")
	# band: widest 3.45 at sample 103, narrowest 2.42 at the end
	average = quality["ParticleSize"].mean()
	moved = (model.predict_online_trace(trajectories[34]).y_hat["ParticleSize"]
	         - average).abs()
	outside = moved > band
	print("batch 34 first sits further from the average than the band at sample",
	      int(outside.idxmax()))
	# batch 34 first sits further from the average than the band at sample 107

.. figure:: ../figures/batch/batch-case-sbr-online-prediction.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Two panels of the evolving particle-size prediction against samples observed, for batch 4 on the left and batch 34 on the right, each with a shaded band of one prediction error, a dashed line at the final prediction and a solid line at the measured value; both start at about 1257, the average, and batch 34's falls to 1245 between samples 100 and 150 while batch 4's stays where it began.
	:width: 1000px
	:scale: 80
	:align: center

	The predicted particle size as each batch is observed: batch 4 (left), nearest the average
	quality, and batch 34 (right), the lowest particle size of the 53. Dotted: the average of
	the 53 batches. Dashed: the prediction from the complete batch. Solid: the measured value.
	Band: one prediction error at that sample, the same band in both panels, centred on each
	batch's own prediction. Both predictions start on the dotted rule, because that is where
	the estimator sits at the start of the batch when no data is available. Gradually, as data
	comes in, the batch prediction changes. On the left the three rules lie within 0.2 units of
	each other and draw as one.

The band is not a property of either batch. It is the leave-one-batch-out prediction error after
that many samples, so it says how far a prediction made at that point in the batch has missed over
all 53, and the same band is drawn in both panels; only its centre differs.

The band is widest in the middle of the batch, at sample 103, and narrowest at the end, 2.42
units.

While a prediction sits inside the band it says only that the batch looks average. Batch 34's
leaves the band at sample 107, seven samples after the impurity enters. The SPE chart flagged the
same batch at 105.

Batch 4 is already at the average, so its prediction is close to right from the tenth sample and
moves little after it. Batch 34 starts in the same place and leaves it between samples 100 and 150,
arriving 12 units lower, which is where the RMSEP curve for the particle size settles below one
standard deviation.

The two panels are the same estimator on the same model. What separates them is when the batch's own
cells began to say something the average did not. A prediction that has not moved off the average is
not yet a statement about the batch.

.. _APPS_batch_case_sbr_online:

Would the model have caught it on-line?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model on this page holds batches 34 and 37, which is right for diagnosing them after the
fact and wrong for monitoring. A monitoring model must describe normal operation, as the
:ref:`first case study <APPS_batch_case_dupont>` does when it removes its outliers. The
reference model here is fitted to the 51 batches without 34 and 37, and the two are run
through it sample by sample, as if they were new batches on a running plant.

Two statistics are tracked. Hotelling's :math:`T^2` of the score estimate says how far the
batch so far sits *along* the model's components; the SPE of the newest sample says how far
that sample sits *away* from them.

The :math:`T^2` limit is the same at every sample, depending only on the number of
components and of reference batches, and it assumes the score estimates of the reference
batches at each sample are normally distributed. What changes is the spread of the score
estimates. A score estimated from the first few samples uses only a few cells of the unfolded
row, and across the reference batches such estimates scatter far more widely than the final
scores.

:math:`T^2` at each sample is therefore computed against the covariance of the reference
estimates at that same sample, which the monitor stores. Nomikos and MacGregor, in their
Technometrics paper of 1995, set their score-chart limits from that spread and note that
:math:`T^2` needs the covariance at each sample too; García-Muñoz, Kourti and MacGregor (2004)
compute it. The SPE limit is fitted sample by sample the same way: at each sample it is a
chi-square approximation matched to the mean and the variance of the 51 reference values
there.

The same normalisation pins the reference batches' average. Measuring a set of batches against
their own covariance forces their mean :math:`T^2` to :math:`A(N-1)/N`, 1.96 here for two
components and 51 batches, whatever the data: it is a property of the arithmetic, not of the
process. The grey line in the monitoring figure below is flat for that reason, and it is what
lets a single limit serve every sample. The SPE is not normalised this way, so its reference
mean does vary.

.. code-block:: python

	normal = {b: t for b, t in trajectories.items() if b not in (34, 37)}
	reference = BatchPLS(n_components=2).fit(normal, quality.loc[list(normal)])
	monitor = BatchMonitor(reference, conf_level=0.99,
	                       spe_statistic="instantaneous").fit(normal)
	# sd of the estimates, per sample
	spread = np.sqrt(np.diagonal(monitor.score_covariance_over_time_, axis1=1, axis2=2))
	# relative to the final scores
	spread = spread / reference.scores_.std(ddof=1).to_numpy()
	fig = go.Figure()
	for a, colour in enumerate((BLUE, ORANGE)):
	    fig.add_trace(go.Scatter(x=np.arange(1, len(spread) + 1), y=spread[:, a],
	                             name=f"t{a + 1}", line=dict(color=colour)))
	fig.add_hline(y=1.0, line_dash="dash", line_color=GREY,
	              annotation_text="spread of the final scores")
	fig.update_layout(xaxis_title="Samples observed",
	                  yaxis_title="Spread relative to the final scores",
	                  yaxis_type="log", height=380)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-score-spread.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Two curves on a logarithmic axis, the standard deviation of the t1 and t2 estimates across the 51 reference batches divided by that of their final scores, against samples observed; both start near a quarter of the final spread and rise to it by the end of the batch, with reference lines at one and at a half.
	:width: 600px
	:scale: 80
	:align: center

	The spread of the on-line score estimates across the 51 reference batches, divided by
	the spread of their final scores, against the number of samples observed (logarithmic
	axis). The estimator pulls the scores toward the average batch while little has been
	observed, so early estimates lie closer together than the final scores do, and the spread
	grows to match them as the batch fills in. :math:`T^2` at each sample is scaled by this
	spread, which is what lets the limit stay the same throughout the batch.

The limits are set at 99%, and an alarm here means three consecutive samples above the
limit, the same kind of rule the departure analysis used.

.. code-block:: python

	def first_sustained(alarm, run=3):
	    """First of the `run` consecutive samples above the limit, counting from one,
	    or None."""
	    runs = np.convolve(alarm.astype(int), np.ones(run, dtype=int), mode="valid") == run
	    return int(runs.argmax()) + 1 if runs.any() else None

	print(f"T2 limit at 99%: {monitor.t2_limit_over_time_[0]:.1f}")
	# T2 limit at 99%: 10.5
	# A(N-1)/N at every sample, whatever the data do
	mean_t2 = np.asarray(monitor.t2_mean_over_time_)
	print(f"reference mean T2: {mean_t2.min():.2f} to {mean_t2.max():.2f}")
	# reference mean T2: 1.96 to 1.96
	for batch_id in (37, 34, 4):
	    result = monitor.monitor(trajectories[batch_id])
	    t2_alarm_at = first_sustained(result.t2_alarm)
	    print(f"batch {batch_id}: T2 alarm after {t2_alarm_at} samples;",
	          f"SPE alarm after {first_sustained(result.spe_alarm)} samples")
	    # batch 37: T2 alarm after 23 samples; SPE alarm after 15 samples
	    # batch 34: T2 alarm after 190 samples; SPE alarm after 105 samples
	    # batch 4: T2 alarm after None samples; SPE alarm after None samples

	def longest_run(alarm):
	    """Longest stretch of consecutive samples above the limit."""
	    best = current = 0
	    for above in alarm:
	        current = current + 1 if above else 0
	        best = max(best, current)
	    return best

	traced = [monitor.monitor(t) for t in normal.values()]
	t2_rate = np.mean([r.t2_alarm.mean() for r in traced])
	spe_rate = np.mean([r.spe_alarm.mean() for r in traced])
	print(f"reference batches: {t2_rate:.2%} of T2 values and",
	      f"{spe_rate:.2%} of SPE values above their limits")
	# reference batches: 0.17% of T2 values and 1.13% of SPE values above their limits
	for run in (3, 5, 10):
	    print(f"  with an SPE alarm of {run} consecutive samples somewhere:",
	          sum(first_sustained(r.spe_alarm, run) is not None for r in traced), "of 51;",
	          "T2:", sum(first_sustained(r.t2_alarm, run) is not None for r in traced),
	          "of 51")
	    #   with an SPE alarm of 3 consecutive samples somewhere: 13 of 51; T2: 1 of 51
	    #   with an SPE alarm of 5 consecutive samples somewhere: 8 of 51; T2: 1 of 51
	    #   with an SPE alarm of 10 consecutive samples somewhere: 3 of 51; T2: 1 of 51
	print("  longest SPE alarm run in a reference batch:",
	      max(longest_run(r.spe_alarm) for r in traced), "samples")
	#   longest SPE alarm run in a reference batch: 15 samples
	print("batch 34: above the SPE limit for",
	      int(monitor.monitor(trajectories[34]).spe_alarm[104:].sum()),
	      "of its last 96 samples; batch 37: longest T2 alarm run",
	      longest_run(monitor.monitor(trajectories[37]).t2_alarm), "samples")
	# batch 34: above the SPE limit for 87 of its last 96 samples;
	# batch 37: longest T2 alarm run 178 samples
	online_monitoring_plot(monitor, trajectories[37], "t2").show()
	fig = online_monitoring_plot(monitor, trajectories[34], "spe")
	fig.add_vline(x=100, line_dash="dash", line_color=ORANGE,
	              annotation_text="impurity enters")
	fig.show()
	alarm_k = first_sustained(monitor.monitor(trajectories[34]).spe_alarm)
	for k in (alarm_k, alarm_k + 4):
	    residuals = reference.predict_online(trajectories[34], upto_k=k).residuals
	    shares = residuals.xs(k - 1, level="sequence") ** 2
	    shares = (shares / shares.sum() * 100).round(0).astype(int)
	    print(f"batch 34 after {k} samples, share of the squared residual per tag [%]:",
	          shares.to_dict())
	    # batch 34 after 105 samples, share of the squared residual per tag [%]:
	    # {'Conversion': 1, 'CoolingTemp': 31, 'EnergyReleased': 11, 'JacketTemp': 17,
	    # 'LatexDensity': 0, 'ReactorTemp': 41}
	    # batch 34 after 109 samples, share of the squared residual per tag [%]:
	    # {'Conversion': 2, 'CoolingTemp': 36, 'EnergyReleased': 19, 'JacketTemp': 30,
	    # 'LatexDensity': 1, 'ReactorTemp': 12}
	alarm_residuals = reference.predict_online(trajectories[34], upto_k=alarm_k).residuals
	at_alarm = alarm_residuals.xs(alarm_k - 1, level="sequence") ** 2
	at_alarm = (at_alarm / at_alarm.sum() * 100).round(0).astype(int)
	fig = go.Figure(go.Bar(x=at_alarm.index, y=at_alarm.values, marker_color=BLUE))
	fig.update_layout(title=f"Batch 34 after {alarm_k} samples",
	                  yaxis_title="Share of the squared residual [%]", height=320)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-online-monitoring.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Three panels: Hotelling's T2 of batch 37 against samples observed with the 99% limit dashed, crossing it after 23 samples and staying above; the SPE of the newest sample of batch 34 with its per-sample limit, a dotted vertical at 100 where the impurity enters, and the first sustained alarm after 105 samples; and the share of the residual per tag at that alarm sample, led by the reactor and cooling-water temperatures.
	:width: 1200px
	:scale: 80
	:align: center

	On-line monitoring of the two faulty batches against the reference model of 51 normal
	batches. Left: Hotelling's :math:`T^2` of batch 37 (aqua) with the 99% limit (dashed) and
	the reference-batch mean (grey, flat by construction); the first sustained alarm is after
	23 samples. Middle:
	the SPE of the newest sample of batch 34 (orange) with its per-sample limit; the impurity
	enters at sample 100 (dotted vertical) and the first sustained alarm is after 105
	samples. Right: the share of the squared residual per tag at that alarm sample.

Batch 37 raises both alarms. Its SPE crosses first, from sample 15, for seven samples; its
:math:`T^2` crosses at 23 and stays above the limit for the rest of the batch, while the SPE
falls back inside until 144. Batch 34 is caught by the SPE after 105 samples, five after the
impurity enters, while its :math:`T^2` stays inside until 190.

Nomikos and MacGregor flagged the same two faults with models of all nine trajectories:
the fault present from the start, in the scores within the first 15 samples (1994), and the
fault from the middle of the batch, in the SPE after 105 samples, the same sample as here
(their multi-way PLS paper of 1995).

The 51 reference batches define normal, so any alarm they raise is a false alarm. Their alarm rate
is a lower bound on what the plant will see, because the limits were fitted to these same batches.

A 99% limit lets 1% of a normal batch's values cross by chance, about two crossings over 200
samples, so a single crossing cannot count as an alarm. The rule used here is three consecutive
samples above the limit, the run length García-Muñoz, Kourti and MacGregor (2004) use, applied to
the 99% limit rather than their 95% one.

That rule holds for :math:`T^2`, where one of the 51 reference batches alarms. It fails for the SPE,
where 13 do, one normal batch in four.

Both statistics are autocorrelated: a sample that fits the model poorly is usually followed by
another that does, so crossings arrive in runs. What separates the two charts is how often they
cross at all. The reference batches cross their own :math:`T^2` limit at a sixth of the nominal
rate, because that limit is derived for a batch outside the reference set, and their SPE limit at
about the nominal rate.

Three responses, each measured on the same 51 batches:

* a limit fitted to the reference values of five neighbouring samples pooled, the window
  Nomikos and MacGregor (1995) use, does not help, with the same 13 batches alarming: the
  crossings are already as rare as a 99% limit intends, and they still come in runs;
* the cumulative SPE, over every cell observed so far, adds each new sample's residual to a
  sum over all the earlier ones, so a run of a few poorly fitting samples barely moves it;
  2 batches alarm, at the price of catching batch 34 after 112 samples rather than 105, since
  the same dilution slows its response to a real change;
* a 99.9% limit, which Nomikos (1996) uses for the residual chart because residuals collect
  every kind of variation the model does not describe, leaves no reference batch alarming
  and catches batch 34 after 106 samples. A 99.9% quantile fitted from 51 values lies beyond
  the largest of them, so no reference batch can be expected to cross it: the count of zero
  says the limit is wide, not what the false-alarm rate on new batches will be.

An alarm on a new batch is trustworthy only once that false-alarm rate has been measured and
made acceptable. Ramaker and co-workers (2006) judge a batch chart on how often it signals
over a normal batch and how long it takes to signal on a faulty one. Here the :math:`T^2`
chart is used as it stands and the SPE chart needs one of the three. Either way batch 34 is
flagged with most of its second half still to run.

.. code-block:: python

	pooled = BatchMonitor(reference, conf_level=0.99, spe_statistic="instantaneous",
	                      spe_window=2).fit(normal)
	pooled_traced = [pooled.monitor(t) for t in normal.values()]
	pooled_rate = np.mean([r.spe_alarm.mean() for r in pooled_traced])
	pooled_count = sum(first_sustained(r.spe_alarm) is not None for r in pooled_traced)
	pooled_at = first_sustained(pooled.monitor(trajectories[34]).spe_alarm)
	print(f"limit pooled over five samples: {pooled_rate:.2%} of the reference",
	      f"SPE values above it; {pooled_count} of 51 batches",
	      f"with a three-sample run; batch 34 flagged after {pooled_at} samples")
	# limit pooled over five samples: 1.16% of the reference SPE values above it;
	# 13 of 51 batches with a three-sample run; batch 34 flagged after 105 samples
	# the SPE over every sample observed so far
	cumulative = BatchMonitor(reference, conf_level=0.99).fit(normal)
	# reference batches with an alarm; batch 34
	print([sum(first_sustained(cumulative.monitor(t).spe_alarm) is not None
	           for t in normal.values()),
	       first_sustained(cumulative.monitor(trajectories[34]).spe_alarm)])
	# [2, 112]
	tight = BatchMonitor(reference, conf_level=0.999,
	                     spe_statistic="instantaneous").fit(normal)   # the 99.9% limit
	# reference batches with an alarm; batch 34
	print([sum(first_sustained(tight.monitor(t).spe_alarm) is not None
	           for t in normal.values()),
	       first_sustained(tight.monitor(trajectories[34]).spe_alarm)])
	# [0, 106]

Which statistic catches a fault says what kind of fault it is. How much of the batch has been
seen says when.

A fault along a direction the reference batches already vary in is carried by the score once
enough of the batch has been seen: a large :math:`T^2` and a small residual, where batch 37 sits
from sample 23 to the end. A fault in a combination of tags the model has no component for never
reaches a score at all, so the newest samples stop fitting, which is what the SPE measures, and
that is batch 34 from sample 105.

Early in a batch every fault looks like the second kind. With fifteen samples in hand the model
cannot yet place batch 37 along its components, so the deviation is left in the residual and the
SPE crosses first, at sample 15; once the score moves out, the SPE falls back inside and the
:math:`T^2` holds. All five faults García-Muñoz, Kourti and MacGregor (2004) simulated also
showed in the SPE chart first.

The reactor temperature is the tag the model explains least, so its residual is large in every
batch and its share is largest at the alarm before falling as the service temperatures stop
fitting. Those shares say which tags stopped fitting the model, not what happened in the
reactor: the departure analysis puts the onsets in the two service temperatures, and none in
the reactor temperature.

The same score estimate that predicts the quality also predicts the rest of the
trajectories, as the model's reconstruction :math:`\hat{\boldsymbol{\tau}} \mathbf{P}^{T}`
read off for the samples not yet seen (Wold and co-workers, 2009, Eq. 4). García-Muñoz,
Kourti and MacGregor (2004) show it to be an adaptive time-series forecast, built on how the
variables co-vary over the whole batch rather than on the trend so far.

It is shown in the z form of the departure analysis, each tag as a distance from the 51
normal batches at that sample in their standard deviations, so a departure reads directly
against the zero line.

.. code-block:: python

	def z_form(frame):
	    """Each tag as a distance from the 51 normal batches at that sample, in their
	    standard deviations."""
	    return pd.DataFrame((frame.to_numpy() - others.mean(axis=0))
	                        / others.std(axis=0, ddof=1),
	                        columns=frame.columns, index=frame.index)

	def forecast_panel(batch_id, tag, from_samples, colour):
	    """The normal batches as a band, what the batch did, and the forecast of the rest
	    from two points."""
	    # A band, not 51 lines: on a noisy tag the lines fill the panel and the forecasts
	    # have to be read through them. It covers the middle 90% of the normal batches at
	    # each sample.
	    spread = np.stack([z_form(t)[tag].to_numpy() for t in normal.values()])
	    lo, hi = np.percentile(spread, 5, axis=0), np.percentile(spread, 95, axis=0)
	    fig = go.Figure([go.Scatter(x=[*range(len(lo)), *reversed(range(len(hi)))],
	                                y=[*lo, *reversed(hi)], fill="toself",
	                                fillcolor="rgba(200, 200, 200, 0.45)", line_width=0,
	                                name="normal batches, middle 90%")])
	    fig.update_layout(title=tag, xaxis_title="Sample [aligned time]", height=320)
	    z_actual = z_form(trajectories[batch_id])[tag]
	    fig.add_trace(go.Scatter(y=z_actual, mode="lines",
	                             name=f"batch {batch_id}, what happened",
	                             line=dict(color=colour, width=1), opacity=0.4))
	    # the later one apart
	    for k, dash, line_colour, width in zip(from_samples, ("dash", "dot"),
	                                           (colour, BLUE), (2, 3)):
	        forecast = z_form(reference.predict_online(trajectories[batch_id],
	                                                   upto_k=k).forecast)[tag]
	        fig.add_trace(go.Scatter(x=forecast.index[k:], y=forecast.iloc[k:],
	                                 mode="lines", name=f"forecast from sample {k}",
	                                 line=dict(color=line_colour, width=width, dash=dash)))
	        # the jump from the data used
	        fig.add_trace(go.Scatter(x=[k - 1, k - 1],
	                                 y=[z_actual.iloc[k - 1], forecast.iloc[k]],
	                                 mode="lines",
	                                 line=dict(color=line_colour, width=1.5),
	                                 showlegend=False))
	    fig.add_trace(go.Scatter(y=z_actual.iloc[:from_samples[0]], mode="lines",
	                             name=f"batch {batch_id}, observed",
	                             line=dict(color=colour, width=3)))
	    fig.add_hline(y=0, line_color=GREY)
	    fig.update_layout(title=f"Batch {batch_id}: {tag}",
	                      yaxis_title="Distance from the normal batches [sd]")
	    return fig

	forecast_panel(37, "Conversion", (30, 60), AQUA).show()
	panel = forecast_panel(34, "CoolingTemp", (60, 115), ORANGE)
	panel.add_vline(x=100, line_dash="dash", line_color=ORANGE).show()
	for batch_id, tag, k in ((37, "Conversion", 30), (37, "Conversion", 60),
	                         (34, "CoolingTemp", 60), (34, "CoolingTemp", 115)):
	    forecast = z_form(reference.predict_online(trajectories[batch_id],
	                                               upto_k=k).forecast)[tag].iloc[k:]
	    print(f"batch {batch_id}, {tag}, from sample {k} onwards:"
	          f" forecast mean {forecast.mean():.2f} sd,",
	          f"actual {z_form(trajectories[batch_id])[tag].iloc[k:].mean():.2f} sd")
	# batch 37, Conversion, from sample 30 onwards: forecast mean -1.81 sd, actual -4.81 sd
	# batch 37, Conversion, from sample 60 onwards: forecast mean -3.62 sd, actual -4.82 sd
	# batch 34, CoolingTemp, from sample 60 onwards: forecast mean 0.01 sd, actual 2.36 sd
	# batch 34, CoolingTemp, from sample 115 onwards: forecast mean 0.36 sd, actual 3.30 sd

.. figure:: ../figures/batch/batch-case-sbr-forecast.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Two panels in z form, each tag as a distance from the normal batches in their standard deviations. Left, the conversion of the normal batches as a grey band around zero, batch 37's observed conversion in aqua up to 30 samples, well below zero, and the model's forecasts of the rest from sample 30 onwards (dashed aqua, near minus two) and from sample 60 onwards (dotted dark blue, near minus three and a half), both below zero and both short of the faint line of what batch 37 did, near minus five. Right, the cooling-water temperature of batch 34 in orange with forecasts from sample 60 onwards (dashed orange) and from sample 115 onwards (dotted dark blue) that stay near zero and miss the rise after sample 100 entirely.
	:width: 1000px
	:scale: 80
	:align: center

	Forecast of the rest of the batch from the score estimate, in z form: each tag as a
	distance from the normal batches at that sample, in their standard deviations, so the zero
	line is the average batch and the grey band holds the middle 90% of them. Left: the
	conversion of batch 37 (aqua), observed
	for 30 samples, and the forecasts from sample 30 onwards (dashed aqua) and from sample 60
	onwards (dotted dark blue); what batch 37 did is the faint line. Right: the cooling-water
	temperature of batch 34 (orange) with the forecasts from sample 60 onwards (dashed
	orange) and from sample 115 onwards (dotted dark blue); the impurity enters at sample 100.
	A vertical line joins each forecast to the observed value at the sample it was made from:
	the forecast uses the batch's own data up to that sample, then continues along the
	model's components. Batch 37's two forecasts lie below zero and above what happened; the
	later one, with more of the batch behind it, lies closer to it.

It is the same distinction as the two statistics. Batch 37's slow conversion lies along the
model's components, so it is forecast in the right direction, and more closely the later the
forecast is made. Batch 34's fault lies off them, so its forecasts stay on the average batch,
and it can be flagged but not forecast.

Both of batch 37's forecasts still understate what happened, because they are built from
estimated scores, and those are pulled toward the average batch while little has been observed,
the same shrinkage as in the quality prediction.

Both faults are found with much of the batch still to run, and the statistic that finds each
says which kind it is. A large :math:`T^2` with a small residual is a batch far along a known
direction, while a large residual with a small :math:`T^2` is a batch doing something the
reference set never did.

Every number here comes from the reference set, easy to choose because the simulation says
which batches are faulty. On plant data those batches are the first thing to get right, and
the :ref:`first case study <APPS_batch_case_dupont>` shows how much of the work that is. The
:ref:`third case study <APPS_batch_case_fmc>` turns to a process where the trajectories are
one of four blocks about a batch, and asks which block matters most.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~

The full list of readings on batch data is on the :ref:`batch process monitoring page
<APPS_batch_readings>`; this page lists what it draws on.

* Paul Nomikos, `Statistical process control of batch processes <https://literature.learnche.org/item/154/statistical-process-control-of-batch-processes>`_,
  Ph.D thesis, McMaster University, 1995. The source of the simulation and of the two
  faulty batches.

* Paul Nomikos and John F. MacGregor, "`Monitoring batch processes using multiway principal
  component analysis <https://literature.learnche.org/item/30/monitoring-batch-processes-using-multiway-principal-component-analysis>`_",
  *AIChE Journal*, **40**, 1361-1375, 1994. Describes the simulation and the two faulty
  batches, and monitors them with a batch PCA model of all nine trajectories.

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

* Paul Nomikos, "`Detection and diagnosis of abnormal batch operations based on multi-way
  principal component analysis <https://literature.learnche.org/item/64/detection-and-diagnosis-of-abnormal-batch-operations-based-on-multi-way-principal-component-analysis>`_",
  *ISA Transactions*, **35**, 259-266, 1996. The 99.9% limit for the residual chart.

* Henk-Jan Ramaker, Eric N. M. Van Sprang, Johan A. Westerhuis, Stephen P. Gurden, Age K.
  Smilde and Frank H. Van Der Meulen, "`Performance assessment and improvement of control
  charts for statistical batch process monitoring <https://literature.learnche.org/item/164/performance-assessment-and-improvement-of-control-charts-for-statistical-batch-process-monitoring>`_",
  *Statistica Neerlandica*, **60**, 339-360, 2006. Assesses a batch chart by its overall
  type I error and by the time it takes to signal.

* Francisco Arteaga and Alberto Ferrer, "`Dealing with missing data in MSPC: several
  methods, different interpretations, some examples <https://literature.learnche.org/item/20/dealing-with-missing-data-in-mspc-several-methods-different-interpretations-some-examples>`_",
  *Journal of Chemometrics*, **16**, 408-418, 2002. Trimmed score regression.

* Salvador García-Muñoz, Theodora Kourti and John F. MacGregor, "`Model predictive
  monitoring for batch processes <https://literature.learnche.org/item/157/model-predictive-monitoring-for-batch-processes>`_", *Industrial and
  Engineering Chemistry Research*, **43**, 5929-5941, 2004. Compares the estimators of the
  scores of a batch so far, shows that the forecast of the rest of the batch is an adaptive
  time-series forecast, and computes Hotelling's :math:`T^2` against the time-varying
  covariance of the score estimates.

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process
  modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_",
  *Comprehensive Chemometrics*, **2**, chapter 2.10, 163-197, 2009. Mid-batch prediction of
  quality and
  of the remaining trajectories.
