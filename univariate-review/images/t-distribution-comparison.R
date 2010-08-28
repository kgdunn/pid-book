#bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/t-distribution-comparison.png', type="png256", width=14, height=7, res=250, pointsize=14)

x <- seq(-5, 5, 0.01)
p.x <- dnorm(x)
p.t <- dt(x, df=8)
plot(x, p.x, type="l", xlab="z", ylab="p(z)", frame.plot=FALSE, main="", cex.lab=1.8, cex.main=1.8, lwd=3, cex.sub=1.8, cex.axis=1.8, xlim=c(-4,4))
lines(x, p.t)
abline(v=0)

legend(1, y=0.35, legend=c("Normal distribution", "t-distribution (df=8)"), lwd = c(3, 1))

#dev.off()