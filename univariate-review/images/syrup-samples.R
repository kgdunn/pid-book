syrup.sigma = 40
c_norm = qnorm(0.975)

range = 60
# range/2 = c_norm * syrup.sigma / sqrt(n)    (by definition)
# range/2 * sqrt(n) = c *s
# sqrt(n) = c_norm * syrup.sigma * 2 / range
n = (c_norm * syrup.sigma * 2 / range)^2
n
