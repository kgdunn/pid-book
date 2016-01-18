Assessing significance of main effects and interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
When there are no :index:`replicate points <pair: replicates; experiments>`, then the number of factors to estimate from a full factorial is :math:`2^k` from the :math:`2^k` observations. There are no degrees of freedom left to calculate the standard error or the confidence intervals for the main effects and interaction terms.

The standard error can be estimated if complete replicates are available. However, a complete replicate is onerous, because a complete replicate implies the entire experiment is repeated: system setup, running the experiment and measuring the result. Taking two samples from one actual experiment and measuring :math:`y` twice is not a true replicate. That is only an estimate of the measurement error and analytical error. 

Furthermore, there are better ways to spend our experimental budget than running complete replicate experiments -- see the section on :ref:`screening designs <DOE-saturated-screening-designs>` later on. Only later in the overall experimental procedure should we run replicate experiments as a verification step and to assess the statistical significance of effects.

.. AU: I inserted the two main ways. Please confirm.

There are two main ways we can determine if a main effect or interaction is significant: by using a Pareto plot or the standard error.

.. _DOE-Pareto-plot:

Pareto plot
^^^^^^^^^^^^^^^^^^^^^^^^^

.. Note:: This is a makeshift approach that is only applicable if all the factors are centered and scaled.

.. image:: ../../figures/doe/pareto-plot-full-fraction.png
	:align: left
	:scale: 50
	:width: 900px
	:alt: fake width
	
A full factorial with :math:`2^k` experiments has :math:`2^k` parameters to estimate. Once these parameters have been calculated, for example, by using a :ref:`least squares model <DOE-analysis-by-least-squares>`, then plot as shown the absolute value of the model coefficients in sorted order, from largest magnitude to smallest, ignoring the intercept term. Significant coefficients are established by visual judgement -- establishing a visual cutoff by contrasting the small coefficients to the larger ones.

The above example was from a full factorial experiment where the results for :math:`y` in standard order were :math:`y = \left[45,71,48,65,68,60,80,65,43,100,45,104,75,86,70,96 \right]`.
	
We would interpret that factors **A**, **C** and **D**, as well as the interactions of **AC** and **AD**, have a significant and causal effect on the response variable, :math:`y`. The main effect of **B** on the response :math:`y` is small, at least over the range that **B** was used in the experiment. Factor **B** can be omitted from future experimentation in this region, though it might be necessary to include it again if the system is operated at a very different point.

The reason why we can compare the coefficients this way, which is not normally the case with least squares models, is that we have both centered and scaled the factor variables. If the centering is at typical baseline operation, and the range spanned by each factor is that expected over the typical operating range, then we can fairly compare each coefficient in the bar plot. Each bar represents the influence of that term on :math:`y` for a one-unit change in the factor, that is, a change over half its operating range.

Obviously, if the factors are not scaled appropriately, then this method will be error prone.  However, the approximate guidance is accurate, especially when you do not have a computer or if additional information required by the other methods (discussed below) is not available. It is also the only way to estimate the effects for :ref:`highly fractionated and saturated designs <DOE-saturated-screening-designs>`.


Standard error: from replicate runs or from an external dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: It is often better to spend your experimental budget screening for additional factors rather than replicating experiments.

.. But, if a duplicate run exists at every combination of the factorial, then the standard error can be estimated as follows:
..
.. 	-	Let :math:`y_{i,1}` and :math:`y_{i,2}` be the two response values for each of the :math:`i^\text{th}` runs, where :math:`i=1, 2, ..., 2^k`
.. 	-	The mean response for the :math:`i^\text{th}` run is :math:`\overline{y}_i = 0.5y_{i,1} + 0.5y_{i,2}`
.. 	-	Denote the difference between them as :math:`d_i = y_{i,2} - y_{i,1}`, or the other way around - it doesn't matter.
.. 	-	The variance can be estimated with a single degree of freedom as :math:`s_i^2 = \dfrac{(y_{i,1} - \overline{y}_i)^2 + (y_{i,2} - \overline{y}_i)^2}{1}`
.. 	-	The variance can also be written as :math:`s_i^2 = d_i^2/2`
.. 	-	Now we can pool the variances for the :math:`2^k` runs to estimate :math:`\hat{\sigma}^2 = S_E^2 = \dfrac{1}{2}\displaystyle\sum_i^{2^k}{d_i^2}`
.. 	-	This estimated standard error is :math:`t`-distributed with :math:`2^k` degrees of freedom.
..
.. The standard error can be calculated in a similar manner if more than one duplicate run is performed. So rather run a :math:`2^4` factorial for 4 factors than a :math:`2^3`factorial twice; or as we will see later - one can screen five or more factors with :math:`2^4` runs.
	
If there are more experiments than parameters to be estimated, then we have extra degrees of freedom. Having degrees of freedom implies we can calculate the standard error, :math:`S_E`. Once :math:`S_E` has been found, we can also calculate the standard error for each model coefficient, and then confidence intervals can be constructed for each main effect and interaction. And because the model matrix is orthogonal, the confidence interval for each effect is independent of the other. This is because the general confidence interval is :math:`\mathcal{V}\left(\mathbf{b}\right) = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}S_E^2`, and the off-diagonal elements in :math:`\mathbf{X}^T\mathbf{X}` are zero.

For an experiment with :math:`n` runs, and where we have coded our :math:`\mathbf{X}` matrix to contain :math:`-1` and :math:`+1` elements, and when the :math:`\mathbf{X}` matrix is orthogonal, the standard error for coefficient :math:`b_i` is :math:`S_E(b_i) = \sqrt{\mathcal{V}\left(b_i\right)} = \sqrt{\dfrac{S_E^2}{\sum{x_i^2}}}`. Some examples:

	*	A :math:`2^3` factorial where every combination has been repeated will have :math:`n=16` runs, so the standard error for each coefficient will be the same, at :math:`S_E(b_i) = \sqrt{\dfrac{S_E^2}{16}} = \dfrac{S_E}{4}`. 
	*	A :math:`2^3` factorial with three additional runs at the center point would have the following least squares representation:
	
		.. math::
		
			\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}\\
			\begin{bmatrix} y_1\\ y_2\\ y_3 \\ y_4 \\ y_5 \\ y_6 \\ y_7 \\ y_8 \\ y_{c,1} \\ y_{c,2} \\ y_{c,3}\end{bmatrix} &=
			\begin{bmatrix} 1 & A_{-} & B_{-} & C_{-} & A_{-}B_{-} & A_{-}C_{-} & B_{-}C_{-} & A_{-}B_{-}C_{-}\\ 
							1 & A_{+} & B_{-} & C_{-} & A_{+}B_{-} & A_{+}C_{-} & B_{-}C_{-} & A_{+}B_{-}C_{-}\\
							1 & A_{-} & B_{+} & C_{-} & A_{-}B_{+} & A_{-}C_{-} & B_{+}C_{-} & A_{-}B_{+}C_{-}\\
							1 & A_{+} & B_{+} & C_{-} & A_{+}B_{+} & A_{+}C_{-} & B_{+}C_{-} & A_{+}B_{+}C_{-}\\
							1 & A_{-} & B_{-} & C_{+} & A_{-}B_{-} & A_{-}C_{+} & B_{-}C_{+} & A_{-}B_{-}C_{+}\\
							1 & A_{+} & B_{-} & C_{+} & A_{+}B_{-} & A_{+}C_{+} & B_{-}C_{+} & A_{+}B_{-}C_{+}\\
							1 & A_{-} & B_{+} & C_{+} & A_{-}B_{+} & A_{-}C_{+} & B_{+}C_{+} & A_{-}B_{+}C_{+}\\
							1 & A_{+} & B_{+} & C_{+} & A_{+}B_{+} & A_{+}C_{+} & B_{+}C_{+} & A_{+}B_{+}C_{+}\\
							1 & 0     & 0     & 0     & 0          & 0          & 0          & 0              \\
							1 & 0     & 0     & 0     & 0          & 0          & 0          & 0              \\
							1 & 0     & 0     & 0     & 0          & 0          & 0          & 0              
			\end{bmatrix}
			\begin{bmatrix} b_0 \\ b_A \\ b_B \\ b_{C} \\ b_{AB} \\ b_{AC} \\ b_{BC} \\ b_{ABC} \end{bmatrix} +
			\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \\ e_5 \\ e_6 \\ e_7 \\ e_8 \\ e_{c,1} \\ e_{c,2} \\ e_{c,3} \end{bmatrix}\\
			\mathbf{y} & = 
			\begin{bmatrix} 1 & -1 & -1 & -1 & +1 & +1 & +1 & -1\\ 
							1 & +1 & -1 & -1 & -1 & -1 & +1 & +1\\
							1 & -1 & +1 & -1 & -1 & +1 & -1 & +1\\
							1 & +1 & +1 & -1 & +1 & -1 & -1 & -1\\
							1 & -1 & -1 & +1 & +1 & -1 & -1 & +1\\ 
							1 & +1 & -1 & +1 & -1 & +1 & -1 & -1\\
							1 & -1 & +1 & +1 & -1 & -1 & +1 & -1\\
							1 & +1 & +1 & +1 & +1 & +1 & +1 & +1\\
							1 &  0 &  0 &  0 &  0 &  0 &  0 &  0\\
							1 &  0 &  0 &  0 &  0 &  0 &  0 &  0\\
							1 &  0 &  0 &  0 &  0 &  0 &  0 &  0
			\end{bmatrix}
			\begin{bmatrix} b_0 \\ b_A \\ b_B \\ b_{C} \\ b_{AB} \\ b_{AC} \\ b_{BC} \\ b_{ABC} \end{bmatrix} + \mathbf{e}
			
		Note that the center point runs do not change the orthogonality of :math:`\mathbf{X}`. However, as we expect after having studied the section on :ref:`least squares modelling <SECTION-least-squares-modelling>`, additional runs decrease the variance of the model parameters, :math:`\mathcal{V}(\mathbf{b})`. In this case, there are :math:`n=2^3+3 = 11` runs, so the standard error is decreased to :math:`S_E^2 = \dfrac{\mathbf{e}^T\mathbf{e}}{11 - 8}`. However, the center points do not further reduce the variance of the parameters in :math:`\sqrt{\dfrac{S_E^2}{\sum{x_i^2}}}`, because the denominator is still :math:`2^k` (**except for the intercept term**, whose variance is reduced by the center points).
	
Once we obtain the standard error for our system and calculate the variance of the parameters, we can multiply it by the critical :math:`t`-value at the desired confidence level in order to calculate the confidence limit. However, it is customary to just report the standard error next to the coefficients, so that users can apply their own level of confidence. For example,

	.. math::
	
		\text{Temperature effect}, b_T &= 11.5 \pm 0.707\\
		\text{Catalyst effect}, b_K &= 1.1 \pm 0.707
		
Even though the confidence interval of the temperature effect would be :math:`11.5 - c_t \times 0.707 \leq \beta_T \leq 11.5 + c_t \times 0.707`, it is clear that at the 95% significance level, the above representation shows the temperature effect is significant, while the catalyst effect is not (:math:`c_t \approx 2`).

.. OMIT: this can be confusing and misleading

	Normal probability plots
	^^^^^^^^^^^^^^^^^^^^^^^^^

	If the hypothesis that there is no causal effect from the :math:`k` factors on the response is true, then the :math:`2^k-1` parameter estimates, not counting the intercept, should be normally distributed. That is from the central limit theorem, and the fact that estimated coefficients are linear combinations of the response variable.

	An example for a :math:`2^3` factorial would be that the seven coefficients, not including :math:`b_0`, in this linear model would be normally distributed:

	.. math::

		y_i = b_0 + b_A x_A + b_B x_B + b_{C}x_C + b_{AB}x_{AB} + b_{AC}x_{AC} +  b_{BC}x_{BC} +  b_{ABC}x_{ABC}
	
	A normal probability plot is a nonlinear transformation of the data so that the s-shape of the cumulative normal distribution appears as a straight line. We used this idea in the section on :ref:`univariate statistics <SECTION-univariate-review>` where a q-q plot was constructed to assess normality. Another way to visualize this concept is to draw vertical divisions on the normal distribution curve, to create :math:`2^k-1` sections of equal area. One effect is expected per division.

	.. TODO: illustration of normal distribution division

	.. code-block:: s

		k = 4
	 	n = 2^k - 1
		index <- seq(1, n)
		p <- (index - 0.5) / n
		theoretical.quantity <- qnorm(p)
	
		labels = c('A', 'B',    'C',   'D', 'AB',  'AC', 'AD',   'BC', 'BD',   'CD', 
		            'ABC',  'ABD',  'ACD',  'BCD',  'ABCD')
		b      = c( -4,  12, -1.125, -2.75,  0.5, 0.375,  0.0, -0.625, 2.25, -0.125, 
		           -0.375,   0.25, -0.125, -0.375,  -0.125)

		b.sort = sort(b)

		plot(theoretical.quantity, b.sort)
		qqline(b.sort)

		# Or more simply: use the qqPlot function:
		library(car)
		qqPlot(b, labels=labels)
	
	.. figure:: ../../figures/doe/normal-probability-signifcant-effects.png
		:align: center
		:scale: 50
		


Refitting the model after removing nonsignificant effects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After having established which effects are significant, we can exclude the nonsignificant effects and increase the degrees of freedom. (We do not have to recalculate the model parameters -- why?) The residuals will be nonzero now, so we can then estimate the standard error and apply all the tools from least squares modelling to assess the residuals. Plots of the residuals in experimental order, against fitted values, q-q plots and all the other assessment tools from earlier are used, as usual.

.. AU: I modified the last sentence of the following paragraph because it seemed redundant. Please confirm.

Continuing the above example, where a :math:`2^4` factorial was run, the response values in standard order were :math:`y = [71, 61, 90, 82, 68, 61, 87, 80, 61, 50, 89, 83, 59, 51, 85, 78]`. The significant effects were from **A**, **B**, **D** and **BD**. Now, omitting the nonsignificant effects, there are only five parameters to estimate, including the intercept, so the standard error is :math:`S_E^2 = \dfrac{39}{16-5} = 3.54`, with 11 degrees of freedom. The :math:`S_E(b_i)` value for all coefficients, except the intercept, is :math:`\sqrt{\dfrac{S_E^2}{16}} = 0.471`, and the critical :math:`t`-value at the 95% level is ``qt(0.975, df=11)`` = 2.2. So the confidence intervals can be calculated to confirm that these are indeed significant effects.

There is some circular reasoning here: postulate that one or more effects are zero and increase the degrees of freedom by removing those parameters in order to confirm the remaining effects are significant. Some general advice is to first exclude effects that are definitely small, and then retain medium-size effects in the model until you can confirm they are not significant.

.. _DOE-COST-vs-factorial-efficiency:
 
Variance of estimates from the COST approach versus the factorial approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: ../../figures/doe/comparison-of-variances.png
	:align: center
	:scale: 70
	:width: 900px
	:alt: fake width

Finally, we end this section on factorials by illustrating their efficiency. Contrast the two cases: COST and the full factorial approach. For this analysis we define the main effect simply as the difference between the high and low values (normally we divide through by 2, but the results still hold). Define the variance of the measured :math:`y` value as :math:`\sigma_y^2`.
	
	.. tabularcolumns:: |l|l|
	
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| COST approach                                                            | Fractional factorial approach                                                                                  |
+==========================================================================+================================================================================================================+
| The main effect of :math:`T` is :math:`b_T = y_2 - y_1`.                 | The main effect is :math:`b_T = 0.5(y_2 - y_1) + 0.5(y_4 - y_3)`.                                              |
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| The variance is :math:`\mathcal{V}(b_T) = \sigma_y^2 + \sigma_y^2`.      | The variance is :math:`\mathcal{V}(b_T) = 0.25(\sigma_y^2 + \sigma_y^2) + 0.25(\sigma_y^2 + \sigma_y^2)`.      |
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| So :math:`\mathcal{V}(b_T) = 2\sigma_y^2`.                               | And :math:`\mathcal{V}(b_T) = \sigma_y^2`.                                                                     |
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+

Not only does the factorial experiment estimate the effects with much greater precision (lower variance), but the COST approach cannot estimate the effect of interactions, which is incredibly important, especially as systems approach optima that are on ridges (see the contour plots earlier in this section for an example).

Factorial designs make each experimental observation work twice.
	

