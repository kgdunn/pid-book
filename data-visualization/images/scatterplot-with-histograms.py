# Idea from matplotlib website gallery: http://matplotlib.sourceforge.net/plot_directive/mpl_examples/axes_grid/scatter_hist.py
# Only difference: I'm using different data

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import matplotlib as mpl

data = loadmat('/Users/kevindunn/ConnectMV/Datasets/Boards/TWObySIXdata.mat')
data = data['Dataset']

x = data[0:1000, 5]
y = data[0:1000, 6]

limit_hi = 1850
limit_lo = 1450
binwidth = 10    # for histograms

# Histogram calculations
bins = np.arange(limit_lo, limit_hi + binwidth, binwidth)
x_hist = np.histogram(x, bins)
y_hist = np.histogram(y, bins)

x_hist_max = max(x_hist[0]) + 10
y_hist_max = max(y_hist[0]) + 10

h_ax = [0, 0]
fig = plt.figure(figsize=(10, 10))
# Definitions for the axis placement
# offset = 0.1
# width  = 0.6
# sliver = 1 - 2*offset - width

# definitions for the axes 
left, width = 0.1, 0.60
bottom, height = 0.1, 0.60
micro  = 0.02
bottom_h = left_h = left+width+micro

rect_scatter = [left, bottom, width, height]
rect_horiz = [left, bottom_h, width, 0.2]
rect_vert = [left_h, bottom, 0.2, height]
#               Left,               bottom,             width,  height
# rect_vert    = [offset+width+micro, offset+width,       sliver, -width]
# rect_scatter = [offset,             offset,             width,  width ]
# rect_horiz   = [offset,             offset+width+micro, width,  sliver]
h_ax_scatter = plt.axes(rect_scatter)
h_ax_horiz   = plt.axes(rect_horiz)
h_ax_vert    = plt.axes(rect_vert)

# No labels on these axes
h_ax_scatter.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
h_ax_scatter.yaxis.set_major_formatter(mpl.ticker.NullFormatter())
h_ax_vert.yaxis.set_major_formatter(mpl.ticker.NullFormatter())
h_ax_horiz.xaxis.set_major_formatter(mpl.ticker.NullFormatter())

# Explode the axes on the joint scatter plot and turn off ticks where there 
# is no spine
for loc, spine in h_ax_scatter.spines.iteritems():
    if loc in ['left', 'bottom']:
        spine.set_position(('outward',10)) # outward by 10 points
    elif loc in ['right', 'top']:
        spine.set_color('none') # don't draw spine
h_ax_scatter.xaxis.set_ticks_position('bottom')
h_ax_scatter.yaxis.set_ticks_position('left')

# Explode the axes on the horizontal plot and turn off ticks 
for loc, spine in h_ax_horiz.spines.iteritems():
   if loc in ['left']:
       spine.set_position(('outward',10)) # outward by 10 points
   elif loc in ['top', 'bottom', 'right']:
       spine.set_color('none') # don't draw spine
h_ax_horiz.yaxis.set_ticks_position('left')

# Explode the axes on the vertical plot and turn off ticks 
for loc, spine in h_ax_vert.spines.iteritems():
   if loc in ['top']:
       spine.set_position(('outward',10)) # outward by 10 points
   elif loc in ['right', 'left', 'bottom']:
       spine.set_color('none') # don't draw spine
h_ax_vert.xaxis.set_ticks_position('top')


# Plot the scatter and time-series plots: x on horiz, y on vert
h_ax_scatter.scatter(x, y, c='k', facecolors='none', marker='o')
h_ax_scatter.set_xlabel('Thickness at position 1')
h_ax_scatter.set_ylabel('Thickness at position 2')


bins = np.arange(limit_lo, limit_hi + binwidth, binwidth)
h_ax_horiz.hist(x, bins=bins, color='black')
h_ax_vert.hist(y, bins=bins, orientation='horizontal', color='black')

# Constrain the limits of all plots to the same values 
h_ax_scatter.axis([limit_lo, limit_hi, limit_lo, limit_hi])
h_ax_horiz.set_xlim( h_ax_scatter.get_xlim() )
h_ax_vert.set_ylim( h_ax_scatter.get_ylim() )


# Show the result
#plt.show()
#plt.close()
fig.savefig('scatterplot-with-histograms.png', dpi=150, facecolor='w', edgecolor='w', 
            orientation='portrait', papertype=None, format=None, 
            transparent=True)
