

set.seed(-92)

steps <- seq(0, 200)
N <- length(steps)

base.sd <- 3
base.mean <- 20
target <- base.mean

data <- rnorm(N, base.mean, base.sd)





# Now add a shift to the data
# ----------------------------
step.point <- 150
step.fraction <- 0.4
data.shift <- data
data.shift[step.point:N] <- data.shift[step.point:N] + step.fraction*base.sd


S.shift <- numeric(N)   # create a vector of zeros
S.shift[1] = data.shift[1] - target
for (k in 2:N)
{
   S.shift[k] <- S.shift[k-1] + data.shift[k] - target
}
plot(S.shift, type="l", cex.lab=1.5, cex.main=3, cex.sub=3, cex.axis=3, xlab="Time steps", ylab="", main="S(t)", ylim=range(S.shift))
abline(h=0)
x=100
d = 10
angle = 25
vert = 12.5
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]-angle, col="red", code=0, lwd=2)
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]+angle, col="red", code=0)
arrows(x0=x, y0=S.shift[x]-vert, x1=x, y1=S.shift[x]+vert, col="red", code=0)


x=170
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]-angle, col="red", code=0)
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]+angle, col="red", code=0)
arrows(x0=x, y0=S.shift[x]-vert, x1=x, y1=S.shift[x]+vert, col="red", code=0)
