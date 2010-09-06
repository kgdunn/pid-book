# Shows how a transformation of the x-data rectifies non-normality in the residuals

library(car)

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/non-normal-errors-transformation-required.png', type="png256", width=14, height=8, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
layout(matrix(c(1,2), 1, 2))

N = 100
set.seed(7)
basex <- rt(N, df=6)*2+7
basey <- 2*basex + 3/(basex) - 1*rnorm(N, sd=8)

x<-basex
y<-basey^2

#plot(x, y, main="Raw data")

model.base <- lm(y ~ x )
summary(model.base)
confint(model.base)
qq.plot(model.base, col=c(1,1,1), ylab="Residuals: y ~ x", main="Original data")

# remove = -c(38, 234, 235, 236)
# x <- x[remove]
# y <- y[remove]

model.rmoutliers <- lm(sqrt(y) ~ x)
summary(model.rmoutliers)
confint(model.rmoutliers)
qq.plot(model.rmoutliers, col=c(1,1,1), ylab="Residuals: sqrt(y) ~ x", main="Applying a square root transformation")

dev.off()

plot(model.rmoutliers$fitted.values, model.rmoutliers$residuals)

# The true effect of the log transformation is to worsen things.
# Actually the qq-plot of the log(residuals) looks OK, but once you take it to original $ units, 
# then you see it is worse

# bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/non-normal-errors-transformation.png', type="png256", width=14, height=9, res=300, pointsize=14)
# par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
# par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
# layout(matrix(c(1,2), 1, 2))
# 
# qq.plot(model.rmoutliers$residuals, col=c(1,1,1), ylab="Residuals: Price ~ Mileage", main="After removing 'outlier' cars")
# 
# pr<- log(Price)
# model.log <- lm(pr ~ Mileage )
# summary(model.log)
# confint(model.log)
# residuals <- exp(pr)-exp(predict(model.log))
# SE.log = sqrt(sum(residuals * residuals) / 792)
# SE.log
# qq.plot(residuals, col=c(1,1,1), ylab="Residuals: log(Price) ~ Mileage", main="Using a logarithmic transformation")
# 
# dev.off()
