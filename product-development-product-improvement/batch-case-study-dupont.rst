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
it. The list plays no part in building the models: each one is a PCA of the trajectories
alone, fitted with the poor batches in the training set like any other, and no batch is
removed or weighted for its quality. The list is compared afterwards with what the
trajectories reveal on their own.

The data
~~~~~~~~

The `polymerization dataset <https://openmv.net/info/polymerization>`_ is a single table of
5500 rows, one per aligned sample of every batch, with a batch identifier and a time index.
The ``load_dupont`` function in the ``process_improve`` package downloads the table and
returns a dictionary with one data frame per batch, 100 samples by 10 tags.

.. code-block:: python

	import numpy as np
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

	GREY, ORANGE, AQUA, BLUE, PURPLE = "#c8c8c8", "#c55a11", "#1baf7a", "#1f3d7a", "#6f42c1"     # figure colours

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

The ``BatchPCA`` class unfolds the batches batchwise, so that each batch becomes one row of
10 tags times 100 samples, 1000 columns in all. Every column is then centred and scaled to
unit variance, the :ref:`preprocessing <LVM_preprocessing>` used for any PCA model.
Centring removes the average trajectory of each tag, and scaling gives every (tag, time)
cell the same weight, so the components describe how the batches deviate from the average
batch. The first model, called model A on this page, uses two components and all 55
batches. The aim is not a final model, but a first look at which batches stand out.

Batchwise unfolding is one of two ways to lay a three-way batch array out as a table. The
other is observation-wise unfolding: one row per time sample of every batch and one column
per tag. Centring that table removes the average of each tag rather than its average
trajectory, so a model of it describes the shape of the trajectories, and a second,
batchwise model of its scores is then needed to compare whole batches. The two layouts
answer different questions, and Wold and co-workers (2009) set both out and compare them,
including on this dataset. All three of these case studies unfold batchwise.

.. code-block:: python

	def scores(model, pc_horiz=1, pc_vert=2):
	    """Score plot with the percent of the variance each component explains on its axis."""
	    fig = model.score_plot(pc_horiz=pc_horiz, pc_vert=pc_vert, settings={"show_labels": True})
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
	the next figure shows what separates them.

The :ref:`score plot <LVM_interpreting_scores>` shows the last six batches away from the
rest, five of them outside the 95% confidence ellipse. Batches this far out pull the
components towards themselves, so the model will have to be rebuilt without them once they
have been examined.

The score plot answers one question about a batch: how far it sits *along* the directions
the model has found. The :ref:`SPE <LVM-interpreting-SPE-residuals>` answers a different
one: how far it sits *away* from them, in directions the model has not described. Drawing
the two against each other puts both questions in one figure. The horizontal axis is
:ref:`Hotelling's T2 <LVM-Hotellings-T2>`, a single number summarising how extreme a batch
is along the components, and the vertical axis is its SPE. Each has its own 95% limit, and
the two limits divide the plot into quadrants.

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

Batch 49 is alone in the upper left: the largest SPE of all batches with one of the
smallest :math:`T^2` values, an entirely ordinary batch along the two components and an
extreme one away from them. Its problem is not a large deviation along the main directions
of variation, which is what the scores measure, but a break in the correlation structure
that the two components describe. Batch 51 sits in the same quadrant. The other five of the
last six batches are in the lower right: extreme along the components, with residuals that
stay below the SPE limit.

Both statistics are needed: a plot of one alone would have missed one of these two
groups.

Batch 49: which variables, and when
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The raw data are ambiguous about batch 49. ``Flow-1`` looks suspicious in the overlay, but
it is a noisy tag in every batch. The SPE :ref:`contributions <LVM_contribution_plots>`
settle the question. For a batch model the contribution vector has one entry per
(tag, time) cell, 1000 entries here: the residual of that cell after the two-component
reconstruction. Write :math:`i` for the batch, :math:`k` for one of the :math:`K = 10` tags
and :math:`j` for one of the :math:`J = 100` time samples, so one cell of the unfolded row
is the pair :math:`(k, j)`. ``process_improve`` reports the SPE of a batch as the length of its
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

``Flow-1`` carries 3% of the residual. It belongs instead to the cooling-medium
temperature, ``Flow-2``, ``Press-2``, the heating-medium temperature and ``Press-3``, in
that order, and 80% of it falls in the eleven samples from 55 to 65. A short disturbance in
the heating, cooling and pressure systems over that stretch broke the usual relationship
between these tags.

The same event has been reported from a different model. Wold and co-workers (2009) monitor
batch 49 on-line against a three-component model built on batches 1 to 36, and their
contribution plot at sample 57 names the heating- and cooling-medium temperatures and the
pressures ``Press-2`` and ``Press-3`` as running too low from sample 57 until sample 65,
with ``Press-2`` the largest contributor. Those are four of the five tags and the same
window that the SPE contributions point at here, reached from a model built a different
way, on all 55 batches and after they had finished.

Nomikos and MacGregor report that the final quality of batch 49 was barely acceptable,
which is consistent with a short event rather than a batch that was wrong throughout. In
the raw data the cooling-medium temperature of batch 49 does fall away from the other
batches after sample 60, a change that is easy to pass over until the contributions point
at it.

The score outliers: batches 50 to 55
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Batches 50 to 55 are far out along the components, so the tool for them is the score
contribution: how much every (tag, time) cell contributes to :math:`t_1` or :math:`t_2`.
A score is the sum over the 1000 cells of the scaled value times the loading,
:math:`t_{i,1} = \sum_{k=1}^{K}\sum_{j=1}^{J} x_{i,kj}\, p_{kj,1}`, so a cell contributes
strongly when its value is far from average in the direction of the loading. The :ref:`loading <LVM_interpreting_loadings>`
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
sample to the last. The whole batch ran away from the average trajectory. The
:ref:`raw trajectory overlay <APPS_batch_case_dupont_overlay>` at the start of this case
study confirms it: in ``Press-1`` the pressure step of batch 54 and its later descent come
later than in the other batches, and its reactor temperature runs below them over the first
20 samples. Batches 50 and 52 also have large positive :math:`t_1` values and can be examined
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
	second_group = [37, 39, 43, 44, 45, 46, 47, 48]
	group_t2, group_t3 = model_b.scores_.loc[second_group].iloc[:, 1:3].mean()   # the group's average point
	fig = scores(model_b, 2, 3)
	fig.add_annotation(x=0, y=0, ax=group_t2, ay=group_t3, axref="x", ayref="y", text="",   # from the average point
	                   showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#4d4d4d")      # to the model centre
	fig.add_annotation(x=group_t2 / 2, y=group_t3 / 2, text="contribution direction", showarrow=False, yshift=12,
	                   textangle=-np.degrees(np.arctan2(group_t3, group_t2)))
	fig.show()

.. figure:: ../figures/batch/batch-case-dupont-model-b-scores.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Scores of model B on components 2 and 3; batches 37, 39 and 43 to 48 form a group at the top right, away from the main cloud, and a thick arrow labelled contribution direction runs from the group's average point to the model centre.
	:width: 600px
	:scale: 80
	:align: center

	Scores of model B on components 2 and 3. Batches 37, 39 and 43 to 48 (orange) form a
	group at the top right of the plot, away from the main cloud of batches. The arrow runs
	from the group's average point to the model centre: the direction along which the
	group's contributions below are computed.

With the extreme batches gone, a second group separates in the plane of :math:`t_2` and
:math:`t_3`: batches 37, 39 and 43 to 48.

A contribution is the weighted difference between two points, and either point can be the
average of a group of batches. The eight batches are compared here as a group against the
model centre, the average of all 48 (the arrow in the score plot): the columns are centred, so the group's mean row is
its displacement from the centre, and its contribution vector adds up to the group's mean
score.

.. code-block:: python

	scaled_b = model_b.unfold_and_scale(kept_b)
	per_component = {a: model_b.score_contributions(scaled_b, component=a) for a in (2, 3)}
	group = {a: c.loc[second_group].mean(axis=0) for a, c in per_component.items()}   # the group against the centre
	for a in (2, 3):
	    print(f"group mean t{a} = {model_b.scores_.loc[second_group].iloc[:, a - 1].mean():5.1f}",
	          f"(the contribution vector sums to {group[a].sum():5.1f});",
	          f"the other 40 batches: {model_b.scores_.drop(index=second_group).iloc[:, a - 1].mean():5.1f}")

.. code-block:: text

   group mean t2 =  15.0 (the contribution vector sums to  15.0); the other 40 batches:  -3.0
   group mean t3 =  14.8 (the contribution vector sums to  14.8); the other 40 batches:  -3.0

.. figure:: ../figures/batch/batch-case-dupont-group-contribution.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Left, the group's contribution to t2 and t3 summed per tag with each of the eight members as a dot; right, the same contributions summed per sample.
	:width: 1000px
	:scale: 80
	:align: center

	The contribution of the eight-batch group to :math:`t_2` and :math:`t_3`, summed per tag
	with each member as a dot (left) and summed per sample (right).

``TempC-1`` and ``Press-3`` carry most of the displacement on both components, every member
contributes in the same direction on those two tags, and the contributions are large over
the first 25 samples and small afterwards. Not every member is consistent with the average:
``TempH-1`` takes both signs across the eight, so its group mean is set by a few of them.
The group contribution is a starting point for a diagnosis of the group, to be checked
member by member.

.. code-block:: python

	for tag in ("TempC-1", "Press-3", "Press-2"):                    # the three largest contributions
	    overlay(kept_b, tag, {batch_id: ORANGE for batch_id in second_group}).show()

.. figure:: ../figures/batch/batch-case-dupont-group-raw.png
	:source: batch/batch-case-dupont-figures.py
	:alt: Three panels of raw trajectories over samples 0 to 30, the eight group batches in orange above the other 40 in light grey for TempC-1 and Press-3, with more overlap for Press-2.
	:width: 1000px
	:scale: 80
	:align: center

	The raw trajectories of the three tags with the largest contributions over the first 30
	samples: the eight batches of the group (orange) and the other 40 batches of model B
	(light grey).

The raw trajectories agree: the eight batches run above the other 40 in ``TempC-1`` and
``Press-3`` until about sample 25, and overlap them in ``Press-2``. Only batches 45 and 46
are on the list of poor or borderline quality; the other six produced acceptable product.
They were operated differently, not badly, and a model of normal operation can either
include enough of them to describe that mode or leave them out. The third model leaves
them out.

The final model, used to verify the unusual batches detected above
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model C is fitted on the 40 batches that remain once batch 49, batches 50 to 55 and the
eight batches of the second group are removed. Whether it describes normal operation is
checked by projecting those 15 batches onto it: each is unfolded and scaled with the centre
and scale of model C, its scores are estimated, and its :math:`T^2` and SPE are compared
with the 95% limits of the 40 training batches.

.. code-block:: python

	kept_c = {batch_id: batch for batch_id, batch in kept_b.items() if batch_id not in second_group}
	model_c = BatchPCA(n_components=3).fit(kept_c)
	print("R2 per component:", model_c.r2_per_component_.round(3).tolist())
	scores(model_c).show()
	left_out = {"batch 49": [49], "batches 50 to 55": list(range(50, 56)), "the second group": second_group}
	colours = {"batch 49": ORANGE, "batches 50 to 55": AQUA, "the second group": PURPLE}
	projected = {b: model_c.predict_online(batches[b], upto_k=model_c.n_timesteps_)   # a complete batch: its scores,
	             for ids in left_out.values() for b in ids}                             # T2 and SPE against model C
	outside = pd.DataFrame({b: (float(r.hotellings_t2), float(r.spe)) for b, r in projected.items()}, index=["T2", "SPE"]).T
	fig = influence_plot(model_c, highlight={}, labels=[])
	for label, ids in left_out.items():
	    fig.add_trace(go.Scatter(x=outside.loc[ids, "T2"], y=outside.loc[ids, "SPE"], mode="markers", name=label,
	                             marker=dict(size=10, color=colours[label]), text=ids, hovertemplate="batch %{text}"))
	fig.update_xaxes(type="log").update_yaxes(type="log")         # the projected batches lie far outside the limits
	fig.show()
	t2_limit, spe_limit = model_c.hotellings_t2_limit(conf_level=0.95), model_c.spe_limit(conf_level=0.95)
	print("left-out batches above the SPE limit:", sorted(outside.index[outside["SPE"] > spe_limit]))
	print("left-out batches above the T2 limit:", sorted(outside.index[outside["T2"] > t2_limit]))
	poor_quality = [38, 40, 41, 42]                                # in the training set, known poor final quality
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

	Left: scores of model C, with batches 38, 40, 41 and 42 (orange) marked. Right:
	Hotelling's :math:`T^2` against the SPE, on logarithmic axes, of the 40 training batches
	(blue) and of the 15 left-out batches projected onto model C: batch 49 (orange), batches
	50 to 55 (aqua) and the second group (purple).

Every one of the 15 lies above the SPE limit, most of them far above it, and the six score
outliers and batch 37 lie above the :math:`T^2` limit as well: the model built without them
flags them. The scores of the 40 training batches are spread more evenly than in the first
two models; a group of nine batches with larger :math:`t_1` values remains inside the 95%
confidence ellipse and is not pursued here. Batches 38, 40, 41 and 42, which produced poor
product and stayed in the training set, sit inside both limits.

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

The :ref:`SBR case study <APPS_batch_case_sbr_online>` runs the same check sample by
sample: a reference model on the normal batches, and limits computed at every sample, so
that a faulty batch is flagged while it is still running.

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

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process
  modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_",
  *Comprehensive Chemometrics*, **2.10**, 163-197, 2009. Sets out the two unfolding layouts,
  and analyses batch 49 of this dataset on-line.

* The full list of readings on batch data is on the
  :ref:`batch process monitoring <APPS_batch_monitoring>` page.
