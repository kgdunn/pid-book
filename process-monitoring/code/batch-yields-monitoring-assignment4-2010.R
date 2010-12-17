batch <- read.csv('http://datasets.connectmv.com/file/batch-yields.csv')
summary(batch)  # make sure we have the expected data
attach(batch)

plot(Yield)     # to get a feel for the data; looks pretty good; no unusual outliers

N.raw = length(Yield)
N.sub = 5       # subgroup size
subgroup <- matrix(Yield, N.sub, N.raw/N.sub)
N.groups <- ncol(subgroup)
dim(subgroup)   # 5 by 60 matrix


subgroup.sd <- apply(subgroup, 2, sd)
subgroup.xbar <- apply(subgroup, 2, mean)

# Take a look at what these numbers mean
plot(subgroup.xbar, type="b", ylab="Subgroup average")
plot(subgroup.sd, type="b",  ylab="Subgroup spread")

# Report your target value, lower control limit and upper control limit, showing the calculations you made. 
target <- mean(subgroup.xbar)
Sbar <- mean(subgroup.sd)
an <- 0.94
sigma.estimate <- Sbar / an  # a_n value is from the table when subgroup size = 5
LCL <-  target - 3 * sigma.estimate/sqrt(N.sub)
UCL <- target + 3 * sigma.estimate/sqrt(N.sub)
c(LCL, target, UCL)

bitmap('../images/batch-yields-monitoring.png', type="png256", width=10, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(subgroup.xbar, ylim=c(LCL-5, UCL+5), ylab="Subgroup means", main="Shewhart chart")
abline(h=target, col="green")
abline(h=UCL, col="red")
abline(h=LCL, col="red")