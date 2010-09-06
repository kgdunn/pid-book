
N=50
set.seed(10)
x <- rnorm(N, mean=12, sd=4)
y <-  5*x + rnorm(N, mean=0, sd=6)
model = lm(y~x)
SE = sqrt(sum(model$residuals * model$residuals)/model$df.residual)


bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/show-naive-predictions.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.4, cex.sub=1.8, cex.axis=1.8)
plot(x,y,cex=1.5)
abline(model, col="red", lwd=3)
abline(a= model$coef[1]+2*SE, b=model$coef[2], col="black", lty=2)
abline(a= model$coef[1]-2*SE, b=model$coef[2], col="black", lty=2)

x0=7.5
ybase = model$coef[1]+model$coef[2]*x0
ybase
ybase-2*SE
arrows(x0=x0,y0=ybase-2*SE,x1=x0,y1=ybase+2*SE, lwd=2, angle=15, length=0.25, code=3)
text(7.6,30, "4 times SE", cex=2, pos=4)
dev.off()