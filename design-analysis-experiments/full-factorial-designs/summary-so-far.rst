Summary so far
~~~~~~~~~~~~~~~~~

-	The factorial experimental design is intentionally constructed so that each factor is independent of the others. There are :math:`2^k` experiments for :math:`k` factors.

	-	This implies the :math:`\mathbf{X}^T\mathbf{X}` matrix is easily constructed (a diagonal matrix, with a value of :math:`2^k` for each diagonal entry).
	-	These coefficients have the lowest variability possible: :math:`(\mathbf{X}^T\mathbf{X})^{-1}S_E^2`.
	-	We have uncorrelated estimates of the slope coefficients in the model. That is, we can be sure the value of the coefficient is unrelated to the other values. 
	
-	However, we still need to take the usual care in *interpreting* the coefficients. The usual precaution, using the example below, is that the temperature coefficient :math:`b_T` is the effect of a one-degree change, holding all other variables constant. That's not possible if :math:`b_{TS}`, the interaction between :math:`T` and :math:`S`, is significant: we cannot hold the :math:`TS` constant while changing :math:`b_T`.
		
	.. math:: 
	
		y = b_0 + b_T x_T + b_S x_S + b_{TS} x_Tx_S + e
	
	*We cannot interpret the main effects separately from the interaction effects* when we have significant interaction terms in the model.  Also, if you conclude the interaction term is significant, then you must also include all main factors that make up that interaction term in the model.
		
	For another example, with an interpretation, please see Box, Hunter and Hunter (2nd edition), page 185.
	
-	Factorial designs use the collected data much more efficiently than one-at-a-time experimentation. As shown in :ref:`the preceding section <DOE-COST-vs-factorial-efficiency>`, the estimated variance is halved when using a factorial design compared to a COST approach.
	
-	A small or zero effect from an :math:`x` variable to the :math:`y` response variable implies the :math:`y` is insensitive to that :math:`x`. This is desirable in some situations. It means we can adjust that :math:`x` without affecting :math:`y`, sometimes stated as "the :math:`y` is robust to changes in :math:`x`".

Example: analysis of systems with 4 factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the prior sections you have seen how to analyze experiments with 2 factors and 3 factors. The logic to analyze systems with 4 or more factors proceeds in exactly the same way. The video here shows how to go about this.

.. youtube:: https://www.youtube.com/watch?v=Rti2zqQFrTY&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=43
