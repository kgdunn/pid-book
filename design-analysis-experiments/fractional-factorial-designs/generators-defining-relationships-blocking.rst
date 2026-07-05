.. _DOE-generators:

Generators and defining relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=3Wp-0aOo-ns&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=45

Calculating which main effects and two-factor interactions will be confounded with each other, called the :index:`confounding pattern <pair: confounding pattern; experiments>`, can be tedious for larger values of :math:`k`. Here we introduce an easy way to calculate the confounding pattern.

Recall for the half-fraction of a :math:`2^k` factorial that the first  :math:`k-1` main factors are written down, then the final :math:`k^\text{th}` factor is *generated* from the product of the previous :math:`k-1` factors. Consider the case of a :math:`2^4` half fraction with factors **A**, **B**, **C** and **D**. The half-fraction has :math:`\frac{1}{2} 2^4 = 2^3 = 8` experiments, so we write this :math:`2^3` factorial in factors **A**, **B**, and **C**, then set:

.. centered:: **D = ABC**

This is called the *generating relation* for the design. Here are some rules when working with this notation:

*	A factor multiplied by itself is the identity, or intercept column: **A** :math:`\times` **A = I**, **B** :math:`\times` **B = I**, etc. Think about that: if you look at the previous designs we have written out, this makes sense. Any column multiplied by itself is equal to a column of ones.
* 	A factor multiplied by a column of ones is equal to itself. For example: **D** :math:`\times` **I = D**
*	The intercept **I** is simply a column of ones, which is what the intercept column is. And for emphasis: **I** :math:`\times` **I = I**.
*	You can substitute in the *generating relation* of **D = ABC**, and like with an algebraic equation, we can multiply both sides by **D** to get **D** :math:`\times` **D** = **ABC** :math:`\times` **D**, which simplifies to **I** = **ABCD**. Another way to get this same result it to substitute the generating relationship in twice: **ABC** :math:`\times` **D** =  **ABC** :math:`\times` **ABC = AABBCC = I I I = I = ABCD**.

.. index::
	pair: generating relationship; experiments
	pair: defining relationship; experiments

This last part, **I = ABCD**, is called the *defining relation* for this design. Notice that we started with the *generating relation* and simplified it by multiplying the terms in that relationship with each other. Since there were two terms, **ABC** and **D**, we multiplied them, and ended up with **I = ABCD**.

This is our defining relationship for this design:

.. centered:: **I = ABCD**

We will discuss this topic again later with more examples. The main point though is that the effects which are aliased (confounded) with each other can be found quickly by multiplying the effect we are interested in by the defining relationship. For example, if we wanted to know what the main effect **A** would be confounded with in this :math:`2^{4-1}` half fraction we should multiply **A** by the defining relationship as in

.. centered:: **A** = **A** :math:`\times` **I = A** :math:`\times` **ABCD = BCD**

indicating that **A** is aliased with the 3-factor interaction **BCD**.  What is the aliasing for these effects:

	-	What is main effect **B** aliased with? (*Answer*: **ACD**)

	-	What is the 2fi **AC** aliased with? (*Answer*: **BD**)

**Another example**:

	Returning back to the :math:`2^{3-1}` half fraction in the :ref:`previous section <DOE-half-fractions>`, use the generating relation to verify the aliasing of main-effects and two-factor interactions derived earlier by hand.

		-	First calculate the defining relationship. It is **I** = .....

		-	Aliasing for **A**? (*Answer*: **BC**)

		-	Aliasing for **B**? (*Answer*: **AC**)

		-	Aliasing for **C**? (*Answer*: **AB**: recall this is how we generated that half fraction)

		-	Aliasing for the intercept term, **I**? (*Answer*: **ABC**)

**Yet another example**:

	Which aliasing (confounding) would occur if you decided for a :math:`2^{4-1}` design to generate the half-fraction by using the 2-factor interaction term **AC** rather than the 3-factor interaction term **ABC**.

		-	First write out your generating relationship: **D** = **AC**
		-	Now calculate the defining relationship: **I** = ....
		-	Aliasing for **A**? (*Answer*: **CD**)
		-	Aliasing for **B**? (*Answer*: **ABCD**)
		-	Aliasing for **C**? (*Answer*: **AD**)

	Why is this a poorer choice than using **D = ABC** to generate the half-fraction? *Answer*: the main effects of **A** and **C**  which could be important, are aliased with 2fi. Had we generated the design with the usual 3fi term, **ABC**, the main effects would only be aliased with three-factor interactions (3fi).

	.. youtube:: https://www.youtube.com/watch?v=LaWQyZxl2do&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=46

.. index::
	pair: complementary half-fraction; experiments

Generating the complementary half-fraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returning to our example in the :ref:`previous section <DOE-half-fractions>` of a half-fraction from a full :math:`2^3` factorial, and imagine the half-fraction of 4 runs was completed. Imagine that all 3 factors showed significant effect on the outcome. Further, imagine that one of the factors actually gave a direction opposite to what was expected. This is really interesting, and unexpected new knowledge.

The original generator was **C = AB** and the defining relation was **I = ABC**; so factor **C** was aliased with the 2fi of **AB**. If it was factor **C** that had an opposite sign, it could be due to **C**, or due to **AB**. So you wish to complete the full-factorial and run the other half fraction to find out. This will help clarify that interesting factor, because it will remove the aliasing when you then analyze all 8 data points together.


The defining relation for the complementary half-fraction is **I = -ABC**, or multiply both sides by **C** to equivalently obtain **IC = C = -AB**. This shows the complementary half fraction is in fact generated by **C = -AB**, while the original half-fraction was generated by **C = AB**. This is a general rule that applies to half-fractions.

Let's return to the table in the :ref:`previous section <DOE-half-fractions>` and generate the other 4 runs from that **C = -AB** defining relationship:

.. tabularcolumns:: |c||c|c|c|

+-----------+------------+-----------+------------+
| Experiment| A          | B         |  C = |-| AB|
+===========+============+===========+============+
| 5         | |-|        | |-|       |  |-|       |
+-----------+------------+-----------+------------+
| 6         | |+|        | |-|       |  |+|       |
+-----------+------------+-----------+------------+
| 7         | |-|        | |+|       |  |+|       |
+-----------+------------+-----------+------------+
| 8         | |+|        | |+|       |  |-|       |
+-----------+------------+-----------+------------+

.. image:: ../../figures/doe/complementary-half-fraction-in-3-factors.png
	:align: right
	:scale: 30
	:alt:	complementary-half-fraction-in-3-factors.svg
	:width: 900px

After running these additional 4 experiments shown (in random order of course) we have a complete set of 8 runs. Analyzing the data together we can calculate the main effects and two-factor interactions without aliasing because we are back to the usual full factorial of :math:`2^3` runs. Confirm it for yourself visually in the plot alongside.

So we see that we can always complete our half-fraction by creating a complementary fraction. This complementary fraction is found by flipping the sign on the generating factor. For example, changing the sign from **C = AB** to **C = -AB**. In the illustration this is equivalent to running the 4 experiments at the closed circles.

.. _DOE-Generators-for-blocking:

Generators: to determine confounding due to blocking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generators are also great for determining the blocking pattern. Recall the case described earlier where we only had enough material to run two sets of 4 experiments to complete our :math:`2^3` full factorial. An unintended disturbance could have been introduced by running the first half-fraction on different materials to the second half-fraction. We :ref:`intentionally decided <DOE-Blocking-and-confounding>` to confound the two blocks of experiments with the 3-factor interaction, **ABC**. So if there is an effect due to the blocks (i.e. the raw materials) or if there truly was a 3-factor interaction, it will show up as a significant coefficient for :math:`b_{ABC}`.

So *in general* if you run a full :math:`2^k` factorial in two blocks you should create a :math:`2^{k-1}` half fraction to run as the first block, and then run the other block on the complementary half-fraction. You should always confound your block effect on the highest possible interaction term. Then block 1 runs will have that highest interaction factor with all positive signs, and block 2 will have all negative signs for that interaction factor.

Here are the block generators you can use when splitting a :math:`2^k` factorial in 2 blocks:

.. tabularcolumns:: |c||c|c|c|

+-----------+-----------------+-------------------------------+-------------------------------+
| :math:`k` | Design          | Block 1 defining relation     | Block 2 defining relation     |
+===========+=================+===============================+===============================+
| 3         | :math:`2^{3-1}` | **I=ABC**                     | **I=-ABC**                    |
+-----------+-----------------+-------------------------------+-------------------------------+
| 4         | :math:`2^{4-1}` | **I=ABCD**                    | **I=-ABCD**                   |
+-----------+-----------------+-------------------------------+-------------------------------+
| 5         | :math:`2^{5-1}` | **I=ABCDE**                   | **I=-ABCDE**                  |
+-----------+-----------------+-------------------------------+-------------------------------+


Blocking into more than two groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What if the disturbance has more than two levels? Suppose we must run a :math:`2^3` factorial, but there is only enough material for two experiments from each lot, so the eight runs are split across four lots. We have :math:`g = 4` groups, and we want to arrange them so that the differences between lots do the least damage.

Find the smallest full factorial that can index the :math:`g` groups: here a :math:`2^2` factorial, with two new indicator variables **D** and **E** labelling the four lots.

.. tabularcolumns:: |c||c|c|

+-------------------+-------------+-------------+
| Lot of material   | D           | E           |
+===================+=============+=============+
|  1                | |-|         | |-|         |
+-------------------+-------------+-------------+
|  2                | |+|         | |-|         |
+-------------------+-------------+-------------+
|  3                | |-|         | |+|         |
+-------------------+-------------+-------------+
|  4                | |+|         | |+|         |
+-------------------+-------------+-------------+

It is as if we have added two new variables to the :math:`2^3` factorial: alongside the real factors **A**, **B** and **C**, the block indicators **D** and **E** record which lot was used (for lot 3, :math:`D = -1` and :math:`E = +1`). Three contrasts carry the differences among the four lots: **D**, **E**, and their product **DE**. The goal is to keep those three block contrasts away from the effects we care about, and especially away from the main effects.

A tempting but poor choice is **D = ABC** and **E = BC**. The generators are then **I = ABCD** and **I = BCE**, and the defining relationship is the product of all the generators, **I = ABCD = BCE = ADE** (the product **ABCD** :math:`\times` **BCE** repeats **B** and **C**, and any letter times itself is the identity, which leaves **ADE**). The three block contrasts are therefore **D = ABC**, **E = BC**, and **DE = A**. That last one is the trouble: **DE = A** means the difference between the lots is confounded with the main effect of **A**. If the lots happen to differ, that difference is indistinguishable from a real **A** effect, and a main effect is what we least want to lose.

A better choice is **D = AB** and **E = AC** (any two distinct two-factor interactions will do). The generators are **I = ABD** and **I = ACE**, giving the defining relationship **I = ABD = ACE = BCDE** (the product **ABD** :math:`\times` **ACE** repeats **A**, which cancels to the identity, leaving **BCDE**). Now the three block contrasts are **D = AB**, **E = AC**, and **DE = BC**, all two-factor interactions. No main effect is confounded with a block; the price of blocking falls entirely on the three two-factor interactions **AB**, **AC** and **BC**, which is usually acceptable.

Rather than search for the best assignment by trial and error, you can read it from a table, such as Table 5A.1 (page 221) in the second edition of Box, Hunter and Hunter, which lists the generators to use for each combination of factor count and block size. For this example you would use the row with :math:`k = 3` and a block size of 2. The same reference (page 219) works a larger case: a 64-run experiment split into 8 blocks of 8 runs.
