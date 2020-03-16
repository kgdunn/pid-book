.. _DOE-saturated-screening-designs:

Saturated designs for screening
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: you don't really described at all what a saturated design is

A :index:`saturated design <pair: saturated design; experiments>` can be likened to a well trained doctor asking you a few, but very specific, questions to identify a disease or problem. On the other hand, if you sit there just tell the doctor all your symptoms, you may or may not get an accurate diagnosis. Designed experiments, like visiting this doctor, shortens the time required to identify the major effects in a system, and to do so as accurately as possible, within limited budget.

Saturated designs are most suited for screening, and should always be run when you are investigating a new system with many factors. These designs are usually of resolution III and allow you to determine the main effects with a low number of experiments.

For example, a :math:`2^{7-4}_{\text{III}}` factorial, introduced in the section on :ref:`highly fractionated designs <DOE-highly-fractionated-designs>`, will screen 7 factors in 8 experiments. Once you have run the 8 experiments you can quickly tell which subset of the 7 factors are actually important, and spend the rest of your budget on clearly understanding these effects and their interactions. Bear in mind that there is a risk of confounding, as previously described in that section.

Let's see how by continuing the previous example, repeated again below with the corresponding values of :math:`y`. Recall it was a
:ref:`set of eight experiments in seven factorss <DOE-highly-fractionated-designs>`:

	.. tabularcolumns:: |c||c|c|c||c|c|c|c|c|

	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| Experiment| A          | B         |  C         |  D=AB      |  E=AC      |  F=BC      |  G=ABC     | :math:`y`  |
	+===========+============+===========+============+============+============+============+============+============+
	| 1         | |-|        | |-|       |  |-|       |  |+|       |  |+|       |  |+|       |  |-|       |  77.1      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| 2         | |+|        | |-|       |  |-|       |  |-|       |  |-|       |  |+|       |  |+|       |  68.9      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| 3         | |-|        | |+|       |  |-|       |  |-|       |  |+|       |  |-|       |  |+|       |  75.5      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| 4         | |+|        | |+|       |  |-|       |  |+|       |  |-|       |  |-|       |  |-|       |  72.5      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| 5         | |-|        | |-|       |  |+|       |  |+|       |  |-|       |  |-|       |  |+|       |  67.9      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| 6         | |+|        | |-|       |  |+|       |  |-|       |  |+|       |  |-|       |  |-|       |  68.5      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| 7         | |-|        | |+|       |  |+|       |  |-|       |  |-|       |  |+|       |  |-|       |  71.5      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
	| 8         | |+|        | |+|       |  |+|       |  |+|       |  |+|       |  |+|       |  |+|       |  63.7      |
	+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+


Use a least squares model to estimate the coefficients in the model:

.. math::
	\mathbf{y} &= \mathbf{Xb} \\
	\mathbf{b} &= \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}^T\mathbf{y}

where :math:`\mathbf{b} = [b_0, b_A, b_B, b_C, b_D, b_E, b_F, b_G]`. The matrix :math:`\mathbf{X}` is essentiall a copy of the above table, but with an added column of 1's for the intercept term. Notice that the :math:`\mathbf{X}^T\mathbf{X}` matrix will be diagonal. Make sure you can calculate :math:`\mathbf{X}^T\mathbf{X}` by hand, at least once. It is also straightforward to calculate the solution vector (by hand!), which you can confirm to be :math:`\mathbf{b} = [70.7, -2.3, 0.1, -2.8, -0.4, 0.5, -0.4, -1.7]`.

How do you assess which main effects are important?  There are eight data points and eight parameters, so there are no degrees of freedom and the residuals are all zero. In this case you have to use a :ref:`Pareto plot <DOE-Pareto-plot>`, which requires that your variables have been suitably scaled in order to judge importance of the main effects relative to each other. The Pareto plot would be given as shown below, and as usual, it does not show the intercept term.

.. dcl:: R
	:height: 700px

	# Create vectors for each factor in the experiment
	A = B = C = c(-1, +1)
	design = expand.grid(A=A, B=B, C=C)
	A = design$A
	B = design$B
	C = design$C
	D = A*B
	E = A*C
	F = B*C
	G = A*B*C
	y = c(77.1, 68.9, 75.5, 72.5, 67.9, 68.5, 71.5, 63.7)

	demo = lm(y ~ A + B + C + D + E + F + G)
	summary(demo)

	# OK, now we are ready to generate the Pareto plot.
	# Let's use a library to do that for us.

	# library(pid) <-- best to use this!
	# It is better to uncomment and use the line above.

	# But this embedded R script on this website does not have the
	# "pid" library available. So we will load the required function
	# from an external server instead:
	source('https://yint.org/paretoPlot.R')

	# And now we can generate the plot:
	paretoPlot(demo)

	# Try getting the results manually:
	X_matrix = model.matrix(demo)
	XtX <- t(X_matrix) %*% X_matrix
	print('The XtX matrix is:')
	print(XtX)

	Xty <- t(X_matrix) %*% y
	b = solve(XtX) %*% Xty
	print('The solution vector is:')
	print(b)


.. image:: ../../figures/doe/pareto-plot-pid.png
	:align: right
	:scale: 37
	:width: 900px
	:alt:	../../figures/doe/pareto-plot.R


Significant effects would be **A**, **C** and **G**. The next largest effect, **E**, though fairly small, could be due to the main effect **E** or due to the **AC** interaction, because recall the confounding pattern, up to the 2 factor-interactions, for main effect was :math:`\widehat{\beta}_{\mathbf{E}} \rightarrow` **E + AC + BG + DF**.

The factor **B** is definitely not important to the response variable in this system and can be excluded in future experiments, as could **F** and **D** likely. Future experiments should focus on the **A**, **C** and **G** factors and their interactions. We show how to use these existing 8 experiments in the above table, but add a few new ones in the next section on design foldover and by understanding projectivity.

A side note on screening designs is a mention of :index:`Plackett and Burman designs <pair: Plackett-Burman designs; experiments>`. These designs can sometimes be of greater use than a highly fractionated design. A fractional factorial must have :math:`2^{k-p}` runs, for integers :math:`k` and :math:`p`: i.e. either :math:`4, 8, 16, 32, 64, 128, \ldots` runs. Plackett-Burman designs are screening designs that can be run in any multiple of 4 greater or equal to 12:, i.e. :math:`12, 16, 20, 24, \ldots` runs. The Box, Hunter, and Hunter book has more information in Chapter 7, but another interesting paper on these topic is by Box and Bisgaard: "What can you find out from 12 experimental runs?", which shows how to screen for 11 factors in 12 experiments.

.. youtube:: https://www.youtube.com/watch?v=zrZS-zovKSc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=49

.. youtube:: https://www.youtube.com/watch?v=dbxijjAHeUU&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=50

An important mention to readers interested in other, arguable better screening strategies, is to consider `definitive screening designs <https://www.google.com/search?q=definitive+screening+designs>`_.
