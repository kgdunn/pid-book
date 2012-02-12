.. Header notes
   -------------
	
	=====
	~~~~~
	^^^^^
	-----
	
.. MIT courseware: http://ocw.mit.edu/OcwWeb/Mechanical-Engineering/2-830JSpring-2008/VideoLectures/index.htm	
		
.. TODO list of plots
    Plot of Shewhart chart
        - just showing target + data
        - with UB and LB and data initial IC then OOC
        - with action and warning limits
	Real-time demo of monitoring lines (matplotlib animation?)
	Picture that shows (Inkscape): region of stable operation (common cause), vs region of assignable cause
	Boards thickness monitoring chart
	Show chart for Shewhart example in class
	Case study: total energy input
	
	Explain how to change Cpk if it is undesirable
	

Process monitoring in context
==============================

In the first section we learned about :ref:`visualizing data <SECTION-data-visualization>`, then we moved on to reviewing :ref:`univariate statistics <SECTION-univariate-review>`. This section combines both areas, showing how to create a system that monitors a single, univariate, value from any process. These systems are easily implemented online, and generate great value for companies that use them in day-to-day production. 

Monitoring charts are a graphical tool, enabling anyone to rapidly detect a problem by visual analysis. The next logical step after detection is to diagnose the problem, but we will cover diagnosis in the section on :ref:`latent variable models <SECTION_latent_variable_modelling>`.

This section is the last section where we deal with univariate data; after this section we start to use and deal with 2 or more variables. 

Usage examples
~~~~~~~~~~~~~~~

.. index::
	pair: usage examples; process monitoring

The material in this section is used whenever you need to rapidly detect problems. It has tangible application in many areas - in fact, you have likely encountered these monitoring charts in areas such as a hospital (monitoring a patient's heart beat), stock market charts (for intraday trading), or in a processing/manufacturing facility (control room computer screens).

	-	*Co-worker*: We need a system to ensure an important dimension on our product is stable and consistent over the entire shift.
	-	*Yourself*: We know that as the position of a manufacturing robot moves out of alignment that our product starts becoming inconsistent; more variable. How can we quickly detect this slow drift?
	-	*Manager*: the hourly average profit, and process throughput is important to the head-office; can we create a system for them to track that?
	-	*Potential customer*: what is your process capability - we are looking for a new supplier that can provide a low-variability raw material for us with |Cpk| of at least 1.6, preferably higher.
	
**Note**: process monitoring is mostly *reactive* and not *proactive*. So it is suited to *incremental* process improvement, which is typical of most improvements.

What we will cover
~~~~~~~~~~~~~~~~~~~~

We will consider 3 main charts after introducing some basic concepts: Shewhart charts, CUSUM charts and EWMA (exponentially weighted moving average) charts. The EWMA chart has an adjustable parameter that captures the behaviour of a Shewhart chart at one extreme and a CUSUM chart at the other extreme.

References and readings
~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: references and readings; process monitoring

#.	**Recommended**: Box, Hunter and Hunter, *Statistics for Experimenters*, Chapter 14 (2nd edition)

#.	**Recommended**: Montgomery and Runger, *Applied Statistics and Probability for Engineers*.

#.	Hogg and Ledolter, *Engineering Statistics*.

#.	Hunter, J.S. "`The Exponentially Weighted Moving Average <http://asq.org/qic/display-item/index.pl?item=5536>`_", *Journal of Quality Technology*, **18** (4) p 203 - 210, 1986.

#.	Macgregor, J.F. "`Using On-Line Process Data to Improve Quality: Challenges for Statisticians <http://dx.doi.org/10.1111/j.1751-5823.1997.tb00311.x>`_", *International Statistical Review*, **65**, p 309-323, 1997.

.. 
	Box, The R. A. Fisher Memorial Lecture, 1988- Quality Improvement- An Expanding Domain for the Application of Scientific Method, Phil. Trans. R. Soc. Lond. A February 24, 1989 327:617-630, [http://dx.doi.org/10.1098/rsta.1989.0017 DOI]
	
.. (Not available): Box critique of Taguchi methods: http://dx.doi.org/10.1002/qre.4680040207
..	Bisgaard, S., "`The Quality Detective: A Case Study <http://dx.doi.org/10.1098/rsta.1989.0006>`_", Philosophical Transactions of the Royal Society-A, **327**, p 499-511, 1989.
.. UMetrics book: review chapter on (M)SPC
.. MacGregors 1997 paper on MSPC
.. * Controversy between monitoring charts and hypothesis tests, Woodall, Woodall, W. Controversies and Contradictions in Statistical Process Control, JQT, 32(4), 341-350, 2000 ([http://filebox.vt.edu/users/bwoodall/ Link])
.. EWMV paper by MacGregor?
.. Box, G.E.P., Comparisons, Absolute Values, and How I Got to Go to the Folies Bergeres, Quality Engineering, 14(1), p167-169, 2001.
.. p 669 of Devore: see also Technometrics, 1989, p173-184, by David M Rocke

Concepts
~~~~~~~~~~~~~~~

Concepts and acronyms that you must be familiar with by the end of this section: 

.. OLD image: image: : ../figures/mindmaps/process-monitoring-concepts.png

	*	Shewhart chart, CUSUM chart and EWMA chart
	*	Phase 1 and phase 2 when building a monitoring system
	*	False alarms
	*	Type 1 and type 2 errors
	*	LCL and UCL
	*	Target
	*	C\ :sub:`p` and |Cpk|
	*	Outliers
	*	Real-time implementation of monitoring systems

What is process monitoring about?
===================================

Most industries have now realized that product quality is not an option. There was historical thinking that quality is equivalent of "gold-plating" your product, but that has mostly fallen away. Product quality is not a cost-benefit trade-off: it is always beneficial to you in the long-term to improve your :index:`product quality`, and for your customers as well.

As we spoke about in the :ref:`univariate review section <SECTION-univariate-review>`, good quality products (low variability) actually boost your profits by lowering costs. You have lower costs when you *do not* have to scrap off-specification product, or have to rework bad product. You have increased long-term sales with more loyal customers and improved brand reputation as a reliable and consistent supplier.

An example that most people in North America can relate to is the rise in Asian car manufacturers' market share, at the expense American manufacturers' market share. The market has the perception that Asian cars are more reliable than American cars and resale rates certainly reflect that. The perception has started to change since 2010, as North American manufacturers have become more quality conscious. That is an illustration of how lack of variability in your product can benefit you.

In order to achieve this high level of final product quality, our systems should be producing low variability product at every step of the manufacturing process. Rather than wait till the end of the process to *discover* poor quality product, we should be monitoring, in real-time, raw materials and the intermediate steps in our process. When we discover unusual variability the lofty aim is to make (permanent) process adjustments to avoid that variability from ever occurring again.

Notice here that process monitoring is not intended to be automatic feedback control. It has the same principles of quantifying unusual operation (errors), but the intention with *process monitoring* is:

*	that any process adjustments are **infrequent**, 
*	these adjustments are made **manually**, 
*	and take place due to **special causes**.

Automatic :index:`feedback control` is applied continuously by computer systems and makes short-term, temporary changes to the system to keep it at the desired target (setpoint).

Note that process monitoring is often called :index:`statistical process control` (SPC). This can lead to unnecessary confusion with process control, i.e. the design and implementation of feedback control, feedforward control and other automated control systems. We will not use the term SPC.

Monitoring charts
~~~~~~~~~~~~~~~~~~~~

We use :index:`monitoring charts`, also called :index:`control charts`, to display and detect this unusual variability. A monitoring chart is a display of one value (variable), against time, or in sequence order. These time-based plots also show some additional information: usually a target value, and one or more limits lines are superimposed on the plot. The plots are most useful when displayed in real-time, or close to real-time. There are various technical ways to express what a monitoring chart does exactly, but a general definition is that a monitoring chart helps you detect outliers and other unusual behaviour.

The key points are:

	-	it is most often a time-series plot, or some sort of sequence,
	-	a target value may be shown,
	-	one or more limit lines are shown,
	-	they are displayed and updated in real-time, or as close to real-time as possible.

Here is an example that shows these properties.

.. TODO: show a time-series on the x-axis instead

.. image:: ../figures/monitoring/demo-of-monitoring-chart.png
	:width: 750px
	:scale: 100

.. _monitoring_general_approach:

General approach
~~~~~~~~~~~~~~~~~~~~

Monitoring charts are developed in 2 phases. You will see the terminology of:

.. index:: phase 1 (monitoring charts)

*	**Phase 1**: building and testing the chart from historical data that you have collected. This phase is performed off-line, it is very iterative, and you will spend most of your time here. The primary purpose of this phase is to 

	-	find portions of the data that are from stable operation
	-	use these stable portions to calculate suitable control chart limits
	-	ensure that your chart works as expected based on historical data

.. index:: phase 2 (monitoring charts)

*	**Phase 2**: We use the monitoring chart on new, fresh data from the process. This phase is implemented with computer hardware and software for real-time display of the charts.

What should we monitor?
========================

Any variable can be monitored. However, the purpose of process monitoring is so that you can **react early** to bad, or unusual operation. This implies we should monitor variables as soon as they become available, preferably in real-time. They are more suitable than variables that take a long time to acquire (e.g. laboratory measurements). We shouldn't have to wait to the end of the production line to find our process was out of statistical control. 

Raw material data from your supplier should also be monitored as soon as it is available, e.g. when received by your company, or even earlier - before the supplier ships it to you.

These intermediate variables measured from the process are (a) available much more frequently and without delay, (b) are more precise, (c) are usually more meaningful to the operating staff than final quality variables from the lab, and (d) contain the "fingerprint" of the fault, helping the engineers with diagnosis and process adjustment (see *MacGregor, 1997*)

Note that we don't have to monitor variables that are measured only from on-line sensors. The variable could be a calculation made from the on-line measurements. For example, an energy balance could be calculated from various thermocouples on the process and the degree of mismatch in the energy balance could be critical to quality. For example, the mismatch could indicate an unexpected source of heat into or out of the process - so monitor that mismatch, rather than the raw temperature data.

..	SLIDE: organoleptic properties, Particle size distribution

Discuss one of these unit operations with your colleague. Which variables would you monitor?

- Waste water treatment process
- Tablet/pharmaceutical manufacturing
- Oil and gas (e.g. a distillation column)
- Food-processing unit
- Mineral processing plant (e.g. a flotation cell)
- Plastics processing (e.g. a twin-screw extruder)

In-control vs out-of-control
=============================

Every book on quality control gives a slightly different viewpoint, or uses different terminology for these terms.

In this book we will take "in-control" to mean that the behaviour of the process is stable over time. Note though, that in-control *does not* mean the variable of interest meets the specifications required by the customer, or set by the plant personnel. All that "in control" means is that there are no **special causes** in the data, i.e. the process is stable. A :index:`special cause`, or an :index:`assignable cause` is an event that occurs to move the process, or destabilize it. Process monitoring charts aim to detect such events. The opposite of "special cause" operation is :index:`common cause` operation.

.. note:: Our objective: quickly detect abnormal variation, and fix it by finding the root cause. In this section we look at the "detection" problem. Diagnosis and process adjustment are two separate steps that follow detection.

.. _monitoring_shewhart_chart:

Shewhart chart
==============

.. For the mean: p174 to p186 of Barnes. KGD: what does "Barnes" refer to?

A :index:`Shewhart chart <pair: Shewhart chart; process monitoring>`, named after Walter Shewhart from Bell Telephone and Western Electric, monitors that a process variable remains on target and within given upper and lower limits. It is a monitoring chart for *location*. It answers the question whether the variable's :index:`location <single: location (process monitoring)>` is stable over time.

The defining characteristics are: a target, upper and lower control limits (:index:`UCL <single: upper control limit>` and :index:`LCL <single: lower control limit>`). These action limits are defined so that no action is required as long as the variable plotted remains within the limits.

Derivation using theoretical parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define the variable of interest as :math:`x`, and assume that we have samples of :math:`x` available in sequence order. No assumption is made regarding the distribution of :math:`x`. The average of :math:`n` of these :math:`x`-values is defined as :math:`\overline{x}`, which from the :ref:`Central limit theorem <central_limit_theorem>` we know will be more normally distributed with unknown population mean :math:`\mu` and unknown population variance :math:`\sigma^2/n`, where :math:`\mu` and :math:`\sigma` refer to the distribution that samples of :math:`x` came from. The figure below shows the case for :math:`n=5`.

.. image:: ../figures/monitoring/explain-Shewhart-data-source.png
	:width: 750px
	:align: center
	:scale: 70

So by taking :index:`subgroups <single: subgroups (monitoring charts)>` of size :math:`n` values, we now have a new variable, :math:`\overline{x}` and we will define a shorthand symbol for its standard deviation: :math:`\sigma_{\overline{X}} = \sigma/\sqrt{n}`. Writing a :math:`z`-value for :math:`\overline{x}`, and its associated confidence interval for :math:`\mu` is now easy after studying :ref:`the section on confidence intervals<univariate_confidence_intervals>`:

.. math::

	z = \frac{\displaystyle \overline{x} - \mu}{\displaystyle \sigma_{\overline{X}}}

Assuming we know :math:`\sigma_{\overline{X}}`, which we usually do not in practice, we can invoke the normal distribution and calculate the probability of finding a value of :math:`z` between :math:`c_n = -3` to :math:`c_n = +3`:

.. math::
	:label: shewhart-theoretical
	
	\begin{array}{rcccl} 
		  - c_n                                              &\leq& \dfrac{\overline{x} - \mu}{\sigma_{\overline{X}}} &\leq&  +c_n\\ \\
		\overline{x}  - c_n\sigma_{\overline{X}}             &\leq&  \mu                                              &\leq& \overline{x}  + c_n\sigma_{\overline{X}} \\ \\
		\text{LCL}                                           &\leq&  \mu                                              &\leq& \text{UCL}
	\end{array}

The reason for :math:`c_n = \pm 3` is that the total area between that lower and upper bound spans 99.73% of the area (in R: ``pnorm(+3) - pnorm(-3)`` gives 0.9973). So it is highly unlikely, a chance of 1 in 370 that a data point, :math:`\overline{x}`, calculated from a subgroup of :math:`n` raw :math:`x`-values, will lie outside these bounds.

The following illustration should help connect the concept of the raw data's distribution (happens to have mean of 6 and standard deviation of 2) to the distribution of the subgroups (thicker line):

.. image:: ../figures/monitoring/explain-shewhart.png
	:alt:	../figures/monitoring/explain-shewhart.R
	:scale: 70
	:width: 750px
	:align: center

Using estimated parameters instead
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The derivation in equation :eq:`shewhart-theoretical` requires knowing the population variance, :math:`\sigma`, and assuming that our target for :math:`x` is :math:`\mu`. The latter assumption is reasonable, but we will estimate a value for :math:`\sigma` instead, using the data.

.. index:: ! phase 1 (monitoring charts)

Let's take a look at phase 1, the step where we are building the monitoring chart's limits from historical data. Create a new variable |xdb| :math:`= \displaystyle \frac{1}{K} \sum_{k=1}^{K}{ \overline{x}_k}`, where :math:`K` is the number of :math:`\overline{x}` samples we have available to build the monitoring chart, called the :index:`phase 1 <single: phase 1 (monitoring charts)>` data. Note that |xdb| is sometimes called the *grand mean*. Alternatively, just set |xdb| to the desired target value for :math:`x` or use a long portion of stable data to estimate a suitable target

The next hurdle is :math:`\sigma`. Define :math:`s_k` to be the standard deviation of the :math:`n` values in the :math:`k^\text{th}` subgroup. We do not show it here, but for a subgroup of :math:`n` samples, an unbiased estimator of :math:`\sigma` is given by :math:`\displaystyle \frac{\overline{S}}{a_n}`, where :math:`\overline{S} =  \displaystyle \frac{1}{K} \displaystyle \sum_{k=1}^{K}{s_k}` is simply the average standard deviation calculated from :math:`K` subgroups. Values for :math:`a_n` are looked up from a table, or using the formula below, and depend on the number of samples we use within each subgroup.

===========  ====== ====== ====== ====== ====== ====== ====== ====== ======
:math:`n`    2      3      4      5      6      7      8      10     15
-----------  ------ ------ ------ ------ ------ ------ ------ ------ ------
:math:`a_n`  0.7979 0.8862 0.9213 0.9400 0.9515 0.9594 0.9650 0.9727 0.9823
===========  ====== ====== ====== ====== ====== ====== ====== ====== ======

..	See Devore, page 683

More generally, using the :math:`\Gamma(...)` function, for example ``gamma(...)`` in R, or MATLAB, you can reproduce the above :math:`a_n` values.

.. math::

	a_n = \frac{\sqrt{2}\,\,\Gamma(n/2)}{\sqrt{n-1}\,\,\Gamma(n/2 - 0.5)}

Now that we have an unbiased estimator for the standard deviation from these :math:`K` subgroups, we can write down suitable :index:`lower <single: lower control limit>` and :index:`upper control limits <single: upper control limit>` for the Shewhart chart:

.. math::
	:label: shewhart-limits
	
	\begin{array}{rcccl} 
		 \text{LCL} = \overline{\overline{x}} - 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} &&  &&  \text{UCL} = \overline{\overline{x}} + 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} 
	\end{array}
	
It is highly unlikely that the data chosen to calculate the phase 1 limits actually lie within these calculated LCL and UCLs. Those portions of data not from stable operation, which are outside the limits, should not have been used to calculate these limits. Those unstable data bias the limits to be wider than required.

Exclude these :index:`outlier` data points and recompute the LCL and UCLs. Usually this process is repeated 2 to 3 times. It is wise to investigate the data being excluded to ensure they truly are from unstable operation. If they are from stable operation, then they should not be excluded. These data may be :ref:`violating the assumption of independence <monitoring_mistakes_to_avoid>`. One may consider using wider limits, or use an :ref:`EWMA control chart <monitoring_EWMA>`. 

.. rubric:: Example

Bales of rubber are being produced, with every 10th bale automatically removed from the line for testing. Measurements of colour intensity are made on 5 sides of that bale, using calibrated digital cameras under controlled lighting conditions. The rubber compound is used for medical devices, so it needs to have the correct whiteness (colour). The average of the 5 colour measurements is to be plotted on a Shewhart chart. So we have a new data point appearing on the monitoring chart after every 10th bale. 

In the above example the raw data are the bale's colour. There are :math:`n = 5` values in each subgroup. Collect say :math:`K=20` samples of 
good production bales considered to be from stable operation. No special process events occurred while these bales were manufactured.

The data below represent the average of the :math:`n=5` samples from each bale, there are :math:`K=20` subgroups.

.. math::
 	\overline{x} = [245, 239, 239, 241, 241, 241, 238, 238, 236, 248, 233, 236, 246, 253, 227, 231, 237, 228, 239, 240]

The overall average is :math:`\overline{\overline{x}} = 238.8` and :math:`\overline{S} = 9.28`. Calculate the lower and upper control limits for this Shewhart chart. Were there any points in the phase 1 data (training phase) that exceeded these limits?

	-	LCL = :math:`\overline{\overline{x}} - 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} = 238.8 - 3 \cdot \displaystyle \frac{9.28}{(0.94)(\sqrt{5})} = 225.6` 
	-	UCL = :math:`\overline{\overline{x}} + 3 \cdot \frac{\displaystyle \overline{S}}{\displaystyle a_n\sqrt{n}} = 238.8 + 3 \cdot \displaystyle \frac{9.28}{(0.94)(\sqrt{5})} = 252.0` 
	-	The group with :math:`\overline{x}` = 253 exceeds the calculated upper control limit. 
	-	That :math:`\overline{x}` point should be excluded and the limits recomputed. You can show the new :math:`\overline{\overline{x}} = 238.0` and :math:`\overline{S} = 9.68` and the new LCL = 224 and UCL = 252.
	
.. todo: show chart in class
		
.. todo: in the future, describe more clearly the difference between phase 1 and phase 2. Students were asking a lot of questions around this.

.. _monitoring_judging_performance:

Judging the chart's performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are 2 ways to :index:`judge performance of any monitoring <single: monitoring chart assessment>`, in particular here we discuss the Shewhart chart:

.. rubric:: 1. Error probability. 

We define two types of errors, Type I and Type II, which are a function of the lower and upper control limits (LCL and UCL).

You make a **type I error** when your sample is typical of normal operation, yet, it falls outside the UCL or LCL limits. We showed in the theoretical derivation that the area covered by the upper and lower control limits is 99.73%. The probability of making a type I error, usually denoted as :math:`\alpha` is then :math:`100 - 99.73 = 0.27\%`.

*Synonyms* for a **type I error**: false alarm, false positive (used mainly for testing of diseases), producer's risk (used for acceptance sampling), false rejection rate, or alpha.

You make a **type II error** when your sample really is abnormal, but falls within the the UCL and LCL limits. This error rate is denoted by :math:`\beta`, and it is a function of the degree of abnormality, which we derive next.

*Synonyms* for a **type II error**: false negative (used mainly for testing of diseases), consumer's risk (used for acceptance sampling), false acceptance rate, or beta.

To quantify the probability :math:`\beta`, recall that a Shewhart chart is for monitoring location, so we make an assumption that the new, abnormal sample comes from a distribution which has shifted its location from :math:`\mu` to :math:`\mu + \Delta\sigma` (e.g. :math:`\Delta` can be positive or negative). Now, what is the probability this new sample, which come from the shifted distribution, will fall within the existing LCL and UCL? This figure shows the probability is :math:`\beta = 1 - \text{the shaded area}`.

.. math::

	\alpha &= Pr\left(\overline{x}\,\,\text{is in control, but lies outside the limits}\right) = \text{type I error rate}\\
	\beta &= Pr\left(\overline{x}\,\,\text{is not in control, but lies inside the limits}\right) = \text{type II error rate}

.. image:: ../figures/monitoring/show-shift-beta-error.png
	:width: 500px
	:align: center
	:scale: 90

.. todo  How did Devore calculate these numbers: see p 667 of his book - it doesn't make sense to me. See my attempt in "show-shift-typeII-error.R"

..	See Montgomery and Runger, Second edition, p 313, for a possible derivation
.. \beta = pnorm(3-delta*sqrt(n)) - pnorm(-3 - delta*sqrt(n))

.. _monitoring_sluggish_shewhart_chart:

The table highlights that :math:`\beta` is a function of the amount by which the process shifts = :math:`\Delta`, where :math:`\Delta=1` implies the process has shifted up by :math:`1\sigma`. The table was calculated for :math:`n=4` and used critical limits of :math:`\pm 3 \sigma_{\overline{X}}`. You can calculate your own values of :math:`\beta` using this line of R code: ``beta <- pnorm(3 - delta*sqrt(n)) - pnorm(-3 - delta*sqrt(n))``

==============================  ====== ====== ====== ====== ====== ====== 
:math:`\Delta`                  0.25   0.50   0.75   1.00   1.50   2.00   
------------------------------  ------ ------ ------ ------ ------ ------ 
:math:`\beta` when :math:`n=4`  0.9936 0.9772 0.9332 0.8413 0.5000 0.1587
==============================  ====== ====== ====== ====== ====== ======

The key point you should note from the table is that a Shewhart chart is *not good* (it is slow) at detecting a change in the location (level) of a variable. This is surprising given the intention of the plot is to monitor the variable's location. Even a moderate shift of :math:`0.75\sigma` units :math:`(\Delta=0.75)` will only be detected around 6.7% of the time (:math:`100-93.3\%`) when :math:`n=4`. We will discuss :ref:`CUSUM charts <monitoring_CUSUM_charts>` and the Western Electric rules, next, as a way to overcome this issue.

It is straightforward to see how the type I, :math:`\alpha`, error rate can be adjusted - simply move the LCL and UCL up and down, as required, to achieve your desired error rates. There is nothing wrong in arbitrarily shifting these limits - :ref:`more on this later <monitoring_adjust_limits>` in the section on adjusting limits.

However what happens to the type II error rate as the LCL and UCL bounds are shifted away from the target?  Imagine the case where you want to have :math:`\alpha \rightarrow 0`. As you make the UCL higher and higher, the value for :math:`\alpha` drops, but the value for :math:`\beta` will also increase, since the control limits have become wider!  **You cannot simultaneously have low type I and type II error**.

.. rubric:: 2. Using the average run length (ARL)

The :index:`average run length` (ARL) is defined as the average number of sequential samples we expect before seeing an out-of-bounds, or out-of-control signal. This is given by the inverse of :math:`\alpha`, as ARL = :math:`\frac{1}{\alpha}`. Recall for the theoretical distribution we had :math:`\alpha = 0.0027`, so the ARL = 370. Thus we expect a run of 370 samples before we get an out-of-control signal.

Extensions to the basic Shewhart chart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*	The :index:`Western Electric rules`: we saw above how sluggish the Shewhart chart is in detecting a small shift in the process mean, from :math:`\mu` to :math:`\mu + \Delta\sigma`. The **Western Electric rules** are an attempt to more rapidly detect a process shift, by raising an alarm when these *improbable* events occur:

	#. 2 out of 3 points lie beyond :math:`2\sigma` on the same side of the centre line
	#. 4 out of 5 points lie beyond :math:`1\sigma` on the same side of the centre line
	#. 8 successive points lie on the same side of the center line
	
	However, an alternative chart, the CUSUM chart is more effective at detecting a shift in the mean. Notice also that the theoretical ARL, :math:`1/\alpha`, is reduced by using these rules in addition to the LCL and UCL bounds.

*	**Adding robustness**: the phase I derivation of a monitoring chart is iterative. If you find a point that violates the LCL and UCL limits, then the approach is to remove that point, and recompute the LCL and UCL values. That is because the LCL and UCL limits would have been biased up or down by these unusual points :math:`\overline{x}_k` points.

	This iterative approach can be tiresome with data that has spikes, missing values, outliers, and other problems typical of data pulled from a process database (:index:`historian <single: data historian>`. Robust monitoring charts are procedures to calculate the limits so the LCL and UCL are resistant to the effect of outliers. For example, a robust procedure might use the medians and MAD instead of the mean and standard deviation. An examination of various robust procedures, especially that of the interquartile range, is given in the paper by D. M. Rocke, `Robust Control Charts <http://dx.doi.org/10.2307/1268815>`_, *Technometrics*, **31** (2), p 173 - 184, 1989.

	*Note*: do not use robust methods to calculate the values plotted on the charts during phase 2, only use robust methods to calculate the chart limits in phase 1!
	
*	**Warning limits**: it is common to see warning limits on a monitoring chart at :math:`\pm 2 \sigma`, while the :math:`\pm 3\sigma` limits are called the action limits. Real-time computer systems usually use a colour scheme to distinguish between the warning state and the action state. For example, the chart background changes from green, to orange to red as the deviations from target become more severe.

.. _monitoring_adjust_limits:

*	**Adjusting the limits**: The :math:`\pm 3\sigma` limits are not set in stone. Depending on the degree to which the source data obey the assumptions, and the frequency with which spikes and outliers contaminate your data, you may need to adjust your limits, usually wider, to avoid frequent false alarms. Nothing makes a monitoring chart more useless to operators than frequent false alarms ("`crying wolf <http://en.wikipedia.org/wiki/The_Boy_Who_Cried_Wolf>`_"). However, :ref:`recall that there is no free lunch <monitoring_judging_performance>`: you cannot simultaneously have low type I and type II error.

*	**Changing the subgroup size**: It is perhaps a counterintuitive result that increasing the subgroup size, :math:`n`, leads to a more sensitive detection system for shifts in the mean, because the control limits are pulled in tighter. However, the larger :math:`n` also means that it will take longer to see the detection signal as the subgroup mean is averaged over more raw data points. So there is a trade-off between subgroup size and the run length (time to detection of a signal).

.. _monitoring_mistakes_to_avoid:

Mistakes to avoid
~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: check if the assumption of independence within each subgroup is required

#.	Imagine you are monitoring an aspect of the final product's quality, e.g. viscosity, and you have a product specification that requires that viscosity to be within, say 40 to 60 cP. It is a mistake to place those **specification limits** on the monitoring chart. It is also a mistake to use the required specification limits instead of the LCL and UCL. The monitoring chart is to detect abnormal variation in the process, not to inspect for quality specifications. You can certainly have another chart for that, but the process monitoring chart's limits are intended to monitor process stability, and these Shewhart stability limits are calculated differently.

#.	Shewhart chart limits were calculated with the assumption of **independent subgroups** (e.g. subgroup :math:`i` has no effect on subgroup :math:`i+1`). For a process with mild autocorrelation, the act of creating subgroups, with :math:`n` samples in each group, removes most, if not all, of the relationship between subgroups. However processes with heavy autocorrelation (slow moving processes sampled at a high rate, for example), will have LCL and UCL calculated from equation :eq:`shewhart-limits` that will raise false alarms too frequently. In these cases you can widen the limits, or remove the autocorrelation from the signal. More on this in the later section on :ref:`exponentially weighted moving average (EWMA) charts <monitoring_EWMA>`.

#.	Using Shewhart charts on two or more **highly correlated quality variables**, usually on your final product measurement, can increase your type II (consumer's risk) dramatically. We will come back to this very important topic in the section on :ref:`latent variable models <SECTION_latent_variable_modelling>`.

.. _monitoring_CUSUM_charts:

CUSUM charts
==============

We :ref:`showed earlier <monitoring_sluggish_shewhart_chart>` that the Shewhart chart is not too sensitive to detecting shifts in the mean. Depending on the subgroup size, :math:`n`, we showed that it can take several consecutive samples before a warning or action limit is triggered. The cumulative sum chart, or :index:`CUSUM chart <pair: CUSUM; process monitoring>`, allows more rapid detection of these shifts away from a target value, :math:`T`.

.. math::
	:label: CUSUM-derivation
	
	S_0 &= (x_0 - T) \\
	S_1 &= (x_0 - T) + (x_1 - T) = S_0 + (x_1 - T) \\
	S_2 &= (x_0 - T) + (x_1 - T) + (x_2 - T) = S_1 + (x_2 - T) \\
	\\
	\text{In general}\qquad S_t &= S_{t-1} + (x_t - T) 

.. TODO: should add Shewhart chart to this to prove its sluggishness

.. figure:: ../figures/monitoring/explain-CUSUM.png
	:alt:	../figures/monitoring/explain-CUSUM.R
	:width: 750px
	:align: center
	
Values of :math:`S_t` for an in-control process should really just be random errors, with mean of zero. The long-term sum of :math:`S_t` is also zero, as the positive and negative errors keep cancelling out.

So imagine a CUSUM chart where at some time point the process mean shifts up by :math:`\Delta` units, causing future values of :math:`x_t` to be :math:`x_t + \Delta` instead. Now the summation in the last equation of :eq:`CUSUM-derivation` has an extra :math:`\Delta` term added at each step to :math:`S_t`. Every point will build up an accumulation of :math:`\Delta`, which shows up as a positive or negative slope in the CUSUM chart. 

The CUSUM chart is extremely sensitive to small changes. The example chart is shown here for a process where the mean is :math:`\mu=20`, and :math:`\sigma=3`. A small shift of :math:`0.4 \times 3 = 1.2` units (i.e from 20 to 21.2) occurs at :math:`t=150`. This shift is almost imperceptible in the raw data (see the 3rd row in the figure). However, the CUSUM chart rapidly picks up the shift by showing a consistent rising slope.

This figure also shows how the CUSUM chart is used with the 2 masks. Notice that there are no lower and upper bounds for :math:`S_t`. A process that is on target will show a "wondering" value of S, moving up and down. In fact, as the second row shows, a surprising amount of movement up and down occurs even when the process is in control.

What is of interest however is a persistent change in slope in the CUSUM chart. The angle of the superimposed V-mask is the control limit: the narrower the mouth of the mask, the more sensitive the CUSUM chart is to deviations from the target. Both the type I and II error are set by the angle of the V and the leading distance (the distance from the short vertical line to the apex of the V).

The process is considered in control as long as all points are within the arms of the V shape.  The mask in the second row of the plot shows "in control" behaviour, while the mask in the fourth row detects the process mean has shifted, and an alarm should be raised.

Once the process has been investigated the CUSUM value, :math:`S_t` is often reset to zero; though other resetting strategies exist. A tabular version of the CUSUM chart also exists which tends to be the version used in software systems.

The purpose of this section is not to provide formulas for the V-mask or tabular CUSUM charts, only to explain the CUSUM concept to put the next section in perspective.

.. _monitoring_EWMA:

EWMA charts
==============

.. index::
	see: exponentially weighted moving average; EWMA
	pair: EWMA; process monitoring

The two previous charts highlight 2 extremes of monitoring charts. On the one hand, a Shewhart chart assumes each subgroup sample is independent (unrelated) to the next - implying there is no "memory" in the chart. On the other hand, a CUSUM chart has an infinite memory, all the way back to the time the chart was started at :math:`t=0` (see equation :eq:`CUSUM-derivation`).

As an introduction to the exponentially weighted moving average (EWMA) chart, consider first the simple :index:`moving average` (MA) chart. This chart is used just like a Shewhart chart, except the samples that make up each subgroup are calculated using a moving window of width :math:`n`. The case of :math:`n=5` is shown below.

.. image:: ../figures/monitoring/explain-moving-average-data-source.png
	:width: 750px
	:align: center
	:scale: 70

The MA chart plots values of :math:`\overline{x}_t`, calculated from groups of size :math:`n`, using equal weight for each of the :math:`n` most recent raw data.

.. math::	
	
	\overline{x}_t = \frac{1}{n}x_{t-1} + \frac{1}{n}x_{t-2} + \ldots + \frac{1}{n}x_{t-n}

The EWMA chart is similar to the MA chart, but uses different weights; heavier weights for more recent observations, tailing off exponentially to very small weights further back in history. Let's take a look at a derivation. 

.. todo: Show a Shewhart chart in the second row; use lambda = 0.5 and 0.15 only, then a CUSUM at the bottom

.. figure:: ../figures/monitoring/explain-EWMA.png
	:width: 750px
	:align: center
	:scale: 95

Define the process target as :math:`T`.

.. math:: 
	:label: ewma-derivation-1
	
		\begin{array}{lcrcl}
			\text{Let}  \qquad\qquad && x_t           &=& \text{new data measurement}\\
			\text{let}  \qquad\qquad && e_t           &=& x_t - \hat{x}_t \\
			\text{where}			 && \hat{x}_t     &=& \hat{x}_{t-1} + \lambda e_{t-1}	\qquad\qquad	 \\
			\text{shifting one step:}&& \hat{x}_{t+1} &=& \hat{x}_{t}   + \lambda e_{t}    \\
		\end{array}

The reason for the :math:`\wedge` above the :math:`x_t`, as in :math:`\hat{x}_t`, is that :math:`\hat{x}_t` is a prediction of the measured :math:`x_t` value. 
		
To start the EWMA sequence we define the value for :math:`\hat{x}_0 = T`, and :math:`e_0 = 0`, so that :math:`\hat{x}_1 = T`. An alternative way of writing the above equation is:

.. math:: 
	:label: ewma-derivation-2
	
		\begin{array}{lcrclcl}
			x_t = \text{new data}\qquad		&& \hat{x}_{t+1} &=& \hat{x}_{t}   + \lambda e_{t}\qquad\qquad	& \text{where~} e_t = x_t - \hat{x}_t \\
			\text{Substituting in the error}&& \hat{x}_{t+1} &=& \hat{x}_{t}   + \lambda \left(x_t - \hat{x}_t\right)     \\
											&& \hat{x}_{t+1} &=& \left(1-\lambda \right)\hat{x}_{t}   + \lambda x_t  \\
		\end{array}

That last line shows the one-step-ahead prediction for :math:`x` at time :math:`t+1` is a weighted sum of two components: the predicted value, :math:`\hat{x}_t`, and the measured value, :math:`x_t`, weighted to add up to 1. The plot below shows visually what happens as the weight of :math:`\lambda` is changed. In this example a shift of :math:`\Delta = 1\sigma = 3` units occurs at :math:`t=150`. Prior to that the process mean is :math:`\mu=20` and the raw data has :math:`\sigma = 3`. The EWMA plots show the one-step-ahead prediction value from equation :eq:`ewma-derivation-2`, :math:`\hat{x}_{t+1}` = EWMA value plotted at time :math:`t`.

As :math:`\lambda` gets smaller, the chart is smoother, because as equation :eq:`ewma-derivation-2` shows, less of the current data, :math:`x_t`, is used, and more historical data, :math:`\hat{x}_{t}`, is used. The "memory" of the EWMA statistic is increased. To see why :math:`\hat{x}_{t}` represents historical data, you can recursively substitute and show that:

.. math::
	
	\hat{x}_{t+1} &= \sum_{i=0}^{i=t}{w_i x_i} = w_0x_0 + w_1x_1 + w_2x_2 + \ldots \\
	\text{where the weights are:} \qquad w_i &= \lambda (1-\lambda)^{t-i}

which shows that the one-step-ahead prediction is a just a weighted sum of the raw measurements, with weights declining in time. In the next figure, we show a comparison of the weights used in 4 different monitoring charts studied so far.

From the above discussion and the weights shown for the 4 different charts, it should be clear now how an EWMA chart is a tradeoff between a  Shewhart chart and a CUSUM chart. As :math:`\lambda \rightarrow 1`, the EWMA chart behaves more as a Shewhart chart, giving only weight to the most recent observation. While as :math:`\lambda \rightarrow 0` the EWMA chart starts to have an infinite memory (like a CUSUM chart).

.. image:: ../figures/monitoring/explain-weights-for-process-monitoring.png
	:alt: ../figures/monitoring/explain-weights-for-process-monitoring.R
	:width: 750px
	:align: center
	:scale: 65
	
The upper and lower control limits for the EWMA plot are plotted in the same way as the Shewhart limits, but calculated differently:

.. math::
	:label: ewma-limits
	
	\begin{array}{rcccl} 
		 \text{LCL} = \overline{\overline{x}} - 3 \cdot \sigma_{\text{Shewhart}}\sqrt{\frac{\displaystyle \lambda}{\displaystyle 2-\lambda}} &&  &&  \text{UCL} = \overline{\overline{x}} + 3 \cdot \sigma_{\text{Shewhart}} \sqrt{\frac{\displaystyle \lambda}{\displaystyle 2-\lambda}}
	\end{array} 

where :math:`\sigma_{\text{Shewhart}}` represents the standard deviation as calculated for the Shewhart chart. Actually one interesting implementation is to show both the Shewhart and EWMA plot on the same chart, with both sets of limits. The EWMA value plotted is actually the one-step ahead prediction of the next :math:`x`-value, which can be informative for slow-moving processes.

The R code here shows one way of calculating the EWMA values for a vector of data. Once you have pasted this function into R, use it as ``ewma(x, lambda=..., target=...)``.

.. code-block:: s

	ewma <- function(x, lambda, target=x[1]){
	    N <- length(x)
	    y <- numeric(N)
	    y[1] = target
	    for (k in 2:N){
	        error = x[k-1] - y[k-1]
	        y[k] = y[k-1] + lambda*error
	    }
	return(y)
	}


.. EWMA can detect both changes in level and changes in variance
.. Todo After introducing concept, show why Shewhart fails with heavy autocorr. Have to increase Shewhart N, or widen the limits.


Other charts
=============

You may encounter other charts in practice:

	*	The *S chart* is for monitoring the subgroup's standard deviation. Take the group of :math:`n` samples and show their standard deviation on a Shewhart-type chart. The limits for the chart are calculated using similar correction factors as were used in the derivation for the :math:`\overline{x}` Shewhart chart. This chart has a LCL :math:`\geq 0`.
	
	*	The *R chart* was a precursor for the *S chart*, where the *R* stands for range, the subgroup's maximum minus minimum. It was used when charting was done manually, as standard deviations were tedious to calculate by hand.
	
	*	The *np chart* and *p chart* are used when monitoring the proportion of defective items using a pass/fail criterion. In the former case the sample size taken is constant, while in the latter the proportion of defective items is monitored. These charts are derived using the binomial distribution.

	*	The *exponentially weight moving variance* (EWMV) chart is an excellent chart for monitoring for an increase in product variability. Like the :math:`\lambda` from an EWMA chart, the EWMV also has a sliding parameter that can balance current information and historical information to trade-off sensitivity. More information is available in the paper by J.F. MacGregor, and T.J. Harris, "The Exponentially Weighted Moving Variance", *Journal of Quality Technology*, **25**, p 106-118, 1993.


Process capability
===================

.. index::
	pair: process capability; process monitoring
	single: capability of a process
	
.. Note:: This section is not about a particular monitoring chart, but is relevant to the topic of process monitoring.

Centered processes
~~~~~~~~~~~~~~~~~~~~

.. index:: Cp

Purchasers of your product may request a :index:`process capability ratio` (PCR) for each of the quality attributes of your product. For example, your plastic product is characterized by its Mooney viscosity and melting point. A PCR value can be calculated for either property, using the definition below:

.. math::
	:label: process-capability-ratio-centered
	
	\text{PCR} = \frac{\text{Upper specification limit} - \text{Lower specification limit}}{6\sigma} = \frac{\text{USL} - \text{LSL}}{6\sigma}
	
Since the population standard deviation, :math:`\sigma`, is not known, an estimate of it is used. Note that the :index:`lower specification limit` (LSL) and :index:`upper specification limit` (USL) are **not the same** as the lower control limit (LCL) and upper control limit (UCL) as were calculated for the Shewhart chart. The LSL and USL are the tolerance limits required by your customers, or set from your internal specifications. 

Interpretation of the PCR:
	
	* assumes the property of interest follows a normal distribution
	* assumes the process is centered (i.e. your long term mean is halfway between the upper and lower specification limits)
	* assumes the PCR value was calculated when the process was stable

The PCR is often called the :index:`process width`. Let's see why by taking a look at a process with PCR=0.5 and then PCR=2.0. In the first case :math:`\text{USL} - \text{LSL} = 3\sigma`. Since the interpretation of PCR assumes a :index:`centered process`, we can draw a diagram as shown below:

.. image:: ../figures/monitoring/explain-PCR-half.png
	:width: 750px
	:align: center
	:scale: 80

The diagram is from a process with mean of 80 and where LSL=65 and USL=95. These specification are fixed, set by our production guidelines. If the process variation is :math:`\sigma = 10`, then this implies that PCR=0.5. Assuming further that the our production is centered at the mean of 80, we can calculate how much defective product is produced in the shaded region of the plot. Assuming a normal distribution:

	-	:math:`z` for LSL = :math:`(65 - 80)/10 = -1.5`

	-	:math:`z` for USL = :math:`(95 - 80)/10 = 1.5`

	-	Shaded area probability = ``pnorm(-1.5) + (1-pnorm(1.5))`` = 13.4% of production is out of the specification limits.

Contrast this to the case where PCR = 2.0 for the same system. To achieve that level of process capability, using the *same upper and lower specifications* we have to  reduce the standard deviation by a factor of 4, down to :math:`\sigma = 2.5`.  The figure below illustrates that almost no off-specification product is produced for a centered process at PCR = 2.0. There is a width of :math:`12 \sigma` units from the LSL to the USL, giving the process location (mean) ample room to drift left or right without creating additional off-specification product. 

.. image:: ../figures/monitoring/explain-PCR-two.png
	:width: 750px
	:align: center
	:scale: 80

.. Note:: You will probably come across the terminology C\ :sub:`p`, especially when dealing with 6 sigma programs. This is the same as PCR for a centered process.

Uncentered processes
~~~~~~~~~~~~~~~~~~~~

.. index::
	single: uncentered process capability; process monitoring
	single: capability of a process
	single: Cpk

Processes are not very often centered between their upper and lower specification limits. So a measure of process capability for an uncentered processes is defined:

.. math::
	:label: process-capability-ratio-uncentered

		\text{PCR}_\text{k} = \text{C}_\text{pk} = \min \left( \frac{\text{Upper specification limit} - \overline{\overline{x}}}{3\sigma};  \frac{\overline{\overline{x}} - \text{Lower specification limit}}{3\sigma} \right)
		
The |xdb| term would be the process target from a Shewhart chart, or simply the actual average operating point. Notice that |Cpk| is a one-sided ratio, only the side closest to the specification is reported. So even an excellent process with C\ :sub:`p` = 2.0 that is running off-center will have a lower |Cpk|.

It is the |Cpk| value that is requested by your customer. Values of 1.3 are usually a minimum requirement, while 1.67 and higher are requested for health and safety-critical applications. A value of |Cpk| :math:`\geq 2.0` is termed a six-sigma process, because the distance from the current operating point, |xdb|, to the closest specification is at least :math:`6\sigma` units.

You can calculate that a shift of :math:`1.5\sigma` from process center will introduce only 3.4 defects per million. This shift would reduce your |Cpk| from 2.0 to 1.5.

.. Note:: It must be emphasized that |Cpk| and C\ :sub:`p` numbers are only useful for a process which is stable. Furthermore the assumption of normally distributed samples is also required to interpret the |Cpk| value.

Industrial practice
===================

.. index::
	pair: industrial practice; process monitoring

This preceding section of the book is only intended to give an overview of the concepts of process monitoring. As you move into an industrial environment you will find there are many such systems already in place. Higher levels of management track statistics from a different point of view, often summarizing data from an entire plant, geographic region, or country. The techniques learned in this book, while focusing mainly on unit operations, are equally applicable though to data from a plant, region, or country.

You may come across systems called dashboards, which are often part of :index:`enterprise resource planning` (ERP) systems. These dashboards are supposed to monitor the pulse of a company and are tracked like any other monitoring chart discussed above. Another area is called :index:`business intelligence` (BI) systems. These typically track sales and other financial information. 

Yet another acronym is the :index:`KPI <see: KPI; key performance indicator>`, :index:`key performance indicator`, which is a summary variable, such as profit per hour, or energy cost per unit of production. These are often monitored and acted on by site managers on a daily or weekly basis. Sites in a global company with the lowest KPIs receive the greatest scrutiny.

But at the unit operation and plant level, you will likely find the hardest part of getting a monitoring chart implemented is the part where you need access to the data. Getting data out of most database systems is not easy, though it has improved quite a bit in the last few years.

It is critical that your monitoring chart display the quantity as close to real-time as possible. It is almost as if the monetary value of the information in a monitoring chart decays exponentially from the time an event occurs. It is hard to diagnose and correct a problem detected yesterday, and harder still if the problem occurred last week or month.

You will also realize that good operator training to interpret and act on the monitoring chart is time-consuming; operators are often cycled between different units or plants, so frequent re-training is required. Concepts from the :ref:`data visualization <SECTION-data-visualization>` section are helpful to minimize training effort - make sure the online plots contain the right level of information, without clutter, so they can be acted on accurately.

Another side effect of large quantities of data are that you will have to work with IT groups to manipulate large chunks of data on dedicated networks, separate from the rest of the plant. The last thing you want to be responsible for is clogging the company network with your traffic. Most industries now have a "production" network running in parallel to the "corporate" network. The production network carries real-time data, images from cameras and so forth, while the company network carries office email and web traffic.

Approach to implement a monitoring chart in an industrial setting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is some general guidance; feel free to adjust the steps as required for your unique situation.

	#.	Identify the variable(s) to monitor. Make sure each variables show different, uncorrelated phenomena to avoid redundancy. If unsure which variables to select, use a :ref:`multivariate monitoring system <LVM_monitoring>`.
	
	#.	Retrieve historical data from your computer systems, or lab data, or paper records.
	
	#.	Import the data and just plot it. Do you see any time trends, outliers, spikes, missing data gaps? Investigate these (to learn more about your process), but then remove them to create the phase 1 data set.
	
	#.	Locate any regions of data which are from generally stable operation. Remove spikes and outliers that will bias your control limits calculations. In other words, find regions of common-cause operation.
	
	#.	Split your phase 1 data into say a 60% and 40% split. Set aside 40% of the cleaned portion to use as phase 1 testing data later on. Keep the data from outliers, spikes and unstable process operation aside as another testing data set (to ensure that these problems are actually detectable).
	
	#.	Using the cleaned 60% portion, estimate limits that you would expect to contain this stable region of operation just by looking at the plots.
	
	#.	On the 60% portion, calculate preliminary control limits (UCL, LCL), using the formulas shown in this section. They should agree with limits in the previous step.
	
	#.	How does your chart work? Test your chart on the 40% cleaned portion. These testing data should not raise many alarms. Any alarms raised will be type I errors, so you can quantify your type I error rate from the fraction of false alarms raised.
	
	#.	Test your chart on the unusual data you found earlier. You can quantify the type II error by counting the fraction of this bad data that went undetected by your chart. 
	
	#.	 Adjust the limits and monitoring chart parameters (e.g. :math:`\lambda`) if necessary, to achieve the required type I and type II balance that is acceptable to your operation staff.  You may even have to resort to using a different chart, or monitoring based on a different variable.
	
	#.	Test the chart on your desktop computer for a couple of days. When you detect an unusual event, go and check with the process operators and verify the event. Would they have reacted to it, had they known about it?  Or, would this have been a false alarm?  You may need to refine your limits, or the value you are plotting again.
	
	#.	Remember that this form of charting is not an expert system - it will not diagnose problems: you have to use your engineering knowledge by looking at patterns in the chart, and use knowledge of other process events.
	
	#.	Demonstrate the system to your colleagues and manager. But show them economic estimates of the value of early detection. They are usually not interested in the plots alone, so convert the statistics into monetary values. For example, dollars saved if we had detected that problem in real-time, rather than waiting till later.
	
	#.	Installation and operator training will take time. This assumes that you have real-time data acquisition systems and real-time processing systems in place - most companies do. You will have to work with your company's IT staff to get this implemented.
	
	#.	Listen to your operators for what they want to see. Use principles of :ref:`good data visualization <SECTION-data-visualization>` to reduce unnecessary information. Make your plots interactive - if you click on an unusual point it should "drill-down" and give you more details and historical context.
	
	#.	Future monitoring charts are easier to get going, once the first system is in place.

.. Workflow for what happens with a new observation, once you have the monitoring settings
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	Once you have the monitoring settings for your variable (i.e the control limits, the target point), you are now in a 

	These steps are generally followed in sequence 
	 - check for gross error (HI/LOW limits)
	 - calculate the number to plot (what happens with missing data)
	 - plot the new observation in relation to prior operating data
	 - diagnose if outside limits

Industrial case study
==========================

ArcelorMittal (Dofasco)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ArcelorMittal's steel mill in Hamilton, Ontario, (formerly called Dofasco) has used multivariate process monitoring tools in many areas of their plant for decades now. One of their most successful applications is that applied to their casting operation. In this section we only focus on the application; the sort of multivariate calculations used by this system are discussed :ref:`later on <SECTION_latent_variable_modelling>`.

The computer screenshot shows the monitoring system, called Caster SOS (Stable Operation Supervisor), which is followed by the operators. There are several charts on the screen: two charts, called "Stability Index 1" and "Stability Index 2", are one-sided monitoring charts. Notice the warning limits and the action limits. In the middle is a two-sided chart. A wealth of information is presented on the screen - their design was heavily influenced and iterated on several times, working with the *operators*. The screen shot is used with permission of Dr. John MacGregor. 

.. image:: ../figures/examples/Dofasco/Dofasco-monitoring-chart.png
	:width: 750px
	:align: center
	:scale: 100
	
The economics of monitoring charts cannot be overstated. The ArcelorMittal example above was introduced around 1997. The calculations required by this system are complex - however the computer systems performs them in near real-time, allowing the operators to take corrective action within a few seconds. The data show a significant reduction in breakouts since 1997 (*used with permission of Dr. John MacGregor*). The economic savings and increased productivity is in the millions of dollars per year, as each breakout costs around $200,000 to $500,000 due to process shutdowns and/or equipment damage.

.. image:: ../figures/examples/Dofasco/breakouts-dofasco-economics.png
	:width: 750px
	:align: center
	:scale: 80

.. FUTURE: Agnico-Eagle monitoring 
.. FUTURE: show how a scatter plot can be used
.. FUTURE: show how a spectral plot can be used (or a distribution, e.g. size distribution)

.. Software for monitoring charts

	* Quality control charts in R: http://cran.r-project.org/web/packages/qcc/

Summary
==========

Montgomery and Runger list 5 reasons why monitoring charts are widely used. After this section of the book you should understand the following about the charts and process monitoring:

	#.	These tools are proven to improve productivity (i.e. to reduce scrap and rework, as described above), and to increase process throughput.
	#.	They detect defective production, consistent with the concept of "doing it right the first time", a mantra that you will increasingly hear in the manufacturing workplace.
	#.	A monitoring chart with good limits will prevent over-control of the process. Operators are trained not to make process adjustments unless there is a clear warning or alarm from the chart.
	#.	The patterns generated by the plots often help determine what went wrong, providing some diagnostic value to the operators. We will see a more formal tool for process diagnosis though in the :ref:`latent variable section <SECTION_latent_variable_modelling>`.
	#.	Monitoring charts are required to judge if a process is stable over time. A stable process allows us to calculate our process capability, which is an important metric for your customers.

