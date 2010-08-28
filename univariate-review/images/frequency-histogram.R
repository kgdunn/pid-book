values = rnorm(1000)

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/frequency-histogram.png', type="png256", res=300, width=15, pointsize=14)

m <- matrix(c(1,2), 1, 2)
layout(m)

hist(values, freq=TRUE,  xlab="Random values", cex.lab=1.5, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8, ylab="Frequency (N=1000)")
hist(values, freq=FALSE, xlab="Random values", cex.lab=1.5, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8)

dev.off()