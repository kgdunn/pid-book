.. _APPS_product_development:

Product development and product improvement
===========================================

.. index::
	single: product development
	single: product improvement
	pair: product development; product improvement

Most "product development" is really product improvement: new products are seldom developed from scratch. The usage examples below show what this looks like in practice, and they motivate the rest of the chapter.

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

As these examples show, the common case is not a request for entirely new specifications, but a change to one of three things while the specifications stay the same:

    * which ingredients (raw materials) we use,
    * the ratios in which we combine them, by mass fraction, and
    * the process conditions used to make the product.

The methods in this chapter handle both situations --- a wholly new product and the adaptation of an existing one --- because the underlying problem is the same: pick values for those three groups of variables that produce the desired outcomes, using whatever historical data we have to guide the choice.

The three degrees of freedom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: degrees of freedom; in product development

The usage examples above already named the three things we can change. Each Design step in a product-development cycle is a choice over these three groups, and the rest of the chapter keeps coming back to them, so it is worth pinning the vocabulary down explicitly.

1.	**Select the ingredients.** This is a discrete choice: either an ingredient is in the recipe, or it is not. The candidate set is usually a catalogue or database of materials. In many of the usage examples above this degree of freedom is actually fixed --- regulatory constraints, validation cost, or the risk of unexpected side-reactions mean we have to keep using what we already use.

2.	**Adjust the ratios of the ingredients.** This is a continuous choice constrained to a simplex: the mass fractions sum to 1, so reducing one ingredient forces another to increase. This sum-to-one structure is exactly what :ref:`mixture designs <DOE-mixture-designs>` are built to handle.

3.	**Choose the process conditions.** Temperature, pH, residence time, addition order, and the on/off state of optional steps. This is usually where the most degrees of freedom live, and where the historical data has the most correlation: temperature and flow rate, for example, are rarely independent in the historical record even when they are independent on paper.

Specifying the desired outcome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The desired outcome is the end goal: a vector of one or more specifications. A simple case is three scalars --- a viscosity, a melting point, a density --- that jointly define what "good" means.

.. index::
	single: sigmoid function
	single: Gompertz function

Some entries are inequalities rather than targets: an *elongation* of 15 or lower is acceptable, a *shelf-life* of 30 days or greater is acceptable. These are yes/no constraints, and they introduce a discontinuity into the objective. Discontinuities are awkward for the optimizers later in the chapter, so we replace each one with a smoothed indicator --- a sigmoid or a `Gompertz function <https://en.wikipedia.org/wiki/Gompertz_function>`_ --- that approximates the cliff but stays differentiable.

The desired outcome is sometimes a very long vector: a release-rate curve, a pH trajectory, an NIR spectrum. The entries in such a vector are heavily correlated, so we do not work with them directly. The first step is a :ref:`principal component model <SECTION_PCA>` of the output space; the few scores that explain it become the specification, and the rest of the methodology proceeds unchanged.

Product design uses every chapter of this book
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	pair: Design-Build-Test-Learn cycle; product development
	single: DBTL cycle

Most product development is still done by intuition and trial-and-error. The methods later in this chapter can speed that work up considerably, but only if they address the things that make the problem difficult in the first place. The challenges below appear in almost every campaign, and a tool that ignores them will not improve on a good engineer's intuition.

We frame each iteration as a Design-Build-Test-Learn (DBTL) cycle, a framing widely used in the biotechnology and autonomous-experimentation literature:

	* **Design**: pick the values for the three groups of degrees of freedom (ingredients, ratios, conditions).
	* **Build**: run one or more experiments with that design.
	* **Test**: measure the outcomes on the resulting product.
	* **Learn**: compare the outcomes against the targets, update the model, decide on the next iteration.

We do not get the product right on the first cycle, so we iterate. Even when you work by eye from plots you are running an implicit model of the system; the methods in this chapter make that model explicit, so it can be reused, criticized and improved. Six broad areas of difficulty recur --- one for each stage of the cycle, plus a cross-cutting set that affects the iteration as a whole.

Problems with the specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	*	The targets are usually correlated. As one increases, so does another. A specification that treats them as independent (or constrains one and lets the other float) ignores this structure and will mislead the optimization.

	*	Specifications are often asymmetric. A weight of "ideally above 4 g" is a soft target, while "must not exceed 7 g" is a hard limit. Casting both into a single objective requires care, often using a smoothed indicator such as a sigmoid or `Gompertz function <https://en.wikipedia.org/wiki/Gompertz_function>`_.

	*	Each DBTL cycle is solved as an optimization, so we have to capture several targets in a single objective. Sum of squared deviations? Absolute deviations? Equal weights, or a ranking? And how do we scale a target measured in 1000s so it does not swamp one measured in 0.01s?

	*	Profit is often suggested as the objective, but reliable estimates of selling price, raw-material costs, emissions, labour and rework costs are rarely all available at the same time.

	*	Closeness to a lab-scale specification is not the same as robustness in production or in the customer's hands. An optimum found in the lab can perform poorly at full scale.

.. index::
	single: model inversion
	pair: model inversion; product development
	see: inverse approach; model inversion

Problems in the Design step
^^^^^^^^^^^^^^^^^^^^^^^^^^^

	*	The first iteration has little or no data, so the search direction has to come from prior knowledge or :ref:`screening designs <DOE-saturated-screening-designs>`.

	*	When experiments can run in parallel (e.g. on a robotic platform), how many points, where in the input space, and with how many replicates?

	*	Step size matters. Moving from :math:`x = 0.5` to :math:`x = 0.499` is wasteful; moving to :math:`x = 0.2` may be too far. The right step balances information against cost, and we would like that choice to be automatic in a self-driving DBTL loop.

	*	Bringing in new candidate ingredients is a combinatorial problem. With 100 candidate plastics it helps to rank them on a continuous scale (e.g. thermal stability) so the choice becomes a numeric variable rather than a 100-way switch.

	*	On/off effects: the mere presence of an ingredient at small amounts can flip the system's behaviour, creating strong nonlinearities that are hard to model.

	*	Process conditions are sometimes discrete (stirrer at off / low / high), and the order of manufacturing steps matters.

	*	Model inversion is non-unique. Solving :math:`x + y = 4` has infinitely many solutions, and product design almost always has more inputs (manipulated variables) than outputs (targets), so the inverse problem is underdetermined.

Problems in the Build step
^^^^^^^^^^^^^^^^^^^^^^^^^^

	*	How repeatable can you run the same recipe? Without good control here an apparent improvement may just be experimental noise, and a move to a new operating region cannot be distinguished from drift.

	*	Even when a recipe is reproduced perfectly, there are :ref:`block effects <DOE_blocking_section>` between iterations. Including references and controls in each cycle lets us correct for these.

	*	Is the lab system a faithful proxy for how the customer actually uses the product? A product that is robust on the bench and fails in customer hands has not really been improved.

Problems in the Test step
^^^^^^^^^^^^^^^^^^^^^^^^^

	*	Measurement reproducibility. Outputs sometimes shift between iterations because of uncontrolled factors. We would like to eliminate those factors, or at least correct for them.

	*	Outputs interact. Viscosity readings depend on pH, for example, so the test result is itself a function of more than one quality.

	*	Sensory and slow lab measurements cannot be done on every experiment. A taste panel, or a 5-day shelf-life test, will not keep up with a fast iteration loop. :ref:`Inferential sensors <LVM_inferential_sensors>` and other surrogate measurements speed up the cycle, but they introduce their own error.

Problems in the Learn step
^^^^^^^^^^^^^^^^^^^^^^^^^^

	*	Which way do we go next: explore an unexamined region, or exploit the neighbourhood of the current best result? And how should the balance shift as we accumulate cycles?

	*	Which model family should we use for the forward (inputs to outputs) prediction: Gaussian processes, polynomial response surfaces, splines, latent variable models? Which can be inverted analytically, and which require an optimization to invert?

	*	When do we drop old data; when is a surprising point an :ref:`outlier <LS-studentized-residuals>` and not the next ah-ha result; and how do we use the model's predictive uncertainty to decide where to sample next?

Problems with the cycle itself
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	*	When do we stop? The obvious case is when the goal is reached, but we also need to detect diminishing returns, and to recognize when no feasible solution exists.

	*	An optimum sits in a nonlinear region by definition. How do we know we have found the global peak rather than a local one?

	*	Storage and provenance. How do we name experiments, record ratios and units, and capture covariates (ambient humidity, operator, lot numbers, raw-material amounts that were "constant") that we did not think mattered until the day they did? Model versioning, input-data lineage and a clear audit trail are part of this discipline.

What we ask of an ideal framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
	pair: subject matter expert; product development
	single: multi-objective optimization
	single: key performance indicator
	single: operating window
	single: explore-exploit tradeoff

The difficulties above tell us what an ideal framework needs to do. Most of those properties --- handling correlated and high-dimensional outputs, tolerating missing data, working from small experimental sets, balancing exploration against exploitation, supporting model inversion --- are addressed directly by the methods later in this chapter and the cross-references above. Four further properties cut across the whole cycle and are worth stating explicitly:

	*	**Guided by the subject matter expert.** The tool accelerates the expert; it does not replace them. The SME specifies constraints, vetoes infeasible suggestions, and chooses between alternative solutions when the inversion is non-unique.

	*	**Inductive, not transductive.** The model must generalize to new ingredients, conditions and properties --- not just interpolate within the training set. This is why we represent the recipe through a property database (the :math:`\mathbf{D}` matrix in the next section), rather than as a categorical choice between named materials. See the `transduction <https://en.wikipedia.org/wiki/Transduction_(machine_learning)>`_ entry for the contrast with the inductive case.

	*	**Interpretable.** The results must be understandable to the expert: they should confirm prior knowledge where it exists, and surface new insight where it does not. Score and loading plots from :ref:`PCA <SECTION_PCA>` and :ref:`PLS <SECTION_PLS>` are the workhorses here, which is one reason we lean on :ref:`latent variable methods <SECTION_latent_variable_modelling>` for the rest of the chapter.

	*	**Reports an operating window.** When constraints are active at a solution, the framework names them, so we learn the limits of the system. When constraints are inactive, the directions in which we can move without losing the solution are reported as an :index:`operating window <single: operating window>`, and ideally the solution is parameterised so the SME can fine-tune within that window. Multivariate :ref:`troubleshooting tools <LVM_troubleshooting>` give us the same diagnostic in the latent-variable space.

The remainder of this chapter shows how the methods already developed in the book --- :ref:`designed experiments <SECTION-design-analysis-experiments>`, :ref:`response surface methods <DOE-RSM>` and :ref:`latent variable models <SECTION_latent_variable_modelling>`, together with standard and Bayesian optimization --- deliver against these properties.

Three further goals are sometimes asked of a product-development framework but are not treated rigorously here: handling **large** data sets, **transfer learning** across manufacturing sites, and a formal proof of **permutation invariance**. The methods we use cope with each of them informally --- latent-variable models scale to large :math:`N`, mean-centring and scaling are insensitive to row order in practice, and a model trained on one site can be re-fit at another --- but a careful treatment is left to the literature.

Data needed for product development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the most heterogeneous of the four. Each column of :math:`\mathbf{D}` is a candidate building block --- an oil, a fat, a binder, a filler, a polymer --- and the rows are properties: molecular weight, melting point, viscosity at a given shear rate, surface tension, NIR absorbance at each wavelength, and so on. Some practitioners prefer the transposed layout (one material per row, properties as columns); either is fine, as long as you stay consistent.

:math:`\mathbf{D}` is assembled from internal lab measurements, supplier data sheets, public databases, and computational property estimators. It is worth investing in: a well-populated :math:`\mathbf{D}` is reused across many product-development campaigns. Collect more rows and more columns than you strictly need for the current project.

A few practical points:

	*	**Do not break "compound" ingredients into their pure constituents.** If you use *milk* as an ingredient, store the properties of milk; do not try to split it into water, fat, protein and lactose. The same goes for any pre-mix or proprietary blend. The columns of :math:`\mathbf{D}` should match the units in which you actually purchase, weigh and add the materials --- the same units that appear in :math:`\mathbf{F}`.

	*	**Properties are usually blocked.** Some rows are only meaningful for solids, others only for liquids, others only for spectroscopic samples. The methods in this chapter handle missing values explicitly, as long as you mark them as missing rather than filling with zeros.

	*	**The result must not depend on the order of rows or columns.** We may *group* rows --- for example, all NIR wavelengths together --- so that block-wise preprocessing is possible, but inside a group the order is arbitrary. This is one of the desiderata (item M) in the previous section.

	*	**Vector-valued properties belong in :math:`\mathbf{D}`** as consecutive rows: a particle-size distribution, a thermogravimetric trace, an NIR spectrum. Such blocks are highly correlated and are a natural fit for a :ref:`principal component model <SECTION_PCA>`.

The recipe :math:`\mathbf{F}`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each row of :math:`\mathbf{F}` is one experiment or one product, and each column is a building block, aligned with the columns of :math:`\mathbf{D}`. The entries in a row are mass fractions and typically sum to 1.

The rows in :math:`\mathbf{F}` need not be products that you sell. Intermediate blends, side experiments and customer trials all belong, as long as each row has a corresponding outcome in :math:`\mathbf{Y}`. It is also useful to split :math:`\mathbf{F}` into sub-blocks --- a binders block, a fats block, a starches block --- so that the model can later assess the effect of each material family separately.

The process conditions :math:`\mathbf{Z}`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The matrix :math:`\mathbf{Z}` has the same number of rows as :math:`\mathbf{F}` and one column per process condition: temperature, pressure, mixing speed, residence time, addition order. Discrete settings (a stirrer that is off, low or high) are :ref:`one-hot encoded <LVM-using-indicator-variables>`. Recipe steps that may or may not be applied are stored as 0/1 indicators.

It is tempting to leave :math:`\mathbf{Z}` out when only the recipe varies during a campaign. Resist that temptation. Conditions that look constant in a campaign --- ambient humidity, operator, raw-material lot number, the calibration date of the analyser --- routinely turn out, after the fact, to have driven a result. If they were never recorded, that diagnosis is impossible. (When such effects *are* expected and we want to remove them by design, we can plan the campaign with :ref:`blocking <DOE_blocking_section>`.) The correct rule is: store the suspected covariates as well as the obvious controlled variables, even if you do not plan to vary them.

The quality outcomes :math:`\mathbf{Y}`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each row of :math:`\mathbf{Y}` is the same experiment as the corresponding row of :math:`\mathbf{F}` and :math:`\mathbf{Z}`. The columns are the key performance indicators (KPIs): viscosity, melting point, shelf life, taste-panel score, and so on. Vector outcomes (such as a release-rate curve) can also be stored in :math:`\mathbf{Y}` as consecutive columns; if they are highly correlated, summarize them with a few principal components first.

The crucial design rule for :math:`\mathbf{Y}` is to capture, at minimum, the same metrics the customer specifies. The whole point of the methodology is to invert the relationship :math:`(\mathbf{D}, \mathbf{F}, \mathbf{Z}) \rightarrow \mathbf{Y}` so that, given a target row :math:`\mathbf{y}_\text{new}`, we can prescribe the recipe and conditions :math:`(\mathbf{f}_\text{new}, \mathbf{z}_\text{new})` that achieve it. If the customer's target metrics are not among the columns of :math:`\mathbf{Y}`, the inversion is solving the wrong problem.

As with :math:`\mathbf{D}`, capture provenance for every entry: who measured the value, where, when, in which units, and with which protocol. Two viscosity numbers measured with different geometries are not the same measurement.

How the four tables fit together
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	*	:math:`\mathbf{D}` and :math:`\mathbf{F}` share columns. Every ingredient appearing in any recipe must have a property column in :math:`\mathbf{D}`. A new, unseen ingredient can later be added to :math:`\mathbf{D}` and then used in :math:`\mathbf{F}`, provided its properties lie within the correlation structure of the existing materials.

	*	:math:`\mathbf{F}`, :math:`\mathbf{Z}` and :math:`\mathbf{Y}` share rows. Row :math:`i` of each describes the same experiment, so they can be concatenated horizontally for a multi-block :ref:`PLS <SECTION_PLS>` analysis. Standard :ref:`preprocessing <LVM_preprocessing>` (mean-centring, scaling, optional block scaling) applies before the model is built.

	*	The forward model :math:`(\mathbf{F}, \mathbf{Z}) \rightarrow \mathbf{Y}` is augmented by the property information in :math:`\mathbf{D}`, so that the model is expressed in terms of *what the materials do* (their physical and chemical properties), not just *which materials were chosen*. This is what allows the model to generalize to new ingredients --- the inductive property (item D) of the desiderata.

	*	Inversion of this model is generally underdetermined: there are typically more inputs than outputs, so a target :math:`\mathbf{y}_\text{new}` corresponds to a *region* of feasible :math:`(\mathbf{f}_\text{new}, \mathbf{z}_\text{new})` rather than a single point. The dimension of that region is the difference between the rank of the input space and the rank of the output space (the "rank" idea in the previous subsection); the inactive directions are the operating window described by item J of the desiderata.

References
~~~~~~~~~~

The four-table organization is drawn from a sequence of papers, several of whose authors I have had the pleasure of working with over the past 25 years:

	*	S. Garcia-Munoz, "Two Novel Methods to Analyze the Combined Effect of Multiple Raw-Materials and Processing Conditions on the Product's Final Attributes: JRPLS and TPLS." *Chemometrics and Intelligent Laboratory Systems*, **133**, 2014, https://doi.org/10.1016/j.chemolab.2014.02.006

	*	K. Muteki, J. F. MacGregor, and T. Ueda. "`Mixture Designs and Models for the Simultaneous Selection of Ingredients and Their Ratios <https://literature.learnche.org/item/146/mixture-designs-and-models-for-the-simultaneous-selection-of-ingredients-and-their-ratios>`_." *Chemometrics and Intelligent Laboratory Systems*, **86**, 2007.

	*	C. M. Jaeckle and J. F. MacGregor. "`Product Design through Multivariate Statistical Analysis of Process Data <https://literature.learnche.org/item/61/product-design-through-multivariate-statistical-analysis-of-process-data>`_." *AIChE Journal*, **44**, 1998.

	*	E. Tomba, M. Barolo, and S. García-Muñoz. "General Framework for Latent Variable Model Inversion for the Design and Manufacturing of New Products." *Industrial & Engineering Chemistry Research*, **51**, 2012, https://doi.org/10.1021/ie301214c


