Topics of aesthetics and style
==============================

We won't cover these topics, but :ref:`Tufte's books <visualization_references>` (see :index:`Tufte <single: Tufte, Edward>`) contain remarkable examples that discuss effective use of colour for good contrast, varying line widths, and graph layout (e.g. use more horizontal than vertical - an :index:`aspect ratio <pair: aspect ratio; visualization>` of about 1.4 to 2.0; and flow the graphics into the location in the text where discussed).

Data frames (axes)
---------------------

.. index::
	pair: data frame; visualization
	single: axes, data frame

Frames are the basic containers that surround the data and give context to our numbers. Here are some tips:

#.	Use round numbers for the axis limits and tick marks.
#.	Generally, tighten the axes as much as possible. Two exceptions: bar plots, where the value
	axis must include zero, and comparison plots, described next.
#.	When showing comparison plots, all axes must have the same minima and maxima.

.. TODO: give an example of a bad visualization here that has unequal axes for comparison

Colour
---------------------

:index:`Colour <pair: colour; visualization>` is very effective in all graphical charts. However, you must bear in mind that your readers might be :index:`colour-blind <single: colour-blindness>`, or the document might be read from a :index:`grayscale <single: grayscale>` printout, or viewed on an electronic device where colours are shown differently than you might intend.

Note also that a single standard colour progression does *not* exist. We often see dark blues and
purples representing low numbers and reds the higher numbers, with greens, yellows and orange
in-between. There are several such `colour schemes
<https://en.wikipedia.org/wiki/Color_scheme>`_ - there isn't a universal standard. Most plotting
software now defaults to a colour scale designed to be *perceptually uniform*: equal steps in the
data appear as equal steps in colour, the scale converts sensibly to grayscale, and it remains
readable for colour-blind readers. Examples are the ColorBrewer schemes of Harrower and Brewer
(2003), listed in the :ref:`references <visualization_references>`, and the viridis and cividis
colour maps that ship with matplotlib, Plotly and R. Avoid the older rainbow (or "jet") colour
scale: its perceived brightness rises and falls along the scale, which creates bands and false
boundaries that are not in the data. A grayscale axis, ranging from black to white, remains a safe
progression for printed output.

See the :ref:`section on scatter plots <reference_to_use_of_colour>` for an example of the effective use of colour.

General summary: revealing complex data graphically
======================================================

There is no generic advice that applies in every instance. These tips are useful, though, in most cases:

-	If the question you want answered is about the relationship between two variables, show that
	relationship (the most effective way is with bivariate scatter plots), keeping in mind that a
	scatter plot shows association: establishing causality requires a
	:ref:`designed experiment <SECTION-design-analysis-experiments>`. If trying to answer a
	question with alternatives, show comparisons (with :index:`tiles of plots
	<pair: small multiples; visualization>` or a simple table).

-	Words and graphics belong together. Add labels to plots for outliers, and explain interesting points. Add equations and even small summary tables on top of your plots. Remember that a graph should be like a paragraph of text, not necessarily just a graphical display of numbers that you discuss later on.

-	Avoid obscure coding on the graph. Don't label points as "A", "B", "C", .... and then put a legend: "A: grade TK133", "B: grade RT231", "C: grade TK134". Just put the labels directly on the plot.

-	Do not assume your audience is ignorant and won't understand a complex plot. Conversely, don't try to enliven a plot with decorations and unnecessary graphics (flip through a copy of almost any weekly news magazine for examples of this sort of embellishment). As Tufte mentions more than once in his books, "*If the statistics are boring, then you've got the wrong numbers.*". The graph should stand on its own.

-	When the graphics involve money and time, make sure you adjust the money for inflation.

-	Maximize the :index:`data-ink ratio <pair: data-ink ratio; visualization>` = (ink for data) / (total ink for graphics). Maximizing this ratio, within reason, means you should (a) eliminate nondata ink and (b) erase redundant data-ink.

-	Maximize :index:`data density <pair: data density; visualization>`. Tufte `estimates
	<https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/>`_ that
	people can interpret data displays of around 100 data points per centimeter (250 data points
	per linear inch) and around 10000 per square centimeter (60000 data points per square inch).
