eta = 4
x <- seq(0, 15, 1)
bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/poisson-distribution.png', type="png256", width=10, height=7, res=200, pointsize=14)
plot(x, dpois(x, lambda=eta), xlab="x = number of events", ylab="p(x)", main=(expression(""*eta*"=4")), type="b", cex.lab=1.5, cex.main=1.8, lwd=2, cex.sub=1.0, cex.axis=1.8, frame.plot=FALSE)
dev.off()
