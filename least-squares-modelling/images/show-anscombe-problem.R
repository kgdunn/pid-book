data(anscombe)
mean(anscombe)
#       x1       x2       x3       x4       y1       y2       y3       y4 
# 9.000000 9.000000 9.000000 9.000000 7.500909 7.500909 7.500000 7.500909 

 
attach(anscombe)
summary(lm(y1 ~ x1))


x = x1
y = y1
# Anscombe data
x <- c(10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5)
y <- c(8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68)


# Other data
#x <- c(20, 60, 100, 140, 180, 220, 260, 300, 340, 380)
#y <- c(.18, 0.37, 0.35, 0.78, 0.56, 0.75, 1.18, 1.36, 1.17, 1.65)

# Devore data
#x<-c(398, 292, 352, 575, 568, 450, 550, 408, 484, 350, 503, 600, 600)
#y<-c(.15, .05, .23, .43, .23, .40, .44, .44, .45, .09, .59, .63, .60)


N = length(x)
N
x.bar = mean(x)
y.bar = mean(y)
num <- sum((x - x.bar) * (y - y.bar)) # 55.0
den <- sum((x - x.bar) * (x - x.bar))  # 110.0

b1 <- num/den
b0 <- y.bar - b1 * x.bar
y.bar
x.bar
num
den
c(b0, b1)

predictions <- b0 + x*b1
predictions
error <- y - predictions

sum(predictions*error)  # check the definitions in the course notes

summary(error)
SE <- sqrt(sum(error^2) / (N-2))
SE.b1 <- sqrt(SE^2 / den)
SE.b0 <- sqrt(SE^2 *(1/N + (x.bar^2)/den))
c(SE, SE.b0, SE.b1)

z.b0 = b0/SE.b0
z.b1 = b1/SE.b1
c(z.b0, z.b1)
t.critical = qt(0.975, df=(N-2))
t.critical
SE.b0
b1
b0.LB <- b0 - t.critical*SE.b0
b0.UB <- b0 + t.critical*SE.b0
b1.LB <- b1 - t.critical*SE.b1
b1.UB <- b1 + t.critical*SE.b1
c(b0.LB, b0.UB)
c(b1.LB, b1.UB)

# R2, TSS, RegSS, RSS
TSS <- sum((y - y.bar)^2)
RegSS <- sum((predictions-y.bar)^2)
RSS <- sum(error^2)
c(TSS, RegSS, RSS, RegSS/TSS)
RSS.adj <- 1- (RSS/(N-2)) / (TSS/(N-1))
RSS.adj
# Error bounds for y-hat
x.new = seq(-2, 15, 0.01)
y.new = b0 + x.new*b1
error.delta <- t.critical*SE*sqrt(1+ 1/N + ((x.new-x.bar)^2)/den)



bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/show-anscome-solution-unmarked.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(x,y, xlim=c(0, 14), ylim=c(0, 12), cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")
grid(lwd=2)
points(x, y)
abline(a=b0, b=b1, col="red", lty=1)
points(x.bar, y.bar, pch="*", cex=2)
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/show-anscome-solution-marked.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(x,y, xlim=c(0, 14), ylim=c(0, 12), cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")
grid(lwd=2)
points(x, y)
abline(a=b0, b=b1, col="red", lty=1)
abline(a=(y.bar-b1.UB*x.bar), b=b1.UB, col="gray60", lty=3, lwd=2)
abline(a=(y.bar-b1.LB*x.bar), b=b1.LB, col="gray60", lty=4, lwd=2)
legend(x=0.5, y=12, legend=c("Least squares fit", "b1 at lower bound", "b1 at upper bound"), col=c("red", "gray60", "gray60"), lty=c(1, 4, 3), lwd=c(1,2,2))
points(x.bar, y.bar, pch="*", cex=2)
dev.off()


bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/show-anscome-solution-with-yhat-bounds.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(x,y, cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="", ylim=c(1, 12))
grid(lwd=2)
points(x, y)
abline(a=b0, b=b1, col="red", lty=1)
lines(x.new, y.new + error.delta, col="gray60")
lines(x.new, y.new - error.delta, col="gray60")

legend(x=6.5, y=2.5, legend=c("Least squares fit", "Lower and upper bound on y-predicted"), col=c("red", "gray60"), lty=c(1,1), lwd=c(1,1)*2)
points(x.bar, y.bar, pch="*", cex=2)
dev.off()



bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/show-anscombe-problem-1.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(x, y, cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")
grid(lwd=2)
points(x, y)
dev.off()



model <- lm(y ~ x)
summary(model)



