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
has three phases: the solvent is collected, the temperature is ramped, and the batch is
cooled down. Operators can adjust some settings of the recipe. This is the case study of
Garcia-Munoz and co-workers (2003), and it is the most complete of the three batch case
studies, because every kind of information about a batch is present.

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
* :math:`\mathbf{Z}_\text{op}`, the operating conditions of the batch: a level, two
  temperatures, four recipe timings, a temperature slope and the weight of the cake, nine
  values in all.
* :math:`\mathbf{X}`, the ten trajectories over the batch, and an eleventh described below.
* :math:`\mathbf{Y}`, eight final quality attributes: seven numbered attributes, ``Y1`` to
  ``Y11`` with gaps, and the residual solvent concentration ``SolventConc``.

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
the same ladder: a PCA on the quality block, a PLS model from each initial-condition block,
a multiblock PLS on both, a batch PCA and a batch PLS on the trajectories, and finally a
batch multiblock PLS that joins all three blocks.

The data
~~~~~~~~

The `batch dryer dataset <https://openmv.net/info/batch-dryer>`_ is a workbook with the four
blocks over 59 batches, one sheet each. The batch identifiers run from 2 to 71 with gaps,
and they carry the plant's disposition: batches numbered 1 to 33 were classed as good, 34 to
61 as abnormal, and 62 to 71 as high in residual solvent. The identifiers are not used to
build any model. As in the first case study, they are kept aside and compared with what the
models find.

The trajectories were aligned within each of the three phases before the data were
archived, to 325 samples per batch. ``ClockTime``, the wall-clock time at each aligned
sample, is carried along as an eleventh trajectory. After alignment it is no longer a clock
but a record of how much each batch was stretched or compressed to fit the template, and
that is information about the batch in its own right: a batch whose temperature ramp took
longer than usual has a ``ClockTime`` that rises faster over that phase. Alignment of raw,
unaligned batch data is a topic of its own; the ``batch_dtw`` function in ``process_improve``
implements dynamic time warping for it, and the unaligned trajectories of this same dryer
are bundled with the package as ``load_dryer``.

Thirteen batches have no chemistry measurements at all. The original study excluded them,
and ``load_fmc`` returns their identifiers as ``missing_chemistry`` so that the exclusion
can be reproduced. The remaining 46 batches still contain genuine missing values: 19 cells
in the quality block, one in the chemistry block, and 1220 cells in the trajectories of ten
batches, where a measurement is absent for a stretch of the batch. The ``PCA``, ``PLS`` and
``MBPLS`` estimators of the ``multivariate`` module handle missing values through the
:ref:`NIPALS algorithm <LVM_PCA_NIPALS_algorithm>`, which is why this case study uses them
directly, after unfolding the trajectories with ``dict_to_wide``, instead of the
``BatchPCA`` and ``BatchPLS`` classes of the two earlier case studies, which require
complete data.

.. code-block:: python

	import pandas as pd
	import plotly.graph_objects as go
	from process_improve.batch import dict_to_wide, load_fmc, time_varying_loading_plot, unfolded_contribution_plot
	from process_improve.multivariate import PCA, PLS, MCUVScaler
	from process_improve.multivariate.methods import MBPLS

	fmc = load_fmc()                                # https://openmv.net/file/batch-dryer.xlsx
	keep = [batch_id for batch_id in fmc.batch_ids if batch_id not in fmc.missing_chemistry]
	X = {batch_id: fmc.X[batch_id] for batch_id in keep}
	Y, Zop, Zchem = fmc.Y.loc[keep], fmc.Zop.loc[keep], fmc.Zchem.loc[keep]
	incomplete = [batch_id for batch_id, batch in X.items() if batch.isna().any().any()]
	print(len(X), "batches kept; missing cells: Y", int(Y.isna().sum().sum()), "Zchem", int(Zchem.isna().sum().sum()),
	      "X in batches", incomplete)

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

	for tag in ("D-Temp", "J-Temp", "CTankLvl", "ClockTime"):
	    overlay(X, tag, {20: ORANGE}).show()

.. figure:: ../figures/batch/batch-case-fmc-raw-trajectories.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Four trajectories of the 46 batches in grey with batch 20 in orange; the dryer temperature of batch 20 sits well above the others through the first 170 samples, and its ClockTime rises steeply between samples 200 and 240.
	:width: 900px
	:scale: 80
	:align: center

	Four trajectories of the 46 batches (grey) with batch 20 (orange) drawn on top. The
	dryer temperature of batch 20 sat well above the other batches through the whole
	solvent-collection phase, and its ``ClockTime`` rises steeply between samples 200 and
	240, where its temperature ramp took longer than usual. The gaps in the orange line are
	missing samples.

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
	pca_y.score_plot(settings={"show_labels": True}).show()
	disposition = pd.cut(pca_y.scores_.index, bins=[0, 33, 61, 71], labels=["good", "abnormal", "high solvent"])
	print(pca_y.scores_.groupby(disposition, observed=True).agg(["mean", "min", "max", "count"]).round(2))
	contributions = pca_y.score_contributions(y_scaled, component=1)
	fig = go.Figure()
	for batch_id, colour in ((61, ORANGE), (14, AQUA)):
	    fig.add_trace(go.Bar(x=list(Y.columns), y=contributions.loc[batch_id], name=f"batch {batch_id}", marker_color=colour))
	fig.update_layout(title="Contributions to t1 of one batch from each group", yaxis_title="Contribution", height=320)
	fig.show()

.. figure:: ../figures/batch/batch-case-fmc-quality-pca.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the scores of the two-component PCA on the quality block with batches 61 and 14 at opposite ends of t1; right, their contributions to t1 for each quality attribute, which are mirror images, with no bar for the missing Y2 of batch 61.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of the two-component PCA on the quality block; batches 61 (orange) and 14
	(aqua) are at opposite ends of :math:`t_1`. Right: their contributions to :math:`t_1`,
	attribute by attribute, are mirror images. ``Y2`` is missing for batch 61 and has no
	bar.

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
	pls_op.score_plot(settings={"show_labels": True}).show()
	print("batch 20 on Zop, t1 contributions:", pls_op.score_contributions(zop_scaled, component=1).loc[20].round(2).to_dict())

Each initial-condition block on its own explains about a quarter of the quality block:
22.2% for the chemistry after two components, and 26.2% for the operating conditions. Batch
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
	mb_z.super_score_plot().show()
	mb_z.super_weights_bar_plot(component=1).show()
	for name, block_contributions in mb_z.score_contributions(blocks_z, component=1).items():
	    print(f"batch 20, block {name}:", block_contributions.loc[20].round(2).to_dict())

.. figure:: ../figures/batch/batch-case-fmc-mbpls-z.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the super scores of the multiblock PLS on the two initial-condition blocks with batch 20 at the lower left; right, the super weights of the two components, larger for the operating-condition block on both.
	:width: 1000px
	:scale: 80
	:align: center

	Left: super scores of the multiblock PLS on the two initial-condition blocks; batch 20
	(orange) is at the lower left. Right: the super weights of the two components; the
	operating-condition block pulls more strongly on both.

Together the two blocks explain 36.4% of the quality block after two components, more than
either alone, and the components describe 29.6% of the chemistry block and 35.6% of the
operating-condition block. The super weights give the operating-condition block the larger
pull on both components. The per-block contributions of batch 20 make the same point for a
single batch: its contributions from the operating-condition block (-0.38 for ``Time2``,
-0.32 for the temperature slope and -0.25 for ``Time4``) are several times larger than any
from the chemistry block, whose largest is -0.08. Batch 20 is unusual in its operation, not
in its chemistry.

The trajectories alone
~~~~~~~~~~~~~~~~~~~~~~

The trajectories are unfolded batchwise with ``dict_to_wide``: one row per batch of 10 tags
times 325 samples, 3250 columns, the layout the ``BatchPCA`` class uses internally. The
original course notes include ``ClockTime`` as an eleventh trajectory. On this page it is
left out of the trajectory block, so that the block holds the ten process measurements
only; the timing information enters the later multiblock model through the recipe timings
of :math:`\mathbf{Z}_\text{op}`. Including it is a change of one line. ``MCUVScaler``
returns flat column labels, so the two-level (tag, sequence) column index is re-attached
after scaling; the batch plots read it.

.. code-block:: python

	wide = dict_to_wide({batch_id: batch.drop(columns="ClockTime") for batch_id, batch in X.items()})
	x_scaled = MCUVScaler().fit_transform(wide)
	x_scaled.columns = wide.columns       # MCUVScaler returns flat labels; the batch plots need the (tag, sequence) index
	print("unfolded trajectories:", wide.shape, "with", int(wide.isna().sum().sum()), "missing cells")
	pca_x = PCA(n_components=2).fit(x_scaled)
	print("batch PCA on X, R2 cumulative:", pca_x.r2_cumulative_.round(3).tolist())
	pca_x.score_plot(settings={"show_labels": True}).show()
	pca_x.spe_plot(settings={"show_labels": True}).show()
	print("largest SPE:", pca_x.spe_.iloc[:, -1].nlargest(4).round(1).to_dict(), "95% limit:", round(float(pca_x.spe_limit(conf_level=0.95)), 1))
	time_varying_loading_plot(pca_x, component=1).show()
	squared = pca_x.spe_contributions(x_scaled) ** 2           # a row of missing values for a batch with missing cells
	spe_share = squared.div(squared.sum(axis=1), axis=0) * 100
	complete = spe_share.dropna(how="all").index
	worst = pca_x.spe_.loc[complete].iloc[:, -1].idxmax()
	print("largest SPE among the complete batches: batch", worst)
	unfolded_contribution_plot(spe_share, batch_id=worst, by_tag=True).show()
	by_time = spe_share.loc[worst].groupby(level="sequence").sum()
	print(f"batch {worst}: share of the SPE in the first 50 samples = {by_time.loc[:49].sum():.0f}%")

.. figure:: ../figures/batch/batch-case-fmc-batch-pca.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Scores and SPE of the batch PCA on the trajectories; batch 20 is outside the confidence ellipse and has the largest SPE, and batch 51 is inside the ellipse but above the SPE limit, as is batch 41.
	:width: 1000px
	:scale: 80
	:align: center

	Scores (left) and SPE (right) of the batch PCA on the trajectories. Batch 20 (orange) is
	outside the 95% confidence ellipse and has the largest SPE. Batch 51 (aqua), the
	complete batch with the largest SPE, is inside the ellipse but above the SPE limit, as
	is batch 41.

Two components describe 34.9% of the batch-to-batch variation in the trajectories. Batch 20
is outside the 95% confidence ellipse in the score plot and has the largest SPE, 77.5
against a limit of 67.5. Batches 51 and 41 are above the limit as well, at 73.0 and 72.9,
and batch 47 is just below it.

.. figure:: ../figures/batch/batch-case-fmc-loadings-p1.png
	:source: batch/batch-case-fmc-figures.py
	:alt: The first loading of the batch PCA over the batch, one panel per tag; the loading is positive and nearly constant for the collector tank level, negative through the first phase for the dryer pressure and the jacket temperature set point, and changes sign within the batch for the dryer temperature.
	:width: 1000px
	:scale: 80
	:align: center

	Loading :math:`\mathbf{p}_1` of the batch PCA over the batch, one panel per tag. The
	loading is positive and nearly constant for the collector tank level, so :math:`t_1`
	is largely a measure of how much solvent a batch collected. The dryer pressure, the
	jacket temperature set point and the dryer temperature have loadings of both signs
	within the batch.

The loading of the first component is positive and nearly constant for the collector tank
level over the whole batch: a batch with a high :math:`t_1` collected more solvent than
average at every point of the batch. The other tags have loadings that change sign within
the batch, with the dryer pressure negative through the solvent-collection phase and the
dryer temperature negative in the first phase and positive in the ramp and cooling phases.

Contribution plots are only defined for batches with complete trajectories. A missing cell
has no residual and no contribution, and ``process_improve`` returns a row of missing values
for such a batch. Batch 20 is one of the ten batches with missing samples, so it is examined
through its raw overlays: it ran hot in the first phase and took longer in the second. Batch
51 is the complete batch with the largest SPE, and its SPE contributions can be drawn.

.. figure:: ../figures/batch/batch-case-fmc-batch-51-spe-contributions.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three panels for batch 51: the share of the SPE carried by each unfolded cell, largest in the dryer temperature set point, the jacket temperature and its set point; the shares summed per tag; and the shares summed per sample, concentrated in the first 50 samples of the batch.
	:width: 800px
	:scale: 80
	:align: center

	Share of the SPE of batch 51 carried by each (tag, time) cell (top), summed per tag
	(middle) and summed per sample (bottom). The dryer temperature set point, the jacket
	temperature and its set point carry about two thirds of the residual, half of which lies
	in the first 50 samples of the batch.

The residual of batch 51 belongs to the dryer temperature set point (27%), the jacket
temperature (24%) and the jacket temperature set point (18%), and half of it lies in the
first 50 samples of the batch. The set points of batch 51 were handled differently from the
other batches at the start of the solvent-collection phase, and the jacket temperature
followed them.

Trajectories to quality
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	pls_x = PLS(n_components=2, scale=False).fit(x_scaled, y_scaled)
	print("batch PLS X -> Y, R2Y cumulative:", pls_x.r2_cumulative_.round(3).tolist())
	pls_x.score_plot(settings={"show_labels": True}).show()
	t1 = pls_x.score_contributions(x_scaled, component=1)
	unfolded_contribution_plot(t1, batch_id=13).show()
	print("batch 13, t1 contributions per tag:", t1.loc[13].groupby(level="tag", sort=False).sum().round(1).to_dict())
	for tag in ("D-Temp", "CTankLvl", "Power", "J-Temp-SP"):
	    overlay(X, tag, {13: ORANGE, 5: AQUA, 7: BLUE}).show()
	print("collector tank level at the end of the batch:", {batch_id: round(float(X[batch_id]["CTankLvl"].iloc[-1])) for batch_id in (13, 5, 7)})
	pls_x.predictions_vs_observed_plot(y_observed=y_scaled, variable="SolventConc").show()

.. figure:: ../figures/batch/batch-case-fmc-batch-pls.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the scores of the batch PLS model from the trajectories to the quality block with batch 13 at the low end of t1 and batches 5 and 7 near each other; right, the contributions of batch 13 to t1 summed per tag, all negative and led by the collector tank level.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of the batch PLS model from the trajectories to the quality block, with
	batch 13 (orange) and batches 5 and 7 (aqua) marked. Right: the contributions of batch
	13 to :math:`t_1`, summed per tag; every tag contributes in the same direction and the
	collector tank level leads.

The trajectories explain 39.2% of the quality block after two components, more than the
initial conditions did (26.2% at best for a single block). Batch 13 is at the low end of
:math:`t_1`, and its contributions are all of the same sign, with the collector tank level
(-9.0), the dryer temperature (-5.3) and the jacket temperature set point (-4.8) leading.
Batches 5 and 7 are near each other in the score plot, at a moderate :math:`t_1` and a
negative :math:`t_2`, and are drawn in the same overlay.

.. figure:: ../figures/batch/batch-case-fmc-raw-batches-13-5-7.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Four trajectories of the 46 batches in grey with batches 13 in orange, 5 in aqua and 7 in blue; batch 13 collected less solvent than almost every other batch, drew less agitator power through the first phase and cooled faster at the end of the batch.
	:width: 900px
	:scale: 80
	:align: center

	Four trajectories of the 46 batches (grey) with batches 13 (orange), 5 (aqua) and 7
	(blue) drawn on top. Batch 13 collected less solvent than almost every other batch,
	drew less agitator power through the first phase and cooled faster at the end of the
	batch.

The overlay shows what the contributions of batch 13 refer to. Its collector tank level
levelled off at 52 units, against 77 units for batch 7, 87 units for batch 5 and up to 117
units for the batches that collected the most; its agitator power ran below the other
batches through the solvent-collection phase, 118 units on average against 135; and its
dryer temperature fell faster than any other batch in the cooling phase. Batch 13 was
classed as a good batch, so a batch at the end of a component is not necessarily a bad one.
The component describes a direction of variation in the trajectories that is related to
quality, and batch 13 is the batch furthest along it. The observed-against-predicted plot
of the residual solvent concentration, one of the attributes on which the batches are
dispositioned, shows how far the trajectories go towards predicting it; the same plot is
drawn again for the final model, in the next section.

All three blocks: batch multiblock PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final model joins the two initial-condition blocks and the unfolded trajectory block in
one multiblock PLS model. The trajectory block enters as 3250 columns; dividing each block
by the square root of its number of columns keeps it from drowning out the eleven chemistry
columns and the nine operating columns.

.. code-block:: python

	blocks = {"Zchem": Zchem, "Zop": Zop, "X": wide}
	mb = MBPLS(n_components=2).fit(blocks, Y)
	print("batch MBPLS, R2Y cumulative:", mb.r2_y_cumulative_.round(3).tolist())
	print("R2X per block after two components:", mb.r2_x_per_block_cumulative_.iloc[:, -1].round(3).to_dict())
	print("super VIP per block:", mb.super_vip_.round(2).to_dict())
	mb.super_score_plot().show()
	mb.super_weights_bar_plot(component=1).show()
	unfolded_contribution_plot(mb.score_contributions(blocks, component=1)["X"], batch_id=13).show()
	mb.predictions_vs_observed_plot(Y, variable="SolventConc").show()

.. figure:: ../figures/batch/batch-case-fmc-batch-mbpls.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three panels: the super scores of the batch multiblock PLS with batches 13, 5 and 7 marked; the R2 of each block after two components beside the super VIP of each block; and the observed against fitted residual solvent concentration with batch 13 marked.
	:width: 1100px
	:scale: 80
	:align: center

	Left: super scores of the batch multiblock PLS, with batches 13 (orange), 5 and 7 (aqua)
	marked. Middle: :math:`R^2` of each block after two components (blue) and the super VIP
	of each block (orange). Right: observed and fitted residual solvent concentration, with
	batch 13 marked.

The combined model explains 46.8% of the quality block after two components, against 39.2%
for the trajectories alone and 36.4% for the two initial-condition blocks together. The
components describe 24.3% of the chemistry block, 30.8% of the operating-condition block
and 21.7% of the trajectory block. The Variable Importance in Projection (VIP) is a summary,
per variable, of how much that variable contributes to explaining the quality block across
the components, scaled so that a value above one marks a variable of above-average
importance; the super VIP applies the same idea to a whole block. It ranks the operating
conditions first (1.10), the trajectories second (1.00) and the chemistry last (0.88), the
same order the earlier models gave one block at a time.

The original study builds its monitoring and prediction tools on this model. The
super-score plot places every batch in one space; the block scores say whether a batch is
unusual in its chemistry, its operation or its trajectories; the contributions of a batch
in the trajectory block, drawn with ``unfolded_contribution_plot``, name the tags and the
phase; and the predicted quality attributes are available as soon as a batch ends, before
the laboratory results.

Where to go next
~~~~~~~~~~~~~~~~

The course material this page is based on goes one step further and replaces the raw
trajectories with blocks of features extracted from them, grouped by what they describe: a
timing block, a temperature block, an impeller block (power, torque and agitator speed) and
a pressure block, with the chemistry and the cake weight in a block of their own. A model
built on feature blocks can be read phase by phase, and its contributions name a feature
rather than a (tag, time) cell. A second step is an on-line monitoring model, which tracks a
running batch against the reference model; that step is deferred here until the missing
cells in the trajectories have been dealt with, either by filling them in or by leaving the
incomplete batches out of the reference set.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~

* Salvador Garcia-Munoz, Theodora Kourti, John F. MacGregor, Antonio G. Mateos and Gerry
  Murphy, "`Troubleshooting of an industrial batch process using multivariate methods
  <https://doi.org/10.1021/ie0300023>`_", *Industrial and Engineering Chemistry Research*,
  **42**, 3592-3601, 2003. The source of the case study.

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process
  modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_",
  *Comprehensive Chemometrics*, **2.10**, 163-197, 2009.

* Salvador Garcia-Munoz, `Batch process improvement using latent variable methods <https://literature.learnche.org/item/3/batch-process-improvement-using-latent-variable-methods>`_,
  Ph.D thesis, McMaster University, 2004.

* Theodora Kourti, Paul Nomikos and John F. MacGregor, "`Analysis, monitoring and fault
  diagnosis of batch processes using multiblock and multiway PLS <https://literature.learnche.org/item/33/analysis-monitoring-and-fault-diagnosis-of-batch-processes-using-multiblock-and-multiway-pls>`_",
  *Journal of Process Control*, **5**, 277-284, 1995.

* The full list of readings on batch data is on the
  :ref:`batch process monitoring <APPS_batch_monitoring>` page.
