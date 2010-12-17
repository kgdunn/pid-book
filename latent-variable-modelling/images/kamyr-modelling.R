kamyr <- read.csv('http://datasets.connectmv.com/file/kamyr-digester.csv')
cleaned <- na.omit(cbind(kamyr$Y.Kappa, kamyr$UCZAA))

bitmap('../images/kappa-number-autocorrelation.png', type="png256", width=14, height=14/2, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 4.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.9, cex.sub=1.8, cex.axis=1.8 )
layout(matrix(c(1,2), 1, 2))

acf(cleaned[,1], main="Autocorrelation function", ylab="")
#par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(cleaned[1:100,1], type='b', ylab="", main="Sample of the raw data")

dev.off()


attach(kamyr)
summary(lm(Y.Kappa ~ ChipRate))

N <- length(Y.Kappa)
summary(lm(Y.Kappa[1:(N-1)] ~ ChipRate[2:N]))

summary(lm(Y.Kappa[1:(N-2)] ~ ChipRate[3:N]))

model <- lm(Y.Kappa ~ ChipLevel4)
plot(Y.Kappa, predict(model))


Y.Kappa[1:N-2]


# These data are from Umetrics Simca-P 11.5, built a PLS with 10 lags + the actual X-variable (ChipRate), against Y=Kappa.  The ChipRate variable was unlagged to get it back to the raw
# data format.  Then the lags were applied.
lags <- read.csv('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/lags-x-y-kappa.csv')
bitmap('../images/plot-PLS-lags-x-y.png', type="png256", width=10, height=5.5, res=300, pointsize=14)
par(cex.lab=1.4, cex.main=1.4, cex.sub=1.4, cex.axis=1.4)
par(mar=c(4.5, 4.5, 0.8, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
barplot(lags$Value, ylim=c(-0.5, 0.4), col=0, names.arg=lags$Name, ylab="1st component weights for each lag", xlab="Lag number")
abline(h=0)
abline(v=13.3, col="red", lty=2)
text(13.9, 0.15,"Y (Kappa)",srt=90)
dev.off()
