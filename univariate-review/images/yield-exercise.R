yields <- c(23, 19, 17, 18, 24, 26, 21, 14, 18)
yield.mean = mean(yields)
yield.sd = sd(yields)
n = 9


# Using the t-distribution

df = n - 1
# 90% confidence
# --------------
p = 0.90
c_t <- qt(p + (1-p)/2, df)
c_t
delta =  c_t * yield.sd / sqrt(n)
LB <- yield.mean - delta
UB <- yield.mean + delta
c(LB, UB, delta)

# 95% confidence
# --------------
p = 0.95
c_t <- qt(p + (1-p)/2, df)
c_t
delta =  c_t * yield.sd / sqrt(n)
LB <- yield.mean - delta
UB <- yield.mean + delta
c(LB, UB, delta)


# 99% confidence
# --------------
p = 0.99
c_t <- qt(p + (1-p)/2, df)
c_t
delta =  c_t * yield.sd / sqrt(n)
LB <- yield.mean - delta
UB <- yield.mean + delta
c(LB, UB, delta)






#------------------------- OLD CODE

yield.sigma = 3.5
# 90% confidence
# --------------
p = 0.90
c_norm <- qnorm(p + (1-p)/2)
delta =  c_norm * yield.sigma / sqrt(n)
LB <- yield.mean - delta
UB <- yield.mean + delta
c(LB, UB, delta)
#[1] 18.08100  21.91900  1.918996


# 95% confidence
# --------------
p = 0.95
c_norm <- qnorm(p + (1-p)/2)
c_norm
delta =  c_norm * yield.sigma / sqrt(n)
LB <- yield.mean - delta
UB <- yield.mean + delta
c(LB, UB, delta)
# [1] 17.71338  22.28662  2.286625

# 99% confidence
# --------------
p = 0.99
c_norm <- qnorm(p + (1-p)/2)
delta =  c_norm * yield.sigma / sqrt(n)
LB <- yield.mean - delta
UB <- yield.mean + delta
c(LB, UB, delta)
# [1] 16.99487  23.00513  3.005134