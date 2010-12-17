# N=14
# set.seed(118)
# reactor = round(runif(N, min=0, max=1))
# sum(reactor)
# speed <- round(rnorm(N, mean=4000, sd=500)/100)*100
# temperature <- round(rnorm(N, mean=80, sd=10))
# duration <- numeric(N) + 260
# quality = round((0.01*speed - 0.5*temperature - 10*reactor) + 50 + rnorm(N)*3)
# 
# #plot(quality)
# #points(which(reactor==1), quality[reactor==1], pch=21, col="red", bg="red")
# 
# r <- data.frame(temperature, duration, speed, reactor, quality)
# write.csv(r, 'bioreactor-yields.csv', row.names=F)

#rm(list = ls())
bio <- read.csv('http://datasets.connectmv.com/file/bioreactor-yields.csv')
attach(bio)
summary(bio)
is.factor(baffles)
# [1] TRUE

model <- lm(yield ~ speed + baffles + temperature )
summary(model)
 
# Call:
# lm(formula = yield ~ speed + baffles + temperature)
# 
# Residuals:
#     Min      1Q  Median      3Q     Max 
# -5.5521 -3.2543 -0.4356  2.2953  8.1519 
# 
# Coefficients:
#              Estimate Std. Error t value Pr(>|t|)   
# (Intercept) 52.483652  18.421511   2.849  0.01728 * 
# speed        0.008711   0.003757   2.319  0.04288 * 
# bafflesYes  -9.090700   3.048811  -2.982  0.01377 * 
# temperature -0.470997   0.119242  -3.950  0.00273 **
# ---
# Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1 
# 
# Residual standard error: 4.651 on 10 degrees of freedom
# Multiple R-squared: 0.8659,   Adjusted R-squared: 0.8256 
# F-statistic: 21.52 on 3 and 10 DF,  p-value: 0.0001108 

# Calculate confidence intervals
confint(model)
#                     2.5 %      97.5 %
# (Intercept)  1.143797e+01 93.52933596
# speed        3.396812e-04  0.01708227
# bafflesYes  -1.588388e+01 -2.29752465
# temperature -7.366849e-01 -0.20530879

# Show a scatterplot matrix 
plot(bio)

# Computing the model's coefficients using inv(X' * X) * X' * y
X <- model.matrix(model)
XtX <- t(X) %*% X
Xty <- t(X) %*% yield
b = solve(XtX) %*% Xty
#                     [,1]
# (Intercept) 52.483652163
# speed        0.008710973
# bafflesYes  -9.090699955
# temperature -0.470996834