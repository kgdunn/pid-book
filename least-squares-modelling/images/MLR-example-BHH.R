
x1 = c(0.34, 0.34, 0.58, 1.26, 1.26, 1.82)
x2 = c(0.73, 0.73, 0.69, 0.97, 0.97, 0.46)
y =  c(5.75, 4.79, 5.44, 9.09, 8.59, 5.09)

# Case with orthogonal regressors
# mod <- lm(x2~x1)
# x2 <- mod$residuals


# x1 = c(1, 3, 4, 7, 9, 9)
# x2 = c(9, 9, 6, 3, 1, 2)
# y = c(3, 5, 6, 8, 7, 10)

n = length(x1)

x1 = x1 - mean(x1)
x2 = x2 - mean(x2)
y = y - mean(y)
x1
x2
y

#plot(x1,x2)
X <- matrix(cbind(x1, x2), n, 2)
XTX <- t(X) %*% X
XTy <- t(X) %*% y
XTX
cor(X)
XTy
Xinv <-solve(XTX) 
Xinv

model <- lm(y ~ x1 + x2)
summary(model)

SR = 1.33
p=2
n=6
alpha=0.10
qf(1-alpha,p,n-p)
SR* (1+p/(n-p) * qf(1-alpha,p,n-p))