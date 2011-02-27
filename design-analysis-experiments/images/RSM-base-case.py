import numpy as np

# Offsets for labeling points
dx = -1.0
dy = 0.03

def surface(x1, x2):
    """ The true response surface for the system """
    x1off = 320.0
    x1scale = 20.0
    x1s = np.array((np.array(x1) - x1off)/(x1scale+0.0))
    
    x2off = 1.5
    x2scale = 1.0
    x2s = np.array((np.array(x2) - x2off)/(x2scale+0.0))

    z = (18*x1s + 10*x2s - 5*x1s*x2s - 7*x1s*x1s - 24*x2s*x2s + 50)*12  + 2*np.sin(x1) + 2*np.cos(x2)
    return z
    
def surface_with_model(x1, x2, model, x1off=0.0, x1scale=1.0, x2off=0.0, x2scale=1.0):
    """ The response surface for the system using the linear model """
    x1s = (np.array(x1) - x1off)/(x1scale+0.0)
    x2s = (np.array(x2) - x2off)/(x2scale+0.0)
    return model[1]*x1s + model[2]*x2s + model[3]*x1s*x2s + model[4]*x1s*x1s + model[5]*x2s*x2s + model[0]
    
def plot_factorial(xlo, xhi, ylo, yhi, ax, add_centerpoint=False, label_points=None, color="k"):
    """ Plots the factorial cube in the required location """
    xdoe = [xlo, xhi, xhi, xlo, xlo]
    ydoe = [ylo, ylo, yhi, yhi, ylo]
    ax.plot(xdoe, ydoe, 'k.-', linewidth=2, ms=20)
    if add_centerpoint:
        ax.plot((xlo+xhi)/2.0, (ylo+yhi)/2.0, 'r.-', linewidth=2, ms=20)
        ax.plot((xlo+xhi)/2.0, (ylo+yhi)/2.0, 'ko', ms=30, markerfacecolor='none', markeredgewidth=2)
        ax.plot((xlo+xhi)/2.0, (ylo+yhi)/2.0, 'k.', ms=20)
    if label_points:
        ax.text(xlo+dx, ylo+dy, label_points[0])
        ax.text(xhi+dx, ylo+dy, label_points[1])
        ax.text(xlo+dx, yhi+dy, label_points[2])
        ax.text(xhi+dx, yhi+dy, label_points[3])
        

def plot_CCD_factorial(xlo, xhi, ylo, yhi, xcp, ycp, ax, label_points=None, color="red"):
    """ Plots the factorial cube in the required location """
    #xdoe = [xlo, xhi, xhi, xlo, xlo]
    #ydoe = [ylo, ylo, yhi, yhi, ylo]
    ax.plot([xlo, xhi], [ycp, ycp], 'k-', linewidth=2, ms=20)
    ax.plot([xcp, xcp], [ylo, yhi], 'k-', linewidth=2, ms=20)
    ax.plot([xlo, xhi], [ycp, ycp], '.', color=color, linewidth=2, ms=20)
    ax.plot([xcp, xcp], [ylo, yhi], '.', color=color, linewidth=2, ms=20)
    if label_points:
        ax.text(xcp+dx, ylo+dy, label_points[0])
        ax.text(xhi+dx, ycp+dy, label_points[1])
        ax.text(xcp+dx, yhi+dy, label_points[2])
        ax.text(xlo+dx, ycp+dy, label_points[3])

def factorial_response(x1, x2):
    """ Computes the factorial's response at the given corner points """
    X1, X2 = np.meshgrid(x1, x2)
    return surface(X1, X2)

def two_factor_model(y):
    """ Enter y-values in standard order as a list. Calculates b = inv(X'*X)*X'*y """
    y = np.array(y)
    X = np.array([[1, 1, 1, 1], [-1, +1, -1, +1], [-1, -1, +1, +1], [+1, -1, -1, +1]]).T
    if y.shape[0] > 4:
        # We have center points!
        n_cp = y.shape[0] - 4
        cp = np.array([[1, 0, 0, 0]])        
        X = np.append(X, cp.repeat(n_cp, axis=0), axis=0)

    XtX = np.dot(X.T, X)
    Xty = np.dot(X.T, y)
    return np.dot(np.linalg.inv(XtX), Xty)

def save_figure(filename, fig):
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    canvas=FigureCanvasAgg(fig)
    fig.savefig(filename, dpi=300, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)
    
# Create base for the surface:
T_low = 315
T_high = 350
S_low = 0.25
S_high = 2.75
r = 200          # resolution of surface

x1 = np.arange(T_low, T_high, step=(T_high-T_low)/(r+0.0))
x2 = np.arange(S_low, S_high, step=(S_high-S_low)/(r+0.0))
X1, X2 = np.meshgrid(x1, x2)
Z = surface(X1, X2)

import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

# ------------------------------
# Added code to get an additional figure in the notes
fig = Figure(figsize=(5, 5))
rect = [0.15, 0.1, 0.80, 0.82]  # Left, bottom, width, height
ax = fig.add_axes(rect, frame_on=True)
levels = np.array([0, 100, 200, 300, 400, 500, 600, 700]) #30, 40, 50, 55, 60, 65, 68, 70, 71, 71.5, 72, 73, 75, 76])
CS = ax.contour(X1, X2, Z, colors='#444444', levels=levels, linestyles='dotted',)
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.0f' )
ax.set_title('Contours of profit per day ($)', fontsize=16)
ax.set_xlabel('Temperature [K]', fontsize=16)
ax.set_ylabel('Substrate concentration [g/L]', fontsize=16)

factorial = np.array([320, 330, 0.5, 1.0])
t_lo, t_hi, s_lo, s_hi = factorial
ax.text(325, 0.75, "    Baseline", horizontalalignment='left', verticalalignment='center')
baseline = factorial_response([t_lo, t_hi], [s_lo, s_hi])
std_order = [baseline[0,0], baseline[0,1], baseline[1,0], baseline[1,1]]
plot_factorial(t_lo, t_hi, s_lo, s_hi, ax=ax, add_centerpoint=True, label_points=['1', '2', '3', '4'])
model = two_factor_model(std_order)


# Fit a local model and show contours for local factorial
# These are constant for the next steps
range_T = t_hi - t_lo
range_S = s_hi - s_lo

# What is our starting point?
prev_T = start_T = (t_hi + t_lo)/2.0
prev_S = start_S = (s_hi + s_lo)/2.0
T_low_local, T_high_local = -1.9, +1.8
S_low_local, S_high_local = -1.8, +1.8
x1 = np.arange(T_low_local, T_high_local, step=(T_high_local-T_low_local)/(r+0.0))
x2 = np.arange(S_low_local, S_high_local, step=(S_high_local-S_low_local)/(r+0.0))
X1, X2 = np.meshgrid(x1, x2)
model[3] = 0  # force interaction term to zero
b = np.append(model, [0, 0])  # no quadratic terms for this model
Z = surface_with_model(X1, X2, b)
#levels = np.array([575, 600, 625, 650, 700, 720, 730, 740])
CS = ax.contour((X1*range_T/2+start_T), (X2*range_S/2+start_S), Z, colors="#007700", levels=[0, 100, 200, 300, 400, 500, 600])
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.0f' )

ax.set_xlim([T_low, 335])
ax.set_ylim([S_low, 1.25])
save_figure('RSM-base-case-with-first-factorial-notes.png', fig)
# -------------------- end: additional figure code

fig = Figure(figsize=(5.5, 8))  # Use (8, 5.5) for slide aspect ratio
rect = [0.15, 0.1, 0.80, 0.85]  # Left, bottom, width, height
ax = fig.add_axes(rect, frame_on=True)
levels = np.array([0, 100, 200, 300, 400, 500, 550, 600, 650, 700, 725, 740]) #30, 40, 50, 55, 60, 65, 68, 70, 71, 71.5, 72, 73, 75, 76])
CS = ax.contour(X1, X2, Z, colors='#444444', levels=levels, linestyles='dotted',)
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.0f' )
ax.set_title('Contours of profit per day ($)', fontsize=16)
ax.set_xlabel('Temperature [K]', fontsize=16)
ax.set_ylabel('Substrate concentration [g/L]', fontsize=16)

factorial = np.array([320, 330, 0.5, 1.0])
t_lo, t_hi, s_lo, s_hi = factorial
ax.text(325, 0.75, "    Baseline", horizontalalignment='left', verticalalignment='center')
baseline = factorial_response([t_lo, t_hi], [s_lo, s_hi])
std_order = [baseline[0,0], baseline[0,1], baseline[1,0], baseline[1,1]]
plot_factorial(t_lo, t_hi, s_lo, s_hi, ax=ax, add_centerpoint=True, label_points=['1', '2', '3', '4'])
model = two_factor_model(std_order)

ax.set_xlim([T_low, T_high])
ax.set_ylim([S_low, S_high])
save_figure('RSM-base-case-with-first-factorial.png', fig)



# These are constant for the next steps
range_T = t_hi - t_lo
range_S = s_hi - s_lo

# What is our starting point?
prev_T = start_T = (t_hi + t_lo)/2.0
prev_S = start_S = (s_hi + s_lo)/2.0

print "Start point = (%f, %f, profit = %f)" % (prev_T, prev_S, surface(prev_T, prev_S))
print "T spans = (%f, %f)" % (t_lo, t_hi)
print "S spans = (%f, %f)" % (s_lo, s_hi)
print "Y in std order is = [%s]" % str(std_order)
print "The local factorial model is %s" % str(model)

# Fit a local model and show contours for local factorial
# ----------
T_low_local, T_high_local = -1.5, +1.6
S_low_local, S_high_local = -1.3, +1.5
x1 = np.arange(T_low_local, T_high_local, step=(T_high_local-T_low_local)/(r+0.0))
x2 = np.arange(S_low_local, S_high_local, step=(S_high_local-S_low_local)/(r+0.0))
X1, X2 = np.meshgrid(x1, x2)
model[3] = 0  # force interaction term to zero
b = np.append(model, [0, 0])  # no quadratic terms for this model
Z = surface_with_model(X1, X2, b)
#levels = np.array([575, 600, 625, 650, 700, 720, 730, 740])
CS = ax.contour((X1*range_T/2+start_T), (X2*range_S/2+start_S), Z, colors="#007700")#, levels=levels)
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.0f' )

# First iteration
#----------------
full_step_T, full_step_S = model[1] * range_T/2, model[2] * range_S/2
step_T = 5 
gamma = step_T / full_step_T
step_S = gamma * full_step_S
next_T, next_S = prev_T + step_T, prev_S + step_S
print "A full step requires %f in T and %f in S" % (full_step_T, full_step_S)
print "Fraction of step taken = %f" % gamma
print "Actual step for T = %f; actual step for S = %f" % (step_T, step_S)
print "Next T = %f; next S = %f" % (next_T, next_S)
y_5 = surface(next_T, next_S)
print "y-value found = %f" % y_5
ax.annotate("", xy=(prev_T + step_T*0.95, prev_S + step_S*0.95), xycoords='data', xytext=(prev_T, prev_S), color="#007700", textcoords='data', size=10, va="center", ha="center",
        arrowprops=dict(arrowstyle="simple",connectionstyle="arc3,rad=0.0001",color="#007700"))

ax.plot(next_T, next_S, 'k.-', linewidth=2, ms=20)
ax.text(next_T+dx, next_S+dy, "5")
prev_T, prev_S = next_T, next_S
print "----------------------------"

# Next step:
step_T = 5
gamma = step_T / full_step_T
step_S = gamma * full_step_S
next_T, next_S = prev_T + step_T, prev_S + step_S
print "A full step requires %f in T and %f in S" % (full_step_T, full_step_S)
print "Fraction of step taken = %f" % gamma
print "Actual step for T = %f; actual step for S = %f" % (step_T, step_S)
print "Next T = %f; next S = %f" % (next_T, next_S)
y_6 = surface(next_T, next_S)
print "y-value found = %f"%  y_6
ax.annotate("", xy=(prev_T + step_T*0.95, prev_S + step_S*0.95), xycoords='data', xytext=(prev_T, prev_S), color="#007700", textcoords='data', size=10, va="center", ha="center",
        arrowprops=dict(arrowstyle="simple",connectionstyle="arc3,rad=0.0001",color="#007700"))
        
                     
ax.plot(next_T, next_S, 'k.-', linewidth=2, ms=20)
ax.text(next_T+dx, next_S+dy/2, "6")
prev_T, prev_S = next_T, next_S
print "----------------------------"

# Another step:
step_T = 5
gamma = step_T / full_step_T
step_S = gamma * full_step_S
next_T, next_S = prev_T + step_T, prev_S + step_S
print "A full step requires %f in T and %f in S" % (full_step_T, full_step_S)
print "Fraction of step taken = %f" % gamma
print "Actual step for T = %f; actual step for S = %f" % (step_T, step_S)
print "Next T = %f; next S = %f" % (next_T, next_S)
y_7 = surface(next_T, next_S)
print "y-value found = %f" % y_7
print "----------------------------"
ax.annotate("", xy=(prev_T + step_T*0.95, prev_S + step_S*0.95), xycoords='data', xytext=(prev_T, prev_S), color="#007700", textcoords='data', size=10, va="center", ha="center",
        arrowprops=dict(arrowstyle="simple",connectionstyle="arc3,rad=0.0001",color="#007700"))
ax.plot(next_T, next_S, 'k.-', linewidth=2, ms=20)
ax.text(next_T+dx, next_S+dy, "7")
#prev_T, prev_S = next_T, next_S
ax.set_xlim([T_low, T_high])
ax.set_ylim([S_low, S_high])
save_figure('RSM-base-case-with-exploration.png', fig)


# Backtrack, form a factorial
delta_T = 4
delta_S = 0.2
t_lo, t_hi = prev_T-delta_T, prev_T+delta_T
s_lo, s_hi = prev_S-delta_S, prev_S+delta_S
full_fact = factorial_response([t_lo, t_hi], [s_lo, s_hi])
plot_factorial(t_lo, t_hi, s_lo, s_hi, ax=ax, add_centerpoint=True, label_points=['8', '9', '10', '11'], color="#0000aa")
std_order = [full_fact[0,0], full_fact[0,1], full_fact[1,0], full_fact[1,1]]# , y_6]
model = two_factor_model(std_order)

# These are constant for the next steps
range_T = t_hi - t_lo
range_S = s_hi - s_lo

print "Start point = (%f, %f, profit = %f)" % (prev_T, prev_S, surface(prev_T, prev_S))
print "T spans = (%f, %f)" % (t_lo, t_hi)
print "S spans = (%f, %f)" % (s_lo, s_hi)
print "Y in std order (with center point) = [%s]" % str(std_order)
print "The local factorial model is %s" % str(model)


# What is the ratio between a step in T and the step in S.
step_T = 4
full_step_T, full_step_S = model[1] * range_T/2, model[2] * range_S/2
gamma = step_T / full_step_T
step_S = gamma * full_step_S
next_T, next_S = prev_T + step_T, prev_S + step_S
y_12 = surface(next_T, next_S)
ax.annotate("", xy=(prev_T + step_T*0.95, prev_S + step_S*0.95), xycoords='data', xytext=(prev_T, prev_S), textcoords='data', size=10, va="center", ha="center",
        arrowprops=dict(arrowstyle="simple",connectionstyle="arc3,rad=0.0001",color="#000000"))
ax.plot(next_T, next_S, 'k.-', linewidth=2, ms=20)
ax.text(next_T-dx, next_S+dy, "12")
ax.set_xlim([T_low, T_high])
ax.set_ylim([S_low, S_high])

print "A full step requires %f in T and %f in S" % (full_step_T, full_step_S)
print "Fraction of step taken = %f" % gamma
print "Actual step for T = %f; actual step for S = %f" % (step_T, step_S)
print "Next T = %f; next S = %f" % (next_T, next_S)
print "y-value found = %f" % y_12
print "----------------------------"

save_figure('RSM-base-case-with-extra-factorial.png', fig)


# Now add terms for a Central Composite Design
alpha = np.sqrt(2)
T_cp, S_cp = prev_T, prev_S
t_lo, t_hi = T_cp - alpha*delta_T, T_cp + alpha*delta_T
s_lo, s_hi = S_cp - alpha*delta_S, S_cp + alpha*delta_S

# CCD layout:
y_botm = surface(T_cp, s_lo)
y_left = surface(t_lo, S_cp)
y_rght = surface(t_hi, S_cp)
y_topp = surface(T_cp, s_hi)
plot_CCD_factorial(t_lo, t_hi, s_lo, s_hi, T_cp, S_cp, ax, label_points=['13', '14', '15', '16'])
ax.set_xlim([T_low, T_high])
ax.set_ylim([S_low, S_high])
save_figure('RSM-base-case-with-CCD-factorial.png', fig)

# [full factorial in standard order; then center point; then CCD bottom, right, top, left]
y = np.append(std_order, [y_6, y_botm, y_rght, y_topp, y_left])

# Model's b = [int, b_T, b_S, b_TS, bTT, BSS]
# n = 4 + 1 + 4
X = np.array([[1, 1, 1, 1], [-1, +1, -1, +1], [-1, -1, +1, +1], [+1, -1, -1, +1]]).T
X = np.append(X, np.array([[1, 0, 0, 0]]), axis=0)
X = np.append(X, np.array([[1, 1, 1, 1, 0]]).T, axis=1)
X = np.append(X, np.array([[1, 1, 1, 1, 0]]).T, axis=1)
X = np.append(X, np.array([[1, 1, 1, 1], [0, +alpha, 0, -alpha], [-alpha, 0, +alpha, 0], [0, 0, 0, 0], [0, alpha**2, 0, alpha**2], [alpha**2, 0, alpha**2, 0]]).T, axis=0)
XtX = np.dot(X.T, X)
Xty = np.dot(X.T, y)
b = np.dot(np.linalg.inv(XtX), Xty)

print "X is %s" % str(X)
print "y is %s" % str(y)
print "b is %s" % str(b)

# Fit a local model
T_low_local, T_high_local = -1.8, +3.0
S_low_local, S_high_local = -2.8, +2.0
x1 = np.arange(T_low_local, T_high_local, step=(T_high_local-T_low_local)/(r+0.0))
x2 = np.arange(S_low_local, S_high_local, step=(S_high_local-S_low_local)/(r+0.0))
X1, X2 = np.meshgrid(x1, x2)
Z = surface_with_model(X1, X2, b)
levels = np.array([575, 600, 650, 700, 720, 730, 735])
CS = ax.contour((X1*delta_T+T_cp), (X2*delta_S+S_cp), Z, colors='red', levels=levels)
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.0f' )
ax.set_xlim([T_low, T_high])
ax.set_ylim([S_low, S_high])
save_figure('RSM-base-case-with-CCD-contours.png', fig)


import Image
left = Image.open('RSM-base-case-with-exploration.png')
right = Image.open('RSM-base-case-with-CCD-contours.png')
width = left.size[0] + right.size[0]
height = left.size[1]
result = Image.new("RGBA", (width, height))
result.paste(left, (0, 0))
result.paste(right, (left.size[0], 0))
result.save('RSM-base-case-combined.png')

