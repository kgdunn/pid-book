.. _LVM_algorithms_for_PCA:

Algorithms to calculate (build) PCA models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The different algorithms used to build a PCA model provide a different insight into the model's structure and how to interpret it. These algorithms are a reflection of how PCA has been used in different disciplines: PCA is called by different names in each area.

.. _LVM-eigenvalue-decomposition:

Eigenvalue decomposition
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Note:: The purpose of this section is not the theoretical details, but rather the interesting interpretation of the PCA model that we obtain from an eigenvalue decomposition.

Recall that the latent variable directions (the loading vectors) were oriented so that the variance of the scores in that direction were maximal. We can cast this as an optimization problem. For the first component:

.. math:: 
	  \max        \quad & \phi = \mathbf{t}'_1 \mathbf{t}_1 = \mathbf{p}'_1\mathbf{X}' \mathbf{X} \mathbf{p}_1 \\
	  \text{s.t.} \quad &  \mathbf{p}'_1 \mathbf{p}_1 = 1

This is equivalent to :math:`\max \,\, \phi = \mathbf{p}'_1 \mathbf{X}' \mathbf{X} \mathbf{p}_1 - \lambda \left(\mathbf{p}'_1 \mathbf{p}_1 - 1\right)`, because we can move the constraint into the objective function with a Lagrange multiplier, :math:`\lambda_1`.

The maximum value must occur when the partial derivatives with respect to :math:`\mathbf{p}_1`, our search variable, are zero:

.. math::
	  \dfrac{\partial \phi}{\partial \mathbf{p}_1} &= \mathbf{0} = \mathbf{p}'_1 \mathbf{X}' \mathbf{X} \mathbf{p}_1 - \lambda_1\left(\mathbf{p}'_1 \mathbf{p}_1 - 1\right) \\
										\mathbf{0} &= 2 \mathbf{X}' \mathbf{X} \mathbf{p}_1 - 2\lambda_1 \mathbf{p}_1 \\
										\mathbf{0} &= (\mathbf{X}' \mathbf{X} - \lambda_1 I_{K\times K}) \mathbf{p}_1 \\
										\mathbf{X}' \mathbf{X}\mathbf{p}_1  &= \lambda_1 \mathbf{p}_1

which is just the eigenvalue equation, indicating that :math:`\mathbf{p}_1` is the eigenvector of :math:`\mathbf{X}' \mathbf{X}` and :math:`\lambda_1` is the eigenvalue. One can show that :math:`\lambda_1 = \mathbf{t}'_1 \mathbf{t}_1`, which is proportional to the variance of the first component.

In a similar manner we can calculate the second eigenvalue, but this time we add the additional constraint that :math:`\mathbf{p}_1 \perp \mathbf{p}_2`. Writing out this objective function and taking partial derivatives leads to showing that :math:`\mathbf{X}' \mathbf{X}\mathbf{p}_2 = \lambda_2 \mathbf{p}_2`. 

From this we learn that:

	*	The loadings are the eigenvectors of :math:`\mathbf{X}'\mathbf{X}`.
	
	*	Sorting the eigenvalues in order from largest to smallest gives the order of the corresponding eigenvectors, the loadings.
	
	*	We know from the theory of eigenvalues that if there are distinct eigenvalues, then their eigenvectors are linearly independent (orthogonal).
	
	*	We also know the eigenvalues of :math:`\mathbf{X}'\mathbf{X}` must be real values and positive; this matches with the interpretation that the eigenvalues are proportional to the variance of each score vector.
	
	*	Also, the sum of the eigenvalues must add up to sum of the diagonal entries of :math:`\mathbf{X}'\mathbf{X}`, which represents of the total variance of the :math:`\mathbf{X}` matrix, if all eigenvectors are extracted. So plotting the eigenvalues is equivalent to showing the proportion of variance explained in :math:`\mathbf{X}` by each component. This is not necessarily a good way to judge the number of components to use, but it is a rough guide: use a Pareto plot of the eigenvalues (though in the context of eigenvalue problems, this plot is called a :index:`scree plot`).

		.. image:: ../../figures/pca/eigenvalue-scree-plot.png
			:alt:	../../figures/pca/eigenvalue-scree-plot.R
			:align: center
			:scale: 70
			:width: 700px

..	Good references for scree plots: 
..		Mardia, K. V., J. T. Kent and J. M. Bibby (1979). Multivariate Analysis, London: Academic Press.
..		Venables, W. N. and B. D. Ripley (2002). Modern Applied Statistics with S, Springer-Verlag.

The general approach to using the eigenvalue decomposition would be:

	#.	Preprocess the raw data, particularly centering and scaling, to create a matrix :math:`\mathbf{X}`.
	#.	Calculate the correlation matrix :math:`\mathbf{X}'\mathbf{X}`.
	#.	Calculate the eigenvectors and eigenvalues of this square matrix and sort the results from largest to smallest eigenvalue.
	#.	A rough guide is to retain only the first :math:`A` eigenvectors (loadings), using a Scree plot of the eigenvalues as a guide. Alternative methods to determine the number of components are described in the section on cross-validation and randomization.

However, we should note that calculating the latent variable model using an eigenvalue algorithm is usually not recommended, since it calculates all eigenvectors (loadings), even though only the first few will be used. The maximum number of components possible is :math:`A_\text{max} = \min(N, K)`. Also, the default eigenvalue algorithms in software packages cannot handle missing data.
	
Singular value decomposition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. TODO: Provide additional insight here on how this is equivalent to rotation, scaling, rotation: break down the data into these 3 SVD components

The singular value decomposition (SVD), in general, decomposes a given matrix |X| into three other matrices:

.. math::
	\mathbf{X} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}'
	
Matrices :math:`\mathbf{U}` and :math:`\mathbf{V}` are orthonormal (each column has unit length and each column is orthogonal to the others), while :math:`\mathbf{\Sigma}` is a diagonal matrix. The relationship to principal component analysis is that:

.. math::
	\mathbf{X} = \mathbf{T}  \mathbf{P}'
	
where matrix :math:`\mathbf{P}` is also orthonormal. So taking the SVD on our preprocessed matrix |X| allows us to get the PCA model by setting :math:`\mathbf{P} = \mathbf{V}`, and :math:`\mathbf{T} = \mathbf{U} \mathbf{\Sigma}`. The diagonal terms in :math:`\mathbf{\Sigma}` are related to the variances of each principal component and can be plotted as a scree plot, as was done for the :ref:`eigenvalue decomposition <LVM-eigenvalue-decomposition>`. 

Like the eigenvalue method, the SVD method calculates all principal components possible, :math:`A=\min(N, K)`, and also cannot handle missing data by default.

.. _LVM_PCA_NIPALS_algorithm:

Non-linear iterative partial least-squares (NIPALS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ADD arrow diagram, with numeric labels next to arrows, as in the PLS section.

The non-linear iterative partial least squares (NIPALS) algorithm is a sequential method of computing the principal components. The calculation may be terminated early, when the user deems that enough components have been computed. Most computer packages tend to use the NIPALS algorithm as it has two main advantages: it handles missing data and calculates the components sequentially.

The purpose of considering this algorithm here is three-fold:  it gives additional insight into what the loadings and scores mean; it shows how each component is independent of (orthogonal to) the other components, and it shows how the algorithm can handle missing data.

The algorithm extracts each component sequentially, starting with the first component, direction of greatest variance, and then the second component, and so on.

We will show the algorithm here for the :math:`a^\text{th}` component, where :math:`a=1` for the first component. The matrix |X| that we deal with below is the :ref:`preprocessed <LVM_preprocessing>`, usually centered and scaled matrix, not the raw data.

#.	The NIPALS algorithm starts by arbitrarily creating an initial column for :math:`\mathbf{t}_a`. You can use a column of random numbers, or some people use a column from the |X| matrix; anything can be used as long as it is not a column of zeros.

#.	Then we take every column in |X|, call it :math:`\mathbf{X}_k`, and regress it onto this initial column :math:`\mathbf{t}_a`;  store the regression coefficient as the entry in :math:`p_{k,a}`. What this means, and it is illustrated below, is that we perform an ordinary least squares regression (:math:`\mathbf{y} = \beta \mathbf{x}`), except our |x|-variable is this column of :math:`\mathbf{t}_a` values, and our |y|-variable is the particular column from |X|.

	.. image:: ../../figures/pca/NIPALS-iterations-columns.png
		:alt:	../../figures/pca/NIPALS-iterations-PCA.svg
		:scale: 35
		:width: 750px
		:align: center

	For ordinary least squares, you will remember that the solution for this regression problem is :math:`\widehat{\beta} = \dfrac{\mathbf{x'y}}{\mathbf{x'x}}`. Using our notation, this means:

	.. math::
		p_{k,a} = \dfrac{\mathbf{t}'_a \mathbf{X}_k}{\mathbf{t}'_a\mathbf{t}_a}

	This is repeated for each column in |X| until we fill the entire vector :math:`\mathbf{p}_k`. This is shown in the illustration where each column from |X| is regressed, one at a time, on :math:`\mathbf{t}_a`, to calculate the loading entry, :math:`p_{k,a}`   In practice we don't do this one column at time; we can regress all columns in |X| in go: :math:`\mathbf{p}'_a = \dfrac{1}{\mathbf{t}'_a\mathbf{t}_a} \cdot \mathbf{t}'_a \mathbf{X}_a`, where :math:`\mathbf{t}_a` is an :math:`N \times 1` column vector, and :math:`\mathbf{X}_a` is an :math:`N \times K` matrix, explained more clearly in step 6.

#.	The loading vector :math:`\mathbf{p}'_a` won't have unit length (magnitude) yet. So we simply rescale it to have magnitude of 1.0:

	.. math::
		\mathbf{p}'_a = \dfrac{1}{\sqrt{\mathbf{p}'_a \mathbf{p}_a}} \cdot \mathbf{p}'_a  

#.	The next step is to regress every row in |X| onto this normalized loadings vector. As illustrated below, in our linear regression the rows in |X| are our |y|-variable each time, while the loadings vector is our |x|-variable. The regression coefficient becomes the score value for that :math:`i^\text{th}` row:

	.. image:: ../../figures/pca/NIPALS-iterations-rows.png
		:alt:	../../figures/pca/NIPALS-iterations-PCA.svg
		:scale: 35
		:width: 750px
		:align: center

	.. math::
		t_{i,a} = \dfrac{\mathbf{x}'_i \mathbf{p}_a}{\mathbf{p}'_a\mathbf{p}_a}
		
	where :math:`\mathbf{x}'_i` is an :math:`K \times 1` column vector. We can combine these :math:`N` separate least-squares models and calculate them in one go to get the entire vector, :math:`\mathbf{t}_a = \dfrac{1}{\mathbf{p}'_a\mathbf{p}_a} \cdot \mathbf{X} \mathbf{p}_a`, where :math:`\mathbf{p}_a` is a :math:`K \times 1` column vector.

#.	We keep iterating steps 2, 3 and 4 until the change in vector :math:`\mathbf{t}_a` from one iteration to the next is small (usually around :math:`1 \times 10^{-6}` to :math:`1 \times 10^{-9}`). Most data sets require no more than 200 iterations before achieving convergence.

#.	On convergence, the score vector and the loading vectors, :math:`\mathbf{t}_a` and :math:`\mathbf{p}_a` are stored as the :math:`a^\text{th}` column in matrix :math:`\mathbf{T}` and :math:`\mathbf{P}` respectively. We then deflate the |X| matrix. This crucial step removes the variability captured in this component (:math:`\mathbf{t}_a` and :math:`\mathbf{p}_a`) from |X|:

	.. math::
		\mathbf{E}_a &= \mathbf{X}_{a} - \mathbf{t}_a \mathbf{p}'_a \\
		\mathbf{X}_{a+1} &= \mathbf{E}_a
		
	For the first component, :math:`\mathbf{X}_{a}` is just the preprocessed raw data. So we can see that the second component is actually calculated on the residuals :math:`\mathbf{E}_1`, obtained after extracting the first component.
	
	This is called *deflation*, and nicely shows why each component is orthogonal to the others. Each subsequent component is only seeing variation remaining after removing all the others; there is no possibility that two components can explain the same type of variability.
	
	After deflation we go back to step 1 and repeat the entire process for the next component. Just before accepting the new component we can use a test, such as a randomization test, or :ref:`cross-validation <LVM_number_of_components>`, to decide whether to keep that component or not.
	
The final reason for outlining the NIPALS algorithm is to show one way in which missing data can be handled. All that step 2 and step 4 are doing is a series of regressions. Let's take step 2 to illustrate, but the same idea holds for step 4. In step 2, we were regressing columns from |X| onto the score :math:`\mathbf{t}_a`. We can visualize this for a hypothetical system below

There are 3 missing observations (open circles), but despite this, the regression's slope can still be adequately determined. The slope is unlikely to change by very much if we did have the missing values. In practice though we have no idea where these open circles would fall, but the principle is the same: we calculate the slope coefficient just ignoring any missing entries.

.. image:: ../../figures/pca/NIPALS-with-missing-values.png
	:alt:	../../figures/pca/NIPALS-with-missing-values.svg
	:scale: 30
	:width: 750px
	:align: center
	
In summary:

	*	The NIPALS algorithm computes one component at a time. The first component computed is equivalent to the :math:`\mathbf{t}_1` and |p1| vectors that would have been found from an eigenvalue or singular value decomposition.
	
	*	The algorithm can handle missing data in |X|.
	
	*	The algorithm always converges, but the convergence can sometimes be slow.
	
	*	It is also known as the Power algorithm to calculate eigenvectors and eigenvalues.
	
	*	It works well for very large data sets.
	
	*	It is used by most software packages, especially those that handle missing data.
	
	*	Of interest: it is well known that Google used this algorithm for the early versions of their search engine, `called PageRank <http://ilpubs.stanford.edu:8090/422/>`_.
	
.. Kernel methods for PCA
.. ^^^^^^^^^^^^^^^^^^^^^^

..	We will also mention here, but not go into the details of kernel algorithms. For example, when we have long and narrow |X| matrix of size :math:`N \times K` we can calculate a kernel matrix, :math:`\mathbf{X}'\mathbf{X}` which then has size :math:`K \times K`. This is a much, much smaller matrix to work with than the original :math:`N \times N` matrix. The eigenvalue decomposition on :math:`\mathbf{X}'\mathbf{X}` will yield eigenvectors which are just the loadings :math:`\mathbf{P}`. Once we have the loadings, then we can calculate the scores: :math:`\mathbf{T}=\mathbf{X}\mathbf{P}`.

	For short and wide matrices where :math:`N << K` we can form the matrix of squares and cross-products, :math:`\mathbf{X}\mathbf{X}'`, an :math:`N \times N` matrix. Had we calculated the singular value decomposition on matrix |X|, where we have set :math:`A = \min(N,K)`,  we would have obtained:

	.. math::
		\mathbf{X}   &= \mathbf{U} \mathbf{\Sigma} \mathbf{V}'
		(N \times K) &= (N \times A)(A \times A)(A \times K)

	and we showed earlier that :math:`\mathbf{V}' = \mathbf{P}'`, which is an orthonormal matrix. Now write:

	.. math::
		\mathbf{X}\mathbf{X}' &= \mathbf{U} \mathbf{\Sigma} \mathbf{V}' (\mathbf{U} \mathbf{\Sigma} \mathbf{V}')' \\
		\mathbf{X}\mathbf{X}' &= \mathbf{U} \mathbf{\Sigma} \mathbf{V}' \mathbf{V} \mathbf{\Sigma}' \mathbf{U}' \\
		\mathbf{X}\mathbf{X}' &= \mathbf{U} (\mathbf{\Sigma} \mathbf{\Sigma}') \mathbf{U}' \\
		(N \times N)          &= (N \times A)(N \times A)(A \times N) 
		
	This indicates that if we take the singular value decomposition on the small matrix :math:`\mathbf{X}\mathbf{X}'` that the left singular vectors in :math:`\mathbf{U}` are the scores.
	How do we get the loadings?  
		If we have calculated all the scores (A = N): X = TP' + 0; inv(T)X = inv(T)TP' = P' ?
		p'_i = t'_i X, and normalize p_i to unit length
	
	Lindgren, Geladi, Wold; J Chemo, 1993
	Rannar, Lingren and Geladi, J Chemo, 1994
	DeJong and TerBraak, J Chemo, 1994
	Dayal and MacGregor, J Chemo 1997: deflate only one
	

