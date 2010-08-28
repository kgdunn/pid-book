import numpy as np
import matplotlib.pyplot as plt

N = 100
targetY = 85
stdevY = 10

# Create a random walk
phi = 0.4
shocks = np.random.normal(loc=targetY, scale=stdevY, size=(N,1))

random_walk1 = np.zeros((N, 1))
random_walk1[0] = targetY
for k in np.arange(start=1, stop=N, step=1):
    random_walk1[k] = phi*random_walk1[k-1] + (1-phi)*shocks[k]

phi = 0
random_walk2 = np.zeros((N, 1))
random_walk2[0] = targetY
for k in np.arange(start=1, stop=N, step=1):
    random_walk2[k] = phi*random_walk2[k-1] + (1-phi)*shocks[k]

phi = -0.6
random_walk3 = np.zeros((N, 1))
random_walk3[0] = targetY
for k in np.arange(start=1, stop=N, step=1):
    random_walk3[k] = phi*random_walk3[k-1] + (1-phi)*shocks[k]


outpath = '/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/'

fig = plt.figure(figsize=(10, 5)) #, dpi=None, facecolor=None, edgecolor=None, frameon=False, subplotpars=None)bplotpars=None)
h_ax1 = fig.add_subplot(3, 1, 1)
h_ax1.plot(random_walk1[0:N], color='k')
h_ax1.set_xlim(0, N)
h_ax1.set_ylabel('Sample 1', fontsize=14)

h_ax2 = fig.add_subplot(3, 1, 2)
h_ax2.plot(random_walk2[0:N], color='k')
h_ax2.set_xlim(0, N)
h_ax2.set_ylabel('Sample 2', fontsize=14)

h_ax3 = fig.add_subplot(3, 1, 3)
h_ax3.plot(random_walk3[0:N], color='k')
h_ax3.set_xlim(0, N)
h_ax3.set_ylabel('Sample 3', fontsize=14)



fig.savefig(outpath + 'simulate-independence.png', dpi=96, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True)

plt.close()
 
