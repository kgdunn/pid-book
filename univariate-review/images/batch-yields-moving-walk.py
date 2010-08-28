import numpy as np
import matplotlib.pyplot as plt

N = 365*5
targetY = 85
stdevY = 10
# Create a random walk
phi = 0.9
shocks = np.random.normal(loc=targetY, scale=stdevY, size=(N,1))

# random_walk = np.zeros((N, 1))
# random_walk[0] = targetY
# for k in np.arange(start=1, stop=N, step=1):
#     random_walk[k] = phi*random_walk[k-1] + (1-phi)*shocks[k]

# Add the odd spikes
phi = 0.9
spike_walk = np.zeros((N, 1))
spike_walk[0] = targetY
spikes = np.random.randint(low=10, high=N, size=15)
for k in np.arange(start=1, stop=N, step=1):
	spike_walk[k] += phi*spike_walk[k-1] + (1-phi)*shocks[k]
	if k in spikes:
		delta = max(spike_walk)*np.sign(np.random.rand()-0.5)*np.random.rand()*0.1
		print delta
		spike_walk[k] += delta
		spike_walk[k+1] -= delta*0.02
		

outpath = '/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/'

fig = plt.figure(figsize=(8, 3)) #, dpi=None, facecolor=None, edgecolor=None, frameon=False, subplotpars=None)bplotpars=None)
h_ax2 = fig.add_subplot(1, 1, 1)
h_ax2.plot(spike_walk[0:N], color='k')
h_ax2.set_xlim(0, N)
h_ax2.set_title('Batch yields for the past 5 years', fontsize=16)
fig.savefig(outpath + 'batch-yields.png', dpi=96, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True)

np.savetxt(outpath + 'batch-yields.dat', spike_walk)
plt.close()
 
