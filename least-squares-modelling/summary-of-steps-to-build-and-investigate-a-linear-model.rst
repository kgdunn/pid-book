Summary of steps to build and investigate a linear model
==========================================================

.. index::
	pair: summary of steps; least squares

#.	Plot the data to assess model structure and degree of correlation between the |x| and |y| variable.

	.. code-block:: s

		plot(x, y)           # plot the raw data
		lines(lowess(x,y))   # superimpose non-parametric smoother to see correlation

#.	Fit the model and examine the printed output.

	.. code-block:: s

		model <- lm(y ~ x)   # fit the model: "y as described by variable x"
		summary(model)
		confint(model)

	- Investigate the model's standard error, how does it compare to the range of the |y| variable?
	- Calculate confidence intervals for the model parameters and interpret them.

#.	Visualize the model's predictions in the context of the model building data.

	.. code-block:: s

		plot(x, y)
		lines(lowess(x,y))        # show the smoother
		abline(model, col="red")  # and show the least squares model

#.	Plot a normal probability plot, or a q-q plot, of the residuals. Are they normally distributed?  If not, investigate if a transformation of the |y| variable might improve them. But also see the additional plots on checking for non-linearity and consider adding extra explanatory variables.

	.. code-block:: s

		library(car)
		qqPlot(resid(model))


#.	Plot the residuals against the |x|-values. We expect to see no particular structure. If you see trends in the data, it indicates that a transformation of the |x| variable might be appropriate, or that there are unmodelled phenomena in the |y| variable - we might need an additional |x| variable.

	.. code-block:: s

		plot(x, resid(model))
		abline(h=0, col="red")

#.	Plot the residuals in time (sequence) order. We expect to see no particular trends in the data. If there are patterns in the plot, assess whether autocorrelation is present in the |y| variable (use the ``acf(y)`` function in R). If so, you might have to sub-sample the data, or resort to proper time-series analysis tools to fit your model.

	.. code-block:: s

		plot(resid(model))
		abline(h=0, col="red")
		lines(lowess(resid(model), f=0.2))   # use a shorter smoothing span

#.	Plot the residuals against the fitted-values. By definition of the least-squares model, the covariance between the residuals and the fitted values is zero. You can verify that :math:`e^T\hat{y} = \sum_i^n{e_i\hat{y}_i} = 0`. A fan-shape to the residuals indicates the residual variance is not constant over the range of data: you will have to use weighted least squares to counteract that. It is better to use :ref:`studentized residuals <LS-studentized-residuals>`, rather than the actual residuals, since the actual residuals can show non-constant variance even though the errors have constant variance.

	.. That last line was from Fox's notes; cross reference it still

	.. code-block:: s

		plot(predict(model), rstudent(model))
		lines(lowess(predict(model), rstudent(model)))
		abline(h=0, col="red")

#.	Plot the predictions of |y| against the actual values of |y|. We expect the data to fall around a 45 degree line.

	.. code-block:: s

		plot(y, predict(model))
		lines(lowess(y, predict(model), f=0.5))     # a smoother
		abline(a=0, b=1, col="red")                 # a 45 degree line


.. _LS_workflow_blender_python:

A worked example of the workflow in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The steps above describe a general workflow that applies to any data analysis project, not just
least squares. We illustrate the early steps of that workflow on the
`blender efficiency <https://openmv.net/info/blender-efficiency>`_ data set, which records the
result of designed experiments where four factors were varied to study blending efficiency:
``ParticleSize``, ``MixerDiameter``, ``MixerRotation``, and ``BlendingTime``.

The six-step workflow on these data:

#.	**Define the objective**: understand which factors drive ``BlendingEfficiency``.

#.	**Get the data**:

	.. code-block:: python

		import pandas as pd

		blender = pd.read_csv(
		    "https://openmv.net/file/blender-efficiency.csv"
		)

#.	**Explore**: look at a few rows, the column types, and a numeric summary.

	.. code-block:: python

		blender.head()
		blender.tail()
		blender.describe()
		blender.info()

#.	**Clean**: in this case the data are pre-cleaned, so we move on.

#.	**Calculate**: a correlation matrix and scatter-plot matrix highlight which factors are most
	related to the outcome variable.

	.. code-block:: python

		from pandas.plotting import scatter_matrix

		# Numeric correlation matrix:
		blender.corr()

		# Visual version: scatter plot of every
		# pair of variables, with a kde on the
		# diagonal.
		scatter_matrix(
		    blender,
		    alpha=0.2,
		    figsize=(10, 8),
		    diagonal="kde",
		)

	Filtering and grouping are part of the daily work of anyone working with data, and Pandas
	makes both very compact:

	.. code-block:: python

		# Boolean indexing returns only the rows
		# where the condition is true:
		blender[blender["ParticleSize"] == 2]
		blender[blender["ParticleSize"] <= 5]
		blender[blender["ParticleSize"] > 5]

		# groupby applies the same calculation
		# to each value of the grouping variable:
		blender.groupby("ParticleSize").mean()
		blender.groupby("ParticleSize").std()
		blender.groupby("ParticleSize").max()

#.	**Communicate**: create a separate plot per particle size, so each subgroup can be inspected
	on its own axes:

	.. code-block:: python

		for psize, subset in blender.groupby("ParticleSize"):
		    ax = subset.plot.scatter(
		        x="BlendingTime",
		        y="BlendingEfficiency",
		    )
		    ax.set_title(f"When particle size = {psize}")

	Once the patterns are clear, you can fit a least squares model using
	:ref:`scikit-learn <LS_single_x_sklearn_distillation>` or
	:ref:`statsmodels <LS-class-example>` and continue with the residual diagnostics outlined in
	the steps above.


..	R2 = corr(x,y) = cov(X,Y)/SD(X)/SD(Y): notice the symmetry, R2 is the same whether y~x or x~y

.. Notes for this section

	p 288 of Hogg and Ledolter:

	1.	Plot residuals (y) against fitted values(x):
	2.	Outliers should be investigated - they are often the most interesting points
	3.	Increase in variance in residuals vs fitted values
	4.	Residuals in sequence (trends?)
	5.	Residuals vs x-variable: model structure deficiency

	Residuals due to (a) experimental error or (b) model structure deficiency

	(b) Model structure deficiency:

		- residual-pattern-forgottern-term.png shows forgotten term


	Pure (experimental) error: assessed with replicate data. How to test for model deficiency?

	Show that the sum of squares of the errors = sum(e^2) = e^Te = y^Ty - beta^TX^Ty

	Leverage, outliers, influence and discrepancy
	- Chatterjee and Hadi paper (see PDF)
