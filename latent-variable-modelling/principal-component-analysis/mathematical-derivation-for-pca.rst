.. _LVM_mathematical_geometric_derivation:

Mathematical derivation for PCA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Geometrically, when finding the *best-fit line* for the swarm of points, our objective was to minimize the error, i.e. the residual distances from each point to the best-fit line is the smallest possible. This is also mathematically equivalent to maximizing the variance of the scores, :math:`\mathbf{t}_a`.

..	See Normal Cliff, Analyzing Multivariate Data, 1987, p 295 to 300

We briefly review here what that means. Let :math:`\mathbf{x}'_i` be a row from our data, so :math:`\mathbf{x}'_i` is a :math:`1 \times K` vector. We defined the score value for this observation as the distance from the origin, along the direction vector, |p1|, to the point where we find the perpendicular projection onto |p1|. This is illustrated below, where the score value for observation :math:`\mathbf{x}_i` has a value of :math:`t_{i,1}`.

.. figure:: ../../figures/pca/component-along-a-vector.png
	:alt:	../../figures/pca/component-along-a-vector.svg
	:align: center
	:width: 500px
	:scale: 50

Recall from geometry that the cosine of an angle in a right-angled triangle is the ratio of the adjacent side to the hypotenuse. But the cosine of an angle is also used in linear algebra to define the dot-product. Mathematically:

.. math::	
	\cos \theta = \dfrac{\text{adjacent length}}{\text{hypotenuse}} = \dfrac{t_{i,1}}{\| \mathbf{x}_i\|} \qquad &\text{and also} \qquad \cos \theta = \dfrac{\mathbf{x}'_i \mathbf{p}_1}{\|\mathbf{x}_i\| \|\mathbf{p}_1\|} \\
	\dfrac{t_{i,1}}{\| \mathbf{x}_i\|} &= \dfrac{\mathbf{x}'_i \mathbf{p}_1}{\|\mathbf{x}_i\| \|\mathbf{p}_1\|} \\
	t_{i,1} &= \mathbf{x}'_i \mathbf{p}_1 \\
	(1 \times 1) &= (1 \times K)(K \times 1)
		
where :math:`\| \cdot \|` indicates the length of the enclosed vector, and the length of the direction vector, |p1| is 1.0, by definition.

Note that :math:`t_{i,1} = \mathbf{x}'_i \mathbf{p}_1` represents a :ref:`linear combination <LVM_linear_combination>`

.. math:: 
	t_{i,1} = x_{i,1} p_{1,1} + x_{i,2} p_{2,1} + \ldots + x_{i,k} p_{k,1}  + \ldots + x_{i,K} p_{K,1}

So :math:`t_{i,1}` is the score value for the :math:`i^\text{th}` observation along the first component, and is a linear combination of the :math:`i^\text{th}` row of data, :math:`\mathbf{x}_i` and the direction vector |p1|. Notice that there are :math:`K` terms in the linear combination: each of the :math:`K` variables *contributes* to the overall score.

We can calculate the second score value for the :math:`i^\text{th}` observation in a similar way:

.. math:: 
	t_{i,2} = x_{i,1} p_{1,2} + x_{i,2} p_{2,2} + \ldots + x_{i,k} p_{k,1}  + \ldots + x_{i,K} p_{K,2}

And so on, for the third and subsequent components. We can compactly write in matrix form for the :math:`i^\text{th}` observation that:

.. math::
	\mathbf{t}'_i &= \mathbf{x}'_i \mathbf{P} \\
	(1 \times A)   &= (1 \times K)(K \times A)

which calculates all :math:`A` score values for that observation in one go. This is exactly what we :ref:`derived earlier <LVM_linear_combination>` in the example with the 4 thermometers in the room.

.. _LVM_eqn_LVM-score-values:

Finally, for an entire matrix of data, |X|, we can calculate all scores, for all observations:

.. math::
	\mathbf{T}   &= \mathbf{X} \mathbf{P} \\
	(N \times A) &= (N \times K)(K \times A)
	:label: LVM-score-values

