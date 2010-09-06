lags <- read.csv('lags-y-kappa-PLS.csv')

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/plot-PLS-lags.png', type="png256", width=10, height=5.5, res=300, pointsize=14)
par(cex.lab=1.4, cex.main=1.4, cex.sub=1.4, cex.axis=1.4)
par(mar=c(4.5, 4.5, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
barplot(lags$Value, ylim=c(-0.3, 0.9), col=0, names.arg=seq(1:20), ylab="1st component weights for each lag", xlab="Lag number")
abline(h=0)
dev.off()