.. _APPS_soft_sensors:

Soft sensors and inferential sensors
=====================================

.. index::
	single: soft sensors
	single: inferential sensors
	pair: soft sensors; applications

A soft sensor (also called an inferential sensor) infers a hard-to-measure quality variable from
cheap, real-time process measurements that are already on the data historian. The use of PLS for
exactly this purpose was introduced by `Kresta, Marlin and MacGregor (1994)
<https://literature.learnche.org/item/17/development-of-inferential-process-models-using-pls>`_.
The next subsection outlines what these sensors are and how they are built; the rest of this
section is a worked example: predicting the Kappa number on a continuous Kamyr pulp digester,
where the Kappa number is reported less often, and with more delay, than the process tags
around it.

.. _LVM_inferential_sensors:

What a soft sensor is
~~~~~~~~~~~~~~~~~~~~~

The intention of an inferential sensor is to infer a hard-to-measure property, usually a lab
measurement or an expensive measurement, using a combination of process data and
software-implemented algorithms. These sensors also go by the names of software sensors or just
soft sensors.

Consider a distillation column where various automatic measurements are used to predict the
vapour pressure. The actual vapour pressure is a lab measurement, usually taken 3 or 4 times per
week, and takes several hours to complete. The soft sensor can predict the lab value from the
real-time process measurements with sufficient accuracy. This is a common soft sensor on
distillation columns. The lab values are used to build (train) the software sensor and to update
in periodically.

Other interesting examples use camera images to predict hard-to-measure values. In the paper by
`Honglu Yu, John MacGregor, Gabe Haarsma and Wilfred Bourg
<https://literature.learnche.org/item/57/digital-imaging-for-online-monitoring-and-control-of-industrial-snack-food-processes>`_
(*Ind. Eng. Chem. Res.*, **42**, 3036–3044, 2003), the authors describe how machine vision is
used to predict, in real-time, the seasoning of various snack-food products. This sensors uses
the colour information of the snacks to infer the amount of seasoning dispensed onto them. The
dispenser is controlled via a feedback loop to ensure the seasoning is at target.

Once validated, a soft sensor can also reduce costs of a process by allowing for rapid feedback
control of the inferred property, so that less off-specification product is produced. They also
often have the side-effect that reduced lab sampling is required; this saves on manpower costs.

Soft sensors using latent variables will almost always be PLS models. Once the model has been
built, it can be applied in real-time. The |T2| and SPE value for each new observation is checked
for consistency with the model before a prediction is made. Contribution plots are used to
diagnose unusual observations.

It is an indication that the predictive models need to be updated if the SPE and/or |T2| values
are consistently above the limits. This is a real advantage over using an MLR-based model, which
has no such consistency checks.

.. _APPS_soft_sensors_monitoring_recap:

Recap: process monitoring and the lab-measurement gap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recall from the earlier chapter on :ref:`process monitoring <SECTION-process-monitoring>` that
control charts are built in two phases: phase 1 fits a chart to a stretch of stable historical
data, and phase 2 uses that chart on new, real-time data to flag unusual variability so that an
operator can intervene. We were careful to point out that
:ref:`monitoring is not feedback control <monitoring_is_not_feedback_control>`: the adjustments
that follow an alarm are infrequent, manual, and made only when a special cause has been
identified.

This procedure has a practical requirement: the variable being charted must be available in
real-time. A temperature, a flow rate, a pressure or an on-line composition analyser update every
few seconds and present no difficulty. The case that does not fit is the lab measurement: a final
quality property that is sampled at intervals of an hour or more, and -- depending on whether the
mill has an on-line analyser or a wet-chemistry titration in a busy lab -- reported with a
turnaround of anywhere from a minute to a couple of hours. Even when the chemistry itself is
fast, the sampling interval is enough to leave a chart that updates only a few times per shift,
which is too sparse to react to disturbances before the off-spec material has moved downstream.

A soft sensor solves this problem by inferring the lab value in real-time from the process tags
that are available at that moment. The model is built on historical data where both the process
tags and the lab values were collected; once it has been validated the prediction is used in
place of the lab value on the monitoring chart, on the on-line trend, or in a feedback loop. The
phase 1 and phase 2 requirements still apply: the model is fit on a representative stretch of
data, then tested on data it has not seen before it is deployed. For a step-by-step procedure
that covers the engineering choices along the way, see `Lin, Recke, Knudsen and Jørgensen (2007)
<https://literature.learnche.org/item/107/a-systematic-approach-for-soft-sensor-development>`_.

.. _APPS_soft_sensors_case_kamyr:

Case study: predicting Kappa number on a Kamyr digester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A continuous Kamyr digester cooks wood chips under pressure in white-liquor to dissolve the lignin
that binds the cellulose fibres. The amount of lignin that remains in the pulp is summarised by a
single quality number, the :index:`Kappa number`. A high Kappa number indicates a brown,
paperboard-grade pulp; a low Kappa number indicates a pulp that is closer to a bleachable grade.
The mill aims to hold the Kappa number on target with as little variability as possible.

The Kappa number is conventionally a wet-chemistry lab measurement defined by the ISO 302
titration method, which is itself about 30 minutes of bench work; once sampling, transport,
sample preparation, lab queueing and reporting are added, the practical turnaround on a busy
mill is typically one to two hours, and the sampling frequency is usually no faster than that.
Modern installations also offer on-line NIR analysers that can return a Kappa-equivalent value
in under a minute, calibrated against ISO 302, but these are still far from universal; on mills
that do not have one the fastest information about the digester is the existing process
historian, which is what a soft sensor lets us turn into a real-time Kappa estimate. `Dayal,
MacGregor, Taylor, Kildaw and Marcikic (1994)
<https://literature.learnche.org/item/124/application-of-feedforward-neural-networks-and-partial-least-squares-regression-to-modelling-kappa-number-in-a-continuous-kamyr-digester>`_
demonstrated PLS and neural networks side by side on exactly this problem and on the same data
set we use here.

The data set used here is the `Kamyr digester data <https://openmv.net/info/kamyr-digester>`_
from openmv.net, an hourly record from a kraft mill in Alberta. The file is 301 rows by 23
columns: the first column is an ``Observation`` timestamp, ``Y-Kappa`` is the lab measurement
that we want to predict, and the remaining 21 columns are process tags. Two of the process
columns, ``AAWhiteSt-4`` and ``SulphidityL-4``, are missing on about half of the rows and we
drop them, leaving 19 process tags in :math:`\mathbf{X}`.

Several of the tags have already been pre-aligned in time: a column name that ends in a digit
indicates how many hours that tag has been shifted to line up with the Kappa number it eventually
produces. For example, ``ChipLevel4`` is the chip level lagged 4 hours, ``BlackFlow-2`` is the
black-liquor flow lagged 2 hours, ``SteamHeatF-3`` is the steam-heater flow lagged 3 hours. The
unlagged tags (``ChipRate``, ``BF-CMratio``, ``BlowFlow``, ``UCZAA``, ``WeakLiquorF``,
``WeakWashF``) measure quantities that affect the pulp downstream of the digester or that change
slowly enough that the lag is negligible. The residence-time estimates were provided by the mill
along with the data.

We load the file, drop the timestamp and the two mostly-missing columns, and median-impute the
remaining gaps. The same ``digester`` dataframe is reused throughout this section, so the
plotting and modelling blocks below can be pasted in order to reproduce every figure:

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.multivariate import PLS, MCUVScaler

	digester = pd.read_csv("https://openmv.net/file/kamyr-digester.csv")
	digester.columns = [c.strip() for c in digester.columns]
	digester = digester.drop(columns=["Observation", "AAWhiteSt-4", "SulphidityL-4"])
	digester = digester.fillna(digester.median(numeric_only=True))

	sample = np.arange(len(digester))
	fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05)
	fig.add_trace(go.Scatter(x=sample, y=digester["Y-Kappa"], mode="lines",
		line=dict(color="black"), showlegend=False), row=1, col=1)
	fig.add_trace(go.Scatter(x=sample, y=digester["ChipLevel4"], mode="lines",
		line=dict(color="#1f77b4"), showlegend=False), row=2, col=1)
	fig.add_trace(go.Scatter(x=sample, y=digester["BlackFlow-2"], mode="lines",
		line=dict(color="#d62728"), showlegend=False), row=3, col=1)
	fig.update_yaxes(title_text="Y-Kappa", row=1, col=1)
	fig.update_yaxes(title_text="ChipLevel4", row=2, col=1)
	fig.update_yaxes(title_text="BlackFlow-2", row=3, col=1)
	fig.update_xaxes(title_text="Sample (1 hour spacing)", row=3, col=1)
	fig.update_layout(height=620, margin=dict(l=70, r=20, t=20, b=50))
	fig.show()

.. figure:: ../figures/monitoring/Kappa-soft-sensor-raw-data.png
	:alt: Raw Kappa number and two of the lagged process tags plotted against sample number.
	:width: 750px
	:scale: 90
	:align: center

	The Kappa number in the top panel covers a range of about 15 units (from 12 to 28 Kappa).
	The two pre-shifted process tags below it move on the same time-scale and provide the
	real-time information that the soft sensor will use.

.. _APPS_soft_sensors_building_model:

Building the soft sensor
~~~~~~~~~~~~~~~~~~~~~~~~

We build the model with PLS, using the Kappa number as the :math:`y`-variable and the nineteen
process tags as the :math:`\mathbf{X}` block. The ``process-improve`` package provides a ``PLS``
class and an ``MCUVScaler`` for centring and scaling. The data are centred to zero mean and
scaled to unit standard deviation before fitting: PLS scores and loadings are only interpretable
in that form.

.. code-block:: python

	X = digester.drop(columns=["Y-Kappa"])
	y = digester[["Y-Kappa"]]

	scaler_x = MCUVScaler().fit(X)
	scaler_y = MCUVScaler().fit(y)

	model = PLS(n_components=2).fit(scaler_x.transform(X), scaler_y.transform(y))

The cumulative :math:`R^2_Y` measures how much of the Kappa variability the model accounts for as
each latent variable is added:

.. code-block:: python

	>>> model.r2_cumulative_.values
	array([0.350, 0.503])

The first component picks up 35% of the Kappa variability, and the second adds another 15%, for a
cumulative 50%. This is not a high-:math:`R^2_Y` model in absolute terms, but for a soft sensor
on a continuous process it is enough to be useful, as we will see when we evaluate it on held-out
data below.

The regression coefficients show which tags drive the model:

.. code-block:: python

	coefs = model.beta_coefficients_.iloc[:, 0]
	colors = ["#1f77b4" if c >= 0 else "#d62728" for c in coefs.values]
	fig = go.Figure(go.Bar(x=coefs.index, y=coefs.values, marker_color=colors))
	fig.add_hline(y=0, line_color="black", line_width=0.6)
	fig.update_layout(yaxis_title="Coefficient on scaled X", xaxis_tickangle=-40,
		height=420, margin=dict(l=70, r=20, t=20, b=120))
	fig.show()

.. figure:: ../figures/monitoring/Kappa-soft-sensor-coefficients.png
	:alt: Bar chart of PLS regression coefficients onto Y-Kappa for the nineteen process tags.
	:width: 750px
	:scale: 80
	:align: center

	PLS regression coefficients on the centred and scaled :math:`\mathbf{X}`. The bar heights are
	directly comparable. ``BF-CMratio``, ``ChipLevel4``, ``SteamHeatF-3``, ``ChipRate``,
	``SteamFlow-4`` and ``WhiteFlow-4`` carry most of the relationship to ``Y-Kappa``.

The signs match what is known about the chemistry of the cook. A higher ``SteamHeatF-3``,
``SteamFlow-4`` or ``WhiteFlow-4`` puts more heat or active alkali into the digester, increases
the rate of delignification, and pulls the Kappa number down -- their coefficients are negative.
A higher ``ChipRate`` or ``ChipLevel4`` moves more wood through the digester for the same heat
and alkali, leaves more residual lignin, and pushes the Kappa number up. The coefficients are a
correlation, not a causation, but they agree with what a process engineer would predict from
first principles.

The cumulative :math:`R^2_Y` reports the fit on the data we trained on. To know whether the model
will be useful as a live soft sensor we have to evaluate it on data it has never seen. We split
the 301 rows in time order: the first 70% (211 rows) for training, the last 30% (90 rows) as a
held-out test set, and we report the root-mean-square error of prediction (RMSEP) on the test
set:

.. code-block:: python

	def evaluate_split(df, x_cols, y_col, frac=0.70):
		n_train = int(round(frac * len(df)))
		train, test = df.iloc[:n_train], df.iloc[n_train:]
		sx = MCUVScaler().fit(train[x_cols])
		sy = MCUVScaler().fit(train[[y_col]])
		m = PLS(n_components=2).fit(sx.transform(train[x_cols]), sy.transform(train[[y_col]]))
		y_hat_scaled = pd.DataFrame(
			np.asarray(m.predict(sx.transform(test[x_cols])).y_hat),
			index=test.index, columns=[y_col])
		y_hat = sy.inverse_transform(y_hat_scaled).values.ravel()
		y_obs = test[y_col].values
		rmsep = float(np.sqrt(np.mean((y_obs - y_hat) ** 2)))
		return rmsep, y_obs, y_hat

	x_cols = list(X.columns)
	rmsep_base, y_obs_base, y_hat_base = evaluate_split(digester, x_cols, "Y-Kappa")
	print(f"RMSEP (process tags only): {rmsep_base:.2f} Kappa units")

The same predicted-vs-observed scatter is reused below for the lag-augmented model, so we
define it once as a helper:

.. code-block:: python

	def plot_obs_pred(y_obs, y_hat, title):
		lo = float(min(y_obs.min(), y_hat.min()))
		hi = float(max(y_obs.max(), y_hat.max()))
		pad = 0.05 * (hi - lo)
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=[lo - pad, hi + pad], y=[lo - pad, hi + pad],
			mode="lines", line=dict(color="black", dash="dash", width=1), name="ideal"))
		fig.add_trace(go.Scatter(x=y_obs, y=y_hat, mode="markers",
			marker=dict(size=8, opacity=0.8), name="predictions"))
		fig.update_layout(title=title, xaxis_title="Observed Kappa",
			yaxis_title="Predicted Kappa", height=520, width=580)
		fig.update_yaxes(scaleanchor="x", scaleratio=1)
		fig.show()

	plot_obs_pred(y_obs_base, y_hat_base, "Soft sensor predictions: process tags only")

.. figure:: ../figures/monitoring/Kappa-soft-sensor-obs-pred-base.png
	:alt: Predicted vs observed Kappa number on the held-out test set with the process-tag model.
	:width: 600px
	:scale: 80
	:align: center

	Predicted *vs* observed Kappa number on the held-out test set, using only the 19 process tags.
	The RMSEP is 1.96 Kappa units.

The held-out RMSEP is 1.96 Kappa units, on a Kappa number that varies between 12 and 28 in this
dataset (standard deviation about 3 units). A soft sensor that is within 2 Kappa of the lab value
is already useful, and a common refinement makes it a fair bit better: include the previous Kappa
value as another predictor. Each time the lab returns a value we keep it as a one-step memory and
feed it back into :math:`\mathbf{X}` until the next lab value arrives. We add a column
``Kappa_lag1`` to the data, drop the first row (which has no previous Kappa), and re-fit:

.. code-block:: python

	df_lag = digester.copy()
	df_lag["Kappa_lag1"] = df_lag["Y-Kappa"].shift(1)
	df_lag = df_lag.dropna(subset=["Kappa_lag1"]).reset_index(drop=True)

	rmsep_lag, y_obs_lag, y_hat_lag = evaluate_split(df_lag, x_cols + ["Kappa_lag1"], "Y-Kappa")
	print(f"RMSEP (with one-step Kappa lag): {rmsep_lag:.2f} Kappa units")

	plot_obs_pred(y_obs_lag, y_hat_lag, "Soft sensor predictions: process tags + 1-step Kappa lag")

.. figure:: ../figures/monitoring/Kappa-soft-sensor-obs-pred-lagged.png
	:alt: Predicted vs observed Kappa with one-step Kappa lag in X.
	:width: 600px
	:scale: 80
	:align: center

	Adding the previous Kappa value as a twentieth predictor reduces the RMSEP from 1.96 to 1.73
	Kappa units, an improvement of about 12% on the same underlying data.

The scatter plots tell us how close the predictions are on average, but they hide *where* the
soft sensor disagrees with the lab. Plotting the two test-set predictions and the lab value
against time shows both stories on one figure:

.. code-block:: python

	sample = np.arange(len(y_obs_base))
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=sample, y=y_obs_base, mode="lines",
		line=dict(color="black", width=2.4), name="Lab (actual)"))
	fig.add_trace(go.Scatter(x=sample, y=y_hat_base, mode="lines+markers",
		line=dict(color="#1f77b4", dash="dash"), marker=dict(symbol="circle", size=6),
		name="Soft sensor: process tags only"))
	fig.add_trace(go.Scatter(x=sample[-len(y_hat_lag):], y=y_hat_lag, mode="lines+markers",
		line=dict(color="#d62728", dash="dot"), marker=dict(symbol="square", size=6),
		name="Soft sensor: process tags + Kappa lag"))
	fig.update_layout(xaxis_title="Test sample index (1 hour spacing)",
		yaxis_title="Kappa number", height=440)
	fig.show()

.. figure:: ../figures/monitoring/Kappa-soft-sensor-time-series.png
	:alt: Time-series overlay of held-out Kappa predictions and the actual lab values.
	:width: 900px
	:scale: 80
	:align: center

	Held-out test predictions over time. The actual lab Kappa is the solid black line; the
	process-tags-only prediction is the blue dashed line with round markers; the lag-augmented
	prediction is the red dotted line with square markers. Both soft sensors track the slow
	upward drift in the second half, but the lag-augmented model stays closer to the lab values
	on sample-to-sample swings, which is what drives the RMSEP down from 1.96 to 1.73.

.. note::

	The PLS coefficients are a measure of correlation, not causation. They are useful as a
	starting point for a discussion with the operators about what is driving the variability in
	the process, but they should not be interpreted as a cause-and-effect statement on their own.

This soft sensor can now be deployed in the same way as any other monitoring artefact: the model
is fit on a representative stretch of historical operation, tested on a held-out tail, and once
the RMSEP is small enough compared to the Kappa specification limits, the prediction is wired
into the same chart that would have been used for the lab value. The chart now updates every hour
rather than once per shift. `Tzovla and Mehta (2002)
<https://literature.learnche.org/item/103/creating-intelligence-automating-the-approach-to-development-and-online-operation-of-soft-sensors>`_
describe how this build-test-deploy loop can be automated for soft sensors inside commercial
control systems.

Two refinements are worth noting. First, the relationship between :math:`\mathbf{X}` and the
Kappa number changes over time, with chip species, mill upsets and seasonal raw-material
variation. A soft sensor that is never re-fit will gradually lose accuracy. The standard practice
is to re-fit the model on a rolling window of the most recent lab values; `Kadlec, Grbić and
Gabrys (2011) <https://literature.learnche.org/item/106/review-of-adaptation-mechanisms-for-data-driven-soft-sensors>`_
review the variations on this adaptation theme. Second, the Kappa number is autocorrelated in
time: we exploited this with a single one-step lag of :math:`y` above, but adding lags of two or
three hours, and lags on the most influential :math:`x` variables, typically reduces the
prediction error further.

.. _APPS_adaptive_soft_sensor:

Keeping a model current: an adaptive soft sensor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Catalysts age, heat exchangers foul, and feedstock and ambient conditions
shift. The operating point of a process drifts even while it stays in
common-cause operation, and a model that is never updated gradually falls out
of step with it. A prediction or monitoring statistic from such a model then
develops a systematic offset: its limits, set on earlier data, no longer match
where the process now sits, and normal operation starts to look abnormal.

The flotation example built one model on a phase-1 stretch and left it fixed,
which is fine for a short demonstration. A process moves over months and years,
though, so here we keep the model current instead.

This section works through that problem on a longer dataset. It uses a
:ref:`soft sensor <APPS_soft_sensors>`: a model that predicts a hard-to-measure
quality variable from routine process tags, filling in the gaps between
infrequent laboratory analyses. To keep the soft sensor current we use a
*recursive* (or *adaptive*) model, one that updates itself from each new
observation instead of being rebuilt from a stored history. The worked example
below builds a static soft sensor, watches it drift, and then lets an adaptive
model track the moving process; a short theory subsection in between explains
what the update actually does.

The `vapour-pressure dataset <https://openmv.net/info/vapor-pressure>`_ is an
hourly series from a distillation column that stabilises a hydrocarbon product
stream in a refinery, spanning about 2.5 years. There are 27 process tags, and
the quantity to predict is the **vapour pressure** of the product, measured in
the laboratory roughly three times a week. The laboratory value therefore
appears on only 232 of the 18 743 rows; on the rest it is blank. Twenty of the
tags are raw measurements (temperatures, flows, a pressure, an analyser and two
controller outputs); the other seven are engineered from first principles
(temperature differences, inverse absolute temperatures of the Antoine /
Clausius-Clapeyron form, an inverse pressure, and a physics-based Antoine
estimate of the vapour pressure itself).

The drift studied below is a genuine feature of this example, not something added
for the illustration. Over the 2.5 years the column did not settle at one new
steady state: it moved through several operating points, so the offset is not a
single fixed bias but shifts as the process does. Every prediction, monitoring
statistic and bias figure in this section is computed directly from the measured
tags and laboratory values.

We build the model on approximately the first half of the laboratory samples and
keep the rest to test on:

.. code-block:: python

	import numpy as np
	import pandas as pd
	import plotly.graph_objects as go
	from plotly.subplots import make_subplots
	from process_improve.multivariate import PLS, AdaptivePLS

	A = 3                                              # number of PLS components, used throughout
	DARK_BLUE, ORANGE, GREEN, GREY = "#1f3d7a", "#c55a11", "#2e6f3e", "#777777"   # figure colours, reused below

	vp = pd.read_csv("https://openmv.net/file/vapor-pressure.csv")
	vp["month"] = vp["hours_elapsed"] / 730.5          # about 730.5 hours per month
	tags = [c for c in vp.columns
	        if c not in ("hours_elapsed", "month", "vapour_pressure_kpa", "current_estimator")]

	lab_rows = np.where(vp["vapour_pressure_kpa"].notna().to_numpy())[0]   # rows with a lab value
	lab = vp.iloc[lab_rows].reset_index(drop=True)                        # the 232 labelled rows
	y_lab = lab["vapour_pressure_kpa"].to_numpy()

	n_train = len(lab) // 2                              # build on the first half of the lab samples
	train = lab.index < n_train
	drift_month = float(np.quantile(lab["month"], 0.60))
	post = lab["month"].to_numpy() >= drift_month       # "post-drift" test samples
	pre = ~post
	print(vp.shape, "| lab samples:", len(lab), "| training:", int(train.sum()),
	      "| drift near month", round(drift_month, 1))

This gives 18 743 hourly rows, 232 laboratory samples, a 116-sample training set
(the first half, covering roughly the first 10 months) and a drift that becomes
established near month 13.

The static soft sensor and its drift
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A PLS model with :math:`A = 3` components, fitted once on the training rows, is the
static baseline. The exact number of components matters little here. On the
training laboratory samples the cross-validated prediction error varies by less
than 1 kPa across two to five components, and the parameter-sensitivity sweep in
:ref:`the settings discussion below <APPS_adaptive_choosing_settings>` shows the
same flatness from the deployment side, where the one-step-ahead error changes
little across that range. Three is a small, standard choice within that flat
region; the adaptive model compensates for a component more or less in any case.

We will run it, and later an adaptive model, through the whole dataset with the
same helper. It is convenient to use ``AdaptivePLS`` for both: with every
forgetting factor set to zero it never changes, so it *is* the regular static PLS
model, and its ``update`` method returns the prediction, Hotelling's :math:`T^2`
and the SPE for each hourly row from one interface:

.. code-block:: python

	def stream(model, learn=None, y_update=None):
	    """Pass every hourly row through the model, returning per-row diagnostics.

	    learn     : boolean mask of rows the model may update from (others are predicted only)
	    y_update  : array of lab values (NaN where none) used to update the Y-side
	    """
	    Xrow = vp[tags].to_numpy()
	    pred = np.zeros(len(vp)); t2 = np.zeros(len(vp))
	    spe = np.zeros(len(vp)); dist = np.zeros(len(vp))
	    for i in range(len(vp)):
	        may_learn = True if learn is None else bool(learn[i])
	        if may_learn:
	            yv = None if (y_update is None or np.isnan(y_update[i])) else np.array([y_update[i]])
	            out = model.update(Xrow[i], y_row=yv, label=vp["month"].iloc[i])   # month-indexed history
	            pred[i], t2[i], spe[i], dist[i] = out.prediction[0], out.hotellings_t2, out.spe, out.distance
	        else:
	            pred[i] = model.predict(vp[tags].iloc[[i]]).to_numpy().ravel()[0]
	            dist[i] = dist[i - 1] if i else model.n_components
	    return pred, t2, spe, dist

	# Every rate below is zero, so this model never changes: it is the static
	# baseline. The adaptive model later turns these same zeros into small
	# non-zero values.
	static = AdaptivePLS(
	    n_components=A,             # three latent variables, as in the batch model above
	    forgetting_factor=0,        # mu = 0: the X-space kernel never updates
	    gamma=0,                    # no injection term (nothing to keep excited when frozen)
	    lambda_center=0,            # centering vector frozen at the training mean
	    alpha_scale=0,              # scaling vector frozen at the training spread
	    lambda_center_y=0,          # Y-centering frozen
	    alpha_scale_y=0,            # Y-scaling frozen
	    adaptive_spe_limit=False,   # keep the fixed SPE limit from the training data
	    conf_level=0.99,            # 99% monitoring limits
	)
	static.fit(lab.loc[train, tags], lab.loc[train, ["vapour_pressure_kpa"]])
	static_pred, static_t2, static_spe, _ = stream(static)

	def bias_std_rmsep(err, mask):
	    e = err[mask]
	    return float(e.mean()), float(e.std()), float(np.sqrt((e ** 2).mean()))

	err_static = static_pred[lab_rows] - y_lab
	print("static post-drift  bias / std / RMSEP:", bias_std_rmsep(err_static, post))
	print("static pre-drift   bias / std / RMSEP:", bias_std_rmsep(err_static, pre))

We report every result in the same form: the RMSEP, the bias and the variance,
each on the held-out testing data (after the drift) and, for reference, on the
baseline (before the drift). The variance is the square of the standard
deviation, so the three combine as
:math:`\text{RMSEP}^2 = \text{bias}^2 + \text{variance}`.

.. list-table:: Static PLS soft sensor: error on the baseline (before the drift) and on the testing data (after the drift).
	:header-rows: 1
	:widths: 34 22 22 22

	* - Data
	  - RMSEP [kPa]
	  - Bias [kPa]
	  - Variance [kPa²]
	* - Baseline (month 0 to 13)
	  - 6.8
	  - :math:`-0.4`
	  - 46
	* - Testing (month 13 to 26)
	  - 12.6
	  - :math:`+11.1`
	  - 35

The model tracks the laboratory values closely at first. From about month 13,
though, its predictions sit systematically **above** the laboratory values: the
error develops a persistent positive **bias** of :math:`+11.1` kPa (with a
standard deviation of 5.9 kPa, so a root-mean-square prediction error, RMSEP, of
12.6 kPa). Before the drift the same model is nearly unbiased (:math:`-0.4` kPa,
RMSEP 6.8 kPa). The bias is the systematic part of the error and the standard
deviation is the scatter; they combine as
:math:`\text{RMSEP}^2 = \text{bias}^2 + \text{variance}`, so after the drift the
error is almost entirely bias.

.. code-block:: python

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=lab["month"], y=y_lab, mode="markers",
	    marker=dict(size=4, color=GREY), name="Lab reference"))
	fig.add_trace(go.Scatter(x=vp["month"], y=static_pred, mode="lines",
	    line=dict(color=DARK_BLUE, width=1), name="Static PLS prediction"))
	fig.add_vline(x=drift_month, line_color=ORANGE, line_dash="dash")   # start of the testing data
	fig.add_annotation(x=drift_month, y=94, text="Testing data →", showarrow=False,
	    xanchor="left", xshift=6, font=dict(color=ORANGE, size=12))
	fig.update_layout(xaxis_title="Time since start [months]",
	    yaxis_title="Vapour pressure [kPa]", height=380,
	    margin=dict(l=70, r=20, t=30, b=50))
	fig.show()

.. figure:: ../figures/monitoring/adaptive-softsensor-motivation.png
	:alt: Static PLS soft-sensor prediction and laboratory values over the whole dataset; the prediction drifts above the lab values after month 13.
	:width: 900px
	:scale: 80
	:align: center

	The static soft sensor (blue) tracks the laboratory vapour pressure (grey)
	well for the first year, then predicts consistently high once the process
	drifts to a new operating point after month 13.

Monitoring shows the model ageing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The prediction error is only visible on the 3 days per week a laboratory sample
happens to arrive. The :math:`T^2` and SPE monitoring statistics are however
available every hour, and they signal any drift directly when they exceed their
limits, for example, the 99% limits. Projecting each hourly row onto the static
model gives both statistics for every hour:

.. code-block:: python

	t2_lim = float(static.hotellings_t2_limit(conf_level=0.99))
	spe_lim = float(static.update(vp[tags].to_numpy()[0]).spe_limit)   # fixed limit from the training data
	spe_cross = int((static_spe > spe_lim).sum())
	print(f"99% T2 limit {t2_lim:.2f} | 99% SPE limit {spe_lim:.2f} "
	      f"| SPE crossings {spe_cross} ({100 * spe_cross / len(vp):.1f}%)")

	fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
	    subplot_titles=("Hotelling's T² (99% limit)", "SPE (99% limit)"))
	fig.add_trace(go.Scatter(x=vp["month"], y=static_t2, line=dict(color=DARK_BLUE, width=0.5)), row=1, col=1)
	fig.add_hline(y=t2_lim, line_color="black", row=1, col=1)
	fig.add_trace(go.Scatter(x=vp["month"], y=static_spe, line=dict(color=DARK_BLUE, width=0.5)), row=2, col=1)
	fig.add_hline(y=spe_lim, line_color="black", row=2, col=1)
	# mark the times a laboratory sample was taken, as a row of asterisks in each panel
	fig.add_trace(go.Scatter(x=lab["month"], y=np.full(len(lab), 30), mode="markers",
	    marker=dict(symbol="star", size=5, color=ORANGE), name="Lab sample"), row=1, col=1)
	fig.add_trace(go.Scatter(x=lab["month"], y=np.full(len(lab), 20), mode="markers",
	    marker=dict(symbol="star", size=5, color=ORANGE), showlegend=False), row=2, col=1)
	for r in (1, 2):
	    fig.add_vline(x=drift_month, line_color="black", line_dash="dash", row=r, col=1)
	fig.update_yaxes(range=[0, 3 * t2_lim], row=1, col=1)
	fig.update_yaxes(range=[0, 3 * spe_lim], row=2, col=1)
	fig.update_layout(height=470, margin=dict(l=70, r=20, t=40, b=40),
	    xaxis2_title="Time since start [months]")
	fig.show()

.. figure:: ../figures/monitoring/adaptive-softsensor-monitoring.png
	:alt: Hotelling's T^2 and SPE traces from the static model over the whole dataset, with 99% limits and asterisks marking the laboratory-sample times; both statistics cross more often after the drift.
	:width: 900px
	:scale: 80
	:align: center

	Hotelling's :math:`T^2` (top) and SPE (bottom) from the static model over
	the whole dataset, against their 99% limits. The orange asterisks along the top
	of each panel mark the times a laboratory sample was taken (at an arbitrary
	height, 30 and 20, purely to sit above the traces); they show how sparse the
	reference is next to the hourly monitoring statistics. The SPE limit (7.89) is
	crossed on 1045 rows (5.6%), clustered in the periods where the process has
	moved off the model plane. These crossings are the signal that the model no
	longer describes current operation and should be brought up to date.

The SPE, the off-plane residual, crosses its 99% limit on 5.6% of the rows,
concentrated in the stretches where the process has moved away from the region
the training model was built on. That is the operational trigger to act on the drift
rather than to wait for the next laboratory result.

How the recursive update works
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two ways to keep a model current once monitoring shows it has aged. The
first, **moving-window re-fit**, holds a sliding window of recent data and refits
the model from it, perhaps weighting earlier observations down exponentially so
the fit tracks the process; this keeps a data store and rebuilds the model at each
refit. The second, **recursive updating**, updates the existing model in place:
each accepted observation moves the centring and scaling vectors and the
association matrices a little, and no window of past data is retained.
``AdaptivePLS`` takes the recursive route: it needs only bounded memory and
produces a model that moves continuously with the process. The rest of this
subsection describes the update; the settings it introduces map directly onto the
constructor arguments used in the next subsection.

The state carried between observations is small. It is a pair of **association
matrices** (also called kernels): :math:`\mathbf{X}'\mathbf{X}`, the sum of
cross-products of the process tags, and :math:`\mathbf{X}'\mathbf{Y}`, the
cross-products of tags with the response. A PLS model's weights and regression
coefficients can be recomputed from these two matrices alone, without the
original rows, using a kernel algorithm. Alongside the kernels the model keeps
the **centring** and **scaling** vectors, :math:`\mathbf{m}` and
:math:`\mathbf{s}`, that standardise each incoming row.

When observation :math:`i` arrives as a raw row :math:`\mathbf{x}_i^0`, the
centring and scaling vectors first move a little towards it, by an
exponentially-weighted moving average (EWMA) with per-variable rates
:math:`\lambda` (centre) and :math:`\alpha` (spread):

.. math::

   \mathbf{s}_{i+1}^2 = (1-\alpha)\,\mathbf{s}_i^2 + \alpha\,(\mathbf{x}_i^0 - \mathbf{m}_i)^2,
   \qquad
   \mathbf{m}_{i+1} = (1-\lambda)\,\mathbf{m}_i + \lambda\,\mathbf{x}_i^0 .

Using values of zero for these two rate parameters is like regular centring and scaling with frozen, unchanging vectors.
The same observation is then standardised with the *updated* vectors,
:math:`\mathbf{x}_i = (\mathbf{x}_i^0 - \mathbf{m}_{i+1}) \oslash \mathbf{s}_{i+1}`,
where :math:`\oslash` is element-by-element division, and this scaled row enters
the kernel update. (The monitoring statistics reported for row :math:`i` use the
*pre-update* vectors, so they judge the row against the model as it stood when
the row arrived.)

The X-space kernel is then blended: a fraction of the old kernel is forgotten and
the new row's contribution is mixed in, controlled by the **forgetting factor**
:math:`\mu`. A larger :math:`\mu` adapts faster but is less stable; in the extreme
it tracks every fluctuation, not only the genuine drift. A third term,
the **injection term**, re-adds a small amount of the *original* training kernel
:math:`(\mathbf{X}'\mathbf{X})_0`:

.. math::

   (\mathbf{X}'\mathbf{X})_{i+1} = (1-\mu)\,(\mathbf{X}'\mathbf{X})_i
      + \mu\,\mathbf{x}_i \mathbf{x}_i'
      + f\,(\mathbf{X}'\mathbf{X})_0,
   \qquad
   f = \gamma\,\frac{\lVert \mu\,\mathbf{x}_i \mathbf{x}_i' \rVert}{\lVert (\mathbf{X}'\mathbf{X})_0 \rVert}.

The injection weight :math:`f` scales with how much new information the row
carries, measured as the ratio of the update's size to the training kernel's size
(here each size is the matrix's trace, the sum of its eigenvalues, which for these
symmetric kernels is also known as the nuclear norm). The
tuning constant :math:`\gamma` sets the strength: with :math:`\gamma = 0.1`, a
row carrying as much information as the training data injects about 10% of the training kernel
back in. This keeps the kernel from becoming ill-conditioned during long quiet
stretches, when little new information arrives to excite it, and gently anchors
the adapting model to the region it was built on. Setting :math:`\gamma = 0`
recovers the textbook recursive update. After the blend, the kernel is rescaled
so its trace equals the training kernel's; this holds the eigenvalue scale
fixed, so the score scaling that Hotelling's :math:`T^2` depends on does not
drift for a purely numerical reason. The :math:`\mathbf{X}'\mathbf{Y}` kernel is
updated the same way when a response is present.

Because the laboratory value arrives only a few times a week, the X-side kernel
and the preprocessing update every hour while the :math:`\mathbf{X}'\mathbf{Y}`
kernel and the regression wait for the next laboratory value: passing
``y_row=None`` updates the process model without the response.

A single number summarises how far the model has moved. The **distance metric**
compares the current weight directions :math:`\mathbf{W}_i` with the training
directions :math:`\mathbf{W}_0`:

.. math::

   d_i = \operatorname{trace}\!\left( \mathbf{W}_0'\,\mathbf{W}_i\,\mathbf{W}_i'\,\mathbf{W}_0 \right).

It is the sum of squared cosines of the angles between the two sets of
directions, so it equals :math:`A` (the number of components) when the model is
unchanged and falls towards :math:`0` as the directions rotate away; it is
unaffected by sign flips of the weights. A value of :math:`0` would mean the
current weight directions are entirely orthogonal to the training ones: the
process would be operating in directions unrelated to those the model was built
on, a signal to rebuild the model rather than keep adapting it. What matters in
practice is its rate of
change: a smooth decline reflects gradual adaptation, while abrupt, noisy swings
indicate the model is chasing short-term upsets and the forgetting factor
:math:`\mu` should be reduced.

The settings map onto the constructor arguments as follows:

- :math:`\mu` is ``forgetting_factor``; :math:`\gamma` is ``gamma``;
- :math:`\lambda`, :math:`\alpha` are ``lambda_center``, ``alpha_scale`` for the
  X-block, and ``lambda_center_y``, ``alpha_scale_y`` for the Y-block;
- :math:`d_i` is available afterwards as the ``distance_`` attribute.

This particular framework, the injection term and the distance metric, comes from
the author's earlier work on an industrial adaptive-monitoring system; the
kernel PLS recomputation follows `Dayal and MacGregor (1997)
<https://literature.learnche.org/item/114/recursive-exponentially-weighted-pls-and-its-applications-to-adaptive-control-and-prediction>`_
and the subspace distance follows `Krzanowski (1979)
<https://literature.learnche.org/item/122/between-groups-comparison-of-principal-components>`_.

An adaptive model that tracks the drift
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the mechanism in hand, we can run the adaptive model. Two practical points
shape how it is used, both drawn from the way such
systems are operated. First, the model should *learn* only from valid,
steady operation: the shutdown and transition rows that push the SPE far past
its limit are still monitored, but they must not update the model. We reuse the
static SPE to select them. Second, the laboratory value is itself noisy, so a
smoothed reference is used to update the Y-side rather than each raw value:

.. code-block:: python

	learn = static_spe < 2.5 * spe_lim            # exclude gross shutdowns/transitions from learning
	print("rows the model may learn from:", int(learn.sum()), "of", len(vp))

	def ewma_smooth(values, lam=0.35):            # smooth the sparse lab reference
	    out = values.astype(float).copy()
	    seen = ~np.isnan(out)
	    idx = np.where(seen)[0]
	    for k in range(1, len(idx)):
	        out[idx[k]] = lam * out[idx[k]] + (1 - lam) * out[idx[k - 1]]
	    return out

	y_update = ewma_smooth(vp["vapour_pressure_kpa"].to_numpy())

	adaptive = AdaptivePLS(
	    n_components=A,                    # same three components as the static model
	    forgetting_factor=0.01,            # mu: how strongly each row is mixed into the kernel
	    gamma=0.05,                        # injection strength (kept small on this well-excited dataset)
	    lambda_center=0.003,               # slow drift of the X-centering vector
	    alpha_scale=0.012,                 # slow drift of the X-scaling vector
	    lambda_center_y=0.12,              # faster drift of the Y-centre (the bias correction)
	    alpha_scale_y=0.05,                # drift of the Y-scale
	    update_when_out_of_control=True,   # learning is gated by the `learn` mask below, not the limits
	    conf_level=0.99,
	)
	adaptive.fit(lab.loc[train, tags], lab.loc[train, ["vapour_pressure_kpa"]])
	adaptive_pred, _, _, distance = stream(adaptive, learn=learn, y_update=y_update)

	err_adaptive = adaptive_pred[lab_rows] - y_lab
	print("adaptive post-drift bias / std / RMSEP:", bias_std_rmsep(err_adaptive, post))
	print("adaptive pre-drift  bias / std / RMSEP:", bias_std_rmsep(err_adaptive, pre))

	def subgroup_mean(x, window, valid):        # trailing mean over valid hours only
	    out = x.copy()
	    for i in range(len(x)):
	        lo = max(0, i - window + 1)
	        seg = x[lo : i + 1][valid[lo : i + 1]]
	        out[i] = seg.mean() if len(seg) else x[i]
	    return out

	adaptive_24h = subgroup_mean(adaptive_pred, 24, learn)
	err_24h = adaptive_24h[lab_rows] - y_lab
	print("adaptive 24h-subgroup post-drift RMSEP:", round(bias_std_rmsep(err_24h, post)[2], 1))
	print("distance metric ages from", round(distance[0], 2), "to", round(distance[-1], 2))

Placing the two models side by side, on the baseline (before the drift) and on
the testing data (after the drift):

.. list-table:: Static and adaptive PLS soft sensors, on the baseline and testing data.
	:header-rows: 1
	:widths: 34 22 22 22

	* - Model and data
	  - RMSEP [kPa]
	  - Bias [kPa]
	  - Variance [kPa²]
	* - Static, baseline
	  - 6.8
	  - :math:`-0.4`
	  - 46
	* - Static, testing
	  - 12.6
	  - :math:`+11.1`
	  - 35
	* - Adaptive, baseline
	  - 9.6
	  - :math:`-2.2`
	  - 87
	* - Adaptive, testing
	  - 8.0
	  - :math:`+1.3`
	  - 63

The adaptive model removes the drift bias: its post-drift error is
:math:`+1.3` kPa (RMSEP 8.0 kPa) where the static model sat at :math:`+11.1` kPa
(RMSEP 12.6 kPa). The remaining error is now scatter rather than bias. That
scatter is set by the hour-to-hour prediction noise and the laboratory
measurement noise; averaging the prediction over a 24-hour window (a subgroup
mean, as with the flotation chart) brings the post-drift RMSEP down to 7.5 kPa,
without changing the bias.

.. code-block:: python

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=lab["month"], y=err_static, mode="markers",
	    marker=dict(size=6, color=GREEN, symbol="square"), name="Static PLS"))
	fig.add_trace(go.Scatter(x=lab["month"], y=err_adaptive, mode="markers",
	    marker=dict(size=6, color=DARK_BLUE, symbol="circle"), name="Adaptive PLS"))
	fig.add_hline(y=0, line_color="black", line_width=0.8)
	fig.add_vline(x=drift_month, line_color=ORANGE, line_dash="dash")   # start of the testing data
	fig.add_annotation(x=drift_month, y=18, text="Testing data →", showarrow=False,
	    xanchor="left", xshift=6, font=dict(color=ORANGE, size=12))
	fig.update_layout(xaxis_title="Time since start [months]",
	    yaxis_title="Prediction error [kPa]", height=380,
	    margin=dict(l=70, r=20, t=30, b=50))
	fig.show()

.. figure:: ../figures/monitoring/adaptive-softsensor-payoff.png
	:alt: Prediction error over time for the static and adaptive models; static errors climb to +11 kPa after the drift while adaptive errors stay near zero.
	:width: 900px
	:scale: 80
	:align: center

	Prediction error (predicted minus laboratory) for the static (green squares)
	and adaptive (blue circles) models. After the drift the static errors sit
	around :math:`+11` kPa; the adaptive errors stay centred near zero, at the cost
	of a little more scatter.

What drives the adaptation: preprocessing or kernel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The adaptive model changes two things as it runs: the **preprocessing** (the
centring and scaling vectors, which follow the operating point) and the
**kernel** (the weight directions and regression coefficients, recomputed from
the association matrices). How much does each contribute, and in what proportion?
``AdaptivePLS`` can separate them. For each observation it splits the adaptive
prediction's departure from the frozen training model into two parts: a
*preprocessing part*, the effect of the moved centring and scaling with the
regression held at its training value; and a *kernel part*, the further effect of
the moved directions and coefficients. The two parts add up to the total
departure. The ``prediction_channels_`` attribute records the split, and
``center_shift_`` and ``distance_`` report how far each kind of state has moved:

.. code-block:: python

	ch = adaptive.prediction_channels_                 # month-indexed: static / preprocessing / kernel
	rotation = A - adaptive.distance_                  # components of subspace rotation from the training model

	fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.09,
	    specs=[[{}], [{"secondary_y": True}]],
	    subplot_titles=("Correction to the prediction, split into two parts", "State drift from the training model"))
	fig.add_trace(go.Scatter(x=ch.index, y=ch["preprocessing"], line=dict(color=DARK_BLUE, width=1),
	    name="Preprocessing part"), row=1, col=1)
	fig.add_trace(go.Scatter(x=ch.index, y=ch["kernel"], line=dict(color=ORANGE, width=1),
	    name="Kernel part"), row=1, col=1)
	fig.add_trace(go.Scatter(x=adaptive.center_shift_.index, y=adaptive.center_shift_,
	    line=dict(color=DARK_BLUE, width=1.2), name="Centre migration"), row=2, col=1, secondary_y=False)
	fig.add_trace(go.Scatter(x=rotation.index, y=rotation, line=dict(color=ORANGE, width=1.2),
	    name="Subspace rotation"), row=2, col=1, secondary_y=True)
	# testing-data divider on the bottom panel only (the top panel is already busy)
	fig.add_vline(x=drift_month, line_color=ORANGE, line_dash="dash", row=2, col=1)
	fig.add_annotation(x=drift_month, y=11.5, text="Testing data →", showarrow=False,
	    xanchor="left", xshift=6, font=dict(color=ORANGE, size=12), row=2, col=1, secondary_y=False)
	fig.update_yaxes(title_text="Correction vs static [kPa]", range=[-25, 25], row=1, col=1)
	fig.update_yaxes(title_text="Centre migration [training SD]", row=2, col=1, secondary_y=False)
	fig.update_yaxes(title_text="Subspace rotation [components]", row=2, col=1, secondary_y=True)
	fig.update_layout(height=520, margin=dict(l=70, r=70, t=40, b=40),
	    xaxis2_title="Time since start [months]")
	fig.show()

.. figure:: ../figures/monitoring/adaptive-softsensor-decomposition.png
	:alt: Two panels: the correction to the prediction split into a large preprocessing part and a small kernel part; and the state drift, with the centre migrating several standard deviations while the subspace rotates about one component.
	:width: 900px
	:scale: 80
	:align: center

	Top: the adaptive model's departure from the static prediction, split into the
	preprocessing part (blue) and the kernel part (orange). The preprocessing part
	carries most of the correction (a median of about 4.6 kPa in size against
	0.9 kPa for the kernel part). Bottom: the state drift, with the centring vector
	migrating several standard deviations from the training data (blue, left axis)
	while the weight directions rotate by only about one of the three components
	(orange, right axis).

In this example the drift is corrected mainly by the moving centre and scale, not
by a re-aimed model. That fits the physical picture: the process moved to new
operating points, so the *level* of the tags shifted while the correlation
structure among them held, and tracking that level is what a moving centre does.
The weight directions and coefficients do change (the regression coefficients
move substantially over the series), but their net effect on the prediction
stays small. The interpretation is specific to this dataset, not a general rule;
on a process whose correlation structure itself changed, the kernel part would
carry more.

Watching the model age
^^^^^^^^^^^^^^^^^^^^^^^

The ``distance_`` metric introduced above reports how far the current model has
moved from the one it started with, in units of components: it starts at 3 (the
model is unchanged) and falls as the model adapts, reaching 1.88 by the end of
the series. It is a compact way to watch a model age, and its rate of change
helps tune the forgetting factor: a value that changes too abruptly means the
model is adapting to transient upsets rather than to genuine drift.

.. code-block:: python

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=vp["month"], y=distance, line=dict(color=DARK_BLUE, width=0.8)))
	fig.add_hline(y=A, line_color="grey", line_dash="dot", annotation_text="unchanged (= n_components)")
	fig.add_vline(x=drift_month, line_color=ORANGE, line_dash="dash")   # start of the testing data
	fig.add_annotation(x=drift_month, y=2.9, text="Testing data →", showarrow=False,
	    xanchor="left", xshift=6, font=dict(color=ORANGE, size=12))
	fig.update_layout(xaxis_title="Time since start [months]",
	    yaxis_title="Subspace overlap [components]", yaxis_range=[1.5, 3.05],
	    height=340, margin=dict(l=70, r=20, t=30, b=50))
	fig.show()

.. figure:: ../figures/monitoring/adaptive-softsensor-diagnostics.png
	:alt: The distance metric declines from 3 to about 1.88 over the series as the adaptive model ages away from its training model.
	:width: 850px
	:scale: 80
	:align: center

	The subspace-overlap distance metric ages from 3.0 (identical to the training
	model) to 1.88 as the adaptive model tracks the drift. A smooth decline
	reflects gradual adaptation; abrupt swings would flag over-fast adaptation.

.. _APPS_adaptive_choosing_settings:

Choosing the adaptation settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The settings above were not guessed. A natural way to score an on-line model is
its **one-step-ahead prediction error**: at each laboratory sample, predict with
the model as it stands from past data only, then reveal the value and let the
model learn from it. Accumulated over the series, this is an unbiased estimate of
how well the deployed sensor predicts the next value, and it penalises both
under-adaptation (a bias creeps back in) and over-adaptation (the predictions
grow noisy). To keep the score from being optimistic, the settings are chosen on
an early stretch of the series and reported on a later stretch the search never
saw, rather than on the same data used to pick them.

Not every setting is equally worth tuning, and a short **sensitivity** study
shows which ones are. Sweeping each parameter around its chosen value, one at a
time, and re-scoring the prequential RMSEP shows where the error stays flat and
where it climbs. The chosen values sit in a flat valley for every parameter (the
local slope, or *elasticity*, is near zero), so the model is not delicate about
any single value; what separates the parameters is how fast the error rises when
a value is pushed away from the valley. The sweep runs on the same tune-on-early,
report-on-late split: the model is fitted on an early tune-train block and scored
on a later inner window, with the far testing data untouched.

.. code-block:: python

	n_tune = int(0.40 * len(lab))                        # tuning study: fit on the first 40% of lab samples
	inner = np.arange(n_tune + 8, int(0.75 * len(lab)))  # score on a later inner window (never the testing data)

	def prequential(**changes):                          # leakage-free one-step-ahead RMSEP on `inner`
	    base = dict(n_components=A, forgetting_factor=0.01, gamma=0.05, lambda_center=0.003,
	                alpha_scale=0.012, lambda_center_y=0.12, alpha_scale_y=0.05)
	    m = AdaptivePLS(update_when_out_of_control=True, conf_level=0.99, **{**base, **changes})
	    m.fit(lab.iloc[:n_tune][tags], lab.iloc[:n_tune][["vapour_pressure_kpa"]])
	    pred, _, _, _ = stream(m, learn=learn, y_update=y_update)
	    return float(np.sqrt(((pred[lab_rows] - y_lab)[inner] ** 2).mean()))

	sweeps = {"n_components": [2, 3, 4, 5], "forgetting_factor": [0.003, 0.01, 0.03, 0.1],
	          "lambda_center": [0.001, 0.003, 0.01, 0.03], "gamma": [0.0, 0.05, 0.1, 0.2]}
	chosen = {"n_components": 3, "forgetting_factor": 0.01, "lambda_center": 0.003, "gamma": 0.05}
	fig = make_subplots(rows=1, cols=4, shared_yaxes=True, subplot_titles=list(sweeps))
	for col, (name, values) in enumerate(sweeps.items(), start=1):
	    rmseps = [prequential(**{name: v}) for v in values]
	    fig.add_trace(go.Scatter(x=values, y=rmseps, mode="lines+markers",
	        line=dict(color=DARK_BLUE)), row=1, col=col)
	    fig.add_vline(x=chosen[name], line_color=ORANGE, line_dash="dot", row=1, col=col)
	fig.update_xaxes(type="log", col=2)
	fig.update_xaxes(type="log", col=3)
	fig.update_layout(height=320, showlegend=False)
	fig.show()

.. figure:: ../figures/monitoring/adaptive-softsensor-sensitivity.png
	:alt: Four panels of prequential RMSEP against each tuning parameter; the forgetting factor and the centring rate rise away from the chosen value, while the number of components and gamma stay flat.
	:width: 900px
	:scale: 80
	:align: center

	Prequential one-step-ahead RMSEP on the inner validation window as each
	parameter is swept around its chosen value (orange dotted). Around the chosen
	values the error is flat for every parameter. It climbs when either of the two
	adaptation rates, the forgetting factor or the centring rate ``lambda_center``,
	is pushed too high; the number of components and ``gamma`` leave it essentially
	unchanged.

The two adaptation rates are the settings to watch. Pushing the forgetting factor
or the centring rate ``lambda_center`` too high makes the model over-react to
each observation and the error climbs; below the valley they are safe, so their
exact value within the valley matters little. The number of components has little
effect once the model adapts, because the adaptation compensates for a component
more or less. The injection strength ``gamma`` has no effect on the error at all:
it is kept small and its value is judged by the kernel's condition number, because
this dataset is rich in genuine variation and never sits quiet long enough for the
kernel to lose conditioning.

The distance metric gives a second, unsupervised check on the forgetting factor,
one that needs no laboratory value. If its trace is jagged, the model is chasing
short-term upsets rather than the slow drift, and the factor should be lowered.
Streaming the model at the chosen factor and at a ten-times-larger one makes the
difference plain:

.. code-block:: python

	jagged = AdaptivePLS(n_components=A, forgetting_factor=0.10, gamma=0.05, lambda_center=0.003,
	                     alpha_scale=0.012, lambda_center_y=0.12, alpha_scale_y=0.05,
	                     update_when_out_of_control=True, conf_level=0.99)
	jagged.fit(lab.loc[train, tags], lab.loc[train, ["vapour_pressure_kpa"]])
	_, _, _, distance_big = stream(jagged, learn=learn, y_update=y_update)

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=vp["month"], y=distance_big, line=dict(color=ORANGE, width=0.7),
	    name="forgetting_factor = 0.10 (jagged)"))
	fig.add_trace(go.Scatter(x=vp["month"], y=distance, line=dict(color=DARK_BLUE, width=0.9),
	    name="forgetting_factor = 0.01 (chosen)"))
	fig.update_layout(xaxis_title="Time since start [months]",
	    yaxis_title="Subspace overlap [components]", height=320, margin=dict(l=70, r=20, t=40, b=50))
	fig.show()

.. figure:: ../figures/monitoring/adaptive-softsensor-distance-roughness.png
	:alt: Two distance-metric traces; the chosen forgetting factor declines smoothly while the ten-times-larger one is jagged.
	:width: 850px
	:scale: 80
	:align: center

	The distance metric of the deployed model at the chosen forgetting factor
	(blue) declines smoothly as the model ages, while at a ten-times-larger factor
	(orange) it jumps from hour to hour: the model is reacting to short-term
	upsets. A jagged trace like the orange one is the signal to lower the factor.

Features or adaptation: a first-principles view
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adaptation is one way to cope with drift; better *features* are another. The
vapour pressure of a hydrocarbon stream is governed by its composition and by
temperature through the Antoine relationship, in which the logarithm of vapour
pressure varies with the inverse absolute temperature. Composition, in turn, is
reflected in temperature *differences* along the column and in flow *ratios*
such as the reflux ratio. These are quantities a linear model cannot form from
the raw tags on its own. Adding temperature differences, bounded flow ratios and
an Antoine coupling term to the 27 tags, at the same three components, lowers the
*static* model's post-drift bias from :math:`+11.1` to :math:`+9.8` kPa (RMSEP
12.6 to 11.2 kPa): the extra physics lets the fixed model extrapolate a little
further into the drifted region. Allowing cross-validation to also pick fewer
components on the richer feature set would widen the gain; the comparison at a
fixed three components isolates the effect of the features alone.

The flow ratios need care: each divides by a denominator held above a small
minimum, because a raw ratio diverges when a flow is near zero during a low-rate
period, and a single such value would distort the fit.

.. list-table:: All four models compared on the testing data (after the drift), each at three components.
	:header-rows: 1
	:widths: 40 20 20 20

	* - Model
	  - RMSEP [kPa]
	  - Bias [kPa]
	  - Variance [kPa²]
	* - Static PLS (no adaptation)
	  - 12.6
	  - :math:`+11.1`
	  - 35
	* - Static PLS + first-principles features
	  - 11.2
	  - :math:`+9.8`
	  - 31
	* - Static PLS + random features (control)
	  - 13.6
	  - :math:`+11.9`
	  - 44
	* - Adaptive PLS
	  - 8.0
	  - :math:`+1.3`
	  - 63

The first three rows are static models differing only in their features; the
last is the adaptive model, repeated from above for comparison. The three static
rows are produced by:

.. code-block:: python

	temp = [c for c in tags if c.startswith("temp_")]
	flow = [c for c in tags if c.startswith("flow_")]

	def add_physics(df):
	    F = df[tags].copy()
	    t_mean = df[temp].mean(axis=1)
	    for c in temp:                                    # temperature differences: composition proxies
	        F[c + "_dev"] = df[c] - t_mean
	    for i in range(len(flow)):                        # bounded flow ratios: reflux-ratio proxies
	        for j in range(i + 1, len(flow)):
	            denom = np.clip(np.abs(df[flow[j]]), max(1e-2, np.nanpercentile(np.abs(df[flow[j]]), 10)), None)
	            r = df[flow[i]].to_numpy() / denom.to_numpy()
	            F[f"ratio_{i}{j}"] = np.clip(r, *np.nanpercentile(r, [1, 99]))
	    p_abs = df["pres_01"] + 101.325                   # Antoine coupling: log-pressure x inverse temperature
	    F["antoine_coupling"] = np.log10(p_abs / 101.325) * df["inv_bot_temp"]
	    return F

	def add_random(df, rng):                              # control: same count of random columns
	    n_extra = add_physics(df).shape[1] - len(tags)
	    F = df[tags].copy()
	    for k in range(n_extra):
	        F[f"rand_{k}"] = rng.standard_normal(len(df))
	    return F

	train_vp = lab_rows[train]                            # vp row indices of the training lab samples
	ys = lab.loc[train, ["vapour_pressure_kpa"]].reset_index(drop=True)

	def evaluate(feature_frame):                          # fit at A = 3, score on the testing (post-drift) data
	    fit = PLS(n_components=A, scale=True).fit(feature_frame.iloc[train_vp].reset_index(drop=True), ys)
	    err = fit.predict(feature_frame).to_numpy().ravel()[lab_rows] - y_lab
	    bias, std, rmsep = bias_std_rmsep(err, post)
	    return round(rmsep, 1), round(bias, 1), round(std ** 2)

	print("static:  RMSEP / bias / variance =", evaluate(vp[tags]))
	print("physics: RMSEP / bias / variance =", evaluate(add_physics(vp)))
	print("control: RMSEP / bias / variance =", evaluate(add_random(vp, np.random.default_rng(0))))

The control row confirms that the gain comes from meaningful physics, not simply
from adding more variables: swapping the engineered features for the same number
of random columns gives a slightly *larger* testing error, not a smaller one. The
improvement follows the physics, not the fact of adding columns.

Those random columns have a second use. Because they carry no real information,
each genuine tag's Variable Importance in Projection (VIP) can be compared
against them: any real tag whose VIP sits below the random columns' VIP is
unlikely to be contributing and is a candidate to drop. On this model eight of
the 27 tags fall below that line.

.. code-block:: python

	Xr = add_random(vp, np.random.default_rng(1)).iloc[train_vp].reset_index(drop=True)
	vip = PLS(n_components=A, scale=True).fit(Xr, ys).vip()          # VIP per variable
	cutoff = max(vip.loc[c] for c in Xr.columns if c.startswith("rand_"))
	weak = [c for c in tags if vip.loc[c] < cutoff]
	print(f"{len(weak)} of {len(tags)} tags below the random-column VIP:", weak)

The same features, added to the adaptive model, make almost no difference: its
post-drift bias is already near zero. First-principles features and recursive
adaptation are, on this data, two routes to the same correction rather than
additive gains. If the model can be updated on-line, adaptation reaches further;
if it cannot, physically-grounded features recover a large part of the same
robustness. Neither route reduces the scatter: that is set by the measurement
noise, and is addressed by averaging, not by the model.

Two cautions to close with. First, holding back the updates during shutdowns and
transitions stops the model from learning off-normal operation, which would
otherwise pull it away from the operating region it is meant to track. Second, the
adaptive model follows the process, so a genuine step-change in the product and a
slow drift the operator wants to accommodate can look alike to it. The monitoring
charts on the fixed training model flag the raw event, and the distance metric
shows whether the model responded with an abrupt jump or a gradual adjustment;
together they keep that distinction visible.

Further reading
~~~~~~~~~~~~~~~~

* Luigi Fortuna, Salvatore Graziani, Alessandro Rizzo and M. Gabriella Xibilia,
  `Soft Sensors for Monitoring and Control of Industrial Processes <https://literature.learnche.org/item/111/soft-sensors-for-monitoring-and-control-of-industrial-processes>`_,
  Springer, 2007. A book-length treatment that covers the modelling, validation and deployment
  topics introduced here in much more depth.

* Petr Kadlec, Bogdan Gabrys and Sibylle Strandt,
  "`Data-driven soft sensors in the process industry <https://literature.learnche.org/item/105/data-driven-soft-sensors-in-the-process-industry>`_",
  *Computers and Chemical Engineering*, **33**, 795-814, 2009. A survey of the field, useful for
  orienting yourself in the wider literature beyond the PLS-based approach used in this section.

* Hector M. Budman, Chris Webb, Tyler R. Holcomb and Manfred Morari,
  "`Robust inferential control for a packed-bed reactor <https://literature.learnche.org/item/22/robust-inferential-control-for-a-packed-bed-reactor>`_",
  *Industrial and Engineering Chemistry Research*, **31**, 1665-1679, 1992. An early industrial
  application of inferential control, on a packed-bed reactor rather than a digester.

* Steven D. Roney,
  `Development of inferential sensors for chemical processes using partial least squares <https://literature.learnche.org/item/143/development-of-inferential-sensors-for-chemical-processes-using-partial-least-squares>`_,
  Masters thesis, McMaster University, 1998. A long-form treatment of how to build a PLS
  inferential sensor for chemical processes.
