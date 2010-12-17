z <- seq(-5, 5, 0.1)
norm <- pnorm(z)

bitmap('../images/normal-t-comparison.png', type="png256", width=12, height=7, res=300, pointsize=14) 
par(mar=c(4.2, 4.2, 2.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)

layout(matrix(c(1,2), 1, 2))
plot(z, norm, type="p", pch=".", cex=5, main="Normal and t-distribution (df=6)", ylab="Cumulative probability")
lines(z, pt(z, df=6), type="l", lwd=2)
legend(0.5, y=0.35, legend=c("Normal distribution", "t-distribution (df=8)"), pch=c(".", "-"), pt.cex=c(5, 2))

plot(z, norm, type="p", pch=".", cex=5, main="Normal and t-distribution (df=35)", ylab="Cumulative probability")
lines(z, pt(z, df=35), type="l", lwd=2)
legend(0.5, y=0.35, legend=c("Normal distribution", "t-distribution (df=35)"), pch=c(".", "-"), pt.cex=c(5, 2))
dev.off()