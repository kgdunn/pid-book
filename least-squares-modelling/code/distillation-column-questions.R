dist <- read.csv('http://stats4.eng.mcmaster.ca/datasets/distillation-tower.csv')
attach(dist)
model <- lm(VapourPressure ~ TempC2)
summary(model)

# From the above output
SE = sqrt(sum(resid(model)^2)/model$df.residual)
n = length(TempC2)
k = model$rank
x.new = data.frame(TempC2 = c(430, 480, 520))
x.bar = mean(TempC2)
x.variance = sum((TempC2-x.bar)^2)
var.y.hat = SE^2 * (1 + 1/n + (x.new-x.bar)^2/x.variance)
c.t = -qt(0.025, df=n-k)
y.hat = predict(model, newdata=x.new, int="p")
PI.LB = y.hat[,1] - c.t*sqrt(var.y.hat)
PI.UB = y.hat[,1] + c.t*sqrt(var.y.hat)

# Results from y.hat agree with PI.LB and PI.UB
y.hat
#        fit      lwr      upr
# 1 53.48817 47.50256 59.47379
# 2 36.92152 31.02247 42.82057
# 3 23.66819 17.71756 29.61883
y.hat[,3] - y.hat[,2]

bitmap('/Users/kevindunn/Statistics course/Course notes/Assignments/Assignment 5/images/distillation-prediction-interval.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 3.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(TempC2, VapourPressure, ylim = c(17, 65), main="Visualizing the prediction intervals")
abline(model, col="red")
library(gplots)
plotCI(x=c(430, 480, 520), y=y.hat[,1], li=y.hat[,2], ui=y.hat[,3], add=TRUE, col="red")
dev.off()

# Model with inverted temperature
model.inv <- lm(VapourPressure ~ I(1/TempC2))
summary(model.inv)

bitmap('/Users/kevindunn/Statistics course/Course notes/Assignments/Assignment 5/images/distillation-prediction-inverted-temperature.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5 )
plot(1/TempC2, VapourPressure, xlab="1/TempC2 [1/degF]", ylab="Vapour pressure [kPa]")
abline(model.inv, col="red")
lines(lowess(1/TempC2, VapourPressure), lty=2, col="red")
dev.off()


x.new = data.frame(TempC2 = c(430, 480, 520))
y.hat = predict(model.inv, newdata=x.new, int="p")
y.hat
#        fit      lwr      upr
# 1 54.98678 49.20604 60.76751
# 2 36.67978 30.99621 42.36334
# 3 24.56899 18.84305 30.29493

bitmap('/Users/kevindunn/Statistics course/Course notes/Assignments/Assignment 5/images/distillation-prediction-qqplots.png', type="png256", width=14, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 3.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
layout(matrix(c(1,2), 1, 2))
library(car)
qq.plot(model, main="Model with temperature", col=c(1, 1))
qq.plot(model.inv, main="Model with inverted temperature",col=c(1, 1))
dev.off()

# Training and testing
# ---------------------

# Poor choice
build = seq(1,n,2); test = seq(2,n,2)

# Better choice 
build = seq(1,159)  # sample 159 is the last sample for 2001
test = seq(160,n)   # first sample for 2002
 
model.sub <- lm(model, subset=build)
summary(model.sub)
confint(model.sub)
SE = sqrt(sum(resid(model.sub)^2)/model.sub$df.residual)

x.new = data.frame(TempC2 = TempC2[test])
y.hat = predict(model.sub, newdata=x.new)
y.actual = VapourPressure[test]
errors <- (y.actual - y.hat)
RMSEP <- sqrt(mean(errors^2))
c(RMSEP, SE)

# Find influential observations and remove them
#-----------------------------------------------
bitmap('/Users/kevindunn/Statistics course/Course notes/Assignments/Assignment 5/images/distillation-influence-plot.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
library(car)
influencePlot(model.sub, identify="auto")
dev.off()

remove = -c(38, 53, 84, 101)
model.update <- lm(model, subset=build[remove])
summary(model.update)
confint(model.update)
SE = sqrt(sum(resid(model.update)^2)/model.update$df.residual)
influencePlot(model.update, identify="auto")

y.hat = predict(model.update, newdata=x.new)
y.actual = VapourPressure[test]
errors <- (y.actual - y.hat)
RMSEP <- sqrt(mean(errors^2))
c(RMSEP, SE)