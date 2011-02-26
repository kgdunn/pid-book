#!/usr/bin/env python
"""
Based on COST-contours.py
"""
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 0.025
Xoff = 360      # offset for X
Xscale = 20.0    # scale factor for X
Yoff = 0         # offset for Y
Yscale = 1.0     # scale factor for Y

#Case 2/ Nice cliff, close the optimum
#z=\frac{\sin \left( x^{2}+y^{2} \right)}{0.1+r^{2}}+\left( x^{2}+x+y^{2} \right)\cdot \frac{\exp \left( 1-r+x^{0.2} \right)}{2},\; r=\sqrt{x^{2}+y^{2}}


x = np.arange(1.0, 2.5, delta)*Xscale + Xoff
y = np.arange(0, 2, delta)*Yscale + Yoff
X, Y = np.meshgrid(x, y)
xs = ((X-Xoff)/Xscale)
ys = ((Y-Yoff)/Yscale)
Z = +30*xs + 16*ys - 10*xs*xs - 20*ys*ys + 16*xs*ys + 40

xlo = 390
xhi = 400
ylo = 0.5
yhi = 1.25
y= np.array([ylo, yhi])

xs = ((xlo-Xoff)/Xscale)
ys = ((y-Yoff)/Yscale)
z = +30*xs + 16*ys - 10*xs*xs - 20*ys*ys + 16*xs*ys + 40
print z

xs = ((xhi-Xoff)/Xscale)
ys = ((y-Yoff)/Yscale)
z = +30*xs + 16*ys - 10*xs*xs - 20*ys*ys + 16*xs*ys + 40
print z

fig = Figure(figsize=(4, 3.5))
rect = [0.2, 0.15, 0.70, 0.75]  # Left, bottom, width, height
ax = fig.add_axes(rect, frame_on=True)
levels = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 95])

CS = ax.contour(X, Y, Z, colors='#444444', linestyles='dotted',)
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.0f')
#ax.set_title('Theoretical yield profiles', fontsize=16)
ax.set_xlabel('Temperature [K]', fontsize=12)
ax.set_ylabel('Substrate \n concentration [g/L]', fontsize=12, multialignment='center')#x`horizontalalignment='center', verticalalignment='baseline')
#ax.set_xticks([330, 340, 350, 360, 370])


xdoe = [xlo, xhi, xhi, xlo, xlo]
ydoe = [ylo, ylo, yhi, yhi, ylo]

ax.plot(xdoe, ydoe, 'k.-', linewidth=2, ms=20)

plt.show()
from matplotlib.backends.backend_agg import FigureCanvasAgg
canvas=FigureCanvasAgg(fig)
fig.savefig('factorial-two-level-with-interactions.png', dpi=300, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)
