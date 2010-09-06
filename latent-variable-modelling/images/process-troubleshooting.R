rm <- read.csv('http://stats4.eng.mcmaster.ca/datasets/raw-materials-data-take-home.csv')
y <- as.numeric(as.factor(rm$Class))
X <- rm[,3:8]
library(car)
some(rm)

rm.pca <- prcomp(X, scale=TRUE)
rm.P <- rm.pca$rotation
rm.T <- rm.pca$x

rm.P
var(rm.T)
mean(rm[,3:8])
sd(rm[,3:8])

c1 = rm$Outcome == "Adequate"
c2 = rm$Outcome == "Poor"

bitmap('process-troubleshooting.png', type="png256", width=15, height=6.5, res=300, pointsize=14)
layout(matrix(c(1,2), 1, 2))
par(mar=c(4.5, 4.5, 4.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)

plot(rm.T[c1,1], rm.T[c1,2], col="darkgreen", pch=2, lwd=2, xlab=expression(t[1]), ylab=expression(t[2]), xlim=range(rm.T[,1]), ylim=range(rm.T[,2]), main="Score plot")
points(rm.T[c2,1], rm.T[c2,2], col="red", pch=1, lwd=2)
abline(h=0, v=0)
text(rm.T[c2,1], rm.T[c2,2], rownames(X)[c2], pos=1)
legend(x=1, y=-2.5, legend=c("Adequate yield", "Poor yield"), col=c("darkgreen", "red"), lty=c(0,0), pch=c(2, 1), lwd=c(2,2), cex=1.0)


p1max = max(abs(rm.P[,1]))*1.1
p2max = max(abs(rm.P[,2]))*1.1

plot(rm.P[,1], rm.P[,2], col="black", xlim=c(-p1max, p1max), ylim=c(-p2max, p2max),  xlab=expression(p[1]), ylab=expression(p[2]), main="Loadings plot")
text(rm.P[seq(1,5),1], rm.P[seq(1,5),2], colnames(X)[seq(1,5)], pos=3)
text(rm.P[6,1], rm.P[6,2], colnames(X)[6], pos=1)


abline(h=0, v=0)
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/unsupervised-classification-process.png', type="png256", width=15, height=15/2, res=300, pointsize=14)
layout(matrix(c(1,2), 1, 2))
par(mar=c(4.5, 4.5, 4.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)

plot(rm.T[c1,1], rm.T[c1,2], col="darkgreen", pch=2, lwd=2, xlab=expression(t[1]), ylab=expression(t[2]), xlim=range(rm.T[,1]), ylim=range(rm.T[,2]), main="Score plot")
points(rm.T[c2,1], rm.T[c2,2], col="darkred", pch=1, lwd=2)
abline(h=0, v=0)
legend(x=1, y=-2.5, legend=c("Adequate yield", "Poor yield"), col=c("darkgreen", "darkred"), lty=c(0,0), pch=c(2, 1), lwd=c(2,2), cex=1.0)

slope = 1/5
inter = 0.75
abline(a=0.75, 1/5, col="black", lwd=2)
x0=-2.5
y0=x0*slope+inter
c = y0-(-1/slope)*x0
x1=-2.8
arrows(x0=x0, y0=y0, x1=x1, y1=(-1/slope)*x1+c, angle=15, code=2, col="darkred")
text(-2.9, 2, "Poor region", col="darkred")

x0=-2.6
y0=x0*slope+inter
perp.slope = -1/slope
c = y0-(perp.slope)*x0
x1=-2.3
arrows(x0=x0, y0=y0, x1=x1, y1=(perp.slope)*x1+c, angle=15, code=2, col="darkgreen")
text(x1, -1.5, "Adequate region", col="darkgreen")
    
plot(rm.P[,1], rm.P[,2], col="black", xlim=c(-1,1), xlab=expression(p[1]), ylab=expression(p[2]), main="Loadings plot")
text(rm.P[1:5,1], rm.P[1:5,2], colnames(X[1:5]), pos=4)
text(rm.P[6,1], rm.P[6,2], colnames(X[6]), pos=1)

abline(h=0, v=0)

dev.off()


# > rm
#    Lot.number  Outcome Size5 Size10 Size15   TGA  DSC  TMA
# 1        B370 Adequate  13.8    9.2   41.2 787.3 18.0 65.0
# 2        B880 Adequate  11.2    5.8   27.6 772.2 17.7 68.8
# 3        B452 Adequate   9.9    5.8   28.3 602.3 18.3 50.7
# 4        B287 Adequate  10.4    4.0   24.7 677.9 17.7 56.5
# 5        B576 Adequate  12.3    9.3   22.0 593.5 19.5 52.0
# 6        B914     Poor  13.7    7.8   27.0 597.9 18.1 49.8
# 7        B404     Poor  15.5   10.7   34.3 668.5 19.6 55.7
# 8        B694     Poor  15.4   10.7   35.9 602.8 19.2 53.6
# 9        B875     Poor  14.9   11.3   41.0 614.6 18.5 50.0
# 10       B475 Adequate  13.7    8.5   28.0 700.4 18.0 57.0
# 11       B517     Poor  16.1   11.6   39.2 682.8 17.5 56.4
# 12       B296 Adequate  12.8    5.4   23.7 739.4 18.2 59.8
# 13       B403 Adequate  10.3    2.5   17.1 595.7 18.4 49.5
# 14       B430     Poor  12.9    9.7   36.3 642.4 19.1 55.0
# 15       B145 Adequate  13.0    7.3   27.0 682.8 19.1 55.3
# 16       B319 Adequate  11.7    5.2   20.2 655.8 19.2 56.3
# 17       B859 Adequate  10.7    6.8   27.7 661.2 18.3 55.5
# 18       B990 Adequate  13.0    5.4   25.3 701.9 19.1 61.0
# 19       B616 Adequate  11.9    7.2   29.8 661.0 18.5 55.4
# 20       B133 Adequate  11.3    7.9   30.0 699.9 18.1 58.1
# 21       B535 Adequate  11.1    4.5   24.8 576.3 19.5 51.6
# 22       B745     Poor  10.2    5.8   24.7 575.9 18.5     
# 23       B380 Adequate  11.4    4.8   26.5 636.0 18.6 58.2
# 24       B986 Adequate  10.7    4.8   26.5 726.7 19.2 58.4
# -----------------------------------------------------------
# MEAN                    12.4    7.2   28.7 660.6 18.6 55.6

rm.mean <- mean(rm[,3:8])
rm.sd   <- sd(rm[,3:8])

x.8 = (rm[8,3:8] - rm.mean)/rm.sd
x.8 * t(rm.P[,1])
x.8 * t(rm.P[,2])


x.22 = (rm[22,3:8] - rm.mean)/rm.sd
x.22 * t(rm.P[,2])

# > 
#      Size5     Size10     Size15        TGA        DSC        TMA 
#  
