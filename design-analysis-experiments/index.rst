.. _SECTION-design-analysis-experiments:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Design and Analysis of Experiments
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. toctree::
   :maxdepth: 2

   design-analysis-experiments
   examples-of-how-designed-experiments-are-used
   why-learning-about-systems-is-important
   experiments-with-a-single-variable-at-two-levels
   changing-one-single-variable-at-a-time
   full-factorial-designs/index
   fractional-factorial-designs/index
   blocking-and-confounding-for-disturbances
   response-surface-methods
   general-approach-for-experimentation
   extended-topics-related-to-designed-experiments
   design-analysis-experiments-exercises


.. to add:

    https://www.coursera.org/learn/experimentation/discussions/all/threads/gOxYFw2-Eeic0RJNIFxTVg

    The statement about OFAT/COST is applicable when cause and effect is not even known, or suspected for a factor. It would be unwise to add a factor to a (fractional) factorial if was unclear that it would even have an effect on the response variable.

    The reason is simple: every factor in the system grows the number of experiments required for that (fractional) factorial design in an exponential manner, it is the kk in the 2^{k-p}2
    k−p
     .

    Let's look at an example.

    Let's say you have doubtful factor D that you are unsure about, and you already have 3 factors that you are relatively certain about: A, B, and C. A full factorial would require 8 experiments. Adding factor D would increase that to 16 experiments.

    It would be wiser to plan you full factorial in factors A, B, and C and randomize your order of experiments. Then for your first run you also put factor D at it's low level. Then run another experiment with D at a high level.

    These 2 experiments at this point is essentially an OFAT: you have only varied D, and you can tell then if it has an effect on yy.

    Case 1 (D has no effect on yy): you have 'wasted' one extra run, but it is not really a waste, since you have essentially run a replicate, and from that you also learn about the noise/reproducibility in the system.

    Case 2 (D has an effect on yy): you can immediately replan your experimental design to include factor D. Whether it is a full factorial (16 experiments, or a fractional factorial), you would have likely have had to do 1 (or both) of those 2 experiments. So no loss either, you get to use that extra experiment to give you an extra degree of freedom in the linear regression model.

    Hopefully that helps to explain an approach I would take if I were to try an evaluate the utility of adding an uncertain factor.
