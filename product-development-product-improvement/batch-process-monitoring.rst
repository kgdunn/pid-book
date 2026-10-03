.. _APPS_batch_monitoring:

Batch process monitoring and improvement
=========================================

.. index::
	single: batch process monitoring
	pair: batch processes; applications

A batch makes its product in a fixed time and is then emptied, so what it leaves behind is not a
row of numbers but a table: every recorded tag, at every sample of the batch. Stack the tables of
many batches and the data set is a three-way array of batches by tags by time.

Every model of the trajectories in this section reaches that array the same way. The table of one batch is flattened
into a single long row, so the array becomes an ordinary matrix with one row per batch and one
column per (tag, time) pair, and the tools of the preceding sections apply to it unchanged. This is
batchwise unfolding, set out for PCA by `Nomikos and MacGregor (1994)
<https://literature.learnche.org/item/30/monitoring-batch-processes-using-multiway-principal-component-analysis>`_
and carried to PLS in their `multi-way partial least squares paper
<https://literature.learnche.org/item/32/multi-way-partial-least-squares-in-monitoring-batch-processes>`_
the following year. A component is then a weight on every (tag, time) cell, which says both which
tags matter and when in the batch they matter. `Westerhuis, Kourti and MacGregor (1999)
<https://literature.learnche.org/item/162/comparing-alternative-approaches-for-multivariate-statistical-analysis-of-batch-process-data>`_
compare it with the other ways of arranging the same array.

**What such a model can be asked is fixed by what it is given.** That single choice, and not the
choice of method, decides what each of the three case studies below can and cannot say.

Three worked case studies accompany this page. Each is built on a dataset that can be
downloaded and on models that can be reproduced with the code shown on the page:

* :ref:`APPS_batch_case_dupont`: a batch PCA model of the trajectories of an industrial
  polymerization reactor, used to find and diagnose unusual batches, and to show what the
  trajectories cannot reveal.
* :ref:`APPS_batch_case_sbr`: a batch PLS model from the trajectories of a simulated rubber
  reactor to the final latex quality, with the same kind of known fault, an impurity in the
  butadiene feed, injected at two different levels and two different times.
* :ref:`APPS_batch_case_fmc`: a multiblock batch PLS model of an industrial batch dryer, from
  the initial chemistry, the operating conditions and the trajectories to the final product
  quality.

.. _APPS_batch_what_goes_in:

What each model can be asked
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each study gives its model one more thing than the study before it, and each addition buys an
answer the previous model could not give.

.. table:: What each case study's model is given, and what that buys.

   +------------------+--------------------------+----------------------------------+----------------------------+
   | Study            | What the model is given  | What the model answers           | What it cannot see         |
   +==================+==========================+==================================+============================+
   | DuPont reactor   | Ten trajectories         | Which batches differ from the    | Anything whose cause       |
   |                  |                          | rest, in which tags, and at      | leaves no trace in those   |
   |                  |                          | which samples                    | ten tags                   |
   +------------------+--------------------------+----------------------------------+----------------------------+
   | SBR reactor      | Six trajectories and     | What the quality will be, from   | A quality attribute the    |
   |                  | five quality attributes  | part of a batch, and whether a   | trajectories do not drive  |
   |                  |                          | running batch is departing       |                            |
   +------------------+--------------------------+----------------------------------+----------------------------+
   | FMC dryer        | Eleven charge-chemistry  | Which of the three input blocks  | A cause in none of the     |
   |                  | measurements, nine       | a quality problem came from      | three input blocks         |
   |                  | operating conditions,    |                                  |                            |
   |                  | eleven trajectories and  |                                  |                            |
   |                  | eight quality attributes |                                  |                            |
   +------------------+--------------------------+----------------------------------+----------------------------+

Read the last column. A model is silent about whatever it was not given, and that silence is not
visible from inside the model. Four of the DuPont batches made poor product and sit among
the normal batches on both statistics the ten trajectories support. The
:ref:`first case study <APPS_batch_case_dupont>` ends on that point: the condition of a batch has
to be observable through the measurements before any model of them can report on it.

Adding a block is therefore a measurement decision before it is a modelling one. It also costs
something: in the :ref:`third case study <APPS_batch_case_fmc>` the chemistry block keeps under a
quarter of its own variation over the two components of the multiblock model, against half over
the two components of a PLS on that block alone, because the shared direction is chosen for what
predicts quality across all three blocks.

The two numbers every one of these models reports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whatever the model was given, a batch is judged on two distances, and they carry the same meaning
in all three studies.

* Hotelling's :math:`T^2` is how far the batch lies **along** the model's components, compared with
  the reference batches. A large value is a batch doing more of what the reference batches did.
* The squared prediction error, SPE, is how far it lies **off** them. A large value is a batch
  doing something the reference batches never did.

Which of the two is large says what kind of departure it is, and that changes what can be done
next. A departure along the components can be extrapolated: in the :ref:`second case study
<APPS_batch_case_sbr_online>` the model forecasts the remainder of such a batch in the right
direction, and more closely the later the forecast is made. A departure off the components can be
flagged, and the tags and samples carrying the residual can be named, but not forecast, because
nothing in the reference set describes where it is going.

`Nomikos and MacGregor (1995)
<https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_
give the charts and the limits for both statistics, and `Nomikos (1996)
<https://literature.learnche.org/item/64/detection-and-diagnosis-of-abnormal-batch-operations-based-on-multi-way-principal-component-analysis>`_
the contribution plots that name the tags behind a large value. How well such a chart
detects a fault of a given size is assessed by `Ramaker and co-workers (2006)
<https://literature.learnche.org/item/164/performance-assessment-and-improvement-of-control-charts-for-statistical-batch-process-monitoring>`_.

Two decisions taken before the model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first is alignment. Unfolding assumes that sample :math:`k` means the same stage of the batch
in every row, so the batches have to be put on one time axis before any of this. Batches that run to different lengths are aligned
within each phase against a maturity variable, a measured quantity that rises steadily through
that phase, as the :ref:`third case study <APPS_batch_case_fmc>` does with the collector level and
the dryer temperature. `González-Martínez, Ferrer and Westerhuis (2011)
<https://literature.learnche.org/item/158/real-time-synchronization-of-batch-trajectories-for-on-line-multivariate-statistical-process-control-using-dynamic-time-warping>`_
set out dynamic time warping, which aligns the raw trajectories instead, and does so for a batch
that is still running.

Alignment discards the durations, so a process where the duration itself carries information keeps
it as a column, which is what the eleventh trajectory of the batch dryer does.

The second decision is which batches count as normal. A monitoring model reports how far a batch
is from its reference set, so that set defines what "unusual" means, and the `rule Nomikos and
MacGregor give for it
<https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_
is that it carries only batches with acceptable operation **and** acceptable product. A
model built to understand what happened rather than to judge a new batch is under no such
constraint, and `Kosanovich, Dahl and Piovoso (1996)
<https://literature.learnche.org/item/156/improved-process-understanding-using-multiway-principal-component-analysis>`_
use one that way. The :ref:`first case study <APPS_batch_case_dupont>` keeps its poor batches in
the model on purpose, to show what the trajectories do and do not separate; the
:ref:`second <APPS_batch_case_sbr_online>` fits its on-line model on the normal batches alone,
because it is judging a running batch against them. Where normal operation is itself moving, as in
a startup or a grade transition, `Duchesne, Kourti and MacGregor (2002)
<https://literature.learnche.org/item/91/multivariate-spc-for-startups-and-grade-transitions>`_
show how the reference set is built.

Beyond monitoring: changing the batch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A model that says which trajectory shape goes with good product can also be read backwards, to ask
what shape to run. `Duchesne and MacGregor (2000)
<https://literature.learnche.org/item/92/multivariate-analysis-and-optimization-of-process-variable-trajectories-for-batch-processes>`_
optimize the trajectories themselves this way, and `Flores-Cerrillo and MacGregor (2004)
<https://literature.learnche.org/item/39/control-of-batch-product-quality-by-trajectory-manipulation-using-latent-variable-models>`_
adjust a running batch to hit a quality target, a mid-course correction, while their
`batch-to-batch paper
<https://literature.learnche.org/item/163/multivariate-monitoring-of-batch-processes-using-batch-to-batch-information>`_
carries information from one batch to the next, for a process that repeats the same recipe. The
:ref:`second case study <APPS_batch_case_sbr_online>` watches a running batch without adjusting
it.

Estimating the scores of a batch observed so far is a
:ref:`missing-data problem <APPS_batch_missing_data>`.
`García-Muñoz, Kourti and MacGregor (2004)
<https://literature.learnche.org/item/157/model-predictive-monitoring-for-batch-processes>`_ carry
that estimate through a running batch and set the limits it is judged against, which is what the
on-line section of the :ref:`second case study <APPS_batch_case_sbr_online>` builds.
`García-Muñoz and co-workers (2003)
<https://literature.learnche.org/item/24/troubleshooting-of-an-industrial-batch-process-using-multivariate-methods>`_
are the source of the batch dryer, and `Wold and co-workers (2009)
<https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_ model the same dryer
with landmark features in place of the raw trajectories.

Two theses carry the derivations and the fuller case studies behind these papers: `Nomikos (1995)
<https://literature.learnche.org/item/154/statistical-process-control-of-batch-processes>`_ for the
charts and their limits, and `García-Muñoz (2004)
<https://literature.learnche.org/item/3/batch-process-improvement-using-latent-variable-methods>`_
for the batch dryer and the score estimate of a running batch.

The columns need not be process tags alone. `Gurden, Westerhuis and Smilde (2002)
<https://literature.learnche.org/item/140/monitoring-of-batch-processes-using-spectroscopy>`_ take
a spectrum at every sample, so each wavelength is a trajectory, and `Kourti, Nomikos and MacGregor
(1995) <https://literature.learnche.org/item/33/analysis-monitoring-and-fault-diagnosis-of-batch-processes-using-multiblock-and-multiway-pls>`_
group the columns into blocks, which is what the :ref:`third case study <APPS_batch_case_fmc>`
builds on.


.. _APPS_batch_readings:

References
~~~~~~~~~~

Foundational multiway PCA / PLS for batches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Paul Nomikos and John F. MacGregor, "`Monitoring batch processes using multiway principal component analysis <https://literature.learnche.org/item/30/monitoring-batch-processes-using-multiway-principal-component-analysis>`_", *AIChE Journal*, **40**, 1361-1375, 1994.

* Paul Nomikos and John F. MacGregor, "`Multi-way partial least squares in monitoring batch processes <https://literature.learnche.org/item/32/multi-way-partial-least-squares-in-monitoring-batch-processes>`_", *Chemometrics and Intelligent Laboratory Systems*, **30**, 97-108, 1995.

* Theodora Kourti, Paul Nomikos and John F. MacGregor, "`Analysis, monitoring and fault diagnosis of batch processes using multiblock and multiway PLS <https://literature.learnche.org/item/33/analysis-monitoring-and-fault-diagnosis-of-batch-processes-using-multiblock-and-multiway-pls>`_", *Journal of Process Control*, **5**, 277-284, 1995.

* Paul Nomikos and John F. MacGregor, "`Multivariate SPC charts for monitoring batch processes <https://literature.learnche.org/item/34/multivariate-spc-charts-for-monitoring-batch-processes>`_", *Technometrics*, **37**, 41-59, 1995.

* Paul Nomikos, "`Detection and diagnosis of abnormal batch operations based on multi-way principal component analysis <https://literature.learnche.org/item/64/detection-and-diagnosis-of-abnormal-batch-operations-based-on-multi-way-principal-component-analysis>`_", *ISA Transactions*, **35**, 259-266, 1996.

* Karlene A. Kosanovich, Kenneth S. Dahl and Michael J. Piovoso, "`Improved process understanding using multiway principal component analysis <https://literature.learnche.org/item/156/improved-process-understanding-using-multiway-principal-component-analysis>`_", *Industrial and Engineering Chemistry Research*, **35**, 138-146, 1996.

* Johan A. Westerhuis, Theodora Kourti and John F. MacGregor, "`Comparing alternative approaches for multivariate statistical analysis of batch process data <https://literature.learnche.org/item/162/comparing-alternative-approaches-for-multivariate-statistical-analysis-of-batch-process-data>`_", *Journal of Chemometrics*, **13**, 397-413, 1999.

* Svante Wold, Nouna Kettaneh-Wold, John F. MacGregor and Kevin G. Dunn, "`Batch process modeling and MSPC <https://literature.learnche.org/item/155/batch-process-modeling-and-mspc>`_", *Comprehensive Chemometrics*, **2**, chapter 2.10, 163-197, 2009.

Control, optimization and product quality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Carl Duchesne and John F. MacGregor, "`Multivariate analysis and optimization of process variable trajectories for batch processes <https://literature.learnche.org/item/92/multivariate-analysis-and-optimization-of-process-variable-trajectories-for-batch-processes>`_", *Chemometrics and Intelligent Laboratory Systems*, **51**, 125-137, 2000.

* Carl Duchesne, Theodora Kourti and John F. MacGregor, "`Multivariate SPC for startups and grade transitions <https://literature.learnche.org/item/91/multivariate-spc-for-startups-and-grade-transitions>`_", *AIChE Journal*, **48**, 2890-2901, 2002.

* Jesus Flores-Cerrillo and John F. MacGregor, "`Control of batch product quality by trajectory manipulation using latent variable models <https://literature.learnche.org/item/39/control-of-batch-product-quality-by-trajectory-manipulation-using-latent-variable-models>`_", *Journal of Process Control*, **14**, 539-553, 2004.

* Jesus Flores-Cerrillo and John F. MacGregor, "`Multivariate monitoring of batch processes using batch-to-batch information <https://literature.learnche.org/item/163/multivariate-monitoring-of-batch-processes-using-batch-to-batch-information>`_", *AIChE Journal*, **50**, 1219-1228, 2004.

* Salvador García-Muñoz, Theodora Kourti, John F. MacGregor, Arthur G. Mateos and Gerald Murphy, "`Troubleshooting of an industrial batch process using multivariate methods <https://literature.learnche.org/item/24/troubleshooting-of-an-industrial-batch-process-using-multivariate-methods>`_", *Industrial and Engineering Chemistry Research*, **42**, 3592-3601, 2003.

* Salvador García-Muñoz, Theodora Kourti and John F. MacGregor, "`Model predictive monitoring for batch processes <https://literature.learnche.org/item/157/model-predictive-monitoring-for-batch-processes>`_", *Industrial and Engineering Chemistry Research*, **43**, 5929-5941, 2004.

Performance, alignment, and spectroscopy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Stephen P. Gurden, Johan A. Westerhuis and Age K. Smilde, "`Monitoring of batch processes using spectroscopy <https://literature.learnche.org/item/140/monitoring-of-batch-processes-using-spectroscopy>`_", *AIChE Journal*, **48**, 2283-2297, 2002.

* Henk-Jan Ramaker, Eric N. M. Van Sprang, Johan A. Westerhuis, Stephen P. Gurden, Age K. Smilde and Frank H. Van Der Meulen, "`Performance assessment and improvement of control charts for statistical batch process monitoring <https://literature.learnche.org/item/164/performance-assessment-and-improvement-of-control-charts-for-statistical-batch-process-monitoring>`_", *Statistica Neerlandica*, **60**, 339-360, 2006.

* José M. González-Martínez, Alberto J. Ferrer and Johan A. Westerhuis, "`Real-time synchronization of batch trajectories for on-line multivariate statistical process control using Dynamic Time Warping <https://literature.learnche.org/item/158/real-time-synchronization-of-batch-trajectories-for-on-line-multivariate-statistical-process-control-using-dynamic-time-warping>`_", *Chemometrics and Intelligent Laboratory Systems*, **105**, 195-206, 2011.

.. _APPS_batch_missing_data:

Missing data and the scores of a batch so far
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A batch that is still running is a row whose later cells are not yet measured. Nomikos and
MacGregor (1995, *Technometrics*, listed above) compared three ways to fill those cells, and
one of them treats them as missing data; the case studies take that route, estimating the
scores from the observed cells alone. The estimators themselves, single-component projection,
projection to the model plane and trimmed score regression, are set out in:

* Philip R. C. Nelson, Paul A. Taylor and John F. MacGregor, "`Missing data methods in PCA and PLS: score calculations with incomplete observations <https://literature.learnche.org/item/68/missing-data-methods-in-pca-and-pls-score-calculations-with-incomplete-observations>`_", *Chemometrics and Intelligent Laboratory Systems*, **35**, 45-65, 1996.

* Francisco Arteaga and Alberto Ferrer, "`Dealing with missing data in MSPC: several methods, different interpretations, some examples <https://literature.learnche.org/item/20/dealing-with-missing-data-in-mspc-several-methods-different-interpretations-some-examples>`_", *Journal of Chemometrics*, **16**, 408-418, 2002.

Theses (McMaster University)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Paul Nomikos, `Statistical process control of batch processes <https://literature.learnche.org/item/154/statistical-process-control-of-batch-processes>`_, Ph.D thesis, 1995.

* Christiane M. Jaeckle, `Product and process improvement using latent variable methods <https://literature.learnche.org/item/167/product-and-process-improvement-using-latent-variable-methods>`_, Ph.D thesis, 1998.

* Jesus Flores-Cerrillo, `Quality control for batch processes using multivariate latent variable methods <https://literature.learnche.org/item/51/quality-control-for-batch-processes-using-multivariate-latent-variable-methods>`_, Ph.D thesis, 2003.

* Salvador García-Muñoz, `Batch process improvement using latent variable methods <https://literature.learnche.org/item/3/batch-process-improvement-using-latent-variable-methods>`_, Ph.D thesis, 2004.

* Cecilia Pereira Rodrigues, `Industrial batch data analysis using latent variable methods <https://literature.learnche.org/item/161/industrial-batch-data-analysis-using-latent-variable-methods>`_, Masters thesis, 2006.
