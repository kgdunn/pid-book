import numpy as np
import matplotlib as mpl
import scipy.stats
from matplotlib.figure import Figure

# TODO : 
# make an "x_1" as the tick label on the horiz axis
# make an "x_2" as the tick label on the vert axis

def get_ellipse_coordinates(s_h, s_v, T2_limit_alpha, n_points=100):
    """ 
    We want the (t_horiz, t_vert) cooridinate pairs that form the T2 ellipse.

    Inputs: s_h (std deviation of the score on the horizontal axis)
            s_v (std deviation of the score on the vertical axis)
            T2_limit_alpha: the T2_limit at the alpha confidence value

    Equation of ellipse in canonical form (http://en.wikipedia.org/wiki/Ellipse)

     (t_horiz/s_h)^2 + (t_vert/s_v)^2  =  T2_limit_alpha

     s_horiz = stddev(T_horiz)
     s_vert  = stddev(T_vert)
     T2_limit_alpha = T2 confidence limit at a given alpha value (e.g. 99%)

    Equation of ellipse, parametric form (http://en.wikipedia.org/wiki/Ellipse)

    t_horiz = sqrt(T2_limit_alpha)*s_h*cos(t) 
    t_vert  = sqrt(T2_limit_alpha)*s_v*sin(t) 

    where t ranges between 0 and 2*pi

    Our function below returns `n-points` equi-spaced points on the ellipses
    """
    h_const = np.sqrt(T2_limit_alpha) * s_h
    v_const = np.sqrt(T2_limit_alpha) * s_v
    dt = 2*np.pi/(n_points-1)
    steps = np.arange(0, n_points)
    out = np.zeros((n_points, 2))
    out[:, 0] = np.cos(steps*dt)*h_const
    out[:, 1] = np.sin(steps*dt)*v_const
    return out

np.random.seed(16)
N = 50
K = 2
sigma = 3.0
alpha = scipy.stats.norm.cdf(sigma) #0.99

# Note: you must set alpha to match sigma;  e.g. (alpha=0.95, sigma=2)

scaling_x1 = -2.4
multiplier_x2 = 2.0 
names = ['x1', 'x2']
factor = 1.09  # by which to expand the axis limits ("tightness")
A = K

# This was how we generated the data ...
X = np.random.standard_normal((N, K))
X[:, [1]] = scaling_x1*X[:, [0]] + multiplier_x2*X[:, [1]]

# Create an SPE outlier in position 10
X[10, 0] = -2.0 + np.random.standard_normal(1)*0.01
X[10, 1] = scaling_x1*X[10, 0] + multiplier_x2*X[10, [1]] - 12

#np.savetxt('raw-data-example.txt', X)
#X = np.loadtxt('raw-data-example.txt')

X = X - X.mean(axis=0)           # force X to be centered for this example

# Get the Hotelling's T2 limits
meanX = X.mean(axis=0)
scaleX = np.sqrt(X.var(axis=0, ddof=1))
X_PCA = X - meanX
X_PCA = X_PCA / scaleX
N = X_PCA.shape[0]
u, s, v = np.linalg.svd(np.dot(X_PCA.T, X_PCA))
s = np.sqrt(s/N)
P = v.T
T = np.dot(X_PCA, P)
T2 = np.zeros(N)

for a in range(A):
    T2 += np.power(T[:, a] / s[a], 2)

T2lim = {}
T2lim[alpha] = A*(N-1)*(N+1)/(N*(N-1)) * scipy.stats.f.ppf(alpha, A, N-A)
ellipse = get_ellipse_coordinates(s[0], s[1], T2lim[alpha])

# Now, untransform these limits back to the X-space (real-world coordinates)
# X = TP', X(realworld) = (X * scaleX) + meanX
ellipse = np.dot(ellipse, P) * scaleX + meanX

# Quick check to see if the ellipse is reasonable
if False:
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ellipse[:,0], ellipse[:,1])
    ax.scatter(X[:,0], X[:, 1])
    ax.grid(True)
    #import matplotlib.pyplot as plt
    #plt.show()
    #plt.close()

# X is normally distributed around zero.  StdDev of x_1 and x_2 should
# theoretically be 1 and scaling_x1+multiplier_x2, respectively, but we will 
# use the sample standard deviation to calculate our limits instead.
limit_hi = X.mean(axis=0) + sigma*X.std(axis=0, ddof=1)
limit_lo = X.mean(axis=0) - sigma*X.std(axis=0, ddof=1)



# Covariance matrix, M is formed from the mean-corrected raw data
M = np.dot(X.T, X) / (N-1)

h_ax = [0, 0]
# Plots the single time-series strip charts for each x variable
if True:
    fig = Figure(figsize=(15, 5))
    
    # Plot the individual time-series plots
    h_ax = [None, None]
    h_ax[0] = fig.add_subplot(2, 1, 1)
    h_ax[1] = fig.add_subplot(2, 1, 2)
    ax = h_ax[0]
    for loc, spine in ax.spines.iteritems():
        if loc in ['top', 'bottom', 'right']:
            spine.set_color('none') # don't draw spine
    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    shift = 0.5
    h_x1 = ax.plot(np.arange(N)+shift, X[:, 0], 'k-o', ms=4)
    ax.set_ylabel('x1', fontsize=16)
    
    ax.plot([0, N], [limit_hi[0], limit_hi[0]], 'r--', linewidth=2)
    ax.plot([0, N], [limit_lo[0], limit_lo[0]], 'r--', linewidth=2)
    delta = (limit_hi[0]-limit_lo[0])*0.01
    ax.axis([0, N, limit_lo[0]-delta, limit_hi[0]+delta])

    ax = h_ax[1]
    for loc, spine in ax.spines.iteritems():
        if loc in ['top', 'bottom', 'right']:
            spine.set_color('none') # don't draw spine
    h_x2 = ax.plot(np.arange(N)+shift, X[:, 1], 'k-o', ms=4)
    ax.set_ylabel('x2', fontsize=16)    
    ax.plot([0, N], [limit_hi[1], limit_hi[1]], 'r--', linewidth=2)
    ax.plot([0, N], [limit_lo[1], limit_lo[1]], 'r--', linewidth=2)
    ax.axis([0, N, limit_lo[1]-delta, limit_hi[1]+delta])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=7))

    for idx, ax in enumerate(h_ax):
        ax.grid(linewidth=1)
        ax.axhline(linewidth=2, color='k')
        ax.patch.set_facecolor('None')

        ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid(False)
    
        for label in ax.get_xticklabels():
            label.set_fontsize(14)
            label.set_fontweight('medium')
        
        for label in ax.get_yticklabels():
            label.set_fontsize(14)
            label.set_fontweight('medium')
            
        # Annotate with some labels
        note = str(sigma) + '$\sigma$ ' 
        ax.annotate(s=note+'UCL', xy=(N*0.7, limit_hi[idx]), color='r', 
                    fontsize=14, fontweight='medium', va='top')
        ax.annotate(s=note+'LCL', xy=(N*0.7, limit_lo[idx]), color='r', 
                    fontsize=14, fontweight='medium', va='bottom')

    # h_ax[0] = fig.add_subplot(2, 1, 1)
    # ax = h_ax[0]
    # h_x1 = ax.plot(X[:, 0], 'k-o', ms=4)
    # ax.set_ylabel('x1', fontsize=16)
    # ax.plot([0, N], [limit_hi[0], limit_hi[0]], 'r--', linewidth=2)
    # ax.plot([0, N], [limit_lo[0], limit_lo[0]], 'r--', linewidth=2)
    # delta = (limit_hi[0]-limit_lo[0])*0.01
    # ax.axis([ 0, N, limit_lo[0]-delta, limit_hi[0]+delta])
    # 
    # h_ax[1] = fig.add_subplot(2, 1, 2)
    # ax = h_ax[1]
    # h_x2 = ax.plot(X[:, 1], 'k-o', ms=4)
    # ax.set_ylabel('x2', fontsize=16)
    # ax.plot([0, N], [limit_hi[1], limit_hi[1]], 'r--', linewidth=2)
    # ax.plot([0, N], [limit_lo[1], limit_lo[1]], 'r--', linewidth=2)
    # ax.axis([ 0, N, limit_lo[1]-delta, limit_hi[1]+delta])
    # ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=7))
    # 
    # for idx, ax in enumerate(h_ax):
    #     ax.grid(linewidth=2)
    #     ax.axhline(linewidth=2, color='k')
    #     ax.patch.set_facecolor('None')
    # 
    #     ax.xaxis.grid(True, which="minor")
    #     ax.yaxis.grid(False)
    # 
    #     for label in ax.get_xticklabels():
    #         label.set_fontsize(16)
    #         label.set_fontweight('medium')
    #     
    #     for label in ax.get_yticklabels():
    #         label.set_fontsize(16)
    #         label.set_fontweight('medium')
    #         
    #     # Annotate with some labels
    #     note = str(sigma) + '$\sigma$ ' 
    #     ax.annotate(s=note+'UCL', xy=(N*0.87, limit_hi[idx]), color='r', 
    #                 fontsize=16, fontweight='medium', va='top')
    #     ax.annotate(s=note+'LCL', xy=(N*0.87, limit_lo[idx]), color='r', 
    #                 fontsize=16, fontweight='medium', va='bottom')
                    
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    canvas = FigureCanvasAgg(fig)                
    fig.savefig('two-axis-monitoring-separate-plots.png', dpi=150, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)

# -------------------------------------------------
# Now create the joint scatterplot and two other plots

if True:
    colour_order = ['g', 'b', 'm', 'y', 'c',  'r',]
    
    all_data = np.append(X, ellipse, axis=0)
    x_lim_outer = np.max(np.abs(all_data), axis=0)*factor
    fig = Figure(figsize=(10, 7))

    # Definitions for the axis placement
    offset_left = 0.08
    offset = 0.02
    width  = 0.2
    length = 1 - offset - offset_left - width
    micro  = 0.000

    #               Left,        bottom,              width, height
    rect_vert    = [offset_left, offset+length-micro, width, -length]
    rect_scatter = [offset_left, offset+length, width, width ]
    rect_horiz   = [offset_left+width+micro, offset+length, length, width]
    rect_x1      = [offset_left+width+micro+length*0.2, offset+length-width*1.75, length*0.8, width*0.75]
    rect_x2      = [offset_left+width+micro+length*0.2, offset+length-width*2.75, length*0.8, width*0.75]

    h_ax_scatter = fig.add_axes(rect_scatter)    
    h_ax_vert    = fig.add_axes(rect_vert)
    h_ax_horiz   = fig.add_axes(rect_horiz)
    h_ax = []
    h_ax.append(fig.add_axes(rect_x1))
    h_ax.append(fig.add_axes(rect_x2))
    
    
    # Plot the individual time-series plots
    ax = h_ax[0]
    for loc, spine in ax.spines.iteritems():
        if loc in ['top', 'bottom', 'right']:
            spine.set_color('none') # don't draw spine
    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    shift = 0.5
    h_x1 = ax.plot(np.arange(N)+shift, X[:, 0], 'k-o', ms=4)
    ax.set_ylabel('x1', fontsize=16)
    
    ax.plot([0, N], [limit_hi[0], limit_hi[0]], 'r--', linewidth=2)
    ax.plot([0, N], [limit_lo[0], limit_lo[0]], 'r--', linewidth=2)
    delta = (limit_hi[0]-limit_lo[0])*0.01
    ax.axis([0, N, limit_lo[0]-delta, limit_hi[0]+delta])

    ax = h_ax[1]
    for loc, spine in ax.spines.iteritems():
        if loc in ['top', 'bottom', 'right']:
            spine.set_color('none') # don't draw spine
    h_x2 = ax.plot(np.arange(N)+shift, X[:, 1], 'k-o', ms=4)
    ax.set_ylabel('x2', fontsize=16)    
    ax.plot([0, N], [limit_hi[1], limit_hi[1]], 'r--', linewidth=2)
    ax.plot([0, N], [limit_lo[1], limit_lo[1]], 'r--', linewidth=2)
    ax.axis([0, N, limit_lo[1]-delta, limit_hi[1]+delta])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=7))

    for idx, ax in enumerate(h_ax):
        ax.grid(linewidth=1)
        ax.axhline(linewidth=2, color='k')
        ax.patch.set_facecolor('None')

        ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid(False)
    
        for label in ax.get_xticklabels():
            label.set_fontsize(14)
            label.set_fontweight('medium')
        
        for label in ax.get_yticklabels():
            label.set_fontsize(14)
            label.set_fontweight('medium')
            
        # Annotate with some labels
        note = str(sigma) + '$\sigma$ ' 
        ax.annotate(s=note+'UCL', xy=(N*0.7, limit_hi[idx]), color='r', 
                    fontsize=14, fontweight='medium', va='top')
        ax.annotate(s=note+'LCL', xy=(N*0.7, limit_lo[idx]), color='r', 
                    fontsize=14, fontweight='medium', va='bottom')
    
    
    
    # DONE WITH THIS: Plot the individual time-series plots 
    # NOW, plot the joint plots
    

    # No labels on these axes
    h_ax_scatter.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    h_ax_scatter.yaxis.set_major_formatter(mpl.ticker.NullFormatter())
    h_ax_vert.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    h_ax_horiz.yaxis.set_major_formatter(mpl.ticker.NullFormatter())

    # Explode the axes on the joint scatter plot and turn off ticks where there 
    # is no spine
    for loc, spine in h_ax_scatter.spines.iteritems():
        if loc in ['left','top']:
            spine.set_position(('outward',10)) # outward by 10 points
        elif loc in ['right', 'bottom']:
            spine.set_color('none') # don't draw spine
    h_ax_scatter.xaxis.set_ticks_position('top')
    h_ax_scatter.yaxis.set_ticks_position('left')

    # Explode the axes on the horizontal plot and turn off ticks 
    for loc, spine in h_ax_horiz.spines.iteritems():
        if loc in ['bottom']:
            spine.set_position(('outward',10)) # outward by 10 points
        elif loc in ['top', 'left', 'right']:
            spine.set_color('none') # don't draw spine
    h_ax_horiz.xaxis.set_ticks_position('bottom')

    # Explode the axes on the vertical plot and turn off ticks 
    for loc, spine in h_ax_vert.spines.iteritems():
        if loc in ['right']:
            spine.set_position(('outward',10)) # outward by 10 points
        elif loc in ['top', 'left', 'bottom']:
            spine.set_color('none') # don't draw spine
    h_ax_vert.yaxis.set_ticks_position('right')

    shift = 0.5
    # Plot the scatter and time-series plots: x_1 or horiz, x_2 on vert
    h_ax_scatter.scatter(X[:, 0], X[:, 1], marker='o', color='k')
    h_ax_horiz.plot(np.arange(N)+shift, X[:, 1], 'k-o', ms=4)
    h_ax_vert.plot(X[:, 0], np.arange(N), 'k-o', ms=4)
    
    # Special colours and symbols for "outliers".  Also find Hotelling's T2 
    # outliers outside the ellipse
    outliers = np.any((X < limit_lo) + (X > limit_hi), axis=1) + (T2 > T2lim[alpha])
    item = 0                
    for idx, an_outlier in enumerate(outliers):
        if an_outlier:
            m = colour_order[np.mod(item, len(colour_order))]  # Recycle colours
            h_ax_scatter.plot(X[idx, 0], X[idx, 1], m+'o', markersize=9)
            h_ax_horiz.plot(idx+shift, X[idx, 1], m+'o', ms=9)
            h_ax_vert.plot(X[idx, 0], idx, m+'o', ms=9)    
            item += 1
            
    # Add a "normal point", given by idx
    idx = N-1
    m = colour_order[np.mod(item, len(colour_order))]  # Recycle colours
    h_ax_scatter.plot(X[idx, 0], X[idx, 1], m+'*', markersize=9)
    h_ax_horiz.plot(idx+shift, X[idx, 1], m+'*', ms=9)
    h_ax_vert.plot(X[idx, 0], idx, m+'*', ms=9)    
    item += 1
    
    # Add a "normal point", given by idx
    idx = 33
    m = colour_order[np.mod(item, len(colour_order))]  # Recycle colours
    h_ax_scatter.plot(X[idx, 0], X[idx, 1], m+'*', markersize=9)
    h_ax_horiz.plot(idx+shift, X[idx, 1], m+'*', ms=9)
    h_ax_vert.plot(X[idx, 0], idx, m+'*', ms=9)    
    item += 1

    # Now draw the UCL and LCL's for x_1 
    h_ax_scatter.axhline(y=limit_hi[1], linewidth=1, color='r', ls='--')
    h_ax_scatter.axhline(y=limit_lo[1], linewidth=1, color='r', ls='--')
    h_ax_horiz.axhline(y=limit_hi[1], linewidth=1, color='r', ls='--')
    h_ax_horiz.axhline(y=limit_lo[1], linewidth=1, color='r', ls='--')

    # Now draw the UCL and LCL's for x_2
    h_ax_scatter.axvline(x=limit_hi[0], linewidth=1, color='r', ls='--')
    h_ax_scatter.axvline(x=limit_lo[0], linewidth=1, color='r', ls='--')
    h_ax_vert.axvline(x=limit_hi[0], linewidth=1, color='r', ls='--')
    h_ax_vert.axvline(x=limit_lo[0], linewidth=1, color='r', ls='--')
    
    # Add a horizontal line:
    h_ax_scatter.axvline(x=0, linewidth=1, color='k', ls='-')
    h_ax_scatter.axhline(y=0, linewidth=1, color='k', ls='-')
    h_ax_horiz.axhline(y=0, linewidth=1, color='k', ls='-')
    h_ax_vert.axvline(x=0, linewidth=1, color='k', ls='-')
    
    h_ax_scatter.set_xticks([-4, -2, 0, +2, +4])
    for label in h_ax_scatter.get_xticklabels() + h_ax_scatter.get_yticklabels() + h_ax_vert.get_yticklabels() + h_ax_horiz.get_xticklabels():
          label.set_fontsize(20)
    
    # Then add the Hotelling's ellipse
    h_ax_scatter.plot(ellipse[:,0], ellipse[:,1], '#803300', linewidth=1.5)
    
    # Annotate with some labels
    note = str(sigma) + '$\sigma$ ' 
    h_ax_horiz.annotate(s=note+'UCL', xy=(N*0.87, limit_hi[1]), color='r', 
                        fontsize=16, fontweight='medium', va='bottom')
    h_ax_horiz.annotate(s=note+'LCL', xy=(N*0.87, limit_lo[1]), color='r', 
                        fontsize=16, fontweight='medium', va='top')
                        
    
    h_ax_vert.annotate(s=note+'UCL', xy=(limit_hi[0], N*0.13), color='r', 
                           fontsize=16, fontweight='medium', va='center', ha='left', rotation=90)
    h_ax_vert.annotate(s=note+'LCL', xy=(limit_lo[0], N*0.13), color='r', 
                           fontsize=16, fontweight='medium', va='center', ha='right',  rotation=90)
                           
    
    # Constrain the limits of all plots to the same values 
    h_ax_scatter.axis([-x_lim_outer[0], x_lim_outer[0], 
                       -x_lim_outer[1], x_lim_outer[1]])
    h_ax_horiz.axis([0, N, -x_lim_outer[1], x_lim_outer[1]])
    h_ax_vert.axis([-x_lim_outer[0], x_lim_outer[0], N, -1])
    
    # And adjust the tick labels for the horizontal axis (a shorter way ??)
    segments = 5
    delta = np.floor(N/segments)
    values = np.arange(0,segments+1)*delta 
    h_ax_horiz.xaxis.set_ticks(values)
    tick_items = []
    for entry in values:
        tick_items.append(str(int(entry)))
    tick_items[0] = ''
    h_ax_horiz.xaxis.set_ticklabels(tick_items)
    
    # And vertical axis (is there a shorter way to do this?)
    values = np.arange(-1,segments+1)*delta 
    h_ax_vert.yaxis.set_ticks(values)
    tick_items = []
    for entry in values:
        tick_items.append(str(int(entry)))
    tick_items[0] = ''
    tick_items[-1] = ''
    h_ax_vert.yaxis.set_ticklabels(tick_items)
        

    from matplotlib.backends.backend_agg import FigureCanvasAgg
    canvas = FigureCanvasAgg(fig)
    fig.savefig('two-axis-monitoring-plot.png', dpi=150, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None,  transparent=True)
    