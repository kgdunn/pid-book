ldpe <- read.csv('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/LDPE-wstar-c-raw-data.csv')
attach(ldpe)

K=14
M=5

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/LDPE-wstar-c-scatterplot.png', type="png256", width=9, height=5, res=300, pointsize=14)
par(mar=c(4.5, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(Wstar1[1:K], Wstar2[1:K], pch=22, xlim=c(-0.6, 0.6), ylim=c(-0.6, 0.6), cex=2, xlab=paste("w", expression(c[1]), sep="*"), ylab=paste("w", expression(c[2]), sep="*"))
points(Wstar1[(K+1):(K+M)], Wstar2[(K+1):(K+M)], col="darkred", cex=2)
abline(h=0, v=0)
text(Wstar1[1:K], Wstar2[1:K], Variable[1:K], pos=4, col="black")
text(Wstar1[(K+1):(K+M)], Wstar2[(K+1):(K+M)], Variable[(K+1):(K+M)], pos=2, col="darkred")
dev.off()
