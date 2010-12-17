nh4 <- read.csv('http://datasets.connectmv.com/file/ammonia.csv')
attach(nh4)
summary(Ammonia)              # just to check we've got the right data
#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#    9.99   30.22   36.18   36.09   42.37   58.74

# The distribution appears normal, apart from the right-hand-side tail
library(car)
qq.plot(Ammonia)

# Estimate the parameters of the distribution
nh4.mean = mean(nh4)
nh4.sd = sd(nh4)

level <- 50

# Using only the data to calculate p(Ammonia > 50)
# ======================
sum(Ammonia>level) / length(Ammonia)

# Using the distribution to estimate p(Ammonia > 50)
# ======================

# Calculate a z-value first, then the cumulative probability
z <- (level - nh4.mean)/nh4.sd
1-pnorm(z)

# Or, you can get the answer more directly:
1-pnorm(level, mean=nh4.mean, sd=nh4.sd)

# More correctly, we should have used the t-distribution, 
# but we basically get the same answer
1-pt(z, df=(length(Ammonia)-1))
