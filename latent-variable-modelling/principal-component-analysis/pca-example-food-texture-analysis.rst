.. _LVM_food_texture_example:

PCA example: Food texture analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's take a look at an example to consolidate and extend the ideas introduced so far. This `data set is from a food manufacturer <http://openmv.net/info/food-texture>`_ making a pastry product. Each sample (row) in the data set is taken from a batch of product where 5 quality attributes are measured:

	#.	Percentage oil in the pastry
	#.	The product's density (the higher the number, the more dense the product)
	#.	A crispiness measurement, on a scale from 7 to 15, with 15 being more crispy.
	#.	The product's fracturability: the angle, in degrees, through which the pasty can be slowly bent before it fractures.
	#.	Hardness: a sharp point is used to measure the amount of force required before breakage occurs. 
	
A scatter plot matrix of these :math:`K = 5` measurements is shown for the :math:`N=50` observations.

.. image:: ../../figures/examples/food-texture/pca-on-food-texture-scatterplot-matrix.png
	:alt:	../../figures/examples/food-texture/pca-on-food-texture-data.R
	:scale: 70
	:width: 900px
	:align: center
	

We can get by with this visualization of the data because :math:`K` is small in this case. This is also a good starting example, because you can refer back to these scatterplots to confirm your findings.

**Preprocessing the data**

The first step with PCA is to center and scale the data. The box plots show how the raw data are located at different levels and have arbitrary units. 

.. image:: ../../figures/examples/food-texture/pca-on-food-texture-centering-and-scaling.png
	:alt:	../../figures/examples/food-texture/pca-on-food-texture-data.R
	:scale: 60
	:width: 900px
	:align: center

Centering removes any bias terms from the data by subtracting the mean value from each column in the matrix |X|. For the :math:`k^\text{th}` column:

.. math::

 	\mathbf{x}_{k,\text{center}} = \mathbf{x}_{k,\text{raw}} - \text{mean}\left(\mathbf{x}_{k,\text{raw}}\right)

Scaling removes the fact that the raw data could be in diverse units: 

.. math::

	\mathbf{x}_{k} = \dfrac{\mathbf{x}_{k,\text{center}}}{ \text{standard deviation}\left(\mathbf{x}_{k,\text{center}}\right) }

Then each column :math:`\mathbf{x}_{k}` is collected back to form matrix |X|. This preprocessing is so common it is called :index:`autoscaling`: center each column to zero mean and then scale it to have unit variance. After this preprocessing each column will have a mean of 0.0 and a variance of 1.0. (Note the box plots don't quite show this final result, because they use the median instead of the mean, and show the interquartile range instead of the standard deviation).

Centering and scaling does not alter the overall interpretation of the data: if two variables were strongly correlated before preprocessing they will still be strongly correlated after preprocessing.

For reference, the mean and standard deviation of each variable is recorded below. In the last 3 columns we show the raw data for observation 33, the raw data after centering, and the raw data after centering and scaling:

.. tabularcolumns:: |l||l|l||r|r|r|

.. csv-table:: 
   :header: Variable, Mean, Standard deviation, Raw data, After centering, After autoscaling
   :widths: 30, 30, 30, 30, 30, 30

	Oil,      17.2,      1.59, 15.5, -1.702, -1.069
	Density,  2857.6,  124.5,  3125, 267.4, +2.148  
	Crispy,   11.52,     1.78, 7, -4.52, -2.546 
	Fracture, 20.86,     5.47, 33,  12.14, +2.221
	Hardness,  128.18,   31.13, 92, -36.18, -1.162

**Loadings:** :math:`\,\mathbf{p}_1`

We will discuss how to determine the number of components to use :ref:`in a future section <LVM_number_of_components>`, and :ref:`how to compute them <LVM_algorithms_for_PCA>`, but for now we accept there are two important components, |p1| and :math:`\mathbf{p}_2`. They are:

.. math:: 
	\mathbf{p}_1 = \begin{bmatrix} +0.46 \\  -0.47 \\ +0.53 \\ -0.50 \\ +0.15 \end{bmatrix} \qquad \text{and} \qquad 
	\mathbf{p}_2 = \begin{bmatrix} -0.37 \\  +0.36 \\ +0.20 \\ -0.22 \\ +0.80 \end{bmatrix}\\


Where we might visualize that first component by a bar plot:

.. image:: ../../figures/examples/food-texture/pca-on-food-texture-pc1-loadings.png
	:alt:	../../figures/examples/food-texture/pca-on-food-texture-data.R
	:scale: 60
	:width: 750px
	:align: center


.. _LVM_eqn_LVM_t1_food_texture:

This plot shows the first component. All variables, except for hardness have large values in :math:`\mathbf{p}_1`. If we write out the equation for :math:`t_1` for an observation :math:`i`:

.. math::
	:label: LVM_t1_food_texture

	t_{i,1} = 0.46 \,\, x_\text{oil} - 0.47 \,\, x_\text{density} + 0.53 \,\, x_\text{crispy} - 0.50 \,\, x_\text{fracture}  + 0.15 \,\, x_\text{hardness}


Once we have centered and scaled the data, remember that a negative :math:`x`-value is a value below the average, and that a positive :math:`x`-value lies above the average.

For a pastry product to have a high :math:`t_1` value would require it to have some combination of above-average oil level, low density, and/or be more crispy and/or only have a small angle by which it can be bent before it fractures, i.e. low fracturability. So pastry observations with high :math:`t_1` values sound like they are brittle, flaky and light. Conversely, a product with low :math:`t_1` value would have the opposite sort of conditions: it would be a heavier, more chewy pastry (higher fracture angle) and less crispy.


**Scores:** :math:`\,\mathbf{t}_1`

Let's examine the score values calculated. As shown in equation :eq:`LVM_t1_food_texture`, the score value is a linear combination of the data, :math:`\mathbf{x}`, given by the weights in the loadings matrix, |P|. For the first component, :math:`\mathbf{t}_1 = \mathbf{X} \mathbf{p}_1`. The plot here shows the values in vector :math:`\mathbf{t}_1` (an :math:`N \times 1` vector) as a sequence plot

.. image:: ../../figures/examples/food-texture/pca-on-food-texture-pc1-scores.png
	:alt:	../../figures/examples/food-texture/pca-on-food-texture-data.R
	:scale: 50
	:width: 750px
	:align: center
	
The samples appear to be evenly spread, some high and some low on the :math:`t_1` scale. Sample 33 has a :math:`t_1` value of -4.2, indicating it was much denser than the other pastries, and had a high fracture angle (it could be bent more than others). In fact, if we `refer to the raw data <http://openmv.net/info/food-texture>`_ we can confirm these findings: :math:`\mathbf{x}_{i=33} = [15.5, \,\, 3125, \,\, 7, \,\, 33, \,\, 92]`. Also refer back to the scatterplot matrix and mark the point which has density of 3125, and fracture angle of 33. This pastry also has a low oil percentage (15.5%) and low crispy value (7).

We can also investigate sample 36, with a :math:`t_1` value of 3.6. The raw data again confirm that this pastry follows the trends of other, high :math:`t_1` value pastries. It has a high oil level, low density, high crispiness, and a low fracture angle: :math:`x_{36} = [21.2, \,\, 2570, \,\, 14, \,\, 13, \,\, 105]`. Locate again on the scatterplot matrices sample 36 where oil level is 21.2 and the crispiness is 14. Also mark the point where density = 2570 and the fracture value = 13 for this sample.

We note here that this component explains 61% of the original variability in the data. It's hard to say whether this is high or low, because we are unsure of the degree of error in the raw data, but the point is that a single variable summarizes about 60% of the variability from all 5 columns of raw data.

.. TODO: summarize here the correlation vs causality effects

**Loadings:** :math:`\,\mathbf{p}_2`

The second loading vector is shown as a bar plot:

.. image:: ../../figures/examples/food-texture/pca-on-food-texture-pc2-loadings.png
	:alt:	../../figures/examples/food-texture/pca-on-food-texture-data.R
	:scale: 55
	:width: 750px
	:align: center

This direction is aligned mainly with the hardness variable: all other variables have a small coefficient in :math:`\mathbf{p}_2`. A high :math:`t_2` value is straightforward to interpret: it would imply the pastry has a high value on the hardness scale. Also, this component explains an additional 26% of the variability in the dataset. 

Because this component is orthogonal to the first component, we can be sure that this hardness variation is independent of the first component. One valuable way to interpret and use this information is that you can adjust the variables in :math:`\mathbf{p}_2`, i.e. the process conditions that affect the pastry's hardness, without affecting the other pastry properties, i.e the variables described in :math:`\mathbf{p}_1`.

