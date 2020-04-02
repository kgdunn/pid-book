.. _DOE-two-level-factorials:

Using two levels for two or more factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's take a look at the mechanics of factorial designs by using our previous example where the conversion, :math:`y`, is affected by two factors: temperature, :math:`T`, and substrate concentration, :math:`S`. 

The range over which they will be varied is given in the table. This range was identified by the process operators as being sufficient to actually show a difference in the conversion, but not so large as to move the system to a totally different operating regime (that's because we will fit a linear model to the data).

	.. tabularcolumns:: |l|c|c|

	+----------------------------+-----------------+-----------------+
	|  Factor                    |  Low level, |-| | High level, |+| |
	+============================+=================+=================+
	| Temperature, :math:`T`     |  338 K          | 354 K           |
	+----------------------------+-----------------+-----------------+
	| Substrate level, :math:`S` |  1.25 g/L       | 1.75 g/L        |
	+----------------------------+-----------------+-----------------+

#.	Write down the factors that will be varied: :math:`T` and :math:`S`.

#.	Write down the coded runs in standard order, also called :index:`Yates order`, which alternates the sign of the first variable the fastest and the last variable the slowest. By convention we start all runs at their low levels and finish off with all factors at their high levels. There will be :math:`2^k` runs, where :math:`k` is the number of variables in the design and the :math:`2` refers to the number of levels for each factor. In this case, :math:`2^2 = 4` experiments (runs). **We perform the actual experiments in random order**, but always write the table in this standard order.

	.. tabularcolumns:: |c|c|c|c|

	+-----------+---------------+-----------------+
	| Experiment| :math:`T` [K] | :math:`S` [g/L] |
	+===========+===============+=================+
	| 1         | |-|           | |-|             |
	+-----------+---------------+-----------------+
	| 2         | |+|           | |-|             |
	+-----------+---------------+-----------------+
	| 3         | |-|           | |+|             |
	+-----------+---------------+-----------------+
	| 4         | |+|           | |+|             |
	+-----------+---------------+-----------------+


#.	Add an additional column to the table for the response variable. The response variable is a quantitative value, :math:`y`, which in this case is the conversion measured as a percentage. 

	.. tabularcolumns:: |c|c|c|c||c|
	
	+-----------+-------+---------------+-----------------+--------------+
	| Experiment|Order  | :math:`T` [K] | :math:`S` [g/L] | :math:`y` [%]|
	+===========+=======+===============+=================+==============+
	| 1         | 3     | |-|           | |-|             |  69          |
	+-----------+-------+---------------+-----------------+--------------+
	| 2         | 2     | |+|           | |-|             |  60          |
	+-----------+-------+---------------+-----------------+--------------+
	| 3         | 4     | |-|           | |+|             |  64          |
	+-----------+-------+---------------+-----------------+--------------+
	| 4         | 1     | |+|           | |+|             |  53          |
	+-----------+-------+---------------+-----------------+--------------+
	
	Experiments were performed in random order; in this case, we happened to run experiment 4 first and experiment 3 last.

#.	For simple systems you can visualize the design and results :ref:`as shown in the following figure <DOE-fig-Cube-plot>`. This is known as a :index:`cube plot`.

	.. _DOE-fig-Cube-plot:
	.. image:: ../../figures/doe/factorial-two-levels-two-variables-no-analysis.png
		:align: center
		:scale: 40
		:width: 900px
		:alt: fake width
		
.. _DOE-two-level-factorials-main-effects:
		
Analysis of a factorial design: main effects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step is to calculate the :index:`main effect` of each variable. The effects are considered, by convention, to be the difference from the high level to the low level. So the interpretation of a main effect is by how much the outcome, :math:`y`, is adjusted when changing the variable.

.. youtube:: https://www.youtube.com/watch?v=fPbd74KN7zw&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=36

Consider the two runs where :math:`S` is at the |-| level for both experiments 1 and 2. The only change between these two runs is the **temperature**, so the temperature effect is :math:`\Delta T_{S-} = 60-69 = -9\%\,\,\text{per}\,\,(354-338)~\text{K}`, that is, a :math:`-9\%` change in the conversion outcome per :math:`+16~\text{K}` change in the temperature. 

Runs 3 and 4 both have :math:`S` at the |+| level. Again, the only change is in the **temperature**: :math:`\Delta T_{S+} = 53-64 = -11\%` per :math:`+16~\text{K}`. So we now have two temperature effects, and the average of them is a :math:`-10\%` change in conversion per :math:`+16~\text{K}` change in temperature.

We can perform a similar calculation for the main effect of substrate concentration, :math:`S`, by comparing experiments 1 and 3: :math:`\Delta S_{T-} = 64-69 = -5\%\,\,\text{per}\,\,0.5\,\text{g/L}`, while experiments 2 and 4 give :math:`\Delta S_{T+} = 53-60 = -7\%` per :math:`0.5\,\text{g/L}`. So the average main effect for :math:`S` is a :math:`-6\%` change in conversion for every :math:`0.5\,\text{g/L}` change in substrate concentration. You should use the following :ref:`graphical method <DOE-fig-Calculate-main-effects>` when calculating main effects from a cube plot by hand.


.. _DOE-fig-Calculate-main-effects:
.. image:: ../../figures/doe/factorial-two-levels-two-variables-with-analysis.png
	:align: center
	:scale: 50
	
This visual summary is a very effective method of seeing how the system responds to the two variables. We can see the gradients in the system and the likely region where we can perform the next experiments to improve the bioreactor's conversion.

The following surface plot illustrates the true, but unknown, surface from which our measurements are taken. Notice the slight curvature on the edges of each face. The main effects estimated above are a linear approximation of the conversion over the region spanned by the factorial.

	.. image:: ../../figures/doe/factorial-two-level-surface-example-cropped.png
		:align: left
		:scale: 50
		:alt: fake width
		:width: 900px

An :index:`interaction plot` is an :ref:`alternative way to visualize these main effects <DOE-fig-Interaction-plot-example>`. Use this method when you don't have computer software to draw the surfaces. [We saw this earlier in the :ref:`visualization section <SECTION-data-visualization>`]. We will discuss interaction plots more in the next section. Here is an illustration of one such plot for a system with little interaction.

	.. _DOE-fig-Interaction-plot-example:
	.. image:: ../../figures/doe/factorial-two-level-line-plot.png
		:align: center
		:scale: 80
		
.. _DOE-two-level-factorials-interaction-effects:	

Analysis of a factorial design: interaction effects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=_NIA8RGGtAs&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=37

We expect in many real systems that the main effect of temperature, :math:`T`, for example, is different at other levels of substrate concentration, :math:`S`. It is quite plausible for a bioreactor system that the main temperature effect on conversion is much greater if the substrate concentration, :math:`S`, is also high, while at low values of :math:`S`, the temperature effect is smaller. 

.. index:: interaction effects

We call this result an *interaction*, when the effect of one factor is different at different levels of the other factors. Let's give a practical, everyday example: assume your hands are covered with dirt or oil. We know that if you wash your hands with cold water, it will take longer to clean them than washing with hot water. So let factor **A** be the temperature of the water; factor **A** has a significant effect on the time taken to clean your hands.  

Consider the case when washing your hands with cold water. If you use soap with cold water, it will take less time to clean your hands than if you did not use soap. It is clear that factor **B**, the categorical factor of using no soap vs some soap, will reduce the time to clean your hands. 

Now consider the case when washing your hands with hot water. The time taken to clean your hands with hot water when you use soap is greatly reduced, far faster than any other combination. We say there is an interaction between using soap and the temperature of the water. This is an example of an interaction that works to help us reach the objective faster. 

The effect of warm water enhances the effect of soap. Conversely, the effect is soap is enhanced by using warm water. So symmetry means that if soap interacts with water temperature, then we also know that water temperature interacts with soap.

In summary, interaction means the effect of one factor depends on the level of the other factor. In this example, that implies the effect of soap is different, depending on if we use cold water or hot water. Interactions are also symmetrical. The soap’s effect is enhanced by warm water, and the warm water’s effect is enhanced by soap. 

Let's use a :ref:`different system here to illustrate <DOE-fig-interaction-example-contour-plot>` interaction effects, but still using :math:`T` and :math:`S` as the variables being changed and keeping the response variable, :math:`y`, as the conversion, shown by the contour lines.

	.. _DOE-fig-interaction-example-contour-plot:
	.. image:: ../../figures/doe/factorial-two-level-with-interactions.png
		:align: center
		:scale: 40
		:width: 900px
		:alt: fake width

	.. tabularcolumns:: |l|c|c||c|
	
	+-----------+---------------+-----------------+--------------+
	| Experiment| :math:`T` [K] | :math:`S` [g/L] | :math:`y` [%]|
	+===========+===============+=================+==============+
	| 1         | |-|  (390 K)  | |-| (0.5 g/L)   |  77          |
	+-----------+---------------+-----------------+--------------+
	| 2         | |+|  (400 K)  | |-| (0.5 g/L)   |  79          |
	+-----------+---------------+-----------------+--------------+
	| 3         | |-|  (390 K)  | |+| (1.25 g/L)  |  81          |
	+-----------+---------------+-----------------+--------------+
	| 4         | |+|  (400 K)  | |+| (1.25 g/L)  |  89          |
	+-----------+---------------+-----------------+--------------+

The main effect of temperature for this system is
		
		-	:math:`\Delta T_{S-} = 79 - 77 = 2\%` per 10 K
		-	:math:`\Delta T_{S+} = 89 - 81 = 8\%` per 10 K

which means that the average temperature main effect is 5% per 10 K.
		
Notice how different the main effect is at the low and high levels of :math:`S`. So the average of the two is an incomplete description of the system. There is some other aspect to the system that we have not captured.

Similarly, the main effect of substrate concentration is
	
		-	:math:`\Delta S_{T-} = 81 - 77 = 4\%` per 0.75 g/L
		-	:math:`\Delta S_{T-} = 89 - 79 = 10\%` per 0.75 g/L

which gives the average substrate concentration main effect as 7% per 0.75 g/L.

.. TODO: Draw in Inkscape, the geometrical analysis of the main effects, and the interaction plot for this system: annotated with T effect at low S, T effect at high S, S effect at low T, S effect at high T

The data may also be visualized using an :ref:`interaction plot <DOE-fig-interaction-plot-with-interaction>` here, showing a higher degree of interaction.

.. _DOE-fig-interaction-plot-with-interaction:
.. image:: ../../figures/doe/factorial-two-level-line-plot-with-interaction.png
	:align: center
	:scale: 100
	
The lack of parallel lines is a clear indication of interaction. The temperature effect is stronger at high levels of :math:`S`, and the effect of :math:`S` on conversion is also greater at high levels of temperature. What is missing is an interaction term, given by the product of temperature and substrate. We represent this as  :math:`T \times S` and call it the temperature-substrate interaction term.  

This interaction term should be zero for systems with no interaction, which implies the lines are parallel in the interaction plot. Such systems will have roughly the same effect of :math:`T` at both low and high values of :math:`S` (and in between). So then, a good way to quantify interaction is by how different the main effect terms are at the high and low levels of the other factor in the interaction. The interaction *must* also be symmetrical: if :math:`T` interacts with :math:`S`, then :math:`S` interacts with :math:`T` by the same amount.

We can quantify the interaction of our current example in this way. For the :math:`T` interaction with :math:`S`:  

	-	Change in conversion due to :math:`T` at high :math:`S`: :math:`89 - 81 = +8`
	-	Change in conversion due to :math:`T` at low :math:`S`: :math:`79 - 77 = +2`
	-	The half difference: :math:`[+8 - (+2)]/2 = \bf{3}`
	
For the :math:`S` interaction with :math:`T`,

	-	Change in conversion due to :math:`S` at high :math:`T`: :math:`89 - 79 = +10`
	-	Change in conversion due to :math:`S` at low :math:`T`: :math:`81 - 77 = +4`
	-	The half difference: :math:`[+10 - (+4)]/2 = \bf{3}`

A large, positive interaction term indicates that temperature and substrate concentration will increase conversion by a greater amount when both :math:`T` and :math:`S` are high. Similarly, these two terms will rapidly reduce conversion when they both are low.

We will get an improved appreciation for interpreting main effects and the interaction effect when we consider the analysis in the form of a linear, least squares model.

.. TODO: point out the interaction is a separate, independent effect from the b_0, b_T and b_S effects.

.. TODO: quantify and describe more completely what the interaction means

