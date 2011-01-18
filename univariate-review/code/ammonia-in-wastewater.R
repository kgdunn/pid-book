nh4 <- read.csv('http://datasets.connectmv.com/file/ammonia.csv')
summary(nh4$Ammonia)              # just to check we've got the right data
#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#    9.99   30.22   36.18   36.09   42.37   58.74

# The distribution appears normal, apart from the right-hand-side tail
library(car)
qqPlot(nh4$Ammonia)

# Estimate the parameters of the distribution
nh4.mean = mean(nh4$Ammonia)  # 36.09499
nh4.sd = sd(nh4$Ammonia)      # 8.518928

level <- 40

# Using only the data to calculate p(Ammonia > 40)
# ======================
sum(nh4$Ammonia>level) / length(nh4$Ammonia)

# Using the distribution to estimate p(Ammonia > 40)
# ======================

# Calculate a z-value first, then the cumulative probability
z <- (level - nh4.mean)/nh4.sd
1-pnorm(z)

# Or, you can get the answer more directly:
1-pnorm(level, mean=nh4.mean, sd=nh4.sd)

# More correctly, we should have used the t-distribution, 
# but we basically get the same answer
1-pt(z, df=(length(nh4$Ammonia)-1))
