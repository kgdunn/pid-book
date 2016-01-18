
PLS Exercises
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _LVM-cheddar-cheese-example:

The taste of cheddar cheese
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*	:math:`N=30`

*	:math:`K=3`

*	:math:`M=1`

*	`Link to cheese data <http://openmv.net/info/cheddar-cheese>`_

*	Description: This very simple case study considers the taste of mature cheddar cheese. There are 3 measurements taken on each cheese: lactic acid, acetic acid and :math:`\text{H}_2\text{S}`. 


#.	Import the data into ``R``: ``cheese <- read.csv('cheddar-cheese.csv')``

#.	Use the ``car`` library and plot a scatter plot matrix of the raw data: 

	* ``library(car)``
	
	* ``scatterplotMatrix(cheese[,2:5])``
	
	.. figure:: ../../figures/examples/cheese/cheese-plots.png
		:alt:	../../figures/examples/cheese/cheese-plots.R
		:scale: 60%
		:width: 900px
		:align: center

#.	Using this figure, how many components do you expect to have in a PCA model on the 3 |X| variables: ``Acetic``, ``H2S`` and ``Lactic``?

#.	What would the loadings look like?

#.	Build a PCA model now to verify your answers.

#.	Before building the PLS model, how many components would you expect?  And what would the weights look like (:math:`\mathbf{r}_1`, and :math:`\mathbf{c}_1`)?

#.	Build a PLS model and plot the :math:`\mathbf{r:c}_1` bar plot. Interpret it.

#.	Now plot the SPE plot; these are the SPE values for the projections onto the |X|-space. Any outliers apparent?

#.	In ``R``, build a least squares model that regresses the ``Taste`` variable on to the other 3 |X| variables. 

	*	``model.lm <- lm(cheese$Taste ~ cheese$Acetic + cheese$H2S + cheese$Lactic)``
	
	*	Report each coefficient :math:`\pm 2 S_E(b_i)`. Which coefficients does ``R`` find significant in MLR?
	
		.. math::
			\beta_\text{Acetic} &= \qquad \qquad \pm \\
			\beta_\text{H2S} &= \qquad  \qquad \pm \\
			\beta_\text{Lactic} &= \qquad  \qquad \pm
			
	*	Report the standard error and the :math:`R^2_y` value for this model.
	
	*	Compare this to the PLS model's :math:`R^2_y` value.
	
#.	Now build a PCR model in ``R`` using only 1 component, then using 2 components. Again calculate the standard error and :math:`R^2_y` values.

	*	``model.pca <- prcomp(cheese[,2:4], scale=TRUE)``
	
	*	``T <- model.pca$x``
	
	*	``model.pcr.1 <- lm(cheese$Taste ~ T[,1]) # one component`` 
	
	*	``model.pcr.2 <- lm(cheese$Taste ~ T[,1:2]) # two components``

#.	Plot the observed |y| values against the predicted |y| values for the PLS model.

#.	PLS models do not have a standard error, since the degrees of freedom are not as easily defined. But you can calculate the RMSEE (root mean square error of estimation) = :math:`\sqrt{\dfrac{\mathbf{e}'\mathbf{e}}{N}}`. Compare the RMSEE values for all the models just built.

Obviously the best way to test the model is to retain a certain amount of testing data (e.g. 10 observations), then calculate the root mean square error of prediction (RMSEP) on those testing data.


Comparing the loadings from a PCA model to a PLS model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PLS explains both the |X| and |Y| spaces, as well as building a predictive model between the two spaces. In this question we explore two models: a PCA model and a PLS model on the same data set.

The data are from the :ref:`plastic pellets troubleshooting example <LVM-process-troubleshooting-plastic-pellets>`. 

*	:math:`N = 24`

*	:math:`K = 6 + 1` designation of process outcome

*	`Link to raw materials data <http://openmv.net/info/raw-material-characterization>`_

*	Description: 3 of the 6 measurements are size values for the plastic pellets, while the other 3 are the outputs from thermogravimetric analysis (TGA), differential scanning calorimetry (DSC) and thermomechanical analysis (TMA), measured in a laboratory. These 6 measurements are thought to adequately characterize the raw material. Also provided is a designation ``Adequate`` or ``Poor`` that reflects the process engineer's opinion of the yield from that lot of materials.

#.	Build a PCA model on all seven variables, including the 0-1 process outcome variable in the |X| space. Previously we omitted that variable from the model, this time include it.

#.	How do the loadings look for the first, second and third components?  

#.	Now build a PLS model, where the |Y|-variable is the 0-1 process outcome variable. In the previous PCA model the loadings were oriented in the directions of greatest variance. For the PLS model the loadings must be oriented so that they *also* explain the |Y| variable and the relationship between |X| and |Y|. Interpret the PLS loadings in light of this fact.

#.	How many components were required by cross-validation for the PLS model?

#.	Explain why the PLS loadings are different to the PCA loadings.

.. _LVM-LDPE-case-study:

Predicting final quality from on-line process data: LDPE system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* 	:math:`N = 54`

* 	:math:`K = 14`

* 	:math:`K = 5`

*	`Link to dataset website <http://openmv.net/info/LDPE>`_ and description of the data.

#.	Build a PCA model on the 14 |X|-variables and the first 50 observations.

#.	Build a PCA model on the 5 |Y|-variables: ``Conv``, ``Mn``, ``Mw``, ``LCB``, and ``SCB``. Use only the first 50 observations

#.	Build a PLS model relating the |X| variables to the |Y| variables (using :math:`N=50`). How many components are required for each of these 3 models?

#.	Compare the loadings plot from PCA on the |Y| space to the weights plot (:math:`\mathbf{c}_1` vs :math:`\mathbf{c}_2`) from the PLS model.

#.	What is the :math:`R^2_X` (not for |Y|) for the first few components?

#.	Now let's look at the interpretation between the |X| and |Y| space. Which plot would you use?
	
	*	Which variable(s) in |X| are strongly related to the conversion of the product (``Conv``)?  In other words, as an engineer, which of the 14 |X| variables would you consider adjusting to improve conversion.
	
	*	Would these adjustments affect any other quality variables? How would they affect the other quality variables?
	
	*	How would you adjust the quality variable called ``Mw`` (the weight average molecular weight)?

.. BLEND PCA QUESTION IN HERE
.. 
.. Principal properties of surfactants (continued)
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. 
.. * :math:`N=38`
.. * :math:`K=19`
.. * :math:`M=4`
.. * Missing data: yes
.. * Web address: http://openmv.net/info/surfactants
.. * Description: These 38 non-ionic surfactants, ingredients for making a detergent, were characterized (described) by taking 19 measurements. 4 columns will be used in a future study). The first purpose of this data set was to understand how these 19 properties are related to each other, and to find a representative sub-sample from the rows in |X| which could be selected for further study.
.. 
.. An earlier exercise had you build a PCA model on the 19 properties of the 38 surfactants; then 10 of the surfactants were chosen and studied in depth to calculate their washing efficiency:
.. 
.. 	*	``YDet``: the percentage soil removed from clothes
.. 	*	``YConc``: the optimal concentration required when using that surfactant 
.. 	*	``YTemp``: the optimal washing temperature required when using that surfactant
.. 	*	``YTox``: the surfactant's toxicity
.. 
.. #.	Write down the number of PCA components required to model only the |X| data (this was from a previous exercise).
.. #.	Build a *PCA model* on these 4 |Y| variables first.
.. #.	What is the dimensionality of the |Y|-space?
.. #.	What are the relationships between these four variables?
.. #.	Now build a PLS model on the 10 observations: the |X|-space will have 10 rows and 19 columns, while the |Y| space will have 10 rows and 4 columns. You should build this from the previous model, using the ``New model as ...`` feature in the software.
.. #.	Answer these questions:
.. 	
.. 	* What portion of the variance for |X| and |Y| do the first 3 components explain?
.. 	* Which variables are well/poorly explained in |X|? 
.. 	* And for |Y|?
.. 	
.. #.	Plot the scores for the |X|-space against the scores for the |Y|-space. What can you say about the covariance (correlation) between these scores?
.. #.	Now repeat this plot for the other two components.
.. #.	Next consider the weights plot: plot :math:`\mathbf{c}_1` for the |Y| space; compare it against :math:`\mathbf{p}_1` from the PCA on the |Y|-variables.
.. #.	Also plot :math:`\mathbf{r}_1` and :math:`\mathbf{r}_2` as bar plots. Compare these two weight vectors against the PCA loadings vectors that you built earlier.



