.. TODO
	=====
	~~~~~
	^^^^^
	-----
	
	Comment on binary factors:
	
		*	can be add/don't add variables
		*	catalyst 1 vs 2
		*	add eggs before milk, or milk before eggs
		*	use the middle oven rack, lower over rack
		*	reactor 1 vs reactor 2
		*	operator 1 vs operator 2
	
	Add the newish Box RSM book to the reference list.
	
	Add reference to the RSM overview article: Myers et al., "Response Surface Methodology: A Retrospective and Literature Survey", Journal of Quality Technology, 36(1), 2004, 53-77.
	
	RSM: fit models, until there is evidence the model is not valid anymore. Evidence: predictions from model don't match what you actually get from the experiment (within experimental/measurements error: found from repeats).
	
	RSM: emphasize the expts should not be done so far outside range. typically use +/- 2 units, whereas +/- 3 units should be quite an extrapolation.
	     Show the extrapolation cartoon from xkcd.com
	RSM: emphasize that if 2fi are significant relative to main effects then you cannot climb steepest path of ascent by taking partial (linear) derivatives. Use a contour plot to show surface and estimate next point based on contour plot.
	RSM: as every new point becomes available: update the model (not necessarily the number of terms in the model), but refit the model parameters and
	     see how much they change by. This also gives you extra degrees of freedom.
	RSM: explain what the partial derivatives are doing: fitting a tangent plane to the nonlinear surface: if there are non-linearities then you cannot
	     use this tangent plane method anymore. Use contour plots from MATLAB or software to visualize the surface and place next point manually.
	RSM: emphasize that CCD can be implemented one axial point at a time and boot strap model. You may not have to complete all CCD axial points to get a reasonable model.
	
	RSM: what happens if you omit the interaction: e.g. y = 61.9 - 1.225 xA + 1.025 xB + 1.38 xA xB.
	     if you optimize A and B, ignoring the AB interaction?  Serious misinterpretation of direction?
	
	RSM: if you have a saddle (in a 2 or 3-factor system): good strategy is to augment the factorial with 2 more experiments to one side of the factorial (left, right, top, bottom, front, back, etc). Fit quadratic model in that direction and draw surface plot. Get a better idea of where to go next. See "Ashley Sebastian, Mondise Sithole, Udit Gupta" take-home exam, Q4.

	
	RSM: why it's better than just a random scatter of points: you learn about the shape of the response surface and the impact of the main factors on the surface. Once you've found an optimum you can be certain that it's the best in the neighbourhood where you are.
	RSM: may not have to always complete a fractional factorial to a full factorial if there is aliasing. E.g. A, B, C=AB. Let all terms be significant. Unsure if C and/or AB is important. So to remove confounding: let's say we see the coefficient for the aliased AB=C maximizes y when C is run at the + level. So run only the next 2 of the remaining 4 experiments: those 2 at the + level of C. Now you have 6 runs, so you can estimate A, B, C, AB and either AC or BC. The ABC cannot be estimated. E.g. Ryan McBride and Stuart Young's DOE RSM Q4 in 2011.
	RSM: systematic methodology: motivated by the fact that you will learn something about your system (important main effects, interactions) *and* optimize the process simultaneously. Whereas a process that is nonlinear and "optimized" by trial and error: leads to nothing learned and always a suboptimal operating point.
	
	
	Choice of range of factors:
		- not too wide so you straddle optimum and get erroneous interpretation of effect (you see negative or +ve slope, but really it is quadratic)
		- not too narrow so that you get no effect showing: you are within the range of the noise of y
		- slightly greater than common cause operation's variation: to see an effect
		- 15 to 25% of the full range of possible operation, taking constraints between factors into account
		- binary factors: if too different, it can invoke totally different operating mechanism from one factor to another, implying you are really study two different systems altogether, and a unified model from a single experiment not appropriate. However this will often show in a factorial as the binary factor having the strongest effect. Analyze the experiments of each binary setting separately.
		
	Must include:
		- Cannot rank factors C > B > AB > etc based on the absolute coefficient size... It's dependent on the levels chosen
		- e.g cannot say factor A has greater effect than factor B, unless factors cover the full range of typical/usual operation
		- i.e. ranking factors is dependent on the ranges chosen for those factors
		
	Disturbances and randomimization:
		- e.g. testing fitness improvement: during experiment you are getting naturally fitter
		- e.g. testing laptop battery performance. But use of battery over and over is going to gradually make it worse (e.g. car tests: wear and tear increase over duration of test). Slowly varying distrbances accounted for by randomization so they show up as noise. Worse thing to do is run the experiments in Yates order: that will confound this disturbance with the last, slowest-varying factor in table.
	
	On Yates (factorial) analysis: http://www.itl.nist.gov/div898/handbook/eda/section3/eda35i.htm
	
	DOE RSM with colour:
	
	
	>>> import numpy as N
	>>> import pylab as pl
	>>> def z_func(x,y):
	((return (1-x+x**3+y**5)*N.exp(-(x**2+y**2 ...
	...
	>>> x = N.arange(-3.0,3.0,0.025)
	>>> y = N.arange(-3.0,3.0,0.025)
	>>> X,Y = pl.meshgrid(x, y)
	>>> Z = z_func(X, Y)
	>>> im = pl.imshow(Z,interpolation='bilinear',/
	(cmap=pl.cm.Spectral ...
	>>> cset = pl.contour(Z,N.arange(-1.2,1.6,0.2),/
	(linewidths=2,cmap=pl.cm.hot ...
	>>> pl.clabel(cset,inline=True,fmt=’%1.1f’,/
	(fontsize=10 ...
	>>> pl.colorbar(im)
	>>> pl.axis(’off’)
	>>> pl.title(’$z=(1-x+xˆ3+yˆ5) eˆ-(xˆ2+yˆ2)$’	
	
	TODO: discuss use of an external data set for S_E
	
	ADD: If you keep the 2 factor interactions you must keep the main effects also. See Fox textbook for why.
	
		Email to Dr. Hrymak on 27 March 2011 about this topic
	
		This Minitab write-up should help the student: http://www.minitab.com/en-US/support/answers/answer.aspx?log=0&id=559&langType=1033

		That write-up, and text books on general linear models always suggest to keep the main effect in the model when estimating the interaction. They never explain why though. I've still not found a satisfactory explanation for myself.

		Take this example: y_actual = 10 + 2xA - 1xB + 12 xA xB and construct a full factorial at the usual -1 and +1 levels for xA and xB.

		A least squares model with 4 points and 4 parameters (b0, bA, bB, bAB) recovers that model exactly. A least squares model with only two columns in X (one for the intercept and one for the interaction) gets similar estimates for b0=10.5 and bAB=11.5, and has 2 degrees of freedom. We haven't lost anything, nor has the prediction ability of the model deteriorated by any amount. Let xA = +1 and xB = -1:
		* y_hat  = 10.5 + (11.5)(+1)(-1) = -1
		* y_actual = 10 + (2)(+1) - 1(-1) + (12)(+1)(-1) = +1

		Things change a bit when y_actual = 10 + 4xA - 2xB + 23 xA xB. When you estimate and use a model without main effects you can get good estimates of the model parameters (y = 10 + 23 xA xB), but poor estimates when you use the model on new data: let xA = +1 and xB = -1:
		* y_hat  = 10 + (23)(+1)(-1) = -13
		* y_actual = 10 + (4)(+1) - 2(-1) + (23)(+1)(-1) = -7

		So at what point is it worth including main effects or leaving them out while retaining their interactions? This is the only reason I can think of for retaining main effects and their interactions. We never really know the true model, and if we use the model without main effects at corner points that conflict with the interactions, we can get poor predictions. After all, that's why we are building these models: to optimize and improve the process later on.
	
	DOE is a way to bring an out of control process back into control. See the comment by Vining (top right, p152) in the  Bisgaard articles http://dx.doi.org/10.1080/08982110701826721
	
	Investigate the .. sectnum:: directive in ReST
	
..	DOE implementation

	* Cocktail algorithm to create D-optimal design: http://arxiv.org/abs/0911.0108 
		
.. FUTURE

	I've noticed with the questions students are asking that they haven't understood what blocking is for, and how to generate expt with it.
	Maybe include several examples in the text to justify why blocking is required and the thought process behind it.
	Blocking: 4 batches in a 8 run experiment: use the example of /Users/kevindunn/Statistics course/Administrative/2010-handin/DOE project/Howard and Booker - 4C3 mini project.doc
	DONE: Remove using a normal probability plot for significance of effects. I don't recall why I wanted to do this though: confusing interpretation, or perhaps q-q plots can misleading values?
	
	Add some notes about factors that are uncontrollable, but still interesting: e.g. outside air humidity;  add it to your :math:`\mathbf{X}` matrix and even though not orthogonal, can still be understood in the model.
	
	Look at the book (PDF format) of Brereton_-_Chemometrics_-_Data_analysis_for_the_laboratory_and_chemical_plant.pdf. It has a whole section on designs. Particularly the section on response surfaces and CCDs.
	
	Add that you cannot remove main effects if their interactions are used in the model. See Fox book on this point also.
	
	Remove the use of the q-q plot to assess significance: misleading. See how Minitab draws its line of significance. 
	Rather use standardized error (effect / SE), if there are degrees of freedom available.

	RSM: show how you decide when to switch to CCD designs.
	RSM: show how to handle binary factors
	RSM: show how to re-use points over and over (e.g. see Richard, Daniel, Jordan, take-home final)
	RSM: use center points for an extra DOF
	RSM: coded plots: make it clear that they need to unconvert back to real-world units when showing them
	RSM: use an example with a negative slope: to show that gamma is always positive (negative/negative)
	RSM: emphasize how do you know you have approaching or reaching an optimum: center effects, two-factor interactions (not always!); start to make smaller steps to avoid overshooting
	
.. Plots to draw

	Low priority:
	Show figure on page 494 of BHH(v1) here
	
	Illustration of normal distribution division into equal areas
	
	DONE: Scan in page 272 of BHH2, p 410 BHH1 to show in class, or draw part of it
	
	.. TODO FUTURE: RSM overview figure here with COST approach superimposed
	
	A RSM contour for 2 y-variables: cost and yield, all p 579 in the RSM overview paper of Hill and Hunter
		.. TODO: figure here showing RSM trade-offs: two contours superimposed
	Use lighter lighting on surface plots: add an arrow to show the direction of steepest ascent?
	
	
	Main effects plot ( p 5.16)
	Interaction effects plot (G p 5.17)
	Cube plot
	
	Constraints on a cube system
	
	TODO FUTURE:
	* Foldover: add 2 examples for each case
	* Projectivity: see the notes added in that section. 
	* Projectivity: use a better example than the 2^{6-2}_{IV} example: 3 factors remaining, vs 3 in is confusing.
	* RSM: if it is a 2-factor factorial and the 2fi is high, then use a plot of the surface to decide on the next point, rather than just a plan \gamma step.
	
	
.. Outline of third class

	* Full factorial experiments
	* Drop out terms that are not significant; extra DOF to estimate error
	* Known, but uncontrollable disturbance: blocking parameter: confound on the highest interaction possible

		-	2^3 example: we do least damage when confound with ABC interaction
	
	* Next step: reduce the number of experiments. Question: which runs do we drop up so we cause least damage to the experiment?

		- half fractions
	
			- introduce a new terminology to deal with them: generators and defining relationship
			- why? so we can determine aliasing (confounding pattern)
			- why? we can see what we are loosing by running these half fractions
		
			- running the other half fraction.
		
			Side-issue:
		
				* using generators to deal with blocking; B_1 = ABC for a 3-factor experiment:
				* find the other half fraction: B_1 = -ABC
			
		- fractionated experiments
	
			-	use generators and def.rel. system to determine aliasing
			-	why? decide which factors to assign to A, B, C, etc
			-	worked example: complete
			-	projectivity
	
		- Special case: saturated experiments (III)
	
	* RSM

		- surfaces are smooth (p438 BHH2)
		- models are approximations (p440 BHH2)
		- direction of ascent:
		
			- show a single curve: optimum by moving \gamma steps along x_1 (\gamma is our step size)
			- two variables: by example
			
		- as we approach optimum: we have to use higher order factorials to estimate 2nd order effects and curvature
		
		- models that take second order effects into account: 3^k, CCD
		
			- CCD: why and when: second order effects (b_AA, b_BB, b_CC terms)
			- add axial points (\pm \alpha, 0, 0), etc
			- use L/S to fit model
			
		- show algorithm
		
		- constraints? p 447 BHH2
		
	* EVOP
	
		- outline of it
		
	* Guidance
	
		- Umetrics book and Esbensen book: Start with screening design (resolution III) for a new system, or if you are unfamiliar with it
		- Foldover idea to sequentially investigate and expand your design
		- Half-fractions used when you don't have time to run full set of experiments (projectivity)
	
.. TODO:

	Chap 17 of Box, Hunter and Hunter once you've done the DOE notes. Add that info into the notes.
	Outline of tools
	Nomenclature side bar

.. Improvements in the future

	Introduce the terms: run, factor, levels, response, effect
	Start with one factor at two levels, and calculate the effect: showing that it is just the least squares line through 2 points
	Show how to estimate the Least squares model with just these two points in matrix form: 2 unknowns & 2 equations
	Show that X = [1 & x_1 \\ 1 & x_2], X^TX = [.....], and inv(X^TX) = [.....], and X^Ty = [....], show that b_0 = .... and b_1 = ....
	
	Then go to 2 factors and repeat it
	When it comes to blocking: use a 2^2 system (factors are A and B), with 2 blocks (block variable is -1 and +1), show that it is as if a new variables is added, C = AB
	Write out X-matrix corresponding to b-vector = [b_0, b_A, b_B, b_AB, b_C]. The last two columns are the same: loss of independence, cannot invert, so you have to group those columns
	New coefficient estimates is (b_AB + b_C) instead
	
	Then run an example where there is a bias added to the block: +g for block 1 and +h for block 2. See how main effects are OK, but the 2-factor interaction, AB, is confounded = AB + 2g - 2h
	
	
.. Outline

	Wold's 3 phases:
	1. Screening	
	2. Optimization
	3. Robustness
	
	
.. index::
   see: Design of experiments; experiments

Design and Analysis of Experiments: in context
===============================================

This section is a totally different approach to learning and understanding about (chemical engineering) systems than what you have seen in other courses. Firstly, we use an empirical (non-theoretical) model to describe the system. Secondly, we learn what is the best way to intentionally manipulate/perturb the system to learn more about it.

We will use the tools of :ref:`least squares modelling <SECTION-least-squares-modelling>`, :ref:`visualization <SECTION-data-visualization>` and :ref:`univariate statistics <SECTION-univariate-review>` that we learned about earlier. We use these tools to analyze and interpret the data from our experiments.

In the next section, on latent variables, we will take a look at learning more about our systems when the condition of independence between variables, required for designed experiments, is not met. But for now we can use least squares and simpler tools, as designed experiments are intentionally orthogonal (independent).

Usage examples
==============

.. index::
	pair: usage examples; experiments

The material in this section is used whenever you need to perturb and learn more about a system.

	- *Colleague*: We have this list of 8 plausible factors that affect the polymer melt index. How do we narrow down the list to a more manageable size and rank their effect on melt index?
 	- *You*: Our initial screening experiments reduced the list down to 3 factors of interest. Now how do we run the rest of the experiments?
 	- *Manager*: Two years ago someone collected these experimental data for the effectiveness of a new catalyst. What can you make of this data, and where should we operate the reactor to get optimal yields?
	- *Colleague*: The current operating conditions give us good yield, but they are quite unstable. Small changes in the feed flowrate can quickly lead to an unsafe spike in the temperature and pressure. How can we locate other operating conditions that give similar yield values, but are less sensitive to feedrate variability.
	- *Colleague*: We would like to run experiments by varying temperature and pressure, but operating at both high temperature and pressure is unsafe. How do we plan such an experiment?

.. TODO: more questions/answers here

What you will be able to do after this section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ../figures/mindmaps/DOE-section-mapping.png
	:width: 750px 
	:align: center
	:scale: 90

References and readings
========================

.. index::
	pair: references and readings; experiments

-	**Strongly recommended**: Box, Hunter and Hunter, *Statistics for Experimenters*, chapters 5 and 6 with topics from chapters 11, 12, 13 and 15.
-	`A web tutorial on designed experiments <http://www.chemometrics.se/index.php?option=com_content&task=view&id=18&Itemid=27>`_
-	Søren Bisgaard: `Must a Process Be in Statistical Control Before Conducting Designed Experiments <http://dx.doi.org/10.1080/08982110701826721>`_, with discussion (`part 1 <http://dx.doi.org/10.1080/08982110701866198>`_, `part 2 <http://dx.doi.org/10.1080/08982110801894892>`_, `part 3 <http://dx.doi.org/10.1080/08982110801890148>`_, `part 4 <http://dx.doi.org/10.1080/08982110801924509>`_, `part 5 <http://dx.doi.org/10.1080/08982110801894900>`_ and a `rejoinder <http://dx.doi.org/10.1080/08982110801973118>`_), 
-	George Box and  J. Stuart Hunter: "The :math:`2^{k-p}` `Fractional Factorial Designs - Part I <http://www.jstor.org/pss/1266725>`_", *Technometrics*, **3**, 311-351, 1961.
-	George Box and  J. Stuart Hunter: "The :math:`2^{k-p}` `Fractional Factorial Designs - Part II <http://www.jstor.org/pss/1266553>`_", *Technometrics*, **3**, 449 - 458, 1961.
-	George Box: `Evolutionary Operation: A Method for Increasing Industrial Productivity <http://www.jstor.org/pss/2985505>`_", *Journal of the Royal Statistical Society* (Applied Statistics), **6**, 81 - 101, 1957.
-	William G. Hunter and J. R. Kittrell, "`Evolutionary Operation: A Review <http://www.jstor.org/pss/1266686>`_", *Technometrics*, **8**, 389-397, 1966.
-	Heather Tye: "`Application of Statistical Design of Experiments Methods in Drug Discovery <http://dx.doi.org/10.1016/S1359-6446(04)03086-7>`_", *Drug Discovery Today*, **9**, 485-491, 2004.
- R.A. Fisher, `Statistical Methods, Experimental Design and Scientific Inference <http://www.amazon.com/Statistical-Methods-Experimental-Scientific-Inference/dp/0198522290>`_, Oxford Science Publications, 2003.
-	Myers and Montgomery: "`Response Surface Methodology: Process and product optimization using designed experiments <http://en.wikipedia.org/wiki/Special:BookSources/0470174463#Canada>`_".
-	Hill and Hunter: "`A Review of Response Surface Methodology: A Literature Survey <http://www.jstor.org/pss/1266632>`_", *Technometrics*, **8**, 571-590 , 1966. 
-	Davies, "`The design and analysis of industrial experiments <http://en.wikipedia.org/wiki/Special:BookSources/0582460530#Canada>`_", chapter 11, revised second edition.
-	Živorad Lazić, "Design of Experiments in Chemical Engineering: A Practical Guide", Wiley-VCH, 2004.

.. OTHER REFERENCES

	Design of Experiments in Chemical Engineering: A Practical Guide, Lazić, Živorad R., Wiley-VCH, 2004. THODE Bookstacks, TP 155 .L34 2004

Background
===========

Learning about systems is important. We strive for this increased knowledge because it brings us profit, and can help us make products more efficiently. As Box, Hunter and Hunter show in the first chapter of their book, it is an iterative process.

	*	Make a conjecture (hypothesis), which we believe is true.
	*	If it is true, we expect certain consequences. 
	*	Experiment and collect data - are the consequences we expected visible in the data?
	*	If so, it may lead to the next hypothesis. If not, we formulate an alternative hypothesis. Or perhaps it is not so clear cut: we see the consequence, but not to the extent expected. Perhaps modifications are required in the experimental conditions.

And so we go about learning. An example: we expect that compounds A and B should combine in the presence of catalyst C to form product D. An initial experiment shows very little D present. Then several conditions (e.g temperature, reaction duration, and pressure) are investigated in a structured experiment to improve the yield of product D. The iterations continue until we find the most economically profitable operating point.

	
Correlation and causality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is only by intentional manipulation of our systems that we learn from them. Collecting happenstance (everyday) operating data does not always help, because it is confounded by other events that occur at the same time. Everyday data is limited by:

	*	Feedback control systems which keep the region of operation to a small zone - better yields or improved operation might exist beyond the bounds created by our automatic control systems.
	
	*	Other factors are always affecting the system. The operator mistakenly adjusts the temperature set point to 480K instead of 470K. The conversion value at the end of the shift is 3% higher. This "experiment" of sorts enters the collection of anecdotes that operators and engineers like to tell each other, and soon it becomes "accepted" that temperature can be used to improve conversion. However, it might have been a lower impurity in the raw materials, the new pump that was installed the previous day, improved controller tuning by another team of engineers, or any other event(s).
	
Designed experiments are the only way we can be sure that these correlated events are causal. You often hear people repeat the (incomplete) phrase that "*correlation does not imply causality*". That is half-true. The other half of the phrase is however: "*correlation is a necessary, but not sufficient, condition for causality*". 

Here's another example from Box's book: consider the negative slope least squares model between pressure and yield. As pressure increases, the yield drops. It is true that they are correlated, as that is exactly what a least squares model is intended for: to quantify correlation. However the true mechanism is rather that pressure is increased to remove frothing that occurs in the reactor. Higher frothing occurs when there is an impurity in the raw material, so operators increase reactor pressure when they see frothing (i.e. high impurity). However, it is the high impurity that actually causes the lower yield.

.. image:: ../figures/doe/yield-pressure-impurity-correlation.png
	:alt:	../figures/doe/yield-pressure-impurity-correlation.svg
	:scale: 50
	:width: 750px
	:align: left
	
Figure adapted from Box, Hunter and Hunter, chapter 14 (1\ :sup:`st` ed) or chapter 10 (2\ :sup:`nd` ed).

So the true effect of pressure on yield is non-existent, it is only appears in the data because of the operating policy. That is why happenstance data cannot be relied on to imply cause-and-effect.  An experiment in which the pressure is changed from low to high, performed on the same batch of raw materials (i.e. at constant impurity level), will quickly reveal that there is no causal relationship effect between pressure and yield. Furthermore, experiments should be performed in random order, further breaking any relationship with other non-causal factors. Only the truly causal effect will remain in experimental data, *correlated* effects will be broken: they show up as having close to zero correlation in the DOE data.

In summary, do not rely on anecdotal "evidence" from colleagues - always question the system and always try to perturb the system intentionally. In practice you won't always be allowed to move the system too drastically, so we will discuss response surface methods and evolutionary operation at the end of this section which can be implemented on-line in production processes.

We will show that experiments are the most efficient way to extract information about a system: i.e. the most information in the fewest number of changes. So it is always worthwhile to experiment.


Experiments with a single variable at two levels
======================================================

This is the simplest type of experiment. It involves an outcome variable, :math:`y`, and one input variable, :math:`x`. The :math:`x` variable could be continuous (e.g. temperature), or discrete (e.g. a yes/no, on/off, A/B) type variable. Some examples:

	*	Has the reaction yield increased when using catalyst A or B?
	
	*	Does the concrete's strength improve when adding a particular binder or not?
	
	*	Does the plastic's stretchability improve when extruded at lower or higher temperatures?
	
So we can perform several runs (experiments) at level A, and then some runs at level B. In both cases we strive to hold all other disturbance variables constant so we pick up only the A to B effect. Disturbances are any variables that might affect :math:`y`, but for whatever reason, we don't wish to quantify. If we cannot control the disturbance, then at least we can using :ref:`blocking <DOE-blocking-section>` and pairing.


Recap of group-to-group differences 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have already seen in the :ref:`univariate statistics section <univariate-group-to-group-differences-no-reference-set>` how to analyze this sort of data. We first calculate a pooled variance, then a :math:`z`-value, and finally a confidence interval based on this :math:`z`. Please refer back to that section to review the important assumptions we have to make to arrive at this equation.

.. math::
	s_P^2 &= \frac{(n_A -1) s_A^2 + (n_B-1)s_B^2}{n_A - 1 + n_B - 1}\\
	z &= \frac{(\overline{x}_B - \overline{x}_A) - (\mu_B - \mu_A)}{\sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}} \\

	\begin{array}{rcccl}  
		-c_t &\leq& \mu_B - \mu_A &\leq & c_t\\
		(\overline{x}_B - \overline{x}_A) - c_t \times \sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)} &\leq& \mu_B - \mu_A &\leq & (\overline{x}_B - \overline{x}_A) + c_t  \times \sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}
	\end{array}

We consider the effect of changing from condition A to condition B to be a *statistically* significant effect when this confidence interval does not span zero. However, the width of this interval and how symmetrically it spans zeros can cause us to come to a different, *practical* conclusion. In other words, we override the narrow statistical conclusion based on the richer information we can infer from the confidence interval's width and the process's variance.

Using linear least squares models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There's another interesting way that you can analyze data from an A vs B set of tests and get the identical result. Use a least squares model of the form:

.. math::

	y_i = b_0 + g d_i
	
where :math:`d_i` is an indicator variable. For example :math:`d_i = 0` when using condition A, and :math:`d_i=1` for condition B, and :math:`y_i` is the response variable. Build this linear model and then examine the *confidence interval* for the coefficient :math:`g`. Here's a small R function that takes the :math:`y` values from experiments under condition A, and the values under condition B and calculates the least squares model.

.. code-block:: s

	lm_difference <- function(groupA, groupB)
	{    
	    # Build a linear model with groupA = 0, and groupB = 1

	    y.A <- groupA[!is.na(groupA)]
	    y.B <- groupB[!is.na(groupB)]
	    x.A <- numeric(length(y.A))
	    x.B <- numeric(length(y.B)) + 1
	    y <- c(y.A, y.B)
	    x <- c(x.A, x.B)
	    x <- factor(x, levels=c("0", "1"), labels=c("A", "B"))

	    model <- lm(y ~ x)
	    return(list(summary(model), confint(model)))
	}
	
	brittle <- read.csv('http://datasets.connectmv.com/file/brittleness-index.csv')

	# We developed the "group_difference" function in the Univariate section
	group_difference(brittle$TK104, brittle$TK107)  
	lm_difference(brittle$TK104, brittle$TK107)
	
Use this function in the same way you did in :ref:`the carbon dioxide exercise in the univariate section <univariate-CO2-question>`. For example, you will find that comparing TK104 and TK107 that :math:`z = 1.4056`, and the confidence interval is: :math:`-21.4 \leq \mu_{107} - \mu_{104}\leq 119`. Similarly when coding :math:`d_i = 0` for reactor TK104 and :math:`d_i = 1` for reactor TK107, we get the least squares confidence interval: :math:`-21.4 \leq g \leq 119`. This is a little surprising, because the first method creates a pooled variance, calculates a :math:`z`-value and then a confidence interval. The least squares method just builds a linear model, then calculates the confidence interval using the model's standard error.

.. _DOE-randomization:

The importance of randomization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We :ref:`emphasized in a previous section <univariate-group-to-group-differences-no-reference-set>` that experiments must be performed in random order to avoid any unmeasured, and uncontrolled disturbances from impacting the system.

The concept of randomization was elegantly described in an example by Fisher in Chapter 2 of *The Design of Experiments* part of his book referenced above. A lady claims that she can taste the difference between a cup of tea where the milk has been added after the tea, or the tea added to the milk. By setting up :math:`N` cups of tea which either contain the milk first (M) or the tea first (T), the lady is asked to taste these :math:`N` cups and make her assessment. Fisher shows that if the experiments are performed in random order that the actual set of decisions made by the lady are just one of many possible outcomes. He calculates all possibilities (we show how below), and then calculates the probability of the lady's actual set of decisions being due to chance alone.

Let's take a look at a more engineering oriented example. We :ref:`previously considered <univariate-CO2-question>` the brittleness of a material made in either TK104 or in TK107. The same raw materials were charged to each reactor. So in effect, we are testing the difference due to using reactor TK104 or reactor TK107. Let's call them case A and case B so the notation is more general. We collected 20 brittleness values from TK104, and 23 values from TK107. We will only use the first 8 values from TK104 and the first 9 values from TK107 (you will see why soon):

.. tabularcolumns:: |l|lllllllll|

==========   === === === === === === === === === 
**Case A**   254 440 501 368 697 476 188 525
----------   --- --- --- --- --- --- --- --- --- 
**Case B**   338 470 558 426 733 539 240 628 517 
==========   === === === === === === === === === 

Fisher's insight was to create one long vector of these outcomes (length of vector = :math:`n_A + n_B`) and randomly assign "A" to :math:`n_A` of the values and "B" to :math:`n_B` of the values. One can show that there are :math:`\dfrac{(n_A + n_B)!}{n_A! n_B!}` possible combinations. For example, if :math:`n_A=8` and :math:`n_B = 9`, then the number of unique ways to split these 17 experiments into 2 groups of 8 (A) and 9 (B) is 24310 ways. E.g. one way is: BABB ABBA ABAB BAAB, so assign the experimental values accordingly [B=254, A=440, B=501, B=368, A=697, etc]. 

Only one of the 24310 sequences will correspond to the actual data printed in the above table, while all the other realizations are possible, they are fictitious. We do this, because the null hypothesis is that there is no difference between A and B. Values in the table could have come from either system.

So for each of the 24310 realizations we calculate the difference of the averages between A and B, :math:`\overline{y}_A - \overline{y}_B`, and plot a histogram of these differences. I have shown this below, together with a vertical line showing the actual realization in the table. There are 4956 permutations that had a greater difference than the one actually realized, i.e. 79.6% of the other combinations had a smaller value. 

Had we used a formal test of differences where we pool the variances, we will find a :math:`z`-value of 0.8435, and the probability of obtaining that value, using the :math:`t`-distribution with :math:`n_A + n_B - 2` degrees of freedom is 79.3%. See how close they agree?  

.. Future improvement: superimpose the t-distribution on top of the histogram (scaled). E.g. see BHH(v1) page 97
.. figure:: ../figures/doe/single-experiment-randomization.png
	:align: center
	:width: 750px
	:scale: 90

Recall that independence is required to calculate the :math:`z`-value for the average difference and compare it against the :math:`t`-distribution. By randomizing our experiments, we are able to guarantee that the results we obtain from using :math:`t`-distributions are appropriate. Without randomization, these :math:`z`-values and confidence intervals may be misleading.

The reason we prefer using the :math:`t`-distribution approach over randomization is that formulating all random combinations and then calculating all the average differences as shown here is intractable. Even on my relatively snappy computer it would take 3.4 years to calculate all possible combinations for the complete data set: 20 values from group A and 23 values from group B. [It took 122 seconds to calculate a million of them, and the full set of 960,566,918,220 combinations would take more than 3 years].

.. _DOE-COST-approach:

Changing one variable at a single time (COST)
==============================================

How do we go about running our experiments when there is more than one variable present that affects our outcome, :math:`y`?  In this section we describe **how not to do it**.

You will often come across the thinking that we should change one variable at a time:

	*	Something goes wrong with a recipe: e.g the pancakes are not as fluffy as normal, or the muffins don't rise as much as they should. You are convinced it is the new brand of all-purpose flour you recently bought. You change only the flour the next time you make pancakes to check your hypothesis.
	
	*	University labs are notorious for asking you to change one variable at a time. The reason is that these labs intend that you learn what the effect of a single variable is on some other variable (e.g. change temperature in a distillation column to improve product purity). The labs teach you that this is good scientific procedure. However, when we want to *optimize and improve* a process we should not be changing one variable at a time.
	
		.. COST is good to learn about the direction of the effect between 2 variables, but not for optimizing a process.

Consider a bioreactor where we are producing a particular enzyme. The yield is known to be affected by these 7 variables: dissolved oxygen level, agitation rate, reaction duration, feed substrate concentration and type, and reactor temperature. For illustration purposes let's assume that temperature and feed substrate concentration are chosen, as they have the greatest effect on yield.

The base operating point is 346K with a feed substrate concentration of 1.5 g/L (point marked with a circle) and a yield in the region of 63%.

.. figure:: ../figures/doe/COST-contours.png
	:align: center
	:width: 700px
	:scale: 80	
	
.. FUTURE: use a curved surface like figure (c) on page 445 of BHH2

At this point we start to investigate the effect of temperature. We decide to move up by 10 degrees to 356K, marked as point 1. After running the experiment we record a lower yield value than our starting point. So we go in the other direction and try temperatures at 338K, 330K and 322K. We are happy that the yields are increasing, but batch 4 shows a slightly lower yield. So we figure that we've reached a plateau in terms of the temperature variable. Our manager is pretty satisfied because we've boosted yield from 63% to around 67%. These 4 runs have cost us around $10,000 in equipment time and manpower costs so far.

So we get approval now to run 4 more batches, and we decide to change the substrate feed concentration. But we're going to do this at the best temperature found so far, 330K at point 3. Our intuition tells us that higher feed concentrations should boost yield, so we try 1.75 g/L. Surprisingly that lowers the yield. There's likely something we don't understand about the reaction mechanism. Anyhow, we try the other direction, down to 1.25 g/L, and we see a yield increase. We decide to keep going, down to 1.0 g/L, and finally to 0.75 g/L. We see very little change between these last two runs and we believe we have reached another plateau. Also our budget of 8 experimental runs is exhausted.

So our final operating point chosen is marked on the plot with a hexagon, at 330K and 0.75 g/L. We're proud of ourselves because we have boosted our yield from 63% to 67%, and then from 67% to 69.5%. We have also learned something interesting about our process. That the temperature appears to be negatively correlated with yield, and that the substrate concentration is negatively correlated with yield. That last observation was unexpected.

However the problem with this approach is that it leaves undiscovered value behind. Changing one variable at a single time (COST) leads you into thinking you've reached the optimum, when all you've done in fact is trap yourself at a sub-optimal solution.

Furthermore, notice that we would have got a completely different outcome had we decided to first change substrate concentration, :math:`S` and then change temperature, :math:`T`. We would have likely landed closer to the optimum. This is very unsatisfactory: we cannot use methods to optimize our processes that depend on the order of experiments!

Designed experiments, on the other hand, provide an efficient mechanism to learn about a system, often in fewer runs, and avoid misleading conclusions, such as from the COST approach. Designed experiments are always run in random order -- as we will presently see -- and we will get the same result, no matter the order.

.. _DOE-two-level-factorials:

Factorial designs: using two levels for two or more factors
==============================================================

In this section we learn how, and why we should change more than one variable at a time. We will use factorial designs because:
	
	-	we can visually interpret these designs, and see where to run future experiments
	
	-	these designs require relatively few experiments 
	
	-	they are often a building block for more complex designs

Most often we have two or more factors that affect our response variable, :math:`y`. In this section we consider the case when these factors are at two levels. Some examples: operate at low and high pH, long operating times or short times, use catalyst A or B, use mixing system A or B. The general guidance is to choose the low and high values at the edges of normal operation. It is not wise to use the lowest and highest values that each factor could possibly have: that will likely be too extreme.
	
Let's take a look at the mechanics of factorial designs by using an example where the conversion, :math:`y`, is affected by two factors: temperature, :math:`T`, and substrate concentration, :math:`S`. 

The range over which they will be varied is given in the table. This range was identified by the process operators as being sufficient to actually show a difference in the conversion, but not so large as to move the system to a totally different operating regime (that's because we will fit a linear model to the data).

	.. tabularcolumns:: |l|c|c|

	+----------------------------+-----------------+-----------------+
	|  Factor                    |  Low level, |-| | High level, |+| |
	+============================+=================+=================+
	| Temperature, :math:`T`     |  338 K          | 354 K           |
	+----------------------------+-----------------+-----------------+
	| Substrate level, :math:`S` |  1.25 g/L       | 1.75 g/L        |
	+----------------------------+-----------------+-----------------+

#.	Write down the factors that will be varied: :math:`T`, and :math:`S`.

#.	Write down the coded runs in standard order, also called :index:`Yates order`, which alternates the sign of the first variable the fastest and the last variable the slowest. By convention we start all runs at their low levels and finish off with all factors at their high levels. There will be :math:`2^k` runs, where :math:`k` is the number of variables in the design, and the :math:`2` refers to the number of levels for each factor. In this case :math:`2^2 = 4` experiments (runs). **We perform the actual experiments in random order though**, but always write the table in this standard order.

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


#.	Add an additional column to the table for the response variable. The response variable is a quantitative value, :math:`y` = conversion in this case, measured as a percentage. 

	.. tabularcolumns:: |c|c|c|c||c|
	
	+-----------+-------+---------------+-----------------+--------------+
	| Experiment|Order *| :math:`T` [K] | :math:`S` [g/L] | :math:`y` [%]|
	+===========+=======+===============+=================+==============+
	| 1         | 3     | |-|           | |-|             |  69          |
	+-----------+-------+---------------+-----------------+--------------+
	| 2         | 2     | |+|           | |-|             |  60          |
	+-----------+-------+---------------+-----------------+--------------+
	| 3         | 4     | |-|           | |+|             |  64          |
	+-----------+-------+---------------+-----------------+--------------+
	| 4         | 1     | |+|           | |+|             |  53          |
	+-----------+-------+---------------+-----------------+--------------+
	
	:math:`\ast` Experiments were performed in random order, in this case we happened to run experiment 4 first, and experiment 3 was run last.

#.	For simple systems you can visualize the design and results as shown here. This is known as a *cube plot*.

	.. image:: ../figures/doe/factorial-two-levels-two-variables-no-analysis.png
		:align: left
		:width: 750px
		:scale: 50
		
.. _DOE-two-level-factorials-main-effects:
		
Analysis of a factorial design: main effects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step is to calculate the :index:`main effect` of each variable. The effects are considered, by convention, to be the difference from the high level to the low level. So the interpretation of a main effect is by how much the outcome, :math:`y` is adjusted when changing the variable.

Consider the two runs where :math:`S` is at the |-| level, experiments 1 and 2. The only change between these two runs is the temperature, so the temperature effect is :math:`\Delta T_{S-} = 60-69 = -9\%` per (354-338)K, i.e. -9% change in the conversion outcome per 16K change in the temperature. 

Runs 3 and 4 have :math:`S` at the |+| level. Again, the only change is in the temperature: :math:`\Delta T_{S+} = 53-64 = -11\%` per 16K. So we now have two temperature effects, and the average of them is a -10% change in conversion per 16K change in temperature.

We can perform a similar calculation for the main effect of substrate concentration, :math:`S` by comparing experiments 1 and 3. :math:`\Delta S_{T-} = 64-69 = -5\%` per 0.5g/L, while experiments 2 and 4 give :math:`\Delta S_{T+} = 53-60 = -7\%` per 0.5g/L. So the average main effect for :math:`S` is a :math:`-6\%` change in conversion for every 0.5 g/L change in substrate concentration. A graphical method is developed below which you should use:

	.. image:: ../figures/doe/factorial-two-levels-two-variables-with-analysis.png
		:align: left
		:width: 750px
		:scale: 60

This visual summary is a very effective method of seeing how the system responds to the two variables. We can see the gradients in the system and the likely region where we can perform the next experiments to improve the bioreactor's conversion.

The following surface plot illustrates the true, but unknown surface, from which our measurements are taken: notice the slight curvature on the edges of each face. The main effects estimated above are a linear approximation of the conversion over the region spanned by the factorial.

	.. image:: ../figures/doe/factorial-two-level-surface-example-cropped.png
		:align: left
		:width: 750px
		:scale: 50

There is an alternative way to visualize these main effects. Use this method when you don't have computer software to draw the surfaces. (We saw this earlier in the :ref:`visualization section <SECTION-data-visualization>`). It is called an :index:`interaction plot`, which we discuss more in the next section.

	.. image:: ../figures/doe/factorial-two-level-line-plot.png
		:align: left
		:width: 750px
		:scale: 80
		
.. _DOE-two-level-factorials-interaction-effects:	

Analysis of a factorial design: interaction effects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We expect in many real systems that the main effect of temperature, :math:`T`, for example, is different at other levels of substrate concentration, :math:`S`. It is quite plausible for a bioreactor system that the main temperature effect on conversion is much greater, if the substrate concentration, :math:`S` is also high. While at low values of :math:`S`, the temperature effect is smaller. 

.. index:: interaction effects

We call this **interaction**, when the effect of one factor is not constant at different levels of the other factors.

Let's use a *different system* here to illustrate interaction effects, but still using :math:`T` and :math:`S` as the variables being changed, and keeping the response variable as :math:`y` = conversion, shown by the contour lines.

	.. image:: ../figures/doe/factorial-two-level-with-interactions.png
		:align: left
		:width: 550px
		:scale: 85
		
	.. tabularcolumns:: |l|c|c||c|
	
	+-----------+---------------+-----------------+--------------+
	| Experiment| :math:`T` [K] | :math:`S` [g/L] | :math:`y` [%]|
	+===========+===============+=================+==============+
	| 1         | |-|  (390K)   | |-| (0.5 g/L)   |  77          |
	+-----------+---------------+-----------------+--------------+
	| 2         | |+|  (400K)   | |-| (0.5 g/L)   |  79          |
	+-----------+---------------+-----------------+--------------+
	| 3         | |-|  (390K)   | |+| (1.25 g/L)  |  81          |
	+-----------+---------------+-----------------+--------------+
	| 4         | |+|  (400K)   | |+| (1.25 g/L)  |  89          |
	+-----------+---------------+-----------------+--------------+

The main effect of temperature for this system is: 
		
		-	:math:`\Delta T_{S-} = 79 - 77 = 2\%` per 10K
		-	:math:`\Delta T_{S+} = 89 - 81 = 8\%` per 10K
		-	the average temperature main effect is: 5% per 10 K
		
Notice how different the main effect is at the low and high level of :math:`S`. So the average of the two is an incomplete description of the system. There is some other aspect to the system that we have not captured.

Similarly, the main effect of substrate concentration is:
	
		-	:math:`\Delta S_{T-} = 81 - 77 = 4\%` per 0.75 g/L
		-	:math:`\Delta S_{T-} = 89 - 79 = 10\%` per 0.75 g/L
		-	the average substrate concentration main effect is: 7% per 0.75 g/L

..	TODO: Draw in Inkscape, the geometrica analysis of the main effects, and the interaction plot for this system: annotated with T effect at low S, T effect at high S, S effect at low T, S effect at high T

The data may also be visualized using an *interaction plot*:

.. figure:: ../figures/doe/factorial-two-level-line-plot-with-interaction.png
	:align: center
	:width: 600px
	:scale: 100

The lack of parallel lines is a clear indication of interaction. The temperature effect is stronger at high levels of :math:`S`, and the effect of :math:`S` on conversion is also greater at high levels of temperature. What is missing is an interaction term, given by the product of temperature and substrate. We represent this as  :math:`T \times S`, and call it temperature-substrate interaction term.  

This interaction term should be zero for systems with no interaction, which implies the lines are parallel in the interaction plot. Such systems will have roughly the same effect of :math:`T` at both low and high values of :math:`S` (and in between). So then, a good way to quantify interaction is by how different the main effect terms are at the high and low levels of the other factor in the interaction. The interaction must also be symmetrical, since if :math:`T` interacts with :math:`S`, then :math:`S` interacts with :math:`T` by the same amount.

:math:`T` interaction with :math:`S`:  

	-	Change in conversion due to :math:`T` at high :math:`S`: :math:`+8`
	-	Change in conversion due to :math:`T` at low :math:`S`: :math:`+2`
	-	The half difference: :math:`[+8 - (+2)]/2 = \bf{3}`
	
:math:`S` interaction with :math:`T`:

	-	Change in conversion due to :math:`S` at high :math:`T`: :math:`+10`
	-	Change in conversion due to :math:`S` at low :math:`T`: :math:`+4`
	-	The half difference: :math:`[+10 - (+4)]/2 = \bf{3}`

A large, positive interaction term indicates that temperature and substrate concentration will increase conversion by a greater amount when both :math:`T` and :math:`S` are high. Similarly, these two terms will rapidly reduce conversion when they both are low.

We will get a much better appreciation for interpreting main effect and interaction effect in the next section, where we consider the analysis in the form of a linear, least squares model.

.. TODO: quantify and describe more completely what the interaction means


.. _DOE-analysis-by-least-squares:

Analysis by least squares modelling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's review the original system (the one with little interaction) and analyze the data using a least squares model. We represent the original data here, with the baseline conditions:

	.. tabularcolumns:: |l|c|c||c|

	+-----------+---------------+-----------------+--------------+
	| Experiment| :math:`T` [K] | :math:`S` [g/L] | :math:`y` [%]|
	+===========+===============+=================+==============+
	| Baseline  | **346 K**     | **1.50**        |              |
	+-----------+---------------+-----------------+--------------+
	| 1         | |-|  (338K)   | |-| (1.25 g/L)  |  69          |
	+-----------+---------------+-----------------+--------------+
	| 2         | |+|  (354K)   | |-| (1.25 g/L)  |  60          |
	+-----------+---------------+-----------------+--------------+
	| 3         | |-|  (338K)   | |+| (1.75 g/L)  |  64          |
	+-----------+---------------+-----------------+--------------+
	| 4         | |+|  (354K)   | |+| (1.75 g/L)  |  53          |
	+-----------+---------------+-----------------+--------------+

It is standard practice to represent the data from DOE runs in a centered and scaled form: :math:`\dfrac{\text{variable} - \text{center point}}{\text{range}/2}`

	*	:math:`T_{-} = \dfrac{338 - 346}{(354-338)/2} = \dfrac{-8}{8} = -1`
	*	:math:`S_{-} = \dfrac{1.25 - 1.50}{(1.75 - 1.25)/2} = \dfrac{-0.25}{0.25} = -1`

Similarly, :math:`T_{+} = +1` and :math:`S_{+} = +1`. While the center points (baseline experiment) would be :math:`T_{0} = 0` and :math:`S_{0} = 0`.

So we will propose a least squares model, that describes this system:

.. math::

	\text{Population model}: \qquad\qquad &y = \beta_0 + \beta_Tx_T + \beta_S x_S + \beta_{TS} x_Tx_S + \varepsilon\\
	\text{Sample model}: \qquad\qquad     &y = b_0 + b_Tx_T + b_S x_S + b_{TS} x_Tx_S + e\\
	
We have 4 parameters to estimate and 4 data points. This means when we fit the model to the data we will have no residual error, since there are no degrees of freedom left. If we had replicate experiments we would have degrees of freedom to estimate the error, but more on that later. Writing the above equation for each observation:

.. math::

	\begin{bmatrix} y_1\\ y_2\\ y_3 \\ y_4 \end{bmatrix} &=
	\begin{bmatrix} 1 & T_{-} & S_{-} & T_{-}S_{-}\\ 
	                1 & T_{+} & S_{-} & T_{+}S_{-}\\
	                1 & T_{-} & S_{+} & T_{-}S_{+}\\
	                1 & T_{+} & S_{+} & T_{+}S_{+}\\
	\end{bmatrix}
	\begin{bmatrix} b_0 \\ b_T \\ b_S \\ b_{TS} \end{bmatrix} +
	\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \end{bmatrix}\\
	\begin{bmatrix} 69\\ 60\\ 64\\ 53 \end{bmatrix} &=
	\begin{bmatrix} 1 & -1 & -1 & +1\\ 
	                1 & +1 & -1 & -1\\
	                1 & -1 & +1 & -1\\
	                1 & +1 & +1 & +1\\
	\end{bmatrix}
	\begin{bmatrix} b_0 \\ b_T \\ b_S \\ b_{TS} \end{bmatrix} +
	\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \end{bmatrix}\\
	\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e} \\
	\mathbf{X}^T\mathbf{X} &=
	\begin{bmatrix} 4   & 0   & 0   & 0\\ 
	                0   & 4   & 0   & 0\\
	                0   & 0   & 4   & 0\\
	                0   & 0   & 0   & 4
	\end{bmatrix} \\
	\mathbf{X}^T\mathbf{y} &= \begin{bmatrix} 246 \\ -20 \\ -12 \\ -2\end{bmatrix}\\
	\mathbf{b} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y} &= 
	\begin{bmatrix} 1/4 & 0   & 0   & 0\\ 
	                0   & 1/4 & 0   & 0\\
	                0   & 0   & 1/4 & 0\\
	                0   & 0   & 0   & 1/4
	\end{bmatrix}
	\begin{bmatrix} 246 \\ -20 \\ -12 \\ -2\end{bmatrix}=
	\begin{bmatrix} 61.5 \\ -5 \\ -3 \\ -0.5 \end{bmatrix}\\
	
Some things to note are (1) the orthogonality of :math:`\mathbf{X}^T\mathbf{X}` and (2) the interpretation of these coefficients.

#.	Note how the :math:`\mathbf{X}^T\mathbf{X}` has zeros on the off-diagonals. This confirms, algebraically, what we knew intuitively. The change we made in temperature, :math:`T`, was independent of the changes we made in substrate concentration, :math:`S`. This means that we can separately calculat *and interpret* the slope coefficients in the model.

#.	What is the interpretation of, for example, :math:`b_T = -5`?  Recall that it is the effect of increasing the temperature by **1 unit**. In this case the :math:`x_T` variable has been  normalized, but this slope coefficient represents the effect of changing :math:`x_T` from 0 to 1, which in the original variables is a change from 346 to 354K, i.e. an 8K increase in temperature. It equally well represents the effect of changing :math:`x_T` from -1 to 0: a change from 338K to 346K decreases conversion by 5%.

	Similarly, the slope coefficient for :math:`b_S = -3` represents the expected decrease in conversion when :math:`S` is increased from 1.50 g/L to 1.75 g/L.

	Now contrast these numbers with those in the :ref:`graphical analysis done previously <DOE-two-level-factorials-main-effects>` and repeated below. They are the same, as long as we are careful to interpret them as the change over **half the range**.
	
	.. image:: ../figures/doe/factorial-two-levels-two-variables-with-analysis.png
		:align: left
		:width: 750px
		:scale: 50

	The 61.5 term in the least squares model is the expected conversion at the baseline conditions. Notice from the least squares equations how it is just the average of the 4 experimental values, even though we did not actually perform an experiment at the center.
		
Let's return to the :ref:`system with high interaction <DOE-two-level-factorials-interaction-effects>` where the four outcome values in standard order were 
77, 79, 81 and 89. Defining the baseline operation as :math:`T` = 395K, and :math:`S` = 1.5 g/L, you should prove to yourself that its least squares model is:

	.. math::
	
		y = 81.5 + 2.5 x_T + 3.5 x_S + 1.5 x_T x_S
		
The interaction term can now be readily interpreted: it is the additional increase in conversion seen when both temperature and :math:`S` are at their high level. If :math:`T` is at the high level and :math:`S` is at the low level, then the least squares model shows that conversion is expected at 81.5 + 2.5 - 3.5 -1.5 = 79. So the interaction term has *decreased* conversion by 1.5 units.

Finally, out of interest, the non-linear surface that was used to generate the experimental data for the interacting system is coloured in the illustration. In practice we never know what this surface looks like, but we estimate it with the least squares plane which appears below the non-linear surface as black and white grids. The corners of the box are outer levels at which we ran the factorial experiments.
	
	.. image:: ../figures/doe/factorial-two-level-surface-with-interaction-cropped.png
		:align: left
		:width: 750px
		:scale: 50
	
The corner points are exact with the nonlinear surface, because we have used the 4 values to estimate 4 model parameters. There are no degrees of freedom left and the model's residuals are therefore zero. Obviously the linear model will be less accurate away from the corner points when the true system is nonlinear, but it is a useful model over the region in which we will use it later in the :ref:`section on response surface methods <DOE-RSM>`.
	
Example: design and analysis of a 3-factor experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example should be done by yourself. It is based on question 19 in the exercises for Chapter 5 in Box, Hunter, and Hunter (2nd edition).

The data are from a plastics molding factory which must treat its waste before discharge. The :math:`y` variable represents the average amount of pollutant discharged [lb per day], while the 3 factors that were varied were:

 	-	:math:`C`: the chemical compound added [A or B]
	-	:math:`T`: the treatment temperature [72°F or 100°F]
	-	:math:`S`: the stirring speed [200 rpm or 400 rpm]
	-	:math:`y`: the amount of pollutant discharged [lb per day]

	.. tabularcolumns:: |l|l||c|c|c||c|

	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| Experiment| Order | :math:`C`     | :math:`T` [°F]  | :math:`S` [rpm] | :math:`y` [lb]  |
	+===========+=======+===============+=================+=================+=================+
	| 1         | 5     | A             | 72              | 200             | 5               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 2         | 6     | B             | 72              | 200             | 30              |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 3         | 1     | A             | 100             | 200             | 6               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 4         | 4     | B             | 100             | 200             | 33              |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 5         | 2     | A             | 72              | 400             | 4               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 6         | 7     | B             | 72              | 400             | 3               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 7         | 3     | A             | 100             | 400             | 5               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+
	| 8         | 8     | B             | 100             | 400             | 4               |
	+-----------+-------+---------------+-----------------+-----------------+-----------------+

#.	Draw a geometric figure that illustrates the data from this experiment.

#.	Calculate the main effect for each factor by hand.

	*	**C effect**: There are 4 estimates of :math:`C = \displaystyle \frac{(+25) + (+27) + (-1) + (-1)}{4} = \frac{50}{4} = \bf{12.5}`
	*	**T effect**: There are 4 estimates of :math:`T = \displaystyle \frac{(+1) + (+3) + (+1) + (+1)}{4} = \frac{6}{4} = \bf{1.5}`
	*	**S effect**: There are 4 estimates of :math:`S = \displaystyle \frac{(-27) + (-1) + (-29) + (-1)}{4} = \frac{58}{4} = \bf{-14.5}`

#.	Calculate the 3 two-factor interactions (2fi) by hand

	*	**CT interaction**: There are 2 estimates of :math:`CT`. Recall that interactions are calculated as the half difference going from high to low. Consider the change in :math:`C` when

		-	:math:`T_\text{high}` (at :math:`S` high) = 4 - 5 = -1
		-	:math:`T_\text{low}` (at :math:`S` high) = 3 - 4 = -1
		-	First estimate = [(-1) - (-1)]/2 = 0
		-	:math:`T_\text{high}` (at :math:`S` low) = 33 - 6 = +27
		-	:math:`T_\text{low}` (at :math:`S` low) = 30 - 5 = +25
		-	Second estimate = [(+27) - (+25)]/2 = +1
	
		-	Average **CT** interaction = (0 + 1)/2 = **0.5**
		-	You can interchange :math:`C` and :math:`T` and still get the same result.

	*	**CS interaction**: There are 2 estimates of :math:`CS`.  Consider the change in :math:`C` when

			-	:math:`S_\text{high}` (at :math:`T` high) = 4 - 5 = -1
			-	:math:`S_\text{low}` (at :math:`T` high) = 33 - 6 = +27
			-	First estimate = [(-1) - (+27)]/2 = -14
			-	:math:`S_\text{high}` (at :math:`T` low) = 3 - 4 = -1
			-	:math:`S_\text{low}` (at :math:`T` low) = 30 - 5 = +25
			-	Second estimate = [(-1) - (+25)]/2 = -13

			-	Average **CS** interaction = (-13 - 14)/2 = **-13.5**
			-	You can interchange :math:`C` and :math:`S` and still get the same result.	
		
	*	**ST interaction**: There are 2 estimates of :math:`ST`: (-1 + 0)/2 = **-0.5**, calculate in the same way as above.

#.	Calculate the single 3 factor interaction (3fi).
	
	There is only a single estimate of :math:`CTS`:

		-	:math:`CT` effect at high :math:`S` = 0
		-	:math:`CT` effect at low :math:`S` = +1
		-	:math:`CTS` interaction = [(0) - (+1)] / 2 = **-0.5**

		-	You can calculate this also by considering the :math:`CS` effect at the two levels of :math:`T`
		-	Or, you can calculate this by considering the :math:`ST` effect at the two levels of :math:`C`.
		-	All 3 approaches give the same result.

#.	Compute the main effects and interactions using matrix algebra and a least squares model.

	.. math::

		\begin{bmatrix} 5\\30\\6\\33\\4\\3\\5\\4 \end{bmatrix} &=
		\begin{bmatrix} +1 & -1 & -1 & -1 & +1 & +1 & +1 & -1\\ 
		                +1 & +1 & -1 & -1 & -1 & -1 & +1 & +1\\
		                +1 & -1 & +1 & -1 & -1 & +1 & -1 & +1\\
		                +1 & +1 & +1 & -1 & +1 & -1 & -1 & -1\\
		                +1 & -1 & -1 & +1 & +1 & -1 & -1 & +1\\
		                +1 & +1 & -1 & +1 & -1 & +1 & -1 & -1\\
		                +1 & -1 & +1 & +1 & -1 & -1 & +1 & -1\\
		                +1 & +1 & +1 & +1 & +1 & +1 & +1 & +1\\
		\end{bmatrix}
		\begin{bmatrix} b_0 \\ b_C \\ b_T \\ b_{S} \\ b_{CT} \\ b_{CS} \\ b_{TS} \\ b_{CTS}  \end{bmatrix} \\
		\mathbf{y} &= \mathbf{X} \mathbf{b} 
	
#.	Use computer software to build the following model and verify that:

	.. math:: 
	
		y = 11.25 + 6.25x_C + 0.75x_T -7.25x_S + 0.25 x_C x_T -6.75 x_C x_S -0.25 x_T x_S - 0.25 x_C x_T x_S

Learning notes:

	*	The chemical compound could be coded either as (A = :math:`-1`, B = :math:`+1`), or (A = :math:`+1`, B = :math:`-1`). The interpretation of the :math:`x_C` coefficient is the same, regardless of the coding.
	
 	*	Just the tabulation of the raw data gives us some interpretation of the results. Why?  Since the variables are manipulated independently, we can just look at the relationship of each factor to :math:`y`, without considering the others.  It is expected that the chemical compound and speed have a strong effect on :math:`y`, but we can also see the **chemical** :math:`\times` **speed** interaction. You get this last interpretation by writing out the full :math:`\mathbf{X}` design matrix.

Assessing significance of main effects and interactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
When there are no :index:`replicate points <pair: replicates; experiments>`, then the number of factors to estimate from a full factorial is :math:`2^k` from the :math:`2^k` observations. So there are no degrees of freedom left to calculate the standard error, nor to calculate the confidence intervals for the main effects and interaction terms.

The standard error can be estimated if complete replicates are available. However, a complete replicate is onerous, because a complete replicate implies the entire experiment is repeated: system setup, running the experiment and measuring the result. Taking two samples from one actual experiment and measuring :math:`y` twice is not a true replicate, that is only an estimate of the measurement error and analytical error. 

Furthermore, there are better ways to spend our experimental budget than running complete replicate experiments - see the section on :ref:`screening designs <DOE-saturated-screening-designs>` later on. Only later in the overall experimental procedure should we run replicate experiments as a verification step and to assess the statistical significance of effects.

There are 2 main ways we can determine if a main effect or interaction is significant.

.. _DOE-Pareto-plot:

Pareto plot
^^^^^^^^^^^^^^^^^^^^^^^^^

.. Note:: This is a make-shift approach that is only applicable if all the factors are centered and scaled.

A full factorial with :math:`2^k` experiments has :math:`2^k` parameters to estimate. Once these parameters have been calculated, for example, by using a :ref:`least squares model <DOE-analysis-by-least-squares>`, then plot the absolute value of the model coefficients in sorted order: from largest magnitude to smallest, ignoring the intercept term. Significant coefficients are established by visual judgement - establishing a visual cut-off by contrasting to small coefficients to the larger ones.

.. image:: ../figures/doe/pareto-plot-full-fraction.png
	:align: left
	:width: 800px
	:scale: 50
	
In the above example we would interpret that factors **A**, **C** and **D**, as well as the interactions of **AC** and **AD** have a significant and causal effect on the response variable, :math:`y`. The main effect of **B** on the response :math:`y` is small - at least over the range that **B** was used in the experiment. Factor **B** can be omitted from future experimentation in this region, though it might be necessary to include it again if the system is operated at a very different point.

The reason why we can compare the coefficients this way, which is not normally the case with least squares models, is that we have both centered and scaled the factor-variables. If the centering is at typical baseline operation, and the range spanned by each factor is that expected over the typical operating range, then we can fairly compare each coefficient in the bar plot. Each bar represents the influence of that term on :math:`y` for a one-unit change in the factor, i.e. a change over half its operating range.

Obviously if the factors are not scaled appropriately, then this method will be error prone.  However, the approximate guidance is accurate, especially when you do not have a computer, or if additional information required by the other methods (discussed below) is not available. It is also the only way to estimate the effects for :ref:`highly fractionated and saturated designs <DOE-saturated-screening-designs>`.


Standard error: from replicate runs, or from an external data set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: It is often better to spend your experimental budget screening for additional factors than for replicating experiments.

But, if a duplicate run exists at every combination of the factorial, then the standard error can be estimated as follows:

	-	Let :math:`y_{i,1}` and :math:`y_{i,2}` be the two response values for each of the :math:`i^\text{th}` runs, where :math:`i=1, 2, ..., 2^k`
	-	The mean response for the :math:`i^\text{th}` run is :math:`\overline{y}_i = 0.5y_{i,1} + 0.5y_{i,2}`
	-	Denote the difference between them as :math:`d_i = y_{i,2} - y_{i,1}`, or the other way around - it doesn't matter.
	-	The variance can be estimated with a single degree of freedom as :math:`s_i^2 = \dfrac{(y_{i,1} - \overline{y}_i)^2 + (y_{i,2} - \overline{y}_i)^2}{1}`
	-	The variance can also be written as :math:`s_i^2 = d_i^2/2`
	-	Now we can pool the variances for the :math:`2^k` runs to estimate :math:`\hat{\sigma}^2 = S_E^2 = \dfrac{1}{2}\displaystyle\sum_i^{2^k}{d_i^2}`
	-	This estimated standard error is :math:`t`-distributed with :math:`2^k` degrees of freedom.

The standard error can be calculated in a similar manner if more than one duplicate run is performed. So rather run a :math:`2^4` factorial for 4 factors than a :math:`2^3` factorial twice; or as we will see later - one can screen five or more factors with :math:`2^4` runs.
	
.. sidebar:: A note about standard errors and magnitude of effects

	In these notes we quantify the effect as the change in response over *half the range* of the factor. For example, if the centerpoint is 400K, the lower level is 375K, and the upper level is 425K, then an effect of ``"-5"`` represents a reduction in :math:`y` of 5 units for every increase in 25K in :math:`x`.
	
	
	We use this representation because it corresponds with the results calculated from least-squares software. Putting the matrix of :math:`-1` and :math:`+1` entries as :math:`\mathbf{X}` into the software, and the corresponding vector of responses, :math:`y`, will calculate these effects as :math:`\mathbf{b} = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}\mathbf{X}\mathbf{y}`.
	
	
	Other textbooks, specifically Box, Hunter and Hunter will report effects that are double ours. This is because they consider the effect to be the change from the lower level to the upper level (double the distance). The advantage of their representation is that binary factors (catalyst A or B; agitator on or off) can be readily interpreted. While in our notation, the effect is a little harder to describe (simply double it!).
	
	
	The advantage of our methodology though is that the results calculated by hand would be the same as that from any computer software with respect to the magnitude of the coefficients and the standard errors; particularly in the case of duplicate runs and experiments with center points.
	
	
	Remember: our effects are half those reported in Box, Hunter, and Hunter, and some other text books; our standard error would also be half of theirs. The conclusions drawn will always be the same, as long as one is consistent.
		
Once :math:`S_E` has been calculated, we can calculate the standard error for each model coefficient, and then confidence intervals can be constructed for each main effect and interaction. And, because the model matrix is orthogonal, the confidence interval for each effect is independent of the other. This is because the general confidence interval is :math:`\mathcal{V}\left(\mathbf{b}\right) = \left(\mathbf{X}^T\mathbf{X}\right)^{-1}S_E^2`, and the off-diagonal elements in :math:`\mathbf{X}^T\mathbf{X}` are zero.

So for an experiment with :math:`n` runs, and where we have coded our :math:`\mathbf{X}` matrix to contain :math:`-1` and :math:`+1` elements, and when the :math:`\mathbf{X}` matrix is orthogonal, then the standard error for coefficient :math:`b_i` is :math:`S_E(b_i) = \sqrt{\mathcal{V}\left(b_i\right)} = \sqrt{\dfrac{S_E^2}{\sum{x_i^2}}}`. Some examples:

	*	A :math:`2^3` factorial where every combination has been repeated will have :math:`n=16` runs, so the standard error for each coefficient will be the same, at :math:`S_E(b_i) = \sqrt{\dfrac{S_E^2}{16}} = \dfrac{S_E}{4}`. 
	*	A :math:`2^3` factorial with 3 additional runs at the center point would have a least squares representation of:
	
		.. math::
		
			\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}\\
			\begin{bmatrix} y_1\\ y_2\\ y_3 \\ y_4 \\ y_5 \\ y_6 \\ y_7 \\ y_8 \\ y_{c,1} \\ y_{c,2} \\ y_{c,3}\end{bmatrix} &=
			\begin{bmatrix} 1 & A_{-} & B_{-} & C_{-} & A_{-}B_{-} & A_{-}C_{-} & B_{-}C_{-} & A_{-}B_{-}C_{-}\\ 
							1 & A_{+} & B_{-} & C_{-} & A_{+}B_{-} & A_{+}C_{-} & B_{-}C_{-} & A_{+}B_{-}C_{-}\\
							1 & A_{-} & B_{+} & C_{-} & A_{-}B_{+} & A_{-}C_{-} & B_{+}C_{-} & A_{-}B_{+}C_{-}\\
							1 & A_{+} & B_{+} & C_{-} & A_{+}B_{+} & A_{+}C_{-} & B_{+}C_{-} & A_{+}B_{+}C_{-}\\
							1 & A_{-} & B_{-} & C_{+} & A_{-}B_{-} & A_{-}C_{+} & B_{-}C_{+} & A_{-}B_{-}C_{+}\\
							1 & A_{+} & B_{-} & C_{+} & A_{+}B_{-} & A_{+}C_{+} & B_{-}C_{+} & A_{+}B_{-}C_{+}\\
							1 & A_{-} & B_{+} & C_{+} & A_{-}B_{+} & A_{-}C_{+} & B_{+}C_{+} & A_{-}B_{+}C_{+}\\
							1 & A_{+} & B_{+} & C_{+} & A_{+}B_{+} & A_{+}C_{+} & B_{+}C_{+} & A_{+}B_{+}C_{+}\\
							1 & 0     & 0     & 0     & 0          & 0          & 0          & 0              \\
							1 & 0     & 0     & 0     & 0          & 0          & 0          & 0              \\
							1 & 0     & 0     & 0     & 0          & 0          & 0          & 0              
			\end{bmatrix}
			\begin{bmatrix} b_0 \\ b_A \\ b_B \\ b_{C} \\ b_{AB} \\ b_{AC} \\ b_{BC} \\ b_{ABC} \end{bmatrix} +
			\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \\ e_5 \\ e_6 \\ e_7 \\ e_8 \\ e_{c,1} \\ e_{c,2} \\ e_{c,3} \end{bmatrix}\\
			\mathbf{y} & = 
			\begin{bmatrix} 1 & -1 & -1 & -1 & +1 & +1 & +1 & -1\\ 
							1 & +1 & -1 & -1 & -1 & -1 & +1 & +1\\
							1 & -1 & +1 & -1 & -1 & +1 & -1 & +1\\
							1 & +1 & +1 & -1 & +1 & -1 & -1 & -1\\
							1 & -1 & -1 & +1 & +1 & -1 & -1 & +1\\ 
							1 & +1 & -1 & +1 & -1 & +1 & -1 & -1\\
							1 & -1 & +1 & +1 & -1 & -1 & +1 & -1\\
							1 & +1 & +1 & +1 & +1 & +1 & +1 & +1\\
							1 &  0 &  0 &  0 &  0 &  0 &  0 &  0\\
							1 &  0 &  0 &  0 &  0 &  0 &  0 &  0\\
							1 &  0 &  0 &  0 &  0 &  0 &  0 &  0
			\end{bmatrix}
			\begin{bmatrix} b_0 \\ b_A \\ b_B \\ b_{C} \\ b_{AB} \\ b_{AC} \\ b_{BC} \\ b_{ABC} \end{bmatrix} + \mathbf{e}
			
		Note that the center point runs do not change the orthogonality of :math:`\mathbf{X}`, however, as we expect after having studied the :ref:`least squares modelling <SECTION-least-squares-modelling>` section, that additional runs decrease the variance of the model parameters, :math:`\mathcal{V}(\mathbf{b})`. In this can there are :math:`n=2^3+3 = 11` runs, so the standard error is decreased to :math:`S_E^2 = \dfrac{\mathbf{e}^T\mathbf{e}}{11 - 8}`, but the center points do not further reduce the variance of the parameters in :math:`\sqrt{\dfrac{S_E^2}{\sum{x_i^2}}}`, since the denominator is still :math:`2^k` (**except for the intercept term**, whose variance is reduced by the center points).
	
Once we obtain the standard error for our system and calculate the variance of the parameters, we can multiply it by the critical :math:`t`-value at the desired confidence level in order to calculate the confidence limit. However, it is customary to just report the standard error next to the coefficients, so that the user can use their own level of confidence. For example:

	.. math::
	
		\text{Temperature effect}, b_T &= 11.5 \pm 0.707\\
		\text{Catalyst effect}, b_K &= 0.75 \pm 0.707
		
So even though the temperature effect's confidence interval would be :math:`11.5 - c_t \times 0.707 \leq \beta_T \leq 11.5 + c_t \times 0.707`, it is clear from the above representation that the temperature effect is significant in this example, while the catalyst effect is not.

.. OMIT: this can be confusing and misleading

	Normal probability plots
	^^^^^^^^^^^^^^^^^^^^^^^^^

	If the hypothesis that there is no causal effect from the :math:`k` factors on the response is true, then the :math:`2^k-1` parameter estimates, not counting the intercept, should be normally distributed. That is from the central limit theorem, and the fact that estimated coefficients are linear combinations of the response variable.

	An example for a :math:`2^3` factorial would be that the 7 coefficients, not including :math:`b_0`, in this linear model would be normally distributed:

	.. math::

		y_i = b_0 + b_A x_A + b_B x_B + b_{C}x_C + b_{AB}x_{AB} + b_{AC}x_{AC} +  b_{BC}x_{BC} +  b_{ABC}x_{ABC}
	
	A normal probability plot is a non-linear transformation of the data so that the s-shape of the cumulative normal distribution appears as a straight line. We used this idea in the section on :ref:`univariate statistics <SECTION-univariate-review>` where a q-q plot was constructed to assess normality. Another way to visualize this concept is to draw vertical divisions on the normal distribution curve, to create :math:`2^k-1` sections of equal area. One effect is expected per division.

	.. TODO: illustration of normal distribution division

	.. code-block:: s

		k = 4
	 	n = 2^k - 1
		index <- seq(1, n)
		p <- (index - 0.5) / n
		theoretical.quantity <- qnorm(p)
	
		labels = c('A', 'B',    'C',   'D', 'AB',  'AC', 'AD',   'BC', 'BD',   'CD', 
		            'ABC',  'ABD',  'ACD',  'BCD',  'ABCD')
		b      = c( -4,  12, -1.125, -2.75,  0.5, 0.375,  0.0, -0.625, 2.25, -0.125, 
		           -0.375,   0.25, -0.125, -0.375,  -0.125)

		b.sort = sort(b)

		plot(theoretical.quantity, b.sort)
		qqline(b.sort)

		# Or more simply: use the qqPlot function:
		library(car)
		qqPlot(b, labels=labels)
	
	.. figure:: ../figures/doe/normal-probability-signifcant-effects.png
		:align: center
		:scale: 50
		:width: 800px
		

Refitting the model after removing non-significant effects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So after having established which effects are significant, we can exclude the non-significant effects and increase the degrees of freedom. (We do not have to recalculate the model parameters - why?). The residuals will be non-zero now, so we can then estimate the standard error, and apply all the tools from least squares modelling to assess the residuals. Plots of the residuals in experimental order, against fitted values, q-q plots, and all the other assessment tools from earlier are used, as usual.

Continuing the above example, where a :math:`2^4` factorial was run, and the response values, in standard order were :math:`y = [71, 61, 90, 82, 68, 61, 87, 80, 61, 50, 89, 83, 59, 51, 85, 78]`. The significant effects were from **A**, **B**, **D**, and **BD**. Now omitting the non-significant effects, there are only 5 parameters to estimate, including the intercept, so the standard error is :math:`S_E^2 = \dfrac{39}{16-5} = 3.54`, with 11 degrees of freedom. The :math:`S_E(b_i)` value for all coefficients, except the intercept, is :math:`\sqrt{\dfrac{S_E^2}{16}} = 0.471`, and the critical :math:`t`-value at the 95% level is ``qt(0.975, df=11)`` = 2.2. So the confidence intervals can be calculated to confirm that these are indeed significant effects by calculating their confidence interval.

There is some circular reasoning here: postulate that one or more effects are zero, increase the degrees of freedom by removing those parameters in order to confirm the remaining effects are significant. So some general advice is to first exclude effects which are definitely small, and retain medium size effects in the model until you can confirm they are not-significant.

.. _DOE-COST-vs-factorial-efficiency:
 
Variance of estimates from the COST approach vs factorial approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finally, we end this section on factorials by illustrating their efficiency. Contrast the two cases: COST and the full factorial approach. For this analysis we define the main effect simply as the difference between the high and low value (normally we divide through by 2, but the results still hold). Define the variance of the measured :math:`y` value as :math:`\sigma_y^2`.

	.. image:: ../figures/doe/comparison-of-variances.png
		:align: left
		:width: 750px
		:scale: 70
	
	.. tabularcolumns:: |l|l|
	
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| COST approach                                                            | Fractional factorial approach                                                                                  |
+==========================================================================+================================================================================================================+
| The main effect of :math:`T` is :math:`b_T = y_2 - y_1`                  | The main effect is :math:`b_T = 0.5(y_2 - y_1) + 0.5(y_4 - y_3)`                                               |
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| The variance is :math:`\mathcal{V}(b_T) = \sigma_y^2 + \sigma_y^2`       | The variance is :math:`\mathcal{V}(b_T) = 0.25(\sigma_y^2 + \sigma_y^2) + 0.25(\sigma_y^2 + \sigma_y^2)`       |
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| So :math:`\mathcal{V}(b_T) = 2\sigma_y^2`                                | And :math:`\mathcal{V}(b_T) = \sigma_y^2`                                                                      |
+--------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+

Not only does the factorial experiment estimate the effects with much greater precision (lower variance), but the COST approach cannot estimate the effect of interactions, which is incredibly important, especially as systems approach optima which are on ridges - see the contour plots earlier in this section for an example.

Factorial designs make each experimental observation work twice.
	
Summary so far
~~~~~~~~~~~~~~~~~

-	The factorial experimental design is intentionally constructed so that each factor is independent of the others. There are :math:`2^k` experiments for :math:`k` factors.

	-	This implies the :math:`\mathbf{X}^T\mathbf{X}` matrix is easily constructed (a diagonal matrix, with a value of :math:`2^k` for each diagonal entry).
	-	These coefficients have the lowest variability possible: :math:`(\mathbf{X}^T\mathbf{X})^{-1}S_E^2`
	-	We have uncorrelated estimates of the slope coefficients in the model. That is we can be sure the value of the coefficient is unrelated to the other values. 
	
-	However, we still need to take the usual care in *interpreting* the coefficients. The usual precaution, using the example below, is that the temperature coefficient :math:`b_T` is the effect of a one degree change, holding all other variables constant. That's not possible if :math:`b_{TS}`, the interaction between :math:`T` and :math:`S`, is significant: we cannot hold the :math:`TS` constant while changing :math:`b_T`.
		
	.. math:: 
	
		y = b_0 + b_T x_T + b_S x_S + b_{TS} x_Tx_S + e
	
	So *we cannot interpret the main effects separately from the interaction effects*, when we have significant interaction terms in the model.  Also, if you conclude the interaction term is significant, then you must also include all main factors that make up that interaction term in the model.
		
	For another example, with interpretation of it, please see Box, Hunter, and Hunter (2nd ed), page 185.
	
-	Factorial designs use the collected data much more efficiently than one-at-a-time experimentation. As shown in :ref:`the preceding section <DOE-COST-vs-factorial-efficiency>`, the estimated variance is halved when using a factorial design than from a COST approach.
	
-		A small or zero effect from an :math:`x` variable to the :math:`y` response variable implies the :math:`y` is insensitive to that :math:`x`. This is desirable in some situations - it means we can adjust that :math:`x` without affecting :math:`y`, sometimes said as "*the* :math:`y` *is robust to changes in* :math:`x`".


.. _DOE-blocking-section:

Blocking and confounding for disturbances
===========================================

Characterization of disturbances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

External disturbances will always have an effect on our response variable, :math:`y`. Operators, ambient conditions, physical equipment, lab analyses, and time-dependent effects (catalyst deactivation, fouling), will impact the response. This is why it is crucial to :ref:`randomize <DOE-randomization>` the order of experiments: so that these **unknown, unmeasurable, and uncontrollable** disturbances cannot systematically affect the response.

However, certain disturbances are **known, or controllable, or measurable**. For these cases we perform pairing and blocking. We have already discussed pairing in the univariate section: pairing is when two experiments are run on the same subject and we analyze the differences in the two response values, rather than the actual response values. If the effect of the disturbance has the same magnitude on both experiments, then that disturbance will cancel out when calculating the difference. The magnitude of the disturbance is expected to be different between paired experiments, but is expected to be the same within the two values of the pair.

Blocking is slightly different: blocking is a special way of running the experiment so that the disturbance actually does affect the response, but we construct the experiment so that this effect is not misleading.

Finally, a disturbance can be characterized as a **controlled disturbance**, in which case it isn't a disturbance anymore, as it is held constant for all experiments, and its effect cancels out. But it might be important to investigate  the controlled disturbance, especially if the system is operated later on when this disturbance is at a different level.

.. _DOE-Blocking-and-confounding:

Blocking and confounding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is extremely common for known, or controllable or measurable factors to have an effect on the response. However these disturbance factors might not be of interest to us during the experiment. Cases are:

	-	*Known and measurable, not controlled*: Reactor vessel A is known to achieve a slightly better response, on average, than reactor B. However both reactors must be used to complete the experiments in the short time available.
	
	-	*Known, but not measurable nor controlled*: There is not enough material to perform all :math:`2^3` runs, there is only enough for 4 runs. The impurity in either the first batch A for 4 experiments, or the second batch B for the other 4 runs will be different, and might either increase or decrease the response variable (we don't know the effect it will have).
	
	-	*Known, measurable and controlled*: Reactor vessel A and B have a known, measurable effect on the output, :math:`y`. To control for this effect we all experiments in either reactor A or B, to prevent the reactor effect from :index:`confounding` (confusing) our results.
	
In this section then we will deal with disturbances that are known, but their effect may or may not be measurable. We will also assume that we cannot control that disturbance, but we would like to minimize its effect.

For example, if we don't have enough material for all :math:`2^3` runs, but only enough for 4 runs, the question is how to arrange the 2 sets of 4 runs so that the known, by unmeasurable disturbance from the impurity has the least effect on our results and interpretation of the 3 factors.
	
Our approach is to intentionally *confound*  the effect of the disturbance with an effect that is expected to be the least significant. The :math:`A \times B \times C` interaction term is almost always going to be small for many systems, so we will split the runs that the first 4 are run at the low level of :math:`ABC` and the other four at the high level, as illustrated below. 

Each group of 4 runs is called a *block* and the process of creating these 2 blocks is called :index:`blocking <pair: blocking; experiments>`. The experiments within each block must be run randomly.

.. image:: ../figures/doe/blocking-factorial-3-factors.png
	:align: left
	:scale: 50
	:width: 500px
	
.. tabularcolumns:: |c||c|c|c||c|c|c||c||c|

+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| Experiment| A          | B         |  C         | AB        | AC        | BC        | ABC           | Response, :math:`y`     | 
+===========+============+===========+============+===========+===========+===========+===============+=========================+
| 1         | |-|        | |-|       |  |-|       | |+|       | |+|       | |+|       | |-| (batch 1) | :math:`\widetilde{y}_1` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 2         | |+|        | |-|       |  |-|       | |-|       | |-|       | |+|       | |+| (batch 2) | :math:`\mathring{y}_2`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 3         | |-|        | |+|       |  |-|       | |-|       | |+|       | |-|       | |+| (batch 2) | :math:`\mathring{y}_3`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 4         | |+|        | |+|       |  |-|       | |+|       | |-|       | |-|       | |-| (batch 1) | :math:`\widetilde{y}_4` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 5         | |-|        | |-|       |  |+|       | |+|       | |-|       | |-|       | |+| (batch 2) | :math:`\mathring{y}_5`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 6         | |+|        | |-|       |  |+|       | |-|       | |+|       | |-|       | |-| (batch 1) | :math:`\widetilde{y}_6` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 7         | |-|        | |+|       |  |+|       | |-|       | |-|       | |+|       | |-| (batch 1) | :math:`\widetilde{y}_7` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 8         | |+|        | |+|       |  |+|       | |+|       | |+|       | |+|       | |+| (batch 2) | :math:`\mathring{y}_8`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+


If the raw material has a significant effect on the response variable, then we will not be able to tell whether it was due to the :math:`A \times B \times C` interaction, or due to the raw material, since :math:`\hat{\beta}_{ABC} \rightarrow \underbrace{\text{ABC interaction}}_{\text{expected to be small}} + \text{raw material effect}`.

But the small loss due to this confusion of effects, is the gain that we can still estimate the main effects and two-factor interactions without bias, provided the effect of the disturbance is constant. Let's see how we get this result by denoting :math:`\widetilde{y}_i` as a :math:`y` response from the first batch of materials and let :math:`\mathring{y}_i` denote a response from the second batch.

Using the least squares equations you can show for yourself that:

	.. math::
	
		\hat{\beta}_A    &= -\widetilde{y}_1 + \mathring{y}_2 - \mathring{y}_3 + \widetilde{y}_4 - \mathring{y}_5 + \widetilde{y}_6 - \widetilde{y}_7 + \mathring{y}_8 \\
		\hat{\beta}_B    &= \\
		\hat{\beta}_C    &= \\
		\hat{\beta}_{AB} &= +\widetilde{y}_1 - \mathring{y}_2 - \mathring{y}_3 + \widetilde{y}_4 + \mathring{y}_5 - \widetilde{y}_6 - \widetilde{y}_7 + \mathring{y}_8\\
		\hat{\beta}_{AC} &= \\
		\hat{\beta}_{BC} &= \\
		\hat{\beta}_{ABC} &= \\
		
Imagine now the :math:`y` response was increased by :math:`g` units for the batch 1 experiments, and increased by :math:`h` units for batch 2 experiments. You can prove to yourself that these biases will cancel out for all main effects and all two-factor interactions. The three factor interaction of :math:`\hat{\beta}_{ABC}` will however be heavily confounded.

Another way to view this problem is that the first batch of materials and the second batch of materials can be represented by a new variable, called :math:`D` with value of :math:`D_{-} =` batch 1 and :math:`D_{+} =` batch 2. We will show next that we must consider this new factor to be generated from the other three: **D = ABC**.

We will also address the case when there are more than two blocks in the next section on the :ref:`use of generators <DOE-generators>`. For example, what should we do if we have to run a :math:`2^3` factorial but with only enough material for 2 experiments at a time?

.. DOE-fractional-factorials:

Fractional factorial designs
===========================================

When there are many factors that we have identified as being potentially important, then the :math:`2^k` runs required for a full factorial can quickly become large and too costly to implement.

For example, you are responsible for a cell-culture bioreactor at a pharmaceutical company and there is a drive to minimize the production of an inhibiting  by-product. Variables known to be related with this by-product are: the temperature profile (:math:`T_{-}`: a fast initial ramp then constant temperature or :math:`T_{+}` a slow ramp over time), the dissolved oxygen, the agitation rate, pH, substrate type. These five factors, at two levels, require :math:`2^5 = 32` runs. It would take almost a year to collect the data when each experiment requires 10 days (typically in this industry), and parallel reactors are not available.

Furthermore, we are probably interested in only the 5 main effects and 10 two-factor interactions. The remaining 10 three-factor interactions, 5 four-factor interactions, a single five-factor interaction are likely not too important, at least initially. A full factorial would estimate 32 effects, even if we likely only interested in at most 16 of them (5 + 10 + 1 intercept).

Running a half fraction, or quarter fraction, of the full set will allow us to estimate the main effects and two-factor interactions (2fi) in many cases, at the expense of confounding the higher interactions. For many real systems it is these main effects that are mostly of interest. In this section we show how to construct and analyze these :index:`fractional factorials <pair: fractional factorial; experiments>`, which are tremendously useful when :index:`screening <pair: screening designs; experiments>` many variables - especially for a first-pass at experimenting on a new system.

.. _DOE-half-fractions:

Half fractions
~~~~~~~~~~~~~~~~~~

A half fraction has :math:`\frac{1}{2}2^k = 2^{k-1}` runs. But which runs do we omit? Let's use an example of a :math:`2^3` full factorial. A half-fraction would have 4 runs. Since 4 runs can be represented by a :math:`2^2` factorial, we start by writing down the usual :math:`2^2` factorial for 2 factors (**A** and **B**), then construct the :math:`3^\text{rd}` factor as the product of the first two (**C** = **AB**).


.. tabularcolumns:: |c||c|c|c|

+-----------+------------+-----------+------------+
| Experiment| A          | B         |  C = AB    |
+===========+============+===========+============+
| 1         | |-|        | |-|       |  |+|       |
+-----------+------------+-----------+------------+
| 2         | |+|        | |-|       |  |-|       |
+-----------+------------+-----------+------------+
| 3         | |-|        | |+|       |  |-|       |
+-----------+------------+-----------+------------+
| 4         | |+|        | |+|       |  |+|       |
+-----------+------------+-----------+------------+

So this is our designed experiment for 3 factors, but it only requires 4 experiments as shown by the open points. The experiments given by the solid points are not run.

.. image:: ../figures/doe/half-fraction-in-3-factors.png
	:align: left
	:scale: 35
	:width: 500px

What have we lost by running only half the factorial?  Let's write out the full design and matrix of all interactions, then construct the :math:`\mathbf{X}` matrix for the least squares model.

.. tabularcolumns:: |c||c|c|c||c|c|c|c|c|

=========== ============ =========== ============ ============ ============ ============ ============ ============
Experiment  A            B           C            AB           AC           BC           ABC          Intercept 
=========== ============ =========== ============ ============ ============ ============ ============ ============
 1          |-|          |-|         |+|          |+|          |-|          |-|          |+|          |+|       
 2          |+|          |-|         |-|          |-|          |-|          |+|          |+|          |+|       
 3          |-|          |+|         |-|          |-|          |+|          |-|          |+|          |+|       
 4          |+|          |+|         |+|          |+|          |+|          |+|          |+|          |+|       
=========== ============ =========== ============ ============ ============ ============ ============ ============

Before even constructing the :math:`\mathbf{X}`-matrix, you can see that **A=BC**, and that **B=AC** and **C=AB** (this last association was intentional), and **I=ABC**. The least squares model would be:

.. math::

	\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}\\
	       y_i &=  b_0 + b_A x_A + b_B x_B + b_C x_C + b_{AB} x_{AB} + b_{AC} x_{AC} + b_{BC} x_{BC} + b_{ABC} x_{ABC} + e_i\\
	\begin{bmatrix} y_1\\ y_2\\ y_3 \\ y_4 \end{bmatrix} &=
	\begin{bmatrix} 1 & -1 & -1 & +1 & +1 & -1 & -1 & +1\\ 
					1 & +1 & -1 & -1 & -1 & -1 & +1 & +1\\
					1 & -1 & +1 & -1 & -1 & +1 & -1 & +1\\
					1 & +1 & +1 & +1 & +1 & +1 & +1 & +1
	\end{bmatrix}
	\begin{bmatrix} b_0 \\ b_A \\ b_B \\ b_{C} \\ b_{AB} \\ b_{AC} \\ b_{BC} \\ b_{ABC} \end{bmatrix} + 
	\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \end{bmatrix}

The :math:`\mathbf{X}` matrix is not orthogonal anymore, so the least squares model cannot be solved by inverting the :math:`\mathbf{X}^T\mathbf{X}` matrix. Also note this system is underdetermined as there are more unknowns than equations. But notice that 4 of the columns are the same as the other 4 (we have perfect collinearity between 4 pairs of columns).

We can reformulate the model to obtain independent columns, where there are now 4 equations and 4 unknowns:

.. math::

	\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}\\
	\begin{bmatrix} y_1\\ y_2\\ y_3 \\ y_4 \end{bmatrix} &=
	\begin{bmatrix} 1 & -1 & -1 & +1  \\ 
					1 & +1 & -1 & -1  \\
					1 & -1 & +1 & -1  \\
					1 & +1 & +1 & +1  
	\end{bmatrix}
	\begin{bmatrix} b_0 + b_{ABC} \\ b_A + b_{BC} \\ b_B + b_{AC} \\ b_{C} + b_{AB} \end{bmatrix} + 
	\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \end{bmatrix}

Writing it this way clearly shows how the main effects and two-factor interactions are *confounded*. 

	-	:math:`\widehat{\beta}_0 \rightarrow` **I + ABC**
	
	-	:math:`\widehat{\beta}_A \rightarrow` **A + BC** : this implies :math:`\beta_A` estimates the **A** main effect and the **BC** interaction
	
	-	:math:`\widehat{\beta}_B \rightarrow` **B + AC**
	
	-	:math:`\widehat{\beta}_C \rightarrow` **C + AB**
	
	
We cannot separate the effect of the **BC** interaction from the main effect **A**: the least-squares coefficient is a sum of both these effects. Similarly for the other pairs. This is what we have lost by running a half-fraction.

We introduce the terminology that **A** is an :index:`alias <pair: aliasing; experiments>` for **BC**, similarly that **B** is an alias for **AC**, *etc*, because we cannot separate these aliased effects.

.. This last :math:`k^\text{th}` factor will be confounded with one of the 2-factor interaction???

.. _DOE-generators:

Generators and defining relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculating which main effects and two-factor interactions will be confounded with each other, called the :index:`confounding pattern`, can be tedious for larger values of :math:`k`. Here we introduce an easy way to calculate the confounding pattern.

Recall for the half-fraction of a :math:`2^k` factorial that the first  :math:`k-1` main factors are written down, then the final :math:`k^\text{th}` factor is *generated* from the product of the previous :math:`k-1` factors. Consider the case of a :math:`2^4` half fraction with factors **A**, **B**, **C** and **D**. We write a :math:`2^3` factorial in factors **A**, **B**, and **C**, then set 

.. centered:: **D = ABC**

This is called the *generating relation* for the design. Some rules when working with this notation are that  **A** :math:`\times` **A = I**, **B** :math:`\times` **B = I**, **I** :math:`\times` **I = I**. So for example,  **D** =  **ABC** can by multiplied on both sides by **D** to get **D** :math:`\times` **D** = **ABC** :math:`\times` **D**, which gives **I** = **ABCD**. Another way to get this same result: **ABC** :math:`\times` **D** =  **ABC** :math:`\times` **ABC = AABBCC = I I I = I = ABCD**.


.. index::
	pair: generating relationship; experiments
	pair: defining relationship; experiments
	
This last part, **I = ABCD**, is called the *defining relation* for this design. The defining relationship is the product of all generator combinations, then simplified to be written as **I = ....**. In this case there is just one generator, so the defining relationship is the generator. We will discuss this again later.

.. centered:: **I = ABCD**

Now the effects which are aliased (confounded) with each other can be found quickly by multiplying the effect by the defining relationship. For example, if we wanted to know what the main effect **A** would be confounded with in this :math:`2^{4-1}` half fraction we should multiply **A** by the defining relationship as in 

.. centered:: **A** :math:`\times` **I = A** :math:`\times` **ABCD = BCD**

indicating that **A** is aliased with the 3-factor interaction **BCD**.  What is the aliasing for these effects:

	-	What is main effect **B** aliased with? (*Answer*: **ACD**)
		
	-	What is the 2fi **AC** aliased with? (*Answer*: **BD**)

**Another example**: 

	Returning back to the :math:`2^{3-1}` half fraction in the :ref:`previous section <DOE-half-fractions>`, use the defining relation to verify the aliasing of main-effects and two-factor interactions derived earlier by hand.

		-	What is the defining relationship?
		
		-	Aliasing for **A**? (*Answer*: **BC**)
	
		-	Aliasing for **B**? (*Answer*: **AC**)
		
		-	Aliasing for **C**? (*Answer*: **AB**: recall this is how we generated that half fraction)
		
		-	Aliasing for the intercept term, **I**? (*Answer*: **ABC**)
	
**Yet another example**: 

	Which aliasing (confounding) would occur if you decided for a :math:`2^{4-1}` design to generate the half-fraction by using the 2-factor interaction term **AC** rather than the 3-factor interaction term **ABC**.

		-	What is the defining relationship?
		-	Aliasing for **A**? (*Answer*: **CD**)
		-	Aliasing for **B**? (*Answer*: **ABCD**)
		-	Aliasing for **C**? (*Answer*: **AD**)
		
	Why is this a poorer choice than using **D = ABC** to generate the half-fraction? *Answer*: the main effects of **A** and **C** are aliased with 2fi which could be important. Had we generated the design with the usual 3fi term, **ABC**, the main effects would only be aliased with three-factor interactions (3fi).

Generating the complementary half-fraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say that a half fraction for a :math:`2^3` factorial was run. The defining relation was **I = ABC**, so factor **C** was aliased with the 2fi **AB**. Now if these 4 runs produce promising results, you might seek approval to complete the factorial and run the other half fraction. This will remove the aliasing when you now analyze all 8 data points together. The defining relation for the complementary half-fraction is **I = -ABC**, or equivalently **IC = C = -AB**.

Let's return to the table in the :ref:`previous section <DOE-half-fractions>` and generate the other 4 runs:

.. tabularcolumns:: |c||c|c|c|

+-----------+------------+-----------+------------+
| Experiment| A          | B         |  C = |-| AB|
+===========+============+===========+============+
| 5         | |-|        | |-|       |  |-|       |
+-----------+------------+-----------+------------+
| 6         | |+|        | |-|       |  |+|       |
+-----------+------------+-----------+------------+
| 7         | |-|        | |+|       |  |+|       |
+-----------+------------+-----------+------------+
| 8         | |+|        | |+|       |  |-|       |
+-----------+------------+-----------+------------+

After running these 4 experiments (in random order of course) we have a complete set of 8 runs. Now the main effects and two-factor interactions can be calculated without aliasing because we are back to the usual full factorial in :math:`2^3` runs.

So we see that we can always complete our half-fraction by creating a complementary fraction. This complimentary fraction is found by flipping the sign on the generating factor. For example, changing the sign from **C** to **-C**. See the illustration.

.. image:: ../figures/doe/complementary-half-fraction-in-3-factors.png
	:align: left
	:scale: 35
	:width: 500px
	:alt:	complementary-half-fraction-in-3-factors.svg

.. _DOE-Generators-for-blocking:

Generators: to determine confounding due to blocking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generators are also great for determining the blocking pattern. Recall the case described earlier where we only had enough material to run two sets of 4 experiments to complete our :math:`2^3` full factorial. An unintended disturbance could have been introduced by running the first half-fraction on different materials to the second half-fraction. We :ref:`intentionally decided <DOE-Blocking-and-confounding>` to confound the two blocks of experiments with the 3-factor interaction, **ABC**. So if there is an effect due to the blocks (i.e. the raw materials) or if there truly was a 3-factor interaction, it will show up as a significant coefficient for :math:`b_{ABC}`.

So *in general* when running a :math:`2^k` factorial in two blocks you should create a :math:`2^{k-1}` half fraction to run as the first block, and then run the other block on the complementary half-fraction. You should always confound your block effect on the highest possible interaction term. Then block 1 runs will have that highest interaction term with all positive signs, and block 2 will have all negative signs for that interaction.

Here are the block generators you can use when splitting a :math:`2^k` factorial in 2 blocks:

.. tabularcolumns:: |c||c|c|c|

+-----------+-----------------+-------------------------------+-------------------------------+
| :math:`k` | Design          | Block 1 defining relation     | Block 2 defining relation     |
+===========+=================+===============================+===============================+
| 3         | :math:`2^{3-1}` | **I=ABC**                     | **I=-ABC**                    |
+-----------+-----------------+-------------------------------+-------------------------------+
| 4         | :math:`2^{4-1}` | **I=ABCD**                    | **I=-ABCD**                   |
+-----------+-----------------+-------------------------------+-------------------------------+
| 5         | :math:`2^{5-1}` | **I=ABCDE**                   | **I=-ABCDE**                  |
+-----------+-----------------+-------------------------------+-------------------------------+

.. My notes on this section are not clear:  how to clearly illustrate that A will be aliased with DE?  And how is it obvious that this aliasing with DE (the block effect contrast) is problematic?  Perhaps use an example where the blocks are biased and factor A was never really significant.

	What if the block effect has more than two levels?  For example, for a :math:`2^3` factorial, there is only enough material for 2 experiments. So :math:`g=4` groups of experiments will be run. How do we assign these groups to minimize confounding?  Find the smallest full factorial that can accommodate these :math:`g` groups, in this case a :math:`2^2` factorial. Write out this factorial and assign the groups accordingly:

	.. tabularcolumns:: |c||c|c|c|
                       
	+-------------------+-------------+-------------+
	| Lot of material   | D           | E           |
	+===================+=============+=============+
	|  1                | |-|         | |-|         | 
	+-------------------+-------------+-------------+
	|  2                | |+|         | |-|         |
	+-------------------+-------------+-------------+
	|  3                | |-|         | |+|         |
	+-------------------+-------------+-------------+
	|  4                | |+|         | |+|         |
	+-------------------+-------------+-------------+

	It is as if we are introducing two new variables into our :math:`2^3` factorial: in addition to the factors **A**, **B** and **C**, we also have factors **D** and **E** corresponding to the different groups of materials. For example, when we use lot 3, then :math:`D = -1` and :math:`E = +1`.

	How do we assign **D** and **E** so that the confounding is minimized?  We might be tempted to use **D = ABC** and then assign **E** to **BC**, an interaction that we are not concerned 
	about. The generators are then **I = ABCD** and **I = BCE** respectively. The *defining relationship* is found from all possible products of all generators. In this case there are just two generators, so the defining relationship, which is the product of all generators is: **I = ABCD = BCE = ADE**.

	Now let's calculate the aliasing structure:

		-	A: aliased with A + BCD + ABCE + DE
		-	Fix this: **B x ADE = ABDE**
		-	Fix this: **C x ADE = ACDE**
		-	Fix this: **AB x ADE = BDE**
		-	Fix this: **AC x ADE = CDE**
		-	Fix this: **BC x ADE = ABCDE**
		-	Fix this: **ABC x ADE = BCDE**

	This indicates the main effect of **A** is aliased with the two-factor interaction **DE**. Why is this problematic?
	
	The other effects are confounded with three-factor interactions

	A better choice of generators is **D = AB** and **E = AC** (or use the other two-factor interaction). Now calculate:

		-	The defining relationship = 
	
			.. I = ABD = ACE = ABD x ACE = BCDE

		-	Aliasing for:

			* **A**
			* **B**
			* **C**
			* **AB**
			* **AC**
			* **BC**
			* **ABC**  
			
	Rather than determine the best aliasing structure by trial-and-error, refer to a table, such as Table 5A.1 (page 221) in the second edition of Box, Hunter and Hunter to read which generators should be assigned to which blocks to minimize confounding. For this example, you would use the row in the table with :math:`k=3`, block size = 2 (two experiments per block). Another example is given in this same reference, page 219, that describes how a 64 run experiments is broken down into 8 blocks of 8 runs.

.. Don't try this example: it's still too early.
	For example, for a :math:`2^3` factorial, the block size is 3 experiments when there is only enough material for 3 experiments. So two experiments will be run with one lot of material, then 3 runs with another lot, and then the final 3 runs.

	Start by rounding down to the closest power of 2, which is :math:`p = 2^1 = 2` in this case. Create a full factorial with :math:`2^p` runs. Assign the blocks according to the different runs in this factorial:

	.. tabularcolumns:: |c||c|c|c|
	                          D              E   
	+-------------------+-------------+-------------+
	| Batch of material | :math:`B_1` | :math:`B_2` |
	+===================+=============+=============+
	|  1                | |-|         | |-|         | 
	+-------------------+-------------+-------------+
	|  2                | |+|         | |-|         |
	+-------------------+-------------+-------------+
	|  3                | |-|         | |+|         |
	+-------------------+-------------+-------------+
	|  4 (ignored)      | |+|         | |+|         |
	+-------------------+-------------+-------------+

	B_1: I=ABCD;  
	B_2: I=BCE

	overall generator: ABCD.BCE = ADE
	A: DE
	B: ABDE
	C: ACDE
	
.. _DOE-highly-fractionated-designs:

Highly fractionated designs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running a half-fraction of a :math:`2^k` factorial is not the only way to reduce the number of runs. In general, we can run a :math:`2^{k-p}` fractional factorial. A system with :math:`2^{k-1}` is called a *half fraction*, while a :math:`2^{k-2}` design is a quarter fraction.

The purpose of a fractionated design is to reduce the number of experiments when your budget or time does not allow you to complete a full factorial. Also, the full factorial is often not required, especially when :math:`k` is greater than about 4, since the higher-order interaction terms are almost always insignificant. If we have a budget for 8 experiments, then we could run a:

	- :math:`2^3` full factorial on **3 factors**
	- :math:`2^{4-1}` half fraction, investigating **4 factors**
	- :math:`2^{5-2}` quarter fraction looking at the effects of **5 factors**
	- :math:`2^{6-3}` fractional factorial with **6 factors**, or a
	- :math:`2^{7-4}` fractional factorial with **7 factors**.
	
At the early stages of our work we might prefer to screen many factors, :math:`k`, accepting a very complex confounding pattern, because we are uncertain which factors actually affect our response. Later, as we are optimizing our process, particularly as we approach an optimum, then the 2 factor and perhaps 3-factor interactions are more dominant. So investigating and calculating these effects more accurately and more precisely becomes important and we have to use full factorials. But by then we have hopefully identified much fewer factors :math:`k` than what we started off with. 

So this section is concerned with the trade-offs as we go from a full factorial with :math:`2^k` runs to a highly fractionated factorial, :math:`2^{k-p}`.

*Example 1* 

	You have identified 7 factors that affect your response. 
	
	-	What is the smallest number of runs that can be performed to screen for the main effects?   
	
		A :math:`2^{7-p}` fractional factorial would have 64 (:math:`p=1`), 32 (:math:`p=2`), 16 (:math:`p=3`), or 8 (:math:`p=4`) runs. The last case is the smallest number that can be used to estimate the intercept and 7 main effects (8 data points, 8 unknowns).

	-	What would be the generators and defining relation for this :math:`2^{7-4} = 8` run experiment and what is the aliasing structure?
	
		#.	Assign **A**, **B**, ... **G** as the 7 factor names. Since there are 8 runs, start by writing out the first 3 factors, **A**, **B**, and **C**, in the usual full factorial layout for these :math:`2^3 = 8` runs. 
	
		#.	Next we assign the remaining factors to the highest-possible interaction terms from these 3 factors. Since we've already assigned **A**, **B** and **C** we only have to assign the other 4 factors, **D**, **E**, **F**, and **G**. Pick the 4 interaction terms that we are least interested in. In this particular example, we have to use all (saturate) the interaction terms.
	
			*	**D = AB**
			*	**E = AC**
			*	**F = BC**
			*	**G = ABC**

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
		
			Record the experimental results for :math:`y` in the last column.
		
		#.	So the 4 generators we used are **I = ABD**, **I = ACE**, **I = BCF** and **I = ABCG**. The generators such as **ABD** and **ACE** are called *"words"*. 
		
		#.	The *defining relationship* is a sequence of :index:`words <pair: words; experiments>` which are all equal to **I**. The :index:`defining relation <pair: defining relationship; experiments>` is found from the product of all possible generator combinations, and then simplified to be written as **I = ....**. 
	
			The rule is that a :math:`2^{k-p}` factorial design is produced by :math:`p` generators and has a defining relationship of :math:`2^p` words. So in this example there are :math:`2^4 = 16` words in our defining relation. They are:

			-	Intercept:	**I** [1]
			-	Generators:	 **I = ABD = ACE = BCF = ABCG** [2,3,4,5]
			-	Two combinations of generators:	**I = BDCE = ACDF = CDG = ABEF = BEG = AFG** [6 to 11]
			-	Three combinations of generators:	**I = DEF = ADEG = CEFG = BDFG** [12 to 15]
			-	Four combinations of generators: **I = ABCDEFG** [16]

			The 16 words in the defining relationship are written as: **I = ABD = ACE = BCF = ABCG = BCDE = ACDF = CDG = ABEF = BEG = AFG = DEF = ADEG = CEFG = BDFG = ABCDEFG**. The shortest length word has 3 letters.

		#.	The aliasing or confounding pattern for any desired effect can be calculated by multiplying the defining relationship by that effect. Let's take **A** as an example, below, and multiply it by the 16 words in the defining relation:

			**AI = BD = CE = ABCF = BCG = ABDCE = CDF = ACDG = BEF = ABEG = FG = ADEF = DEG = ACEFG = ABDFG = BCDEFG**
		
			:math:`\widehat{\beta}_A \rightarrow` A + **BD** + **CE** + ABCF + BCG + ABCDE + CDF + ACDG + BEF + ABEG + **FG** + ADEF + DEG + ACEFG + ABDFG + BCDEFG.

			So by performing 8 runs instead of the full :math:`2^7`, we confound the main effects with a large number of 2-factor and higher interaction terms. In particular, the main effect of **A** is confounded here with the **BD**, **CE** and **FG** two-factor interactions. Any 3 and higher-order interaction confounding is usually not of interest.
		
			Listed below are all the aliases for the main effects, reporting only the two-factor interactions. The bold sections indicate the confounding that was intentionally created when we set up the design.

			-	:math:`\widehat{\beta}_0` = ABCDEFG
			-	:math:`\widehat{\beta}_{\mathbf{A}} \rightarrow` A + BD + CE + FG
			-	:math:`\widehat{\beta}_{\mathbf{B}} \rightarrow` B + AD + CF + EG 
			-	:math:`\widehat{\beta}_{\mathbf{C}} \rightarrow` C + AE + BF + DG
			-	:math:`\widehat{\beta}_{\mathbf{D}} \rightarrow` **D + AB** + CG + EF
			-	:math:`\widehat{\beta}_{\mathbf{E}} \rightarrow` **E + AC** + BG + DF
			-	:math:`\widehat{\beta}_{\mathbf{F}} \rightarrow` **F + BC** + AG + DE
			-	:math:`\widehat{\beta}_{\mathbf{G}} \rightarrow` G + CD + BE + AF

		#.	If this confounding pattern is not suitable, for example, if you expect interaction **BG** to be important but also main effect **E**, then choose a different set of generators before running the experiment. Or more simply, reassign your variables (temperature, pressure, pH, agitation, *etc*) to different letters of **A**, **B**, *etc* to obtain a more desirable confounding relationship.

*Example 2*

	From a cause-and-effect analysis, flowcharts, brainstorming session, expert opinions, operator opinions, and information from suppliers you might determine that there are 8 factors that could impact an important response variable. Rather than running :math:`2^8 = 256` experiments, you can run :math:`2^{8-4} = 16` experiments. (Note: you cannot have fewer experiments: :math:`2^{8-5} = 8` runs are not sufficient to estimate the intercept and 8 main effects).

	So the :math:`2^{8-4}` factorial will have :math:`2^4` runs. Assign the first 4 factors to **A**, **B**, **C** and **D** in the usual full factorial manner to create these 16 runs, then assign the remaining 4 factors to the three-factor interactions:

	-	**E** = **ABC**, or **I = ABCE**
	-	**F** = **ABD**, or **I = ABDF**
	-	**G** = **BCD**, or **I = BCDG**
	-	**H** = **ACD**, or **I = ACDH**
	
	So by multiplying all combinations of the words we obtain the complete defining relationship.
	
	-	Two at a time: **I = ABCE** :math:`\times` **ABDF = CDEF**, **I = ABCE** :math:`\times` **BCDG = ADEG**, *etc*
	-	Three at a time: **I = ABCE** :math:`\times` **ABDF** :math:`\times` **BCDG = BEFG**, *etc*
	-	Four at a time: **I = ABCE** :math:`\times` **ABDF** :math:`\times` **BCDG** :math:`\times` **ACDH = ABCDEFGH**. 
	
	The defining relationship is **I = ABCE = ABDF = BCDG = ACDH = CDEF = ADEG = ... = ABCDEFGH**, and the shortest word has 4 characters.

	Next we can calculate all aliases of the main effects. So for **A = IA = BCE = BDF = ABCDG = CDH = ACDEF = DEG = ... = BCDEFGH**, indicating that A will be confounded with **BCE + BDF + ABCDG + ...**. In this example none of the main effects have been aliased with two-factor interactions. The aliasing is only with 3-factor and higher interaction terms.
	
.. rubric:: Summary

#.	It is tedious and error prone to calculate the aliasing structure by hand, so computer software is useful in this case.  For example, for the :math:`2^{7-4}` system can be created in  R by first loading the ``BHH2`` package, then using the command ``ffDesMatrix(k=7, gen=list(c(4,1,2), c(5,1,3), c(6,2,3), c(7,1,2,3)))``. See the `R tutorial <http://connectmv.com/tutorials/r-tutorial/>`_ for more details.

#.	The choice of generators is not unique and other choices may lead to a different, more preferable confounding pattern. But it is often easier to use the letters **A, B, C**, *etc*, then just reassign the factors to the letters to achieve the "least-worst" confounding.

#.	In general, a :math:`2^{k-p}` factorial design is produced by :math:`p` generators and has a defining relationship of :math:`2^p` words.

There is a quick way to calculate if main effects will be confounded with 2fi or 3fi without having to go through the process shown in this section. This is described next when we look at design resolution.

Design resolution
~~~~~~~~~~~~~~~~~~~

The :index:`resolution <pair: design resolution; experiments>` of a design is given by the length of the shortest word in the defining relation. We normally write the resolution as a subscript to the factorial design. Some examples:

	#.	The :math:`2^{7-4}` *example 1* in the previous section had  the shortest word of 3 characters, so this would be called a :math:`2^{7-4}_\text{III}` design. Main effects were confounded with 2-factor interactions.
	#.	The :math:`2^{8-5}` *example 2* had as the shortest word length of 4 characters, so this would be a :math:`2^{8-5}_\text{IV}` design. Main effects were confounded with 3-factor interactions.
	#.	Finally, imagine the case of :math:`2^{5-1}`, in other words a half-fraction design. The first four factors are written in the standard factorial, but the fifth factor is generated from **E = ABCD**. So its defining relation is  **I = ABCDE**, where the shortest word is 5 characters - it is a :math:`2^{5-1}_{\text{V}}` design. You can verify for yourself that main effects will be confounded with 4-factor interactions in this design.
	
You can consider the resolution of a design to be an indication of how clearly the effects can be separated in a design. The higher the resolution, the lower the degree of confounding, which is valuable. Within reason, always aim for a higher resolution design given your experimental budget, but also accept a lower resolution, at least initially, in order to test for more factors. We will discuss this further in the section on :ref:`screening designs <DOE-saturated-screening-designs>`.

You can interpret the resolution index as follows: let main effects = 1, two-factor interactions = 2, three-factor interactions = 3, *etc*. Then subtract this number from the resolution index to show how that effect is aliased. Consider a resolution IV design, since :math:`4-1=3`, it indicates that main effects are aliased with 3fi, but not with two-factor interactions; and :math:`4-2 = 2` indicates that 2fi are aliased with each other. Here is a summary:

Resolution III designs 
	-	Are excellent for initial screening: to separate out the important factors from the many potential factors
	-	Main effects are not confounded with each other 
	-	Main effects are aliased with two-factor interactions (:math:`3 - 1 = 2`)
	-	Two-factor interactions are aliased with each other (:math:`3 - 2 = 1`)

Resolution IV designs
	-	Most useful for characterizing (learning about and understanding) a system, since:
	-	Main effects are not confounded with each other 
	-	Main effects are not aliased with two-factor interactions either (:math:`4-1=3`)
	-	Two-factor interactions are still aliased with each other though (:math:`4-2=2`)
	
Resolution V designs 
	-	For optimizing a process, learning about complex effects, and developing high-accuracy models, since:
	-	Main effects are not confounded with each other
	-	Main effects are not aliased with two-factor interactions 
	-	Two-factor interactions are not aliased with each other either
	-	But two-factor interactions are aliased with three-factor interactions (:math:`5-2=3`)
	
The above guidance about using resolution IV and V designs for characterization and optimization is general - there are many cases where a satisfactory optimization can be performed with a resolution IV experiment.

Use this table to visualize the trade-off between design resolution, number of factors (:math:`k`), the number of runs required, and the aliasing pattern.

.. _DOE_design_trade_off_BHH_272:

.. image:: ../figures/doe/DOE-trade-off-table.png
	:alt:	../figures/doe/DOE-trade-off-table.svg
	:scale: 80
	:width: 550px
	:align: left

Adapted from Box, Hunter and Hunter (2nd edition, p 272), and (1st edition, p 410).

.. _DOE-saturated-screening-designs:

Saturated designs for screening
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: you don't really described at all what a saturated design is

A :index:`saturated design <pair: saturated design; experiments>` can be likened to a well trained doctor asking you a few, but very specific, questions to identify a disease or problem. On the other hand, if you sit there just tell the doctor all your symptoms, you may or may not get an accurate diagnosis. Designed experiments, like visiting this doctor, shortens the time required to identify the major effects in a system, and to do so accurately.

Saturated designs are most suited for screening, and should always be run when you are investigating a new system with many factors. These designs are usually of resolution III and allow you to determine the main effects with the smallest number of experiments.

For example, a :math:`2^{7-4}_{\text{III}}` factorial introduced in the section on :ref:`highly fractionated designs <DOE-highly-fractionated-designs>` will screen 7 factors in 8 experiments. Once you have run the 8 experiments you can quickly tell which subset of the 7 factors are actually important, and spend the rest of your budget on clearly understanding these effects and their interactions. Let's see how by continuing the previous example, repeated again below with the corresponding values of :math:`y`.

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

where :math:`\mathbf{b} = [b_0, b_A, b_B, b_C, b_D, b_E, b_F, b_G]`. The matrix :math:`\mathbf{X}` is derived from the preceding table, but with an added column of 1's for the intercept term. Notice that the :math:`\mathbf{X}^T\mathbf{X}` matrix will be diagonal. It is straightforward to calculate the  solution vector (by hand!) as :math:`\mathbf{b} = [70.7, -2.3, 0.1, -2.8, -0.4, 0.5, -0.4, -1.7]`. 

How do you assess which main effects are important?  There are eight data points and eight parameters, so there are no degrees of freedom and the residuals are all zero. In this case you have to use a :ref:`Pareto plot <DOE-Pareto-plot>`, which requires that your variables have been suitably scaled in order to judge importance of the main effects. The Pareto plot would be given as shown below, and as usual, it does not include the intercept term.

.. image:: ../figures/doe/pareto-plot.png
	:align: left
	:width: 800px
	:scale: 37
	:alt:	../figures/doe/pareto-plot.R
	
Significant effects would be **A**, **C** and **G**. The next largest effect, **E**, though fairly small, could be due to the main effect **E** or due to the **AC** interaction, because recall the confounding pattern for main effect was :math:`\widehat{\beta}_{\mathbf{E}} \rightarrow` **E + AC + BG + DF**.

The factor **B** is definitely not important to the response variable in this system and can be excluded in future experiments, as could **F** and **D**. Future experiments should focus on the **A**, **C** and **G** factors and their interactions. We show how to use these existing experiments, but add a few new ones in the next section on design foldover and by understanding projectivity.

A side note on screening designs is a mention of :index:`Plackett and Burman designs <pair: Plackett-Burman designs; experiments>`. These designs can sometimes be of greater use than a highly fractionated design. A fractional factorial must have :math:`2^{k-p}` runs, for integers :math:`k` and :math:`p`: i.e. either :math:`4, 8, 16, 32, 64, 128, \ldots` runs. Plackett-Burman designs are screening designs that can be run in any multiple of 4 greater or equal to 12:, i.e. :math:`12, 16, 20, 24, \ldots` runs. The Box, Hunter, and Hunter book has more information in Chapter 7, but another interesting paper on these topic is by Box and Bisgaard: "`What can you find out from 12 experimental runs? <http://cqpi.engr.wisc.edu/system/files/r088.pdf>`_", which shows how to screen for 11 factors in 12 experiments.

Design foldover
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Experiments are not a one-shot operation. They are almost always sequential, as we learn more and more about our system. Once the first screening experiments are complete there will always be additional questions. In this section we consider two common questions that arise after a fraction has been run. 

*Dealias a single main effect* (switch sign of one factor)

In the previous example we had a :math:`2^{7-4}_{\text{III}}` system with generators **D=AB**, **E=AC**, **F=BC**, and **G=ABC**. Effect **C** was the largest effect. But we cannot be sure it was large due to factor **C** alone - it might have been one of the interactions it is aliased with. We would like to do some additional experiments so that **C** becomes unconfounded with any two-factor interactions (currently it is confounded with **AE** + **BF** + **DG**). 

Run another 8 experiments, but this time just change the sign of **C** to **-C**. Now the generators are **D=AB**, **E=-AC**, **F=-BC**, and **G=-ABC**. This is just another :math:`2^{7-4}_{\text{III}}` design. You can calculate the aliasing pattern, but in particular the aliasing pattern for effect **C**  will be :math:`\widehat{\beta}_{\mathbf{C}} \rightarrow` **C** - **AE** - **BF** - **DG**. So it is now estimated without any confounding from two-factor interactions when putting all 16 runs together. Also, any two-factor interactions involving **C** are removed from the other main effects. For example, confounding due to **CE** will be removed from main effect **A**, and **CF** will be removed from main effect **B**. 

**In general**: switching the sign of one factor will de-alias that factor's main effect, and all its associated two-factor interactions. In the above example, we will have an unconfounded estimate of **C** and unconfounded estimates of the 2-factor interactions involving **C**, i.e. **AC**, **BC**, **CD**, **CE**, **CF** and **CG** after analyzing the 8 + 8 experiments together.

*Increase design resolution* (switching all signs)

One can improve the aliasing structure of a design when switching all the signs of all factors from the first fraction.

In the :math:`2^{7-4}_\text{III}` example, we ran 8 experiments. If we now run another 8 experiments with all the signs switched, then these 8+8 experiments would be equivalent to a :math:`2^{7-3}_\text{IV}` design. This resolution IV design means that all the main effects can now be estimated without confounding from any two-factor interactions. However, the two-factor interactions are still confounded with themselves. 

This is a good strategy in general: run the first fraction of runs to assess the main effects; it serves as a good checkpoint as well to provide feedback to colleagues and get approval/budget to run the next set of experiments. Then if we perform another set of runs we know that we are doing them in a way that captures the most additional information, and with the least confounding.

Projectivity 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A final observation for this section is how fractional factorials will collapse down to a full factorial under certain conditions.

Consider the diagram here, where a half fraction in factors **A**, **B** and **C** was run (4 experiments) at the closed points. 

.. figure:: ../figures/doe/projectivity-of-a-half-fraction-in-3-factors.png
	:align: center
	:width: 800px
	:scale: 50
	:alt:	../figures/doe/projectivity-of-a-half-fraction-in-3-factors.svg

On analyzing the data, the experimenter discovers that factor **C** does not actually have an impact on response :math:`y`. This means the **C** dimension could have been removed from the experiment, and is illustrated by projecting the **A** and **B** factors forward, removing factor **C**. Notice that this is now a full factorial in factors **A** and **B**. The same situation would hold if either factor **B** or factor **A** were found to be unimportant. Furthermore if two factors are found to be unimportant, then this corresponds to 2 replicate experiments in 1 factor.

This projectivity of factorials holds in general for a larger number of factors. The above example, actually a :math:`2^{3-1}_\text{III}` experiment, was a case of projectivity = 2. In general, projectivity = :math:`P` = resolution :math:`-` 1. So if you have a resolution IV fractional factorial, then it has projectivity = :math:`P = 4 - 1`, implying that it contains a full factorial in 3 factors. So a :math:`2^{6-2}_\text{IV}` (16 runs) system with 6 factors, contains an embedded full factorial using a combination of any 3 factors; if any 3 factors were found unimportant, then a replicated full factorial exists in the remaining 3 factors.


.. TODO: point out how blocking can be visualized as projectivity: in a 2 factor system (A and B) you have enough material only for 2 runs at a time. So you block on the AB interaction. But you can visualize that as a 3-factor factorial now, but run as a half-fraction, i.e. a 2^3_{III} design (show the cube with open and closed circles). This design has projectivity of 2 = 3-1, meaning a full 2^2 factorial is embedded in the design. If factor C (the blocking variable) has no effect on y, then you recover your full 2^2 factorial. That's why we typically block on the highest interaction possible.

.. _DOE-RSM:

Response surface methods
==========================


.. Add this somewhere appropriate: http://xkcd.com/605/   .... on extrapolation

The purpose of :index:`response surface methods <pair: response surface methods; experiments>` (RSM) is to optimize a process or system. RSM is a way to explore the effect of operating conditions (the factors) on the response variable, :math:`y`. As we map out the unknown response surface of :math:`y`, we move our process as close as possible towards the optimum, taking into account any constraints. 

Initially, when we are far away from the optimum, we will use factorial experiments. As we approach the optimum then these factorials are replaced with better designs that more closely approximate conditions at the optimum.

.. TODO: RSM overview figure here with COST approach superimposed

Notice how it is a *sequential* approach. RSM then is a tool the describes how we should run these sequential sets of experiments. At the start of this :ref:`section on designed experiments <DOE-COST-approach>` we showed how sequential experimentation (COST) leads to sub-optimal solutions. Why are we advocating sequential experimentation now?   The difference is that here we use sequential experiments by changing *multiple factors simultaneously*, and not changing only one factor at a time.

.. rubric:: RSM concept for a single variable: COST approach

We will however first consider just the effect of a single factor, :math:`x_1` as it relates to our response, :math:`y`. This is to illustrate the general response surface process.

.. figure:: ../figures/doe/steepest-ascent-univariately-corrected.png
	:alt: steepest-ascent-univariately.svg
	:align: center
	:scale: 70
	:width: 750px

We start at the point marked :math:`i=0` as our initial baseline (cp=center point). We run a 2-level experiment, above and below this baseline at :math:`-1` and :math:`+1`, in coded units of :math:`x_1`, and obtain the corresponding response values of :math:`y_{0,-}` and :math:`y_{0,+}`. From this we can estimate a best-fit straight line and move in the direction that increases :math:`y`. The sloping tangential line, also called the *path of steepest ascent*. Make a move of step-size = :math:`\gamma_1` units along :math:`x_1` and measure the response, recorded as :math:`y_1`. The response variable increased, so we keep going in this direction.

Make another step-size, this time of :math:`\gamma_2` units in the direction that increases :math:`y`. We measure the response, :math:`y_2`, and are still increasing. Encouraged by this, we take another step of size :math:`\gamma_3`. The step-sizes, :math:`\gamma_i` should be of a size that is big enough to cause a change in the response in a reasonable number of experiments, but not so big as to miss an optimum.

Our next value of :math:`y_3` is about the same size as :math:`y_2`, indicating that we have plateaued. At this point we can take some exploratory steps and refit the tangential line (which now has a slope in the opposite direction). Or we can just use the accumulated points :math:`y = [y_{0-},\,\, y_{0+},\,\, y_1,\,\, y_2,\,\, y_3]` and their corresponding :math:`x`-values to fit a non-linear curve. Either way, we can then estimate a different step-size :math:`\gamma_4` that will bring us closer to the optimum.

This univariate example is in fact what experimenters do when using the :ref:`COST approach <DOE-COST-approach>` described earlier. We have:

* exploratory steps of different sizes towards an optimum
* refit the model once we plateau
* repeat

This approach works well if there really is only a single factor that affects the response. But with most systems there are multiple factors that affect the response. We show next how the exact same idea is used, only we change multiple variables at a time to find the optimum on the response surface.

Response surface optimization via a 2-variable system example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
	\hat{y} &= 385.6 + 55 x_T + 134 x_S - 3.75 x_T x_S 
		
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
	:scale: 80
	:width: 750px
	

To improve our profit in the optimal way we move along our estimated model's surface, in the direction of steepest ascent. This direction is found by taking partial derivatives of the model function, ignoring the interaction term, since it is so small.

.. math::
		\dfrac{\partial \hat{y}}{\partial x_T} = b_T = 55  \qquad \qquad & \dfrac{\partial \hat{y}}{\partial x_S} = b_S = 134
		
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
*	:math:`S_5 = S_\text{baseline} + \Delta x_{S,\text{actual}} = 0.75 + 0.6` = 1.36`` g/L
	
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
| 9         | 339 K      | 2.17 g/L  | |+|        | |-|          |  725       |
+-----------+------------+-----------+------------+--------------+------------+
| 10        | 331 K      | 1.77 g/L  | |-|        | |+|          |  620       |
+-----------+------------+-----------+------------+--------------+------------+
| 11        | 339 K      | 2.17 g/L  | |+|        | |+|          |  642       |
+-----------+------------+-----------+------------+--------------+------------+

This time we have deciding to slightly smaller ranges in the factorial :math:`\Delta_T = 8 = (339 - 331)` K and :math:`\Delta_S = 0.4 = (2.17 - 1.77)` g/L so that we can move more slowly along the surface.

.. figure:: ../figures/doe/RSM-base-case-combined.*
	:align: center
	:width: 900px
	:scale: 100
	:alt:	RSM-base-case.py

A least squares model from the 4 factorial points (experiments 8, 9, 10, 11, run in random order), seems to show that the promising direction now is to increase temperature but decrease the substrate concentration.

.. math::
		\hat{y} &= b_0 + b_T x_T + b_S x_S + b_{TS} x_T x_S \\
		\hat{y} &= 670 + 13 x_T - 39 x_S - 2.4 x_T x_S
		
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

We will not go into too much detail about :index:`central composite designs`, other than to show what they look like for the case of 2 and 3 variables. These designs take an existing orthogonal factorial and augment it will axial points. This is great, because we can start off with an ordinary factorial and always come back later to add the terms to account for nonlinearity.

The :index:`axial points <pair: axial points; experiments>` are placed :math:`\sqrt{2} = 1.4` coded units away from the center for a 2 factor system, and 1.7 units away for a :math:`k=3` factor system. Rules for higher numbers of factors, and the reasoning behind the 1.4 and 1.7 unit step size can be found, for example in the textbook by Box, Hunter and Hunter.

.. image:: ../figures/doe/central-composite-design.png
	:align: left
	:width: 900px
	:scale: 50
	:alt:	central-composite-design.svg

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

The final step in the response surface methodology is to plot this model's contour plot and predict where to run the next few experiments. As the solid contour lines in the illustration show, we should run our next experiments roughly at :math:`T` = 343K and :math:`S` = 1.65 g/L where the expected profit is around $735. We get those two values by eye-balling the solid contour lines, drawn from the above non-linear model. You could find this point analytically as well. 

This is not exactly where the true process optimum is, but it is pretty close to it (the temperature of :math:`T` = 343K is just a little lower that where the true optimum is.

This example has demonstrated how powerful response surface methods are. A minimal number of experiments has quickly converged onto the true, unknown process optimum. We achieved this by building successive least squares models that approximate the underlying surface. Those least squares models are built using the tools of fractional and full factorials and basic optimization theory, to climb the hill of steepest ascent.

The general approach for response surface modelling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#.	Start at your baseline conditions and identify the main factors based on physics of the process, operator input, expert opinion input, and intuition. Also be aware of any constraints, especially for safe process operation. Perform factorial experiments (full or fractional factorials), completely randomized. Use the results from the experiment to estimate a linear model of the system:

	.. math::
	
		\hat{y} = b_0 + b_Ax_A + b_B x_B + b_C x_C  \ldots + b_{AB}x_Ax_B + b_{AC} x_A x_C + \ldots

#.	The main effects are usually significantly larger than the two-factor interactions, so these higher interaction terms can be safely ignored. Any main effects that are not significant may be dropped for future iterations.

#.	Use the model to estimate the path of steepest ascent (or descent if minimizing :math:`y`):

	.. math::	
	
		\dfrac{\partial \hat{y}}{\partial x_1} = b_1 & \qquad\qquad \dfrac{\partial \hat{y}}{\partial x_2} = b_2 \qquad \ldots
		
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

	Response surface methods consider optimization of a single outcome, or response variable, called :math:`y`. In many instances we are interested in just a single response, but more often we are interested in the a multi-objective response, i.e. there are trade-offs. For example we can achieve a higher production rate, but it is at the expense of more energy. 

	One way to balance all competing objectives is to rephrase the :math:`y` variable in terms of total costs, or better still, net profit. This makes calculating the :math:`y` value more complex, as we have to know the various costs and their relative weightings to calculate the profit. Now you have a single :math:`y` to work with.
	
	Another way is to superimpose the response surfaces of two or more :math:`y`-variables. This is tremendously helpful when discussing and evaluating alternate operating points, because plant managers and operators can then visually see the trade-offs.
	
.. TODO: figure here showing RSM trade-offs: two contours superimposed

.. rubric:: Summary

#.	In the previous sections we used factorials and fractional factorials for screening the important factors. When we move to process optimization,  we are assuming that we have already identified the important variables. In fact, we might find that variables that were previously important, appear unimportant as we approach the optimum. Conversely, variables that might have been dropped out earlier, become important at the optimum.

#.	Response surface methods assume the variables we adjust are continuous. Binary variables (yes/no, catalyst A or B) are handled by fixing them at one or the other value, and then performing the optimization conditional on those selected values. It is always worth investigating the alternative values once the optimum has been reached.

#.	Many software packages provide tools that help with an RSM study. If you would like to use R in your work, we highly recommend the ``rsm`` package in R. You can read more about the package from `this article <http://www.jstatsoft.org/v32/i07>`_ in the Journal of Statistical Software (**32**, October 2009).

.. rubric:: References

*	A good book on response surface methods is by Myers and Montgomery: "`Response Surface Methodology: Process and product optimization using designed experiments <http://en.wikipedia.org/wiki/Special:BookSources/0470174463#Canada>`_".
*	A review paper citing many examples of RSM in the chemical and engineering industries is by William Hill and William Hunter: "`A Review of Response Surface Methodology: A Literature Survey <http://www.jstor.org/pss/1266632>`_", *Technometrics*, **8**, 571-590 , 1966. 
*	An excellent overview with worked examples is given by Davies in Chapter 11 of the revised second edition of "`The design and analysis of industrial experiments <http://en.wikipedia.org/wiki/Special:BookSources/0582460530#Canada>`_"

.. _DOE-EVOP:

Evolutionary operation
===========================

Evolutionary operation (EVOP) is a tool to help maintain a full-scale process at its optimum. Since the process is not constant, the optimum will gradually move away from its current operating point. Chemical processes drift due to things such as heat-exchanger fouling, build-up inside reactors and tubing, catalyst deactivation, and other slowly varying disturbances in the system.

EVOP is an iterative hunt for the process optimum by making small perturbations to the system. Similar to response surface methods, once every iteration is completed, the process is moved towards the optimum. The model used to determine the move direction and levels of next operation are from full or fractional factorials, or designs that estimate curvature, like the central composite design.

Because every experimental run is a run that is expected to produce saleable product (we don't want off-specification product), the range over which each factor is varied must be small. Replicate runs are also made to separate the signal from noise, because the optimum region is usually flat.

Some examples of the success of EVOP and a review paper are in these readings:

- George Box: `Evolutionary Operation: A Method for Increasing Industrial Productivity <http://www.jstor.org/pss/2985505>`_", *Journal of the Royal Statistical Society* (Applied Statistics), **6**, 81 - 101, 1957.
- William G. Hunter and J. R. Kittrell, "`Evolutionary Operation: A Review <http://www.jstor.org/pss/1266686>`_", *Technometrics*, **8**, 389-397, 1966.

Current day examples of EVOP do not appear in the scientific literature much, because this methodology is now so well established.


..	Robust process operation
	============================

	* Process robustness lecture: http://ocw.mit.edu/OcwWeb/Mechanical-Engineering/2-830JSpring-2008/VideoLectures/index.htm
	* BHH(v2) has some discussion about this


General approach for experimentation in industry
================================================

.. Reference: p 251 of BHH2, and personal experience

We complete this section with some guidance for experimentation in general. The main point is that experiments are never run in one go. You will always have more questions after the first round. Box, Hunter and Hunter provide two pieces of guidance on this:

	#.	The best time to run an experiment is after the experiment. You will discover things from the previous experiment that you wish you had considered the first time around.
	#.	For the above reason, do not spend more than 20% to 25% of your time and budget on your first group of experiments. Keep some time aside to add more experiments and learn more about the system.

The **first phase** is usually *screening*. Screening designs are used when developing new products and tremendous uncertainty exists; or sometimes when a system is operating so poorly that one receives the go-ahead to manipulate the operating conditions wide enough to potentially upset the process, but learn from it.

	-	The ranges for each factor may also be uncertain; this is a perfect opportunity to identify suitable ranges for each factor.
	
	-	You also learn how to run the experiment on this system, as the operating protocol isn't always certain ahead of time. It is advisable to choose your first experiment to be the center point, since the first experiment will often "fail" for a variety of reasons (you discover that you need more equipment midway, you realize the protocol isn't sufficient, *etc*). Since the center point is not required to analyze the data, it worth using that first run to learn about your system. If successful though, that center point run can be included in the least squares model.
	
	-	Include as many factors into as few runs as possible. Use a saturated, resolution III design, or a Plackett and Burham design.
	
	-	Main effects will be extremely confounded, but this is a preliminary investigation to isolate the important effects.
	
The **second phase** is to add *sequential experiments* to the previous experiments.

	-	Use the concept of foldover: switching the sign of the factor of interest to learn more about a single factor, or switch all signs to increase the design's resolution.
	-	If you had a prior screening experiment, use the concept of projectivity in the important factors to limit the number of additional experiments required.
	-	Move to quarter and half-fractions of higher resolution, to better understand the main effects and 2-factor interactions.
	
The **third phase** is to start *optimizing* by exploring the response surface using the important variables discovered in the prior phases.

	-	Use full or half-fraction factorials to estimate the direction of steepest ascent or descent.
	-	Once you reach the optimum, then second order effects and curvature must be added to assess the direction of the optimum.
	
The **fourth phase** is to *maintain the process optimum* using the concepts of evolutionary operation (EVOP). 

	-	An EVOP program should always be in place on a process, because raw materials change, fouling and catalyst deactivation take place, and other slow moving disturbances have an effect. You should be always hunting for the process optimum.


Extended topics related to designed experiments
==========================================================================

.. p 414 Esbensen
.. Objectives of Trygg p 2 and p5 of wikipedia article

This section is just an overview  of some interesting topics, together with references to guide you to more information.

Experiments with mistakes, missing values, or belatedly discovered constraints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. BHH1: p 503

Many real experiments do not go smoothly. Once the experimenter has established their :math:`-1` and :math:`+1` levels for each variable, they back that out to real units. For example, if temperature was scaled as :math:`T = \dfrac{T_\text{actual} - 450\text{K}}{\text{25K}}`, then :math:`T = -1` corresponds to 425K and :math:`T= +1` corresponds to 475K.

But if the operator mistakenly sets the temperature to :math:`T_\text{actual} = 465K`, then it doesn't quite reach the +1 level required. This is not a wasted experiment. Simply code this as :math:`T = \dfrac{465 - 450}{25} = 0.6`, and enter that value in the least squares model for matrix :math:`\mathbf{X}`. Then proceed to calculate the model parameters using the standard least squares equations. Note that the columns in the X-matrix will not be orthogonal anymore, so :math:`\mathbf{X}^T\mathbf{X}` will not be a diagonal matrix, but it will be almost diagonal.

Similarly, it might be discovered that temperature cannot be set to 475K when the other factor, for example concentration, is also at its high level. This might be due to physical or safety constraints. On the other hand, :math:`T=475K` can be used when concentration is at its low level. This case is the same as described above: set the temperature to the closest possible value for that experiment, and then analyze the data using a least squares model. The case when the constraint is known ahead of time is :ref:`dealt with later on <DOE-handling-constraints>`, but in this case, the constraint was discovered just as the run was to be performed.

Also see the section on :ref:`optimal designs <DOE-optimial-designs>` for how one can add one or more additional experiments to fix an existing bad set of experiments.

The other case that happens occasionally is that samples are lost, or the final response value is missing for some reason. Not everything is lost: recall the main effects for a full :math:`2^k` factorial are estimated :math:`k` times at :ref:`each combination of the factors <DOE-COST-vs-factorial-efficiency>`. 

If one or more experiments have missing :math:`y` values, you can still estimate these main effects, and sometimes the interaction parameters by hand. Furthermore, analyzing the data in a least squares model will be an undetermined system: more unknowns than equations. You could choose to drop out higher-order interaction terms to reduce the equations to a square system: as many unknowns as equations. Then proceed to analyze the results from the least squares model as usual. There are actually slightly more sophisticated ways of dealing with this problem, as described by Norman Draper in "`Missing Values in Response Surface Designs <http://www.jstor.org/pss/1266729>`_", *Technometrics*, **3**, 389-398, 1961.

The above discussion illustrates clearly our preference for using the least squares model: whether the experimental design was executed accurately or not: the least squares model always works, whereas the :ref:`short cut tools <DOE-two-level-factorials>` developed for perfectly executed experiments will fail.


.. _DOE-handling-constraints:

Handling of constraints
~~~~~~~~~~~~~~~~~~~~~~~~~

Most engineering systems have limits of performance, either by design or from a safety standpoint. It is also common that optimum production levels are found close to these constraints. The factorials we use in our experiments must, by necessity, span a wide range of operation so that we see systematic change in our response variables, and not merely measure noise. These large ranges that we choose for the factors often hit up again constraints. 

A simple bioreactor example for 2 factors is shown: at high temperatures and high substrate concentrations we risk activating a different, undesirable side-reaction. The shaded region represents the constraint where we may not operate. We could for example replace the :math:`(T_{+}, C_{+})` experiment with two others, and then analyze these 5 runs using least squares.

.. figure:: ../figures/doe/two-factors-with-constraint.png
	:align: center
	:width: 500px
	:scale: 45
	:alt:	../figures/doe/two-factors-with-constraint.svg

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

* St. John and Draper: "`D-Optimality for Regression Designs: A Review <http://www.jstor.org/pss/1267995>`_", *Technometrics*, **17**, 15-, 1975.

.. _DOE-mixture-designs:

Mixture designs
~~~~~~~~~~~~~~~~~~~~~~~~~

The area of mixture designs is incredibly important for optimizing recipes, particularly in the area of fine chemicals, pharmaceuticals, food manufacturing, and polymer processing. Like factorial designs, there are screening and optimization designs for mixtures also.

A mixture design is required when the factors being varied add up to 100% to form a mixture. Then these factors cannot be adjusted in an independent, factorial-like manner, since their proportion in the recipe must add to 100%: :math:`\sum_i x_i = 1`. These designs result in triangular patterns (called simplexes). The experimental points at the 3 vertices are for pure components :math:`x_A, x_B`, or :math:`x_C`. Points along the sides represent a 2-component mixture, and points in the interior represent a 3-component blend.

.. figure:: ../figures/doe/mixture-design.png
	:align: center
	:width: 500px
	:scale: 100
	:alt:	../figures/doe/mixture-design.svg

In the above figure on the right, the shaded region represents a constraint that cannot be operated in. A D-optimal algorithm must then be used to select experiments in the remaining region. The example is for finding the lowest cost mixture for a fruit punch, while still meeting certain taste requirements (e.g. watermelon juice is cheap, but has little taste). The constraint represents a region where the acidity is too high. 

.. Clean this up and make it clearer

	You may not always need a mixture design for recipe experiments if you are only changing a small amount of ingredient, and your factors include only a subset of the ingredients. For example, you are investigating the properties of a new polymer blend, made with ingredients:

		-	**A**: 25% or 30%
		-	**B**: 1% or 2%
		-	**C** and **D** make up the rest of the recipe in a consistent 40/60 ratio
		-	**T**: is the temperature at which the blend is extruded, either high or low
	
	In this case **A** and **B** are the factors being investigated in the recipe, in addition to temperature **T**. The results from a full factorial in factors **A**, **B** and **T** (i.e. a :math:`2^3` factorial) would give similar results to a mixture design at high temperature and low temperature, but 


