.. _univariate_bayesian_credible_intervals:

Bayesian estimates and credible intervals
==========================================

.. index::
	single: Bayes' rule
	single: prior
	single: likelihood
	single: posterior
	single: credible interval

In the section on :ref:`confidence intervals <univariate_confidence_intervals>` we calculated the
95% confidence interval :math:`[17.1; 22.9]` for the viscosity of a polymer cube, from nine
destructively tested samples. That interval is a statement about the procedure that produced it:
intervals constructed this way contain the population mean, :math:`\mu`, in 95% of cases.

Two further questions come up in practice. Can we make a probability statement about :math:`\mu`
itself, of the form "there is a 95% probability that the long-run viscosity lies between these two
numbers"? And our plant has usually made this product before: can the interval use that prior
knowledge, together with the nine new measurements?

The Bayesian tools in this section answer both questions. They work from the same data and the
same distributional assumptions as the earlier sections, and add one ingredient: a probability
distribution describing what was known before the data arrived. They are complementary tools that
reach the same end goal, an interval for :math:`\mu`, by a different route. We will see that when
little is known beforehand, the two routes give intervals with the same numbers.

.. _univariate_bayes_rule:

Updating a belief with data: Bayes' rule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start with a situation where everything can be counted. A filter in a batch plant becomes blocked
during 5% of batches. An automatic alarm is configured to detect this: it sounds during 90% of the
batches where the filter really is blocked, but it also sounds, falsely, during 10% of the batches
where the filter is fine. This morning the alarm sounds. What is the probability the filter
actually is blocked?

Count it out per 1000 batches. In 50 of them the filter is blocked, and the alarm catches 45 of
those (90%). Of the 950 batches with a clean filter, the alarm falsely sounds in 95 (10%). So the
alarm sounds in :math:`45 + 95 = 140` of every 1000 batches, and in 45 of those 140 the filter
really is blocked:

.. math::

	p(\text{blocked} \,|\, \text{alarm}) = \frac{45}{140} = 0.32

Three quantities appeared in that calculation, and each has a name:

	-	The 5% chance of a blocked filter, before hearing anything, is the **prior** probability:
		what was known beforehand.

	-	The alarm's behaviour under each state of the filter (sounding in 90% of blocked-filter
		batches and 10% of clean ones) is the **likelihood**: how probable the observed evidence is,
		for each possible state.

	-	The 32% is the **posterior** probability: the updated belief about the filter, after the
		evidence has been taken into account.

Written as a formula, the counting argument above is :index:`Bayes' rule <single: Bayes' rule>`:

.. math::

	p(\text{blocked} \,|\, \text{alarm}) =
	\frac{p(\text{alarm} \,|\, \text{blocked}) \,\times\, p(\text{blocked})}{p(\text{alarm})} =
	\frac{0.90 \times 0.05}{0.14} = 0.32

The denominator, :math:`p(\text{alarm}) = 0.90 \times 0.05 + 0.10 \times 0.95 = 0.14`, is the
total probability of hearing the alarm, from either cause. Note what the rule did: it reversed the
direction of the conditioning. The alarm's specification sheet gives probabilities of the alarm,
given the state of the filter; the operator wants the probability of the filter's state, given the
alarm. Bayes' rule converts the one into the other, using the prior.

From two outcomes to a continuous quantity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The filter had only two states: blocked or clean. A parameter such as the viscosity mean
:math:`\mu` can take any value on a continuous scale, so beliefs about it are described by a
probability density rather than by two probabilities. The recipe stays the same. A **prior
distribution**, :math:`p(\mu)`, says which values of :math:`\mu` were considered plausible before
the data; the likelihood, :math:`p(\text{data} \,|\, \mu)`, says how probable the observed data are
for each candidate value of :math:`\mu`; and their product, rescaled to have unit area, is the
**posterior distribution**:

.. math::

	p(\mu \,|\, \text{data}) \,\propto\, p(\text{data} \,|\, \mu) \times p(\mu)

The rescaling constant plays the same role as the 0.14 in the alarm example, so the proportional
sign, :math:`\propto`, is used and the constant is left out.

An interval containing the central 95% of the posterior's area is called a 95% **credible
interval**. Since the posterior is a probability distribution for :math:`\mu`, this interval
carries the direct interpretation: given the data and the prior, there is a 95% probability that
:math:`\mu` lies inside it. That is the form of statement asked about at the start of this
section. A confidence interval makes a different statement, about the long-run behaviour of the
procedure; both are interval summaries of what the data say about :math:`\mu`.

The viscosity example when the variance is known
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return to the polymer cube, with its nine viscosity values ``23, 19, 17, 18, 24, 26, 21, 14, 18``
and sample average :math:`\overline{x} = 20.0`. As in :ref:`Case A of the confidence-interval
section <univariate_eqn_CI-mean-variance-known-again>`, take the standard deviation as known:
:math:`\sigma = 3.5`.

To apply Bayes' rule we need a prior for :math:`\mu`. Begin with a prior so wide that it expresses
no preference among the plausible viscosity values: a normal distribution whose standard deviation
is made as large as we please. The likelihood of the nine observations, seen as a function of
:math:`\mu`, is a normal curve centred at :math:`\overline{x} = 20.0` with standard deviation
:math:`\sigma/\sqrt{n} = 3.5/3 = 1.17`. Multiplying that curve by an essentially constant prior
changes nothing, so the posterior is the likelihood itself:

.. math::

	\mu \,|\, \text{data} \,\sim\, \mathcal{N}\left(\overline{x}, \, \sigma^2/n\right) =
	\mathcal{N}\left(20.0, \, 1.17^2\right)

The central 95% of this posterior runs from :math:`20.0 - 1.96 \times 1.17` to
:math:`20.0 + 1.96 \times 1.17`, giving the credible interval :math:`[17.7; 22.3]`. These are the
same numbers as the known-variance confidence interval of :eq:`CI-mean-variance-known-again`. With
a prior this weak the data dominate completely, and the two routes arrive at the same interval;
what differs is the sentence each attaches to it.

.. code-block:: python

	import numpy as np
	from scipy import stats

	viscosity = np.array([23, 19, 17, 18, 24, 26, 21, 14, 18])
	n = len(viscosity)
	x_avg = viscosity.mean()
	sigma = 3.5  # taken as known, for now

	# Weak prior: the posterior is the likelihood, centred at the sample average
	post_sd = sigma / np.sqrt(n)
	lo, hi = stats.norm.ppf([0.025, 0.975], loc=x_avg, scale=post_sd)
	print(f"95% credible interval: [{lo:.1f}; {hi:.1f}]")  # [17.7; 22.3]

For a normal prior that is not necessarily wide, :math:`\mu \sim \mathcal{N}(m_0, s_0^2)`, the
multiplication can be carried out by hand, and the posterior turns out to be normal as well. The
result is neatest when written in terms of the *precision*, defined as one divided by the
variance, so that a high precision means a narrow distribution:

.. math::

	\frac{1}{s_{\text{post}}^2} = \frac{1}{s_0^2} + \frac{n}{\sigma^2}
	\qquad\text{and}\qquad
	m_{\text{post}} = \left(\frac{m_0}{s_0^2} + \frac{n \overline{x}}{\sigma^2}\right) s_{\text{post}}^2

In words: the precisions of the prior and of the data add, and the posterior mean is a weighted
average of the prior mean, :math:`m_0`, and the sample average, :math:`\overline{x}`, each weighted
by its precision. Letting :math:`s_0` grow without bound removes the prior's contribution and
recovers the weak-prior result above.

.. _univariate_bayes_informative_prior:

Adding plant knowledge: an informative prior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now suppose the long-run production records for cubes of this same polymer grade show the batch
viscosity mean has been close to 18, varying with a standard deviation of about 2 from campaign to
campaign. If we judge those records to apply to the current cube, they can be encoded as the prior
:math:`\mu \sim \mathcal{N}(18, 2^2)`; a prior that carries information is called an
**informative prior**.

The update equations give the posterior precision as
:math:`1/2^2 + 9/3.5^2 = 0.25 + 0.73 = 0.98`, so :math:`s_{\text{post}} = 1.01`, and the posterior
mean as :math:`m_{\text{post}} = (0.25 \times 18 + 0.73 \times 20)/0.98 = 19.49`. The 95% credible
interval is :math:`19.49 \pm 1.96 \times 1.01 = [17.5; 21.5]`, which is 3.95 units wide, against
4.57 units for the weak-prior interval :math:`[17.7; 22.3]`.

Two features of this answer are worth noting. The posterior mean, 19.49, lies between the prior
mean of 18 and the sample average of 20.0, and closer to the sample average, because the nine
measurements carry about three times the precision of the prior (0.73 against 0.25). And the
interval is narrower than the weak-prior interval, because the plant records contribute
information the nine measurements alone do not have.

.. code-block:: python

	import plotly.graph_objects as go
	from plotly.subplots import make_subplots

	def posterior_normal(m0, s0, x_avg, n, sigma):
	    """Posterior (mean, sd) of the mean, for a N(m0, s0**2) prior."""
	    precision = 1 / s0**2 + n / sigma**2
	    mean = (m0 / s0**2 + n * x_avg / sigma**2) / precision
	    return mean, 1 / np.sqrt(precision)

	m_post, s_post = posterior_normal(18.0, 2.0, x_avg, n, sigma)
	lo, hi = stats.norm.ppf([0.025, 0.975], loc=m_post, scale=s_post)
	print(f"Posterior mean = {m_post:.2f} and sd = {s_post:.2f}")
	print(f"95% credible interval: [{lo:.1f}; {hi:.1f}]")  # [17.5; 21.5]

	mu = np.linspace(12, 26, 500)
	likelihood = stats.norm.pdf(mu, loc=x_avg, scale=sigma / np.sqrt(n))
	fig = make_subplots(rows=1, cols=2,
	                    subplot_titles=("Weak prior", "Informative prior"))
	fig.add_trace(go.Scatter(x=mu, y=likelihood,
	                         name="Posterior = likelihood"), row=1, col=1)
	fig.add_trace(go.Scatter(x=mu, y=stats.norm.pdf(mu, 18.0, 2.0),
	                         name="Prior N(18, 2^2)"), row=1, col=2)
	fig.add_trace(go.Scatter(x=mu, y=likelihood,
	                         name="Likelihood"), row=1, col=2)
	fig.add_trace(go.Scatter(x=mu, y=stats.norm.pdf(mu, m_post, s_post),
	                         name="Posterior"), row=1, col=2)
	fig.update_layout(xaxis_title="Viscosity mean", yaxis_title="Density")
	fig.show()

.. figure:: ../figures/univariate/bayes-viscosity-prior-likelihood-posterior.png
	:alt:	Generated by univariate/bayesian_univariate_figures.py in the figures repository
	:width: 750px
	:align: center
	:scale: 90

The figure shows both cases. On the left, the wide prior leaves the posterior equal to the
likelihood. On the right, the informative prior pulls the posterior toward 18 and narrows it; the
shaded region is the central 95% of the posterior, the credible interval.

The prior is the ingredient that must be justified. It has to describe knowledge that genuinely
applies to the quantity being estimated: if this cube came from a modified formulation, the
production records for the old grade do not apply, and a posterior built on them inherits that
mismatch. When there is doubt, a wider prior concedes influence to the data; in the limit, the
weak prior reproduces the data-only answer.

Updating one observation at a time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The update equations can also be applied one observation at a time: process the first viscosity
value with the plant-records prior :math:`\mathcal{N}(18, 2^2)`, then use the resulting posterior
as the prior for the second value, and so on. Yesterday's posterior becomes today's prior. Doing
so with :math:`\sigma = 3.5` gives a posterior mean and standard deviation of :math:`(19.23, 1.74)`
after the first observation, :math:`(18.82, 1.42)` after three, :math:`(19.36, 1.23)` after five,
and :math:`(19.49, 1.01)` after all nine: exactly the answer obtained by processing the nine values
in one step. This sequential form suits plant data, which arrive one batch at a time.

.. code-block:: python

	fig = go.Figure()
	m, v = 18.0, 2.0 ** 2
	fig.add_trace(go.Scatter(x=mu, y=stats.norm.pdf(mu, m, np.sqrt(v)),
	                         name="Prior (0 observations)"))
	for i, x in enumerate(viscosity, start=1):
	    v_new = 1 / (1 / v + 1 / sigma**2)
	    m = (m / v + x / sigma**2) * v_new
	    v = v_new
	    if i in {1, 3, 5, 9}:
	        fig.add_trace(go.Scatter(x=mu, y=stats.norm.pdf(mu, m, np.sqrt(v)),
	                                 name=f"After {i} observation(s)"))
	fig.update_layout(xaxis_title="Viscosity mean", yaxis_title="Density")
	fig.show()

.. figure:: ../figures/univariate/bayes-viscosity-sequential-updating.png
	:alt:	Generated by univariate/bayesian_univariate_figures.py in the figures repository
	:width: 750px
	:align: center
	:scale: 90

.. _univariate_bayes_unknown_variance:

When the variance is also unknown
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The known-:math:`\sigma` assumption is as unrealistic here as it was in :ref:`Case A of the
confidence-interval section <univariate_eqn_CI-mean-variance-known-again>`. In the more common
situation, :math:`\sigma` is estimated from the same nine values: :math:`s = 3.81`. The Bayesian
treatment then places a prior on :math:`\sigma` as well; with weak priors on both :math:`\mu` and
:math:`\sigma`, the posterior for :math:`\mu` works out to be a :math:`t`-distribution with
:math:`n - 1 = 8` degrees of freedom, centred at :math:`\overline{x} = 20.0` and scaled by
:math:`s/\sqrt{n} = 3.81/3 = 1.27`. We state this result without derivation:

.. math::

	\frac{\mu - \overline{x}}{s/\sqrt{n}} \,\Big|\, \text{data} \,\sim\, t_{n-1}

The 95% credible interval is :math:`20.0 \pm 2.306 \times 1.27 = [17.1; 22.9]`: the same numbers as
the confidence interval of :eq:`CI-mean-variance-unknown`, which used the same critical value
``qt(0.975, df=8) = 2.306``. The pattern from the known-variance case repeats: with weak priors,
the credible interval and the confidence interval agree numerically, and prior plant knowledge,
where it applies, is the extra information the Bayesian route can carry into the interval.

.. code-block:: python

	s = viscosity.std(ddof=1)
	lo, hi = stats.t.ppf([0.025, 0.975], df=n - 1,
	                     loc=x_avg, scale=s / np.sqrt(n))
	print(f"95% credible interval: [{lo:.1f}; {hi:.1f}]")  # [17.1; 22.9]

The same complementary reading returns at two later points in this chapter: for :ref:`comparing
two systems <univariate_bayesian_two_sample>`, where the posterior gives the probability that one
system's long-run mean exceeds the other's, and for :ref:`proportions
<univariate_beta_binomial>`, where the posterior for a proportion is a Beta distribution.
