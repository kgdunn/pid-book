Least squares models with a single x-variable
======================================================

.. index::
	pair:	derivation; least squares
	pair:	slope; least squares
	pair:	intercept; least squares
	single: ordinary least squares (OLS)
	see:    OLS; ordinary least squares (OLS)
	see:    predicted value; fitted value

The general linear least squares model is a very useful tool (in the right circumstances), and it is the workhorse for a number of algorithms in data analysis.

This part covers the relationship between two variables only: :math:`x` and :math:`y`. In a :ref:`later part on general least squares <LS_multiple_X_MLR>` we will consider more than two variables and use matrix notation. But we start off slowly here, looking first at the details for relating two variables.

We will follow these steps:

#.	Model definition (this subsection)

#.	Building the model

#.	Interpretation of the model parameters and model outputs (coefficients, :math:`R^2`, and standard error :math:`S_E`)

#.	Consider the effect of unusual and influential data

#.	Assessment of model residuals

The least squares model postulates that there is a linear relationship between measurements in vector :math:`x` and vector :math:`y` of the form:

.. math::
	:label: define-2-LS

		\mathcal{E}\left\{\mathrm{y}\right\} &= \beta_0 + \beta_1 \mathrm{x} \\
		\mathrm{y} &= \beta_0 + \beta_1 \mathrm{x} + \epsilon

The :math:`\beta_0`, :math:`\beta_1` and :math:`\epsilon` terms are *population* parameters, which are unknown (see the :ref:`section on univariate statistics <univariate-population>`). The :math:`\epsilon` term represents any unmodelled components of the linear model, measurement error, and is simply called *the error* term. Notice that the error is not due to :math:`x`, but is the error in fitting :math:`y`; we will return to this point in the section on :ref:`least squares assumptions <LS-assumptions>`. Also, if there is no relationship between :math:`x` and :math:`y` then :math:`\beta_1 = 0`.

We develop **the least squares method** to estimate these parameters; these estimates are defined as :math:`b_0 = \hat{\beta_0}`, :math:`b_1 = \hat{\beta_1}` and :math:`e = \hat{\epsilon}`. Using this new nomenclature we can write, for a given observation :math:`i`:

.. math::
	:label: define-2-LS-i

		y_i &= b_0 + b_1 x_i + e_i \\
		\hat{y}_i &= b_0 + b_1 x_i

.. image:: ../figures/least-squares/least-squares-picture.png
	:width: 600px
	:align: center
	:scale: 65
	:alt: A least squares line with an observed value, its fitted value and the residual labelled

Presuming we have calculated estimates |b0| and |b1| we can use the model with a new x-observation, :math:`x_i`, and predict its corresponding :math:`\hat{y}_i`. The error value, :math:`e_i`, is generally non-zero, indicating our prediction estimate of :math:`\hat{y}_i` is not exact. All this new nomenclature is illustrated in the figure.

Minimizing errors as an objective
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=8d_pbx4vnsI&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=20

Our immediate aim however is to calculate the |b0| and |b1| estimates from the :math:`n` pairs of data collected: :math:`(x_i, y_i)`.

Here are some valid approaches, usually called objective functions for making the :math:`e_i\,` values small. One could use:

 	#.	:math:`\sum_{i=1}^{n}{(e_i)^2}`, which leads to the least squares model
	#.	:math:`\sum_{i=1}^{n}{(e_i)^4}`
	#.	sum of perpendicular distances to the line :math:`y = b_0 + b_1 x`
	#.	:math:`\sum_{i=1}^{n}{|e_i|}`, known as the least absolute deviations model, or the :math:`l`-1 norm problem
	#.	*least median of squared error* model, which is a robust form of least squares that is far less sensitive to outliers.

The traditional least squares model, the first objective function listed, has the lowest variance for |b0| and |b1| among all estimators that are linear in the :math:`y`-values and unbiased, provided certain additional :ref:`assumptions are met <LS-assumptions>` (this result is known as the Gauss-Markov theorem). The low variance of these parameter estimates is very desirable, for both model interpretation and using the model. The other objective functions are good alternatives and may be useful in many situations, particularly the last alternative.

Other reasons for so much focus on the least squares alternative is because it is computationally tractable by hand and very fast on computers, and it is easy to prove various mathematical properties. The other forms take much longer to calculate, almost always have to be done on a computer, may have multiple solutions, the solutions can change dramatically given small deviations in the data (unstable, high variance solutions), and the mathematical proofs are difficult. Also the interpretation of the least squares objective function is suitable in many situations: it penalizes deviations quadratically; i.e. large deviations much more than the smaller deviations.

You can read more about least squares alternatives in the book by Birkes and Dodge: "Alternative Methods of Regression".

Solving the least squares problem and interpreting the model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Having settled on the least squares objective function, let's construct the problem as an optimization problem and understand its characteristics.

The least squares problem can be posed as an :index:`unconstrained optimization` problem:

.. math::
	:label: define-2-LS-optimization

		\min_{\displaystyle b_0, b_1} f(b_0, b_1) &= \sum_{i=1}^{n}{(e_i)^2} \\
												  &= \sum_{i=1}^{n}{\left(y_i - b_0 - b_1 x_i\right)^2}

Returning to our example of the gas cylinder. In this case we know that :math:`\beta_0 = 0` from theoretical principles. So we can solve the above problem by trial and error for |b1|. We expect :math:`b_1 \approx \beta_1 = \dfrac{nR}{V} = \dfrac{(14.1 \text{~mol})(8.314 \text{~J/(mol.K)})}{20 \times 10^{-3} \text{m}^3} = 5.861 \text{~kPa/K}`. So construct equally spaced points of :math:`5.0 \leq b_1 \leq 6.5`, set :math:`b_0 = 0`. Then calculate the objective function using the :math:`(x_i, y_i)` data points recorded earlier using :eq:`define-2-LS-optimization`.

.. image:: ../figures/least-squares/cylinder-case-study-objective.png
	:align: left
	:scale: 40
	:width: 900px
	:alt: Least squares objective function values from a grid search over the slope coefficient

We find our best estimate for :math:`b_1` roughly at 5.88, the minimum of our grid search, which is very close to the theoretically expected value of 5.86 kPa/K.

For the case where we have both |b0| and |b1|  varying we can construct a grid and tabulate the objective function values at all points on the grid. The least squares objective function is shaped like a bowl for these cases, and a unique minimum will be found as long as there is variation in the :math:`x`-data, because the objective function is :index:`convex <pair: convex optimization; least squares>`.

.. image:: ../figures/least-squares/least-squares-objective-function-annotated.png
	:width: 750px
	:align: left
	:scale: 45

The above figure shows the general nature of the :index:`least-squares objective function <pair: objective function; least squares>` where the two horizontal axes are for |b0| and |b1|, while the vertical axis represents the least squares objective function :math:`f(b_0, b_1)`.

The illustration highlights the quadratic nature of the objective function. To find the minimum analytically we start with equation :eq:`define-2-LS-optimization` and take partial derivatives with respect to :math:`b_0` and :math:`b_1`, and set those equations to zero. This is a required condition at any optimal point (see a reference on optimization theory), and leads to 2 equations in 2 unknowns.

.. math::
	:label: define-2-LS-b0-b1-partials

	\dfrac{\partial f(b_0, b_1)}{\partial{b_0}} &= -2 \sum_i^{n}{(y_i -  b_0 - b_1 x_i)} = 0 \\
 	\dfrac{\partial f(b_0, b_1)}{\partial{b_1}} &= -2 \sum_i^{n}{(x_i)(y_i -  b_0 - b_1 x_i)} = 0\\

Now divide the first line through by :math:`n` (the number of data pairs we are using to estimate the parameters) and solve that equation for |b0|. Then substitute that into the second line to solve for |b1|. From this we obtain the parameters that provide the least squares optimum for :math:`f(b_0, b_1)`:

.. _LS_eqn_define-2-LS-b0-b1-result:
.. math::
	:label: define-2-LS-b0-b1-result

	b_0 &= \overline{\mathrm{y}} - b_1\overline{\mathrm{x}} \\
	b_1 &= \dfrac{ \sum_i{\left(x_i - \overline{\mathrm{x}}\right)\left(y_i - \overline{\mathrm{y}}\right) } }{ \sum_i{\left( x_i - \overline{\mathrm{x}}\right)^2} }


**Verify for yourself that**:

#.	The first part of equation :eq:`define-2-LS-b0-b1-partials` shows :math:`\sum_i{e_i} = 0`, also implying the average error is zero.

#.	The first part of equation :eq:`define-2-LS-b0-b1-result` shows that the straight line equation passes through the mean of the data :math:`(\overline{\mathrm{x}}, \overline{\mathrm{y}})` without error.

#.	From second part of equation :eq:`define-2-LS-b0-b1-partials` prove to yourself that :math:`\sum_i{(x_i e_i)} = 0`, just another way of saying the dot product of the :math:`x`-data and the error, :math:`x^Te`, is zero.

#.	Also prove and *interpret* that :math:`\sum_i{(\hat{y}_i e_i)} = 0`, the dot product of the predictions and the errors is zero.

#.	Notice that the parameter estimate for |b0| depends on the value of |b1|: we say the estimates are correlated - you cannot estimate them independently.

#.	You can also compute the second derivative of the objective function to confirm that the optimum is indeed a minimum.

**Remarks**:

#.	What units does parameter estimate :math:`b_1` have?

	-	The units of :math:`y` divided by the units of :math:`x`.

#.	Recall the :ref:`temperature and pressure example <LS_covariance>`: let  :math:`\hat{p}_i = b_0 + b_1 T_i`:

	#.	What is the interpretation of coefficient :math:`b_1`?

		-	A one Kelvin increase in temperature is associated, on average, with an increase of :math:`b_1` kPa in pressure.

	#.	What is the interpretation of coefficient :math:`b_0`?

		-	It is the expected pressure when temperature is zero. Note: often the data used to build the model are not close to zero, so this interpretation may have no meaning.

#.	What does it mean that :math:`\sum_i{(x_i e_i)} = x^T e = 0` (i.e. the dot product is zero):

	-	The residuals are uncorrelated with the input variables, :math:`x`. There is no information in the residuals that is in :math:`x`.

#.	What does it mean that :math:`\sum_i{(\hat{y}_i e_i)} =  \hat{y}^T e = 0`

		-	The :index:`fitted values <pair: fitted value; least squares>` are uncorrelated with the residuals.

#.	How could the denominator term for :math:`b_1` equal zero?  And what would that mean?

	-	This shows that as long as there is variation in the :math:`x`-data that we will obtain a solution. We get no solution to the least squares objective if there is no variation in the data.

.. _LS-class-example:

Example
~~~~~~~~

We will refer back to the following example several times. Calculate the least squares estimates for the model :math:`y = b_0 + b_1 x` from the given data. Also calculate the predicted value of :math:`\hat{y}_i` when :math:`x_i = 5.5`

=========== ==== ==== ==== ==== ==== ==== ==== ==== ===== ==== ====
:math:`x`   10.0 8.0  13.0 9.0  11.0 14.0 6.0  4.0  12.0  7.0  5.0
----------- ---- ---- ---- ---- ---- ---- ---- ---- ----- ---- ----
:math:`y`   8.04 6.95 7.58 8.81 8.33 9.96 7.24 4.26 10.84 4.82 5.68
=========== ==== ==== ==== ==== ==== ==== ==== ==== ===== ==== ====

.. image:: ../figures/least-squares/show-anscombe-problem-1.png
	:align: center
	:width: 900px
	:scale: 40
	:alt: Scatter plot of the 11-point example data

..
	.. image:: ../figures/least-squares/regression-exercise.png
		:align: center
		:scale: 40

To calculate the least squares model:

.. code-block:: python

	import numpy as np
	import statsmodels.api as sm

	x = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
	y = np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96,
	              7.24, 4.26, 10.84, 4.82, 5.68])

	# Calculate the linear model, where y
	# is described by x. add_constant adds
	# the intercept term.
	X = sm.add_constant(x)
	mod_ls = sm.OLS(y, X).fit()

	# Coefficients:
	# const     3.0001
	# x1        0.5001
	mod_ls.params

	# You can get more information with
	print(mod_ls.summary())

	print("The model coefficients are: ")
	mod_ls.params

	b0, b1 = mod_ls.params
	x_new = 5.5
	y_predicted = b0 + b1 * x_new
	print(f"Given a new x value of {x_new} "
	      f"the predicted y = "
	      f"{round(y_predicted, 3)}")

.. code-block:: r

	x <- c(10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5)
	y <- c(8.04, 6.95, 7.58, 8.81, 8.33, 9.96,
	      7.24, 4.26, 10.84, 4.82, 5.68)

	# "Calculate for me the linear model,
	# where y is described by x"
	mod.ls <- lm(y ~ x)

	# Call:
	# lm(formula = y ~ x)
	#
	# Coefficients:
	# (Intercept)            x
	#	       3.0001       0.5001

	# You can get more information with
	summary(mod.ls)

	print('The model coefficients are: ')
	coefficients(mod.ls)

	b0 <- coefficients(mod.ls)[1]
	b1 <- coefficients(mod.ls)[2]
	x.new <- 5.5
	y_predicted <- b0 + b1 * x.new
	paste0('Given a new x value of ', x.new,
	       ' the predicted y = ',
	       round(y_predicted, 3))

*	:math:`b_0 = 3.0`
*	:math:`b_1 = 0.5`
*	When :math:`x_i = 5.5`, then :math:`\hat{y}_i = 3.0 + 0.5 \times 5.5 = 5.75`


.. _LS_single_x_sklearn_distillation:

A larger example: predicting vapour pressure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For larger data sets, the ``OLS`` class from the `process_improve
<https://github.com/kgdunn/process_improve>`_ package (the Python library accompanying this book)
provides a convenient API that fits naturally with Pandas data frames. It follows the scikit-learn
estimator convention of ``fit``, ``predict`` and ``score``, so everything shown here carries over
unchanged to scikit-learn's own ``LinearRegression`` class. We will use it again on the
`distillation tower <https://openmv.net/info/distillation-tower>`_ data set introduced in the
:ref:`prior section <LS_correlation_matrix_in_python>`.

Good statistical practice is to split the data: build the model on one part, then test it on
unseen data. Otherwise we get an inflated sense of how well the model performs. The ``.iloc``
accessor in Pandas selects rows by position, so we use it to split the 253 observations into a
"build" partition (the first 150 rows) and a "test" partition (the remaining rows):

.. code-block:: python

	import pandas as pd

	distill = pd.read_csv(
	    "https://openmv.net/file/distillation-tower.csv"
	)

	# Use the first 150 rows to build the model,
	# and the remaining rows to test it later.
	build = distill.iloc[:150]
	test = distill.iloc[150:]
	build.shape, test.shape

Now fit a single-variable least squares model that uses ``InvTemp3`` (the inverse of a temperature
measurement on tray 3) to predict ``VapourPressure``. The double-bracket idiom
``build[["InvTemp3"]]`` returns a column matrix (a 2-D :math:`n \times 1` array), which is the
shape these estimators expect for the predictor matrix :math:`\mathbf{X}`:

.. code-block:: python

	from process_improve.regression import OLS

	# X must be a 2-D array (n_rows by n_cols).
	# build[["InvTemp3"]] returns a column matrix;
	# build["InvTemp3"] would return a 1-D array.
	X = build[["InvTemp3"]].values
	y = build["VapourPressure"].values

	mymodel = OLS()
	mymodel.fit(X, y)

	# .intercept_ is a scalar; .coefficients_ is an
	# array, so we index it with [0] for the slope.
	print(
	    f"Intercept = {mymodel.intercept_:.5g}, "
	    f"slope = {mymodel.coefficients_[0]:.5g}"
	)

	# Printing the model shows a summary in the same
	# layout as R's summary(lm(...)), interpreted in
	# the section on software output:
	print(mymodel)

We will return to this model in the :ref:`next section <standard-error-section>` to inspect its
residuals, its standard error, and its :math:`R^2` value, and again in the section on
:ref:`multiple linear regression <LS_multiple_X_MLR>` to extend it with a second predictor.



..	Estimating the parameters when the data are centered
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	A small rearrangement of equation :eq:`define-2-LS` is given below. The modification centers the x-variables to a mean of zero. One can show, though we don't do it here, that the parameter estimates obtained are still the same (the new \beta_0 is zero)

		.. math::
			:label:define-2-LS-modified

				\mathrm{y} &= \beta_0 + \beta_1 (\mathrm{x} -\overline{\mathrm{x}}) + \epsilon
