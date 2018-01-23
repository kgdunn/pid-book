Enrichment topics
==========================================


These topics are not covered in depth in this book, but might be of interest to you. I provide a small introduction to each topic, showing what their purpose is, together with some examples.

Nonparametric models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:index:`Nonparametric modelling <single:nonparametric modelling>` is a general model where the relationship between :math:`x` and :math:`y` is of the form: :math:`y = f(x) + \varepsilon`, but the function :math:`f(x)`, i.e. the model, is left unspecified. The model is usually a smooth function.

Consider the example of plotting Prestige (the `Pineo-Porter prestige <https://en.wikipedia.org/wiki/John_Porter_(sociologist)>`_ score) against Income, from the 1971 Canadian census. A snippet of the data is given by:

.. code-block:: s

	                       education income women prestige census type
	ECONOMISTS                 14.44   8049 57.31     62.2   2311 prof
	VOCATIONAL.COUNSELLORS     15.22   9593 34.89     58.3   2391 prof
	PHYSICIANS                 15.96  25308 10.56     87.2   3111 prof
	NURSING.AIDES               9.45   3485 76.14     34.9   3135   bc
	POSTAL.CLERKS              10.07   3739 52.27     37.2   4173   wc
	TRAVEL.CLERKS              11.43   6259 39.17     35.7   4193   wc
	BABYSITTERS                 9.46    611 96.53     25.9   6147 <NA>
	BAKERS                      7.54   4199 33.30     38.9   8213   bc
	MASONS                      6.60   5959  0.52     36.2   8782   bc
	HOUSE.PAINTERS              7.81   4549  2.46     29.9   8785   bc

The plot on the left is the raw data, while on the right is the raw data with the nonparametric model (line) superimposed. The smoothed line is the nonparametric function, :math:`f(x)`, referred to above, and :math:`x` = Income ($), and :math:`y` = Prestige.

.. image:: ../figures/least-squares/nonparametric-plots.png
	:width: 900px
	:align: center
	:scale: 70
	:alt: fake width

For bivariate cases, the nonparametric model is often called a *scatterplot smoother*. There are several methods to calculate the model; one way is by locally weighted scatterplot smoother (LOESS), described as follows. Inside a fixed subregion along the :math:`x`-axis (called the window):

.. TODO: be specific in point 2 below

-	collect the :math:`x`- and :math:`y`-values inside this window

-	calculate a fitted :math:`y`-value, but use a weighted least squares procedure, with weights that peak at the center of the window and declines towards the edges,

-	record that average :math:`y`-value against the window's center (:math:`x`-value)

-	slide the window along the :math:`x` axis and repeat

The *model* is the collection of these :math:`x`- and :math:`y`-values. This is why it is called nonparameteric: there are no parameters to quantify the model. For example: if the relationship between the two variables is linear, then a linear smooth is achieved. It is hard to express the relationship between :math:`x` and :math:`y` in written form, so usually these models are shown visually. The nonparametric model is not immune to outliers, but it is resistant to them.

More details can be found in W.S. Cleveland, `Robust Locally Weighted Regression and Smoothing Scatterplots <http://www.jstor.org/stable/2286407>`_, *Journal of the American Statistical Association*, **74** (368), p. 829-836, 1979.


Robust least squares models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: robust least squares

Outliers are often the most interesting observations and are usually the points from which we learn the most about the system. A manual step where we review the :index:`outliers <pair: outliers; least squares>` and their influence should always done for any important model. For example, inspection of the residual plots as described in the preceding sections.

However, the ability to build a linear model that is not heavily influenced by outliers might be of interest in certain cases.

*	The model is built automatically and is not reviewed by a human (e.g. as an intermediate step in a data-mining procedure). This is increasingly common in systems that build on top of the least squares model to improve their performance in some way.

*	The human reviewer is not skilled to know which plots to inspect for influential and discrepant observations, or may not know how to interpret these plots.

Some criticism of robust methods are that there are too many different robust methods and that these routines are much more computationally expensive than ordinary least squares. The first point is true, as this as a rapidly evolving field, however the latter objection is not of too much concern these days. Robust methods are now available in most decent software packages, and are stabilizing towards a few reliable robust estimators.

If you would like to read up some more, a nice introduction targeted at engineering readers is given in PJ Rousseeuw's "`Tutorial to Robust Statistics <http://dx.doi.org/10.1002/cem.1180050103>`_", *Journal of Chemometrics*, **5**, 1-20, 1991.

In R the various efforts of international researchers is being consolidated. The ``robustbase`` package provides basic functionality that is now well established in the field; use that package if you want to assemble various robust tools yourself. On the other hand, a more comprehensive package called ``robust`` is also available which provides robust tools that you should use if you are not too concerned with the details of implementation.

For example:

.. code-block:: s

	> data <- read.csv('http://openmv.net/file/distillation-tower.csv')

	# Using ordinary least squares
	# -----------------------------
	> summary(lm(data$VapourPressure ~ data$TempC2))

	Call:
	lm(formula = data$VapourPressure ~ data$TempC2)

	Residuals:
	     Min       1Q   Median       3Q      Max
	-5.59621 -2.37597  0.06674  2.00212 14.18660

	Coefficients:
	             Estimate Std. Error t value Pr(>|t|)
	(Intercept) 195.96141    4.87669   40.18   <2e-16 ***
	data$TempC2  -0.33133    0.01013  -32.69   <2e-16 ***
	---
	Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

	Residual standard error: 2.989 on 251 degrees of freedom
	Multiple R-squared: 0.8098,	Adjusted R-squared: 0.8091
	F-statistic:  1069 on 1 and 251 DF,  p-value: < 2.2e-16

	# Use robust least squares (with automatic selection of robust method)
	# --------------------------------------------------------------------
	> library(robust)
	> summary(lmRob(data$VapourPressure ~ data$TempC2))

	Call: lmRob(formula = data$VapourPressure ~ data$TempC2)

	Residuals:
	       Min         1Q     Median         3Q        Max
	-5.2631296 -1.9805384  0.1677174  2.1565730 15.8846460

	Coefficients:
	            Value        Std. Error   t value      Pr(>|t|)
	(Intercept) 179.48579886   4.92870640  36.41641120   0.00000000
	data$TempC2  -0.29776778   0.01021412 -29.15256677   0.00000000

	Residual standard error: 2.791 on 251 degrees of freedom
	Multiple R-Squared: 0.636099

	Test for Bias:
	            statistic     p-value
	M-estimate   7.962583 0.018661525
	LS-estimate 12.336592 0.002094802

In this example the two models perform similarly in terms on their :math:`S_E`, :math:`b_0` and :math:`b_1` values, as well as confidence intervals for them.

.. - Least angle least squares (regression)
.. see the Efron paper mentioned above
.. also note the rlm() function in MASS

Logistic modelling (regression)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: integer variables in least squares, logistic regression

There are many practical cases in engineering modelling where our |y|-variable is a discrete entity. The most common case is pass or failure, naturally coded as |y| = 0 for failure, and |y| = 1 is coded as success. Some examples:

	*	Predict whether our product specifications are achieved (|y| = 0 or 1) given the batch reaction's temperature as :math:`x_1`, the reaction duration :math:`x_2` and the reactor vessel, where :math:`x_3=0` for reactor A and :math:`x_3=1` for reactor B.
	
	*	Predict the likelihood of making a sale in your store (|y| = 0 or 1), given the customer's age :math:`x_1`, whether they are a new or existing customers, :math:`x_2` is either 0 or 1, and the day of the week as :math:`x_3`.
	
	*	Predict if the final product will be |y| = acceptable, medium, or unsellable based on the raw material's properties :math:`x_1, x_2, x_3` and the ambient temperature :math:`x_4`.

We could naively assume that we just code our |y| variable as 0 or 1 (pass/fail) and build our least squares model as usual, using the |x| variables. While a seemingly plausible approach, the problems are that:

	-	The predictions when using the model are not dichotomous (0 or 1), which is not too much of a problem if we interpret our prediction more as a probability. That is, our prediction is the probability of success or failure, according to how we coded it originally. However the predictions often lie outside the range :math:`[0, 1]`.  We can attempt to compensate for this by clamping the output to zero or one, but this non-linearity causes instability in the estimation algorithms.
	
	-	The errors are not normally distributed.
	
	-	The variance of the errors are not constant and the assumption of linearity breaks down.

.. image:: ../figures/least-squares/logistic-regression-function.png
	:scale: 40
	:width: 900px
	:align: right
	:alt: fake width

A logistic model however accounts for the nature of the y-variable by creating a function, called a logistic function, which is bounded between 0 and 1. In fact you are already familiar with such a function: the cumulative probability of the normal distribution does exactly this.

Once the :math:`y` data are appropriately transformed, then the model can be calculated. In R one uses the ``glm(y ~ x1 + x2, family=binomial)`` function to build a model where ``y`` must be a factor variable: type ``help(factor)`` to learn more. The model output is interpreted as any other.


Testing of least-squares models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: testing least squares models

Before launching into this concept, first step back and understand why we are building least squares models. One objective is to learn more about our systems: (a) what is the effect of one variable on another, or (b) is the effect significant (examine the confidence interval). Another objective is purely predictive: build a model so that we can use it to make predictions. For this last case we must test our model's capability for accurate predictions.

The gold standard is always to have a testing data set available to quantify how good (adequate) your least squares model is. It is important that (a) the test set has no influence on the calculation of the model parameters, and (b) is representative of how the model will be used in the future. We will illustrate this with 2 examples: you need to build a predictive model for product viscosity from 3 variables on your process. You have data available, once per day, for 2006 and 2007 (730 observations).

	*	Use observation 1, 3, 5, 7, ... 729 to build the least squares model; then use observation 2, 4, 6, 8, ... 730 to test the model.
	
	*	Use observations 1 to 365 (data from 2006) to build the model, and then use observations 366 to 730 (data from 2007) to test the model.

In both cases, the testing data has no influence on the model parameters. However the first case is not representative of how the model will be used in the future. The results from the first case are likely to give over-optimistic results, while the second case represents the intended use of the model more closely, and will have more honest results. Find out sooner, rather than later, that the model's long-term performance is not what you expect. It may be that you have to keep rebuilding the model every 3 months, updating the model with the most recent data, in order to maintain it's predictive performance.

How do we quantify this predictive performance?  A common way is to calculate the root mean square of the prediction error (:index:`RMSEP`), this is very similar to the :ref:`standard error <standard-error-section>` that we saw earlier for regression models. Assuming the errors are centered at zero and follow a normal distribution, the RMSEP can be interpreted as the standard deviation of the prediction residuals. It is important the RMSEP be calculated only from new, unseen testing data. By contrast, you might see the term RMSEE (root mean square error of estimation), which is the RMSEP, but calculated from the training (model-building) data. The :index:`RMSEE` :math:`\approx S_E` = standard error; the small difference being due to the denominator used (:math:`n` versus :math:`n-k`).

.. math::

	\text{RMSEP} = \sqrt{\dfrac{1}{n}\sum_{i}^{n}{\left(y_{\text{new}, i} - \hat{y}_{\text{new}, i}\right)^2}} \\


The units of RMSEP and RMSEE are the same as the units of the |y|-variable.

In the :ref:`latent variable modelling <SECTION_latent_variable_modelling>` section of the book we will introduce the concept of :index:`cross-validation` to test a model. Cross-validation uses the model training data to simulate the testing process. So it is not as desirable as having a fresh testing data set, but it works well in many cases. Cross-validation can be equally well applied to least squares models. We will revisit this topic later.

.. TODO: cf the book by Esbensen for other methods

.. TODO: see these bootstrap confidence intervals: https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html#the-bootstrap-method-and-empirical-confidence-intervals

.. TODO: add the topic of randomization here

Bootstrapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bootstrapping is an extremely useful tool when theoretical techniques to estimate confidence intervals and uncertainty are not available to us.

Let's give an example where :index:`bootstrapping` is strictly not required, but is definitely useful. When fitting a least squares model of the form :math:`y = \beta_0 + \beta_1 x` we are interested in the confidence interval of the slope coefficient, :math:`\beta_1`. Recall this coefficient indicates by how much the |y|-variable changes on average when changing the |x| variable by one unit. The slope coefficient might represent a rate constant, or be related to the magnitude of the feedback control loop gain. Whatever the case, it is important we understand the degree of uncertainty associated with it, so we can make an appropriate judgement.

In the preceding section on least squares model analysis we :ref:`derived this confidence interval <LS_eqn_least-squares-CI>` for :math:`\beta_1`, repeated here:

	.. math::
		
		\begin{array}{rcccl}
			- c_t                  &\leq& \dfrac{b_1 - \beta_1}{S_E(b_1)} &\leq &  +c_t\\
			  b_1 - c_t S_E(b_1)   &\leq& \beta_1                         &\leq&	b_1 + c_t S_E(b_1)
		\end{array}

Visualize this confidence in the context of the following example where |x| is the dose of radiation administered (rads), and |y| is the survival percentage. The plot shows the data and the least square slope coefficient (notice the |y| variable is a transformed variable, ``log(survival)``).

The thick line represents the slope coefficient (:math:`-0.0059`) using all the data. Clearly the unusual point number 13 has some influence on that coefficient. Eliminating it and refitting the model makes the slope coefficient more steep (:math:`-0.0078`), which could change our interpretation of the model. This raises the question though: what happens to the slope coefficient when we eliminate other points in the training data?  How sensitive are our model parameters *to the data themselves*?

	.. image:: ../figures/least-squares/bootstrap-example.png
		:align: center
		:width: 900px
		:scale: 65
		:alt: fake width

Bootstrapping gives us an indication of that sensitivity, as shown in the other plot. The original data set had 14 observations. What bootstrapping does is to randomly select 14 rows from the original data, allowing for duplicate selection. These selected rows are used to build a least squares model, and the slope coefficient is recorded. Then another 14 random rows are selected and this process is repeated ``R`` times (in this case ``R=1000``). On some of these occasions the outlier points will be included, and other times they will be excluded. 

A histogram of the 1000 computed slope coefficients is shown here. This histogram gives us an additional indication of the uncertainty of the slope coefficient. It shows many possible slope coefficients that could have been obtained. One in particular has been marked, the slope when point 13 was omitted.

For completeness the confidence interval at the 95% level for :math:`\beta_1` is calculated here, and also superimposed on the histogram.

.. math::
	
	\begin{array}{rcccl}
		- c_t                  					&\leq& \dfrac{b_1 - \beta_1}{S_E(b_1)} &\leq &  +c_t\\
		  -0.005915 - 2.1788 \times 0.001047  	&\leq& \beta_1   &\leq&	-0.005915 + 2.1788 \times 0.001047 \\
		  -0.0082 								&\leq& \beta_1   &\leq& -0.0036
	\end{array}

This confidence interval, together with the bootstrapped values of :math:`b_1` give us additional insight when when making our interpretation of :math:`b_1`. 

By now you should also be wondering whether you can bootstrap the confidence interval bounds! That's left as exercise for interested readers. The above example was inspired from an example in `ASA Statistics Computing and Graphics <http://stat-computing.org/newsletter/>`_, **13** (1), 2002.

.. Give R example source code for bootstrapping.

.. Ridge least squares (regression)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. Variable selection and stepwise regression
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	The variable selection problem is ...

	We will start off by saying that variable selection is a topic that is widely and actively researched.

