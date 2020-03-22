.. _LVM_testing_PCA_models:

Testing the PCA model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As mentioned previously there are 3 major steps to building a PCA model for engineering applications. We have already considered the first two steps in the preceding sections.

	#.	Preprocessing the data 
	#.	Building the latent variable model
	#.	Testing the model, including testing for the number of components to use

The last step of testing, interpreting and using the model is where one will spend the most time. Preparing the data can be time-consuming the first time, but generally the first two steps are less time-consuming. In this section we investigate how to determine the number of components that should be used in the model and how to use an existing latent variable model. The issue of interpreting a model has been addressed in the section on :ref:`interpreting scores <LVM_interpreting_scores>` and :ref:`interpreting loadings <LVM_interpreting_loadings>`.
	
.. _LVM-using-a-PCA-model:

Using an existing PCA model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this section we outline the process required to use an existing PCA model. What this means is that you have already calculated the model and validated its usefulness. Now you would like to use the model on a new observation, which we call :math:`\mathbf{x}'_{\text{new, raw}}`. The method described below can be efficiently applied to many new rows of observations by converting the row vector notation to matrix notation.

	#.	Preprocess your vector of new data in the same way as you did when you built the model. For example, if you took the log transform of a certain variable, then you must do so for the corresponding entry in :math:`\mathbf{x}'_{\text{new, raw}}`. Also apply mean centering and scaling, using the mean centering and scaling information you calculated when you originally built the model.
	
	#.	Call this preprocessed vector :math:`\mathbf{x}_{\text{new}}` now; it has size :math:`K \times 1`, so :math:`\mathbf{x}'_{\text{new}}` is a :math:`1 \times K` row vector.
	
	#.	Calculate the location, on the model (hyper)plane, where the new observation would project. In other words, we are calculating the scores: 
	
		.. math::
			\mathbf{t}'_\text{new} = \mathbf{x}'_{\text{new}} \mathbf{P}
			
		where |P| is the :math:`K \times A` matrix of loadings calculated when building the model, and :math:`\mathbf{t}'_\text{new}` is a :math:`1 \times A` vector of scores for the new observation.
	
	#.	Calculate the residual distance off the model plane. To do this, we require the vector called :math:`\widehat{\mathbf{x}}'_\text{new}`, the point on the plane, a :math:`1 \times K` vector:
	
	 	.. math::
			\widehat{\mathbf{x}}'_\text{new} = \mathbf{t}'_\text{new} \mathbf{P}'

	#.	The residual vector is the difference between the actual observation and its projection onto the plane. The :math:`K` individual entries inside this residual vector are also the called the *contributions* to the error.
	
		.. math:: 
			\mathbf{e}'_\text{new} = \mathbf{x}'_{\text{new}} - \widehat{\mathbf{x}}'_\text{new}
	
	#.	And the residual distance is the sum of squares of the entries in the residual vector, followed by taking a square root. 
	
		.. math::
			\text{SPE}_\text{new} = \sqrt{\mathbf{e}'_\text{new} \mathbf{e}_\text{new}}
	
	
		This is called the squared prediction error, SPE, even though it is more accurately a distance.
	
	
	#.	Another quantity of interest is Hotelling's :math:`T^2` value for the new observation:
	
		.. math::
			T^2_\text{new} = \sum_{a=1}^{a=A}{\left(\dfrac{t_{\text{new},a}}{s_a}\right)^2}
			
		where the :math:`s_a` values are the standard deviations for each component's scores, calculated when the model was built.
		
The above outline is for the case when there is no missing data in a new observation. When there are missing data present in :math:`\mathbf{x}'_{\text{new}}`, then we require a method to estimate the score vector, :math:`\mathbf{t}_\text{new}` in step 3. Methods for doing this are outlined and compared in the paper by `Nelson, Taylor and MacGregor <https://dx.doi.org/10.1016/S0169-7439(96)00007-X>`_ and the paper by `Arteaga and Ferrer <https://dx.doi.org/10.1002/cem.750>`_. After that, the remaining steps are the same, except of course that missing values do not contribute to the residual vector and the SPE.

