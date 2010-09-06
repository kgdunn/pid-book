# Non-constant error
# ---------------------
set.seed(42)
x <- seq(5, 9.0, 0.1)
N = length(x)
y <- (0.4*x + exp(0.6*x) -2 + rnorm(N, sd=9))/2.3

for (i in seq(N)){
    y[i] = y[i]
}
startx = 11
endx = 30


bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/nonlinear-linear-region.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(x[1:startx], y[1:startx], pch=21, xlim=range(x), ylim=range(y), bg=1, xlab="x", ylab="y")
points(x[(startx+1):endx], y[(startx+1):endx], pch=2)
points(x[endx+1:N], y[endx+1:N], pch=21, bg=1)

abline(v=6.05, lty=2)
abline(v=7.95, lty=2)

model <- lm(y[(startx+1):endx] ~ x[(startx+1):endx])
abline(model, lwd=2, lty=2)
lines(lowess(x,y), col="blue", lty=3, lwd=3)
ytext=80
arrows(6.05, ytext, 7.95, ytext, angle=15, length=0.25, code=3)
text((6.05+7.95)/2, ytext, "Model region", pos=1)
dev.off()


# What if we had used the whole region to build the linear model?
model.all <- lm(y ~ x)
bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/nonlinear-detection.png', type="png256", width=16, height=16/3, res=300, pointsize=14)
layout(matrix(c(1,2,3), 1, 3))
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(x, y, xlab="x", ylab="y")
abline(model.all)

plot(x, model.all$residuals, xlab="x", ylab="Residuals")
lines(lowess(x, model.all$residuals), col="blue", lty=2, lwd=2)
abline(h=0, lwd=2, lty=2)
plot(model.all$fitted.values, model.all$residuals, xlab=expression(hat(y)), ylab="Residuals")
lines(lowess(model.all$fitted.values, model.all$residuals), col="blue", lty=2, lwd=2)
abline(h=0, lwd=2, lty=2)
dev.off()