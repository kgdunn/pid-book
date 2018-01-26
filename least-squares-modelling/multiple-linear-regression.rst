.. _LS_multiple_X_MLR:

More than one variable: multiple linear regression (MLR)
================================================================================

.. index:: 
	pair: multiple linear regression (MLR); least squares
	
.. youtube:: https://www.youtube.com/watch?v=qiv1nBCfwBg&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=26

We now move to including more than one explanatory |x| variable in the linear model. We will:

 	#.	introduce some matrix notation for this section

	#.	show how the optimization problem is solved to estimate the model parameters
	
	#.	how to interpret the model coefficients
	
	#.	extend our tools from the previous section to analyze the MLR model
	
	#.	use integer (yes/no *or* on/off) variables in our model.

First some motivating examples:

	-	A relationship exists between :math:`x_1` = reactant concentration and :math:`x_2` = temperature with respect to :math:`y` = reaction rate. We already have a linear model between :math:`y = b_0 + b_1x_1`, but we want to improve our understanding of the system by learning about the temperature effect, :math:`x_2`.
	
	-	We want to predict melt index in our reactor from the reactor temperature, but we know that the feed flow and pressure are also good explanatory variables for melt index. How do these additional variables improve the predictions?
	
	-	We know that the quality of our plastic product is a function of the mixing time, and also the mixing tank in which the raw materials are blended. How do we incorporate the concept of a mixing tank indicator in our model?

..	- Ian Nichols example
..	- Case study/Example: http://www.amstat.org/publications/jse/v16n3/datasets.kuiper.html
..	- Show that R2 increases when adding a new variable to the equation (also see p105 of Fox)
	- Consider summarizing p223-225 of Fox here regarding t- and F-tests
	- Add Q5.11 from assignment 3 here to show how adding terms increases R2

Multiple linear regression: notation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=dkfY0OKH12g&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=27

To help the discussion below it is useful to omit the least squares model's intercept term. We do this by first centering the data.

.. math::

	y_i &= b_0 + b_1 x_i \\
	\overline{y} &= b_0 + b_1 \overline{x} \\
	y_i - \overline{y} &= 0 +b_1(x_i - \overline{x}) \qquad \text{by subtracting the previous lines from each other}

This indicates that if we fit a model where the |x| and |y| vectors are first mean-centered, i.e. let :math:`x = x_\text{original} - \text{mean}\left(x_\text{original} \right)` and :math:`y = y_\text{original} - \text{mean}\left(y_\text{original} \right)`, then we still estimate the same slope for :math:`b_1`, but the intercept term is zero. All we gain from this is simplification of the subsequent analysis. Of course, if you need to know what :math:`b_0` was, you can use the fact that :math:`b_0 = \overline{y} - b_1 \overline{x}`. Nothing else changes: the :math:`R^2, S_E, S_E(b_1)` and all other model interpretations remain the same. You can easily prove this for yourself.

So in the rest of the this section we will omit the model's intercept term, since it can always be recovered afterwards.

The general linear model is given by:

.. math::

	y_i &= \beta_1 x_1 + \beta_2x_2 + \ldots + \beta_kx_k + \epsilon_i \\
	y_i &= [x_1, x_2, \ldots, x_k] \begin{bmatrix} \beta_1 \\ \beta_2 \\ \vdots \\ \beta_k \end{bmatrix} + \epsilon_i \\
	y_i &= \underbrace{\mathit{x}^T}_{(1 \times k)} \underbrace{\beta}_{(k \times 1)} + \,\epsilon_i

And writing the last equation |n| times over for each observation in the data:

.. math::

	\begin{bmatrix} y_1\\ y_2\\ \vdots \\ y_n \end{bmatrix} &=
	\begin{bmatrix} x_{1,1} & x_{1,2} & \ldots & x_{1,k}\\
	                x_{2,1} & x_{2,2} & \ldots & x_{2,k}\\
	                \vdots  & \vdots  & \ddots & \vdots\\
	                x_{n,1} & x_{n,2} & \ldots & x_{n,k}\\
	\end{bmatrix}
	\begin{bmatrix} b_1 \\ b_2 \\ \vdots \\ b_k \end{bmatrix} +
	\begin{bmatrix} e_1\\ e_2\\ \vdots \\ e_n \end{bmatrix}\\
	\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}

where:

	- :math:`\mathbf{y}`: :math:`n \times 1`
	- :math:`\mathbf{X}`: :math:`n \times k`
	- :math:`\mathbf{b}`: :math:`n \times 1`
	- :math:`\mathbf{e}`: :math:`n \times 1`

Estimating the model parameters via optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As with the simple least squares model, :math:`y = b_0 + b_1 x`, we aim to minimize the sum of squares of the errors in vector :math:`\mathbf{e}`. This least squares objective function can be written compactly as:

	.. math::
	
		\begin{array}{rl}
		    f(\mathbf{b}) &= \mathbf{e}^T\mathbf{e} \\
		                  &= \left(\mathbf{y} - \mathbf{X} \mathbf{b} \right)^T \left( \mathbf{y} - \mathbf{X} \mathbf{b} \right) \\
		                  &= \mathbf{y}^T\mathbf{y} - 2 \mathbf{y}^T\mathbf{X}\mathbf{b} + \mathbf{b}\mathbf{X}^T\mathbf{X}\mathbf{b}
		\end{array}

Taking partial derivatives with respect to the entries in :math:`\mathbf{b}` and setting the result equal to a vector of zeros, you can prove to yourself that :math:`\mathbf{b} = \left( \mathbf{X}^T\mathbf{X} \right)^{-1}\mathbf{X}^T\mathbf{y}`. You might find the `Matrix Cookbook <http://www.google.ca/search?q=The+Matrix+Cookbook/>`_ useful in solving these equations and optimization problems.

Three important relationships are now noted:

#. :math:`\mathcal{E}\{\mathbf{b}\} = \mathbf{\beta}`
#. :math:`\mathcal{V}\{\mathbf{b}\} = \left( \mathbf{X}^T\mathbf{X} \right)^{-1} S_E^2`
#. An estimate of the standard error is given by: :math:`\sigma_e \approx S_E = \sqrt{\dfrac{\mathbf{e}^T\mathbf{e}}{n-k}}`, where :math:`k` is the number of parameters estimated in the model and :math:`n` is the number of observations.

These relationships imply that our estimates of the model parameters are unbiased (the first line), and that the variability of our parameters is related to the :math:`\mathbf{X}^T\mathbf{X}` matrix and the model's standard error, :math:`S_E`.

Going back to the single variable case we showed in the section where we derived :ref:`confidence intervals <LS-CI-for-model-parameters>` for :math:`b_0` and :math:`b_1`  that:

	.. math::

		\mathcal{V}\{b_1\} = \dfrac{S_E^2}{\sum_j{\left( x_j - \overline{\mathrm{x}} \right)^2}}

Notice that our matrix definition, :math:`\mathcal{V}\{\mathbf{b}\} = \left( \mathbf{X}^T\mathbf{X} \right)^{-1} S_E^2`, gives exactly the same result, remembering the |x| variables have already been centered in the matrix form. Also recall that the variability of these estimated parameters can be reduced by (a) taking more samples, thereby increasing the denominator size, and (b) by including observations further away from the center of the model.

.. rubric:: Example

Let :math:`x_1 = [1, 3, 4, 7, 9, 9]`, and :math:`x_2 = [9, 9, 6, 3, 1, 2]`, and :math:`y = [3, 5, 6, 8, 7, 10]`. By inspection, the :math:`x_1` and :math:`x_2` variables are negatively correlated, and the :math:`x_1` and :math:`y` variables are positively correlated (also positive covariance). Refer to the definition of covariance in :ref:`an equation from the prior section <LS_eqn_definition-covariance>`.

After mean centering the data we have that :math:`x_1 = [-4.5, -2.5, -1.5 , 1.5 , 3.5,  3.5]`, and :math:`x_2 = [4,  4,  1, -2, -4, -3]` and :math:`y = [-3.5, -1.5, -0.5,  1.5,  0.5,  3.5]`. So in matrix form:

.. math::

	\begin{array}{lr}
		\mathbf{X} = \begin{bmatrix} -4.5 & 4\\ -2.5 & 4 \\ -1.5 & 1 \\ 1.5 & -2 \\ 3.5 & -4 \\  3.5 & -3 \end{bmatrix}
	&\qquad\qquad
		\mathbf{y} = \begin{bmatrix} -3.5 \\ -1.5\\ -0.5\\  1.5\\  0.5\\  3.5 \end{bmatrix}
	\end{array}

The :math:`\mathbf{X}^T\mathbf{X}` and :math:`\mathbf{X}^T\mathbf{y}` matrices can then be calculated as:

.. math::

	\begin{array}{lr}
		\mathbf{X}^T\mathbf{X} = \begin{bmatrix} 55.5 &   -57.0 \\-57.0  & 62\end{bmatrix}
	&\qquad\qquad
		\mathbf{X}^T\mathbf{y} = \begin{bmatrix} 36.5 \\ -36.0 \end{bmatrix}
	\end{array}

Notice what these matrices imply (remembering that the vectors in the matrices have been centered). The :math:`\mathbf{X}^T\mathbf{X}` matrix is a scaled version of the covariance matrix of :math:`\mathbf{X}`. The diagonal terms show how strongly the variable is correlated with itself, which is the variance, and always a positive number. The off-diagonal terms are symmetrical, and represent the strength of the relationship between, in this case, :math:`x_1` and :math:`x_2`. The off-diagonal terms for two uncorrelated variables would be a number close to, or equal to zero.

The inverse of the :math:`\mathbf{X}^T\mathbf{X}` matrix is particularly important - it is related to the standard error for the model parameters - as in: :math:`\mathcal{V}\{\mathbf{b}\} = \left( \mathbf{X}^T\mathbf{X} \right)^{-1} S_E^2`.

.. math::
	
	\begin{array}{lr}
		\left(\mathbf{X}^T\mathbf{X}\right)^{-1}= \begin{bmatrix} 0.323 & 0.297 \\ 0.297 & 0.289 \end{bmatrix}
	\end{array}

The non-zero off-diagonal elements indicate that the variance of the :math:`b_1` coefficient is related to the variance of the :math:`b_2` coefficient as well. This result is true for most regression models, indicating we can't accurately interpret each regression coefficient's confidence interval on its own.

For the two variable case, :math:`y = b_1x_1 + b_2x_2`, the general relationship is that:

.. math::

	\mathcal{V}\left(b_1\right) &= \dfrac{1}{1-r^2_{12}} \times \dfrac{S_E^2}{\sum{x_1^2}} \\
	\mathcal{V}\left(b_2\right) &= \dfrac{1}{1-r^2_{12}} \times \dfrac{S_E^2}{\sum{x_2^2}}

where :math:`r^2_{12}` represents the correlation between variable :math:`x_1` and :math:`x_2`. What happens as the correlation between the two variables increases?

.. We won't go into details here, but these lead to oval-shaped confidence intervals. Show picture and illustrate the marginal vs elliptical CI; see BHH,v2, page 370


Interpretation of the model coefficients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=FkZZiv3J6xQ&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=28

.. _MLR_coefficient_interpretation:

Let's take a look at the case where :math:`y = b_1x_1 + b_2x_2`. We can plot this on a 3D plot, with axes of :math:`x_1`, :math:`x_2` and :math:`y`:

.. image:: ../figures/least-squares/least-squares-two-x-variables.png
	:width: 900px
	:align: left
	:scale: 40
	:alt: fake width

The points are used to fit the plane by minimizing the sum of square distances shown by vertical lines from each point to the plane. The interpretation of the slope coefficients for :math:`b_1` and :math:`b_2` is **not the same** as for the case with just a single |x| variable.

When we have multiple |x| variables, then the value of coefficient :math:`b_1` is the average change we would expect in :math:`\mathbf{y}` for a one unit change in :math:`{x}_1` provided we hold :math:`{x}_2` fixed. It is the last part that is new:  we must assume that other |x| variables are fixed.

For example, let :math:`y = b_T T + b_S S = -0.52 T + 3.2 S`, where :math:`T` is reactor temperature in Kelvin, and :math:`S` is substrate concentration in g/L, and :math:`y` is yield in :math:`\mu\text{g}`, for a bioreactor reactor system. The :math:`b_T = -0.52 \mu\text{g}/\text{K}` coefficient is the decrease in yield for every 1 Kelvin increase in temperature, holding the substrate concentration fixed.

This is a good point to introduce some terminology you might come across.  Imagine you have a model where :math:`{y}` is the used vehicle price and :math:`{x}_1` is the mileage on the odometer (we expect that :math:`b_1` will be negative) and :math:`{x}_2` is the number of doors on the car. You might hear the phrase: "the effect of the number of doors, controlling for mileage, is not significant". The part "controlling for ..." indicates that the controlled variable has been added to regression model, and its effect is accounted for. In other words, for two vehicles with the same mileage, the coefficient :math:`b_2` indicates whether the second hand price increases or decreases as the number of doors on the car changes (e.g. a 2-door vs a 4-door car).

In the prior example, we could say: the effect of substrate concentration on yield, :index:`controlling <single: controlling for another variable>` for temperature, is to increase the yield by 3.2 :math:`\mu\text{g}` for every increase in 1 g/L of substrate concentration.

Integer (dummy, indicator) variables in the model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	pair: integer variables; least squares

.. youtube:: https://www.youtube.com/watch?v=TrhG-XhnBK4&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=29

Now that we have introduced multiple linear regression to expand our models, we also consider these sort of cases:

	-	We want to predict yield, but want to indicate whether a radial or axial impeller was used in the reactor and learn whether it has any effect on yield.
	
	-	Is there an important difference when we add the catalyst first and then the reactants, or the reactants followed by the catalyst?
	
	-	Use an indicator variable to show if the raw material came from the supplier in Spain, India, or Vietnam and interpret the effect of supplier on yield.

	..	image:: ../figures/least-squares/Mixing_-_flusso_assiale_e_radiale.jpg
		:width: 900px
		:align: left
		:scale: 40
		:alt: fake width

	Axial and radial blades; figure from `Wikipedia <https://en.wikipedia.org/wiki/Impeller>`_

We will start with the simplest case, using the example of the radial or axial impeller. We wish to understand the effect on yield, :math:`y [\mu\text{g}]`, as a function of the impeller type, and impeller speed, :math:`x`.

.. math::

	y &= \beta_0 + \beta_1x + \gamma d + \varepsilon \\
	y &= b_0 + b_1 x + g d_i + e_i \\

where :math:`d_i = 0` if an axial impeller was used, or :math:`d_i = 1` if a radial impeller was used. All other least squares assumptions hold, particularly that the variance of :math:`y_i` is unrelated to the value of :math:`d_i`. For the initial discussion let's assume that :math:`\beta_1 = 0`, then geometrically, what is happening here is:

.. image:: ../figures/least-squares/least-squares-dummy-variable-and-intercept.png
	:width: 900px
	:align: right
	:scale: 60
	:alt: fake width

The :math:`\gamma` parameter, estimated by :math:`g`, is the difference in intercept when using a different impeller type. Note that the lines are parallel.

.. math::
	
	\begin{array}{ll}
		\text{Axial impellers:} \qquad &\qquad y = b_0 + 0 \\
		\text{Radial impellers:} \qquad &\qquad y = b_0 + g
	\end{array}

Now if :math:`\beta_1 \neq 0`, then the horizontal lines in the above figure are tilted, but still parallel to each other. Nothing else is new here, other than the representation of the variable used for :math:`d_i`. The interpretation of its coefficient, :math:`g`, is the same as with any other least squares coefficient. In this particular example, had :math:`g = -56 \mu\text{g}`, it would indicate that the average decrease in yield is 56 :math:`\mu\text{g}` when using a radial impeller.

The rest of the analysis tools for least squares models can be used quite powerfully. For example, a 95% confidence interval for the impeller variable might have been:

.. math::

	-32 \mu\text{g} \leq \gamma \leq 21 \mu\text{g}

which would indicate the impeller type has no significant effect on the yield amount, the :math:`y`-variable.

Integer variables are also called dummy variables or indicator variables. Really what is happening here is the same concept as for multiple linear regression, the equation of a plane is being estimated. We only use the equation of the plane at integer values of :math:`d`, but mathematically the underlying plane is actually continuous.

.. image:: ../figures/least-squares/least-squares-two-x-variables-one-integer.png
	:width: 900px
	:align: left
	:scale: 50
	:alt: fake width

We have to introduce additional terms into the model if we have integer variables with more than 2 levels. In general, if there are :math:`p`-levels, then we must include :math:`p-1` terms. For example, if we wish to test the effect of :math:`y` = yield achieved from the raw material supplier in Spain, India, or Vietnam, we could code:

	- Spain: :math:`d_{i1} = 0` and :math:`d_{i2} = 0`
	- India: :math:`d_{i1} = 1` and :math:`d_{i2} = 0`
	- Vietnam: :math:`d_{i1} = 0` and :math:`d_{i2} = 1`.

and solve for the least squares model: :math:`y = \beta_0 + \beta_1x_1 + \ldots + \beta_k x_k + \gamma_1 d_1 + \gamma_2 d_2 + \varepsilon`, where :math:`\gamma_1` is the effect of the Indian supplier, holding all other terms constant (i.e. it is the incremental effect of India relative to Spain);  :math:`\gamma_2` is the incremental effect of the Vietnamese supplier relative to the base case of the Spanish supplier. Because of this somewhat confusing interpretation of the coefficients, sometimes people will assume they can sacrifice an extra degree of freedom, but introduce :math:`p` new terms for the :math:`p` levels of the integer variable, instead of :math:`p-1` terms.

	- Spain: :math:`d_{i1} = 1` and :math:`d_{i2} = 0` and :math:`d_{i3} = 0`
	- India: :math:`d_{i1} = 0` and :math:`d_{i2} = 1` and :math:`d_{i3} = 0`
	- Vietnam: :math:`d_{i1} = 0` and :math:`d_{i2} = 0` and :math:`d_{i3} = 1`

and :math:`y = \beta_0 + \beta_1x_1 + \ldots + \beta_k x_k + \gamma_1 d_1 + \gamma_2 d_2 + \gamma_3 d_3 + \varepsilon`, where the coefficients :math:`\gamma_1, \gamma_2` and :math:`\gamma_3` are assumed to be more easily interpreted. However, calculating this model will fail, because there is a built-in perfect linear combination. The :math:`\mathbf{X}^T\mathbf{X}` matrix is not invertible.

