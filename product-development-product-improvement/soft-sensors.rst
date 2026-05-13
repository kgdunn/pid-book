.. _APPS_soft_sensors:

Soft sensors and inferential sensors
=====================================

.. index::
	single: soft sensors
	single: inferential sensors
	pair: soft sensors; applications

A soft sensor (also called an inferential sensor) is a model that infers a quality variable from
the cheap, real-time process measurements you already have. We met the idea in passing back in
:ref:`the latent-variable applications section <LVM_inferential_sensors>`. This section is the
worked example, on a Kamyr digester where the quality variable is the Kappa number and the only
real source of it is a lab measurement that arrives hours late.

.. _APPS_soft_sensors_monitoring_recap:

Recap: what process monitoring did, and where it falls short
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When we talked about :ref:`process monitoring <SECTION-process-monitoring>` in the earlier chapter,
the workflow was: build a chart on a stretch of stable historical data
(:ref:`phase 1 <monitoring_general_approach>`), then run it live on new data to flag unusual
variability (:ref:`phase 2 <monitoring_general_approach>`) so a human can decide whether to
intervene. We were careful to say that
:ref:`monitoring is not feedback control <monitoring_is_not_feedback_control>`: the adjustments are
infrequent, manual, and only made when special causes are detected.

That whole story rests on a quiet assumption -- that the variable you want to watch is *available*
to watch. Most of the time it is: a temperature, a flow rate, a pressure, an on-line composition
analyser are all sitting on the data historian, refreshed every few seconds. The problem comes when
the variable that *actually matters to the customer* only gets measured in the lab, hours after the
material has already moved downstream. You cannot react early to something you only learn about
late, and you certainly cannot monitor a chart that updates four times a week.

This is exactly where the soft sensor earns its keep. We build a model from a stretch of historical
data that pairs the slow lab values with the fast process tags that were collected alongside them.
Once that model is in place, we infer the lab variable in real-time from the process tags, and
monitor *that* prediction. The same phase 1 and phase 2 discipline still applies; what changes is
that the quantity being charted is now a calculated quantity, exactly as we discussed when we
asked :ref:`what should we monitor <SECTION-process-monitoring>` -- the calculation just happens to
be a multivariate regression rather than an energy balance.

.. _APPS_soft_sensors_case_kamyr:

Case study: predicting Kappa number on a Kamyr digester
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A continuous Kamyr digester cooks wood chips under pressure in white-liquor to dissolve the lignin
that binds the cellulose fibres together. The amount of lignin that remains in the pulp is summarised
by a single number, the :index:`Kappa number`. A high Kappa number means lots of residual lignin and
a brown, paperboard-grade pulp; a low Kappa number means the cook is closer to a bleachable grade.
Either way, holding the Kappa number on target while keeping its variability small is what the mill
gets paid for.

The Kappa number is a lab measurement. Even in a well-instrumented mill the sample has to be taken,
transported, prepared, and titrated; the whole loop can easily run three hours, and at smaller mills
the analysis only happens on day shift. By the time the lab calls back, you have already produced
several cubic metres of pulp at the wrong setting. Feedback control on Kappa is therefore not
practical, and a monitoring chart on Kappa shows the problem long after the operator could have
done anything about it.

The data we use here is the public subset of one such mill in Alberta that ships with
``process-improve`` at ``process_improve/datasets/multivariate/kamyr.csv``. Each row is an hourly
snapshot. There are nine process tags in the :math:`\mathbf{X}` block and the Kappa number in
:math:`\mathbf{y}`; the lab returned a value for only 52 of the 96 hours, which is realistic for a
once-per-shift assay. Two of the columns -- ``ChipLevel-4`` and ``BlackFlow-2`` -- have already
been shifted in time so that the row of process data lines up with the Kappa number it eventually
produces. The lag of four hours on chip level and two hours on black-liquor flow are
residence-time estimates from the operators; they let us build a model on aligned rows without
having to do the alignment ourselves.

.. figure:: ../figures/monitoring/Kappa-soft-sensor-raw-data.png
	:alt: Raw Kappa number and two of the lagged process tags plotted against sample number.
	:width: 750px
	:scale: 90
	:align: center

	The Kappa number drifts slowly between roughly 29 and 32, on a clear weekly rhythm. The two
	lagged process tags shown underneath move on the same time-scale, which is what we want from a
	soft-sensor: the inputs should carry the information that drives the output.

.. _APPS_soft_sensors_building_model:

Building the soft sensor
~~~~~~~~~~~~~~~~~~~~~~~~

We will build the model with PLS, treating Kappa as the single :math:`y`-variable and the nine
process tags as the :math:`\mathbf{X}` block. The ``process-improve`` package gives us a ``PLS``
class and the ``MCUVScaler`` that we should always reach for first, because PLS scores and loadings
are only interpretable after we have centred each variable and scaled it to unit standard deviation.

.. code-block:: python

	import pandas as pd
	from process_improve.multivariate import PLS, MCUVScaler

	# 9 X columns + Y-Kappa. Two X columns are already lagged in the source data.
	X_COLS = [
		"ChipRate", "BlackFlow", "ChipLevel-4", "T-upper-Ext-2", "T-lower-Ext-2",
		"UCZAA", "WhiteFlow-L", "AAWhiteFlow", "BlackFlow-2",
	]
	Y_COL = "Y-Kappa"

	df = pd.read_csv(
		"process_improve/datasets/multivariate/kamyr.csv",
		header=None,
		names=X_COLS + [Y_COL],
	)
	df = df.dropna(subset=[Y_COL]).fillna(df.median(numeric_only=True))

	X, y = df[X_COLS], df[[Y_COL]]
	scaler_x = MCUVScaler().fit(X)
	scaler_y = MCUVScaler().fit(y)

	model = PLS(n_components=2).fit(scaler_x.transform(X), scaler_y.transform(y))

After fitting we go straight to the cumulative :math:`R^2_Y` to see whether two components are even
worth looking at:

.. code-block:: python

	>>> model.r2_cumulative_.values
	array([0.411, 0.531])

A single latent variable already accounts for 41 % of the Kappa variability and the second adds
another 12 %. That is not a brilliant model -- on a well-instrumented mill with the *full* set of
tags one would aim for the high seventies -- but it is comfortably enough signal to be useful, and
on a subset of nine tags it is more or less what we should expect.

The regression coefficients show *which* tags carry that signal:

.. figure:: ../figures/monitoring/Kappa-soft-sensor-coefficients.png
	:alt: Bar chart of PLS regression coefficients onto Y-Kappa for the nine process tags.
	:width: 750px
	:scale: 80
	:align: center

	Coefficients are on the scaled :math:`\mathbf{X}`, so the bar heights are directly comparable.
	``UCZAA``, ``T-upper-Ext-2``, ``AAWhiteFlow`` and ``ChipLevel-4`` carry most of the model.

The signs are also consistent with the chemistry: a higher temperature in the upper extraction zone
and a higher active-alkali charge both lift the rate of delignification and pull the Kappa number
down. The model is *correlation*, not causation, but the coefficients line up with what the
operators would tell us if we walked into the control room.

To know whether this thing will work as a live soft sensor we have to test it on data the model has
never seen. We split the 52 rows chronologically -- the first 70 % to train, the last 30 % to test
-- and report the root-mean-square error of prediction (RMSEP) on the held-out tail:

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

	rmsep_base, _ = evaluate_split(df, X_COLS, Y_COL)
	print(f"RMSEP (process tags only): {rmsep_base:.2f} Kappa units")

.. figure:: ../figures/monitoring/Kappa-soft-sensor-obs-pred-base.png
	:alt: Predicted vs observed Kappa number on the held-out test set with the process-tag model.
	:width: 600px
	:scale: 80
	:align: center

	Observed-vs-predicted Kappa on the held-out tail of the dataset, using only the nine process
	tags. The model lands within roughly 1.7 Kappa units (RMSEP = 1.66), but the points hug the
	ideal line less tightly than we would like for a charting application.

An RMSEP of 1.66 on a process where the Kappa number varies by about three units is not great --
the signal-to-noise ratio of the soft sensor would only be borderline useful on a chart. The fix is
the trick that practical soft sensors lean on almost always: feed the *previous* lab value back to
the model as an extra input. Whenever the lab returns a result we keep it, and we use it as a
one-step memory until the next result arrives.

.. code-block:: python

	df_lag = df.copy()
	df_lag["Kappa_lag1"] = df_lag[Y_COL].shift(1)
	df_lag = df_lag.dropna(subset=["Kappa_lag1"]).reset_index(drop=True)

	rmsep_lag, _ = evaluate_split(df_lag, X_COLS + ["Kappa_lag1"], Y_COL)
	print(f"RMSEP (with one-step Kappa lag): {rmsep_lag:.2f} Kappa units")

.. figure:: ../figures/monitoring/Kappa-soft-sensor-obs-pred-lagged.png
	:alt: Predicted vs observed Kappa with one-step Kappa lag in X.
	:width: 600px
	:scale: 80
	:align: center

	Adding the previous Kappa value as a tenth predictor brings RMSEP down to 1.28 -- a 23 %
	improvement over the process-tags-only model, with no change to the underlying data
	infrastructure.

.. note::

	The interpretation of the soft-sensor coefficients is correlation, not causation. They are a
	helpful prompt for a discussion with the operators about what is driving the variability they
	are seeing, but they are not a substitute for the conversation. Pair the model with the process
	knowledge.

In production we would deploy this exactly as we built it. The model lives in the same
phase 1 / phase 2 split as any other monitoring artefact: we fit on a representative stretch of
historical operation, we test it on a held-out tail, and once we are comfortable that the RMSEP is
small enough relative to the Kappa-number spec, we wire the prediction into the same SPC chart we
would have used on the lab value itself. The chart now updates every hour instead of every shift,
and any out-of-target deviation that develops over a few hours is visible to the operator while
there is still time to do something about it.

There are two refinements worth mentioning before moving on. First, the model decays: chip species,
mill upsets, and seasonal raw-material drift will all pull the relationship between
:math:`\mathbf{X}` and Kappa away from where we fit it, and a soft sensor that is never re-fit will
eventually start charting noise. The pragmatic fix is to refit on a rolling window of the last few
hundred lab values. Second, the same dataset has a strong autocorrelation in :math:`y` itself: we
exploited that crudely with the one-step lag here, but adding two or three lags of both :math:`y`
and the most influential :math:`x` variables typically buys another fraction of the variance.

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
