Exercises
=========

.. index::
	pair: exercises; least squares

.. question::

	Use the `distillation column data set <http://datasets.connectmv.com/info/distillation-tower>`_ and choose any two variables, one for |x| and one as |y|.  Then fit the following models by least squares in any software package you prefer:

		-	:math:`y_i = b_0 + b_1 x_i`
		-	:math:`y_i = b_0 + b_1 (x_i - \overline{x})` (what does the :math:`b_0` coefficient represent in this case?)
		-	:math:`(y_i - \overline{y}) = b_0 + b_1 (x_i - \overline{x})`

		Prove to yourself that centering the |x| and |y| variables gives the same model for the 3 cases in terms of the :math:`b_1` slope coefficient, standard errors and other model outputs.

.. answer::

	Once you have created an ``x`` and ``y`` variable in R, compare the output from these 3 models:

	.. code-block:: s

		# Model 1
		summary(lm(y ~ x))

		# Model 2
		x.mc <- x - mean(x)
		summary(lm(y ~ x.mc))

		# Model 3
		y.mc <- y - mean(y)
		summary(lm(y.mc ~ x.mc))

.. question::

	For a :math:`x_{\text{new}}` value and the linear model :math:`y = b_0 + b_1 x` the prediction interval for :math:`\hat{y}_\text{new}` is:

		.. math::
		
			\hat{y}_i \pm c_t \sqrt{V\{\hat{y}_i\}}

		where :math:`c_t` is the critical t-value, for example at the 95% confidence level.

	Use the `distillation column data set <http://datasets.connectmv.com/info/distillation-tower>`_ and with |y| as ``VapourPressure`` (units are kPa) and |x| as ``TempC2`` (units of degrees Farenheit) fit a linear model.  Calculate the prediction interval for vapour pressure at these 3 temperatures: 430, 480, 520 °F.

.. answer::

	The prediction interval is dependent on the value of :math:`x_\text{new, i}` used to make the prediction.  For this model, :math:`S_E = 2.989` kPa, :math:`n=253`,  :math:`\sum_j{(x_j - \overline{x})^2} = 86999.6`, and :math:`\overline{x} = 480.82`.

	.. math::

		\mathcal{V}\left(\hat{y}_\text{new,i}\right) = S_E^2 \left(1 + \dfrac{1}{n} + \dfrac{\left(x_\text{new}-\overline{x}\right)^2}{ \sum_j{(x_j - \overline{x})^2}} \right)

	Calculating this term manually, or using the ``predict(model, newdata=..., int="p")`` function in R gives the 95% prediction interval:

		*	:math:`x_\text{new} = 430` °F: :math:`\hat{y}_\text{new} = 53.49 \pm 11.97`, or [47.50, 59.47]
		*   :math:`x_\text{new} = 480` °F: :math:`\hat{y}_\text{new} = 36.92 \pm 11.80`, or [31.02, 42.82]
		*	:math:`x_\text{new} = 520` °F: :math:`\hat{y}_\text{new} = 23.67 \pm 11.90`, or [17.72, 29.62]

	.. figure:: ../figures/least-squares/distillation-prediction-interval.png
		:align: center
		:width: 750px
		:scale: 50

	.. literalinclude:: ../figures/least-squares/distillation-column-questions.R
		:language: s
		:lines: 1-25,30-33

.. question::

	 Refit the distillation model from the previous question with a transformed temperature variable.  Use :math:`1/T` instead of the actual temperature.

		-	Does the model fit improve?
		-	Are the residuals more normally distributed with the untransformed or transformed temperature variable?
		-	How do you interpret the slope coefficient for the transformed temperature variable?
		-	Use the model to compute the predicted vapour pressure at a temperature of 480 °F, and also calculate the corresponding prediction interval at that new temperature.

.. answer::

	-	Using the ``model.inv <- lm(VapourPressure ~ I(1/TempC2))`` instruction, one obtains the model summary below.  The model fit has improved slightly: the standard error is 2.88 kPa, reduced from 2.99 kPa.

		.. code-block:: text

			Call:
			lm(formula = VapourPressure ~ I(1/TempC2))

			Residuals:
			     Min       1Q   Median       3Q      Max
			-5.35815 -2.27855 -0.08518  1.95057 13.38436

			Coefficients:
			             Estimate Std. Error t value Pr(>|t|)
			(Intercept)  -120.760      4.604  -26.23   <2e-16 ***
			I(1/TempC2) 75571.306   2208.631   34.22   <2e-16 ***
			---
			Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

			Residual standard error: 2.88 on 251 degrees of freedom
			Multiple R-squared: 0.8235,	Adjusted R-squared: 0.8228
			F-statistic:  1171 on 1 and 251 DF,  p-value: < 2.2e-16

	-	The residuals have roughly the same distribution as before, maybe a little more normal on the left tail, but hardly noticeable.

		.. figure:: ../figures/least-squares/distillation-prediction-qqplots.png
			:align: center
			:width: 750px
			:scale: 80

	-	The slope coefficient of 75571 has units of ``kPa.°F``, indicating that each one unit *decrease* in temperature results in an *increase* in vapour pressure.  Since division is not additive, the change in vapour pressure when decreasing 10 degrees from 430 °F is a different decrease to that when temperature is 530 °F.  The interpretation of transformed variables in linear models is often a lot harder.  The easiest interpretation is to show a plot of 1/T against vapour pressure.

		.. figure:: ../figures/least-squares/distillation-prediction-inverted-temperature.png
			:align: center
			:width: 750px
			:scale: 40

	-	The predicted vapour pressure at 480 °F is 36.68 kPa :math:`\pm 11.37`, or within the range [31.0 to 42.4] with 95% confidence, very similar to the prediction interval from question 2.


	.. literalinclude:: ../figures/least-squares/distillation-column-questions.R
		:language: s
		:lines: 36-39,43-45,48-56,60-63


.. question::

	Again, for the distillation model, use the data from 2000 and 2001 to build the model (the first column in the data set contains the dates). Then use the remaining data to test the model.  Use |x| = ``TempC2`` and |y| = ``VapourPressure`` in your model.

		-	Calculate the RMSEP for the testing data.  How does it compare to the standard error from the model?
		-	Now use the ``influencePlot(...)`` function from the ``car`` library, to highlight the influential observations in the model building data (2000 and 2001).  Show your plot with observation labels (observation numbers are OK).  See part 5 of the `R tutorial <http://connectmv.com/tutorials/r-tutorial/>`_ for some help.
		-	Explain how the points you selected are influential on the model?
		-	Remove these influential points, and refit the model on the training data.  How has the model's slope and standard error changed?
		-	Recalculate the RMSEP for the testing data; how has it changed?

.. answer::
	:fullinclude: no
	:short: RMSEP = 4.18 kPa; standard error = 2.68 kPa.

	-	The testing data starts at index 160.  The code at the end of this question shows how RMSEP was calculated as 4.18 kPa, as compared to the standard error from the model building data (observations 1 to 159) of 2.679 kPa.  This indicates the predictions on totally new data have greater error that those observations used to build the model - an expected result.

	-	The influence plot from the model building data is given below.

		.. figure:: ../figures/least-squares/distillation-influence-plot.png
			:align: center
			:width: 750px
			:scale: 45

	-	The points considered as influential would be 38 and 84, which have both high leverage and high discrepancy.  Points 53 and 101 would also be considered influential: they have high leverage, though moderately sized residuals.  The other points marked in red have a large Cook's D value, however, their leverage is low, so it is unlikely that their removal will change the plot and its interpretation by very much.

	-	The points selected for removal are [38, 53, 84, 101].  The model was rebuilt and the slope coefficient changed from -0.368 to -0.358, while the standard error decreased from 2.679 to 2.455.  So their removal has decreased the size of the confidence intervals (before: :math:`-0.395 \leq \beta_T \leq - 0.342`, and after: :math:`-0.385 \leq \beta_T \leq -0.332`), however the slope coefficient is roughly comparable to that from before.

	-	The RMSEP has reduced from 4.18kPa to 3.92 kPa, a smallish reduction, given the range of the |y| variable.

	.. literalinclude:: ../figures/least-squares/distillation-column-questions.R
		:language: s
		:lines: 1-3,8,66-89,93-94,96-108

.. question::

	The `Kappa number data set <http://datasets.connectmv.com/info/kappa-number>`_ was used in an :ref:`earlier question <monitoring-kappa-number-question>` to construct a Shewhart chart.  The :ref:`"Mistakes to avoid" <monitoring-mistakes-to-avoid>` section (Process Monitoring), warns that the subgroups for a Shewhart chart must be independent to satisfy the assumptions used to derived the Shewhart limits. If the subgroups are not independent, then it will increase the type I (false alarm) rate.

	This is no different to the independence required for least squares models. Use the autocorrelation tool to determine a subgroup size for the Kappa variable that will satisfy the Shewhart chart assumptions.  Show your autocorrelation plot and interpret it as well.

.. answer::
	:fullinclude: no

	The autocorrelation plot shows significant lags up to lag 3, or even 4.  So subsampling the vector with every 4th or 5th element should yield independent samples.  The autocorrelation with every 5th observation confirms this.  You could also use every 6th, 7th, *etc* observation.  Using every 30th observation though is not too useful, since it would lead to a long delay before the control chart showed any problems.

	.. figure:: ../figures/least-squares/kappa-number-autocorrelation.png
		:align: center
		:width: 750px
		:scale: 50

	The ACF plot indicates that there is significant reappearance of correlation around lags 9 to 15.  It wasn't required for you to identify why for this assignment, but usually this would be related to a recycle stream that reenters a reactor, or due to an oscillation in a control loop.

	You can also verify the autocorrelation by plotting scatterplots of the vector against itself.  The first plot below shows what an ACF coefficient of 1.0 means, while the second plot shows what it means to use a lag offset of 1 position.  The correlation value = :math:`\sqrt{R^2}` is shown on each plot.  Compare that value shown to the y-axis of the ACF plots.

	.. image:: ../figures/least-squares/kappa-number-autocorrelation-scatterplots.png
		:align: center
		:width: 900px
		:scale: 100

	.. literalinclude:: ../figures/least-squares/kappa-number-autocorrelation.R
	       :language: s
	       :lines: 1-9,13-15,21-37

.. question::

	You presume the yield from your lab-scale bioreactor, :math:`y`, is a function of reactor temperature, batch duration, impeller speed and reactor type (one with with baffles and one without).  You have collected these data from various experiments.

	.. tabularcolumns:: |C|p{5em}|C|C|C|

	.. csv-table::
	   :header: Temp = :math:`T` [°C], Duration = :math:`d` [minutes], Speed = :math:`s` [RPM], Baffles = :math:`b` [Yes/No], Yield = :math:`y` [g]
	   :widths: 30, 30, 30, 30, 30

			82,      260,  4300,       No,      51
			90,      260,  3700,       Yes,     30
			88,      260,  4200,       Yes,     40
			86,      260,  3300,       Yes,     28
			80,      260,  4300,       No,      49
			78,      260,  4300,       Yes,     49
			82,      260,  3900,       Yes,     44
			83,      260,  4300,       No,      59
			64,      260,  4300,       No,      60
			73,      260,  4400,       No,      59
			60,      260,  4400,       No,      57
			60,      260,  4400,       No,      62
			101,     260,  4400,       No,      42
			92,      260,  4900,       Yes,     38


	-	Use software to fit a linear model that predicts the yield from these variables (the `data set is available from the website <http://datasets.connectmv.com/info/bioreactor-yields>`_).  See the `R tutorial <http://connectmv.com/tutorials/r-tutorial/>`_ for building linear models with integer variables in R.
	-	Interpret the meaning of each effect in the model.  If you are using R, then the ``confint(...)`` function will be helpful as well. Show plots of each |x| variable in the model against yield.  Use a box plot for the baffles indicator variable.
	-	Now calculate the :math:`\mathbf{X}^T\mathbf{X}` and :math:`\mathbf{X}^T\mathbf{y}` matrices; include a column in the :math:`\mathbf{X}` matrix for the intercept. Since you haven't mean centered the data to create these matrices, it would be misleading to try interpret them.
	-	Calculate the least squares model estimates from these two matrices.  See the `R tutorial <http://connectmv.com/tutorials/r-tutorial/>`_ for doing matrix operations in R, but you might prefer to use MATLAB for this step.  Either way, you should get the same answer here as in the first part of this question.

.. answer::
	:fullinclude: no

	-	After importing the data, just make sure the ``baffles`` variable is imported as a factor.  Then build the model as usual.  The computer output below shows the linear model's coefficients.

		.. literalinclude:: ../figures/least-squares/bioreactor-yields-problem.R
			:language: s
			:lines: 17-45

	-	The confidence intervals for each variable is significant at the 95% level.  The duration variable must be omitted from the model, because it has no variation.  While it might affect the yield, there is no variability in this data set to assess that.

		* :math:`0.00034 \leq b_\text{speed} \leq 0.017`: a 100rpm increase in impeller speed serves to increase yield by 0.87g on average, keeping all other variables constant
		* :math:`-15.9 \leq b_\text{baffles} \leq -2.30`: the use of baffles decreases yield, on average, by 9.1g, keeping all other variables constant
		* :math:`-0.74 \leq b_\text{temp} \leq -0.21`: each one degree increase in temperature lowers yield by 0.47g on average, keeping all other variables constant
		* We cannot say anything about the effect of batch duration

		The plots are not shown here, they can be drawn with ``plot(bio)`` to obtain a scatterplot matrix of plots.

	-	For the model :math:`y = b_0  + b_\text{speed}x_\text{speed} + b_\text{baffles}x_\text{baffles} + b_\text{temp}x_\text{temp}` let the coefficient vector be :math:`\mathrm{b} = [b_0, b_\text{speed},  b_\text{baffles}, b_\text{temp}]`, then we can write down the following X matrix to estimate it:

		.. math::
		
			\mathrm{X} = \begin{bmatrix}
							1 &  4300 & 0 & 82  \\
							1 &  3700 & 1 & 90  \\
							1 &  4200 & 1 & 88  \\
							1 &  3300 & 1 & 86  \\
							1 &  4300 & 0 & 80  \\
							1 &  4300 & 1 & 78  \\
							1 &  3900 & 1 & 82  \\
							1 &  4300 & 0 & 83  \\
							1 &  4300 & 0 & 64  \\
							1 &  4400 & 0 & 73  \\
							1 &  4400 & 0 & 60  \\
							1 &  4400 & 0 & 60  \\
							1 &  4400 & 0 & 101 \\
							1 &  4900 & 1 & 92
						\end{bmatrix}

		You can obtain the above :math:`\mathrm{X}` matrix in R using the ``model.matrix(model)`` function.  The :math:`\mathrm{X}^T\mathrm{X}` and :math:`\mathrm{X}^T\mathrm{y}` matrices are:

		.. math::
		
			\mathrm{X}^T\mathrm{X} = \begin{bmatrix}
							14      &   59100      &    6  &  1119 \\
							59100   & 251330000    & 24300 & 4714700 \\
							6       & 24300        & 6     & 516     \\
							1119    & 4714700      & 516   & 91351
						\end{bmatrix}
			\qquad \text{and} \qquad
			\mathrm{X}^T\mathrm{y} = \begin{bmatrix}
							668 \\
							2849600 \\
							229 \\
							52082
						\end{bmatrix}

	-	Using these matrices to solve for :math:`\mathrm{b}`

	 	.. math::
	
			\mathrm{b} = \left(\mathrm{X}^T\mathrm{X} \right)^{-1}\mathrm{X}^T\mathrm{y} =  \begin{bmatrix} 52.48 \\ 0.00871 \\ -9.09 \\ -0.471 \end{bmatrix}


		This result matches the results from R.  Note however that R, like most decent software packages, will not solve for the inverse of :math:`\left(\mathrm{X}^T\mathrm{X} \right)^{-1}` directly to compute :math:`\mathrm{b}`; instead it uses the `QR decomposition <http://en.wikipedia.org/wiki/QR_decomposition>`_.

		.. literalinclude:: ../figures/least-squares/bioreactor-yields-problem.R
			:language: s
			:lines: 46-

.. question::

	In the section on comparing differences between two groups we used, without proof, the fact that:

	.. math::

		\mathcal{V}\left\{\overline{x}_B - \overline{x}_A\right\} = \mathcal{V}\left\{\overline{x}_B\right\} + \mathcal{V}\left\{\overline{x}_A\right\}

	Prove this statement, and clearly explain all steps in your proof.

.. answer::
	:fullinclude: no

	I don't normally concentrate on proofs in the book, unless they show something interesting, or are used over and over.  This short mathematical statement fits both criteria.

	The important point with this proof is that :math:`\overline{x}_A` and :math:`\overline{x}_B` are the variables, not :math:`x`.  These variables come from a normal distribution (Central limit theorem), as long as we assume independent sampling: :math:`\overline{x}_A \sim \mathcal{N} \left(\mu; \sigma^2/n_A\right)`, and similarly for :math:`\overline{x}_B`.

	.. math::

		\mathcal{V}\left\{\overline{x}_B - \overline{x}_A\right\}	&= \mathcal{V}\left\{\overline{x}_B + \left(-\overline{x}_A\right) \right\} \\
														&= \mathcal{V}\left\{\overline{x}_B \right\} + 2\text{Cov}\left\{\overline{x}_B, \left(-\overline{x}_A\right)\right\} + \mathcal{V}\left\{-\overline{x}_A \right\} \\
														&= \mathcal{V}\left\{\overline{x}_B \right\} + 0 + \left(-1\right)^2\mathcal{V}\left\{\overline{x}_A \right\} \\
														&= \mathcal{V}\left\{\overline{x}_B\right\} + \mathcal{V}\left\{\overline{x}_A\right\}

	The second line is a result shown earlier. The third line requires that we assume the between-group means :math:`\overline{x}_B` and :math:`\overline{x}_A` are independent, and so they are uncorrelated (their covariance is zero).  This was one of the key assumptions when we studied between-group differences; and is one assumption that is often true in many real cases.

.. question::

	The production of low density polyethylene is carried out in long, thin pipes at high temperature and pressure (1.5 kilometres long, 50mm in diameter, 500 K, 2500 atmospheres).  One quality measurement of the LDPE is its melt index.  Laboratory measurements of the melt index can take between 2 to 4 hours.  Being able to predict this melt index, in real time, allows for faster adjustment to process upsets, reducing the product's variability.  There are many variables that are predictive of the melt index, but in this example we only use a temperature measurement that is measured along the reactor's length.

	These are the data of temperature (K) and melt index (units of melt index are "grams per 10 minutes").

	.. Previous table
		======================= ======================
		Temperature = :math:`T` Melt index = :math:`m`
		----------------------- ----------------------
		(Kelvin)       			(g per 10 mins)
		======================= ======================
		     441       			  9.3
		     453       			  6.6
		     461       			  6.6
		     470       			  7.0
		     478       			  6.1
		     481       			  3.5
		     483       			  2.2
		     485       			  3.6
		     499       			  2.9
		     500       			  3.6
		     506       			  4.2
		     516       			  3.5
		======================= ======================

	=============================================  === === === === === === === === === === === ===
	**Temperature** = :math:`T` [Kelvin]           441 453 461 470 478 481 483 485 499 500 506 516
	---------------------------------------------  --- --- --- --- --- --- --- --- --- --- --- ---
	**Melt index** = :math:`m`  [g per 10 mins]    9.3 6.6 6.6 7.0 6.1 3.5 2.2 3.6 2.9 3.6 4.2 3.5
	=============================================  === === === === === === === === === === === ===


	The following calculations have already been performed:

		* Number of samples, :math:`n = 12`
		* Average temperature = :math:`\overline{T} = 481` K
		* Average melt index, :math:`\overline{m} = 4.925` g per 10 minutes.
		* The summed product, :math:`\sum_i{\left(T_i-\overline{T}\right)\left(m_i - \overline{m}\right)} = -422.1`
		* The sum of squares, :math:`\sum_i{\left(T_i-\overline{T}\right)^2} = 5469.0`

	#.	Use this information to build a predictive linear model for melt index from the reactor temperature.
	#.	What is the model's standard error and how do you interpret it in the context of this model?  You might find the following software software output helpful, but it is not required to answer the question.

		.. code-block:: text

			Call:
			lm(formula = Melt.Index ~ Temperature)

			Residuals:
			    Min      1Q  Median      3Q     Max
			-2.5771 -0.7372  0.1300  1.2035  1.2811

			Coefficients:
			            Estimate Std. Error t value Pr(>|t|)
			(Intercept) --------    8.60936   4.885 0.000637
			Temperature --------    0.01788  -4.317 0.001519

			Residual standard error: 1.322 on 10 degrees of freedom
			Multiple R-squared: 0.6508,	Adjusted R-squared: 0.6159
			F-statistic: 18.64 on 1 and 10 DF,  p-value: 0.001519

	#.	Quote a confidence interval for the slope coefficient in the model and describe what it means.  Again, you may use the above software output to help answer your question.

.. answer::
	:fullinclude: no
	:short: m = 42.0 - 0.0772 T

	#.	The simplest linear predictive model possible is :math:`m = \beta_0 + \beta_1 T + \varepsilon`, predicting the melt index from temperature.  Once we find estimates for these coefficients we write: :math:`m = b_0 + b_1 T + e`.  And one way to calculate these coefficients is by least squares.  In the class notes we showed that for a variable :math:`x` used to predict a variable :math:`y` that:

	.. math::

		b_0 &= \overline{\mathrm{y}} - b_1\overline{\mathrm{x}} \\
		b_1 &= \dfrac{ \sum_i{\left(x_i - \overline{\mathrm{x}}\right)\left(y_i - \overline{\mathrm{y}}\right) } }{ \sum_i{\left( x_i - \overline{\mathrm{x}}\right)^2} }

	Using the pre-calculated values, and that in our case :math:`T = x`, and that :math:`m = y`

	.. math::

		b_1 &= \dfrac{ -422.1 }{ 5469.0 } = - 0.0772 \frac{\text{g per 10 minutes}}{K}\\
		b_0 &= 4.925 + 0.0772 \times 481 = 42.0 \text{g per 10 minutes}

	A predictive model of melt flow is: :math:`\hat{m} = 42.0 - 0.0772 \times T`

	#.	The standard error, :math:`S_E` can be read directly from the software output as 1.322 g per 10 minutes.  If you like, you could also have calculated it by hand, using the above predictive model, calculating residuals (:math:`e_i = m_i - \hat{m}_i`), from which the standard error is :math:`\sqrt{\dfrac{\sum_i^n{e_i^2}}{n-k}}`, where :math:`n=12` and :math:`k=2` (there are 2 parameters in the model).  However I recommend you always use the software output and avoid these tedious hand calculations.

	The interpretation of the standard error for this model is that the approximate prediction error of melt index has a standard deviation of 1.322 grams per 10 minutes (if the residuals are normally distributed).

	#.	The slope coefficient estimate, :math:`b_1` has standard error of 0.01788 (from the software output), or it could be calculated as :math:`S_E^2(b_1) = \dfrac{S_E^2}{\sum_j{\left( T_j - \overline{T} \right)^2}} = \dfrac{1.322^2}{5469.0} = 0.01788^2 = 3.19 \times 10^{-4}`.

	From this we can construct the confidence interval for the actual slope coefficient, :math:`\beta_1`.  I have used the 95% confidence level, but you could use any level you prefer.  The degrees of freedom to use for the :math:`t`-distribution are :math:`n-k = 12 -2 = 10`.

	.. math::

		\begin{array}{rcccl}
			- c_t                			&\leq& \dfrac{b_1 - \beta_1}{S_E(b_1)} &\leq &  +c_t\\
			b_1 - c_t S_E(b_1)   			&\leq& \beta_1                         &\leq&	b_1 + c_t S_E(b_1) \\
			-0.0772 - 2.23 \times 0.01788	&\leq& \beta_1                         &\leq&	-0.0772 + 2.23 \times 0.01788 \\
			-0.117							&\leq& \beta_1                         &\leq&	-0.037
		\end{array}

	You may also have chosen to answer at the 99% confidence level:

	.. math::

		\begin{array}{rcccl}
			b_1 - c_t S_E(b_1)   			&\leq& \beta_1                         &\leq&	b_1 + c_t S_E(b_1) \\
			-0.0772 - 3.17 \times 0.01788	&\leq& \beta_1                         &\leq&	-0.0772 + 3.17 \times 0.01788 \\
			-0.134							&\leq& \beta_1                         &\leq&	-0.0205
		\end{array}

	This shows, at which ever confidence level (95% or 99%), the range within which we can expect to find the true slope coefficient.  This slope represents the magnitude by which the melt index changes, on average, for a one degree change in temperature.  If we plan to manipulate the melt index using temperature, then this range will help us estimate an upper and lower bound for the effort required to adjust the melt index.

.. question::

	For a distillation column, it is well known that the column temperature directly influences the purity of the product, and this is used in fact for feedback control, to achieve the desired product purity.  Use the `distillation data set <http://datasets.connectmv.com/info/distillation-tower>`_ , and build a least squares model that predicts ``VapourPressure`` from the temperature measurement, ``TempC2``.  Report the following values:

	#.	the slope coefficient, and describe what it means in terms of your objective to control the process with a feedback loop
	#.	the interquartile range and median of the model's residuals
	#.	the model's standard error
	#.	a confidence interval for the slope coefficient, and its interpretation.

	You may use any computer package to build the model and read these values off the computer output.

.. answer::
	:fullinclude: no

	The solution to this question can be almost entirely solved using R, though any other language could be used.  These commands, with the output that follows, were used:

	.. code-block:: text

		> distillation <- read.csv('http://datasets.connectmv.com/file/distillation-tower.csv')
		> model <- lm(distillation$VapourPressure ~ distillation$TempC2)
		> summary(model)

		Call:
		lm(formula = distillation$VapourPressure ~ distillation$TempC2)

		Residuals:
		     Min       1Q   Median       3Q      Max
		-5.59621 -2.37597  0.06674  2.00212 14.18660

		Coefficients:
		                     Estimate Std. Error t value Pr(>|t|)
		(Intercept)         195.96141    4.87669   40.18   <2e-16 ***
		distillation$TempC2  -0.33133    0.01013  -32.69   <2e-16 ***
		---
		Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

		Residual standard error: 2.989 on 251 degrees of freedom
		Multiple R-squared: 0.8098,	Adjusted R-squared: 0.8091
		F-statistic:  1069 on 1 and 251 DF,  p-value: < 2.2e-16


	#.	This predictive model allows us to achieve better control of the vapour pressure, because we can predict it from temperature (measured in real-time), rather than wait several hours for the laboratory vapour pressure value. The slope coefficient is -0.331, and since no units were given, I can't expect any in your solution; however one should report the units, which is this case would be units of pressure divided by units temperature (e.g. psi/K).  What this means, in terms of feedback control of the vapour pressure is that we must decrease the temperature to raise the vapour pressure.  This is important when tuning the feedback control loop in 2 ways: (a) firstly, the the sign of the gain in the feedback controller (i.e. negative gain) must be the same as the process gain to achieve a stable feedback loop, (b) the magnitude of the slope provides an estimate of how sensitive the vapour pressure is to temperature.  For example: do we have to add a large amount of energy into the distillation column to achieve a smallish reduction in vapour pressure?  The answer depends heavily on the units, which I omitted to provide.

	#.	These are reported in the above software output: (a) the residual IQR is 2.00 - (-2.38) = 4.38 units of vapour pressure, while (b) the median residual is close to zero, as expected.

	#.	The model's standard error is 2.989 in the output, or around 3.00 units of vapour pressure.

	#.	The slope coefficient's confidence interval can be calculated from its :math:`z`-value = :math:`\dfrac{b_1 - \beta_1}{S_E(b_1)}`; but we require the standard error of the slope coefficient, which is :math:`S_E(b_1) = 0.01013` from the software output.  The value for :math:`c_t = 1.969` from the :math:`t`-distribution at the 95% confidence level, with :math:`n-k = 253 - 2 = 251` degrees of freedom (a normal distribution would work equally well in this case).

		.. math::

			\begin{array}{rcccl}
				- c_t                			&\leq& \dfrac{b_1 - \beta_1}{S_E(b_1)} &\leq &  +c_t\\
				-0.33133 - 1.969 \times 0.01013	&\leq& \beta_1                         &\leq&	-0.33133 + 1.969 \times 0.01013 \\
				-0.35							&\leq& \beta_1                         &\leq&	-0.31
			\end{array}

		This shows, at the 95% confidence level, the range within which we can expect to find the true slope coefficient. This range is remarkably narrow; i.e. our feedback controller gain is unlikely to change on either extreme.  So we can likely design our control loop at the center point, and be sure it will work over the entire range of expected operation.  Please also cross reference the solutions to question 2.4 in the written midterm to correctly understand what a confidence interval is.

		If you used 99% confidence levels, the answer should be: :math:`-0.358 \leq \beta_1 \leq -0.305`.

		We have illustrated the actual slope (thick, solid line) at the upper and lower bounds of the slope coefficient (thin, dashed lines) in the accompanying figure.  Not required for this question, but added nevertheless, are the prediction intervals for :math:`\hat{y}_i`.

		.. figure:: ../figures/least-squares/distillation-least-squares.png
			:align: center
			:width: 750px
			:scale: 60

	I recommended that you reproduce R's output yourself.  The code below calculates these same values.

	.. literalinclude:: ../figures/least-squares/distillation-least-squares.R
	       :language: s
	       :lines: 1-67,70-82

.. question::
	
	Use the `bioreactor data <http://datasets.connectmv.com/info/bioreactor-yields>`_, which shows the percentage yield from the reactor when running various experiments where temperature was varied, impeller speed and the presence/absence of baffles were adjusted.

	#.	Build a linear model that uses the reactor temperature to predict the yield. Interpret the slope and intercept term.

	#.	Build a linear model that uses the impeller speed to predict yield. Interpret the slope and intercept term.

	#.	Build a linear model that uses the presence (represent it as 1) or absence (represent it as 0) of baffles to predict yield. Interpret the slope and intercept term. 

		*Note*: if you use R it will automatically convert the ``baffles`` variable to 1's and 0's for you. If you wanted to make the conversion yourself, to  verify what R does behind the scenes, try this:

		.. code-block:: s

			# Read in the data frame
			bio <- read.csv('http://datasets.connectmv.com/file/bioreactor-yields.csv')

			# Force the baffles variables to 0's and 1's
			bio$baffles <- as.numeric(bio$baffles) - 1

	#.	Which variable(s) would you change to boost the batch yield, at the lowest cost of implementation?

	#.	Use the ``plot(bio)`` function in R, where ``bio`` is the data frame you loaded using the ``read.csv(...)`` function. R notices that ``bio`` is not a single variable, but a group of variables, i.e. a data frame, so it plots what is called a *scatterplot matrix* instead. Describe how the scatterplot matrix agrees with your interpretation of the slopes in parts 1, 2 and 3 of this question.

	Solution
	--------

	The R code (below) was used to answer all questions.

	#.	
		*	The model is: :math:`\hat{y} = 102.5 - 0.69T`, where :math:`T` is tank temperature.
		*	Intercept = :math:`102.5` % points is the yield when operating at 0 :math:`^\circ \text{C}`. Obviously not a useful interpretation, because data have not been collected in a range that spans, or is even close to 0 :math:`^\circ \text{C}`. It is likely that this bioreactor system won't yield any product under such cold conditions. Further, a yield greater than 100% is not realizable.
		*	Slope = -0.69 :math:`\frac{[\%]}{[^\circ \text{C}]}`, indicating the yield decreases, on average, by about 0.7 units for every degree increase in tank temperature.

	#.	
		*	The model is: :math:`\hat{y} = -20.3 + 0.016S`, where :math:`S` is impeller speed.
		*	Intercept = :math:`-20.3` % points is the yield when operating no agitation. Again, obviously not a useful interpretation, because the data have not been collected under these conditions, and yield can't be a negative quantity.
		*	Slope = 0.016 :math:`\frac{[\%]}{[\text{RPM}]}`, indicating the yield increases, on average, by about 1.6 percentage points per 100 RPM increase.

	#.	
		*	The model is: :math:`\hat{y} = 54.9 - 16.7B`, where :math:`B` is 1 if baffles are present and :math:`B=0` with no baffles.
		*	Intercept = :math:`54.9` % points yield is the yield when operating with no baffles (it is in fact the average yield of all the rows that have "No" as their baffle value).
		*	Slope = -16.7 %, indicating the presence of baffles decreases the yield, on average, by about 16.7 percentage points.

	#.	This is an open-ended, and case specific. Some factors you would include are:

		*	Remove the baffles, but take into account the cost of doing so. Perhaps it takes a long time (expense) to remove them, especially if the reactor is used to produce other products that do require the baffles.

		*	Operate at lower temperatures. The energy costs of cooling the reactor would factor into this.

		*	Operate at higher speeds and take that cost into account. Notice however there is one observation at 4900 RPM that seems unusual: was that due to the presence of baffles, or due to temperature in that run?  We'll look into this issue with multiple linear regression later on.

		.. note:: 

			Please note that our calculations above are not the true effect of each of the variables (temperature, speed and baffles) on yield. Our calculations assume that there is no interaction between temperature, speed and baffles, and that each effect operates independent of the others. That's not necessarily true. See the section on :ref:`interpreting MLR coefficients <MLR_coefficient_interpretation>` to learn how to "control for the effects" of other variables.

	#.	The scatterplot matrix, shown below, agrees with our interpretation. This is an information rich visualization that gives us a feel for the multivariate relationships and really summarizes all the variables well (especially the last row of plots).

		*	The yield-temperature relationship is negative, as expected.
		*	The yield-speed relationship is positive, as expected.
		*	The yield-baffles relationship is negative, as expected.
		*	We can't tell anything about the yield-duration relationship, as it doesn't vary in the data we have (there could/should be a relationship, but we can't tell).

		.. figure:: ../figures/least-squares/bioreactor-scatterplot-matrix.png
			:alt:	images/math
			:scale: 70
			:width: 750px
			:align: center

	.. literalinclude:: ../figures/least-squares/bioreactor-regression-assignment.R
		:language: s

.. question::

	.. _gas_furnace_LS_question:

	Use the `gas furnace data <http://datasets.connectmv.com/info/gas-furnace>`_ from the website to answer these questions. The data represent the gas flow rate (centered)  from a process and the corresponding CO\ :sub:`2` measurement.

	#.	Make a scatter plot of the data to visualize the relationship between the variables.  How would you characterize the relationship?

	#.	Calculate the variance for both variables, the covariance between the two variables, and the correlation between them, :math:`r(x,y)`. Interpret the correlation value; i.e. do you consider this a strong correlation?

	#.	Now calculate a least squares model relating the gas flow rate as the :math:`x` variable to the CO\ :sub:`2` measurement as the :math:`y`-variable.  Report the intercept and slope from this model.

	#.	Report the :math:`R^2` from the regression model.  Compare the squared value of :math:`r(x,y)` to :math:`R^2`.  What do you notice? Now reinterpret what the correlation value means (i.e. compare this interpretation to your answer in part 2).

	#.	**Advanced**: Switch :math:`x` and :math:`y` around and rebuild your least squares model.  Compare the new :math:`R^2` to the previous model's :math:`R^2`.  Is this result surprising?  How do interpret this?

.. answer::

	#.	Relationship: the data are negatively correlated.

		.. figure:: ../figures/least-squares/CO2-gas-furnace-raw-data.png
			:alt:	../figures/least-squares/CO2-gas-furnace-question.R
			:scale: 70
			:width: 750px
			:align: center

		I've chosen to use the ``sp`` or ``scatterplot`` function from the ``car`` library.  It shows the scatterplot smoother (a.k.a. loess line) as solid red, the spread around the smoother (dashed red), the least squares regression line (black) and boxplots for each axis.

		This is a great example of an information-rich visualization: packing the maximum amount of information into a small space.  This plot answers so many questions we might have about the data.

	#.	The ``cov(...)`` command supplies the variance and covariance, and the ``cor(...)`` command gives the correlation.

		*	Variance of input gas flow rate = 1.15 [gas flow units] :math:`^2`
		*	Variance of CO\ :sub:`2` = 10.3 [CO\ :sub:`2` units] :math:`^2`
		*	Covariance between input gas flow and CO\ :sub:`2` = -1.66 [gas flow units][CO\ :sub:`2` units]
		*	Correlation = -0.48, i.e. around -0.5.

		From my experience with data, I personally would interpret this as a reasonably strong correlation.  There is reasonably strong linear behaviour in the data cloud shown above, enough of a relationship to confidently say that "the CO\ :sub:`2` output does decrease at higher gas flow rates".

	#.	From the R model output:

	 	*	intercept is -1.44 units of CO\ :sub:`2` 
		*	slope is 53.4 :math:`\frac{[\text{units of CO}_2]}{[\text{units of gas flow}]}`

	#.	
		*	From the R model output: :math:`R^2 = 0.2347`
		*	From earlier, the squared correlation is :math:`(-0.484)^2 = 0.2347`, the same value.  
		*	Correlation can be interpreted as the square root of the :math:`R^2` value when regressing :math:`y` on :math:`x` (i.e. fitting a linear model to :math:`y` using :math:`x` as the input). 
		*	Most novices would be misled and consider an :math:`R^2` value of 0.23 quite low.  But notice that there is a repeatable and consistent negative linear relationship between :math:`x` and :math:`y` in this data.


	#.	This shows the interesting result that when regressing :math:`x` on :math:`y` (instead of the usual regression of :math:`y` on :math:`x`), that we get the same :math:`R^2` value.  Note however that the *intercept* and *slope* are different between the two regressions.  

		This also calls into question the interpretation of the :math:`R^2` value in regression. :math:`R^2` is just the square of the correlation coefficient. Recall from class the slide on the `Wikipedia examples of correlation <http://en.wikipedia.org/wiki/File:Correlation_examples.png>`_: there were examples where :math:`r(x,y) = \sqrt{R^2}` was zero, but still a strong *relationship* existing in the data. So we should interpret :math:`R^2` as a measure only of the *linear relationship* between two variables.  And bear its quadratic nature in mind  - interpreting the correlation is actually easier, and more "linear", in that a 0.2 improvement in correlation means the same thing when going from :math:`r=0.2` to 0.4, as it does when going from :math:`r=0.7` to 0.9 (not so for :math:`R^2`).

	.. literalinclude:: ../figures/least-squares/CO2-gas-furnace-question.R
		:language: s


.. question::

	.. _thermocouple_LS_question:
	
	A new type of `thermocouple <http://en.wikipedia.org/wiki/Thermocouple>`_ is being investigated by your company's process control group.  These devices produce an *almost* linear voltage  (millivolt) response at different temperatures. In practice though it is used the other way around: use the millivolt reading to predict the temperature.  The process of fitting this linear model is called *calibration*.  

	#.	Use the following data to calibrate a linear model:

		================= ==== ==== ==== ==== ==== ==== ==== ==== ==== ====
		Temperature [K]   273  293  313  333  353  373  393  413  433  453 
		----------------- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
		Reading [mV]	  0.01 0.12 0.24 0.38 0.51 0.67 0.84 1.01 1.15 1.31  
		================= ==== ==== ==== ==== ==== ==== ==== ==== ==== ====

		Show the linear model and provide the predicted temperature when reading 1.00 mV.

	#.	Are you satisfied with this model, based on the coefficient of determination (:math:`R^2`) value?  

	#.	What is the model's standard error?  Now, are you satisfied with the model's prediction ability, given that temperatures can usually be recorded to an accuracy of :math:`\pm 0.5` K with most inexpensive thermocouples.

	#.	What is your (revised) conclusion now about the usefulness of the :math:`R^2` value?

	**Note**: This example explains why we don't use the terminology of *independent* and *dependent* variables in this book.  Here the temperature truly is the independent variable, because it causes the voltage difference that we measure.  But the voltage reading is the independent variable in the least squares model. The word *independent* is being used in two different senses (its English meaning *vs* its mathematical meaning), and this can be misleading.

.. answer::

	#.	The linear model is used to predict temperature given the reading in millivolts.  The reason is that in modelling, in general, we specify as :math:`x` the variable(s) we always have available, while :math:`y` is the variable we would like to predict from the :math:`x`.

		The model has the form: :math:`T = b_0 + b_1V`, where :math:`T` is temperature and :math:`V` is the voltage reading.  Coefficients in the linear model are:

		.. math::

			T = 278.6 + 135.3 V 

		implies that recording an increase in 0.1 mV means, on average, the temperature has increased by 13.5 K in the system.

		The temperature prediction at 1.00 mV would be 413.9 K.

		.. figure:: ../figures/least-squares/voltage-linear-model.png
			:scale: 60
			:align: center

		The following Python code was used to fit the model and draw the plot.
		
		.. literalinclude:: ../figures/least-squares/voltage_linear_model.py
			:language: python

		If you used ``R`` to fit the model, you would written something like this::

			> V <- c(0.01, 0.12, 0.24, 0.38, 0.51, 0.67, 0.84, 1.01, 1.15, 1.31)
			> T <- c(273, 293, 313, 333, 353, 373, 393, 413, 433, 453)
			> model <- lm(T ~ V)
			> summary(model)

			Call:
			lm(formula = T ~ V)

			Residuals:
			    Min      1Q  Median      3Q     Max 
			-6.9272 -2.1212 -0.1954  2.7480  5.4239 

			Coefficients:
			            Estimate Std. Error t value Pr(>|t|)    
			(Intercept)  278.574      2.204  126.39 1.72e-14 ***
			V            135.298      2.922   46.30 5.23e-11 ***
			---
			Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1 

			Residual standard error: 3.916 on 8 degrees of freedom
			Multiple R-squared: 0.9963,	Adjusted R-squared: 0.9958 
			F-statistic:  2144 on 1 and 8 DF,  p-value: 5.229e-11

	#.	The :math:`R^2` value from this linear fit is :math:`R^2 = 0.996`, which being so close to 1.0, implies the linear relationship in the data is strong (the linear model fits the data very well) - that's all.  

		One cannot be satisfied with only an :math:`R^2` value: it has nothing to do with whether the model's prediction accuracy is any good.  So we can't tell anything from this number.

	#.	The model's standard error is 3.9 K.  If we assume the prediction error is normally distributed around the linear fit, this corresponds to one standard deviation.  So 95% of our prediction error lies roughly within a range of :math:`\pm 2\times 3.92` or :math:`\pm 7.8` K.  These are the dashed red lines drawn on the figure.  (Please note: the true error intervals are not parallel to the regression line, they are curved; however the :math:`\pm 2S_E` limits are a good-enough approximation for most engineering applications.

		This prediction ability of :math:`\pm 8` K is probably not satisfying for most engineering applications, since we can predict temperatures far more accurately, over the range from 273K to 453K, using off-the-shelf commercial thermocouples.  

	#.	The purpose of this question is to mainly point out the misleading nature of :math:`R^2` - this value looks really good: 99.6%, yet the actual purpose of the model, the ability to predict temperature from the millivolt reading, has no relationship at all to this :math:`R^2` value.

	.. sd(T) = 60.5
	.. diff(range(T)) = 180
	.. baseline_ratio = 60/180 = 0.3333
	.. SE = 3.9
	.. model_ratio = 3.9/180 = 0.0216
	.. ratio = 1 - 0.0216/0.3333 = 0.935: seems pretty good
	

.. question::

	#.	Use the linear model you derived in the :ref:`gas furnace question <gas_furnace_LS_question>`, where you used the gas flow rate to predict the CO\ :sub:`2` measurement, and construct the analysis of variance table (ANOVA) for the dataset. Use your ANOVA table to reproduce the residual standard error, :math:`S_E` value, that you get from the R software output.

		Go through the `R tutorial <http://connectmv.com/tutorials/r-tutorial/>`_ to learn how to efficiently obtain the residuals and predicted values from a linear model object.

	#.	Also for the above linear model, verify whether the residuals are normally distributed.

	#.	Use the linear model you derived in :ref:`the thermocouple question <thermocouple_LS_question>`, where you used the voltage measurement to predict the temperature, and construct the analysis of variance table (ANOVA) for that dataset. Use your ANOVA table to reproduce the residual standard error, :math:`S_E` value, that you get from the R software output.

.. answer::

	#.	The ANOVA table values were calculated in the code solutions for question 2:

		=================== ========================================= =================== ============== ========================================
		Type of variance    Distance                                  Degrees of freedom  SSQ            Mean square
		=================== ========================================= =================== ============== ========================================
		Regression          :math:`\hat{y}_i - \overline{\mathrm{y}}` :math:`k-2`         709.9          354.9
		------------------- ----------------------------------------- ------------------- -------------- ----------------------------------------
		Error               :math:`y_i - \hat{y}_i`                   :math:`n-k`         2314.9         7.87
		------------------- ----------------------------------------- ------------------- -------------- ----------------------------------------
		Total               :math:`y_i - \overline{\mathrm{y}}`       :math:`n`           3024.8         10.2
		=================== ========================================= =================== ============== ========================================

		The residual standard error, or just standard error, :math:`S_E = \sqrt{\frac{2314.9}{296-2}} = 2.8` %CO\ :sub:`2`, which agrees with the value from R.

	#.	These residuals were normally distributed, as verified in the qq-plot:

		.. image:: ../figures/least-squares/CO2-gas-furnace-residuals.png
			:alt:	../figures/least-squares/CO2-gas-furnace-question.R
			:scale: 60
			:width: 750px
			:align: center

		As mentioned in the ``help(qqPlot)`` output, the dashed red line is the confidence envelope at the 95% level.  The single point just outside the confidence envelope is not going to have any practical effect on our assumption of normality.  We expect 1 point in 20 to lie outside the limits.

		Read ahead, if required, on the meaning of :ref:`studentized residuals <LS-studentized-residuals>`, which are used on the :math:`y`-axis.

	#.	For the thermocouple data set:

		=================== ========================================= =================== ============== ========================================
		Type of variance    Distance                                  Degrees of freedom  SSQ            Mean square
		=================== ========================================= =================== ============== ========================================
		Regression          :math:`\hat{y}_i - \overline{\mathrm{y}}` :math:`k-2`         32877          16438
		------------------- ----------------------------------------- ------------------- -------------- ----------------------------------------
		Error               :math:`y_i - \hat{y}_i`                   :math:`n-k`         122.7          15.3
		------------------- ----------------------------------------- ------------------- -------------- ----------------------------------------
		Total               :math:`y_i - \overline{\mathrm{y}}`       :math:`n`           33000          3300
		=================== ========================================= =================== ============== ========================================

		The residual standard error, or just standard error, :math:`S_E = \sqrt{\frac{122.7}{10-2}} = 3.9` K, which agrees with the value from R.

