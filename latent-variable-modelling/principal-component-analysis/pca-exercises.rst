PCA Exercises
~~~~~~~~~~~~~

.. index::
	pair: exercises; latent variable modelling
	
Each exercise introduces a new topic or highlights some interesting aspect of PCA.

Room temperature data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :math:`N = 144`
* :math:`K = 4` + 1 column containing the date and time at which the 4 temperatures were recorded
* Web address: http://openmv.net/info/room-temperature
* Description: Temperature measurements from 4 corners of a room

.. image:: ../../figures/examples/room-temperature/room-temperature-plots.png
	:alt:	../../figures/examples/room-temperature/room-temperature-plots.R
	:scale: 80
	:width: 750px
	:align: center

**Objectives**

Before even fitting the model:

#.	How many latent variables do you expect to use in this model?  Why?.

#.	What do you expect the first loading vector to look like?

Now build a PCA model using any software package.

#.	How much variation was explained by the first and second latent variables? Is this result surprising, :ref:`given the earlier description <LVM_room_temperature_example>` of the dataset?

#.	Plot a time series plot (also called a line plot) of :math:`t_1`. Did this match your expectations?  Why/why not?

#.	Plot a bar plot of the loadings for the second component. Given this bar plot, what are the characteristics of an observation with a large, positive value of :math:`t_2`; and a large, negative :math:`t_2` value?

#.	Now plot the time series plot for :math:`t_2`. Again, does this plot match your expectations?

Now use the :ref:`concept of brushing <LVM_linking_brushing>` to interrogate and learn from the model.

#.	Plot a score plot of :math:`t_1` against :math:`t_2`.

#.	Also plot the time series plot of the raw data.

#.	Select a cluster of interest in the score plot and see the brushed values in the raw data. Are these the values you expected to be highlighted?

#.	Next plot the Hotelling's |T2| line plot, as :ref:`described earlier <LVM-Hotellings-T2>`. Does the 95% limit in the Hotelling's |T2| line plot correspond to the 95% limit in the score plot?

#.	Also plot the SPE line plot. Brush the outlier in the SPE plot and find its location in the score plot. 

#.	Why does this point have a large SPE value?

#.	Describe how a 3-D scatter plot would look with :math:`t_1` and :math:`t_2` as the :math:`(x,y)` axes, and SPE as the :math:`z`-axis.

.. image:: ../../figures/examples/room-temperature/3d-example-empty.png
	:alt:	../../figures/examples/room-temperature//3d-example.R
	:scale: 50
	:width: 750px
	:align: center

What have we learned?

*	Interpreted that a latent variable is often a true driving force in the system under investigation.
*	How to interpret a loadings vector and its corresponding score vector.
*	Brushing multivariate and raw data plots to confirm our understanding of the model.
*	Learned about Hotelling's |T2|, whether we plot it as a line plot, or as an ellipse on a scatter plot.
*	We have confirmed how the scores are on the model plane, and the SPE is the distance from the model plane to the actual observation.

Food texture data set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :math:`N = 50`
* :math:`K = 5` + 1 column containing the labels for each batch
* Web address: http://openmv.net/info/food-texture
* Description: Data from a :ref:`food manufacturer making a pastry product <LVM_food_texture_example>`. Each row contains the 5 quality attributes of a batch of product.

#.	Fit a PCA model.

#.	Report the :math:`R^2` values for the overall model and the :math:`R^2` values for each variable, on a per-component basis for components 1, 2, and 3. Comment on what each latent variable is explaining and by how much.

#.	Plot the loadings plot as a bar plot for :math:`p_1`. Does this match the values :ref:`given earlier <LVM_food_texture_example>`?  Interpret what kind of pastry would have a large positive :math:`t_1` value?

#.	What feature(s) of the raw data does the second component explain?  Plot sequence-ordered plots of the raw data to confirm your answer.

#.	Look for any observations that are unusual. Are there any unusual scores? SPE values?  Plot contribution plots for the unusual observations and interpret them.

Food consumption data set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This data set has become a classic data set when learning about multivariate data analysis. It consists of 

*	:math:`N=16` countries in the European area
*	:math:`K=20` food items
*	Missing data: yes
*	Web address: http://openmv.net/info/food-consumption
*	Description: The data table lists for each country the relative consumption of certain food items, such as tea, jam, coffee, yoghurt, and others.

.. image:: ../../figures/examples/food-consumption/food-consumption.png
	:alt:	../../figures/examples/food-consumption/food-consumption.numbers
	:scale: 100
	:width: 750px
	:align: center

#.	Fit a PCA model to the data using 2 components.

#.	Plot a loadings plot of :math:`p_1` against :math:`p_2`. Which are the important variables in the first component? And the second component?

#.	Since each column represents food consumption, how would you interpret a country with a high (positive or negative) :math:`t_1` value?  Find countries that meet this criterion.  Verify that this country does indeed have this interpretation (*hint*: use a contribution plot and examine the raw data in the table).

#.	Now plot SPE after 2 components (don't plot the default SPE, make sure it is the SPE only after two components). Use a contribution plot to interpret any interesting outliers.

#.	Now add a third component and plot SPE after 3 components. What has happened to the observations you identified in the previous question?  Investigate the loadings plot for the third component now (as a bar plot)  and see which variables are heavily loaded in the 3rd component.

#.	Also plot the :math:`R^2` values for each variable, after two components, and after 3 components. Which variables are modelled by the 3rd component?  Does this match with your interpretation of the loadings bar plot in the previous question?
#.	Now plot a score plot of the 3rd component against the 1st component. Generate a contribution plot in the score from the interesting observation(s) you selected in part 4. Does this match up with your interpretation of what the 3rd component is modelling?

What we learned:

* Further practice of our skills in interpreting score plots and loading plots.
* How to relate contribution plots to the loadings and the :math:`R^2` values for a particular component.

Silicon wafer thickness
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :math:`N=184`
* :math:`K=9`
* Web address: http://openmv.net/info/silicon-wafer-thickness
* Description: These are nine thickness measurements recorded from various batches of silicon wafers. One wafer is removed from each batch and the thickness of the wafer is measured at the nine locations, as shown in the illustration. 

.. figure:: ../../figures/examples/silicon-wafer-thickness/silicon-wafer-thickness-locations.png
	:alt:	../../figures/examples/silicon-wafer-thickness/silicon-wafer-thickness-locations.svg
	:scale: 50
	:width: 500px
	:align: center

#.	Build a PCA model on all the data.

#.	Plot the scores for the first two components. What do you notice?  Investigate the outliers, and the raw data for each of these unusual observations. What do you conclude about those observations?

#.	Exclude the unusual observations and refit the model. 

#.	Now plot the scores plot again; do things look better?  Record the :math:`R^2` and :math:`Q^2` values (from cross-validation) for the first three components. Are the :math:`R^2` and :math:`Q^2` values close to each other; what does this mean?

#.	Plot a loadings plot for the first component. What is your interpretation of :math:`p_1`?  Given the :math:`R^2` and :math:`Q^2` values for this first component (previous question), what is your interpretation about the variability in this process?

#.	And the interpretation of :math:`p_2`?  From a quality control perspective, if you could remove the variability due to :math:`p_2`, how much of the variability would you be removing from the process?

#.	Also plot the corresponding time series plot for :math:`t_1`. What do you notice in the sequence of score values?

#.	Repeat the above question for the second component.

#.	Finally, plot both the :math:`t_1` and :math:`t_2` series overlaid on the same plot, in time-order, to see the smaller variance that :math:`t_2` explains.

What we learned:

* Identifying outliers; removing them and refitting the model.
* Variability in a process can very often be interpreted. The :math:`R^2` and :math:`Q^2` values for each component show which part of the variability in the system is due the particular phenomenon modelled by that component.

	
.. _LVM-process-troubleshooting-plastic-pellets:

Process troubleshooting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recent trends show that the yield of your company's flagship product is declining. You are uncertain if the supplier of a key raw material is to blame, or if it is due to a change in your process conditions. You begin by investigating the raw material supplier.

The data available has:

*	:math:`N = 24`

*	:math:`K = 6` + 1 designation of process outcome

*	Web address: http://openmv.net/info/raw-material-characterization

*	Description: 3 of the 6 measurements are size values for the plastic pellets, while the other 3 are the outputs from thermogravimetric analysis (TGA), differential scanning calorimetry (DSC) and thermomechanical analysis (TMA), measured in a laboratory. These 6 measurements are thought to adequately characterize the raw material. Also provided is a designation ``Adequate`` or ``Poor`` that reflects the process engineer's opinion of the yield from that lot of materials.

Import the data, and set the ``Outcome`` variable as a secondary identifier for each observation, as shown in the illustration below. The observation's primary identifier is its batch number.

.. figure:: ../../figures/examples/raw-material-outcome/raw-material-characterization.png
	:alt:	Screenshot from software
	:scale: 80
	:width: 750px
	:align: center

#.	Build a latent variable model for all observations and use auto-fit to determine the number of components. If your software does not have and auto-fit features (cross-validation), then use a Pareto plot of the eigenvalues to decide on the number of components.

#.	Interpret component 1, 2 and 3 separately (using the loadings bar plot).

#.	Now plot the score plot for components 1 and 2, and colour code the score plot with the ``Outcome`` variable. Interpret why observations with ``Poor`` outcome are at their locations in the score plot (use a contribution plot). 

#.	What would be your recommendations to your manager to get more of your batches classified as ``Adequate`` rather than ``Poor``?

#.	Now build a model only on the observations marked as ``Adequate`` in the Outcome variable.

#.	Re-interpret the loadings plot for :math:`p_1` and :math:`p_2`. Is there a substantial difference between this new loadings plot and the previous one?

What we learned:

*	How to use an indicator variable in the model to learn more from our score plot.

*	How to build a data set, and bring in new observations as testing data.


.. Principal properties of surfactants
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. * :math:`N=38`
.. * :math:`K=19`
.. * :math:`M=4`
.. * Missing data: yes
.. * Web address: http://openmv.net/info/surfactants
.. * Description: These 38 non-ionic surfactants, ingredients for making a detergent, were characterized (described) by taking 19 measurements (the other 4 columns will be used in a future study). The first purpose of this data set was to understand how these 19 properties are related to each other, and to find a representative sub-sample from the rows in |X| which could be selected for further study.
.. 
.. #.	Import the data, making sure you *exclude* the ``YDet``, ``YConc``, ``YTemp``, and ``YTox`` variables. Build a PCA model on the 19 columns in remaining in |X|.
.. #.	Study the first two components. What do you notice in the score plot?  Investigate this feature that seems interesting and try to explain why it occurs.
.. #.	Exclude the cluster (they were related to surfactants which were too lipophilic) for the rest of the study.
.. #.	Rebuild the model. 
.. #.	Since the purpose of the original data set was to find a smaller group of samples that are representative of all surfactants, which samples would you select for further study and why?
.. #.	Save the :math:`t_1` *vs* :math:`t_2` score plot to a figure (e.g. BMP) and mark these samples on it to show your colleagues/manager.


