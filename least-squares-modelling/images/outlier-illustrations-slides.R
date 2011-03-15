set.seed(41)
N = 25
x <- rnorm(N, sd=4, mean=10)
y <- x*4 - 6 + log(x) +rnorm(N, sd=3)

x[N+1] = mean(x[1:N])
y[N+1] = x*4 - 6 + log(x) +rnorm(1, sd=4) + 50


model1 <- lm(y~x)
model.rm <- lm(y[-N-1] ~ x[-N-1])
summary(model1)
summary(model.rm)


bitmap('influence-of-outliers-slide-1.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
plot(x[1:N], y[1:N], cex=1.5, lwd=2, xlab="x", ylab="y", xlim=c(min(x), max(x)+1), main="Model A")
points(x[N+1], y[N+1], pch=22, cex=1.5, lwd=4)

abline(coef(model1), lwd=2, lty=1)
abline(coef(model.rm), lwd=2, lty=2)
legend(x=10, y=20, legend=c("Model using all data", "Model omitting square point"), col=c("black", "black"), lty=c(1, 2), lwd=c(2, 2))
dev.off()

bitmap('influence-of-outliers-slide-2.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
x[N+1] = 25
y[N+1] = mean(y[1:N])
model2 <- lm(y~x)
plot(x[1:N], y[1:N], cex=1.5, lwd=2, xlab="x", ylab="y", xlim=c(min(x), x[N+1]), main="Model B")
points(x[N+1], y[N+1], pch=22, cex=1.5, lwd=4)
abline(coef(model2), lwd=2, lty=1)
abline(coef(model.rm), lwd=2, lty=2)

legend(x=10, y=20, legend=c("Model using all data", "Model omitting square point"), col=c("black", "black"), lty=c(1, 2), lwd=c(2, 2))
dev.off()

bitmap('influence-of-outliers-slide-3.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)

x[N+1] = 25
y[N+1] = predict.lm(model.rm, data.frame(x=x[N+1]))+rnorm(1, sd=20)
model3 <- lm(y~x)
plot(x[1:N], y[1:N], cex=1.5, lwd=2, xlab="x", ylab="y", xlim=c(min(x), x[N+1]), ylim=c(min(y), y[N+1]), main="Model C")
points(x[N+1], y[N+1], pch=22, cex=1.5, lwd=4)
abline(coef(model3), lwd=2, lty=1)
abline(coef(model.rm), lwd=2, lty=2)
legend(x=10, y=20, legend=c("Model using all data", "Model omitting square point"), col=c("black", "black"), lty=c(1, 2), lwd=c(2, 2))
dev.off()


bitmap('hatvalue-of-outliers-slides.png', type="png256", width=16, height=16/2, res=300, pointsize=14)
layout(matrix(c(1,2), 1, 2))
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)


hats1 <- hatvalues(model1)
hbar1 = (2)/(N+1)
hats3 <- hatvalues(model3)
hbar3 = (2)/(N+1)
 
plot(hats1[1:N], cex=1.5, lwd=2, xlab="Order of the x-data", ylab="Hat value", ylim=c(0,max(hats3)), xlim=c(0,N+1), main="Model A")   # Use the larger limit from "hats3"
points(N+1, hats1[N+1], pch=22, cex=1.5, lwd=4)

abline(h=hbar1*1, col="black", lwd=2, lty=2)
x=1
text(x, y=hbar1*1, expression(bar(h)), pos=1)
abline(h=hbar1*2, col="red", lwd=2, lty=2)
text(x, y=hbar1*2, expression(2 %*% bar(h)), pos=1)
abline(h=hbar1*3, col="red", lwd=3, lty=2)
text(x, y=hbar1*3, expression(3 %*% bar(h)), pos=1)

plot(hats3[1:N], cex=1.5, lwd=2, xlab="Order of the x-data", ylab="Hat value", ylim=c(0,max(hats3)), xlim=c(0,N+1), main="Model B and C (the same values)")
points(N+1, hats3[N+1], pch=22, cex=1.5, lwd=4)

abline(h=hbar3*1, col="black", lwd=2, lty=2)
x=1
text(x, y=hbar3*1, expression(bar(h)), pos=1)
abline(h=hbar3*2, col="red", lwd=2, lty=2)
text(x, y=hbar3*2, expression(2 %*% bar(h)), pos=1)
abline(h=hbar3*3, col="red", lwd=3, lty=2)
text(x, y=hbar3*3, expression(3 %*% bar(h)), pos=1)
dev.off()


bitmap('studentized-residuals-slides.png', type="png256", width=16, height=16/3, res=300, pointsize=14)
layout(matrix(c(1,2,3), 1, 3))
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)

rs1 <- rstudent(model1)
rs2 <- rstudent(model2)
rs3 <- rstudent(model3)

plot(rs1[1:N], cex=1.5, lwd=2, xlab="Order of the data", ylab="Studentized residuals", ylim=range(rs1), xlim=c(0,N+1), main="Model A")
points(N+1, rs1[N+1], pch=22, cex=1.5, lwd=5)

plot(rs2[1:N], cex=1.5, lwd=2, xlab="Order of the data", ylab="Studentized residuals", ylim=range(rs2), xlim=c(0,N+1), main="Model B")
points(N+1, rs2[N+1], pch=22, cex=1.5, lwd=5)

plot(rs3[1:N], cex=1.5, lwd=2, xlab="Order of the data", ylab="Studentized residuals", ylim=range(rs3), xlim=c(0,N+1), main="Model C")
points(N+1, rs3[N+1], pch=22, cex=1.5, lwd=5)

dev.off()


bitmap('cooks-distances-slides.png', type="png256", width=16, height=16/3, res=300, pointsize=14)
layout(matrix(c(1,2,3), 1, 3))
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)

cd1 <- cooks.distance(model1)
cd2 <- cooks.distance(model2)
cd3 <- cooks.distance(model3)
K=2
cutoff <- 4/(N-K)


plot(cd1[1:N], cex=1.5, lwd=2, xlab="Order of the data", ylab="Cook's distance", ylim=range(cd1), xlim=c(0,N+1), main="Model A")
points(N+1, cd1[N+1], pch=22, cex=1.5, lwd=4)
abline(h=cutoff, col="red", lwd=3, lty=2)
text(x, y=cutoff, "Cutoff", pos=3,cex=1.5)

plot(cd2[1:N], cex=1.5, lwd=2, xlab="Order of the data", ylab="Cook's distance", ylim=range(cd2), xlim=c(0,N+1), main="Model B")
points(N+1, cd2[N+1], pch=22, cex=1.5, lwd=4)
abline(h=cutoff, col="red", lwd=3, lty=2)
text(x, y=cutoff, "Cutoff", pos=3,cex=1.5)


plot(cd3[1:N], cex=1.5, lwd=2, xlab="Order of the data", ylab="Cook's distance", ylim=range(cd3), xlim=c(0,N+1), main="Model C")
points(N+1, cd3[N+1], pch=22, cex=1.5, lwd=4)
abline(h=cutoff, col="red", lwd=3, lty=2)
text(x, y=cutoff, "Cutoff", pos=3,cex=1.5)

dev.off()

library(car)
bitmap('influence-plots-slides.png', type="png256", width=16, height=16/3, res=300, pointsize=14)
layout(matrix(c(1,2,3), 1, 3))
par(mar=c(4.2, 5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.7, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)

influencePlot(model1, main="Model A")
influencePlot(model2, main="Model B")
influencePlot(model3, main="Model C")
dev.off()