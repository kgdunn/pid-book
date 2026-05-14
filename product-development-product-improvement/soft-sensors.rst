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
<https://literature.learnche.org/item/17/development-of-inferential-process-models-using-pls>`_;
the general idea was touched on in :ref:`an earlier section <LVM_inferential_sensors>`. This
section is a worked example: predicting the Kappa number on a continuous Kamyr pulp digester,
where the Kappa number is reported less often, and with more delay, than the process tags
around it.

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

	import matplotlib.pyplot as plt
	import numpy as np
	import pandas as pd
	from process_improve.multivariate import PLS, MCUVScaler

	digester = pd.read_csv("https://openmv.net/file/kamyr-digester.csv")
	digester.columns = [c.strip() for c in digester.columns]
	digester = digester.drop(columns=["Observation", "AAWhiteSt-4", "SulphidityL-4"])
	digester = digester.fillna(digester.median(numeric_only=True))

	fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
	sample = np.arange(len(digester))
	axes[0].plot(sample, digester["Y-Kappa"], "k-", linewidth=1.0)
	axes[0].set_ylabel("Y-Kappa")
	axes[1].plot(sample, digester["ChipLevel4"], "C0-", linewidth=1.0)
	axes[1].set_ylabel("ChipLevel4")
	axes[2].plot(sample, digester["BlackFlow-2"], "C3-", linewidth=1.0)
	axes[2].set_ylabel("BlackFlow-2")
	axes[2].set_xlabel("Sample (1 hour spacing)")
	for ax in axes:
		ax.grid(True, alpha=0.3)
	fig.tight_layout()
	plt.show()

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
	fig, ax = plt.subplots(figsize=(11, 4.8))
	ax.bar(coefs.index, coefs.values, color=["C0" if c >= 0 else "C3" for c in coefs.values])
	ax.axhline(0, color="k", linewidth=0.6)
	ax.set_ylabel("Coefficient on scaled X")
	plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
	ax.grid(True, axis="y", alpha=0.3)
	fig.tight_layout()
	plt.show()

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
		fig, ax = plt.subplots(figsize=(7.5, 6))
		lo = float(min(y_obs.min(), y_hat.min()))
		hi = float(max(y_obs.max(), y_hat.max()))
		pad = 0.05 * (hi - lo)
		ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], "k--", linewidth=0.8, label="ideal")
		ax.plot(y_obs, y_hat, "o", markersize=6, alpha=0.8)
		ax.set_xlabel("Observed Kappa")
		ax.set_ylabel("Predicted Kappa")
		ax.set_title(title)
		ax.grid(True, alpha=0.3)
		ax.legend(loc="upper left")
		ax.set_aspect("equal", adjustable="box")
		fig.tight_layout()
		plt.show()

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

	fig, ax = plt.subplots(figsize=(11, 4.8))
	sample = np.arange(len(y_obs_base))
	ax.plot(sample, y_obs_base, color="black", linewidth=1.8, label="Lab (actual)")
	ax.plot(sample, y_hat_base, color="C0", linestyle="--", linewidth=1.4,
		marker="o", markersize=4, label="Soft sensor: process tags only")
	ax.plot(sample[-len(y_hat_lag):], y_hat_lag, color="C3", linestyle=":", linewidth=1.4,
		marker="s", markersize=4, label="Soft sensor: process tags + Kappa lag")
	ax.set_xlabel("Test sample index (1 hour spacing)")
	ax.set_ylabel("Kappa number")
	ax.grid(True, alpha=0.3)
	ax.legend(loc="best")
	fig.tight_layout()
	plt.show()

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
