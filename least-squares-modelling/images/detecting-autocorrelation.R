# Autocorrelated data
N = 100
set.seed(52)
e <- numeric(N)
x <- numeric(N)

phi_x = 0.0
phi_e = 0.86
for (k in 2:N)
{
    e[k] = rnorm(1, sd=3) + phi_e*e[k-1]
}
x = rnorm(N, mean=10, sd=2)
y <- -3*x +50 + e
model <- lm(y~x)
summary(model)


bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/residual-pattern-unmodelled-dynamics.png', type="png256", width=14, height=14/3, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8 )
layout(matrix(c(1,2,3), 1, 3))
plot(y, type='b',xlab="Time order", ylab="y", main="Time order of the y-variable")
plot(x, y, type="p",  main="Raw data with the calculated least squares model")
abline(model)
plot(model$residuals, type="b", ylab="Residuals", xlab="Time order",main="Residuals in time-order")
abline(h=0)
dev.off()

# SLIDES
bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/residual-pattern-unmodelled-dynamics-slides.png', type="png256", width=14, height=14/2, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8 )
layout(matrix(c(1,2), 1, 2))
plot(x, y, type="p",  main="Raw data with the calculated least squares model")
abline(model)
plot(model$residuals, type="b", ylab="Residuals", xlab="Time order",main="Residuals in time-order")
abline(h=0)
dev.off()


# Use the CAR library to test it

library(car)
durbin.watson(model)


set.seed(56)


# NOTE: you should use longer time-series to estimate the ACF than those here


long <- numeric(N)
medium <- numeric(N)
negative <- numeric(N)

phi_long = 0.95
phi_medium = 0.3
phi_negative = -0.6
for (k in 2:N){
    long[k] = rnorm(1, sd=3) + phi_long*long[k-1]
    medium[k] = rnorm(1, sd=3) + phi_medium*medium[k-1]
    negative[k] = rnorm(1, sd=3) + phi_negative*negative[k-1]
}
bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/demonstrate-autocorrelation.png', type="png256", width=14, height=14/3*2, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 4.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.9, cex.sub=1.8, cex.axis=1.8 )
layout(matrix(c(1,2,3,4, 5, 6 ), 2, 3))
acf(long, main=expression(paste("Long autocorrelation: ", phi, " = 0.95")), ylab="")
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(long, type='b', ylab="")
abline(h=0, lty=2)

par(mar=c(4.2, 4.2, 4.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
acf(medium, main=expression(paste("Medium autocorrelation: ", phi, " = 0.3" )), ylab="")
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(medium, type='b', ylab="")
abline(h=0, lty=2)


par(mar=c(4.2, 4.2, 4.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
acf(negative, main=expression(paste("Negative autocorrelation: ", phi, " = -0.6" )), ylab="")
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(negative, type='b', ylab="")
abline(h=0, lty=2)


dev.off()