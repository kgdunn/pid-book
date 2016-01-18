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

