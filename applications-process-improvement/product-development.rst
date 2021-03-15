.. _APPS_product_development:

Product development and product improvement
===========================================


This section covers product development, but it is called product improvement. The reason is that new products are seldom developed, but products are regularly improved as the following usage examples show:

Usage examples
~~~~~~~~~~~~~~~

.. index::
	pair: usage examples; product development
	

-	*Colleague*: Our most high profile customer wants us to develop a product with similar, but different specifications to the prior products we have made. Is it feasible to say '*yes*' to them?

-   *You*: we have an existing product, but a customer just wants to change one of the 7 specifications: they want a slightly higher *viscosity*. Keep the ingredients and ratios the same, but which process setting(s) do we change?
    
-   *Manager*: Keep the specifications the same, but adjust the process to use less energy and reduce emmissions, even if we use slightly more expensive materials, with different ratios. Is this possible?
    
-   *Engineer*: A constraint has changed (e.g. a new government regulation, we have to use a different piece of equipment): how can we still get the same final product by adjusting the process conditions, or materials used in the process?
    
-	*Financial controller*: We can buy raw ingredients from these 4 different suppliers. Which ones do we pick to most cost-effictively make the product, but still achieve the specifications?

-   *Engineer 2*: Our current top line product is made with 6 different ingredients. Can we reduce this number down by adjusting the ratios or the choices of ingredients?


As these examples show: "product development" actually happens far more frequently than simply the case of a customer coming to ask for *different, entirely new, specifications* to those you currently have in your portfolio or product catalogue. The opposite case of changing these 3 things, in order to keep the *same specifications* is far more common:

    * which ingredients (raw materials) do you use?
    * which ingredient ratios, specified by mass fraction, do you use?
    * which conditions do you implement to get the final product?

Both the case of creating an entirely new product, or improving an existing product can be considered with the methods described here.

The end goal is "faster development of personalized products and customer-centric development", using the information and databases we have accumulated over the many years of experience with the process.


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

Finally, sometimes the desired outcome is a very large vector, such as time series showing the change of the product, such as elongation in a controlled experiments, or a pH over time. It can also be a spectrum, such as an NIR spectrum. The number of entries in this long vector are highly correlated. So the first step in such a situation is to use a :ref:`principal component model <SECTION_PCA>`_ and understand the true lower dimensional space that the output space has. Then these, far smaller number of components, are used as a specification. Therefore the methods of product design are applicable in this case too.

The "rank"
~~~~~~~~~~~

Details to come in March 2021, with illustrations and interactive case studies.

