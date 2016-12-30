.. TODO
	
	=====
	~~~~~
	^^^^^
	-----

	Linear regression in Python:

	>>> from scipy.stats import linregress
	>>> slope, intercept, r, prob, stderr = linregress(a, b)

.. Plots to draw

	Cylinder temp and pressure and humidity

.. TO ADD LATER ON

	Transformation: more systematic discussion; see BHH2, p 322
	Linear models: go into details also how to calculate confidence intervals and prediction intervals for MLR
	Show the spinning plane for highly correlated X's
	Include the influecePlot in the notes (PDF): you have it in the slides, but not here

	Be clearer on what a CI for the MLR or OLS terms mean (i.e. it shows when a term is necessary; can be used to free up DOF)  Show examples and how to interpret them.


.. Case studies to consider

	Cigarette: http://www.amstat.org/publications/jse/v2n1/datasets.mcintyre.html
	Car sales: http://www.amstat.org/publications/jse/v16n3/datasets.kuiper.html

.. Enrichment topics

	Ill-conditioning
	Non-linear least squares
	Generalized linear models

.. Outline

	Correlation
	Covariance
	Least squares:
		- minimizing errors as the objective function
		- solution to the minimization problem: grid search vs analytically
		- breakdown (allocation) of variance
		- R2 derivation
		- conf. interval for coefficients
		- conf. interval for predictions
		- interpretation of results from software packages
		- assessment of residuals (interpretation)
			- residuals in sequence
			- residuals vs y-hat
			- residuals vs y
			- residuals vs x
		- leverage, outliers and influence
		- matrix approach
			- introduce notation
			- resolve the optimization problem
			- interpretation of coefficients
			- errors on the coefficients

Least squares modelling in context
====================================

This section begins a new part: we start considering more than one variable at a time. However, you will see the tools of confidence intervals and visualization from the previous sections coming into play so that we can interpret our least squares models both analytically and visually.

The following sections, on design and analysis of experiments and latent variable models, will build on the least squares model we learn about here.

Usage examples
~~~~~~~~~~~~~~~

.. index::
	pair: usage examples; least squares
	
.. youtube:: https://www.youtube.com/watch?v=RW_8yKbMzUA&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=17

The material in this section is used whenever you need to interpret and quantify the relationship between two or more variables.

	-	*Colleague*: How is the yield from our lactic acid batch fermentation related to the purity of the sucrose substrate?
	
		*You*: The yield can be predicted from sucrose purity with an error of plus/minus 8%
		
		*Colleague*: And how about the relationship between yield and glucose purity?
		
		*You*: Over the range of our historical data, there is no discernible relationship.
		
	-	*Engineer 1*: The theoretical equation for the melt index is non-linearly related to the viscosity
	
		*Engineer 2*: The linear model does not show any evidence of that, but the model's prediction ability does improve slightly when we use a non-linear transformation in the least squares model.
		
	-	*HR manager*: We use a least squares regression model to graduate personnel through our pay grades. The model is a function of education level and  number of years of experience. What do the model coefficients mean?

What you will be able to do after this section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: ../figures/mindmaps/least-squares-section-mapping.png
  :width: 900px
  :scale: 90
  :alt: Map of the least squares section

.. Notes
	Specifically, we cover the technical topics of:
	#. Covariance
	#. Correlation
	#. The relationship between correlation, covariance and variance
	#. Introduction to bivariate least squares (the linear relationship between 2 variables).
	#. We will also discuss the short-sighted idiom that is often repeated: *correlation does not imply causation* and complete it by understanding that *correlation is a necessary, but not sufficient, condition for causality*. We will take a look at an example of correlation and understand that it is impossible to imply causality without doing intentional experimentation.
	
.. _LS_references:

References and readings
====================================

.. index::
	pair: references and readings; least squares
	
This section is only a simple review of the least squares model. More details may be found in these references.

-	**Recommended**: John Fox, *Applied Regression Analysis and Generalized Linear Models*, Sage.

-	**Recommended**: N.R. Draper and H. Smith, *Applied Regression Analysis*, Wiley.

-	Box, Hunter and Hunter, *Statistics for Experimenters*, selected portions of Chapter 10 (2nd edition), Wiley.

-	Hogg and Ledolter, *Applied Statistics for Engineers and Physical Scientists*, Prentice Hall.

-	Montgomery and Runger, *Applied Statistics and Probability for Engineers*, Wiley.

..	Efron, Hastie, Johnstone and Tibshirani, `Least Angle Regression <http://www.jstor.org/stable/3448465>`_, *The Annals of Statistics*, **32**, p 407-451, 2004.

..	S. Chatterjee and A. S. Hadi, `Influential Observations, High Leverage Points, and Outliers in Linear Regression <http://www.jstor.org/stable/2245477>`_, *Statistical Science*, **1** (3), 379-416, 1986.

.. G.E.P. Box, `Use and Abuse of Regression <http://www.jstor.org/stable/1266635>`_, *Technometrics*, **8** (4), 625-629, 1966.

