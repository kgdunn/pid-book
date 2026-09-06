.. _APPS_batch_case_fmc:

Combining initial conditions and trajectories: multiblock batch PLS on a batch dryer
=====================================================================================

.. index::
	single: batch data; batch dryer case study
	pair: multiblock PLS; batch data
	pair: initial conditions; batch data
	single: missing data; batch data

An agricultural chemical is dried in an industrial batch dryer. Wet cake, the solid product
with the solvent still embedded in it, is charged to the dryer, and the solvent is driven off
and collected in a side tank. Chemical changes take place in the solid while it dries, so
the drying step sets part of the product quality, not only its residual solvent. The recipe
has three phases, each bounded by a landmark in the trajectories: solvent collection, from
the start of the batch until the agitator is turned up to high speed; the temperature ramp,
from there until the dryer temperature reaches its maximum; and cooling, from there to the
end of the batch. The operators adjusted the peak temperature set point from batch to
batch to correct the quality of the product, a manual feedback on quality. This is the case
study of Garcia-Munoz and co-workers (2003), and it is the most complete of the three batch
case studies, because every kind of information about a batch is present.

.. figure:: ../figures/examples/fmc/dryer_flowsheet.png
	:alt: Flowsheet of the batch dryer: the dryer tank with its agitator and heating medium, the collector tank with its level measurement, a pressure controller between them, and two temperature controllers for the jacket and the dryer; the ten measured trajectories are numbered on the drawing.
	:width: 700px
	:scale: 80
	:align: center

	The batch dryer and its ten measured trajectories: the level in the collector tank
	(``CTankLvl``), the differential pressure (``DiffPres``), the dryer pressure
	(``DryPress``), the agitator power, torque and speed (``Power``, ``Torque``,
	``Agitator``), the jacket temperature and its set point (``J-Temp``, ``J-Temp-SP``) and
	the dryer temperature and its set point (``D-Temp``, ``D-Temp-SP``).

Four blocks of data describe each batch:

* :math:`\mathbf{Z}_\text{chem}`, the chemistry of the wet cake before the batch: eleven
  measurements, ``Z1`` to ``Z11``.
* :math:`\mathbf{Z}_\text{op}`, nine values the original study calls the operating
  conditions: the weight of the cake charged, which is known before the batch starts, and
  eight landmarks read off the batch's own trajectories when they were aligned: the
  collector tank level and the dryer temperature at the end of the first phase, the peak
  dryer temperature, the length of each of the three phases and of the high-speed
  agitation, and the slope of the temperature ramp.
* :math:`\mathbf{X}`, the ten trajectories over the batch, and an eleventh described below.
* :math:`\mathbf{Y}`, eight final quality attributes: seven numbered attributes, ``Y1`` to
  ``Y11`` with gaps, and the residual solvent concentration ``SolventConc``. The original
  study had eleven; the public workbook carries these eight.

.. figure:: ../figures/examples/fmc/fmc-data-structure.png
	:alt: The four blocks side by side: two flat blocks with one row per batch for the chemistry and the operating conditions, a three-way block of trajectories with batches, variables and time as its dimensions, and a flat block of final properties.
	:width: 800px
	:scale: 80
	:align: center

	The four blocks: two blocks with one row per batch describing its initial conditions
	and its operation, the three-way block of trajectories, and the block of final
	properties.

The questions are those a plant asks, in the order it asks them. What does product quality
look like, and do the batches fall into groups? Do the initial conditions explain the
quality? What do the trajectories add? Which batches deserve a closer look? The original
study answers them with a ladder of models, each with two components, and this page follows
the same ladder:

* A PCA on the quality block.
* A PLS model from each initial-condition block to the quality block.
* A multiblock PLS on both initial-condition blocks.
* A batch PCA and a batch PLS on the trajectories.
* A batch multiblock PLS that joins all three blocks.

The data
~~~~~~~~

The `batch dryer dataset <https://openmv.net/info/batch-dryer>`_ is a workbook with the four
blocks over 59 batches, one sheet each. The batch identifiers run from 2 to 71 with gaps,
and the plant's disposition is encoded in the numbering: batches 1 to 33 were classed as
good, 34 to 61 as abnormal, and 62 to 71 as high in residual solvent. As in the first case
study, that classification plays no part in building the models; it is compared afterwards
with what the models find. The score plots on this page carry it as a colour and a marker
shape per class, so that the comparison can be read off each plot.

Batch durations vary widely, so the trajectories were aligned within each phase before
archiving, to 325 samples per batch. The first two phases were aligned against a maturity
variable, a quantity that moves one way through the phase and so can be sampled at equal
steps of itself instead of time: the collector tank level, then the dryer temperature. The
cooling phase was stretched linearly. In the aligned data the first phase ends at sample 175
and the ramp at sample 249.

``ClockTime``, the wall-clock time at each aligned sample, is carried along as an eleventh
trajectory. After alignment it records how much each batch was stretched or compressed to
fit the template: a batch whose ramp took longer than usual has a ``ClockTime`` that rises
faster over that phase. Alignment itself is a topic of its own; the
`batch_dtw <https://github.com/kgdunn/process-improve/blob/main/src/process_improve/batch/preprocessing.py>`_ function in ``process_improve`` implements dynamic time warping, and the unaligned
trajectories of this dryer are bundled with the package as ``load_dryer``.

Thirteen batches have no chemistry measurements at all. The original study excluded the
batches without a chemistry analysis and worked with 44; ``load_fmc`` returns the
identifiers of the thirteen as ``missing_chemistry`` so that the exclusion can be
reproduced, and 46 batches remain. They still contain genuine missing values: 19 cells
in the quality block, one in the chemistry block, and 1340 cells in the eleven trajectories
of ten batches, where the record has gaps. The ``PCA``, ``PLS`` and
`MBPLS <https://github.com/kgdunn/process-improve/blob/main/src/process_improve/multivariate/_mbpls.py>`_ estimators of the ``multivariate`` module handle missing values through the
:ref:`NIPALS algorithm <LVM_PCA_NIPALS_algorithm>`, which is why this case study uses them
directly, after unfolding the trajectories with ``dict_to_wide``, instead of the
``BatchPCA`` and ``BatchPLS`` classes of the two earlier case studies, which require
complete data.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.batch import dict_to_wide, load_fmc, unfolded_contribution_plot
	from process_improve.multivariate import PCA, PLS, MCUVScaler
	from process_improve.multivariate.methods import MBPLS

	fmc = load_fmc()                                # https://openmv.net/file/batch-dryer.xlsx
	keep = [batch_id for batch_id in fmc.batch_ids if batch_id not in fmc.missing_chemistry]
	X = {batch_id: fmc.X[batch_id] for batch_id in keep}
	Y, Zop, Zchem = fmc.Y.loc[keep], fmc.Zop.loc[keep], fmc.Zchem.loc[keep]
	groups = pd.Series(pd.cut(keep, bins=[0, 33, 61, 71], labels=["good", "abnormal", "high solvent"]).astype(str), index=keep)
	incomplete = [batch_id for batch_id, batch in X.items() if batch.isna().any().any()]
	print(len(X), "batches kept; missing cells: Y", int(Y.isna().sum().sum()), "Zchem", int(Zchem.isna().sum().sum()),
	      "X in batches", incomplete)
	average = pd.concat(X.values()).groupby(level=0).mean()                  # the average trajectory of every tag
	agitator = average["Agitator"]
	phase_ends = (int((agitator > (agitator.min() + agitator.max()) / 2).idxmax()), int(average["D-Temp"].idxmax()))
	print(*phase_ends)                              # the first high-speed sample, and the sample of the peak dryer temperature
	# 175 249

.. code-block:: python

	GREY, ORANGE, AQUA, BLUE = "#c8c8c8", "#c55a11", "#1baf7a", "#1f3d7a"                  # figure colours
	PURPLE, GOLD, BAND = "#6f42c1", "#d4a017", "#e9edf4"                                   # ... and the shading behind bars
	DARK_GREY = "#8c8c8c"                                                                  # the phase-separator lines
	STYLES = {"good": (BLUE, "circle"), "abnormal": (PURPLE, "triangle-up"), "high solvent": (GOLD, "square")}

	def overlay(batches, tag, highlight):
	    """One tag for every batch in grey, the batches in `highlight` (id -> colour) on top, the phase ends marked."""
	    fig = go.Figure()
	    for x in phase_ends:
	        fig.add_vline(x=x, line_color=DARK_GREY, line_dash="dash", line_width=1)
	    for batch_id, batch in batches.items():
	        if batch_id not in highlight:
	            fig.add_trace(go.Scatter(y=batch[tag], mode="lines", line=dict(color=GREY, width=1), showlegend=False))
	    for batch_id, colour in highlight.items():
	        fig.add_trace(go.Scatter(y=batches[batch_id][tag], mode="lines", name=f"batch {batch_id}",
	                                 line=dict(color=colour, width=3)))
	    fig.update_layout(title=tag, xaxis_title="Sample [aligned time]", height=320)
	    return fig

	for tag in ("D-Temp", "J-Temp", "CTankLvl", "ClockTime"):
	    overlay(X, tag, {20: ORANGE}).show()

.. _APPS_batch_case_fmc_overlay:

.. figure:: ../figures/batch/batch-case-fmc-raw-trajectories.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Four trajectories of the 46 batches in grey with batch 20 in orange, with dashed vertical lines at the ends of the first two phases; the dryer temperature of batch 20 sits well above the others through the first 170 samples, and its ClockTime rises steeply between samples 200 and 240.
	:width: 900px
	:scale: 80
	:align: center

	Four trajectories of the 46 batches (grey) with batch 20 (orange) drawn on top. The
	dryer temperature of batch 20 sat well above the other batches through the whole
	solvent-collection phase, and its ``ClockTime`` rises steeply between samples 200 and
	240, where its temperature ramp took longer than usual. The gaps in the orange line are
	missing samples. The dashed lines mark the ends of the first two phases, at samples 175
	and 249.

The batch chosen for the overlay, batch 20, is one to keep in mind. Its dryer temperature
averaged 33.8 units over the first 170 samples, the solvent-collection phase, against 23.6
units for the other batches, and its ``ClockTime`` shows that its temperature ramp took
longer than usual. The gaps in the orange line are the missing samples mentioned earlier;
in a raw plot a missing cell is simply a gap.

Product quality on its own
~~~~~~~~~~~~~~~~~~~~~~~~~~

Product quality is a multivariate property. A :ref:`PCA <SECTION_PCA>` on the eight quality
attributes shows how the batches group in quality space before any process data are
involved.

.. code-block:: python

	y_scaled = MCUVScaler().fit_transform(Y)              # missing cells pass through; PCA switches to NIPALS
	pca_y = PCA(n_components=2).fit(y_scaled)
	print("PCA on Y, R2 cumulative:", pca_y.r2_cumulative_.round(3).tolist())
	def group_scatter(fig, x, y, highlight, row=None, col=None, showlegend=True):
	    """One trace per class of the plant's disposition (colour and marker shape from STYLES); the batches in
	    `highlight` (id -> colour) are drawn larger and labelled, in the marker shape of their class."""
	    for label, (colour, symbol) in STYLES.items():
	        members = [b for b in x.index if groups[b] == label and b not in highlight]
	        fig.add_trace(go.Scatter(x=x.loc[members], y=y.loc[members], mode="markers", name=f"classed {label}",
	                                 marker=dict(color=colour, symbol=symbol, size=14 if symbol == "square" else 16),
	                                 text=members,
	                                 hovertemplate="batch %{text}", showlegend=showlegend), row=row, col=col)
	    for b, colour in highlight.items():
	        fig.add_trace(go.Scatter(x=[x.loc[b]], y=[y.loc[b]], mode="markers+text", text=[str(b)], textposition="top right",
	                                 marker=dict(color=colour, symbol=STYLES[groups[b]][1],
	                                             size=20 if STYLES[groups[b]][1] == "square" else 22), showlegend=False),
	                      row=row, col=col)
	    return fig

	def scores(model, r2, highlight):
	    """Score plot of a PCA or PLS model coded by disposition, with the percent of the variance each component
	    explains (`r2`, per component) on its axes and the 95% confidence ellipse."""
	    t = model.scores_
	    fig = group_scatter(go.Figure(), t.iloc[:, 0], t.iloc[:, 1], highlight)
	    ex, ey = model.ellipse_coordinates(score_horiz=1, score_vert=2, conf_level=0.95)
	    fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", line=dict(color=GREY, dash="dash"), name="95% confidence ellipse"))
	    r2 = np.asarray(r2)
	    fig.update_layout(xaxis_title=f"t1 [{r2[0]:.1%}]", yaxis_title=f"t2 [{r2[1]:.1%}]", height=440)
	    return fig

	def shade_alternate(fig, n, row=None, col=None):
	    """Shade every second position of a bar chart, so that neighbouring groups of bars read apart."""
	    for k in range(0, n, 2):
	        fig.add_vrect(x0=k - 0.5, x1=k + 0.5, fillcolor=BAND, line_width=0, layer="below", row=row, col=col)

	def explained_x(pls_model):
	    """R2 of X per component of a PLS model, from the cumulative R2 of its columns."""
	    return np.diff([0.0, *pls_model.r2_per_variable_.mean(axis=0)])

	scores(pca_y, pca_y.r2_per_component_, {61: ORANGE, 14: AQUA}).show()
	print(pca_y.scores_.groupby(groups).agg(["mean", "min", "max", "count"]).round(2))
	contributions = pca_y.score_contributions(y_scaled, component=1)
	fig = go.Figure()
	for batch_id, colour in ((61, ORANGE), (14, AQUA)):
	    fig.add_trace(go.Bar(x=list(Y.columns), y=contributions.loc[batch_id], name=f"batch {batch_id}", marker_color=colour))
	shade_alternate(fig, len(Y.columns))
	fig.update_layout(title="Contributions to t1 of one batch from each group", yaxis_title="Contribution", height=320)
	fig.show()

.. figure:: ../figures/batch/batch-case-fmc-quality-pca.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the scores of the two-component PCA on the quality block, coded by the plant's disposition with blue circles for good, purple triangles for abnormal and gold squares for high solvent, the abnormal batches mostly at negative t1 and batches 61 and 14 at opposite ends; right, their contributions to t1 for each quality attribute on alternately shaded positions, mirror images, with no bar for the missing Y2 of batch 61.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of the two-component PCA on the quality block, coded by the plant's
	disposition (blue circles good, purple triangles abnormal, gold squares high solvent);
	batches 61 (orange) and 14 (aqua) are at opposite ends of :math:`t_1`. Right: their
	contributions to :math:`t_1`, attribute by attribute, are mirror images. ``Y2`` is
	missing for batch 61 and has no bar.

Two components explain 70.3% of the quality block. The first component separates the
batches by their disposition: 15 of the 17 batches classed as abnormal have a negative
:math:`t_1`, and 21 of the 23 batches classed as good have a positive one. The six batches
classed as high in residual solvent all have positive :math:`t_1` and positive :math:`t_2`
values. Batches 61 and 14 are one member of each of the first two groups, and their
:math:`t_1` contributions are mirror images, with the same attributes (``Y1``, ``Y4``,
``Y6``, ``Y10`` and ``Y11``) low in the abnormal group and high in the good group. The first
component is a general level of quality rather than a trade-off between attributes. A
missing quality cell has no contribution: ``Y2`` was not measured for batch 61.

Do the initial conditions explain quality?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A PLS model from each initial-condition block to the quality block answers this question
one block at a time. The blocks are centred and scaled with ``MCUVScaler`` before the fit,
and ``scale=False`` tells the ``PLS`` class not to scale them again.

.. code-block:: python

	zchem_scaled = MCUVScaler().fit_transform(Zchem)
	zop_scaled = MCUVScaler().fit_transform(Zop)
	pls_chem = PLS(n_components=2, scale=False).fit(zchem_scaled, y_scaled)
	pls_op = PLS(n_components=2, scale=False).fit(zop_scaled, y_scaled)
	print("PLS Zchem -> Y, R2Y cumulative:", pls_chem.r2_cumulative_.round(3).tolist())
	print("PLS Zop -> Y, R2Y cumulative:", pls_op.r2_cumulative_.round(3).tolist())
	scores(pls_op, explained_x(pls_op), {20: ORANGE}).show()
	print("batch 20 on Zop, t1 contributions:", pls_op.score_contributions(zop_scaled, component=1).loc[20].round(2).to_dict())

Each initial-condition block on its own explains about a quarter of the quality block after
two components, the operating conditions more than the chemistry: 26.2% against 22.2%, the
same order the original study found on its 44 batches and eleven quality attributes. Batch
20 stands out in the score plot of the operating-condition model, and its contributions to
:math:`t_1` come from the recipe timings ``Time2`` (-1.42) and ``Time4`` (-1.01) and from the
temperature slope (-1.27). This is the batch whose temperature ramp was seen to take longer
in the trajectory overlay; the timings in :math:`\mathbf{Z}_\text{op}` record the same
batch as unusual.

Both blocks together: multiblock PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two blocks can be modelled together in a multiblock PLS model. Multiblock PLS fits one
set of components to several X blocks at once. Each block gets its own block scores and
block weights, and the block scores are combined into a super score, one number per batch
per component, through super weights that say how much each block pulls. The ``MBPLS``
class scales each block on its own and then divides it by the square root of its number of
columns, so a block with eleven columns and a block with nine pull on the super score with
equal total weight, and no block dominates only because it is wider. The super-score plot
shows the batches in the combined space, and the :math:`R^2` per block says how much of
each block the components describe.

.. code-block:: python

	blocks_z = {"Zchem": Zchem, "Zop": Zop}
	mb_z = MBPLS(n_components=2).fit(blocks_z, Y)
	print("MBPLS Z -> Y, R2Y cumulative:", mb_z.r2_y_cumulative_.round(3).tolist())
	print("R2X per block after two components:", mb_z.r2_x_per_block_cumulative_.iloc[:, -1].round(3).to_dict())

	def block_axes(fig, r2, row=None, col=None, prefix="block t", note=""):
	    """Axis titles of one score plot, with the percent of the variance each component explains (`r2`)."""
	    r2 = np.asarray(r2)
	    fig.update_xaxes(title_text=f"{prefix}1 [{note}{r2[0]:.1%}]", row=row, col=col)
	    fig.update_yaxes(title_text=f"{prefix}2 [{note}{r2[1]:.1%}]", row=row, col=col)

	fig = make_subplots(rows=2, cols=2, subplot_titles=["Super scores", "Super weights", "Zchem block scores", "Zop block scores"])
	super_t = mb_z.super_scores_
	group_scatter(fig, super_t.iloc[:, 0], super_t.iloc[:, 1], {20: ORANGE}, row=1, col=1)
	block_axes(fig, mb_z.r2_y_per_component_, 1, 1, prefix="super t", note="R2Y ")
	weights = mb_z.super_weights_                                            # one row per block, one column per component
	for a, colour in ((1, BLUE), (2, ORANGE)):
	    fig.add_trace(go.Bar(x=list(weights.index), y=weights.iloc[:, a - 1], name=f"component {a}", marker_color=colour), row=1, col=2)
	for col, (name, block_t) in enumerate(mb_z.block_scores_.items(), start=1):
	    group_scatter(fig, block_t.iloc[:, 0], block_t.iloc[:, 1], {20: ORANGE}, row=2, col=col, showlegend=False)
	    block_axes(fig, np.diff([0.0, *mb_z.r2_x_per_block_cumulative_.loc[name]]), 2, col)
	fig.update_layout(height=820).show()

.. figure:: ../figures/batch/batch-case-fmc-mbpls-z.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Four panels: the super scores of the multiblock PLS on the two initial-condition blocks, coded by disposition, with batch 20 at the lower left; the super weights of the two components, larger for the operating-condition block on both; the chemistry block scores, where batch 20 sits inside the cloud of batches; and the operating-condition block scores, where batch 20 sits far outside it.
	:width: 1000px
	:scale: 80
	:align: center

	Top left: super scores of the multiblock PLS on the two initial-condition blocks, coded
	by the plant's disposition, with batch 20 (orange) at the lower left. Top right: the
	super weights of the two components. Bottom: the block scores of the same model; batch
	20 sits inside the cloud of batches in the chemistry block (left) and far outside it in
	the operating-condition block (right).

Together the two blocks explain 36.4% of the quality block after two components, more than
either alone, and the components describe 29.6% of the chemistry block and 35.6% of the
operating-condition block. The super weights give the operating-condition block the larger
pull on both components. The block scores make the same point for a single batch: batch 20
sits inside the cloud of batches in the chemistry block and far outside it in the
operating-condition block. It is unusual in its operation, not in its chemistry.

The trajectories alone
~~~~~~~~~~~~~~~~~~~~~~

The trajectories are unfolded batchwise with ``dict_to_wide``: one row per batch of 11 tags
times 325 samples, 3575 columns, the layout the ``BatchPCA`` class uses internally. The
eleventh tag is ``ClockTime``, so that how fast each batch moved through each phase is part
of what the models see. ``MCUVScaler`` returns flat column labels, so the two-level (tag,
sequence) column index is re-attached after scaling; the batch plots read it.

.. code-block:: python

	wide = dict_to_wide(X)                # the ten process tags and ClockTime: 11 x 325 = 3575 columns per batch
	x_scaled = MCUVScaler().fit_transform(wide)
	x_scaled.columns = wide.columns       # MCUVScaler returns flat labels; the batch plots need the (tag, sequence) index
	print(list(wide.shape), int(wide.isna().sum().sum()))       # batches x columns; missing cells
	# [46, 3575] 1340
	pca_x = PCA(n_components=2).fit(x_scaled)
	print(pca_x.r2_per_component_.round(3).tolist())            # R2 of the trajectory block, per component
	# [0.231, 0.146]
	scores(pca_x, pca_x.r2_per_component_, {20: ORANGE}).show()
	t2, spe = pca_x.hotellings_t2_.iloc[:, -1], pca_x.spe_.iloc[:, -1]
	t2_limit, spe_limit = pca_x.hotellings_t2_limit(conf_level=0.95), pca_x.spe_limit(conf_level=0.95)
	both = sorted(t2.index[(t2 > t2_limit) & (spe > spe_limit)])            # above both limits
	spe_only = sorted(spe.index[(spe > spe_limit) & (t2 <= t2_limit)])      # above the SPE limit only
	print(both, spe_only)
	# [20] [41, 51]

	def influence_plot(model, highlight, labels, conf_level=0.95):
	    """Hotelling's T2 against SPE, one marker per batch coded by disposition, with both limits drawn."""
	    t2, spe = model.hotellings_t2_.iloc[:, -1], model.spe_.iloc[:, -1]
	    fig = group_scatter(go.Figure(), t2, spe, highlight)
	    fig.add_vline(x=model.hotellings_t2_limit(conf_level=conf_level), line_dash="dash", line_color=GREY)
	    fig.add_hline(y=model.spe_limit(conf_level=conf_level), line_dash="dash", line_color=GREY)
	    for batch_id in labels:
	        fig.add_annotation(x=t2.loc[batch_id], y=spe.loc[batch_id], text=str(batch_id),
	                           showarrow=False, xshift=13, yshift=9)
	    fig.update_layout(xaxis_title="Hotelling's T\u00b2", yaxis_title="SPE", height=420)
	    return fig

	influence_plot(pca_x, highlight={20: ORANGE}, labels=[41, 51]).show()

.. figure:: ../figures/batch/batch-case-fmc-batch-pca.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Scores and the influence plot of the batch PCA on the trajectories, coded by the plant's disposition; batch 20 is outside the confidence ellipse and is the only batch above both limits, while batches 41 and 51 are above the SPE limit only.
	:width: 1000px
	:scale: 80
	:align: center

	Scores (left) and Hotelling's :math:`T^2` against the SPE (right) of the batch PCA on the
	trajectories, coded by the plant's disposition. Batch 20 (orange) is outside the 95%
	confidence ellipse and is the only batch above both limits; batches 41 and 51 are above
	the SPE limit only.

Two components describe 37.6% of the batch-to-batch variation in the trajectories. Batch 20
is the only batch above both limits, with a :math:`T^2` twice its limit and an SPE next to
the largest of the 46 batches, so it is both unusual along the components and poorly
described by them. Batches 41 and 51 are above the SPE limit alone, and batch 47 is just
below it.

.. code-block:: python

	tags = list(wide.columns.get_level_values("tag").unique())
	p1 = pca_x.loadings_.iloc[:, 0].unstack(level="sequence").reindex(index=tags)             # rows = tags, columns = time
	r2_cell = pd.Series(pca_x.r2_per_variable_.iloc[:, -1].to_numpy(), index=wide.columns)    # R2 of every cell, two components
	r2_grid = r2_cell.unstack(level="sequence").reindex(index=tags)
	r2_tag = r2_cell.groupby(level="tag").mean().round(2)
	print(r2_tag.nlargest(2).to_dict(), r2_tag.nsmallest(1).to_dict())    # the tags the components describe best and least
	# {'CTankLvl': 0.71, 'ClockTime': 0.71} {'Agitator': 0.08}
	fig = make_subplots(rows=3, cols=4, subplot_titles=tags, specs=[[{"secondary_y": True}] * 4] * 3, shared_xaxes=True)
	for k, tag in enumerate(tags):
	    row, col = divmod(k, 4)
	    fig.add_trace(go.Scatter(x=p1.columns, y=p1.loc[tag], mode="lines", line=dict(color=BLUE), name="p1",
	                             showlegend=k == 0), row=row + 1, col=col + 1)
	    fig.add_trace(go.Scatter(x=r2_grid.columns, y=r2_grid.loc[tag], mode="lines", line=dict(color=ORANGE, width=1),
	                             opacity=0.55, name="R2 per cell", showlegend=k == 0), row=row + 1, col=col + 1, secondary_y=True)
	    fig.update_yaxes(range=[0, 1], showgrid=False, row=row + 1, col=col + 1, secondary_y=True)
	    for x in phase_ends:
	        fig.add_vline(x=x, line_color=GREY, line_width=1, row=row + 1, col=col + 1)
	fig.update_layout(height=780, title="Loading p1 (blue) and R2 per cell (orange) of the batch PCA over the batch").show()

.. figure:: ../figures/batch/batch-case-fmc-loadings-p1.png
	:source: batch/batch-case-fmc-figures.py
	:alt: The first loading of the batch PCA over the batch, one panel per tag, with the R2 of every cell after two components on a second axis in orange and two faint vertical lines at the ends of the first two phases; the loading is positive and nearly constant for the collector tank level and, after the first 50 samples, for the clock time, negative through the first phase for the dryer pressure and the jacket temperature set point, and changes sign within the batch for the dryer temperature; the R2 is highest for the collector tank level and the clock time and falls in the cooling phase for most tags.
	:width: 1000px
	:scale: 80
	:align: center

	Loading :math:`\mathbf{p}_1` of the batch PCA over the batch (blue), one panel per tag,
	with the :math:`R^2` of each (tag, time) cell after two components (orange, right-hand
	axis) and the ends of the first two phases at samples 175 and 249 (grey). The loading is
	positive and nearly constant for the collector tank level, and for the clock time after
	the first 50 samples, so :math:`t_1` is largely a measure of how much solvent a batch
	collected and how much clock time it used. The dryer pressure, the jacket temperature set
	point and the dryer temperature have loadings of both signs within the batch.

The loading of the first component is positive and nearly constant for the collector tank
level over the whole batch, and for the clock time once the batch is under way: a batch with
a high :math:`t_1` collected more solvent than average at every point of the batch and took
more clock time to reach each point. The other tags have loadings that change sign within
the batch, with the dryer pressure negative through the solvent-collection phase and the
dryer temperature negative in the first phase and positive in the ramp and cooling phases.

The :math:`R^2` per cell says how much of the batch-to-batch variation in that cell the two
components describe, and so where the loadings can be read with confidence. The collector
tank level and the clock time are described best, at about 70% of their variance on average,
and the agitator speed least, at under 10%. For most tags the :math:`R^2` falls in the
cooling phase, so the model says little about how the batches differ there.

A missing cell has no residual and no contribution. Batch 20 is one of the ten batches with
missing samples, and its scores are estimated from the cells it does have, the same estimate
the NIPALS fit used, so its contributions are defined at every observed cell and absent only
at the missing ones. As in the :ref:`first case study <APPS_batch_case_dupont>`, the vector
has one entry per (tag, time) cell, here :math:`K = 11` tags by :math:`J = 325` time
samples.

.. code-block:: python

	squared = pca_x.spe_contributions(x_scaled) ** 2      # for a batch with missing cells, from its observed cells
	spe_share = squared.div(squared.sum(axis=1), axis=0) * 100
	share_20 = spe_share.loc[20]
	gaps = share_20[share_20.isna()].index.get_level_values("sequence")
	print(len(gaps), int(gaps.min()), int(gaps.max()))      # missing cells of batch 20, and the first and last sample with one
	# 205 34 109
	unfolded_contribution_plot(spe_share.fillna(0.0), batch_id=20, by_tag=True).show()
	by_tag = share_20.groupby(level="tag", sort=False).sum()
	print(f"{by_tag.idxmax()} {by_tag.max():.0f}")           # the tag carrying the largest share of the SPE
	# DryPress 49
	by_time = share_20.groupby(level="sequence").sum()
	first, second = phase_ends
	print(f"{by_time.loc[:first - 1].sum():.0f} {by_time.loc[first:second].sum():.0f} {by_time.loc[second + 1:].sum():.0f}")   # per phase
	# 58 31 11
	fig = go.Figure(go.Bar(x=list(by_time.index), y=by_time, marker_color=BLUE))
	for x in phase_ends:
	    fig.add_vline(x=x, line_color=ORANGE, line_width=1.5)
	fig.update_layout(title="Batch 20: share of the SPE per sample", xaxis_title="Sample [aligned time]",
	                  yaxis_title="Share of SPE [%]", height=320).show()
	overlay(X, "DryPress", {20: ORANGE}).show()
	print(round(X[20]["DryPress"].iloc[:first].mean()), round(average["DryPress"].iloc[:first].mean()))   # phase 1: batch 20, average
	# 85 37

.. figure:: ../figures/batch/batch-case-fmc-batch-20-spe-contributions.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three panels for batch 20: the share of the SPE carried by each unfolded cell, blank between samples 34 and 109 in every tag but the collector tank level where the record has gaps, and largest in the dryer pressure through the first phase; the shares summed per tag, half of them in the dryer pressure; and the shares summed per sample with orange lines at the phase ends, most of the share in the first phase.
	:width: 800px
	:scale: 80
	:align: center

	Top: the share of the SPE of batch 20 carried by each (tag, time) cell; the blank
	positions between samples 34 and 109 are the missing cells, which carry no residual.
	Middle: the same shares summed per tag. Bottom: summed per sample, with the ends of the
	first two phases in orange. The dryer pressure carries half of the residual, and most of
	it lies in the first phase.

The residual of batch 20 belongs to the dryer pressure (49%), and most of it lies in the
first phase (58% of the total): the dryer pressure of batch 20 sat far above the other
batches through the solvent-collection phase, at 85 units against 37 for the average batch,
and through the ramp, where its dryer temperature was also seen to run hot in the
:ref:`raw trajectory overlay <APPS_batch_case_fmc_overlay>`. The temperatures, the power
and the torque share the rest in small parts.

Trajectories to quality
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	pls_x = PLS(n_components=2, scale=False).fit(x_scaled, y_scaled)
	print(pls_x.r2_cumulative_.round(3).tolist())               # R2 of the quality block, cumulative
	# [0.266, 0.41]
	scores(pls_x, explained_x(pls_x), {13: ORANGE, 5: AQUA, 7: AQUA}).show()
	t1 = pls_x.score_contributions(x_scaled, component=1)
	unfolded_contribution_plot(t1, batch_id=13).show()
	print(t1.loc[13].groupby(level="tag", sort=False).sum().nsmallest(4).round(1).to_dict())   # batch 13's four largest
	# {'ClockTime': -8.1, 'CTankLvl': -8.0, 'D-Temp': -4.7, 'J-Temp-SP': -4.2}
	for tag in ("D-Temp", "CTankLvl", "ClockTime", "J-Temp-SP"):
	    overlay(X, tag, {13: ORANGE, 5: AQUA, 7: BLUE}).show()
	print({batch_id: round(float(X[batch_id]["CTankLvl"].iloc[-1])) for batch_id in (13, 5, 7)})   # collector level at the end
	# {13: 52, 5: 87, 7: 77}
	print({batch_id: int(X[batch_id]["ClockTime"].iloc[174]) for batch_id in (13, 5, 7)})         # clock time when phase 1 ends
	# {13: 29, 5: 113, 7: 62}
	pls_x.predictions_vs_observed_plot(y_observed=y_scaled, variable="SolventConc").show()

.. figure:: ../figures/batch/batch-case-fmc-batch-pls.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the scores of the batch PLS model from the trajectories to the quality block with batch 13 at the low end of t1 and batches 5 and 7 on the other side; right, the contributions of batch 13 to t1 summed per tag, all negative and led by the clock time and the collector tank level.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of the batch PLS model from the trajectories to the quality block, coded by
	the plant's disposition, with batch 13 (orange) and batches 5 and 7 (aqua) marked. Right:
	the contributions of batch
	13 to :math:`t_1`, summed per tag; every tag contributes in the same direction and the
	clock time and the collector tank level lead.

The trajectories explain 41.0% of the quality block after two components, more than the
initial conditions did (26.2% at best for a single block). Batch 13 is at the low end of
:math:`t_1`, and its contributions are all of the same sign, with the clock time (-8.1) and
the collector tank level (-8.0) leading, then the dryer temperature (-4.7) and the jacket
temperature set point (-4.2). Batches 5 and 7 lie on the other side of :math:`t_1`, among
the batches classed abnormal, although both were classed good; they are drawn in the same
overlay, and the block scores of the final model come back to them.

.. _APPS_batch_case_fmc_overlay_13:

.. figure:: ../figures/batch/batch-case-fmc-raw-batches-13-5-7.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Four trajectories of the 46 batches in grey with batches 13 in orange, 5 in aqua and 7 in blue, with dashed vertical lines at the ends of the first two phases; batch 13 collected less solvent than almost every other batch, reached the end of the first phase in less clock time than most, and cooled faster at the end of the batch.
	:width: 900px
	:scale: 80
	:align: center

	Four trajectories of the 46 batches (grey) with batches 13 (orange), 5 (aqua) and 7
	(blue) drawn on top. Batch 13 collected less solvent than almost every other batch,
	reached the end of the first phase in less clock time than most, and cooled faster at
	the end of the batch. The dashed lines mark the ends of the first two phases.

The :ref:`overlay of these three batches <APPS_batch_case_fmc_overlay_13>` shows what the
contributions of batch 13 refer to. Its collector tank level
levelled off at 52 units, against 77 units for batch 7, 87 units for batch 5 and up to 117
units for the batches that collected the most; its first phase took 29 clock samples,
against 62 for batch 7 and 113 for batch 5; and its dryer temperature fell faster than any
other batch in the cooling phase. Batch 13 was
classed as a good batch, so a batch at the end of a component is not necessarily a bad one.
The component describes a direction of variation in the trajectories that is related to
quality, and batch 13 is the batch furthest along it. The observed-against-predicted plot
of the residual solvent concentration, one of the attributes on which the batches are
dispositioned, shows how far the trajectories go towards predicting it; the same plot is
drawn again for the final model, in the next section.

All three blocks: batch multiblock PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final model joins the two initial-condition blocks and the unfolded trajectory block in
one multiblock PLS model. The trajectory block enters as 3575 columns; dividing each block
by the square root of its number of columns keeps it from drowning out the eleven chemistry
columns and the nine operating columns.

.. code-block:: python

	blocks = {"Zchem": Zchem, "Zop": Zop, "X": wide}
	mb = MBPLS(n_components=2).fit(blocks, Y)
	print(mb.r2_y_cumulative_.round(3).tolist())                # R2 of the quality block, cumulative
	# [0.37, 0.472]
	print(mb.r2_x_per_block_cumulative_.iloc[:, -1].round(3).to_dict())   # R2 of each block after two components
	# {'Zchem': 0.233, 'Zop': 0.304, 'X': 0.259}
	print(mb.super_vip_.round(2).to_dict())                     # super VIP per block
	# {'Zchem': 0.86, 'Zop': 1.07, 'X': 1.06}
	super_t = mb.super_scores_
	fig = group_scatter(go.Figure(), super_t.iloc[:, 0], super_t.iloc[:, 1], {13: ORANGE, 5: AQUA, 7: AQUA})
	block_axes(fig, mb.r2_y_per_component_, prefix="super t", note="R2Y ")
	fig.update_layout(height=440).show()
	mb.super_weights_bar_plot(component=1).show()
	unfolded_contribution_plot(mb.score_contributions(blocks, component=1)["X"], batch_id=13).show()
	mb.predictions_vs_observed_plot(Y, variable="SolventConc").show()

.. figure:: ../figures/batch/batch-case-fmc-batch-mbpls.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three panels: the super scores of the batch multiblock PLS with batches 13, 5 and 7 marked; the R2 of each block after two components beside the super VIP of each block; and the observed against fitted residual solvent concentration with batch 13 marked.
	:width: 1100px
	:scale: 80
	:align: center

	Left: super scores of the batch multiblock PLS, coded by the plant's disposition, with
	batches 13 (orange), 5 and 7 (aqua) marked. Middle: :math:`R^2` of each block after two components (blue) and the super VIP
	of each block (orange). Right: observed and fitted residual solvent concentration, with
	batch 13 marked.

The combined model explains 47.2% of the quality block after two components, against 41.0%
for the trajectories alone and 36.4% for the two initial-condition blocks together. The
components describe 23.3% of the chemistry block, 30.4% of the operating-condition block
and 25.9% of the trajectory block. The Variable Importance in Projection (VIP) is a summary,
per variable, of how much that variable contributes to explaining the quality block across
the components, scaled so that a value above one marks a variable of above-average
importance; the super VIP applies the same idea to a whole block. It puts the operating
conditions (1.07) and the trajectories (1.06) level and the chemistry last (0.86), the
order the earlier models gave one block at a time. That ordering is what the original
study set out to establish: the plant had been looking to the incoming chemistry for the
cause of poor product, and the models put the way the batch was operated ahead of it.

The original study builds its monitoring and prediction tools on this model. The
super-score plot places every batch in one space; the contributions of a batch in the
trajectory block, drawn with ``unfolded_contribution_plot``, name the tags and the phase;
and the predicted quality attributes are available as soon as a batch ends, before the
laboratory results. The block scores, which say whether a batch is unusual in its
chemistry, its operation or its trajectories, are read in the next section.

.. _APPS_batch_case_fmc_block_scores:

The block scores, and four batches whose trajectories look off-specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A multiblock model has a score plot for every block, not only the super-score plot. The
block scores of a batch say where it sits when only its chemistry, only its operating
conditions or only its trajectories are considered, and the three plots need not agree.

.. code-block:: python

	def nearer_group(block_scores):
	    """Place each batch with the group, good or abnormal, whose average point is nearer in this score plot."""
	    centres = {name: block_scores.loc[groups == name].mean() for name in ("good", "abnormal")}
	    return pd.DataFrame({name: ((block_scores - centre) ** 2).sum(axis=1) for name, centre in centres.items()}).idxmin(axis=1)

	placed = pd.DataFrame({name: nearer_group(block_scores) for name, block_scores in mb.block_scores_.items()})
	with_abnormal = [b for b in placed.index if groups[b] == "good" and placed.loc[b, "X"] == "abnormal"]
	print(with_abnormal, placed.loc[with_abnormal, ["Zchem", "Zop"]].eq("good").all(axis=1).to_dict())
	# [2, 3, 5, 6, 7] {2: True, 3: True, 5: False, 6: True, 7: True}
	anomalous = [2, 3, 6, 7]
	print(mb.super_scores_.iloc[:, 0].groupby(groups).mean().round(2).to_dict(), mb.super_scores_.loc[anomalous].iloc[:, 0].round(2).to_dict())
	# {'abnormal': -0.55, 'good': 0.36, 'high solvent': 0.19} {2: 0.31, 3: 0.14, 6: 0.17, 7: 0.18}
	fig = make_subplots(rows=1, cols=3, subplot_titles=[f"{name} block" for name in blocks])
	for col, (name, block_t) in enumerate(mb.block_scores_.items(), start=1):
	    group_scatter(fig, block_t.iloc[:, 0], block_t.iloc[:, 1], dict.fromkeys(anomalous, ORANGE), row=1, col=col, showlegend=col == 1)
	    block_axes(fig, np.diff([0.0, *mb.r2_x_per_block_cumulative_.loc[name]]), 1, col)
	fig.update_layout(height=420).show()

.. figure:: ../figures/batch/batch-case-fmc-block-scores.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three score plots side by side, one per block of the batch multiblock PLS, with the batches coloured by the plant's disposition; batches 2, 3, 6 and 7, classed good, sit among the batches classed abnormal in the trajectory block and among the good ones in the chemistry and operating-condition blocks.
	:width: 1100px
	:scale: 80
	:align: center

	Block scores of the batch multiblock PLS: the chemistry block (left), the operating-condition
	block (middle) and the trajectory block (right), coloured by the plant's disposition.
	Batches 2, 3, 6 and 7 (orange) were classed good; in the trajectory block they sit among
	the batches classed abnormal (purple), in the other two blocks among the good ones (blue).

In the trajectory block the batches classed abnormal lie at negative :math:`t_1` and the
good ones at positive :math:`t_1`, and four batches classed good lie among the abnormal
ones: 2, 3, 6 and 7. In both initial-condition blocks the same four lie among the good
batches, and in the quality PCA at the start of this case study they are inside the good
group. Their trajectories have the features of an off-specification batch, and their product
was on-specification.

To make that reading reproducible, each batch is placed, block by block, with the group
whose average point is nearer in that block's score plot. Five batches classed good are
placed with the abnormal batches by the trajectory block, and four of them with the good
batches by both initial-condition blocks. The fifth, batch 5, is placed with the abnormal
batches by the operating-condition block as well and is left aside. On the super score the
four lie between the two groups, and nothing marks them out; a batch that is unusual in one
block and ordinary in the others is visible only in the block score plots.

.. code-block:: python

	x_scores = mb.block_scores_["X"]
	abnormal = x_scores.loc[groups == "abnormal"]
	neighbours = sorted({int(b) for a in anomalous for b in ((abnormal - x_scores.loc[a]) ** 2).sum(axis=1).nsmallest(2).index})
	print(neighbours)                                          # the two nearest abnormal batches of each of the four
	# [42, 43, 44, 47, 50]
	contributions = mb.score_contributions(blocks, component=1)
	x_by_tag = contributions["X"].T.groupby(level="tag", sort=False).sum().T
	print(x_by_tag.loc[anomalous].mean().nsmallest(3).round(2).to_dict())     # the four batches' largest trajectory contributions
	# {'CTankLvl': -0.07, 'ClockTime': -0.03, 'J-Temp-SP': -0.02}
	print(x_by_tag.loc[neighbours].mean().nsmallest(3).round(2).to_dict())    # their neighbours'
	# {'ClockTime': -0.07, 'J-Temp-SP': -0.03, 'CTankLvl': -0.03}
	move = contributions["Zop"].loc[anomalous].mean() - contributions["Zop"].loc[neighbours].mean()
	print(move.round(2)[move.abs() >= 0.01].to_dict())         # Zop: from the neighbours' average to the four's average
	# {'Level1': -0.05, 'Temp1': 0.02, 'Time4': 0.05, 'Time2': 0.06, 'Time3': 0.11, 'TempSlope': 0.06, 'WgtCake': -0.05}
	fig = go.Figure(go.Bar(x=list(move.index), y=move, marker_color=BLUE))
	shade_alternate(fig, len(move))
	fig.update_layout(title="Operating conditions: from the neighbours' average to the four batches' average",
	                  yaxis_title="Contribution to the block t1", height=340).show()
	for tag in ("CTankLvl", "ClockTime", "D-Temp", "D-Temp-SP"):
	    overlay(X, tag, {**{b: AQUA for b in neighbours}, **{b: ORANGE for b in anomalous}}).show()
	keys = ["WgtCake", "Level1", "Temp1", "Temp2", "Time2", "Time3", "Time4"]
	print(Zop.loc[anomalous, keys].mean().round(0).astype(int).to_dict())          # the four batches
	# {'WgtCake': 7076, 'Level1': 75, 'Temp1': 40, 'Temp2': 86, 'Time2': 24, 'Time3': 50, 'Time4': 25}
	print(Zop.loc[neighbours, keys].mean().round(0).astype(int).to_dict())         # their neighbours
	# {'WgtCake': 6787, 'Level1': 66, 'Temp1': 33, 'Temp2': 85, 'Time2': 32, 'Time3': 38, 'Time4': 34}
	print(round(np.mean([X[b]["D-Temp-SP"].max() for b in anomalous]), 1), round(np.mean([X[b]["D-Temp-SP"].max() for b in neighbours]), 1))
	# 86.9 87.2

.. figure:: ../figures/batch/batch-case-fmc-anomalous.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the contribution from the neighbours' average to the four batches' average in the operating-condition block, positive for the length of the cool-down, the length and slope of the ramp and the high-speed agitation, negative for the collector level and the cake weight; right, four raw trajectories with the four batches in orange and their neighbours in aqua, running together in the collector level and the clock time, with the same peak set point.
	:width: 1100px
	:scale: 80
	:align: center

	Left: the contribution from the average point of the five neighbours to the average point
	of the four batches, in the operating-condition block. Right: four raw trajectories, with
	the four batches (orange) and their nearest abnormal neighbours (aqua) over the other
	batches (grey), with the ends of the first two phases marked. The two groups run together
	in the collector level and the clock time, and their peak temperature set points are the
	same.

What puts the four with the abnormal batches is what puts their neighbours there: the
collector tank level, the clock time and the jacket temperature set point carry the
largest contributions to the trajectory block score in both groups, and the overlays show
the two groups running together, with a heavy charge, a high collector level and a slow
first phase.

What separates the four from their neighbours lies in the operating-condition block. The
contribution from the neighbours' average point to the four's, the same construction as the
group-to-centre contribution of the :ref:`first case study <APPS_batch_case_dupont>`, is
carried by the length of the cooling phase (``Time3``), the length and the slope of the
temperature ramp (``Time2``, ``TempSlope``) and the length of the high-speed agitation
(``Time4``); the cake weight and the collector level pull the other way. In the recipe's own
units, the four ramped in 24 clock samples against 32 for their neighbours and cooled for 50
against 38, and their peak temperature set point was the same, 86.9 against 87.2. The
difference is not a set point that was moved but how long each phase was run.

Read together: the four batches began like an off-specification batch, with a heavy charge
and a slow first phase, were run differently through the second and third phases, and
yielded on-specification product. Whether the later phases were run that way to correct for
the first, the record does not say; the original study reports only that the peak
temperature set point was adjusted from batch to batch. Nor does the model say that a
shorter ramp and a longer cool-down would bring a slow batch on-specification. It describes
how the batches that were run co-varied, not cause and effect (Nomikos and MacGregor,
1995), so that reading is a hypothesis for a designed experiment, not a conclusion of the
model. The original study found four such batches as well, with the same reading of their
operating conditions.

Where to go next
~~~~~~~~~~~~~~~~

Wold and co-workers (2009) go one step further on this dryer and replace the raw
trajectories with blocks of features extracted from them, grouped by what they describe: a
timing block, a temperature block, an impeller block (power, torque and agitator speed) and
a pressure block, with the chemistry and the cake weight in a block of their own. A model
built on feature blocks can be read phase by phase, and its contributions name a feature
rather than a (tag, time) cell.

This is the landmark feature approach: pick a handful of quantities that summarise each
trajectory, such as the slope of the temperature over a phase or the duration of the phase
itself, and use those as the columns in place of the trajectory. The operating-condition
block of this case study is already such a block, since eight of its nine columns are
landmarks of the trajectories. It is the simplest of the
three approaches to set up, and it rests on the engineer's judgement about which landmarks
matter, so a feature that is important but not obvious can be left out. It suits a process
with distinct operational changes, which this dryer has, and less so one whose trajectories
are smooth, such as the polymerization reactor of the
:ref:`first case study <APPS_batch_case_dupont>`. Wold and co-workers (2009) build all
three kinds of model on this dryer, landmark and both unfoldings, and their score plots
separate the on-specification from the off-specification batches in the same way.

A second step is an on-line monitoring model, which tracks a running batch against the
reference model; that step is deferred here until the missing cells in the trajectories
have been dealt with, either by filling them in or by leaving the incomplete batches out of
the reference set. The :ref:`SBR case study <APPS_batch_case_sbr_online>` shows that step on
a dataset without missing cells, with the prediction of the final quality as the batch runs.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~

* Salvador Garcia-Munoz, Theodora Kourti, John F. MacGregor, Antonio G. Mateos and Gerry
  Murphy, "`Troubleshooting of an industrial batch process using multivariate methods
  <https://literature.learnche.org/item/24/troubleshooting-of-an-industrial-batch-process-using-multivariate-methods>`_", *Industrial and Engineering Chemistry Research*,
  **42**, 3592-3601, 2003. The source of the case study.

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process
  modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_",
  *Comprehensive Chemometrics*, **2.10**, 163-197, 2009.

* Salvador Garcia-Munoz, `Batch process improvement using latent variable methods <https://literature.learnche.org/item/3/batch-process-improvement-using-latent-variable-methods>`_,
  Ph.D thesis, McMaster University, 2004.

* Theodora Kourti, Paul Nomikos and John F. MacGregor, "`Analysis, monitoring and fault
  diagnosis of batch processes using multiblock and multiway PLS <https://literature.learnche.org/item/33/analysis-monitoring-and-fault-diagnosis-of-batch-processes-using-multiblock-and-multiway-pls>`_",
  *Journal of Process Control*, **5**, 277-284, 1995.

* Paul Nomikos and John F. MacGregor, "`Multivariate SPC charts for monitoring batch
  processes <https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_",
  *Technometrics*, **37**, 41-59, 1995. Its closing discussion sets out why a batch model
  describes correlation, not cause and effect.

* The full list of readings on batch data is on the
  :ref:`batch process monitoring <APPS_batch_monitoring>` page.
