.. _APPS_image_analysis:

Multivariate image analysis
============================

.. index::
	single: multivariate image analysis (MIA)
	pair: multivariate image analysis; applications
	single: image unfolding
	pair: masking; multivariate image analysis

A digital image is a measurement with several variables at every pixel, and once it is arranged
as a matrix, the latent variable methods of the :ref:`PCA <SECTION_PCA>` and :ref:`PLS
<SECTION_PLS>` sections apply to it unchanged. A camera above a conveyor, or looking into a flame,
then becomes a sensor that reports with every new image on what the product or the process looks
like: its colour, its coating, its defects.

An image as a matrix of pixels by channels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An image from a colour camera has :math:`I` rows and :math:`J` columns of pixels, on :math:`K = 3`
layers, or *channels*: the intensities of red, green and blue light, each a number from 0 to 255
for an 8-bit camera. An image with several values per pixel is a *multivariate image*, and
`Geladi, Bengtsson, Esbensen and Grahn (1992)
<https://literature.learnche.org/item/133/image-analysis-in-chemistry-i-properties-of-images-greylevel-operations-the-multivariate-image>`_
set out its properties. A hyperspectral camera records a whole spectrum at every pixel, so that
:math:`K` is a hundred or more.

PCA and PLS work on a two-dimensional matrix, so the three-way image array is unfolded first.
Each pixel becomes one row and each channel one column, which gives a matrix of :math:`IJ` rows
and :math:`K` columns, as the figure below shows. A colour image of 768 by 1024 pixels unfolds to a
matrix of 786,432 rows and 3 columns.

.. image:: ../figures/image/image-unfolding.jpg
	:alt:	A three-layer colour image unfolded into a matrix with one row per pixel
	:scale: 55
	:width: 750px
	:align: center

A :ref:`PCA model <SECTION_PCA>` fitted to this matrix, as proposed by `Geladi, Isaksson,
Lindqvist, Wold and Esbensen (1989)
<https://literature.learnche.org/item/126/principal-component-analysis-of-multivariate-images>`_,
gives every pixel a score on each component and an SPE value. Folding a column of scores back into
the :math:`I \times J` shape of the image gives a *score image*. The figure below shows a board of
lumber, the score image of its first component, and the residual of each pixel after that
component. The knots and the split stand out in the score image, while the residual image picks
out the grain lines, colour variation that the first component does not describe.

.. image:: ../figures/examples/lumber-images/lumber-example-combine.png
	:alt:	A lumber board in colour, its first score image, and its residual image
	:scale: 70
	:width: 900px
	:align: center

Unfolding discards where each pixel is. PCA treats the pixels as unrelated observations, and the
spatial arrangement comes back only when the scores are folded into an image again. A model of the
unfolded image therefore describes the colour, or spectrum, of each pixel, not the shape or
texture of the regions that the pixels form.

For a hyperspectral image, the same model compresses hundreds of correlated channels into a few
scores. This reduces the volume of data, which `Burger and Gowen (2011)
<https://literature.learnche.org/item/132/data-handling-in-hyperspectral-image-analysis>`_
identify as a main concern when such images are used in real time.

Classes of pixels, selected in the score space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pixels of one material, such as clear wood or a knot, have similar colours and so fall close
together in the score plot of :math:`t_1` against :math:`t_2`, wherever they are in the image.
With hundreds of thousands of pixels a scatter plot is a solid block of points, so the score space
is drawn as a two-dimensional histogram instead: the plane is divided into small bins, and each bin
is shaded by the number of pixels that fall in it.

A *mask* is a region drawn on this density plot. The pixels whose scores fall inside it form one
class, and highlighting them in the image shows where that class sits in the scene. This strategy,
of defining pixel classes in the score space and checking them in the image, is set out by
`Esbensen and Geladi (1989)
<https://literature.learnche.org/item/137/strategy-of-multivariate-image-analysis-mia>`_. `Liu,
Bharati, Dunn and MacGregor (2005)
<https://literature.learnche.org/item/42/automatic-masking-in-multivariate-image-analysis-using-support-vector-machines>`_
build masks automatically rather than by hand, by treating mask building as a classification
problem solved with support vector machines. This also gives masks in more than two score
dimensions, for hyperspectral images.

The number of pixels inside a mask is one number per image, and it can be charted over a sequence
of images like any other process variable. `Bharati and MacGregor (1998)
<https://literature.learnche.org/item/19/multivariate-image-analysis-for-real-time-process-monitoring-and-control>`_
propose this for real-time monitoring, tracking how often features occur in the score space and
mapping them back to their locations, and demonstrate it on a sequence of satellite images.
`Bharati, MacGregor and Tropper (2003)
<https://literature.learnche.org/item/117/softwood-lumber-grading-through-on-line-multivariate-image-analysis-techniques>`_
grade softwood lumber on-line this way: a camera above the conveyor images each board, masks
select the pixels of defects such as knots and splits, and a board whose count of defect pixels is
outside its limits is downgraded.

Features from images, used to predict quality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For prediction, each image is reduced to a row of features, and a :ref:`PLS model <SECTION_PLS>`
relates those rows to a quality that is measured in the laboratory. This is a :ref:`soft sensor
<APPS_soft_sensors>` with a camera in place of the process tags. One choice of features is the
score-space histogram itself: the count of pixels in each bin, or in each mask, forms the row for
that image. A quality that the laboratory measures only occasionally can then be predicted from
every image the camera takes.

Coated snack foods are one application. `Yu and MacGregor (2003)
<https://literature.learnche.org/item/119/multivariate-image-analysis-and-regression-for-prediction-of-coating-content-and-distribution-in-the-production-of-snack-foods>`_
extract features from colour images of the product with PCA and PLS, and predict both the average
coating content and how the coating is distributed among the pieces. `Yu, MacGregor, Haarsma and
Bourg (2003)
<https://literature.learnche.org/item/57/digital-imaging-for-online-monitoring-and-control-of-industrial-snack-food-processes>`_
report the system on industrial production lines, where the predictions are used to monitor
product quality, to detect and diagnose operational problems, and to control the coating
concentration in closed loop.

Flames are another, where the colour of the flame is used to infer the state of the combustion.
`Yu and MacGregor (2004)
<https://literature.learnche.org/item/118/monitoring-flames-in-an-industrial-boiler-using-multivariate-image-analysis>`_
predict the performance of an industrial boiler, the NO\ :sub:`x` and SO\ :sub:`2`
concentrations in its exhaust gas, and the energy content of a waste fuel fed to it, from images
of its flame. `Szatvanyi, Duchesne and Bartolacci (2005)
<https://literature.learnche.org/item/141/multivariate-image-analysis-of-flames-for-product-quality-and-combustion-control-in-rotary-kilns>`_
predict the temperature of the solids leaving a rotary kiln, over a horizon of up to about the
kiln's mean residence time, from a single image of its flame.

Colour is not always the property of interest. When the quality lies in the spatial arrangement
of the pixels, such as the roughness of a surface, the features must carry that arrangement.
`Bharati, Liu and MacGregor (2004)
<https://literature.learnche.org/item/116/image-texture-analysis-methods-and-comparisons>`_
compare methods for this *texture analysis* on images of rolled steel sheets, classified into
quality grades. In their comparison, a PLS classification model fitted directly to the raw images
performs poorly, while methods that first restore spatial information, for example a
two-dimensional Fourier transform of each image, perform well. `Liu and MacGregor (2007)
<https://literature.learnche.org/item/125/on-the-extraction-of-spectral-and-spatial-information-from-images>`_
combine PCA with a multiresolution (wavelet) decomposition of the image, so that the information
across channels and the spatial information within each channel are extracted together.

`Prats-Montalbán, De Juan and Ferrer (2011)
<https://literature.learnche.org/item/127/multivariate-image-analysis-a-review-with-applications>`_
review these methods, from greyscale to hyperspectral images, and their use in exploratory
analysis, process monitoring and regression.

References to incorporate
~~~~~~~~~~~~~~~~~~~~~~~~~

Foundational MIA papers and books
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Paul Geladi, Svante Wold and Kim H. Esbensen, "`Image analysis and chemical information in images <https://literature.learnche.org/item/136/image-analysis-and-chemical-information-in-images>`_", *Analytica Chimica Acta*, **191**, 473-480, 1986.

* Paul Geladi, Hans Isaksson, Lennart Lindqvist, Svante Wold and Kim H. Esbensen, "`Principal component analysis of multivariate images <https://literature.learnche.org/item/126/principal-component-analysis-of-multivariate-images>`_", *Chemometrics and Intelligent Laboratory Systems*, **5**, 209-220, 1989.

* Kim H. Esbensen and Paul Geladi, "`Strategy of multivariate image analysis (MIA) <https://literature.learnche.org/item/137/strategy-of-multivariate-image-analysis-mia>`_", *Chemometrics and Intelligent Laboratory Systems*, **7**, 67-86, 1989.

* Paul Geladi, Ewert Bengtsson, Kim H. Esbensen and Hans Grahn, "`Image analysis in chemistry I: Properties of images, greylevel operations, the multivariate image <https://literature.learnche.org/item/133/image-analysis-in-chemistry-i-properties-of-images-greylevel-operations-the-multivariate-image>`_", *TrAC Trends in Analytical Chemistry*, **11**, 41-53, 1992.

* Paul Geladi, Hans Grahn, Kim H. Esbensen and Ewert Bengtsson, "`Image analysis in chemistry II: Multivariate image analysis <https://literature.learnche.org/item/134/image-analysis-in-chemistry-ii-multivariate-image-analysis>`_", *TrAC Trends in Analytical Chemistry*, **11**, 121-130, 1992.

* Paul Geladi and Hans Grahn, `Multivariate Image Analysis <https://literature.learnche.org/item/138/multivariate-image-analysis>`_, Wiley, 1997.

* Hans Grahn and Paul Geladi, `Techniques and Applications of Hyperspectral Image Analysis <https://literature.learnche.org/item/139/techniques-and-applications-of-hyperspectral-image-analysis>`_, Wiley, 2007.

* José M. Prats-Montalbán, Anna De Juan and Alberto J. Ferrer, "`Multivariate image analysis: A review with applications <https://literature.learnche.org/item/127/multivariate-image-analysis-a-review-with-applications>`_", *Chemometrics and Intelligent Laboratory Systems*, **107**, 1-23, 2011.

* James Burger and Aoife A. Gowen, "`Data handling in hyperspectral image analysis <https://literature.learnche.org/item/132/data-handling-in-hyperspectral-image-analysis>`_", *Chemometrics and Intelligent Laboratory Systems*, **108**, 13-22, 2011.

* Aoife A. Gowen, Federico Marini, Carlos Esquerre, C. P. F. O'Donnell, G. Downey and James Burger, "`Time series hyperspectral chemical imaging data: Challenges, solutions and applications <https://literature.learnche.org/item/135/time-series-hyperspectral-chemical-imaging-data-challenges-solutions-and-applications>`_", *Analytica Chimica Acta*, **705**, 272-282, 2011.

Industrial applications and case studies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Manish H. Bharati and John F. MacGregor, "`Multivariate image analysis for real-time process monitoring and control <https://literature.learnche.org/item/19/multivariate-image-analysis-for-real-time-process-monitoring-and-control>`_", *Industrial and Engineering Chemistry Research*, **37**, 4715-4724, 1998.

* Manish H. Bharati, John F. MacGregor and William Tropper, "`Softwood lumber grading through on-line multivariate image analysis techniques <https://literature.learnche.org/item/117/softwood-lumber-grading-through-on-line-multivariate-image-analysis-techniques>`_", *Industrial and Engineering Chemistry Research*, **42**, 5345-5353, 2003.

* Honglu Yu and John F. MacGregor, "`Multivariate image analysis and regression for prediction of coating content and distribution in the production of snack foods <https://literature.learnche.org/item/119/multivariate-image-analysis-and-regression-for-prediction-of-coating-content-and-distribution-in-the-production-of-snack-foods>`_", *Chemometrics and Intelligent Laboratory Systems*, **67**, 125-144, 2003.

* Honglu Yu, John F. MacGregor, Gabe Haarsma and Wilfred Bourg, "`Digital imaging for online monitoring and control of industrial snack food processes <https://literature.learnche.org/item/57/digital-imaging-for-online-monitoring-and-control-of-industrial-snack-food-processes>`_", *Industrial and Engineering Chemistry Research*, **42**, 3036-3044, 2003.

* Honglu Yu and John F. MacGregor, "`Monitoring flames in an industrial boiler using multivariate image analysis <https://literature.learnche.org/item/118/monitoring-flames-in-an-industrial-boiler-using-multivariate-image-analysis>`_", *AIChE Journal*, **50**, 1474-1483, 2004.

* Manish H. Bharati, Jay Liu and John F. MacGregor, "`Image texture analysis: Methods and comparisons <https://literature.learnche.org/item/116/image-texture-analysis-methods-and-comparisons>`_", *Chemometrics and Intelligent Laboratory Systems*, **72**, 57-71, 2004.

* Jay Liu, Manish H. Bharati, Kevin G. Dunn and John F. MacGregor, "`Automatic masking in multivariate image analysis using support vector machines <https://literature.learnche.org/item/42/automatic-masking-in-multivariate-image-analysis-using-support-vector-machines>`_", *Chemometrics and Intelligent Laboratory Systems*, **79**, 42-54, 2005.

* Gabor Szatvanyi, Carl Duchesne and G. Bartolacci, "`Multivariate image analysis of flames for product quality and combustion control in rotary kilns <https://literature.learnche.org/item/141/multivariate-image-analysis-of-flames-for-product-quality-and-combustion-control-in-rotary-kilns>`_", *Industrial and Engineering Chemistry Research*, **45**, 4706-4715, 2005.

* Jay Liu and John F. MacGregor, "`On the extraction of spectral and spatial information from images <https://literature.learnche.org/item/125/on-the-extraction-of-spectral-and-spatial-information-from-images>`_", *Chemometrics and Intelligent Laboratory Systems*, **85**, 119-130, 2007.

Theses (McMaster University)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Manish H. Bharati, `Multivariate image analysis for real-time process monitoring <https://literature.learnche.org/item/144/multivariate-image-analysis-for-real-time-process-monitoring>`_, Masters thesis, 1997.

* Manish H. Bharati, `Multivariate image analysis and regression for industrial process monitoring and product quality control <https://literature.learnche.org/item/128/multivariate-image-analysis-and-regression-for-industrial-process-monitoring-and-product-quality-control>`_, Ph.D thesis, 2002.

* Jay Liu, `Machine vision for process industries: Monitoring, control, and optimization of visual quality of processes and products <https://literature.learnche.org/item/129/machine-vision-for-process-industries-monitoring-control-and-optimization-of-visual-quality-of-processes-and-products>`_, Ph.D thesis, 2004.

* Zheng Liu, `NIR imaging and its application to wheat grading <https://literature.learnche.org/item/130/nir-imaging-and-its-application-to-wheat-grading>`_, Masters thesis, 2006.

* Mark-John Bruwer, `Process systems approaches to diagnostic imaging and property prediction <https://literature.learnche.org/item/131/process-systems-approaches-to-diagnostic-imaging-and-property-prediction>`_, Ph.D thesis, 2006.
