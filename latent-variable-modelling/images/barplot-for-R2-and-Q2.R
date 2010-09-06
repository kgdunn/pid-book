
# Data from the LDPE case study; PCA on all the variables, all the rows; Simca-P v 11.5 (Nov 2006)

R2 = c(0.369877,0.547855,0.65697,0.747528,0.831526,0.885739,0.928337,0.962801)
Q2 = c(0.253787,0.341342,0.318556,0.250411,0.32386,0.270315,0.19828,0.245897)

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/barplot-for-R2-and-Q2.png', type="png256", width=8, height=3.5, res=300, pointsize=14)
par(cex.lab=1.1, cex.main=1.1, cex.sub=1.1, cex.axis=1.1)
par(mar=c(2.5, 4.2, 1.0, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
layout(matrix(c(1,2), 1, 2))

barplot(R2, names.arg=seq(1,8), col=0, width=1, ylab=expression(paste("Cumulative ",  R^2, " "  )), ylim=c(0,1))
abline(h=c(0,1), col="black")

barplot(Q2, names.arg=seq(1,8), col=0, width=1, ylab=expression(paste("Cumulative ",  Q^2, " "  )), ylim=c(0,1))
abline(v=1.9, col="darkred", lty=2)
abline(v=3.1, col="darkred", lty=2)
abline(h=c(0,1), col="black")
dev.off()