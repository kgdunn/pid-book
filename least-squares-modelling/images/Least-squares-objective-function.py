import numpy as np
import matplotlib.pyplot as plt

N = 50
x = np.random.random((N, 1))*3 - 1.5
y = x*0.75 + np.random.random((N, 1))*0.5

steps = np.arange(0, 1.2, 0.05)
S = np.zeros(steps.shape)
for index, b_1 in enumerate(steps):
    prediction = x*b_1
    error = y - prediction
    S[index] = sum(error*error)
    
print S

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel(r'$\mathbf{\mathit{b}_1}$', fontsize=16, weight=800)
ax.set_ylabel(r'$\mathbf{f(\mathit{b}_0, \mathit{b}_1)}$', fontsize=16, weight=800)
ax.plot(steps, S, '.', markersize=12)
ax.axis([0, 1.2, 3, 22])
ax.grid(True)


for label in ax.get_xticklabels():
    label.set_fontsize(16)
    label.set_weight(800)
for label in ax.get_yticklabels():
        label.set_fontsize(16)
        label.set_weight(800)

fig.savefig('least-squares-objective-function-old.png', dpi=96, facecolor='w', edgecolor='w',  orientation='portrait', papertype=None, format=None, transparent=True)
