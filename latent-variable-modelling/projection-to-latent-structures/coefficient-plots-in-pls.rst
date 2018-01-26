Coefficient plots in PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After building an initial PLS model one of the most informative plots to investigate are plots of the :math:`\mathbf{r:c}` vectors: using either bar plots or scatter plots. (The notation :math:`\mathbf{r:c}` implies we superimpose a plot of :math:`\mathbf{r}` on a plot of :math:`\mathbf{c}`.) These plots show the relationship between variables in |X|, between variables in |Y|, as well as the latent variable relationship between these two spaces. The number of latent variables, |A|, is much smaller number than the original variables, :math:`K + M`, effectively compressing the data into a small number of informative plots.

There are models where the number of components is of moderate size, around |A| = 4 to 8, in which case there are several combinations of :math:`\mathbf{r:c}` plots to view. If we truly want to understand how all the |X| and |Y| variables are related, then we must spend time investigating all these plots. However, the coefficient plot can be a useful compromise if one wants to learn, in a single plot,how the |X| variables are related to the |Y| variables using *all* |A| *components*.

.. sidebar:: Caution using the coefficients
	:class:	caution
	
	It is not recommended that PLS be implemented in practice as described here. In other words, do not try make PLS like multiple linear regression and go directly from the |X|'s to the |Y|'s using :math:`\widehat{\mathbf{y}}'_\text{new} = \mathbf{x}'_\text{new} \beta`.
	
	Instead, one of the major benefits of a PLS model is that we first calculate the scores, then verify |T2| and SPE are below their critical limits, e.g. 95% limits. If so, then we go ahead and calculate the predictions of |Y|. Direct calculation of |Y| bypasses this helpful information. Furthermore, using the :math:`\beta` coefficients directly means that we cannot handle missing data. 
	
	*Only use the coefficients to learn about your system*. Do not use them for prediction.

The coefficient plot is derived as follows. First preprocess the new observation, :math:`\mathbf{x}_\text{new,raw}`, to obtain :math:`\mathbf{x}_\text{new}`.

	*	Project the new observation onto the model to get scores: :math:`\mathbf{t}'_\text{new} = \mathbf{x}'_\text{new} \mathbf{R}`.
	
	*	Calculate the predicted :math:`\widehat{\mathbf{y}}'_\text{new} = \mathbf{t}'_\text{new} \mathbf{C}'` using these scores.
	
	*	Now combine these steps: 
	
		.. math::
			\begin{array}{rcl}
			    \widehat{\mathbf{y}}'_\text{new} &=& \mathbf{t}'_\text{new} \mathbf{C}' \\
			    \widehat{\mathbf{y}}'_\text{new} &=& \mathbf{x}'_\text{new} \mathbf{R} \mathbf{C}' \\
			    \widehat{\mathbf{y}}'_\text{new} &=& \mathbf{x}'_\text{new} \beta
			\end{array}
		
		where the matrix :math:`\beta` is a :math:`K \times M` matrix: each column in :math:`\beta` contains the regression coefficients for all |K| of the |X| variables, showing how they are related to each of the |M| |Y|-variables. 
		
From this derivation we see these regression coefficients are a function of *all* the latent variables in the model, since :math:`\mathbf{R} = \mathbf{W}\left(\mathbf{P}'\mathbf{W}\right)^{-1}` as shown in :ref:`an earlier section of these notes <LVM_PLS_W_and_R>`.

In the example below there were :math:`A=6` components, and :math:`K=14` and :math:`M=5`. Investigating all 6 of the  :math:`\mathbf{r:c}` vectors is informative, but the coefficient plot provides an efficient way to understand how the |X| variables are related to this particular |Y| variable across all the components in the model.

.. figure:: ../../figures/pls/coefficient-plot-LDPE-A-is-6.png
	:alt:	../../figures/pls/coefficient-plot-LDPE.R
	:scale: 70%
	:width: 900px
	:align: center
	
In this example the ``Tin``, ``z2``, ``Tcin2`` and ``Tmax2``, ``Fi2``, ``Fi1``, ``Tmax1``, and ``Press`` variables are all related to conversion, the |y| variable. This does not imply a cause and effect relationships, rather it just shows they are strongly correlated.

.. The coefficient plots from PLS-DA models (:ref:`supervised classification <LVM-supervised-classification-PLSDA>`) can be particularly informative if there are many components. It shows which variables in |X| are important in discriminating (predicting) the particular class. To see this, one plots the coefficients from the relevant class column in :math:`\beta`.

.. MENTION HERE HOW PCA, with A=K is exactly MLR.

.. YOU NEED AN EXAMPLE HERE. I can find several contradicting examples; eg. Kamyr digester case study, where Y = YKappa; 4 components by cross; not all the variables in PC 3 and 4 match up with the coefficient plot's expectation.

.. Variable importance to projection (VIP): See: http://dx.doi.org/10.1137/0905052 - this paper has no mention of VIP (despite what ProSensus software says)
