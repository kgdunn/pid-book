.. To add

	* see p 295 of Devore here for in-class example
	* Put "paired" tests under the main section of testing for differences	
	* Explain more clearly when a paired test is required vs a test of differences
	* Chi-squared goodness of fit test for normality; also a way to introduce the chi-squared test
	
Univariate data analysis in context
====================================

This section is an introduction to the area of data analysis. We cover concepts from univariate data analysis, specifically the concepts shown in the pictorial outline below. This section is only a *review of these concepts*; for a more comprehensive treatment, please consult an introductory statistics textbook (see the recommended readings further down).

Usage examples
==============

.. index::
	pair: usage examples; univariate data

The material in this section is used whenever you want to learn more about a single variable in your data set:

	- *Co-worker*: Here are the yields from a batch system for the last 3 years (1256 data points)
		
		- what sort of distribution do the data have?
		- yesterday our yield was less than 50%, what are the chances of that happening under typical conditions?
		
	- *Yourself*: We have historical failure rate data of the pumps in a section of the process. What is the probability that 3 pumps will fail this month?
	
	- *Manager*: does reactor 1 have better final product purity, on average, than reactor 2?
	
	- *Colleague*: what does the 95% confidence interval for the density of our powder ingredient really mean?

References and readings
=======================

.. index::
	pair: references and readings; univariate data

Any standard statistics text book will cover the topics from this part of the book in much greater depth than these notes. Some that you might refer to:
	
#. **Recommended**: Box, Hunter and Hunter, *Statistics for Experimenters*, Chapter 2.
#. Hodges and Lehmann, *Basic Concepts of Probability and Statistics*
#. Hogg and Ledolter, *Engineering Statistics*
#. Montgomery and Runger, *Applied Statistics and Probability for Engineers*

What we will cover
==================

.. image:: ../figures/mindmaps/univariate-section-mapping.png
  :align: center
  :scale: 92

.. Concepts
.. ========
.. 
.. Concepts that you must be familiar with by the end of this section:
.. 
.. .. tabularcolumns:: LLL
.. 
.. .. csv-table:: 
..    :widths: 10, 10, 10
.. 
.. 	, independence, outliers
.. 	"frequency histogram", probability, variation
.. 	"cumulative distribution", median, MAD
.. 	population, sample, error
.. 	"Central limit theorem", parameter, statistic
.. 	"confidence interval", outlier, "paired test"

	
.. _univariate-about-variability:

Variability
===========

Life is pretty boring without :index:`variability`, and this book, and almost all the field of statistics would be unnecessary if things did not naturally vary.

.. image:: ../figures/concepts/variation/variation-none.png
		:scale: 60
		:align: center
		
Fortunately, we have plenty of variability in the recorded data from our processes and systems:

	-	Raw material properties are not constant
	
	-	Unknown sources, often called "*error*" (note that the word :index:`error <single: error; statistical>` in statistics does not have the usual negative connotation from English). These errors are all sources of variation which our imperfect knowledge of physics cannot account for.
	
		.. image:: ../figures/concepts/variation/variation-some.png
			:scale: 50
			:align: center
			
	-	Measurement and sampling variability: sensor drift, spikes, noise, recalibration shifts, errors in our sample analysis.

		.. image:: ../figures/concepts/variation/variation-more.png
			:scale: 50
			:align: center

	-	Production disturbances:
	
		- external conditions change (ambient temperature, humidity)
		- pieces of plant equipment break down, wear out and are replaced
		
		.. image:: ../figures/concepts/variation/variation-spikes.png
			:scale: 50
			:align: center
	
	-	:index:`Feedback control <single: feedback control>` systems introduce variability in your process, in order to reduce variability in another part of the process (think of what a :ref:`feedback control system <univariate_feedback_and_variability>` does)
	
		..	See Marlin textbook, p 880 and p222 for illustrations and concepts
		
	-	Operating staff: introduce variability into a process in feedback manner (i.e. they react to process upsets) or in a feedforward manner, for example, to preemptively act on the process to counteract a known disturbance.
	
	
All this variability, although a good opportunity to keep us process engineers employed, comes at a price as described next.
	
The high cost of variability in your final product
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: variability; cost of
	
**Assertion**
	Customers expect both uniformity and low cost when they buy your product. Variability defeats both objectives. 
	
Three broad outcomes are possible when you sell a highly variable product:

#. The customer may be totally unable to use your product for the intended purpose. Imagine a food ingredient such as fresh milk, or a polymer with viscosity that is too high, or a motor oil with unsuitable properties that causes engine failure.

#. Your product leads to poor performance.  The user must compensate for the poor properties through additional cost: more energy will be required to work with a polymer whose melting point is higher than expected, longer reaction times will be required if the catalyst purity is not at specification.

#. Your brand is diminished: your products, even though acceptable will be considered with suspicion in the future.

	An extreme example was the food poisoning and deaths that occurred due to the listeriosis outbreak at Maple Leaf Foods, Canada in 2008. The bacterial count in food products is always non-zero, however the established tolerance limits were exceeded during this outbreak.
	
	Another example was the inadvertent acceleration that occurred in some Toyota car models in 2010. It is still uncertain whether this was manufacturer error or driver error.

In addition to the risk of decreasing your market share (see the above 3 points), variability in your product also has these costs:

.. index::
	single: inspection costs

#.	Inspection costs: to mitigate the above risks you must inspect your product before you ship it to your customers. It is prohibitively expensive and inefficient to test every product (known as "*inspecting quality into your product*"). A production line with low variability on the other hand, does not require us to inspect every product downstream of production.

	The pharmaceutical industry is well known to be inefficient in this respect, with terms such as "100% inspection" and even "200% inspection".

	.. index::
		single: off-specification product
	
#.	Off-specification products: must be reworked, disposed of, or sold at a loss or much lower profit. These costs are ultimately passed onto your customers, costing you money.
 
Note: the above discussion assumes that you are able to quantify product quality with one or more univariate quality metrics and that these metrics are independent of each other. Quality is almost always a multivariate attribute of the product. We will :ref:`discuss the use of multivariate methods <SECTION_latent_variable_modelling>` to judge product quality later.

The high cost of variability in your raw materials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: Add a feedforward arrow to the diagram

.. index::
	single: variability; in raw materials
	
.. index::
	single: raw material variability
	
.. _univariate_feedback_and_variability:

Turning the above discussion around, with you on the receiving end of a highly variable raw material:

-	If you do not implement any sort of process control system, then any variability in these raw materials is manifest as variability in your final product. This usually shows up in proportion: higher variability in the inputs results in higher variability in the product quality.

	.. image:: ../figures/concepts/variation/feedback-control-variance-reduction-reduced.png
		:align: center
		:scale: 50

-	Even if you do take feedback or feed-forward corrective control: you have to incur additional cost, since you have to process materials that are not to specification: this will require energy and/or time, reducing your profit due to the supplier's raw material variability.

	*Note*: Feedback control around a given set point can be seen as *introducing* additional variation into a process to counteract other sources of variation (called *disturbances* in the process control lingo). This is done with the hope of reducing the output variability. 

Dealing with variability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So, how do we make progress despite this variability?  This whole book, and all of statistical data analysis, is about variability:

- in the :ref:`data visualization section <SECTION-data-visualization>` we gave some hints how to plot graphics that **show the variability** in our process clearly
- in this section we learn how to **quantify variability** and then **compare variability**
- later we consider how to :ref:`construct monitoring charts <SECTION-process-monitoring>` to **track variability**
- in the section on :ref:`least squares modelling <SECTION-least-squares-modelling>` we learn how **variation in one variable might affect another variable**
- with :ref:`designed experiments <SECTION-design-analysis-experiments>` we intentionally **introduce variation** into our process to learn more about the process (e.g. so that we can optimize our process for improved profitability); and
- and in the :ref:`latent variable modelling <SECTION_latent_variable_modelling>` section we learn how to deal with **multiple variables**, simultaneously extracting information from the data to understand how variability affects the process.

	
Histograms and probability distributions
=========================================

.. index:: histograms, frequency distribution

The :ref:`previous section <univariate-about-variability>` has hopefully convinced you that variation in a process is inevitable. This section aims to show how we can visualize and quantify variability in a recorded vector of data.

A histogram is a summary of the variation in a measured variable. It shows the *number* of samples that occur in a *category*: this is called a **frequency distribution**. For example: number of children born, categorized against their gender: male or female.

.. image:: ../figures/univariate/histogram-children-by-gender.png
	:scale: 40
	:align: center
	
The raw data in the above example was a vector of consisted of 2739 text entries, with 1420 of them as ``Male`` and 1319 of them as ``Female``. In this case ``Female`` and ``Male`` represent the two categories.

Histograms make sense for categorical variables, but a histogram can also be derived from a continuous variable. Here is an example showing the mass of cartons of 1 kg of flour. The continuous variable, mass, is divided into equal-size bins that cover the range of the available data.  Notice how the packaging system has to overfill each carton so that the vast majority of packages weigh over 1 kg (what is the average package mass?). If the variability in the packaging system could be reduced, then the histogram can be shifted to the left, thereby reducing overfill.

.. image:: ../figures/univariate/histogram-package-mass.png
	:scale: 60
	:align: center

Plot histograms for the following:

-	The grades for a class for a really easy test
-	The numbers thrown from a 6-sided die
-	The annual income for people in your country

.. - seeds with the same size later become plants of different heights and yield of fruit
.. - people born in the same year have lives of different duration due to environmental, genetic, health and societal factors
.. - games such as poker, roulette, lotteries, dice
.. - analytical measurements taken in a laboratory, even by the same person or computerized process have different outcomes
.. - weight of corn seeds (average is 200mg)

In preparing the above histograms, what have you implicitly inferred about time-scales? These histograms show the long-term distribution (probabilities) of the system being considered. This is why *concepts of chance and random phenomena* can be use to described systems and processes. Probabilities describe our long-term expectations:

-	The long-term sex ratio at birth 1.06:1 (boy:girl) is expected in Canada; but a newly pregnant mother would not know the sex.
-	The long-term data from a process shows an 85% yield from our batch reactor; but tomorrow it could be 59% and the day after that 86%.
-	Canadian life tables from 2002 (`Statistics Canada website <http://www.statcan.gc.ca/bsolc/olc-cel/olc-cel?catno=84-537-XIE&lang=eng>`_) show that females have a 98.86% chance of reaching age 30 and a 77.5% chance of reaching age 75; but people die at different ages due to different causes.
-	We know that a fair die has a 16.67% chance of showing a 4 when thrown, but we cannot predict the value of the next throw.

Even if we have complete mechanistic knowledge of our process, the concepts from probability and statistics are useful to summarize and communicate information about past behaviour, and the expected future behaviour. 

Steps to creating a frequency distribution, illustrated with 4 examples:

	#.	Decide what you are measuring:
	
		A.	acceptable or unacceptable metal appearance: yes/no
		B.	number of defects on a metal sheet: none, low, medium, high
		C.	yield from the batch reactor: somewhat continuous - quantized due to rounding to the closest integer
		D.	daily ambient temperature, in Kelvin: continuous values
	
	#.	Decide on a resolution for the measurement axis:
	
		A.	acceptable/unacceptable (1/0) code for the metal's appearance
		B.	use a scale from 1 to 4 that grades the metal's appearance
		C.	batch yield is measured in 1% increments, reported either as 78, 79, 80, 81%, *etc*.
		D.	temperature is measured to a 0.05 K precision, but we can report the values in bins of 5K
	
	#.	Report the number of observations in the sample or population that fall within each bin (resolution step):
	
		A.	number of metal pieces with appearance level "acceptable" and "unacceptable"
		B.	number of pieces with defect level 1, 2, 3, 4
		C.	number of batches with yield inside each bin level
		D.	number of temperature values inside each bin level
		
	#.	Plot the number of observations in category as a bar plot. If you plot the number of observations divided by the total number of observations, :math:`N`, then you are plotting the **relative frequency**.
	
.. TODO: show the above plots

.. index:: 
	single: frequency, relative

A :index:`relative frequency`, also called :index:`density`, is sometimes preferred:

-	we do not need to report the total number of observations, :math:`N`
-	it can be compared to other distributions
-	if :math:`N` is large enough, then the relative frequency histogram starts to resemble the population's distribution
-	the area under the histogram is equal to 1, and related to probability

.. image:: ../figures/univariate/frequency-histogram.png
	:scale: 60
	:align: center
	
Some nomenclature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We review a couple of concepts that you should have seen in prior statistical work.

.. _univariate-population:

.. raw:: latex

	\\

**Population**
	
	A large collection of observations that *might* occur; a set of *potential* measurements. Some texts consider an infinite collection of observations, but a large number of observations is good enough. 

.. We will use capital :math:`N` in this section to denote the :index:`population` size. WE USUALLY USE "N" as the sample size
.. We will use lowercase :math:`n` in this section to denote the :index:`sample` size.

**Sample**

	A collection of observations that have *actually* occurred; a set of *existing* measurements that we have recorded in some way, usually electronically.
	
	.. index:: 
		single: sample

	.. image:: ../figures/univariate/batch-yields.png
		:scale: 60
		:align: center
	
	In engineering applications where we have plenty of data, we can characterize the population from all available data. The figure here shows the viscosity of a motor oil, from all batches produced in the last 5 years (about 1 batch per day). These 1825 data points, though technically a *sample* are an excellent surrogate for the *population* viscosity because they come from such a long duration. Once we have characterized these samples, future viscosity values will likely follow that same distribution, provided the process continues to operate in a similar manner.

**Distribution**

	Distributions are used to provide a much smaller summary of many data points. Histograms, discussed above, are one way of visualizing a distribution. We will look at various distributions in the next section.

**Probability**
	
	The area under a plot of relative frequency distribution is equal to 1. :index:`Probability <single: probability>` is then the fraction of the area under the frequency distribution curve (also called density curve).
	
	Superimpose on your histograms drawn earlier:
	
	-	The probability of a test grades less than 80%
	-	The probability that the number thrown from a 6-sided die is less than or equal to 2
	-	The probability of someone's income exceeding $50,000

**Parameter**

	.. index:: 
		pair: population; parameter

	A parameter is a value that describes the population's **distribution** in some way. For example, the population mean.
	
**Statistic**
	
	A :index:`statistic` is an estimate of a population parameter.

**Mean (location)**
	
	.. _univariate_calculate_mean:
	
	The :index:`mean`, or :index:`average`, is a measure of :index:`location` of the distribution. For each measurement, :math:`x_i`, in your sample

	.. math::
		:nowrap:
			
			\begin{alignat*}{2}
				\text{population mean:} &\qquad&  \mathcal{E}\left\{x \right\} = \mu &= \frac{1}{N}\sum{x} \\
				\text{sample mean:}     &\qquad&                       \overline{x}  &= \frac{1}{n}\sum_{i=1}^{n}{x_i}
			\end{alignat*}
			
	where :math:`N` represents the entire population, and :math:`n` are the number of entries in the sample.
		
	.. code-block:: s

		x <- rnorm(50)   # a vector of 50 normally distributed random numbers
		mean(x)
	
	This is one of several statistics that describes your data: if you told your customer that the average density of your liquid product was 1.421 g/L, and nothing further, the customer might assume that some lots of the same product could have a density of 0.824 g/L, or 2.519 g/L. We need information in addition to the mean to quantify the distribution of values: *the spread*.

.. _univariate-variance:

**Variance (spread)**

	.. _univariate_calculate_variance:

	A measure of :index:`spread`, or :index:`variance`, is useful to quantify your distribution. 

	.. math::
		:nowrap:
		
	   	\begin{alignat*}{2}
	      	\text{Population variance}: &\qquad& \mathcal{V}\left\{x\right\} = \mathcal{E}\left\{ (x - \mu )^2\right\} = \sigma^2 &= \frac{1}{N}\sum{(x-\mu)^2} \\
			\text{Sample variance}:     &\qquad&                                                                             s^2  &= \frac{1}{n-1}\sum_{i=1}^{n}{(x_i - \overline{x})^2}
		\end{alignat*}

	Dividing by :math:`n-1` makes the variance statistic, :math:`s^2`, an unbiased estimator of the population variance, :math:`\sigma^2`. However, in most engineering data sets our value for :math:`n` is large, so using a divisor of :math:`n`, which you might come across in computer software or other texts, rather than :math:`n-1` as shown here, has little difference.

	.. code-block:: s

		sd(x)     # for standard deviation
		var(x)    # for variance
		
	The square root of variance, called the :index:`standard deviation` is a more useful measure of spread to engineers: it is easier to visualize on a histogram and has the advantage of being in the same units of the variable.

	**Degrees of freedom**: The denominator in the sample variance calculation, :math:`n-1`, is called the degrees of freedom. We have one fewer than :math:`n` degrees of freedom, because there is a constraint that the sum of the deviations around :math:`\overline{x}` must add up to zero. This constraint is from the definition of the mean. However, if we knew what the sample mean was without having to estimate it, then we could subtract each :math:`x_i` from that value, and our degrees of freedom would be :math:`n`.

**Outliers**

	Outliers are hard to define precisely, but an acceptable definition is that an :index:`outlier` is a point that is unusual, given the context of the surrounding data. The following 2 sequences of numbers show the number 4024 that appears in the first sequence, has become an outlier in the second sequence. It is an outlier based on the surrounding context.

	* 4024, 5152, 2314, 6360, 4915, 9552, 2415, 6402, 6261
	* 4, 61, 12, 64, 4024, 52, -8, 67, 104, 24
	
.. TODO: add a multivariate outlier illustration here
	
.. _univariate-median:

.. index:: robust statistics

**Median (robust measure of location)**

	The :index:`median` is an alternative measure of :index:`location`. It is a sample statistic, not a population statistic, and is computed by sorting the data and taking the middle value (or average of the middle 2 values, for even :math:`n`). It is also called a robust statistic, because it is insensitive (robust) to outliers in the data. 

	.. note::	
	
		The median is the most robust estimator of the sample location: it has a breakdown of 50%, which means that just under 50% of the data need to be replaced with unusual values before the median breaks down as a suitable estimate. The mean on the other hand has a breakdown value of :math:`1/n`, as only one of the data points needs to be unusual to cause the mean to be a poor estimate.

	.. code-block:: s

		median(x)
		
	Governments will report the median income, rather than the mean, to avoid influencing the value with the few very high earners and the many low earners. The median income per person is a more fair measure of location in this case.

**Median absolute deviation, MAD (robust measure of spread)**

	A robust measure of :index:`spread` is the :index:`MAD`, the :index:`median absolute deviation <see: median absolute deviation; MAD>`.  The name is descriptive of how the MAD is computed:

	.. math::
	
			\text{mad}\left\{ x_i \right\} = c \cdot \text{median}\left\{ \| x_i - \text{median}\left\{ x_i \right\}  \|  \right\} \qquad\qquad \text{where}\qquad c = 1.4826

	The constant :math:`c` makes the MAD consistent with the standard deviation when the observations :math:`x_i` are normally distributed. The MAD has a :index:`breakdown point` of 50%, because like the median, we can replace just under half the data with outliers before the estimate becomes unbounded.

	.. code-block:: s

		mad(x)

	Enrichment reading: read pages *1 to 8* of "`Tutorial to Robust Statistics <http://dx.doi.org/10.1002/cem.1180050103>`_", PJ Rousseeuw, *Journal of Chemometrics*, **5**, 1-20, 1991.


.. For each of the distributions:
.. #.	show a typical plot of the probability function :math:`p(x)` against the variable's value :math:`x`
.. #.	learn when to use that distribution (we will show some examples)
.. #.	know what the parameters of the distribution are


.. _univariate_binary_distribution:

Binary (Bernoulli) distribution
================================

.. index:: binary distribution, Bernoulli distribution

Systems that have binary outcomes (pass/fail; yes/no) must obey the probability principle that: :math:`p(\text{pass}) + p(\text{fail}) = 1`. A Bernoulli distribution only has one parameter, :math:`p_1`, the probability of observing event 1. The probability of the other event, :math:`p_2 = 1 - p_1`. 

An example: a histogram for a system that produces 70% acceptable product, :math:`p(\text{pass}) = 0.7`, could look like:

.. image:: ../figures/univariate/histogram-70-30.png
	:align: center
	:scale: 45

If each observation is independent of the other, then:

	-	For the above system where :math:`p(\text{pass}) = 0.7`, what is probability of seeing the following outcome: **pass**, **pass**, **pass** (3 times in a row)?

		:math:`(0.7)(0.7)(0.7) = 0.343`, about one third

	-	What is the probability of seeing the sequence: **pass**, **fail**, **pass**, **fail**, **pass**, **fail**?

		:math:`(0.7)(0.3)(0.7)(0.3)(0.7)(0.3) = 0.0093`, less than 1%

Another example: you work in a company that produces tablets. The machine creates acceptable, unbroken tablets 97% of the time, so :math:`p_\text{acceptable} = 0.97`, so :math:`p_\text{defective} = 0.03`.

	-	In a future batch of 850,000 tablets, how many tablets are expected to be defective? (Most companies will call this quantity "the cost of waste".)
	
		:math:`850000 \times (1-0.97) = 25,500` tablets per batch
		
	-	You take a random sample of :math:`n` tablets from a large population of :math:`N` tablets. What is the chance that **all** :math:`n` tablets are acceptable if :math:`p` is the Bernoulli population parameter of finding acceptable tablets:
	
		===================== ================== =================
		Sample size           :math:`p` = 95%    :math:`p` = 97%
		===================== ================== =================
		:math:`n=10`
		:math:`n=50`
		:math:`n=100`
		===================== ================== =================
		
	-	Are you surprised by the large reduction in the number of defective tablets for only a small increase in :math:`p`?
	
Uniform distribution
=====================

A :index:`uniform distribution` arises when an observation's value is equally as likely to occur as all the other recorded values. The classic example are dice: each face of a die is equally as likely to show up as any of the others. This forms a discrete, uniform distribution.

The histogram for an event with 4 possible outcomes that are uniformly distributed is shown below. Notice that the *sample* histogram will not necessarily have equal bar heights for all categories (bins).

.. image:: ../figures/univariate/histogram-4-cuts.png
	:align: center
	:scale: 50

You can simulate uniformly distributed random numbers in most software packages. As an example, to generate 50 uniformly distributed random *integers* between 2 and 10, inclusive:

	**R**: ``x <- as.integer(runif(50, 2, 11))``

	**MATLAB/Octave**: ``round(rand(50, 1) * (10 - 2) + 2)``

	**Python**:

		.. code-block:: python

			import numpy as np     # requires installing the Numpy library
			(np.random.rand(50, 1) * (10 - 2) + 2).round()

A continuous, uniform distribution arises when there is equal probability of every measurement occurring within a given lower- and upper-bound. This sort of phenomena is not often found in practice. Usually, continuous measurements follow some other distribution, of which we will discuss the normal and :math:`t`-distribution next.

Normal distribution
====================

Before introducing the normal distribution, we first look at two important concepts: the Central limit theorem, and the concept of independence.

.. _central_limit_theorem:

Central limit theorem 
~~~~~~~~~~~~~~~~~~~~~

The :index:`Central limit theorem` plays an important role in the theory of probability and in the derivation of the normal distribution. We don't prove this theorem here, but we only use the result:

	The average of a sequence of values *from any distribution* will approach the normal distribution, provided the original distribution has finite variance. 

The condition of finite variance is true for almost all systems of practical interest.
	
.. image:: ../figures/univariate/CLT-derivation.png
	:alt:	../figures/univariate/CLT-derivation.svg
	:align: center
	
The critical requirement for the central limit theorem to be true, is that the samples used to compute the average are independent. In particular, we **do not** require the original data to be normally distributed. The average produced from these samples will be be more nearly normal though.

Imagine a case where we are throwing dice. The distributions, shown below, are obtained when we throw a die :math:`M` times and we plot the distribution of the *average* of these :math:`M` throws.

.. image:: ../figures/univariate/simulate-CLT.png
	:align: center

As one sees from the above figures, the distribution from these averages quickly takes the shape of the so-called *normal distribution*. As :math:`M` increases, the y-axis starts to form a peak. 

What is the engineering significance of this averaging process (which is really just a weighted sum)?  Many of the quantities we measure are bulk properties, such as viscosity, density, or particle size. We can conceptually imagine that the bulk property measured is the combination of the same property, measured on smaller and smaller components. Even if the value measured on the smaller component is not normally distributed, the bulk property will be as if it came from a normal distribution.

Independence 
~~~~~~~~~~~~~~~~~~~~~

The assumption of :index:`independence` is widely used in statistical work and is a condition for using the central limit theorem. 

.. note:: The assumption of independence means the the samples we have in front of us are *randomly taken* from a population. If two samples are independent, there is no possible relationship between them.

We frequently violate this assumption of independence in engineering applications. Think about these examples for a while:

-	A questionnaire is given to a group of people. What happens if they discuss the questionnaire in sub-groups prior to handing it in?

		We are not going to receive :math:`n` independent answers, rather we will receive as many independent opinions as there are sub-groups.
		
-	The rainfall amount, recorded every day, over the last 30 days.

		These data are not independent: if it rains today, it can likely rain tomorrow as the weather usually stays around for some days. These data are not useful as a representative sample of typical rainfall, however they are useful for complaining about the weather. Think about the case if we had considered rainfall in hourly intervals, rather than daily intervals.
		
-	The snowfall, recorded on 3 January for every year since 1976: independent or not? 

		These sampled data will be independent.
		
-	The impurity values in the last 100 batches of product produced is shown below. Which of the 3 time sequences has independent values?

	In chemical processes there is often a transfer from batch-to-batch: we usually use the same lot of raw materials for successive batches, the batch reactor may not have been cleaned properly between each run, and so on. It is very likely that two successive batches (:math:`k` and :math:`k+1`) are somewhat related, and less likely that batch :math:`k` and :math:`k+2` are related. In the figure below, can you tell which sequence of values are independent?
	
	.. image:: ../figures/univariate/simulate-independence.png
		:align: center
	
	Sequence 2 (sequence 1 is positively correlated, while sequence 3 is negatively correlated).

-	We need a highly reliable pressure release system. Manufacturer A sells a system that fails 1 in every 100 occasions, and manufacturer B sells a system that fails 3 times in every 1000 occasions. Given this information, answer the following:

		-	The probability that system A fails: :math:`p(\text{A}_\text{fails}) = 1/100` 
		-	The probability that system B fails::math:`p(\text{B}_\text{fails}) = 3/1000` 
		-	The probability that both system A and fail at the same time: :math:`p(\text{both A and B fail}) = \frac{1}{100} \cdot \frac{3}{1000} = 3 \times 10^{-5}`, but only if system A and B are totally independent.
		-	For the previous question, what does it mean for system A to be totally independent of system B?
	
				It means the 2 systems must be installed in parallel, so that there is no interaction between them at all.
				
		-	How would the probability of both A and B failing simultaneously change if A and B were not independent?
		
				The probability of both failing simultaneously will increase.
	
.. See Hodges and Lehmann (1970): there is a whole Chapter devoted to it.

.. See: http://www.rsscse.org.uk/ts/gtb/contents.html: article on Teaching Independence; see PDF file in Readings directory.


Formal definition for the normal distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: normal distribution; formal definition

.. math:: p(x) = \dfrac{1}{\sqrt{2\pi \sigma^2}}e^{-\dfrac{\left(x-\mu\right)^2}{2\sigma^2}}
	
.. image:: ../figures/univariate/normal-distribution-standardized.png
	:align: center

-	:math:`x` is the variable of interest

-	:math:`p(x)` is the probability of obtaining that value of :math:`x`

-	:math:`\mu` is the population average for the distribution (first parameter)

-	:math:`\sigma` is the population standard deviation for the distribution, and is always a positive quantity (second parameter)

Some questions: 

#.	What is the maximum value of :math:`p(x)` and where does it occur, using the formula above?

#.	What happens to the shape of :math:`p(x)` as :math:`\sigma` gets larger ?

#.	What happens to the shape of :math:`p(x)` as :math:`\sigma \rightarrow 0` ?

#.	Fill out this table:

	.. csv-table:: 
	   :header: :math:`\\mu`, :math:`\\sigma`, :math:`x`, :math:`p(x)`
	   :widths: 30, 30, 30, 80

		0, 1, 0,
		0, 1, 1,
		0, 1, -1,
		
Some useful points:

	-	The total area from :math:`x=-\infty` to :math:`x=+\infty` is 1.0; we cannot calculate the integral of :math:`p(x)` analytically.

	-	:math:`\sigma` is the distance from the mean, :math:`\mu`, to the point of inflection
	
	-	The normal distribution only requires two parameters to describe it: :math:`\mu` and :math:`\sigma`
	
	-	The area from :math:`x= -\sigma` to :math:`x = \sigma` is about 70% (68.3% exactly) of the distribution. So we have a probability of about 15% of seeing an :math:`x` value greater than :math:`x = \sigma`, and also 15% of :math:`x < -\sigma`
	
	-	The :index:`tail <single: tail, in a histogram>` area outside :math:`\pm 2\sigma` is about 5% (2.275 outside each tail)

To calculate the point on the curve :math:`p(x)` we use the ``dnorm(...)`` function in R. It requires you specify the two parameters:

	.. code-block:: s

		> dnorm(-1, mean=0, sd=1)    # gives value of p(x = -1) when mu=0, sigma=1
		[1] 0.2419707

It is more useful to calculate the area under :math:`p(x)` from :math:`x=-\infty` to a particular point :math:`x`. This is called the cumulative distribution, and is discussed more fully in :ref:`the next section <univariate_check_for_normality_qqplot>`.

	.. code-block:: s
	
		> pnorm(-1, mean=0, sd=1)    # gives area from -inf to -1, for mu=0, sigma=1
		[1] 0.1586553
		> pnorm(1, mean=0, sd=1)     # gives area from -inf to +1, for mu=0, sigma=1
		[1] 0.8413447
		> pnorm(3, mean=0, sd=3)     # spread is wider, but fractional area the same
		[1] 0.8413447

You might still find yourself having to refer to tables of cumulative area under the normal distribution, instead of using the ``pnorm()`` function (for example in a test or exam). If you look at the appendix of most statistical texts you will find these tables, and there is one :ref:`at the end of this chapter <univariate_statistical_tables>`. Since these tables cannot be produced for all combinations of mean and standard deviation parameters, they use what is called *standard form*.

.. math::

	z_i = \frac{x_i - \text{mean}}{\text{standard deviation}}
	
The values of the mean and standard deviation are either the population parameters, if known, or using the best estimate of the mean and standard deviation from the sampled data. 

For example, if our values of :math:`x_i` come from a normal distribution with mean of 34.2 and variance of 55. Then we could write :math:`x \sim \mathcal{N}(34.2, 55)`, which is short-hand notation of saying the same thing. The equivalent :math:`z`-values for these :math:`x_i` values would be: :math:`z_i = \dfrac{x_i - 34.2}{\sqrt{55}}`. 

This transformation to standard form **does not change the distribution** of the original :math:`x`, it only changes the parameters of the distribution. You can easily prove to yourself that :math:`z` is normally distributed as :math:`z \sim \mathcal{N}(0.0, 1.0)`. So statistical tables only report the area under the distribution of a :math:`z` value with mean of zero, and unit variance.

This is a common statistical technique, to :index:`standardize a variable`, which we will see several times. Standardization takes our variable from :math:`x \sim \mathcal{N}(\text{some mean}, \text{some variance})` and converts it to :math:`z \sim \mathcal{N}(0.0, 1.0)`. It is just as easy to go backwards, from a given :math:`z`-value and return back to our original :math:`x`-value.

The units of :math:`z` are dimensionless, no matter what the original units of :math:`x` were. Standardization also allows us to straightforwardly compare 2 variables that may have different means and spreads. For example if our company has two reactors at different locations, producing the same product. We can standardize a variable of interest, e.g. viscosity, from both reactors and then proceed to use the standardized variables to compare performance.

Consult a statistical table found in most statistical textbooks for the normal distribution, such as the one found at the :ref:`end of this chapter <univariate_statistical_tables>`. Make sure you can firstly understand how to read the table. Secondly, duplicate a few entries in the table using R. Complete these small exercises by estimating what the rough answer should be. Use the tables first, then use R to get a more accurate estimate.

#.	Assume :math:`x`, the measurement of biological activity for a drug, is normally distributed with mean of 26.2 and standard deviation of 9.2. What is the probability of obtaining an activity reading less than or equal to 30.0?

#.	Assume :math:`x` is the yield for a batch process, with mean of 85 g/L and variance of 16 g/L. What proportion of batch yield values lie between 70 and 95 g/L?

.. _univariate_check_for_normality_qqplot:

Checking for normality: using a q-q plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: quantile-quantile plot (q-q plot)
	single: normal distribution; check if

Often we are not sure if a sample of data can be assumed to be normally distributed. This section shows you how to test whether the data are normally distributed, or not. 

Before we look at this method, we need to introduce the concept of the inverse :index:`cumulative distribution` function (inverse CDF). Recall the **cumulative distribution** is the area underneath the distribution function, :math:`p(z)`, which goes from :math:`-\infty` to :math:`z`. For example, the area from :math:`-\infty` to :math:`z=-1` is about 15%, as we showed earlier, and we can use the ``pnorm()`` function in R to verify that. 
	
.. index:: inverse cumulative distribution

Now the **inverse cumulative distribution** is used when we know the area, but want to get back to the value along the :math:`z`-axis. For example, below which value of :math:`z` does 95% of the area lie for a standardized normal distribution?  Answer: :math:`z=1.64`. In R we use the ``qnorm(0.95, mean=0, sd=1)`` to calculate this value. The ``q`` stands for `quantile <http://en.wikipedia.org/wiki/Quantile>`_, because we give it the quantile and it returns the :math:`z`-value: e.g. ``qnorm(0.5)`` gives 0.0.

.. image:: ../figures/univariate/show-pnorm-and-qnorm.png
	:width: 600px
	:scale: 20
	:align: center
		
On to checking for normality. p by first constructing some quantities that we would expect for truly normally distributed data. Secondly, we construct the same quantities for the actual data. A plot of these 2 quantities against each other will reveal if the data are normal, or not.

#.	Imagine we have :math:`N` observations which are normally distributed. Sort the data from smallest to largest. The first data point should be the :math:`(1/N \times 100)` quantile, the next data point is the :math:`(2/N \times 100)` quantile, the middle, sorted data point is the 50th quantile, :math:`(1/2 \times 100)`, and the last, sorted data point is the :math:`(N/N \times 100)` quantile.

	The middle, sorted data point from this truly normal distribution must have a :math:`z`-value on the standardized scale of 0.0 (we can verify that by using ``qnorm(0.5)``). By definition, 50% of the data should lie below this mid point. The first data point will be at ``qnorm(1/N)``, the second at ``qnorm(2/N)``, the middle data point at ``qnorm(0.5)``, and so on. In general, the :math:`i^\text{th}` sorted point should be at ``qnorm((i-0.5)/N)``, for values of :math:`i = 1, 2, \ldots, N`. We subtract off 0.5 by convention to account for the fact that ``qnorm(1.0) = Inf``. So we construct this vector of theoretically expected quantities from the inverse cumulative distribution function.
	
	.. code-block:: s
	
		N = 10
		index <- seq(1, N)
		P <- (index - 0.5) / N
		P
		[1] 0.05  0.15  0.25  0.35  0.45  0.55  0.65  0.75  0.85  0.95
		theoretical.quantity <- qnorm(P)
		[1] -1.64 -1.04 -0.674 -0.385 -0.126  0.125  0.385  0.6744 1.036  1.64

#.	We also construct the actual quantiles for the sampled data. First, standardize the sampled data by subtracting off its mean and dividing by its standard deviation. Here is an example of 10 batch yields (see actual values below). The mean yield is 80.0 and the standard deviation is 8.35. The standardized yields are found by subtracting off the mean and dividing by the standard deviation. Then the standardized values are sorted. Compare them to the theoretical quantities.

	.. code-block:: s

		yields <- c(86.2, 85.7, 71.9, 95.3, 77.1, 71.4, 68.9, 78.9, 86.9, 78.4)
		mean.yield <- mean(yields)		# 80.0
		sd.yield <- sd(yields)			# 8.35
	
		yields.z <- (yields - mean.yield)/sd.yield
		[1] 0.734  0.674 -0.978  1.82 -0.35 -1.04 -1.34 -0.140  0.818 -0.200
	
		yields.z.sorted <- sort(yields.z)
		[1] -1.34 -1.04 -0.978 -0.355 -0.200 -0.140  0.674  0.734  0.818  1.82
		
		theoretical.quantity  # numbers are rounded in the printed output
		[1] -1.64 -1.04 -0.674 -0.385 -0.126  0.125  0.385  0.6744 1.036  1.64
	
#.	The final step is to plot this data in a suitable way. If the sampled quantities match the theoretical quantities, then a scatter plot of these numbers should form a 45 degree line. 

	.. code-block:: s
		
		plot(theoretical.quantity, yields.z.sorted, type="p")
		
	.. image:: ../figures/univariate/qqplot-derivation.png
		:align: center
		:scale: 50

A built-in function exists in R that runs the above calculations and shows a scatter plot. The 45 degree line is added using the ``qqline(...)`` function. However, a better function that adds a confidence limit envelope is included in the ``car`` library (see the *Package Installer* menu in R for adding libraries from the internet). 

.. code-block:: s
	
	qqnorm(yields)
	qqline(yields)
	
	# or, using the ``car`` library
	library(car)
	qqPlot(yields)

.. image:: ../figures/univariate/qqplot-from-R.png
	:align: center
	:scale: 100
	
The R plot rescales the :math:`y`-axis (sample quantiles) back to the original units to make interpretation easier. We expect some departure from the 45 degree line due to the fact that these are only a sample of data. However, large deviations indicates the data are not normally distributed. An error region, or confidence envelope, may be superimposed around the 45 degree line.

The q-q plot, quantile-quantile plot, shows the quantiles of 2 distributions against each other. In fact, we can use the horizontal axis for any distribution, it need not be the theoretical normal distribution. We might be interested if our data follow an :math:`F`-distribution then we could use the quantiles for that theoretical distribution on the horizontal axis.

We can use the q-q plot to compare any 2 *samples of data*, even if they have different values of :math:`N`, by calculating the quantiles for each sample at different step quantiles (e.g. 1, 2, 3, 4, 5, 10, 15, .... 95, 96, 97, 98, 99), then plot the q-q plot for the two samples. You can calculate quantiles for any sample of data using the ``quantile`` function in R. The simple example below shows how to compare the q-q plot for 1000 normal distribution samples against 2000 :math:`F`-distribution samples. 

	.. code-block:: s
	
		rand.norm <- rnorm(1000)            # 1000 normal values
		rand.f <- rf(2000, df1=200, df=150) # 2000 values from F-distribution
		hist(rand.f)                        # looks sort of normally distributed
		quantiles <- c(1, 2, 3, 4, seq(5, 95, 5), 96, 97, 98, 99)/100
		norm.quantiles <- quantile(rand.norm, quantiles)
		f.quantiles <- quantile(rand.f, quantiles)
		plot(f.quantiles, norm.quantiles)   # proves it isn't
		library(car)
		qqPlot(rand.f, distribution="norm") # also proves it isn't
		
.. image:: ../figures/univariate/qqplot-comparison.png
	:alt:   ../figures/univariate/qqplot-comparison.R
	:align: center
	
Even though the histogram of the :math:`F`-distribution samples looks normal to the eye (left), the q-q plot (right) quickly confirms it is definitely not normal, particularly, that the right-tail is too heavy.

Introduction to confidence intervals from the normal distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We introduce the concept of confidence intervals here as a straightforward application of the normal distribution, Central limit theorem, and standardization.

Suppose we have a quantity of interest from a process, such as the daily profit. We have many measurements of this profit, and we can easily calculate the **average** profit. But we know that if we take a different data set of profit values and calculate the average, we will get a similar, but different average. Since we will never know the true population average, the question we want to answer is:

	What is the range within which the true (population) average value lies?  E.g. give a range for the true, but unknown, daily profit.
	
This range is called a :index:`confidence interval`, and we study them :ref:`in more depth later on <univariate_confidence_intervals>`. We will use an example to show how to calculate this range.

Let's take :math:`n` values of this daily profit value, let's say :math:`n=5`.

#.	An estimate of the population mean is given by :math:`\overline{x} = \displaystyle  \dfrac{1}{n}  \sum_i^{i=n}{x_i}\qquad\qquad` (we :ref:`saw this before <univariate_calculate_mean>`)

#.	The estimated population variance is :math:`s^2 =\displaystyle  \frac{1}{n-1}\sum_i^{i=n}{(x_i - \overline{x})^2}\qquad` (we also :ref:`saw this before <univariate_calculate_variance>`)

#.	This is new: the estimated mean, :math:`\overline{x}`, is a value that is also normally distributed with mean of :math:`\mu` and variance of :math:`\sigma^2/n`, with only one requirement: this result holds only if each of the :math:`x_i` values are independent of each other.

	Mathematically we write: :math:`\displaystyle \overline{x} \sim \mathcal{N}\left(\mu, \sigma^2/n\right)`.

	This important results helps answer our question above. It says that repeated estimates of the mean will be an accurate, unbiased estimate of the population mean, and interestingly, the variance of that estimate is decreased by using a greater number of samples, :math:`n`, to estimate that mean. This makes intuitive sense: the more **independent** samples of data we have, the *better* our estimate ("better" in this case implies lower error, i.e. lower variance).
	
	We can illustrate this result as shown here:
	
	.. image:: ../figures/univariate/explain-confidence-interval.png
		:alt:	../figures/univariate/explain-confidence-interval.R
		:scale: 80
		:align: center

	The true population (but unknown to us) profit value is $700.

	-	The 5 samples come from the distribution given by the thinner line: :math:`\displaystyle x \sim \mathcal{N}\left(\mu, \sigma^2\right)`
	-	The :math:`\overline{x}` average comes from the distribution given by the thicker line: :math:`\displaystyle \overline{x} \sim \mathcal{N}\left(\mu, \sigma^2/n\right)`.
	
#.	Creating :math:`z` values for each :math:`x_i` raw sample point:

	.. math::
	
		z_i = \frac{x_i - \mu}{\sigma}
		
#.	The :math:`z`-value for :math:`\overline{x}` would be:

	.. math::
	
		z = \dfrac{\overline{x} - \mu}{\sigma / \sqrt{n}}

	which subtracts off the unknown population mean from our estimate of the mean, and divides through by the standard deviation for :math:`\overline{x}`.
	
	We can illustrate this as:
	
	.. image:: ../figures/univariate/explain-confidence-interval-normalized.png
		:alt:	../figures/univariate/explain-confidence-interval.R
		:scale: 80
		:align: center
	
#.	Using the known normal distribution for :math:`\displaystyle \overline{x} \sim \mathcal{N}\left(\mu, \sigma^2/n\right)`, we can find the vertical, dashed red lines shown in the previous figure, that contain 95% of the area under the distribution for :math:`\overline{x}`.

#.	These vertical lines are symmetrical about 0, and we will call them :math:`-c_n` and :math:`+c_n`, where the subscript :math:`n` refers to the fact that they are from the normal distribution (it doesn't refer to the :math:`n` samples). From the preceding section on q-q plots we know how to calculate the :math:`c_n` value from R: using ``qnorm(1 - 0.05/2)``, so that there is 2.5% area in each tail.

#.	Finally, we construct an interval for the true population mean, :math:`\mu`, using the standard form:

	.. math::
			:label: CI-mean-variance-known

			\begin{array}{rcccl} 
				  - c_n                                      &\leq& z                                                        &\leq &  +c_n\\
				  - c_n                                      &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}} &\leq &  +c_n\\
				\overline{x}  - c_n \dfrac{\sigma}{\sqrt{n}} &\leq&  \mu                                                     &\leq& \overline{x}  + c_n\dfrac{\sigma}{\sqrt{n}} \\
				  \text{LB}                                  &\leq&  \mu                                                     &\leq& \text{UB}
			\end{array}

	Notice that the lower and upper bound are a function of the known sample mean, :math:`\overline{x}`, the values for :math:`c_n` which we chose, the known sample size, :math:`n`, and the unknown population standard deviation, :math:`\sigma`.
	
	So to estimate our bounds we must know the value of this population standard deviation. This is not very likely, (I can't think of any practical cases where we know the population standard deviation, but not the population mean, which is the quantity we are constructing this range for), however there is a hypothetical example in :ref:`the next section <univariate_confidence_interval_t_distribution>` to illustrate the calculations.
	
	The :math:`t`-distribution is required to remove this impractical requirement of knowing the population standard deviation.

The t-distribution
=======================

.. index:: t-distribution

Suppose we have a quantity of interest from a process, such as the daily profit. In the preceding section we started to answer the useful and important question: 

	What is the range within which the true average value lies?  E.g. the range for the true, but unknown, daily profit.
	
But we got stuck, because the lower and upper bounds we calculated for the true average, :math:`\mu` were a function of the unknown population standard deviation, :math:`\sigma`. Repeating :eq:`CI-mean-variance-known`:

.. math::

		\begin{array}{rcccl} 
			  - c_n                                      &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}} &\leq &  +c_n\\
			\overline{x}  - c_n \dfrac{\sigma}{\sqrt{n}} &\leq&  \mu                                                     &\leq& \overline{x}  + c_n\dfrac{\sigma}{\sqrt{n}} \\
			  \text{LB}                                  &\leq&  \mu                                                     &\leq& \text{UB}
		\end{array}

which we derived by using the fact that :math:`\dfrac{\overline{x} - \mu}{\sigma/\sqrt{n}}` is normally distributed.

An obvious way out of our dilemma is to replace :math:`\sigma` by the sample standard deviation, :math:`s`, which is exactly what we will do, however, the quantity :math:`\frac{\overline{x} - \mu}{s/\sqrt{n}}` is not normally distributed, but is :math:`t`-distributed. Before we look at the details, it is helpful to see how similar in appearance the :math:`t` and normal distribution are: the :math:`t`-distribution peaks slightly lower than the normal distribution, but it has broader tails. The total area under both curves illustrated here is 1.0.

.. image:: ../figures/univariate/t-distribution-comparison.png
	:align: center
	:scale: 100

There is one other requirement we have to ensure in order to use the :math:`t`-distribution: the values that we sample, :math:`x_i` must come from a normal distribution (carefully note that in the previous section we didn't have this restriction!). Fortunately it is easy to check this requirement: just use the :ref:`q-q plot method described earlier <univariate_check_for_normality_qqplot>`. Another requirement, which we had before, was that we must be sure these measurements, :math:`x_i`, are independent.

.. image:: ../figures/univariate/t-distribution-derivation.png
	:align: center
	:scale: 75

So given our :math:`n` samples, which are independent, and from a normal distribution, we can now say: 

.. math::
	:label: distribution-for-sample-average

	\frac{\overline{x} - \mu}{s/\sqrt{n}} \sim t_{n-1}

Compare this to the previous case where our :math:`n` samples are independent, and we happen to know, by some unusual way, what the population standard deviation is, :math:`\sigma`:

.. math::

	\frac{\overline{x} - \mu}{\sigma/\sqrt{n}} \sim \mathcal{N} \left(0, 1\right)

So the more practical and useful case where :math:`z  = \frac{\overline{x} - \mu}{s/\sqrt{n}} \sim t_{n-1}` can now be used to construct an interval for :math:`\mu`. We say that :math:`z` follows the :math:`t`-distribution with :math:`n-1` degrees of freedom, where the degrees of freedom refer to those from the calculating the *estimated* standard deviation, :math:`s`. 
 
Note that the new variable :math:`z` only requires we know the population mean (:math:`\mu`), not the population standard deviation; rather we use our estimate of the standard deviation :math:`s/\sqrt{n}` in place of the population standard deviation.

We will come back to :eq:`distribution-for-sample-average` in a minute; let's first look at how we can calculate values from the :math:`t`-distribution in computer software.

.. 
	From Box, Hunter and Hunter, 1st edition, p 50-51
	To use the :math:`t`-distribution we must ensure that these 3 conditions are true:

	#. the sampled values :math:`y_i` are normally distributed around the mean :math:`\mu` and have variance :math:`\sigma` (note that we do not need to know the value of :math:`\sigma`)
	#. the variance estimate, :math:`s` is distributed independently of :math:`y`
	#. the quantity :math:`s^2` is calculated from normally and independently distributed observations having variance :math:`\sigma^2`.

.. TODO: see p 295 of Devore here for in-class example

Calculating the t-distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-	In R we use the function ``dt(x=..., df=...)`` to give us the values of the probability density values, :math:`p(x)`, of the :math:`t`-distribution (compare this to the ``dnorm(x, mean=..., sd=...)`` function for the normal distribution).

	For example ``dt(x=0, df=8)`` returns 0.386699, while the same ordinate under the standard normal distribution, ``dnorm(x=0)`` gives 0.3989423, proving the :math:`t`-distribution has a lower peak than the normal distribution. 

-	The cumulative area from :math:`-\infty` to :math:`x` under the probability density curve gives us the probability that values less than or equal to :math:`x` could be observed. It is calculated in R using ``pt(q=..., df=...)``. For example, ``pt(1.0, df=8)`` is 0.8267. Compare this to the R function for the standard normal distribution: ``pnorm(1.0, mean=0, sd=1)`` which returns 0.8413.

-	And similarly to the ``qnorm`` function which returns the ordinate for a given area under the normal distribution, the function ``qt(0.8267, df=8)`` returns 0.9999857, close enough to 1.0, which is the inverse of the previous example.


.. _univariate_confidence_interval_t_distribution:

Using the t-distribution to calculate our confidence interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  But in R, we use the ``dt(x, df=...)`` function to give us the values of the :math:`t`-distribution for a given value of :math:`x` which has been computed with ``df`` degrees of freedom. We use the :math:`t`-distribution in calculations related to a sample *mean*, and it is the sample mean that we use as the :math:`z` value, on the :math:`x`-axis in the distribution. This is why the distribution is only a function of the degrees of freedom.

Returning back to :eq:`distribution-for-sample-average` we stated that

.. math::
	
		\frac{\overline{x} - \mu}{s/\sqrt{n}} &\sim t_{n-1}

We can plot the :math:`t`-distribution for a given value of :math:`n-1`, the degrees of freedom. Then we can locate vertical lines on the :math:`x`-axis at :math:`-c_t` and :math:`+c_t` so that they area between the verticals covers say 95% of the total distribution's area. The subscript :math:`t` refers to the fact that these are critical values from the :math:`t`-distribution.


Then we write:

.. math::
	:label: CI-mean-variance-unknown

	\begin{array}{rcccl} 
		  - c_t                                  &\leq& z                                                   &\leq &  +c_t\\
		  - c_t                                  &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
		\overline{x}  - c_t \dfrac{s}{\sqrt{n}}  &\leq&  \mu                                                &\leq& \overline{x}  + c_t\dfrac{s}{\sqrt{n}} \\
		  \text{LB}                              &\leq&  \mu                                                &\leq& \text{UB}
	\end{array}

Now all the terms in the lower and upper bound are known, or easily calculated.

So we finish this section off with an example. We produce large cubes of polymer product on our process. We would like to estimate the cube's average viscosity, but measuring the viscosity is a destructive laboratory test. So using 9 independent samples taken from this polymer cube, we get the 9 lab values of viscosity: ``23, 19, 17, 18, 24, 26, 21, 14, 18``. 

If we repeat this process with a different set of 9 samples we will get a different average viscosity. So we recognize the average of a sample of data, is itself just a single estimate of the population's average. What is more helpful is to have **a range**, given by a lower and upper bound, that we can say the true population mean lies within.

#.	The average of these nine values is :math:`\overline{x} = 20` units.

#.	Using the Central limit theorem, what is the distribution from which :math:`\overline{x}` comes?

		:math:`\overline{x} \sim \mathcal{N}\left(\mu, \sigma^2/n \right)`
		
		This also requires the assumption that the samples are independent estimates of the population viscosity. We **don't** have to assume the :math:`x_i` are normally distributed.
		
#.	What is the distribution of the sample average?  What are the parameters of that distribution?

		The sample average is normally distributed as :math:`\mathcal{N}\left(\mu, \sigma^2/n \right)`
		
#.	Assume, for some hypothetical reason, that we know the population viscosity standard deviation is :math:`\sigma=3.5` units. Calculate a lower and upper bound for :math:`\mu`:

		The interval is calculated using :eq:`CI-mean-variance-known`:
		
		.. math::
		
			\text{LB} &= \overline{x} - c_n \dfrac{\sigma}{\sqrt{n}} \\
			          &= 20 - 1.95996 \cdot \dfrac{3.5}{\sqrt{9}} \\
			          &= 20 - 2.286 = {\bf 17.7} \\
			\text{UB} &= 20 + 2.286 = {\bf 22.3}

#.	We can confirm these 9 samples are normally distributed by using a q-q plot (not shown). This is an important requirement to use the :math:`t`-distribution, next.

#.	Calculate an estimate of the standard deviation.

		:math:`s = 3.81`
	
#.	Now construct the :math:`z`-value for the sample average and from what distribution does this :math:`z` come from?

		It comes the :math:`t`-distribution with :math:`n-1 = 8` degrees of freedom, and is given by :math:`z = \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}}`

#.	Construct an interval, symbolically, that will contain the population mean of the viscosity. Also calculate the lower and upper bounds of the interval assuming the internal to span 95\% of the area of this distribution.

		The interval is calculated using :eq:`CI-mean-variance-unknown`:
		
		.. math::
		
			\text{LB} &= \overline{x}  - c_t \dfrac{s}{\sqrt{n}} \\
			          &= 20 - 2.306004 \cdot \dfrac{3.81}{\sqrt{9}} \\
			          &= 20 - 2.929 = 17.1 \\
			\text{UB} &= 20 + 2.929 = 22.9

		using from R that ``qt(0.025, df=8)`` and ``qt(0.975, df=8)``, which gives ``2.306004``
			
Comparing the answers for parts 4 and 8 we see the interval, for the same level of 95% certainty, is wider when we have to estimate the standard deviation. This makes sense: the standard deviation is an estimate (meaning there is error in that estimate) of the true standard deviation. That uncertainty must propagate, leading to a wider interval within which we expect to locate the true population viscosity, :math:`\mu`.

We will interpret confidence intervals in more detail a :ref:`little later on <univariate_confidence_intervals>`.

.. sum((x-20) * (x-20)) = 116, DOF=8, s^2 = 116/8 = 14.5, s=3.81. Distribution is normal, mean=\mu, stddev=3.5/sqrt(9) = (3.5^2)/9 = 2.286
.. s/sqrt(n) = 3.81/sqrt(9) = 1.27

.. The value of :math:`\overline{x}` is not normally distributed, it is :math:`t`distributed. This means that if we had to repeatedly calculate :math:`\overline{x}`, those averages would follow a :math:`t`distribution, even though the source values, :math:`x_i` are normally distributed. 

.. another example
	
Poisson distribution
=======================

.. index:: rare events, system failures

The :index:`Poisson distribution` is useful to characterize rare events (number of cell divisions in a small time unit), system failures and breakdowns, or number of flaws on a product (contaminations per cubic millimetre). These are events that have a very small probability of occurring within a given time interval or unit area (e.g. pump failure probability per minute = 0.000002), but there are many opportunities for the event to possibly occur (e.g. the pump runs continuously). A key assumption is that the events must be independent. If one pump breaks down, then the other pumps must not be affected; if one flaw is produced per unit area of the product, then other flaws that appear on the product must be independent of the first flaw.

Let :math:`n` = number of opportunities for the event to occur. If this is a time-based system, then it would be the number of minutes the pump is running. If it were an area/volume based system, then it might be the number of square inches or cubic millimetres of the product. Let :math:`p` = probability of the event occurring: e.g. :math:`p = 0.000002` chance per minute of failure, or :math:`p = 0.002` of a flaw being produced per square inch.  The rate at which the event occurs is then given by :math:`\eta = np` and is a count of events per unit time or per unit area. A value for :math:`p` can be found using long-term, historical data.

There are two important properties:

#.	The mean of the distribution for the rate happens to be the rate at which unusual events occur = :math:`\eta = np`
#.	The variance of the distribution is also :math:`\eta`. This property is particularly interesting - state in your own words what this implies.

Formally, the Poisson distribution can be written as :math:`\displaystyle \frac{e^{-\eta}\eta^{x}}{x!}`, with a plot as shown for :math:`\eta = 4`. Please note the lines are only guides, the probability is only defined at the integer values marked with a circle. 

.. image:: ../figures/univariate/poisson-distribution.png
	:align: center
	:scale: 50
	
:math:`p(x)` expresses the probability that there will be :math:`x` occurrences (must be an integer) of this rare event in the same interval of time or unit area as :math:`\eta` was measured.

*Example*: Equipment in a chemical plant can and will fail. Since it is a rare event, let's use the Poisson distribution to model the failure rates. Historical records on a plant show that a particular supplier's pumps are, on average, prone to failure in a month with probability :math:`p = 0.01` (1 in 100 chance of failure each month). There are 50 such pumps in use throughout the plant. *What is the probability that* either 0, 1, 3, 6, 10, or 15 *pumps will fail this year?* (Create a table)

	:math:`\eta = 12\,\frac{\displaystyle \text{months}}{\displaystyle \text{year}} \times 50\,\text{pumps} \times 0.01\,\frac{\displaystyle\text{failure}}{\displaystyle\text{month}} = 6\,\frac{\displaystyle\text{pump failures}}{\displaystyle\text{year}}`

	.. csv-table:: 
	   :header: :math:`x`, :math:`p(x)`
	   :widths: 30, 80

		0, 0.25% chance
		1, 1.5%
		3, 8.9
		6, 16%
		10, 4.1%
		15, 0.1%
		
.. code-block:: s

    > x <- c(0, 1, 3, 6, 10, 15)
    > dpois(x, lambda=6)    # Note: R calls the Poisson parameter 'lambda'
	[1] 0.0025 0.0149 0.0892 0.161 0.0413 0.001

.. _univariate_confidence_intervals:

Confidence intervals
====================

.. See code in yield-exercise.R for the R source code

.. index:: confidence interval

So far we have calculated point estimates of parameters, called statistics. In the last section in the :math:`t`-distribution we already calculated a confidence interval. In this section we formalize the idea, starting with an example.

*Example*: a new customer is evaluating your product, they would like a confidence interval for the impurity level in your sulphuric acid. You can tell them: "*the range from 429ppm to 673ppm contains the true impurity level with 95% confidence*". This is a compact representation of the impurity level. You could have told your potential customer that

	- the sample mean from the last year of data is 551 ppm
	- the sample standard deviation from the last year of data is 102 ppm
	- the last year of data are normally distributed

But a confidence interval conveys a similar concept, in a useful manner. It gives an estimate of the location and spread and uncertainty associated with that parameter (e.g. impurity level in this case).

Let's return to the previous viscosity example, where we had the 9 viscosity measurements ``23, 19, 17, 18, 24, 26, 21, 14, 18``. The sample average was :math:`\overline{x} = 20.0` and the standard deviation was :math:`s = 3.81`. The :math:`z`-value is: :math:`z = \dfrac{\overline{x} - \mu}{s/\sqrt{n}}`. And we showed this was distributed according to the :math:`t`-distribution with 8 degrees of freedom. 

Calculating a confidence interval requires we find a range within which that :math:`z`-value occurs. Most often we are interested in symmetrical confidence intervals, so the procedure is:

.. math::
	:label: CI-mean-variance-unknown-repeated
		
		\begin{array}{rcccl} 
		      - c_t                                  &\leq& z                                                   &\leq &  +c_t\\
			  - c_t                                  &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
			\overline{x}  - c_t \dfrac{s}{\sqrt{n}}  &\leq&  \mu                                                &\leq& \overline{x}  + c_t\dfrac{s}{\sqrt{n}} \\
			  \text{LB}                              &\leq&  \mu                                                &\leq& \text{UB}
		\end{array}
	
The critical values of :math:`c_t` are ``qt(1 - 0.05/2, df=8) = 2.306004`` when we used the 95% confidence interval (2.5% in each tail). We calculated that LB = 20.0 - 2.92 = 17.1 and that UB = 20.0 + 2.92 = 22.9.  

Interpreting the confidence interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: confidence interval; interpreting

-	The expression in :eq:`CI-mean-variance-unknown-repeated` should not be interpreted to mean that the viscosity is 20 units and lies inside the LB (lower-bound) to UB (upper-bound) range of 17.1 to 22.9 with a 95% probability. In fact, the sample mean lies exactly at the mid-point of the range with 100% certainty - that is how the range was calculated.

-	What the expression in :eq:`CI-mean-variance-unknown-repeated` **does imply** is that :math:`\mu` lies in this interval. The confidence interval is a range of possible values for :math:`\mu`, not for :math:`\overline{x}`. Confidence intervals are for parameters, not for statistics.
	
-	Notice that the upper and lower bounds are a function of the data sample used to calculate :math:`\overline{x}` and the number of points, :math:`n`. If we take a different sample of data, we will get different upper and lower bounds.
	
-	What does the level of confidence mean?  

		It is the probability that the true population viscosity, :math:`\mu` is in the given range. At 95% confidence, it means that 5% of the time the interval *will not contain* the true mean. So if we collected 20 sets of :math:`n` samples, 19 times out of 20 the confidence interval range **will contain** the true mean, but one of those 20 confidence intervals is expected not to contain the true mean.

-	What happens if the level of confidence changes?  Calculate the viscosity confidence intervals for 90%, 95%, 99%.

		.. csv-table:: 
		   :header: Confidence, LB, UB
		   :widths: 33, 33, 33

			90%, 17.6, 22.4
			95%, 17.1, 22.9
			99%, 15.7, 24.2			
			
		As the confidence value is increased, our interval widens, indicating that we have a more reliable region, but it is less precise.
			
..	TODO: show the confidence ranges, like BHH, p114 (1st edition)

-	What happens if the level of confidence is 100%?

		The confidence interval is then infinite. We are 100% certain this infinite range contains the population mean, however this is not a useful interval.

-	What happens if we increase the value of :math:`n`?

		As intuitively expected, as the value of :math:`n` increases, the confidence interval decreases in width.
		
-	Returning to the case above, where at the 95% level we found the confidence interval was :math:`[17.1; 22.9]` for the bale's viscosity. What if we were to analyze the bale thoroughly, and found the population viscosity to be 23.2. What is the probability of that occurring?

		Less than 5% of the time.

Confidence interval for the mean from a normal distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The aim here is to formalize the calculations for the confidence interval of :math:`\overline{x}`, given a sample of :math:`n` 

	a)	independent points, taken from 
	b)	the normal distribution. 

Be sure to check those two assumptions before going ahead.

There are 2 cases: one where you know the population standard deviation (unlikely), and one where you do not (the usual case). It is safer to use the confidence interval for the case when you do not know the standard deviation, as it is a more conservative (i.e. wider) interval.

The detailed derivation for the two cases was covered in earlier sections.

A. Variance is known
^^^^^^^^^^^^^^^^^^^^^

When the variance is known, the confidence interval is given by :eq:`CI-mean-variance-known-again` below, derived from this :math:`z`-deviate:  :math:`z = \dfrac{\overline{x} - \mu}{\sigma/\sqrt{n}}` back in :eq:`CI-mean-variance-known`

.. math::
		:label: CI-mean-variance-known-again
		
		\begin{array}{rcccl} 
			  - c_n                                      &\leq& z                                                        &\leq &  +c_n\\
			  - c_n                                      &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}} &\leq &  +c_n\\
			\overline{x}  - c_n \dfrac{\sigma}{\sqrt{n}} &\leq&  \mu                                                     &\leq& \overline{x}  + c_n\dfrac{\sigma}{\sqrt{n}} \\
			  \text{LB}                                  &\leq&  \mu                                                     &\leq& \text{UB}
		\end{array}

The values of :math:`c_n` are ``qnorm(1 - 0.05/2) = 1.96`` when we happen to use the 95% confidence interval (2.5% in each tail). 

B. Variance is unknown
^^^^^^^^^^^^^^^^^^^^^^

.. index::
	single: confidence interval; unknown variance

In the more realistic case when the variance is unknown we use equation :eq:`CI-mean-variance-unknown`, repeated here below. This is derived from the :math:`z`-deviate: :math:`z = \dfrac{\overline{x} - \mu}{s/\sqrt{n}}`:

.. math::
	:label: CI-mean-variance-unknown-again
		
	\begin{array}{rcccl} 
		  - c_n                                 &\leq& z                                                   &\leq &  +c_n\\
		  - c_t                                 &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
		\overline{x}  - c_t \dfrac{s}{\sqrt{n}} &\leq& \mu                                                 &\leq& \overline{x}  + c_t\dfrac{s}{\sqrt{n}} \\
		  \text{LB}                             &\leq& \mu                                                 &\leq& \text{UB}
	\end{array}
		
The values of :math:`c_t` are ``qt(1 - 0.05/2, df=...)`` when we use the 95% confidence interval (2.5% in each tail). This :math:`z`-deviate is distributed according to the :math:`t`-distribution, since we have additional uncertainty when using the standard deviation estimate, :math:`s`, instead of the population standard deviation, :math:`\sigma`.

Comparison
^^^^^^^^^^

If we have the fortunate case where our estimated variance, :math:`s^2`, is equal to the population variance, :math:`\sigma^2`, then we can compare the 2 intervals in equations :eq:`CI-mean-variance-known-again` and :eq:`CI-mean-variance-unknown-again`. The only difference would be the value of the :math:`c_n` from the normal distribution and :math:`c_t` from the :math:`t`-distribution. For typical values used as confidence levels, 90% to 99.9%, values of :math:`c_t > c_n` for any degrees of freedom. 

This implies the confidence limits are wider for the case when the standard deviation is unknown, leading to more conservative results, reflecting our uncertainty of the standard deviation parameter, :math:`\sigma`.

.. Plot these in R to verify:  plot(seq(0,1,0.01), qt(seq(0,1,0.01), df=2)); lines(seq(0,1,0.01), qnorm(seq(0,1,0.01)))

Testing for differences and similarity
========================================

.. index:: 
	single: tests for differences
	see: significant difference; tests for differences

These sort of questions often arise in data analysis:

	- We want to change to a cheaper material, B. Does it work as well as A?
	- We want to introduce a new catalyst B. Does it improve our product properties over the current catalyst A?
	
Either we want to confirm things are statistically the same, or confirm they have changed. Notice that in both the above cases we are testing the population mean (location). Has the mean shifted or is it the same?  There are also tests for changes in variance (spread), which we will cover. We will work with an example throughout this section. 

*Example*: A process operator needs to verify that a new form of feedback control on the batch reactor leads to improved yields. Yields under the current control system, A, are compared with yields under the new system, B. The last ten runs with system A are compared to the next 10 sequential runs with system B. The data are shown in the table, and shown in graphical form as well. (Note that the box plot uses the median, while the plots on the right show the mean.)  
 
.. image:: ../figures/univariate/system-comparison-boxplot-plots.png
	:scale: 60
	:align: center

.. wikicode for table:

	{| class="wikitable center"
	|-
	! Experiment number
	! Feedback system
	! Yield
	!
	! Experiment number
	! Feedback system
	! Yield
	|-                  
	| 1 || A ||  92.7 ||  || 11 || B || 83.5
	|-                     
	| 2 || A ||  73.3 ||  || 12 || B || 78.9
	|-                     
	| 3 || A ||  80.5 ||  || 13 || B || 82.7
	|-                     
	| 4 || A ||  81.2 ||  || 14 || B || 93.2
	|-                     
	| 5 || A ||  87.1 ||  || 15 || B || 86.3
	|-                     
	| 6 || A ||  69.2 ||  || 16 || B || 74.7
	|-                     
	| 7 || A ||  81.9 ||  || 17 || B || 81.6
	|-                     
	| 8 || A ||  73.9 ||  || 18 || B || 92.4
	|-                     
	| 9 || A ||  78.6 ||  || 19 || B || 83.6
	|-                     
	| 10 || A || 80.5 ||  || 20 || B || 72.4
	|-
	| colspan="7" | 
	|-
	| colspan="2" |Mean  || 79.89|| || colspan="2" | Mean || 82.93
	|-
	| colspan="2" |Standard deviation  || 6.81|| || colspan="2" | Standard deviation || 6.70
	|}

.. image:: ../figures/univariate/system-comparison-wikitable.png
	:align: center
	:scale: 75

We address the question of whether or not there was a *significant difference* between system A and B. A significant difference means that when system B is compared to a suitable reference, that we can be sure that the long run implementation of B will lead, in general, to an a different yield (%). We want to be sure that any change in the 10 runs under system B were not *only due to chance*, because system B will cost us $100,000 to install, and $20,000 in annual software license fees.

	*Note*: those with a traditional statistical background will recognize this section as one-sided hypothesis tests. We will only consider tests for a significant increase or decrease, i.e. one-sided tests, in this section. We use confidence intervals, rather than hypothesis tests; the results are exactly the same. Arguably the confidence interval approach is more interpretable, since we get a bound, rather that just a clear-cut yes/no answer.

There are two main ways to test for a significant increase or significant decrease.

Comparison to a long-term reference set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: long-term reference set

Continuing the above example we can compare the past 10 runs from system B with the 10 runs from system A. The average difference between these runs is :math:`\overline{x}_B - \overline{x}_A = 82.93 - 79.89 = 3.04` units of improved yield. Now, if we have a long-term reference data set available, we can compare if any 10 historical, sequential runs from system A, followed by another 10 historical, sequential runs under system A had a difference that was this great. If not, then we know that system B leads to a definite improvement, not likely to be caused by chance alone.

Here's the procedure:

	#.	Imagine that we have have 300 historical data points from this system, tabulated in time order: yield from batch 1, 2, 3 ... (the data are available on the `website <http://datasets.connectmv.com/info/batch-yields>`_).
	
	#.	Calculate the average yields from batches 1 to 10. Then calculate the average yield from batches 11 to 20. Notice that this is exactly like the experiment we performed when we acquired data for system B: two groups of 10 batches, with the groups formed from sequential batches.
	
	#.	Now subtract these two averages: (group average 11 to 20) minus (group average 1 to 10).
	
	#.	Repeat steps 2 and 3, but use batches 2 to 11 and 12 to 21. Repeat until all historical batch data are used up, i.e. batches 281 to 290 and 291 to 300. The plot below can be drawn, one point for each of these difference values.
	
		.. image:: ../figures/univariate/system-comparison-dotplot-grouped.png
			:align: center
			:scale: 100
	
The vertical line at 3.04 is the difference value recorded between system B and system A.  From this we can see that historically, there were 31 out of 281 batches, about 11% of historical data, that had a difference value of 3.04 or greater. So there is a 11% probability that system B was better than system A purely by chance, and not due to any technical superiority. Given this information, we can now judge, if the improved control system will be economically viable and judge, based on internal company criteria, if this is a suitable investment, also considering the 11% risk that our investment will fail.

Notice that no assumption of independence or any form of distributions was required for this work!   The only assumption made is that the historical data are relevant. We might know this if, for example, no substantial modification was made to the batch system for the duration over which the 300 samples were acquired. If however, a different batch recipe were used for sample 200 onwards, then we may have to discard those first 200 samples: it is not fair to judge control system B to the first 200 samples under system A, when a different operating procedure was in use.

So to summarize: we can use a historical data set if it is relevant. And there are no assumptions of independence or shape of the distribution, e.g. a normal distribution.

In fact, for this example, the data were not independent, they were autocorrelated. There was a relationship from one batch to the next: :math:`x[k] = \phi x[k-1] + a[k]`, with :math:`\phi = -0.3`, and  :math:`a[k] \sim \mathcal{N}\left(\mu=0, \sigma^2=6.7^2\right)`. You can simulate your own set of autocorrelated data using this R code:

.. code-block:: s

	N <- 300
	phi <- -0.3
	spread <- 6.7
	location <- 79.9
	A.historical <- numeric(N)   # create a vector of zeros
	for (k in 2:N)
	{
	   A.historical[k] <- phi*(A.historical[k-1]) + rnorm(1, mean=0, sd=spread)
	}
	A.historical <- A.historical + location

We can visualize this :index:`autocorrelation` by plotting the values of :math:`x[k]` against :math:`x[k+1]`:

.. image:: ../figures/univariate/system-comparison-autocorrelation-scatterplot.png
	:align: center
	:scale: 60
	
We can immediately see the data are **not independent**, because the slope is non-zero.

.. _univariate-group-to-group-differences-no-reference-set:

Comparison when a reference set is not available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A reference data set may not always be available, only the data from the 20 experimental runs (10 from system A and 10 from B). We can proceed to compare the data, but we will require a strong assumption of random sampling (independence), which is often not valid in engineering data sets. Fortunately, engineering data sets are usually large - we are good at collecting data - so the methodology in the preceding section on using a reference set, is greatly preferred, when possible.

How could the assumption of independence (random sampling) be made more realistically?  How is the :index:`lack of independence <single: independence; lack of>` detrimental?  We show below that the assumption of independence is made twice: the samples within group A and B must be independent; furthermore, the samples between the groups should be independent. But first we have to understand why the assumption of independence is required, by understanding the usual approach for estimating if differences are significant or not.

The usual approach for assessing if the difference between :math:`\overline{x}_B - \overline{x}_A` is significant follows this approach:

	#.	Assume the data for sample A and sample B have been independently sampled from their respective populations.
	
	#.	Assume the data for sample A and sample B have the same population variance, :math:`\sigma_A = \sigma_B = \sigma` (there is a test for this, see the next section).
	
	#.	Let the sample A have population mean :math:`\mu_A` and sample B have population mean :math:`\mu_B`.
	
	#.	From the central limit theorem (this is where the assumption of independence of the samples within each group comes), we know that:

		.. math::
			:nowrap:
			
			\begin{alignat*}{2}
				\mathcal{V}\left\{\overline{x}_A\right\} = \frac{\sigma^2_A}{n_A} &\qquad\qquad & \mathcal{V}\left\{\overline{x}_B\right\} = \frac{\sigma^2_B}{n_B}
			\end{alignat*}
	
	#.	Assuming independence again, but this time between groups, this implies the average of each sample group is independent, i.e. :math:`\overline{x}_A` and :math:`\overline{x}_B` are independent of each other. This allows us to write:
	
		.. math::
		   :label: eq_add_variance_1
		
				\mathcal{V}\left\{\overline{x}_B - \overline{x}_A\right\} = \frac{\sigma^2}{n_A} + \frac{\sigma^2}{n_B} = \sigma^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)
				
		..	For a full proof of this result, please see :eq:`eq_add_variance_2`.

	#.	Using the central limit theorem, even if the samples in A and the samples in B are non-normal, the sample averages :math:`\overline{x}_A` and :math:`\overline{x}_B` will be much more normal, even for small sample sizes. So the difference between these means will also be more normal: :math:`\overline{x}_B - \overline{x}_A`. Now express this difference in the form of a :math:`z`-deviate (:index:`standard form`):

		.. math::
			:label: zvalue-for-difference

				z = \frac{(\overline{x}_B - \overline{x}_A) - (\mu_B - \mu_A)}{\sqrt{\sigma^2 \left(\displaystyle \frac{1}{n_A} + \frac{1}{n_B}\right)}}
				
	 	We could ask, what is the probability of seeing a :math:`z` value from equation :eq:`zvalue-for-difference` of that magnitude?  Recall that this :math:`z`-value is the equivalent of :math:`\overline{x}_B - \overline{x}_A`, expressed in deviation form, and we are interested if this difference is due to chance. So we should ask, what is the probability of getting a value of :math:`z` **greater** than this, or **smaller** that this, depending on the case? 
		
		The only question remains is what is a suitable value for :math:`\sigma`?  As we have seen before, when we have a large enough reference set, then we can use the value of :math:`\sigma` from the historical data, called an *external estimate*. Or we can use an *internal estimate* of spread; both approaches are discussed below.
	

..	ON USING CONFIDENCE INTERVAL  #. A confidence limit for :math:`z` can be formed, and if this limit includes zero, then we have some evidence that there may not be long term improvement, i.e. we have some evidence that :math:`\mu_B - \mu_A` may be zero. 

				.. math::
					:nowrap:
						\begin{alignat*}{4}
							(\overline{x}_B - \overline{x}_A) - c_n \sqrt{\sigma^2 \left(\displaystyle \frac{1}{n_A} + \frac{1}{n_B}\right)}  &\qquad<\qquad& \mu_B - \mu_A &\qquad<\qquad& (\overline{x}_B - \overline{x}_A) + c_n \sqrt{\sigma^2 \left(\displaystyle \frac{1}{n_A} + \frac{1}{n_B}\right)}
						\end{alignat*}


		 		The value for :math:`c_n` is determined by confidence level, and is taken from the normal distribution (e.g. :math:`c_n` = ``qnorm(0.975)`` for a 95% confidence limit).
		
		HOWEVER, DO NOT INTRODUCE it with this example, because this example is actually a one-sided t-test, where as the CI is usually 2-sided. To introduce a 1-sided CI in addition to the other topics is a mess.
	
	
Now we know the approach required, using the above 6 steps, to determine if there was a significant difference. And we know the assumptions that are required: normally distributed and independent samples. But how can we be sure our data are independent?  This is the most critical aspect, so let's look at a few cases and discuss, then we will return to our example and calculate the :math:`z`-values with both an *external* and *internal* estimate of spread.

Discuss whether these experiments would lead to :index:`independent data <single: independence>` or not, and how we might improve the situation.

	a)	We are testing a new coating to repel moisture. The coating is applied to packaging sheets that are already hydrophobic, however this coating enhances the moisture barrier property of the sheet. In the lab, we take a large packaging sheet and divide it into 16 blocks. We coat the sheet as shown in the figure and then use the :math:`n_A=8` and :math:`n_B=8` values of hydrophobicity to judge if coating B is better than coating A.
	
		.. image:: ../figures/univariate/sheet-coating-application.png
			:align: center
			:scale: 50
		
		Some problems with this approach:
		
		-	The packaging sheet to which the new coating is applied may not be uniform. The sheet is already hydrophobic, but the hydrophobicity is probably not evenly spread over the sheet, nor are any of the other physical properties of the sheet. When we measure the moisture repelling property with the different coatings applied, we will not have an accurate measure of whether coating A or B worked better. We must randomly assign blocks A and B on the packaging sheet. 
			
		-	Even so, this may still be inadequate, because what if the packaging sheet selected has overly high or low hydrophobicity (i.e. it is not representative of regular packaging sheets). What should be done is that random packaging sheets should be selected, and they should be selected across different lots from the sheet supplier (sheets within one lot are likely to be more similar than between lots). Then on each sheet we apply coatings A and B, in a random order on each sheet.
		
		-	It is tempting to apply coating A and B to one half of the various sheets and measure the *difference* between the moisture repelling values from each half. It is tempting because this approach would cancel out any base variation between difference sheets, as long as that variation is present across the entire sheet. Then we can go on to assess if this difference is significant. 
		
			There is nothing wrong with this methodology, however, there is a different, specific test for paired data, covered in a :ref:`later section <univariate_paired_tests>`. If you use the above test, you violate the assumption in step 5, which requires that :math:`\overline{x}_A` and :math:`\overline{x}_B` be independent. Values within group A and B are independent, but not their sample averages, because you cannot calculate :math:`\overline{x}_A` and :math:`\overline{x}_B` independently.
	
	b)	We are testing an alternative, cheaper raw material in our process, but want to be sure our product's final properties are unaffected. Our raw material dispensing system will need to be modified to dispense material B. This requires the production line to be shut down for 15 hours while the new dispenser, lent from the supplier, is installed. The new supplier has given us 8 representative batches of their new material to test, and each test will take 3 hours. We are inclined to run these 8 batches over the weekend: set up the dispenser on Friday night (15 hours), run the tests from Saturday noon to Sunday noon, then return the line back to normal for Monday's shift. How might we violate the assumptions required by the data analysis steps above when we compare 8 batches of material A (collected on Thursday and Friday) to the 8 batches from material B (from the weekend)?  What might we do to avoid these problems?
	
		-	The 8 tests are run sequentially, so **any changes** in conditions between these 8 runs and the 8 runs from material A will be confounded (confused) in the results. List some actual scenarios how confounding between the weekday and weekend experiments occur:
	
			-	For example, the staff running the equipment on the weekend are likely not the same staff that run the equipment on weekdays. 
			
			-	The change in the dispenser may have inadvertently modified other parts of the process, and in fact the dispenser itself might be related to product quality. 
			
			-	The samples from the tests will be collected and only analyzed in the lab on Monday, whereas the samples from material A are usually analyzed on the same day: that waiting period may degrade the sample. 
			
		 This confounding with all these other, potential factors means that we will not be able to determine whether material B caused a true difference, or whether it was due to the other conditions.
		
		-	It is certainly expensive and impractical to randomize the runs in this case. Randomization would mean we randomly run the 16 tests, with the A and B chosen in random order, e.g. ``A B A B A A B B A A B B B A B A``. This particular randomization sequence would require changing the dispenser 9 times. 

		-	One suboptimal sequence of running the system is ``A A A A B B B B A A A A B B B B``. This requires changing the dispenser 4 times (one extra change to get the system back to material A). We run each (``A A A A B B B B``) sequence on two different weekends, changing the operating staff between the two groups of 8 runs, making sure the sample analysis follows the usual protocols: so  we reduce the chance of confounding the results. 

Randomization might be expensive and time-consuming in some studies, but it is the insurance we require to avoid being misled. These two examples demonstrate this principle: **block what you can and randomize what you cannot**. We will review these concepts again in the :ref:`design and analysis of experiments section <SECTION-design-analysis-experiments>`. If the change being tested is expected to improve the process, then we must follow these precautions to avoid a process upgrade/modification  that does not lead to the expected improvement; or the the converse - a missed opportunity of implementing a change for the better.

External and internal estimates of spread
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So to recap the progress so far, we are aiming to test if there is a *significant, long-term difference* between two systems: A and B. We showed the most reliable way to test this difference is to compare it with a body of historical data, with the comparison made in the same way as when the data from system A and B were acquired; this requires no additional assumptions, and even allows one to run experiments for system B in a **non-independent** way.

But, because we do not always have a large and relevant body of data available, we can calculate the difference between A and B and test if this difference could have occurred by chance alone. For that we use equation :eq:`zvalue-for-difference`, but we need an estimate of the spread, :math:`\sigma`.

.. Then, because we do not always have a large, relevant body of data available, we can calculate the difference between A and B and test if this difference lies in a confidence interval that includes zero. We highlighted several assumptions required to generate this confidence interval, noting that these assumptions are quite demanding.

	.. math::
		:nowrap:
		\begin{alignat*}{4}
			(\overline{x}_B - \overline{x}_A) - c_n \sqrt{\sigma^2 \left(\displaystyle \frac{1}{n_A} + \frac{1}{n_B}\right)}  &\qquad<\qquad& \mu_B - \mu_A &\qquad<\qquad& (\overline{x}_B - \overline{x}_A) + c_n \sqrt{\sigma^2 \left(\displaystyle \frac{1}{n_A} + \frac{1}{n_B}\right)}
		\end{alignat*}
	
	.. todo:: this is a one-sided :math:`t`-test: why is the CI symmetric?
	
.. AS BEFORE, DO NOT use confidence limits here. Perhaps if you rework the example to be one where we test for no-difference, then a CI would work nicely.

**External estimate of spread**

The question we turn to now is what value to use for :math:`\sigma`  in equation :eq:`zvalue-for-difference`. We got to that equation by assuming we have no historical, external data. But what if we did have some external data?  We could at least estimate :math:`\sigma` from that.  For example, the 300 historical batch yields has :math:`\sigma = 6.61`:


.. At the 95% confidence level: IGNORE THIS SECTION FOR NOW

	.. math::
		:nowrap:
		\begin{alignat*}{3}
			(82.93-79.89) - 1.96 \sqrt{6.61^2 \left(\displaystyle \frac{1}{10} + \frac{1}{10}\right)}  &\qquad<\qquad \mu_B - \mu_A &\qquad<\qquad& (82.93-79.89) + 1.96 \sqrt{6.61^2 \left(\displaystyle \frac{1}{10} + \frac{1}{10}\right)} \\
			-2.75  &\qquad<\qquad \mu_B - \mu_A &\qquad<\qquad& 8.83
		\end{alignat*}
		
.. AGAIN, avoid using CI's here
	
Check the probability of obtaining the :math:`z`-value in :eq:`zvalue-for-difference` by using the hypothesis that the value :math:`\mu_B - \mu_A = 0`. In other words we are making a statement, or a test of significance. Then we calculate this :math:`z`-value and its associated *cumulative probability*:

.. math::
	:nowrap:
	
	\begin{alignat*}{2}
	    z &= \dfrac{(\overline{x}_B - \overline{x}_A) - (\mu_B - \mu_A)}{\sqrt{\sigma^2 \left( \dfrac{1}{n_A} + \dfrac{1}{n_B}\right)}} \\
		z &= \dfrac{(82.93-79.89) - (\mu_B - \mu_A)}{\displaystyle \sqrt{6.61^2 \left(\displaystyle \frac{1}{10} + \frac{1}{10}\right)}} \\
		z &= \dfrac{3.04 - 0}{2.956} = {\bf 1.03}
	\end{alignat*}
	
	
The probability of seeing a :math:`z`-value from :math:`-\infty` up to 1.03 is 84.8% (use the ``pnorm(1.03)`` function in R). But we are interested in the probability of obtaining a :math:`z`-value **larger** than this. Why?  Because :math:`z=0` represents no improvement, and a value of :math:`z<0` would mean that system B is worse than system A. So what are the chances of obtaining :math:`z=1.03`?  It is (100-84.8)% = 15.2%, which means that system B's performance could have been obtained by pure luck in 15% of cases. 

We interpret this number in the summary section, but let's finally look at what happens if we have no historical data - then we generate an *internal* estimate of :math:`\sigma` from the 20 experimental runs alone.

**Internal estimate of spread**

The sample variance from each system was :math:`s_A^2 = 6.81^2` and :math:`s_B^2 = 6.70^2`, and in this case it happened that :math:`n_A = n_B = 10`, although the sample sizes do not necessarily have to be the same.

If the variances are comparable (there is a :ref:`test for that below <univariate_pooled_variance>`), then we can calculate a pooled variance, :math:`s_P^2`, which is a weighted sum of the sampled variances:

.. math:: 
	:label: pooled-variance

	s_P^2 &= \frac{(n_A -1) s_A^2 + (n_B-1)s_B^2}{n_A - 1 + n_B - 1} \\
	s_P^2 &= \frac{9\times 6.81^2 + 9 \times 6.70^2}{18} \\
	s_P^2 &= 45.63

Now using this value of :math:`s_P` instead of :math:`\sigma` in :eq:`zvalue-for-difference`:

.. math::
 

	z &= \frac{(\overline{x}_B - \overline{x}_A) - (\mu_B - \mu_A)}{\sqrt{\sigma^2 \left(\displaystyle \frac{1}{n_A} + \frac{1}{n_B}\right)}} \\
	  &= \frac{(82.93 - 79.89) - (\mu_B - \mu_A)}{\sqrt{s_P^2 \left(\displaystyle \frac{1}{10} + \frac{1}{10}\right)}} \\
	  &= \frac{3.04 - 0}{\sqrt{45.63 \times 2/10}} \\
	z  &= {\bf 1.01}

..	TODO: add the equation for the confidence interval here

The probability of obtaining a :math:`z`-value greater than this can be calculated as 16.3% using the :math:`t`-distribution with 18 degrees of freedom (use ``1-pt(1.01, df=18)`` in R). We use a :math:`t`-distribution because an estimate of the variance is used, :math:`s_p^2`, not a population variance, :math:`\sigma^2`. 

As an aside: we used a normal distribution for the external :math:`\sigma` and a :math:`t`-distribution for the internal :math:`s`. Both cases had a similar value for :math:`z` (compare :math:`z = 1.01` to :math:`z = 1.03`). Note however that the probabilities are higher in the :math:`t`-distribution's tails, which means that even though we have similar :math:`z`-values, the probability is greater: 16.3% against 15.2%. While this difference is not much from a practical point of view, it illustrates the difference between the :math:`t`-distribution and the normal distribution.

The results from this section were achieved by only using the 20 experimental runs, no external data. However, it made some strong assumptions: 

	-	The variances of the two samples are comparable, and can :ref:`therefore be pooled <univariate_pooled_variance>` to provide an estimate of :math:`\sigma`.
	 
	-	The usual assumption of independence within each sample is made (which we know not to be true for many practical engineering cases).
	
	-	The assumption of independence between the samples is also made (this is more likely to be true in this example, because the first runs to acquire data for A are not likely to affect the runs for system B).
	
	-	Each sample, A and B, is assumed to be normally distributed.

Summary and comparison of methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's compare the 3 estimates. Recall our aim is to convince ourself/someone that system B will have better long-term performance than the current system A. 

If we play devil's advocate, our *null hypothesis* is that system B has no effect. Then it is up to us to prove, convincingly, that the change from A to B has a systematic, permanent effect. That is what the calculated probabilities represent :, the probability of us being wrong.

	#.	Using only reference data: 11% (about 1 in 10)
	
	#.	Using the 20 experimental runs, but an external estimate of :math:`\sigma`: 15.2% (about 1 in 7)
	
	#.	Using the 20 experimental runs only, no external data: 16.3% (about 1 in 6)

The reference data method shows that the trial with 10 experiments using system B could have actually been taken from the historical data with a chance of 11%. A risk adverse company may want this number to be around 5%, or as low as 1% (1 in 100), which essentially guarantees the new system will have better performance. 

When constructing the reference set, we have to be sure the reference data are appropriate. Were the reference data acquired under conditions that were similar to the time in which data from system B were acquired?  In this example, they were, but in practice, careful inspection of plant records must be made to verify this.

The other two methods mainly use the experimental data, and provide essentially the same answer *in this case study*, though that is not always the case. The main point here is that our experimental data are usually not independent. However, by careful planning, and expense, we can meet the requirement of independence by randomizing the order in which we acquire the data. Randomization is the insurance (cost) we pay so that we do not have to rely of a large body of prior reference data. But in some cases it is not possible to randomize, so blocking is required. More on blocking in the :ref:`design of experiments section <DOE_blocking_section>`.

.. _univariate_paired_tests:

Paired tests
============

.. Verify this section against other notes.

.. index::
	single: two treatments

A :index:`paired test` is a test that is run twice on the same object or batch of materials. You might see the nomenclature of "two treatments" being used in the literature. For example: 

	-	A drug trial could be run in two parts: each person randomly receives a placebo or the drug, then 3 weeks later they receive the opposite, for another 3 weeks. Tests are run at 3 weeks and 6 weeks and the difference in the test result is recorded.
	
	-	We are testing two different additives, A and B, where the additive is applied to a base mixture of raw materials. Several raw material lots are received from various suppliers, supposedly uniform. Split each lot into 2 parts, and run additive A and B on each half. Measure the outcome variable, e.g. conversion, viscosity, or whatever the case might be, and record the difference.
	
	-	We are testing a new coating to repel moisture. The coating is applied to randomly selected sheets in a pattern [A|B] or [B|A] (the pattern choice is made randomly). We measure the repellent property value and record the difference.
	
.. Is this really a paired test? A new polymer is tested for surgical gloves. Physicians are randomly assigned a glove with the new polymer on one hand and the current polymer on the other hand. There is no visual difference.

In each case we have a table of :math:`n` samples recording the **difference values**. The question now is whether the difference is significant, or is it essentially zero?

The advantage of the paired test is that any :index:`systematic error` in our measurement system, what ever it might be, is removed as long as that error is consistent. Say for example we are measuring blood pressure, and the automated blood pressure device has a bias of -5 mmHg. This systematic error will cancel out when we subtract the 2 test readings. In the example of the raw materials and additives: any variation in the raw materials and its (unintended) effect on the outcome variable of interest will be cancelled.

The disadvantage of the paired test is that we lose degrees of freedom. Let's see how:

	#.	Calculate the :math:`n` differences: :math:`w_1 = x_{B,1} - x_{A,1}; w_2 = x_{B,2} - x_{A,2}, \ldots` to create the sample of values :math:`\mathbf{w} = [w_1, w_2, \ldots, w_n]`
	
	#.	Assume these values, :math:`w_i`, are independent, because they are taken on independent objects (people, base packages, sheets of paper, *etc*)
	
	#.	Calculate the mean, :math:`\overline{w}` and the standard deviation, :math:`s_w`, of these :math:`n` difference values. 
	
	#.	What do we need to assume about the population from which :math:`w` comes?  Nothing. We are not interested in the :math:`w` values, we are interested in :math:`\overline{w}`. OK, so what distribution would values of :math:`\overline{w}` come from?  By the central limit theorem, the :math:`\overline{w}` values should be normally distributed as :math:`\overline{w} \sim \mathcal{N}\left(\mu_w, \sigma_w^2/n \right)`, where :math:`\mu_w = \mu_{A-B}`.
	
	#.	Now calculate the :math:`z`-value, but use the sample standard deviation, instead of the population standard deviation.
	
		.. math::			
			z = \frac{\overline{w} - \mu_w}{s_w / \sqrt{n}}
			
	#.	Because we have used the sample standard deviation, :math:`s_w`, we have to use to the :math:`t`-distribution with :math:`n-1` degrees of freedom, to calculate the critical values.
	
	#.	We can calculate a confidence interval, below, and if this interval includes zero, then the change from treatment A to treatment B had no effect.

		.. math::		
			\overline{w} - c_t \frac{s_w}{\sqrt{n}} < \mu_w < \overline{w} + c_t \frac{s_w}{\sqrt{n}}
			
		The value of :math:`c_t` is taken from the :math:`t`-distribution with :math:`n-1` degrees of freedom at the level of confidence required: use the ``qt(...)`` function in R to obtain the values of :math:`c_t`.

The :index:`loss of degrees of freedom <single: degrees of freedom; loss of>` can be seen when we use exactly the same data and treat the problem as one where we have :math:`n_A` and :math:`n_B` samples in groups A and B and want to test for a difference between :math:`\mu_A` and :math:`\mu_B`. You are encouraged to try this out. There are more degrees of freedom, :math:`n_A + n_B - 2` in fact when we use the :math:`t`-distribution with the pooled variance from equation :eq:`pooled-variance`. Compare this to the case just described above where there are only :math:`n` degrees of freedom.
	
.. This example illustrates:
.. todo:: example showing loss of DOF (boys shoes example in BHH2). particularly, show the plots (p98 on BHH2- edition 1)


Other confidence intervals
====================================

There are several other confidence intervals that you might come across in your career. We merely mention them here and don't cover their derivation. What is important is that you understand *how* to interpret a confidence interval.  Hopefully the previous discussion achieved that.

.. _univariate_CI_variance:

Confidence interval for the variance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: confidence interval; for variance

This confidence interval finds a region in which the normal distribution's variance parameter, :math:`\sigma`, lies. The range is obviously positive, since variance is a positive quantity. For reference, this range is:

.. math::
	\left[\frac{(n-1)S^2}{\chi^2_{n-1, \alpha/2}} \quad\text{to}\quad \frac{(n-1)S^2}{\chi^2_{n-1, 1-\alpha/2}} \right]

-	:math:`n` is the number of samples
-	:math:`S^2` is the sample variance
-	:math:`\chi^2_{n-1, \alpha/2}` are values from the :math:`\chi^2` distribution with :math:`n-1` and :math:`\alpha/2` degrees of freedom 
-	:math:`1-\alpha`: is the level of confidence, usually 95%, so :math:`\alpha = 0.05` in that case.

.. todo: give some R code still

.. _univariate_pooled_variance:

Confidence interval for the ratio of two variances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: pooled variances
	
.. index:: 
	single: confidence interval; ratio of variances

One way to test whether we can pool (combine) two variances, taken from two different normal distributions, is to construct the ratio: :math:`\dfrac{s^2_1}{s^2_2}`. We can construct a confidence interval, and if this interval contains the value of 1.0, then we have no evidence to presume they are different (i.e. we can assume the two population variances are similar).

.. math::	
	:nowrap:
	
	\begin{alignat*}{4}
		  F_{\alpha/2, \nu_1, \nu_2}\dfrac{s_2^2}{s_1^2} &\qquad<\qquad& \dfrac{\sigma_2^2}{\sigma_1^2} &\qquad<\qquad& F_{1-\alpha/2, \nu_1, \nu_2}\dfrac{s_2^2}{s_1^2}
	\end{alignat*}

where we use :math:`F_{\alpha/2, \nu_1, \nu_2}` to mean the point along the cumulative :math:`F`-distribution which has area of :math:`\alpha/2` using :math:`\nu_1` degrees of freedom for estimating :math:`s_1` and :math:`\nu_2` degrees of freedom for estimating :math:`s_2`. For example, in R, the value of :math:`F_{0.05/2, 10, 20}` can be found from ``qf(0.025, 10, 20)`` as 0.2925. The point along the cumulative :math:`F`-distribution which has area of :math:`1-\alpha/2` is denoted as :math:`F_{1-\alpha/2, \nu_1, \nu_2}`,  and :math:`\alpha` is the level of confidence, usually :math:`\alpha = 0.05` to denote a 95% confidence level.

.. Source: Devore, Probability and Statistics, 5th edition, p.392-395

Confidence interval for proportions: the binomial proportion confidence interval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: 
	single: confidence interval; for proportions

Sometimes we measure the proportion of successes (passes). For example, if we take a sample of :math:`n` independent items from our production line, and with an inspection system we can judge pass or failure. The proportion of passes is what is important, and we wish to construct a confidence region for the population *proportion*. This allows one to say the population proportion of passes lies between the given range. As in *the proportion of packaged pizzas with 20 or more pepperoni slices is between 86 and 92\%*.

Incidentally, it is this confidence interval that is used in polls to judge the proportion of people that prefer a political party. One can run this confidence interval backwards and ask: how many independent people do I need to poll to achieve a population proportion that lies within a range of :math:`\pm 2\%`, 19 times out of 20?  The answer actually is function of the poll result!  But the worst case scenario is a split-poll, and that requires 2400 respondents.

.. Hypothesis tests; test of significance
	=======================================

	A confidence interval gives an engineer a sense of the precision of a parameter from a distribution. The engineer can then use their judgement to determine if that confidence interval is important to them or not. For example, knowing that your plastic product has a melting point of 455K to 495K, with 95% probability, can be used by your customer, e.g. 3M, to judge whether that product is suitable in their extruders. 

	A hypothesis test, or test of significance as it is also known, is use to make a statement, and then verify that statement. For example, 3M could say, we tried 8 samples of your plastic, and the average melting point for the 8 samples was 500K. Is that normal?  You product specification says your melting point is in the range 455K to 495K, with 95% probability. 

	 455K to 495K. So then you go perform a hypothesis test to verify if 500K is reasonable. Your hypothesis is that 500K is not unusual. The alternative hypothesis is that 500K is unusual.

	  What is the significance level?  How do you get to a test statistic?
	  You must present strong evidence to 

	reject that statement (hypothesis), otherwise it is accepted; sometimes we are prone to say this with a double-negative: "*there is no evidence to show that the melting point is not 472K*". 

	Hypothesis tests always work in this way:

		#. Specify your *null hypothesis*, a statement of what you want to test: the melting point is 472K. The null hypothesis will be accepted as long as there is no evidence to show otherwise.
		#. Specify an alternative hypothesis, which will be accepted if you do have evidence to reject (disprove) the null hypothesis. The alternative hypothesis is not always the opposite of the null hypothesis, though it may be. We'll see some examples shortly.
		#. Specify a level of significance, a low probability number that indicates the threshold between a significant and insignificant difference, e.g. :math:`p = 0.05`. This number represents the strength of evidence we require
		#. Then construct a test statistic, which is a function of the sampled data that ....
		#. And define a rejection region, which is a region for the test statistic's values that will result in you rejecting the null hypothesis.
	
		.. todo:: how does this level change our answer as it varies?

.. _univariate_statistical_tables:

.. index::
	single: statistical tables
	single: normal distribution; table for
	single: t-distribution; table for

Statistical tables for the normal- and t-distribution
============================================================================

.. image:: ../figures/univariate/Statistical-tables/Statistical-tables.png
	:scale: 95
	:align: center

