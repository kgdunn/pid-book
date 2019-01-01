
.. _LS_covariance:	

Covariance
===========

.. youtube:: https://www.youtube.com/watch?v=tXOCOMtSWrc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=18

You probably have an intuitive sense for what it means when two things are correlated. We will get to correlation next, but we start by first looking at :index:`covariance`. Let's take a look at an example to formalize this, and to see how we can learn from data.

Consider the measurements from a gas cylinder; temperature (K) and pressure (kPa). We know the ideal gas law applies under moderate conditions: :math:`pV = nRT`.

	-	Fixed volume, :math:`V = 20 \times 10^{-3} \text{m}^3` = 20 L
	-	Moles of gas, :math:`n = 14.1` mols of chlorine gas, molar mass = 70.9 g/mol, so this is 1 kg of gas
	-	Gas constant, :math:`R = 8.314` J/(mol.K)

Given these numbers, we can simplify the ideal gas law to: :math:`p=\beta_1 T`, where :math:`\beta_1 = \dfrac{nR}{V} > 0`. These data are collected from sampling the system:

.. wikitable

	{| class="wikitable center"
	|-
	!
	! :math:`T` = Cylinder temperature (K)
	! :math:`p` = Cylinder pressure (kPa)
	! :math:`h` = Room humidity (%)
	|-
	|||273|| 1600|| 42
	|-
	|||285|| 1670|| 48
	|-
	|||297|| 1730|| 45
	|-
	|||309|| 1830|| 49
	|-
	|||321|| 1880|| 41
	|-
	|||333|| 1920|| 46
	|-
	|||345|| 2000|| 48
	|-
	|||357|| 2100|| 48
	|-
	|||369|| 2170|| 45
	|-
	|||381|| 2200|| 49
	|-
	| || ||
	|-
	|'''Mean''' || 327 || 1910 || 46.1
	|-
	|'''Variance''' || 1320 || 43267 || 8.1
	|}


.. image:: ../figures/least-squares/table-of-cylinder-data.png
	:width: 900px
	:scale: 67
	:alt: fake width

.. _LS_eqn_definition-covariance:

The formal definition for covariance between any two variables is:

.. math::
	:label: definition-covariance

		\text{Cov}\left\{x, y\right\} = \mathcal{E}\left\{ (x - \overline{x}) (y - \overline{y})\right\} \qquad \text{where} \qquad \mathcal{E}\left\{ z \right\} = \overline{z}

Use this to calculate the covariance between temperature and pressure by breaking the problem into steps:

	-	First calculate :index:`deviation variables`. They are called this because they are now the deviations from the mean: :math:`T - \overline{T}` and :math:`p - \overline{p}`. Subtracting off the mean from each vector just centers their frame of reference to zero.
	
	-	Next multiply the two vectors, element-by-element, to calculate a new vector :math:`(T - \overline{T}) (p - \overline{p})`.

		.. dcl:: R
			:height: 600px
		
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

	-	More specifically, we should provide the units as well:  the covariance between temperature and pressure is 6780 [K.kPa] in this example. Similarly the covariance between temperature and humidity is 202 [K.%].

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

Using the ``cov(temp, pres)`` function in R gives ``7533.333``, while we calculated 6780. The difference comes from :math:`6780 \times \dfrac{N}{N-1}= 7533.33`, indicating that R divides by :math:`N-1` rather than :math:`N`. This is because the variance function in R for a vector ``x`` is internally called as ``cov(x, x)``. Since R returns the unbiased variance, it divides through by :math:`N-1`. This inconsistency does not really matter for large values of :math:`N`, but emphasizes that one should always read the documentation for the software being used.

Note that deviation variables are not affected by a *shift* in the raw data of :math:`x` or :math:`y`. For example, measuring temperature in Celsius or Kelvin has no effect on the covariance number; but measuring it in Celsius vs Fahrenheit does change the covariance value.

.. Another point to note: recall from geometry that the length of a vector, :math:`x`, is calculated from the sum of squares of the elements in vector :math:`x`, and then taking the square root of the sum. Mathematically the sum of squares is can be written as: math:`x^Tx`. For a vector :math:`x` that is centered, this corresponds


.. _LS_correlation:

Correlation
===========

.. youtube:: https://www.youtube.com/watch?v=tXOCOMtSWrc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=18

The variance and covariance values are units dependent. For example, you get a very different covariance when calculating it using grams vs kilograms. The :index:`correlation` on the other hand removes the effect of scaling and arbitrary unit changes. It is defined as:

.. math::
	:label: definition-correlation

		\text{Correlation}\,\,=\,\,r(x, y) = \dfrac{\mathcal{E}\left\{ (x - \overline{x}) (y - \overline{y})\right\}}{\sqrt{\mathcal{V}\left\{x\right\}\mathcal{V}\left\{y\right\}}} = \dfrac{\text{Cov}\left\{x, y\right\}}{\sqrt{\mathcal{V}\left\{x\right\}\mathcal{V}\left\{y\right\}}}

It takes the covariance value and divides through by the units of :math:`x` and of :math:`y` to obtain a dimensionless result. The values of :math:`r(x,y)` range from :math:`-1` to :math:`+1`. Also note that :math:`r(x,y) = r(y,x)`.

So returning back to our example of the gas cylinder, the correlation between temperature and pressure, and temperature and humidity can be calculated now as:

.. dcl:: R
	:height: 450px

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
	:alt: fake width
	
	
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
			\mathcal{V}\{x+y\}	&= \mathcal{V}\{x\} + \mathcal{V}\{y\}, \qquad\text{only if $x$ and $y$ are independent}
