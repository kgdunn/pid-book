.. _APPS_process_understanding:

Improved process understanding
==============================

.. index::
	pair: applications; latent variable modelling

.. TODO: another example: https://dx.doi.org/10.1016/S0169-7439(02)00088-6

:ref:`Interpreting the loadings plot <LVM_interpreting_loadings>` from a model is well worth the time spent. At the very least, one will confirm what you already know about the process, but sometimes there are unexpected insights that are revealed. Guide your interpretation of the loadings plot with contributions in the scores, and cross-referencing with the raw data, to verify your interpretation.

There are :math:`A` loadings and score plots. In many cases this is far fewer than the :math:`K` number of original variables. Furthermore, these :math:`A` variables have a much higher signal and lower noise than the original data. They can also be calculated if there are missing data present in the original variables.

In the example shown here the company was interested in how their product performed against that of their competitor. Six variables called A to F were measured on all the product samples, (codes are used, because the actual variables measured are proprietary). The loadings for these 6 variables are labelled below, while the remaining points are the scores. The scores have been scaled and superimposed on the loadings plot, to create what is called a :index:`biplot`. The square, green points were the competitor's product, while the smaller purple squares were their own product.

.. figure:: ../figures/examples/competitor-product/competitor-product.png
	:alt:	process-understanding.key
	:scale: 80
	:width: 750px
	:align: center

.. This figure was from an earlier project on plastic pellets (around 2006?).
.. The keynote presentation was used to disguise the original variable names.

From this single figure the company learned that:

	*	The quality characteristics of this material is not six-dimensional; it is two-dimensional. This means that based on the data used to create this model, there is no apparent way to independently manipulate the 6 quality variables. Products produced in the past land up on a 2-dimensional latent variable plane, rather than a 6-dimensional space.

	*	Variables D, E and F in particular are very highly correlated, while variable C is also somewhat correlated with them. Variable A and C are negatively correlated, as are variables B and C. Variables A and B are positively correlated with each other.

	*	This company' competitor was able to manufacture the product with much lower variability than they were: there is greater spread in their own product, while the competitor's product is tightly clustered.

	*	The competitors product is characterized as having lower values of C, D, E, and F, while the values of A and B are around the average.

	*	The company had produced product similar to their competitor's only very infrequently, but since their product is spread around the competitor's, it indicates that they could manufacture product of similar characteristics to their competitor. They could go query the score values close those of those of the competitors and using their company records, locate the machine and other process settings in use at that time.

		However, it might not just be *how* they operate the process, but also which raw materials and their consistency, and the control of outside disturbances on the process. These all factor into the final product's variability.

It it is not shown here, but the competitor's product points are close to the model plane (low SPE values), so this comparison is valid. This analysis was tremendously insightful, and easier to complete on this single plot, rather than using plots of the original variables.
