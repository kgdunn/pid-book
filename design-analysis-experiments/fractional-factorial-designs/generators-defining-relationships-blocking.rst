.. _DOE-generators:

Generators and defining relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube:: https://www.youtube.com/watch?v=3Wp-0aOo-ns&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=44

Calculating which main effects and two-factor interactions will be confounded with each other, called the :index:`confounding pattern`, can be tedious for larger values of :math:`k`. Here we introduce an easy way to calculate the confounding pattern.

Recall for the half-fraction of a :math:`2^k` factorial that the first  :math:`k-1` main factors are written down, then the final :math:`k^\text{th}` factor is *generated* from the product of the previous :math:`k-1` factors. Consider the case of a :math:`2^4` half fraction with factors **A**, **B**, **C** and **D**. We write a :math:`2^3` factorial in factors **A**, **B**, and **C**, then set 

.. centered:: **D = ABC**

This is called the *generating relation* for the design. Some rules when working with this notation are that  **A** :math:`\times` **A = I**, **B** :math:`\times` **B = I**, **I** :math:`\times` **I = I**. So for example,  **D** =  **ABC** can by multiplied on both sides by **D** to get **D** :math:`\times` **D** = **ABC** :math:`\times` **D**, which gives **I** = **ABCD**. Another way to get this same result: **ABC** :math:`\times` **D** =  **ABC** :math:`\times` **ABC = AABBCC = I I I = I = ABCD**.


.. index::
	pair: generating relationship; experiments
	pair: defining relationship; experiments
	
This last part, **I = ABCD**, is called the *defining relation* for this design. The defining relationship is the product of all generator combinations, then simplified to be written as **I = ....**. In this case there is just one generator, so the defining relationship is the generator. We will discuss this again later.

.. centered:: **I = ABCD**

Now the effects which are aliased (confounded) with each other can be found quickly by multiplying the effect by the defining relationship. For example, if we wanted to know what the main effect **A** would be confounded with in this :math:`2^{4-1}` half fraction we should multiply **A** by the defining relationship as in 

.. centered:: **A** :math:`\times` **I = A** :math:`\times` **ABCD = BCD**

indicating that **A** is aliased with the 3-factor interaction **BCD**.  What is the aliasing for these effects:

	-	What is main effect **B** aliased with? (*Answer*: **ACD**)
		
	-	What is the 2fi **AC** aliased with? (*Answer*: **BD**)

**Another example**: 

	Returning back to the :math:`2^{3-1}` half fraction in the :ref:`previous section <DOE-half-fractions>`, use the defining relation to verify the aliasing of main-effects and two-factor interactions derived earlier by hand.

		-	What is the defining relationship?
		
		-	Aliasing for **A**? (*Answer*: **BC**)
	
		-	Aliasing for **B**? (*Answer*: **AC**)
		
		-	Aliasing for **C**? (*Answer*: **AB**: recall this is how we generated that half fraction)
		
		-	Aliasing for the intercept term, **I**? (*Answer*: **ABC**)
	
**Yet another example**: 

	Which aliasing (confounding) would occur if you decided for a :math:`2^{4-1}` design to generate the half-fraction by using the 2-factor interaction term **AC** rather than the 3-factor interaction term **ABC**.

		-	What is the defining relationship?
		-	Aliasing for **A**? (*Answer*: **CD**)
		-	Aliasing for **B**? (*Answer*: **ABCD**)
		-	Aliasing for **C**? (*Answer*: **AD**)
		
	Why is this a poorer choice than using **D = ABC** to generate the half-fraction? *Answer*: the main effects of **A** and **C** are aliased with 2fi which could be important. Had we generated the design with the usual 3fi term, **ABC**, the main effects would only be aliased with three-factor interactions (3fi).
	
	.. youtube:: https://www.youtube.com/watch?v=LaWQyZxl2do&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=45

Generating the complementary half-fraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say that a half fraction for a :math:`2^3` factorial was run. The defining relation was **I = ABC**, so factor **C** was aliased with the 2fi **AB**. Now if these 4 runs produce promising results, you might seek approval to complete the factorial and run the other half fraction. This will remove the aliasing when you now analyze all 8 data points together. The defining relation for the complementary half-fraction is **I = -ABC**, or equivalently **IC = C = -AB**.

Let's return to the table in the :ref:`previous section <DOE-half-fractions>` and generate the other 4 runs:

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

After running these 4 experiments (in random order of course) we have a complete set of 8 runs. Now the main effects and two-factor interactions can be calculated without aliasing because we are back to the usual full factorial in :math:`2^3` runs.

So we see that we can always complete our half-fraction by creating a complementary fraction. This complimentary fraction is found by flipping the sign on the generating factor. For example, changing the sign from **C** to **-C**. See the illustration.

.. image:: ../../figures/doe/complementary-half-fraction-in-3-factors.png
	:align: right
	:scale: 30
	:alt:	complementary-half-fraction-in-3-factors.svg
	:width: 900px

.. FAKE WIDTH ABOVE

.. _DOE-Generators-for-blocking:

Generators: to determine confounding due to blocking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generators are also great for determining the blocking pattern. Recall the case described earlier where we only had enough material to run two sets of 4 experiments to complete our :math:`2^3` full factorial. An unintended disturbance could have been introduced by running the first half-fraction on different materials to the second half-fraction. We :ref:`intentionally decided <DOE-Blocking-and-confounding>` to confound the two blocks of experiments with the 3-factor interaction, **ABC**. So if there is an effect due to the blocks (i.e. the raw materials) or if there truly was a 3-factor interaction, it will show up as a significant coefficient for :math:`b_{ABC}`.

So *in general* when running a :math:`2^k` factorial in two blocks you should create a :math:`2^{k-1}` half fraction to run as the first block, and then run the other block on the complementary half-fraction. You should always confound your block effect on the highest possible interaction term. Then block 1 runs will have that highest interaction term with all positive signs, and block 2 will have all negative signs for that interaction.

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

.. My notes on this section are not clear:  how to clearly illustrate that A will be aliased with DE?  And how is it obvious that this aliasing with DE (the block effect contrast) is problematic?  Perhaps use an example where the blocks are biased and factor A was never really significant.

	What if the block effect has more than two levels?  For example, for a :math:`2^3` factorial, there is only enough material for 2 experiments. So :math:`g=4` groups of experiments will be run. How do we assign these groups to minimize confounding?  Find the smallest full factorial that can accommodate these :math:`g` groups, in this case a :math:`2^2` factorial. Write out this factorial and assign the groups accordingly:

	.. tabularcolumns:: |c||c|c|c|
                       
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

	It is as if we are introducing two new variables into our :math:`2^3` factorial: in addition to the factors **A**, **B** and **C**, we also have factors **D** and **E** corresponding to the different groups of materials. For example, when we use lot 3, then :math:`D = -1` and :math:`E = +1`.

	How do we assign **D** and **E** so that the confounding is minimized?  We might be tempted to use **D = ABC** and then assign **E** to **BC**, an interaction that we are not concerned 
	about. The generators are then **I = ABCD** and **I = BCE** respectively. The *defining relationship* is found from all possible products of all generators. In this case there are just two generators, so the defining relationship, which is the product of all generators is: **I = ABCD = BCE = ADE**.

	Now let's calculate the aliasing structure:

		-	A: aliased with A + BCD + ABCE + DE
		-	Fix this: **B x ADE = ABDE**
		-	Fix this: **C x ADE = ACDE**
		-	Fix this: **AB x ADE = BDE**
		-	Fix this: **AC x ADE = CDE**
		-	Fix this: **BC x ADE = ABCDE**
		-	Fix this: **ABC x ADE = BCDE**

	This indicates the main effect of **A** is aliased with the two-factor interaction **DE**. Why is this problematic?
	
	The other effects are confounded with three-factor interactions

	A better choice of generators is **D = AB** and **E = AC** (or use the other two-factor interaction). Now calculate:

		-	The defining relationship = 
	
			.. I = ABD = ACE = ABD x ACE = BCDE

		-	Aliasing for:

			* **A**
			* **B**
			* **C**
			* **AB**
			* **AC**
			* **BC**
			* **ABC**  
			
	Rather than determine the best aliasing structure by trial-and-error, refer to a table, such as Table 5A.1 (page 221) in the second edition of Box, Hunter and Hunter to read which generators should be assigned to which blocks to minimize confounding. For this example, you would use the row in the table with :math:`k=3`, block size = 2 (two experiments per block). Another example is given in this same reference, page 219, that describes how a 64 run experiments is broken down into 8 blocks of 8 runs.

.. Don't try this example: it's still too early.
	For example, for a :math:`2^3` factorial, the block size is 3 experiments when there is only enough material for 3 experiments. So two experiments will be run with one lot of material, then 3 runs with another lot, and then the final 3 runs.

	Start by rounding down to the closest power of 2, which is :math:`p = 2^1 = 2` in this case. Create a full factorial with :math:`2^p` runs. Assign the blocks according to the different runs in this factorial:

	.. tabularcolumns:: |c||c|c|c|
	                          D              E   
	+-------------------+-------------+-------------+
	| Batch of material | :math:`B_1` | :math:`B_2` |
	+===================+=============+=============+
	|  1                | |-|         | |-|         | 
	+-------------------+-------------+-------------+
	|  2                | |+|         | |-|         |
	+-------------------+-------------+-------------+
	|  3                | |-|         | |+|         |
	+-------------------+-------------+-------------+
	|  4 (ignored)      | |+|         | |+|         |
	+-------------------+-------------+-------------+

	B_1: I=ABCD;  
	B_2: I=BCE

	overall generator: ABCD.BCE = ADE
	A: DE
	B: ABDE
	C: ACDE
	
