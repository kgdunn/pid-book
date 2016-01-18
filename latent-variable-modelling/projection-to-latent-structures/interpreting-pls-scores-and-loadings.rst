Interpreting the scores in PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like in PCA, our scores in PLS are a summary of the data from *both* blocks. The reason for saying that, even though there are two sets of scores, |T| and |U|, for each of |X| and |Y| respectively, is that they have maximal covariance. We can interpret one set of them. In this regard, the |T| scores are more readily interpretable, since they are always available. The |U| scores are not available until |Y| is known. We have the |U| scores during model-building, but when we use the model on new data (e.g. when making predictions using PLS), then we only have the |T| scores. 

The scores for PLS are interpreted in exactly the :ref:`same way as for PCA <LVM_interpreting_scores>`. Particularly, we look for clusters, outliers and interesting patterns in the line plots of the scores.

The only difference that must be remembered is that these scores have a different orientation to the PCA scores. As illustrated below, the PCA scores are found so that they only explain the variance in |X|; the PLS scores are calculated so that they also explain |Y| and have a maximum relationship between |X| and |Y|. Most time these directions will be close together, but not identical.

.. image:: ../../figures/pls/geometric-comparison-PCA-PLS.png
	:alt:	../../figures/pls/geometric-comparison-PCA-PLS.svg
	:scale: 60%
	:width: 900px
	:align: center

Interpreting the loadings in PLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`Like with the loadings from PCA <LVM_interpreting_loadings>`, :math:`\mathbf{p}_a`,we interpret the loadings :math:`\mathbf{w}_a` from PLS in the same way. Highly correlated variables have similar weights in the loading vectors and appear close together in the loading plots of all dimensions. 

We tend to refer to the PLS loadings, :math:`\mathbf{w}_a`, as weights; this is for reasons that will be explained soon.

There are two important differences though when plotting the weights. The first is that we superimpose the loadings plots for the |X| and |Y| space simultaneously. This is very powerful, because we not only see the relationship between the |X| variables (from the :math:`\mathbf{w}` vectors), we also see the relationship between the |Y| variables (from the :math:`\mathbf{c}` vectors), and even more usefully, the relationship between all these variables.

This agrees again with our (engineering) intuition that the |X| and |Y| variables are from the same system; they have been, somewhat arbitrarily, put into different blocks. The variables in |Y| could just have easily been in |X|, but they are usually not available due to time delays, expense of measuring them frequently, *etc*. So it makes sense to consider the :math:`\mathbf{w}_a` and :math:`\mathbf{c}_a` weights simultaneously.

The second important difference is that we don't actually look at the :math:`\mathbf{w}` vectors directly, we consider rather what is called the :math:`\mathbf{r}` vector, though much of the literature refers to it as the :math:`\mathbf{w*}` vector (w-star). The reason for the change of notation from existing literature is that :math:`\mathbf{w*}` is confusingly similar to the multiplication operator (e.g. :math:`\mathbf{w*c}`: is frequently confused by newcomers, whereas :math:`\mathbf{r:c}` would be cleaner). The :math:`\mathbf{w*}` notation gets especially messy when adding other superscript and subscript elements to it. Further, some of the newer literature on PLS, particularly SIMPLS, uses the :math:`\mathbf{r}` notation.

The :math:`\mathbf{r}` vectors show the effect of each of the original variables, in undeflated form, rather that using the :math:`\mathbf{w}` vectors which are the deflated vectors. This is explained next.
