coeff <- read.csv('coefficient-plot-LDPE-A-is-6.csv')


library(lattice)

bitmap('coefficient-plot-LDPE-A-is-6.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.5, 4.5, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
barchart(as.matrix(coeff$Value), ylab=list(label="X-variables", cex=1.5), xlab=list(cex=1.5,label="Coefficients related to y=Conversion"), 
         scales=list(y=list(labels=coeff$Name),cex=1.25), col=0)
dev.off()