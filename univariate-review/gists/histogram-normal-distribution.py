# Create 1000 normally distributed points
# with mean of 0 and standard deviation of 1.
import numpy as np
import matplotlib.pyplot as plt

N = 1000
values = np.random.normal(loc=0, scale=1,
                          size=N)

plt.subplot(1, 2, 1)
plt.hist(values, color="white",)
plt.ylabel("Frequency (N={})".format(N))

plt.subplot(1, 2, 2)
plt.hist(values,
         color="white",
         # For older matplotlib versions
         normed=True,
         # Rather, use 'density' instead
         #density=True
         )
plt.ylabel("Relative density")

plt.tight_layout()
plt.show()
