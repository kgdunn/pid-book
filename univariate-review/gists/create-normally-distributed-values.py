# A vector of 50 normally distributed
# random numbers. If you have Python 3.8
# or higher, consider using the
# 'statistics' package.

import numpy as np

N = 50
x = np.random.normal(size=N)
print(np.mean(x))
# Run the code several times, to check
# that the mean is approximately 0
# Check what the 'x' variable contains.
