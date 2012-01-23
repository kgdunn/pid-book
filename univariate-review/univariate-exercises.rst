Exercises
==========

.. index::
	pair: exercises; univariate data

.. question::

	Recall that :math:`\mu = \mathcal{E}(x) = \dfrac{1}{N}\sum{x}` and :math:`\mathcal{V}\left\{x\right\} = \mathcal{E}\left\{ (x - \mu )^2\right\} = \sigma^2 = \dfrac{1}{N}\sum{(x-\mu)^2}`. 

	#. What is the expected value thrown of a fair 6-sided die? (Note: plural of die is dice)
	#. What is the expected variance of a fair 6-sided die?
	
.. answer::
	:fullinclude: no 
	:short: 3.5; 2.92

	Often the mean and standard deviation of a uniform distribution are not actual values from the distribution, however the definitions for them hold:

	#. :math:`\mu = \mathcal{E}(x) = \dfrac{1}{N}\sum{x} = \dfrac{1}{6}(1+2+3+4+5+6) = \mathbf{3.5}`
	#. :math:`\mathcal{V}\left\{x\right\} = \mathcal{E}\left\{ (x - \mu )^2\right\} =  \dfrac{1}{N}\sum{(1-3.5)^2 + (2-3.5)^2 + (3-3.5)^2 + (4-3.5)^2 + (5-3.5)^2 + (6-3.5)^2} = 17.5/6 = \mathbf{2.92}`

	If you're feeling adventurous, you can simulate random dice rolls and verify your answers::

		> N = 10000
		> hist(as.integer(runif(N, 1, 7)))      # make sure you get a uniform distribution
		> mean(as.integer(runif(N, 1, 7)))      # 3.4929
		> var(as.integer(runif(N, 1, 7)))       # 2.885426

.. question::

	Characterizing a distribution: Compute the mean, median, standard deviation and MAD for salt content for the various soy sauces given `in this report <http://beta.images.theglobeandmail.com/archive/00245/Read_the_report_245543a.pdf>`_ (page 41) as described in the the article from the `Globe and Mail <http://www.theglobeandmail.com/life/health/salt-variation-between-brands-raises-call-for-cuts/article1299117/>`_ on 24 September 2009. Plot a box plot of the data and report the interquartile range (IQR). Comment on the 3 measures of spread you have calculated: standard deviation, MAD, and interquartile range.
	
	The raw data are given below in units of milligrams of salt per 15 mL serving::
		
			[460, 520, 580, 700, 760, 770, 890, 910, 920, 940, 960, 1060, 1100]

.. answer::
	:fullinclude: no 
	:short: IQR = 240 mg salt/15 mL serving

	.. literalinclude:: ../figures/univariate/soy-salt-content.R
	   :language: s
	   :lines: 1-11,13,15-

	.. image:: ../figures/univariate/soy-salt-content.png
		:width: 400px
		:scale: 50
	
	Note that the units of spread are the same as the variable being quantified. The IQR is 240 mg salt/15 mL serving. The standard deviation (202 mg salt/15 mL serving), and MAD (193 mg salt/15 mL serving), are 2 other ways to quantify the spread of the data.  Note that the IQR, for normally distributed data, will only be consistent if you divide the result by 1.349. Read the help for the ``IQR`` function in R for more details. Note from the code how the IQR is a *distance* between two points.

	In this example the numbers are mostly in agreement, because there are no major outliers. The MAD and IQR are two robust methods of quantifying spread, while the standard deviation is extremely sensitive to outliers - due to the squaring of residuals about the mean.  You can verify this by replacing one of the values and recalculating the numbers.

.. question::

	Give a reason why Statistics Canada reports the median income when reporting income by geographic area. Where would you expect the mean to lie, relative to the median?  Use `this table <http://www40.statcan.gc.ca/l01/cst01/famil107a-eng.htm>`_ to look up the income for Hamilton. How does it compare to Toronto?  And all of Canada?

.. answer::

	We described how easily the :ref:`mean is influenced by unusual data points <univariate-median>`. Take any group of people anywhere in the world, and there will always be a few who earn lots of money (not everyone can be the CEO, especially of a bank!). Also, since no one earns negative income, the distribution piles up at the left, with fewer people on the right. This implies that the mean will lie above the median, since 50% of the histogram area must lie below the median, by definition. A previous student pointed out that low income earners are less likely to file tax returns, so they are underrepresented in the data.

	Even though the median is a more fair way of reporting income, and :index:`robust <single: robustness; example>` to unusual earners (many low income earners, very few super-rich), I would prefer if Statistics Canada released a histogram - that would tell a lot more - even just the the MAD, or IQR would be informative. It was surprising that Hamilton showed higher median earnings per family than Toronto. I infer from this that there are more low income earners in Toronto and Canada than in Hamilton, but without the histograms it is hard to be sure. Also, I wasn't able to find exactly what StatsCan means by a family - did they include single people as a "family"?  Maybe there are more, wealthy singles in Toronto, but they are aren't included in the numbers. The median income *per person* would be a useful statistic to help judge that.

.. question::

	Use the data set on `raw materials <http://datasets.connectmv.com/info/raw-material-properties>`_.

		- How many variables in the data set?
		- How many observations?
		- The data are properties of a powder. Plot each variable, one at a time, and locate any outliers. R-users will benefit from `the R tutorial <http://connectmv.com/tutorials/r-tutorial/>`_ (see the use of the ``identify`` function).
		
.. answer::

	See the code below that generates the plots.  Outliers were identified by visual inspection of these plots. Recall an outlier is an unusual/interesting point, and a function of the surrounding data. You can use a box plot to locate *preliminary* outliers, but recognize that you are leaving the computer to determine what is unusual. Automated outlier detection systems work moderately well, but there is no substitute (yet!) for visual inspection of the data.

	The same few samples appear to be outliers in most of the variables.

	.. literalinclude:: ../figures/univariate/raw-materials-univariate-checks.R
	   :lines: 1-27
	   :language: s

	.. image:: ../figures/univariate/size1.png
		:width: 300px
		:scale: 40
	.. image:: ../figures/univariate/size2.png
		:width: 300px
		:scale: 40
	.. image:: ../figures/univariate/size3.png
		:width: 300px
		:scale: 40
	.. image:: ../figures/univariate/density1.png
		:width: 300px
		:scale: 40
	.. image:: ../figures/univariate/density2.png
		:width: 300px
		:scale: 40
	.. image:: ../figures/univariate/density3.png
		:width: 300px
		:scale: 40
	

.. question::

	Write a few notes on the purpose of feedback control, and its effect on variability of process quality.

.. answer::
	:fullinclude: no

	*	Purpose is to keep the process close to a desired set point (or mean).

	*	Sometimes used to maintain the process variability within a desired tolerance limit (or standard deviation).

	*	Lowers the variability of the process outputs (i.e., narrow the distribution) by actually introducing *greater* variability into the process, to counteract external variation in the the process inputs. For example, variation from the raw materials, or ambient conditions, such as seasonal temperature are process inputs.

	*	Feedback control allows us to move the process operation closer to targets, without less likelihood of deviation outside these limits. (In the next section on process monitoring we will learn how to track and quantify this).

.. question::

	Use the section on `Historical data <http://climate.weatheroffice.gc.ca/climateData/canada_e.html>`_ from Environment Canada's website and use the ``Customized Search`` option to obtain data for the ``HAMILTON A`` station from 2000 to 2009. Use the settings as ``Year=2000``, and ``Data interval=Monthly`` and request the data for 2000, then click ``Next year`` to go to 2001 and so on. 

		-	For each year from 2000 to 2009, get the total snowfall and the average of the ``Mean temp`` over the whole year (the sums and averages are reported at the bottom of the table).
		-	Plot these 2 variables against time
		-	Now retrieve the long-term averages for these data `from a different section of their website <http://climate.weatheroffice.gc.ca/climate_normals/index_e.html>`_ (use the same location, ``HAMILTON A``, and check that the data range is 1971 to 2000). Superimpose the long-term average as a horizontal line on your previous plot.
		-	**Note**: the purpose of this exercise is more for you to become comfortable with web-based data retrieval, which is common in most companies.
		-	**Note**: please use any other city for this question if you prefer.

.. answer::
	:fullinclude: no 
		
	.. Snow:     170.9, 94.1, 138.0, 166.2, 175.8, 218.4, 56.6, 182.4, 243.2,   avg=161.8
	.. MeanTemp: 7.6,   8.8,  8.8,   7.3,   7.7,   8.2,   9.1 , 8.2,  7.7

	These are the data, and the code to plot the results. The temperature for the last decade trended higher than the average for the prior 3 decades, 1971 to 2000.
 
	.. literalinclude:: ../figures/univariate/hamilton-weather-data.R
		:language: s
		:lines: 1-7,9-11,13,15-17


	.. image:: ../figures/univariate/snowfall-data.png
		:width: 750px
		:scale: 75
	
	.. image:: ../figures/univariate/temperature-data.png
		:width: 750px
		:scale: 75
	
.. question::

	Does the number of visits in the `website traffic <http://datasets.connectmv.com/info/website-traffic>`_ data set follow a normal distribution?  If so, what are the parameters for the distribution?  What is the likelihood that you will have between 10 and 30 visits to the website?
	
.. answer:: 
	:fullinclude: no 
	:short: These data are normally distributed according to the q-q plot.
	
	.. literalinclude:: ../figures/univariate/website-visits-univariate.R
		:language: s
		:lines: 1-19

	The above source code was used to generate these plots to answer the question. The data do appear to follow a normal distribution. This means we can calculate the mean and standard deviation from the data.

		-	Mean number of visits = 22 visits
		-	Standard deviation of the number of visits = 8.3 visits
		-	Probability that there are between 10 and 30 visits to the site each day: 75.3%
		
	We should use the :math:`t`-distribution to answer the last part, but at this stage we had not yet looked at the :math:`t`-distribution. However, the large number of observations (214) means the :math:`t`-distribution is no different than the normal distribution.


.. question::

	The ammonia concentration in your wastewater treatment plant is measured every 6 hours. The data for one year are available from the `dataset website <http://datasets.connectmv.com/info/ammonia>`_. 

	#.	Use a visualization plot to hypothesize from which distribution the data might come. Which distribution do you think is most likely? Once you've decided on a distribution, use a qq-plot to test your decision.
	#.	Estimate location and spread statistics assuming the data are from a normal distribution. You can investigate using the ``fitdistr`` function in R, in the MASS package.
	#.	What if you were told the measured values are not independent. How does it affect your answer?
	#.	What is the probability of having an ammonia concentration greater than 40 mg/L when:

		- you may use only the data (do not use *any* estimated statistics)
		- you use the estimated statistics for the distribution?
	
		**Note**: Answer this entire question using computer software to calculate values from the normal distribution. But also make sure you can answer the last part of the question by hand, (when given the mean and variance), and using a table of normal distributions.

.. answer::
	:fullinclude: no 
	
	.. literalinclude:: ../figures/univariate/ammonia-in-wastewater.R
		:language: s
	
	#.	When plotting a histogram, it seems that an appropriate distribution might be the normal distribution. A qq-plot shows it it mostly normal, apart from the right hand side tail (upper tail) which is slightly heavier, outside the given limits,  than would be found on the normal distribution. 
	
	#.	Assuming the data are normal, we can calculate the distribution's parameters as :math:`\overline{x} = \hat{\mu} = 36.1` and :math:`s= \hat{\sigma} = 8.52`.
	
	#.	The fact that the data are not independent is not an issue. To calculate estimates of the parameter's distribution (the mean and standard deviation) we do not need to assume independence. One way to see this: if I randomly reorder the data, I will still get the same value for the mean and standard deviation. The assumption of independence is required for the central limit theorem, but we have not used that theorem here.
		
	#.	The probability of having an ammonia concentration greater than 40 mg/L:
		
		-	When counting the fraction of the samples greater than 40 mg/L (i.e. we only use the data themselves): **3.44%** (see code)
		-	When using the estimated values of the mean and standard deviation from the normal distribution, we can calculate a :math:`z`-value, then find the area under the normal distribution corresponding to this :math:`z`: **3.23%** (see code)
		
			*Note*: We should use actually be using the :math:`t`-distribution, since we used *an estimate* of the population variance and not the true population variance to calculate :math:`z`. However, since the degrees of freedom, :math:`n-1 = 1439`, are so large, there is no practical difference in our answer.

.. question::

	We take a large bale of polymer composite from our production line and using good sampling techniques, we take 9 samples from the bale and measure the viscosity in the lab for each sample. These samples are independent estimates of the population (bale) viscosity. We will believe these samples follow a normal distribution (we could confirm this in practice by running tests and verifying that samples from any bale are normally distributed). Here are 9 sampled values: ``23, 19, 17, 18, 24, 26, 21, 14, 18``. 

		- The sample average
		- An estimate of the standard deviation
		- What is the distribution of the sample average, :math:`\overline{x}`? What are the parameters of that distribution?

	              *Additional information*: I use a group of samples and calculate the mean, :math:`\overline{x}`, then I take another group of samples and calculate another :math:`\overline{x}`, and so on. Those values of :math:`\overline{x}` are not going to be the same, but they should be similar. In other words, the :math:`\overline{x}` also has a distribution. So this question asks what that distribution is, and what its parameters are.

		- Construct an interval, symbolically, that will contain, with 95% certainty (probability), the population mean of the viscosity.

			*Additional information*: To answer this part, you should move everything to :math:`z`-coordinates first. Then you need to find the points :math:`-c` and :math:`+c` in the following diagram that mark the boundary for a 95% of the total area under the distribution. This region is an interval that will contain, with 95% certainty, the population mean of the viscosity, :math:`\mu`. Write your answer in form: :math:`\text{LB} < \mu < \text{UB}`.

			.. image:: ../figures/univariate/show-confidence-interval.png
				:width: 500px
				:scale: 50

		- Now assume that for some hypothetical reason we know the standard deviation of the bale's viscosity is :math:`\sigma=3.5` units, calculate the population mean's interval numerically.

			*Additional information*: In this part you are just finding the values of :math:`\text{LB}` and :math:`\text{UB}`
	
.. answer::  
	:fullinclude: no 
	:short: Average = 20, standard deviation = 3.81

	.. literalinclude:: ../figures/univariate/polymer-bale-samples.R
		:language: s
	
	-	Sample average = 20
	-	Sample standard deviation = 3.81
	-	By the central limit theorem, and if the samples are taken independently, the mean, :math:`\overline{x} \sim \mathcal{N}\left(\mu, \sigma/\sqrt{n}\right)`
	-	The z-value for :math:`\overline{x}` can be constructed as :math:`z = \dfrac{\overline{x} - \mu}{\sigma/\sqrt{n}}`. An interval within which we can find :math:`\mu` with 95\% certainty is given below where :math:`c_n` is found from the normal distribution, and in R: ``qnorm(0.975) = 1.959964``, approximately 1.96.

	.. math::
		\begin{array}{rcccl} 
			  - c_n                                              &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}} &\leq &  +c_n\\
			\overline{x}  - c_n \dfrac{\sigma}{\sqrt{n}}              &\leq&  \mu                                                &\leq& \overline{x}  + c_n\dfrac{\sigma}{\sqrt{n}} \\
			  \text{LB}                                          &\leq&  \mu                                                 &\leq& \text{UB}
		\end{array}
		
	-	The 95% confidence interval for :math:`\mu` is from 17.7 to 22.3.
	
.. question::

	You are responsible for the quality of maple syrup produced at your plant. Historical data show that the standard deviation of the syrup viscosity is 40 cP. How many lab samples of syrup must you measure so that an estimate of the syrup's long-term average viscosity is inside a **range** of 60 cP, 95% of the time. This question is like the previous one: except this time you are given the range of the interval :math:`\text{UB}\,-\,\text{LB}`, and you need to find :math:`n`.
	
.. answer::
	:fullinclude: no 
	:short: 7 samples

	We can write the range symbolically as:
	
	.. math::
	
		\text{LB} &= \overline{x} - c_n \dfrac{\sigma}{\sqrt{n}} \\
		\text{UB} &= \overline{x} + c_n \dfrac{\sigma}{\sqrt{n}}
	
	Subtracting and setting equal to 60 cP:
	
	.. math::
	
		\text{UB} - \text{LB} &= 60 = 2 c_n \cdot \dfrac{\sigma}{\sqrt{n}} \\
		n &= \left( \dfrac{(2)(1.96)(40)}{60}\right)^2 \\
		n &\approx 7 \text{~samples}

.. question::

	Your manager is asking for the average viscosity of a product that you produce in a batch process. Recorded below are the 12 most recent values, taken from consecutive batches. State any assumptions, and clearly show the calculations which are required to estimate a 95% confidence interval for the mean. Interpret that confidence interval for your manager, who is not sure what a confidence interval is.

	.. math::
		\text{Raw data:} &\qquad [13.7,\, 14.9,\, 15.7,\, 16.1,\, 14.7,\, 15.2,\, 13.9,\, 13.9,\, 15.0,\, 13.0,\, 16.7,\, 13.2] \\
		\text{Mean:} &\qquad 14.67 \\
		\text{Standard deviation:} &\qquad 1.16 

	Ensure you can also complete the question by hand, using statistical tables.

.. answer::
	:fullinclude: no 
	
	The confidence interval for a mean requires the assumption that the individual numbers are taken from a normal distribution, and they are sampled independently (no sample has an effect on the others). Under these assumptions we can calculate a :math:`z`-value for the sampled mean, :math:`\overline{x}`, and construct upper and lower bounds reflecting the probability of sampling that :math:`z`-value.
	
	.. math::
		\begin{array}{rcccl}
		-c_n &\leq& \dfrac{\overline{x} - \mu}{\sigma/\sqrt{n}} &\leq& c_n \\
		\end{array}
		
	Since we don't know the value of :math:`\sigma`, we use the sampled value, :math:`s=1.16`. But this means our :math:`z`-value is no longer normally distributed, rather it is :math:`t`-distributed. The limits, :math:`\pm c_t` that contain 95% of the area under the :math:`t`-distribution, with 11 degrees of freedom, are 2.20 (or any close approximation from the tables provided). From this we get the confidence interval:
	
	.. math::
		\begin{array}{rcccl}
			-c_t &\leq& \dfrac{\overline{x} - \mu}{s / \sqrt{n}} &\leq& c_t \\
			14.67 - \dfrac{2.20 \times 1.16}{\sqrt{12}} &\leq& \mu &\leq& 14.67 + \dfrac{2.20 \times 1.16}{\sqrt{12}} \\
			13.93 &\leq& \mu &\leq& 15.41
		\end{array}
	
	This confidence interval means that we have 95% confidence that the true average viscosity lies within these bounds. If we took 100 groups of 12 samples, then the limits calculated from 95 of those groups are expected to contain the true mean. It is **incorrect** to say that there is 95% probability the true mean lies within these bounds; the true mean is fixed, there is no probability associated with it.

.. question::

	A new wastewater treatment plant is being commissioned and part of the commissioning report requires a statement of the confidence interval of the `biochemical oxygen demand (BOD) <http://en.wikipedia.org/wiki/Biochemical_oxygen_demand>`__. How many samples must you send to the lab to be sure the true BOD is within a range of 2 mg/L, centered about the sample average?  If there isn't enough information given here, specify your own numbers and assumptions and work with them to answer the question.

.. answer::
	:fullinclude: no 

	The objective is to calculate :math:`n`, the number of samples. Let :math:`\overline{x}` be the average of these :math:`n` samples, and this will be distributed according to the normal distribution with mean and standard deviation as shown below, if the samples are taken independently (which may not be possible in practice!):

	.. math::
		z = \dfrac{\overline{x}_{\text{BOD}} - \mu_{\text{BOD}}}{\sigma_{\text{BOD}}}
	
	The value of :math:`z` will lie within this confidence interval:

	.. math::
	
			\begin{array}{rcccl} 
			  - c_n                                                             &\leq& \dfrac{\overline{x}_{\text{BOD}} - \mu_{\text{BOD}}}{\sigma_{\text{BOD}}/\sqrt{n}}    &\leq&  +c_n \\
			\overline{x}_{\text{BOD}}  - c_n \dfrac{\sigma_{\text{BOD}}}{\sqrt{n}}   &\leq& \mu_{\text{BOD}}                                                                 &\leq& \overline{x}_{\text{BOD}}  + c_n\dfrac{\sigma_{\text{BOD}}}{\sqrt{n}} \\
			  \text{LB}                                                         &\leq& \mu_{\text{BOD}}                                                                 &\leq& \text{UB}
			\end{array}

	At this point all we know is that UB - LB = 2 mg/L. These are the rest of the assumptions we have to make: 

		- assume a standard deviation of :math:`\hat{\sigma}_{\text{BOD}}` = 4 mg/L
		- use 95% confidence intervals
		- assume we know the population standard deviation, so we use the normal distribution to calculate :math:`c_n` as ``qnorm(1-0.05/2)`` in R.
	
	Solving for :math:`n` at these values gives: :math:`n = \left(\dfrac{2(1.96)(\hat{\sigma}_{\text{BOD}})}{2}\right)^2 = (1.96 \times 4)^2 \sim 62`. This large number of samples makes sense: compare the range (2 mg/L) to the standard deviation of 4 mg/L: you have to take a large number of samples to get your precision up when you have so much noise in your signal.


.. question::
	
	One of the question we posed at the start of this chapter was: `Here are the yields from a batch bioreactor system <http://datasets.connectmv.com/info/batch-yields>`_  for the last 3 years (300 data points; we run a new batch about every 3 to 4 days).

	#.	What sort of distribution do the yield data have?
	#.	A recorded yield value was less than 60%, what are the chances of that occurring?  Express your answer as: *there's a 1 in n chance* of it occurring.
	#.	Which assumptions do you have to make for the second part of this question?
	
	.. From assignment 2, 2011

.. question::

    One aspect of your job responsibility is to reduce energy consumption on the plant floor. You ask the electrical supplier for the energy requirements (W.h) for running a particular light fixture for 24 hours. They won't give you the raw data, only their histogram when they tested randomly selected bulbs (see the data and code below). 

	.. code-block:: s

		> bin.centers <- c(4025, 4075, 4125, 4175, 4225, 4275, 4325, 4375)
		> bin.counts <- c(4, 19, 14,  5,  4,  1,  2,  1)
		> barplot(bin.counts, names.arg=bin.centers, ylab="Number of bulbs (N=50)", 
		     xlab="Energy required over 24 hours (W.h)", col="White", ylim=c(0,20))
	
	.. image:: ../figures/univariate/bulb-energy-barplot.png
		:width: 500px
		:align: center
		:scale: 50

	- Calculate an estimate of the mean and standard deviation, even though you don't have the original data.
	- What is a confidence interval for the mean at 95% probability, stating and testing any assumptions you need to make.

.. answer::
	:fullinclude: no 
	:short: mean = 4127, standard deviation = 77.2

	-   The mean and standard deviation can be estimated as shown in the code below. The estimates are: the mean energy usage is **4127 W.hours**, and the standard deviation is **79 W.hours**. This corresponds very closely to the raw data I used to generate this question (mean of actual data = 4125, sd of actual data = 77.2).

	    .. literalinclude:: ../figures/univariate/bulb-energy-assignment3-2010.R
	       :language: s
	       :lines: 13-17

	-   Strictly speaking we cannot calculate a confidence interval for the mean, as the data are not normally distributed. We can see that there is a heavy tail to the right hand side. Why do we require the data to be normally distributed?  To create the confidence interval we have to use an estimate of the standard deviation, and then use the :math:`t`-distribution to estimate the confidence interval bounds. However, the :math:`t`-distribution requires that we assume the raw data come from a normal distribution.

	    But if we do calculate the confidence interval, we have to use the :math:`t`-distribution at the 95% cumulative area, with 50 - 1 = 49 degrees of freedom. In R: ``qt(0.025, df=49)`` gives :math:`-c_t = -2.009575`. Using our estimates of :math:`s=79` and :math:`\overline{x} = 4127`
    
	    .. math::
    
	        \begin{array}{rcccl} 
	    		  - c_t                                              &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
	    		\overline{x}  - c_t \dfrac{s}{\sqrt{n}}                   &\leq&  \mu                                                 &\leq& \overline{x}  + c_t\dfrac{s}{\sqrt{n}} \\
	    		4127 - 2.01 \times \dfrac{79}{7}                     &\leq&  \mu                                                 &\leq& 4127 + 2.01 \times \dfrac{79}{7}\\
	    		4104                                                 &\leq&  \mu                                                 &\leq& 4150
	    	\end{array}

	    Look at this answer and compare it to the original histogram; does it make sense to you?

.. question::

    The confidence interval for the population mean takes one of two forms below, depending on whether we know the variance or not. At the 90% confidence level, for a sample size of 13, compare and comment on the upper and lower bounds for the two cases. Assume that :math:`s = \sigma = 3.72`.

	.. math::

		\begin{array}{rcccl} 
			  - c_n &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}}  &\leq &  c_n\\ \\
			  - c_t &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}}  &\leq &  c_t
		\end{array}

.. answer::
	:fullinclude: no 
	
	This question aims for you to prove to yourself that the :math:`t`-distribution is **wider (more broad)** than the normal distribution. The 90% region spanned by the :math:`t`-distribution with 12 degrees of freedom has upper and lower limits at ``qt((1-0.9)/2, df=12)``, i.e. from **-1.782** to **1.782**. The equivalent 90% region spanned by the normal distribution is ``qnorm((1-0.9)/2)``, spanning from **z=-1.64** to **z=1.64**. Everything else in the center of the 2 inequalities is the same, so we only need to compare :math:`c_t` and :math:`c_n`.


.. question::

	.. _univariate-CO2-question:

    A major aim of many engineers is/will be to reduce the carbon footprint of their company's high-profile products. Next week your boss wants you to evaluate a new raw material that requires 2.6 :math:`\dfrac{\text{kg CO}_2}{\text{kg product}}` less than the current material, but the final product's brittleness must be the same as achieved with the current raw material. This is a large reduction in :math:`\text{CO}_2`, given your current production capacity of 51,700 kg of product per year. Manpower and physical constraints prevent you from running a randomized test; you don't have a suitable database of historical data either.

    One idea you come up with is to use to your advantage the fact that your production line has three parallel reactors, TK104, TK105, and TK107. They were installed at the same time, they have the same geometry, the same instrumentation, *etc*; you have pretty much thought about every factor that might vary between them, and are confident the 3 reactors are identical. Typical production schedules split the raw material between the 3 reactors. Data `on the website <http://datasets.connectmv.com/info/brittleness-index>`_ contain the brittleness values from the three reactors for the past few runs on the current raw material.

	#.	Which two reactors would you pick to run your comparative trial on next week?
	
	#.	Repeat your calculations assuming pairing.

.. answer::
	:fullinclude: no 
	:short: You can do an ordinary test of differences, or a paired test. Also note that there are missing data which reduce the degrees of freedom.
	
		The purpose of this question is to compare two system. There are two ways: either compare one group to another group, or to have paired tests. We could consider this a paired test, because the material is run in both reactors at the same conditions. In this answer we compare reactor I to reactor J as groups. Our answer will be to run experiments in the reactors that show the smallest difference.

	.. note:: This question also has missing data, denote as ``NA`` in R. Most real data sets that you deal with will have missing data and the questions will expect to deal with them. For example, the degrees of freedom will be reduced because of the missing data. Use this solution to see how to write code in R that deals with missing values.

	We can start by looking at the data. A box plot is a reasonable way to compare both the location and spread of the brittleness values from each reactor.

	.. image:: ../figures/univariate/brittleness-boxplot.png
	    :width: 750px
	    :align: center
	    :scale: 50

	The standard way to test for differences between two groups of samples is given by equation :eq:`zvalue-for-difference` - it is derived as coming from the normal distribution with mean of :math:`\mu_A - \mu_B` and the standard deviation as shown in the denominator.

	.. math::
	    z = \frac{(\overline{x}_B - \overline{x}_A) - (\mu_B - \mu_A)}{\sqrt{\sigma^2 \left(\displaystyle \frac{1}{n_A} + \frac{1}{n_B}\right)}}

	Assuming the two *population* means are identical, the :math:`z`-value is a direct estimate of the probability with which that assumption is wrong. A :math:`z`-value around zero indicates that the assumption was true, a large or small :math:`z`-value indicates that the assumption was wrong.

	So we can calculate the :math:`z`-value, and the corresponding probability for each pair of reactor differences using the code below. 

	But the next problem we face is that we don't know the value of :math:`\sigma`. We can estimate it however, by pooling the variances of the two groups. Strictly speaking we should do a check for comparable variances before pooling them - described :ref:`in a previous section <univariate_pooled_variance>`.

	When we use the pooled variance now, then the assumption that the :math:`z`-value follows the normal distribution is not correct anymore; it follows the :math:`t`-distribution, with the pooled number of degrees of freedom. Once we have the :math:`z`-value we can calculate the probability of finding a :math:`z`-value of at least that big. Anything beyond that is the risk that we are wrong.

	We can also expand the :math:`z` value into a confidence interval at a given confidence level. We do this in the code at the 95% level (see ``LB`` and ``UB`` terms).

	    -   :math:`\mu_{104} - \mu_{105}`: :math:`z` = 1.25; risk we are wrong: 89.1%; CI: :math:`-31.4 \leq \mu_{104} - \mu_{105} \leq 134`
	    -   :math:`\mu_{104} - \mu_{107}`: :math:`z` = 1.41; risk we are wrong: 91.6%; CI  :math:`-21.4 \leq \mu_{104} - \mu_{107} \leq 120`
	    -   :math:`\mu_{105} - \mu_{107}`: :math:`z` = -0.0532; risk we are wrong: 52.1% and :math:`-81.8 \leq \mu_{105} - \mu_{107} \leq 77.6` (note that the minimum risk is 50%; the risk is not 47.8%)
    
	While all three reactors have confidence intervals that span zero at the 95% level, notice how the interval gives us a feel for the degree of difference. Clearly **reactors TK105 and TK107 are the most similar**, however all 3 are statistically equivalent from a confidence interval point of view. Contrast this to using a hypothesis test, which you may have encountered in other statistical courses. A hypothesis test just tells you  "yes" or "no"; a confidence interval gives a much better engineering feel for the degree of difference.

	A full solution to this question require you report the z-values and its corresponding risk.

	.. literalinclude:: ../figures/univariate/brittleness-comparison-assignment3-2010.R
	       :language: s
	
	**Using a paired test**
	
	Pairing assumes that each reactor was run with the same material, except that the material was split into thirds: one third for each reactor. As described in the :ref:`section on paired tests <univariate_paired_tests>` we rely on calculating the difference in brittleness, then calculating the z-value of the average difference. Contrast this to the unpaired tests, where we calculated the difference of the averages.

	The code below shows how the paired differences are evaluated for each of the 3 combinations. The paired test highlights the similarity between TK105 and TK107, the same as the unpaired test. However the paired test shows much more clearly how different tanks TK104 and TK105 are, and especially TK104 and TK107. 

	In the case of TK104 and TK105 the difference might seem surprising - take a look back at the box plots and how much they overlap.  However a paired test cannot be judged by a box plot, because it looks at the case-by-case difference, not the overall between group difference. A better plot with which to confirm the really large :math:`z`-value for the TK105 and TK107 difference is the plot of the differences.

	.. literalinclude:: ../figures/univariate/brittleness-paired-comparison-assignment3-2010.R
	       :language: s
	       :lines: 1-36

	Not required for the full grade, but one can show the confidence intervals are:

	.. math::
	
			\begin{array}{rcccl} 
			  9.81  &\leq& \mu_{105 - 104}    &\leq&  88.4 \\
			  48.3  &\leq& \mu_{107 - 104}    &\leq&  68.7 \\
			  -46.1  &\leq& \mu_{107 - 105}    &\leq&  33.5 \\
			\end{array}

	Advanced students should look at how the reduction in degrees of freedom affects this test; and contrast the results to those when using an unpaired test.

.. question::

	Use the `website traffic data <http://datasets.connectmv.com/info/website-traffic>`_ from the dataset website:

	- Write down, symbolically, the z-value for the difference in average visits on a Friday and Saturday.
	- Estimate a suitable value for the variance and justify your choice.
	- What is the probability of obtaining a z-value of this magnitude or smaller?  Would you say the difference is significant?
	- Pick any other 2 days that you would find interesting to compare and repeat your analysis.

	.. image:: ../figures/univariate/Website-traffic-TS.png
		:width: 750px
		
.. answer::
	
	-   Let our variable of interest be the difference between the average of the 2 groups: :math:`\overline{x}_{\text{Fri}} - \overline{x}_{\text{Sat}}`. This variable will be distributed normally (why? - see the notes) according to :math:`\overline{x}_{\text{Fri}} - \overline{x}_{\text{Sat}} \sim \mathcal{N}\left(\mu_{\text{Fri}}-\mu_{\text{Sat}}, \sigma^2_{\text{diff}}\right)`. So the z-value for this variable is: :math:`z = \dfrac{(\overline{x}_{\text{Fri}} - \overline{x}_{\text{Sat}}) - (\mu_{\text{Fri}}-\mu_{\text{Sat}}) }{\sigma_{\text{diff}}}`

	-   The variance of the difference, :math:`\sigma^2_{\text{diff}} = \sigma^2\left(\dfrac{1}{n_{\text{Fri}}} + \dfrac{1}{n_{\text{Sat}}} \right)`, where :math:`\sigma^2` is the variance of the number of visits to the website on Friday and Saturday. Since we don't know that value, we can estimate it from pooling the 2 variances of each group. We should calculate first that these variances are comparable (they are; but you :ref:`should confirm this yourself <univariate_pooled_variance>`).

	.. math::
	   \sigma^2 \approx s_P^2 &= \frac{(n_{\text{Fri}} -1) s_{\text{Fri}}^2 + (n_{\text{Sat}}-1)s_{\text{Sat}}^2}{n_{\text{Fri}} - 1 + n_{\text{Sat}} - 1} \\
	      &= \frac{29 \times 45.56 + 29 \times 48.62}{58} \\
	      &= 47.09
      
	-   The z-value calculated from this pooled variance is:

	    .. math::

	        z = \dfrac{20.77 - 15.27}{47.09 \left(\dfrac{1}{30} + \dfrac{1}{30} \right)} = 3.1
    
	    But since we used an estimated variance, we cannot say that :math:`z` comes from the normal distribution anymore. It now follows the :math:`t`-distribution with 58 degrees of freedom (which is still comparable to the normal distribution - see question 7 below). The corresponding probability that :math:`z<3.1` is 99.85%, using the :math:`t`-distribution with 58 degrees of freedom. This difference is significant; there is a very small probability that this difference is due to chance alone.

	-   The code was modified to generate the matrix of z-value results in the comments below. The largest difference is between Sunday and Wednesday, and the smallest difference is between Monday and Tuesday.

	.. literalinclude:: ../figures/univariate/website-differences-assignment3-2010.R
		:language: s
		:lines: 32-54,75-

.. question::

	You plan to run a series of 22 experiments to measure the economic advantage, if any, of switching to a corn-based raw material, rather than using your current sugar-based material. You can only run one experiment per day, and there is a high cost to change between raw material dispensing systems. Describe two important precautions you would implement when running these experiments, so you can be certain your results will be accurate.

.. answer::
	:fullinclude: no 

	Some important precautions one has to take are:

	#.	Keep all disturbance factors as constant as possible: e.g. use the same staff for all experiments (*Corn* and *Sugar*), keep other variables on the process as constant as possible.
	
	#.	Randomize the **order** of the experiments, despite the cost, to obtain independent experimental measurements. For example, if you cannot use the same staff for all experiments, then the experiment order must be randomization. Do not, for example, use group A staff to run the *Corn* experiments and group B staff to run the *Sugar* experiments.

		Randomization is expensive and inconvenient, but is the insurance we pay to ensure the results are not confounded by unmeasured disturbances.

	#.	Use representative lots of corn- and sugar-based materials. You don't want to run all your experiments on one batch of corn or sugar. What if the batch of corn-based material was an unusual in some way and showed no difference, when really there is a long-term difference? Or the opposite could have occurred as well.

.. question::

    There are two analytical techniques for measuring BOD. You wish to evaluate the two testing procedures, so that you can select the test which has lower cost, and fastest turn-around time, but without a compromise in accuracy. The table contains the results of the each test, performed on a sample that was split in half. 

	#.	Is there a *statistical* difference in accuracy between the two methods? 
	#.	Review the raw data and answer whether there is a practical difference in accuracy.

	=============== =================
	Dilution method Manometric method
	=============== =================
	11              25
	26              3
	18              27
	16              30
	20              33
	12              16
	8               28
	26              27
	12              12
	17              32
	14              16
	=============== =================

.. answer::
	:fullinclude: no 

	The temptation is to jump into the code and calculate the :math:`t`-values and averages differences (:math:`\overline{x}_D = 16.4`, and :math:`\overline{x}_M = 22.6`). But start with a plot of the data, specifically a plot of the differences between the two methods. The immediate problem you see is that average difference of 6.2 between the methods is strongly influenced by a single observation (the second one). In general, the dilution method always produced a smaller result than the manometric method. We expect to see that in our analytical results.

	.. image:: ../figures/univariate/BOD-comparison-plot.png
	    :width: 750px
	    :align: center
	    :scale: 60

	Now let's look at the analytical answer. As before, we can calculate :math:`z = 1.86 = \dfrac{6.27}{3.375}` (where :math:`s_p^2 = 62.7`), with a probability of 96.1% that we will have a value smaller than this (risk = 3.9% that we are wrong). A confidence interval would be :math:`-0.77 <  \mu_{\text{M}} - \mu_{\text{D}}< 13.3`. And it is at this point that you should realize the problem, even if you didn't plot your data. The fact that the confidence interval only just includes zero is what should raise concern; if the two methods were roughly equivalent, then the interval should span zero with rough symmetry. But this is too close.

	So omitting the second point and repeating the analysis gives: calculate :math:`z = 3.24 = \dfrac{9.20}{2.84}` (where :math:`s_p^2 = 40.4`), with a probability of 99.8% that we will have a value smaller than this (risk = 0.2% that we are wrong). A confidence interval would be :math:`3.2 <  \mu_{\text{M}} - \mu_{\text{D}}< 15.2`; this is a result that is much more aligned with the plotted data.

	.. note:: You may have discovered/used the ``t.test(...)`` function in R. If you know what you are doing with this function, you are welcome to use it; however I'm reluctant to advocate its use at this point, because these exercises are all about understanding what is going on with confidence intervals and calculating them yourself.

.. question::

	Plot the cumulative probability function for the normal distribution and the :math:`t`-distribution on the same plot. 

		- Use 6 degrees of freedom for :math:`t`-distribution. 
		- Repeat the plot for a larger number of degrees of freedom. 
		- At which point is the :math:`t`-distribution indistinguishable from the normal distribution?  
		- What is the practical implication of this result?

.. answer::

	.. literalinclude:: ../figures/univariate/t-distribution-normal-comparison-assignment3-2010.R
	       :language: s

	.. image:: ../figures/univariate/normal-t-comparison.png
	    :width: 750px
	    :align: center
    
	The above source code and figure output shows that the :math:`t`-distribution starts being indistinguishable from the normal distribution after about 35 to 40 degrees of freedom. This means that when we deal with large sample sizes (over 40 or 50 samples), then we can use critical values from the normal distribution rather than the :math:`t`-distribution. Furthermore, it indicates that our estimate of the variance is a pretty good estimate of the population variance for largish sample sizes.
	
.. question::

	Explain why tests of differences are insensitive to unit changes. If this were not the case, then one could show a significant difference for a weight-loss supplement when measuring waist size in millimetres, yet show no significant difference when measuring in inches!

.. question::

	A food production facility fills bags with potato chips. The advertised bag weight is 35.0 grams.  But, the current bagging system is set to fill bags with a mean weight of 37.4 grams, and this done so that only 1% of bags have a weight of 35.0 grams or less. 

		-	Back-calculate the standard deviation of the bag weights, assuming a normal distribution.
		-	Out of 1000 customers, how many are lucky enough to get 40.0 grams or more of potato chips in their bags?

.. answer::
	:fullinclude: no 
	:short: standard deviation = 1.03 grams

	-	Calculate the z-value and find which fraction of :math:`z` falls at or below 1% of the probability area. From the tables this is -2.326.

		Then solve for :math:`\sigma`:

		.. math::
			z &= \dfrac{35 - 37.4}{\sigma} = -2.326 \\
			\sigma &= \dfrac{35-37.4}{-2.326} = \mathrm{1.03} \text{~grams }

	-	Probability of 40.0 grams of more is the area above the corresponding :math:`z`-value:

		.. math::
			z &>	\dfrac{40- 37.4}{1.03} \\
			z &> 2.52

		The exact answer is ``(1 - pnorm(2.52))*1000 = 5.86``, though using tables you could use the value corresponding to :math:`z=2.5`, which is 99.38%, which is the area below that z-value. The area above it is 0.62%, corresponding to 6.2 people. Either 5, 6 or 7 people is an acceptable answer, depending on your rounding error.
	
.. question::

	A common unit operation in the pharmaceutical area is to uniformly blend powders for tablets. In this question we consider blending an excipient (an inactive magnesium stearate base), a binder, and the active ingredient. The mixing process is tracked using a wireless near infrared (NIR) probe embedded in a V-blender. The mixer is stopped when the NIR spectra become stable. A new supplier of magnesium stearate is being considered that will save $ 294,000 per year.

	..	figure:: ../figures/univariate/V-Blender.png
		:width: 500px
		:align: center
		:scale: 40
	
		Illustration from `Wikipedia <http://en.wikipedia.org/wiki/Industrial_mixer>`__

	The 15 most recent runs with the current magnesium stearate supplier had an average mixing time of 2715 seconds, and a standard deviation of 390 seconds. So far you have run 6 batches from the new supplier, and the average mixing time of these runs is 3115 seconds with a standard deviation of 452 seconds. Your manager is not happy with these results so far - this extra mixing time will actually cost you more money via lost production. 

	The manager wants to revert back to the original supplier, but is leaving the decision up to you; what would be your advice?  Show all calculations and describe any additional assumptions, if required.

.. answer::
	:fullinclude: no 
	:short: This problem is open-ended: pay attention to having a significant difference vs a practical difference.

	This question, similar to most real statistical problems, is open-ended. This problem considers whether a significant difference has occurred. And in many cases, even though there is significant difference, it has to be weighed up whether there is a *practical* difference as well, together with the potential of saving money (increased profit).

	You should always state any assumptions you make, compute a confidence interval for the difference and interpret it. 

	The decision is one of whether the new material leads to a significant difference in the mixing time. It is desirable, from a production point of view, that the new mixing time is shorter, or at least the same. Some notation:

	.. math::
		\begin{array}{rclrcl}
			\hat{\mu}_\text{Before} 	= \overline{x}_B &=& 2715 	&\qquad\qquad \hat{\mu}_\text{After} 	= \overline{x}_A &=& 3115\\
			\hat{\sigma}_\text{Before} 	= s_B &=& 390			&\qquad\qquad \hat{\sigma}_\text{After} = s_A &=& 452\\
			n_B 						&=& 15 					&\qquad\qquad n_A 						&=& 6
		\end{array}
	
	Assumptions required to compare the two groups:

		*	The individual samples within each group were taken independently, so that we can invoke the central limit theorem and assume these means and standard deviation are normal distributed.
		*	Assume the individual samples within each group are from a normal distribution as well.
		*	Assume that we can pool the variances, i.e. :math:`\sigma_\text{Before}` and :math:`\sigma_\text{After}` are from comparable distributions.
		*	Using the pooled variance implies that the :math:`z`-value follows the :math:`t`-distribution.
		*	The mean of each group (before and after) is independent of the other (very likely true).
		*	No other factors were changed, other than the raw material (we can only hope, though in practice this is often not true, and a paired test would eliminate any differences like this).

	Calculating the pooled variance:

	.. math::
		s_P^2 &= \dfrac{(n_A -1) s_A^2 + (n_B-1)s_B^2}{n_A - 1 + n_B - 1} \\
		      & = \dfrac{(6-1) 452^2 + (15-1)390^2}{6 - 1 + 15 - 1} \\
		      & = 165837
	
	Computing the z-value for this difference:

	.. math::	
		z &= \dfrac{(\overline{x}_B - \overline{x}_A) - (\mu_B - \mu_A)}{\sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}}\\
		z &= \dfrac{(2715 - 3115) - (\mu_B - \mu_A)}{\sqrt{165837 \left(\frac{1}{6} + \frac{1}{15}\right)}} \\
		z &= \dfrac{-400 - (\mu_B - \mu_A)}{196.7} = -2.03 \qquad \text{on the hypothesis that}\qquad \mu_B = \mu_A


	The probability of obtaining this value of :math:`z` can be found using the :math:`t`-distribution at 6 + 15 - 2 = 19 degrees of freedom (because the standard deviation is an estimate, not a population value). Using tables, a value of 0.025, or 2.5% is found (in R, it would be ``pt(-2.03, df=19) = 0.0283``, or 2.83%). At this point one can argue either way that the new excipient leads to longer times, though I would be inclined to say that this probability is too small to be due to chance alone. Therefore there is a significant difference, and we should revert back to the previous excipient. Factors such as operators, and other process conditions could have affected the 6 new runs.

	Alternatively, and this is the way I prefer to look at these sort of questions, is to create a confidence interval. At the 95% level, the value of :math:`c_t` in the equation below, using 19 degrees of freedom is ``qt(0.975, df=19) = 2.09`` (any value close to this from the tables is acceptable):

		.. math::
			\begin{array}{rcccl} 
				-c_t &\leq& z	&\leq & +c_t \\
				(\overline{x}_B - \overline{x}_A) - c_t \sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}	&\leq& \mu_B - \mu_A	&\leq &  (\overline{x}_B - \overline{x}_A) + c_t \sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}\\
				-400 - 2.09 \sqrt{165837 \left(\frac{1}{6} + \frac{1}{15}\right)} 	&\leq& \mu_B - \mu_A	&\leq& -400 + 2.09 \sqrt{165837 \left(\frac{1}{6} + \frac{1}{15}\right)} \\
				-400 - 412	&\leq& \mu_B - \mu_A	&\leq&   -400 + 412 \\
				-812		&\leq& \mu_B - \mu_A	&\leq&   12 
			\end{array}

	The interpretation of this confidence interval is that there is no difference between the current and new magnesium stearate excipient. The immediate response to your manager could be "*keep using the new excipient*". 

	However, the confidence interval's asymmetry should give you pause, certainly from a practical point of view (this is why I prefer the confidence interval - you get a better interpretation of the result). The 12 seconds by which it overlaps zero is so short when compared to average mixing times of around 3000 seconds, with standard deviations of 400 seconds. The practical recommendation is that the new excipient has longer mixing times, so "*revert to using the previous excipient*".

	One other aspect of this problem that might bother you is the low number of runs (batches) used. Let's take a look at how sensitive the confidence interval is to that. Assume that we perform one extra run with the new excipient (:math:`n_A = 7` now), and assume the pooled variance, :math:`s_p^2 = 165837` remains the same with this new run. The new confidence interval is:

	.. math::
		\begin{array}{rcccl} 
			(\overline{x}_B - \overline{x}_A) - c_t \sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}	&\leq& \mu_B - \mu_A	&\leq &  (\overline{x}_B - \overline{x}_A) + c_t \sqrt{s_P^2 \left(\frac{1}{n_A} + \frac{1}{n_B}\right)}\\
			(\overline{x}_B - \overline{x}_A)- 2.09 \sqrt{165837 \left(\frac{1}{7} + \frac{1}{15}\right)} 	&\leq& \mu_B - \mu_A	&\leq& (\overline{x}_B - \overline{x}_A)  + 2.09 \sqrt{165837 \left(\frac{1}{7} + \frac{1}{15}\right)} \\
			(\overline{x}_B - \overline{x}_A)  - 390	&\leq& \mu_B - \mu_A	&\leq&   (\overline{x}_B - \overline{x}_A) + 390 
		\end{array}

	So comparing this :math:`\pm 390` with 7 runs, to the :math:`\pm 412` with 6 runs, shows that the confidence interval shrinks in quite a bit, much more than the 12 second overlap of zero. Of course we don't know what the new :math:`\overline{x}_B - \overline{x}_A` will be with 7 runs, so my recommendation would be to perform at least one more run with the new excipient, but I suspect that the new run would show there to be a significant difference, and statistically confirm that we should "*revert to using the previous excipient*".
	
.. question::

	List an advantage of using a paired test over an unpaired test. Give an example, not from the notes, that illustrates your answer.

.. answer::
	:fullinclude: no 
	
	One primary advantage of pairing is that any systematic difference between the two groups (A and B) is eliminated. For example, a bias in the measurement will cancel out when calculating the pairs of differences. Any example is suitable as an answer: e.g. laboratory miscalibration; an offset in an on-line sensor, *etc*.

	Other advantages are that the raw data do not need to be normally distributed, only the paired differences. 

	Another advantage is that randomization of the trials is required in the unpaired case (often a costly extra expense), whereas in the paired case, we only need to be sure the pairs are independent of each other (that's much easier to assume, and often true). For example testing drug A and B on a person, some time apart. The pairs are run on the same person, but each person in the drug trial is independent of the other.

.. question::

	An *unpaired* test to distinguish between group A and group B was performed with 18 runs: 9 samples for group A and 9 samples for group B. The pooled variance was 86 units. 

	Also, a *paired* test on group A and group B was performed with 9 runs. After calculating the paired differences, the variance of these differences was found to be 79 units. 

	Discuss, in the context of this example, an advantage of paired tests over unpaired tests. Assume 95% confidence intervals, and that the true result was one of "no significant difference between method A and method B". Give numeric values from this example to substantiate your answer.

.. answer::
	:fullinclude: no 

	One advantage of the paired test is that often a fewer number of samples are required to obtain a more sensitive result than when analyzing the data as from two distinct, unpaired groups.

	Construct the confidence interval for both cases, substitute in these values and then compare the confidence intervals. The equations for both confidence intervals are derived directly from the :math:`z`-value.

	**Unpaired case**:

	.. math::

		\begin{array}{rcccl} 
			  - c_t                                              &\leq& \dfrac{(\overline{x}_B - \overline{x}_A) - (\mu_B - \mu_A)}{\sqrt{s_P^2 \left(\dfrac{1}{n_A} + \dfrac{1}{n_B}\right)}} &\leq &  +c_t\\
			(\overline{x}_B - \overline{x}_A)  - c_t \sqrt{s_P^2 \left(\dfrac{1}{n_A} + \dfrac{1}{n_B}\right)}  &\leq&  \mu_B - \mu_A &\leq& (\overline{x}_B - \overline{x}_A) + c_t \sqrt{s_P^2 \left(\dfrac{1}{n_A} + \dfrac{1}{n_B}\right)} \\
		   	(\overline{x}_B - \overline{x}_A)  - 2.12 \times \sqrt{86 \left(\dfrac{1}{9} + \dfrac{1}{9}\right)}  &\leq&  \mu_B - \mu_A &\leq& (\overline{x}_B - \overline{x}_A) + 2.12 \times \sqrt{86 \left(\dfrac{1}{9} + \dfrac{1}{9}\right)} \\
			(\overline{x}_B - \overline{x}_A)  - 9.27  &\leq&  \mu_B - \mu_A &\leq& (\overline{x}_B - \overline{x}_A) + 9.27 \\
		\end{array}

	The :math:`c_t` value for the unpaired case is from the :math:`t`-distribution with 16 degrees of freedom, a value of around 2.12.

	**Paired case**:

	In this case the vector of differences is :math:`w`, and by the central limit theorem it is distributed as :math:`w \sim \mathcal{N}\left( \mu_{B-A} , \sigma_w^2/n \right)`, but we use the estimated variance, :math:`s_w^2` instead.

		.. math::

			\begin{array}{rcccl} 
				  - c_t               						&\leq& \dfrac{\overline{w} - \mu_{B-A}}{s_w / \sqrt{n}} 	&\leq &  +c_t\\
				\\
				\overline{w} - c_t \dfrac{s_w}{\sqrt{n}}			&\leq& \mu_w 									&\leq &  \overline{w} + c_t \dfrac{s_w}{\sqrt{n}} \\
				\overline{w} - 2.3 \dfrac{\sqrt{79}}{\sqrt{9}}	&\leq& \mu_w 									&\leq &  \overline{w} + 2.3 \dfrac{\sqrt{79}}{\sqrt{9}} \\
				\overline{w} - 6.81								&\leq& \mu_w 				&\leq&  \overline{w} + 6.81
			\end{array}

	The :math:`c_t` value for the paired case is from the :math:`t`-distribution with 8 degrees of freedom, a value of around 2.3.

	The key result of this question is that the confidence interval for the paired case is tighter (narrower) than the confidence interval from the unpaired case. Given that the true result was one of no significant difference, it implies that :math:`\mu_A = \mu_B` and that :math:`\mu_w = 0`. The tighter confidence interval comes purely from the fact that the standard deviation used for the paired case is smaller, :math:`\sqrt{\dfrac{79}{9}}` *vs* the :math:`\sqrt{86 \left(\dfrac{1}{9} + \dfrac{1}{9}\right)}` from the unpaired case. This is not due to the variances, since :math:`\sqrt{86} \approx \sqrt{79}`, i.e. (9.27 vs 8.88), but rather due to the fact that that unpaired standard deviation is multiplied by :math:`\sqrt{2/9}`, while the paired standard deviation is multiplied by :math:`\sqrt{1/9}`.

	So while the :math:`c_t` value for the paired case is actually larger (widening the confidence interval due to the fewer degrees of freedom), the overall effect is  that the paired confidence interval is narrower than the unpaired confidence interval. This result holds for most cases of paired and unpaired studies, though not always.
	
.. question::

	You are convinced that a different impeller (mixing blade) shape for your tank will lead to faster, i.e. shorter, mixing times. The choices are either an axial blade or a radial blade. 

	..	figure:: ../figures/univariate/Mixing_-_flusso_assiale_e_radiale.jpg
		:width: 500px
		:align: center
		:scale: 40

		Axial and radial blades; figure `from Wikipedia <http://en.wikipedia.org/wiki/Impeller>`__

	Before obtaining approval to run some experiments, your team wants you to explain how you will interpret the experimental data. Your reply is that you will calculate the average mixing time from each blade type and then calculate a confidence interval for the difference. A team member asks you what the following 95% confidence intervals would mean:

		#.	:math:`-453 \text{~seconds} \leq \mu_{\text{Axial}} - \mu_{\text{Radial}} \leq 390 \text{~seconds}`
		#.	:math:`-21 \text{~seconds} \leq \mu_{\text{Axial}} - \mu_{\text{Radial}} \leq 187 \text{~seconds}`

	For both cases (a) explain what the confidence interval means in the context of this experiment, and (b) whether the recommendation would be to use radial or axial impellers to get the shortest mixing time.

	\3. Now assume the result from your experimental test was :math:`-21 \text{~seconds} \leq \mu_{\text{Axial}} - \mu_{\text{Radial}} \leq 187 \text{~seconds}`; how can you make the confidence interval narrower?

.. answer::
	:fullinclude: no 

	#.	This confidence interval spans zero, and nearly symmetrically. This implies the population difference is likely zero, while the symmetry implies their is no preference either way: the difference in mixing times is as low as -453 seconds or as high as 390 seconds. The recommendation is that either the axial or radial impeller could be used, with no expected long-term difference. Use the cheaper impeller; or use the axial impeller if the costs are the same (only because of the very slight imbalance in the CI). Note that there is a 5% chance that the confidence interval does not contain the true difference.

	#.	This confidence interval also spans zero, so there is **no statistical difference** between the two impellers. However the CI does not span zero symmetrically. The asymmetry of the interval makes me much less comfortable recommending that there is no **practical difference** between the impellers. It often happens in these cases that by removing a single data point that the confidence interval does not span zero anymore. In this case I would recommend either impeller, but if there is no cost difference, I would prefer the radial impeller, as it might have shorter mixing times, especially if the confidence interval quoted here is only due to one observation. A careful review of the raw data would be useful in this case.

	#.	The confidence interval can be made narrower in 2 ways (as long as the sample mean and sample standard deviation remain stable):

		-	Use more data points, :math:`n` in both groups.
		-	Choose a lower degree of confidence, e.g. 90%  instead of 95%, which is really just an artificial reduction of the interval.

		One can also reduce the interval by shrinking the standard deviation, but that's usually not a practical possibility. You cannot perform a paired test, as you only have one mixing tank.

	.. sidebar:: Interpreting confidence intervals

		Recall the definition of the confidence interval is subtle: it says 95% of the time, the upper and lower bounds of the confidence interval contain the true value of the parameter; it does *not* say there is a 95% probability the true value of the parameter lies inside the bounds. That last part is incorrect because it implies the true value of the parameter can vary, which it can't: the true parameter value is fixed, only the bounds change. 
		
.. question::

	The paper by PJ Rousseeuw, "`Tutorial to Robust Statistics <http://dx.doi.org/10.1002/cem.1180050103>`_", *Journal of Chemometrics*, **5**, 1-20, 1991 discusses the breakdown point of a statistic. 
	
	#.	Describe what the breakdown point is, and give two examples: one with a low breakdown point, and one with a high breakdown point. Use a vector of numbers to help illustrate your answer.
	
	#.	What is an advantage of using robust methods over their "classical" counterparts?

.. answer::

	#.	PJ Rousseeuw defines the breakdown point on page 3 of his paper as "... the smallest fraction of the observations that have to be replaced to make the estimator unbounded. In this definition one can choose which observations are replaced, as well as the magnitude of the outliers, in the least favourable way".

		A statistic with a low breakdown point is the mean, of the :math:`n` values used to calculate the mean, only 1 needs to be replaced to make the estimator unbounded; i.e. its breakdown point is :math:`1/n`. The median though has a breakdown point of 50%, as one would have to replace 50% of the :math:`n` data points in the vector before the estimator becomes unbounded.

		Use this vector of data as an example: :math:`[2, 6, 1, 9151616, -4, 2]`. The mean is 1525270, while the median is 2.
		
	#.	
		*	Robust methods are insensitive to outliers, which is useful when we need a measure of location or spread that is calculated in an automated way. It is increasingly prevalent to skip out the "human" step that might have detected the outlier, but our datasets are getting so large that we can't possibly visualize or look for outliers manually anymore.

		*	As described in the above paper by Rousseeuw, robust methods also emphasize outliers. Their "lack of sensitivity to outliers" can also be considered an advantage.

.. question::

	Recall that :math:`\mu = \mathcal{E}(x) = \frac{1}{N}\sum{x}` and :math:`\mathcal{V}\left\{x\right\} = \mathcal{E}\left\{ (x - \mu )^2\right\} = \sigma^2 = \frac{1}{N}\sum{(x-\mu)^2}`. 

		#.	What is the expected value thrown of a fair, 12-sided dice?
		#.	What is the expected variance of a fair, 12-sided dice?
		#.	Simulate 10,000 throws in a software package (R, MATLAB, or Python) from this dice and see if your answers match those above. Record the average value from the 10,000 throws, call that average :math:`\overline{x}`.
		#.	Repeat the simulation 10 times, calculating the average value of all the dice throws. Calculate the mean and standard deviation of the 10 :math:`\overline{x}` values and *comment* whether the results match the theoretically expected values.

.. answer::

	The objective of this question is to recall basic probability rules.

	#. Each value on the dice is equally probable, so the expected value thrown will be:

		.. math::
			\mathcal{E}(X) = \sum_{i=1}^{12}x_{i}P(x_{i}) = P(x) \sum_{i=1}^{12} x_{i} = \frac{1}{12} \left( 1 + 2 + \cdots + 12 \right) = \bf{6.5}
		
		This value is the population mean, :math:`\mu`.

	#. Continuing the notation from the above question we can derive the expected variance as,

		.. math::
			\mathcal{V}(X) &= \frac{1}{N}\sum_i^{12}{(x_i - \mu)^2} = \frac{1}{12} \cdot \left[ (1 - 6.5)^2 + (2 - 6.5)^2 + \ldots + (12 - 6.5)^2 \right] \approx \bf{11.9167}

	#.	Simulating 10,000 throws corresponds to 10,000 independent and mutually exclusive random events, each with an outcome between 1 and 12. The sample mean and variance from my sample was calculated using this code in R:

		.. math::

			\overline{x} &= 6.5219\\
			s^2 &= 12.03732
		
		.. literalinclude:: ../figures/univariate/simulate-dice.R
			:language: s

	#.	Repeating the above simulation 10 times (i.e. 10 independent experiments) produces 10 different estimates of :math:`\mu` and :math:`\sigma^2`. Note, your answer should be slightly different, and different each time you run the simulation. 

		.. literalinclude:: ../figures/univariate/simulate-dice-CLT.R
			:language: s

		Note that each :math:`\overline{x} \sim \mathcal{N}\left(\mu, \sigma^2/n \right)`, where :math:`n = 10000`. We know what :math:`\sigma^2` is in this case: it is our theoretical value of **11.92**, calculated earlier, and for :math:`n=10000` samples, our theoretical expectation is that :math:`\overline{x} \sim \mathcal{N}\left(6.5, 0.00119167\right)`.

		Calculating the average of those 10 means, let's call that :math:`\overline{\overline{x}}`, shows a value close to 6.5, the theoretical mean.

		Calculating the variance of those 10 means shows a number around 0.00119167, as expected.

.. question::
	
	One of the questions we posed at the start of this chapter was: "`Here are the yields <http://datasets.connectmv.com/info/batch-yields>`_ from a batch bioreactor system for the last 3 years (300 data points; we run a new batch about every 3 to 4 days).

	#.	What sort of distribution do the yield data have?
	#.	A recorded yield value today was less than 60%, what are the chances of that occurring?  Express your answer as: *there's a 1 in x chance* of it occurring.
	#.	Which assumptions do you have to make for the second part of this question?
	
	.. From assignment 2, 2011

.. answer::
	:fullinclude: no

	#.	Assume the 300 data points represent an entire population. Plot a ``qqPlot(...)`` using the ``car`` package:

		.. image:: ../figures/univariate/batch-yields-qqplot.png
			:alt:	../figures/univariate/batch-yields.R
			:scale: 60
			:width: 500px
			:align: center  

		The data appear to follow a normal distribution, based on the visual test of this qq-plot.

	#.	We need to find the probability that the yield, :math:`Y`, is less than or equal to 60, stated as :math:`P(Y\le 60)`. If we assume :math:`Y \sim \mathcal{N}(\mu,\sigma^{2})` then we first need to find the :math:`z`-value bound corresponding to 60, and then find the probability of finding values below, or equal to that bound.

		.. math::

			z_\text{bound} = \frac{y-\mu}{\sigma} = \frac{60-80.353}{6.597} = -3.085

		In this data set of 300 numbers there are zero entries below this limit. But using the distribution's fit, we can calculate the probability as ``pnorm(-3.085)``, which is :math:`\approx 0.001`. This is equivalent to saying that there is a *1 in 1000 chance* of achieving a yield less than 60\%.

	#.	We only had to assume the data are normally distributed - we did not need the data to be independent - in order to use the estimated parameters from the distribution to calculate the probability.
	
		.. literalinclude:: ../figures/univariate/batch-yields.R
			:language: s

.. question::

	#.	At the 95% confidence level, for a sample size of 7, compare and comment on the upper and lower bounds of the confidence interval that you would calculate if:

		a)	you know the population standard deviation
		b)	you have to estimate it for the sample.

		Assume that the calculated standard deviation from the sample, :math:`s` matches the population :math:`\sigma = 4.19`.

	#.	As a follow up, overlay the probability distribution curves for the normal and :math:`t`-distribution that you would use for a sample of data of size :math:`n=7`.

	#.	Repeat part of this question, using larger sample sizes. At which point does the difference between the :math:`t`- and normal distributions become *practically* indistinguishable? 
	
	#.	What is the implication of this?

.. answer::
	:fullinclude: no
	
	#.	This question aims for you to prove to yourself that the :math:`t`-distribution is **wider (more broad)** than the normal distribution, and as a result, the confidence interval is wider as well. This is because we are less certain of the data's spread when using the estimated variance.
	
		The confidence intervals are:
	
		.. math::

			\begin{array}{rcccl} 
				  - c_n &\leq& \displaystyle \frac{\overline{x} - \mu}{\sigma/\sqrt{n}}  &\leq &  c_n\\ \\
				  - c_t &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}}  &\leq &  c_t
			\end{array}	
	
		The 95% region spanned by the :math:`t`-distribution with 6 degrees of freedom has upper and lower limits at :math:`c_t = \pm` ``qt((1-0.95)/2, df=6)``, i.e. from **-2.45** to **2.45**. The equivalent 95% region spanned by the normal distribution is :math:`c_n = \pm` ``qnorm((1-0.95)/2)``, spanning from **z=-1.96** to **z=1.96**. Everything else in the center of the 2 inequalities is the same, so we only need to compare :math:`c_t` and :math:`c_n`.
	
	#.	The question asked to overlay the probability distributions (not cumulative probability distributions):

		.. image:: ../figures/univariate/overlaid-distributions-normal-and-t.jpg
			:alt:	../figures/univariate/overlaid-distributions-normal-and-t.R
			:scale: 50
			:width: 750px
			:align: center
		
		where the above figure was generated with the R-code:
	
		.. literalinclude:: ../figures/univariate/overlaid-distributions-normal-and-t.R
			:language: s	

	#.	Repeated use of the above code, but changing :math:`n`, shows that little *practical* difference between the distributions with as few as :math:`n=20` samples. After :math:`n=40` and especially :math:`n=60`, there is almost no *theoretical* difference between them.

	#.	This implies that when we do any analysis of large samples of data, say :math:`n>50`, and if those data are independently sampled, then we can just use the normal distribution's critical value (e.g. the :math:`\pm 1.96` value for 95% confidence, which you now know from memory), instead of looking up the :math:`t`-distribution's values.

		Since the wider values from the :math:`t`-distribution reflect our uncertainty in using an *estimate of the variance*, rather than the population variance, this result indicates that our estimated variances are a good estimate of the population variance for largish sample sizes.

.. question::

	.. _lack_of_independence_question:
	
	Engineering data often violate the assumption of independence. In this question you will create (simulate) sequences of autocorrelated data, i.e. data that lack independence, and investigate how lack of independence affects our results. 
	
	The simplest form of autocorrelation is what is called lag-1 autocorrelation, when the series of values, :math:`x_k` is correlated with itself only 1 step back in time, :math:`x_{k-1}`:

	.. math::

		x_k = \phi x_{k-1} + a_k
	
	The :math:`a_k` value is a random error and for this question let :math:`a_k \sim \mathcal{N}\left(\mu=0, \sigma^2 = 25.0 \right)`. 
	
	Create 3 sequences of autocorrelated data with:

		A:	:math:`\qquad \phi = +0.7` (positively correlated)
	
		B:	:math:`\qquad \phi = 0.0` (uncorrelated data)
	
		C: 	:math:`\qquad \phi = -0.6` (negatively correlated)

	For case A, B and C perform the following analysis. Repeat the following 1000 times (let :math:`i = 1, 2, \ldots, 1000`):
	
		*	Create a vector of 100 autocorrelated :math:`x` values using the above formula, using the current level of :math:`\phi`
		*	Calculate the mean of these 100 values, call it :math:`\overline{x}_i` and store the result
		
	At this point you have 1000 :math:`\overline{x}_i` values for case A, another 1000 :math:`\overline{x}_i` values for case B, and similarly for case C. Now answer these questions:
	
	#.	Assuming independence, which is obviously not correct for 2 of the 3 cases, nevertheless, from which population should :math:`\overline{x}` be from, and what are the 2 parameters of that population?
	#.	Now, using your 1000 simulated means, estimate those two population parameters.
	#.	Compare your estimates to the theoretical values.

	Comment on the results, and the implication of this regarding tests of significance (i.e. statistical tests to see if a significant change occurred or not).

.. answer::

	.. See BHH, 2nd edition. p 60.

	We expect that case B should match the theoretical case the closest, since data from case B are truly independent, since the autocorrelation parameter is zero. We expect case A and C datasets, which violate that assumption of independence, to be biased one way or another. This question aims to see **how** they are biased.

	.. literalinclude:: ../figures/univariate/variance-inflation.R
		:language: s
	
	You should be able to reproduce the results I have below, because the above code uses the ``set.seed(...)`` function, which forces R to generate random numbers in the same order on my computer as yours (as long as we all use the same version of R).
	
	*	Case A:	``0.50000000, 0.00428291,   1.65963302``
	*	Case B:	``0.50000000, 0.001565456,  0.509676562``
	*	Case C:	``0.50000000, 0.0004381761, 0.3217627596``

	The first output is the same for all 3 cases: this is the theoretical standard deviation of the distribution from which the :math:`\overline{x}_i` values come: :math:`\overline{x}_i \sim \mathcal{N}\left(\mu, \sigma^2/N \right)`, where :math:`N=100`, the number of points in the autocorrelated sequence. This result comes from the central limit theorem, which tells us that :math:`\overline{x}_i` should be normally distributed, with the same mean as our individual :math:`x`-values, but have smaller variance. That variance is :math:`\sigma^2/N`, where :math:`\sigma` is the variance of the distribution from which we took the raw :math:`x` values. That theoretical variance value is :math:`25/100`, or theoretical standard deviation of :math:`\sqrt{25/100} = \bf{0.5}`.

	But, the central limit theorem only has one *crucial* assumption: that those raw :math:`x` values are independent. We intentionally violated this assumption for case A and C. 

	We use the 1000 simulated values of :math:`\overline{x}_i` and calculate the average of the 1000 :math:`\overline{x}_i` values and the standard deviation of the 1000 :math:`\overline{x}_i` values. Those are the second and third values reported above. 

	We see in all cases that the mean of the 1000 values nearly matches 0.0. If you run the simulations again, with a different seed, you will see it above zero, and sometimes below zero for all 3 cases. So we can conclude that lack of independence *does not* affect the estimated mean.

	The major disagreement is in the variance though. Case B matches the theoretical variance; data that are positively correlated have an inflated standard deviation, 1.66; data that are negatively correlated have a deflated standard deviation, 0.32 when :math:`\phi=-0.6`.

	This is problematic for the following reason. When doing a test of significance, we construct a confidence interval:

	.. math::
		
			\begin{array}{rcccl} 
				- c_t                                   &\leq& \displaystyle \frac{\overline{x} - \mu}{s/\sqrt{n}} &\leq &  +c_t\\
				\overline{x} - c_t \dfrac{s}{\sqrt{n}}  &\leq& \mu                                                 &\leq& \overline{x} + c_t\dfrac{s}{\sqrt{n}} \\
				\text{LB}                               &\leq& \mu                                                 &\leq& \text{UB}
			\end{array}

	We use an estimated standard deviation, :math:`s`, whether that is found from pooling the variances or found separately (it doesn't really matter), but the main problem is that :math:`s` is not accurate when the data are not independent:

	*	For positive correlations (quite common in industrial data): our confidence interval will be too wide, likely spanning zero, indicating no statistical difference, when in fact there might be one.
	*	For negative correlations (less common, but still seen in practice): our confidence interval will be too narrow, more likely to indicate there is a difference.

	The main purpose of this question is for you to see how use to understand what happens when a key assumption is violated. There are cases when an assumption is violated, but it doesn't affect the result too much.
	
	In this particular example there is a known theoretical relationship between :math:`\phi` and the inflated/deflated variance that can be derived (with some difficulty). But in most situations the affect of violating assumptions is too difficult to derive mathematically, so we use computer power to do the work for us: but then we still have to spend time thinking and interpreting the results.

.. question::

	A concrete slump test is used to test for the fluidity, or workability, of concrete. It's a crude, but quick test often used to measure the effect of polymer additives that are mixed with the concrete to improve workability.
	
	The concrete mixture is prepared with a polymer additive. The mixture is placed in a mold and filled to the top. The mold is inverted and removed. The height of the mold minus the height of the remaining concrete pile is called the "slump". 
	
	.. image:: ../figures/least-squares/concrete-slump.png
		:alt:	../figures/least-squares/concrete-slump.svg
		:scale: 70
		:width: 750px
		:align: center

	Your company provides the polymer additive, and you are developing an improved polymer formulation, call it B, that hopefully provides the same slump values as your existing polymer, call it A. Formulation B costs less money than A, but you don't want to upset, or loose, customers by varying the slump value too much.
	
	#.	You have a single day to run your tests (experiments). Preparation, mixing times, measurement and clean up take 1 hour, only allowing you to run 10 experiments. Describe all precautions, and why you take these precautions, when planning and executing your experiment. Be very specific in your answer (use bullet points).

	#.	The following slump values were recorded over the course of the day:

		==========  ================
		Additive	Slump value [cm]
		==========  ================
		A           5.2            
		A           3.3            
		B           5.8            
		A           4.6            
		B           6.3            
		A           5.8            
		A           4.1            
		B           6.0            
		B           5.5            
		B           4.5            
		==========  ================
		
		What is your conclusion on the performance of the new polymer formulation (system B)?  Your conclusion must either be "send the polymer engineers back to the lab" or "let's start making formulation B for our customers". Explain your choice clearly.
		
		To help you, :math:`\overline{x}_A = 4.6` and :math:`s_A = 0.97`. For system B: :math:`\overline{x}_B = 5.62` and :math:`s_B = 0.69`.
		
		*Note*: In your answer you must be clear on which assumptions you are using and, where necessary, why you need to make those assumptions.
	
	#.	Describe the circumstances under which you would rather use a paired test for differences between polymer A and B.
	
	#.	What are the advantage(s) of the paired test over the unpaired test?  

	#.	Clearly explain which assumptions are used for paired tests, and why they are likely to be true in this case?
	
	#.	The slump tests were actually performed in a paired manner, where pairing was performed based on the cement supplier. Five different cement suppliers were used:
	
		==========  =======================  =======================
		Supplier    Slump value [cm] from A  Slump value [cm] from B
		==========  =======================  =======================
		1           5.2                      5.8
		2           3.3                      4.5
		3           4.6                      6.0
		4           5.8                      5.5
		5           4.1                      6.2
		==========  =======================  =======================

		Use these data, and provide, if necessary, an updated recommendation to your manager.
	
.. answer::
	:fullinclude: no
	
	#.	The basic rule is to control what you can and randomize against what you cannot. You should have mentioned some of these items:
	
		*	Control: clean equipment thoroughly between runs.
		*	Control: other factors that might affect the slump: temperature, humidity.
		*	Control: ensure the same person prepares all mixtures, or randomize the allocation of people if you have to use more than 1 person. Don't let person 1 prepare all the A mixtures and person 2 the B mixtures.
		*	Control: mixing times and how the mixture is created could have an effect. This should ideally be done by the same person.
		*	Randomize the order of all the A and B experiments: don't run all the A's, then all the B's, as that will confound with other factors. For example, even though temperature might vary during the day, if we randomize the run order, then we prevent temperature from affecting the results.
		*	Use raw materials (cement, binder, other ingredients) from all possible suppliers. And the supplier raw materials should be representative.

	#.	We will initially assume that :math:`\mu_A = \mu_B`, in other words, the outcome is "let's start making formulation B for our customers". We will construct a confidence interval for the difference, :math:`\mu_B - \mu_A` and interpret that CI.
	
		*	Assume the slump values within each group are independent, which will be true if we take the precautions above. We do this because then we can use the central limit theorem (CLT) to state :math:`\overline{x}_A \sim \mathcal{N}\left(\mu_A, \sigma_A^2/n_A \right)` and that :math:`\overline{x}_B \sim \mathcal{N}\left(\mu_B, \sigma_B^2/n_B \right)`.
		
		*	Note: we don't require the samples within each group to be normally distributed.
		
		*	Assume the variances are the same: :math:`\sigma_A^2 = \sigma_B^2 = \sigma^2`: this is required to simplify the next step.
		
		*	Assume the :math:`\overline{x}_A` and :math:`\overline{x}_B` means are independent. This allows us to calculate a variance value,
			:math:`\mathcal{V} \left\{\overline{x}_B - \overline{x}_A \right\}` from which we can create a :math:`z`-value for :math:`\mu_B - \mu_A`:
			
			.. math::
					
					z = \frac{\left(\overline{x}_B - \overline{x}_A \right) - \left(\mu_B - \mu_A\right)}{\sqrt{\mathcal{V} \left\{\overline{x}_B - \overline{x}_A \right\}}}
					
			That denominator variance can be written as: 
			
			.. math::
			
				\mathcal{V} \left\{\overline{x}_B - \overline{x}_A\right\} &= \mathcal{V} \left\{\overline{x}_B \right\} + \mathcal{V} \left\{\overline{x}_A\right\}\\
					&= \sigma^2\left(\frac{1}{n_B} + \frac{1}{n_A} \right)
					
			using our previous assumption that the variances are equal. We can verify this with an :math:`F`-test, but won't do it here.
	
			Because we do not have an external estimate of the variance, :math:`\sigma^2`, available, we must assume a good estimate for it can be found by  pooling the estimated variances of the group A and B samples (which requires our equal variance assumption from earlier).
			
			.. math::
			
				s_P^2 &= \frac{4s_A^2 + 4s_B^2}{4 + 4} \\
				s_P^2 &= \frac{4(0.97)^2 + 4(0.69)^2}{4 + 4} = 0.709\\
				
			This pooling also gives us 8 degrees of freedom for the :math:`t`-distribution, which is how the :math:`z`-value is distributed. 
			
			Using that :math:`z`-value and filling our assumed difference of zero for the true means, we can construct a 95% confidence interval:
			
			.. math::
					
				\begin{array}{rcccl} 
					-c_t &\leq& z	&\leq & +c_t \\
					(\overline{x}_B - \overline{x}_A) - c_t \sqrt{s_P^2 \left(\frac{1}{n_B} + \frac{1}{n_A}\right)}	&\leq& \mu_B - \mu_A	&\leq &  (\overline{x}_B - \overline{x}_A) + c_t \sqrt{s_P^2 \left(\frac{1}{n_B} + \frac{1}{n_A}\right)}\\
					1.02 - 2.3 \sqrt{0.709 \left(\frac{1}{5} + \frac{1}{5}\right)} 	&\leq& \mu_B - \mu_A	&\leq& 1.02 + 2.3 \sqrt{0.709 \left(\frac{1}{5} + \frac{1}{5}\right)} \\
					-0.21	&\leq& \mu_B - \mu_A	&\leq&   2.2
				\end{array}
				
			The statistical conclusion is that there is **no difference between formulation A and B**, since the CI spans zero. However, the practical interpretation is that the CI only just contains zero, and this should cause us to stop, and really consider the risk of the statistical conclusion.
			
			If one of the data points were in error just slightly, or if we ran a single additional experiment, it is quite possible the CI will *not span zero* anymore. In my mind, this risk is too great, and we risk upsetting the customers. 
			
			So my conclusion would be to "send the polymer engineers back to the lab" and have them improve their formulation until that CI spans zero more symmetrically.
				
	#.	A paired test should be used when there is something is common *within* pairs of samples in group A and B, but that commonality does not extend between the pairs. Some examples though you could have mentioned:
	
		Pairing is appropriate: person 1 mixes polymer for test A and B; person 2 mixes polymer for test A and B (but with different time and agitation level that person 2); person 3 mixes ... *etc*
		Pairing *not* appropriate: person 1 mixes all the polymer A samples; person 2 mixes all the polymer B samples (pairing won't fix this, and even the unpaired results will be inaccurate - see precautions mentioned above).
		Pairing appropriate: you only have enough cement and raw materials to create the concrete mixture for 2 samples: one for A and one for B. You repeat this 5 times, each time using a different supplier's raw materials.
	
		In other words, pairing is appropriate when there is something the prevents the :math:`\overline{x}_A` and :math:`\overline{x}_B` quantities from being independent. 

	#.	The one advantage of the paired test is that it will cancel out any effect that is common between the pairs (whether that effect actually affects the slump value or not). Pairing is a way to guard against *potential effect*.
	
		This makes the test more sensitive to the difference actually being tested for (formulation A vs B) and prevents confounding from the effect we are not testing for (suppliers' raw material). 
		
		Unpaired tests, but with randomization will only prevent us from being misled, however that supplier effect is still present in the 10 experimental values. The 5 difference values used in the paired tests will be free from that effect.

	#.	Pairing requires/assumes that the paired objects have something in common (e.g. a common bias due to the cement raw material). This common bias will be cancelled out once we calculate the difference in measurements.
	
		*	The difference values calculated, :math:`w_i`, are assumed to be independent. This is likely true in this case because each raw material supplier is different (unrelated) to the other.
	
		*	If the differences are independent, then the central limit theorem can be safely assumed so that the average of these differences, :math:`\overline{w} \sim \mathcal{N}\left(\mu_w, \sigma_w^2/n \right)`.

	#.	The 5 difference values are :math:`w_i = \left[ 0.6,\,\, 1.2,\,\, 1.4,\,\, -0.3, \,\, 2.1  \right]` and the average difference value is :math:`\overline{w} = 1` and its estimated variance is :math:`s_w^2 = 0.815`.

		Create the :math:`z`-value against the :math:`t`-distribution with 4 degrees of freedom (:math:`c_t = 2.78`), at the 95% confidence level, and unpack it into a confidence interval.
	
		.. math::
	
			\begin{array}{rcccl} 
				-c_t &\leq& z	&\leq & +c_t \\
				\overline{w} - c_t \sqrt{\frac{s^2}{n}}      &\leq& \mu_w       &\leq &  \overline{w} + c_t \sqrt{\frac{s^2}{n}}\\
				1 - 2.78 \sqrt{\frac{0.815}{4}}              &\leq& \mu_w       &\leq &  1 + 2.78 \sqrt{\frac{0.815}{4}}\\
				-0.12                                        &\leq& \mu_w       &\leq &  2.12
			\end{array}
		
		The interpretation is that the true difference in slump, :math:`\mu_w`, when accounting for variation from the cement raw material, is again not statistically significant, at the 95% confidence level.
	
		Practically though, there is a bit of a risk, due to the imbalance (asymmetry) in the confidence interval. It would be reluctant to hinge my company's profitability on this result, especially with the fact that there are only 4 experiments.  So my personal conclusion would be to still "send the polymer engineers back to the lab".
