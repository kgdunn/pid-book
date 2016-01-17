Topics of aesthetics and style
==============================

We won't cover these topics, but :ref:`Tufte's books <visualization_references>` contain remarkable examples that discuss effective use of colour for good contrast, varying line widths, and graph layout (e.g. use more horizontal than vertical - an aspect ratio of about 1.4 to 2.0; and flow the graphics into the location in the text where discussed).

Data frames (axes)
---------------------

Frames are the basic containers that surround the data and give context to our numbers. Here are some tips:

#.	Use round numbers.
#.	Generally, tighten the axes as much as possible, except ...
#.	When showing comparison plots, all axes must have the same minima and maxima.

.. TODO: give an example of a bad visualization here that has unequal axes for comparison

Colour
---------------------

:index:`Colour <pair: colour; visualization>` is very effective in all graphical charts. However, you must bear in mind that your readers might be colour-blind, or the document might be read from a grayscale printout. 

Note also that a standard colour progression does *not* exist. We often see dark blues and purples representing low numbers and reds the higher numbers, with greens, yellows and orange in-between. Also, there are several such colour schemes - there isn't a universal standard. The only safest colour progression is the grayscale axis, ranging from black to white at each extreme: this satisfies both colour-blind readers and users of your grayscale printed output.

See the :ref:`section on scatter plots <reference_to_use_of_colour>` for an example of the effective use of colour.

General summary: revealing complex data graphically
======================================================

There is no generic advice that applies in every instance. These tips are useful, though, in most cases:

-	If the question you want answered is causality, then show causality (the most effective way is with bivariate scatter plots). If trying to answer a question with alternatives, show comparisons (with tiles of plots or a simple table).

-	Words and graphics belong together. Add labels to plots for outliers, and explain interesting points. Add equations and even small summary tables on top of your plots. Remember that a graph should be like a paragraph of text, not necessarily just a graphical display of numbers that you discuss later on.

-	Avoid obscure coding on the graph. Don't label points as "A", "B", "C", .... and then put a legend: "A: grade TK133", "B: grade RT231", "C: grade TK134". Just put the labels directly on the plot.

-	Do not assume your audience is ignorant and won't understand a complex plot. Conversely, don't try to enliven a plot with decorations and unnecessary graphics (flip through a copy of almost any weekly news magazine for examples of this sort of embellishment). As Tufte mentions more than once in his books, "*If the statistics are boring, then you've got the wrong numbers.*". The graph should stand on its own.

-	When the graphics involve money and time, make sure you adjust the money for inflation.

-	Maximize the data-ink ratio = (ink for data) / (total ink for graphics). Maximizing this ratio, within reason, means you should (a) eliminate nondata ink and (b) erase redundant data-ink.

-	Maximize data density. Humans can interpret data displays of 250 data points per linear inch and 60,000 data points per square inch.

.. see http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0001OR for the above numbers

