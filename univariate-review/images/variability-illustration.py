from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

# Load the lumber data
path = '/Users/kevindunn/ConnectMV/Datasets/Boards/'
data = loadmat(path + 'TWObySIXdata.mat')
data = data['Dataset']
N = data.shape[0]

targetY = 1680
raw = data[:,5:11]
avg_thickness = np.sum(raw, axis=1)/6

N = 500
# Create a random walk
phi = 0.9
random_walk = np.zeros((N, 1))
random_walk[0] = targetY
for k in np.arange(start=1, stop=N, step=1):
    random_walk[k] = phi*random_walk[k-1] + (1-phi)*avg_thickness[k]

# Add the odd spikes
phi = 0.9
spike_walk = np.zeros((N, 1))
spike_walk[0] = targetY
spikes = np.random.randint(low=10, high=N, size=10)
for k in np.arange(start=1, stop=N, step=1):
	spike_walk[k] += phi*spike_walk[k-1] + (1-phi)*avg_thickness[k]
	if k in spikes:
		delta = max(spike_walk)*np.sign(np.random.rand()-0.5)*np.random.rand()*0.05
		spike_walk[k] += delta
		spike_walk[k+1] -= delta*0.02
		
flat_line = np.random.randint(low=10, high=N, size=1)
number = np.median(spike_walk)
for k in np.arange(start=flat_line, stop=flat_line+N/10, step=1):
	spike_walk[k] = number

outpath = '/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/'

fig = plt.figure(figsize=(8, 3)) #, dpi=None, facecolor=None, edgecolor=None, frameon=False, subplotpars=None)

h_ax1 = fig.add_subplot(1, 1, 1)
h_ax1.axhline(y=targetY, xmin=0, xmax=N, linewidth=2, color='k')
h_ax1.axis([0, N, targetY-100, targetY+100])
h_ax1.set_title('No variability', fontsize=16)

fig.savefig(outpath + 'variation-none.png', dpi=96, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True)

fig = plt.figure(figsize=(8, 3)) #figsize=(8, 15), dpi=None, facecolor=None, edgecolor=None, frameon=False, subplotpars=None)
h_ax2 = fig.add_subplot(1, 1, 1)
h_ax2.plot(avg_thickness[0:N], color='k')
h_ax2.set_title('Some variation', fontsize=16)
fig.savefig(outpath + 'variation-some.png', dpi=96, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True)

fig = plt.figure(figsize=(8, 3)) #figsize=(8, 15), dpi=None, facecolor=None, edgecolor=None, frameon=False, subplotpars=None)
h_ax3 = fig.add_subplot(1, 1, 1)
h_ax3.plot(random_walk[0:N], color='k')
h_ax3.set_title('A bit more variation', fontsize=16)

fig.savefig(outpath + 'variation-more.png', dpi=96, facecolor='w', edgecolor='w',
         orientation='portrait', papertype=None, format=None,
         transparent=True)

fig = plt.figure(figsize=(8, 3)) #figsize=(8, 15), dpi=None, facecolor=None, edgecolor=None, frameon=False, subplotpars=None)
h_ax4 = fig.add_subplot(1, 1, 1)
h_ax4.plot(spike_walk[0:N], color='k')
h_ax4.set_title('More variation, spikes and other real phenomena', fontsize=16)

fig.savefig(outpath + 'variation-spikes.png', dpi=96, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True)

np.savetxt(outpath + 'spike_walk-numpy-python.dat', spike_walk)
plt.close()
 
