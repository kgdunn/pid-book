.. _DOE-highly-fractionated-designs:

Highly fractionated designs: beyond half-fractions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running a half-fraction of a :math:`2^k` factorial is not the only way to reduce the number of runs. In general, we can run a :math:`2^{k-p}` fractional factorial. A system with :math:`2^{k-1}` is called a *half fraction*, while a :math:`2^{k-2}` design is a quarter fraction, and so on.

The purpose of a fractionated design is to reduce the number of experiments when your budget - or time - does not allow you to complete a full factorial. Also, the full factorial is often not required, especially when :math:`k` is greater than about 4, since the higher-order interaction terms are almost always insignificant. If we have a budget - or time - for only 8 experiments, then our options are to run a:

	- :math:`2^3` full factorial on **3 factors**
	- :math:`2^{4-1}` half fraction, investigating **4 factors**
	- :math:`2^{5-2}` quarter fraction looking at the effects of **5 factors**
	- :math:`2^{6-3}` fractional factorial with **6 factors**, or a
	- :math:`2^{7-4}` fractional factorial with **7 factors**.

At the early stages of our work we might prefer to screen many factors, :math:`k = 6~\text{or}~7`, accepting a very complex confounding pattern, because we are uncertain which factors actually affect our response. Later, as we are optimizing our process, particularly as we approach an optimum, then the 2 factor and perhaps 3-factor interactions are more dominant. So investigating and calculating these effects more accurately and more precisely becomes important and we have to use full factorials. But by then we have hopefully identified much fewer factors :math:`k` than what we started off with.

So this section is concerned with the trade-offs as we go from a full factorial with :math:`2^k` runs to a highly fractionated factorial, :math:`2^{k-p}`.

*Example 1*

	You have identified 7 factors that affect your response.

	-	What is the smallest number of runs that can be performed to screen for the main effects?

		A :math:`2^{7-p}` fractional factorial would have 64 (:math:`p=1`), 32 (:math:`p=2`), 16 (:math:`p=3`), or 8 (:math:`p=4`) runs. The last case is the smallest number that can be used to estimate the intercept and 7 main effects (8 data points, 8 unknowns).

	-	What would be the generators and defining relation for this :math:`2^{7-4} = 8` run experiment and what is the aliasing structure?

		#.	Assign **A**, **B**, ... **G** as the 7 factor names. Since there are 8 runs, start by writing out the first 3 factors, **A**, **B**, and **C**, in the usual full factorial layout for these :math:`2^3 = 8` runs.

		#.	Next we assign the remaining factors to the highest-possible interaction terms from these 3 factors. Since we've already assigned **A**, **B** and **C** we only have to assign the other 4 factors, **D**, **E**, **F**, and **G**. Pick the 4 interaction terms that we are least interested in. In this particular example, we have to use all (saturate) the interaction terms.

			*	**D = AB**
			*	**E = AC**
			*	**F = BC**
			*	**G = ABC**

		Record the experimental results for :math:`y` in the last column.

			.. tabularcolumns:: |c||c|c|c||c|c|c|c|c|

			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| Experiment| A          | B         |  C         |  D=AB      |  E=AC      |  F=BC      |  G=ABC     | :math:`y`  |
			+===========+============+===========+============+============+============+============+============+============+
			| 1         | |-|        | |-|       |  |-|       |  |+|       |  |+|       |  |+|       |  |-|       |  77.1      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| 2         | |+|        | |-|       |  |-|       |  |-|       |  |-|       |  |+|       |  |+|       |  68.9      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| 3         | |-|        | |+|       |  |-|       |  |-|       |  |+|       |  |-|       |  |+|       |  75.5      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| 4         | |+|        | |+|       |  |-|       |  |+|       |  |-|       |  |-|       |  |-|       |  72.5      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| 5         | |-|        | |-|       |  |+|       |  |+|       |  |-|       |  |-|       |  |+|       |  67.9      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| 6         | |+|        | |-|       |  |+|       |  |-|       |  |+|       |  |-|       |  |-|       |  68.5      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| 7         | |-|        | |+|       |  |+|       |  |-|       |  |-|       |  |+|       |  |-|       |  71.5      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+
			| 8         | |+|        | |+|       |  |+|       |  |+|       |  |+|       |  |+|       |  |+|       |  63.7      |
			+-----------+------------+-----------+------------+------------+------------+------------+------------+------------+

		#.	So the 4 generators we used to create, or generate, the experimental design are **I = ABD**, **I = ACE**, **I = BCF** and **I = ABCG**. The generator terms such as **ABD** and **ACE** are called *"words"*.

		#.	The *defining relationship* is a sequence of :index:`words <pair: words; experiments>` which are all equal to **I**. The :index:`defining relation <pair: defining relationship; experiments>` is found from the product of all possible generator combinations, and then simplified to be written as **I = ....**.

			The rule is that a :math:`2^{k-p}` factorial design is produced by :math:`p` generators and has a defining relationship of :math:`2^p` words. So in this example there are :math:`p` generators and :math:`2^p = 2^4 = 16` words in our defining relation. They are:

			-	Intercept:	**I** [1]
			-	Each generator combined with **I**:	 **I = ABD = ACE = BCF = ABCG** [2,3,4,5]
			-	Two combinations of generators:	**I = BDCE = ACDF = CDG = ABEF = BEG = AFG** [6 to 11]
			-	Three combinations of generators:	**I = DEF = ADEG = CEFG = BDFG** [12 to 15]
			-	Four combinations of generators: **I = ABCDEFG** [16]

			The 16 words in the defining relationship are written as: **I = ABD = ACE = BCF = ABCG = BCDE = ACDF = CDG = ABEF = BEG = AFG = DEF = ADEG = CEFG = BDFG = ABCDEFG**. The shortest length word, not counting the intercept, has 3 letters. We will refer to this later as the :ref:`design's resolution <DOE-design-resolution>`.

		#.	The aliasing or confounding pattern for any desired effect can be calculated by multiplying the defining relationship by that effect. Let's take **A** as an example, below, and multiply it by the 16 words in the defining relation:

			**AI = BD = CE = ABCF = BCG = ABDCE = CDF = ACDG = BEF = ABEG = FG = ADEF = DEG = ACEFG = ABDFG = BCDEFG**. So our factor **A** estimate is not just factor **A**, it is also a combined estimate of:

				:math:`\widehat{\beta}_A \rightarrow` A + **BD** + **CE** + ABCF + BCG + ABCDE + CDF + ACDG + BEF + ABEG + **FG** + ADEF + DEG + ACEFG + ABDFG + BCDEFG.

				:math:`\widehat{\beta}_A \approx` A + **BD** + **CE** + **FG** + ...

			So by performing 8 runs instead of the full :math:`2^7`, we confound the main effects with a large number of 2-factor and higher interaction terms. In particular, the main effect of **A** is confounded here with the **BD**, **CE** and **FG** two-factor interactions. Any 3 and higher-order interaction confounding is usually not of interest.

			Listed below are all the aliases for the main effects, reporting only the two-factor interactions. The bold words indicate the confounding that was intentionally created when we set up the design.

			-	:math:`\widehat{\beta}_0` = ABCDEFG
			-	:math:`\widehat{\beta}_{\mathbf{A}} \rightarrow` A + BD + CE + FG
			-	:math:`\widehat{\beta}_{\mathbf{B}} \rightarrow` B + AD + CF + EG
			-	:math:`\widehat{\beta}_{\mathbf{C}} \rightarrow` C + AE + BF + DG
			-	:math:`\widehat{\beta}_{\mathbf{D}} \rightarrow` **D + AB** + CG + EF
			-	:math:`\widehat{\beta}_{\mathbf{E}} \rightarrow` **E + AC** + BG + DF
			-	:math:`\widehat{\beta}_{\mathbf{F}} \rightarrow` **F + BC** + AG + DE
			-	:math:`\widehat{\beta}_{\mathbf{G}} \rightarrow` G + CD + BE + AF

		#.	If this confounding pattern is not suitable, for example, if you expect interaction **BG** to be important but also main effect **E**, then choose a different set of generators before running the experiment. Or more simply, reassign your variables (temperature, pressure, pH, agitation, *etc*) to different letters of **A**, **B**, *etc* to obtain another, hopefully more desirable, confounding relationship.

*Example 2*

	From a cause-and-effect analysis, flowcharts, brainstorming session, expert opinions, operator opinions, and information from suppliers you might determine that there are 8 factors that could impact an important response variable. Rather than running :math:`2^8 = 256` experiments, you can run :math:`2^{8-4} = 16` experiments. (Note: you cannot have fewer experiments: :math:`2^{8-5} = 8` runs are not sufficient to estimate the intercept and 8 main effects).

	So the :math:`2^{8-4}` factorial will have :math:`2^4` runs. Assign the first 4 factors to **A**, **B**, **C** and **D** in the usual full factorial manner to create these 16 runs, then assign the remaining 4 factors to the three-factor interactions:

	-	**E** = **ABC**, or **I = ABCE**
	-	**F** = **ABD**, or **I = ABDF**
	-	**G** = **BCD**, or **I = BCDG**
	-	**H** = **ACD**, or **I = ACDH**

	So by multiplying all combinations of the words we obtain the complete defining relationship. We expect :math:`p=4` generators and :math:`2^p=16` words in the defining relationship.

	-	Two at a time: **I = ABCE** :math:`\times` **ABDF = CDEF**, **I = ABCE** :math:`\times` **BCDG = ADEG**, *etc*
	-	Three at a time: **I = ABCE** :math:`\times` **ABDF** :math:`\times` **BCDG = BEFG**, *etc*
	-	Four at a time: **I = ABCE** :math:`\times` **ABDF** :math:`\times` **BCDG** :math:`\times` **ACDH = ABCDEFGH**.

	The defining relationship is **I = ABCE = ABDF = BCDG = ACDH = CDEF = ADEG = ... = ABCDEFGH**, and the shortest word, not counting the intercept, has 4 characters. We will refer to this later as the :ref:`design's resolution <DOE-design-resolution>`.

	Next we can calculate all aliases of the main effects. So for **A = IA = BCE = BDF = ABCDG = CDH = ACDEF = DEG = ... = BCDEFGH**, indicating that A will be confounded with **BCE + BDF + ABCDG + ...**. In this example none of the main effects have been aliased with two-factor interactions. The aliasing is only with 3-factor and higher interaction terms.

.. rubric:: Summary

#.	It is tedious and error prone to calculate the aliasing structure by hand, so computer software is useful in this case.  For example, for the :math:`2^{7-4}` system can be created in  R by first loading the ``BHH2`` package, then using the command ``ffDesMatrix(k=7, gen=list(c(4,1,2), c(5,1,3), c(6,2,3), c(7,1,2,3)))``. See the `R tutorial <https://learnche.org/4C3/Software_tutorial>`_ for more details on how to install packages like BHH2.

#.	The choice of generators is not unique and other choices may lead to a different, more preferable confounding pattern. But it is often easier to use the letters **A, B, C**, *etc*, then just reassign the factors to the letters to achieve the "least-worst" confounding for your situation.

#.	In general, a :math:`2^{k-p}` factorial design is produced by :math:`p` generators and has a defining relationship of :math:`2^p` words.

There is a quick way to calculate if main effects will be confounded with 2fi or 3fi without having to go through the process shown in this section. This is described next when we look at :ref:`design resolution <DOE-design-resolution>`.
