.. _LVM-PCA-properties:

Some properties of PCA models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..	Show the 3D to 2D projection

We summarize various properties of the PCA model, most have been described in the previous sections. Some are only of theoretical interest, but others are more practical.

*	The model is defined by the direction vectors, or loadings vectors, called :math:`\mathbf{p}_1, \mathbf{p}_2, \ldots, \mathbf{p}_A`; each are a :math:`K \times 1` vector, and can be collected into a single matrix, :math:`\mathbf{P}`, a :math:`K \times A` loadings matrix.

*	These vectors form a line for one component, a plane for 2 components, and a hyperplane for 3 or more components. This line, plane or hyperplane define the latent variable model.

*	An equivalent interpretation of the model plane is that these direction vectors are oriented in such a way that the scores have maximal variance for that component. No other directions of the loading vector (i.e. no other hyperplane) will give a greater variance.

*	This plane is calculated with respect to a given data set, |X|, an :math:`N \times K` matrix, so that the direction vectors best-fit the data. We can say then that with one component, the best estimate of the original matrix |X| is:

	.. math::
		\widehat{\mathbf{X}}_1 = \mathbf{t}_1 \mathbf{p}_1 \qquad \text{or equivalently:} \qquad \mathbf{X}_1 = \mathbf{t}_1 \mathbf{p}_1 + \mathbf{E}_1
		
	where :math:`\mathbf{E}_1` is the residual matrix after fitting one component. The estimate for |X| will have smaller residuals if we fit a second component:
	
	.. math::
		\widehat{\mathbf{X}}_2 = \mathbf{t}_1 \mathbf{p}_1 + \mathbf{t}_2 \mathbf{p}_2 \qquad \text{or equivalently:} \qquad \mathbf{X}_2 = \mathbf{t}_1 \mathbf{p}_1 + \mathbf{t}_1 \mathbf{p}_1 + \mathbf{E}_2
		
	In general we can illustrate this:
	
		.. image:: ../../figures/pca/decomposition-of-PCA-X-matrix.png
			:alt:	../../figures/pca/decomposition-of-PCA-X-matrix.svg
			:scale: 75
			:width: 750px
			:align: center
			
			
*	The loadings vectors are of unit length: :math:`\| \mathbf{p}_a \| = \sqrt{\mathbf{p}'_a \mathbf{p}_a} = 1.0`

*	The loading vectors are independent or orthogonal to one another: :math:`\mathbf{p}'_i \mathbf{p}_j  = 1.0` for :math:`i \neq j`; in other words :math:`\mathbf{p}_i \perp \mathbf{p}_j`.

*	Orthonormal matrices have the property that :math:`\mathbf{P}'\mathbf{P} = \mathbf{I}_A`, an identity matrix of size :math:`A \times A`.

*	These last 3 properties imply that :math:`\mathbf{P}` is an orthonormal matrix. From matrix algebra and geometry you will recall that this means |P| is a rigid rotation matrix. We are rotating our real-world data in |X| to a new set of values, scores, using the rotation matrix |P|. But a rigid rotation implies that distances and angles between observations are preserved. Practically, this means that by looking at our data in the score space, points which are close together in the original :math:`K` variables will be close to each other in the scores, :math:`\mathbf{T}`, now reduced to :math:`A` variables.
	
*	The variance of the :math:`\mathbf{t}_1` vector must be greater than the variance of the :math:`\mathbf{t}_2` vector. This is because we intentionally find the components in this manner. In our notation: :math:`s_1 > s_2 > \ldots > s_A`, where :math:`s_a` is the standard deviation of the :math:`a^\text{th}` score.

*	The maximum number of components that can be extracted is the smaller of :math:`N` or :math:`K`; but usually we will extract only :math:`A \ll K` number of components. If we do extract all components, :math:`A^* = \min(N, K)`, then our loadings matrix, |P|, merely rotates our original coordinate system to a new system without error.

*	The eigenvalue decomposition of :math:`\mathbf{X}'\mathbf{X}` gives the loadings, |P|, as the eigenvectors, and the eigenvalue for each eigenvector is the variance of the score vector.

* 	The singular value decomposition of |X| is given by :math:`\mathbf{X} = \mathbf{U \Sigma V}'`, so :math:`\mathbf{V}' = \mathbf{P}'` and :math:`\mathbf{U\Sigma} = \mathbf{T}`, showing the equivalence between PCA and this method.

*	If there are no missing values in |X|, then the mean of each score vector is 0.0, which allows us to calculate the variance of each score simply from :math:`\mathbf{t}'_a \mathbf{t}_a`.

*	Notice that some score values are positive and others negative. Each loading direction, :math:`\mathbf{p}_a`, must point in the direction that best explains the data; but this direction is not unique, since :math:`-\mathbf{p}_a` also meets this criterion. If we did select :math:`-\mathbf{p}_a` as the direction, then the scores would just be :math:`-\mathbf{t}_a` instead. This does not matter too much, because :math:`(-\mathbf{t}_a)(-\mathbf{p}'_a) = \mathbf{t}_a \mathbf{p}'_a`, which is used to calculate the predicted |X| and the residuals. But this phenomena can lead to a confusing situation for newcomers when different computer packages give different-looking loading plots and score plots for the same data set. 

