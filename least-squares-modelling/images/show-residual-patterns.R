x <- seq(5, 10, 0.1)
N = length(x)

# Unmodelled structure
# ---------------------
set.seed(42)
y <- 0.4*x + exp(0.5*x) -2 + rnorm(N, sd=6)
model <- lm(y~x)

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/residual-pattern-forgottern-term.png', type="png256", width=14, height=9, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
layout(matrix(c(1,2), 1, 2))
plot(x, y, type="p", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Raw data with the calculated least squares model")
abline(a=model$coefficients[1], b=model$coefficients[2])

plot(model$fitted, model$residuals, ylab="Residuals", xlab="Fitted values (y-hat)", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Fitted values vs the residuals")
abline(h=0)
lines(lowess(model$fitted, model$residuals), col="red")
dev.off()


# Non-constant error
# ---------------------
set.seed(12)
x <- seq(5, 10, 0.1)
N = length(x)
y <- 20*x  
for (i in seq(N)){
    y[i] = y[i] + rt(1, df=5)*x[i]*5
}
model <- lm(y~x)
#summary(model)

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/residual-pattern-non-contant-error.png', type="png256", width=14, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
layout(matrix(c(1,2), 1, 2))
plot(x, y, type="p", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Raw data with the calculated least squares model")
abline(a=model$coefficients[1], b=model$coefficients[2])

plot(model$fitted, model$residuals, ylab="Residuals", xlab="Fitted values (y-hat)", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Fitted values vs the residuals")
abline(h=0)
#lines(lowess(model$fitted, model$residuals), col="red")
dev.off()


# Non-normal error structure
# ---------------------
set.seed(12)
x <- seq(-5, 5, 0.1)
y <- 5*x  -2 + rf(N, df1=6, df2=6)*2
model <- lm(y~x)
summary(model)
bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/residual-pattern-heavy-tails.png', type="png256", width=14, height=9, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
layout(matrix(c(1,2), 1, 2))
plot(x, y, type="p", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Raw data with the calculated least squares model")
abline(a=model$coefficients[1], b=model$coefficients[2])
library(car)
par(cex.main=1.2, cex.sub=1.8, cex.axis=1.8, cex.lab=1.5)
qq.plot(model$residuals, main="qq-plot of the residuals", ylab="Model residuals")
dev.off()

# Strong outliers
# ---------------------
set.seed(12)
x <- seq(-5, 5, 0.1)
y <- 5*x  -2 + rnorm(N)
x[5] = 32
model <- lm(y~x)
#bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/residual-strong-outliers.png', type="png256", width=14, height=9, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
layout(matrix(c(1,2), 1, 2))
plot(x, y, type="p", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Raw data with the calculated least squares model")
abline(a=model$coefficients[1], b=model$coefficients[2])

plot(model$fitted, model$residuals, ylab="Residuals", xlab="Fitted values (y-hat)", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Fitted values vs the residuals")
abline(h=0)
lines(lowess(model$fitted, model$residuals), col="red")
dev.off()



