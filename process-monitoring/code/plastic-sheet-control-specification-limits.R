bitmap('../images/plastic-sheet-control-specification-limits.png', type="png256", width=9, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 2, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)

n = 4                   # subgroup size
Cp = 1.7
x.range = 0.8
x.sd = x.range/Cp/6     # process std.dev.
x.bar = 2               # process target
LSL = x.bar - 0.4
USL = x.bar + 0.4
LCL = x.bar - 3 * x.sd / sqrt(n)
UCL = x.bar + 3 * x.sd / sqrt(n)

# A vector of 500 equally spaced points, with 10% offset on either side
x <- seq(LSL-0.1*x.range, USL+0.1*x.range, x.range/500)  
px <- dnorm(x, mean=x.bar, sd=x.sd)
p.shewhart <- dnorm(x, mean=x.bar, sd=x.sd/sqrt(n))

plot(x, p.shewhart, type="l", xlab=(expression(""*x)), ylab="", frame.plot=FALSE, 
                    main=(expression(""*mu*"=2.0")), xlim=c(LSL, USL), cex.lab=1.8, 
                    cex.main=1.8, lwd=3, cex.sub=1.8, cex.axis=1.8, yaxt="n")
lines(x, px, type="l", col="gray50")
abline(v=x.bar)

upper.limit = max(p.shewhart)*0.8
segments(x0=LSL,y0=0, x1=LSL, y1=upper.limit, col="gray30")
segments(x0=USL,y0=0, x1=USL, y1=upper.limit, col="gray30")
segments(x0=LCL,y0=0, x1=LCL, y1=upper.limit, col="red")
segments(x0=UCL,y0=0, x1=UCL, y1=upper.limit, col="red")
text(LSL, upper.limit, "LSL", cex=1.3, pos=3)
text(USL, upper.limit, "USL", cex=1.3, pos=3)
text(LCL, upper.limit, "LCL", cex=1.3, pos=3)
text(UCL, upper.limit, "UCL", cex=1.3, pos=3)

# Sigma for the process
y <- dnorm(x.bar+x.sd, mean=x.bar, sd=x.sd)
arrows(x0=x.bar, y0=y, x1=x.bar+x.sd, y1=y, code=3, angle=15, length=0.1) 
text(x.bar + x.sd, y+0.2, (expression(""*sigma)), cex=1.8, pos=4)

# Sigma for the Shewhart chart
y <- dnorm(x.bar+x.sd/sqrt(n), mean=x.bar, sd=x.sd/sqrt(n))
arrows(x0=x.bar, y0=y, x1=x.bar+x.sd/sqrt(n), y1=y, code=3, angle=15, length=0.1) 
text(x.bar+x.sd/sqrt(n), y+0.2, (expression(""*sigma/sqrt(n))), cex=1.8, pos=4)

dev.off()