.. _APPS_product_development:

Product development and product improvement
===========================================

.. index::
	single: product development
	single: product improvement
	pair: product development; product improvement

This section covers product development, but it is more correctly called product improvement.
The reason is that new products are seldom developed completely from scratch; products are regularly improved. The following usage examples show:

Usage examples
~~~~~~~~~~~~~~~

.. index::
	pair: usage examples; product development

-	*Colleague*: Our most high profile customer wants us to develop a product with similar, but different specifications to the prior products we have made. Is it feasible to say '*yes*' to them?

-   *You*: we have an existing product, but a customer just wants to change one of the 7 specifications: they want a slightly higher *viscosity*. Keep the ingredients and ratios the same, but which process setting(s) do we change?

-   *Manager*: Keep the specifications the same, but adjust the process to use less energy and reduce emissions, even if we use slightly more expensive materials, with different ratios. Is this possible?

-   *Engineer*: A constraint has changed (e.g. a new government regulation, we have to use a different piece of equipment): how can we still get the same final product by adjusting the process conditions, or materials used in the process?

-	*Financial controller*: We can buy the raw ingredient from 4 different suppliers. Which suppliers do we pick to most cost-effectively make the product, but still achieve the specifications?

-   *Engineer 2*: Our current top line product is made with 6 different ingredients. Can we reduce this number down by adjusting the ratios or the choices of ingredients?

As these examples show: "product development" actually happens far more frequently than simply the case of a customer coming to ask for *different, entirely new, specifications* to those you currently have in your portfolio or product catalogue. The opposite case of changing these 3 things, in order to keep the *same specifications* is far more common:

    * which ingredients (raw materials) do you use?
    * which ingredient ratios, specified by mass fraction, do you use?
    * which conditions do you implement to get the final product?

Both cases of creating an entirely new product, or improving an existing product can be considered with the methods described here.

The end goal is "faster development of personalized products and customer-centric development", using the information and databases we have accumulated over the many years of experience with the process.

Product design uses every chapter of this book
================================================

.. index::
	pair: five uses of data; product development
	pair: extracting value from data; product development

The :ref:`introduction to latent variable methods <LVM_extracting_value_from_data>` listed the five main areas where engineers extract value from process data:

#.	**Improved process understanding** --- confirming what we know, and seeing the unexpected, often by inspecting :ref:`score and loading plots <LVM_interpreting_scores>`.

#.	**Troubleshooting process problems** --- isolating which variables drove a deviation, using the multivariate :ref:`troubleshooting tools <LVM_troubleshooting>`.

#.	**Improving, optimizing and controlling processes** --- moving the operating point on purpose, using :ref:`designed experiments <SECTION-design-analysis-experiments>` and :ref:`response surface methods <DOE-RSM>`.

#.	**Predictive modelling** --- estimating a hard-to-measure quantity from the easy-to-measure ones, either with :ref:`least-squares models <SECTION-least-squares-modelling>` or with :ref:`inferential sensors <LVM_inferential_sensors>` built on PLS.

#.	**Process monitoring** --- raising an alarm when the process drifts away from where it should be, with :ref:`univariate charts <SECTION-process-monitoring>` or :ref:`multivariate ones <LVM_monitoring>`.

Product design and improvement is not a sixth area. It is what happens when we do all five at once, on the same data set, in the same iteration. Each Design-Build-Test-Learn cycle (introduced below) draws on every one of them:

	*	We start each campaign with a round of **process understanding** on the historical :math:`(\mathbf{F}, \mathbf{Z}, \mathbf{Y})` data: which materials, ratios and conditions drove the past quality outcomes? The score and loading plots of a :ref:`PCA <SECTION_PCA>` or :ref:`PLS <SECTION_PLS>` model on these matrices answer that question directly.

	*	Each new experiment that misses the target is an act of **troubleshooting**: the same multivariate contribution plots that diagnose a process upset tell us which input is responsible for a missed quality target.

	*	The **improvement and optimization** step is what proposes the next recipe and conditions to try. Sometimes this is a :ref:`response-surface optimization <DOE-RSM>` on top of a designed experiment; sometimes it is :ref:`mixture-design <DOE-mixture-designs>` reasoning on the ratios; often it is the inverse of a PLS model, with :ref:`constraints <DOE-handling-constraints>` from the operating window.

	*	**Predictive models** are how slow or expensive measurements --- a taste panel, a 30-day shelf-life test, a customer trial --- are estimated from quick lab data so the cycle does not stall waiting for the slowest test.

	*	**Monitoring** in the latent-variable space tells us whether a proposed recipe is still inside the region where the historical model can be trusted, or whether the optimizer has pushed us into an extrapolated region where the predictions are not reliable.

The chapter therefore does not introduce many new techniques: it shows how to assemble the methods you already know into a single workflow that designs and improves products.

Why product development is difficult
=====================================

.. index::
	pair: Design-Build-Test-Learn cycle; product development
	single: DBTL cycle

Most product development is still done by intuition and trial-and-error. The methods of optimization and mathematical modelling in this chapter can speed that work up considerably, and in some settings can even automate it. But before getting to the methods, it is worth being honest about why the problem is difficult: there are several places where things can go wrong, and a tool that does not address them will not improve on a good engineer's intuition.

We frame each iteration as a Design-Build-Test-Learn (DBTL) cycle, a framing widely used in the biotechnology and autonomous-experimentation literature:

	* **Design**: pick the values for the three groups of degrees of freedom (ingredients, ratios, conditions).
	* **Build**: run one or more experiments with that design.
	* **Test**: measure the outcomes on the resulting product.
	* **Learn**: compare the outcomes against the targets, update the model, decide on the next iteration.

We do not get the product right on the first cycle, so we iterate. Even when you work "by eye" from plots, you are using an implicit model of the system; the methods in this chapter make that model explicit so it can be reused, criticized and improved. Six broad areas of difficulty appear in almost every product-development problem.

Problems with the specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	*	The targets are usually correlated. As one increases, so does another. A specification that treats them as independent (or constrains one and lets the other float) ignores this structure and will mislead the optimization.

	*	Specifications are often asymmetric. A weight of "ideally above 4 g" is a soft target, while "must not exceed 7 g" is a hard limit. Casting both into a single objective requires care, often using a smoothed indicator such as a sigmoid or `Gompertz function <https://en.wikipedia.org/wiki/Gompertz_function>`_.

	*	Each DBTL cycle is solved as an optimization, so we have to capture several targets in a single objective. Sum of squared deviations? Absolute deviations? Equal weights, or a ranking? And how do we scale a target measured in 1000s so it does not swamp one measured in 0.01s?

	*	Profit is often suggested as the objective, but reliable estimates of selling price, raw-material costs, emissions, labour and rework costs are rarely all available at the same time.

	*	Closeness to a lab-scale specification is not the same as robustness in production or in the customer's hands. An optimum found in the lab can perform poorly at full scale.

Problems in the Design step
~~~~~~~~~~~~~~~~~~~~~~~~~~~

	*	The first iteration has little or no data, so the search direction has to come from prior knowledge or :ref:`screening designs <DOE-saturated-screening-designs>`.

	*	When experiments can run in parallel (e.g. on a robotic platform), how many points, where in the input space, and with how many replicates?

	*	Step size matters. Moving from :math:`x = 0.5` to :math:`x = 0.499` is wasteful; moving to :math:`x = 0.2` may be too far. The right step balances information against cost, and we would like that choice to be automatic in a self-driving DBTL loop.

	*	Bringing in new candidate ingredients is a combinatorial problem. With 100 candidate plastics it helps to rank them on a continuous scale (e.g. thermal stability) so the choice becomes a numeric variable rather than a 100-way switch.

	*	On/off effects: the mere presence of an ingredient at small amounts can flip the system's behaviour, creating strong nonlinearities that are hard to model.

	*	Process conditions are sometimes discrete (stirrer at off / low / high), and the order of manufacturing steps matters.

	*	Model inversion is non-unique. Solving :math:`x + y = 4` has infinitely many solutions, and product design almost always has more inputs (manipulated variables) than outputs (targets), so the inverse problem is underdetermined.

Problems in the Build step
~~~~~~~~~~~~~~~~~~~~~~~~~~

	*	How repeatable can you run the same recipe? Without good control here an apparent improvement may just be experimental noise, and a move to a new operating region cannot be distinguished from drift.

	*	Even when a recipe is reproduced perfectly, there are :ref:`block effects <DOE_blocking_section>` between iterations. Including references and controls in each cycle lets us correct for these.

	*	Is the lab system a faithful proxy for how the customer actually uses the product? A product that is robust on the bench and fails in customer hands has not really been improved.

Problems in the Test step
~~~~~~~~~~~~~~~~~~~~~~~~~

	*	Measurement reproducibility. Outputs sometimes shift between iterations because of uncontrolled factors. We would like to eliminate those factors, or at least correct for them.

	*	Outputs interact. Viscosity readings depend on pH, for example, so the test result is itself a function of more than one quality.

	*	Sensory and slow lab measurements cannot be done on every experiment. A taste panel, or a 5-day shelf-life test, will not keep up with a fast iteration loop. :ref:`Inferential sensors <LVM_inferential_sensors>` and other surrogate measurements speed up the cycle, but they introduce their own error.

Problems in the Learn step
~~~~~~~~~~~~~~~~~~~~~~~~~~

	*	Which way do we go next: explore an unexamined region, or exploit the neighbourhood of the current best result? And how should the balance shift as we accumulate cycles?

	*	Which model family should we use for the forward (inputs to outputs) prediction: Gaussian processes, polynomial response surfaces, splines, latent variable models? Which can be inverted analytically, and which require an optimization to invert?

	*	When do we drop old data; when is a surprising point an :ref:`outlier <LS-studentized-residuals>` and not the next ah-ha result; and how do we use the model's predictive uncertainty to decide where to sample next?

Problems with the cycle itself
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	*	When do we stop? The obvious case is when the goal is reached, but we also need to detect diminishing returns, and to recognize when no feasible solution exists.

	*	An optimum sits in a nonlinear region by definition. How do we know we have found the global peak rather than a local one?

	*	Storage and provenance. How do we name experiments, record ratios and units, and capture covariates (ambient humidity, operator, lot numbers, raw-material amounts that were "constant") that we did not think mattered until the day they did? Model versioning, input-data lineage and a clear audit trail are part of this discipline.

The remainder of this chapter describes how the methods already developed in the book --- :ref:`designed experiments <SECTION-design-analysis-experiments>`, :ref:`response surface methods <DOE-RSM>` and :ref:`latent variable models <SECTION_latent_variable_modelling>`, together with standard and Bayesian optimization --- address most of these issues.

Scope of the problem
=====================

Before working through any specific method, it helps to lay out what an ideal framework for data-driven product development should look like. The fifteen features below are the design goals we hold the methods later in this chapter against. None of them is unique to a particular algorithm; together they tell us which combinations of methods are worth assembling.

.. index::
	pair: subject matter expert; product development
	single: multi-objective optimization
	single: key performance indicator

A. The tool is **guided by the subject matter expert** (SME) to accelerate the process; it is not intended to replace them. It will allow them to more rapidly prototype and test alternatives, and guide them. The expert also plays an active role: for example, constraints can be specified by the expert and the tool can help them understand the tradeoffs by providing alternative solutions that they select from.

B. It is **multi-objective**. Multiple goals and targets can be taken along, each with different weights and prioritization if needed. For example, if a certain target objective is poorly explained by the data, then it can be down weighted, but not ignored. We should not have to build models for each outcome variable: we must be able to handle multiple key performance indicators (KPIs), even highly correlated ones and also high-dimensional ones (such as vectors).

C. We must be able to **handle missing data**. Our knowledge regarding physical and chemical properties of the materials is incomplete; we might only have partial results, or loss of data might have occurred. We might have results from earlier experiments, while later experiments may have extra or more sophisticated measurements. In all of these cases we should use the data we have available, and not have to discard rows or columns of incomplete knowledge. (:ref:`PCA <SECTION_PCA>` and :ref:`PLS <SECTION_PLS>` models tolerate missing values natively.)

D. It should **not be dependent on the specific training dataset** and therefore unable to generalize to new ingredients, other properties, new experiments or other conditions used to create the product. Another way of saying this is that it should not be `transductive <https://en.wikipedia.org/wiki/Transduction_(machine_learning)>`_, but rather inductive.

E. It should be able to handle **small data**, particularly small sets of experimentally acquired data that iteratively and sequentially become available. We should not need large amounts of data to get good results as long as we have well-designed experimental data which is strategically chosen to give the most information.

F. It should however be able to handle **large data**. If we do have large quantities of data, then it should be able to handle these as well.

G. It must allow for **learning and interpretation** by the expert. The model results should be understandable, confirm prior knowledge, and generate new insights not yet known to the experts.

H. It should be able to handle **high-dimensional data**, even if many of the measured data are affected by random noise, or are unrelated to the problem. As we will not always know upfront what is important, if we do happen to add more information in our models, then we should not be penalized. It is acceptable to learn iteratively that certain data are uninteresting. (This is one of the central reasons we lean on :ref:`latent variable methods <SECTION_latent_variable_modelling>` later in the chapter.) See the prior point.

.. index::
	single: explore-exploit tradeoff
	single: operating window
	single: transfer learning

I. It should provide guidance to **fill in the spaces of unknown knowledge**. It is therefore both sequential and active. The expert can influence where future experiments should be done, to help expand the model's predictive power, or the model actively indicates the regions where experimental input is needed (the standard explore-and-exploit tradeoff).

J. An **operating window** for the solution is provided. When constraints are active at a solution, these should be reported, to learn the limits of the system. Conversely, inactive constraints are also insightful, since these provide an operating window within which we can move without changing the optimization result too much. Even better is if a parameterized solution is presented, allowing the user to fine-tune the solution based on tuneable parameters.

K. The method should enable **transfer learning** across different manufacturing sites, lines, or even different products. For example, a new product can be developed on site A, and then transferred to site B, using data from both sites, to learn the transferable knowledge, and ignore the regions of operation which have no impact.

L. Different conditions must be handled. Extending an existing product from one matrix to another (e.g. from a liquid to a gel) or when used at different settings (e.g. high or low temperature, pH etc) it will alter the outcomes. So modelling to predict and handle these cases is desirable.

M. It is **permutation invariant**. The order in which we acquire experimental data or present the data to our models should not alter the outcomes we achieve.

N. **Handling different scales** should also be accommodated; cheap experiments at a smaller scale being combined with sparse data at a larger scale (e.g. customer trials).

.. index::
	single: model inversion
	pair: model inversion; product development
	see: inverse approach; model inversion

O. Allow for **model inversion**: we do not only want to predict an outcome from upstream information, but also to use the inverse approach: to predict upstream settings for a given set of performance outcomes. This inverse approach is in many cases non-unique: there are multiple upstream settings that can give the same performance outcome. The system should indicate when multiple solutions are possible (the rank of the input space exceeds the output space) and as such there are directions in input space which are unrelated to the output, giving us extra degrees of freedom.

These are ambitious goals. Let us explore how we can achieve most of these in the next sections.

Important concepts
===================

What are the "Degrees of freedom"?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: degrees of freedom; in product development

As just mentioned, there are 3 groups of things you can change:

1. **Select your ingredients**. This is a discrete choice: either you use an ingredient or raw materials, or you do not. It is a yes/no selection. You might have a whole catalogue, or database, of materials that you can select from. In many of the cases described in the "Usage examples" above this degree of freedom is actually fixed. In other words, you cannot change the ingredient choice and you must keep using what you already use. This is often due to regulations, or the fact that introducing new ingredients will be too expensive to test and validate and might lead to unexpected side-reactions or interactions.

2. **Adjust the ratios of the ingredients**. This is a sliding parameter: for example you can go from 45% weight fraction of material A, to 41% weight fraction, but remember by using less material A, the weight fractions of other materials change. The total weight fractions always add up to 1.0, so there is a constraint in the system, and adjusting one material will force the other material ratio to also be adjusted. This sum-to-one structure is exactly what :ref:`mixture designs <DOE-mixture-designs>` are built to handle.

3. **Use different process conditions**. This group is where often you have the most degrees of freedom. You can adjust process settings used to make the product quite easily, such as temperature, pH, duration of certain steps, and order in which you add ingredients and complete the manufacturing steps. Because of the diversity of the options here, you might need to spend quite some time thinking about the process, and seeing what freedom you practically and economically have. Like the prior group, the ratios, this group of degrees of freedom also has some correlations in the historical data. For example, you might not be able to independently increase temperature in the process, without adjusting flow rate.


The "desired outcome"
~~~~~~~~~~~~~~~~~~~~~~

This is a specification of what you want to achieve. Your end goal. It is often given as a vector of one or more specifications. For example: you might need to achieve a given viscosity, melting point and product density. These 3 numbers jointly define the expectations.

.. index::
	single: sigmoid function
	single: Gompertz function

Some entries in the desired outcome vector might simply be given as constraints. For example, an *elongation* value of 15 or lower is acceptable, or a *shelf-life* of 30 days or greater is acceptable. This is more of a yes/no constraint: it is either met, or it is not. It creates a discontinuity in our system when we specify it as an equation later on. Discontinuities are often undesirable from a mathematical modelling and optimization perspective. However these can be dealt with by converting them to a smoothed version, such as by using a sigmoid function or a `Gompertz function <https://en.wikipedia.org/wiki/Gompertz_function>`_.

Finally, sometimes the desired outcome is a very large vector, such as time series showing the change of the product, such as elongation in a controlled experiments, or a pH over time. It can also be a spectrum, such as an NIR spectrum. The number of entries in this long vector are highly correlated. So the first step in such a situation is to use a :ref:`principal component model <SECTION_PCA>` and understand the true lower dimensional space that the output space has. Then these, far smaller number of components, are used as a specification. Therefore the methods of product design are applicable in this case too.

Data needed for product development
====================================

.. index::
	pair: data organization; product development
	single: D matrix; product development
	single: F matrix; product development
	single: Z matrix; product development
	single: Y matrix; product development

The methods later in this chapter operate on four data tables that fit together. We refer to them by capital letters: :math:`\mathbf{D}`, :math:`\mathbf{F}`, :math:`\mathbf{Z}` and :math:`\mathbf{Y}`. Each table answers a different question and each one normally comes from a different source. Setting them up correctly --- and getting the alignment between them right --- is most of what makes the rest of the workflow possible.

* :math:`\mathbf{D}`: a property database, one column per candidate building block, one row per measured property.
* :math:`\mathbf{F}`: a recipe table, one row per experiment, columns aligned with :math:`\mathbf{D}`, entries are mass fractions that sum to 1.
* :math:`\mathbf{Z}`: a process-conditions table, one row per experiment, columns are the conditions used to make that row's product.
* :math:`\mathbf{Y}`: a quality-outcomes table, one row per experiment, columns are the KPIs that the customer (or our specification) cares about.

The matrix :math:`\mathbf{D}` shares columns with :math:`\mathbf{F}`. The matrices :math:`\mathbf{F}`, :math:`\mathbf{Z}` and :math:`\mathbf{Y}` share rows: row :math:`i` of each describes the same experiment.

The property database :math:`\mathbf{D}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the most heterogeneous of the four. Each column of :math:`\mathbf{D}` is a candidate building block --- an oil, a fat, a binder, a filler, a polymer --- and the rows are properties: molecular weight, melting point, viscosity at a given shear rate, surface tension, NIR absorbance at each wavelength, and so on. Some practitioners prefer the transposed layout (one material per row, properties as columns); either is fine, as long as you stay consistent.

:math:`\mathbf{D}` is assembled from internal lab measurements, supplier data sheets, public databases, and computational property estimators. It is worth investing in: a well-populated :math:`\mathbf{D}` is reused across many product-development campaigns. Collect more rows and more columns than you strictly need for the current project.

A few practical points:

	*	**Do not break "compound" ingredients into their pure constituents.** If you use *milk* as an ingredient, store the properties of milk; do not try to split it into water, fat, protein and lactose. The same goes for any pre-mix or proprietary blend. The columns of :math:`\mathbf{D}` should match the units in which you actually purchase, weigh and add the materials --- the same units that appear in :math:`\mathbf{F}`.

	*	**Properties are usually blocked.** Some rows are only meaningful for solids, others only for liquids, others only for spectroscopic samples. The methods in this chapter handle missing values explicitly, as long as you mark them as missing rather than filling with zeros.

	*	**The result must not depend on the order of rows or columns.** We may *group* rows --- for example, all NIR wavelengths together --- so that block-wise preprocessing is possible, but inside a group the order is arbitrary. This is one of the desiderata (item M) in the previous section.

	*	**Vector-valued properties belong in :math:`\mathbf{D}`** as consecutive rows: a particle-size distribution, a thermogravimetric trace, an NIR spectrum. Such blocks are highly correlated and are a natural fit for a :ref:`principal component model <SECTION_PCA>`.

The recipe :math:`\mathbf{F}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each row of :math:`\mathbf{F}` is one experiment or one product, and each column is a building block, aligned with the columns of :math:`\mathbf{D}`. The entries in a row are mass fractions and typically sum to 1.

The rows in :math:`\mathbf{F}` need not be products that you sell. Intermediate blends, side experiments and customer trials all belong, as long as each row has a corresponding outcome in :math:`\mathbf{Y}`. It is also useful to split :math:`\mathbf{F}` into sub-blocks --- a binders block, a fats block, a starches block --- so that the model can later assess the effect of each material family separately.

The process conditions :math:`\mathbf{Z}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The matrix :math:`\mathbf{Z}` has the same number of rows as :math:`\mathbf{F}` and one column per process condition: temperature, pressure, mixing speed, residence time, addition order. Discrete settings (a stirrer that is off, low or high) are :ref:`one-hot encoded <LVM-using-indicator-variables>`. Recipe steps that may or may not be applied are stored as 0/1 indicators.

It is tempting to leave :math:`\mathbf{Z}` out when only the recipe varies during a campaign. Resist that temptation. Conditions that look constant in a campaign --- ambient humidity, operator, raw-material lot number, the calibration date of the analyser --- routinely turn out, after the fact, to have driven a result. If they were never recorded, that diagnosis is impossible. (When such effects *are* expected and we want to remove them by design, we can plan the campaign with :ref:`blocking <DOE_blocking_section>`.) The correct rule is: store the suspected covariates as well as the obvious controlled variables, even if you do not plan to vary them.

The quality outcomes :math:`\mathbf{Y}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each row of :math:`\mathbf{Y}` is the same experiment as the corresponding row of :math:`\mathbf{F}` and :math:`\mathbf{Z}`. The columns are the key performance indicators (KPIs): viscosity, melting point, shelf life, taste-panel score, and so on. Vector outcomes (such as a release-rate curve) can also be stored in :math:`\mathbf{Y}` as consecutive columns; if they are highly correlated, summarize them with a few principal components first.

The crucial design rule for :math:`\mathbf{Y}` is to capture, at minimum, the same metrics the customer specifies. The whole point of the methodology is to invert the relationship :math:`(\mathbf{D}, \mathbf{F}, \mathbf{Z}) \rightarrow \mathbf{Y}` so that, given a target row :math:`\mathbf{y}_\text{new}`, we can prescribe the recipe and conditions :math:`(\mathbf{f}_\text{new}, \mathbf{z}_\text{new})` that achieve it. If the customer's target metrics are not among the columns of :math:`\mathbf{Y}`, the inversion is solving the wrong problem.

As with :math:`\mathbf{D}`, capture provenance for every entry: who measured the value, where, when, in which units, and with which protocol. Two viscosity numbers measured with different geometries are not the same measurement.

How the four tables fit together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	*	:math:`\mathbf{D}` and :math:`\mathbf{F}` share columns. Every ingredient appearing in any recipe must have a property column in :math:`\mathbf{D}`. A new, unseen ingredient can later be added to :math:`\mathbf{D}` and then used in :math:`\mathbf{F}`, provided its properties lie within the correlation structure of the existing materials.

	*	:math:`\mathbf{F}`, :math:`\mathbf{Z}` and :math:`\mathbf{Y}` share rows. Row :math:`i` of each describes the same experiment, so they can be concatenated horizontally for a multi-block :ref:`PLS <SECTION_PLS>` analysis. Standard :ref:`preprocessing <LVM_preprocessing>` (mean-centring, scaling, optional block scaling) applies before the model is built.

	*	The forward model :math:`(\mathbf{F}, \mathbf{Z}) \rightarrow \mathbf{Y}` is augmented by the property information in :math:`\mathbf{D}`, so that the model is expressed in terms of *what the materials do* (their physical and chemical properties), not just *which materials were chosen*. This is what allows the model to generalize to new ingredients --- the inductive property (item D) of the desiderata.

	*	Inversion of this model is generally underdetermined: there are typically more inputs than outputs, so a target :math:`\mathbf{y}_\text{new}` corresponds to a *region* of feasible :math:`(\mathbf{f}_\text{new}, \mathbf{z}_\text{new})` rather than a single point. The dimension of that region is the difference between the rank of the input space and the rank of the output space (the "rank" idea in the previous subsection); the inactive directions are the operating window described by item J of the desiderata.

References
~~~~~~~~~~

The four-table organization is drawn from a sequence of papers, several of whose authors I have had the pleasure of working with over the past 25 years:

	*	S. Garcia-Munoz, "Two Novel Methods to Analyze the Combined Effect of Multiple Raw-Materials and Processing Conditions on the Product's Final Attributes: JRPLS and TPLS." *Chemometrics and Intelligent Laboratory Systems*, **133**, 2014, https://doi.org/10.1016/j.chemolab.2014.02.006

	*	K. Muteki, J. F. MacGregor, and T. Ueda. "Mixture Designs and Models for the Simultaneous Selection of Ingredients and Their Ratios." *Chemometrics and Intelligent Laboratory Systems*, **86**, 2007, https://doi.org/10.1016/j.chemolab.2006.08.003

	*	C. M. Jaeckle and J. F. MacGregor. "Product Design through Multivariate Statistical Analysis of Process Data." *AIChE Journal*, **44**, 1998, https://doi.org/10.1002/aic.690440509

	*	E. Tomba, M. Barolo, and S. García-Muñoz. "General Framework for Latent Variable Model Inversion for the Design and Manufacturing of New Products." *Industrial & Engineering Chemistry Research*, **51**, 2012, https://doi.org/10.1021/ie301214c


