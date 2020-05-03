.. _DOE-RSM:

Response surface methods
==========================

.. youtube:: https://www.youtube.com/watch?v=CFoj2mEVWvA&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=51

.. Add this somewhere appropriate: http://xkcd.com/605/   .... on extrapolation

The purpose of :index:`response surface methods <pair: response surface methods; experiments>` (RSM) is to optimize a process or system. RSM is a way to explore the effect of operating conditions (the factors) on the response variable, :math:`y`. As we map out the unknown response surface of :math:`y`, we move our process as close as possible towards the optimum, taking into account any constraints.

Initially, when we are far away from the optimum, we will use factorial experiments. As we approach the optimum then these factorials are replaced with better designs that more closely approximate conditions at the optimum.

.. TODO: RSM overview figure here with COST approach superimposed

Notice how it is a *sequential* approach. RSM then is a tool the describes how we should run these sequential sets of experiments. At the start of this :ref:`section on designed experiments <DOE-COST-approach>` we showed how sequential experimentation (COST) leads to sub-optimal solutions. Why are we advocating sequential experimentation now?   The difference is that here we use sequential experiments by changing *multiple factors simultaneously*, and not changing only one factor at a time.

.. rubric:: RSM concept for a single variable: COST approach

We will however first consider just the effect of a single factor, :math:`x_1` as it relates to our response, :math:`y`. This is to illustrate the general response surface process.

.. youtube:: https://www.youtube.com/watch?v=id71dS8b8EA&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=52

.. image:: ../figures/doe/steepest-ascent-univariately-corrected.png
	:alt: steepest-ascent-univariately.svg
	:align: left
	:scale: 70
	:width: 900px

We start at the point marked :math:`i=0` as our initial baseline (cp=center point). We run a 2-level experiment, above and below this baseline at :math:`-1` and :math:`+1`, in coded units of :math:`x_1`, and obtain the corresponding response values of :math:`y_{0,-}` and :math:`y_{0,+}`. From this we can estimate a best-fit straight line and move in the direction that increases :math:`y`. The sloping tangential line, also called the *path of steepest ascent*. Make a move of step-size = :math:`\gamma_1` units along :math:`x_1` and measure the response, recorded as :math:`y_1`. The response variable increased, so we keep going in this direction.

Make another step-size, this time of :math:`\gamma_2` units in the direction that increases :math:`y`. We measure the response, :math:`y_2`, and are still increasing. Encouraged by this, we take another step of size :math:`\gamma_3`. The step-sizes, :math:`\gamma_i` should be of a size that is big enough to cause a change in the response in a reasonable number of experiments, but not so big as to miss an optimum.

Our next value of :math:`y_3` is about the same size as :math:`y_2`, indicating that we have plateaued. At this point we can take some exploratory steps and refit the tangential line (which now has a slope in the opposite direction). Or we can just use the accumulated points :math:`y = [y_{0-},\,\, y_{0+},\,\, y_1,\,\, y_2,\,\, y_3]` and their corresponding :math:`x`-values to fit a non-linear curve. Either way, we can then estimate a different step-size :math:`\gamma_4` that will bring us closer to the optimum.

This univariate example is in fact what experimenters do when using the :ref:`COST approach <DOE-COST-approach>` described earlier. We have:

* exploratory steps of different sizes towards an optimum
* refit the model once we plateau
* repeat

.. youtube:: https://www.youtube.com/watch?v=jSOBZ4yT3Sc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=53

This approach works well if there really is only a single factor that affects the response. But with most systems there are multiple factors that affect the response. We show next how the exact same idea is used, only we change multiple variables at a time to find the optimum on the response surface.

Response surface optimization via a 2-variable system example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=7WXN3QgzkbE&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=54

This example considers a new system here where two factors, temperature **T**, and substrate concentration **S** are known to affect the yield from a bioreactor. But in this example we are not just interested in yield, but actually the total profit from the system. This profit takes into account energy costs, raw materials costs and other relevant factors. The illustrations in this section show the contours of profit in light grey, but in practice these are obviously unknown.

We currently operate at this baseline condition:

	*	**T** = 325 K
	*	**S** = 0.75 g/L
	*	Profit = $407 per day

We start by creating a full factorial around this baseline by choosing :math:`\Delta_T = 10` K, and :math:`\Delta_S = 0.5` g/L based on our knowledge that  these are sufficiently large changes to show an actual difference in the response value, but not too large so as to move to a totally different form of operation in the bioreactor.

The results from the full factorial are in the table here:

.. tabularcolumns:: |c||c|c||c|c||c|

+-----------+------------+-----------+------------+-----------+------------+
| Experiment| T (actual) | S (actual)| T (coded)  | S (coded) |  Profit    |
+===========+============+===========+============+===========+============+
| Baseline  | 325 K      | 0.75 g/L  | 0          | 0         |  407       |
+-----------+------------+-----------+------------+-----------+------------+
| 1         | 320 K      | 0.50 g/L  | |-|        | |-|       |  193       |
+-----------+------------+-----------+------------+-----------+------------+
| 2         | 330 K      | 0.50 g/L  | |+|        | |-|       |  310       |
+-----------+------------+-----------+------------+-----------+------------+
| 3         | 320 K      | 1.0 g/L   | |-|        | |+|       |  468       |
+-----------+------------+-----------+------------+-----------+------------+
| 4         | 330 K      | 1.0 g/L   | |+|        | |+|       |  571       |
+-----------+------------+-----------+------------+-----------+------------+

Clearly the promising direction to maximize profit is to operate at higher temperatures and higher substrate concentrations. But how much much higher and in what ratio should we increase :math:`T` and :math:`S`?  These answers are found by building a linear model of the system from the factorial data:

.. math::

	\hat{y} &= b_0 + b_T x_T + b_S x_S + b_{TS} x_T x_S \\
	\hat{y} &= 389.8 + 55 x_T + 134 x_S - 3.50 x_T x_S

where :math:`x_T = \dfrac{x_{T,\text{actual}} - \text{center}_T}{\Delta_T / 2} = \dfrac{x_{T,\text{actual}} - 325}{5}` and similarly,  :math:`x_S = \dfrac{x_{S,\text{actual}} - 0.75}{0.25}`.

The model shows that we can expect an increase of $55/day of profit for a unit increase in :math:`x_T` (coded units). In real-world units that would require increasing temperature by :math:`\Delta x_{T,\text{actual}} = (1) \times \Delta_T /2` = 5K to achieve that goal. That scaling factor comes from the coding we used:

.. math::

	x_T &= \displaystyle \frac{x_{T,\text{actual}} - \text{center}_T}{\Delta_T / 2} \\
	\Delta x_T &= \displaystyle \frac{\Delta x_{T,\text{actual}}}{\Delta_T / 2}

Similarly, we can increase :math:`S` by :math:`\Delta x_S = \text{1 unit} = 1 \times \Delta_S/2 = 0.5/2` = 0.25 g/L real-world units, to achieve a $134 per day profit increase.

The interaction term is small, indicating the response surface is mostly linear in this region. The illustration shows the model's contours (straight, green lines). Notice that the model contours are a good approximation to the actual contours (dotted, light grey), which are unknown in practice.

.. image:: ../figures/doe/RSM-base-case-with-first-factorial-notes.png
	:alt:	RSM-base-case.py
	:align: left
	:scale: 40
	:width: 900px

To improve our profit in the optimal way we move along our estimated model's surface, in the direction of steepest ascent. This direction is found by taking partial derivatives of the model function, ignoring the interaction term, since it is so small.

.. math::

		\dfrac{\partial \hat{y}}{\partial x_T} = b_T = 55  \qquad \qquad  \dfrac{\partial \hat{y}}{\partial x_S} = b_S = 134

This says for every :math:`b_T = 55` coded units that we move by in :math:`x_T` we should also move :math:`x_S` by :math:`b_S = 134` coded units. Mathematically:

.. math::

	\frac{\Delta x_S}{\Delta x_T} = \frac{134}{55}

The simplest way to do this is just to pick a move size in one of the variables, then change the move size of the other one.

So we will choose to increase :math:`\Delta x_T = 1` coded unit, which means:

.. math::

                                        \Delta x_T &= 1 \\
                        \Delta x_{T,\text{actual}} &= 5 \,\text{K} \\
	                                    \Delta x_S &= \frac{b_S}{b_T} \Delta x_T = \frac{134}{55} \Delta x_T \\
	\text{but we know that}\qquad\qquad \Delta x_S &= \frac{x_{S,\text{actual}}}{\Delta_S / 2} \\
	                    \Delta x_{S,\text{actual}} &= \frac{134}{55} \times 1 \times \Delta_S / 2\,\, \text{by equating previous 2 lines} \\
	                    \Delta x_{S,\text{actual}} &= \frac{134}{55} \times 1 \times 0.5 / 2  = \bf{0.61}\,\,\text{g/L}\\

*	:math:`T_5 = T_\text{baseline} + \Delta x_{T,\text{actual}} = 325 + 5 = 330` K
*	:math:`S_5 = S_\text{baseline} + \Delta x_{S,\text{actual}} = 0.75 + 0.6 = 1.36` g/L

So when we run the next experiment at these conditions. The daily profit is :math:`y_5 =` $ 669, improving quite substantially from the  baseline case.

We decide to make another move, in the same direction of steepest ascent, i.e. along the vector that points in the :math:`\frac{134}{55}` direction. We  move the temperature up 5K, although we could have used a larger or smaller step size if we wanted:

	*	:math:`T_6 = T_5 + \Delta x_{T,\text{actual}} = 330 + 5 = 335` K
	*	:math:`S_6 = S_5 + \Delta x_{S,\text{actual}} = 1.36 + 0.61 = 1.97` g/L

Again, we determine profit at :math:`y_6 =` $ 688. It is still increasing, but not by nearly as much. Perhaps we are starting to level off. However, we still decide to move temperature up by another 5 K and increase the substrate concentration in the required ratio:

	*	:math:`T_7 = T_6 + \Delta x_{T,\text{actual}} = 335 + 5 = 340` K
	*	:math:`S_7 = S_6 + \Delta x_{S,\text{actual}} = 1.97 + 0.61 = 2.58` g/L

The profit at this point is :math:`y_7 =` $ 463. We have gone too far as profit has dropped off. So we return back to our *last best point*, because the surface has obviously changed, and we should refit our model with a new factorial in this neighbourhood:

.. tabularcolumns:: |c||c|c||c|c||c|

+-----------+------------+-----------+------------+--------------+------------+
| Experiment| T (actual) | S (actual)| T          | S            |  Profit    |
+===========+============+===========+============+==============+============+
| 6         | 335 K      | 1.97 g/L  | 0          | 0            |  688       |
+-----------+------------+-----------+------------+--------------+------------+
| 8         | 331 K      | 1.77 g/L  | |-|        | |-|          |  694       |
+-----------+------------+-----------+------------+--------------+------------+
| 9         | 339 K      | 1.77 g/L  | |+|        | |-|          |  725       |
+-----------+------------+-----------+------------+--------------+------------+
| 10        | 331 K      | 2.17 g/L  | |-|        | |+|          |  620       |
+-----------+------------+-----------+------------+--------------+------------+
| 11        | 339 K      | 2.17 g/L  | |+|        | |+|          |  642       |
+-----------+------------+-----------+------------+--------------+------------+

This time we have deciding to slightly smaller ranges in the factorial :math:`\text{range}_T = 8 = (339 - 331)` K and :math:`\text{range}_S = 0.4 = (2.17 - 1.77)` g/L so that we can move more slowly along the surface.

.. figure:: ../figures/doe/RSM-base-case-combined.png
	:align: center
	:scale: 100
	:alt:	RSM-base-case.py

A least squares model from the 4 factorial points (experiments 8, 9, 10, 11, run in random order), seems to show that the promising direction now is to increase temperature but decrease the substrate concentration.

.. math::
		\hat{y} &= b_0 + b_T x_T + b_S x_S + b_{TS} x_T x_S \\
		\hat{y} &= 673.8 + 13.25 x_T - 39.25 x_S - 2.25 x_T x_S

As before we take a step in the direction of steepest ascent of :math:`b_T` units along the :math:`x_T` direction and :math:`b_S` units along the :math:`x_S` direction. Again we choose :math:`\Delta x_T = 1` unit, though we must emphasize that we could used a smaller or larger amount, if desired.

.. math::

	\frac{\Delta x_S}{\Delta x_T} &= \frac{-39}{13} \\
	\Delta x_S &= \frac{-39}{13} \times 1\\
	\Delta x_{S, \text{actual}} &= \frac{-39}{13} \times 1 \times 0.4 /2 = -0.6\,\text{g/L}\\
	\Delta x_{T, \text{actual}} &= 4\,\text{K}\\

*	:math:`T_{12} = T_6 + \Delta x_{T, \text{actual}}` = 335 + 4 = 339K
*	:math:`S_{12} = S_6 + \Delta x_{S, \text{actual}}` = 1.97 - 0.6 = 1.37 g/L

We determine that at run 12 the profit is :math:`y_{12}` = $ 716. But our previous factorial had a profit value of $725 on one of the corners. Now it could be that we have a noisy system; after all, the difference between $716 and $725 is not too much, but there is a relatively large difference in profit between the other points in the factorial.

One must realize that as one approaches an optimum we will find:

	-	The response variable will start to plateau, since, recall that the first derivative is zero at an optimum, implying the surface flattens out, and all points, in all directions away from the optimum are worse off.

	-	The response variable remains roughly constant for two consecutive jumps, because one has jumped over the optimum.

	-	The response variable decreases, sometimes very rapidly, because we have overshot the optimum.

	-	The presence of curvature can also be inferred when interaction terms are similar or larger in magnitude than the main effect terms.

An optimum therefore exhibits curvature, so a model that only has linear terms in it will not be suitable to use to find the direction of steepest ascent along the *true response surface*. We must add terms that account for this curvature.

**Checking for curvature**

The factorial's center point can be predicted from :math:`(x_T, x_S) = (0, 0)`, and is just the intercept term. In the last factorial, the predicted center point was  :math:`\hat{y}_\text{cp}` = $670; yet the actual center point from run 6 showed a profit of $ 688. This is a difference of $18, which is substantial when compared to the main effects' coefficients, particularly of temperature.

So when the measured center point value is quite different from the predicted center point in the linear model, then that is a good indication there is :index:`curvature <pair: curvature; response surface>` in the response surface. The way to accommodate for that is to add quadratic terms to the estimate model.

**Adding higher-order terms using central composite designs**

.. _DOE_central_composite_designs:

We will not go into too much detail about :index:`central composite designs`, other than to show what they look like for the case of 2 and 3 variables. These designs take an existing orthogonal factorial and augment it with axial points. This is great, because we can start off with an ordinary factorial and always come back later to add the terms to account for nonlinearity.

The :index:`axial points <pair: axial points; experiments>` are placed :math:`4^{0.25} = 1.4` coded units away from the center for a 2 factor system, and :math:`8^{0.25} = 1.7` units away for a :math:`k=3` factor system. Rules for higher numbers of factors, and the reasoning behind the 1.4 and 1.7 unit step size can be found, for example in the textbook by Box, Hunter and Hunter.

.. image:: ../figures/doe/central-composite-design.png
	:align: left
	:scale: 50
	:alt:	central-composite-design.svg
	:width: 900px

So a central composite design layout was added to the factorial in the above example and the experiments run, randomly, at the 4 axial points.

The four response values were :math:`y_{13} = 720`, :math:`y_{14} = 699`, :math:`y_{15} = 610`, and :math:`y_{16} = 663`. This allows us to estimate a model with quadratic terms in it: :math:`y = b_0 + b_T x_T + b_S x_S + b_{TS} x_T x_S + b_{TT} x_T^2 + b_{SS} x_S^2`. The parameters in this model are found in the usual way, using a least-squares model:

	.. math::
		\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}\\
		\begin{bmatrix} y_8\\ y_9\\ y_{10} \\ y_{11} \\ y_{6} \\ y_{13} \\ y_{14} \\ y_{15} \\ y_{16} \end{bmatrix} &=
		\begin{bmatrix} 1 & -1 & -1 & +1 & +1 & +1\\
						1 & +1 & -1 & -1 & +1 & +1\\
						1 & -1 & +1 & -1 & +1 & +1\\
						1 & +1 & +1 & +1 & +1 & +1\\
						1 &  0 &  0 &  0 &  0 &  0\\
						1 &  0 &-1.41&  0 &  0 &  2\\
						1 & 1.41&   0&  0 &  2 &  0\\
						1 & 0  & 1.41&  0 &  0 &  2\\
						1 &-1.41&   0&  0 &  2 &  0
		\end{bmatrix}
		\begin{bmatrix} b_0 \\ b_T \\ b_S \\ b_{TS} \\ b_{TT} \\ b_{SS} \end{bmatrix} + \mathbf{e}\\
		y &= 688 + 13x_T - 39x_S - 2.4 x_T x_S - 4.2 x_T^2 - 12.2 x_S^2

Notice how the linear terms estimated previously are the same! The quadratic effects are clearly significant when compared to the other effects, which was what prevented us from successfully using a linear model to project out to point 12 previously.

The final step in the response surface methodology is to plot this model's contour plot and predict where to run the next few experiments. As the solid contour lines in the illustration show, we should run our next experiments roughly at :math:`T` = 343K and :math:`S` = 1.60 g/L where the expected profit is around $736. We get those two values by eye-balling the solid contour lines, drawn from the above non-linear model. You could find this point analytically as well.

This is not exactly where the true process optimum is, but it is pretty close to it (the temperature of :math:`T` = 343K is just a little lower that where the true optimum is.

This example has demonstrated how powerful response surface methods are. A minimal number of experiments has quickly converged onto the true, unknown process optimum. We achieved this by building successive least squares models that approximate the underlying surface. Those least squares models are built using the tools of fractional and full factorials and basic optimization theory, to climb the hill of steepest ascent.

.. youtube:: https://www.youtube.com/watch?v=h80k3AusIcI&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=55

.. youtube:: https://www.youtube.com/watch?v=AcEPqVr4JJQ&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=56

.. youtube:: https://www.youtube.com/watch?v=s_sutHvaBZE&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=57


The general approach for response surface modelling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#.	Start at your baseline conditions and identify the main factors based on physics of the process, operator input, expert opinion input, and intuition. Also be aware of any constraints, especially for safe process operation. Perform factorial experiments (full or fractional factorials), completely randomized. Use the results from the experiment to estimate a linear model of the system:

	.. math::

		\hat{y} = b_0 + b_Ax_A + b_B x_B + b_C x_C  \ldots + b_{AB}x_Ax_B + b_{AC} x_A x_C + \ldots

#.	The main effects are usually significantly larger than the two-factor interactions, so these higher interaction terms can be safely ignored. Any main effects that are not significant may be dropped for future iterations.

#.	Use the model to estimate the path of steepest ascent (or descent if minimizing :math:`y`):

	.. math::

		\dfrac{\partial \hat{y}}{\partial x_1} = b_1  \qquad\qquad \dfrac{\partial \hat{y}}{\partial x_2} = b_2 \qquad \ldots

	The path of steepest ascent is climbed. Move any one of the main effects, e.g. :math:`b_A` by a certain amount, :math:`\Delta x_A`. Then move the other effects: :math:`\Delta x_i = \frac{b_i}{b_A} \Delta x_A`. For example, :math:`\Delta x_C` is moved by :math:`\frac{b_C}{b_A} \Delta x_A`.

	If any of the :math:`\Delta x_i` values are too large to safely implement, then take a smaller proportional step in all factors. Recall that these are coded units, so unscale them to obtain the move amount in real-world units.

#.	One can make several sequential steps until the response starts to level off, or if you become certain you have entered a different operating mode of the process.

#.	At this point you repeat the factorial experiment from step 1, making the last best response value your new baseline. This is also a good point to reintroduce factors that you may have omitted earlier. Also, if you have a binary factor; investigate the effect of alternating its sign at this point. These additional factorial experiments should also include center points.

#.	Repeat steps 1 through 5 until the linear model estimate starts to show evidence of curvature, or that the interaction terms start to dominate the main effects. This indicates that you are reaching an optimum.

	-	Curvature can be assessed by comparing the predicted center point, i.e. the model's intercept = :math:`b_0`, against the actual center point response(s). A large difference in the prediction, when compared to the model's effects, indicates the response surface is curved.

#.	If there is curvature, add axial points to expand the factorial into a central composite design. Now estimate a quadratic model of the form:

	.. math::

		y = b_0 + b_1x_1 + b_2 x_2	+ \ldots + b_{12}x_1x_2 + \ldots + b_{11}x_1^2 + b_{22}x_2^2 +  \ldots

#.	Draw contour plots of this estimated response surface (all data analysis software packages have contour plotting functions) and determine where to place your sequential experiments. You can also find the model's optimum analytically by taking derivatives of the model function.


.. sidebar:: What is the response variable when optimizing more than one outcome?

	.. youtube:: https://www.youtube.com/watch?v=LrCvoK7Ve0Q&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=58

	Response surface methods consider optimization of a single outcome, or response variable, called :math:`y`. In many instances we are interested in just a single response, but more often we are interested in the a multi-objective response, i.e. there are trade-offs. For example we can achieve a higher production rate, but it is at the expense of more energy.

	One way to balance all competing objectives is to rephrase the :math:`y` variable in terms of total costs, or better still, net profit. This makes calculating the :math:`y` value more complex, as we have to know the various costs and their relative weightings to calculate the profit. Now you have a single :math:`y` to work with.

	Another way is to superimpose the response surfaces of two or more :math:`y`-variables. This is tremendously helpful when discussing and evaluating alternate operating points, because plant managers and operators can then visually see the trade-offs.

.. TODO: figure here showing RSM trade-offs: two contours superimposed

.. rubric:: Summary

#.	In the previous sections we used factorials and fractional factorials for screening the important factors. When we move to process optimization,  we are assuming that we have already identified the important variables. In fact, we might find that variables that were previously important, appear unimportant as we approach the optimum. Conversely, variables that might have been dropped out earlier, become important at the optimum.

#.	Response surface methods generally work best when the variables we adjust are numerically continuous. Categorical variables (yes/no, catalyst A or B) are handled by fixing them at one or the other value, and then performing the optimization conditional on those selected values. It is always worth investigating the alternative values once the optimum has been reached.

#.	Many software packages provide tools that help with an RSM study. If you would like to use R in your work, we highly recommend the ``rsm`` package by Russel Lenth, available in R. You can read more about the package in `this article <https://cran.r-project.org/web/packages/rsm/vignettes/rsm.pdf>`_ as well as a `case-study <https://cran.r-project.org/web/packages/rsm/vignettes/rs-illus.pdf>`_.

.. _DOE-EVOP:

Evolutionary operation
===========================

Evolutionary operation (EVOP) is a tool to help maintain a full-scale process at its optimum. Since the process is not constant, the optimum will gradually move away from its current operating point. Chemical processes drift due to things such as heat-exchanger fouling, build-up inside reactors and tubing, catalyst deactivation, and other slowly varying disturbances in the system.

EVOP is an iterative hunt for the process optimum by making small perturbations to the system. Similar to response surface methods, once every iteration is completed, the process is moved towards the optimum. The model used to determine the move direction and levels of next operation are from full or fractional factorials, or designs that estimate curvature, like the central composite design.

Because every experimental run is a run that is expected to produce saleable product (we don't want off-specification product), the range over which each factor is varied must be small. Replicate runs are also made to separate the signal from noise, because the optimum region is usually flat.

Some examples of the success of EVOP and a review paper are in these readings:

- George Box: `Evolutionary Operation: A Method for Increasing Industrial Productivity <https://www.jstor.org/stable/2985505>`_", *Journal of the Royal Statistical Society* (Applied Statistics), **6**, 81 - 101, 1957.
- William G. Hunter and J. R. Kittrell, "`Evolutionary Operation: A Review <https://www.jstor.org/stable/1266686>`_", *Technometrics*, **8**, 389-397, 1966.

Current day examples of EVOP do not appear in the scientific literature much, because this methodology is now so well established.


..	Robust process operation
	============================

	* Process robustness lecture: http://ocw.mit.edu/OcwWeb/Mechanical-Engineering/2-830JSpring-2008/VideoLectures/index.htm
	* BHH(v2) has some discussion about this
