#!/usr/bin/env python
"""
Based on COST-contours.py
"""
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 0.025
Xoff = 320     # offset for X
Xscale = 20.0    # scale factor for X


xlo = 330
xhi = 346
ylo = 0.75
yhi = 1.25

x= 330
y= np.array([0.25, 0.75])
z = +18*((x-Xoff)/Xscale) + 10*y - 7*(x-Xoff)/Xscale*(x-Xoff)/Xscale - 4*y*y - 7.5*((x-Xoff)/Xscale)*y + 60

#Case 2/ Nice cliff, close the optimum
#z=\frac{\sin \left( x^{2}+y^{2} \right)}{0.1+r^{2}}+\left( x^{2}+x+y^{2} \right)\cdot \frac{\exp \left( 1-r+x^{0.2} \right)}{2},\; r=\sqrt{x^{2}+y^{2}}

#Case 3/ Typical COST shape where optimum is not parallel to axes
# z=1.6x+1.0y-0.46x^{2}-1.2y^{2}+0.8xy+3




print z

x = np.arange(0, 3.0, delta)*Xscale + Xoff
y = np.arange(0, 2.0, delta)
X, Y = np.meshgrid(x, y)

Z = +18*((X-Xoff)/Xscale) + 10*Y - 7*(X-Xoff)/Xscale*(X-Xoff)/Xscale - 4*Y*Y - 7.5*((X-Xoff)/Xscale)*Y + 60

fig=plt.figure(figsize=(7,5))
levels = np.array([10, 20, 30, 40, 50, 60, 65, 68, 70, 71, 71.5, 74, 76, 77])

CS = plt.contour(X, Y, Z, levels, colors='k')
plt.clabel(CS, inline=1, fontsize=10, fmt='%1.0f' )
plt.title('Theoretical yield profiles', fontsize=16)
plt.xlabel('Temperature [K]', fontsize=16)
plt.ylabel('Substrate concentration [g/L]', fontsize=16)

#from matplotlib.backends.backend_agg import FigureCanvasAgg
#canvas=FigureCanvasAgg(fig)
#fig.savefig('COST-contours-no-markers.png', dpi=300, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)

xlo = 338
xhi = 354
ylo = 1.75
yhi = 1.25
xdoe = [xlo, xhi, xhi, xlo, xlo]
ydoe = [ylo, ylo, yhi, yhi, ylo]

plt.plot(xdoe, ydoe, 'k.-', linewidth=2, ms=20)

# xlo = 330
# xhi = 346
# ylo = 0.75
# yhi = 0.25
# xdoe = [xlo, xhi, xhi, xlo, xlo]
# ydoe = [ylo, ylo, yhi, yhi, ylo]
# 
# plt.plot(xdoe, ydoe, 'r.-', linewidth=2, ms=20)


# plt.plot(xhoriz, yhoriz, 'k.-', linewidth=2, ms=20)
plt.plot(346, 1.5, 'ko', ms=25, markerfacecolor='none', markeredgewidth=2)
plt.plot(346, 1.5, 'k.', ms=20)

# plt.plot(330, 0.75, 'kH', ms=25, markerfacecolor='none', markeredgewidth=2)
# 
# 
#plt.text(346, 1.60, "Baseline", horizontalalignment='center')
# plt.text(355, 1.53, "1", horizontalalignment='center')
# plt.text(339, 1.53, "2", horizontalalignment='center')
# plt.text(323, 1.53, "4", horizontalalignment='center')
# 
# plt.text(328, 1.77, "5", horizontalalignment='center')
# plt.text(331, 1.53, "3", horizontalalignment='center')
# plt.text(328, 1.23, "6", horizontalalignment='center')
# plt.text(328, 0.97, "7", horizontalalignment='center')
# plt.text(332.5, 0.72, "Final", horizontalalignment='left')

#plt.show()
from matplotlib.backends.backend_agg import FigureCanvasAgg
canvas=FigureCanvasAgg(fig)
fig.savefig('factorial-two-levels-two-variables-contour-plot.png', dpi=300, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)
