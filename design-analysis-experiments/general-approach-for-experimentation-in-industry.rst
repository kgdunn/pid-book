
General approach for experimentation in industry
================================================

.. Reference: p 251 of BHH2, and personal experience

We complete this section with some guidance for experimentation in general. The main point is that experiments are never run in one go. You will always have more questions after the first round. Box, Hunter and Hunter provide two pieces of guidance on this:

	#.	The best time to run an experiment is after the experiment. You will discover things from the previous experiment that you wish you had considered the first time around.
	#.	For the above reason, do not spend more than 20% to 25% of your time and budget on your first group of experiments. Keep some time aside to add more experiments and learn more about the system.

The **first phase** is usually *screening*. Screening designs are used when developing new products and tremendous uncertainty exists; or sometimes when a system is operating so poorly that one receives the go-ahead to manipulate the operating conditions wide enough to potentially upset the process, but learn from it.

	-	The ranges for each factor may also be uncertain; this is a perfect opportunity to identify suitable ranges for each factor.
	
	-	You also learn how to run the experiment on this system, as the operating protocol isn't always certain ahead of time. It is advisable to choose your first experiment to be the center point, since the first experiment will often "fail" for a variety of reasons (you discover that you need more equipment midway, you realize the protocol isn't sufficient, *etc*). Since the center point is not required to analyze the data, it worth using that first run to learn about your system. If successful though, that center point run can be included in the least squares model.
	
	-	Include as many factors into as few runs as possible. Use a saturated, resolution III design, or a Plackett and Burham design.
	
	-	Main effects will be extremely confounded, but this is a preliminary investigation to isolate the important effects.
	
The **second phase** is to add *sequential experiments* to the previous experiments.

	-	Use the concept of foldover: switching the sign of the factor of interest to learn more about a single factor, or switch all signs to increase the design's resolution.
	-	If you had a prior screening experiment, use the concept of projectivity in the important factors to limit the number of additional experiments required.
	-	Move to quarter and half-fractions of higher resolution, to better understand the main effects and 2-factor interactions.
	
The **third phase** is to start *optimizing* by exploring the response surface using the important variables discovered in the prior phases.

	-	Use full or half-fraction factorials to estimate the direction of steepest ascent or descent.
	-	Once you reach the optimum, then second order effects and curvature must be added to assess the direction of the optimum.
	
The **fourth phase** is to *maintain the process optimum* using the concepts of evolutionary operation (EVOP). 

	-	An EVOP program should always be in place on a process, because raw materials change, fouling and catalyst deactivation take place, and other slow moving disturbances have an effect. You should be always hunting for the process optimum.

