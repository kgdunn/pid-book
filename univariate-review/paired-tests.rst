.. _univariate_paired_tests:

Paired tests
============

.. Verify this section against other notes.

.. index::
	single: two treatments
	
.. youtube:: https://www.youtube.com/watch?v=OI1RD6gPALw&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=16

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

The :index:`loss of degrees of freedom <single: degrees of freedom; loss of>` can be seen when we use exactly the same data and treat the problem as one where we have :math:`n_A` and :math:`n_B` samples in groups A and B and want to test for a difference between :math:`\mu_A` and :math:`\mu_B`. You are encouraged to try this out. There are more degrees of freedom, :math:`n_A + n_B - 2` in fact when we use the :math:`t`-distribution with the :ref:`pooled variance shown here <univariate_eqn_pooled_variance>`. Compare this to the case just described above where there are only :math:`n` degrees of freedom.
	
.. This example illustrates:
.. todo:: example showing loss of DOF (boys shoes example in BHH2). particularly, show the plots (p98 on BHH2- edition 1)


