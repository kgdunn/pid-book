.. _DOE-half-fractions:

Half fractions
~~~~~~~~~~~~~~~~~~

A half fraction has :math:`\frac{1}{2}2^k = 2^{k-1}` runs. But which runs do we omit? Let's use an example of a :math:`2^3` full factorial. A half-fraction would have 4 runs. Since 4 runs can be represented by a :math:`2^2` factorial, we start by writing down the usual :math:`2^2` factorial for 2 factors (**A** and **B**), then construct the :math:`3^\text{rd}` factor as the product of the first two (**C** = **AB**).


.. tabularcolumns:: |c||c|c|c|

+-----------+------------+-----------+------------+
| Experiment| A          | B         |  C = AB    |
+===========+============+===========+============+
| 1         | |-|        | |-|       |  |+|       |
+-----------+------------+-----------+------------+
| 2         | |+|        | |-|       |  |-|       |
+-----------+------------+-----------+------------+
| 3         | |-|        | |+|       |  |-|       |
+-----------+------------+-----------+------------+
| 4         | |+|        | |+|       |  |+|       |
+-----------+------------+-----------+------------+

So this is our designed experiment for 3 factors, but it only requires 4 experiments as shown by the open points. The experiments given by the solid points are not run.

.. youtube:: https://www.youtube.com/watch?v=yddiDn_0vww&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=43

.. image:: ../../figures/doe/half-fraction-in-3-factors.png
	:align: center
	:scale: 35
	:width: 900px
	:alt: fake width

What have we lost by running only half the factorial?  Let's write out the full design and matrix of all interactions, then construct the :math:`\mathbf{X}` matrix for the least squares model.

.. tabularcolumns:: |c||c|c|c||c|c|c|c|c|

=========== ============ =========== ============ ============ ============ ============ ============ ============
Experiment  A            B           C            AB           AC           BC           ABC          Intercept 
=========== ============ =========== ============ ============ ============ ============ ============ ============
 1          |-|          |-|         |+|          |+|          |-|          |-|          |+|          |+|       
 2          |+|          |-|         |-|          |-|          |-|          |+|          |+|          |+|       
 3          |-|          |+|         |-|          |-|          |+|          |-|          |+|          |+|       
 4          |+|          |+|         |+|          |+|          |+|          |+|          |+|          |+|       
=========== ============ =========== ============ ============ ============ ============ ============ ============

Before even constructing the :math:`\mathbf{X}`-matrix, you can see that **A=BC**, and that **B=AC** and **C=AB** (this last association was intentional), and **I=ABC**. The least squares model would be:

.. math::

	\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}\\
	       y_i &=  b_0 + b_A x_A + b_B x_B + b_C x_C + b_{AB} x_{AB} + b_{AC} x_{AC} + b_{BC} x_{BC} + b_{ABC} x_{ABC} + e_i\\
	\begin{bmatrix} y_1\\ y_2\\ y_3 \\ y_4 \end{bmatrix} &=
	\begin{bmatrix} 1 & -1 & -1 & +1 & +1 & -1 & -1 & +1\\ 
					1 & +1 & -1 & -1 & -1 & -1 & +1 & +1\\
					1 & -1 & +1 & -1 & -1 & +1 & -1 & +1\\
					1 & +1 & +1 & +1 & +1 & +1 & +1 & +1
	\end{bmatrix}
	\begin{bmatrix} b_0 \\ b_A \\ b_B \\ b_{C} \\ b_{AB} \\ b_{AC} \\ b_{BC} \\ b_{ABC} \end{bmatrix} + 
	\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \end{bmatrix}

The :math:`\mathbf{X}` matrix is not orthogonal anymore, so the least squares model cannot be solved by inverting the :math:`\mathbf{X}^T\mathbf{X}` matrix. Also note this system is underdetermined as there are more unknowns than equations. But notice that 4 of the columns are the same as the other 4 (we have perfect collinearity between 4 pairs of columns).

We can reformulate the model to obtain independent columns, where there are now 4 equations and 4 unknowns:

.. math::

	\mathbf{y} &= \mathbf{X} \mathbf{b} + \mathbf{e}\\
	\begin{bmatrix} y_1\\ y_2\\ y_3 \\ y_4 \end{bmatrix} &=
	\begin{bmatrix} 1 & -1 & -1 & +1  \\ 
					1 & +1 & -1 & -1  \\
					1 & -1 & +1 & -1  \\
					1 & +1 & +1 & +1  
	\end{bmatrix}
	\begin{bmatrix} b_0 + b_{ABC} \\ b_A + b_{BC} \\ b_B + b_{AC} \\ b_{C} + b_{AB} \end{bmatrix} + 
	\begin{bmatrix} e_1\\ e_2\\ e_3 \\ e_4 \end{bmatrix}

Writing it this way clearly shows how the main effects and two-factor interactions are *confounded*. 

	-	:math:`\widehat{\beta}_0 \rightarrow` **I + ABC**
	
	-	:math:`\widehat{\beta}_A \rightarrow` **A + BC** : this implies :math:`\beta_A` estimates the **A** main effect and the **BC** interaction
	
	-	:math:`\widehat{\beta}_B \rightarrow` **B + AC**
	
	-	:math:`\widehat{\beta}_C \rightarrow` **C + AB**
	
	
We cannot separate the effect of the **BC** interaction from the main effect **A**: the least-squares coefficient is a sum of both these effects. Similarly for the other pairs. This is what we have lost by running a half-fraction.

We introduce the terminology that **A** is an :index:`alias <pair: aliasing; experiments>` for **BC**, similarly that **B** is an alias for **AC**, *etc*, because we cannot separate these aliased effects.

.. This last :math:`k^\text{th}` factor will be confounded with one of the 2-factor interaction???
