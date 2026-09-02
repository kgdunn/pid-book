.. _DOE-omars-worked-study:

A worked OMARS study: four factors on a fed-batch bioreactor
==============================================================

The :ref:`OMARS trade-off table <DOE-omars-trade-off-table>` says what each run count makes
estimable, and the :ref:`staged analysis <DOE-analysing-economical-designs>` says how to fit
the result. Neither says what the runs are worth. This section runs a study end to end on a
process whose true behaviour is known, so the answer can be given in the units a team budgets
in: grams per litre of product, and weeks of bioreactor time.

The process is the fed-batch cell culture met in :ref:`Fractional factorial designs
<DOE-fractional-factorials>`, where a run takes ten days and a full factorial in five factors
"would take almost a year ... if parallel reactors are not available". Parallel reactors are
now the normal way such studies are run. A multi-parallel mini-bioreactor system such as the
Sartorius Ambr 250 holds 12 or 24 vessels of 100 to 250 mL under individual control, so a
campaign of thirty batches is two cassettes and about five weeks, turnaround included. That
is the calendar the run counts below are measured against.

The simulator is ``process_improve.simulation.batch``, a ten-day fed-batch bioreactor with
growth following the cardinal temperature and pH model of Rosso et al. (1995), production
following Luedeking and Piret (1959), an oxygen-transfer ceiling, hypothermic growth arrest,
and substrate-coupled production. Its kinetics are fixed and documented, so the true optimum
is computable and every recovered result can be scored against it. The noise the study faces
is the simulator's own, at a development-scale setting of its within-batch disturbance.

The process and the question
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The current recipe grows the culture at 36.8 °C, starts a temperature downshift on day 2.75
that takes 1.5 days to reach a production hold at 30 °C, holds pH at 7.1 throughout, and
feeds at a constant 0.055 L/day per litre of starting volume. Titer, the product
concentration at harvest, runs 7 to 8 g/L. The team wants to know whether the hold
temperature, the timing of the shift, the pH and the feed rate should move, and by how much.

Four factors, one response. Their ranges are what a process engineer would choose around a
running recipe, and the centre of each is the current setting:

.. list-table::
	:widths: 44 14 14 14
	:header-rows: 1

	* - Factor
	  - Low
	  - Centre
	  - High
	* - Production hold temperature, °C
	  - 28.5
	  - 30.0
	  - 31.5
	* - Shift start, day
	  - 2.0
	  - 2.75
	  - 3.5
	* - pH setpoint
	  - 6.9
	  - 7.1
	  - 7.3
	* - Feed rate, L/day per litre
	  - 0.040
	  - 0.055
	  - 0.070

Every figure in this section is reproducible with ``process_improve``. Each block imports
what it needs and reuses variables from the blocks before it, so paste them in order.

.. code-block:: python

	import dataclasses
	import itertools

	import numpy as np
	import pandas as pd
	from scipy import optimize, stats

	from process_improve.experiments import Factor, analyze_omars, generate_omars
	from process_improve.simulation import BioreactorConfig, BioreactorSimulator

	factors = [
	    Factor(name="hold_temp", low=28.5, high=31.5),    # production hold temperature, degC
	    Factor(name="shift_day", low=2.0, high=3.5),      # day the downshift starts
	    Factor(name="pH", low=6.9, high=7.3),
	    Factor(name="feed_rate", low=0.040, high=0.070),  # L/day per litre of starting volume
	]
	names = [f.name for f in factors]
	GROWTH_TEMP, RAMP_DAYS = 36.8, 1.5

	# The simulator's default disturbance level is pilot scale; a development-scale system
	# with tighter control sees less within-batch variation.
	config = dataclasses.replace(BioreactorConfig(), within_batch_scale=0.7)

	def recipe(cfg, hold_temp, shift_day, pH):
	    """The setpoint schedule for one batch: warm growth, a ramp, then the cold hold."""
	    days = cfg.interval_start_days
	    fraction = np.clip((days - shift_day) / RAMP_DAYS, 0.0, 1.0)
	    temperature = GROWTH_TEMP - (GROWTH_TEMP - hold_temp) * fraction
	    return pd.DataFrame({"pH": np.full_like(days, pH), "temperature": temperature},
	                        index=pd.Index(days, name="day"))

	def run_batch(cfg, hold_temp, shift_day, pH, feed_rate, random_state):
	    """Final titer, in g/L, of one batch at these settings."""
	    sim = BioreactorSimulator(dataclasses.replace(cfg, feed_rate=feed_rate))
	    return sim.simulate_batch(trajectory=recipe(cfg, hold_temp, shift_day, pH),
	                              random_state=random_state).titer

	current = {"hold_temp": 30.0, "shift_day": 2.75, "pH": 7.1, "feed_rate": 0.055}
	reps = np.array([run_batch(config, **current, random_state=s) for s in range(20)])
	print(f"{reps.mean():#.4g} {reps.std(ddof=1):#.4g}")   # 7.477 0.2308, a CV of 3.1%

Twenty replicate batches at the current recipe give 7.477 g/L with a standard deviation of
0.2308 g/L, a coefficient of variation of 3.1%. That is the noise every effect below is
measured against. The response is analysed as log titer: the kinetics are multiplicative,
and the replicate spread is not constant across the region, being about three times larger at
a 29 °C hold than at 31 °C. On the log scale that spread is near enough constant for a single
error estimate to serve.

Choosing the run count
~~~~~~~~~~~~~~~~~~~~~~~~~

The four-factor column of the :ref:`trade-off table <DOE-omars-trade-off-table>` offers
``Quad`` from 11 runs and ``Full`` from 21, with the Box-Behnken design at 27. The team has
no reason to expect the interactions to be absent, and the shift timing and hold temperature
are the sort of pair that plausibly interact, so the study needs ``Full``: every two-factor
interaction in the model. That leaves the choice between 21 runs, the frontier, and 27. The
section :ref:`What fewer runs would have bought <DOE-omars-study-fewer-runs>` measures that
choice; the study takes 27 runs and adds three centre runs, for thirty batches in two cassettes.

Building the campaign
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	design = generate_omars(factors, n_runs=27, model="main_quadratic", random_seed=42)
	coded = design.design[names].to_numpy(float)
	print(design.metadata["model_rank"], design.metadata["expected_error_df"])   # 9, 18

The 27 runs are thirteen half-rows, their thirteen mirror images, and one centre run. The two
cassettes run weeks apart, so anything that differs between them, a new lot of feed medium
in this study, shifts every batch in the second cassette by a common amount. That shift must
not be confused with a factor effect, and a foldover makes that easy to arrange: keep each
half-row with its mirror image in the same cassette, and every main effect sums to zero
within each cassette, whichever way the pairs are divided.

.. code-block:: python

	is_centre = np.all(coded == 0, axis=1)
	rows = [i for i in range(len(coded)) if not is_centre[i]]
	pairs, seen = [], set()
	for i in rows:
	    if i in seen:
	        continue
	    j = next(k for k in rows if k not in seen and k != i and np.allclose(coded[k], -coded[i]))
	    pairs.append((i, j))
	    seen.update((i, j))
	print(len(pairs), int(is_centre.sum()))   # 13 mirror pairs, 1 centre run

The second-order columns do not sum to zero within a cassette, so the split of the thirteen
pairs into seven and six is chosen to keep the cassette indicator as nearly uncorrelated with
the quadratics and interactions as it can be. There are 1716 ways to choose seven pairs from
thirteen; all are tried.

.. code-block:: python

	def second_order_columns(C):
	    cols = [C[:, i] ** 2 for i in range(C.shape[1])]
	    cols += [C[:, i] * C[:, j] for i, j in itertools.combinations(range(C.shape[1]), 2)]
	    return np.column_stack(cols)

	so = second_order_columns(coded)
	keep = ~is_centre
	best_split, best_r = None, np.inf
	for chosen in itertools.combinations(range(len(pairs)), 7):
	    block = np.full(len(coded), -1.0)
	    for p in chosen:
	        block[list(pairs[p])] = 1.0
	    r = max(abs(np.corrcoef(block[keep], so[keep, c])[0, 1])
	            for c in range(so.shape[1]) if so[keep, c].std() > 0)
	    if r < best_r:
	        best_split, best_r = chosen, r
	block = np.full(len(coded), -1.0)
	for p in best_split:
	    block[list(pairs[p])] = 1.0
	print(f"{best_r:#.4g}")   # 0.2271, the largest |r| between cassette and any second-order column

Three centre runs are added so that each cassette carries two, placed about a third and two
thirds of the way through its run order rather than together. The run order within a cassette
is otherwise random.

.. code-block:: python

	rng = np.random.default_rng(7)
	plan = pd.DataFrame(coded, columns=names)
	plan["cassette"] = np.where(block > 0, 1, 2)
	plan.loc[is_centre, "cassette"] = 1
	extra = pd.DataFrame(np.zeros((3, 4)), columns=names)
	extra["cassette"] = [1, 2, 2]
	plan = pd.concat([plan, extra], ignore_index=True)

	order = []
	for c in (1, 2):
	    idx = plan.index[plan["cassette"] == c].to_numpy()
	    centres = idx[np.all(plan.loc[idx, names] == 0, axis=1)]
	    seq = list(rng.permutation(idx[~np.isin(idx, centres)]))
	    for k, cpt in enumerate(centres):
	        seq.insert(int(round((k + 1) * len(idx) / (len(centres) + 1))), cpt)
	    order.extend(seq)
	plan = plan.loc[order].reset_index(drop=True)
	plan.index = pd.RangeIndex(1, len(plan) + 1, name="run")
	for n, f in zip(names, factors):
	    plan[n] = f.low + (plan[n] + 1) / 2 * (f.high - f.low)   # coded to real units
	print(plan["cassette"].value_counts().sort_index().tolist())   # [16, 14]

Cassette 1 holds sixteen batches and cassette 2 fourteen. Both fit a 24-vessel system with
room to spare.

Running it
~~~~~~~~~~~~

The second cassette draws on a new lot of feed medium that assays 12% weaker in substrate.
Nothing else changes between the cassettes. Each batch gets its own disturbance draw.

.. code-block:: python

	lot = {1: config, 2: dataclasses.replace(config, feed_substrate=0.88 * config.feed_substrate)}
	seeds = np.random.default_rng(2026).integers(1 << 30, size=len(plan))
	plan["titer"] = [run_batch(lot[int(r.cassette)], r.hold_temp, r.shift_day, r.pH, r.feed_rate, int(s))
	                 for r, s in zip(plan.itertuples(), seeds)]
	plan["log_titer"] = np.log(plan["titer"])
	print(f"{plan['titer'].min():#.4g} {plan['titer'].max():#.4g}")   # 4.290 9.116

	is_cp = np.all(np.isclose(plan[names], list(current.values())), axis=1)
	print(plan.loc[is_cp, ["cassette", "titer"]])

.. code-block:: text

	     cassette     titer
	run
	6           1  7.804948
	12          1  7.267075
	22          2  6.538538
	26          2  6.893483

The titer ranges from 4.290 to 9.116 g/L across the thirty batches, against 7.477 g/L at the
current recipe: the region is wide enough that some settings are clearly worse and some
clearly better than what the team runs today. The four centre points, at runs 6, 12, 22 and
26, average 7.536 g/L in the first cassette and 6.716 g/L in the second.

The cassette effect
~~~~~~~~~~~~~~~~~~~~~~

The centre points suggest the second cassette ran lower, but four points on two degrees of
freedom cannot say so with any confidence. The design as a whole can. A least-squares fit of
log titer on a cassette indicator and the four main effects estimates the shift from all
thirty runs, and because whole mirror pairs were kept together, the main effects and the
cassette indicator are exactly orthogonal, so neither steals from the other.

.. code-block:: python

	C = np.column_stack([(plan[n] - f.low) / (f.high - f.low) * 2 - 1 for n, f in zip(names, factors)])
	cassette = np.where(plan["cassette"] == 2, 1.0, 0.0)
	X = np.column_stack([np.ones(len(plan)), cassette, C])
	b = np.linalg.lstsq(X, plan["log_titer"], rcond=None)[0]
	resid = plan["log_titer"] - X @ b
	df = len(plan) - X.shape[1]
	se = np.sqrt(resid @ resid / df * np.linalg.inv(X.T @ X)[1, 1])
	print(f"{b[1]:#.4g} {se:#.4g} {b[1] / se:#.4g} on {df} df")   # -0.1272 0.05092 -2.498 on 24 df

	cp = plan[is_cp]
	t_cp = stats.ttest_ind(cp.loc[cp.cassette == 2, "log_titer"], cp.loc[cp.cassette == 1, "log_titer"])
	print(f"{t_cp.statistic:#.4g} {t_cp.pvalue:#.4g}")   # -2.587 0.1226

	plan["log_titer_adj"] = plan["log_titer"] - b[1] * cassette

The second cassette ran 0.1272 log units lower, a titer 11.9% below the first, with a
standard error of 0.05092: a *t* of 2.498 on 24 degrees of freedom. The four centre points on
their own give almost the same *t*, 2.587, and a *p*-value of 0.12, because they have two
degrees of freedom to judge it on. The signal is the same size in both; only the design has
the degrees of freedom to call it. The shift is subtracted from the second cassette's
responses, and the rest of the analysis works on the adjusted values.

This is the practical reason to build a block into a design rather than to hope a few
replicates will reveal one afterwards. The OMARS family has been extended to orthogonally
blocked designs, referenced in :ref:`the introduction <DOE-omars-designs>`; the pairing
argument above is the simplest form of the same idea.

The staged analysis
~~~~~~~~~~~~~~~~~~~~~~

At thirty runs the full second-order model, fifteen terms, can be fitted in one step, and
it can here: feed rate, the hold-temperature quadratic and the hold-temperature by shift-day
interaction come out significant, with fifteen degrees of freedom for error. The
:ref:`staged analysis <DOE-analysing-economical-designs>` reaches the same three terms by a
route that also works at the sizes where the full model cannot be fitted at all, and it
pools the inactive terms into the error estimate as it goes.

.. code-block:: python

	result = analyze_omars(plan[names], plan["log_titer_adj"],
	                       quadratic_heredity="none", interaction_heredity="none")
	print(result.active_main_effects)               # ['feed_rate']
	print(f"{result.main_effect_p_values['hold_temp']:#.4g}")   # 0.06814
	print(result.updated_error_df, f"{result.updated_rmse:#.4g}")   # 18 0.08047
	print(f"{result.second_order_overall_p_value:#.4g}")          # 0.0006660
	print(result.active_quadratics, result.active_interactions)
	# ['hold_temp^2'] ['hold_temp:shift_day']

Of the four main effects only the feed rate is active. The hold temperature's linear effect
has a *p*-value of 0.068: not because the hold temperature does not matter, but because the
region straddles its optimum, so the response goes up and then down across the range and the
linear term is nearly zero. pH and shift day are inactive and are pooled into the error,
which rises from fifteen to eighteen degrees of freedom. The gate on the second-order terms
then opens decisively, *p* = 0.000666, and the search selects two of the ten: the
hold-temperature quadratic and the interaction between hold temperature and shift day.

The heredity option matters here, and in the direction that is easy to get wrong.

.. code-block:: python

	strict = analyze_omars(plan[names], plan["log_titer_adj"],
	                       quadratic_heredity="strong", interaction_heredity="strong")
	print(strict.active_quadratics, strict.active_interactions)   # ['feed_rate^2'] []

Strong heredity admits a second-order term only if its parent main effect is active. At an
optimum the linear term vanishes by definition, so the rule discards exactly the terms that
locate it, and offers a quadratic in the one active factor instead. The heredity principle
in the :ref:`staged workflow <DOE-analysing-economical-designs>` is a guide to which of many
candidate interactions to prefer, not a filter to apply before looking; when a factor's
linear effect is small in a region that contains its optimum, the quadratic and the
interactions of that factor are the ones to look for.

The recommended recipe, against the truth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The selected model has four terms: the intercept, the feed rate, the hold-temperature
quadratic and the interaction. It is refitted, and its maximum found over the region, moving
only the three factors the model mentions; the pH stays where it is, since the study found no
reason to move it.

.. code-block:: python

	terms = [("m", names.index(m)) for m in result.active_main_effects]
	terms += [("q", names.index(q[:-2])) for q in result.active_quadratics]
	terms += [("i", tuple(names.index(v) for v in it.split(":"))) for it in result.active_interactions]

	def model_matrix(terms, C):
	    C = np.atleast_2d(np.asarray(C, float))
	    cols = [np.ones(len(C))]
	    for kind, j in terms:
	        cols.append(C[:, j] if kind == "m" else C[:, j] ** 2 if kind == "q"
	                    else C[:, j[0]] * C[:, j[1]])
	    return np.column_stack(cols)

	bs = np.linalg.lstsq(model_matrix(terms, C), plan["log_titer_adj"], rcond=None)[0]
	moved = sorted({j for k, j in terms if k != "i"} | {v for k, j in terms if k == "i" for v in j})

	def predicted(z):
	    x = np.zeros(4)
	    x[moved] = z
	    return -float((model_matrix(terms, x) @ bs).ravel()[0])

	starts = [np.zeros(len(moved)), -np.ones(len(moved)), np.ones(len(moved))]
	opt = min((optimize.minimize(predicted, s, method="Powell", bounds=[(-1, 1)] * len(moved))
	           for s in starts), key=lambda r: r.fun)
	x_rec = np.zeros(4)
	x_rec[moved] = opt.x
	decode = lambda x: {n: f.low + (x[i] + 1) / 2 * (f.high - f.low)
	                    for i, (n, f) in enumerate(zip(names, factors))}
	print({n: f"{v:#.4g}" for n, v in decode(x_rec).items()})
	# {'hold_temp': '29.54', 'shift_day': '3.500', 'pH': '7.100', 'feed_rate': '0.07000'}
	print(f"{np.exp(-opt.fun):#.4g}")   # 8.570 g/L predicted

The model recommends a hold at 29.54 °C, the shift starting on day 3.5, and the feed at
0.070 L/day, and predicts 8.570 g/L there. Two of those settings are at the edge of the
region. The feed rate at its top is what the data say, a strong positive main effect with no
curvature found. The shift day at its top is different: the model carries the shift day only
through its interaction with hold temperature, and at the recommended hold that interaction
is positive, so the optimiser pushes it to the boundary. A recommendation on a boundary is
the model saying it does not know the shape of the response in that direction.

The simulator settles what the data could not. With every disturbance switched off, the true
titer at any recipe is a single number.

.. code-block:: python

	quiet = dataclasses.replace(config, ic_scale=0.0, within_batch_scale=0.0, noise_scale=0.0)
	truth = lambda x: run_batch(quiet, **decode(np.clip(x, -1, 1)), random_state=0)
	best = max((optimize.minimize(lambda x: -truth(x), s, method="Powell", bounds=[(-1, 1)] * 4)
	            for s in [np.zeros(4), np.array([-1.0, -1, 0, 1]), np.array([-0.5, 0.5, 0, 1])]),
	           key=lambda r: -r.fun)
	print(f"{truth(np.zeros(4)):#.4g} {truth(x_rec):#.4g} {-best.fun:#.4g}")   # 7.436 8.376 9.442
	print({n: f"{v:#.4g}" for n, v in decode(best.x).items()})
	# {'hold_temp': '29.52', 'shift_day': '2.624', 'pH': '7.100', 'feed_rate': '0.07000'}

.. list-table::
	:widths: 34 22 22
	:header-rows: 1

	* - Recipe
	  - True titer, g/L
	  - Gain over current
	* - Current
	  - 7.436
	  -
	* - Recommended by the study
	  - 8.376
	  - 0.940
	* - True best in the region
	  - 9.442
	  - 2.006

The study captured 0.940 g/L of the 2.006 g/L that was available, 47%. The hold temperature
is right to within 0.02 °C and the feed rate is right. The shift day is wrong: the true
optimum shifts on day 2.62, earlier than today's 2.75, and the study sent it later. The
shift-day quadratic that would have caught this is the smallest of the real effects, and this
campaign did not find it. Repeated over two hundred disturbance draws, the 27-run design
finds it in 29% of them.

The four centre points supply a pure-error estimate and a test of whether the four-term
model is adequate.

.. code-block:: python

	rs = plan["log_titer_adj"] - model_matrix(terms, C) @ bs
	cp_adj = plan.loc[is_cp, "log_titer_adj"]
	pure = ((cp_adj - cp_adj.mean()) ** 2).sum()
	df_pe = len(cp_adj) - 1
	df_lof = len(plan) - len(bs) - df_pe
	F = ((rs @ rs - pure) / df_lof) / (pure / df_pe)
	p_lof = 1 - stats.f.cdf(F, df_lof, df_pe)
	print(f"{np.sqrt(pure / df_pe):#.4g} {F:#.4g} on ({df_lof}, {df_pe}) df, p = {p_lof:#.4g}")
	# 0.03696 5.349 on (23, 3) df, p = 0.09582

The lack-of-fit *F* is 5.349, with a *p*-value of 0.096: not significant at 5%, on three
degrees of freedom of pure error. A team that wanted this test to have teeth would run more
centre points, or accept, as here, that it is a check rather than a verdict.

.. _DOE-omars-study-fewer-runs:

What fewer runs would have bought
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thirty batches in five weeks is a real cost, and the question a team will ask is whether
seventeen, or thirteen, would have done. The simulator can answer it, because the same study
can be rerun at every size with fresh disturbance draws, and each rerun scored the same way:
follow the recipe the fitted model recommends, and read the true titer there.

.. figure:: ../figures/doe/omars-worked-study-tradeoff.png
	:source: doe/omars-worked-study-tradeoff.py
	:alt: Titer gained over the current recipe against the number of runs, for OMARS designs of 13 to 31 runs and for the 27-run Box-Behnken and central composite designs, showing the median, the 10th to 90th percentile band and the worst case over two hundred campaigns each.
	:width: 760px
	:align: center

	What each design size buys, over two hundred simulated campaigns per design. The line
	is the median gain in titer at the recipe each campaign recommends, the band runs from
	the 10th to the 90th percentile, and the marks below are the worst campaign of the two
	hundred. The dashed line is the 2.006 g/L that was available. The Box-Behnken and
	face-centred central composite designs, both 27 runs, are placed beside the 27-run OMARS.

.. list-table::
	:widths: 20 10 12 12 12 12 12
	:header-rows: 1

	* - Design
	  - Runs
	  - Finds feed rate
	  - Finds the interaction
	  - Finds the quadratic
	  - Median gain, g/L
	  - Worst case, g/L
	* - OMARS
	  - 13
	  - 0.14
	  - 0.67
	  - 0.30
	  - +0.000
	  - -1.973
	* - OMARS
	  - 17
	  - 0.94
	  - 0.35
	  - 0.21
	  - +0.717
	  - -3.246
	* - OMARS
	  - 21
	  - 0.33
	  - 0.72
	  - 0.40
	  - +0.118
	  - -2.560
	* - OMARS
	  - 27
	  - 1.00
	  - 0.99
	  - 0.78
	  - +1.072
	  - -0.350
	* - Box-Behnken
	  - 27
	  - 0.99
	  - 0.41
	  - 0.77
	  - +1.199
	  - -2.810
	* - Central composite
	  - 27
	  - 0.91
	  - 1.00
	  - 0.88
	  - +0.942
	  - -1.584
	* - OMARS
	  - 31
	  - 0.98
	  - 0.97
	  - 0.88
	  - +1.034
	  - -1.298

Every row is two hundred campaigns, each drawing fresh disturbances and scored by the true
titer at the recipe its analysis recommended. The columns headed *finds* give the fraction of
campaigns in which the staged analysis declared that effect active.

Below 27 runs the outcome is closer to a lottery than to a smaller version of the same
study. The 13-run design leaves the median campaign exactly where it started, having found
nothing it could act on, and its worst campaign loses 1.973 g/L. The 17-run design finds the
feed rate in 94% of campaigns and gains 0.717 g/L at the median, but its worst campaign
loses 3.246 g/L, because a design that finds the feed rate without the curvature sends the
hold temperature to an edge of the region.

The 21-run design, the estimability frontier, does worse at the median than the 17-run
design, and the reason is worth knowing. The search returned a 21-run design that varies the
feed rate in twelve of its runs, the same twelve as the 17-run design; the four added runs
hold the feed rate at its centre while moving the hold temperature and shift day. Those
runs add second-order variation to the residual the main effects are first tested against,
and no information about the feed rate, so the feed rate is declared active in only a third
of campaigns. Which design occupies a cell matters, as :ref:`Nine measures down one column
<DOE-omars-metric-choice>` showed for the three-factor column; here it is the difference
between finding the largest main effect and missing it.

At 27 runs every real effect but the shift-day curvature is found in three campaigns out of
four or better, the median gain is 1.072 g/L, and the worst of two hundred campaigns loses
0.350 g/L. Four more runs, at 31, raise the 10th percentile from 0.118 to 0.577 g/L and leave
the median where it was.

The two classical designs at 27 runs sit alongside. The Box-Behnken design has the higher
median, 1.199 g/L, and the wider spread in both directions: a 90th percentile of 1.677 g/L
and a worst campaign of 2.810 g/L lost. It finds the interaction in 41% of campaigns
against 99% for the OMARS design, and campaigns that miss the interaction leave the shift
day at its current setting, which in this process happens to be nearer the true optimum
than the edge the interaction sends it to. The face-centred central composite design finds
the interaction every time and gains 0.942 g/L at the median. On this process and this
region the three 27-run designs are comparable at the middle of their distributions; they
differ in the tails, and a team choosing among them would be choosing how much downside to
accept.

The model that generated the data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simulator's kinetics are given in full in the module documentation of
``process_improve.simulation.batch``. The parts that shaped this study are three. The
production hold has an interior optimum near 29.5 °C because residual growth at a warmer
hold burns feed the product needs, while a colder hold arrests growth before the culture has
built enough biomass to produce from. The timing of the shift interacts with the hold
temperature for the same reason: shifting late is right only if the hold is warm enough to
keep some growth going. And pH is held at the optimum of a cardinal model that is flat within
0.2 of it, so the study was correct to find nothing there.

The disturbance channel that gave every batch its own outcome is an autocorrelated
multiplier on the growth and production rates, with a correlation time comparable to the
batch length, at 0.7 of the simulator's pilot-scale default. The lot change was a 12%
reduction in the feed medium's substrate concentration. None of these were visible to the
analysis; all of them were recovered from thirty batches, except the direction in which to
move the shift day.

**Readings**

* Rosso, L., Lobry, J. R., Bajard, S. and Flandrois, J. P.: "Convenient model to describe
  the combined effects of temperature and pH on microbial growth", *Applied and
  Environmental Microbiology*, **61**, 610--616, 1995.
* Luedeking, R. and Piret, E. L.: "A kinetic study of the lactic acid fermentation",
  *Journal of Biochemical and Microbiological Technology and Engineering*, **1**, 393--412,
  1959.
