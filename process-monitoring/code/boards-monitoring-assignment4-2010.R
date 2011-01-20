boards <- read.csv('http://datasets.connectmv.com/file/board-thickness.csv')
attach(boards)

N.raw <- length(Thickness)  # Total number of boards
N.sub <- 7                  # subgroup size
N.phase1 <- 500             # number of phase 1 raw data points

# a) Plot all the data.  
bitmap('../images/boards-monitoring-raw-data.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
plot(Thickness, type="p", main="Thickness: all data")
dev.off()

# b) Now assume that boards 1 to 500 are the phase I data; identify unusual boards
bitmap('../images/boards-monitoring-find-outliers-phase1.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
plot(Thickness[1:N.phase1], type="p", main="Phase 1 raw data", ylab="Thickness")
identify(Thickness)             # There are no major outliers
dev.off()

# c) Remove unusual boards from the phase I data. 
#    Calculate the Shewhart monitoring limits and show the phase I data with these limits.  
#    Note: choose an appropriate subgroup size of your choice.

subgroup <- matrix(Thickness, N.sub, N.raw/N.sub)
N.groups <- ncol(subgroup)

subgroup.sd <- apply(subgroup, 2, sd)
subgroup.xbar <- apply(subgroup, 2, mean)

phase1.start <- 1
phase1.end <- floor(N.phase1/N.sub)

target <- mean(subgroup.xbar[phase1.start:phase1.end])
Sbar <- mean(subgroup.sd[phase1.start:phase1.end])

an <- c(NA, 0.793, 0.886, 0.921, 0.940, 0.952, 0.959, 0.965)
sigma.estimate <- Sbar / an[N.sub]  
LCL <-  target - 3 * sigma.estimate/sqrt(N.sub)
UCL <- target + 3 * sigma.estimate/sqrt(N.sub)
round(c(LCL, target, UCL), 0)


# But there is 1 point outside the limits; happens to be the first one: take a short-cut
phase1.start = 2
phase1.end = floor(N.phase1/N.sub)

target <- mean(subgroup.xbar[phase1.start:phase1.end])
Sbar <- mean(subgroup.sd[phase1.start:phase1.end])
sigma.estimate <- Sbar / an[N.sub]  
LCL <-  target - 3 * sigma.estimate/sqrt(N.sub)
UCL <- target + 3 * sigma.estimate/sqrt(N.sub)
round(c(LCL, target, UCL), 0)
# Limits are pretty much the same: not surprising.

bitmap('../images/boards-monitoring-Shewhart-phase1.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.9, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
phase1.data <- subgroup.xbar[1:phase1.end]
plot(phase1.data, type="b", ylim=c(LCL-10, UCL+10), pch=".", cex=5, ylab="Subgroup mean", main="Shewhart chart for phase I: training data")
abline(h=UCL, col="red")
abline(h=LCL, col="red")
abline(h=target, col="green")
dev.off()

# d) Test the Shewhart chart on boards 501 to 2000, the phase II data.  
#    Show the plot and calculate the type I error rate (alpha) from the phase II data.
bitmap('../images/boards-monitoring-Shewhart-phase2.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.9, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
phase2.data <- subgroup.xbar[(phase1.end+1):length(subgroup.xbar)]
plot(phase2.data, type="b", pch=".", cex=5, ylab="Subgroup mean", main="Shewhart chart for phase II: testing data")
abline(h=UCL, col="red")
abline(h=LCL, col="red")
abline(h=target, col="green")
dev.off()

phase2.N <- length(phase2.data)
points.outside <- (sum(phase2.data<LCL) + sum(phase2.data>UCL))
alpha.calculated <- points.outside / phase2.N
c(points.outside, phase2.N, alpha.calculated)
alpha.expected = 0.27/100

# e) Calculate the ARL.  Given the time information in the raw data,
#    use the ARL and calculate how many minutes between a false alarm.  
#    Will the operators be happy this?

ARL = ceiling(1/alpha.calculated)                # On average, you will have about 1 in 24 
                                                 # subgroups giving a false alarm
                                                 # units = [subgroups per false alarm]
n.mins = 15 + 60 + 4*60                          # Or use some other approximation 
product.rate = (N.raw/N.sub) / n.mins            # [subgroups per minute]: i.e. how often 
                                                 # a new subgroup is shown on the screen
minutes.between.false.alarm = ARL / product.rate # [subgroups per false alarm]/[subgroups per minute]
                                                 # = [minutes/false alarm]    
c(num.minutes.production, production.rate, N.raw/N.sub, minutes.between.false.alarm)

# g) How would you monitor if the saws are slowly going out of alignment? 
#    Show the increase in variance over time with a nonparametric smooth of subgroup standard deviation
bitmap('../images/boards-monitoring-subgroup-standard-deviation.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.9, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
plot(subgroup.sd, type="p", ylab="Subgroup standard deviation", main="Slow increase in subgroup variability over the day")
lines(lowess(subgroup.sd))
dev.off()
