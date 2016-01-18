Variability explained with each component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can calculate :math:`R^2` values, since PLS explains both the |X|-space and the |Y|-space. We use the :math:`\mathbf{E}_a` matrix to calculate the cumulative variance explained for the |X|-space. 

.. math::
	R^2_{\mathbf{X}, a, \text{cum}} = 1 - \dfrac{\text{Var}(\mathbf{E}_a)}{\text{Var}(\mathbf{X}_{a=1})}
	
Before the first component is extracted we have :math:`R^2_{\mathbf{X}, a=0} = 0.0`, since :math:`\mathbf{E}_{a=0} = \mathbf{X}_{a=1}`. After the second component, the residuals, :math:`\mathbf{E}_{a=1}`, will have decreased, so :math:`R^2_{\mathbf{X}, a}` would have increased.

We can construct similar :math:`R^2` values for the |Y|-space using the :math:`\mathbf{Y}_a` and :math:`\mathbf{F}_a` matrices. Furthermore, we construct in an analogous manner the :math:`R^2` values for each column of :math:`\mathbf{X}_a` and :math:`\mathbf{Y}_a`, exactly as :ref:`we did for PCA <LVM_PCA_R2_values>`.

These :math:`R^2` values help us understand which components best explain different sources of variation. Bar plots of the :math:`R^2` values for each column in |X| and |Y|, after a certain number of |A| components are one of the best ways to visualize this information.


.. Common questions about PLS models
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. 
.. .. _LVM-PLS-what-in-X-and-Y:
.. 
.. What goes in |X| and what goes in |Y| ?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. .. Still to come.
.. 
.. .. 	* handles collinear variables
.. .. 	* handles multiple Y
.. .. 	* PLS1 vs PLS2
.. .. 
.. .. Uses:
.. .. 
.. .. 	* Predictive modelling; QSAR
.. .. 	* Monitoring
.. 	
.. 
.. One Y or many Y's?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. .. Still to come.
.. 
.. .. Do PLS2 first, then do PLS1 if the Y's are relatively orthogonal.
.. 
.. .. Wold 2001, p 116
.. 
.. 	
.. .. _LVM-PLS-number-of-components:
.. 
.. How many components?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. .. Still to come.
.. 
.. .. One technique to estimate Q2 is by cross-validation. This method consists of dividing the data into a number of groups. Models are built with a group of data left out – one group at a time. With each model, the corresponding omitted data are predicted and the total prediction error sum of squares calculated. Q2, like R2, varies between 0 and 1, where values closer to 1 indicate better prediction ability. The Q2 value will always be smaller than R2. Finally, Q2 is used to select the number of principal components (model complexity) to avoid over-fitting. PLS models can be converted to a standard linear regression form as given by the following equation:
.. 
.. .. Almost all software packages will use cross-validation for PLS to determine the number of components. The cross-validation for PLS only considers the predictive capability of |Y|; in other words the cross-validation criterion stops adding components once the variance explained in |Y| starts to drop off.
.. 
.. .. This is perfectly adequate in many cases; but is certain instances we would also like the |X|-space to be well explained. For example, when building a monitoring model, we would like to also monitor the SPE from the |X|-space. Fortunately, in many cases, just adding one or two components manually, beyond the number from cross-validation will achieve the objective of additionally modelling the |X|-space.
.. 
.. .. * Wold 2001, p 116
.. .. * Why can we have more than 1 PC when there is only a single y?
.. 
.. .. _LVM-PLS-on-new-data:
.. 	
.. How do I use a PLS model on new data?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. .. Still to come.


.. What is the difference between |W| and |P|?
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. This question is best answered by first reading the subsection above called ":ref:`How do I use a PLS model on new data <LVM-PLS-on-new-data>`". After that, please read the description of deflation in the section on the :ref:`NIPALS algorithm for PLS <LVM_PLS_calculation>`.

.. Comparison to MLR (using R)
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. 
.. .. Still to come.
.. 
.. The properties of PLS
.. ~~~~~~~~~~~~~~~~~~~~~~~~
.. 
.. For reference, we list some properties of the PLS model structure:
.. 
.. *	The |A| vectors in the columns on :math:`\mathbf{W}` are orthogonal to each other: :math:`w_i \perp w_j` where :math:`i \neq j`, and :math:`i, j = 1, 2, \ldots, A`.
.. *	The vectors :math:`t_i` in the scores, |T|, are mutually orthogonal.
.. *	The vectors :math:`w_i` are orthogonal to the vectors :math:`p_j`, only for :math:`i \leq j`.
.. 
.. More still to come.
.. 
.. ..	u't = (c'c)^{-1}(c'Y') t
.. .. * Is c'c = 1 for each component?  I.e. can we see the u's as an orthogonal projection onto the loadings for Y?  They are not unit length and they are not orthogonal. So we cannot make that claim.
