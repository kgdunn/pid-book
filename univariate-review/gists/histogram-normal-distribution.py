# Create 500 normally distributed points
# with a mean of 1100 and standard deviation
# of 50 units.
import numpy as np
import matplotlib.pyplot as plt

N = 500
values = np.random.normal(loc=1100,
                          scale=50,
                          size=N)

plt.hist(values, color="white", bins=8)
plt.xlabel("Mass [g] of each package")
plt.ylabel("Number of packages (N={})".format(N))
plt.show()
