Latent variable contribution plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have :ref:`previously seen <LVM_mathematical_geometric_derivation>` how :index:`contribution plots` are constructed for a score value, for the SPE and for |T2|. We breakdown the value, such as SPE, into its individual terms, one from each variable. Then we plot these |K| contribution values as a bar chart. 

There are :math:`K` contribution terms for a score: :math:`t_{i,a} = \mathbf{x}_{i} \mathbf{p}_a`:

.. math::
	\begin{bmatrix}x_{i,1} \,\, p_{1,a} & x_{i,2} \,\, p_{2,a} & \ldots & x_{i,k} \,\, p_{k,a} & \ldots & x_{i,K} \,\, p_{K,a} \end{bmatrix}

The contribution to |T2| is similar to a score contribution, except we calculate the weighted summation over all the scores, :math:`t_{i,a}`, where the weights are the variances of the :math:`a^\text{th}` score.

For SPE = :math:`\sqrt{\mathbf{e}'_{i}\mathbf{e}_{i}}`, where :math:`\mathbf{e}'_{i} = \mathbf{x}'_i - \widehat{\mathbf{x}}'_{i}`, the bars in the contribution plots are:

.. math::
	\begin{bmatrix}(x_{i,1} - \hat{x}_{i,1}) & (x_{i,2} - \hat{x}_{i,2}) & \ldots & (x_{i,k} - \hat{x}_{i,k}) &  \ldots & (x_{i,K} - \hat{x}_{i,K})\end{bmatrix}
	
The SPE contributions are usually shown as the square of the values in brackets, accounting for the sign, as in :math:`e_{i,k} = (x_{i,k} - \hat{x}_{i,k})`, and then plot each bar: :math:`\text{sign}(e_{i,k}) \times e^2_{i,k}`. The squared values are more realistic indicators of the contributions, while the sign information might be informative in some cases.
	
The other point to mention here is that contributions are calculated *from* one point *to* another point. Most often, the *from* point is the model center or the model plane. So for SPE, the contributions are *from* the model plane *to* the :math:`i^\text{th}` observation off the model plane. The score contributions are *from* the model center *to* the observation's projection on the (hyper)plane. 

But sometimes we would like to know, as in the figure below, what are the contribution from one point to another. And these start and end points need not be an actual point; for a group of points we can use a suitable average of the points in the cluster. So there are point-to-point, point-to-group, group-to-point, and group-to-group contributions in the scores.

.. image:: ../../figures/concepts/contributions/contribution-plots-in-the-scores.png
	:alt:	../../figures/concepts/contributions/contribution-plots-in-the-scores.svg
	:scale: 70
	:width: 750px
	:align: center

The calculation procedure is actually the same in all cases: for a group of points, collapse it down to the center point in the group, then calculate the point-to-point contribution. If the starting point is not specified, then the contribution will be from the model center, i.e. :math:`(t_i, t_j) = (0, 0)` to the point.
