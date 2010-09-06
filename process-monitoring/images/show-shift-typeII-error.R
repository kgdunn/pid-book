steps <- seq(-5, 5, 0.01)
Delta = 1
N = 4

base.sd = 1
base.mean = 6
steps <- steps + base.mean
shift <- steps + base.mean + Delta


raw <- dnorm(steps, mean=base.mean, sd=base.sd)
raw.sample <- dnorm(steps, mean=base.mean, sd=base.sd/sqrt(N))
after <- dnorm(steps, mean=base.mean+Delta, sd=base.sd)
after.sample <- dnorm(steps, mean=base.mean+Delta, sd=base.sd/sqrt(N))

#bitmap('/Users/kevindunn/transfer/Stats-course/Course notes/Control charts/images/show-shift-beta-error-raw.png', type="png256", width=20, height=20, res=300, pointsize=14)
library(RSvgDevice)
devSVG("show-shift-beta-error-raw.svg", width=20, height=10)

plot(steps, raw.sample, lwd=2, type="l", ylim=c(0, 1), ylab="Probability density", xlab="X", cex.lab=1.5, cex.main=3, cex.sub=3, cex.axis=3, )
lines(steps, after.sample, col="red", lwd=2)
abline(v=base.mean, col="gray60")
abline(v=base.mean+3*(base.sd/sqrt(N)), col="gray60")
abline(v=base.mean-3*(base.sd/sqrt(N)), col="gray60")
abline(h=0)
y = 0.9
arrows(x0=base.mean, y0=y, x1=base.mean+3*(base.sd/sqrt(N)), y1=y, code=2)
arrows(x0=base.mean, y0=y, x1=base.mean-3*(base.sd/sqrt(N)), y1=y, code=2)
text(base.mean, y+0.05, "From LCL to UCL")


dev.off()


#lines(steps, raw)
#lines(steps, after, col="red")
#yval = dnorm(1)# sd=base.sd/sqrt(N))
#arrows(x0=base.mean, y0=yval, x1=base.mean+base.sd, y1=yval, code=2)
#abline(v=base.mean+base.sd, col="gray60")