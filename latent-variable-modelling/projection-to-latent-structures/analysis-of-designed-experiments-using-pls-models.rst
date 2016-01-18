.. _LVM_DOE_data:

Analysis of designed experiments using PLS models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. NOTE: you already have some of these ideas in the section "LVM-preprocessing": combine them; cross reference them?

Data from a designed experiment, particularly factorial experiments, will have independent columns in |X|. These data tables are adequately analyzed using :ref`multiple linear regression <LS_multiple_X_MLR>` (MLR) least squares models. 

These factorial and fractional factorial data are also well suited to analysis with PLS. Since factorial models support interaction terms, these additional interactions should be added to the |X| matrix. For example, a full factorial design with variables **A**, **B** and **C** will also support the **AB**, **AC**, **BC** and **ABC** interactions. These four columns should be added to the |X| matrix so that the loadings for these variables are also estimated. If a :ref:`central composite design <DOE_central_composite_designs>`, or some other design that supports quadratic terms has been performed, then these columns should also be added to |X|, e.g.: :math:`\text{\textbf{A}}^2`, :math:`\text{\textbf{B}}^2` and :math:`\text{\textbf{C}}^2`.

The PLS loadings plots from analyzing these DOE data are interpreted in the usual manner; and the coefficient plot is informative if :math:`A>2`.

.. EXAMPLE: Carlos' thesis.

There are some other advantages of using and interpreting a PLS model built from DOE data, rather than using the MLR approach:

	*	If *additional data* (not the main factors) are captured during the experiments, particularly measurable disturbances, then these additional columns can, and should, be included in |X|. These extra data are called covariates in other software packages. These additional columns will remove some of the orthogonality in |X|, but this is why a PLS model would be more suitable.
	
	*	If multiple |Y| measurements were recored as the response, and particularly if these |Y| variables are correlated, then a PLS model would be better suited than building |K| separate MLR models. A good example is where the response variable from the experiment is a complete spectrum of measurements, such as from a NIR probe.
	
One other point to note when analyzing DOE data with PLS is that the |Q2| values from cross-validation are often very small. This makes intuitive sense: if the factorial levels are suitably spaced, then each experiment is at a point in the process that provides new information. It is unlikely that cross-validation, when leaving out one or more experiments, is able to accurately predict each corner in the factorial.

Lastly, models built from DOE data allow a much stronger interpretation of the loading vectors, :math:`\mathbf{R:C}`. This time we can infer cause-and-effect behaviour; normally in PLS models the best we can say is that the variables in |X| and |Y| are correlated. Experimental studies that are run in a factorial manner will break happenstance correlation structures; so if any correlation that is present, then this truly is causal in nature.

.. ALSO, with DOE data we have A=1 usually;  why is this?  Try it with some data sets to verify; particularly interpret w1 and p1.


.. Analysis with additional first-principles knowledge
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. We rarely only have data from a process; as engineers we also have additional, first-principles knowledge about the system being investigated. We can always embed this information in the data.
.. 
.. An example that was mentioned in the :ref:`section of data preprocessing <LVM_preprocessing>` was that of a distillation column. The inverse temperature is known to more correlated to the vapour pressure, known from first-principles modelling. Using the temperature variable by itself will lead to an adequate model, but the transformed variable can lead to a better model. We sometimes leave both variables in the model: the temperature and the calculated inverted temperature.
