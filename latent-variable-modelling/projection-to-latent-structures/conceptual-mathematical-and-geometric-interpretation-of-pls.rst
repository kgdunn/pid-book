.. _LVM-PLS-conceptual-interpretation:

A conceptual explanation of PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that you are comfortable with the concept of a latent variable using PCA and PCR, you can interpret PLS as a latent variable model, but one that has a different objective function. In PCA the objective function was to calculate each latent variable so that it best explains the available variance in :math:`\mathbf{X}_a`, where the subscript |A| refers to the matrix :math:`\mathbf{X}` *before* extracting the :math:`a^\text{th}` component.

In PLS, we also find these latent variables, but we find them so they best explain :math:`\mathbf{X}_a` and best explain :math:`\mathbf{Y}_a`, and so that these latent variables have the strongest possible relationship between :math:`\mathbf{X}_a` and :math:`\mathbf{Y}_a`.

In other words, there are three simultaneous objectives with PLS:

	#. The best explanation of the |X|-space.
	
	#. The best explanation of the |Y|-space.
	
	#. The greatest relationship between the |X|- and |Y|-space.

.. _LVM_PLS_mathematical_interpretation:

A mathematical/statistical interpretation of PLS 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will get back to the :ref:`mathematical details later on <LVM_PLS_calculation>`, but we will consider our conceptual explanation above in terms of mathematical symbols.

In PCA, the objective was to best explain :math:`\mathbf{X}_a`. To do this we calculated scores, |T|, and loadings |P|, so that each component, :math:`\mathbf{t}_a`, had the greatest variance, while keeping the loading direction, :math:`\mathbf{p}_a`, constrained to a unit vector.

.. math::

	\max : \mathbf{t}'_a \mathbf{t}_a \qquad \text{subject to}\quad \mathbf{p}'_a \mathbf{p}_a = 1.0

The above was shown to be a concise mathematical way to state that these scores and loadings best explain |X|; no other loading direction will have greater variance of :math:`\mathbf{t}'_a`. (The scores have mean of zero, so their variance is proportional to :math:`\mathbf{t}'_a \mathbf{t}_a`).

For PCA, for the :math:`a^\text{th}` component, we can calculate the scores as follows (we are projecting the values in :math:`\mathbf{X}_a` onto the loading direction :math:`\mathbf{p}_a`):

.. math::

	\mathbf{t}_a &= \mathbf{X}_a \mathbf{p}_a
	

Now let's look at PLS. Earlier we said that PLS extracts a single set of scores, |T|, from |X| and |Y| simultaneously. That wasn't quite true, but it is still an accurate statement!  PLS actually extracts two sets of scores, one set for |X| and another set for |Y|. We write these scores for each space as:

.. math::
	:nowrap:

	\begin{align*}
	\mathbf{t}_a &= \mathbf{X}_a \mathbf{w}_a \qquad &\text{for the $\mathbf{X}$-space} \\
	\mathbf{u}_a &= \mathbf{Y}_a \mathbf{c}_a \qquad &\text{for the $\mathbf{Y}$-space}
	\end{align*}
	
The objective of PLS is to extract these scores so that they have *maximal covariance*. Let's take a look at this. :ref:`Covariance was shown <LS_covariance>` to be:
	
.. math::

	\text{Cov}\left(\mathbf{t}_a, \mathbf{u}_a\right) = \mathcal{E}\left\{ (\mathbf{t}_a - \overline{\mathbf{t}}_a) (\mathbf{u}_a - \overline{\mathbf{u}}_a)\right\} 
	
Using the fact that these scores have mean of zero, the covariance is proportional (with a constant scaling factor of :math:`N`) to :math:`\mathbf{t}'_a \mathbf{u}_a`. So in summary, each component in PLS is maximizing that covariance, or the dot product: :math:`\mathbf{t}'_a \mathbf{u}_a`.

Now covariance is a hard number to interpret; about all we can say with a covariance number is that the larger it is, the greater the relationship, or *correlation*, between two vectors. So it is actually more informative to rewrite covariance in terms of :ref:`correlations <LS_correlation>` and variances:

.. math::

	\text{Cov}\left(\mathbf{t}_a, \mathbf{u}_a\right) &= \text{Correlation}\left(\mathbf{t}_a, \mathbf{u}_a\right) \times \sqrt{\text{Var}\left(\mathbf{t}_a\right)}\times \sqrt{\text{Var}\left(\mathbf{u}_a\right)} \\
	\text{Cov}\left(\mathbf{t}_a, \mathbf{u}_a\right) &= \text{Correlation}\left(\mathbf{t}_a, \mathbf{u}_a\right) \times \sqrt{\mathbf{t}'_a \mathbf{t}_a}  \times \sqrt{\mathbf{u}'_a \mathbf{u}_a} \\

As this shows then, maximizing the covariance between :math:`\mathbf{t}'_a` and :math:`\mathbf{u}_a` is actually maximizing the 3 simultaneous objectives mentioned earlier:

	#. The best explanation of the |X|-space: given by :math:`\mathbf{t}'_a \mathbf{t}_a`
	
	#. The best explanation of the |Y|-space. given by :math:`\mathbf{u}'_a \mathbf{u}_a`
	
	#. The greatest relationship between the |X|- and |Y|-space: given by :math:`\text{correlation}\left(\mathbf{t}_a, \mathbf{u}_a\right)`

These scores, :math:`\mathbf{t}'_a` and :math:`\mathbf{u}_a`, are found subject to the constraints that :math:`\mathbf{\mathbf{w}'_a \mathbf{w}_a} = 1.0` and :math:`\mathbf{\mathbf{c}'_a \mathbf{c}_a} = 1.0`. This is similar to PCA, where the loadings :math:`\mathbf{p}_a` were constrained to unit length. In PLS we constrain the loadings for |X|, called :math:`\mathbf{w}_a`, and the loadings for |Y|, called :math:`\mathbf{c}_a`, to unit length.

The above is a description of one variant of PLS, `known as SIMPLS <http://dx.doi.org/10.1016/0169-7439(93)85002-X>`_ (simple PLS). 

.. _LVM_PLS_geometric_interpretation:

A geometric interpretation of PLS 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`As we did with PCA <LVM_PCA_geometric_interpretation>`, let's take a geometric look at the PLS model space. In the illustration below we happen to have :math:`K=3` variables in |X|, and :math:`M=3` variables in |Y|. (In general :math:`K \neq M`, but :math:`K=M=3` make explanation in the figures easier.)  Once the data are centered and scaled we have just shifted our coordinate system to the origin. Notice that there is one dot in |X| for each dot in |Y|. Each dot represents a row from the corresponding |X| and |Y| matrix.

.. image:: ../../figures/pls/geometric-interpretation-of-PLS-step1.png
	:alt:	../../figures/pls/geometric-interpretation-of-PLS.svg
	:scale: 70
	:width: 900px
	:align: center

We assume here that you understand how the scores are the perpendicular projection of each data point onto each direction vector (if not, please review the :ref:`relevant section <LVM_PCA_geometric_interpretation>` in the PCA notes). In PLS though, the direction vectors, :math:`\mathbf{w}_1` and :math:`\mathbf{c}_1`, are found and each observation is projected onto the direction. The point at which each observation lands is called the |X|-space score, :math:`t_i`, or the |Y|-space score, :math:`u_i`. These scores are found so that the covariance between the :math:`t`-values and :math:`u`-values is maximized.

.. image:: ../../figures/pls/geometric-interpretation-of-PLS-step3.png
	:alt:	../../figures/pls/geometric-interpretation-of-PLS.svg
	:scale: 70
	:width: 900px
	:align: center

As :ref:`explained above <LVM-PLS-conceptual-interpretation>`, this means that the latent variable directions are  oriented so that they best explain |X|, and best explain |Y|, and have the greatest possible relationship between |X| and |Y|.

The second component is then found so that it is orthogonal to the first component in the |X| space (the second component is not necessarily orthogonal in the |Y|-space, though it often is close to orthogonal).

.. image:: ../../figures/pls/geometric-interpretation-of-PLS-step4.png
	:alt:	../../figures/pls/geometric-interpretation-of-PLS.svg
	:scale: 70
	:width: 900px
	:align: center
