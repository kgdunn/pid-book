library(boot)
attach(survival)

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/bootstrap-example.png', type="png256", width=15, height=7, res=300, pointsize=14)
layout(matrix(c(1,2), 1, 2))
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.5)
plot(dose, log(surv), xlab="Dosage [rads]", ylab="log(Survival percentage)")
text(dose[13], log(surv[13]), "Point 13", pos=2)

base.lm <- lm(log(survival$surv) ~ survival$dose)
summary(base.lm)
abline(coef(base.lm), lwd=3, col="blue")

base.lm.rm13 <- lm(log(survival$surv[-13]) ~ survival$dose[-13])
summary(base.lm.rm13)
abline(coef(base.lm.rm13), lwd=1, col="darkgreen")

legend(x=650, y=3, legend=c("OLS: all data", "OLS: all data except point 13"), col=c("blue", "darkgreen"), lty=c(1, 1), lwd=c(3,1))

# Regression confidence intervals
predictions <- base.lm$fitted
residuals <- base.lm$residuals

# Calculate the 3 standard errors
n = 14
den <- sum((dose - mean(dose)) * (dose - mean(dose)))
SE <- sqrt(sum(residuals^2) / (n-2))
SE.b1 <- sqrt(SE^2 / den)

# Confidence intervals for the least squares parameters
alpha = 0.95
b1 = coef(base.lm)[2]
t.critical = qt(1-(1-alpha)/2, df=(n-2))
b1.LB <- b1 - t.critical*SE.b1
b1.UB <- b1 + t.critical*SE.b1
c(b1.LB, b1.UB)




ls.fun <- function(data, i){
	# `i` contains the indices of the rows to use in the
	# least squares model
	print (i)
	d.subset <- data[i,]
	d.ols <- lm(log(d.subset$surv) ~ d.subset$dose)
	
	# Return just the slope coefficient
	return(coef(d.ols)[2])
}
set.seed(43)
library(boot)
data.boot <- boot(survival, ls.fun, R=1000)

library(MASS)
truehist(data.boot$t, col=0, xlab="Slope coefficient", ylab="Count [R = 1000]")
lines(density(data.boot$t))

ymax=250  #  I don't know how else to get "truehist" maximum value on the y-axis
segments(x0=coef(base.lm)[2], y0=0, y1 = ymax, col="blue", lwd=3)
segments(x0=coef(base.lm.rm13)[2], y0=0, y1 = ymax, col="darkgreen", lwd=1)
segments(x0=b1.LB, y0=0, y1 = ymax, col="red", lwd=2)
segments(x0=b1.UB, y0=0, y1 = ymax, col="red", lwd=2)

delta=0.0001
text(x=b1.LB-delta, y=ymax, "CI: lower bound", srt=90, pos=4)
text(x=b1.UB-delta, y=ymax, "CI: upper bound", srt=90, pos=4)
#text(x=coef(base.lm)[2]-0.0002, y=ymax, "Using all data", srt=90, pos=4)
text(x=coef(base.lm.rm13)[2]-delta, y=ymax, "Except point 13", srt=90, pos=4)

arrows(x0=b1.LB, x1=b1.UB, y0=50, y1=50, angle=15, length=0.15, col="red", code=3)
text(x=(b1.LB+b1.UB)/2, y=50, "Confidence interval", pos=1, col="red")
dev.off()



bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/bootstrap-example-slide1.png', type="png256", width=7, height=7, res=300, pointsize=14)
#layout(matrix(c(1,2), 1, 2))
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.5)
plot(dose, log(surv), xlab="Dosage [rads]", ylab="log(Survival percentage)")
text(dose[13], log(surv[13]), "Point 13", pos=2)
abline(coef(base.lm), lwd=3, col="blue")
abline(coef(base.lm.rm13), lwd=1, col="darkgreen")
legend(x=650, y=3, legend=c("OLS: all data", "OLS: all data except point 13"), col=c("blue", "darkgreen"), lty=c(1, 1), lwd=c(3,1))
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/bootstrap-example-slide2.png', type="png256", width=10, height=7, res=300, pointsize=14)
#layout(matrix(c(1,2), 1, 2))
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.5)
truehist(data.boot$t, col=0, xlab="Slope coefficient", ylab="Count [R = 1000]")
lines(density(data.boot$t))

ymax=250  #  I don't know how else to get "truehist" maximum value on the y-axis
segments(x0=coef(base.lm)[2], y0=0, y1 = ymax, col="blue", lwd=3)
segments(x0=coef(base.lm.rm13)[2], y0=0, y1 = ymax, col="darkgreen", lwd=1)
segments(x0=b1.LB, y0=0, y1 = ymax, col="red", lwd=2)
segments(x0=b1.UB, y0=0, y1 = ymax, col="red", lwd=2)

delta=0.0001
text(x=b1.LB-delta, y=ymax, "CI: lower bound", srt=90, pos=4)
text(x=b1.UB-delta, y=ymax, "CI: upper bound", srt=90, pos=4)
#text(x=coef(base.lm)[2]-0.0002, y=ymax, "Using all data", srt=90, pos=4)
text(x=coef(base.lm.rm13)[2]-delta, y=ymax, "Except point 13", srt=90, pos=4)

arrows(x0=b1.LB, x1=b1.UB, y0=50, y1=50, angle=15, length=0.15, col="red", code=3)
text(x=(b1.LB+b1.UB)/2, y=50, "Confidence interval", pos=1, col="red")
dev.off()