.. _univariate_paired_tests:

Paired tests
============

.. index::
	single: two treatments

.. youtube:: https://www.youtube.com/watch?v=OI1RD6gPALw&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=17

A :index:`paired test` compares two treatments, A and B, that are both applied to the same object or
batch of materials, so that every result under A has a partner result under B. You might see the
nomenclature of "two treatments" being used in the literature. For example:

	-	A drug trial could be run in two parts: each person randomly receives a placebo or the drug, then 3 weeks later they receive the opposite, for another 3 weeks. Tests are run at 3 weeks and 6 weeks and the difference in the test result is recorded.

	-	We are testing two different additives, A and B, where the additive is applied to a base mixture of raw materials. Several raw material lots are received from various suppliers, supposedly uniform. Split each lot into 2 parts, and run additive A and B on each half. Measure the outcome variable, e.g. conversion, viscosity, or whatever the case might be, and record the difference.

	-	We are testing a new coating to repel moisture. The coating is applied to randomly selected sheets in a pattern [A|B] or [B|A] (the pattern choice is made randomly). We measure the repellent property value and record the difference.

	-	A new polymer for surgical gloves is tested against the current polymer. Each physician wears
		one glove of each polymer, the two gloves look identical, and the hand that gets the new
		polymer is chosen at random, so that hand dominance is not mistaken for a polymer effect. A
		property of each glove, such as its tensile strength after the operation, is measured and the
		difference recorded. A physician's preference for one glove is a single yes/no answer, not
		two values to subtract, and is not analysed with a paired test.

In each case we have a table of :math:`n` samples recording the **difference values**. The question now is whether the difference is significant, or is it essentially zero?

How the data were collected decides which test applies. When every result under A has a partner
under B from the same object, the two groups are not independent, so the assumption behind the
:ref:`unpaired test of differences <univariate-group-to-group-differences-no-reference-set>` does
not hold, and the paired test is used. When A and B are applied to separate objects there is
nothing to pair, and the unpaired test is used.

The advantage of the paired test is that anything that shifts both results in a pair by the same
amount cancels when we subtract them, even when that shift differs from one pair to the next. Say
for example the drug trial measures blood pressure: each person's usual blood pressure, and the
bias (a :index:`systematic error`) of the device used on that person, are in both readings and
cancel in the difference. In the example of the raw materials and additives, the lot-to-lot
variation in the raw materials, and its (unintended) effect on the outcome variable, cancels in
the same way. An unpaired test leaves this object-to-object variation in the pooled variance,
where it widens the confidence interval.

The disadvantage of the paired test is that we lose degrees of freedom. Let's see how:

	#.	Calculate the :math:`n` differences: :math:`w_1 = x_{B,1} - x_{A,1}; w_2 = x_{B,2} - x_{A,2}, \ldots` to create the sample of values :math:`\mathbf{w} = [w_1, w_2, \ldots, w_n]`

	#.	Assume these values, :math:`w_i`, are independent, because they are taken on independent objects (people, base packages, sheets of paper, *etc*)

	#.	Calculate the mean, :math:`\overline{w}` and the standard deviation, :math:`s_w`, of these :math:`n` difference values.

	#.	What do we need to assume about the population from which :math:`w` comes? By the central
		limit theorem, :math:`\overline{w}` is approximately normally distributed as
		:math:`\overline{w} \sim \mathcal{N}\left(\mu_w, \sigma_w^2/n \right)`, where
		:math:`\mu_w = \mu_{B-A} = \mu_B - \mu_A`, and the approximation improves as :math:`n` grows.
		The :math:`t`-distribution used in step 6 further assumes that the :math:`w` values come from
		a normal distribution, which a :ref:`q-q plot <univariate_check_for_normality_qqplot>` of the
		:math:`n` differences can check. The raw values, :math:`x_A` and :math:`x_B`, need not be
		normally distributed.

	#.	Now calculate the :math:`z`-value, but use the sample standard deviation, instead of the population standard deviation.

		.. math::
			z = \frac{\overline{w} - \mu_w}{s_w / \sqrt{n}}

	#.	Because we have used the sample standard deviation, :math:`s_w`, we have to use to the :math:`t`-distribution with :math:`n-1` degrees of freedom, to calculate the critical values.

	#.	We can calculate a confidence interval, below, and if this interval includes zero, then the
		difference between treatments A and B is not statistically significant at that level of
		confidence.

		.. math::
			\overline{w} - c_t \frac{s_w}{\sqrt{n}} < \mu_w < \overline{w} + c_t \frac{s_w}{\sqrt{n}}

		The value of :math:`c_t` is taken from the :math:`t`-distribution with :math:`n-1` degrees of freedom at the level of confidence required: use the ``qt(...)`` function in R to obtain the values of :math:`c_t`.

The :index:`loss of degrees of freedom <single: degrees of freedom; loss of>` is the cost of
pairing. The same :math:`2n` measurements, made instead on :math:`2n` separate objects (two
independent groups of :math:`n_A = n_B = n`) and analysed with the
:ref:`pooled variance <univariate_eqn_pooled_variance>`, give :math:`n_A + n_B - 2 = 2n - 2`
degrees of freedom, against :math:`n-1` for the :math:`n` pairs. The fewer degrees of freedom give
a larger :math:`c_t`, which widens the paired interval. Against that, :math:`s_w` excludes the
object-to-object variation that cancels within each pair, whereas the pooled variance includes it.

Pairing therefore gives the narrower interval when the variation from one object to the next
(people, lots, sheets) is large compared with the random variation within an object, which shows
up as a strong positive correlation between the A and B results across the pairs. When the objects
are alike, pairing removes little variation, and the larger :math:`c_t` makes the paired interval
slightly wider than the unpaired one.

.. This example illustrates:
.. todo:: example showing loss of DOF (boys shoes example in BHH2). particularly, show the plots (p98 on BHH2- edition 1)
