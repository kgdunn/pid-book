# Create 500 normally distributed points
# with a mean of 1100 and standard deviation
# of 50 units.
data = rnorm(500, mean=1100, sd=50)
hist(data,
     xlab="Mass [g] of each package",
     ylab="Number of packages (N=500)")
