# How the data were generated/modified
#
# data <- read.csv('/Users/kevindunn/ConnectMV/Datasets/KamyrData/kamyr_data/kappa-number-original.csv', col.names="Kappa" )
# 
# set.seed(42)
# N = length(data$Kappa)
# Kappa <- round(data$Kappa * 0.94 + rnorm(N, mean=2, sd=2), 1)
# library(car)
# qq.plot(Kappa)
# kapdata <- data.frame(Kappa)
# write.csv(kapdata, 'kappa-number.csv', row.names=F)

# Use the first 2000 data points to construct a Shewhart monitoring chart for the Kappa number. 
# You may use any subgroup size you like. 
# Then use the remaining data as your phase II (testing) data. 
# Does the chart perform as expected?

kappa <- read.csv('http://datasets.connectmv.com/file/kappa-number.csv')
summary(kappa)
attach(kappa)    # gives access to the variable "Kappa"

N.all <- length(Kappa)
N.phase1 <- 2000
N.phase2 <- N.all - N.phase1
N.subgroup <- 5

phase1.start <- 1
phase1.end <- floor(N.phase1/N.subgroup)
phase2.start <- phase1.end + 1
phase2.end <- floor(N.all/N.subgroup)

# Plot all the data
bitmap('../images/Kappa-raw-data.png', type="png256", width=10, height=4, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(Kappa, type="p", pch=".", cex=2, main="", ylab="Kappa number: raw data", 
     xlab="Sequence order")
abline(v=N.phase1, col="gray50")
text(N.phase1/2, 10, "Phase I data", col="blue")
text(N.phase1 + N.phase2/2, 10, "Phase II data", col="blue")
dev.off()

# We won't check the phase I raw data for outliers; we will use the phase I 
# subgroups to check for outliers.

# Create the subgroups on ALL the raw data.  Form a matrix with `N.subgroup` rows
# placing the vector of data down each row, then going across to form the columns.

# Calculate the mean and standard deviation within each subgroup (columns of the matrix)
reshaped.data <- matrix(Kappa, N.subgroup, N.all/N.subgroup)
subgroup.x.bar <- apply(reshaped.data, 2, mean)
subgroup.S <- apply(reshaped.data, 2, sd)

phase1.xbar <- subgroup.x.bar[phase1.start:phase1.end]
phase1.S <- subgroup.S[phase1.start:phase1.end]
phase2.xbar <- subgroup.x.bar[phase2.start:phase2.end]
phase2.S <- subgroup.S[phase2.start:phase2.end]

# We are going to repeatedly have to calculate the phase 1 limits.  Create a function.
shewhart_limits <- function(xbar, S, subgroup.size, N.stdev=3){
    # Give the xbar and S vector containing the subgroup means and standard deviations.
    # Also give the subgroup size used.  Returns the lower and upper control limits
    # for the Shewhart chart (UCL and LCL) which are N.stdev away from the target.
    
    x.double.bar <- mean(xbar)     
    s.bar <- mean(S)
    an = c(NA, 0.793, 0.886, 0.921, 0.940, 0.952, 0.959, 0.965)
    LCL <- x.double.bar - 3*s.bar/an[subgroup.size]/sqrt(subgroup.size)
    UCL <- x.double.bar + 3*s.bar/an[subgroup.size]/sqrt(subgroup.size)
    c(LCL, UCL)
    
return(list(LCL, x.double.bar, UCL))
}
limits <- shewhart_limits(phase1.xbar, phase1.S, N.subgroup)
LCL <- limits[1]
xdb <- limits[2]
UCL <- limits[3]
c(LCL, xdb, UCL)

# Any points outside these limits?  Yup, quite a few.
bitmap('../images/Kappa-phaseI-first-round.png', type="png256", width=10, height=4, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(phase1.xbar, type="b", pch=".", cex=5, main="", ylab="Phase I subgroups: round 1", 
     xlab="Sequence order")
abline(h=UCL, col="red")
abline(h=LCL, col="red")
abline(h=xdb, col="green")
lines(phase1.xbar, type="b", pch=".", cex=5)
dev.off()

# Find the indices of the point outside the limits.  You could use the identify function,
# or you can find them programatically, using boolean (logical) vectors.  Take a look 
# at what the variables "outside" and "inside" look like to understand what they do.
outside <- (phase1.xbar > UCL) + (phase1.xbar < LCL)
outside <- as.logical(outside)
inside <- !outside     

# Now use only the data inside the existing limits to recalculate the phase I limits.
phase1.xbar <- phase1.xbar[inside]
phase1.S <- phase1.S[inside]
limits <- shewhart_limits(phase1.xbar, phase1.S, N.subgroup)
LCL <- limits[1]
xdb <- limits[2]
UCL <- limits[3]
c(LCL, xdb, UCL)

# Replot the data: everything is inside the limits this time
bitmap('../images/Kappa-phaseI-second-round.png', type="png256", width=10, height=4, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(phase1.xbar, type="b", pch=".", cex=5, main="", ylab="Phase I subgroups: round 2", 
     xlab="Sequence order")
abline(h=UCL, col="red")
abline(h=LCL, col="red")
abline(h=xdb, col="green")
lines(phase1.xbar, type="b", pch=".", cex=5)
dev.off()

outside <- (phase1.xbar > UCL) + (phase1.xbar < LCL)
sum(outside)  # yeah, it is zero!

# Using subgroups of size 4 or smaller will require an additional
# round of pruning subgroups  
outside <- as.logical(outside)
inside <- !outside
phase1.xbar <- phase1.xbar[inside]
phase1.S <- phase1.S[inside]
limits <- shewhart_limits(phase1.xbar, phase1.S, N.subgroup)
LCL <- limits[1]
xdb <- limits[2]
UCL <- limits[3]
c(LCL, xdb, UCL)

# Replot the data: everything is inside the limits after the second
# or third round of pruning.
bitmap('../images/Kappa-phaseI-third-round.png', type="png256", width=10, height=4, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(phase1.xbar, type="b", pch=".", cex=5, main="", ylab="Phase I subgroups: round 3", 
    xlab="Sequence order")
abline(h=UCL, col="red")
abline(h=LCL, col="red")
abline(h=xdb, col="green")
lines(phase1.xbar, type="b", pch=".", cex=5)
dev.off()

outside <- (phase1.xbar > UCL) + (phase1.xbar < LCL)
sum(outside)  # yeah, it is zero!

# Now test the Shewhart limits on the phase II data
bitmap('../images/Kappa-phaseII-testing.png', type="png256", width=10, height=4, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(phase2.xbar, type="b", pch=".", cex=5, main="", ylab="Phase II subgroups: testing", 
     xlab="Sequence order")
abline(h=UCL, col="red")
abline(h=LCL, col="red")
abline(h=xdb, col="green")
lines(phase2.xbar, type="b", pch=".", cex=5)
dev.off()
outside.phase2 <- (phase2.xbar > UCL) + (phase2.xbar < LCL)
alpha <- sum(outside.phase2) / length(phase2.xbar)
alpha  

# Alpha = 7.5% for this phase 2 data, much higher than the 0.27% expected for 
# 3 sigma limits to be expected, because there are process problems on at 
# least 3 occasions in this phase 2 data.