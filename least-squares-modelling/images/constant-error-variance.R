library(RSvgDevice)
steps <- seq(-5, 5, 0.01)


devSVG("constanst-error-variance.svg", width=10, height=10)
plot(steps, dnorm(steps), type="l", xaxt="n", yaxt="n", xlab="", ylab="", frame=F)
abline(h=0)
dev.off()
