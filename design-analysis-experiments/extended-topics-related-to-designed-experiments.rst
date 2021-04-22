Extended topics related to designed experiments
==========================================================================

.. p 414 Esbensen
.. Objectives of Trygg p 2 and p5 of wikipedia article

This section is just an overview  of some interesting topics, together with references to guide you to more information.

Experiments with mistakes, missing values, or belatedly discovered constraints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. BHH1: p 503

.. youtube:: https://www.youtube.com/watch?v=AcEPqVr4JJQ&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=57

Many real experiments do not go smoothly. Once the experimenter has established their :math:`-1` and :math:`+1` levels for each variable, they back that out to real units. For example, if temperature was scaled as :math:`T = \dfrac{T_\text{actual} - 450\text{K}}{\text{25K}}`, then :math:`T = -1` corresponds to 425K and :math:`T= +1` corresponds to 475K.

But if the operator mistakenly sets the temperature to :math:`T_\text{actual} = 465K`, then it doesn't quite reach the +1 level required. This is not a wasted experiment. Simply code this as :math:`T = \dfrac{465 - 450}{25} = 0.6`, and enter that value in the least squares model for matrix :math:`\mathbf{X}`. Then proceed to calculate the model parameters using the standard least squares equations. Note that the columns in the X-matrix will not be orthogonal anymore, so :math:`\mathbf{X}^T\mathbf{X}` will not be a diagonal matrix, but it will be almost diagonal.

Similarly, it might be discovered that temperature cannot be set to 475K when the other factor, for example concentration, is also at its high level. This might be due to physical or safety constraints. On the other hand, :math:`T=475K` can be used when concentration is at its low level. This case is the same as described above: set the temperature to the closest possible value for that experiment, and then analyze the data using a least squares model. The case when the constraint is known ahead of time is :ref:`dealt with later on <DOE-handling-constraints>`, but in this case, the constraint was discovered just as the run was to be performed.

Also see the section on :ref:`optimal designs <DOE-optimial-designs>` for how one can add one or more additional experiments to fix an existing bad set of experiments.

The other case that happens occasionally is that samples are lost, or the final response value is missing for some reason. Not everything is lost: recall the main effects for a full :math:`2^k` factorial are estimated :math:`k` times at :ref:`each combination of the factors <DOE-COST-vs-factorial-efficiency>`.

If one or more experiments have missing :math:`y` values, you can still estimate these main effects, and sometimes the interaction parameters by hand. Furthermore, analyzing the data in a least squares model will be an undetermined system: more unknowns than equations. You could choose to drop out higher-order interaction terms to reduce the equations to a square system: as many unknowns as equations. Then proceed to analyze the results from the least squares model as usual. There are actually slightly more sophisticated ways of dealing with this problem, as described by Norman Draper in "`Missing Values in Response Surface Designs <https://www.jstor.org/stable/1266729>`_", *Technometrics*, **3**, 389-398, 1961.

The above discussion illustrates clearly our preference for using the least squares model: whether the experimental design was executed accurately or not: the least squares model always works, whereas the :ref:`short cut tools <DOE-two-level-factorials>` developed for perfectly executed experiments will fail.


.. _DOE-handling-constraints:

Handling of constraints
~~~~~~~~~~~~~~~~~~~~~~~~~

Most engineering systems have limits of performance, either by design or from a safety standpoint. It is also common that optimum production levels are found close to these constraints. The factorials we use in our experiments must, by necessity, span a wide range of operation so that we see systematic change in our response variables, and not merely measure noise. These large ranges that we choose for the factors often hit up again constraints.

A simple bioreactor example for 2 factors is shown: at high temperatures and high substrate concentrations we risk activating a different, undesirable side-reaction. The shaded region represents the constraint where we may not operate. We could for example replace the :math:`(T_{+}, C_{+})` experiment with two others, and then analyze these 5 runs using least squares.

.. image:: ../figures/doe/two-factors-with-constraint.png
	:align: right
	:scale: 40
	:alt:	../figures/doe/two-factors-with-constraint.svg
	:width: 900px

Unfortunately, these 5 runs do not form an orthogonal (independent) :math:`\mathbf{X}` matrix anymore. We have lost orthogonality. We have also reduced the space (or volume when we have 3 or more factors) spanned by the factorial design.

It is easy to find experiments that obey the constraints for 2-factor cases: run them on the corner points. But for 3 or more factors the constraints form planes that cut through a cube. We then use :ref:`optimal designs <DOE-optimial-designs>` to determine where to place our experiments. A D-optimal design works well for constraint-handling because it finds the experimental points that would minimize the loss of orthogonality (i.e. they try to achieve the most orthogonal design possible). A compact way of stating this is to maximize the determinant of :math:`\mathbf{X}^T\mathbf{X}`, which is why it is called D-optimal (it maximizes the determinant).

These designs are generated by a computer, using iterative algorithms. See the D-optimal reference in the :ref:`section on optimal designs <DOE-optimial-designs>` for more information.

.. _DOE-optimial-designs:

Optimal designs
~~~~~~~~~~~~~~~~~~~~~~~~~

If you delve into the modern literature on experimental methods you will rapidly come across the concept of an *optimal* design. This begs the question, what is sub-optimal about the factorial designs we have focussed on so far?

A full factorial design spans the maximal space possible for the :math:`k` factors. From least squares modelling we know that large deviations from the model center reduces the variance of the parameter estimates. Furthermore, a factorial ensures the factors are moved independently, allowing us to estimate their effects independently as well. These are all "optimal" aspects of a factorial.

So again, what is sub-optimal about a factorial design?  A factorial design is an excellent design in most cases. But if there are constraints that must be obeyed, or if the experimenter has an established list of possible experimental points to run, but must choose a subset from the list, then an "optimal" design is useful.

All an optimal design does is select the experimental points by optimizing some criterion, subject to constraints. Some examples:

 	- The design region is a cube with a diagonal slice cut-off on two corner due to constraints. What is the design that spans the maximum volume of the remaining cube?

	- The experimenter wishes to estimate a non-standard model, e.g. :math:`y = b_0 + b_\mathrm{A}x_\mathrm{A} + b_\mathrm{AB}x_\mathrm{AB} + b_\mathrm{B}x_\mathrm{B} + b_\mathrm{AB}\exp^{-\tfrac{dx_\mathrm{A}+e}{fx_\mathrm{B}+g}}` for fixed values of :math:`d, e, f` and :math:`g`.

	-	For a central composite design, or even a factorial design with constraints, find a smaller number of experiments than required for the full design, e.g. say 14 experiments (a number that is not a power of 2).

	-	The user might want to investigate more than 2 levels in each factor.

	-	The experimenter has already run :math:`n` experiments, but wants to add one or more additional experiments to improve the parameter estimates, i.e. decrease the variance of the parameters. In the case of a D-optimal design, this would find which additional experiment(s) would most increase the determinant of the :math:`\mathbf{X}^T\mathbf{X}` matrix.

The general approach with optimal designs is

	#.	The user specifies the model (i.e. the parameters).

	#.	The computer finds all possible combinations of factor levels that satisfy the constraints, including center-points. These are now called the *candidate points* or :index:`candidate set <pair: candidate set; optimal designs>`, represented as a long list of all possible experiments. The user can add extra experiments they would like to run to this list.

	#.	The user specifies a small number of experiments they would actually like to run.

	#.	The computer algorithm finds this required number of runs by picking entries from the list so that those few runs optimize the chosen criterion.

The most common optimality criteria are:

	-	A-optimal designs minimize the average variance of the parameters, i.e. minimizes :math:`\text{trace}\left\{(\mathbf{X}^T\mathbf{X})^{-1}\right\}`

	-	D-optimal designs minimize the general variance of the parameters, i.e. maximize :math:`\text{det}\left(\mathbf{X}^T\mathbf{X}\right)`

	-	G-optimal designs minimize the maximum variance of the predictions

	-	V-optimal designs minimize the average variance of the predictions

It must be pointed out that a full factorial design, :math:`2^k` is already A-, D- G- and V-optimal. Also notice that for optimal designs the user must specify the model required. This is actually no different to factorial and central composite designs, where the model is implicit in the design.

The algorithms used to find the subset of experiments to run are called candidate exchange algorithms. They are usually just a brute force evaluation of the objective function by trying all possible combinations. They bring a new trial combination into the set, calculate the objective value for the criterion, and then iterate until the final candidate set provides the best objective function value.

**Readings**

* St. John and Draper: "`D-Optimality for Regression Designs: A Review <https://www.jstor.org/stable/1267995>`_", *Technometrics*, **17**, 15-, 1975.

.. _DOE-definitive-screening-designs:

Definitive screening designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final type of design to be aware of is a class of designs called the :index:`definitive screening design <pair: definitive screening design; experiments>`, and below is a link that you can read up some more information.

These designs are a type of :ref:`optimal design <DOE-optimial-designs>`. Optimal designs can be very flexible. For example, if you had a limited budget you can create an optimal design for a given number of factors you are investigating to maximize one of these optimality criteria to fit your budget. A computer algorithm is used to find the settings for each one of the budgeted number of runs, so that the optimization criterion is maximized. In other words the computer is designing the experiments for you, so they have some very distinct advantages.

The readings below give more details, and a practical implementation of these designs using the R software package.

**Readings**

* John Lawson "`DefScreen: Definitive Screening Designs, in package "daewr": Design and Analysis of Experiments with R <https://rdrr.io/cran/daewr/man/DefScreen.html>`_".
* Bradley Jones: "`Class of Three-Level Designs for Definitive Screening in the Presence of Second-Order Effects <https://yint.org/dsdesign>`_", Journal of Quality Technology, 2011.


.. _DOE-mixture-designs:

Mixture designs
~~~~~~~~~~~~~~~~~~~~~~~~~

The area of mixture designs is incredibly important for optimizing recipes, particularly in the area of fine chemicals, pharmaceuticals, food manufacturing, and polymer processing. Like factorial designs, there are screening and optimization designs for mixtures also.

A mixture design is required when the factors being varied add up to 100% to form a mixture. Then these factors cannot be adjusted in an independent, factorial-like manner, since their proportion in the recipe must add to 100%: :math:`\sum_i x_i = 1`. These designs result in triangular patterns (called simplexes). The experimental points at the 3 vertices are for pure components :math:`x_A, x_B`, or :math:`x_C`. Points along the sides represent a 2-component mixture, and points in the interior represent a 3-component blend.

.. image:: ../figures/doe/mixture-design.png
	:align: center
	:scale: 60
	:width: 900px
	:alt:	../figures/doe/mixture-design.svg

In the above figure on the right, the shaded region represents a constraint that cannot be operated in. A D-optimal algorithm must then be used to select experiments in the remaining region. The example is for finding the lowest cost mixture for a fruit punch, while still meeting certain taste requirements (e.g. watermelon juice is cheap, but has little taste). The constraint represents a region where the acidity is too high.

.. Clean this up and make it clearer

	You may not always need a mixture design for recipe experiments if you are only changing a small amount of ingredient, and your factors include only a subset of the ingredients. For example, you are investigating the properties of a new polymer blend, made with ingredients:

		-	**A**: 25% or 30%
		-	**B**: 1% or 2%
		-	**C** and **D** make up the rest of the recipe in a consistent 40/60 ratio
		-	**T**: is the temperature at which the blend is extruded, either high or low

	In this case **A** and **B** are the factors being investigated in the recipe, in addition to temperature **T**. The results from a full factorial in factors **A**, **B** and **T** (i.e. a :math:`2^3` factorial) would give similar results to a mixture design at high temperature and low temperature, but
