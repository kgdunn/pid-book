web <- read.csv('http://stats4.eng.mcmaster.ca/datasets/website-traffic.csv')
summary(web)

# Check for normality: use a qq-plot
qqnorm(web$Visits)
qqline(web$Visits)

# Use the qq.plot function from the "car" package for qq-plots with error bars
library(car)
qq.plot(web$Visits)

# Mean and standard deviation
visits.mean <- mean(web$Visits)              # 22.23364
visits.sd <- sd(web$Visits)                  #  8.331826

z.LB <- (10 - visits.mean) / visits.sd
z.UB <- (30 - visits.mean) / visits.sd
c(z.LB, z.UB)                                # -1.4683029  0.9321312
pnorm(z.UB) - pnorm(z.LB)                    #  0.7533546
#-------- END OF CODE HERE


bitmap('../images/website-visits-univariate.png', type="png256", width=14, height=7, res=300, pointsize=14) 
layout(matrix(c(1,2), 1, 2))

qqnorm(web$Visits)#, cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
qqline(web$Visits)

# Use the qq.plot function from the "car" package for better looking plots
library(car)
qq.plot(web$Visits, main="Test for normality (qq-plot)")
dev.off()
