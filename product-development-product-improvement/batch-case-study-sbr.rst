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
(Nomikos, 1995), and that makes it a rare kind of case study: the fault is known. Batches 34
and 37 both received 30% more organic impurity in the butadiene feed than the other batches,
from the very start of batch 37 and, in the description given in the original course notes,
midway through batch 34. Simulated data are useful for exactly this reason. A model can be
checked against what is known to have happened before it is trusted on plant data, where
nothing is known for certain.

The :ref:`first case study <APPS_batch_case_dupont>` used a PCA model of the trajectories
alone. Here a block of final quality attributes is available, so the model is a
:ref:`PLS <SECTION_PLS>` model from the unfolded trajectories to the five quality
attributes. Two questions are asked of it: does the model single out the two faulty
batches, and does it say what went wrong and when.

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
	from process_improve.batch import BatchPLS, contribution_at_time_plot, load_sbr, time_varying_loading_plot, unfolded_contribution_plot

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

The overlay already tells part of the story. The conversion of batch 37 runs below every
other batch from the start. Batch 34 follows the other batches for the first half of the
batch, and then its cooling-water and jacket temperatures rise above them while the energy
released falls below them. Both batches stay inside the band of the others in the reactor
temperature, which is held within a narrow range in every batch.

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
	model.score_plot(settings={"show_labels": True}).show()
	for batch_id in (34, 37):
	    print(f"batch {batch_id}: T2 = {model.hotellings_t2_.loc[batch_id].iloc[-1]:.1f} (limit {model.hotellings_t2_limit(conf_level=0.95):.1f}),",
	          f"SPE = {model.spe_.loc[batch_id].iloc[-1]:.1f} (limit {model.spe_limit(conf_level=0.95):.1f})")

The first component explains 24.5% of the variance in the trajectories and 65.3% of the
variance in the quality block; the second adds 12.7% and 6.9%.

.. figure:: ../figures/batch/batch-case-sbr-scores.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Scores of the batch PLS model with the 95% confidence ellipse; batch 37 has the lowest t1 of all batches and batch 34 the highest t2, both far outside the ellipse.
	:width: 600px
	:scale: 80
	:align: center

	Scores of the batch PLS model. Batch 37 (aqua) has the lowest :math:`t_1` of all
	batches and batch 34 (orange) the highest :math:`t_2`; both lie far outside the 95%
	confidence ellipse.

The score plot flags both faulty batches. Batch 37 has the lowest :math:`t_1` of all 53
batches and batch 34 the highest :math:`t_2`, and both are far outside the 95% confidence
ellipse: their :ref:`Hotelling's T2 <LVM-Hotellings-T2>` values are 28.2 and 19.2 against a
limit of 6.6.

The SPE measures the other thing a model can say about a batch: how far it sits away from
the components, in directions the model has not described. Drawing it against
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

The two faulty batches sit well to the right of the :math:`T^2` limit and below the SPE
limit. The batches the SPE does flag are different ones, in the upper left: batches 8 and
16, and batch 15 just on the limit, all three with ordinary :math:`T^2` values. Three
batches at or above a limit set at 95% is within what that limit allows for among 53
batches.

The SPE of a batch model is computed from the residuals of the whole batch, all 1200 cells,
so a deviation that the model can describe, a shift along its components, leaves little
residual behind. The scores and the SPE answer different questions. The scores say that a
batch moved in a direction the model knows; the SPE says that it moved in a direction the
model does not know.

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

The weights show what each component describes. :math:`\mathbf{w}_1` is dominated by the
latex density and the conversion, with a positive weight over the whole batch: a batch
with a low :math:`t_1` has a below-average latex density and a below-average conversion
throughout. :math:`\mathbf{w}_2` is dominated by the second half of the batch, with
positive weights on the cooling-water and jacket temperatures and negative weights on the
energy released, the latex density and the conversion: in a batch with a high :math:`t_2`
those two temperatures run above their average trajectories over the second half, while the
energy released and the extent of reaction run below theirs.

Note which temperature is missing from that list. The reactor temperature is the tag this
component involves least, and its weight over the second half is close to zero, so what
moves is the cooling and jacket side and not the reactor measurement itself. The component
says that the two groups move together; it does not say which of them drives the other.
Those are predictions about batches 37 and 34 respectively, and the contribution plots test
them.

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
were below average: the two tags contribute -33.4 and -25.5 to the score, the other four
between -1.3 and -5.2. The contribution is spread over the whole batch. Each fifth of the
batch carries between 15% and 26% of the total, which is what a fault present from the
first sample looks like. The :ref:`raw trajectory overlay <APPS_batch_case_sbr_overlay>` at
the start of this case study agrees: the conversion of batch 37 is below the other batches
from the start of the batch to the end. The impurity slowed the reaction from
the moment the batch began.

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

Batch 34 is high on :math:`t_2`, and the contributions come from the energy released
(14.3), the jacket temperature (12.3) and the cooling-water temperature (12.2), with the
conversion and the latex density behind them (8.1 and 7.2). The timing is what
distinguishes this batch from batch 37. The first two fifths of the batch carry 15% of the
:math:`t_2` contribution and the last two fifths carry 68%; the contribution per sample
stays small until about sample 100 and then rises, to a maximum near sample 140.
``contribution_at_time_plot`` shows the same three tags carrying the deviation at a single
sample, here sample 120.

The raw data can be asked the same question directly, tag by tag: at which sample does each
trajectory of a faulty batch leave the band of the other batches? The code below expresses
each trajectory of batches 34 and 37 as a distance from the mean of the other 51 batches,
in units of their standard deviation at that sample, and records the first sample from
which a tag stays more than two standard deviations away for 20 samples in a row, a tenth
of the batch. A single crossing is not informative on its own, because a noisy tag such as
the reactor temperature crosses the two-standard-deviation line now and then in every
batch.

.. code-block:: python

	others = np.stack([batch.to_numpy() for batch_id, batch in trajectories.items() if batch_id not in (34, 37)])
	z = {batch_id: (trajectories[batch_id].to_numpy() - others.mean(axis=0)) / others.std(axis=0, ddof=1)
	     for batch_id in (37, 34)}

	def sustained_departure(z_batch, n_sd=2.0, run=20):
	    """First sample from which each tag stays more than `n_sd` standard deviations away for `run` samples in a row."""
	    outside = (np.abs(z_batch) > n_sd).astype(int)
	    onset = {}
	    for j, tag in enumerate(sbr.trajectory_tags):
	        runs = np.convolve(outside[:, j], np.ones(run, dtype=int), mode="valid") == run
	        onset[tag] = int(runs.argmax()) if runs.any() else None
	    return onset

	for batch_id in (37, 34):
	    print(f"batch {batch_id}, first sustained departure:", sustained_departure(z[batch_id]))

	fig = make_subplots(rows=2, cols=6, subplot_titles=sbr.trajectory_tags, shared_yaxes=True)
	for row, (batch_id, colour) in enumerate([(37, AQUA), (34, ORANGE)], start=1):
	    for col in range(6):
	        fig.add_trace(go.Scatter(y=np.abs(z[batch_id][:, col]), mode="lines", name=f"batch {batch_id}",
	                                 line=dict(color=colour, width=1.5), showlegend=(col == 0)), row=row, col=col + 1)
	        fig.add_hline(y=2, line_dash="dash", line_color=GREY, row=row, col=col + 1)
	fig.update_layout(title="Distance from the other batches [standard deviations of the others]", height=420)
	fig.show()

.. figure:: ../figures/batch/batch-case-sbr-departure.png
	:source: batch/batch-case-sbr-figures.py
	:alt: Twelve small panels, one per tag for batch 37 in the top row and batch 34 in the bottom row, showing the distance of each trajectory from the other batches in standard deviations with the two-standard-deviation line dashed; batch 37 departs in latex density and conversion within the first 20 samples, batch 34 in the temperatures and the energy released at about sample 100 and in latex density and conversion later.
	:width: 1100px
	:scale: 80
	:align: center

	Distance of batch 37 (top, aqua) and batch 34 (bottom, orange) from the other batches
	for each of the six tags, in standard deviations of the other batches, with the
	two-standard-deviation line dashed. Batch 37 departs in latex density and conversion
	within the first 20 samples; batch 34 departs in the two temperatures and the energy
	released at about sample 100, and in latex density and conversion some 20 to 25 samples
	later.

The two batches leave the band at different times and in a different order. Batch 37
departs in the conversion at sample 9 and in the latex density at sample 13, and stays away
for the rest of the batch; none of its other four trajectories stays outside the band for
20 samples in a row. Batch 34 departs first in the cooling-water temperature, the jacket
temperature and the energy released, at samples 103 to 105, and in the conversion and the
latex density at samples 123 and 129. The same impurity, introduced midway, shows up first
in the energy released and the two service temperatures, and only afterwards in the extent
of reaction.

That order is consistent with a reaction that slowed down: less heat released leaves less
for the temperature control system to remove, the jacket and cooling-water temperatures
settle higher, and the conversion falls behind the other batches over the samples that
follow. The dataset names its tags and no more. It does not say where on the reactor each
temperature is measured, whether at a service inlet or a return, so that reading fits the
order of the departures without being established by it.

One fault, two places in the score plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same fault appears in two different places of the score plot because it started at two
different times. A batch model describes deviations in (tag, time) cells, so the time of an
event is part of its signature: a slow reaction from the start is a deviation along
:math:`\mathbf{w}_1`, and a slow reaction from the middle of the batch a deviation along
:math:`\mathbf{w}_2`. This is what makes batch models useful for diagnosis, and it is also a
caution. A library of known faults built in score space needs the time of onset as a
coordinate, and a fault that has been seen only at one onset time appears as a new fault
when it occurs at another.

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
lowest. Both batches produced poor latex. Batch 37 has the lowest branching, cross-linking
and polydispersity of all 53 batches and the second-smallest particle size; batch 34 has
the smallest particle size and is among the five lowest in composition, branching and
cross-linking. The fitted values from the PLS model place both batches at the same end of
these attributes, so a quality prediction from the trajectories would have flagged both
batches before the laboratory results arrived.

The two batches are not fitted equally well. The composition of batch 37 is fitted at
0.4500, below its observed 0.4525, whereas that of batch 34 is fitted at 0.4540, closer to
the average batch (0.4546) than to its observed value. The :math:`t_1` direction, which
carries the fault of batch 37, explains 65.3% of the quality block; the :math:`t_2`
direction, which carries the fault of batch 34, explains 6.9%. A deviation along a
component that explains little of the quality block moves the prediction less.

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

* The full list of readings on batch data is on the
  :ref:`batch process monitoring <APPS_batch_monitoring>` page.
