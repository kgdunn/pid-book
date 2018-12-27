Exercises
=========

.. index::
	pair: exercises; process monitoring
	
.. question::

	Is it fair to say that a monitoring chart is like an online version of a :ref:`confidence interval <univariate_confidence_intervals>`?  Explain your answer.

.. answer::
	:fullinclude: no 

	This question is likely to generate a wide range of answers. No surprise, since there are strong feelings on this point in the `quality control literature <http://filebox.vt.edu/users/bwoodall/2000%20JQT%20Controversies%20and%20Contradictions.pdf>`_ as well. The confusion stems from the fact that if you are in phase 1, then no, a monitoring chart is not a confidence interval, but in phase 2, then you can argue that confidence intervals have many similarities to monitoring charts.

	But, in general, I feel the above statement is incorrect. Even in phase 2 a monitoring chart is not really like an on-line confidence interval. Mainly because a monitoring chart is intended to check for *system stability*, and to alarm quickly if the system moves away from the assumed distribution (usually a normal distribution). The monitoring limits are calculated to provide the required alarm level (the ARL). A confidence interval, on the other hand, defines the limits within which we expect to find the true population mean with a certain degree of confidence when we use a given sample of data.

	The similarity comes from the way the monitoring chart's limits are calculated: by using the concept of a confidence interval. But a monitoring chart's limits can and *should be adjusted* up or down to improve your type I and II error levels, while for a confidence interval, the only way to alter the limits is to take a different sample size, take a new sample of data, and choose a different level of confidence. But doing this, will still only find you bounds within which you expect the population mean to lie. A monitoring chart's bounds are only there to signal when things are not the same any more.

.. question::

    Use the `batch yields data <http://openmv.net/info/batch-yields>`_ and construct a monitoring chart using the 300 yield values. Use a subgroup of size 5. Report your target value, lower control limit and upper control limit, showing the calculations you made. I recommend that you write your code so that you can reuse it for other questions.

.. answer::

	Pleaseode below. The Shewhart chart's parameters are as below, with plots generated from the R code.

	-	Target = 80.4
	-	Lower control limit at 3 standard deviations = 71.1
	-	Upper control limit at 3 standard deviations = 89.6

	.. image:: ../figures/monitoring/batch-yields-monitoring.png
		:align: right
		:width: 750px
		:scale: 60
		:alt: ../figures/monitoring/batch-yields-monitoring-assignment4-2010.R

	.. dcl:: R
		:height: 800px
	
		data_file <- 'http://openmv.net/file/batch-yields.csv'
		batch <- read.csv(data_file)

		# make sure we have the expected data
		summary(batch)  
		attach(batch)

		# To get a feel for the data; 
		# looks pretty good; no unusual outliers
		plot(Yield)     

		N = length(Yield)
		N.sub = 5       # subgroup size
		subgroup <- matrix(Yield, N.sub, N/N.sub)
		N.groups <- ncol(subgroup)
		dim(subgroup)   # 5 by 60 matrix

		subgroup.sd <- apply(subgroup, 2, sd)
		subgroup.xbar <- apply(subgroup, 2, mean)

		# Take a look at what these numbers mean
		plot(subgroup.xbar, 
		     type="b", 
		     ylab="Subgroup average")
		plot(subgroup.sd, 
		     type="b",
		     ylab="Subgroup spread")

		# Report your target value, lower control 
		# limit and upper control limit, showing
		# the calculations you made. 
		target <- mean(subgroup.xbar)
		Sbar <- mean(subgroup.sd)

		# a_n value is from the table when 
		# subgroup size = 5
		an <- 0.94
		an.num <- sqrt(2)*gamma(N.sub/2)
		an.den <- sqrt(N.sub-1)*gamma(N.sub/2-0.5)
		an <- an.num/an.den
		sigma.estimate <- Sbar / an  
		LCL <- target - 3 * sigma.estimate/sqrt(N.sub)
		UCL <- target + 3 * sigma.estimate/sqrt(N.sub)
		c(LCL, target, UCL)
		plot(subgroup.xbar, 
		     ylim=c(LCL-5, UCL+5), 
		     ylab="Subgroup means", 
		     main="Shewhart chart")
		abline(h=target, col="green")
		abline(h=UCL, col="red")
		abline(h=LCL, col="red")


.. question::

    The `boards data <http://openmv.net/info/six-point-board-thickness>`_ on the website are from a line which cuts spruce, pine and fir (SPF) to produce general quality lumber that you could purchase at Rona, Home Depot, etc. The price that a saw mill receives for its lumber is strongly dependent on how accurate the cut is made. Use the data for the 2 by 6 boards (each row is one board) and develop a monitoring system using these steps.

    	a) Plot all the data. 
    	b) Now assume that boards 1 to 500 are the phase 1 data; identify any boards in this subset that appear to be unusual (where the board thickness is not consistent with most of the other operation)
    	c) Remove those unusual boards from the phase 1 data. Calculate the Shewhart monitoring limits and show the phase 1 data with these limits. Note: choose a subgroup size of 7 boards.
    	d) Test the Shewhart chart on boards 501 to 2000, the phase 2 data. Show the plot and calculate the type I error rate (:math:`\alpha`) from the phase 2 data; assuming, of course, that all the phase 2 data are from in-control operation.
    	e) Calculate the ARL and look at the chart to see if the number looks about right. Use the time information in the raw data and your ARL value to calculate how many minutes between a false alarm. Will the operators be happy with this?
    	f) Describe how you might calculate the consumer's risk (:math:`\beta`).
    	g) How would you monitor if the saws are slowly going out of alignment? 

.. answer::
	:fullinclude: no 

	This questions answers are derived in the source code (at the end).

	#.	A plot of the raw data:

		.. image:: ../figures/monitoring/boards-monitoring-raw-data.png
			:width: 750px
			:align: center
	#.	A plot of just the phase 1 data shows no particular outliers. Most people found a few outliers, that's OK - remember it is a subjective test, and if this were a process you were responsible for, then you would know more clearly what an outlier was. For me though, I didn't think any of these points were particularly unusual.

		.. image:: ../figures/monitoring/boards-monitoring-find-outliers-phase1.png
			:width: 750px
			:align: center
		
	#.	The initial Shewhart parameters found were:
	
		-	UCL = 1701
		-	Target = 1676
		-	LCL	= 1652
	
		When plotting these limits on the phase 1 data, there was only one subgroup that was found outside the limits (the first subgroup). This subgroup is removed and the limits recalculated. (For this case there was only one, very moderate, subgroup outside the limits - the new limits are basically the same). The new limits
	
		-	UCL = 1700
		-	Target = 1676
		- 	LCL = 1651
	
		A Shewhart chart of all the phase 1 data (including outliers, to highlight them) is shown here. The limits were the final limits, after iteratively removing the first unusual subgroup	. The code contains all the calculation steps.
	
		.. image:: ../figures/monitoring/boards-monitoring-Shewhart-phase1.png
			:width: 750px
			:align: center
	
	#.	Using these parameters on the phase 2 data generates the following plot:

		.. image:: ../figures/monitoring/boards-monitoring-Shewhart-phase2.png
			:width: 750px
			:align: center
		
		Assuming the subgroups in phase 2 are all in control, the :math:`\alpha` value is sum of the points outside the limits, divided by the total number of subgroups in phase 2 = 9/214 = 4.2%. This is much greater than the theoretically expected :math:`\alpha` of 0.27%.
	
		Notice though there is a group of points all on one side of the target line. According to the Western Electric rules, a group of more than 8 points on one side of the target line is highly improbable and an alarm should be raised. This indicates that these phase 2 testing data are likely not from in-control operation.

	#.	The ARL = :math:`1/\alpha = 1/0.042` = 23.8; i.e. 1 subgroup in every 24 will lie outside the control limits, even if that subgroup is from in-control operation. That number looks about right from the above phase 2 chart, although, most of the outliers seem to occur in the last half of the chart (see answer to part 4). The data set comes from about 5 hours and 15 minutes (315 minutes) of operation; during this time there were 286 subgroups that would have been shown on a real Shewhart chart. With an ARL of 24 subgroups, there would be about 12 (286/24) false alarms over these 315 minutes. In other words a false alarm about once every 26 minutes. This is much too high for practical use. Either the limits must be made wider, or this data really is not from in-control operation.

		
	#.	To calculate the consumer's risk (:math:`\beta`) we require a period of data where we know the blades have shifted, so that the board thickness has been increased or decreased to a new level (mean operating point). Using that out of control, or unstable data, we calculate Shewhart subgroups as usual, and count the number of data points falling within the current LCL and UCL. A count of those in control subgroups divided by the total number of these out of control subgroups would be an estimate of :math:`\beta`.

	#.	As the blades go out of alignment, the variability in the thickness values increases. Two ways to monitor this are

		-	To plot the subgroup standard deviation over time. I have added the nonparametric regression lines against time on the plot to highlight how the variability increases over time. This indicates to me that this data probably was not from in control operation. This is the reality in most processes: we are never sure that the data are from in-control operation; it is always trial and error.
	
		-	Use a CUSUM chart.
	
		-	A more sensitive monitoring chart for this would be the exponentially weighted moving variance: MacGregor, J.F. and Harris, T.J., "The Exponentially Weighted Moving Variance", *Journal of Quality Technology*, **25**, p 106-118, 1993.

		.. image:: ../figures/monitoring/boards-monitoring-subgroup-standard-deviation.png
			:width: 750px
			:align: center
			:scale: 80
		

	.. literalinclude:: ../figures/monitoring/boards-monitoring-assignment4-2010.R
	       :language: s
	       :lines: 1-8, 12,14-15,19-20,22-57,61-65,67-69,73-77,79-101,105-106

.. question::

	Your process with Cpk of 2.0 experiences a drift of :math:`1.5\sigma` away from the current process operating point towards the closest specification limit. What is the new Cpk value; how many defects per million items did you have before the drift?  And after the drift?

.. answer::
	:fullinclude: yes 
	:short: The new Cpk value is 1.5.

	The new Cpk value is 1.5. The number of defects per million items at Cpk = 2.0 is 0.00098 (essentially no defects), while at Cpk = 1.5 it is 3.4 defects per million items. You only have to consider one-side of the distribution, since Cpk is by definition for an uncentered process, and deals with the side closest to the specification limits.

	.. dcl:: R

		Cpk <- 1.5
		n.sigma.distance <- 3 * Cpk
		defects.per.million <- pnorm(-n.sigma.distance, mean=0, sd=1) * 1E6
	
.. question::

	Which type of monitoring chart would be appropriate to detect unusual spikes (outliers) in your production process?
	
.. answer::

	A Shewhart chart has no memory, and is suited to detecting unusual spikes in your production. CUSUM and EWMA charts have memory, and while they would pick up this spike, they would also create a long duration of false alarms after that. So those charts are much less appropriate.

.. question::

	A tank uses small air bubbles to keep solid particles in suspension. If too much air is blown into the tank, then excessive foaming and loss of valuable solid product occurs; if too little air is blown into the tank the particles sink and drop out of suspension. 

	.. image:: ../figures/monitoring/tank-suspension.png
		:scale: 70
		:align: right
		:width: 400px
		:alt: fake width

	#.	Which monitoring chart would you use to ensure the airflow is always near target?

	#.	Use the `aeration rate dataset <http://openmv.net/info/aeration-rate>`_ from the website and plot the raw data (total litres of air added in a 1 minute period). Are you able to detect any problems?

	#.	Construct the chart you described in part 1, and show it's performance on all the data. Make any necessary assumptions to construct the chart.

	#.	At what point in time are you able to detect the problem, using this chart?

	#.	Construct a Shewhart chart, choosing appropriate data for phase 1, and calculate the Shewhart limits. Then use the entire dataset as if it were phase 2 data.

		*	Show this phase 2 Shewhart chart.
		*	Compare the Shewhart chart's performance to the chart in part 3 of this question.

.. answer::
	:fullinclude: no 

	*Solution based on work by Ryan and Stuart (2011 class)*

	#.	A CUSUM chart would be a suitable chart to monitor that the airflow is near target. While a Shewhart chart is also intended to monitor the location of a variable, it has a much larger run length for detecting small shifts. An EWMA chart with small :math:`\lambda` (long memory) would approximate a CUSUM chart, and so would also be suitable

	#.	The aeration rate dataset is depicted below:

		.. image:: ../figures/monitoring/aeration-rate-raw-data.png
			:alt:	images/airflow-monitoring.R
			:scale: 100
			:width: 750px
			:align: center

		It is very difficult to assess problems from the raw data plot. There might be a slight upward shift around 300 and 500 minutes.

	#.	Assumptions for the CUSUM chart:

		*	We will plot the CUSUM chart on raw data, though you could use subgroups if you wanted to.
		*	The target value can be the mean (24.17) of all the data, or more robustly, use the median (24.1), especially if we expect problems with the raw data (true of almost every real data set).
	
	#.	The CUSUM chart, using the median as target value showed a problem starting to occur around :math:`t=300`. So we recalculated the median, using only data from 0 to :math:`t=200`, to avoid biasing the target value. Using this median instead, 23.95, we get the following CUSUM chart:
	
		.. image:: ../figures/monitoring/aeration-CUSUM.png
			:alt:	images/airflow-monitoring.R
			:scale: 100
			:width: 750px
			:align: center

	#.	The revised CUSUM chart suggests that the error occurs around 275 min, as evidenced by the steep positive slope thereafter. It should be noted that the CUSUM chart begins to bear a positive slope around 200 min, but this initial increase in the cumulative error would likely not be diagnosable (i.e. using a V-mask).

		.. literalinclude:: ../figures/monitoring/aeration-rate-monitoring.R
			:language: s
	
	#.	Using the iterative Shewhart code from the previous question, we used

	 	*	Phase I was taken far enough away from the suspected error: 0 - 200 min
	 	*	Subgroup size of :math:`n=5`
		*	:math:`\bar{\bar{x}} = 23.9`
		*	:math:`\bar{S} = 1.28`
		*	:math:`a_n = 0.940`
		*	LCL = :math:`23.9 - 3\cdot\frac{1.28}{0.940\sqrt{5}}= 22.1`
		*	UCL = :math:`23.9 + 3\cdot\frac{1.28}{0.940\sqrt{5}}= 25.8`
	
	The Shewhart chart applied to the entire dataset is shown below. In contrast to the CUSUM chart, the Shewhart chart is unable to detect the problem in the aeration rate. Unlike the CUSUM chart, which has infinite memory, the Shewhart chart has no memory and cannot adequately assess the location of the monitored variable in relation to its specified target. Instead, the Shewhart chart merely monitors aeration rate with respect to the control limits for the process. Since the aeration rate does not exceed the control limits for the process (i.e. process remains in control), the Shewhart chart does not detect any abnormalities. 

		.. image:: ../figures/monitoring/aeration-Shewhart-chart.png
			:scale: 100
			:width: 750px
			:align: center
	
	If you used the Western Electric rules, in addition to the Shewhart chart limits, you would have picked up a consecutive sequence of 8 points on one side of the target around :math:`t=350`.

.. question::

	Do you think a Shewhart chart would be suitable for monitoring the closing price of a stock on the stock market?  Please explain your answer if you agree, or describe an alternative if you disagree.
	
.. answer::

	No, a Shewhart chart is not suitable for monitoring stock prices. Stock prices are volatile variables (not stable), so there is no sense in monitoring their location. Hopefully the stock is moving up, which it should on average, but the point is that stock prices are not stable. Nor are stock prices independent day-to-day.
	
	So what aspect of a stock price is stable?  The difference between the opening and closing price of a stock is remarkably stationary. Monitoring the day-to-day change in a stock price would work. Since you aren't expected to know this fact, any reasonable answer that attempts to monitor a *stable* substitute for the price will be accepted. E.g. another alternative is to remove the linear up or down trend from a stock price and monitor the residuals. 
		
	There are many alternatives; if this sort of thing interests you, you might find the area called `technical analysis <https://en.wikipedia.org/wiki/Technical_analysis>`_ worth investigating. An EWMA chart is widely used in this sort of analysis.
	
	
.. question::

	Describe how a monitoring chart could be used to prevent over-control of a batch-to-batch process. (A batch-to-batch process is one where a batch of materials is processed, followed by another batch, and so on).

.. answer::
	
	Over-control of any process takes place when too much corrective action is applied. Using the language of feedback control, your gain is the right sign, but the magnitude is too large. Batch processes are often subject to this phenomenon: e.g. the operator reduces the set-point temperature for the next batch, because the current batch produced product with a viscosity that was too high. But then the next batch has a viscosity that is too low, so the operator increases the temperature set-point for the following batch. This constant switching is known as over-control (the operator is the feedback controller and his/her gain is too high, i.e. they are over-reacting).
		
	A monitoring chart such as a Shewhart chart would help the operator: if the previous batch was within the limits, then s/he should not take any corrective action. Only take action when the viscosity value is outside the limits. An EWMA chart would additionally provide a one-step ahead prediction, which is an advantage.
	
.. question::

	You need to construct a Shewhart chart. You go to your company's database and extract data from 10 periods of time lasting 6 hours each. Each time period is taken approximately 1 month apart so that you get a representative data set that covers roughly 1 year of process operation. You choose these time periods so that you are confident each one was from in control operation. Putting these 10 periods of data together, you get one long vector that now represents your phase 1 data.

		-	There are 8900 samples of data in this phase 1 data vector.
		-	You form subgroups: there are 4 samples per subgroup and 2225 subgroups.
		-	You calculate the mean within each subgroup (i.e. 2225 means). The mean of those 2225 means is 714.
		-	The standard deviation within each subgroup is calculated; the mean of those 2225 standard deviations is 98.

	#.	Give an unbiased estimate of the process standard deviation? 

	#.	Calculate lower and upper control limits for operation at :math:`\pm 3` of these standard deviations from target. These are called the action limits.

	#.	Operators like warning limits on their charts, so they don't have to wait until an action limit alarm occurs. Discussions with the operators indicate that lines at 590 and 820 might be good warning limits. What percentage of in control operation will lie inside the proposed warning limit region?
	
.. answer::
	:fullinclude: no 
	:short: Unbiased estimate of the process standard deviation = 106.4; UCL = 874; LCL = 554.
	
	#.	An unbiased estimate of the process standard deviation is :math:`\hat{\sigma} = \frac{\overline{S}}{a_n} = \frac{98}{0.921} = \mathrm{106.4}`, since the subgroup size is :math:`n=4`.
	#.	Using the data provided in the question:

		.. math::

			\text{UCL} &= \overline{\overline{x}} + 3 \frac{\overline{S}}{a_n \sqrt{n}} = 714 + 3 \times \frac{98}{0.921 \times 2 } = \mathrm{874} \\
			\text{LCL} &= \overline{\overline{x}} - 3 \frac{\overline{S}}{a_n \sqrt{n}} = 714 - 3 \times \frac{98}{0.921 \times 2 } = \mathrm{554}

	#.	Since Shewhart charts assume a normal distribution in their derivation, we can use the same principle to calculate a :math:`z`-value, and the fraction of the area under the distribution. But you have to be careful here: which standard deviation do you use to calculate the :math:`z`-value?   You should use the subgroup's standard deviation, not the process standard deviation. The Shewhart chart shows the subgroup averages, so the values of 590 and 820 refer to the subgroup values.

	If that explanation doesn't make sense, think of the central limit theorem: the mean of a group of samples, :math:`\overline{x} \sim \mathcal{N}\left(\mu, \sigma^2/n\right)`, where :math:`\sigma^2` is the process variance, and :math:`\sigma^2/n` is the subgroup variance of :math:`\overline{x}`.

	.. math::
		z_{\text{low}}  &= \frac{x_\text{low} - \overline{\overline{x}}}{\hat{\sigma}/\sqrt{n}} = \frac{590 - 714}{106.4/\sqrt{4}} = -2.33 \\
		z_{\text{high}} &= \frac{x_\text{high} - \overline{\overline{x}}}{\hat{\sigma}/\sqrt{n}} =\frac{820 - 714}{106.4/\sqrt{4}} = +2.00

	The area below -2.33 is ``pnorm(-2.33) = 0.009903076``, though I will accept any value around 1%, eyeballed from the printed tables. The area below +2.00 is 97.73%, which was on the tables already. So the total amount of normal operation within the warning limits is 97.73-1.00 = **96.7%**.

	The asymmetry in their chosen warning limits might be because a violation of the lower bound is more serious than the upper bound.
	
.. question::

	.. From the final exam, 2010

	If an exponentially weighted moving average (EWMA) chart can be made to approximate either a CUSUM or a Shewhart chart by adjusting the value of :math:`\lambda`, what is an advantage of the EWMA chart over the other two?  Describe a specific situation where you can benefit from this.
		
.. answer::
	:fullinclude: no 
	
	The EWMA chart not only provides control limits for monitoring a process, it also provides a one-step-ahead prediction of the variable being monitored. This is particularly beneficial as the EWMA chart's prediction can be used to adjust process conditions, should the prediction show the process heading towards, or outside, the control limits. This means that changes to the process are only made if they are required. This is extremely important on slow-moving processes, which are prone to overly aggressive control.
		
.. question::

	.. From the final exam, 2010

	The most recent estimate of the process capability ratio for a key quality variable was 1.30, and the average quality value was 64.0. Your process operates closer to the lower specification limit of 56.0. The upper specification limit is 93.0.

	What are the two parameters of the system you could adjust, and by how much, to achieve a capability ratio of 1.67, required by recent safety regulations. Assume you can adjust these parameters independently.
	
.. answer::
	:fullinclude: no 
		
	The process capability ratio for an uncentered process, :math:`\text{PCR}_\text{k}`, is given by: 
	
	.. math::
		\text{PCR}_\text{k} = \min \left( \frac{\text{Upper specification limit} - \overline{\overline{x}}}{3\sigma};  \frac{\overline{\overline{x}} - \text{Lower specification limit}}{3\sigma} \right)
		
	The two adjustable parameters are :math:`\overline{\overline{x}}`, the process target (operating point) and :math:`\sigma`, the process variance. The current process standard deviation is:
	
	.. math::
		1.30 &= \frac{64.0 - 56.0}{3\sigma} \\
		\sigma &= \frac{64.0 - 56.0}{3 \times 1.30} = 2.05
	
	*	Adjusting the *operating point* (we would expect to move the operating point away from the LSL):
	
		.. math::
			1.67 &= \frac{\overline{\overline{x}} - 56.0}{3 \times 2.05}\\
			\overline{\overline{x}} &= 56.0 + 1.67 \times 3 \times 2.05  = 66.3
			
		So the operating point increases from 64.0 to 66.3 to obtain a higher capability ratio.
		
	*	Adjusting the *process standard deviation* (we would have to assume we can decrease the standard deviation, keeping the operating point fixed):
	
		.. math::
			1.67 &= \frac{64.0 - 56.0}{3 \times \sigma}\\
			\sigma &= \frac{64.0 - 56.0}{3 \times 1.67} = 1.60

		Decrease the process standard deviation from 2.05 to 1.60.
	
.. question::

	A bagging system fills bags with a target weight of 37.4 grams and the lower specification limit is 35.0 grams. Assume the bagging system fills the bags with a standard deviation of 0.8 grams:

	#.	What is the current Cpk of the process? 
	#.	To what target weight would you have to set the bagging system to obtain Cpk=1.3? 
	#.	How can you adjust the Cpk to 1.3 without adjusting the target weight (i.e. keep the target weight at 37.4 grams)?

.. answer::
	:fullinclude: no 
	:short: Current Cpk = 1.0

	#.	Recall the Cpk is defined relative to the closest specification limit. So in this case it must be due to the lower limit. Cpk = :math:`\frac{\overline{\overline{x}} - LSL}{3\sigma} = \frac{37.4 - 35.0}{3 \times 0.8} = \mathrm{1.0}` 
	#.	To obtain Cpk = 1.3 we solve the above equation for :math:`\overline{\overline{x}} = 1.3 \times 3 \times 0.8 + 35.0 = \mathrm{38.12}` grams.
	#.	Changing the lower specification limit is not an option to raise Cpk, because the bags are sold as containing 35.0 grams of snackfood. Changing the specification limit is in general an artificial way of changing Cpk. The only practical way to improve Cpk is to decrease the process variance (e.g. using better equipment with tighter control). The new :math:`\sigma = \frac{37.4 - 35.0}{3 \times 1.3} = \mathrm{0.615}` grams.
	
.. question::

	Plastic sheets are manufactured on your blown film line. The Cp value is 1.7. You sell the plastic sheets to your customers with specification of 2 mm :math:`\pm` 0.4 mm.

		#.	List three important assumptions you must make to interpret the Cp value.
		#.	What is the theoretical process standard deviation, :math:`\sigma`?
		#.	What would be the Shewhart chart limits for this system using subgroups of size :math:`n=4`?
		#.	Illustrate your answer from part 2 and 3 of this question on a diagram of the normal distribution.

.. answer::
	:fullinclude: no 
	
	#.	The notes show that Cp values require us to assume that (a) the process values follow a normal distribution, the process was centered when the data were collected, and (c) that the process was stable (use a monitoring chart to verify this last assumption).
	#.	The range from the lower to the upper specification limit is 0.8 mm, which spans 6 standard deviations. Given the Cp value of 1.7, the process standard deviation must have been :math:`\sigma = \frac{0.8}{1.7 \times 6} = \mathrm{0.0784}` mm.
	#.	This time we have the process standard deviation, so there is no need to estimate it from historical phase 1 data (remember the assumption that Cp and Cpk value are calculated from stable process operation?). The Shewhart control limits would be: :math:`\overline{\overline{x}} \pm 3 \times \frac{\sigma}{\sqrt{n}} = 2 \pm 3 \times 0.0784 / 2`. The LCL = 1.88 mm and the UCL = 2.12 mm.
	#.	An illustration is shown here with the USL, LSL, LCL and UCL, and target values. This question merely required you to show the LCL and UCL within the LSL and USL, on any normal distribution curve. However, for illustration, I have added to the diagram the distribution for the Shewhart chart (thicker line) and distribution for the raw process data (thinner line). 

	.. image:: ../figures/monitoring/plastic-sheet-control-specification-limits.png
		:scale: 80
		:align: center
		:width: 600px

	The R code used to generate this figure:

	.. literalinclude:: ../figures/monitoring/plastic-sheet-control-specification-limits.R
			:language: s
			:lines: 3-44
			
.. question::

	.. Final exam, 2010
	
	The following charts show the weight of feed entering your reactor. The variation in product quality leaving the reactor was unacceptably high during this period of time. 

	.. image:: ../figures/monitoring/monitoring-chart-cycling.png
		:alt:	../figures/monitoring/monitoring-chart-cycling.R
		:scale: 80
		:width: 750px
		:align: center	

	#.	What can your group of process engineers learn about the problem, using the time-series plot (100 consecutive measurements, taken 1 minute apart). 	
	#.	Why is this variability not seen in the Shewhart chart?
	#.	Using concepts described elsewhere in this book, why might this sort of input to the reactor have an effect on the quality of the product leaving the reactor?

.. answer::
	:fullinclude: no 

	#.	The time-series plot shows a cyclical, almost saw-tooth, pattern in the weight of feed entering. I would investigate the feeding equipment to see what is leading to these fluctuations in the feed weight. Perhaps some rotary device is responsible for the periodic variation.

	#.	The variability is not seen in the Shewhart monitoring chart. The Shewhart chart used subgroups of size 5 (20 Shewhart samples for 100 time-series samples). These fluctuations obviously cancel out when calculating the Shewhart subgroups (a limitation of the Shewhart chart).

	#.	As engineers we are aiming for stability in our processes; stability in the raw material characteristics, stability in how we operate the process over time and minimizing as many disturbances as possible. If we can do this, it will lead to greatly improved consistency in our products (low output variability). Having this sort of input to the reactor means we have to provide apply (feedback) control to counteract it. In this case the feedback control may not have been effective to eliminate the feed variation, or the feedback control itself caused other disruptions to the process quality.
				
.. question::

	You will come across these terms in the workplace. Investigate one of these topics, using the Wikipedia link below to kick-start your research. Write a paragraph that (a) describes what your topic is and (b) how it can be used when you start working in a company after you graduate, or how you can use it now if you are currently working.

		- `Lean manufacturing <https://en.wikipedia.org/wiki/Lean_manufacturing>`_
		- `Six sigma <https://en.wikipedia.org/wiki/Six_Sigma>`_ and the DMAIC cycle. See the `list of companies <https://en.wikipedia.org/wiki/List_of_Six_Sigma_companies>`_ that use six sigma tools.
		- `Kaizen <https://en.wikipedia.org/wiki/Kaizen>`_ (a component of `The Toyota Way <https://en.wikipedia.org/wiki/The_Toyota_Way>`_)
		- `Genchi Genbutsu <https://en.wikipedia.org/wiki/Genchi_Genbutsu>`_  (also a component of `The Toyota Way <https://en.wikipedia.org/wiki/The_Toyota_Way>`_)

		In early 2010 Toyota experienced some of its worst press coverage on this very topic. `Here is an article <http://www.reuters.com/article/2010/02/07/us-toyota-us-manufacturers-analysis-idUSTRE6161RV20100207>`_ in case you missed it.

.. _monitoring-kappa-number-question:

.. question::

	The Kappa number is a widely used measurement in the pulp and paper industry. It can be measured on-line, and indicates the severity of chemical treatment that must be applied to a wood pulp to obtain a given level of whiteness (i.e. the pulp's bleachability). Data on the `website <http://openmv.net/info/kappa-number>`_ contain the Kappa values from a pulp mill. Use the first 2000 data points to construct a Shewhart monitoring chart for the Kappa number. You may use any subgroup size you like. Then use the remaining data as your phase 2 (testing) data. Does the chart perform as expected?

.. answer::
	:fullinclude: no 
	:short: The intention of this question is for you to experience the process of iteratively calculating limits from phase 1 data and applying them to phase 2 data.	

	The intention of this question is for you to experience the process of iteratively calculating limits from phase 1 data and applying them to phase 2 data.

	The raw data for the entire data set looks as follows. There are already regions in the phase 2 data that we expect to not be from normal operation (around 2500 and 2900)

	.. image:: ../figures/monitoring/Kappa-raw-data.png
		:align: center
		:width: 750px
	
	I used subgroups of size 6 for the figures in this answer, however, the code below is very general, and you can regenerate the plots if you chose a different subgroup size. Just change one of the lines near the top. 

	The upper and lower control limits are calculated, and with a subgroup size of :math:`n=6`, there are 333 subgroups and the limits are: UCL = 18.26, target = 21.73, and UCL = 25.21. This is illustrated on the phase 1 data here:

	.. image:: ../figures/monitoring/Kappa-phaseI-first-round.png
		:align: center
		:width: 750px
	
	Next we remove the subgroups which lie outside the limits. Please try using the R code to see how to do it automatically. The new limits, after removing the subgroups beyond the limits from the first round are: LCL = 18.24, target = 21.71 and UCL = 25.18. They barely changed. But the updated plot with subgroups removed is now shown below. There is no need to perform another round of pruning. Only if you used a subgroup size of 4 would you need to do a third round. You could also have just shifted the limits to a different level, for example, to :math:`\pm 4` standard deviations. We can do this if we have enough process knowledge to understand the implication of it, in terms of profit.

	.. image:: ../figures/monitoring/Kappa-phaseI-second-round.png
		:align: center
		:width: 750px

	Now apply these control limits to the phase 2 data. The plot is shown below:

	.. image:: ../figures/monitoring/Kappa-phaseII-testing.png
		:align: center
		:width: 750px
	
	The limits identify 2 prolonged periods of unusual operation at sequence point 80 and 140. If we apply the Western Electric rules, we see a third unusual region around sequence step 220. A few other alarms are scattered in the phase 2 data. About 7% of the subgroups lie outside these control limits, so these phase 2 data are definitely not from in-control operation; which we expected from the raw data plot at the start of this question.

	The code for all the calculation steps is provided here:

	.. literalinclude:: ../figures/monitoring/Kappa-number-monitoring.R
	       :language: s
	       :lines: 18-32,36-40,42-80,84-89,91-108,112-117,119-136,140-145,147-151,155-160,162-

.. question::

	In this section we showed how one can monitor any variable in a process. Modern instrumentation though capture a wider variety of data. It is common to measure point values, e.g. temperature, pressure, concentration and other hard-to-measure values. But it is increasingly common to measure spectral data. These spectral data are a vector of numbers instead of a single number. 
	
	Below is an example from a pharmaceutical process: a complete spectrum can be acquired many times per minute, and it gives a complete chemical fingerprint or signature of the system. There are 460 spectra in figure below; they could have come, for example, from a process where they are measured 5 seconds apart. It is common to find fibre optic probes embedded into pipelines and reactors to monitor the progress of a reaction or mixing.

	Write a few bullet points how you might monitor a process where a spectrum (a vector) is your data source, and not a "traditional" single point measurement, like a temperature value.

	.. /Users/kevindunn/ConnectMV/Datasets/Spectral data set - NIR/plot_spectra.py

	.. image:: ../figures/monitoring/pharma-spectra.jpg
		:width: 750px
		:align: center
		:scale: 80

.. answer::
	:fullinclude: no 

	A complete spectrum (vector) of values is obtained with every observation. To monitor a process using one of the charts learned about so far (Shewhart, CUSUM, or EWMA chart) we have to reduce this vector down to a single number. Any of these methods will do:

	-	Use a single point at a particular wavelength in the spectrum (e.g. the peak at 1200 nm or 1675 nm).
	-	Use a weighted sum of a region of the spectrum, or the integrated area under a region in the spectrum (these 2 approaches are similar/equivalent)
	-	Use the spectrum to predict a certain property of interest, and then monitor that property instead. For example: use the spectrum to predict the colour of cookies (i.e. how well baked they are) and monitor the "well-bakedness" characteristic.

	Later on we will learn about :ref:`multivariate monitoring methods <LVM_monitoring>`.

.. question::

	.. Advanced question

	The carbon dioxide measurement is available from a `gas-fired furnace <http://openmv.net/info/gas-furnace>`_. These data are from phase 1 operation.

	#.	Calculate the Shewhart chart upper and lower control limits that you would use during phase 2 with a subgroup size of :math:`n=6`. 
	#.	Is this a useful monitoring chart? What is going in this data?
	#.	How can you fix the problem?

.. answer:: 

	*Solution based on work by Ryan and Stuart (2011 class)*

	First a plot of the raw data will be useful:

	.. image:: ../figures/monitoring/CO2-raw-data.png
		:scale: 75
		:width: 750px
		:align: center

	#.	Assuming that the CO\ :sub:`2` data set is from phase 1 operation, the control limits were calculated as follows:

		*	Assume subgroups are independent
		*	:math:`\bar{\bar{x}} =\frac{1}{K}\sum\limits_{k=1}^K\bar{x}_k= 53.5`\
		*	:math:`\bar{S} =\frac{1}{K}\sum\limits_{k=1}^K s_k= 1.10`
		*	:math:`a_n =0.952` 
		*	LCL = :math:`53.5 -3 \cdot\frac{1.10}{0.952\sqrt{6}} = 52.08`
		*	UCL = :math:`53.5 +3 \cdot\frac{1.10}{0.952\sqrt{6}} = 54.92`

	#.	The Shewhart chart using a subgroup of size 6 is not a useful monitoring chart. There are too many false alarms, which will cause the operators to just ignore the chart. The problem is that the first assumption of independence is not correct and has a detrimental effect, as shown in :ref:`a previous question <lack_of_independence_question>`. 

		.. image:: ../figures/monitoring/CO2-phaseI-first-round.png
			:scale: 75
			:width: 750px
			:align: center

	#.	One approach to fixing the problem is to subsample the data, i.e. only use every :math:`k^\text{th}` data point as the raw data, e.g. :math:`k=10`, and then form subgroups from that sampled data.

		Another is to use a larger subgroup size. Use the `autocorrelation function <https://en.wikipedia.org/wiki/Autocorrelation>`_, and the corresponding ``acf(...)`` function in R to verify the degree of relationship. Using this function we can see the raw data are unrelated after the 17th lag, so we could use subgroups of that size. However, even then we see the Shewhart chart showing frequent violation, though fewer than before.

		Yet another alternative is to use an EWMA chart, which takes the autocorrelation into account. However, the EWMA chart limits are found from the assumption that the subgroup means (or raw data, if subgroup size is 1), are independent.

		So we are finally left with the conclusion that perhaps there data really are not from in control operation, or, if they are, we must manually adjust the limits to be wider.

	.. literalinclude:: ../figures/monitoring/CO2-question.R
		:language: s

.. question::

	The percentage yield from a batch reactor, and the purity of the feedstock are available as the `Batch yield and purity <http://openmv.net/info/batch-yield-and-purity>`_ data set. Assume these data are from phase 1 operation and calculate the Shewhart chart upper and lower control limits that you would use during phase 2. Use a subgroup size of :math:`n=3`.

	#.	What is phase 1?
	#.	What is phase 2?
	#.	Show your calculations for the upper and lower control limits for the Shewhart chart on the *yield value*.
	#.	Show a plot of the Shewhart chart on these phase 1 data.

.. answer:: 

	*Solution based on work by Ryan McBride, Stuart Young, and Mudassir Rashid (2011 class)*
	
	#.	Phase 1 is the period from which historical data is taken that is known to be "in control". From this data, upper and lower control limits can be established for the monitored variable that contain a specified percent of all in control data.

	#.	Phase 2 is the period during which new, unseen data is collected by process monitoring in real-time. This data can be compared with the limits calculated from the "in control" data.

	#.	Assuming the dataset was derived from phase 1 operation, the batch yield data was grouped into subgroups of size 3. However, since the total number of data points (N=241) is not a multiple of three, the data set was truncated to the closest multiple of 3, i.e. :math:`N_{new} = 240`, by removing the last data point. Subsequently, the mean and standard deviation were calculated for each of the 80 subgroups. From this data, the lower and upper control limits were calculated as follows:

		.. math::	

			\overline{\overline{x}} &= \frac{1}{80}\sum\limits_{k=1}^{80}\overline{x}_k = \bf{75.3}\\
			\overline{S}			&= \frac{1}{80}\sum\limits_{k=1}^{80}s_k = \bf{5.32}\\
			\text{LCL}				&= \overline{\overline{x}} - 3\cdot\frac{\overline{S}}{a_n\sqrt{n}} = \bf{64.9}\\
			\text{UCL}				&= \overline{\overline{x}} + 3\cdot\frac{\overline{S}}{a_n\sqrt{n}} = \bf{85.7}\\
			\text{using}\,\,a_n		&=  0.886\qquad \text{for a subgroup size of 3}\\
			\text{and}\,\,\overline{\overline{x}} &= 75.3

		Noticing that the mean for subgroup 42, :math:`\overline{x}_{42}=63.3`, falls below this LCL, the control limits were recalculated excluding this subgroup from phase 1 data (see R-code). Following this adjustment, the new control limits were calculated to be:

		*	LCL = 65.0
		*	UCL = 85.8

	#.	Shewhart charts for both rounds of the yield data (before and after removing the outlier):

		.. image:: ../figures/monitoring/batch-yield-phaseI-round-1-Yield.png
			:width: 750px
			:align: center
			:scale: 80

		.. image:: ../figures/monitoring/batch-yield-phaseI-round-2-Yield.png
			:scale: 80
			:width: 750px
			:align: center

	.. literalinclude:: ../figures/monitoring/batch-yield-and-purity-recursive.R
		:language: s
		
.. question::

	You will hear about 6-sigma processes frequently in your career. What does it mean exactly that a process is "6-sigma capable"? Draw a diagram to help illustrate your answer. 
