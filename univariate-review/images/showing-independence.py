import numpy as np
phi = -0.0
N = 100
data = np.zeros((N, 1))
data[0] = np.random.normal()


for k in range(N-1):
	data[k+1] = data[k]*phi + np.random.normal()
	
plot(data, '.-')
