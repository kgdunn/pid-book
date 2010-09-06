cars <-read.csv('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/Readings/kuiper.csv')
attach(cars)
library(car)

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/non-normal-errors-outliers.png', type="png256", width=14, height=9, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
layout(matrix(c(1,2), 1, 2))

model.base <- lm(Price ~ Mileage)
summary(model.base)
confint(model.base)
remove = -seq(151,160)
qq.plot(model.base$residuals, col=c(1,1,1), ylab="Residuals: Price ~ Mileage", main="All data")

y=40000
text(-3.5,y,"Cadillac convertibles", pos=4, col="blue", cex=2)
arrows(1,y,2,y, col="blue", angle=15, length=0.25, lwd=2)

detach(cars)
cars <- cars[remove,]
attach(cars)

model.rmoutliers <- lm(Price ~ Mileage)
summary(model.rmoutliers)
confint(model.rmoutliers)
qq.plot(model.rmoutliers$residuals, col=c(1,1,1), ylab="Residuals: Price ~ Mileage", main="After removing 'outlier' cars")
dev.off()

# bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/non-normal-errors-outliers-slide-1.png', type="png256", width=7, height=7, res=300, pointsize=14)
# par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
# par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
# 
# qq.plot(model.base$residuals, col=c(1,1,1), ylab="Residuals: Price ~ Mileage", main="All data")
# 
# y=40000
# text(-1.5,y,"Cadillac convertibles", pos=4, col="blue")
# arrows(1,y,2,y, col="blue", angle=15, length=0.25)
# dev.off()
# 
# detach(cars)
# cars <- cars[remove,]
# attach(cars)
# 
# bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/non-normal-errors-outliers-slide-2.png', type="png256", width=7, height=7, res=300, pointsize=14)
# par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
# par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
# model.rmoutliers <- lm(Price ~ Mileage)
# summary(model.rmoutliers)
# confint(model.rmoutliers)
# qq.plot(model.rmoutliers$residuals, col=c(1,1,1), ylab="Residuals: Price ~ Mileage", main="After removing 'outlier' cars")
# dev.off()


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
