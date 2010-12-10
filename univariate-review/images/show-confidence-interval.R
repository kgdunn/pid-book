library(RSvgDevice)
devSVG("show-confidence-interval.svg", width=20, height=10)


z <- seq(-4, 4, 0.05)
val=2.2

plot(z, dnorm(z), type="l", cex.lab=1.5, cex.main=1.8, lwd=3, cex.sub=1.8, cex.axis=1.8, ylab="p(z)", xlab="z", xaxt="n")
abline(v=-val, col="gray70")
abline(v=+val, col="gray70")
abline(h=0)

axis(1, at=c(-val, +val), labels=c("-c", "+c"), cex.lab=2)
dev.off()
