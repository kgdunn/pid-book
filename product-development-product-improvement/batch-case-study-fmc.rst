.. _APPS_batch_case_fmc:

Combining initial conditions and trajectories: multiblock batch PLS on a batch dryer
=====================================================================================

.. index::
	single: batch data; batch dryer case study
	pair: multiblock PLS; batch data
	pair: initial conditions; batch data
	single: missing data; batch data

An agricultural chemical is dried in an industrial batch dryer. Wet cake, the solid product
with the solvent still in it, is charged, and the solvent is driven off into a side tank.
Chemical changes take place in the solid while it dries, so the drying step sets part of the
product quality, not only its residual solvent.

The recipe has three phases, each bounded by a landmark in the trajectories:

* solvent collection, from the start until the agitator is turned up to high speed;
* the temperature ramp, from there until the dryer temperature reaches its maximum;
* cooling, from there to the end of the batch.

The operators adjusted the peak temperature set point from batch to batch to correct the
product quality, a manual feedback loop. This is the case study of Garcia-Munoz and
co-workers (2003), and the most complete of the three. The
:ref:`first <APPS_batch_case_dupont>` had trajectories alone and the
:ref:`second <APPS_batch_case_sbr>` added final quality, while here the chemistry of the
charge and the operating conditions are recorded as well.

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
  conditions: the weight of the cake charged, known before the batch starts, and eight
  landmarks read off the batch's own trajectories when they were aligned, among them the
  peak dryer temperature, the length of each phase and the slope of the temperature ramp.
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
look like, and do the batches fall into groups? Do the initial conditions explain it? What
do the trajectories add? Which batches deserve a closer look? The original study answers
with a ladder of two-component models, and this page climbs the same ladder one block at a time:

* A PCA on the quality block.
* A PLS model from each initial-condition block to the quality block.
* A multiblock PLS on both initial-condition blocks.
* A batch PCA and a batch PLS on the trajectories.
* A batch multiblock PLS that joins all three blocks.

The data
~~~~~~~~

The `batch dryer dataset <https://openmv.net/info/batch-dryer>`_ holds the four blocks for
59 batches, numbered 2 to 71 with gaps. The numbering encodes the plant's classification,
good up to 33, abnormal to 61 and high in residual solvent beyond, which plays no part in
the models and appears on the score plots only as a colour and marker shape.

Batch durations vary widely, so the trajectories were aligned within each phase to 325
samples. The first two phases were aligned against a maturity variable, a quantity that rises
steadily through the phase, first the collector tank level and then the dryer temperature,
and the cooling phase linearly in time. The first phase ends at sample 175 and the ramp at
249.

``ClockTime``, the wall-clock time at each aligned sample, is the eleventh trajectory. It
records how much each batch was stretched or compressed, so a batch whose ramp took longer
than usual has a ``ClockTime`` rising faster over that phase. `batch_dtw <https://github.com/kgdunn/process-improve/blob/main/src/process_improve/batch/preprocessing.py>`_
aligns raw batch data by dynamic time warping, and ``load_dryer`` bundles this dryer's
unaligned trajectories, so the same batches can be drawn before and after.

Thirteen batches have no chemistry measurements and are left out, the same exclusion the
original study made;
``load_fmc`` lists them as ``missing_chemistry``, and 46 remain. A few quality and chemistry
cells and the trajectories of ten batches still have missing values.

The ``PCA``, ``PLS`` and `MBPLS <https://github.com/kgdunn/process-improve/blob/main/src/process_improve/multivariate/_mbpls.py>`_ estimators handle missing values through the
:ref:`NIPALS algorithm <LVM_PCA_NIPALS_algorithm>`, so this case study uses them on the
unfolded trajectories. ``BatchPCA`` and ``BatchPLS`` need complete data.

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.batch import dict_to_wide, load_dryer, load_fmc, unfolded_contribution_plot
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
	# 46 batches kept; missing cells: Y 19 Zchem 1 X in batches [20, 22, 27, 28, 31, 55, 60, 61, 67, 71]
	average = pd.concat(X.values()).groupby(level=0).mean()                  # the average trajectory of every tag
	agitator = average["Agitator"]
	phase_ends = (int((agitator > (agitator.min() + agitator.max()) / 2).idxmax()), int(average["D-Temp"].idxmax()))
	print(*phase_ends)                              # the first high-speed sample, and the sample of the peak dryer temperature
	# 175 249

	GREY, ORANGE, AQUA, BLUE = "#c8c8c8", "#c55a11", "#1baf7a", "#1f3d7a"                  # figure colours
	PURPLE, GOLD, BAND = "#6f42c1", "#d4a017", "#e9edf4"                                   # ... and the shading behind bars
	DARK_GREY = "#8c8c8c"                                                                  # the phase-separator lines
	PALE_GREY = "#dcdcdc"                                                                  # many batches drawn at once

.. code-block:: python

	raw = load_dryer()                              # the same dryer, before alignment
	shared = [batch_id for batch_id in raw if batch_id in fmc.X]
	duration = {batch_id: float(np.nanmax(batch["ClockTime"]) - np.nanmin(batch["ClockTime"]))
	            for batch_id, batch in raw.items() if batch_id in fmc.X}
	by_duration = sorted(duration, key=duration.get)
	shortest, middling, longest = by_duration[0], by_duration[len(by_duration) // 2], by_duration[-1]
	print(f"{len(shared)} batches, {min(duration.values()):.0f} to {max(duration.values()):.0f} time units",
	      f"(batch {shortest} and batch {longest}); every one is aligned to {len(fmc.X[shortest])} samples")
	# 59 batches, 93 to 200 time units (batch 9 and batch 34); every one is aligned to 325 samples

	panels = [("Before: dryer temperature against clock time", raw, "ClockTime", "DryerTemp"),
	          ("After: the same batches against aligned sample", fmc.X, None, "D-Temp"),
	          ("The warp itself: clock time at each aligned sample", fmc.X, None, "ClockTime")]
	fig = make_subplots(rows=1, cols=3, subplot_titles=[title for title, *_ in panels])
	for col, (_, source, x_tag, y_tag) in enumerate(panels, start=1):
	    for batch_id in shared:
	        batch = source[batch_id]
	        x = batch[x_tag] if x_tag else np.arange(len(batch))
	        colour, width = {shortest: (AQUA, 2), middling: (PURPLE, 2),
	                         longest: (ORANGE, 2)}.get(batch_id, (PALE_GREY, 0.7))
	        fig.add_trace(go.Scatter(x=x, y=batch[y_tag], mode="lines", showlegend=False,
	                                 line=dict(color=colour, width=width)), row=1, col=col)
	    if x_tag is None:
	        for end in phase_ends:
	            fig.add_vline(x=end, line_dash="dot", line_color=GREY, row=1, col=col)
	fig.update_layout(height=340).show()

.. figure:: ../figures/batch/batch-case-fmc-alignment.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three panels. Left, the dryer temperature of 59 batches against clock time: the traces end anywhere between 93 and 200 time units, with the shortest batch in aqua finishing while the longest, in orange, is still heating. Middle, the same batches against aligned sample: every trace now runs to 325 samples and the temperature ramps line up at the phase end. Right, the clock time at each aligned sample: the shortest batch rises almost as a straight line, the longest jumps steeply at the first phase end, and the rest lie between them.
	:width: 1200px
	:scale: 80
	:align: center

	What the alignment did. Left: the dryer temperature against clock time, as recorded. The
	batches end anywhere between 93 and 200 time units, so the same clock reading means a
	different stage of the recipe in each one; the shortest, a middling and the longest batch
	are drawn in colour. Middle: after alignment every batch runs to
	325 samples and the ramps line up, which is what lets one column of the unfolded matrix
	hold the same event for every batch. Right: the clock time at each aligned sample is the
	record of the stretching, and it is kept as a trajectory of the model.

.. code-block:: python

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
	first_phase = pd.concat([X[batch_id]["D-Temp"].iloc[:phase_ends[0]] for batch_id in keep if batch_id != 20])
	print(f"dryer temperature over the first phase: batch 20 {X[20]['D-Temp'].iloc[:phase_ends[0]].mean():.1f},"
	      f" the others {first_phase.mean():.1f}")
	# dryer temperature over the first phase: batch 20 33.8, the others 23.7

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

Batch 20, chosen for the overlay, is one to keep in mind. Its dryer temperature averaged
33.8 units over the solvent-collection phase against 23.7 for the other batches.

Product quality on its own
~~~~~~~~~~~~~~~~~~~~~~~~~~

Product quality is a multivariate property. A :ref:`PCA <SECTION_PCA>` on the eight quality
attributes shows how the batches group in quality space before any process data are
involved.

.. code-block:: python

	y_scaled = MCUVScaler().fit_transform(Y)              # missing cells pass through; PCA switches to NIPALS
	pca_y = PCA(n_components=2).fit(y_scaled)
	print("PCA on Y, R2 cumulative:", pca_y.r2_cumulative_.round(3).tolist())
	# PCA on Y, R2 cumulative: [0.5, 0.703]
	def group_scatter(fig, x, y, highlight, row=None, col=None, showlegend=True):
	    """One trace per class of the plant's classification (colour and marker shape from STYLES); the batches in
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

	def label_corner(points, here):
	    """The corner around `here` with the fewest close neighbours: where a label will not sit on a marker.

	    Distances are taken in units of each axis's own range, so the choice matches what the reader sees
	    rather than the units the scores happen to have."""
	    span = np.ptp(points, axis=0)
	    near = (points - here) / np.where(span > 0, span, 1)
	    near = near[(np.hypot(*near.T) < 0.10) & (np.hypot(*near.T) > 0)]   # close enough to collide with
	    corners = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
	    crowd = [np.sum((np.sign(near[:, 0]) == dx) & (np.sign(near[:, 1]) == dy)) for dx, dy in corners]
	    return corners[int(np.argmin(crowd))]

	def scores(model, r2, highlight, note="", labels=()):
	    """Score plot of a PCA or PLS model coded by classification, with the percent of the variance each
	    component explains (`r2`, per component, `note` saying of which block) on its axes, the 95% confidence
	    ellipse, and a name against each batch in `labels`, so the text's batches carry from figure to figure."""
	    t = model.scores_
	    fig = group_scatter(go.Figure(), t.iloc[:, 0], t.iloc[:, 1], highlight)
	    points, placed = t.iloc[:, :2].to_numpy(dtype=float), []
	    for batch_id in labels:
	        here = t.loc[batch_id].to_numpy(dtype=float)[:2]
	        dx, dy = label_corner(np.vstack([points, *placed]), here)
	        fig.add_annotation(x=here[0], y=here[1], text=str(batch_id), showarrow=False,
	                           xshift=13 * dx, yshift=11 * dy, font=dict(size=11))
	        placed.append(here + 0.03 * np.ptp(points, axis=0) * np.array([dx, dy]))  # so the next label avoids it
	    ex, ey = model.ellipse_coordinates(score_horiz=1, score_vert=2, conf_level=0.95)
	    fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", line=dict(color=GREY, dash="dash"), name="95% confidence ellipse"))
	    r2 = np.asarray(r2)
	    fig.update_layout(xaxis_title=f"t1 [{note}{r2[0]:.1%}]", yaxis_title=f"t2 [{note}{r2[1]:.1%}]", height=440)
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
	t1_y = pca_y.scores_.iloc[:, 0]
	print(f"negative t1: {int((t1_y[groups == 'abnormal'] < 0).sum())} of {int((groups == 'abnormal').sum())} abnormal;"
	      f" positive t1: {int((t1_y[groups == 'good'] > 0).sum())} of {int((groups == 'good').sum())} good;"
	      f" positive on both: {int((pca_y.scores_.loc[groups == 'high solvent'] > 0).all(axis=1).sum())} of"
	      f" {int((groups == 'high solvent').sum())} high solvent")
	# negative t1: 15 of 17 abnormal; positive t1: 21 of 23 good; positive on both: 6 of 6 high solvent
	contributions = pca_y.score_contributions(y_scaled, component=1)
	fig = go.Figure()
	for batch_id, colour in ((61, ORANGE), (14, AQUA)):
	    fig.add_trace(go.Bar(x=list(Y.columns), y=contributions.loc[batch_id], name=f"batch {batch_id}", marker_color=colour))
	shade_alternate(fig, len(Y.columns))
	fig.update_layout(title="Contributions to t1 of one batch from each group", yaxis_title="Contribution", height=320)
	fig.show()

.. figure:: ../figures/batch/batch-case-fmc-quality-pca.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the scores of the two-component PCA on the quality block, coded by the plant's classification with blue circles for good, purple triangles for abnormal and gold squares for high solvent, the abnormal batches mostly at negative t1 and batches 61 and 14 at opposite ends; right, their contributions to t1 for each quality attribute on alternately shaded positions, mirror images, with no bar for the missing Y2 of batch 61.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of the two-component PCA on the quality block, coded by the plant's
	classification (blue circles good, purple triangles abnormal, gold squares high solvent);
	batches 61 (orange) and 14 (aqua) are at opposite ends of :math:`t_1`. Right: their
	contributions to :math:`t_1`, attribute by attribute, are mirror images. ``Y2`` is
	missing for batch 61 and has no bar.

Two components explain 70.3% of the quality block, and the first separates the batches by
class. Of the 17 abnormal batches 15 have a negative :math:`t_1`, 21 of the 23 good ones a
positive :math:`t_1`, and the six high in residual solvent are positive on both components.

Batches 61 and 14, one from each of the first two groups, have mirror-image :math:`t_1`
contributions, with the same attributes (``Y1``, ``Y4``, ``Y6`` and ``Y10``) low in the
abnormal group and high in the good one. The first component is a general level of
quality rather than a trade-off between attributes.

Do the initial conditions explain quality?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A PLS model from each initial-condition block to the quality block answers this question
one block at a time.

.. code-block:: python

	zchem_scaled = MCUVScaler().fit_transform(Zchem)
	zop_scaled = MCUVScaler().fit_transform(Zop)
	pls_chem = PLS(n_components=2, scale=False).fit(zchem_scaled, y_scaled)
	pls_op = PLS(n_components=2, scale=False).fit(zop_scaled, y_scaled)
	for name, model in (("PCA on Y", pca_y), ("PLS Zchem", pls_chem), ("PLS Zop", pls_op)):
	    print(name, (model.r2_cumulative_ * 100).round(1).tolist())   # quality explained, cumulative
	# PCA on Y [50.0, 70.3]
	# PLS Zchem [16.3, 22.2]
	# PLS Zop [20.7, 26.2]
	for name, Z in (("PLS Zchem", Zchem), ("PLS Zop", Zop)):          # the same, on held-out batches
	    cv = PLS.select_n_components(Z, Y, max_components=2, cv=7, random_state=0)
	    print(name, (cv.r2y_validated["total"] * 100).round(1).tolist())
	# PLS Zchem [-5.0, -4.9]
	# PLS Zop [14.8, 11.1]
	fig = scores(pls_op, explained_x(pls_op), {20: ORANGE}, note="R2X ", labels=[20, 61, 14])
	contribution = pls_op.score_contributions(zop_scaled, component=1).loc[20]
	bars = go.Figure([go.Bar(x=contribution.index, y=contribution, marker_color=BLUE)])
	shade_alternate(bars, len(contribution))
	bars.update_layout(title="What puts batch 20 there", yaxis_title="Contribution to t1", height=440)
	fig.show()
	bars.show()

Each initial-condition block alone explains about a quarter of the quality block after two
components, the operating conditions more than the chemistry, the same order the original
study found.

.. table:: Quality explained, as a cumulative percentage, after one and after two components.
   :math:`R^2_Y` is the fit to the 46 batches; :math:`Q^2_Y` is the same quantity for batches
   held out of the fit, in seven folds, averaged over ten splits into folds.

   +----------------------+--------------------------+-----------------------------+-----------------------------+
   | Model                | Quality explained from   | Cumulative :math:`R^2_Y`    | Cumulative :math:`Q^2_Y`    |
   |                      |                          +--------------+--------------+--------------+--------------+
   |                      |                          | :math:`t_1`  | :math:`t_2`  | :math:`t_1`  | :math:`t_2`  |
   +======================+==========================+==============+==============+==============+==============+
   | PCA on quality       | the quality block itself | 50.0         | 70.3         | -            | -            |
   +----------------------+--------------------------+--------------+--------------+--------------+--------------+
   | PLS from Zchem       | the incoming chemistry   | 16.3         | 22.2         | -5.0         | -4.9         |
   +----------------------+--------------------------+--------------+--------------+--------------+--------------+
   | PLS from Zop         | the operating conditions | 20.7         | 26.2         | 14.8         | 11.1         |
   +----------------------+--------------------------+--------------+--------------+--------------+--------------+

The first row answers a different question from the other two, and the gap between them is
not a ranking. A PCA describes the quality block using that same block, so its number says
how strongly the eight attributes co-vary with each other. The two PLS models predict those
attributes from a separate block of process data, which is the harder task, and every later
rung of the ladder is measured the same way. The PCA has no held-out batches to predict,
since there is nothing to predict them from, so its :math:`Q^2_Y` cells are empty.

The :math:`Q^2_Y` columns separate the two blocks more sharply than the fit does. Held out
of the fit, the batches are predicted worse from their chemistry than by the average
batch, which is what a negative :math:`Q^2_Y` means, while the operating conditions keep
about half of their fitted value. A cross-validated number moves with the split into folds,
so it is read for its sign and its size, not its second decimal.

Batch 20 stands out in the operating-condition score plot, put there by the recipe timings
and the temperature slope. It is the batch whose temperature ramp took longer in the
trajectory overlay.

.. figure:: ../figures/batch/batch-case-fmc-pls-zop.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the scores of the PLS from the operating conditions to quality, coded by the plant's classification, with batch 20 as an orange circle at the lower left well outside the confidence ellipse and batches 61 and 14 labelled inside the cloud. Right, batch 20's contribution to the first component, variable by variable: the two recipe timings Time2 and Time4 and the temperature slope are large and negative, the others near zero.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of the PLS from the operating conditions to quality, coded by the plant's
	classification. Batch 20 (orange) lies well outside the confidence ellipse. Right: what
	puts it there, variable by variable. Two of the recipe timings and the temperature slope
	carry the batch's first-component score; the dryer temperature at the end of the first phase
	and the peak temperature contribute little.

Both blocks together: multiblock PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiblock PLS fits one set of components to several X blocks at once. Each block gets its
own block scores and block weights, and those block scores combine into a super score, one
number per batch per component, through super weights that say how much each block pulls.

The ``MBPLS`` class scales each block on its own and then divides it by the square root of
its number of columns, so no block dominates merely because it is wider. The super-score
plot shows the batches in the combined space, and the :math:`R^2` per block says how much
of each block the components describe.

.. code-block:: python

	blocks_z = {"Zchem": Zchem, "Zop": Zop}
	mb_z = MBPLS(n_components=2).fit(blocks_z, Y)
	print("MBPLS Z -> Y, R2Y cumulative:", mb_z.r2_y_cumulative_.round(3).tolist())
	# MBPLS Z -> Y, R2Y cumulative: [0.292, 0.364]
	print("R2X per block after two components:", mb_z.r2_x_per_block_cumulative_.iloc[:, -1].round(3).to_dict())
	# R2X per block after two components: {'Zchem': 0.296, 'Zop': 0.356}

	def block_axes(fig, r2, row=None, col=None, prefix="block t", note=""):
	    """Axis titles of one score plot, with the percent of the variance each component explains (`r2`)."""
	    r2 = np.asarray(r2)
	    fig.update_xaxes(title_text=f"{prefix}1 [{note}{r2[0]:.1%}]", row=row, col=col)
	    fig.update_yaxes(title_text=f"{prefix}2 [{note}{r2[1]:.1%}]", row=row, col=col)

	fig = make_subplots(rows=2, cols=3, subplot_titles=["Super scores", "Zchem block scores", "Zop block scores",
	                                                   "Super weights", "Zchem block weights", "Zop block weights"])
	super_t = mb_z.super_scores_
	group_scatter(fig, super_t.iloc[:, 0], super_t.iloc[:, 1], {20: ORANGE}, row=1, col=1)
	block_axes(fig, mb_z.r2_y_per_component_, 1, 1, prefix="super t", note="R2Y ")
	weights = mb_z.super_weights_                                            # one row per block, one column per component
	for a, colour in ((1, BLUE), (2, ORANGE)):
	    fig.add_trace(go.Bar(x=list(weights.index), y=weights.iloc[:, a - 1], name=f"component {a}", marker_color=colour), row=2, col=1)
	for col, (name, block_t) in enumerate(mb_z.block_scores_.items(), start=2):
	    group_scatter(fig, block_t.iloc[:, 0], block_t.iloc[:, 1], {20: ORANGE}, row=1, col=col, showlegend=False)
	    block_axes(fig, np.diff([0.0, *mb_z.r2_x_per_block_cumulative_.loc[name]]), 1, col, note="R2X ")
	    w = mb_z.block_weights_[name]                                         # one row per variable of the block
	    fig.add_trace(go.Scatter(x=w.iloc[:, 0], y=w.iloc[:, 1], mode="markers+text", text=list(w.index), textposition="top right",
	                             marker=dict(color=BLUE, size=16), showlegend=False), row=2, col=col)
	    fig.update_xaxes(title_text="block weight w1", row=2, col=col)      # weights carry no percent
	    fig.update_yaxes(title_text="block weight w2", row=2, col=col)
	fig.update_layout(height=820).show()

.. figure:: ../figures/batch/batch-case-fmc-mbpls-z.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Six panels in three columns: the super scores of the multiblock PLS on the two initial-condition blocks, coded by classification, with batch 20 at the lower left, above the super weights of the two components, larger for the operating-condition block on both; the chemistry block scores, where batch 20 sits inside the cloud of batches, above the chemistry block weights; and the operating-condition block scores, where batch 20 sits far outside, above the operating-condition block weights.
	:width: 1000px
	:scale: 80
	:align: center

	Left column: super scores of the multiblock PLS on the two initial-condition blocks,
	coded by the plant's classification, with batch 20 (orange) at the lower left, and below
	them the super weights of the two components. Middle and right columns: the chemistry
	block and the operating-condition block, each with its block scores above the block
	weights that define them. Batch 20 sits inside the cloud of batches in the chemistry
	block and far outside it in the operating-condition block.

Together the two blocks explain 36.4% of the quality block after two components, more than
either alone, and the super weights give the operating conditions the larger pull on both.
The block scores make the same point for a single batch. Batch 20 sits inside the cloud in
the chemistry block and far outside it in the operating-condition block. It is unusual in
its operation, not in its chemistry.

The trajectories alone
~~~~~~~~~~~~~~~~~~~~~~

``dict_to_wide`` unfolds the trajectories batchwise, one row per batch of 11 tags by 325
samples, 3575 columns, the layout ``BatchPCA`` uses internally. The eleventh tag is
``ClockTime``, so how fast each batch moved through each phase is part of what the models
see.

.. code-block:: python

	wide = dict_to_wide(X)                # the ten process tags and ClockTime: 11 x 325 = 3575 columns per batch
	x_scaled = MCUVScaler().fit_transform(wide)
	x_scaled.columns = wide.columns       # MCUVScaler returns flat labels; the batch plots need the (tag, sequence) index
	print(list(wide.shape), int(wide.isna().sum().sum()))       # batches x columns; missing cells
	# [46, 3575] 1340
	pca_x = PCA(n_components=2).fit(x_scaled)
	print(pca_x.r2_cumulative_.round(3).tolist())               # R2 of the trajectory block, cumulative
	# [0.231, 0.376]
	scores(pca_x, pca_x.r2_per_component_, {20: ORANGE}, labels=[20, 61, 14]).show()
	t2, spe = pca_x.hotellings_t2_.iloc[:, -1], pca_x.spe_.iloc[:, -1]
	t2_limit, spe_limit = pca_x.hotellings_t2_limit(conf_level=0.95), pca_x.spe_limit(conf_level=0.95)
	both = sorted(t2.index[(t2 > t2_limit) & (spe > spe_limit)])            # above both limits
	spe_only = sorted(spe.index[(spe > spe_limit) & (t2 <= t2_limit)])      # above the SPE limit only
	print(both, spe_only)
	# [20] [41, 51]

	def influence_plot(model, highlight, labels, conf_level=0.95):
	    """Hotelling's T2 against SPE, one marker per batch coded by classification, with both limits drawn."""
	    t2, spe = model.hotellings_t2_.iloc[:, -1], model.spe_.iloc[:, -1]
	    fig = group_scatter(go.Figure(), t2, spe, highlight)
	    fig.add_vline(x=model.hotellings_t2_limit(conf_level=conf_level), line_dash="dash", line_color=GREY)
	    fig.add_hline(y=model.spe_limit(conf_level=conf_level), line_dash="dash", line_color=GREY)
	    for batch_id in labels:
	        fig.add_annotation(x=t2.loc[batch_id], y=spe.loc[batch_id], text=str(batch_id),
	                           showarrow=False, xshift=13, yshift=9)
	    fig.update_layout(xaxis_title="Hotelling's T\u00b2", yaxis_title="SPE", height=420)
	    return fig

	influence_plot(pca_x, highlight={20: ORANGE}, labels=[41, 47, 51]).show()

.. figure:: ../figures/batch/batch-case-fmc-batch-pca.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Scores and the influence plot of the batch PCA on the trajectories, coded by the plant's classification; batch 20 is outside the confidence ellipse and is the only batch above both limits, while batches 41 and 51 are above the SPE limit only.
	:width: 1000px
	:scale: 80
	:align: center

	Scores (left) and Hotelling's :math:`T^2` against the SPE (right) of the batch PCA on the
	trajectories, coded by the plant's classification. Batch 20 (orange) is outside the 95%
	confidence ellipse and is the only batch above both limits; batches 41 and 51 are above
	the SPE limit only.

Two components describe 37.6% of the batch-to-batch variation in the trajectories. Batch 20
is the only batch above both limits, with a :math:`T^2` twice its limit and an SPE next to
the largest of the 46, so it is both unusual along the components and poorly described by
them. Batches 41 and 51 are above the SPE limit alone, and batch 47 just below it.

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
	axis) and the ends of the first two phases at samples 175 and 249 (grey). The collector
	tank level, and the clock time after the first 50 samples, hold one sign over the whole
	batch; the dryer pressure, the jacket temperature set point and the dryer temperature
	change sign within it.

A batch with a high :math:`t_1` collected more solvent than average at every point and took
more clock time to reach each one. Where a loading changes sign the component contrasts the
phases, as the dryer temperature does in going from negative over the first part of the batch
to positive from about sample 130 onwards.

The :math:`R^2` per cell says how much of that cell's batch-to-batch variation the two
components describe, and so where the loadings can be read with confidence. The collector
tank level and the clock time are described best, about 70% of their variance on average,
and the agitator speed least, under 10%. For most tags the :math:`R^2` falls in the cooling
phase, so the model says little about how the batches differ there.

A missing cell has no residual and no contribution. Batch 20 is one of the ten batches with
missing samples, and its scores come from the cells it does have, the same estimate the
NIPALS fit used, so its contributions are defined at every observed cell and absent only at
the missing ones. As in the :ref:`first case study <APPS_batch_case_dupont>`, the
vector has one entry per (tag, time) cell, here :math:`K = 11` tags by :math:`J = 325`
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
	:alt: Three panels for batch 20: the share of the SPE carried by each unfolded cell, blank over samples 95 to 109 in every tag but the collector tank level and over samples 34 to 44 in five of them, where the record has gaps, and largest in the dryer pressure through the first phase; the shares summed per tag, half of them in the dryer pressure; and the shares summed per sample with orange lines at the phase ends and the three phases named, most of the share in the solvent-collection phase.
	:width: 800px
	:scale: 80
	:align: center

	Top: the share of the SPE of batch 20 carried by each (tag, time) cell; the blank
	positions between samples 34 and 109 are the missing cells, which carry no residual.
	Middle: the same shares summed per tag. Bottom: summed per sample, with the three phases
	named between the orange phase ends. The dryer pressure carries half of the residual, and
	most of it lies in the solvent-collection phase.

The residual of batch 20 belongs to the dryer pressure (49%), most of it in the first phase
(58% of the total). Its dryer pressure sat at 85 units against 37 for the average batch
through solvent collection, where its dryer temperature also ran hot in the
:ref:`raw trajectory overlay <APPS_batch_case_fmc_overlay>`, and on through the ramp. The
temperatures, power
and torque share the rest.

Trajectories to quality
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	pls_x = PLS(n_components=2, scale=False).fit(x_scaled, y_scaled)
	print(pls_x.r2_cumulative_.round(3).tolist())               # R2 of the quality block, cumulative
	# [0.266, 0.41]
	print(explained_x(pls_x).round(3).tolist())                # R2 of the trajectory block, per component
	# [0.217, 0.131]
	scores(pls_x, explained_x(pls_x), {13: ORANGE, 5: AQUA, 7: AQUA}, note="R2X ", labels=[13, 5, 7, 61, 14]).show()
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
	level_end = pd.Series({batch_id: float(batch["CTankLvl"].iloc[-1]) for batch_id, batch in X.items()})
	clock_p1 = pd.Series({batch_id: float(batch["ClockTime"].iloc[174]) for batch_id, batch in X.items()})
	print("batch 13, counting from the lowest:", int((level_end <= level_end.loc[13]).sum()),
	      "of 46 on the collector level and", int((clock_p1 <= clock_p1.loc[13]).sum()), "on the clock time")
	# batch 13, counting from the lowest: 11 of 46 on the collector level and 4 on the clock time
	pls_x.predictions_vs_observed_plot(y_observed=y_scaled, variable="SolventConc").show()

.. figure:: ../figures/batch/batch-case-fmc-batch-pls.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Left, the scores of the batch PLS model from the trajectories to the quality block with batch 13 at the low end of t1 and batches 5 and 7 on the other side; right, the contributions of batch 13 to t1 summed per tag, all negative and led by the clock time and the collector tank level.
	:width: 1000px
	:scale: 80
	:align: center

	Left: scores of the batch PLS model from the trajectories to the quality block, coded by
	the plant's classification, with batch 13 (orange) and batches 5 and 7 (aqua) marked.
	Right: the contributions of batch 13 to :math:`t_1`, summed per tag; every tag contributes
	in the same direction and the clock time and the collector tank level lead.

The score plot axes carry the share of the trajectory block each component describes, its
:math:`R^2_X`. The model is judged on the quality block, where the trajectories explain
41.0% after two components, more than the 26.2% of the best single initial-condition block.

.. table:: Quality explained, as a cumulative percentage, with the trajectory block added to the
   earlier table. The batch PLS has no cross-validated value printed: on 46 batches the held-out
   estimate for a block of 3575 columns moves too much from one fold split to another to
   quote as a single number.

   +----------------------+--------------------------+-----------------------------+-----------------------------+
   | Model                | Quality explained from   | Cumulative :math:`R^2_Y`    | Cumulative :math:`Q^2_Y`    |
   |                      |                          +--------------+--------------+--------------+--------------+
   |                      |                          | :math:`t_1`  | :math:`t_2`  | :math:`t_1`  | :math:`t_2`  |
   +======================+==========================+==============+==============+==============+==============+
   | PCA on quality       | the quality block itself | 50.0         | 70.3         | -            | -            |
   +----------------------+--------------------------+--------------+--------------+--------------+--------------+
   | PLS from Zchem       | the incoming chemistry   | 16.3         | 22.2         | -5.0         | -4.9         |
   +----------------------+--------------------------+--------------+--------------+--------------+--------------+
   | PLS from Zop         | the operating conditions | 20.7         | 26.2         | 14.8         | 11.1         |
   +----------------------+--------------------------+--------------+--------------+--------------+--------------+
   | Batch PLS on X       | the trajectories         | 26.6         | 41.0         | -            | -            |
   +----------------------+--------------------------+--------------+--------------+--------------+--------------+

Batch 13 sits at the low end of :math:`t_1` with contributions all of one sign, led by the
clock time (-8.1) and the collector tank level (-8.0), then the dryer temperature (-4.7) and
the jacket temperature set point (-4.2). Batches 5 and 7 lie on the other side of
:math:`t_1` among the batches classed abnormal, although both were classed good.

.. _APPS_batch_case_fmc_overlay_13:

.. figure:: ../figures/batch/batch-case-fmc-raw-batches-13-5-7.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Four trajectories of the 46 batches in grey with batches 13 in orange, 5 in aqua and 7 in blue, with dashed vertical lines at the ends of the first two phases; batch 13 collected less solvent than almost every other batch, reached the end of the first phase in less clock time than most, and cooled faster at the end of the batch.
	:width: 900px
	:scale: 80
	:align: center

	Four trajectories of the 46 batches (grey) with batches 13 (orange), 5 (aqua) and 7
	(blue) drawn on top. Batch 13 collected less solvent than most of the batches and reached
	the end of the first phase in less clock time than all but three of them. The dashed lines
	mark the ends of the first two phases.

The :ref:`overlay of these three batches <APPS_batch_case_fmc_overlay_13>` shows what batch
13's contributions refer to: a collector level below most of the batches, and a first phase
that ended in less clock time than all but three of them.

Batch 13 was classed good, so a batch at the end of a component is not necessarily a bad
one. The component describes a direction of variation related to quality, and batch 13 sits well
out along it. The observed-against-predicted plot of the residual solvent concentration
shows how far the trajectories go towards predicting it, and is drawn again for the final
model in the next section.

All three blocks: batch multiblock PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final model joins the two initial-condition blocks and the unfolded trajectory block in
one multiblock PLS. The trajectory block enters as 3575 columns, so dividing each block by the
square root of its number of columns is what keeps it from drowning out the eleven chemistry
columns and the nine operating ones.

.. code-block:: python

	blocks = {"Zchem": Zchem, "Zop": Zop, "X": wide}
	mb = MBPLS(n_components=2).fit(blocks, Y)
	print(mb.r2_y_cumulative_.round(3).tolist())                # R2 of the quality block, cumulative
	# [0.369, 0.47]
	print(mb.r2_x_per_block_cumulative_.iloc[:, -1].round(3).to_dict())   # R2 of each block after two components
	# {'Zchem': 0.234, 'Zop': 0.304, 'X': 0.258}
	print(mb.super_vip_.round(2).to_dict())                     # super VIP per block
	# {'Zchem': 0.86, 'Zop': 1.07, 'X': 1.06}
	super_t = mb.super_scores_
	fig = group_scatter(go.Figure(), super_t.iloc[:, 0], super_t.iloc[:, 1], {13: ORANGE, 5: AQUA, 7: AQUA})
	block_axes(fig, mb.r2_y_per_component_, prefix="super t", note="R2Y ")
	fig.update_layout(height=440).show()
	mb.super_weights_bar_plot(component=1).show()
	unfolded_contribution_plot(mb.score_contributions(blocks, component=1)["X"], batch_id=13).show()
	mb.predictions_vs_observed_plot(Y, variable="SolventConc").show()
	solvent = Y["SolventConc"].dropna()
	residual = mb.predictions_["SolventConc"].loc[solvent.index] - solvent    # positive: fitted above observed
	high = solvent.index[groups.loc[solvent.index] == "high solvent"]
	print(f"{(residual.loc[high] < 0).sum()} of {len(high)} fitted low, by {-residual.loc[high].mean():.2f}"
	      f" on average, in an attribute spanning {solvent.max() - solvent.min():.2f}")
	# 6 of 6 fitted low, by 0.47 on average, in an attribute spanning 1.26

.. figure:: ../figures/batch/batch-case-fmc-batch-mbpls.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three panels: the super scores of the batch multiblock PLS with batches 13, 5 and 7 marked; the R2 of each block after two components beside the super VIP of each block; and the observed against fitted residual solvent concentration, coded by classification as the score plot is, with batches 13, 5 and 7 marked.
	:width: 1100px
	:scale: 80
	:align: center

	Left: super scores of the batch multiblock PLS, coded by the plant's classification, with
	batches 13 (orange), 5 and 7 (aqua) marked. Middle: :math:`R^2` of each block after two
	components (blue) and the super VIP of each block (orange). Right: observed and fitted
	residual solvent concentration, coded by classification and marked exactly as the left
	panel, so each batch can be followed from the score plot to its fit.

The combined model explains 47.0% of the quality block after two components, against 41.0%
for the trajectories alone and 36.4% for the two initial-condition blocks together. The
components describe 23.4% of the chemistry block, 30.4% of the operating-condition block
and 25.8% of the trajectory block.

Every one of the six batches classed high in residual solvent is fitted below the line, by
0.47 on average in an attribute spanning 1.26 across the batches. A model that describes
under half of the quality block pulls the extremes back towards the middle, so a group
sitting at the top of the range is fitted below it.

The Variable Importance in Projection (VIP) summarises, per variable, how much it
contributes to explaining the quality block, scaled so that a value above one marks
above-average importance. The super VIP applies the same idea to a whole block. It puts the
operating conditions (1.07) and the trajectories (1.06) level and the chemistry last (0.86),
the order the earlier models gave one block at a time.

That ordering is what the original study set out to establish: the plant had been looking to
the incoming chemistry for the cause of poor product, and the models put the way the batch
was operated ahead of it.

A model of this kind is what a plant builds its monitoring and prediction tools on. The super-score
plot places every batch in one space. A batch's contributions in the trajectory block, drawn
with ``unfolded_contribution_plot``, name the tags and the phase. The predicted quality
attributes are available as soon as a batch ends, before the laboratory results. The block
scores, which say whether a batch is unusual in its chemistry, its operation or its
trajectories, are read in the next section.

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
	    for label in ("good", "abnormal"):                       # a spoke from each batch to its group's average
	        members = [b for b in block_t.index if placed.loc[b, name] == label]
	        centre = block_t.loc[members].mean()
	        for b in members:
	            fig.add_trace(go.Scatter(x=[centre.iloc[0], block_t.iloc[:, 0].loc[b]],
	                                     y=[centre.iloc[1], block_t.iloc[:, 1].loc[b]], mode="lines",
	                                     line=dict(color=PALE_GREY, width=1), showlegend=False), row=1, col=col)
	        fig.add_trace(go.Scatter(x=[centre.iloc[0]], y=[centre.iloc[1]], mode="markers", showlegend=False,
	                                 marker=dict(color=GREY, symbol="cross", size=13,
	                                             line=dict(color="white", width=1.5))), row=1, col=col)
	    group_scatter(fig, block_t.iloc[:, 0], block_t.iloc[:, 1], dict.fromkeys(anomalous, ORANGE), row=1, col=col, showlegend=col == 1)
	    block_axes(fig, np.diff([0.0, *mb.r2_x_per_block_cumulative_.loc[name]]), 1, col, note="R2X ")
	fig.update_layout(height=420).show()

.. figure:: ../figures/batch/batch-case-fmc-block-scores.png
	:source: batch/batch-case-fmc-figures.py
	:alt: Three score plots side by side, one per block of the batch multiblock PLS, with the batches coloured by the plant's classification; batches 2, 3, 6 and 7, classed good, sit among the batches classed abnormal in the trajectory block and among the good ones in the chemistry and operating-condition blocks.
	:width: 1100px
	:scale: 80
	:align: center

	Block scores of the batch multiblock PLS: the chemistry block (left), the
	operating-condition block (middle) and the trajectory block (right), coded by the plant's
	classification.
	Batches 2, 3, 6 and 7 (orange) were classed good. Each batch is joined by a faint line to
	the average point of the group it is placed with, and a cross marks the two averages. In
	the trajectory block the four reach across to the abnormal group (purple); in the other
	two blocks they reach to the good one (blue).

In the trajectory block the abnormal batches lie at negative :math:`t_1` and the good ones
at positive, with five classed good among the abnormal. Four of those five, batches 2, 3, 6
and 7, sit with the good batches in both initial-condition blocks and in the quality PCA at
the start of this case study. Their trajectories have the features of an off-specification
batch, and their product was on-specification.

That a batch sits among a group is a claim about a picture. To make it reproducible, take
the average score point of the good batches and of the abnormal ones in each block, and
place every batch with whichever of the two centres is nearer. The figure joins each batch
to the centre it was placed with.

Five batches classed good are placed with the abnormal centre in the trajectory block. Four
of them are placed with the good centre in both initial-condition blocks: ordinary
chemistry, ordinary operating conditions, and trajectories that look abnormal. The fifth,
batch 5, is placed with the abnormal centre in the operating-condition block as well, so it
is not a case of an ordinary charge with an unusual trajectory, and it is left aside.

On the super score of this model those four lie between the two groups with nothing to mark them
out: a
batch unusual in one block and ordinary in the others is visible only in the block score
plots.

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

The four and their neighbours share one trajectory signature: the collector tank level, the
clock time and the jacket temperature set point carry the largest contributions in both
groups, and the overlays show a high collector level and a slow first phase.

What separates them lies in the operating-condition block. The contribution from the
neighbours' average point to the four's, the construction of the
:ref:`first case study <APPS_batch_case_dupont>`, is carried by the lengths of the cooling
phase (``Time3``), the ramp (``Time2``, ``TempSlope``) and the high-speed agitation
(``Time4``).

In the recipe's units the four ramped in 24 clock samples against 32 and cooled for 50
against 38, at the same peak set point (86.9 against 87.2): not a set point that was moved,
but how long each phase was run.

Read together:

* The four began like an off-specification batch, with a heavy charge and a slow first
  phase, were run differently through the later phases, and gave on-specification product.
* Whether the later phases were run that way to correct for the first, the record does not
  say.
* The model does not say that a shorter ramp and a longer cool-down would rescue a slow
  batch: it describes how the batches co-varied, not cause and effect (Nomikos and
  MacGregor, 1995). That reading is a hypothesis for a designed experiment.
* The original study found the same four batches, with the same reading.

The models side by side
~~~~~~~~~~~~~~~~~~~~~~~

Each rung of the ladder sees a different set of blocks, and what its two components describe
of each says what that model captured. The table below collects every model on this page
across the four blocks, the chemistry :math:`\mathbf{Z}_\text{chem}`, the operating
conditions :math:`\mathbf{Z}_\text{op}`, the trajectories :math:`\mathbf{X}` and the
quality :math:`\mathbf{Y}`, with a dash where the model never saw that block.

.. code-block:: python

	def block_r2(model):
	    """R2 per component of each X block of a multiblock model, from its cumulative R2 per block."""
	    return {name: np.diff([0.0, *row]) for name, row in model.r2_x_per_block_cumulative_.iterrows()}

	per_component = {                                             # R2 per component of every block a model saw
	    "PCA on quality": {"Y": pca_y.r2_per_component_},
	    "PLS from Zchem": {"Zchem": explained_x(pls_chem), "Y": pls_chem.r2_per_component_},
	    "PLS from Zop": {"Zop": explained_x(pls_op), "Y": pls_op.r2_per_component_},
	    "Multiblock PLS on Z": {**block_r2(mb_z), "Y": mb_z.r2_y_per_component_},
	    "Batch PCA on X": {"X": pca_x.r2_per_component_},
	    "Batch PLS on X": {"X": explained_x(pls_x), "Y": pls_x.r2_per_component_},
	    "Batch multiblock PLS": {**block_r2(mb), "Y": mb.r2_y_per_component_},
	}
	summary = pd.DataFrame({(block, f"t{a + 1}"): {name: np.asarray(r[block])[a] * 100 if block in r else np.nan
	                                               for name, r in per_component.items()}
	                        for block in ("Zchem", "Zop", "X", "Y") for a in (0, 1)})
	print(summary.round(1).to_string(na_rep="-"))
	print(summary["Y"].sum(axis=1, min_count=1).round(1).dropna().tolist())   # quality explained, per model
	# [70.3, 22.2, 26.2, 36.4, 41.0, 47.0]
	zchem = summary["Zchem"].round(1)
	print("Zchem: its own PLS", zchem.loc["PLS from Zchem"].sum().round(1),
	      "against the batch multiblock PLS", zchem.loc["Batch multiblock PLS"].tolist())
	# Zchem: its own PLS 52.0 against the batch multiblock PLS [6.5, 16.9]

.. table:: :math:`R^2` of each block, as a percentage, per component, for every model of the ladder.

   +----------------------+-------------+-------------+-------------+-------------+
   | Model                | Zchem       | Zop         | X           | Y           |
   |                      +------+------+------+------+------+------+------+------+
   |                      | t1   | t2   | t1   | t2   | t1   | t2   | t1   | t2   |
   +======================+======+======+======+======+======+======+======+======+
   | PCA on quality       | -    | -    | -    | -    | -    | -    | 50.0 | 20.3 |
   +----------------------+------+------+------+------+------+------+------+------+
   | PLS from Zchem       | 28.8 | 23.2 | -    | -    | -    | -    | 16.3 | 5.8  |
   +----------------------+------+------+------+------+------+------+------+------+
   | PLS from Zop         | -    | -    | 30.4 | 23.6 | -    | -    | 20.7 | 5.5  |
   +----------------------+------+------+------+------+------+------+------+------+
   | Multiblock PLS on Z  | 11.1 | 18.4 | 22.3 | 13.3 | -    | -    | 29.2 | 7.2  |
   +----------------------+------+------+------+------+------+------+------+------+
   | Batch PCA on X       | -    | -    | -    | -    | 23.1 | 14.6 | -    | -    |
   +----------------------+------+------+------+------+------+------+------+------+
   | Batch PLS on X       | -    | -    | -    | -    | 21.7 | 13.1 | 26.6 | 14.4 |
   +----------------------+------+------+------+------+------+------+------+------+
   | Batch multiblock PLS | 6.5  | 16.9 | 20.0 | 10.5 | 12.4 | 13.4 | 36.9 | 10.2 |
   +----------------------+------+------+------+------+------+------+------+------+

Read down the quality columns and the ladder pays off. Each rung adds to the one before it,
and the trajectories carry more of the quality block than either set of initial conditions.
Read across a row and the cost appears. The chemistry block, half described over the two
components of its own PLS, keeps under a quarter of itself over the two of the batch
multiblock PLS while the quality block gains, because a PLS component turns towards whatever
predicts :math:`\mathbf{Y}`, not towards describing its own block.

Where to go next
~~~~~~~~~~~~~~~~

Wold and co-workers (2009) go one step further on this dryer, replacing the raw trajectories
with thirteen landmark features, each read from one phase: the duration of each of the three
phases, the dryer temperature at the end of the first two, the average collector level,
differential pressure, dryer pressure, dryer temperature and its set point, and the slopes
of the power, the torque and the dryer temperature. Their contributions name a feature
rather than a (tag, time) cell.

This is the landmark feature approach: pick a handful of quantities that summarise each
trajectory, such as the slope of the temperature over a phase or its duration, and use
those as the columns. The operating-condition block here is already one, since eight of its
nine columns are landmarks of the trajectories.

Of the three ways of handling the trajectory array, landmark features, batchwise unfolding
and observation-wise unfolding, it is the simplest to set up, and the engineer chooses which
landmarks matter, so a feature that is important but not obvious can be left out. It suits a
process with distinct operational changes, which this dryer has, and less so one whose
trajectories are smooth, such as the reactor of the
:ref:`first case study <APPS_batch_case_dupont>`. Wold and co-workers (2009) build all three
kinds on this dryer, and their score plots separate the on- from the off-specification
batches in the same way.

A second step is an on-line monitoring model, which tracks a running batch against the
reference model and predicts its final quality before the batch ends. Estimating the scores
of a batch observed so far is a missing-data problem of the same shape as the gaps in these
trajectories, with the samples not yet seen standing in for the missing cells, so the
incomplete batches are no obstacle. The
:ref:`SBR case study <APPS_batch_case_sbr_online>` works that step through.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~

The full list of readings on batch data is on the
:ref:`batch process monitoring page <APPS_batch_readings>`; this page lists what it draws on.

* Salvador Garcia-Munoz, Theodora Kourti, John F. MacGregor, Antonio G. Mateos and Gerry
  Murphy, "`Troubleshooting of an industrial batch process using multivariate methods
  <https://literature.learnche.org/item/24/troubleshooting-of-an-industrial-batch-process-using-multivariate-methods>`_", *Industrial and Engineering Chemistry Research*,
  **42**, 3592-3601, 2003. The source of the case study.

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process
  modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_",
  *Comprehensive Chemometrics*, **2**, chapter 2.10, 163-197, 2009. Builds feature-block,
  landmark and
  unfolded-trajectory models on this same dryer.

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
