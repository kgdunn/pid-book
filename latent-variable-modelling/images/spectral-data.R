spectra <- read.csv('http://datasets.connectmv.com/file/tablet-spectra.csv', header=FALSE)
K <- ncol(spectra)
spectra <- spectra[,2:K]
model.pca <- prcomp(spectra, scale=TRUE)
summary(model.pca)
spectra.P <- model.pca$rotation
spectra.T <- model.pca$x

# Baseline
spectra.mean <- apply(spectra, 2, mean, na.rm=TRUE)  # mean for each column
spectra.sd <- apply(spectra, 2, sd, na.rm=TRUE)      # sd for each column
 
# Remove the calculated mean (the statistic) from each column (margin=2)
# by using the subtract function (FUN argument)
spectra.mc <- sweep(spectra, 2, spectra.mean, FUN='-')
 
# Scale each column, by dividing through by the standard deviation
spectra.mcuv <- sweep(spectra.mc, 2, spectra.sd, FUN='/') 

# Baseline variance
spectra.X2 <- spectra.mcuv * spectra.mcuv

# A = 1
#------
a = 1
spectra.Xhat.a <- spectra.T[,seq(1,a)] %*% t(spectra.P[,seq(1,a)])
spectra.E <- spectra.mcuv - spectra.Xhat.a
spectra.E2 <- spectra.E * spectra.E
spectra.Xhat.a.2 <- spectra.Xhat.a * spectra.Xhat.a

SPE.1 <- sqrt(apply(spectra.E2, 1, sum))
R2.k.a <- apply(spectra.Xhat.a.2, 2, sum) / apply(spectra.X2, 2, sum)

bitmap('spectral-data-R2-per-variable.png', type="png256", width=15, height=6.6665, res=300, pointsize=14)
par(mar=c(4.5, 4.5, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=2, cex.main=2, cex.sub=2, cex.axis=2)
wavelengths=seq(600, 1898, 2)
plot(wavelengths, R2.k.a, col='darkgreen', type='l', lwd=a*2, ylim=c(0,1), ylab="R2 for each variable", xlab="Wavelengths")

# A = 2
#------
a = 2
spectra.Xhat.a <- spectra.T[,seq(1,a)] %*% t(spectra.P[,seq(1,a)])
spectra.E <- spectra.mcuv - spectra.Xhat.a
spectra.E2 <- spectra.E * spectra.E
spectra.Xhat.a.2 <- spectra.Xhat.a * spectra.Xhat.a

SPE.2 <- sqrt(apply(spectra.E2, 1, sum))
R2.k.a <- apply(spectra.Xhat.a.2, 2, sum) / apply(spectra.X2, 2, sum)

lines(wavelengths, R2.k.a, col='black', type='l', lwd=a*2)


# A = 2
#------
a = 3
spectra.Xhat.a <- spectra.T[,seq(1,a)] %*% t(spectra.P[,seq(1,a)])
spectra.E <- spectra.mcuv - spectra.Xhat.a
spectra.E2 <- spectra.E * spectra.E
spectra.Xhat.a.2 <- spectra.Xhat.a * spectra.Xhat.a

SPE.3 <- sqrt(apply(spectra.E2, 1, sum))
R2.k.a <- apply(spectra.Xhat.a.2, 2, sum) / apply(spectra.X2, 2, sum)

lines(wavelengths, R2.k.a, col='blue', type='l', lwd=a*2)

legend(x=650, y=0.35, legend=c("R2: 1st component", "R2: 2nd component", "R2: 3rd component"), col=c("darkgreen", "black", "blue"), lty=c(1, 1, 1), lwd=c(2,4,6), cex=2.0)
dev.off()

bitmap('spectral-data-SPE-per-tablet.png', type="png256", width=15, height=7, res=300, pointsize=14)
N <- dim(spectra)[1]
par(mar=c(2.5, 5.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=2, cex.main=2, cex.sub=2, cex.axis=2)
layout(matrix(c(1,2,3), 3, 1))
plot(seq(1,N), SPE.1, col='darkgreen', type='l', lwd=2,  ylab="SPE: A=1", ylim=c(0, max(SPE.1)))
plot(seq(1,N), SPE.2, col='black', type='l', lwd=2,  ylab="SPE: A=2", ylim=c(0, max(SPE.2)))
par(mar=c(4.5, 5.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=2, cex.main=1.8, cex.sub=1.5, cex.axis=2)
plot(seq(1,N), SPE.2, col='blue', type='l', lwd=2,  ylab="SPE: A=3", xlab="Tablet number", ylim=c(0, max(SPE.3)))
dev.off()


# Hotelling's T2, using A=3:
# --------------------------
T2 = 0
for (a in seq(1,3)){
    T2 = T2 + spectra.T[,a]*spectra.T[,a]/var(spectra.T[,a])
}
T2lim.95 = 7.90771
T2lim.99 = 11.5244
ellipse <- function(s_i, s_j, T2_limit) {
    # Confidence ellipse for score plots
    
    # Equation of an ellipse: (\frac{t_i}{s_i})^2 + (\frac{t_j}{s_j})^2 = T2_limit
    # where    s_i = stdT(i)
    #          s_j = stdT(j)
    #          T2_limit = confidence limit for T^2 at a set level of confidence, 95% in this case
    #
    # But, an ellipse can be given in parametric form by:  t_i = sqrt(T2_limit) * s_i * cos(t)
    #                                                      t_j = sqrt(T2_limit) * s_j * sin(t)
    #                                                  where t = lies between 0 and 2*Math.PI
    #
    # How to use it:   Specify t_i and then solve equation for t_j
    #                  t_i starts and ends where the ellipse intersects the domain-axis
    nEllipsePoints = 200
    constant_X = sqrt(T2_limit) * s_i
    constant_Y = sqrt(T2_limit) * s_j
    delta = (2*pi-0.0)/(nEllipsePoints-1)
    points = seq(nEllipsePoints)
    return( list(x=constant_X * cos(points*delta),  y=constant_Y * sin(points*delta)) )
}

bitmap('spectral-data-t1-t2-scoreplot.png', type="png256", width=10, height=6, res=300, pointsize=14)
par(mar=c(4.5, 4.5, 3.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=2, cex.main=1.5, cex.sub=2, cex.axis=1.8)
plot(spectra.T[,1], spectra.T[,2], xlim=c(-80, 70), ylim=c(-40,40), xlab=expression(t[1]), ylab=expression(t[2]), main="Score plot for tablet spectra")
lines(ellipse(sd(spectra.T[,1]), sd(spectra.T[,2]), T2lim.95), lty=2, col="darkgreen")
lines(ellipse(sd(spectra.T[,1]), sd(spectra.T[,2]), T2lim.99), lty=2, col="red")
abline(h=0, v=0)
dev.off()

bitmap('spectral-data-T2-lineplot.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.5, 4.5, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.5, cex.axis=1.5)
plot(T2, type="l", xlab="Tablet order", ylab="Hotelling's T2")
abline(h=T2lim.95, col="darkgreen", lty=2, lwd=2)
abline(h=T2lim.99, col="red", lty=2, lwd=2)
text(20,T2lim.95,"95% limit", pos=3, col="darkgreen")
text(20,T2lim.99,"99% limit", pos=3, col="red")
dev.off()

