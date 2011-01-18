data <-read.csv('system-comparison.csv', header=TRUE)
summary(data)

A <- data$obs[data$method==data$method[1]]
B <- data$obs[data$method==data$method[11]]
B

bitmap('system-comparison-boxplot-plots.png', type="png256", width=12, height=7, res=250, pointsize=14) 
limits <- range(data$obs)
layout(matrix(c(1, 1:3), 1, 4))
boxplot(data$obs ~ data$method, cex.lab=1.8, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8, ylim=limits, main="Batch yield (%) for two trials")
plot(A, main="A", ylab="", ylim=limits, cex.lab=1.8, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8)
abline(h=mean(A))
plot(B, main="B", ylab="", ylim=limits, cex.lab=1.8, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8)
abline(h=mean(B))
dev.off()


bitmap('system-comparison-boxplot-plots-obvious.png', type="png256", width=12, height=7, res=250, pointsize=14) 
data$obs[data$method==data$method[1]] <- data$obs[data$method==data$method[1]] - 12
data$obs[data$method==data$method[11]] <- data$obs[data$method==data$method[11]] + 4
limits <- range(data$obs)
A <- data$obs[data$method==data$method[1]]
B <- data$obs[data$method==data$method[11]]
layout(matrix(c(1, 1:3), 1, 4))
boxplot(data$obs ~ data$method, cex.lab=1.8, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8, ylim=limits, main="Batch yield (%) for two trials")
plot(A, main="A", ylab="", ylim=limits, cex.lab=1.8, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8)
abline(h=mean(A))
plot(B, main="B", ylab="", ylim=limits, cex.lab=1.8, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8)
abline(h=mean(B))
dev.off()

library(BHH2)
data(tab03B1)

# Use this A.hist if you want to check BHH2 figures
A.hist = (tab03B1$yield-80)*2.341+70
# mean(A)
# mean(B)
sd(A)
sd(B)
# mean(A.hist)

# Create more data like A.hist.  
# N = 300
# phi=-0.3
# shock_mean = 0
# shock_sd = sd(A.hist)
# targetY = mean(A)
# 
# A.hist.sim = numeric(N)   # vector of zeros
# for (k in 2:N){
# 	toadd = rnorm(1, mean=shock_mean, sd=shock_sd)
# 	A.hist.sim[k] <- phi*(A.hist.sim[k-1]) + toadd 
# }
# A.hist.sim <- A.hist.sim + targetY
# plot(A.hist.sim[1:N-1], A.hist.sim[2:N])
# lines(lowess(A.hist.sim[1:N-1], A.hist.sim[2:N]))
# cov(A.hist.sim[1:N-1], A.hist.sim[2:N])
# range(A.hist.sim) 
# write.csv(round(A.hist.sim,2), '/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/system-comparison-historical-data.csv', quote=FALSE, row.names=FALSE)

A.hist <- read.csv('system-comparison-historical-data.csv', header=FALSE)
#A.hist <- read.csv('http://datasets.connectmv.com/file/batch-yields.csv', header=FALSE)
A.hist <- A.hist$V1
N = length(A.hist)

#library(nlme)
#acf(A.hist)

bitmap('system-comparison-sequence-plot.png', type="png256", width=10, height=7, res=250, pointsize=14) 
plot(c(A.hist, B), xlab="300 samples from A, 10 samples of B", ylab="Yield (%)", main="", cex.lab=1.5, cex.main=1.8, lwd=3, cex.sub=1.8, cex.axis=1.8)
abline(v=length(A.hist))
text(length(A.hist)/2, 98, "A", cex=2)
text(length(A.hist)+length(B), 98, "B", cex=2)
dev.off()


bitmap('system-comparison-autocorrelation-scatterplot.png',type="png256", width=10, height=7, res=250, pointsize=14) 
plot(A.hist[1:N-1], A.hist[2:N], xlab="x[k]", ylab="x[k+1]", main="Autocorrelation between successive values of batch yield", cex.lab=1.2, cex.main=1.2, lwd=3, cex.sub=1.2, cex.axis=1.2)
lines(lowess(A.hist[1:N-1], A.hist[2:N]))
dev.off()

summary(A.hist)
delta=10
A.hist.means <- numeric(N-delta+1) 

for (i in 1:(N-delta+1))
{
    A.hist.means[i] <- mean(A.hist[i:(i+delta-1)])
}

# Cross-reference to BHH: 
# (A.hist.means-70)/2.341+80  <---- should get the same results as their table 2.2 (edition 1)

A.hist.means.diffs = numeric(N-delta-delta+1) 
for (i in 1:(N-delta-delta+1))
{
    A.hist.means.diffs[i] <- A.hist.means[i+delta] - A.hist.means[i]   # (mean of group k+1) - (mean of group k)	
}
# Cross-reference to BHH: 
# A.hist.means.diffs/2.341  <---- should get the same results as their table 2.2 (edition 1)

difference = mean(B)-mean(A)
maxrange = max(ceiling(abs(A.hist.means.diffs)))

#bitmap('system-comparison-dotplot-grouped.png', type="png256", width=12, height=7, res=300, pointsize=14) 
dotPlot(A.hist.means.diffs, xlab="Difference between means of 2 adjacent groups (10 batches per group)", xlim=c(-maxrange, maxrange))
lines(x=c(difference, difference), y=c(0,0.35))
arrows(difference, 0.2, difference+1.6, 0.2, code=2)
text(difference, 0.40, round(difference,2))
#dev.off()

sum(A.hist.means.diffs > difference)
length(A.hist.means.diffs)
sum(A.hist.means.diffs > difference) / length(A.hist.means.diffs)


#---------
# Using external variance estimate
#---------------------------
B.mean <- mean(B)
A.mean <- mean(A)
difference <- B.mean - A.mean
c_n = qnorm(0.975)
sigma = sd(A.hist)
sigma
na = length(A)
nb = length(B)

denom_sigma =  sqrt(sigma^2*(1/na + 1/nb))

z = (difference - 0)/denom_sigma
z
1-pnorm(z)

LB = difference - c_n * sqrt(sigma^2*(1/na + 1/nb))
UB = difference + c_n * sqrt(sigma^2*(1/na + 1/nb))
c(LB, UB)

#---------
# Using intenal variance estimate
#---------------------------
na = length(A)
nb = length(B)
B.mean <- mean(B)
A.mean <- mean(A)
B.var <- var(B)
A.var <- var(A)
dof <- na+nb-2
var.pooled = ((na-1)*A.var + (nb-1)*B.var) / (na+nb-2)

difference <- B.mean - A.mean
c_t = qt(0.975, df = dof)

denom_sigma =  sqrt(var.pooled*(1/na + 1/nb))
denom_sigma
z = (difference - 0)/denom_sigma
z
1-pt(z, df=dof)

# LB = difference - c_t * denom_sigma
# UB = difference + c_t * denom_sigma
# c(LB, UB)
