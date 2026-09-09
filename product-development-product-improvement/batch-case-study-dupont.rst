.. _APPS_batch_case_dupont:

Learning from batch trajectories: the DuPont polymerization reactor
=====================================================================

.. index::
	single: batch data; DuPont polymerization case study
	pair: batch PCA; outlier diagnosis
	pair: contribution plots; batch trajectories
	single: observability; batch data

This is the first of three case studies on batch data. A principal component model of the
trajectories finds which batches differ from the rest, names the variables and the times at
which they differ, and shows what such a model cannot detect.

The :ref:`second <APPS_batch_case_sbr>` adds final quality and uses PLS. The
:ref:`third <APPS_batch_case_fmc>` joins several blocks in a multiblock model. All three
plot the raw trajectories, fit a few components, examine the batches singled out, and
confirm each finding in the raw data.

Nylon is made in two stages in an industrial batch reactor: an hour of charging and solvent
removal, then a controlled pressure and temperature ramp to the final polymer.

The critical quality property is measured in the laboratory about 12 hours after the batch
ends. Nothing measured during a batch can correct it, and the result arrives only after the
next few batches have started.

The plant records ten trajectories per batch: three reactor temperatures, three pressures,
two flow rates, and the heating- and cooling-medium temperatures. The data are the worked
example of Nomikos and MacGregor (1995), supplied by DuPont, of 55 batches aligned to 100
time intervals and scaled for confidentiality.

From the laboratory records, batches 40, 41, 42, 50, 51, 53, 54 and 55 were well outside the
quality limit, and batches 38, 45, 46, 49 and 52 above or close to it. The models never use
that list: each is a PCA of the trajectories alone, poor batches included, and the list is
compared afterwards with what the trajectories reveal.

The data
~~~~~~~~

The `polymerization dataset <https://openmv.net/info/polymerization>`_ is one table of 5500
rows, one per aligned sample, with a batch identifier and a time index. ``load_dupont``, in
the `process_improve <https://github.com/kgdunn/process-improve>`_ package, downloads it and
splits it into one data frame per batch, 100 samples by 10 tags.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from process_improve.batch import BatchPCA, load_dupont, time_varying_loading_plot, unfolded_contribution_plot

	batches = load_dupont()                    # https://openmv.net/file/polymerization.csv
	first = next(iter(batches.values()))
	print(len(batches), "batches;", first.shape[0], "samples per batch;", list(first.columns))

Plotting one tag for every batch, a few of them in colour, is the first check. The
trajectories overlay well, confirming the alignment, and a few batches are visibly unusual
in the cooling-medium temperature ``TempC-1`` and in ``Press-1``, while the two flow rates
are noisy in every batch.

.. code-block:: python

	GREY, ORANGE, AQUA, BLUE = "#c8c8c8", "#c55a11", "#1baf7a", "#1f3d7a"          # figure colours: one
	PURPLE, MAGENTA = "#6f42c1", "#b03a78"                                        # meaning each, throughout

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
	    overlay(batches, tag, {49: ORANGE, 54: AQUA}).show()

.. _APPS_batch_case_dupont_overlay:

.. figure:: ../figures/batch/batch-case-dupont-raw-trajectories.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Four tags of the 55 batches overlaid in grey with batch 49 in orange and batch 54 in aqua; the cooling-medium temperature of batch 49 falls below the others after sample 60, and the pressure step of batch 54 comes later than in the other batches.
	:width: 900px
	:scale: 80
	:align: center

	Four of the ten tags for all 55 batches (grey), with batch 49 (orange) and batch 54
	(aqua) drawn on top. The cooling-medium temperature of batch 49 falls away from the
	other batches after sample 60. The pressure step of batch 54 in ``Press-1`` comes later
	than in the other batches, and its reactor temperature ``TempR-1`` runs slightly below
	them over the first 20 samples.

A first model on all 55 batches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`BatchPCA <https://github.com/kgdunn/process-improve/blob/main/src/process_improve/batch/_batch_pca.py>`_ unfolds batchwise, so each batch becomes one row of 10 tags by 100 samples,
1000 columns. Every column is centred and scaled to unit variance, the
:ref:`preprocessing <LVM_preprocessing>` any PCA model uses. Centring removes each tag's
average trajectory and scaling weights every (tag, time) cell equally, so the components
describe how batches deviate from the average batch.

Model A, the first of three, uses two components and all 55 batches, not as a final model
but as a first look at which batches stand out.

The alternative, observation-wise unfolding, has one row per time sample and one column per
tag. It describes the shape of the trajectories rather than the differences between batches,
so comparing batches needs a second model of its scores, and matching the same residual
needs twice as many components (Westerhuis, Kourti and MacGregor, 1999). It suits
trajectories varied on purpose, as in a designed experiment. All three case studies unfold
batchwise.

.. code-block:: python

	def scores(model, pc_horiz=1, pc_vert=2, highlight=None):
	    """Score plot with the percent of the variance each component explains on its axis."""
	    fig = model.score_plot(pc_horiz=pc_horiz, pc_vert=pc_vert, items_to_highlight=highlight,
	                           settings={"show_labels": True})
	    r2 = model.r2_per_component_
	    fig.update_layout(xaxis_title=f"t{pc_horiz} [{r2.iloc[pc_horiz - 1]:.1%}]",
	                      yaxis_title=f"t{pc_vert} [{r2.iloc[pc_vert - 1]:.1%}]")
	    return fig

	model_a = BatchPCA(n_components=2).fit(batches)
	print("R2 per component:", model_a.r2_per_component_.round(3).tolist())
	print("R2 cumulative:", model_a.r2_cumulative_.round(3).tolist())
	scores(model_a).show()
	spe = model_a.spe_.iloc[:, -1]                          # SPE of every batch after the second component
	t2 = model_a.hotellings_t2_.iloc[:, -1]                 # ... and its Hotelling's T2
	print(f"largest SPE: batch {spe.idxmax()} ({spe.max():.1f} against the 95% limit {model_a.spe_limit(conf_level=0.95):.1f})")
	print("above the SPE limit:", sorted(spe.index[spe > model_a.spe_limit(conf_level=0.95)]))
	print("above the T2 limit:", sorted(t2.index[t2 > model_a.hotellings_t2_limit(conf_level=0.95)]))

The two components together explain 55.9% of the variance in the unfolded matrix. Two
plots are enough to find the batches that differ.

.. figure:: ../figures/batch/batch-case-dupont-model-a-scores.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Score plot of model A with the 95% confidence ellipse; batches 50, 52, 53, 54 and 55 lie outside the ellipse, while batches 49 and 51 sit inside it among the other batches.
	:width: 600px
	:scale: 80
	:align: center

	Score plot of model A. Batches 50, 52, 53, 54 and 55 (aqua) lie outside the 95%
	confidence ellipse. Batches 49 and 51 (orange) sit inside it, among the other batches;
	the figure below shows what separates them.

The :ref:`score plot <LVM_interpreting_scores>` puts the last six batches away from the
rest, five outside the 95% confidence ellipse. Batches this far out pull the components
towards themselves, so the model is rebuilt without them once they have been examined.

The score plot says how far a batch sits *along* the directions the model found. The
:ref:`SPE <LVM-interpreting-SPE-residuals>` says how far it sits *away* from them. Drawing
:math:`T^2` (:ref:`Hotelling's statistic <LVM-Hotellings-T2>`) against the SPE puts both in
one figure, each 95% limit dividing it into quadrants.

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

	above_spe, above_t2 = [49, 51], [50, 52, 53, 54, 55]
	influence_plot(model_a, highlight={**{b: AQUA for b in above_t2}, **{b: ORANGE for b in above_spe}},
	               labels=above_spe + above_t2).show()

.. figure:: ../figures/batch/batch-case-dupont-model-a-influence.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Hotelling's T2 against SPE for the 55 batches, with both 95% limits; batches 49 and 51 are in the upper left with large SPE and small T2, and batches 50, 52, 53, 54 and 55 are in the lower right with large T2 and ordinary SPE.
	:width: 620px
	:scale: 80
	:align: center

	Hotelling's :math:`T^2` against the SPE for every batch, with both 95% limits. Batches 49
	and 51 (orange) are above the SPE limit and inside the :math:`T^2` limit; batches 50, 52,
	53, 54 and 55 (aqua) are the other way round. Colour marks which of the two limits the
	batch exceeds.

Batches 49 and 51 are in the upper left, ordinary along the two components and extreme away
from them, which is a break in the correlation structure rather than a large deviation along
it. The other five of the last six are in the lower right, extreme along the components with
ordinary residuals, so one statistic alone would have missed a group.

Batch 49: which variables, and when
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The raw data are ambiguous about batch 49: ``Flow-1`` looks suspicious in the overlay, but
it is a noisy tag in every batch. The SPE :ref:`contributions <LVM_contribution_plots>`
settle the question.

The contribution vector has one entry per (tag, time) cell, 1000 here, holding that cell's
residual after the two-component reconstruction. The SPE is the length of that vector, so
each squared residual divided by the total is the share of the SPE the cell carries. Those
shares are summed two ways:

* per tag, which ranks the variables, a summary Garcia-Munoz and co-workers (2003)
  introduced;
* per time sample, which locates the event in the batch.

``unfolded_contribution_plot`` draws the full vector of 1000 bars, grouped by tag or summed
per tag.

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
	print(f"share of samples 55 to 65: {by_time.loc[55:65].sum():.0f}%")

.. figure:: ../figures/batch/batch-case-dupont-batch-49-spe-contributions.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Three panels for batch 49: the share of the SPE carried by each of the 1000 unfolded cells, grouped by tag; the shares summed per tag, led by TempC-1, Flow-2 and Press-2; and the shares summed per sample, a single narrow peak between samples 55 and 65.
	:width: 800px
	:scale: 80
	:align: center

	Top: the share of the SPE of batch 49 carried by each (tag, time) cell. Middle: the
	same shares summed per tag. Bottom: summed per sample. The residual is concentrated in a
	single window, samples 55 to 65, and in the heating- and cooling-medium temperatures,
	the pressures and ``Flow-2``.

``Flow-1`` carries almost none of the residual. It belongs to the two medium temperatures,
``Flow-2``, ``Press-2`` and ``Press-3``, and 80% falls in the eleven samples from 55 to 65.
Nomikos (1996) attributes that short disturbance to a failure in the heating system, and
Wold and co-workers (2009) reach the same event from a different model.

The final quality of batch 49 was barely acceptable, which fits a short event rather than a
batch wrong throughout. Its cooling-medium temperature does fall away from the others after
sample 60, a change easy to miss until the contributions point at it.

The score outliers: batches 50 to 55
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Batches 50 to 55 are far out along the components, so the tool for them is the score
contribution: how much every (tag, time) cell contributes to :math:`t_1` or :math:`t_2`.

A score sums the scaled value times the loading over all 1000 cells,
:math:`t_{i,1} = \sum_{k=1}^{K}\sum_{j=1}^{J} x_{i,kj}\, p_{kj,1}`, for batch :math:`i`
over the :math:`K = 10` tags and :math:`J = 100` samples. A cell contributes strongly when
it is far from average in the direction of the loading. ``time_varying_loading_plot`` draws
the 1000-entry :ref:`loading <LVM_interpreting_loadings>` :math:`\mathbf{p}_1` as ten
curves.

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

Batch 54 has a high :math:`t_1` because every tag contributes in the same direction over the
whole batch. It ran away from the average trajectory from its first sample to its last, as
the :ref:`raw trajectory overlay <APPS_batch_case_dupont_overlay>` confirms. Batches 50 and
52 are read the same way, and batch 55, highest in :math:`t_2`, stands out through
``Press-3``, ``Press-2`` and ``TempC-1``.

Exclude and rebuild: a second group of batches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A reference model must describe normal operation, so batches 49 to 55 are removed and model
B is fitted to the remaining 48 with three components. Removing batches changes the model,
so the plots are examined again.

.. code-block:: python

	kept_b = {batch_id: batch for batch_id, batch in batches.items() if batch_id < 49}
	model_b = BatchPCA(n_components=3).fit(kept_b)
	print("R2 per component:", model_b.r2_per_component_.round(3).tolist())
	second_group = [37, 39, 43, 44, 45, 46, 47, 48]
	group_t2, group_t3 = model_b.scores_.loc[second_group].iloc[:, 1:3].mean()   # the group's average point
	# One colour and one marker for the group wherever it appears: orange already means batch 49.
	fig = scores(model_b, 2, 3, highlight={f'{{"color": "{PURPLE}", "symbol": "triangle-up"}}': second_group})
	fig.add_trace(go.Scatter(x=[group_t2], y=[group_t3], mode="markers", showlegend=False,     # a square at the
	                         marker=dict(symbol="square", size=9, color="#4d4d4d")))             # average point
	fig.add_annotation(x=0, y=0, ax=group_t2, ay=group_t3, axref="x", ayref="y", text="",       # the arrow from it
	                   showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#4d4d4d")          # to the model centre
	fig.add_annotation(x=group_t2 / 2, y=group_t3 / 2, text="contribution direction", showarrow=False, yshift=12,
	                   textangle=-np.degrees(np.arctan2(group_t3, group_t2)), font=dict(size=10))
	fig.show()

.. figure:: ../figures/batch/batch-case-dupont-model-b-scores.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Scores of model B on components 2 and 3; batches 37, 39 and 43 to 48 form a group at the top right, away from the main cloud, and a thick arrow labelled contribution direction runs from the group's average point to the model centre.
	:width: 600px
	:scale: 80
	:align: center

	Scores of model B on components 2 and 3. Batches 37, 39 and 43 to 48 (purple triangles) form a
	group at the top right of the plot, away from the main cloud of batches. The arrow runs
	from the group's average point (square) to the model centre: the direction along which
	the group's contributions below are computed.

With the extreme batches gone, a second group separates in the plane of :math:`t_2` and
:math:`t_3`: batches 37, 39 and 43 to 48.

A contribution is the weighted difference between two points, each either an actual batch or
a synthetic one such as the model centre or a group average. Here the eight are compared
against the centre, the average of all 48 and the arrow in the score plot. Their mean row is
the displacement from it, and its contributions add up to their mean score.

.. code-block:: python

	scaled_b = model_b.unfold_and_scale(kept_b)
	per_component = {a: model_b.score_contributions(scaled_b, component=a) for a in (2, 3)}
	group = {a: c.loc[second_group].mean(axis=0) for a, c in per_component.items()}   # the group against the centre
	for a in (2, 3):
	    early = group[a][group[a].index.get_level_values("sequence") <= 25].sum() / group[a].sum()
	    print(f"group mean t{a} = {model_b.scores_.loc[second_group].iloc[:, a - 1].mean():5.1f}",
	          f"(the contribution vector sums to {group[a].sum():5.1f});",
	          f"the other 40 batches: {model_b.scores_.drop(index=second_group).iloc[:, a - 1].mean():5.1f};",
	          f"samples 0 to 25 carry {early:.0%} of it")
	per_tag = pd.DataFrame({f"t{a}": group[a].groupby(level="tag", sort=False).sum() for a in (2, 3)})
	go.Figure([go.Bar(x=per_tag.index, y=per_tag[component], name=component) for component in per_tag]).show()
	for tag in ("TempC-1", "Press-3", "Press-2", "Flow-2"):          # the three largest contributions, and Flow-2
	    overlay(kept_b, tag, {batch_id: PURPLE for batch_id in second_group}).show()

.. code-block:: text

   group mean t2 =  15.0 (the contribution vector sums to  15.0); the other 40 batches:  -3.0; samples 0 to 25 carry 66% of it
   group mean t3 =  14.8 (the contribution vector sums to  14.8); the other 40 batches:  -3.0; samples 0 to 25 carry 90% of it

.. figure:: ../figures/batch/batch-case-dupont-group-contribution.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Left, the group's contribution to t2 and t3 summed per tag with each of the eight members as a dot; right, four panels of raw trajectories over samples 0 to 30 for TempC-1, Press-3, Press-2 and Flow-2, the eight group batches in purple and the other 40 in light grey.
	:width: 1000px
	:scale: 80
	:align: center

	The contribution of the eight-batch group to :math:`t_2` and :math:`t_3`, summed per tag
	with each member as a dot (left). Dots help show how consistent each batch in the cluster
	is with the group. Right: the raw trajectories over the first 30 samples of the three tags
	with the largest contributions, and of ``Flow-2``: the eight batches of the group (purple)
	and the other 40 batches of model B (light grey).

``TempC-1`` and ``Press-3`` carry most of the displacement on both components, every member
in the same direction, most of it from the first 25 samples. Not every member agrees.
``TempH-1`` takes both signs across the eight, so its group mean rests on a few. A group
contribution is a starting point, checked member by member.

The raw trajectories agree: the eight run above the other 40 in ``TempC-1`` and ``Press-3``
until about sample 25, and only slightly above in ``Press-2`` and ``Flow-2``.

Only batches 45 and 46 are on the poor or borderline list. The other six produced acceptable
product. They were operated differently, not badly, and a model of normal operation can
include enough of them to describe that mode or leave them out. The third model leaves them
out.

The final model, used to verify the unusual batches detected above
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model C is fitted on the 40 batches left once batch 49, batches 50 to 55 and the second
group are removed. The 15 removed batches are projected onto it to check that it describes
normal operation. Each is unfolded and scaled with model C's centre and scale, its scores
estimated, and its :math:`T^2` and SPE compared with the 95% limits of the 40.

.. code-block:: python

	kept_c = {batch_id: batch for batch_id, batch in kept_b.items() if batch_id not in second_group}
	model_c = BatchPCA(n_components=3).fit(kept_c)
	print("R2 per component:", model_c.r2_per_component_.round(3).tolist())
	poor_quality = [38, 40, 41, 42]                                # in the training set, known poor final quality
	# The four are marked in their own colour and shape: orange means batch 49 in the panel beside this one.
	scores(model_c, highlight={f'{{"color": "{MAGENTA}", "symbol": "diamond"}}': poor_quality}).show()
	left_out = {"batch 49": [49], "batches 50 to 55": list(range(50, 56)), "the second group": second_group}
	styles = {"batch 49": (ORANGE, "circle"), "batches 50 to 55": (AQUA, "circle"),
	          "the second group": (PURPLE, "triangle-up")}          # the group's colour and shape, as in model B
	projected = {b: model_c.predict_online(batches[b], upto_k=model_c.n_timesteps_)   # a complete batch: its scores,
	             for ids in left_out.values() for b in ids}                             # T2 and SPE against model C
	outside = pd.DataFrame({b: (float(r.hotellings_t2), float(r.spe)) for b, r in projected.items()}, index=["T2", "SPE"]).T
	fig = influence_plot(model_c, highlight={}, labels=[])
	for label, ids in left_out.items():
	    colour, symbol = styles[label]
	    fig.add_trace(go.Scatter(x=outside.loc[ids, "T2"], y=outside.loc[ids, "SPE"], mode="markers", name=label,
	                             marker=dict(size=10, color=colour, symbol=symbol), text=ids,
	                             hovertemplate="batch %{text}"))
	fig.update_xaxes(type="log").update_yaxes(type="log")         # the projected batches lie far outside the limits
	fig.show()
	t2_limit, spe_limit = model_c.hotellings_t2_limit(conf_level=0.95), model_c.spe_limit(conf_level=0.95)
	print("left-out batches above the SPE limit:", sorted(outside.index[outside["SPE"] > spe_limit]))
	print("left-out batches above the T2 limit:", sorted(outside.index[outside["T2"] > t2_limit]))
	print("batches 38, 40, 41 and 42 inside both limits:",
	      bool((model_c.hotellings_t2_.loc[poor_quality].iloc[:, -1] < t2_limit).all()
	           and (model_c.spe_.loc[poor_quality].iloc[:, -1] < spe_limit).all()))

.. code-block:: text

   R2 per component: [0.375, 0.114, 0.064]
   left-out batches above the SPE limit: [37, 39, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
   left-out batches above the T2 limit: [37, 50, 51, 52, 53, 54, 55]
   batches 38, 40, 41 and 42 inside both limits: True

.. figure:: ../figures/batch/batch-case-dupont-model-c.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Left, the scores of model C's 40 batches with 38, 40, 41 and 42 marked inside the ellipse; right, Hotelling's T2 against SPE on logarithmic axes, the 40 training batches below both limits and the 15 left-out batches above the SPE limit, seven of them above the T2 limit as well.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of model C, with batches 38, 40, 41 and 42 (magenta diamonds) marked. Right:
	Hotelling's :math:`T^2` against the SPE, on logarithmic axes, of the 40 training batches
	(blue) and of the 15 left-out batches projected onto model C: batch 49 (orange), batches
	50 to 55 (aqua circles) and the second group (purple triangles).

All 15 lie above the SPE limit, most far above, and the six score outliers and batch 37
above the :math:`T^2` limit as well, so the model built without them flags them. The 40
training batches are spread more evenly than in the first two models.

Batches 38, 40, 41 and 42 produced poor product, stayed in the training set, and sit inside
both limits. Nomikos and MacGregor (1995) left these four out too, holding that a reference
set should carry only batches with acceptable operation *and* acceptable product. They are
kept here so that this check can be made.

Nothing in the ten trajectories separates those four from the batches that produced good
product. That is the lesson of the case study. A model detects only what the measurements
contain, so if the cause leaves no trace in them, because the trajectory that matters is not
recorded or because the cause lies in the raw materials, no modelling of these ten tags will
reveal it.

In control engineering the condition of the batch must be *observable* through the
measurements. The remedy is to measure something else, such as the raw material properties,
and the :ref:`third case study <APPS_batch_case_fmc>` shows how such blocks are added.

The :ref:`SBR case study <APPS_batch_case_sbr_online>` runs the same check sample by sample,
comparing each statistic with its limit at every sample, so a faulty batch is flagged while
it still runs.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~

The full list of readings on batch data is on the
:ref:`batch process monitoring page <APPS_batch_readings>`; this page lists what it draws on.

* Paul Nomikos and John F. MacGregor, "`Multivariate SPC charts for monitoring batch
  processes <https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_",
  *Technometrics*, **37**, 41-59, 1995. The source of the data and of the list of batches
  with poor final quality.

* Paul Nomikos and John F. MacGregor, "`Monitoring batch processes using multiway principal
  component analysis <https://literature.learnche.org/item/30/monitoring-batch-processes-using-multiway-principal-component-analysis>`_",
  *AIChE Journal*, **40**, 1361-1375, 1994. The batchwise unfolding used on this page.

* Paul Nomikos, "`Detection and diagnosis of abnormal batch operations based on multi-way
  principal component analysis <https://literature.learnche.org/item/64/detection-and-diagnosis-of-abnormal-batch-operations-based-on-multi-way-principal-component-analysis>`_",
  *ISA Transactions*, **35**, 259-266, 1996. The contribution plots of batch 49 and the
  cause found for its event.

* Paul Nomikos, `Statistical process control of batch processes <https://literature.learnche.org/item/154/statistical-process-control-of-batch-processes>`_,
  Ph.D thesis, McMaster University, 1995.

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process
  modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_",
  *Comprehensive Chemometrics*, **2.10**, 163-197, 2009. Sets out the two unfolding layouts,
  and analyses batch 49 of this dataset on-line.

* Johan A. Westerhuis, Theodora Kourti and John F. MacGregor, "`Comparing alternative
  approaches for multivariate statistical analysis of batch process data <https://literature.learnche.org/item/162/comparing-alternative-approaches-for-multivariate-statistical-analysis-of-batch-process-data>`_",
  *Journal of Chemometrics*, **13**, 397-413, 1999. Sets out the six ways of unfolding a
  three-way batch array, and compares them on these data and on the SBR data.

* The full list of readings on batch data is on the
  :ref:`batch process monitoring <APPS_batch_monitoring>` page.
