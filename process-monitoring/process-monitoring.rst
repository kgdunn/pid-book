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

.. youtube:: https://www.youtube.com/watch?v=o97imeRitMI&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=59

The material in this section is used whenever you need to rapidly detect problems. It has tangible application in many areas - in fact, you have likely encountered these monitoring charts in areas such as a hospital (monitoring a patient's heart beat), stock market charts (for intraday trading), or in a processing/manufacturing facility (control room computer screens).

	-	*Co-worker*: We need a system to ensure an important dimension on our product is stable and consistent over the entire shift.
	-	*Yourself*: We know that as the position of a manufacturing robot moves out of alignment that our product starts becoming inconsistent; more variable. How can we quickly detect this slow drift?
	-	*Manager*: the hourly average profit, and process throughput is important to the head-office; can we create a system for them to track that?
	-	*Potential customer*: what is your process capability - we are looking for a new supplier that can provide a low-variability raw material for us with |Cpk| of at least 1.6, preferably higher.
	
**Note**: process monitoring is mostly *reactive* and not *proactive*. So it is suited to *incremental* process improvement, which is typical of most improvements.

What we will cover
~~~~~~~~~~~~~~~~~~~~

We will consider 3 main charts after introducing some basic concepts: Shewhart charts, CUSUM charts and EWMA (exponentially weighted moving average) charts. The EWMA chart has an adjustable parameter that captures the behaviour of a Shewhart chart at one extreme and a CUSUM chart at the other extreme.

Concepts
~~~~~~~~~~~~~~~

Concepts and acronyms that you must be familiar with by the end of this section: 

	*	Shewhart chart, CUSUM chart and EWMA chart
	*	Phase 1 and phase 2 when building a monitoring system
	*	False alarms
	*	Type 1 and type 2 errors
	*	LCL and UCL
	*	Target
	*	C\ :sub:`p` and |Cpk|
	*	Outliers
	*	Real-time implementation of monitoring systems

.. OLD image: image: : ../figures/mindmaps/process-monitoring-concepts.png

References and readings
==============================

.. index::
	pair: references and readings; process monitoring

#.	**Recommended**: Box, Hunter and Hunter, *Statistics for Experimenters*, Chapter 14 (2nd edition)

#.	**Recommended**: Montgomery and Runger, *Applied Statistics and Probability for Engineers*.

#.	Hogg and Ledolter, *Engineering Statistics*.

#.	Hunter, J.S. "`The Exponentially Weighted Moving Average <https://asq.org/qic/display-item/index.pl?item=5536>`_", *Journal of Quality Technology*, **18** (4) p 203 - 210, 1986.

#.	Macgregor, J.F. "`Using On-Line Process Data to Improve Quality: Challenges for Statisticians <https://dx.doi.org/10.1111/j.1751-5823.1997.tb00311.x>`_", *International Statistical Review*, **65**, p 309-323, 1997.

.. 
	Box, The R. A. Fisher Memorial Lecture, 1988- Quality Improvement- An Expanding Domain for the Application of Scientific Method, Phil. Trans. R. Soc. Lond. A February 24, 1989 327:617-630, [https://dx.doi.org/10.1098/rsta.1989.0017 DOI]
	
.. (Not available): Box critique of Taguchi methods: https://dx.doi.org/10.1002/qre.4680040207
..	Bisgaard, S., "`The Quality Detective: A Case Study <https://dx.doi.org/10.1098/rsta.1989.0006>`_", Philosophical Transactions of the Royal Society-A, **327**, p 499-511, 1989.
.. UMetrics book: review chapter on (M)SPC
.. MacGregors 1997 paper on MSPC
.. * Controversy between monitoring charts and hypothesis tests, Woodall, Woodall, W. Controversies and Contradictions in Statistical Process Control, JQT, 32(4), 341-350, 2000 ([http://filebox.vt.edu/users/bwoodall/ Link])
.. EWMV paper by MacGregor?
.. Box, G.E.P., Comparisons, Absolute Values, and How I Got to Go to the Folies Bergeres, Quality Engineering, 14(1), p167-169, 2001.
.. p 669 of Devore: see also Technometrics, 1989, p173-184, by David M Rocke

