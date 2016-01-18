More about the direction vectors (loadings)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The direction vectors |p1|, :math:`\mathbf{p}_2` and so on, are each :math:`K \times 1` unit vectors. These are vectors in the original coordinate space (the :math:`K`-dimensional real-world) where the observations are recorded.

But these direction vectors are also our link to the latent-variable coordinate system. These direction vectors create a (hyper)plane that is embedded inside the :math:`K`-dimensional space of the :math:`K` original variables. You will see the terminology of *loadings* - this is just another name for these direction vectors:

.. math::
	\text{Loadings, a $K \times A$ matrix:}\qquad\qquad \mathbf{P} = \begin{bmatrix} \mathbf{p}_1 & \mathbf{p}_2 & \ldots & \mathbf{p}_A \end{bmatrix}

Once this hyperplane is mapped out, then we start to consider how each of the observations lie on this hyperplane. We start to be more and more interested in this reduced dimensional plane, because it is an :math:`A`-dimensional plane, where :math:`A` is often much smaller than :math:`K`. Returning back to the case of the thermometers in a room: we had 4 thermometers (:math:`K=4`), but only one latent variable, :math:`A=1`. Rather than concern ourself with the original 4 measurements, we only focus on the single column of score values, since this single variables is the best summary possible of the 4 original variables.

How do we get the score value(s)? We use the :ref:`equation from the prior section <LVM_eqn_LVM-score-values>` (repeated here). It is the multiplication of the pre-processed data by the loadings vectors:

.. math::
	\mathbf{T}   &= \mathbf{X} \mathbf{P} \\
	(N \times A) &= (N \times K)(K \times A)

and it shows how the loadings are our link from the :math:`K`-dimensional, real-world, coordinate system to the :math:`A`-dimensional, latent variable-world, coordinates.

Let's return to the :ref:`example of the 4 temperatures <LVM_room_temperature_example>`. We derived there that a plausible summary of the 4 temperatures could be found from:

.. math::
	t_1 &= \begin{bmatrix} x_1 & x_2 & x_3 & x_4 \end{bmatrix}\begin{bmatrix} p_{1,1} \\ p_{2,1} \\ p_{3,1} \\ p_{4,1} \end{bmatrix} = \begin{bmatrix} x_1 & x_2 & x_3 & x_4 \end{bmatrix}\begin{bmatrix} 0.25 \\ 0.25 \\ 0.25 \\ 0.25 \end{bmatrix}  = \mathbf{x}_i \mathbf{p}_1

So the loading vector for this example points in the direction :math:`\mathbf{p}'_1 = [0.25, 0.25, 0.25, 0.25]`. This isn't a unit vector though; but we can make it one:

	*	Current magnitude of vector = :math:`\sqrt{0.25^2 + 0.25^2 + 0.25^2 + 0.25^2} = 0.50`
	
	*	Divide the vector by current magnitude: :math:`\mathbf{p}_1 = \dfrac{1}{0.5} \cdot [0.25, 0.25, 0.25, 0.25]`
	
	*	New, unit vector = :math:`\mathbf{p}_1 = [0.5, 0.5, 0.5, 0.5]`
	
	*	Check new magnitude = :math:`\sqrt{0.5^2 + 0.5^2 + 0.5^2 + 0.5^2} = 1.0`

What would be the entries in the |p1| loading vector if we had 6 thermometers? (*Ans* = 0.41; in general, for :math:`K` thermometers, :math:`1/\sqrt{K}`).

This is very useful, because now instead of dealing with :math:`K` thermometers we can reduce the columns of data down to just a single, average temperature. This isn't a particularly interesting case though; you would have likely done this anyway as an engineer facing this problem. But the next :ref:`food texture example <LVM_food_texture_example>` will illustrate a more realistic case.
