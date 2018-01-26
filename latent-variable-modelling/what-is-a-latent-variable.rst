What is a latent variable?
===================================================

.. index::
	pair: latent variable modelling; what is a latent variable

We will take a look at what a latent variable is conceptually, geometrically, and mathematically.

Your health
~~~~~~~~~~~~~~~~~~~~~~~~

Your overall health is a latent variable. But there isn't a single measurement of "*health*" that can be measured - it is a rather abstract concept. Instead we measure physical properties from our bodies, such as blood pressure, cholesterol level, weight, various distances (waist, hips, chest), blood sugar, temperature, and a variety of other measurements. These separate measurements can be used by a trained person to judge your health, based on their experience of seeing these values from a variety of healthy and unhealthy patients.

In this example, your *health* is a latent, or hidden variable. If we had a sensor for health, we could measure and use that variable, but since we don't, we use other measurements which all contribute in some way to assessing health.

.. _LVM_room_temperature_example:

Room temperature
~~~~~~~~~~~~~~~~~~~~~~~~

**Conceptually**

Imagine the room you are in has 4 temperature probes that sample and record the local temperature every 30 minutes. Here is an example of what the four measurements might look like over 3 days.

.. image:: ../figures/examples/room-temperature/room-temperature-plots.png
	:alt:	../figures/examples/room-temperature/room-temperature-plots.py
	:scale: 70
	:width: 900px
	:align: center
	
In table form, the first few measurements are:

.. csv-table:: 
   :header: Date, :math:`x_1`, :math:`x_2`, :math:`x_3`, :math:`x_4`
   :widths: 50, 30, 30, 30, 30

	Friday 11:00, 295.2,     297.0,     295.8,     296.3
	Friday 11:30, 296.2,     296.4,     296.2,     296.3
	Friday 12:00, 297.3,     297.5,     296.7,     297.1
	Friday 12:30, 295.9,     296.7,     297.4,     297.0
	Friday 13:00, 297.2,     296.5,     297.6,     297.4
	Friday 13:30, 296.6,     297.7,     296.7,     296.5

.. Some questions that come to mind are what are fluctuations due to in the data; what is the sharp spike in the 3rd measurement due to; and why is there an unusual dip in the first temperature measurement?

The general up and down fluctuations are due to the daily change in the room's temperature. The single, physical phenomenon being recorded in these four measurements is just the variation in room temperature.  

If we added two more thermometers in the middle of the room, we would expect these new measurements to show the same pattern as the other four. In that regard we can add as many thermometers as we like to the room, but we won't be recording some new, independent piece of information with each thermometer. There is only one true variable that drives all the temperature readings up and down: it is a latent variable. 

Notice that we don't necessarily have to know what *causes* the latent variable to move up and down (it could be the amount of sunlight on the building; it could be the air-conditioner's settings). All we know is that these temperature measurements just reflect the underlying phenomenon that drives the up-and-down movements in temperature; they are *correlated* with the latent variable.

Notice also the sharp spike recorded at the back-left corner of the room could be due to an error in the temperature sensor. And the front part of the room showed a dip, maybe because the door was left open for an extended period; but not long enough to affect the other temperature readings.  These two events go against the general trend of the data, so we expect these periods of time to *stand out* in some way, so that we can detect them. 

**Mathematically**

If we wanted to summarize the events taking place in the room we might just use the average of the recorded temperatures. Let's call this new, average variable :math:`t_1`, which summarizes the other four original temperature measurements :math:`x_1, x_2, x_3` and :math:`x_4`.

.. math:: t_1 &= \begin{bmatrix} x_1 & x_2 & x_3 & x_4 \end{bmatrix}\begin{bmatrix} p_{1,1} \\ p_{2,1} \\ p_{3,1} \\ p_{4,1} \end{bmatrix} = x_1 p_{1,1} + x_2 p_{2,1} + x_3 p_{3,1} + x_4 p_{4,1} 

and suitable values for each of the weights are :math:`p_{1,1} = p_{2,1} = p_{3,1} = p_{4,1} = 1/4`.

.. _LVM_linear_combination:

Mathematically the correct way to say this is that :math:`t_1` is a *linear combination* of the raw measurements (:math:`x_1, x_2, x_3` and :math:`x_4`) given by the weights (:math:`p_{1,1}, p_{2,1}, p_{3,1}, p_{4,1}`).

**Geometrically**

We can visualize the data from this system in several ways, but we will simply show a 3-D representation of the first 3 temperatures: :math:`x_1, x_2, x_3`.

.. image:: ../figures/examples/room-temperature/room-temperature-plots-combine.png
	:alt:	../figures/examples/room-temperature/room-temperature-plots-combine.py
	:scale: 70
	:width: 900px
	:align: center

The 3 plots show the same set of data, just from different points of view. Each observation is a single dot, the location of which is determined by the recorded values of temperature, :math:`x_1, x_2` and :math:`x_3`. We will use this representation in the next section again.

Note how correlated the data appear: forming a diagonal line across the cube's interior, with a few outliers (described above) that don't obey this trend.

.. OMIT FOR NOW

	Thickness of wood boards
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	Wood boards (for example 2 by 4 boards) are measured for thickness at 6 locations prior to leaving the lumber mill (see the illustration). Three important quality variables are derived from these 6 measurements:

		* :math:`x_1` = average tail thickness: average of thickness 1 and 4
		* :math:`x_2` = average feed thickness: average of thickness 3 and 6
		* :math:`x_3` = average taper: average of thickness 1, 2 and 3 subtracted from average thickness 4, 5, and 6

		.. figure:: ../figures/examples/board-thickness//board_measurement_locations.png
			:alt:	../figures/examples/board-thickness//board_measurement_locations.svg
			:scale: 50
			:width: 900px
			:align: center


	Imagine that we have data from 100 boards, so we could represent this raw data a matrix where each row are the 3 measurements from one board.

	.. math:: 
		\underbrace{\mathbf{X}_\text{raw}}_{100 \times 3}
	
	The plots of these different thicknesses are 

	.. figure:: ../figures/examples/board-thickness/board-thickness-2d-and-3d-plot.png
		:alt:	../figures/examples/board-thickness/board-thickness-data-combine.py
		:scale: 70
		:width: 900px
		:align: center

	It is not surprising that the feed and tail thickness are related to each other. They are expected to have a positive correlation, because if the board is thicker, it will be thick at all locations. The taper measurement is unrelated to the boards thickness, since it doesn't matter if the board is thick or thin: it can still be tapered.

	So there are two latent variables in this system: 

		#.	The fact that the entire board is thicker or thinner is captured by the feed and tail thickness measurements.  These measurements are correlated with whatever physical phenomenon causes that average thickness to increase or decrease (e.g. spacing of the saw blades).
		#.	The third measurement, taper of the board, is capturing a different phenomenon in the system; possibly caused by how much the blades are skewed out of alignment. 
	
		.. But unless we perform an experiment where we change the saw alignment and measure the taper, we won't be sure that this is a causal relationship. 

	The main points from this section so far:

		*	Latent variables capture, in some way, an underlying phenomenon in the system being investigated.
		*	The actual measurements we take on the system are *correlated* with the latent variable.
		*	Latent variables that are unrelated to to each other are said to be independent, or orthogonal to each other.

	Latent variable modelling is concerned with how we can reduce the number of values we measure on each observation, but still retain the important features. In this example of the board thickness, we could use an average of the feed and tail measurements as one of the summary variables, called :math:`t_1`. And since the taper is independent of thickness, we would retain a second latent variable, called :math:`t_2`, that captures the taper measurement.

		.. math::
	
			t_1 &= \begin{bmatrix} x_1 & x_2 & x_3 \end{bmatrix}\begin{bmatrix} p_{1,1} \\ p_{2,1} \\ p_{3,1} \end{bmatrix} = x_1 p_{1,1} + x_2 p_{2,1} + x_3 p_{3,1}  \\
			t_2 &= \begin{bmatrix} x_1 & x_2 & x_3 \end{bmatrix}\begin{bmatrix} p_{1,2} \\ p_{2,2} \\ p_{3,2} \end{bmatrix} = x_1 p_{1,2} + x_2 p_{2,2} + x_3 p_{3,2}

	So using the measurements from each board, :math:`\begin{bmatrix} x_1, & x_2, & x_3 \end{bmatrix}` we obtain two derived values, :math:`\begin{bmatrix} t_1, & t_2 \end{bmatrix}`. These two values are intended to capture the essence of the original measurements. The weights :math:`p_{k,a}` are selected so that we meet that objective.

	What values would be suitable for the weights?  One option might be that:

	.. math::	
			t_1 &= \begin{bmatrix} x_1 & x_2 & x_3 \end{bmatrix}\begin{bmatrix} 1/2 \\ 1/2 \\ 0 \end{bmatrix} = \dfrac{x_1}{2} + \dfrac{x_2}{2} + 0 \\
			t_2 &= \begin{bmatrix} x_1 & x_2 & x_3 \end{bmatrix}\begin{bmatrix} 0 \\ 0 \\ \,1\, \end{bmatrix} = 0 + 0 + x_3
		
	or more compactly:

	.. math::
			\mathbf{t}' = \begin{bmatrix} t_1 & t_2 \end{bmatrix} &=
			\begin{bmatrix} x_1 & x_2 & x_3 \end{bmatrix} 
			\begin{bmatrix}  0.5 & 0 \\ 0.5 & 0 \\ 0  & 1  \end{bmatrix} =
			\begin{bmatrix} x_1 & x_2 & x_3 \end{bmatrix}
			\begin{bmatrix} p_{1,1} & p_{1,2}\\ p_{2,1} & p_{2,2} \\ p_{3,1} & p_{3,2} \end{bmatrix} =
			 \underbrace{\mathbf{x}_\text{raw}}_{1 \times 3} \underbrace{\mathbf{P}}_{3 \times 2} = \underbrace{\begin{bmatrix} t_1 & t_2 \end{bmatrix}}_{1 \times 2}
		
	The matrix |P| can now be used to take any vector of board measurements, represented as vector :math:`\mathbf{x}`, and calculate a summary vector, |t|, from it.

.. BACK TO NORMAL

The main points from this section are:

	*	Latent variables capture, in some way, an underlying phenomenon in the system being investigated.
	*	After calculating the latent variables in a system, we can use these fewer number of variables, instead of the :math:`K` columns of raw data. This is because the actual measurements are *correlated* with the latent variable.
	
The examples given so far showed what a single latent variables is. In practice we usually obtain several latent variables for a data array. At this stage you likely have more questions, such as "*how many latent variables are there in a matrix*" and "*how are the values in* |P| *chosen*", and "*how do we know these latent variables are a good summary of the original data*"?

We address these issues more formally in the next section on :ref:`principal component analysis <SECTION_PCA>`.

