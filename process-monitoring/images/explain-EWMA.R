# Use the same settings as "explain-CUSUM.R"
set.seed(-92)
steps <- seq(0, 200)
N <- length(steps)
base.sd <- 3
base.mean <- 20
target <- base.mean
data <- rnorm(N, base.mean, base.sd)

step.point <- 150
step.fraction <- 1
data[step.point:N] <- data[step.point:N] + step.fraction*base.sd


bitmap('/Users/kevindunn/transfer/Stats-course/Course notes/Control charts/images/explain-EWMA.png', type="png256", width=10, height=15, res=300, pointsize=14)

ewma <- function(x, lambda, target=x[1]){
    N <- length(x)
    y <- numeric(N)
    y[1] = target
    for (k in 2:N)
    {
        error = x[k-1] - y[k-1]
        y[k] = y[k-1] + lambda*error
    }
return(y)
}

m <- t(matrix(seq(1,5), 1, 5))
layout(m)

# Base case
LCL = base.mean-3*base.sd
UCL = base.mean+3*base.sd
plot(data, type="l", cex.lab=1.5, cex.main=2, cex.sub=2, cex.axis=2, xlab="", ylab="", main=(expression("Raw data")), ylim=c(LCL*0.95, UCL*1.05))
abline(h=base.mean, col="grey80")
lines(data)
# abline(h=LCL, col="red")
# abline(h=UCL, col="red")
abline(v=step.point, col="red")

lambda=0.8
LCL = base.mean-3*base.sd * sqrt(lambda/(2-lambda))
UCL = base.mean+3*base.sd * sqrt(lambda/(2-lambda))
plot(ewma(data, lambda=lambda, target=base.mean), type="l", ylim=c(LCL*0.90, UCL*1.10), xlab="", ylab="", main=(expression(paste("EWMA with "*lambda,' = ',0.8))), cex.lab=1.5, cex.main=2, cex.sub=2, cex.axis=2,)
abline(h=base.mean, col="grey80")
lines(ewma(data, lambda=lambda, target=base.mean))
abline(h=LCL, col="red")
abline(h=UCL, col="red")


lambda=0.4
c(LCL, UCL)
LCL = base.mean-3*base.sd * sqrt(lambda/(2-lambda))
UCL = base.mean+3*base.sd * sqrt(lambda/(2-lambda))
plot(ewma(data, lambda=lambda, target=base.mean), type="l", ylim=c(LCL*0.95, UCL*1.05), xlab="", ylab="", main=(expression(paste("EWMA with "*lambda,' = ',0.4))), cex.lab=1.5, cex.main=2, cex.sub=2, cex.axis=2,)
abline(h=base.mean, col="grey80")
lines(ewma(data, lambda=lambda, target=base.mean))
abline(h=LCL, col="red")
abline(h=UCL, col="red")

lambda=0.1
LCL = base.mean-3*base.sd * sqrt(lambda/(2-lambda))
UCL = base.mean+3*base.sd * sqrt(lambda/(2-lambda))
c(LCL, UCL)
plot(ewma(data, lambda=lambda, target=base.mean), type="l", ylim=c(LCL*0.90, UCL*1.10), xlab="", ylab="", main=(expression(paste("EWMA with "*lambda,' = ',0.1))), cex.lab=1.5, cex.main=2, cex.sub=2, cex.axis=2,)
abline(h=base.mean, col="grey80")
lines(ewma(data, lambda=lambda, target=base.mean))
abline(h=LCL, col="red")
abline(h=UCL, col="red")


S.shift <- numeric(N)   # create a vector of zeros
S.shift[1] = data[1] - target
for (k in 2:N)
{
   S.shift[k] <- S.shift[k-1] + data[k] - target
}
plot(S.shift, type="l", cex.lab=1.5, cex.main=2, cex.sub=2, cex.axis=2, xlab="Time steps", ylab="", main=(expression("CUSUM"))) #, ylim=c(-20, 120))
x=160
d = 10
angle = 30
vert = 15
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]-angle, col="red", code=0, lwd=2)
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]+angle, col="red", code=0, lwd=2)
arrows(x0=x, y0=S.shift[x]-vert, x1=x, y1=S.shift[x]+vert, col="red", code=0, lwd=2)


dev.off()