.. _APPS_product_development:

Product development and product improvement
===========================================


This section covers product development, but it is called product improvement. The reason is that new products are seldom developed, but products are improved almost on a daily basis. The following usage examples show what we will cover:

Usage examples
~~~~~~~~~~~~~~~

.. index::
	pair: usage examples; product development
	

-	*Colleague*: Our most high profile customer want us to develop a product with similar, but different specifications to prior products we have made. Is it feasible to say '*yes*' to them?

-   *You*: we have an existing product, but a customer just wants to change one of the 7 specifications: they want a slightly higher *viscosity*. Keep the ingredients the same, but what process setting(s) do we change?
    
-   *Manager*: Keep the specifications the same, but adjust the process to use less energy and reduce emmissions, even if we use slightly more expensive materials, with different ratios. Is this possible?
    
-   *Engineer*: A constraint has changed (e.g. government regulation, a piece of broken equipment): how can we still get the same final product by adjusting the process conditions, or materials used in the process?
    
-	*Financial controller*: We can buy raw ingredients from these 4 different suppliers. Which ones do we pick to most cost effictively make the product, but still achieve the specification?

-   *Engineer 2*: Our current top line product is made with 6 different ingredients. Can we reduce the number down by adjusting the ratios and the choices of ingredients?


As these examples show: "product development" actually happens far more frequently than simply the case of a (new) customer coming to ask for *different specifications* to those you currently have in your portfolio or product catalogue. The opposite case of changing these 3 things, in order to keep the *same specifications* is far more common:

    * which ingredients (raw materials) do you use?
    * which ratios do you use, e.g. based on relative weight percentage?
    * and which conditions and steps do you follow to get the final product?

Both the case of creating an entirely new product, or improving an existing product can be considered with the methods described here.

The end goal is simple "faster development of personalized products and customer-centric development", using the information and databases we have accumulated over the many years of experience with the process.


Important Concepts
===================

What are the "Degrees of freedom"?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As just mentioned, there are 3 groups of things you can change:

1. **Select your ingredients**. This is discrete choice: either you use an ingredient or raw materials, or you do not. It is a yes/no selection. You might have a whole catalogue, or database, of materials that you can select from. In many of the cases described in the "Usage examples" above this degree of freedom is actually fixed. In other words, you cannot change the ingredient choice and you must keep using what you already use. This is often due to regulations, or the fact that introducing new ingredients will be too expensive to test and validate.

2. **Adjust the ratios of the ingredients**. This is a sliding parameter: for example you can go from 45% weight fraction of material A, to 41% weight fraction, but remember by using less material A, the weight fractions of other materials change. The total weight fractions always add up to 1.0, so there is a constraint in the system, and adjusting one materials forces the other material(s) to also be adjusted. There are some built-in correlations here.

3. **Use different process conditions and steps**. This group is where often you have the most degrees of freedom. You can adjust process settings used to make the product quite easily, such as temperature, pH, duration of certain steps, and order in which you add ingredients and complete the manufacturing steps. Because of the diversity of the options here, you might need to spend quite some time thinking about the process, and seeing what freedom you practically have. Like the prior group, the ratios, this group of degrees of freedom also has some correlations in the historical data. For example, you might not be able to independently increase temperature in the process, without adjusting flow rate.


The "desired outcome"
~~~~~~~~~~~~~~~~~~~~~~

This is a specification of what you want to achieve. Your end goal. It is often given as a vector of one or more specifications. For example: you might need to achieve a given viscosity, melting point and product density. These 3 numbers jointly defind the expectations.

Some entries in the desired outcome vector might simply be given as constraints. For example, "an *elongation* value of 15 or lower is acceptable, or a *shelf-life* of 30 days or greater is acceptable. This is more of a yes/no constraint: it is either met, or it is not. It creates a discontinuity in our system when we specify it as an equation later on. Discontinuities are often undesirable from a mathematical modelling and optmization perspective.

The "rank"
~~~~~~~~~~~

Details to come in March 2021, with illustrations and interactive case studies.

