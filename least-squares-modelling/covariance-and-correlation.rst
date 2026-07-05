
.. _LS_covariance:

Covariance
===========

.. youtube:: https://www.youtube.com/watch?v=tXOCOMtSWrc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=19

You probably have an intuitive sense for what it means when two things are correlated. We will get to correlation next, but we start by first looking at :index:`covariance`. Let's take a look at an example to formalize this, and to see how we can learn from data.

Consider the measurements from a gas cylinder; temperature (K) and pressure (kPa). We know the ideal gas law applies under moderate conditions: :math:`pV = nRT`.

	-	Fixed volume, :math:`V = 20 \times 10^{-3} \text{m}^3` = 20 L
	-	Moles of gas, :math:`n = 14.1` mols of chlorine gas, molar mass = 70.9 g/mol, so this is 1 kg of gas
	-	Gas constant, :math:`R = 8.314` J/(mol.K)

Given these numbers, we can simplify the ideal gas law to: :math:`p=\beta_1 T`, where :math:`\beta_1 = \dfrac{nR}{V} > 0`. These data are collected from sampling the system:

.. image:: ../figures/least-squares/table-of-cylinder-data.png
	:width: 900px
	:scale: 67
	:alt: Table of cylinder temperature, pressure and humidity data with means and variances

.. _LS_eqn_definition-covariance:

The formal definition for covariance between any two variables is: [terminology used here was defined :ref:`in a previous section <univariate_calculate_mean>`]

.. math::
	:label: definition-covariance

		\text{Cov}\left\{x, y\right\} = \mathcal{E}\left\{ (x - \overline{x}) (y - \overline{y})\right\} \qquad \text{where} \qquad \mathcal{E}\left\{ z \right\} = \overline{z}

Use this to calculate the covariance between temperature and pressure by breaking the problem into steps:

	-	First calculate :index:`deviation variables`. They are called this because they are now the deviations from the mean: :math:`T - \overline{T}` and :math:`p - \overline{p}`. Subtracting off the mean from each vector just centers their frame of reference to zero.

	-	Next multiply the two vectors, element-by-element, to calculate a new vector :math:`(T - \overline{T}) (p - \overline{p})`.

		.. code-block:: python

			import numpy as np

			temp = np.array([273, 285, 297, 309, 321, 333,
			                 345, 357, 369, 381])
			pres = np.array([1600, 1670, 1730, 1830, 1880,
			                 1920, 2000, 2100, 2170, 2200])
			humidity = np.array([42, 48, 45, 49, 41, 46,
			                     48, 48, 45, 49])

			temp_centered = temp - temp.mean()
			pres_centered = pres - pres.mean()
			product = temp_centered * pres_centered

			# numpy does element-by-element multiplication.
			print(product)
			# [16740 10080  5400  1440   180
			#     60  1620  5700 10920 15660]

			# Average of `product`:
			product.mean()    # 6780

			# np.cov returns the covariance matrix; the
			# off-diagonal entry [0, 1] is Cov{temp, pres}
			# (with N-1 normalisation, matching R).
			# Calculated covariance is 7533.33
			print("Covariance of temperature and "
			      "pressure is = "
			      f"{round(np.cov(temp, pres)[0, 1], 2)}")

			# The covariance of a variable with
			# itself is just the variance:
			print("Covariance with itself is = "
			      f"{round(np.cov(temp, temp)[0, 1], 2)}")
			print("while the variance = "
			      f"{round(temp.var(ddof=1), 2)}")

		.. code-block:: r

			temp <- c(273, 285, 297, 309, 321, 333,
			          345, 357, 369, 381)
			pres <- c(1600, 1670, 1730, 1830, 1880,
			          1920, 2000, 2100, 2170, 2200)
			humidity <- c(42, 48, 45, 49, 41, 46,
			              48, 48, 45, 49)

			temp.centered <- temp - mean(temp)
			pres.centered <- pres - mean(pres)
			product <- temp.centered * pres.centered

			# R does element-by-element  multiplication in the above line
			print(product)
			# [1] 16740 10080  5400  1440   180
			#        60  1620  5700 10920 15660

			# Average of 'product':
			mean(product)    # 6780

			# Calculated covariance is 7533.33
			paste0('Covariance of temperature and ',
			       'pressure is = ',
			       round(cov(temp, pres), 2))

			# The covariance of a variable with
			# itself is just the variance:
			paste0('Covariance with itself is = ',
			       round(cov(temp, temp), 2))
			paste0('while the variance = ',
			       round(var(temp), 2))

	-	The expected value of this product can be estimated by using the average, or any other suitable measure of location. In this case ``mean(product)`` in R gives 6780. This is the covariance value.

	-	More specifically, we should provide the units as well:  the covariance between temperature and pressure is 6780 [K.kPa] in this example. Similarly the covariance between temperature and humidity is 35.4 [K.%].

In your own time calculate a rough numeric value and give the units of covariance for these cases:

	========================================================== ===================================================
	:math:`x`                                                  :math:`y`
	========================================================== ===================================================
	:math:`x` = age of married partner 1                       :math:`y` = age of married partner 2
	:math:`x` = gas pressure                                   :math:`y` = gas volume at a fixed temperature
	:math:`x` = mid term mark for this course                  :math:`y` = final exam mark
	:math:`x` = hours worked per week                          :math:`y` = weekly take home pay
	:math:`x` = cigarettes smoked per month                    :math:`y` = age at death
	:math:`x` = temperature on top tray of distillation column :math:`y` = top product purity
	========================================================== ===================================================

	Also describe what an outlier observation would mean in these cases.

One last point is that the covariance of a variable with itself is the variance: :math:`\text{Cov}\left\{x, x\right\} = \mathcal{V}(x) = \mathcal{E}\left\{ (x - \overline{x}) (x - \overline{x})\right\}`, a definition :ref:`we saw earlier <univariate-variance>`.

Using the ``cov(temp, pres)`` function in R gives ``7533.333``, while we calculated 6780. The difference comes from :math:`6780 \times \dfrac{N}{N-1}= 7533.33`, indicating that R divides by :math:`N-1` rather than :math:`N`. This is because the variance function in R for a vector ``x`` is internally called as ``cov(x, x)``. Since R returns the unbiased estimate of the variance, it divides through by :math:`N-1` (the same correction :ref:`seen earlier <univariate-variance>` for the sample variance). The difference between the two conventions shrinks as :math:`N` grows, but it emphasizes that one should always read the documentation for the software being used.

Note that deviation variables are not affected by a *shift* in the raw data of :math:`x` or :math:`y`. For example, measuring temperature in Celsius or Kelvin has no effect on the covariance number; but measuring it in Celsius vs Fahrenheit does change the covariance value.

.. Another point to note: recall from geometry that the length of a vector, :math:`x`, is calculated from the sum of squares of the elements in vector :math:`x`, and then taking the square root of the sum. Mathematically the sum of squares is can be written as: math:`x^Tx`. For a vector :math:`x` that is centered, this corresponds


.. _LS_correlation:

Correlation
===========

.. youtube:: https://www.youtube.com/watch?v=tXOCOMtSWrc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=19

The variance and covariance values are units dependent. For example, you get a very different covariance when calculating it using grams vs kilograms. The :index:`correlation` on the other hand removes the effect of scaling and arbitrary unit changes. It is defined as:

.. math::
	:label: definition-correlation

		\text{Correlation}\,\,=\,\,r(x, y) = \dfrac{\mathcal{E}\left\{ (x - \overline{x}) (y - \overline{y})\right\}}{\sqrt{\mathcal{V}\left\{x\right\}\mathcal{V}\left\{y\right\}}} = \dfrac{\text{Cov}\left\{x, y\right\}}{\sqrt{\mathcal{V}\left\{x\right\}\mathcal{V}\left\{y\right\}}}

It takes the covariance value and divides through by the product of the standard deviations of :math:`x` and :math:`y`, which carry the units of :math:`x` and :math:`y`, to obtain a dimensionless result. The values of :math:`r(x,y)` range from :math:`-1` to :math:`+1`. Also note that :math:`r(x,y) = r(y,x)`.

So returning back to our example of the gas cylinder, the correlation between temperature and pressure, and temperature and humidity can be calculated now as:

.. code-block:: python

	import numpy as np

	temp = np.array([273, 285, 297, 309, 321, 333, 345,
	                 357, 369, 381])
	pres = np.array([1600, 1670, 1730, 1830, 1880, 1920,
	                 2000, 2100, 2170, 2200])
	humidity = np.array([42, 48, 45, 49, 41, 46, 48,
	                     48, 45, 49])

	# np.corrcoef returns the correlation matrix; the
	# off-diagonal entry [0, 1] is r(x, y).

	# Correlation between temperature
	# and pressure is high: 0.9968355
	np.corrcoef(temp, pres)[0, 1]

	# Correlation between temperature
	# and humidity is low: 0.3803919
	np.corrcoef(temp, humidity)[0, 1]

	# What is correlation of humidity
	# and pressure?
	np.corrcoef(___, ___)[0, 1]

.. code-block:: r

	temp <- c(273, 285, 297, 309, 321, 333, 345,
	          357, 369, 381)
	pres <- c(1600, 1670, 1730, 1830, 1880, 1920,
	          2000, 2100, 2170, 2200)
	humidity <- c(42, 48, 45, 49, 41, 46, 48,
	              48, 45, 49)

	# Correlation between temperature
	# and pressure is high: 0.9968355
	cor(temp, pres)

	# Correlation between temperature
	# and humidity is low: 0.3803919
	cor(temp, humidity)

	# What is correlation of humidity
	# and pressure?
	cor(___, ___)


Note that correlation is the same whether we measure temperature in Celsius or Kelvin. Study the plots here to get a feeling for the correlation value and its interpretation:

.. image:: ../figures/least-squares/correlation-calculation.png
	:width: 900px
	:align: center
	:scale: 65
	:alt: Example scatter plots with their correlation values


.. _LS_correlation_matrix_in_python:

Visualizing the correlation matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When working with a real data set that has many variables, looking at correlations one pair at a
time is tedious. Pandas can compute every pairwise correlation in one call with ``.corr()``, and we
can visualize the resulting matrix as a *heat map* to spot patterns at a glance.

The example below uses a `flotation cell <https://openmv.net/info/flotation-cell>`_ data set:

.. code-block:: python

	import pandas as pd

	flot = pd.read_csv("https://openmv.net/file/flotation-cell.csv")

	# A square matrix of correlation values, one
	# per pair of numeric columns:
	flot.corr()

For a wider data set, the numeric matrix becomes hard to read; a heat map encodes the same
information visually. Here we use a `distillation column
<https://openmv.net/info/distillation-tower>`_ data set, where the goal is to predict
``VapourPressure`` from process measurements:

.. code-block:: python

	import pandas as pd
	import seaborn as sns

	distill = pd.read_csv(
	    "https://openmv.net/file/distillation-tower.csv"
	)

	# Print the correlation matrix as numbers:
	display(distill.corr())

	# A diverging palette is helpful: red for
	# positive, blue for negative correlations,
	# white for near-zero.
	cmap = sns.diverging_palette(220, 10, as_cmap=True)
	sns.set(rc={"figure.figsize": (15, 15)})
	sns.heatmap(
	    distill.corr(),
	    cmap=cmap,
	    square=True,
	    linewidths=0.2,
	    cbar_kws={"shrink": 0.5},
	)

A complementary view is the *scatter plot matrix*, which shows the actual data behind each
correlation. The diagonal panels are replaced by a kernel density estimate (kde) of each variable's
distribution:

.. code-block:: python

	from pandas.plotting import scatter_matrix

	scatter_matrix(
	    distill,
	    alpha=0.2,
	    figsize=(15, 15),
	    diagonal="kde",
	)

	# For large data sets, sub-sample to speed
	# up the plot, e.g. every second row:
	scatter_matrix(
	    distill.iloc[0::2, :],
	    alpha=0.2,
	    figsize=(15, 15),
	    diagonal="kde",
	)

When the goal is to model a particular outcome variable (here ``VapourPressure``), the most useful
slice of the correlation matrix is its last row: it ranks every potential predictor by how strongly
it correlates with the outcome.

.. code-block:: python

	# The last row of the correlation matrix shows
	# how each x-variable correlates with the
	# outcome variable VapourPressure.
	distill.corr().iloc[-1, :]


.. _LS_correlation_near_zero_example:

What does a near-zero correlation look like?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The cylinder-pressure, distillation-tower and flotation-cell examples above all show *strong*
correlations. It is just as important to develop intuition for what :math:`r \approx 0` looks like
in real data. The `unlimited-time-test <https://openmv.net/info/unlimited-time-test>`_ data set is
a useful counter-example: students were given as much time as they wanted to write an open-book
exam, and we have two columns: ``Time`` taken to finish, and the ``Grade`` achieved.

.. code-block:: python

	import pandas as pd

	grades = pd.read_csv(
	    "https://openmv.net/file/unlimited-time-test.csv"
	)
	grades.plot.scatter(x="Time", y="Grade", figsize=(8, 6))

	# Correlation of -0.044 -- essentially zero.
	grades.corr()

The scatter plot shows no visible pattern, and the correlation matrix confirms it: :math:`r =
-0.044`. Two things are worth noting from this example:

	-	The correlation is *symmetric*: :math:`r(\text{Time}, \text{Grade}) = r(\text{Grade},
		\text{Time}) = -0.044`. There is no notion of an :math:`x`- or :math:`y`-variable yet.

	-	The :math:`R^2` value commonly reported with a least-squares model is just :math:`r^2`. So
		without fitting any model we already know that a straight line through these data would
		have :math:`R^2 = (-0.044)^2 \approx 0.002`. Said differently: ``Time`` would explain
		about 0.2% of the variation in ``Grade``. This is one reason :math:`R^2` on its own is a
		poor way to judge a regression model.

Compare this against the cheddar-cheese exercise in the :ref:`exercises section <LS-exercises>`
(:math:`r` around 0.5 to 0.8 between flavour and the chemical predictors), and against the
:ref:`cylinder-pressure example <LS_covariance>` where :math:`r = 0.997`. Looking at the *scatter
plots* alongside the *correlation values* for these three regimes (near-zero, moderate, near-one)
is the fastest way to develop a calibrated visual sense of what a correlation coefficient really
means.


.. TODO See article by Brillinger: John Tukey and the correlation coefficient (included as a PDF in the repo)

Some definitions
================

Be sure that you can derive (and interpret!) these relationships, which are derived from the definition of the covariance and correlation:

	-	:math:`\mathcal{E}\{x\} = \overline{x}`

	-	:math:`\mathcal{E}\{x+y\} = \mathcal{E}\{x\} + \mathcal{E}\{y\} = \overline{x} + \overline{y}`

	-	:math:`\mathcal{V}\{x\} = \mathcal{E}\{(x-\overline{x})^2\}`

	-	:math:`\mathcal{V}\{cx\} = c^2\mathcal{V}\{x\}`

	-	:math:`\text{Cov}\{x,y\} = \mathcal{E}\{(x-\overline{x})(y-\overline{y})\}` which we take as the definition for covariance

	-	:math:`\mathcal{V}\{x+x\} = 2\mathcal{V}\{x\} + 2\text{Cov}\{x,x\} = 4\mathcal{V}\{x\}`

	-	:math:`\text{Cov}\{x,y\} = \mathcal{E}\{xy\} - \mathcal{E}\{x\}\mathcal{E}\{y\}`

	-	:math:`\text{Cov}\{x,c\} = 0`

	-	:math:`\text{Cov}\{x+a, y+b\} = \text{Cov}\{x,y\}`

	-	:math:`\text{Cov}\{ax, by\} = ab \cdot \text{Cov}\{x,y\}`

	-	:math:`\mathcal{V}\{x+y\} \neq \mathcal{V}\{x\} + \mathcal{V}\{y\}`, which is counter to what might be expected.

	-	Rather:

		.. math::
			:label: eq_add_variance_2

			\mathcal{V}\{x+y\}	&= \mathcal{E}\{ \left(  x+y-\overline{x}-\overline{y} \right)^2 \}  \\
								&= \mathcal{E}\{ \left( (x-\overline{x}) + (y-\overline{y}) \right)^2 \} \\
								&= \mathcal{E}\{ (x-\overline{x})^2 + 2(x-\overline{x})(y-\overline{y}) + (y-\overline{y})^2 \}\\
								&= \mathcal{E}\{ (x-\overline{x})^2 \} + 2\mathcal{E}\{(x-\overline{x})(y-\overline{y})\} + \mathcal{E}\{(y-\overline{y})^2 \} \\
								&= \mathcal{V}\{ x \}             + 2\text{Cov}\{x,y\} + \mathcal{V}\{ y \}\\
			\mathcal{V}\{x+y\}	&= \mathcal{V}\{x\} + \mathcal{V}\{y\}, \qquad\text{only if $x$ and $y$ are uncorrelated, i.e. } \text{Cov}\{x,y\} = 0
