steps <- seq(-5, 5, 0.01)
Delta = 1
N = 5

base.sd = 3
base.mean = 6
steps <- steps + base.mean


raw <- dnorm(steps, mean=base.mean, sd=base.sd)
raw.sample <- dnorm(steps, mean=base.mean, sd=base.sd/sqrt(N))


bitmap('/Users/kevindunn/transfer/Stats-course/Course notes/Control charts/images/explain-shewhart.png', type="png256", width=10, height=7, res=300, pointsize=14)

plot(steps, raw.sample, lwd=2, type="l", xlab="x", ylab="Probability density", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
lines(steps, raw)

abline(v=base.mean)

#yval = dnorm(1)
#arrows(x0=base.mean, y0=yval, x1=base.mean+base.sd, y1=yval, code=2)
#abline(v=base.mean+base.sd)

yval = 0.3
arrows(x0=base.mean, y0=yval, x1=base.mean+3*(base.sd/sqrt(N)), y1=yval, code=2)
abline(v=base.mean+3*(base.sd/sqrt(N)), col="red")
abline(v=base.mean-3*(base.sd/sqrt(N)), col="red")
text(base.mean+1.6*(base.sd/sqrt(N)), yval-0.01, (expression("3"*sigma[bar(x)])), cex=1.3)

dev.off()