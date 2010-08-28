import numpy as np

# Generate seven uniform distributions, of 1000 values in each.
# Each distribution contains values between 0 and 1
N = 100000
k = 10
B = k  # number of bins

x = np.zeros(N)
for i in range(k):
    x = x + np.random.random(N)
x = x/(k+0.0)

# Now generate the histogram using B bins
values, bins = np.histogram(x, bins=np.linspace(0, 1, B))
bin_width = 1/(B+0.0)
bar(bins[0:-1], values, width=bin_width)




# Throw a 6-sided die randomly:
x = np.ones(N)
for i in range(k):
    x = x * ceil(np.random.random(N)*6)
#x = x/(k+0.0)

# Now generate the histogram using B bins
values, bins = np.histogram(x, bins=np.linspace(0, 6, B))
bin_width = 1/(B+0.0)
bar(bins[0:-1], values, width=bin_width)