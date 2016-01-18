Least squares model analysis
====================================

Once we have fitted the |b0| and |b1| terms using the data and the equations from :ref:`the prior section <LS_eqn_define-2-LS-b0-b1-result>`, it is of interest to know how well the model performed. That is what this section is about. In particular:

#.	Analysis of variance: breaking down the data's variability into components

#.	Confidence intervals for the model coefficients, :math:`b_0` and :math:`b_1`

#.	Prediction error estimates for the :math:`y`-variable

#.	We will also take a look at the interpretation of the software output.

In order to perform the second part we need to make a few assumptions about the data, and if the data follow those assumptions, then we can derive confidence intervals for the model parameters.

The variance breakdown
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=xIjAD_6nXto&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=20

Recall that :ref:`variability <univariate-about-variability>` is what makes our data interesting. Without variance (i.e. just flat lines) we would have nothing to do. The :index:`analysis of variance` is just a tool to show how much variability in the :math:`y`-variable is explained by:

 	#.	Doing nothing (no model: this implies :math:`\hat{y} = \overline{y}`)
 	#.	The model (:math:`\hat{y}_i = b_0 + b_1 x_i`)
 	#.	How much variance is left over in the errors, :math:`e_i`

These 3 components must add up to the total variance we started with. By definition, the variance is computed about a mean, so the variance of no model (i.e. the "doing nothing" case) is zero. So the total variance in vector :math:`y` is just the sum of the other two variances: the model's variance, and the error variance. We show this next.

.. The variance breakdown: graphically
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the accompanying figure, we see that geometrically, at any fixed value of :math:`x_i`, that any :math:`y` value above or below the least squares line, call it :math:`y_i` and shown with a circle, must obey the distance relationship:

.. math::
	
	\begin{array}{lrcl}
		\text{Distance relationship:} & (y_i - \overline{\mathrm{y}})         &=& (\hat{y}_i - \overline{\mathrm{y}}) + (y_i - \hat{y}_i) \\
		\text{Squaring both sides:}   & (y_i - \overline{\mathrm{y}})^2       &=& (\hat{y}_i - \overline{\mathrm{y}})^2 + 2(\hat{y}_i - \overline{\mathrm{y}})(y_i - \hat{y}_i) + (y_i - \hat{y}_i)^2 \\
		\text{Sum and simplify:}      & \sum{(y_i - \overline{\mathrm{y}})^2} &=& \sum{(\hat{y}_i - \overline{\mathrm{y}})^2} + \sum{(y_i - \hat{y}_i)^2} \\
		                              & \text{Total sum of squares (TSS)} &=& \text{Regression SS (RegSS)} + \text{Residual SS (RSS)}
	\end{array}

.. image:: ../figures/least-squares/ANOVA-graphically.png
	:width: 900px
	:align: center
	:scale: 60
	:alt: fake width

The total sum of squares (TSS) is the total variance in the vector of :math:`y`-data. This broken down into two components: the sum of squares due to regression, :math:`\sum \left(\hat{y}_i - \overline{y}\right)^2`, called RegSS, and the sum of squares of the residuals (RSS), :math:`\sum e_i^2 = e^T e`.


It is convenient to write these sums of squares (variances) in table form, called an Analysis of Variance (:index:`ANOVA`) table:

	=================== ========================================= ================================================ ======= ========================================
	Type of variance    Distance                                  Degrees of freedom                               SSQ     Mean square
	=================== ========================================= ================================================ ======= ========================================
	Regression          :math:`\hat{y}_i - \overline{y}`          :math:`k` (:math:`k=2` in the examples so far)   RegSS   :math:`\text{RegSS}/k`
	------------------- ----------------------------------------- ------------------------------------------------ ------- ----------------------------------------
	Error               :math:`y_i - \hat{y}_i`                   :math:`n-k`                                      RSS     :math:`\text{RSS}/(n-k)`
	------------------- ----------------------------------------- ------------------------------------------------ ------- ----------------------------------------
	Total               :math:`y_i - \overline{y}`                :math:`n`                                        TSS     :math:`\text{TSS}/n`
	=================== ========================================= ================================================ ======= ========================================

..	Original table in wiki form

		{| class="wikitable"
		|-
		! Type of variance
		! Distance
		! Degrees of freedom
		! SSQ
		! Mean square
		|-
		| Regression
		| :math:`\hat{y}_i - \overline{\mathrm{y}}`
		| :math:`k` (k=2 in the examples so far)
		| RegSS
		| :math:`RegSS/k`
		|-
		| Error
		| :math:`y_i - \hat{y}_i`
		| :math:`n-k`
		| RSS
		| :math:`RSS/(n-k)`
		|-
		|
		|
		|
		|
		|-
		| Total
		| :math:`y_i - \overline{\mathrm{y}}`
		| :math:`n`
		| TSS
		| :math:`TSS/n`
		|}


.. _standard-error-section:

Interpreting the standard error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The term :math:`S_E^2 = \text{RSS}/(n-k)` is one way of quantifying the model's performance. The value :math:`S_E = \sqrt{\text{RSS}/(n-k)} = \sqrt{(e^Te)/(n-k)}` is called the :index:`standard error`. It is really just the standard deviation of the error term, accounting correctly for the degrees of freedom.

*Example*: Assume we have a model for predicting batch yield in kilograms from |x| = raw material purity, what does a standard error of 3.4 kg imply?

*Answer*: Recall if the assumption of normally distributed errors is correct, then this value of 3.4 kg indicates that about two thirds of the yield predictions will lie within :math:`\pm 3.4` kg, and that 95% of the yield predictions will lie within :math:`\pm 2 \times 3.4` kg. We will quantify the prediction interval more precisely, but the standard error is a good approximation for the error of |y|.

Exercise
^^^^^^^^^

For two extreme cases:

#. :math:`y_i = e_i`, i.e. where :math:`b_0 = 0` and :math:`b_1 = 0`. In other words, our :math:`y_i` measurements are just random noise.
#. :math:`y_i = b_0 + b_1 x_i + e_i`, for any values of :math:`b_0` and :math:`b_1`, that model fits the data perfectly, with no residuals.

Do the following:

 	- draw a generic plot
	- create an ANOVA table with fake values
 	- write down the value of the ratio :math:`\dfrac{\text{RegSS}}{\text{TSS}}`
	- interpret what this ratio means: :math:`F_0 = \dfrac{\text{mean square of regression}}{\text{mean square of residuals}}`

.. raw:: latex

	\vspace{2cm}

From this exercise we learn that:

-	The null model (:math:`y_i = e_i`) has ratio :math:`\dfrac{\text{RegSS}}{\text{TSS}} = 0`.
-	Models where the fit is perfect have a ratio :math:`\dfrac{\text{RegSS}}{\text{TSS}} = 1`. This number is called :math:`R^2`, and we will see why it is called that next.


.. The variance breakdown: algebraically
	^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	For those of you that prefer to understand concepts algebraically, you can get the equivalent result by starting with the definition of the variance of :math:`\mathrm{y}`.

	.. todo:: check this still: there is a mistake in the middle line

	.. math::

		\mathcal{V}\{\mathrm{y}\} 	&= \mathcal{E}\{(\mathrm{y}-\overline{\mathrm{y}})^2\} \\
						 			&= \mathcal{E}\{(b_0 + b_1 \mathrm{x} + e - \overline{\mathrm{y}})^2\} \\
						 			&= \mathcal{E}\{(b_0 + b_1 \mathrm{x} + e)^2\} \\
						 			&= \mathcal{E}\{(b_0 + b_1 \mathrm{x} + e)^2\} \\
						 			&= \mathcal{V}\{b_0 + b_1 \mathrm{x}\} + \mathcal{V}\{e\} + 2\text{Cov}\{b_0 + b_1 \mathrm{x}, e\}

	Since the covariance between the predicted |y| value and the residuals is zero (we proved that earlier with :math:`\mathrm{\hat{y}}^T\mathrm{e} = 0`), we have:

	.. math::

		\mathcal{V}\{\mathrm{y}\} 	&= \mathcal{V}\{b_0 + b_1 \mathrm{x}\} + \mathcal{V}\{e\} \\
									&= \mathcal{V}\{\hat{\mathrm{y}}\} + \mathcal{V}\{e\}


Derivation of :math:`R^2`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. index:: R2 (correlation coefficient)

.. To use this derivation you have to work in deviation variables (x-mean(x)) and (y-mean(y)). Too early in the notes to do that.
	.. image:: ../figures/least-squares/angle-between-two-vectors.png
		:width: 400px
		:align: center

	Recall, perhaps from a second year math course, that the cosine of the angle between any two vectors, :math:`a` and :math:`b` is related to the vector dot product

	.. math::
	
		\cos \theta_{ab} = \dfrac{a^Tb}{\|a\| \|b\|}

As introduced by example in the previous part, :math:`R^2 = \dfrac{\text{RegSS}}{\text{TSS}} = \dfrac{\sum_i{ \left(\hat{y}_i - \overline{\mathrm{y}}\right)^2}}{\sum_i{ \left(y_i - \overline{\mathrm{y}}\right)^2}}`: simply the ratio between the variance we can explain with the model (RegSS) and the total variance we started off with (TSS). We can also write that :math:`R^2 = 1-\dfrac{\text{RSS}}{\text{TSS}}`, based on the fact that TSS = RegSS + RSS.

From the above ratios it is straightforward to see that if :math:`R^2 = 0`, it requires that :math:`\hat{y}_i = \overline{\mathrm{y}}`: we are predicting just a flat line, the mean of the |y| data. On the other extreme, an :math:`R^2 = 1` implies that :math:`\hat{y}_i = y_i`, we have perfect predictions for every data point.

The nomenclature :math:`R^2` comes from the fact that it is the square of the correlation between |x| and |y|. Recall from the :ref:`correlation section <LS_correlation>` that

.. math::

	r(x, y) = \dfrac{\mathcal{E}\left\{ (x - \overline{x}) (y - \overline{y})\right\}}{\sqrt{\mathcal{V}\left\{x\right\}\mathcal{V}\left\{y\right\}}} = \dfrac{\text{Cov}\left\{x, y\right\}}{\sqrt{\mathcal{V}\left\{x\right\}\mathcal{V}\left\{y\right\}}}

and can range in value from :math:`-1` to :math:`+1`. The :math:`R^2` ranges from 0 to +1, and is the square of :math:`r(x,y)`. :math:`R^2` is just a way to tell how far we are between predicting a flat line (no variation) and the extreme of being able to predict the model building data, :math:`y_i`, exactly.

The :math:`R^2` value is likely well known to anyone that has encountered least squares before. This number must be interpreted with caution. It is most widely **abused** as a way to measure "*how good is my model*".

These two common examples illustrate the abuse. You likely have said or heard something like this before:

	#.	"the :math:`R^2` value is really high, 90%, so this is a good model".
	#.	"Wow, that's a really low :math:`R^2`, this model can't be right - it's no good".

How **good** a model is *for a particular purpose* is almost never related to the :math:`R^2` value. The goodness of a model is better assessed by:

- your engineering judgment: does the *interpretation* of model parameters make sense?
- use testing data to verify the model's predictive performance,
- using cross-validation tools (we will see this topic later on).

We will see later on that :math:`R^2` can be arbitrarily increased by adding terms to the linear model, as we will see in the section on :ref:`multiple linear regression (MLR) <LS_multiple_X_MLR>`. So sometimes you will see the adjusted :math:`R^2` used to account for the :math:`k` terms used in the model:

.. math::

	R^2_\text{adj} = 1 - \dfrac{\text{RSS}/(n-k)}{\text{TSS}/(n-1)}

where :math:`k=2` for the case of estimating a model :math:`y_i = b_0 + b_1 x_i`, as there are 2 parameters.


Confidence intervals for the model coefficients |b0| and |b1|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. Note:: A good reference for this section is the book by Fox (Chapter 6), and the book by Draper and Smith.

Up to this point we have made no assumptions about the data. In fact we can calculate the model estimates, |b0| and |b1| as well as predictions from the model without any assumptions on the data. It is only when we need additional information such as :index:`confidence intervals <pair: confidence interval; least squares>` for the coefficients and prediction error estimates that we must make assumptions.

Recall the |b1| coefficient represents the average effect on |y| when changing the |x|-variable by 1 unit. Let's say you are estimating a reaction rate (kinetics) from a linear least squares model, a standard step in reactor design, you would want a measure of confidence of your coefficient. For example, if you calculate the reaction rate as :math:`k = b_1 = 0.81 \,\text{s}^{-1}` you would benefit from knowing whether the 95% confidence interval was :math:`k = 0.81 \pm 0.26 \,\text{s}^{-1}` or :math:`k = 0.81 \pm 0.68 \,\text{s}^{-1}`. In the latter case it is doubtful whether the reaction rate is of practical significance. Point estimates of the least squares model parameters are satisfactory, but the confidence interval information is richer to interpret.

We first take a look at some assumptions in least squares modelling, then return to deriving the confidence interval.

.. _LS-assumptions:

Assumptions required for analysis of the least squares model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
	pair: least squares; assumptions for
	
.. youtube:: https://www.youtube.com/watch?v=Qls1R2HOzy0&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=21

Recall that the population (true) model is :math:`y_i = \beta_0 + \beta_1 x_i + \epsilon_i` and :math:`b_0` and :math:`b_1` are our estimates of the model's coefficients, and :math:`\mathrm{e}` be the estimate of the true error :math:`\epsilon`. Note we are assuming imperfect knowledge of the :math:`y_i` by lumping all errors into :math:`e_i`. For example, measurement error, structural error (we are not sure the process follows a linear structure), inherent randomness, and so on.

Furthermore, our derivation for the confidence intervals of |b0| and |b1| requires that we assume:

#.	Linearity of the model, and that the values of |x| are fixed (have no error). This implies that the error captured by :math:`\epsilon` is the error of |y|, since the :math:`\beta_0 + \beta_1 \mathrm{x}` terms are fixed.

	-	In an engineering situation this would mean that your |x| variable has much less uncertainty than the |y| variable; and is often true in many situations.

#.	The variance of |y| is the same (constant) at all values of |x|, known as the constant error variance assumption.

	-	The variability of |y| can be non-constant in several practical cases (e.g. our measurement accuracy deteriorates at extreme high and low levels of |x|).

	.. image:: ../figures/least-squares/constant-error-variance.png
		:width: 900px
		:align: center
		:scale: 60
		:alt: fake width
		
	Illustration of the constant error variance assumption and the normally distributed error assumption.

#.	The errors are normally distributed: :math:`e_i \sim \mathcal{N}(0, \sigma_\epsilon^2)`. This also implies that :math:`y_i \sim \mathcal{N}(\beta_0 + \beta_1x_i, \sigma_\epsilon^2)` from the first linearity assumption.

#.	Each error is independent of the other. This assumption is often violated in cases where the observations are taken in time order on slow moving processes (e.g. if you have a positive error now, your next sample is also likely to have a positive error). We will have more to say about this later when we check for independence with an :ref:`autocorrelation test <LS-autocorrelation-test>`.

#.	In addition to the fact that the |x| values are fixed, we also assume they are independent of the error. If the |x| value is fixed (i.e. measured without error), then it is already independent of the error.

	- When the |x| values are not fixed, there are cases where the error gets larger as |x| gets smaller/larger.

#.	All :math:`y_i` values are independent of each other. This again is violated in cases where the data are collected in time order and the :math:`y_i` values are autocorrelated.

.. note:: Derivation of the model's coefficients do not require these assumptions, only the derivation of the coefficient's confidence intervals require this. 

Also, if we want to interpret the model's :math:`S_E` as the estimated standard deviation of the residuals, then it helps if the residuals are normally distributed.

.. _LS-CI-for-model-parameters:

Confidence intervals for :math:`\beta_0` and :math:`\beta_1`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recall from our discussions on :ref:`confidence intervals <univariate_confidence_intervals>` that we need to know the mean and variance of the population from which |b0| and |b1| come. Specifically for the least squares case:

.. math::

	\begin{array}{lcr}
		b_0 \sim \mathcal{N}(\beta_0, \mathcal{V}\{\beta_0\}) &\qquad\text{and}\qquad& b_1 \sim \mathcal{N}(\beta_1,\mathcal{V}\{\beta_1\})
	\end{array}

Once we know those parameters, we can create a :math:`z`-value for |b0| and |b1|, and then calculate the confidence interval for :math:`\beta_0` and :math:`\beta_1`. So our quest now is to calculate :math:`\mathcal{V}\{\beta_0\}` and :math:`\mathcal{V}\{\beta_1\}`, and we will use the 6 assumptions we made in the previous part.

Start from the equations that define |b0| and |b1| :ref:`in the prior section <LS_eqn_define-2-LS-b0-b1-result>` where we showed that:

.. math::

	\begin{array}{rclrcl}
		b_0 &=& \overline{\mathrm{y}} - b_1\overline{\mathrm{x}}  \\ \\
    	b_1 &=& \dfrac{ \sum_i{\left(x_i - \overline{\mathrm{x}}\right)\left(y_i - \overline{\mathrm{y}}\right) } }{ \sum_i{\left( x_i - \overline{\mathrm{x}}\right)^2}}\\ \\
    	b_1 &=& \sum{m_iy_i} &\text{where} \qquad m_i &=& \dfrac{x_i - \overline{\mathrm{x}}}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}
	\end{array}

That last form of expressing :math:`b_1` shows that every data point contributes a small amount to the coefficient :math:`b_1`. But notice how it is broken into 2 pieces: each term in the sum has a component due to :math:`m_i` and one due to :math:`y_i`. The :math:`m_i` term is a function of the x-data only, and since we assume the x's are measured without error, that term has no error. The :math:`y_i` component is the only part that has error.

So we can write:

.. math::

        b_1 &= m_1y_1 + m_2y_2 + \ldots + m_Ny_N \\
        \mathcal{E}\{b_1\} &= \mathcal{E}\{m_1y_1\} + \mathcal{E}\{m_2y_2\} + \ldots + \mathcal{E}\{m_Ny_N\} \\
        \mathcal{V}\{b_1\} &= m_1^2\mathcal{V}\{y_1\} + m_2^2 \mathcal{V}\{y_2\} + \ldots + m_N^2\mathcal{V}\{y_N\} \\
        \mathcal{V}\{b_1\} &= \sum_i{ \left( \dfrac{x_i - \overline{\mathrm{x}}}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}} \right)^2   } \mathcal{V}\{y_i\} \\
        \mathcal{V}\{b_1\} &= \dfrac{\mathcal{V}\{y_i\}}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}

**Questions**:

#.	So now apart from the numerator term, how could you decrease the error in your model's |b1| coefficient?

	- Use samples that are far from the mean of the |x|-data.
	
	- Use more samples.

#.	What do we use for the numerator term :math:`\mathcal{V}\{y_i\}`?

	-	This term represents the variance of the :math:`y_i` values at a given point :math:`x_i`. If (a) there is no evidence of lack-of-fit, and (b) if |y| has the same error at all levels of |x|, then we can write that :math:`\mathcal{V}\{y_i\}` = :math:`\mathcal{V}\{e_i\}  = \dfrac{\sum{e_i^2}}{n-k}`, where :math:`n` is the number of data points used, and :math:`k` is the number of coefficients estimated (2 in this case). The :math:`n-k` quantity is the degrees of freedom.

Now for the variance of :math:`b_0 = \overline{\mathrm{y}} - b_1 \overline{\mathrm{x}}`. The only terms with error are :math:`b_1`, and :math:`\overline{\mathrm{y}}`. So we can derive that:

.. math::

	\mathcal{V}\{b_0\} = \left(\dfrac{1}{N} + \dfrac{\overline{\mathrm{x}}^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}} \right)\mathcal{V}\{y_i\}

**Summary of important equations**

.. math::

	\mathcal{V}\{\beta_0\} \approx \mathcal{V}\{b_0\} &= \left(\dfrac{1}{N} + \dfrac{\overline{\mathrm{x}}^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}} \right)\mathcal{V}\{y_i\} \\ \\
	\mathcal{V}\{\beta_1\} \approx \mathcal{V}\{b_1\} &= \dfrac{\mathcal{V}\{y_i\}}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}} \\ \\
	\text{where}\qquad \mathcal{V}\{y_i\} &= \mathcal{V}\{e_i\}  = \dfrac{\sum{e_i^2}}{n-k}, \text{~if there is no lack-of-fit and the y's are independent of each other}.

For convenience we will define some short-hand notation, which is common in least squares:

.. math::

	S_E^2 &= \mathcal{V}\{e_i\}  = \mathcal{V}\{y_i\} = \dfrac{\sum{e_i^2}}{n-k} \qquad\qquad \text{or~~} S_E = \sqrt{ \dfrac{\sum{e_i^2}}{n-k} }\\
	S_E^2(b_0) &= \mathcal{V}\{b_0\} = \left(\dfrac{1}{N} + \dfrac{\overline{\mathrm{x}}^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}} \right)S_E^2\\
	S_E^2(b_1) &= \mathcal{V}\{b_1\} = \dfrac{S_E^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}

You will see that :math:`S_E` is an estimate of the standard deviation of the error (residuals), while :math:`S_E(b_0)` and :math:`S_E(b_1)` are the standard deviations of estimates for |b0| and |b1| respectively.

Now it is straight forward to construct **confidence intervals for the least squares model parameters**. You will also realize that we have to use the :math:`t`-distribution, because we are using an estimate of the variance.

.. _LS_eqn_least-squares-CI:
.. math::
	:label: least-squares-CI

	\begin{array}{rccclrcccl}
		- c_t                &\leq& \dfrac{b_0 - \beta_0}{S_E(b_0)} &\leq &  +c_t               &\qquad- c_t                &\leq& \dfrac{b_1 - \beta_1}{S_E(b_1)} &\leq &  +c_t\\
		b_0 - c_t S_E(b_0)   &\leq& \beta_0                         &\leq&	b_0 + c_t S_E(b_0)  &\qquad b_1 - c_t S_E(b_1)   &\leq& \beta_1                         &\leq&	b_1 + c_t S_E(b_1)
	\end{array}

**Example**


.. youtube:: https://www.youtube.com/watch?v=sY8CVMGUD54&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=22

Returning :ref:`back to our ongoing example <LS-class-example>`, we can calculate the confidence interval for :math:`\beta_0` and :math:`\beta_1`. We calculated earlier already that |b0| = 3.0 and |b1| = 0.5. Using these values we can calculate the standard error:

.. code-block:: s

	# Assume you have calculated "b0" and "b1" already using vectors "x" and "y"

	> predictions <- b0 + x*b1
	> predictions
	[1]  8.001  7.000  9.501  7.501  8.501  10.001  6.00  5.000  9.001  6.500  5.501
	> error <- y - predictions
	> SE <- sqrt(sum(error^2) / (N-2))
	> SE
	1.236603

Use that :math:`S_E` value to calculate the confidence intervals for :math:`\beta_0` and :math:`\beta_1`, and use that :math:`c_t = 2.26` at the 95% confidence level. You can calculate  this value in R using ``qt(0.975, df=(N-2))``. There are :math:`n-2` degrees of freedom, the number of degrees of freedom used to calculate :math:`S_E`.

First calculate the :math:`S_E` value and the standard errors for the |b0| and |b1|. Substitute these into the equation for the confidence interval and calculate:

.. math::

	S_E & = 1.237 \\
	S_E^2(b_1) &= \dfrac{S_E^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}} = \dfrac{1.237^2}{110} = 0.0139\\
	S_E^2(b_0) &= \left(\dfrac{1}{N} + \dfrac{\overline{\mathrm{x}}^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}} \right)S_E^2 = \left(\dfrac{1}{11} + \dfrac{9^2}{110} \right)1.237^2 = 1.266

The 95% confidence interval for :math:`\beta_0`:

.. math::

	
	\begin{array}{rccclrcccl}
		- c_t                &\leq& \dfrac{b_0 - \beta_0}{S_E(b_0)} &\leq &  +c_t               \\
		3.0 - 2.26 \times \sqrt{1.266}  &\leq& \beta_0   &\leq&	3.0 + 2.26 \times \sqrt{1.266}   \\
		0.457 &\leq& \beta_0   &\leq&	5.54
	\end{array}


The confidence interval for :math:`\beta_1`:

.. math::

	\begin{array}{rccclrcccl}
		- c_t                &\leq& \dfrac{b_1 - \beta_1}{S_E(b_1)} &\leq &  +c_t               \\
		0.5 - 2.26 \times \sqrt{0.0139}   &\leq& \beta_1                         &\leq& 0.5 + 2.26 \times \sqrt{0.0139}\\
		0.233  &\leq& \beta_1                         &\leq& 0.767	\\
	\end{array}

The plot shows the effect of varying the slope parameter, :math:`b_1`, from its lower bound to its upper bound. Notice that the slope always passes through the mean of the data :math:`(\overline{x}, \overline{y})`.

.. image:: ../figures/least-squares/show-anscome-solution-marked.png
	:width: 750px
	:align: center
	:scale: 50

In many cases the confidence interval for the intercept is not of any value because the data for |x| is so far away from zero, or the true value of the intercept is not of concern for us.


Prediction error estimates for the y-variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=N8NF1_CBTw4&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=23

Apart from understanding the error in the model's coefficient, we also would like an estimate of the error when predicting :math:`\hat{y}_i` from the model, :math:`y_i = b_0 + b_1 x_i + e_i` for a new value of :math:`x_i`. This is known as the :index:`prediction interval`, or :index:`prediction error interval`.

A naive first attempt
^^^^^^^^^^^^^^^^^^^^^^^

We might expect the error is related to the average size of the residuals. After all, :ref:`our assumptions we made earlier <LS-assumptions>` showed the standard error of the residuals was the standard error of the |y|: :math:`S_E^2 = \mathcal{V}\left\{e_i\right\} = \mathcal{V}\left\{y_i\right\} = \dfrac{\sum{e_i^2}}{n-k}`.

.. image:: ../figures/least-squares/residual-plots.png
	:width: 900px
	:align: center
	:scale: 80
	:alt: fake width

A typical histogram of the residuals looks as shown here: it is always centered around zero, and appears to be normally distributed. So we could expect to write our prediction error as :math:`\hat{y}_\text{new} = \left(b_0 + b_1 x_\text{new}\right) \pm c \cdot S_E`, where :math:`c` is the number of standard deviations around the average residual, for example we could have set :math:`c=2`, approximating the 95% confidence limit.

But there is something wrong with that error estimate. It says that our prediction error is constant at any value of :math:`x_i`, even at values far outside the range where we built the model. This is a naive estimate of the prediction error. We have forgotten that coefficients :math:`b_0` and :math:`b_1` have error, and that error must be propagated into :math:`\hat{y}_\text{new}`.

.. CHECK THIS STILL

This estimate is however a reasonable guess for the prediction interval when you only know the model's :math:`S_E` and don't have access to a calculator or computer to calculate the proper prediction interval, shown next.

A better attempt to construct prediction intervals for the least squares model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Note:: A good reference for this section is Draper and Smith, *Applied Regression Analysis*, page 79.

.. As is Devore, Probability and statistics for engineering and the sciences, page 506

The derivation for the :index:`prediction interval` is similar to that for |b1|. We require an estimate for the variance of the predicted |y| at at given value of |x|. Let's fix our |x| value at :math:`x_*` and since :math:`b_0 = \overline{\mathrm{y}} - b_1 \overline{\mathrm{x}}`, we can write the prediction at this fixed |x| value as :math:`\hat{y}_* = \overline{\mathrm{y}} - b_1(x_* - \overline{\mathrm{x}})`.

.. math::

        \mathcal{V}\{y_*\} &= \mathcal{V}\{\overline{\mathrm{y}}\} + \mathcal{V}\{b_1(x_* - \overline{\mathrm{x}})\} + 2 \text{Cov}\{\overline{\mathrm{y}}, b_1(x_* - \overline{\mathrm{x}})\} \\
        \mathcal{V}\{y_*\} &= \dfrac{S_E^2}{n} + (x_* - \overline{\mathrm{x}})^2 S_E^2(b_1) + 0

You may read the reference texts for the interesting derivation of this variance. However, this is only the variance of the average predicted value of |y|. In other words, it is the variance we expect if we repeatedly brought in observations at :math:`x_*`. The prediction error of an individual observation, :math:`x_i`, and its corresponding prediction, :math:`\hat{y}_i`, is inflated slightly further:

:math:`\mathcal{V}\{\hat{y}_i\} = S_E^2\left(1 + \dfrac{1}{n} + \dfrac{(x_i - \overline{\mathrm{x}})^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}\right)`, where :math:`j` is the index for all points used to build the least squares model.

We may construct a prediction interval in the standard manner, assuming that :math:`\hat{y}_i \sim \mathcal{N}\left( \overline{\hat{y}_i}, \mathcal{V}\{\hat{y}_i\} \right)`. We will use an estimate of this variance since we do not know the population variance. This requires we use the :math:`t`-distribution with :math:`n-k` degrees of freedom, at a given degree of confidence, e.g. 95%.

.. math::
	
    \begin{array}{rcccl}
        -c_t &<& \dfrac{\hat{y}_i - \overline{\hat{y}_i}}{\sqrt{V\{\hat{y}_i\}}} &<& +c_t \\
        \hat{y}_i -c_t \sqrt{V\{\hat{y}_i\}} &<& \overline{\hat{y}_i} &<& \hat{y}_i + c_t \sqrt{V\{\hat{y}_i\}}
    \end{array}

This is a prediction interval for a new prediction, :math:`\hat{y}_i` given a new |x| value, :math:`x_i`. For example, if :math:`\hat{y}_i` = 20 at a given value of :math:`x_i`, and if :math:`c_t \sqrt{V\{\hat{y}_i\}}` = 5, then you will usually see written in reports and documents that, the prediction was :math:`20 \pm 5`. A more correct way of expressing this concept is to say the true prediction at the value of :math:`x_i` lies within a bound from 15 to 25, with 95% confidence.

Implications of the prediction error of a new |y|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's understand the interpretation of :math:`\mathcal{V}\{\hat{y}_i\} = S_E^2 \left(1 + \dfrac{1}{n} + \dfrac{(x_i - \overline{\mathrm{x}})^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}\right)` as the variance of the predicted :math:`\hat{y}_i` at the given value of :math:`x_i`. Using the previous example where we calculated the least squares line, now:

#.	Now let's say our :math:`x_\text{new}` happens to be :math:`\overline{\mathrm{x}}`, the center point of our data. Write down the upper and lower value of the prediction bounds for the corresponding :math:`\hat{y}`, given that :math:`c_t = 2.26` at the 95% confidence level.

	- The LB = :math:`\hat{y}_i - c_t \sqrt{V\{\hat{y}_i\}} = 7.5 - 2.26 \times \sqrt{(1.236)^2  \left(1+\dfrac{1}{11} + \dfrac{(\overline{\mathrm{x}} - \overline{\mathrm{x}})^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}\right)} = 7.5 - 2.26  \times 1.29 = 7.50 - 2.917 = 10.4`
	
	- The UB = :math:`\hat{y}_i + c_t \sqrt{V\{\hat{y}_i\}} = 7.5 + 2.26 \times \sqrt{(1.236)^2  \left(1+\dfrac{1}{11} + \dfrac{(\overline{\mathrm{x}} - \overline{\mathrm{x}})^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}\right)} = 7.5 + 2.26 \times 1.29 = 7.50 + 2.917 = 4.58`

#.	Now move left and right, away from :math:`\overline{\mathrm{x}}`, and mark the confidence intervals. What general shape do they have?

	-	The confidence intervals have a quadratic shape due to the square term under the square root. The smallest prediction error will always occur at the center of the model, and expands progressively wider as one moves away from the model center. This is illustrated in the figure and makes intuitive sense as well.

	.. image:: ../figures/least-squares/show-anscome-solution-with-yhat-bounds.png
		:width: 900px
		:align: center
		:scale: 60

Interpretation of software output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To complete this section we show how to interpret the output from computer software packages. Most packages have very standardized output, and you should make sure that whatever package you use, that you can interpret the estimates of the parameters, their confidence intervals and get a feeling for the model's performance.

The following output is obtained in R for the :ref:`example <LS-class-example>` we have been using in this section.

.. code-block:: text

	> x <- c(10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5)
	> y <- c(8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68)
	> model <- lm(y ~ x)    # "The linear model, where y is described by x"
	> summary(model)

	Call:
	lm(formula = y ~ x)

	Residuals:
	     Min       1Q   Median       3Q      Max
	-1.92127 -0.45577 -0.04136  0.70941  1.83882

	Coefficients:
	            Estimate Std. Error t value Pr(>|t|)
	(Intercept)   3.0001     1.1247   2.667  0.02573 *
	x             0.5001     0.1179   4.241  0.00217 **
	---
	Signif. codes:  0 `***' 0.001 `**' 0.01 `*' 0.05 `.' 0.1 ` ' 1

	Residual standard error: 1.237 on 9 degrees of freedom
	Multiple R-squared: 0.6665,	Adjusted R-squared: 0.6295
	F-statistic: 17.99 on 1 and 9 DF,  p-value: 0.002170

Make sure you can calculate the following values using the equations developed so far, and the above software output:

	- The intercept term |b0| = 3.0001.
	- The slope term |b1| = 0.5001.
	- The standard error of the model, :math:`S_E` = 1.237, using :math:`n-k = 11 - 2 = 9` degrees of freedom.
	- Using the standard error, calculate the standard error for the intercept = :math:`S_E(b_0) = 1.1247`.
	- Using the standard error, calculate the standard error for the slope = :math:`S_E(b_1) = 0.1179`.
	- The :math:`z`-value for the |b0| term is 2.667 (R calls this the ``t value`` in the printout, but in our notes we have called this :math:`z = \dfrac{b_0 - \beta_0}{S_E(b_0)}`; the value that we compare to the :math:`t`-statistic and used to create the confidence interval).
	- The :math:`z`-value for the |b1| term is 4.241 (see the above comment again).
	- The two probability values, ``Pr(>|t|)``, for |b0| and |b1| should be familiar to you; they are the probability with which we expect to find a value of :math:`z` greater than the calculated :math:`z`-value (called ``t value`` in the output above). The smaller the number, the more confident we can be the confidence interval contains the parameter estimate.
	- You can construct the confidence interval for |b0| or |b1| by using their reported standard errors and multiplying by the corresponding :math:`t`-value. For example, if you want 99% confidence limits, then look up the 99% values for the :math:`t`-distribution using :math:`n-k` degrees of freedom, in this case it would be ``qt((1-0.99)/2, df=9)``, which is :math:`\pm 3.25`. So the 99% confidence limits for the slope coefficient would be :math:`[0.5 - 3.25 \times 0.1179; 0.5 + 3.25 \times 0.1179] = [0.12; 0.88]`.
	- The :math:`R^2 = 0.6665` value.
	- Be able to calculate the residuals: :math:`e_i = y_i - \hat{y}_i = y_i - b_0 - b_1 x_i`. We expect the median of the residuals to be around 0, and the rest of the summary of the residuals gives a feeling for how far the residuals range about zero.
