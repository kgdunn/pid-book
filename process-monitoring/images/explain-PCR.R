library(RSvgDevice)

steps <- seq(-15, 15, 0.01)

PCR = 2.0      # Create one figure with this at 0.5, and the other with this at 2.0
USL = 95
LSL = 65

base.sd = (USL-LSL)/PCR/6
base.mean = 80

base.sd

steps <- steps*base.sd + base.mean

raw <- dnorm(steps, mean=base.mean, sd=base.sd)

USL = base.mean + PCR*base.sd*6/2
LSL = base.mean - PCR*base.sd*6/2
c(LSL, USL)
z.LSL = (LSL-base.mean)/base.sd
z.USL = (USL-base.mean)/base.sd
z.LSL
z.USL


devSVG("explain-PCR-half-raw.svg", width=20, height=10)
plot(steps, raw, lwd=2, type="l", xlab="Viscosity (cP)", ylab="", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, xlim=c(20, 140))
abline(v=base.mean, col="grey80")
abline(v=USL, col="grey40")
abline(v=LSL, col="grey40")
abline(h=0)
dev.off()
