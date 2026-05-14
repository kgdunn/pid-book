.. _APPS_multivariate_monitoring:

Multivariate process monitoring case studies
=============================================

.. index::
	single: multivariate process monitoring (MSPC)
	pair: multivariate process monitoring; applications

Chapter 3 introduced the toolkit of univariate process monitoring -- the
:ref:`Shewhart chart <monitoring_shewhart_chart>`,
:ref:`CUSUM <monitoring_CUSUM_charts>` and :ref:`EWMA <monitoring_EWMA>` -- and
applied them one variable at a time. That works when the upset shows up as a
movement in a single tag, but real industrial faults usually distort several
variables at once, in directions that respect the correlation structure of the
process. A chart that watches each tag on its own does not see the joint
shift; it can either miss the fault entirely or, more often, raise the alarm
only after the disturbance has grown large enough to be visible in one
variable. This section is a worked example of that, on the same mineral
flotation cell mentioned in :ref:`an earlier chapter <SECTION-process-monitoring>`
as one of the canonical processes for monitoring: we build a Shewhart chart on
a single variable, then a multivariate-statistical-process-control (MSPC)
chart on all five variables, and compare what each one detects.

.. _APPS_multivariate_monitoring_flotation:

The flotation cell
~~~~~~~~~~~~~~~~~~

`Flotation <https://openmv.net/info/flotation-cell>`_ is the workhorse
separation step in mineral processing. Crushed ore is mixed with water and a
collector reagent into a slurry, fed into an agitated tank, and aerated from
below. Hydrophobic particles (the valuable mineral) attach to the rising
bubbles and concentrate in the froth at the surface; hydrophilic particles
(the gangue) sink and leave through the tailings stream. The product is the
froth that overflows. Five process tags are recorded every 30 seconds:

* ``Feed rate`` -- slurry feed into the cell (tonnes per hour),
* ``Upstream pH`` -- pH of the upstream conditioner where collector dosing
  happens,
* ``CuSO4 added`` -- copper sulphate dose, an activator used to make the
  target mineral more responsive to the collector,
* ``Pulp level`` -- froth-pulp interface depth inside the cell,
* ``Air flow rate`` -- aeration rate into the bottom of the cell.

The dataset is a 30-second sampling of those five tags over two consecutive
days. The first day (15 December 2004) is used as the phase 1 stretch, on
which we will build both the univariate chart limits and the multivariate
model. The second day onwards is the phase 2 stretch, against which both
charts are evaluated.

Loading the data and setting up the phase split:

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.multivariate import PCA, MCUVScaler

	flot = pd.read_csv("https://openmv.net/file/flotation-cell.csv")
	num = flot.drop(columns=["Date and time"])

	N_phase1 = 479
	phase1 = num.iloc[:N_phase1]
	phase2 = num.iloc[N_phase1:]
	print(f"phase1 shape: {phase1.shape}  phase2 shape: {phase2.shape}")

This gives 479 phase-1 observations on 15 December and 2442 phase-2
observations from 16 December onwards.

.. _APPS_multivariate_monitoring_univariate:

Univariate Shewhart chart on the feed rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following the same recipe as in :ref:`the Shewhart chapter <monitoring_shewhart_chart>`,
we reduce the raw 30-second feed-rate measurements into 2-minute subgroups
(size :math:`n = 4`), compute the subgroup means and standard deviations on
phase 1, and turn them into target / lower / upper limits. We then apply
those same limits to phase-2 subgroups:

.. code-block:: python

	from math import gamma, sqrt

	def subgroup(x, n_sub):
	    """Reshape a 1-D time series into (n_groups, n_sub) without the trailing partial subgroup."""
	    n_groups = len(x) // n_sub
	    return np.asarray(x[: n_groups * n_sub]).reshape((n_groups, n_sub))

	n_sub = 4
	sub_p1 = subgroup(phase1["Feed rate"].values, n_sub)
	sub_p2 = subgroup(phase2["Feed rate"].values, n_sub)

	xbar_p1 = sub_p1.mean(axis=1)
	s_p1 = sub_p1.std(axis=1, ddof=1)
	xbar_p2 = sub_p2.mean(axis=1)

	target = xbar_p1.mean()
	sbar = s_p1.mean()
	a_n = sqrt(2) * gamma(n_sub / 2) / (sqrt(n_sub - 1) * gamma((n_sub - 1) / 2))
	sigma_hat = sbar / a_n
	lcl = target - 3 * sigma_hat / sqrt(n_sub)
	ucl = target + 3 * sigma_hat / sqrt(n_sub)
	print(f"Feed rate Shewhart: target={target:.1f}  LCL={lcl:.1f}  UCL={ucl:.1f}")

	first_alarm_p2 = int(np.where((xbar_p2 < lcl) | (xbar_p2 > ucl))[0][0])
	print(f"first phase-2 alarm at subgroup index {first_alarm_p2}")

The 99.7% Shewhart limits on the feed rate come out at :math:`325.5 \pm 24.4`
(LCL = 301.0, UCL = 349.9), no phase-1 alarms, and the **first phase-2 alarm
appears at subgroup 62** -- about two hours into 16 December. The trace below
shows the phase-1 subgroups (in black) and the phase-2 subgroups (in blue),
with the limits derived from phase 1 carried across:

.. code-block:: python

	x_all = np.concatenate([xbar_p1, xbar_p2])
	idx_p1 = np.arange(len(xbar_p1))
	idx_p2 = np.arange(len(xbar_p1), len(x_all))

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=idx_p1, y=xbar_p1, mode="lines+markers",
		line=dict(color="black"), marker=dict(size=4, color="black"),
		name="Phase 1 (15 Dec)"))
	fig.add_trace(go.Scatter(x=idx_p2, y=xbar_p2, mode="lines+markers",
		line=dict(color="#1f77b4"), marker=dict(size=4, color="#1f77b4"),
		name="Phase 2 (16 Dec onwards)"))
	fig.add_hline(y=target, line_color="grey", line_dash="dot",
		annotation_text="target")
	fig.add_hline(y=ucl, line_color="red", line_dash="dash",
		annotation_text="UCL (3 sigma)")
	fig.add_hline(y=lcl, line_color="red", line_dash="dash",
		annotation_text="LCL (3 sigma)")
	fig.add_vline(x=len(xbar_p1) - 0.5, line_color="grey", line_dash="dot",
		annotation_text="phase 1 / 2")
	fig.update_layout(xaxis_title="Subgroup index (2 min each)",
		yaxis_title="Feed rate (subgroup mean)", height=380,
		margin=dict(l=70, r=20, t=40, b=50))
	fig.show()

.. figure:: ../figures/monitoring/Flotation-MSPC-shewhart.png
	:alt: Shewhart chart of Feed rate subgroup means across phase 1 and phase 2 with 3-sigma limits.
	:width: 900px
	:scale: 80
	:align: center

	Shewhart chart on ``Feed rate`` (subgroup size 4, 2-minute aggregation):
	phase-1 subgroups in black, phase-2 subgroups in blue, 3-sigma limits
	(``LCL = 301.0`` and ``UCL = 349.9``) carried across from phase 1. The
	first phase-2 alarm sits at subgroup 62, ~2 hours into 16 December.

The chart does flag the disturbance eventually, but the first alarm sits at
subgroup 62, with the disturbance well-established by that point. The
question is whether the other four tags carry information that, combined
with feed rate, would have caught the shift earlier.

.. _APPS_multivariate_monitoring_pca:

Multivariate model on phase 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So the multivariate analysis is on the same statistical object as the
univariate Shewhart chart above, we aggregate each set of four
consecutive 30-second observations into a 2-minute subgroup mean before
fitting. Otherwise, the multivariate model would be fit on the raw
30-second observations and the comparison against the Shewhart chart
later in the section would be unfair: the multivariate machinery would
be picking up within-subgroup noise that the Shewhart chart has averaged
away.

.. code-block:: python

	def subgroup_means(df, n_sub):
	    """Average each block of n_sub consecutive rows into a single row."""
	    n_groups = len(df) // n_sub
	    arr = df.values[: n_groups * n_sub].reshape((n_groups, n_sub, df.shape[1]))
	    return pd.DataFrame(arr.mean(axis=1), columns=df.columns)

	p1_sub = subgroup_means(phase1, n_sub)
	p2_sub = subgroup_means(phase2, n_sub)
	print(f"phase 1 subgroups: {p1_sub.shape}   phase 2 subgroups: {p2_sub.shape}")

This gives 119 phase-1 subgroups and 610 phase-2 subgroups. We centre
and scale the 5 tags using their phase-1 subgroup means and standard
deviations, then fit a :math:`A`-component PCA on phase 1 only. The
cumulative :math:`R^2_X` tells us how much joint variability each latent
variable picks up:

.. code-block:: python

	scaler = MCUVScaler().fit(p1_sub)
	model = PCA(n_components=2).fit(scaler.transform(p1_sub))
	print("R^2 cumulative (2 components):", model.r2_cumulative_.values)

	model3 = PCA(n_components=3).fit(scaler.transform(p1_sub))
	print("R^2 cumulative (3 components):", model3.r2_cumulative_.values)

A 2-component model captures :math:`R^2_X \approx [0.38, 0.61]` (38% and an
extra 23%, for a cumulative 61%), and a third component adds another 21%.
Two components are enough to demonstrate the monitoring idea, so we proceed
with the 2-component model.

The score plot of phase 1 with the 95% Hotelling's :math:`T^2` ellipse shows
where the in-control operating region lies in score space:

.. code-block:: python

	model.score_plot(pc_horiz=1, pc_vert=2).show()

.. figure:: ../figures/monitoring/Flotation-MSPC-score-phase1.png
	:alt: Phase-1 score plot of the flotation cell with the 95% T^2 ellipse.
	:width: 600px
	:scale: 80
	:align: center

	Phase-1 score plot (119 subgroup means from 15 December) with the 95%
	:math:`T^2` ellipse drawn in. The in-control cloud sits inside the
	ellipse and is roughly centred at the origin.

The phase-1 cloud is roughly elliptical and centred at the origin -- exactly
what we want from a stable operating period. The loadings tell us which raw
tags align with each latent direction:

.. code-block:: python

	for a in (1, 2):
	    p = model.loadings_.iloc[:, a - 1]
	    fig = go.Figure(go.Bar(x=p.index, y=p.values, marker_color="#4c72b0"))
	    fig.add_hline(y=0, line_color="black", line_width=0.6)
	    fig.update_layout(yaxis_title=f"p{a} loading", height=320,
	        margin=dict(l=70, r=20, t=20, b=80))
	    fig.show()

.. figure:: ../figures/monitoring/Flotation-MSPC-loadings.png
	:alt: Loading bar plots for the first two principal components of the flotation model.
	:width: 900px
	:scale: 80
	:align: center

	First and second loading vectors as bar plots. :math:`p_1` is dominated
	by the air-flow / pulp-level / pH triple (the aeration-and-froth regime
	of the cell); :math:`p_2` is dominated by ``Feed rate`` and ``CuSO4
	added`` (the reagent-and-throughput axis).

.. _APPS_multivariate_monitoring_phase2:

Monitoring phase 2 with :math:`T^2` and SPE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To monitor phase 2, we project each new subgroup mean onto the model and
read out two diagnostics:

* the Hotelling's :math:`T^2` score on the model plane (how unusual the
  subgroup is *within* the in-control subspace), and
* the squared prediction error SPE (how far off the model plane the
  subgroup sits -- i.e. how much of the joint structure is *not* explained
  by the model).

``PCA.predict`` returns both, alongside the per-subgroup scores:

.. code-block:: python

	result = model.predict(scaler.transform(p2_sub))
	t2 = result.hotellings_t2.iloc[:, -1]
	spe = result.spe
	t2_lim = float(model.hotellings_t2_limit(conf_level=0.95))
	spe_lim = float(model.spe_limit(conf_level=0.95))
	print(f"95% T^2 limit: {t2_lim:.2f}")
	print(f"95% SPE limit: {spe_lim:.2f}")

	flagged_t2 = t2[t2 > t2_lim]
	flagged_spe = spe[spe > spe_lim]
	first_t2 = int(flagged_t2.index[0]) if len(flagged_t2) else None
	first_spe = int(flagged_spe.index[0]) if len(flagged_spe) else None
	print(f"first T^2 alarm at phase-2 subgroup {first_t2}")
	print(f"first SPE alarm at phase-2 subgroup {first_spe}")

The 95% T² limit is 6.25 and the 95% SPE limit is 2.38. **Both diagnostics
first alarm at phase-2 subgroup 5**, about ten minutes into 16 December.
Compare that with ~120 minutes of feed-rate Shewhart silence before its
first alarm at subgroup 62. Drawing the two multivariate traces side by
side with their 95% limits:

.. code-block:: python

	fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.07,
		subplot_titles=("Hotelling's T^2 on phase 2", "SPE on phase 2"))
	fig.add_trace(go.Scatter(x=t2.index, y=t2.values, mode="lines",
		line=dict(color="#1f77b4"), name="T^2", showlegend=False),
		row=1, col=1)
	fig.add_hline(y=t2_lim, line_color="red", line_dash="dash",
		annotation_text="95%", row=1, col=1)
	fig.add_trace(go.Scatter(x=spe.index, y=spe.values, mode="lines",
		line=dict(color="#d62728"), name="SPE", showlegend=False),
		row=2, col=1)
	fig.add_hline(y=spe_lim, line_color="red", line_dash="dash",
		annotation_text="95%", row=2, col=1)
	fig.update_xaxes(title_text="Phase-2 subgroup index (2 min each)", row=2, col=1)
	fig.update_yaxes(title_text="T^2", row=1, col=1)
	fig.update_yaxes(title_text="SPE", row=2, col=1)
	fig.update_layout(height=560, margin=dict(l=70, r=20, t=60, b=50))
	fig.show()

.. figure:: ../figures/monitoring/Flotation-MSPC-t2-spe.png
	:alt: Hotelling's T^2 and SPE traces on the phase-2 flotation subgroups with 95% limits.
	:width: 900px
	:scale: 80
	:align: center

	Hotelling's :math:`T^2` (top, 95% limit at 6.25) and SPE (bottom, 95%
	limit at 2.38) on the 610 phase-2 subgroups. Both first cross their
	limit at subgroup 5 (~10 minutes into 16 December) and stay elevated
	through most of the day.

Both diagnostics rise within minutes of 16 December starting and stay
elevated for most of the day -- a much earlier and stronger signal than the
univariate chart on feed rate alone.

.. _APPS_multivariate_monitoring_contribution:

Diagnosing the alarm: contribution plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :math:`T^2` and SPE statistics tell us *that* the operation has moved
off-spec; the contribution plot tells us *which* tag drove the alarm. For an
SPE alarm, the per-variable contribution is :math:`(x_k - \hat{x}_k)^2` in
the centred-and-scaled space:

.. code-block:: python

	first_alarm = int(flagged_spe.index[0])
	row_scaled = scaler.transform(p2_sub).loc[first_alarm].values
	row_hat = row_scaled @ model.loadings_.values @ model.loadings_.values.T
	contribs = pd.Series((row_scaled - row_hat) ** 2,
		index=p1_sub.columns, name="SPE contribution")

	fig = go.Figure(go.Bar(x=contribs.index, y=contribs.values,
		marker_color="#d62728"))
	fig.update_layout(
		title=f"SPE contributions at phase-2 subgroup {first_alarm} (16 Dec, first SPE alarm)",
		yaxis_title="(x_k - x_hat_k)^2 in scaled units", height=380,
		margin=dict(l=70, r=20, t=60, b=80))
	fig.show()

.. figure:: ../figures/monitoring/Flotation-MSPC-contributions.png
	:alt: Per-variable SPE contributions at the first phase-2 SPE alarm.
	:width: 700px
	:scale: 80
	:align: center

	Per-variable contributions to SPE at phase-2 subgroup 5 (16 Dec, first
	SPE alarm). ``Pulp level`` (5.8) and ``Feed rate`` (3.8) dominate;
	``Upstream pH`` is a distant third (1.3). ``CuSO4 added`` and ``Air
	flow rate`` are essentially in pattern.

At the first SPE alarm, **``Pulp level`` and ``Feed rate``** carry the
largest contributions (5.8 and 3.8 respectively in scaled-squared units),
with ``Upstream pH`` a distant third (1.3). The contribution plot points
the operator straight at the two tags worth investigating, without having
to scan all five line plots by eye.

.. _APPS_multivariate_monitoring_compare:

What the multivariate chart catches that the univariate chart misses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To make the comparison concrete we plot the ``Feed rate`` subgroup mean
(left axis, blue) and the multivariate Hotelling's :math:`T^2` (right
axis, red) on the same time axis -- 610 phase-2 subgroups, each two
minutes apart:

.. code-block:: python

	fig = make_subplots(specs=[[{"secondary_y": True}]])
	x = np.arange(len(t2))
	feed_p2 = subgroup_means(phase2[["Feed rate"]], n_sub)["Feed rate"].values
	fig.add_trace(go.Scatter(x=x, y=feed_p2, mode="lines+markers",
		line=dict(color="#1f77b4"), marker=dict(size=3),
		name="Feed rate (subgroup mean, left)"), secondary_y=False)
	fig.add_hline(y=target, line_color="#1f77b4", line_dash="dot", opacity=0.6)
	fig.add_hline(y=ucl, line_color="#1f77b4", line_dash="dash", opacity=0.6)
	fig.add_hline(y=lcl, line_color="#1f77b4", line_dash="dash", opacity=0.6)

	fig.add_trace(go.Scatter(x=x, y=t2.values, mode="lines+markers",
		line=dict(color="#d62728"), marker=dict(size=3),
		name="Hotelling's T^2 (right)"), secondary_y=True)
	fig.add_hline(y=t2_lim, line_color="#d62728", line_dash="dash", opacity=0.6)

	fig.update_yaxes(title_text="Feed rate (t/h)", color="#1f77b4", secondary_y=False)
	fig.update_yaxes(title_text="Hotelling's T^2", color="#d62728", secondary_y=True)
	fig.update_xaxes(title_text="Phase-2 subgroup index (2 min each)")
	fig.update_layout(height=440, margin=dict(l=70, r=70, t=40, b=60))
	fig.show()

.. figure:: ../figures/monitoring/Flotation-MSPC-comparison.png
	:alt: Dual-axis overlay of Feed-rate subgroups and Hotelling's T^2 on phase 2.
	:width: 950px
	:scale: 80
	:align: center

	Phase-2 ``Feed rate`` subgroup mean (left axis, blue) and Hotelling's
	:math:`T^2` of the 5-variable subgroup mean (right axis, red), on a
	shared subgroup-index x-axis. Dashed lines on each axis are the 95 %
	limits; vertical dotted lines mark the first alarm on each chart. The
	multivariate :math:`T^2` (subgroup 5) leads the univariate Shewhart
	(subgroup 62) by 57 subgroups, or about 114 minutes.

Putting the two stories side by side:

* The univariate Shewhart chart on ``Feed rate`` is silent through all
  of phase 1 (as it should be) and only alarms at subgroup 62 of phase 2,
  about **two hours** into the new day. By the time it alarms, the
  disturbance has grown large enough to push the subgroup mean past the
  3-sigma limit on this *single* tag.
* The multivariate :math:`T^2` chart -- on the *same* 2-minute subgroups
  -- alarms at phase-2 subgroup 5, about **ten minutes** into the new day.
  The SPE chart alarms at the same subgroup. Both diagnose the cause as a
  joint shift in ``Pulp level`` and ``Feed rate``.

The ~110-minute gap is the multivariate dividend on this dataset, and
the fair-comparison qualifier matters: both charts are aggregating the
same data into the same 2-minute subgroups, so the dividend cannot be
explained away by saying "the multivariate chart just samples faster".
It comes from the fact that the disturbance is initially small in each
individual tag (no single tag is yet outside its own 3-sigma band) but
it has already broken the *correlation structure* the model learned in
phase 1 -- and the SPE statistic catches that violation directly.

This is the same pattern :ref:`monitoring is not feedback control
<monitoring_is_not_feedback_control>` warned about in chapter 3: catching
the upset early gives the operator time to act before off-spec material
moves downstream. The price of admission is a model -- not three chart
limits, but a 2-component PCA on a phase-1 stretch -- and the running cost
is a single ``model.predict(scaler.transform(new_row))`` per new
observation.

.. note::

	A few practical considerations not pursued here but worth flagging:

	* **Re-fitting**. The phase-1 / phase-2 split is a static demonstration;
	  in production the model has to be kept current. Several strategies
	  are in routine use: re-fit periodically on the most recent stretch of
	  fresh data; re-fit *reactively* when the alarm rate climbs above
	  some threshold (simple, but it can produce frustrating false alarms
	  if "alarm rate" is just measuring a real but slow drift the operator
	  is already aware of); or use an *adaptive* model that updates
	  continuously from a small rolling window of in-control data without
	  a discrete re-fit step. `Kadlec, Grbić and Gabrys (2011)
	  <https://literature.learnche.org/item/106/review-of-adaptation-mechanisms-for-data-driven-soft-sensors>`_
	  review the trade-offs of the three approaches in detail. The same
	  considerations apply to the :ref:`Kappa soft sensor
	  <APPS_soft_sensors_case_kamyr>` discussed in §7.2.
	* **Autocorrelation**. The 30-second sampling makes consecutive
	  observations highly correlated. A practical deployment usually
	  monitors the 2-minute subgroup mean rather than every 30-second
	  sample, exactly as the univariate Shewhart chart above does.
	* **Contribution plots are correlational**. A high contribution from
	  ``Pulp level`` says the variable is *off-pattern relative to the
	  others*, not that it is the *cause* of the upset. Diagnosis is for
	  the process engineer with knowledge of the unit operation.

Further reading
~~~~~~~~~~~~~~~

Foundational MSPC papers
^^^^^^^^^^^^^^^^^^^^^^^^

* James V. Kresta, John F. MacGregor and Thomas E. Marlin, "`Multivariate statistical monitoring of process operating performance <https://literature.learnche.org/item/9/multivariate-statistical-monitoring-of-process-operating-performance>`_", *Canadian Journal of Chemical Engineering*, **69**, 35-47, 1991.

* John F. MacGregor and Theodora Kourti, "`Statistical process control of multivariate processes <https://literature.learnche.org/item/16/statistical-process-control-of-multivariate-processes>`_", *Control Engineering Practice*, **3**, 403-414, 1995.

* Theodora Kourti and John F. MacGregor, "`Process analysis, monitoring and diagnosis using multivariate projection methods <https://literature.learnche.org/item/31/process-analysis-monitoring-and-diagnosis-using-multivariate-projection-methods>`_", *Chemometrics and Intelligent Laboratory Systems*, **28**, 3-21, 1995.

* Theodora Kourti and John F. MacGregor, "`Multivariate SPC methods for process and product monitoring <https://literature.learnche.org/item/81/multivariate-spc-methods-for-process-and-product-monitoring>`_", *Journal of Quality Technology*, **28**, 409-428, 1996.

* Johan A. Westerhuis, Theodora Kourti and John F. MacGregor, "`Analysis of multiblock and hierarchical PCA and PLS models <https://literature.learnche.org/item/95/analysis-of-multiblock-and-hierarchical-pca-and-pls-models>`_", *Journal of Chemometrics*, **12**, 301-321, 1998.

* Theodora Kourti, "`Process analysis and abnormal situation detection: From theory to practice <https://literature.learnche.org/item/87/process-analysis-and-abnormal-situation-detection-from-theory-to-practice>`_", *IEEE Control Systems*, **22**, 10-25, 2002.

* Theodora Kourti, "`Abnormal situation detection, three-way data and projection methods; robust data archiving and modeling for industrial applications <https://literature.learnche.org/item/120/abnormal-situation-detection-three-way-data-and-projection-methods-robust-data-archiving-and-modeling-for-industrial-applications>`_", *Annual Reviews in Control*, **27**, 131-139, 2003.

* Theodora Kourti, "`Application of latent variable methods to process control and multivariate statistical process control in industry <https://literature.learnche.org/item/88/application-of-latent-variable-methods-to-process-control-and-multivariate-statistical-process-control-in-industry>`_", *International Journal of Adaptive Control and Signal Processing*, **19**, 213-246, 2005.

Fault detection and diagnosis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Seongkyu Yoon and John F. MacGregor, "`Statistical and causal model-based approaches to fault detection and isolation <https://literature.learnche.org/item/89/statistical-and-causal-model-based-approaches-to-fault-detection-and-isolation>`_", *AIChE Journal*, **46**, 1813-1824, 2000.

* Seongkyu Yoon and John F. MacGregor, "`Fault diagnosis with multivariate statistical models part I: Using steady state fault signatures <https://literature.learnche.org/item/90/fault-diagnosis-with-multivariate-statistical-models-part-i-using-steady-state-fault-signatures>`_", *Journal of Process Control*, **11**, 387-400, 2001.

* Paige Miller, Ronald E. Swanson and Charles E. Heckler, "`Contribution plots: A missing link in multivariate quality control <https://literature.learnche.org/item/78/contribution-plots-a-missing-link-in-multivariate-quality-control>`_", *Applied Mathematics and Computer Science*, **8**, 775-792, 1998.

* Carlos R. Alvarez, Adriana Brandolin and Mabel C. Sánchez, "`On the variable contributions to the D-statistic <https://literature.learnche.org/item/21/on-the-variable-contributions-to-the-d-statistic>`_", *Chemometrics and Intelligent Laboratory Systems*, **88**, 189-196, 2007.

* Roy De Maesschalck, Delphine Jouan-Rimbaud and D. Luc Massart, "`The Mahalanobis distance <https://literature.learnche.org/item/67/the-mahalanobis-distance>`_", *Chemometrics and Intelligent Laboratory Systems*, **50**, 1-18, 2000.

* Joe Qin, Sergio Valle and Michael J. Piovoso, "`On unifying multiblock analysis with application to decentralized process monitoring <https://literature.learnche.org/item/165/on-unifying-multiblock-analysis-with-application-to-decentralized-process-monitoring>`_", *Journal of Chemometrics*, **15**, 715-742, 2001.

Industrial troubleshooting case studies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Bert Skagerberg, John F. MacGregor and Costas Kiparissides, "`Multivariate data analysis applied to low-density polyethylene reactors <https://literature.learnche.org/item/27/multivariate-data-analysis-applied-to-low-density-polyethylene-reactors>`_", *Chemometrics and Intelligent Laboratory Systems*, **14**, 341-356, 1992.

* John F. MacGregor, Christiane M. Jaeckle, Costas Kiparissides and M. Koutoudi, "`Process monitoring and diagnosis by multiblock PLS method <https://literature.learnche.org/item/29/process-monitoring-and-diagnosis-by-multiblock-pls-method>`_", *AIChE Journal*, **40**, 826-838, 1994.

* Salvador García-Muñoz, Theodora Kourti, John F. MacGregor, Arthur G. Mateos and Gerald Murphy, "`Troubleshooting of an industrial batch process using multivariate methods <https://literature.learnche.org/item/24/troubleshooting-of-an-industrial-batch-process-using-multivariate-methods>`_", *Industrial and Engineering Chemistry Research*, **42**, 3592-3601, 2003.

* Ivan Miletic, Shannon Quinn, Michael Dudzic, Vit Vaculik and Marc Champagne, "`An industrial perspective on implementing on-line applications of multivariate statistics <https://literature.learnche.org/item/18/an-industrial-perspective-on-implementing-on-line-applications-of-multivariate-statistics>`_", *Journal of Process Control*, **14**, 821-836, 2004.

Theses (McMaster University)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Carol F. Slama, `Multivariate statistical analysis of data from an industrial fluidized catalytic cracking process using PCA and PLS <https://literature.learnche.org/item/59/multivariate-statistical-analysis-of-data-from-an-industrial-fluidized-catalytic-cracking-process-using-pca-and-pls>`_, Masters thesis, 1991.

* Carl Duchesne, `Improvement of processes and product quality through multivariate data analysis <https://literature.learnche.org/item/46/improvement-of-processes-and-product-quality-through-multivariate-data-analysis>`_, Ph.D thesis, 2000.

* François Yacoub, `Learning from data using latent variable methods <https://literature.learnche.org/item/112/learning-from-data-using-latent-variable-methods>`_, Ph.D thesis, 2006.

* Emily Nichols, `Latent variable methods: Case studies in the food industry <https://literature.learnche.org/item/113/latent-variable-methods-case-studies-in-the-food-industry>`_, Masters thesis, 2011.
