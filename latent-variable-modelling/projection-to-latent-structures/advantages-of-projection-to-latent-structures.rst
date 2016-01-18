Advantages of the projection to latent structures (PLS) method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So for predictive uses, a PLS model is very similar to :ref:`principal component regression <LVM_PCR>` (PCR) models. And PCR models were a big improvement over using multiple linear regression (MLR). In brief, :ref:`PCR was shown to have these advantages <PCR_advantages_over_MLR>`:

*	It handles the correlation among variables in |X| by building a PCA model first, then using those orthogonal scores, |T|, instead of |X| in an ordinary multiple linear regression. This prevents us from having to resort to variable selection.

*	It extracts these scores |T| even if there are missing values in |X|.

*	We reduce, but don't remove, the severity of the assumption in MLR that the predictor's, |T| in this case, are noise-free. This is because the PCA scores are less noisy than the raw data |X|.

*	With MLR we require that :math:`N > K` (number of observations is greater than the number of variables), but with PCR this is reduced to :math:`N > A`, and since :math:`A \ll K` this requirement is often true, especially for spectral data sets.

*	We get the great benefit of a consistency check on the raw data, using SPE and |T2| from PCA, before moving to the second prediction step.

An important point is that PCR is a two-step process:

.. image:: ../../figures/pls/PCR-data-structure-compared-to-MLR.png
	:alt:	../../figures/pls/PCR-data-structure-compared-to-MLR.svg
	:scale: 100%
	:width: 900px
	:align: center

In other words, we replace the :math:`N \times K` matrix of raw data with a smaller :math:`N \times A` matrix of data that summarizes the original |X| matrix. Then we relate these scores to the |y| variable. Mathematically it is a two-step process:

.. math::

	1.&\qquad \mathbf{T} = \mathbf{XP}\\
	2.&\qquad \widehat{\mathbf{y}} = \mathbf{Tb} \qquad \text{and can be solved as}\qquad \mathbf{b} = \left(\mathbf{T'T}\right)^{-1}\mathbf{T'y}

The PLS model goes a bit further and introduces some additional advantages over PCR:

*	A single PLS model can be built for multiple, correlated |Y| variables. The eliminates having to build |M| PCR models, one for each column in |Y|.

*	The PLS model directly assumes that there is error in |X| and |Y|. We will return to this important point of an |X|-space model later on.

.. LINK BACK TO THE X-space model discussion !!!

*	PLS is more efficient than PCR in two ways: with PCR, one or more of the score columns in |T| may only have a small correlation with |Y|, so these scores are needlessly calculated. Or as is more common, we have to extract many PCA components, going beyond the level of what would normally be calculated (essentially over fitting the PCA model), in order to capture sufficient predictive columns in |T|. This augments the size of the PCR model, and makes interpretation harder, which is already strained by the two-step modelling required for PCR.

Similar to PCA, the basis for PCR, we have that PLS also extracts sequential components, but it does so using the data in both |X| *and* |Y|. So it can be seen to be very similar to PCR, but that it calculates the model in one go. From the last point just mentioned, it is not surprising that PLS often requires fewer components than PCR to achieve the same level of prediction. In fact when compared to several regression methods, MLR, ridge regression and PCR, a PLS model is often the most "compact" model.

We will get into the details shortly, but as a starting approximation, you can visualize PLS as a method that extracts a single set of scores, |T|, from both |X| and |Y| simultaneously.

.. image:: ../../figures/pls/PLS-data-structure.png
	:alt:	../../figures/pls/PLS-data-structure.svg
	:scale: 50%
	:width: 900px
	:align: center

From an engineering point of view this is quite a satisfying interpretation. After all, the variables we chose to be in |X| and in |Y| come from the same system. That system is driven (moved around) by the *same underlying latent variables*. 
