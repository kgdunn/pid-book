.. _APPS_soft_sensors:

Soft sensors and inferential sensors
=====================================

.. index::
	single: soft sensors
	single: inferential sensors
	pair: soft sensors; applications

A soft sensor (also called an inferential sensor) infers a hard-to-measure quality variable from
cheap, real-time process measurements that are already on the data historian. The general idea
was introduced in :ref:`an earlier section <LVM_inferential_sensors>`. This section is a worked
example: predicting the Kappa number on a continuous Kamyr pulp digester, where the Kappa number
is a lab measurement that arrives several hours after the pulp it describes was made.

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
quality property that arrives several hours, sometimes a full shift, after the material it
describes was made. A monitoring chart on such a variable shows the problem long after it
happened, and corrective action is no longer possible without scrapping or reworking the
intermediate product.

A soft sensor solves this problem by inferring the lab value in real-time from the process tags
that are available at that moment. The model is built on historical data where both the process
tags and the lab values were collected; once it has been validated the prediction is used in
place of the lab value on the monitoring chart, on the on-line trend, or in a feedback loop. The
phase 1 and phase 2 requirements still apply: the model is fit on a representative stretch of
data, then tested on data it has not seen before it is deployed.

.. _APPS_soft_sensors_case_kamyr:

Case study: predicting Kappa number on a Kamyr digester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A continuous Kamyr digester cooks wood chips under pressure in white-liquor to dissolve the lignin
that binds the cellulose fibres. The amount of lignin that remains in the pulp is summarised by a
single quality number, the :index:`Kappa number`. A high Kappa number indicates a brown,
paperboard-grade pulp; a low Kappa number indicates a pulp that is closer to a bleachable grade.
The mill aims to hold the Kappa number on target with as little variability as possible.

The Kappa number is a wet-chemistry lab measurement. The sample must be taken, transported,
prepared and titrated; the whole loop runs about three hours, and in many mills the analysis is
only performed once per shift. Feedback control on the Kappa number is therefore not practical,
and a monitoring chart on the Kappa number shows the problem long after the operator could have
adjusted the process. This is the situation a soft sensor is designed for.

The data set used here is the `Kamyr digester data <https://openmv.net/info/kamyr-digester>`_
from openmv.net, an hourly record of nine process tags and the Kappa number for a kraft mill in
Alberta. Two of the process columns, ``ChipLevel-4`` and ``BlackFlow-2``, have already been
shifted in time so that the row of process data lines up with the Kappa number that the lab will
eventually report; the lag of 4 hours on the chip level and 2 hours on the black-liquor flow are
residence-time estimates from the mill. The lab returned a Kappa value for 52 of the 96 hourly
samples; the remaining rows have a missing Kappa.

.. figure:: ../figures/monitoring/Kappa-soft-sensor-raw-data.png
	:alt: Raw Kappa number and two of the lagged process tags plotted against sample number.
	:width: 750px
	:scale: 90
	:align: center

	The Kappa number in the top panel covers a range of about 3 units, and is missing on roughly
	half of the samples. The two lagged process tags shown underneath are sampled every hour and
	provide the real-time information that the soft sensor uses.

.. _APPS_soft_sensors_building_model:

Building the soft sensor
~~~~~~~~~~~~~~~~~~~~~~~~

We build the model with PLS, using the Kappa number as the :math:`y`-variable and the nine
process tags as the :math:`\mathbf{X}` block. The ``process-improve`` package provides a ``PLS``
class and an ``MCUVScaler`` for centring and scaling. The data are centred to zero mean and
scaled to unit standard deviation before fitting: PLS scores and loadings are only interpretable
in that form.

.. code-block:: python

	import pandas as pd
	from process_improve.multivariate import PLS, MCUVScaler

	digester = pd.read_csv("https://openmv.net/file/kamyr-digester.csv")
	digester = (
		digester.dropna(subset=["Y-Kappa"])
		        .fillna(digester.median(numeric_only=True))
	)

	X_COLS = [
		"ChipRate", "BlackFlow", "ChipLevel-4", "T-upper-Ext-2", "T-lower-Ext-2",
		"UCZAA", "WhiteFlow-L", "AAWhiteFlow", "BlackFlow-2",
	]
	X, y = digester[X_COLS], digester[["Y-Kappa"]]

	scaler_x = MCUVScaler().fit(X)
	scaler_y = MCUVScaler().fit(y)

	model = PLS(n_components=2).fit(scaler_x.transform(X), scaler_y.transform(y))

The cumulative :math:`R^2_Y` measures how much of the Kappa variability the model accounts for as
each latent variable is added:

.. code-block:: python

	>>> model.r2_cumulative_.values
	array([0.411, 0.531])

The first component picks up 41% of the Kappa variability, and the second adds another 12%, for a
cumulative 53%. This is not a high-:math:`R^2_Y` model in absolute terms; the number of process
tags in this public subset is the limiting factor. Even so, the signal is enough for the model
to be useful as a soft sensor, as we will see when we evaluate it on held-out data below.

The regression coefficients show which tags drive the model:

.. figure:: ../figures/monitoring/Kappa-soft-sensor-coefficients.png
	:alt: Bar chart of PLS regression coefficients onto Y-Kappa for the nine process tags.
	:width: 750px
	:scale: 80
	:align: center

	PLS regression coefficients on the centred and scaled :math:`\mathbf{X}`. The bar heights are
	directly comparable. ``UCZAA``, ``T-upper-Ext-2``, ``AAWhiteFlow`` and ``ChipLevel-4`` carry
	most of the relationship to ``Y-Kappa``.

The signs match what is known about the chemistry of the cook: a higher temperature in the upper
extraction zone or a higher active-alkali charge both increase the rate of delignification and
reduce the Kappa number. The coefficients are a correlation, not a causation, but they agree
with what a process engineer would predict from first principles.

The cumulative :math:`R^2_Y` reports the fit on the data we trained on. To know whether the model
will be useful as a live soft sensor we have to evaluate it on data it has never seen. We split
the 52 rows in time order: the first 70% for training, the last 30% as a held-out test set, and
we report the root-mean-square error of prediction (RMSEP) on the test set:

.. code-block:: python

	import numpy as np

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
		return float(np.sqrt(np.mean((test[y_col].values - y_hat) ** 2))), y_hat

	rmsep_base, _ = evaluate_split(digester, X_COLS, "Y-Kappa")
	print(f"RMSEP (process tags only): {rmsep_base:.2f} Kappa units")

.. figure:: ../figures/monitoring/Kappa-soft-sensor-obs-pred-base.png
	:alt: Predicted vs observed Kappa number on the held-out test set with the process-tag model.
	:width: 600px
	:scale: 80
	:align: center

	Predicted *vs* observed Kappa number on the held-out test set, using only the nine process
	tags. The RMSEP is 1.66 Kappa units; the points scatter around the ideal line but are not
	tightly aligned.

An RMSEP of 1.66 Kappa units is large compared to the 3 Kappa unit range of the historical data,
and a soft sensor with this much error would be of limited use on a monitoring chart. A standard
improvement is to add the previous Kappa value as another predictor: each time the lab returns a
value we keep it as a one-step memory and feed it back into :math:`\mathbf{X}` until the next lab
value arrives. We add a column ``Kappa_lag1`` to the data, drop the first row (which has no
previous Kappa), and re-fit:

.. code-block:: python

	df_lag = digester.copy()
	df_lag["Kappa_lag1"] = df_lag["Y-Kappa"].shift(1)
	df_lag = df_lag.dropna(subset=["Kappa_lag1"]).reset_index(drop=True)

	rmsep_lag, _ = evaluate_split(df_lag, X_COLS + ["Kappa_lag1"], "Y-Kappa")
	print(f"RMSEP (with one-step Kappa lag): {rmsep_lag:.2f} Kappa units")

.. figure:: ../figures/monitoring/Kappa-soft-sensor-obs-pred-lagged.png
	:alt: Predicted vs observed Kappa with one-step Kappa lag in X.
	:width: 600px
	:scale: 80
	:align: center

	Adding the previous Kappa value as a tenth predictor reduces the RMSEP from 1.66 to 1.28
	Kappa units, an improvement of about 23% on the same underlying data.

.. note::

	The PLS coefficients are a measure of correlation, not causation. They are useful as a
	starting point for a discussion with the operators about what is driving the variability in
	the process, but they should not be interpreted as a cause-and-effect statement on their own.

This soft sensor can now be deployed in the same way as any other monitoring artefact: the model
is fit on a representative stretch of historical operation, tested on a held-out tail, and once
the RMSEP is small enough compared to the Kappa specification limits, the prediction is wired
into the same chart that would have been used for the lab value. The chart now updates every hour
rather than once per shift.

Two refinements are worth noting. First, the relationship between :math:`\mathbf{X}` and the
Kappa number changes over time, with chip species, mill upsets and seasonal raw-material
variation. A soft sensor that is never re-fit will gradually lose accuracy. The standard practice
is to re-fit the model on a rolling window of the most recent lab values. Second, the Kappa
number is autocorrelated in time: we exploited this with a single one-step lag of :math:`y`
above, but adding lags of two or three hours, and lags on the most influential :math:`x`
variables, typically reduces the prediction error further.

References
~~~~~~~~~~~

**Foundational and review papers**

* James V. Kresta, Thomas E. Marlin and John F. MacGregor, "`Development of inferential process
  models using PLS <https://literature.learnche.org/item/17/development-of-inferential-process-models-using-pls>`_",
  *Computers and Chemical Engineering*, **18**, 597-611, 1994.

* Luigi Fortuna, Salvatore Graziani, Alessandro Rizzo and M. Gabriella Xibilia,
  `Soft Sensors for Monitoring and Control of Industrial Processes <https://literature.learnche.org/item/111/soft-sensors-for-monitoring-and-control-of-industrial-processes>`_,
  Springer, 2007.

* Petr Kadlec, Bogdan Gabrys and Sibylle Strandt,
  "`Data-driven soft sensors in the process industry <https://literature.learnche.org/item/105/data-driven-soft-sensors-in-the-process-industry>`_",
  *Computers and Chemical Engineering*, **33**, 795-814, 2009.

* Petr Kadlec, Ratko Grbić and Bogdan Gabrys,
  "`Review of adaptation mechanisms for data-driven soft sensors <https://literature.learnche.org/item/106/review-of-adaptation-mechanisms-for-data-driven-soft-sensors>`_",
  *Computers and Chemical Engineering*, **35**, 1-24, 2011.

* Bao Lin, Bodil Recke, Jørgen K. H. Knudsen and Sten Bay Jørgensen,
  "`A systematic approach for soft sensor development <https://literature.learnche.org/item/107/a-systematic-approach-for-soft-sensor-development>`_",
  *Computers and Chemical Engineering*, **31**, 419-425, 2007.

**Industrial applications and case studies**

* Hector M. Budman, Chris Webb, Tyler R. Holcomb and Manfred Morari,
  "`Robust inferential control for a packed-bed reactor <https://literature.learnche.org/item/22/robust-inferential-control-for-a-packed-bed-reactor>`_",
  *Industrial and Engineering Chemistry Research*, **31**, 1665-1679, 1992.

* Bhupinder S. Dayal, John F. MacGregor, Paul A. Taylor, R. Kildaw and S. Marcikic,
  "`Application of feedforward neural networks and partial least squares regression to modelling
  Kappa number in a continuous Kamyr digester <https://literature.learnche.org/item/124/application-of-feedforward-neural-networks-and-partial-least-squares-regression-to-modelling-kappa-number-in-a-continuous-kamyr-digester>`_",
  *Pulp and Paper Canada*, **95**, T7-T13, 1994.

* Vasiliki Tzovla and Ashish Mehta,
  "`Creating intelligence: Automating the approach to development and online operation of soft sensors <https://literature.learnche.org/item/103/creating-intelligence-automating-the-approach-to-development-and-online-operation-of-soft-sensors>`_",
  *InTech*, September, 30-33, 2002.

**Theses**

* Steven D. Roney,
  `Development of inferential sensors for chemical processes using partial least squares <https://literature.learnche.org/item/143/development-of-inferential-sensors-for-chemical-processes-using-partial-least-squares>`_,
  Masters thesis, McMaster University, 1998.
