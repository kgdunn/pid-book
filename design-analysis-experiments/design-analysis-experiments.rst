.. TODO

	Website with DOE problems and R code: http://www.stat.ualberta.ca/~wiens/stat368/stat368.html
	DOE Textbook: http://users.stat.umn.edu/~gary/Book.html
	
	Mention that experiments don't have to be done in order. Can be done in parallel (e.g. growing plants).
	Give code on generating random order 

	=====
	~~~~~
	^^^^^
	-----
	
	RSM:
	 * pay attention to subsequent models. How do the slope coefficients changes from model to model? What are we learning about the system and how it changes in different operating regions
	
	* RSM: emphasize 25% range by giving an example: some students thought this was the half-range, so used 50% range actually.
	
	* RSM: emphasize that star points must be added to support a quadratic. Cannot just add quadratic terms to the model.
	
	
	From JMP, Bradley Jones, Linked-In, 11 February 2013 : 
	
	 I will repost my material on design evaluation below but first I would like to talk about the Design Diagnostics report in JMP. The report provides 4 scalar design summary measures. These all have to do with either the variance of predicted responses or the variance of parameter estimates. These scalars are the D Efficiency, G Efficiency, A Efficiency and Average Variance of Prediction. 

	I will explain what each of these are but first, I need to define some terms. Suppose I have 3 factors F1, F2 and F3. Suppose that I want to fit a model containing the main effects and two-factor interactions of these factors. The factor settings matrix, F, has rows that are the values of F1, F2 and F3 (in vector notation [F1 F2 F3]. Note that JMP always scales continuous factors to lie on the interval between -1 and 1. 

	When you expand the above row to model form you get a vector x that looks like this: 
	[1 F1 F2 F3 F1*F2 F1*F3 F2*F3]. The 1 is for the intercept of the model and the last three terms are the two factor interactions. 

	The model matrix, X, is composed of all the rows of the factor settings matrix expanded to model form. I call p the number of columns in X and n the number of rows in X. 

	D-Efficiency is defined as 100(det(X'X)^(1/p))/n 
	The D-Efficiency is one omnibus measure of how precise the estimates of the model coefficients are compared to the theoretically perfect design (which might not exist). 

	The prediction variance relative to the unknown value of the error variance for a given row, x, is x*inverse(X'X)*x' 

	Let maxV be the maximum variance of prediction inside the region of the factors. For the "perfect design" maxV would be p. The G-efficiency is defined as 
	100p/maxV. It is a measure of how bad the worst case prediction variance is. 

	Call the sum of the diagonal elements of inverse(X'X), sV. For the "perfect design" sV would be p/n 
	The A-efficiency is 100*n*sV/p. It is another omnibus measure of the precision of the parameter estimates. 

	The Average Variance of Prediction is the the prediction variance integrated over the region of the factors divided by the volume of the region. This is a more balanced measure of the prediction variance than G-Efficiency. 

	None of these "one number summaries" is adequate by itself. The other Design Evaluation tools in JMP provide much more information. 

	Next I will re-post my comments from the other thread about design evaluation.
	
	The question is how to use the Design Evaluation outputs in JMP to compare designs. 

	Variance and bias are two fundamental concepts in statistics. In the analysis of designed experiments you look at the estimates of the parameters and make predictions of the response at various factor settings. Whether these estimates and predictions are useful depends on the magnitude of the variance and bias. 

	The uncertainty (noise or variance) in parameter estimates or response predictions is transmitted from noise (random variation) in the measurements and noise in the system or process under investigation. Good designs transmit less noise to the parameters and response predictions than poor designs. The Prediction Variance Profile, Fraction of the Design Space Plot andPrediction Variance Surface show the effect of noise on the response predictions. The Power Analysis and Variance Inflation Factors (VIF) measure the effect of noise on the parameter estimates. Personally, I use the Fraction of Design Space Plot for comparing prediction variance of two designs. For comparing the variance of parameter estimates, I put the Variance Inflation Factors reports for the two designs side-by-side. You want the VIFs to be as close to 1 (perfect) as possible. But VIFs are not scale invariant, so I just compare alternatives rather than making rules on the absolute numbers. This is especially important in mixture design and designs with restrictions on the allowable settings of the factors. 

	The Alias Matrix and the Color Map On Correlations address bias. In DOE a common source pf bias is that the model you use to analyze the data is missing a term. For example in the orthogonal half fraction of the 2x2x2 design, the main effects are each biased by a different two-factor interaction if that interaction effect is not negligible. In JMP you can define a set of Alias Terms that while they are not in your model, you think they might turn out to be active. Each element in the Alias Matrix shows the fraction by which an active alias term will bias the given term in the model. For example, in the design I mention above, the entries in the Alias Matrix are all either 0, 1 or -1. That means that if the true main effect of a factor is 5 and the aliasing two-factor interaction's effect is 4, then the expected parameter estimate will be 5+4 = 9. So, you would think that the main effect was much bigger than it actually is. Obviously, you would like the entries of the Alias Matrix to be zero or as small as possible. The Color Map On Correlations is a cell plot where each cell shows the absolute value of the correlation between two design (or model term) columns. If you are using a white-to-black color scale, you want everything off the diagonal of this plot to be as nearly white as possible. 

	None of these outputs is a one number summary. Choosing between design alternatives represents making trade-offs between the number of runs you are willing to perform, the number of terms in the model you wish to estimate and the number of additional terms that you think might be active but are not willing to spend the extra runs to estimate. Usually increasing the number of runs will lower the variance and can also lower the bias. However, more runs generally cost more.
	
	
	---------------
	
	From NIST: Rotatability: A design is rotatable if the variance of the predicted response at any point x depends only on the distance of x from the design center point. A design with this property can be rotated around its center point without changing the prediction variance at x. Note: Rotatability is a desirable property for response surface designs (i.e. quadratic model designs). https://www.itl.nist.gov/div898/handbook/pri/section7/pri7.htm#Rotatability
	
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
	
	On Yates (factorial) analysis: https://www.itl.nist.gov/div898/handbook/eda/section3/eda35i.htm
	
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
	
	DOE is a way to bring an out of control process back into control. See the comment by Vining (top right, p152) in the  Bisgaard articles https://dx.doi.org/10.1080/08982110701826721
	
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

.. note:: Coursera students

	If you are using this chapter with the `Coursera MOOC <https://yint.org/experiments>`_ (massive open online course), then we wish to welcome you and want to let you know that this book is generally part of a larger set of notes. The cross-references in this chapter will point you to other parts, where background knowledge is provided.
	
	.. youtube:: https://www.youtube.com/watch?v=9Sljs2064u4&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=31
	
	This chapter was written for engineers originally, but you will see the examples are very general and can be applied to any other systems.
	
	You can safely skip over the section on :ref:`DOE_expts_with_single_variable`; that section is not covered in the MOOC. You can also initially skip the section on :ref:`DOE_learning_about_systems`, but make sure you come back and read it.

.. AU: In this chapter, page references to section links are shown as "page 279". I have been using "p. 279" in previous chapters. To be consistent, please either change the format in previous chapters to "page", or change the ones in this chapter to "p.".

.. index::
   see: Design of experiments; experiments

Design and analysis of experiments in context
===============================================

.. youtube:: https://www.youtube.com/watch?v=iYsR93LpHi8&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=32

This chapter will take a totally different approach to learning about and understanding systems in general, not only (chemical) engineering systems. The systems we could apply this to could be as straightforward as growing plants or perfecting your favourite recipe at home. Or they may be as complex as the entire production line in a large factory producing multiple products and shipping them to customers.


In order to learn about a system, we have to disturb it and change it. This is to ensure cause and effect. If we do not intentionally change the system, we are only guessing, or using our intuition. To disturb the system, we change several factors. When we make these changes, we say that we have "run an experiment". 

In this chapter we learn the best way to intentionally disturb the system to learn more about it. We will use some of the tools of :ref:`least squares modelling <SECTION-least-squares-modelling>`, :ref:`visualization <SECTION-data-visualization>` and :ref:`univariate statistics <SECTION-univariate-review>` that were described in earlier chapters. Where necessary, we will refer back to those earlier sections.

.. In the next section, on latent variables, we will take a look at learning more about our systems when the condition of independence between variables, required for designed experiments, is not met. But for now we can use least squares and simpler tools, as designed experiments are intentionally orthogonal (independent).

Terminology
===========

.. youtube:: https://www.youtube.com/watch?v=0vzsc2daVKU&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=33

The area of designed experiments uses specific terminology.

Every experiment has these two components: 

.. AU: It would be nice to italicize the individual terminology words (outcome, factor, objective, etc.) to make them stand out. But italicizing doesn't seem to be compatible with :index:. Is there a way to make it work?

.. index::
	pair: outcome; experiments
	pair: response; experiments
	pair: factor; experiments
	pair: variable; experiments

#.  An *outcome*: the result or the *response* from an experiment.
#.  One or more factors: a *factor* is the thing you can change to influence the outcome. Factors are also called *variables*.

An important aspect about the outcome is that it is always measurable--in some way. In other words, after you finish the experiment, you must have some measurement. 

Let's use an example of growing plants. The outcome of growing a plant might be the height of the plant, or the average width of the leaves, or the number of flowers on the plant. These are numeric measurements, also called quantitative measurements. Qualitative measurements are also possible. For example, perhaps the outcome is the colour of the flower: light red, red, or dark red. A qualitative outcome might also be a description of what happened, for example, *pass* or *fail*.

.. index::
	 pair: objective; experiments

An experiment can have an *objective*, which combines an outcome and the need to adjust that outcome. For example, you may want to maximize the height of the plant. Most often you want to maximize or minimize the outcome as your objective. Sometimes, though, you want the outcome to be *the same* even though you are changing factors. For example, you might want to change a recipe for your favourite pastry to be gluten-free but keep the taste the same as the original recipe. Your outcome is taste, and your objective is "the same".

Every experiment always has an outcome. Every experiment does not have to have an objective, but usually we have an objective in our mind.

Another term we will use is factors. In the plant example, you could have changed three factors:

#.	The amount of water that you give the plant each day
#.	The amount of fertilizer that you give the plant each week
#.	The type of soil you use, A or B

.. index::
	pair: categorical factor; experiments

All experiments must have at least one factor that is changed. We distinguish between two types of factors: *numeric factors* and *categorical factors*. 

Numeric factors are quantified by measuring, such as giving 15 mL of water or 30 mL of water to the plant each day. An important point about numerical variables is that there is some order to them. 15 mL of water is less than 30 mL or water. Another name for this type of factor is a quantitative factor.

Categorical factors usually take on a limited number of values. For example, soil type A or soil type B could be used to grow the plants. Categorical variables have no implicit ordering. You could have switched the names of soil A and soil B around. Categorical variables and qualitative variables can be used as synonyms.

Most categorical variables can be converted to continuous variables, with some careful thought. For example: no water vs some water (categorical) can be converted to 0 mL and 40 mL (now it is numeric). In the case of soil A vs soil B it might be that soil A contains a higher level of nutrients in total than soil B, so a numeric version of this factor could be measured as nutrient load.

If you were working in the area of marketing, you might try three different colours of background in your advertising poster. Those 3 colours are categorical variables in the context of the experiment. 

Most experiments will have both numeric and categorical factors.

.. index:: 
	pair: run; experiments
	
When we perform an experiment, we call it a run. If we perform eight experiments, we can say "there are eight runs" in the set of experiments.

