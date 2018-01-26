
.. _LVM_PLS_calculation:

How the PLS model is calculated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section assumes that you are comfortable with the :ref:`NIPALS algorithm for calculating a PCA model <LVM_PCA_NIPALS_algorithm>` from |X|. The NIPALS algorithm proceeds in exactly the same way for PLS, except we iterate through both blocks of |X| and |Y|.

.. figure:: ../../figures/pls/NIPALS-iterations-PLS.png
	:alt:	../../figures/pls/NIPALS-iterations-PLS.svg
	:scale: 70
	:width: 900px
	:align: center

The algorithm starts by selecting a column from :math:`\mathbf{Y}_a` as our initial estimate for :math:`\mathbf{u}_a`. The :math:`\mathbf{X}_a` and  :math:`\mathbf{Y}_a` matrices are just the preprocessed version of the raw data when :math:`a=1`. 

   **Arrow 1**
      Perform |K| regressions, regressing each column from :math:`\mathbf{X}_a` onto the vector :math:`\mathbf{u}_a`. The slope coefficients from the regressions are stored as the entries in :math:`\mathbf{w}_a`. Columns in :math:`\mathbf{X}_a` which are strongly correlated with :math:`\mathbf{u}_a` will have large weights in :math:`\mathbf{w}_a`, while unrelated columns will have small, close to zero, weights. We can perform these regression in one go:

      .. math::
			\mathbf{w}_a = \dfrac{1}{\mathbf{u}'_a\mathbf{u}_a} \cdot \mathbf{X}'_a\mathbf{u}_a
	
	
   **Step 2**
      Normalize the weight vector to unit length: :math:`\mathbf{w}_a = \dfrac{\mathbf{w}_a}{\sqrt{\mathbf{w}'_a \mathbf{w}_a}}`.

   **Arrow 3**
      Regress every row in :math:`\mathbf{X}_a` onto the weight vector. The slope coefficients are stored as entries in :math:`\mathbf{t}_a`. This means that rows in :math:`\mathbf{X}_a` that have a similar pattern to that described by the weight vector will have large values in :math:`\mathbf{t}_a`. Observations that are totally different to :math:`\mathbf{w}_a` will have near-zero score values. These :math:`N` regressions can be performed in one go:

	.. math::
			\mathbf{t}_a = \dfrac{1}{\mathbf{w}'_a\mathbf{w}_a} \cdot \mathbf{X}_a\mathbf{w}_a

   **Arrow 4**
      Next, regress every column in :math:`\mathbf{Y}_a` onto this score vector, :math:`\mathbf{t}_a`. The slope coefficients are stored in :math:`\mathbf{c}_a`. We can calculate all |M| slope coefficients:

      .. math::
			\mathbf{c}_a = \dfrac{1}{\mathbf{t}'_a\mathbf{t}_a} \cdot \mathbf{Y}'_a\mathbf{t}_a
			
   **Arrow 5**
      Finally, regress each of the :math:`N` rows in :math:`\mathbf{Y}_a` onto this weight vector, :math:`\mathbf{c}_a`. Observations in :math:`\mathbf{Y}_a` that are strongly related to :math:`\mathbf{c}_a` will have large positive or negative slope coefficients in vector :math:`\mathbf{u}_a`:

      .. math::
		\mathbf{u}_a = \dfrac{1}{\mathbf{c}'_a\mathbf{c}_a} \cdot \mathbf{Y}_a\mathbf{c}_a

This is one round of the NIPALS algorithm. We iterate through these 4 arrow steps until the :math:`\mathbf{u}_a` vector does not change much. On convergence, we store these 4 vectors: :math:`\mathbf{w}_a, \mathbf{t}_a, \mathbf{c}_a`, and :math:`\mathbf{u}_a`, which jointly define the :math:`a^{\text{th}}` component.

.. Research topic: if we deflate |X| using the u's, predicted from |Y| and |c|, then how does the second component look?  Can we calculate all the |P| loadings after NIPALS has completed all components? 


.. TO ADD: discussion of the X-space model, the loadings. We assume the X's are measured in error X= TP' + E, so we have a model for the X's.
.. LINK back to the start of PLS, where we mention this X-space model.

Then we deflate. Deflation removes variability already explained from :math:`\mathbf{X}_a` and :math:`\mathbf{Y}_a`. Deflation proceeds as follows:

   **Step 1: Calculate a loadings vector for the X space**
      We calculate the loadings for the |X| space, called :math:`\mathbf{p}_a`, using the |X|-space scores: :math:`\mathbf{p}_a = \dfrac{1}{\mathbf{t}'_a\mathbf{t}_a} \cdot \mathbf{X}'_a\mathbf{t}_a`. This loading vector contains the regression slope of every column in :math:`\mathbf{X}_a` onto the scores, :math:`\mathbf{t}_a`. In this regression the |x|-variable is the score vector, and the |y| variable is the column from :math:`\mathbf{X}_a`. If we want to use this regression model in the usual least squares way, we would need a score vector (our |x|-variable) and predict the column from :math:`\mathbf{X}_a` as our |y|-variable.

      If this is your first time reading through the notes, you should probably skip ahead to the next step in deflation. Come back to this section after reading about how to use a PLS model on new data, then it will make more sense.

      Because it is a regression, it means that if we have a vector of scores, :math:`\mathbf{t}_a`, in the future, we can predict each column in :math:`\mathbf{X}_a` using the corresponding slope coefficient in :math:`\mathbf{p}_a`. So for the :math:`k^\text{th}` column, our prediction of column :math:`\mathbf{X}_k` is the product of the slope coefficient, :math:`p_{k,a}`, and the score vector, :math:`\mathbf{t}_a`. Or, we can simply predict the entire matrix in one operation: :math:`\widehat{\mathbf{X}} = \mathbf{t}_a\mathbf{p}'_a`.

      Notice that the loading vector :math:`\mathbf{p}_a` was calculated *after* convergence of the 4-arrow steps. In other words, these regression coefficients in :math:`\mathbf{p}_a` are not really part of the PLS model, they are merely calculated to later predict the values in the |X|-space. But why can't we use the :math:`\mathbf{w}_a` vectors to predict the :math:`\mathbf{X}_a` matrix?  Because after all, in arrow step 1 we were regressing columns of :math:`\mathbf{X}_a` onto :math:`\mathbf{u}_a` in order to calculate regression coefficients :math:`\mathbf{w}_a`. That would imply that a good prediction of :math:`\mathbf{X}_a` would be :math:`\widehat{\mathbf{X}}_a = \mathbf{u}_a \mathbf{w}'_a`.

      That would require us to know the scores :math:`\mathbf{u}_a`. How can we calculate these?  We get them from :math:`\mathbf{u}_a = \dfrac{1}{\mathbf{c}'_a\mathbf{c}_a} \cdot \mathbf{Y}_a\mathbf{c}_a`. And there's the problem: the values in :math:`\mathbf{Y}_a` are not available when the PLS model is being used in the future, on new data. In the future we will only have the new values of :math:`\mathbf{X}`. This is why we would rather predict :math:`\mathbf{X}_a` using the :math:`\mathbf{t}_a` scores, since those :math:`\mathbf{t}`-scores are available in the future when we apply the model to new data.

      This whole discussion might also leave you asking why we even bother to have predictions of the :math:`\mathbf{X}`. We do this primarily to ensure orthogonality among the |t|-scores, by removing everything from :math:`\mathbf{X}_a` that those scores explain (see the next deflation step).

      These predictions of :math:`\widehat{\mathbf{X}}` are also used to calculate the squared prediction error, a very important consistency check when using the PLS model on new data. 

   **Step 2: Remove the predicted variability from X and Y**
      Using the loadings, :math:`\mathbf{p}_a` just calculated above, we remove from :math:`\mathbf{X}_a` the best prediction of :math:`\mathbf{X}_a`, in other words, remove everything we can explain about it. 

      .. math::
          \widehat{\mathbf{X}}_a &= \mathbf{t}_a \mathbf{p}'_a \\
          \mathbf{E}_a &= \mathbf{X}_a - \widehat{\mathbf{X}}_a = \mathbf{X}_a - \mathbf{t}_a \mathbf{p}'_a  \\
          \mathbf{X}_{a+1} &= \mathbf{E}_a

      For the first component, the :math:`\mathbf{X}_{a=1}` matrix contains the preprocessed raw |Y|-data. By convention, :math:`\mathbf{E}_{a=0}` is the residual matrix *before*  fitting the first component and is just the same matrix as :math:`\mathbf{X}_{a=1}`, i.e. the data used to fit the first component.

      We also remove any variance explained from :math:`\mathbf{Y}_a`:

      .. math::
          \widehat{\mathbf{Y}}_a &= \mathbf{t}_a \mathbf{c}'_a \\
          \mathbf{F}_a &= \mathbf{Y}_a - \widehat{\mathbf{Y}}_a = \mathbf{Y}_a - \mathbf{t}_a \mathbf{c}'_a  \\
          \mathbf{Y}_{a+1} &= \mathbf{F}_a

      For the first component, the :math:`\mathbf{Y}_{a=1}` matrix contains the preprocessed raw data. By convention, :math:`\mathbf{F}_{a=0}` is the residual matrix *before*  fitting the first component and is just the same matrix as :math:`\mathbf{Y}_{a=1}`.

      Notice how in both deflation steps we only use the scores, :math:`\mathbf{t}_a`, to deflate. The scores, :math:`\mathbf{u}_a`, are not used for the reason described above: when applying the PLS model to new data in the future, we won't have the actual |y|-values, which means we also don't know the :math:`\mathbf{u}_a` values.

The algorithm repeats all over again using the deflated matrices for the subsequent iterations.


.. _LVM_PLS_W_and_R: 

What is the difference between |W| and |R|?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After reading about the :ref:`NIPALS algorithm for PLS <LVM_PLS_calculation>` you should be aware that we deflate the |X| matrix after every component is extracted. This means that :math:`\mathbf{w}_1` are the weights that best predict the :math:`\mathbf{t}_1` score values, our summary of the data in :math:`\mathbf{X}_{a=1}` (the preprocessed raw data). Mathematically we can write the following:

.. math::
	\mathbf{t}_1 &= \mathbf{X}_{a=1} \mathbf{w}_1 = \mathbf{X}_1 \mathbf{w}_1 

The problem comes once we deflate. The :math:`\mathbf{w}_2` vector is calculated from the deflated matrix :math:`\mathbf{X}_{a=2}`, so  interpreting these scores is a quite a bit harder.

.. math::

	\mathbf{t}_2 = \mathbf{X}_2 \mathbf{w}_2 &= \left(\mathbf{X}_1 - \mathbf{t}_1 \mathbf{p}'_1 \right) \mathbf{w}_2 \\
	                                         &= \left(\mathbf{X}_1 - \mathbf{X}_1 \mathbf{w}_1 \mathbf{p}_1 \right) \mathbf{w}_2

The :math:`\mathbf{w}_2` is not really giving us insight into the relationships between the score, :math:`\mathbf{t}_2`, and the data, :math:`\mathbf{X}`, but rather between the score and the *deflated* data, :math:`\mathbf{X}_2`. 

Ideally we would like a set of vectors we can interpret directly; something like:

.. math::
	\mathbf{t}_a &= \mathbf{X} \mathbf{r}_a
	
One can show, using repeated substitution, that a matrix |R|, whose columns contain :math:`\mathbf{r}_a`, can be found from: :math:`\mathbf{R} = \mathbf{W}\left(\mathbf{P}'\mathbf{W}\right)^{-1}`. The first column, :math:`\mathbf{r}_1 = \mathbf{w}_1`.

So our preference is to interpret the |R| weights (often called :math:`\mathbf{W}^*` in some literature), rather than the |W| weights when investigating the relationships in a PLS model.