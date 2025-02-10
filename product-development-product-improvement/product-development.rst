.. _APPS_product_development:

Product development and product improvement
===========================================


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

Scope of the problem
=====================


There are a few key features that are desired for any data-driven product development tool:

A. The tool is **guided by the expert** to accelerate the process; it is not intended to replace the expert. It will allow the expert to more rapidly prototype and test alternatives, guide the expert. The expert also plays an active role: for example, constraints can be specified by the subject matter expert (SME), and the tool can help the expert to understand the tradeoffs by providing alternative solutions that the SME selects from.

B. It is **multi-objective**. Multiple goals and targets can be taken along, each with different weights and prioritization if needed. For example, if a certain target objective is poorly explained by the data, then it can be down weighted, but not ignored. We should not have to build models for each outcome variable: we must be able to handle multiple key performance indicators (KPIs), even highly correlated ones and also high-dimensional ones (such a vectors).

C. It is **permutation invariant**. The order in which we acquire experimental data should not alter the outcome.

D. We must be able to **handle missing data**. Our knowledge regarding physical and chemical properties of the materials is incomplete; we might only have partial results, or loss of data might have occurred. We might have results from earlier experiments, while later experiments are have extra/more sophisticated data. In all of these cases we should use the data we have, and not have to discard rows or columns of incomplete knowledge.

E. It should **not be dependent on the specific training dataset** and  therefore unable to generalize to new ingredients, other properties, new experiments or other conditions used to create the product. Another way of saying this is that it should not be `transductive <https://en.wikipedia.org/wiki/Transduction_(machine_learning)>`_, but rather inductive.


F. It should be able to handle **small data**. We should not need large amounts of data to get good results as long as we have well-designed experimental data which is strategically chosen to give the most information.

G. It should however be able to handle **large data**. If we do have large quantities of data, then it should be able to handle these as well.

H. It must allow for **learning and interpretation** by the expert. The model results should be understandable, confirm prior knowledge, and generate new insights.

I. It should be able to handle **high-dimensional data**, even if many of the measured data are affected by random noise, or are unrelated to the problem. As we will not always know upfront what is important, if we do happen to add more information, then we should not be penalized. It is acceptable to learn iteratively that certain data are uninteresting. See the prior point.

J. It should provide guidance to **fill in the spaces of unknown knowledge**. It is therefore sequential. The expert can provide influence on where future experiments should be done, to help expand the model's predictive power.

K. An **operating window** for the solution is provided. When constraints are active at a solution, these should be reported, to learn the limits of the system. Conversely, inactive constraints are also insightful, since these provide an operating windows in which we can move without changing the optimization result too much. Even better is if a parameterized solution is presented, allowing the user to fine-tune the solution.

L. The method should **enable transfer learning** across different sites, lines, or even different products. For example, a new product can be developed on site A, and then transferred to site B, using data from both sites, to learn the transferable knowledge, and ignore the regions of operation which have no impact. Extending an existing product from one matrix to another  (e.g. from a liquid to a gel) is another example of transferability.

M. **Handling different scales** should also be accommodated; cheap experiments at a smaller scale being combined with sparse data at a larger scale (e.g. customer trials).

N. Allow for **model inversion**: we do not only want to predict an outcome from upstream information, but also to use the inverse approach: to predict upstream settings for a given set of performance outcomes. This inverse approach is in many cases non-unique: there are multiple upstream settings that can give the same performance outcome. The system should indicate when multiple solutions are possible (the rank of the input space exceeds the output space) and as such there are directions in input space which are unrelated to the output, giving us extra degrees of freedom.

These are ambitious goals. Let us explore how we can achieve most of these in the next sections.

Important concepts
===================

What are the "Degrees of freedom"?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As just mentioned, there are 3 groups of things you can change:

1. **Select your ingredients**. This is a discrete choice: either you use an ingredient or raw materials, or you do not. It is a yes/no selection. You might have a whole catalogue, or database, of materials that you can select from. In many of the cases described in the "Usage examples" above this degree of freedom is actually fixed. In other words, you cannot change the ingredient choice and you must keep using what you already use. This is often due to regulations, or the fact that introducing new ingredients will be too expensive to test and validate and might lead to unexpected side-reactions or interactions.

2. **Adjust the ratios of the ingredients**. This is a sliding parameter: for example you can go from 45% weight fraction of material A, to 41% weight fraction, but remember by using less material A, the weight fractions of other materials change. The total weight fractions always add up to 1.0, so there is a constraint in the system, and adjusting one material will force the other material ratio to also be adjusted.

3. **Use different process conditions**. This group is where often you have the most degrees of freedom. You can adjust process settings used to make the product quite easily, such as temperature, pH, duration of certain steps, and order in which you add ingredients and complete the manufacturing steps. Because of the diversity of the options here, you might need to spend quite some time thinking about the process, and seeing what freedom you practically and economically have. Like the prior group, the ratios, this group of degrees of freedom also has some correlations in the historical data. For example, you might not be able to independently increase temperature in the process, without adjusting flow rate.


The "desired outcome"
~~~~~~~~~~~~~~~~~~~~~~

This is a specification of what you want to achieve. Your end goal. It is often given as a vector of one or more specifications. For example: you might need to achieve a given viscosity, melting point and product density. These 3 numbers jointly defind the expectations.

Some entries in the desired outcome vector might simply be given as constraints. For example, "an *elongation* value of 15 or lower is acceptable, or a *shelf-life* of 30 days or greater is acceptable. This is more of a yes/no constraint: it is either met, or it is not. It creates a discontinuity in our system when we specify it as an equation later on. Discontinuities are often undesirable from a mathematical modelling and optmization perspective. However these can be dealt with by converting them to a smoothed version, such as by using a sigmoid function or a `Gompertz function <https://en.wikipedia.org/wiki/Gompertz_function>`_.

Finally, sometimes the desired outcome is a very large vector, such as time series showing the change of the product, such as elongation in a controlled experiments, or a pH over time. It can also be a spectrum, such as an NIR spectrum. The number of entries in this long vector are highly correlated. So the first step in such a situation is to use a :ref:`principal component model <SECTION_PCA>` and understand the true lower dimensional space that the output space has. Then these, far smaller number of components, are used as a specification. Therefore the methods of product design are applicable in this case too.

The "rank"
~~~~~~~~~~~

More to come.


