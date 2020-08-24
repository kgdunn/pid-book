# A vector of 50 normally distributed
# random numbers with a standard
# deviation of 5.
# If you have Python 3.8
# or higher, consider using the
# 'statistics' package instead.

import numpy as np

N = 50
spread = 5
x = np.random.normal(loc=0, scale=spread, size=N)
print("Standard deviation      = " +\
       str(np.std(x)))
print("The variance is         = " +\
       str(np.var(x)))
print("Square root of variance = " +\
       str(np.sqrt(np.var(x))))

# Run the code several times.
