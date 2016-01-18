Example: design and analysis of a three-factor experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=H_s5gGyXor8&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=38


This example should be done by yourself. It is based on Question 19 in the exercises for Chapter 5 in Box, Hunter and Hunter (2nd edition).

The data are from a plastics molding factory that must treat its waste before discharge. The :math:`y`-variable represents the average amount of pollutant discharged (lb per day), while the three factors that were varied were

 	-	:math:`C` = the chemical compound added (choose either chemical P or chemical Q)
	-	:math:`T` = the treatment temperature (72 °F or 100 °F)
	-	:math:`S` = the stirring speed (200 rpm or 400 rpm)
	-	:math:`y` = the amount of pollutant discharged (lb per day)

	.. tabularcolumns:: |l|l||c|c|c||c|

	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| Experiment| Order | :math:`C`     | :math:`T` [°F]  | :math:`S` [rpm] | :math:`y` [lb]  |
	+===========+=======+===============+=================+=================+=================+
	| 1         | 5     | Choice P      | 72              | 200             | 5               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 2         | 6     | Choice Q      | 72              | 200             | 30              |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 3         | 1     | Choice P      | 100             | 200             | 6               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 4         | 4     | Choice Q      | 100             | 200             | 33              |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 5         | 2     | Choice P      | 72              | 400             | 4               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 6         | 7     | Choice Q      | 72              | 400             | 3               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 7         | 3     | Choice P      | 100             | 400             | 5               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 8         | 8     | Choice Q      | 100             | 400             | 4               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+

#.	Draw a geometric figure that illustrates the data from this experiment.

#.	Calculate the main effect for each factor by hand.

		For the **C effect**, there are four estimates of :math:`C`:

		.. math::
			\displaystyle \frac{(+25) + (+27) + (-1) + (-1)}{4} = \frac{50}{4} = \bf{12.5}
	
		For the	**T effect**, there are four estimates of :math:`T`:

		.. math::
			\displaystyle \frac{(+1) + (+3) + (+1) + (+1)}{4} = \frac{6}{4} = \bf{1.5}
	
		For the **S effect**, there are four estimates of :math:`S`:

		.. math::
			\displaystyle \frac{(-27) + (-1) + (-29) + (-1)}{4} = \frac{-58}{4} = \bf{-14.5}

#.	Calculate the 3 two-factor interactions (2fi) by hand, recalling that interactions are defined as the half difference going from high to low.

		For the **CT interaction**, there are two estimates of :math:`CT`. Recall that interactions are calculated as the half difference going from high to low. Consider the change in :math:`C` when

		*	:math:`T_\text{high}` (at :math:`S` high) = :math:`4 - 5 = -1`
		*	:math:`T_\text{low}` (at :math:`S` high) = :math:`3 - 4 = -1`
		
		This gives a first estimate of :math:`[(-1) - (-1)]/2 = 0`. Similarly,

		*	:math:`T_\text{high}` (at :math:`S` low) = :math:`33 - 6 = +27`
		*	:math:`T_\text{low}` (at :math:`S` low) = :math:`30 - 5 = +25`
		
		gives a second estimate of :math:`[(+27) - (+25)]/2 = +1`.
	
		The average **CT** interaction  is therefore :math:`(0 + 1)/2 = \mathbf{0.5}`. You can interchange :math:`C` and :math:`T` and still get the same result.

		For the **CS interaction**, there are two estimates of :math:`CS`.  Consider the change in :math:`C` when

		*	:math:`S_\text{high}` (at :math:`T` high) = :math:`4 - 5 = -1`
		*	:math:`S_\text{low}` (at :math:`T` high) = :math:`33 - 6 = +27`
			
		This gives a first estimate of :math:`[(-1) - (+27)]/2 = -14`. Similarly,

		*	:math:`S_\text{high}` (at :math:`T` low) = :math:`3 - 4 = -1`
		*	:math:`S_\text{low}` (at :math:`T` low) = :math:`30 - 5 = +25`
			
		gives a second estimate of :math:`[(-1) - (+25)]/2 = -13`.

		The average **CS** interaction is therefore :math:`(-13 - 14)/2 = \mathbf{-13.5}`. You can interchange :math:`C` and :math:`S` and still get the same result.	
		
		For the **ST interaction**, there are two estimates of :math:`ST`: :math:`(-1 + 0)/2 = \mathbf{-0.5}`. Calculate in the same way as above.

#.	Calculate the single three-factor interaction (3fi).
	
		There is only a single estimate of :math:`CTS`. The :math:`CT` effect at high :math:`S` is 0, and the :math:`CT` effect at low :math:`S` is :math:`+1`. The :math:`CTS` interaction is then :math:`[(0) - (+1)] / 2 = \mathbf{-0.5}`.

		You can also calculate this by considering the :math:`CS` effect at the two levels of :math:`T`, or by considering the :math:`ST` effect at the two levels of :math:`C`. All three approaches give the same result.

#.	Compute the main effects and interactions using matrix algebra and a least squares model.

	.. youtube:: https://www.youtube.com/watch?v=5qBTXnfp94M&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=41

	.. math::

		\begin{bmatrix} 5\\30\\6\\33\\4\\3\\5\\4 \end{bmatrix} &=
		\begin{bmatrix} +1 & -1 & -1 & -1 & +1 & \mathbf{+1} & +1 & -1\\ 
		                +1 & +1 & -1 & -1 & -1 & \mathbf{-1} & +1 & +1\\
		                +1 & -1 & +1 & -1 & -1 & \mathbf{+1} & -1 & +1\\
		                +1 & +1 & +1 & -1 & +1 & \mathbf{-1} & -1 & -1\\
		                +1 & -1 & -1 & +1 & +1 & \mathbf{-1} & -1 & +1\\
		                +1 & +1 & -1 & +1 & -1 & \mathbf{+1} & -1 & -1\\
		                +1 & -1 & +1 & +1 & -1 & \mathbf{-1} & +1 & -1\\
		                +1 & +1 & +1 & +1 & +1 & \mathbf{+1} & +1 & +1\\
		\end{bmatrix}
		\begin{bmatrix} b_0 \\ b_C \\ b_T \\ b_{S} \\ b_{CT} \\ b_{CS} \\ b_{TS} \\ b_{CTS}  \end{bmatrix} \\
		\mathbf{y} &= \mathbf{X} \mathbf{b} 
	
#.	Use computer software to build the following model and verify that:

	.. math:: 
	
		y = 11.25 + 6.25x_C + 0.75x_T -7.25x_S + 0.25 x_C x_T -6.75 x_C x_S -0.25 x_T x_S - 0.25 x_C x_T x_S

Learning notes:

	*	The chemical compound could be coded either as (chemical P = :math:`-1`, chemical Q = :math:`+1`) or (chemical P = :math:`+1`, chemical Q = :math:`-1`). The interpretation of the :math:`x_C` coefficient is the same, regardless of the coding.
	
 	*	Just the tabulation of the raw data gives us some interpretation of the results. Why?  Since the variables are manipulated independently, we can just look at the relationship of each factor to :math:`y`, without considering the others.  It is expected that the chemical compound and speed have a strong effect on :math:`y`, but we can also see the **chemical** :math:`\times` **speed** interaction. You can see this last interpretation by writing out the full :math:`\mathbf{X}` design matrix and comparing the bold column, associated with the :math:`b_\text{CS}` term, with the :math:`y` column.
	
.. rubric:: A note about magnitude of effects

In this text we quantify the effect as the change in response over *half the range* of the factor. For example, if the center point is 400 K, the lower level is 375 K and the upper level is 425 K, then an effect of ``"-5"`` represents a reduction in :math:`y` of 5 units for every increase of 25 K in :math:`x`.
	
We use this representation because it corresponds with the results calculated from least-squares software. Putting the matrix of :math:`-1` and :math:`+1` entries into the software as :math:`\mathbf{X}`, along with the corresponding vector of responses, :math:`y`, you can calculate these effects as :math:`\mathbf{b} = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}\mathbf{y}`.

Other textbooks, specifically Box, Hunter and Hunter, will report effects that are double ours. This is because they consider the effect to be the change from the lower level to the upper level (double the distance). The advantage of their representation is that binary factors (catalyst A or B; agitator on or off) can be readily interpreted, whereas in our notation, the effect is a little harder to describe (simply double it!).

The advantage of our methodology, though, is that the results calculated by hand would be the same as those from any computer software with respect to the magnitude of the coefficients and the standard errors, particularly in the case of duplicate runs and experiments with center points.

Remember: our effects are half those reported in Box, Hunter and Hunter, and in some other textbooks; our standard error would also be half of theirs. The conclusions drawn will always be the same, as long as one is consistent.

