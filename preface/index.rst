.. raw:: latex

	\pagestyle{plain}
	\makeatletter
	\renewcommand{\py@noticestart@tip}{\py@heavybox}
	\renewcommand{\py@noticeend@tip}{\py@endheavybox}
	\pagenumbering{roman}
	\setcounter{secnumdepth}{-1}
	\makeatother
	

Preface
=========

.. Disclaimer re Index
.. Experiment in book publishing

.. For all the previous clients and companies that I've learnt from, experimented with their money, data, time and patience.

.. This book is an experiment. And as in all good experiments we are testing the effect of changing more than one variable at a time.
 
.. Firstly, this book is not available from a publisher. Of course a publisher adds value by having the manuscript professionally reviewed, they do a nice layout and printing the material, and marketing and distribution of the final product. In exchange the publisher takes a cut of the sales and almost always retains the intellectual property rights to the book. This is a very crude description, but regardless of the publisher's effectiveness, the result is an increased cost to the final user.

.. May be repetitive in cases, assumption is that people are coming from on-line search engines, and may start reading a section without the preceding parts.
.. 
.. Is not a comprehensive statistical textbook: each topic (visualization, univariate data analysis, least squares, process monitoring, latent variable regression, design of experiments) can fill a book or two on its own. We aim to cover the most important topics from each area, defering to references for the interested ready
.. 
.. The objective is a high-level treatment of these topics, with enough mathematical background to understand and interpret the results. It is the understanding and interpretation of equations that helps the engineer solve the data-analysis problem.
.. 
.. For example: we cover tests of differences, but a complete treatment would consider tests that are one-sided or two-sided, knowing the population variance or using an estimate of the variance. There are too many combinations to be practical for an introduction. We always defer to the most commonly encountered case. In the above example it would be a two-sided test, using an estimate of the variance (who really ever knows the population variance?)
.. 
.. Being a predominantly electronic book, we resort to many hyperlinks in the text. We recommend a good PDF reader that allows forward and back navigation of links, or use a web-browser, 
.. 
.. Distribution: PDF, web-files for off-line reading in your browser; ebook (e.g. iPad); or printed dead-tree version available on-demand. The printed version is available in hard-cover and soft-cover, and all profits are used to pay for the website hosting.

This book is a *preliminary draft* on how to improve processes using the large quantities of data that are routinely collected from process systems.

We cover :ref:`data visualization <SECTION-data-visualization>` first, in Chapter 1, since most data analysis studies start by plotting the data. This is an extremely brief introduction to this topic, only illustrating the most basic plots required for this book. Please consult the references in this chapter for more exciting plots that provide insight to your data.

This is followed by Chapter 2 on :ref:`univariate data analysis <SECTION-univariate-review>`, which is a comprehensive treatment of univariate techniques to *quantify variability* and then to *compare variability*. We look at various univariate distributions and consider tests of significance from a confidence-interval viewpoint. This is arguably a more useful and intuitive way, instead of using hypothesis tests.

The next chapter, Chapter 3, is on :ref:`monitoring charts <SECTION-process-monitoring>` to track variability: a straightforward application of univariate data analysis and data visualization from the previous two chapters.

Chapter 4 introduces the area of multivariate data. The first natural application is :ref:`least squares modelling <SECTION-least-squares-modelling>`, where we learn how variation in one variable is related to another variable. This chapter briefly covers multiple linear regression and outliers. We don't cover nonlinear regression models but hope to add that in future updates to the book.

Chapter 5 covers :ref:`designed experiments <SECTION-design-analysis-experiments>`, where we intentionally introduce variation into our system to learn more about it. We learn how to use the models from the experiments to optimize our process (e.g. for improved profitability).

The final chapter, Chapter 6, is on :ref:`latent variable modelling <SECTION_latent_variable_modelling>` where we learn how to deal with multiple variables and extract information from them. This section is divided in several chapters (PCA, PLS, and applications). It is still a work in progress and will be improved in the future.

Because this is a predominantly electronic book, we resort to many hyperlinks in the text. We recommend a good PDF reader that allows forward and back navigation of links. However, we have ensured that a printed copy can be navigated just as easily, especially if you use the table of contents and index for cross referencing.

**Updates**: This book is continually updated; there isn't a fixed edition. You should view it as a wiki. You might currently have an incomplete or older draft of the document. The latest version is always available at http://learnche.org/pid

**Acknowledgements**: I would like to thank my students and teaching assistants who over the years have made valuable comments, suggestions and corrections, and given permission to use their solutions to various questions. Particular thanks to Emily Nichols (2010), Ian Washington (2011), Ryan McBride (2011), Stuart Young (2011), Mudassir Rashid (2011), Yasser Ghobara (2012), Pedro Castillo (2012), Miles Montgomery (2012), Cameron DiPietro (2012), Andrew Haines (2012), Krishna Patel (2012), Xin Yuan (2013), Sean Johnstone (2013), Jervis Pereira (2013), and Ghassan Marjaba (2014). *Their contributions are greatly appreciated.*

The textbook was used in an online course from July to August 2014, `Experimentation for Improvement <https://www.coursera.org/course/experiments>`_. Comments and feedback from that course have greatly improved this book. *Thanks to all the Courserians*.

In particular, I'd like to thank Devon Mordell, from McMaster University, for her informal help on editing parts of the book. As well as my formal editor, `Teresa Wilson <http://tdwcommunications.com>`_, 


Thanks also to instructors at other universities who have used these notes and slides in their courses and provided helpful feedback.

Thanks everyone!

.. tip:: **Copyright and Your Rights**


	This book is unusual in that it is not available from a publisher. You may download it electronically, use it for yourself, or share it with anyone.

	The copyright to the book is held by Kevin Dunn, but it is licensed to you under the permissive `Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) <https://creativecommons.org/licenses/by-sa/3.0/>`_  license.

	In particular, you are free to

	*	**share** -  copy, distribute and transmit the work (which includes printing it).
	*	**adapt** - but you must distribute the new result under the same or similar license to this one.
	*	**commercialize** - you *are allowed* to create commercial applications based on this work.
	*	**attribute** - but you must attribute the work as follows:

		*	*Using selected portions*: "Portions of this work are the copyright of Kevin Dunn."
		*	*Or if used in its entirety*: "This work is the copyright of Kevin Dunn."
	
	You don't have to, but it would be nice if you tell us you are using this book. That way we can let you know of any errors.

		*	Please tell us if you find errors in these chapters, or have suggestions for improvements.
		*	Please email to ask permission if you would like changes to the above terms and conditions.


	Thanks, 
	`Kevin <mailto:kgdunn@gmail.com>`_ (kgdunn@gmail.com)

.. raw:: latex

	\makeatletter
	\renewcommand{\py@noticestart@tip}{\py@lightbox}
	\renewcommand{\py@noticeend@tip}{\py@endlightbox}
	\makeatother
	\clearpage
	\setcounter{page}{1}
	\pagenumbering{arabic}
	\setcounter{secnumdepth}{0}
	\pagestyle{normal}

