# Calcuations with R

distillation <- read.csv('http://datasets.connectmv.com/file/distillation-tower.csv')
model <- lm(distillation$VapourPressure ~ distillation$TempC2)
summary(model)

# Calculations by hand
# -----------------------

# Confidence level
alpha = 0.99

# Raw data
x <- distillation$TempC2
y <- distillation$VapourPressure
n = length(x)

# Some intermediate values
x.bar = mean(x)
y.bar = mean(y)
num <- sum((x - x.bar) * (y - y.bar))
den <- sum((x - x.bar) * (x - x.bar))

# Model coefficients
b1 <- num/den
b0 <- y.bar - b1 * x.bar
c(b0, b1)

# Model predictions and residuals, with their summary (IQR and median)
predictions <- b0 + x*b1
residuals <- y - predictions
summary(residuals)

# Calculate the 3 standard errors
SE <- sqrt(sum(residuals^2) / (n-2))
SE.b1 <- sqrt(SE^2 / den)
SE.b0 <- sqrt(SE^2 *(1/n + (x.bar^2)/den))
c(SE, SE.b0, SE.b1)

# Confidence intervals for the least squares parameters
z.b0 = b0/SE.b0
z.b1 = b1/SE.b1
c(z.b0, z.b1)
t.critical = qt(1-(1-alpha)/2, df=(n-2))
t.critical
b0.LB <- b0 - t.critical*SE.b0
b0.UB <- b0 + t.critical*SE.b0
b1.LB <- b1 - t.critical*SE.b1
b1.UB <- b1 + t.critical*SE.b1
c(b0.LB, b0.UB)
c(b1.LB, b1.UB)

# R2, TSS, RegSS, RSS, Adjusted R2
TSS <- sum((y - y.bar)^2)
RegSS <- sum((predictions-y.bar)^2)
RSS <- sum(residuals^2)
R2 <- RegSS/TSS
RSS.adj <- 1- (RSS/(n-2)) / (TSS/(n-1))
c(TSS, RegSS, RSS, R2, RSS.adj)

# Error bounds for y-hat
x.new = seq(min(x), max(x), diff(range(x))/100)
y.new = b0 + x.new*b1
error.delta <- t.critical*SE*sqrt(1+ 1/n + ((x.new-x.bar)^2)/den)

# Plot of the raw data, least squares line, prediction interval for yhat, 
# slope coefficient confidence interval range
bitmap('../images/distillation-least-squares.png', type="png256", width=9, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 2, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(x,y, cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="", 
          xlab="Temperature (TempC2)", ylab="VapourPressure")
grid(lwd=2)
points(x, y)
lines(x.new, y.new + error.delta, col="gray40", lty=3)
lines(x.new, y.new - error.delta, col="gray40", lty=3)

abline(a=b0, b=b1, col="red", lty=1, lwd=3)

# One extreme of the beta_1 slope CI
abline(a=(y.bar-b1.UB*x.bar), b=b1.UB, col="red", lty=2, lwd=1)  
# Other extreme of the beta_1 slope CI
abline(a=(y.bar-b1.LB*x.bar), b=b1.LB, col="red", lty=2, lwd=1)  
dev.off()