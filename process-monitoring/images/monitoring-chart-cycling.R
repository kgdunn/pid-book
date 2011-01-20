feed <- read.csv('/Users/kevindunn/Statistics course/Course notes/Assignments/Written final/images/monitoring-data.csv', header=F)
set.seed(44)
N = length(feed$V1)
Feed <- feed$V1 + rnorm(N, mean=2.0, sd=0.3) 

N.raw <- length(Feed)  # Total number of boards
N.sub <- 5                  # subgroup size
N.phase1 <- N             # number of phase 1 raw data points


bitmap('monitoring-chart-question.png', type="png256", width=15, height=8, res=300, pointsize=14)
layout(matrix(c(1,2), 1, 2))
par(mar=c(3.9, 4.5, 3.0, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.2, cex.main=1.2, cex.sub=1.2, cex.axis=1.2)

layout(matrix(c(1,2),2,1))

plot(Feed[1:N.phase1], type="b", main="Raw data: weight of feed entering", ylab="Feed [kg/s]", xlab="Time-ordered samples")

subgroup <- matrix(Feed, N.sub, N.raw/N.sub)
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

phase1.data <- subgroup.xbar[1:phase1.end]
plot(phase1.data, type="b", ylim=c(LCL-0.25, UCL+0.25), pch=".", cex=5, ylab="Subgroup mean", main="Shewhart chart: weight of feed entering", xlab="Time order")
abline(h=UCL, col="darkred", lty=2, lwd=2); text(1, UCL, "UCL", col="darkred", pos=3)
abline(h=LCL, col="darkred", lty=2, lwd=2); text(1, LCL, "LCL", col="darkred", pos=1)
abline(h=target, col="darkgreen", lwd=2)
lines(phase1.data, type="b", pch=".", cex=5)
dev.off()

plot(cumsum(Feed[1:N.phase1]-2))