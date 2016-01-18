.. _LVM_extracting_value_from_data:

Extracting value from data
===================================================

There are five main areas where engineers use large quantities of data.

	#.	**Improved process understanding**
	
		This is an implicit goal in any data analysis: either we confirm what we know about the process, or we see something unusual show up and learn from it. Plots that show, in one go, how a complex set of variables interact and relate to each other are required for this step.
		
	#.	**Troubleshooting process problems**
	
		Troubleshooting occurs after a problem has occurred. There are many potential sources that could have caused the problem. Screening tools are required that will help isolate the variables most related to the problem. These variables, combined with our engineering knowledge, are then used to troubleshoot why the problem occurred.
		
	#.	**Improving, optimizing and controlling processes**
	
		We have already introduced the concept of :ref:`designed experiments and response surface methods <SECTION-design-analysis-experiments>`. These are excellent tools to intentionally manipulate your process so that you can find a more optimal operating point, or even develop a new product. We will show how latent variable tools can be used on a large historical data set to improve process operation, and to move to a new operating point. There are also tools for applying process control in the latent variable space.
		
	#.	**Predictive modelling** (inferential sensors)
	
		The section on :ref:`least squares modelling <SECTION-least-squares-modelling>` provided you with a tool for making predictions. We will show some powerful examples of how a "difficult-to-measure" variable can be predicted in real-time, using other easy-to-obtain process data. Least squares modelling is a good tool, but it lacks some of the advantages that latent variable methods provide, such as the ability to handle highly collinear data, and data with missing values. 
	
	#.	**Process monitoring**
	
		Once a process is running, we require monitoring tools to ensure that it maintains and stays at optimal performance. We have already considered :ref:`process monitoring charts <SECTION-process-monitoring>` for univariate process monitoring. In this section we extend that concept to monitoring multiple variables.
		
The types of data engineers deal with now
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When industrial manufacturing and chemical engineering started to develop around the 1920's to 1950's, data collected from a process were, at most, just a handful of columns. These data were collected manually and often at considerable expense.

The "classical" tools required to visualize and understand these datasets are :ref:`scatter plots <visualization_scatter_plots>`, :ref:`time-series plots <visualization_time_series>`, :ref:`Shewhart charts <monitoring_shewhart_chart>` and :ref:`EWMA charts <monitoring_EWMA>` for process monitoring, and :ref:`multiple linear regression <LS_multiple_X_MLR>` (MLR) least-squares models; all the tools which we have already learned about so far.

We will represent any data set as a matrix, called |X|, where each row in |X| contains values taken from an *object* of some sort. These rows, or *observations* could be a collection of measurements at a particular point in time, various properties on a sample of final product, or a sample of raw material from a supplier. The columns in |X| are the values recorded for each observation. We call these the *variables* and there are :math:`K` of them.

	.. figure:: ../figures/data-types/X-matrix-long-and-thin.png
		:alt:	../figures/data-types/X-matrix-long-and-thin.svg
		:align: center
		:scale: 18
		:width: 400px

These data sets from the 1950's frequently had many more rows than columns, because it was expensive and time-consuming to measure additional columns. The choice of which columns to measure was carefully thought out, so that they didn't unnecessarily duplicate the same measurement. As a result:

	* the columns of X were often independent, with little or no overlapping information
	* the variables were measured in a controlled environment, with a low amount of error

These data sets meet all the assumptions required to use the so-called "classical" tools, especially least squares modelling. Data sets that engineers currently deal with though can be of any configuration with both large and small :math:`N` and large and small :math:`K`, but more likely we have many columns for each observation.

**Small N and small K**

	These cases are mostly for when we have expensive measurements, and they are hard to obtain frequently. Classical methods to visualize and analyze these data always work well: scatterplots, linear regression, *etc*.
	
**Small N and large K**

	This case is common for laboratory instrumentation, particularly spectroscopic devices. In recent years we are routinely collecting large quantities of data. A typical example is with near-infrared probes embedded at-line. These probes record a spectral response at around 1000 to 2000 different wavelengths. The data are represented in |X| using one wavelength per column and each sample appears in a row. The illustration here shows data from :math:`N=460` samples, with data recorded every 2 nm (:math:`K=650`).
	
	.. image:: ../figures/examples/tablet-spectra/pharma-spectra.png
		:alt:	../figures/examples/tablet-spectra/pharma-spectra.py
		:scale: 70
		:width: 750px
		:align: center

	Obviously not all the columns in this matrix are important; some regions are more useful than others, and columns immediately adjacent to each other are extremely similar (non-independent).
	
	An ordinary least squares regression model, where we would like to predict some :math:`y`-variable from these spectral data, cannot be calculated when :math:`K>N`, since we are then estimating more unknowns than we have observations for. A common strategy used to deal with non-independence is to select only a few columns (wavelengths in the spectral example) so that :math:`K < N`. The choice of columns is subjective, so a better approach is required, such as :ref:`projection to latent structures <SECTION_PLS>`.
	
**Large N and small K**

	A current-day chemical refinery easily records about 2 observations (rows) per second on around 2000 to 5000 variables (called tags); generating in the region of 50 to 100 Mb of data per second.
	
	For example, a modest size distillation column would have about 35 temperature measurements, 5 to 10 flow rates, 10 or so pressure measurements, and then about 5 more measurements derived from these recorded values.
	 
	.. figure:: ../figures/examples/distillation/Distillation_column_correlation.png
		:alt:	../figures/examples/distillation/Distillation_column_correlation.svg
		:scale: 45
		:width: 500px
		:align: center
		
	An `industrial distillation example <http://openmv.net/info/distillation-tower>`_ is given on the data set website with :math:`K=27`, from a small column in Canada.

**N approximately equal to K**
	
	The case of squarish matrices mostly occurs by chance: we just happen to have roughly the same number of variables as observations.

**X and Y matrices**

	This situation arises when we would like to predict one or more variables from another group of variables. We have already seen this data structure in the :ref:`least squares section <LS_multiple_X_MLR>` where :math:`M = 1`, but more generally we would like to predict several :math:`y`-values from the same data in |X|. 
	
	
	.. image:: ../figures/data-types/X-and-Y-matrices.png
		:alt:	../figures/data-types/X-and-Y-matrices.svg
		:scale: 30
		:width: 500px
		:align: center
		
	The "classical" solution to this problem is to build and maintain :math:`M` different least squares models. We will see in the section on  :ref:`projection to latent structures <SECTION_PLS>` that we can build a single regression model. The sections on :ref:`principal component regression <LVM_PCR>` also investigates the above data structure, but for single :math:`y`-variables.	

**3D data sets and higher dimensions**	

	These data tables are becoming very common, especially since 2000 onwards. A typical example is for image data from digital cameras. In this illustration a single image is taken at a point in time. The camera records the response at 6 different wavelengths, and the :math:`x-y` spatial directions (top-to-bottom and left-to-right). These values are recorded in a 3D data cube.
	
	
	.. image:: ../figures/data-types/image-data.png
		:alt:	../figures/data-types/image-data.svg
		:scale: 25
		:width: 500px
		:align: center
		
	A fourth dimension can be added to this data if we start recording images over time. Such systems generate between 1 and 5 Mb of data per second. As with the spectral data set mentioned earlier, these camera systems generate large quantities of redundant data, because neighbouring pixels, both in time and spatially, are so similar. It is a case of high noise and little real information.

**Batch data sets**	

	Batch systems are common with high-value products: pharmaceuticals, fine-chemicals, and polymers. The |Z| matrix below contains data that describes how the batch is prepared and also contains data that is constant over the duration of the whole batch. The |X| matrix contains the recorded values for each variable over the duration of the batch. For example, temperature ramp-up and ramp-down, flow rates of coolant, agitator speeds and so on. The final product properties, recorded at the end of the batch, are collected in matrix |Y|.
	
	.. figure:: ../figures/batch/Batch-data-layers-into-the-page.png
		:alt:	../figures/batch/Batch-data-layers-into-the-page.svg
		:scale: 40
		:width: 750px
		:align: center
		
	An example of batch trajectory data, in matrix |X|, where there are 4 variables, recorded at 80 times points, on about 20 batches is shown here:
	
	.. image:: ../figures/batch/aligned-trajectories-many-batches-yeast.png
		:scale: 40
		:width: 550px
		:align: center

	.. Figure just a screen grab from the Yeast case study

**Data fusion**	

	This is a recent buzz-word that simply means we collect and use data from multiple sources. Imagine the batch system above: we already have data in |Z| recorded by manual entry, data in |X| recorded by sensors on the process, and then |Y|, typically from lab measurements. We might even have a near infrared probe in the reactor that provides a complete spectrum (a vector) at each point in time. The process of combining these data sets together is called data fusion. Each data set is often referred to as a :index:`block <single: block (data set)>`. We prefer to use the term :index:`multiblock` data analysis when dealing with combined data sets.

Issues faced with engineering data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Size of the data**

	The most outstanding feature of the above data sets is their large size, both in terms of the number of rows and columns. This is primarily because data acquisition and data storage has become cheap.
	
	The number of rows isn't too big of a deal: we can sub-sample the data, use parallel processors on our computers or distributed computing (a.k.a. cloud computing) to deal with this. The bigger problem is the number of columns in the data arrays. A data set with :math:`K` columns can be visualized using :math:`K(K-1)/2` :ref:`pairs of scatterplots <LVM_visualization_scatterplot_matrix>`;  this is manageable for :math:`K < 8`, but the quadratic number of combinations prevents us from using scatterplot matrices to visualize this data, especially when :math:`K>10`. 
	
	The need here is for a toll that deals with large :math:`K`.
	
**Lack of independence**

	The lack of independence is a big factor in modern data sets - it is problematic for example with MLR where the :math:`\mathbf{X}'\mathbf{X}` becomes singular as the data become more dependent. Sometimes we can make our data more independent by selecting a reduced number of columns, but this requires good knowledge of the system being investigated, is time-consuming, and we risk omitting important variables. 
	
**Low signal to noise ratio**

	Engineering systems are usually kept as stable as possible: the ideal being a flat line. Data from such systems have very little signal and high noise. Even though we might record 50 Mb per second from various sensors, computer systems can, and actually do, "throw away" much of the data. This is not advisable from a multivariate data analysis perspective, but the reasoning behind it is hard to fault: much of the data we collect is not very informative. A lot of it is just from constant operation, noise, slow drift or error. 
	
	Finding the interesting signals in these routine data (also known as happenstance data), is a challenge.
		
**Non-causal data**

	This happenstance data is also non-causal. The opposite case is when one runs a designed experiment; this intentionally adds variability into a process, allowing us to conclude cause-and-effect relationships, if we properly block and randomize. 
	
	But happenstance data just allows us to draw inference based on correlation effects. Since correlation is a prerequisite for causality, we can often learn a good deal from the correlation patterns in the data. Then we use our engineering knowledge to validate any correlations, and we can go on to truly verify causality with a randomized designed experiment, if it is an important effect to verify.
	
**Errors in the data**

	Tools, such as least squares analysis, assume the recorded data has no error. But most engineering systems have error in their measurements, some of it quite large, since much of the data is collected by automated systems under non-ideal conditions. 
	
	So we require tools that relax the assumption that measurements have no error.
	
**Missing data**

	Missing data are very common in engineering applications. Sensors go off-line, are damaged, or it is simply not possible to record all the variables (attributes) on each observation. Classical approaches are to throw away rows or columns with incomplete information, which might be acceptable when we have large quantities of data, but could lead to omitting important information in many cases.

.. OMIT FOR NOW
		:alt:	../figures/data-types/missing-data.png
		:scale: 50
		:width: 750px
		:align: center
		
		.. Figure is just screen grab

.. OMIT FOR NOW
	**Unaligned data**

		Increasingly common, especially with multidimensional data blocks and batch systems, is that we have to pre-align the data. Not every dimension in these data cubes have the same number of entries.....

**In conclusion**, we require methods that:

	*	are able to rapidly extract the relevant information from a large quantity of data
	*	deal with missing data
	*	deal with 3-D and higher dimensional data sets
	*	be able to combine data on the same object, that is stored in different data tables
	*	handle collinearity in the data (low signal to noise ratio)
	*	assume measurement error in all the recorded data.

Latent variable methods are a suitable tool that meet these requirements.

