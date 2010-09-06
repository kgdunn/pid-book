z <- seq(-4, 4, 0.01)

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/logistic-regression-function.png', type="png256", width=5, height=5, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.2, cex.main=1.3, cex.sub=1.5, cex.axis=1.3)

plot(z, pnorm(z), type="l", xlab="Function input", ylab="Function output")
abline(h=0, col = "gray30", lty=3, lwd=2)
abline(h=1, col = "gray30", lty=3, lwd=2)
dev.off()