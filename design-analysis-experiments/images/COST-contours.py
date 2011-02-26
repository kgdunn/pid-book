#!/usr/bin/env python
"""
Illustrate simple contour plotting, contours on an image with
a colorbar for the contours, and labelled contours.

See also contour_image.py.
"""
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# fig = Figure(figsize=(2,1))
# rect = [0.1, 0.10, 0.80, 0.80]  # Left, bottom, width, height
# ax = fig.add_axes(rect, frameon=False)

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 0.025
Xoff = 320     # offset for X
Xscale = 20.0    # scale factor for X


x= 354
y= np.array([1.25, 1.75])
z = +18*((x-Xoff)/Xscale) + 10*y - 7*(x-Xoff)/Xscale*(x-Xoff)/Xscale - 4*y*y - 7.5*((x-Xoff)/Xscale)*y + 60
print z

x = np.arange(0, 3.0, delta)*Xscale + Xoff
y = np.arange(0, 2.0, delta)
X, Y = np.meshgrid(x, y)

Z = +18*((X-Xoff)/Xscale) + 10*Y - 7*(X-Xoff)/Xscale*(X-Xoff)/Xscale - 4*Y*Y - 7.5*((X-Xoff)/Xscale)*Y + 60




# Create a simple contour plot with labels using default colors.  The
# inline argument to clabel will control whether the labels are draw
# over the line segments of the contour, removing the lines beneath
# the label
fig=plt.figure(figsize=(7,5))
levels = np.array([10, 20, 30, 40, 50, 60, 65, 68, 70, 71, 71.5, 74, 76, 77])

CS = plt.contour(X, Y, Z, colors='#444444', levels=levels, linestyles='dotted',)
plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f' )
plt.xlabel('Temperature [K]', fontsize=14)
plt.ylabel('Substrate concentration [g/L]', fontsize=14)
plt.text(352, 0.08, 'Theoretical yield profiles (unknown)', fontsize=10)

from matplotlib.backends.backend_agg import FigureCanvasAgg
canvas=FigureCanvasAgg(fig)
fig.savefig('COST-contours-no-markers.png', dpi=300, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)

yvert = [0.75, 1.0, 1.25, 1.5, 1.75]
xvert = [330]*len(yvert)

xhoriz = [322, 330, 338, 346, 354]
yhoriz = [1.5]*len(xhoriz)

plt.plot(xvert, yvert, 'k.-', linewidth=2, ms=20)
plt.plot(xhoriz, yhoriz, 'k.-', linewidth=2, ms=20)
plt.plot(346, 1.5, 'ko', ms=25, markerfacecolor='none', markeredgewidth=2)
plt.plot(330, 0.75, 'kH', ms=25, markerfacecolor='none', markeredgewidth=2)


plt.text(346, 1.60, "Baseline", horizontalalignment='center')
plt.text(355, 1.53, "1", horizontalalignment='center')
plt.text(339, 1.53, "2", horizontalalignment='center')
plt.text(323, 1.53, "4", horizontalalignment='center')

plt.text(328, 1.77, "5", horizontalalignment='center')
plt.text(331, 1.53, "3", horizontalalignment='center')
plt.text(328, 1.23, "6", horizontalalignment='center')
plt.text(328, 0.97, "7", horizontalalignment='center')
plt.text(332.5, 0.72, "Final", horizontalalignment='left')

from matplotlib.backends.backend_agg import FigureCanvasAgg
canvas=FigureCanvasAgg(fig)
fig.savefig('COST-contours.png', dpi=300, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)