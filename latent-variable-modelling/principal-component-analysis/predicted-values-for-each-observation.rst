.. _LVM_geometric_predictions:

Predicted values for each observation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An interesting aspect of a PCA model is that it provides an estimate of each observation in the data set. Recall the latent variable model was oriented to create the best-fit plane to the data. This plane was oriented to minimize the errors, which implies the best estimate of each observation is its *perpendicular projection* onto the model plane.

Referring to the illustration and assume we have a PCA model with a single component, the best estimate of observation :math:`\mathbf{x}_i` is the point along the direction vector, |p1|, where the original observation is projected. Recall that the distance along that direction vector was :math:`t_{i,1}`, but the actual point along |p1| is a vector, and it is our best estimate of the original observation. We will call that estimate :math:`\widehat{\mathbf{x}}_{i,1}`, indicating that it is an estimate of :math:`\mathbf{x}_i` along the first component.

.. image:: ../../figures/pca/prediction-along-a-vector.png
	:alt:	../../figures/pca/prediction-along-a-vector.svg
	:align: center
	:scale: 50
	:width: 500px

Since :math:`\widehat{\mathbf{x}}_{i,1}` is a vector, we can write it as the product of a magnitude value and a direction vector. The magnitude of :math:`\widehat{\mathbf{x}}_i` is :math:`t_i` in the direction of |p1|, which is a unit vector, then mathematically we can write:

.. math::
	\widehat{\mathbf{x}}_{i,1}' &= t_{i,1} \,\,\mathbf{p}'_1 \\
	(1 \times K) &= (1 \times 1)(1 \times K)
		
This is the best prediction of the original observation using one component. If we added a second component to our model, then our estimate improves:

.. math::
	\widehat{\mathbf{x}}_{i,2}' &= t_{i,1}\,\, \mathbf{p}'_1 + t_{i,2}\,\, \mathbf{p}'_2 \\
	(1 \times K) &= (1 \times K) + (1 \times K)

With multiple components, we write:

.. math::
	\widehat{\mathbf{x}}_{i,A}' &= \begin{bmatrix}t_{i,1} & t_{i,2}, \,\,\ldots, \,\, t_{i,A} \end{bmatrix} \mathbf{P}'\\
	\widehat{\mathbf{x}}_{i,A}' &= \mathbf{t}'_i \, \mathbf{P}'\\
	(1 \times K) &= (1 \times A) (A \times K)

This is interesting: :math:`\widehat{\mathbf{x}}_{i,A}` is a prediction of every variable in the :math:`i^\text{th}` observation. We only require the score values for that :math:`i^\text{th}` observation in order to get this prediction. We multiply the scores :math:`\mathbf{t}_i` by the direction vectors in matrix |P| to get the prediction. 

.. TODO: image here showing vector arms

The preceding equation can be written in a way that handles the entire matrix |X|:

.. math:: 
	\widehat{\mathbf{X}} &= \mathbf{T}\mathbf{P}'\\
	(N \times K) &= (N \times A) (A \times K)
	:label: LVM-X-hat-prediction-PCA

Once we have the predicted value for an observation, we are also interested in the residual vector between the actual and predicted observation:

.. math::
	\mathbf{e}'_{i,A} &= \mathbf{x}'_i - \widehat{\mathbf{x}}'_{i,A} \\
	(1 \times K) &= (1 \times K) - (1 \times K)

.. You can add this to the above, but it doesn't advance the concepts for this particular section. Rather leave it out for now.		
	\mathbf{e}_{i,A}'  &= \mathbf{x}'_i - \mathbf{t}'_i \mathbf{P}' \\
					   &= \mathbf{x}'_i - \mathbf{x}'_i \mathbf{P} \mathbf{P}' \\
					   &= \mathbf{x}'_i \left(I_{K \times K} - \mathbf{P} \mathbf{P}' \right)

The residual *length* or *distance* is the sum of squares of this residual, then we take the square root to form a distance. Technically the *squared prediction error* (SPE) is just the sum of squares for each observation, but often we refer to the square root of this quantity as the SPE as well. Some software packages will scale the root of the SPE by some value; you will see this referred to as the DModX, distance to the model plane for |X|. 

.. math::
	\text{SPE}_i &= \sqrt{\mathbf{e}'_{i,A} \mathbf{e}_{i,A}} \\
	(1 \times 1) &= (1 \times K)(K \times 1)
	
where :math:`\mathbf{e}_{i,A}` is the residual vector of the :math:`i^\text{th}` observation using :math:`A` components.

