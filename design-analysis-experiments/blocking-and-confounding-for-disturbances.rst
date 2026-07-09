.. _DOE_blocking_section:

Blocking and confounding for disturbances
===========================================

Characterization of disturbances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: disturbance; experiments

.. youtube:: https://www.youtube.com/watch?v=ugqXsS_r4WU&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=47

External disturbances will always have an effect on our response variable, :math:`y`. Operators, ambient conditions, physical equipment, lab analyses, and time-dependent effects (catalyst deactivation, fouling), will impact the response. This is why it is crucial to :ref:`randomize <DOE-randomization>` the order of experiments: so that these **unknown, unmeasurable, and uncontrollable** disturbances cannot systematically affect the response.

However, certain disturbances are **known, or controllable, or measurable**. For these cases we perform pairing and blocking. We have already discussed pairing in the univariate section: pairing is when two experiments are run on the same subject and we analyze the differences in the two response values, rather than the actual response values. If the effect of the disturbance has the same magnitude on both experiments, then that disturbance will cancel out when calculating the difference. The magnitude of the disturbance is expected to be different between paired experiments, but is expected to be the same within the two values of the pair.

Blocking is slightly different: blocking is a special way of running the experiment so that the disturbance actually does affect the response, but we construct the experiment so that this effect is not misleading.

Finally, a disturbance can be characterized as a **controlled disturbance**, in which case it isn't a disturbance anymore, as it is held constant for all experiments, and its effect cancels out. But it might be important to investigate  the controlled disturbance, especially if the system is operated later on when this disturbance is at a different level.


.. Add discussion from MOOC about disturbances and covariates here, including the mind map from that discussion.



.. _DOE-Blocking-and-confounding:

Blocking and confounding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=In-ai2FLVGQ&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=48

It is common for known, or controllable or measurable factors to have an effect on the response. However these disturbance factors might not be of interest to us during the experiment. Cases are:

	-	*Known and measurable, not controlled*: Reactor vessel A is known to achieve a slightly better response, on average, than reactor B. However both reactors must be used to complete the experiments in the short time available.

	-	*Known, but not measurable nor controlled*: There is not enough material to perform all :math:`2^3` runs, there is only enough for 4 runs. The impurity in either the first batch A for 4 experiments, or the second batch B for the other 4 runs will be different, and might either increase or decrease the response variable (we don't know the effect it will have).

	-	*Known, measurable and controlled*: Reactor vessel A and B have a known, measurable effect on the output, :math:`y`. To control for this effect we perform all experiments in either reactor A or B, to prevent the reactor effect from :index:`confounding` (confusing) our results.

.. image:: ../figures/doe/blocking-factorial-3-factors.png
	:align: left
	:scale: 50
	:width: 900px
	:alt: Cube showing a two-level, three-factor factorial split into two blocks on the ABC interaction

In this section then we will deal with disturbances that are known, but their effect may or may not be measurable. We will also assume that we cannot control that disturbance, but we would like to minimize its effect.

For example, if we don't have enough material for all :math:`2^3` runs, but only enough for 4 runs, the question is how to arrange the 2 sets of 4 runs so that the known, by unmeasurable disturbance from the impurity has the least effect on our results and interpretation of the 3 factors.

Our approach is to intentionally *confound*  the effect of the disturbance with an effect that is expected to be the least significant. The :math:`A \times B \times C` interaction term is almost always going to be small for many systems, so we will split the runs that the first 4 are run at the low level of :math:`ABC` and the other four at the high level, as illustrated.

Each group of 4 runs is called a *block* and the process of creating these 2 blocks is called :index:`blocking <pair: blocking; experiments>`. The experiments within each block must be run randomly.

.. tabularcolumns:: |c||c|c|c||c|c|c||c||c|

+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| Experiment| A          | B         |  C         | AB        | AC        | BC        | ABC           | Response, :math:`y`     |
+===========+============+===========+============+===========+===========+===========+===============+=========================+
| 1         | |-|        | |-|       |  |-|       | |+|       | |+|       | |+|       | |-| (batch 1) | :math:`\widetilde{y}_1` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 2         | |+|        | |-|       |  |-|       | |-|       | |-|       | |+|       | |+| (batch 2) | :math:`\mathring{y}_2`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 3         | |-|        | |+|       |  |-|       | |-|       | |+|       | |-|       | |+| (batch 2) | :math:`\mathring{y}_3`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 4         | |+|        | |+|       |  |-|       | |+|       | |-|       | |-|       | |-| (batch 1) | :math:`\widetilde{y}_4` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 5         | |-|        | |-|       |  |+|       | |+|       | |-|       | |-|       | |+| (batch 2) | :math:`\mathring{y}_5`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 6         | |+|        | |-|       |  |+|       | |-|       | |+|       | |-|       | |-| (batch 1) | :math:`\widetilde{y}_6` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 7         | |-|        | |+|       |  |+|       | |-|       | |-|       | |+|       | |-| (batch 1) | :math:`\widetilde{y}_7` |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+
| 8         | |+|        | |+|       |  |+|       | |+|       | |+|       | |+|       | |+| (batch 2) | :math:`\mathring{y}_8`  |
+-----------+------------+-----------+------------+-----------+-----------+-----------+---------------+-------------------------+


If the raw material has a significant effect on the response variable, then we will not be able to tell whether it was due to the :math:`A \times B \times C` interaction, or due to the raw material, since :math:`\hat{\beta}_{ABC} \rightarrow \underbrace{\text{ABC interaction}}_{\text{expected to be small}} + \text{raw material effect}`.

But the small loss due to this confusion of effects, is the gain that we can still estimate the main effects and two-factor interactions without bias, provided the effect of the disturbance is constant. Let's see how we get this result by denoting :math:`\widetilde{y}_i` as a :math:`y` response from the first batch of materials and let :math:`\mathring{y}_i` denote a response from the second batch.

Each estimate is the corresponding column of :math:`\pm 1` signs applied to the responses. Writing :math:`\widetilde{y}` for a batch 1 response and :math:`\mathring{y}` for a batch 2 response, the seven contrasts are:

	.. math::

		\hat{\beta}_A    &= -\widetilde{y}_1 + \mathring{y}_2 - \mathring{y}_3 + \widetilde{y}_4 - \mathring{y}_5 + \widetilde{y}_6 - \widetilde{y}_7 + \mathring{y}_8 \\
		\hat{\beta}_B    &= -\widetilde{y}_1 - \mathring{y}_2 + \mathring{y}_3 + \widetilde{y}_4 - \mathring{y}_5 - \widetilde{y}_6 + \widetilde{y}_7 + \mathring{y}_8 \\
		\hat{\beta}_C    &= -\widetilde{y}_1 - \mathring{y}_2 - \mathring{y}_3 - \widetilde{y}_4 + \mathring{y}_5 + \widetilde{y}_6 + \widetilde{y}_7 + \mathring{y}_8 \\
		\hat{\beta}_{AB} &= +\widetilde{y}_1 - \mathring{y}_2 - \mathring{y}_3 + \widetilde{y}_4 + \mathring{y}_5 - \widetilde{y}_6 - \widetilde{y}_7 + \mathring{y}_8\\
		\hat{\beta}_{AC} &= +\widetilde{y}_1 - \mathring{y}_2 + \mathring{y}_3 - \widetilde{y}_4 - \mathring{y}_5 + \widetilde{y}_6 - \widetilde{y}_7 + \mathring{y}_8 \\
		\hat{\beta}_{BC} &= +\widetilde{y}_1 + \mathring{y}_2 - \mathring{y}_3 - \widetilde{y}_4 - \mathring{y}_5 - \widetilde{y}_6 + \widetilde{y}_7 + \mathring{y}_8 \\
		\hat{\beta}_{ABC} &= -\widetilde{y}_1 + \mathring{y}_2 + \mathring{y}_3 - \widetilde{y}_4 + \mathring{y}_5 - \widetilde{y}_6 - \widetilde{y}_7 + \mathring{y}_8 \\

Now imagine the :math:`y` response was raised by :math:`g` units for every batch 1 experiment and by :math:`h` units for every batch 2 experiment. The bias this adds to a contrast is :math:`g` times the sum of that contrast's signs on the batch 1 runs, plus :math:`h` times the sum of its signs on the batch 2 runs. Take :math:`\hat{\beta}_A`: its batch 1 runs are 1, 4, 6, 7 with signs :math:`-, +, +, -` which sum to zero, and its batch 2 runs are 2, 3, 5, 8 with signs :math:`+, -, -, +` which also sum to zero, so the bias is :math:`0 \cdot g + 0 \cdot h = 0`. The same holds for every main effect and every two-factor interaction: each is orthogonal to the :math:`ABC` column that defines the blocks, so its signs balance within each batch and the biases :math:`g` and :math:`h` cancel exactly.

The :math:`ABC` contrast is the exception. By construction batch 1 is the four runs with :math:`ABC = -1` and batch 2 the four with :math:`ABC = +1`, so :math:`\hat{\beta}_{ABC}` has all :math:`-1` signs on batch 1 and all :math:`+1` on batch 2. Its bias is :math:`(-4)g + (+4)h = 4(h - g)`: the whole batch-to-batch difference lands on :math:`\hat{\beta}_{ABC}`, which is why the block is confounded with the three-factor interaction and nowhere else. This is exactly the outcome we wanted: the disturbance is quarantined in the one effect we expected to be negligible, leaving all the main effects and two-factor interactions clean.

Another way to view this problem is that the first batch of materials and the second batch of materials can be represented by a new variable, called :math:`D` with value of :math:`D_{-} =` batch 1 and :math:`D_{+} =` batch 2. We will show next that we must consider this new factor to be generated from the other three: **D = ABC**.

We will also address the case when there are more than two blocks in the next section on the :ref:`use of generators <DOE-generators>`. For example, what should we do if we have to run a :math:`2^3` factorial but with only enough material for 2 experiments at a time?

.. _DOE-fixed-and-random-blocks:

Fixed and random block effects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far the block has been a single :math:`\pm 1` column (the :math:`ABC` contrast, or the factor
:math:`D`), and we estimated its effect like any other. Whether to treat that block effect as
*fixed* or *random* is a modelling choice, and it depends on where the blocks came from.

Treat the blocks as **fixed** when they are specific, non-repeatable conditions and you care only
about the runs you actually performed: this particular reactor versus that one, or these two
particular batches of material. Each block then carries its own effect, so :math:`b` blocks cost
:math:`b - 1` parameters to estimate. Ordinary least squares handles this, and it is what the
confounding approach above does. The limitation is that a fixed-block model says nothing about a
*future* block: it describes only the blocks in hand.

Treat the blocks as **random** when they are a sample from a larger population you want to
generalize over. A blocking factor is usually not under your control and not reproducible: you can
include several days, operators, or supplier lots in the study, but you cannot recreate a given day
or lot to run more experiments on it later. When the interest is in future days or lots, model the
block-to-block variation as random. The block effect :math:`\gamma_i` is then a draw from a
distribution with variance :math:`\sigma_\gamma^2`, and quantifying the differences between blocks
costs just that *one* variance parameter, no matter how many blocks there are.

Writing the response of the :math:`j`-th run in block :math:`i`,

.. math::

	Y_{ij} = \mathbf{f}'(\mathbf{x}_{ij})\,\boldsymbol{\beta} + \gamma_i + \varepsilon_{ij},

gives a :index:`mixed model <pair: mixed model; experiments>`: the factor effects
:math:`\boldsymbol{\beta}` are *fixed*, while the block effects
:math:`\gamma_i \sim N(0, \sigma_\gamma^2)` and the residuals
:math:`\varepsilon_{ij} \sim N(0, \sigma_\varepsilon^2)` are *random*. Two runs in the same block
share the same :math:`\gamma_i`, so they are correlated. That within-block (intraclass) correlation
is

.. math::

	\rho = \frac{\sigma_\gamma^2}{\sigma_\gamma^2 + \sigma_\varepsilon^2},

the fraction of the total variance that the block-to-block differences account for. The two
variance components are the two scatters in the figure below: :math:`\sigma_\gamma` is the spread of
the block means about the grand mean, and :math:`\sigma_\varepsilon` is the scatter of the runs
about their own block mean.

.. code-block:: python

	import plotly.graph_objects as go

	# Five blocks (e.g. days); each block's four runs scatter about that block's mean.
	blocks = [1, 2, 3, 4, 5]
	responses = {
	    1: [46.4, 47.9, 46.8, 47.7], 2: [51.6, 53.1, 52.0, 52.9],
	    3: [47.9, 49.3, 48.1, 49.1], 4: [52.9, 54.4, 53.1, 54.0],
	    5: [48.5, 49.9, 48.6, 49.8],
	}
	fig = go.Figure()
	for b in blocks:
	    ys = responses[b]
	    fig.add_trace(go.Scatter(x=[b] * len(ys), y=ys, mode="markers", showlegend=False))
	    mean = sum(ys) / len(ys)
	    fig.add_trace(go.Scatter(x=[b - 0.2, b + 0.2], y=[mean, mean], mode="lines",
	                             showlegend=False))          # the block mean
	grand = sum(v for ys in responses.values() for v in ys) / 20
	fig.add_hline(y=grand, line_dash="dash")                 # the grand mean
	fig.update_layout(xaxis_title_text="Block (e.g. day)", yaxis_title_text="Response")
	fig.show()

.. figure:: ../figures/doe/blocking-variance-components.png
	:align: center
	:width: 620px
	:alt: blocking-variance-components.py

	The two variance components of a blocked experiment. Each block (day) has a mean offset from
	the grand mean; the spread of those offsets is :math:`\sigma_\gamma`, the random block effect.
	Within a block, the runs scatter about the block mean by :math:`\sigma_\varepsilon`, the
	residual. The larger :math:`\sigma_\gamma` is relative to :math:`\sigma_\varepsilon`, the more
	alike two runs from the same block are.

The two ways of modelling the block differ in what they cost and what they deliver. Fixed blocks
make no assumption about a population of blocks, but they spend :math:`b - 1` parameters and cannot
predict beyond the blocks that were run. Random blocks spend a single variance parameter and support
statements about future blocks, at the cost of assuming the blocks are exchangeable draws. Because
random blocks are so much cheaper in parameters, a fixed-block design needs more runs to fit the
same factor model: when each block holds only two runs, the smallest fixed-block design needs
roughly twice as many runs as the smallest random-block design.

Because the responses within a block are correlated, ordinary least squares is no longer the most
precise estimator (it stays unbiased, but discards the correlation). The mixed model is fitted by
*generalized least squares* (GLS), which weights the correlated responses through their
covariance, with the variance components :math:`\sigma_\gamma^2` and :math:`\sigma_\varepsilon^2`
estimated by *restricted maximum likelihood* (REML), a method that returns unbiased variance
estimates. Statistical software does this for you; the derivation is given in
:ref:`Goos and Jones <DOE_references>`.

Whichever way the block is modelled, making the grouping explicit pulls the block-to-block variation
out of the residual. That lowers the error variance, :math:`\sigma_\varepsilon^2`, which raises the
:ref:`power <DOE-statistical-power>` of the significance tests for the factor effects. So blocking a
known source of variation does two things at once: it keeps the disturbance from biasing the factor
effects, and it sharpens the tests of those effects.


.. TODO: point out how blocking can be visualized as projectivity: in a 2 factor system (A and B) you have enough material only for 2 runs at a time. So you block on the AB interaction. But you can visualize that as a 3-factor factorial now, but run as a half-fraction, i.e. a 2^3_{III} design (show the cube with open and closed circles). This design has projectivity of 2 = 3-1, meaning a full 2^2 factorial is embedded in the design. If factor C (the blocking variable) has no effect on y, then you recover your full 2^2 factorial. That's why we typically block on the highest interaction possible.
