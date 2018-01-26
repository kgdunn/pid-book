
.. _LVM-using-indicator-variables:

Using indicator variables in a latent variable model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
	single: indicator variable
	
.. index::
	single: dummy variable
	seealso: dummy variable; indicator variable

.. ... you use the term "binary" and "indicator" interchangeably. Specifically you say, "Indicator variables, also called dummy variables, are most often binary variables..." which is imprecise and vague. My experience with latent variable modeling suggests that "indicators" (in measurement models) are the things that load on a latent variable, such as "words per minute" which is manifested by literacy. 

.. I suppose it is has to do with comfort of terminology regarding the use of the word 'indicator'. There's a bad track recording in statistics and mathematics to use everyday English words in slightly different ways, that then leads to confusion with people coming from different backgrounds/trainings.

.. I've generally (in my field at least of engineering) seen the word indicator used to indicate the presence or absence of something. For example, the page you referred to has a diagram where there was an indicator variable of "Adequate yield" (probably a 1 in the data column) vs "Poor yield" (probably a 0 in that same column). In that sense, that column in the data matrix indicates which row was adequate or poor. In that sense it is a binary variable. 

.. But I have also seen situations where the indicator variable indicates multiple levels, and is included as an ordinal variable. There that variables also indicates something meaningful.

.. When such a variable is included in the latent variable model it will appear in the loadings plot, and can be meaningfully interpreted, perhaps hinting at some cause-effect possibilities, or at least raising interesting questions that can be verified by further research/experiments.



Indicator variables, also called dummy variables, are most often binary variables that indicate the presence or absence of a certain effect. For example, a variable that shows if reactor A or reactor B was used. Its value is either a 0 or a 1 in the data matrix |X|. It's valid to include these sort of variables in a principal component analysis model where they are used and interpreted as any other continuous variable.

Sometimes these variables are imported into the computer software, but *not used in the model*. They are only used in the display of results, where the indicator variable is shown in a different colour or with a different marker shape. We will see :ref:`an example of this for process troubleshooting <LVM_troubleshooting>`, to help isolate causes for poor yield from a process:

.. image:: ../../figures/examples/raw-material-outcome/process-troubleshooting.png
	:alt:	../../figures/examples/raw-material-outcome/process-troubleshooting.R
	:scale: 80
	:width: 750px
	:align: center
	
If the variable is included in the model then it is centered and scaled (preprocessed) like any other variable. Care must be taken to make sure this variable is reasonably balanced. There is no guide as to how balanced it needs to be, but there should be a good number of observations of both zeros and ones. The extreme case is where there are :math:`N` observations, and only 1 of them is a zero or a one, and the other :math:`N-1` observations are the rest. You are not likely to learn much from this variable in any case; furthermore, the scaling for this variable will be poor (the variance will be small, so dividing by this small variance will inflate that variable's variance).

Interpreting these sort of variables in a loading plot is also no different; strong correlations with this variable are interpreted in the usual way.

