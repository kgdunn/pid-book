bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/normal-distribution-standardized.png', type="png256", width=14, height=7, res=300, pointsize=14)
x <- seq(-3.8, 3.8, 0.01)
px <- dnorm(x)
plot(x, px, type="l", xlab=(expression(""*x)), ylab="p(x)", frame.plot=FALSE, main=(expression(""*mu*"=0")), cex.lab=1.8, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8)
abline(v=0)

abline(v=1, col = "gray60")
arrows(0, y=dnorm(1), x1=1, y1=dnorm(1), code=3) #, length = 0.25, angle = 30, code = 2,      col = par("fg"), lty = par("lty"), lwd = par("lwd"),
text(0.5, dnorm(1)+0.015, (expression(""*sigma)), cex=1.8)

abline(v=2, col = "gray60")
arrows(0, y=dnorm(2), x1=2, y1=dnorm(2), code=3) #, length = 0.25, angle = 30, code = 2,      col = par("fg"), lty = par("lty"), lwd = par("lwd"),
text(1.0, dnorm(2)+0.015, (expression("2"*sigma)), cex=1.8)

abline(v=3, col = "gray60")
arrows(0, y=dnorm(3), x1=3, y1=dnorm(3), code=3) #, length = 0.25, angle = 30, code = 2,      col = par("fg"), lty = par("lty"), lwd = par("lwd"),
text(1.5, dnorm(3)+0.015, (expression("3"*sigma)), cex=1.8)

dev.off()