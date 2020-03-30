Histograms and probability distributions
=========================================

.. youtube:: https://www.youtube.com/watch?v=oA5HgF1vmXE&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=5

.. index:: histograms, frequency distribution

The :ref:`previous section <univariate-about-variability>` has hopefully convinced you that variation in a process is inevitable. This section aims to show how we can visualize and quantify any variability in a recorded vector of data.

A histogram is a summary of the variation in a measured variable. It shows the *number* of samples that occur in a *category*: this is called a **frequency distribution**. For example: number of children born, categorized against their birth gender: male or female.

.. image:: ../figures/univariate/histogram-children-by-gender.png
	:scale: 35
	:align: left
	:width: 900px
	:alt: fake width

The raw data in the above example was a vector that consisted of 2739 text entries, with 1420 of them as ``Male`` and 1319 of them as ``Female``. In this case ``Female`` and ``Male`` represent the two categories.

Histograms make sense for categorical variables, but a histogram can also be derived from a continuous variable. Here is an example showing the mass of cartons of 1 kg of flour. The continuous variable, mass, is divided into equal-size bins that cover the range of the available data.  Notice how the packaging system has to overfill each carton so that the vast majority of packages weigh over 1 kg (what is the average package mass?). If the variability in the packaging system could be reduced - the spread of the data made narrower - then the histogram can be shifted to the left, thereby reducing overfill.

.. image:: ../figures/univariate/histogram-package-mass.png
	:scale: 50
	:align: center
	:width: 900px
	:alt: fake width

.. dcl:: R
	:height: 650px

	# Create 500 normally distributed points
	# with a mean of 1100 and standard deviation
	# of 50 units.
	data <- rnorm(500, mean=1100, sd=50)
	hist(data,
	     xlab="Mass [g] of each package",
	     ylab="Number of packages (N=500)")


Try creating a fictitious histogram for each of the following situations:

-	The grades for a class for a really easy test.
-	The numbers thrown from a 6-sided die.
-	The annual income for people in your country.
-   Analytical measurements taken in a laboratory, by the same person or computerized process.

.. - seeds with the same size later become plants of different heights and yield of fruit
.. - people born in the same year have lives of different duration due to environmental, genetic, health and societal factors
.. - games such as poker, roulette, lotteries, dice
.. - weight of corn seeds (average is 200mg)

In preparing the above histograms, what have you implicitly inferred about time-scales? These histograms show the long-term distribution (probabilities) of the system being considered. This is why *concepts of chance and random phenomena* can be use to described systems and processes. Probabilities can be used to describe our long-term expectations. Let us contrast some long-term and short-term expectations next:

-	The long-term sex ratio at birth 1.06:1 (boy:girl) is expected in Canada; but a newly pregnant mother would not know the sex.
-	The long-term data from a process shows an 85% output yield from our batch reactor; but tomorrow it could be 59% and the day after that 86%.
-	We know that a fair die has a 16.67% chance of showing a 4 when thrown, but we cannot predict the value of the next throw.

Even if we have complete mechanistic knowledge of our process, the concepts from probability and statistics are useful to summarize and communicate information about past behaviour, and the expected future behaviour.

Steps to creating a frequency distribution, illustrated with 4 examples, labelled A, B, C, and D.

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

		A.	number of metal pieces with appearance level "acceptable" and "unacceptable" are added up
		B.	number of pieces with defect level 1, 2, 3, 4 are counted
		C.	number of batches with yield inside each bin level are calculated 
		D.	number of temperature values inside each bin level are computed

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


.. dcl:: R
	:height: 450px

	# 1000 normally distributed values
	N <- 1000
	values <- rnorm(N)
	hist(values, freq=TRUE,  xlab="Random values",
		 cex.lab=1.5, cex.main=1.8, lwd=2,
		 cex.sub=1.8, cex.axis=1.8,
		 ylab=paste0("Frequency (N=",N,")"))
	hist(values, freq=FALSE, xlab="Random values",
		 cex.lab=1.5, cex.main=1.8, lwd=2,
		 cex.sub=1.8, cex.axis=1.8,
		 ylab="Relative density")

	# Compare the two plots: only the y-axis
	# changes but the general shape remains.


Some nomenclature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=FIuU1REQvRM&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=6

We review a couple of concepts that you should have seen in a prior statistical course or elsewhere. If unfamiliar, please type the word or concept in a search engine for more background.

.. _univariate-population:

**Population**

	A large collection of observations that *might* occur; a set of *potential* measurements. Some texts consider an infinite collection of observations, but a large number of observations is good enough.

.. We will use capital :math:`N` in this section to denote the :index:`population` size. WE USUALLY USE "N" as the sample size
.. We will use lowercase :math:`n` in this section to denote the :index:`sample` size.

**Sample**

	A collection of observations that have *actually* occurred; a set of *existing* measurements that we have recorded in some way, usually electronically.

	.. index::
		single: sample

	.. image:: ../figures/univariate/batch-yields.png
		:scale: 80
		:align: center

	In engineering applications where we have plenty of data, we can characterize the population from all available data. The figure here shows the viscosity of a motor oil, from all batches produced in the last 5 years (about 1 batch per day). These 1825 data points, though technically a *sample* are an excellent surrogate for the *population* viscosity because they come from such a long duration. Once we have characterized these samples, future viscosity values will likely follow that same distribution, provided the process continues to operate in a similar manner.

**Distribution**

	Distributions are used to summarize, in a compact way, a much larger collection of a much larger collection of data points. Histograms, just discussed above, are one way of visualizing a distribution. We can also express distributions by a few numerical parameters. See below.

**Probability**

	The area under a plot of relative frequency distribution is equal to 1. :index:`Probability <single: probability>` is then the fraction of the area under the frequency distribution curve (also called density curve).

	Superimpose a vertical line on your fictitious histograms you drew earlier to indicate:

	-	the probability of a test grades less than 80%;
	-	the probability that the number thrown from a 6-sided die is less than or equal to 2;
	-	the probability of someone's income exceeding $60000;
	-	the probability of the measurement exceeding a certain critical value.

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

	where :math:`N` represents the size of the entire population, and :math:`n` is the number of samples measured from the population.

	.. dcl:: R
		:height: 200px

		# A vector of 50 normally distributed
		# random numbers
		N <- 50
		x <- rnorm(N)
		mean(x)

		# Run the code several times, to check
		# that the mean is approximately 0
		# Check what the 'x' variable contains.


	This is only one of several statistics that describes your data: if you told your customer that the average density of your liquid product was 1.421 g/L, and nothing further, the customer might assume all lots of the same product have a density of 1.421 g/L. But we know from :ref:`our earlier discussion <univariate-about-variability>` that there will be variation. We need information, in addition to the mean, to quantify the distribution of values: *the spread*.

.. _univariate-variance:

**Variance (spread)**

	.. _univariate_calculate_variance:

	A measure of :index:`spread`, or :index:`variance`, is also essential to quantify your distribution.

	.. math::
		:nowrap:

	   	\begin{alignat*}{2}
	      	\text{Population variance}: &\qquad& \mathcal{V}\left\{x\right\} = \mathcal{E}\left\{ (x - \mu )^2\right\} = \sigma^2 &= \frac{1}{N}\sum{(x-\mu)^2} \\
			\text{Sample variance}:     &\qquad&                                                                             s^2  &= \frac{1}{n-1}\sum_{i=1}^{n}{(x_i - \overline{x})^2}
		\end{alignat*}

	Dividing by :math:`n-1` makes the variance statistic, :math:`s^2`, an unbiased estimator of the population variance, :math:`\sigma^2`. However, in many data sets our value for :math:`n` is large, so using a divisor of :math:`n`, which you might come across in computer software or other texts, rather than :math:`n-1` as shown here, leads to little difference.

	.. dcl:: R
		:height: 350px

		# A vector of 50 normally distributed
		# random numbers with a standard
		# deviation of 5
		N <- 50
		spread <- 5
		x <- rnorm(N, sd=spread)

		paste0('Standard deviation = ',
		       round(sd(x), 3))
		paste0('The variance is    = ',
		       round(var(x), 3))
		paste0('Square root of variance = ',
		       round(sqrt(var(x)), 3))

		# Run the code several times.


	The square root of variance, called the :index:`standard deviation` is a more useful measure of spread: it is easier to visualize on a histogram and has the advantage of being in the same units of measurement as the variable itself.

**Degrees of freedom**

	The denominator in the sample variance calculation, :math:`n-1`, is called the :index:`degrees of freedom`. We have one fewer than :math:`n` degrees of freedom, because there is a constraint that the sum of the deviations around :math:`\overline{x}` must add up to zero. This constraint is from the definition of the mean. However, if we knew what the sample mean was without having to estimate it, then we could subtract each :math:`x_i` from that value, and our degrees of freedom would be :math:`n`.

**Outliers**

	.. youtube:: https://www.youtube.com/watch?v=GlVNclR6UVo&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=7

	Outliers are hard to define precisely, but an acceptable definition is that an :index:`outlier` is a point that is unusual, given the context of the surrounding data. Another definition which is less useful, but nevertheless points out the problem of concretely defining what an outlier is, is this: "*An outlier - I know it when I see it!*"
	
	The following 2 sequences of numbers show the number **4024** that appears in the first sequence, has become an outlier in the second sequence. It is an outlier based on the surrounding context.

	* 4024, 5152, 2314, 6360, 4915, 9552, 2415, 6402, 6261
	* 4, 61, 12, 64, 4024, 52, -8, 67, 104, 24

.. _univariate-median:

.. index:: robust statistics

**Median (robust measure of location)**

	The :index:`median` is an alternative measure of :index:`location`. It is a sample statistic, not a population statistic, and is computed by sorting the data and taking the middle value (or average of the middle 2 values, for even :math:`n`). It is also called a robust statistic, because it is insensitive (robust) to outliers in the data.

	.. note::

		The median is the most robust estimator of the sample location: it has a breakdown of 50%, which means that just under 50% of the data need to be replaced with unusual values before the median breaks down as a suitable estimate. The mean on the other hand has a breakdown value of :math:`1/n`, as only one of the data points needs to be unusual to cause the mean to be a poor estimate. To compute the median in R, use the ``median(x)`` function on a vector ``x``.


	Governments will report the median income, rather than the mean, to avoid influencing the value with the few very high earners and the many low earners. The median income per person is a more fair measure of location in this case.

**Median absolute deviation, MAD (robust measure of spread)**

	A robust measure of :index:`spread` is the :index:`MAD`, the :index:`median absolute deviation <see: median absolute deviation; MAD>`.  The name is descriptive of how the MAD is computed:

	.. math::

			\text{mad}\left\{ x_i \right\} = c \cdot \text{median}\left\{ \| x_i - \text{median}\left\{ x_i \right\}  \|  \right\} \qquad\qquad \text{where}\qquad c = 1.4826

	The constant :math:`c` makes the MAD consistent with the standard deviation when the observations :math:`x_i` are normally distributed. The MAD has a :index:`breakdown point` of 50%, because like the median, we can replace just under half the data with outliers before the MAD estimate becomes unbounded. To compute the MAD in R, use the ``mad(x)`` function on a vector ``x``.

	.. dcl:: R
		:height: 500px

		# A vector of 500 normally distributed
		# random numbers

		x <- rnorm(500)

		paste0('Without any outliers:')
		paste0('Standard deviation = ', sd(x))
		paste0('The MAD is         = ', mad(x))
		print('These two should agree mostly')

		# Run it several times to verify that the
		# two are similar, when they are not
		# outliers

		# Now add a huge outlier:
		x[2] <- 9876
		paste0('But now add an outlier...')
		paste0('*Standard deviation = ', sd(x))
		paste0('*The MAD is         = ', mad(x))
		paste0('See how MAD is not affected.')

	Enrichment reading: read pages *1 to 8* of "`Tutorial to Robust Statistics <https://dx.doi.org/10.1002/cem.1180050103>`_", PJ Rousseeuw, *Journal of Chemometrics*, **5**, 1-20, 1991.


.. For each of the distributions:
.. #.	show a typical plot of the probability function :math:`p(x)` against the variable's value :math:`x`
.. #.	learn when to use that distribution (we will show some examples)
.. #.	know what the parameters of the distribution are
