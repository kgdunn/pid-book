.. _DOE-design-resolution:

Design resolution
~~~~~~~~~~~~~~~~~~~

The :index:`resolution <pair: design resolution; experiments>` of a design is given by the length of the shortest word in the defining relation. We normally write the resolution as a subscript to the factorial design using Roman numerals. Some examples:

	#.	The :math:`2^{7-4}` *example 1* in the previous section had  the shortest word of 3 characters, so this would be called a :math:`2^{7-4}_\text{III}` design. Main effects were confounded with 2-factor interactions in that example.
	#.	The :math:`2^{8-5}` *example 2* had as the shortest word length of 4 characters, so this would be a :math:`2^{8-5}_\text{IV}` design. Main effects were confounded with 3-factor interactions.
	#.	Finally, imagine the case of :math:`2^{5-1}`, in other words a half-fraction design. The first four factors are written in the standard factorial way, but the fifth factor is generated from **E = ABCD**. So its defining relation is  **I = ABCDE**, where the shortest word, not counting the intercept, is 5 characters - it is a :math:`2^{5-1}_{\text{V}}` design. You can verify for yourself that main effects will be confounded with 4-factor interactions in this design.

You can consider the resolution of a design to be an indication of how clearly the effects can be separated in a design. The higher the resolution, the lower the degree of confounding: this is desirable. Within reason, always aim for a higher resolution design given your experimental budget, but also accept a lower resolution, at least initially, in order to test for more factors. We will discuss this further in the section on :ref:`screening designs <DOE-saturated-screening-designs>`.

You can interpret the resolution index as follows: let main effects = 1, two-factor interactions = 2, three-factor interactions = 3, *etc*. Then subtract this number from the resolution index to show how that effect is aliased. Consider a resolution IV design, since :math:`4-1=3`, it indicates that main effects are aliased with 3fi, but not with two-factor interactions; and :math:`4-2 = 2` indicates that 2fi are aliased with each other. Here is a summary:

Resolution III designs: are good for screening
	-	Are excellent for initial screening: to separate out the important factors from the many potential factors. To identify important variables that can be studied in the next experiments.
	-	Main effects are not confounded with each other.
	-	Main effects are aliased with two-factor interactions (:math:`3 - 1 = 2`).
	-	Two-factor interactions are aliased with main effects (:math:`3 - 2 = 1`).

Resolution IV designs: are good for characterizing
	-	Most useful for characterizing (learning about and understanding) a system, both the main effects and the interactions, since:
	-	Interactions are very interesting in many systems, since they go beyond just the main effects and can improve your process even more (or sometimes take away from it too!).
	-	Main effects are not confounded with each other.
	-	Main effects are not aliased with two-factor interactions either (:math:`4-1=3`).
	-	Main effects are aliased with three-factor interactions though (:math:`4-1=3`).
	-	Two-factor interactions are still aliased with each other though (:math:`4-2=2`).

Resolution V designs: are good for optimizing
	-	For optimizing a process, learning about complex effects, and developing high-accuracy predictive models, since:
	-	Main effects are not confounded with each other.
	-	Main effects are not aliased with two-factor interactions.
	-	Two-factor interactions are not aliased with each other either.
	-	But two-factor interactions are aliased with three-factor interactions (:math:`5-2=3`).

The above guidance about using resolution IV and V designs for characterization and optimization is fairly general - there are many cases where a satisfactory optimization can be performed with a resolution IV experiment.

In this text currently, for resolution III, IV and V designs we look at factorial designs. However, there are a number of other design types which can also be used. If you are interested, please research Plackett-Burman designs, Box-Behnken designs, central composite designs, and :ref:`definitive screening designs <DOE-definitive-screening-designs>`.

.. you could also include ideas from this link?
	https://asq.org/quality-progress/2005/10/statistics-roundtable/how-to-choose-the-appropriate-design.html

.. youtube:: https://www.youtube.com/watch?v=uYdLP4TJHYA&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=49

You can use the following table to visualize the trade-off between design resolution, the number of factors (:math:`k`), the number of runs required, and the aliasing pattern. The table is adapted from the text by  Box, Hunter and Hunter (2nd edition, p 272), and (1st edition, p 410).

.. _DOE_design_trade_off_BHH_272:
.. image:: ../../figures/doe/DOE-trade-off-table.png
	:alt:	../../figures/doe/DOE-trade-off-table.svg
	:scale: 100
	:align: center
