.. _lvm_spectral_data_example:

PCA example: analysis of spectral data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A data set, `available on the dataset website <https://openmv.net/info/tablet-spectra>`_, contains data on 460 tablets, measured at 650 different wavelengths.

.. image:: ../../figures/examples/tablet-spectra/pharma-spectra.png
	:alt:	../../figures/examples/tablet-spectra/pharma-spectra.py
	:scale: 80
	:width: 750px
	:align: center
	
This R code will calculate principal components for this data:

.. dcl:: R
	:height: 300px

	# Read large data file
	file <- 'http://openmv.net/file/tablet-spectra.csv'
	spectra <- read.csv(file, header=FALSE)
	model.pca <- prcomp(spectra[,2:651], scale=TRUE)
	summary(model.pca)
	
	#Importance of components:
	#                          PC1    PC2    PC3    PC4 ... 
	#Standard deviation     21.883 10.975 3.6008 3.2708 ...
	#Proportion of Variance  0.737  0.185 0.0199 0.0165 ...
	#Cumulative Proportion   0.737  0.922 0.9420 0.9585

The :math:`R^2_a` (``Cumulative Proportion``) values shows the first component explains 73.7% of the variability in |X|, the second explains an additional 18.5% for a cumulative total of 92.2%, and the third component explains an additional 1.99%. These three components together explain 94.2% of all the variation in |X|. This means we have reduced |X| from a :math:`460 \times 650` matrix to a :math:`460 \times 3` matrix of scores, |T|, and a :math:`650 \times 3` matrix of loadings, |P|. This is a large reduction in data size, with a minimal loss of information.

Let's visually show what the :math:`R^2` values are for each column. Shown below are these values for the first 3 components. The first component (green, thin line) explains certain regions of the spectra very well, particularly the region around 1100nm. Wavelengths beyond 1800 nm are not well explained at all. The second component is primarily responsible for explaining additional variability in the 700 to 1100nm region. The third component only seems to explain the additional variability from 1700 to 1800nm. Fitting a fourth component is only going to start fitting the noisy regions of the spectrum on the very right. For these data we could use 2 components for most applications, or perhaps 3 if the region between 1700 and 1800nm was also important.

.. image:: ../../figures/examples/tablet-spectra/spectral-data-R2-per-variable.png
	:alt:	../../figures/examples/tablet-spectra/spectral-data.R
	:scale: 75
	:width: 750px
	:align: center

Finally, we can show the SPE plot for each observation. SPE values for each tablet become smaller and smaller as each successive component is added. Since each new component explains additional variance, the size of SPE must decrease. There don't appear to be any major outliers off the model's plane after the first component.

.. image:: ../../figures/examples/tablet-spectra/spectral-data-SPE-per-tablet.png
	:alt:	../../figures/examples/tablet-spectra/spectral-data.R
	:scale: 80
	:width: 750px
	:align: center

