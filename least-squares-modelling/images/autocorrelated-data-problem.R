# Autocorrelated data
N = 1000
set.seed(50)
e <- numeric(N)
x <- numeric(N)

phi_x = 0.0
phi_e = 0.8
for (k in 2:N)
{
    e[k] = rnorm(1, sd=3) + phi_e*e[k-1]
    x[k] = rnorm(1, sd=3) + phi_x*x[k-1]
}
y <- 0.8*x+ e
model <- lm(y~x)
summary(model)


#bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/residual-pattern-unmodelled-dynamics.png', type="png256", width=14, height=9, res=300, pointsize=14)
# par(mar=c(4.2, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
# layout(matrix(c(1,2,3), 1, 3))
plot(y[1:(N-1)], y[2:N] )
plot(y, type='b',xlab="Sequence order", ylab="y", main="Time order of the y-variable")
plot(x, y, type="p", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Raw data with the calculated least squares model")
abline(model)
abline(a=0,b=1, col="red")

# plot(model$residuals, type="b", ylab="Residuals", xlab="Time order", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Residuals in time-order")
# abline(h=0)
# dev.off()

# Sub sample the data to avoid autocorrelated data
# CONFUSED: the subsampled model still gets the same slope coefficient, but with a weaker confidence interval
steps = seq(1,N,20)
ys <- y[steps]
xs <- x[steps]
model.s <- lm(ys ~ xs)
summary(model.s)
plot(ys[1:(N-1)], ys[2:N] )

plot(xs, ys, type="p", cex.lab=1.5, cex.main=1.2, cex.sub=1.8, cex.axis=1.8, main="Raw data with the calculated least squares model")
abline(model.s)
abline(model, col="red")


