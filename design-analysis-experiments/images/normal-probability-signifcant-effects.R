k = 4
n = 2^k - 1
index <- seq(1, n)
p <- (index - 0.5) / n
theoretical.quantity <- qnorm(p)


labels = c('A', 'B',    'C',   'D', 'AB',  'AC', 'AD',   'BC', 'BD',   'CD', 
            'ABC',  'ABD',  'ACD',  'BCD',  'ABCD')
b      = c( -4,  12, -1.125, -2.75,  0.5, 0.375,  0.0, -0.625, 2.25, -0.125, 
           -0.375,   0.25, -0.125, -0.375,  -0.125)
b.sort = sort(b)

plot(theoretical.quantity, b.sort)
qqline(b.sort)

# Or more simply: use the qq.plot function:
library(car)
par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
qq.plot(b, labels=labels, col=c(1,1), cex=1.5, lwd=2, pch=21, ylab="Effect", xlab="Normal quantiles")



# Now omit the terms and refit.  Actually we don't have to refit: the terms are the same, do to orthogonality of X!!
# Confirm it for yourself though:
library(BHH2)
f <- ffDesMatrix(4)
ff <- ffFullMatrix(f, x=c(1,2,3,4), 4)
y = c(71, 61, 90, 82, 68, 61, 87, 80, 61, 50, 89, 83, 59, 51, 85, 78)
XtX <- t(ff$Xa) %*% ff$Xa
Xty <- t(ff$Xa) %*% y
b = solve(XtX) %*% Xty

# Significant effects = [B, BD, D, A].  For example, I believe that effect C is also important
X <- ff$Xa[,c(1,2,3,5,10)]
XtX <- t(X) %*% X
Xty <- t(X) %*% y
b = solve(XtX) %*% Xty

# Calculate residuals
e = y - X %*% b

qq.plot(e)
k = length(b)  # parameters being fit here
df = length(y) - k
SE.model = sqrt(sum(e * e) / df)
SE.b.i = SE.model^2 / sum(X[,2]*X[,2])
ct = qt(0.975, df=df)
c(SE.model, SE.b.i, ct)

fit <- data.frame(fit=b)
fit$low <- b - ct * SE.b.i
fit$high <- b + ct * SE.b.i
fit